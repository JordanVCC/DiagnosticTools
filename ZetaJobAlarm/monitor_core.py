from collections import deque
from dataclasses import dataclass
from datetime import datetime
import re
from urllib.parse import parse_qs, urlencode, urlsplit, urlunsplit


ANSI = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")
LEVEL = re.compile(r"\b(DEBUG|INFO|WARNING|WARN|ERROR|CRITICAL|SUCCESS)\b\s*(?:::|\||\]| -)")
RETURN_CODE = re.compile(r"^Run finished with return code\s+(-?\d+)\s*$", re.I)
RESULT_BANNER = re.compile(r"^\*{40}\s*(Success|Failed|Abort)\s*\*{40}$")
CONNECTION_FAILURE = re.compile(
    r"(?:failed to connect|could not connect|unable to connect|connection (?:failed|refused|timed out)|"
    r"(?:VCU|HPA|SSH).*?(?:unreachable|not reachable|timeout|timed out))", re.I
)


def redact(text: str) -> str:
    text = ANSI.sub("", text)
    text = re.sub(r"(https?://)[^\s/@]+:[^\s@]+@", r"\1[REDACTED]@", text)
    text = re.sub(r"(?i)(\b[\w-]*(?:token|secret|password|authorization|api_key)\b\s*[:=]\s*).*", r"\1[REDACTED]", text)
    return re.sub(r"\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+", "[REDACTED]", text)


def stream_url(value: str) -> str:
    parsed = urlsplit(value.strip())
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("Enter an HTTP or HTTPS live-log URL.")
    if parsed.username or parsed.password or parsed.fragment:
        raise ValueError("Credentials and fragments are not supported in the URL.")
    if parsed.path not in {"", "/", "/view", "/stream"}:
        raise ValueError("Use a Carbit /view or /stream URL.")
    file_name = parse_qs(parsed.query).get("file", ["zeta_log.txt"])[0]
    if file_name != "zeta_log.txt":
        raise ValueError("Monitor zeta_log.txt to detect the runner's final result.")
    return urlunsplit((parsed.scheme, parsed.netloc, "/stream", urlencode({"file": file_name}), ""))


def message_and_time(line: str, fallback: float) -> tuple[str, float, str]:
    line = ANSI.sub("", line)
    line = re.sub(r"^\[zeta_log\.txt\]\s?", "", line)
    timestamp = re.search(r"\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}", line)
    when = fallback
    stamp = ""
    if timestamp:
        stamp = timestamp.group()
        when = datetime.fromisoformat(stamp).timestamp()
    level = LEVEL.search(line)
    message = line
    if level:
        message = line[level.end():].strip()
        if "|" in message and "|" in line[:level.end()]:
            message = message.split("|", 1)[1].strip()
    return message.strip(), when, stamp


@dataclass(frozen=True)
class Event:
    status: str
    title: str
    detail: str
    alert: bool = False
    kind: str = "info"


class Detector:
    def __init__(self, retry_count: int = 3, retry_seconds: float = 60):
        self.retry_count = retry_count
        self.retry_seconds = retry_seconds
        self.status = "Running"
        self.terminal = False
        self.recent: deque[tuple[str, str]] = deque(maxlen=512)
        self.attempts: dict[str, deque[float]] = {}
        self.notified: set[str] = set()
        self.pending_error = False
        self.powered_off = False
        self.wake_deadline: float | None = None
        self.reset_iterations()

    def reset_iterations(self) -> None:
        self.iteration: int | None = None
        self.iteration_total: int | None = None
        self.iteration_base: int | None = None
        self.iteration_started: float | None = None
        self.iteration_seconds = 0.0
        self.iteration_samples = 0

    @property
    def average_iteration_seconds(self) -> float | None:
        return self.iteration_seconds / self.iteration_samples if self.iteration_samples else None

    @property
    def estimated_remaining_seconds(self) -> float | None:
        if self.terminal:
            return 0.0 if self.status == "Completed Successfully" else None
        average = self.average_iteration_seconds
        if average is None or self.iteration is None or self.iteration_total is None or self.iteration_base is None:
            return None
        remaining = self.iteration_total - (self.iteration - self.iteration_base)
        return average * remaining if remaining > 0 else None

    def track_iteration(self, message: str, when: float, stamp: str) -> list[Event]:
        if re.match(r"^Test Case #\d+:", message):
            self.reset_iterations()
        total = re.fullmatch(r"Number of standby cycles set to:\s*(\d+)", message, re.I)
        if total:
            self.iteration_total = int(total.group(1)) or None
        marker = re.fullmatch(r"#+\s*Iteration\s+(\d+)\s*#+", message, re.I)
        if not marker:
            return []
        index = int(marker.group(1))
        if index == self.iteration:
            return []
        if self.iteration is not None and index < self.iteration:
            total_count = self.iteration_total
            self.reset_iterations()
            self.iteration_total = total_count
        if self.iteration is None:
            self.iteration_base = 0 if index == 0 else 1
        if self.iteration is not None and index == self.iteration + 1 and stamp and self.iteration_started is not None:
            duration = when - self.iteration_started
            if duration > 0:
                self.iteration_seconds += duration
                self.iteration_samples += 1
        self.iteration = index
        self.iteration_started = when if stamp else None
        return [Event(self.status, f"Iteration {index} started", redact(message), kind="progress")]

    def connection_phase(self, message: str, when: float) -> bool:
        power_off = bool(re.fullmatch(r"VCU power off signal set", message, re.I))
        suspend = bool(re.match(r"LPA confirmed VCU suspend", message, re.I))
        wake = bool(re.fullmatch(r"VCU power on signal set", message, re.I) or re.search(r"TX: power wake vcu$", message, re.I))
        waiting = re.fullmatch(r"Waiting for VCU to become on \(timeout: (\d+(?:\.\d+)?)s\)\.\.\.", message, re.I)
        ready = bool(re.search(r"vcu_operation\.is_vcu_open\(\).*became True", message) or re.fullmatch(r"(?:Current platform state: '?Run'?|Platform state\s*:\s*Run)", message, re.I))
        if power_off or suspend or wake or waiting or ready:
            self.attempts.clear()
            self.notified.intersection_update({"critical"})
            if power_off or suspend:
                self.powered_off = True
                self.wake_deadline = None
            elif wake or waiting:
                self.powered_off = False
                self.wake_deadline = when + (float(waiting.group(1)) if waiting else self.retry_seconds)
            else:
                self.powered_off = False
                self.wake_deadline = None
        return self.powered_off or (self.wake_deadline is not None and when <= self.wake_deadline)

    def consume(self, line: str, now: float) -> list[Event]:
        message, when, stamp = message_and_time(line, now)
        identity = (stamp, message)
        if stamp and identity in self.recent:
            return []
        self.recent.append(identity)
        if self.terminal:
            return []
        terminal = RETURN_CODE.fullmatch(message)
        banner = RESULT_BANNER.fullmatch(message)
        if terminal or banner:
            code = int(terminal.group(1)) if terminal else None
            self.status = ("Completed Successfully" if code == 0 else "Failed") if terminal else {"Success": "Completed Successfully", "Failed": "Failed", "Abort": "Aborted"}[banner.group(1)]
            self.terminal = True
            detail = f"Execution ended with return code {code}." if terminal else "The runner reported its final execution result."
            return [Event(self.status, self.status, detail + " Artifact uploads may still be running.", True)]
        if message.startswith("Run failed with error:") or message.startswith("Abort detected at runtime") or message.startswith("Abort detected after HIL server startup"):
            self.status = "Failed" if message.startswith("Run failed") else "Aborted"
            self.terminal = True
            return [Event(self.status, self.status, redact(message), True)]
        events = self.track_iteration(message, when, stamp)
        expected_downtime = self.connection_phase(message, when)
        failed_connection = CONNECTION_FAILURE.search(message)
        if failed_connection and not expected_downtime:
            address = re.search(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", message)
            target = address.group() if address else ("VCU" if re.search(r"\bVCU\b", message, re.I) else "HPA" if re.search(r"\bHPA\b", message, re.I) else "SSH")
            attempts = self.attempts.setdefault(target, deque(maxlen=100))
            if attempts and when - attempts[-1] > max(120, self.retry_seconds * 2):
                attempts.clear()
                self.notified.discard(target)
            if not attempts or when - attempts[-1] >= 2:
                attempts.append(when)
            wake_expired = self.wake_deadline is not None and when > self.wake_deadline
            persistent = len(attempts) >= self.retry_count and attempts[-1] - attempts[0] >= self.retry_seconds
            if (wake_expired or persistent) and target not in self.notified:
                self.notified.add(target)
                self.status = "Needs Attention"
                evidence = "Connection failure after the VCU wake/startup deadline." if wake_expired else f"{len(attempts)} attempts spanning {attempts[-1] - attempts[0]:.0f}s."
                events.append(Event(self.status, f"Persistent connection problem: {target}", redact(f"{evidence} {message}"), True))
        elif re.search(r"(?:successfully connected|connection established|connected to)", message, re.I) and not re.search(r"disconnected|connected to vehicle", message, re.I):
            for target in list(self.attempts):
                if target.lower() in message.lower():
                    del self.attempts[target]
                    self.notified.discard(target)
        if "Traceback (most recent call last):" in message or re.search(r"\bCRITICAL\b", line):
            if "critical" not in self.notified:
                self.notified.add("critical")
                self.status = "Needs Attention"
                events.append(Event(self.status, "Execution exception or critical error", redact(message), True))
        is_error = bool(re.search(r"\bERROR\b\s*(?:::|\||\]| -)", ANSI.sub("", line)))
        if is_error:
            self.pending_error = bool(re.match(r"^\d{2}:\d{2}:\d{2}", message))
            if not self.pending_error:
                events.append(Event(self.status, "Error reported (outcome unconfirmed)", redact(message)))
        elif self.pending_error and message:
            self.pending_error = False
            events.append(Event(self.status, "Error reported (outcome unconfirmed)", redact(message)))
        else:
            success_level = bool(re.search(r"\bSUCCESS\b\s*(?:::|\||\])", ANSI.sub("", line)))
            success_message = bool(re.search(r"\b(?:success|successful|successfully)\b", message, re.I))
            readiness = bool(re.match(r"LPA confirmed VCU suspend", message) or re.search(r"vcu_operation\.is_vcu_open\(\).*became True", message))
            negative = bool(re.search(r"\b(?:not|never|no)\s+(?:a\s+)?success\w*\b", message, re.I))
            if (success_level or success_message or readiness) and not negative:
                events.append(Event(self.status, "Success reported", redact(message), kind="success"))
        return events


class ReplayGuard:
    def __init__(self):
        self.history: list[bytes] = []
        self.position = 0

    def reconnect(self) -> None:
        self.position = 0

    def accept(self, fingerprint: bytes) -> bool:
        if self.position < len(self.history):
            if self.history[self.position] != fingerprint:
                raise ValueError("Log content changed or rotated. Start monitoring again to select the current job.")
            self.position += 1
            return False
        if len(self.history) >= 1_000_000:
            raise ValueError("Log exceeded the one-million-line monitoring limit. Start a new monitor session.")
        self.history.append(fingerprint)
        self.position += 1
        return True