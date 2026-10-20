# Diagnostic DID and DTC Availability

## Scope

Diagnostic DTC suffixes and diagnostic DID identifiers for exterior cameras. Camera DTC
prefixes are universal across diagnostics and calibration; the suffixes and DIDs listed
here are diagnostics-specific.

The values below are project knowledge from the Confluence page `Diagnostics DID/DTC
Summary`, which states that Carweaver should be checked for the most up-to-date DTC
information and dates the DTC content to 2026-04-23.

## DTC Composition

Camera DTCs are composed from a universal per-camera prefix and a domain-specific suffix.
For diagnostics, the suffix identifies the diagnostic fault category. For example,
`D50A93` indicates the `SRCF` prefix (`D50Axx`) with the diagnostic initialization fault
suffix (`xxxx93`).

### Camera DTC prefixes

| Camera | DTC prefix |
| --- | --- |
| `FLCW` | `D4D5xx` |
| `SRCF` | `D50Axx` |
| `SRCL` | `D50Bxx` |
| `SRCR` | `D50Cxx` |
| `SRCB` | `D509xx` |
| `LRBL` | `D4EExx` |
| `LRBR` | `D4EFxx` |
| `LRIL` | `D606xx` |
| `LRIR` | `D607xx` |

### Fault-category suffixes

| Category | Diagnostic DTC suffix | Meaning | Triggering fault categories |
| --- | --- | --- | --- |
| INIT faults | `xxxx93` | Faults occurring during initialization. | `kEepromDataIntegrityCheckFault`, `kEepromReadFault`, `kInitializationAndStartupFault`, `kLinkLockFault`, `kSafetyMechanismCheckFault`, `kSensorGpioTestFault`, `kUnrecoverableSystemFault`, `kSerializerGpioTestFault` |
| Unrecoverable runtime faults | `xxxx96` | Runtime faults that require suspend/resume or VCU reset to recover. | `kDeserializerElectricalFault`, `kDeserializerLinkError`, `kDeserializerPipelineFault`, `kFsyncError`, `kLinkLockFault`, `kModuleElectricalFault`, `kSensorFault`, `kUnrecoverableSystemFault`, `kUnknownDriverErrors`, `kEmbeddedDataErrorFlag`, `kSerializerFault` |
| Recoverable runtime faults | `xxxx92` | Runtime faults that can recover. | `kTemperatureOutOfRange`, `kBadVideoData`, `kDeserializerFault`, `kDeserializerGlobalFault`, `kInvalidImageMetadata`, `kSystemFault`, `kVehicleTimeFault`, `kCaptureTimeoutError` |
| Environmental faults | `xxxx98` | Temperature out of range; previously described as over-temperature and expected to cover both over- and under-temperature. | `kTemperatureOutOfRange` |
| System faults | `xxxx9A` | Overvoltage. | Not mapped to a fault category; currently unused and should not be reported. |
| Electrical faults | `xxxx11` | Short to ground. | Not mapped to a fault category; reported by CPDD. |
| Electrical faults | `xxxx12` | Short to battery. | Not mapped to a fault category; reported by CPDD. |
| Electrical faults | `xxxx13` | Open circuit. | Not mapped to a fault category; reported by CPDD. |
| No fault | `-` | Default case. | `-` |

## Diagnostic DIDs

These DID values are for diagnostic visibility and service diagnostics, not calibration.

| Description | Cluster A on HPA (`FLCW`, `SRCx`) | Cluster B on HPA (`LRIx`, `LRBx`) | Cluster B on HPB (`LRIx`, `LRBx`) | Contains / purpose |
| --- | --- | --- | --- | --- |
| Cameras Power Switch Enable Status | `0xD931` | `0x2151` | `0xD931` | Enable/disable state of each camera power-switch channel, including timestamp. Used for diagnostic visibility and service power-control decisions. |
| Cameras Power Switch Output Voltage | `0xD932` | `0x2152` | `0xD932` | Measured supply voltage per camera channel in mV with timestamp. Used to diagnose overvoltage, undervoltage, and power-integrity issues. |
| Camera Power Switch Output Current | `0xD933` | `0x2153` | `0xD933` | Measured supply current per camera channel in mA with timestamp. Supports detection and correlation of short-to-battery, short-to-ground, overcurrent, and thermal events. See `current-draw.md` for typical camera current ranges. |
| Cameras Power Switch Channel Status | `0xD934` | `0x2154` | `0xD934` | Channel status flags with timestamp, including thermal shutdown, overcurrent, overvoltage, and undervoltage. Provides high-level power-switch fault context per channel. |
| Freeze Frame Data | `0xD0FD` | `0x2150` | `0xD0FD` | Snapshot captured when a camera DTC is reported as `TestFailed`. Includes the fault category received from Camera Service for fault tracing and diagnostics. |
| Camera Part Number | `0xF13B` | `0xD996` | `0xD996` | Camera hardware part number read from Camera Service, with timestamp. Used for hardware identification and service diagnostics. |
| Camera Serial Number | `0xF13F` | `0xD997` | `0xD997` | Camera hardware serial number read from Camera Service, with timestamp. Used for traceability, manufacturing data, and service analysis. |

## Reporting Guidance

- Use this page to identify universal camera DTC prefixes, diagnostic DTC suffix
  categories, and diagnostic DID availability by cluster.
- Use `diagnostic-identifier-change-surfaces.md` when investigating why a DID, RID, or
  DTC is available, decoded, or implemented differently between products or releases.
- For a camera DTC, combine the camera prefix with the suffix category, then cross-check
  the underlying Camera Service `k...` fault category in `fault-reasons.md` and the
  master tables under `tables/`.
- Use `log-sources.md` when deciding whether to extract Diagnostics (`Diag DK--`) logs
  to confirm DTC state or camera diagnostic failures.
- If a case concerns calibration suffixes or DIDs, state that this page does not apply
  to those identifiers and request or consult calibration-specific knowledge. The camera
  DTC prefixes still apply.

## Caveats

- Carweaver is the freshness authority for diagnostic DTC information; check it before
  treating the DTC list as complete.
- The DTC table is dated 2026-04-23 in the source page. Later platform, cluster, or
  diagnostic changes may supersede these values.
- `xxxx9A`, `xxxx11`, `xxxx12`, and `xxxx13` are listed for diagnostics visibility, but
  the source says they are not mapped to Camera Service fault categories. Do not infer a
  Camera Service root cause from these suffixes alone.