# Glossary

| Term | Meaning |
| --- | --- |
| BQ | Baseline Qualification; regular testing run in the CI pipeline. |
| CFM | Camera Fault Monitor; detects and reports camera faults to DK and handles camera DIDs related to the power switch. |
| CPDD | Camera Power Diagnostics Driver; monitors the power-switch chip that supplies power to the cameras and is responsible for diagnostics of these chips. |
| DK | Diagnostic Kernel; manages DTC state transitions. |
| DLT | Diagnostic Log and Trace format used for ECU/application logging. |
| SIPL | Platform-level initialization phase that must succeed before GPIO checks and camera container initialization. See `startup/01-sipl.md`. |
| Camera container | Per-camera runtime component initialized during startup, after SIPL succeeds. See `startup/03-camera-container.md`. |
| Fault Reason | Application-defined `k...` identifier reported for camera-service faults across initialization and runtime phases. See `fault-reasons.md`. |
| Evidence | Filtered ASCII log lines selected for agent analysis. |
| DLT source filter | Reviewed file containing APP-ID/CTX-ID pairs passed to `dlt-convert -f`. |
| Manifest | Reproducibility record containing input checksum, source filters, command, and output/chunk counts. |
| Hypothesis | A plausible explanation that still requires confirmation. |
| Root cause | A confirmed cause supported by sufficient evidence, not just a familiar pattern. |
