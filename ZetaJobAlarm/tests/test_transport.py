import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import queue
import threading
import time
import unittest

from monitor_core import Detector
from transport import StreamWorker


class StreamIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.payloads = ["Preparing run", "Run finished with return code 0"]
        self.content_type = "text/event-stream"
        self.raw_payload = None
        test = self

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.send_header("Content-Type", test.content_type)
                self.end_headers()
                if test.content_type != "text/event-stream":
                    return
                frames = []
                for line in test.payloads:
                    data = test.raw_payload or json.dumps({"file": "zeta_log.txt", "line": line})
                    frames.append(f": comment\r\ndata: {data}\r\n\r\n")
                try:
                    self.wfile.write("".join(frames).encode())
                    self.wfile.flush()
                except OSError:
                    return

            def log_message(self, *_args):
                pass

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.server.daemon_threads = True
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.messages = queue.Queue(maxsize=10)
        self.stop = threading.Event()
        self.worker = StreamWorker(f"http://127.0.0.1:{self.server.server_port}/stream?file=zeta_log.txt", self.messages, self.stop, timeout=1)

    def tearDown(self):
        self.stop.set()
        if self.worker.is_alive():
            self.worker.join(timeout=3)
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=3)

    def test_sse_delivery_completion_and_replay(self):
        self.worker.start()
        detector = Detector()
        received = []
        while True:
            kind, value = self.messages.get(timeout=5)
            if kind == "line":
                received.append(value)
                detector.consume(value, time.time())
            if kind == "disconnected":
                break
        self.assertEqual(received, self.payloads)
        self.assertEqual(detector.status, "Completed Successfully")
        self.assertEqual(self.messages.get(timeout=5)[0], "connected")
        self.assertEqual(self.messages.get(timeout=5)[0], "disconnected")

    def test_invalid_content_type_stops(self):
        self.content_type = "text/html"
        self.worker.start()
        kind, value = self.messages.get(timeout=5)
        self.assertEqual(kind, "source_error")
        self.assertIn("event stream", value)

    def test_invalid_json_stops(self):
        self.raw_payload = "not-json"
        self.worker.start()
        self.assertEqual(self.messages.get(timeout=5)[0], "connected")
        self.assertEqual(self.messages.get(timeout=5)[0], "source_error")


if __name__ == "__main__":
    unittest.main()