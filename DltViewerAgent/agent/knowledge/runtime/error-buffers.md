# Error Buffer Dumps & Decoded Diagnostics

## Scope

Use this document when evidence includes error buffer updates, error buffer dumps, or decoded deserializer/serializer diagnostic printouts.

## Error Buffer Log Structure

During hardware faults or periodic checks, the camera driver requests error buffer updates from the serializer, sensor, and deserializer hardware.

### 1. Serializer & Sensor Error Buffers

Logs report an error buffer update notification followed by raw hex dump output:

```text
<CAMERA> Serializer error buffer update
Error buffer dump: 0x000001010000000000000000000000DA00
```

```text
<CAMERA> Sensor error buffer update
Error buffer dump: 0x800000000000000000000000000000000000
```

- When a serializer fault occurs (`kDeviceBlockNotifErrorSerializerFailure`), inspect the Serializer error buffer update and its raw hex dump.
- When a sensor fault occurs (`kDeviceBlockNotifErrorSensorFailure`), inspect the Sensor error buffer update and its raw hex dump.

### 2. Deserializer Error Buffers & Decoded Printouts

When a deserializer fault occurs, Zenseact logging provides decoded deserializer status printouts directly in the DLT output:

```text
Deserializer error buffer update
Global failure [0]: MAX96712_GLOBAL_REMOTE_SIDE (8) - 0x2
Global failure [1]: MAX96712_GLOBAL_ERR (1) - 0xde
Link 3 error [0]: MAX96712_GMSL2_LINK_UNLOCK_ERR (1) - 0x0
Link 3 error [1]: MAX96712_GMSL2_LINK_DEC_ERR (2) - 0x8
Link 3 error [2]: MAX96712_GMSL2_LINK_VIDEO_PXL_CRC_ERR (7) - 0x8
Error buffer dump: 0x0800000001000000...
```

#### Decoded Fields Breakdown

- **Global Failures:**
  - `MAX96712_GLOBAL_REMOTE_SIDE`: Indicates a fault detected on the remote (serializer/camera) side.
  - `MAX96712_GLOBAL_ERR`: General global error register flags on the deserializer.
- **Link Errors (e.g. Link 0-3):**
  - `MAX96712_GMSL2_LINK_UNLOCK_ERR`: GMSL2 link lock loss / unlock count or status.
  - `MAX96712_GMSL2_LINK_DEC_ERR`: GMSL2 decode error count or flags.
  - `MAX96712_GMSL2_LINK_VIDEO_PXL_CRC_ERR`: Video pixel CRC error count or flags.

Because decoded printouts are emitted directly in the log stream, read and cite the decoded `MAX96712_*` lines directly in the analysis report without attempting manual hex decoding.

## Reporting Guidance

- Whenever an error buffer update appears in evidence, quote the `<CAMERA> Serializer error buffer update`, `<CAMERA> Sensor error buffer update`, or `Deserializer error buffer update` header and the hex `Error buffer dump: ...`.
- If decoded deserializer lines (`MAX96712_*`) are present, include them in the key evidence section of the report.
- Note whether the error buffer update points to a remote side issue (`MAX96712_GLOBAL_REMOTE_SIDE`), decode errors (`LINK_DEC_ERR`), or pixel CRC errors (`LINK_VIDEO_PXL_CRC_ERR`).
