import hashlib
import json
import queue
import socket
import threading
from urllib.request import Request, urlopen

from monitor_core import ReplayGuard, redact


def decode_event(data: list[str]) -> str | None:
    if not data:
        return None
    payload = json.loads("\n".join(data))
    if not isinstance(payload, dict) or not isinstance(payload.get("line"), str):
        raise ValueError("The endpoint returned an invalid Carbit log event.")
    if payload.get("file") != "zeta_log.txt":
        return None
    return payload["line"]


class StreamWorker(threading.Thread):
    def __init__(self, url: str, messages: queue.Queue, stop: threading.Event, timeout: float = 30):
        super().__init__(daemon=True, name="zeta-log-stream")
        self.url = url
        self.messages = messages
        self.stop_event = stop
        self.timeout = timeout
        self.guard = ReplayGuard()

    def emit(self, kind: str, value: str) -> None:
        while not self.stop_event.is_set():
            try:
                self.messages.put((kind, value), timeout=0.2)
                return
            except queue.Full:
                continue

    def read_stream(self) -> None:
        request = Request(self.url, headers={"Accept": "text/event-stream", "Cache-Control": "no-cache"})
        with urlopen(request, timeout=self.timeout) as response:
            if response.headers.get_content_type() != "text/event-stream":
                raise ValueError("The URL did not return a Carbit event stream.")
            self.guard.reconnect()
            self.emit("connected", "Live stream connected")
            data: list[str] = []
            event_size = 0
            while not self.stop_event.is_set():
                raw = response.readline(1_048_577)
                if not raw:
                    raise ConnectionError("The live-log stream closed without a confirmed result.")
                event_size += len(raw)
                if event_size > 1_048_576:
                    raise ValueError("A log event exceeded the 1 MB safety limit.")
                field = raw.decode("utf-8", errors="replace").rstrip("\r\n")
                if not field:
                    line = decode_event(data)
                    data = []
                    event_size = 0
                    if line is not None and self.guard.accept(hashlib.sha256(line.encode("utf-8")).digest()):
                        self.emit("line", line)
                elif field.startswith("data:"):
                    data.append(field[5:].removeprefix(" "))

    def run(self) -> None:
        delay = 2
        while not self.stop_event.is_set():
            try:
                self.read_stream()
            except (ValueError, json.JSONDecodeError) as error:
                self.emit("source_error", redact(str(error)))
                return
            except (socket.timeout, TimeoutError):
                self.emit("retry", "Stream idle; reconnecting to verify the source.")
            except OSError as error:
                self.emit("disconnected", redact(f"Log source unavailable: {error}"))
            if self.stop_event.wait(delay):
                return
            delay = min(delay * 2, 30)