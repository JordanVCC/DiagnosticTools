from pathlib import Path
import unittest

from monitor_core import Detector, ReplayGuard, redact, stream_url
from transport import decode_event


class DetectorTests(unittest.TestCase):
    def test_sample_is_not_complete(self):
        detector = Detector()
        alerts = []
        sample = Path(__file__).resolve().parents[1] / "Examples" / "ExampleLiveLog.txt"
        for line in sample.read_text(encoding="utf-8").splitlines():
            alerts.extend(event for event in detector.consume(line, 0) if event.alert and event.title.startswith("Persistent connection problem"))
        self.assertFalse(detector.terminal)
        self.assertEqual(alerts, [])

    def test_power_cycles_do_not_accumulate_109_second_outage(self):
        detector = Detector()
        sequence = [
            (0, "VCU power off signal set"),
            (4, "Failed to connect to HPA 169.254.4.10"),
            (12, "VCU power on signal set"),
            (15, "Failed to connect to HPA 169.254.4.10"),
            (49, "Platform state : Run"),
            (89, "LPA confirmed VCU suspend after 6.62 seconds"),
            (104, "[06:16:44] TX: power wake vcu"),
            (104, "Waiting for VCU to become on (timeout: 40s)..."),
            (107, "Failed to connect to HPA 169.254.4.10"),
            (113, "Failed to connect to HPA 169.254.4.10"),
            (118, "`vcu_operation.is_vcu_open()` became True after 14.06 seconds."),
            (125, "Platform state : Run"),
        ]
        for when, message in sequence:
            self.assertFalse(any(event.alert for event in detector.consume(message, when)), message)
        self.assertEqual(detector.attempts, {})

    def test_failure_beyond_wake_deadline_alerts(self):
        detector = Detector()
        detector.consume("Waiting for VCU to become on (timeout: 40s)...", 0)
        self.assertFalse(any(event.alert for event in detector.consume("Failed to connect to HPA", 39)))
        events = detector.consume("Failed to connect to HPA", 41)
        self.assertTrue(any(event.alert for event in events))
        self.assertIn("deadline", events[0].detail)
        self.assertFalse(detector.terminal)

    def test_doip_success_does_not_prove_ssh_recovery(self):
        detector = Detector()
        detector.consume("SSH connection failed: Unable to connect to port 22 on 169.254.4.10", 0)
        detector.consume("Successfully connected to vehicle TEST on IP 169.254.4.10", 10)
        self.assertIn("169.254.4.10", detector.attempts)

    def test_exact_terminal_markers(self):
        for code, status in [(0, "Completed Successfully"), (1, "Failed"), (-15, "Failed")]:
            detector = Detector()
            events = detector.consume(f"[INFO] 08:00:00 - runner.py:80", 0)
            events += detector.consume(f"  Run finished with return code {code}", 0)
            self.assertEqual(detector.status, status)
            self.assertTrue(events[-1].alert)
            self.assertEqual(detector.consume("Run finished with return code 0", 1), [])

    def test_partial_completion_is_not_terminal(self):
        detector = Detector()
        for line in ["HIL setup completed successfully", "All threads have completed.", "Hil server thread finished, proceeding with run", "No abort flag and no existing abort file, proceeding with job execution"]:
            detector.consume(line, 0)
        self.assertFalse(detector.terminal)

    def test_duplicate_retry_does_not_inflate_count(self):
        detector = Detector(retry_seconds=60)
        for second in [0, 30, 61]:
            minute, seconds = divmod(second, 60)
            stamp = f"2026-10-07 06:{minute:02d}:{seconds:02d}"
            events = detector.consume(f"{stamp}::ERROR   ::SSH connection failed: Unable to connect to port 22 on 169.254.4.10", 0)
            duplicate = detector.consume(f"{stamp} | ERROR | carbit | SSH connection failed: Unable to connect to port 22 on 169.254.4.10", 0)
            self.assertEqual(duplicate, [])
        self.assertTrue(any(event.alert for event in events))
        self.assertFalse(detector.terminal)
        self.assertFalse(any(event.alert for event in detector.consume("Failed to connect to HPA 169.254.4.10", 9999999999)))

    def test_generic_error_does_not_fail_job(self):
        detector = Detector()
        events = detector.consume("2026-10-07 06:00:00 | ERROR | carbit | Remote file not found", 0)
        self.assertEqual(detector.status, "Running")
        self.assertFalse(events[0].alert)

    def test_result_banners(self):
        for marker, status in [("Success", "Completed Successfully"), ("Failed", "Failed"), ("Abort", "Aborted")]:
            detector = Detector()
            self.assertTrue(detector.consume("*" * 40 + marker + "*" * 40, 0)[0].alert)
            self.assertEqual(detector.status, status)

    def test_old_retries_and_recovery(self):
        detector = Detector()
        detector.consume("Failed to connect to VCU", 0)
        detector.consume("Failed to connect to VCU", 30)
        self.assertFalse(any(event.alert for event in detector.consume("Failed to connect to VCU", 600)))
        detector.consume("Successfully connected to VCU", 610)
        self.assertNotIn("VCU", detector.attempts)

    def test_decode_event(self):
        self.assertEqual(decode_event(['{"file":"zeta_log.txt","line":"hello"}']), "hello")
        self.assertIsNone(decode_event(['{"file":"worker.log","line":"hello"}']))
        with self.assertRaises(ValueError):
            decode_event(['{"line":123}'])

    def test_successes_are_nonterminal_and_deduplicated(self):
        detector = Detector()
        first = detector.consume("2026-10-07 06:00:00::INFO ::HIL setup completed successfully", 0)
        self.assertEqual(first[0].kind, "success")
        self.assertFalse(first[0].alert)
        self.assertFalse(detector.terminal)
        self.assertEqual(detector.consume("2026-10-07 06:00:00 | INFO | carbit | HIL setup completed successfully", 0), [])
        for message in ["Operation was not successful", "Operation unsuccessful", "ERROR ::Command failed; earlier step successful"]:
            self.assertFalse(any(event.kind == "success" for event in detector.consume(message, 0)))
        events = detector.consume("2026-10-07 06:00:02 | SUCCESS | swut | Operation finished", 0)
        self.assertEqual(events[0].kind, "success")

    def test_iteration_average_uses_log_timestamps(self):
        detector = Detector()
        detector.consume("Number of standby cycles set to: 200", 0)
        for minute, index in [(0, 0), (2, 1), (5, 2)]:
            line = f"2026-10-07 06:{minute:02d}:00::INFO ::############# Iteration {index} #############"
            detector.consume(line, 9999999999)
            self.assertEqual(detector.consume(line, 9999999999), [])
        self.assertEqual(detector.iteration, 2)
        self.assertEqual(detector.iteration_total, 200)
        self.assertEqual(detector.iteration_samples, 2)
        self.assertEqual(detector.average_iteration_seconds, 150)
        detector.consume("Iteration 2 failed to suspend", 0)
        self.assertEqual(detector.iteration_samples, 2)

    def test_iteration_reset_gaps_and_missing_timestamps(self):
        detector = Detector()
        detector.consume("############# Iteration 0 #############", 0)
        detector.consume("############# Iteration 1 #############", 100)
        self.assertIsNone(detector.average_iteration_seconds)
        detector.consume("2026-10-07 06:00:00::INFO ::### Iteration 2 ###", 0)
        detector.consume("2026-10-07 06:05:00::INFO ::### Iteration 4 ###", 0)
        self.assertIsNone(detector.average_iteration_seconds)
        detector.consume("2026-10-07 06:08:00::INFO ::### Iteration 5 ###", 0)
        self.assertEqual(detector.average_iteration_seconds, 180)
        detector.consume("Test Case #2: Another test", 0)
        self.assertIsNone(detector.iteration)
        self.assertIsNone(detector.iteration_total)
        self.assertIsNone(detector.average_iteration_seconds)

    def test_iteration_number_restart_resets_average(self):
        detector = Detector()
        for minute, index in [(0, 0), (2, 1), (3, 0)]:
            detector.consume(f"2026-10-07 06:{minute:02d}:00::INFO ::### Iteration {index} ###", 0)
        self.assertEqual(detector.iteration, 0)
        self.assertEqual(detector.iteration_samples, 0)

    def test_remaining_estimate_includes_unfinished_iteration(self):
        for base in [0, 1]:
            detector = Detector()
            self.assertIsNone(detector.estimated_remaining_seconds)
            detector.consume("Number of standby cycles set to: 3", 0)
            for minute, offset in [(0, 0), (2, 1), (4, 2)]:
                detector.consume(f"2026-10-07 06:{minute:02d}:00::INFO ::### Iteration {base + offset} ###", 0)
                expected = None if offset == 0 else 120 * (3 - offset)
                self.assertEqual(detector.estimated_remaining_seconds, expected)
            detector.consume("Run finished with return code 0", 0)
            self.assertEqual(detector.estimated_remaining_seconds, 0)

    def test_remaining_unknown_without_total_or_after_failure(self):
        detector = Detector()
        for minute, index in [(0, 0), (2, 1)]:
            detector.consume(f"2026-10-07 06:{minute:02d}:00::INFO ::### Iteration {index} ###", 0)
        self.assertIsNone(detector.estimated_remaining_seconds)
        detector.consume("Number of standby cycles set to: 3", 0)
        self.assertEqual(detector.estimated_remaining_seconds, 240)
        detector.consume("Run finished with return code 1", 0)
        self.assertIsNone(detector.estimated_remaining_seconds)

    def test_remaining_resets_and_rejects_out_of_range_index(self):
        detector = Detector()
        detector.consume("Number of standby cycles set to: 2", 0)
        for minute, index in [(0, 0), (2, 1), (4, 2)]:
            detector.consume(f"2026-10-07 06:{minute:02d}:00::INFO ::### Iteration {index} ###", 0)
        self.assertIsNone(detector.estimated_remaining_seconds)
        detector.consume("Test Case #2: New test", 0)
        self.assertIsNone(detector.estimated_remaining_seconds)

    def test_fatal_and_abort(self):
        for line, status in [("Run failed with error: unavailable", "Failed"), ("Abort detected at runtime", "Aborted")]:
            detector = Detector()
            self.assertTrue(detector.consume(line, 0)[0].alert)
            self.assertEqual(detector.status, status)

    def test_url_and_redaction(self):
        self.assertEqual(stream_url("http://10.0.0.1:8766/view?file=zeta_log.txt"), "http://10.0.0.1:8766/stream?file=zeta_log.txt")
        for url in ["file:///tmp/log", "http://host/view?file=worker.log", "http://user:pass@host/view"]:
            with self.assertRaises(ValueError):
                stream_url(url)
        self.assertNotIn("private-value", redact("ARA_TOKEN: private-value"))
        self.assertNotIn("private-value", redact("https://user:private-value@host/path"))

    def test_reconnect_and_rotation(self):
        guard = ReplayGuard()
        self.assertTrue(guard.accept(b"first"))
        guard.reconnect()
        self.assertFalse(guard.accept(b"first"))
        self.assertTrue(guard.accept(b"second"))
        guard.reconnect()
        with self.assertRaises(ValueError):
            guard.accept(b"different-job")


if __name__ == "__main__":
    unittest.main()