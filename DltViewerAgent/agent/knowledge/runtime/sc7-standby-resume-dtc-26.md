# SC7 Standby/Resume DTC 26 Fault Tracing

## Scope

Fault-tracing guidance for camera DTCs reported during repeated standby/resume, also
called SC7, especially when BQ stability tests report exterior-camera DTCs with status
`26` after resume.

This page is project knowledge from the Confluence page `Standby Resume (aka SC7) DTC's
being set as 26`. A historical issue was fixed in REL13 where CPDD did not ignore the
first power-switch frames after resume, even though it ignored them during boot, after a
functional reset, or on first start.

For Camera Service vehicle-time integrity warnings across standby/resume, follow
`vehicle-time-integrity.md`; a backward vehicle-time jump is a separate signature
from the CPDD first-frames/DTC status issue described here.

## Normal Behavior

During BQ standby/resume stability testing, each standby/resume cycle should allow the
cameras to boot successfully after resume and should not leave camera DTCs set.

CPDD monitors the camera power-switch chip. During power-switch soft start, some fault
bits can be set transiently. CPDD is expected to avoid reporting those transient startup
or resume readings as real DTC failures.

## Failure Signature

The investigation starts when BQ or diagnostic test output reports camera DTCs during
standby/resume. In `carbit.debug.log`, look for camera DTC check failures such as:

```text
ERROR carbit:checks.py:362 {
 "2": [
 "D50911: 26 (General Electrical Failures Circuit short to ground)",
 "D50A11: 26 (General Electrical Failures Circuit short to ground)",
 "D50C11: 26 (General Electrical Failures Circuit short to ground)",
 "D50B11: 26 (General Electrical Failures Circuit short to ground)"
 ],
 "95": [
 "D50911: 26 (General Electrical Failures Circuit short to ground)",
 "D50A11: 26 (General Electrical Failures Circuit short to ground)",
 "D50C11: 26 (General Electrical Failures Circuit short to ground)",
 "D50B11: 26 (General Electrical Failures Circuit short to ground)"
 ]
}
```

This example says that SRCx DTCs were seen with status `26` on runs 2 and 95. Confirm
that the DTC appeared in standby/resume test cases, not during initial boot, before using
this SC7-specific reasoning.

## Diagnostic Status Interpretation

- Status `27` is more consistent with a real fault. If Camera Service also reports link
  lock issues or fails to boot, treat the evidence as a real camera or link fault unless
  disconfirmed.
- Status `26` during SC7 is more suspicious for the historical CPDD/resume behavior or a
  timing/data-race issue, especially when the DTC fails around suspend/resume and then
  passes again after the camera becomes operational.

## Evidence To Correlate

Use Diagnostics (`Diag DK--`) to confirm that DK received a `TestFailed` event for the
camera DTC. These logs contain DTCs from all applications on the node, so identify camera
events by the `ZenseactCameras...` event name and camera DTC ID.

```text
Handlers::SetEvent::ECU 0x1d12 reported status FAILED for event "ZenseactCamerasA::Z_SRCR_ShortToGround" (DTC 0xd50c11). Brief description: Event indicating that there is a Short To Ground event in CFM
```

Use CFM internal logs (`ZCD1 ZCD1`) to confirm that Camera Fault Monitor reported the
same DTC state transition internally:

```text
Camera DTC 0xD50C11 status changed (DEBUG): previous=Passed, current=Failed
```

If both DK and CFM messages are present for the same DTC and timestamp region, the
evidence supports that CFM reported the fault to DK. If the DTC should not have been
reported, continue the investigation in CFM and CPDD behavior rather than treating DK as
the first suspect.

If a DK `FAILED` message appears without the matching CFM status-change message, DK or
diagnostic state handling becomes more plausible, although a CFM issue is still not ruled
out.

## I2C Access Mode Clue

During affected SC7 cases, evidence may show I2C access mode switching `3 -> 0`, the DTC
reported as failed, I2C returning `0 -> 3`, and then the DTC reported as passed.

I2C mode is based on the camera operational state and timestamps provided by the camera;
it is not dependent on the current data value. Mode `0` can occur when CPDD cuts off I2C
access, including during suspend or after a startup fault. In the SC7 timing issue, mode
`0` is a symptom of camera suspension rather than the cause of the DTC.

The project hypothesis from the source discussion is a data race around suspend/resume:
the container may stop before CPDD detects a stale timestamp, or after resume CPDD may
still temporarily be in mode `3` before stale timestamp or operational-state information
reaches it. That can allow I2C reads or cached updates while the camera is not yet
operational.

Resetting selected CPDD caches/counters, or setting I2C mode to `0` from the container
suspend callback, were discussed as possible mitigations. Counters can be selected rather
than always resetting all counters, which matters for future power-cycle or go-to-service
logic.

## Reporting Guidance

- Start from the test summary or `carbit.debug.log` to identify the failing run numbers,
  affected DTCs, and status values (`26` or `27`).
- Confirm whether the failures occurred in standby/resume test cases rather than boot
  test cases; boot DTCs require a different investigation path.
- Extract Diagnostics (`Diag DK--`) to find `Handlers::SetEvent` camera DTC `FAILED` and
  `PASSED` transitions.
- Escalate to the CFM supporting source (`ZCD1 ZCD1`) when the question is whether CFM
  reported the fault to DK or whether DK created the DTC state without a CFM transition.
- Correlate DK, CFM, I2C mode, Camera Service state, and timestamps around suspend and
  resume. The strongest pattern for the SC7 timing hypothesis is: I2C `3 -> 0`, DTC
  failed, I2C `0 -> 3`, then DTC passed.
- Report status `26` during SC7 as suspicious for transient CPDD/resume timing only when
  the surrounding evidence supports it. Do not call it false solely from the status code.

## Caveats

- The REL13 fix covered a known CPDD first-frames-after-resume issue. Later SC7 DTCs can
  still be real faults or different regressions.
- Repeated functional resets can cause DK to read old state files and set DTCs without
  the CFM failed messages above. That behavior is known and may be avoided by clearing DK
  state files, but that workaround is not confirmed here.
- Do not treat `ZenseactCameras` events as the only DTCs in Diagnostics logs; they are the
  camera-specific subset within node-wide DK output.