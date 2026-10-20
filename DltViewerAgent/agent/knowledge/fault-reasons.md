# Fault Reasons and Categories

## Scope

Guide to Fault Reason values reported during initialization, runtime, frame degradation,
temperature handling, and vehicle-time processing, such as:

```text
Initialization failed with fault reason: <fault code>
```

Fault Reasons are application-defined identifiers starting with `k` followed by PascalCase
words (for example, `kDeviceBlockNotifErrorSerializerGpioTestFailure`).

## Master Tables

The authoritative master mappings are stored in structured CSV files under `knowledge/tables/`:

1. **`knowledge/tables/CS_Fault_Reasons_Mapping.csv`**
   Maps each Fault Reason (`k...`) to:
   - **FR Description**: Detailed explanation of the fault trigger.
   - **Needs HPA Restart / SC7 to Recover**: `YES` (hard restart required) or `NO` (self-healing / cooldown).
   - **Camera Service Status**: Impact on camera service (`Deactivated`, `SelfHealing`, `Cooldown`, etc.).
   - **CFM DTC**: Phase/DTC code classification (e.g. `init_phase (xxxx93)`, `runtime_phase (xxxx96)`, `frame_degradation (xxxx92)`).
   - **CFM Fault Category**: High-level fault category `k...`.

2. **`knowledge/tables/CFM_Fault_Categories.csv`**
   Defines descriptions for each high-level CFM Fault Category (e.g. `kSerializerGpioTestFault`, `kDeserializerFault`, `kInitializationAndStartupFault`, `kLinkLockFault`).

Fault Reasons and categories evolve over time: values may be introduced or deprecated.
When an approved newer mapping is available, replace the CSV files and review this guide
for stale quick-reference entries. Treat the CSV content as versioned knowledge, not an
exhaustive permanent enum.

For camera DTC prefixes and diagnostic DTC suffix composition, see `diagnostics.md`.
That page covers diagnostic suffixes and DIDs only and does not define calibration
suffixes or calibration DIDs.

## Common initialization Fault Reasons

Below are key startup and initialization fault reasons from the mapping table:

| Fault Reason (FR) | Description | Needs HPA Restart | Camera Service Status | CFM Fault Category |
| --- | --- | --- | --- | --- |
| `kDeviceBlockNotifErrorSerializerGpioTestFailure` | Triggering the serializer pin does not result in expected notification | YES | Deactivated | `kSerializerGpioTestFault` |
| `kDeviceBlockNotifErrorSensorGpioTestFailure` | Triggering the sensor pin does not result in expected notification | YES | Deactivated | `kSensorGpioTestFault` |
| `kDeviceBlockNotifErrorGpioTestSerializerFaultInjectionFailure` | Call to trigger serializer pin fails | YES | Deactivated | `kLinkLockFault` |
| `kDeviceBlockNotifErrorGpioTestSensorFaultInjectionFailure` | Call to trigger sensor pin fails | YES | Deactivated | `kLinkLockFault` |
| `kSiplCameraInit` | Failed to initialize camera | YES | Deactivated | `kInitializationAndStartupFault` |
| `kSiplCameraStart` | Failed to start the camera stream | YES | Deactivated | `kInitializationAndStartupFault` |
| `kInitTimeout` | I/O timeout when initializing camera service | YES | Deactivated | `kSystemFault` |
| `kEepromIntegrityError` | EEPROM data integrity check failed or unsupported camera revision | YES | Deactivated | `kEepromDataIntegrityCheckFault` |
| `kReadEeprom` | Failed to read EEPROM | YES | Deactivated | `kEepromReadFault` |
| `kDeviceBlockNotifErrorDeserializerFailure` | Device block event indicating deserializer failure | NO | SelfHealing | `kDeserializerFault` |

## Reporting Guidance

- Always quote the exact Fault Reason `k...` from the evidence log line.
- Look up the fault reason in `knowledge/tables/CS_Fault_Reasons_Mapping.csv` to report:
  1. Human-readable description.
  2. Severity / recovery impact (whether HPA restart / SC7 is required vs SelfHealing/Cooldown).
  3. Camera Service Status (`Deactivated` vs `SelfHealing`).
  4. High-level CFM Fault Category and DTC phase (`init_phase`, `runtime_phase`, `frame_degradation`).
- If a Fault Reason is absent from the current mapping, state that it is uncatalogued in
  this mapping version and report the raw string verbatim.

## Caveats

- Do not guess recovery impact or service status for an uncatalogued reason.
- If a mapped value is marked deprecated, report that status and avoid treating it as a
  current expected reason.
