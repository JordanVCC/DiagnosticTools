# Camera Container Initialization

## Scope

Third phase of the exterior-camera startup sequence, occurring once per camera after SIPL initialization (and GPIO checks) succeed. See `knowledge/cameras.md` for the full list of valid camera names.

## Success pattern

```text
Initializing camera container for <camera>
Camera container initialization successful!
```

- `Initializing camera container for <camera>` marks the start of this phase for a specific camera (e.g. `Initializing camera container for SRCF`).
- `Camera container initialization successful!` confirms that camera's container initialized successfully.

This phase repeats once per active camera. A system with multiple cameras will show one init/success pair per camera in the evidence.

## Failure pattern

When a camera container fails to initialize, a fault reason line is observed instead of the success line:

```text
Initialization failed with fault reason: <fault code>
```

- `<fault code>` is an application-defined error code that always begins with `k` (PascalCase after that), e.g. `kDeviceBlockNotifErrorDeserializerFailure`.
- Confirmed example: `Initialization failed with fault reason: kDeviceBlockNotifErrorDeserializerFailure`
- See `knowledge/fault-reasons.md` and its source tables for the current description,
  recovery behavior, service status, DTC phase, and category.

## Reporting guidance

- Match each `Initializing camera container for <camera>` line to its corresponding success or failure line. If neither line follows, the outcome for that camera is unknown from this evidence — say so rather than assuming success or failure.
- If a Fault Reason line appears, quote it exactly and look it up in
  `knowledge/tables/CS_Fault_Reasons_Mapping.csv`. If it is absent from the current
  mapping, state that explicitly instead of guessing its meaning.
- Do not generalize a single camera's failure to the whole system unless every camera shows the same pattern.
- Confirm SIPL succeeded first (see `01-sipl.md`) before treating a camera container failure as camera-specific; if SIPL never succeeded, camera container failures are expected and not independently diagnostic.

## Caveats

The mapping changes over time. Do not invent meanings for unseen Fault Reasons; report
the value verbatim and identify it as absent from the current mapping version.
