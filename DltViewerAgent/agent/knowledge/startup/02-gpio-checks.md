# GPIO Checks

## Scope

Second phase of the exterior-camera startup sequence, occurring after SIPL initialization succeeds (`01-sipl.md`) and before camera container initialization (`03-camera-container.md`).

## Mechanism

Toggles GPIO pins on the serializer hardware and checks whether Nvidia reports the expected device block notification.

## Per-Camera Group Execution Rules

### 1. Short Range Cameras (SRCx)

SRCx cameras are checked sequentially in strict order:

1. `SRCF` (Front)
2. `SRCL` (Left)
3. `SRCR` (Right)
4. `SRCB` (Back)

Execution is **fail-fast**: if a camera's GPIO test fails, initialization stops immediately and subsequent cameras in the chain are not tested.

#### Log Patterns for SRCx

- **Success per camera:**
  `Expected device block notification received`
- **Failure on a camera:**
  `Failed to receive expected device block notification`
  `Initialization failed with fault reason: kDeviceBlockNotifErrorSerializerGpioTestFailure`

#### Deductive Rule for Identifying the Failing SRCx Camera

You can identify which camera failed by counting the number of `Expected device block notification received` lines preceding `Failed to receive expected device block notification`:

| Preceding Success Count | Failed Camera | Notes |
| --- | --- | --- |
| 0 | `SRCF` | Failed on 1st camera |
| 1 | `SRCL` | `SRCF` passed, `SRCL` failed |
| 2 | `SRCR` | `SRCF`, `SRCL` passed; `SRCR` failed |
| 3 | `SRCB` | `SRCF`, `SRCL`, `SRCR` passed; `SRCB` failed |

A minimized, redacted regression fixture at
`tests/fixtures/gpio-test-failure-srcb.txt` shows three successful notifications followed
by `Failed to receive expected device block notification` and
`kDeviceBlockNotifErrorSerializerGpioTestFailure`, identifying `SRCB` as the failing
camera. The fixture proves the sequence rule; it is not a complete production log.

---

### 2. Front Looking Centre Wide (FLCW)

FLCW is a single camera. Two explicit checks are declared in the DLT before performing the GPIO test:

1. `Calling AssertImagerSysCheck..`
2. `Calling AssertMax9295Errb..`

Followed by `Expected device block notification received` for success, or `Failed to receive expected device block notification` for failure.

---

### 3. Long Range Cameras (LRxx)

LRxx consists of 4 cameras checked sequentially in strict order:

1. `LRBR` (Back Right)
2. `LRBL` (Back Left)
3. `LRIR` (Intersection Right)
4. `LRIL` (Intersection Left)

Each LRxx camera performs the same explicit checks as FLCW (`Calling AssertImagerSysCheck..` and `Calling AssertMax9295Errb..`) in that order.

---

## Reporting Guidance

- Always report both the fault code (`kDeviceBlockNotifErrorSerializerGpioTestFailure`) and the specific camera name derived from the execution order / preceding success count or explicit log context.
- Distinguish between a platform-level SIPL failure (`01-sipl.md`) and a GPIO test failure. If SIPL succeeded, a GPIO test failure indicates a serializer/GPIO notification issue for a specific camera in the chain.
- Note if preceding cameras passed (e.g., "SRCF, SRCL, and SRCR GPIO checks succeeded; SRCB GPIO check failed").

## Caveats

- For SRCx, because evaluation is fail-fast, a failure on `SRCF` means `SRCL`, `SRCR`, and `SRCB` were not tested—do not report un-tested subsequent cameras as healthy or faulty.
