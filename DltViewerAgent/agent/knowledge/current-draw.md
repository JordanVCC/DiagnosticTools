# Camera Current Draw

## Scope

Typical camera supply-current ranges by camera phase. Use this page when diagnostic
evidence includes camera power-switch output current, current draw, ADC current readings,
or questions about whether a camera appears off, powered, delinked, or streaming.

The values below are project knowledge from the Confluence page `Camera HW Notes`, sourced
from Andreas knowledge. Treat them as typical ranges, not exact electrical limits.

## Typical Current Ranges

| Phase / camera state | `FLCW` / `LRxx` | `SRCx` | `DMS` |
| --- | --- | --- | --- |
| Off | 0-9 mA | 0-9 mA | More than `FLCW` |
| Powered, not initialized | 20-40 mA | 20-40 mA | More than `FLCW` |
| Delinked | 20-40 mA | 20-40 mA | More than `FLCW` |
| Init successful / streaming | 100-120 mA | 60-80 mA | More than `FLCW` |

## Camera-Family Notes

- `FLCW` and `LRIx` use the same typical current ranges.
- `LRBx` uses the same typical current ranges as `FLCW` / `LRIx`, but has a different
  lens.
- `SRCx` streaming current is typically lower than `FLCW` / `LRxx` streaming current.
- `DMS` current is expected to be higher than `FLCW`; this page does not define exact
  DMS ranges.

## Reporting Guidance

- Compare current readings against the phase-specific ranges only after establishing the
  expected camera state from Camera Service or Diagnostics evidence.
- Use the diagnostic DID for camera power-switch output current in `diagnostics.md` when
  interpreting DID-based current evidence.
- Treat 20-40 mA as consistent with a powered but not initialized camera, or a delinked
  camera. Use link, startup, and fault evidence to distinguish between those states.
- Treat 100-120 mA for `FLCW` / `LRxx` and 60-80 mA for `SRCx` as typical streaming
  ranges, not proof by themselves that the camera pipeline is healthy.

## Caveats

- Current values can vary because of camera hardware variation and noise in the ADC
  reading.
- Do not report a fault from current draw alone. Correlate with Camera Service state,
  diagnostic DTC/DID data, device-block notifications, or relevant driver evidence.
- The DMS values are relative only (`More than FLCW`) in the source material, so do not
  invent numeric DMS thresholds.