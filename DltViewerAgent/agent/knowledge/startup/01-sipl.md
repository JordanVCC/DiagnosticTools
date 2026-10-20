# SIPL Initialization

## Scope

First phase of the exterior-camera startup sequence. Platform-level; occurs once per startup, not per camera.

## Success pattern

```text
Initializing SIPL
SIPL initialization successful!
```

- `Initializing SIPL` marks the start of this phase.
- `SIPL initialization successful!` confirms it completed successfully.

## Reporting guidance

- If `Initializing SIPL` is present but `SIPL initialization successful!` never follows, SIPL did not complete — treat this as blocking for every downstream camera container, since GPIO checks and camera container initialization both depend on SIPL succeeding first.
- If neither line appears in the evidence, state that explicitly rather than assuming
  SIPL succeeded. Confirm that the correct Camera Service APP/CTX filter was selected
  before concluding SIPL was skipped.

## Caveats

Failure/error log formats for a failed SIPL initialization are not yet confirmed. Do not invent or assume specific SIPL error messages; only report on the presence or absence of the two confirmed lines above until failure signatures are documented.
