# DLT Log Sources

## Camera Service

Camera Service contains camera status, startup, and fault-related logs.

| Camera family | APP/CTX | Cameras |
| --- | --- | --- |
| FLCW | `ZFLC ----` | FLCW |
| SRCx | `ZSRC ----` | SRCF, SRCL, SRCR, SRCB |
| LRxx | `ZLRX ----` | LRBR, LRBL, LRIR, LRIL |

Start with only the matching Camera Service source.

## Supporting sources

| Source | APP/CTX | Diagnostic value |
| --- | --- | --- |
| Nvidia SLOG | `LGST SLOG` | Lower-level Nvidia/driver evidence |
| Vehicle-time readings | `LGST LGST` | Compare successive vehicle-time readings for a backward jump on any platform; not Nvidia SLOG |
| DMS | `DMS ----` | Interior-camera service; relevant to some FLCW issues because DMS and FLCW share a deserializer |
| Diagnostics | `Diag DK--` | DTC state and camera diagnostic failures |
| CFM / power-switch time fetch | `ZCD1 ZCD1` | Camera Fault Monitor DTC state transitions or explicit `getVehicleSystemTime` fetch failure |
| Execution Manager | `EXMN ----` | Final-resort application lifecycle and state evidence |

## Staged extraction

Do not extract every source together. Start with one Camera Service family. When that
evidence leaves a specific question unresolved, add one supporting source:

1. Diagnostics for camera DTC confirmation.
2. CFM when DK Diagnostics shows a camera DTC and the question is whether Camera Fault
  Monitor reported the state transition.
3. Nvidia SLOG for lower-level driver evidence.
4. DMS after any confirmed FLCW initialization or runtime failure.
5. Execution Manager only after all other relevant supporting sources are inconclusive
   and application lifecycle remains unresolved.

For a Camera Service vehicle-time integrity fault, check `LGST LGST` first
for backward `Current vehicle time` movement, even without standby/resume.
Use the separate reviewed `filters/supporting/vehicle-time-lgst.filter`,
not `LGST SLOG`. Then check `ZCD1 ZCD1` for
`failed on getVehicleSystemTime during fetch`, even if a jump is found or
there is no DK DTC. A jump takes precedence when both occur; see
`runtime/vehicle-time-integrity.md` for classification when readings are
missing.

Extract a supporting source separately unless its relative timing with Camera Service
evidence matters. A combined extraction scans the capture once and preserves chronological
interleaving; it is valuable for correlation but produces more ASCII evidence.

DMS produces substantial output, so do not include it in the initial FLCW pass. If that
pass confirms an FLCW failure, however, a DMS correlation pass is mandatory even when
the failure occurred during SIPL or container initialization. DMS can disturb the shared
MAX96712 before FLCW finishes initialization, so limiting this check to runtime failures
can omit the event that establishes precedence.

A confirmed failure includes failed SIPL or container initialization, GPIO/device-block
failure, deactivation, or a reported runtime fault. Always extract FLCW
(`filters/camera-service/flcw.filter`) and DMS (`filters/supporting/dms.filter`)
**together** in a single extraction pass:

```bash
scripts/extract-evidence.sh workspace/<case-id> \
  filters/camera-service/flcw.filter \
  filters/supporting/dms.filter
```

Extracting FLCW and DMS together merges both sources into a single chronologically
interleaved timeline (`filtered.txt`). Check DMS serializer and deserializer activity
before, during, and after the FLCW failure to determine event precedence. Do not extract
DMS in isolation. A preceding DMS event supports a shared-deserializer interference
hypothesis, but timing alone does not prove DMS is the root cause.

## Diagnostics (DTC) Log Reduction

Diagnostics logs (`Diag DK--`) capture ECU-wide DTC events across all vehicle systems. To minimize line volume and processing overhead when checking camera diagnostics:

- Camera DTC events in `Diag DK--` logs are prefixed with `ZenseactCameras` (e.g. `ZenseactCamerasA`, `ZenseactCamerasB`) and `ZenseactVision` (e.g. `ZenseactVisionCalibrationFLCW`, `ZenseactVisionCalibrationSenseA`, `ZenseactVisionCalibrationSenseB`).
- Post-filtering `filtered.txt` or `Diag DK--` output for `"ZenseactCameras"` (or `grep -E "ZenseactCameras|ZenseactVision"`) isolates camera-specific DTC events, eliminating generic ECU configuration and non-camera event noise.

## Execution Manager application names

| Camera service | Application name |
| --- | --- |
| FLCW | `zen_camera_flcw` |
| SRCx | `zen_camera_srcx` |
| LRxx | `zen_camera_lrbx` |

`zen_camera_lrbx` is a legacy LRxx name from before LRIX was introduced. It may later be
renamed to `zen_camera_lrxx`.

Do not consult Execution Manager merely to confirm an explanation already supported by
Camera Service, Diagnostics, Nvidia SLOG, or relevant DMS evidence.
