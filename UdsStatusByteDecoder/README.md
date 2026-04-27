# UDS Status Byte Decoder

Lightweight, shareable tool to decode UDS DTC status bytes (ISO 14229 bit definitions).

## Usage

1. Open `uds_status_decoder.html` in any web browser.
2. Enter bytes like:
   - `26 27 2f af`
   - `0x26, 0x27, 2F, AF`
3. Click **Decode**.

The tool maps each byte to standard UDS status bits:

- bit 0: `testFailed`
- bit 1: `testFailedThisOperationCycle`
- bit 2: `pendingDTC`
- bit 3: `confirmedDTC`
- bit 4: `testNotCompletedSinceLastClear`
- bit 5: `testFailedSinceLastClear`
- bit 6: `testNotCompletedThisOperationCycle`
- bit 7: `warningIndicatorRequested`

No install steps required. This is a single HTML file with embedded CSS and JavaScript.
