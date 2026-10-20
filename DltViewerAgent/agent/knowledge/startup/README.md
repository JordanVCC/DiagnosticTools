# Startup Sequence Overview

## Scope

Use this document when investigating whether exterior-camera startup completed successfully. It describes the ordered phases and links to a detail document per phase.

## Phases, in order

1. **SIPL initialization** — platform-level, happens once (not per camera). See `01-sipl.md`.
2. **GPIO checks** — toggles GPIO pins on serializer/deserializer hardware after SIPL succeeds. Evaluated per camera or camera group (`SRCx`, `FLCW`, `LRxx`). See `02-gpio-checks.md`.
3. **Camera container initialization** — happens per camera, after the phases above. See `03-camera-container.md`.

## Reading the evidence

For a fully healthy startup, expect this pattern per case:

```text
Initializing SIPL
SIPL initialization successful!
Expected device block notification received
Initializing camera container for <camera>
Camera container initialization successful!
```

- GPIO checks occur after SIPL success. For `SRCx`, `Expected device block notification received` appears per camera in order (`SRCF` -> `SRCL` -> `SRCR` -> `SRCB`). For `FLCW` and `LRxx`, explicit `Calling AssertImagerSysCheck..` / `Calling AssertMax9295Errb..` calls precede the notification check.
- The camera container phase repeats once per relevant camera — see `knowledge/cameras.md` for valid camera names.

## Reporting guidance

- Confirm SIPL succeeded before treating any camera container failure as camera-specific — if SIPL never succeeded, no camera container should be expected to initialize.
- For GPIO check failures (`kDeviceBlockNotifErrorSerializerGpioTestFailure`), evaluate preceding success counts or explicit call context to identify the specific failing camera (see `02-gpio-checks.md`).
- If a camera container's "Initializing camera container for `<camera>`" line has no matching "Camera container initialization successful!" afterward, that camera failed to start; report it as an observed fact with any reported Fault Reason (`../fault-reasons.md`).
- Do not assume the same root cause across cameras. Report per-camera status explicitly (e.g. "SRCF, SRCL, SRCR succeeded; SRCB failed").

## Caveats

This document currently only describes the success path. Failure/error log formats for each phase are not yet confirmed and should not be assumed — add them here once verified against real evidence.
