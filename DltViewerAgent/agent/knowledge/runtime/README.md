# Runtime Faults Overview

## Scope

Use this document when investigating camera failures that occur during post-initialization runtime operation (after startup and container initialization have completed).

## Runtime Fault Signatures

### 1. New Camera Faults Reported

When camera supervision or driver components detect a runtime error, it is reported in the log as:

```text
New camera faults reported on <CAMERA>: <FaultReason1> [<FaultReason2> ...]
```

Examples:
- `New camera faults reported on FLCW: kDeviceBlockNotifErrorSerializerFailure`
- `New camera faults reported on FLCW: kDisableLink`
- `New camera faults reported on FLCW: kDeviceBlockNotifErrorGetModuleErrorInfoFailure`
- `New camera faults reported on FLCW: kDeserializerGlobalError kErrbLockContention`
- `New camera faults reported on FLCW: kDeserializerLinkError`

### 2. Device Block Notification Events

Runtime hardware interrupt events from Nvidia / GMSL drivers:

- `Device-block: NOTIF_ERROR_SERIALIZER_FAILURE - INTR_STATUS_SER_FAILURE`
- `Device-block: NOTIF_ERROR_DESERIALIZER_FAILURE - INTR_STATUS_DES_ERRB_ERR`
- `Device-block: NOTIF_ERROR_SENSOR_FAILURE - INTR_STATUS_SEN_FAILURE`

### 3. Camera Operation State Changes

Following a reported fault, the operational state of the camera is updated:

```text
Camera operation state on <CAMERA>: <State>
```

Example:
- `Camera operation state on FLCW: Deactivated`

## Reporting Guidance

- Always cite the exact `New camera faults reported on <CAMERA>: ...` log line and timestamp.
- For DTCs appearing during SC7 standby/resume, especially status `26`, use
  `runtime/sc7-standby-resume-dtc-26.md` to correlate DK, CFM, CPDD, I2C mode, and
  camera-state timing evidence.
- For vehicle-time integrity faults, use `vehicle-time-integrity.md` to check
  `LGST LGST` for a backward jump first on any platform. Then check
  `ZCD1 ZCD1` for a time-fetch warning, which may also occur after a jump.
- Look up every reported `<FaultReason>` in `knowledge/fault-reasons.md` and `knowledge/tables/CS_Fault_Reasons_Mapping.csv` to report:
  - Human-readable description.
  - Recovery requirement (`YES` = Requires HPA Restart / SC7 vs `NO` = SelfHealing / Cooldown).
  - Camera Service Status (e.g. `Deactivated` vs `SelfHealing`).
  - High-level CFM Fault Category and DTC phase (`init_phase`, `runtime_phase`, `frame_degradation`).
- Check `knowledge/runtime/error-buffers.md` for serializer, sensor, and deserializer error buffer dumps associated with the fault.
