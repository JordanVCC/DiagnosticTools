import tkinter as tk
import unittest

from app import AlarmApp
from monitor_core import Event


class DesktopTests(unittest.TestCase):
    def setUp(self):
        try:
            self.root = tk.Tk()
        except tk.TclError as error:
            self.skipTest(str(error))
        self.root.withdraw()
        self.app = AlarmApp(self.root)
        self.app.sound.set(False)
        self.app.toasts.set(False)
        self.app.focus.set(False)

    def tearDown(self):
        self.app.stop_event.set()
        self.root.destroy()

    def test_alert_persists_until_acknowledged(self):
        self.app.record(Event("Needs Attention", "Blocking warning", "Evidence", True))
        self.app.record(Event("Running", "Ordinary error", "Recoverable"))
        self.assertEqual(self.app.status.get(), "Needs Attention")
        self.assertTrue(self.app.unacknowledged)
        self.app.acknowledge()
        self.assertFalse(self.app.unacknowledged)

    def test_terminal_result_stops_monitoring(self):
        self.assertTrue(self.app.prepare())
        self.app.process_line("Run finished with return code 0")
        self.app.flush_log()
        self.assertFalse(self.app.active)
        self.assertTrue(self.app.stop_event.is_set())
        self.assertTrue(self.app.unacknowledged)
        self.assertEqual(self.app.status.get(), "Completed Successfully")
        self.assertGreater(self.app.ended, 0)

    def test_batched_log_is_redacted_and_bounded(self):
        self.app.pending_log = ["Ordinary line"] * 5500
        self.app.flush_log()
        self.assertLessEqual(int(self.app.log.index("end-1c").split(".")[0]), 5001)
        self.app.process_line("ARA_TOKEN: private-value")
        self.app.flush_log()
        visible = self.app.log.get("1.0", "end")
        self.assertIn("[REDACTED]", visible)
        self.assertNotIn("private-value", visible)

    def test_silence_is_not_completion(self):
        self.app.prepare()
        self.app.last_output -= self.app.stall_limit + 1
        self.app.tick()
        self.assertEqual(self.app.status.get(), "Needs Attention")
        self.assertFalse(self.app.detector.terminal)
        self.assertTrue(self.app.active)

    def test_success_row_is_green_without_clearing_attention(self):
        self.app.record(Event("Needs Attention", "Warning", "Original evidence", True))
        self.app.process_line("2026-10-07 06:00:00::INFO ::HIL setup completed successfully")
        item = self.app.event_view.get_children()[-1]
        self.assertIn("success", self.app.event_view.item(item, "tags"))
        self.assertEqual(self.app.events[-1]["kind"], "success")
        self.assertEqual(self.app.status.get(), "Needs Attention")
        self.assertEqual(self.app.detail.get(), "Original evidence")
        self.assertTrue(self.app.unacknowledged)

    def test_iteration_progress_and_reset(self):
        self.app.process_line("Number of standby cycles set to: 200")
        self.app.process_line("2026-10-07 06:00:00::INFO ::### Iteration 0 ###")
        self.assertIn("Iteration 1 / 200 (log #0)", self.app.progress.get())
        self.assertIn("Avg / iteration --", self.app.progress.get())
        self.app.process_line("2026-10-07 06:03:00::INFO ::### Iteration 1 ###")
        self.assertIn("Iteration 2 / 200 (log #1)", self.app.progress.get())
        self.assertIn("3m 00s (1 measured)", self.app.progress.get())
        self.assertIn("Est. remaining 9h 57m 00s", self.app.progress.get())
        self.assertFalse(self.app.unacknowledged)
        self.app.prepare()
        self.assertEqual(self.app.progress.get(), "Iteration --   |   Avg / iteration --   |   Est. remaining --")


if __name__ == "__main__":
    unittest.main()