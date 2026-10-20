# Vehicle-Time Integrity Faults

## Scope and source

Investigate `kImageTimestampIntegrityFalse` or `Vehicle time integrity is 'false'`
from an exterior Camera Service (`ZFLC ----`, `ZSRC ----`, or `ZLRX ----`).
The two recurring signatures below come from engineering observations supplied for
this knowledge base. The example standby/resume backward jump has so far been
observed **only on SPA3 VCUs**, where the vehicle-time grand master moved to the zone
controller. Check for backward time movement on any platform, but do not
generalize that particular SPA3 mechanism to other platforms.

## Expected behavior

Camera Service can obtain valid vehicle time, and successive vehicle-time
readings remain consistent across a standby/suspend and resume cycle. A
`Self-healing` camera state describes the service response to a fault, not
the cause or confirmation that time is valid again.

## Investigation sequence

1. Start with the affected Camera Service filter. Confirm the timestamp-integrity
   warning and the exact camera fault and operation-state lines, with timestamps.
   This fault alone does not distinguish a fetch failure from a backward jump.
2. First extract `filters/supporting/vehicle-time-lgst.filter` (`LGST LGST`)
   separately. Compare successive `Current vehicle time` readings in record
   order for backward movement on **any** platform, even without a visible
   suspend/resume. If a standby/resume boundary is present, compare readings
   on both sides as well. A backward jump is the leading explanation for
   the Camera Service integrity fault, even if a time-fetch warning follows.
3. Then extract `filters/supporting/cfm.filter` (`ZCD1 ZCD1`) separately,
   regardless of whether a jump was found. Look for
   `failed on getVehicleSystemTime during fetch` in the incident window.
   This directly logs a MAX20087 power-switch driver's failed fetch, not a
   Camera Service fetch call. A backward jump can also produce this warning;
   the warning alone must not short-circuit the earlier time comparison.

Classify the result after both passes:

| Observations | Conclusion |
| --- | --- |
| Backward `Current vehicle time` jump, with or without a ZCD1 warning | Lead with the observed jump as the explanation for Camera Service's integrity fault; cite any ZCD1 warning as a concurrent consequence, not an alternative root cause. |
| No observed jump, Camera Service integrity fault and matching ZCD1 warning | Infer that Camera Service could not obtain valid vehicle time. Cite the ZCD1 fetch failure as corroboration, while noting it is not a direct Camera Service fetch log. |
| No comparable readings, Camera Service integrity fault and matching ZCD1 warning | Use the same fetch-failure conclusion, but explicitly state that a simultaneous backward jump cannot be ruled out from this capture. Do not claim time was monotonic. |
| Neither a jump nor a matching ZCD1 warning | Leave the mechanism inconclusive; absence of a ZCD1 warning does not prove fetching succeeded. |

These are focused supporting-source passes after Camera Service. If relative
timing cannot be established from separate passes, combine that Camera Service
source with **one** supporting source per pass; retain the ordinary mandatory
FLCW+DMS correlation pass when its failure criteria apply. `LGST LGST` is
distinct from Nvidia SLOG's `LGST SLOG`.

## Example signatures

**Fetch failure (`ZCD1 ZCD1`):**

```text
2026/09/18 23:50:43.408839 HPA ZCD1 ZCD1 log warn blocks/pd/max20087/src/power_switch_driver_csp.cpp:220: PowerSwitchDriver MAX20087 U121 (csp) failed on getVehicleSystemTime during fetch
```

**Backward jump across standby/resume (`LGST LGST`, observed on SPA3):**

```text
before suspend: Current vehicle time: 2000-01-01T03:36:55.484302Z, UTC time: 1970-01-01T00:32:28.171003Z
after resume:   Current vehicle time: 1970-01-01T00:00:09.364185Z, UTC time: 1970-01-01T00:00:30.756002Z
```

Compare the `Current vehicle time` field in record order, and the actual
suspend/resume boundary when available, not just DLT record timestamps or
the `UTC time` field. The examples are illustrative excerpts supplied by
an engineer, not evidence from every case.

## Reporting and limits

- Cite the Camera Service integrity fault and the ordered `LGST` readings
  when available; cite the `ZCD1` warning whenever present. If both appear,
  prioritize the jump, which can also lead to the fetch warning. Do not
  attribute the jump to a specific clock component without corroboration.
- If no jump is observed and ZCD1 warns, describe Camera Service's inability
  to obtain valid vehicle time as an inference from the concurrent fault
  and power-switch fetch failure, not as a directly logged Camera Service call.
- If ZCD1 has no matching warning and LGST has no comparable readings,
  request a capture including the relevant time producer and consecutive
  vehicle-time readings; the mechanism remains unresolved.
