# MAX20087 DLT Parser Knowledge Base

## Purpose

This document defines everything required for an agent to parse and decode MAX20087 debug messages from DLT logs.

The parser shall:

- Extract MAX20087 dump records from raw DLT logs.
- Decode all 10 bytes according to the MAX20087 register map.
- Identify the MAX device (U119/U120/U121).
- Classify channels and cameras using platform mappings.
- Convert ADC values into engineering units.
- Track value changes over time.
- Generate concise summaries and visual timelines.
- Never hallucinate unknown values.
- Preserve raw values whenever decoding is uncertain.

Reference datasheet:

- max20086-max20089 rev7_07_23 (AIng from ADI 2025-09-10) 1.pdf 

---

# 1. Expected Log Format

Example:

```text
62520 2026/04/02 09:19:44.955385 24.9886 56 HPA ZCD1 ZCD1 0 log info verbose 1 blocks/pd/max20087/src/power_switch_driver_csp.cpp:263: MAX20087 U120 = 7f:2e:21:10:11:11:00:0d:09:09, ts = 13812963e7de41
```

Example:

```text
62623 2026/04/02 09:19:45.256940 25.0886 159 HPA ZCD1 ZCD1 0 log info verbose 1 blocks/pd/max20087/src/power_switch_driver_csp.cpp:263: MAX20087 U120 = 7f:3f:21:10:00:00:00:07:0a:09, ts = 13812969de26b5
```

Important section:

```text
MAX20087 U120 = 7f:2e:21:10:11:11:00:0d:09:09
```

This consists of:

```text
MAX20087
Device ID
10-byte register dump
```

---

# 2. Extraction Regex

Recommended:

```regex
MAX20087\s+
(?<device>U(?:1_)?(?:119|120|121))
\s*=\**
(?<dump>[0-9a-fA-F]{2}(?::[0-9a-fA-F]{2}){9})
(?:\s*,\s*ts\s*=\s*(?<hwts>[0-9a-fA-F]+))?
```

---

# 3. Device Normalization

Normalize:

| Raw | Canonical |
|-------|-------|
| U119 | U1_119 |
| U120 | U1_120 |
| U121 | U1_121 |
| U1_119 | U1_119 |
| U1_120 | U1_120 |
| U1_121 | U1_121 |

Output:

```yaml
device_raw: U120
device_canonical: U1_120
```

---

# 4. Register Layout

The dump contains exactly 10 bytes.

| Byte | Register | Address |
|--------|--------|--------|
| 0 | MASK | 0x00 |
| 1 | CONFIG | 0x01 |
| 2 | ID | 0x02 |
| 3 | STAT1 | 0x03 |
| 4 | STAT2 lower | 0x04 |
| 5 | STAT2 upper | 0x05 |
| 6 | ADC1 | 0x06 |
| 7 | ADC2 | 0x07 |
| 8 | ADC3 | 0x08 |
| 9 | ADC4 | 0x09 |

Example:

```text
7f:3b:21:10:00:01:0b:0b:00:0a
```

maps to:

```yaml
MASK        = 0x7F
CONFIG      = 0x3B
ID          = 0x21
STAT1       = 0x10
STAT2_LOWER = 0x00
STAT2_UPPER = 0x01
ADC1        = 0x0B
ADC2        = 0x0B
ADC3        = 0x00
ADC4        = 0x0A
```

---

# 5. MASK Register (0x00)

Bit definitions:

| Bit | Name |
|------|------|
| 7 | OVTST |
| 6 | ACCM |
| 5 | TSM |
| 4 | VDDM |
| 3 | VINM |
| 2 | OCM |
| 1 | OVM |
| 0 | UVM |

Meaning:

```text
OVTST = Overvoltage diagnostics enabled
ACCM  = ADC completion interrupt masked
TSM   = Thermal shutdown interrupt masked
VDDM  = VDD fault interrupt masked
VINM  = VIN fault interrupt masked
OCM   = Overcurrent interrupt masked
OVM   = Overvoltage interrupt masked
UVM   = Undervoltage interrupt masked
```

Important:

MASK bits indicate interrupt masking.

They DO NOT indicate faults.

Faults come from STAT1 and STAT2.

---

# 6. CONFIG Register (0x01)

Bit layout:

| Bits | Meaning |
|--------|--------|
| 7:6 | MUX[1:0] |
| 5 | ENC |
| 4 | CLR |
| 3 | EN4 |
| 2 | EN3 |
| 1 | EN2 |
| 0 | EN1 |

---

## ADC MUX Selection

### 00 = CURRENT MODE

```text
ADC1 -> OUT1 current
ADC2 -> OUT2 current
ADC3 -> OUT3 current
ADC4 -> OUT4 current
```

### 01 = VOLTAGE MODE

```text
ADC1 -> OUT1 voltage
ADC2 -> OUT2 voltage
ADC3 -> OUT3 voltage
ADC4 -> OUT4 voltage
```

### 10 = SYSTEM VOLTAGE MODE

```text
ADC1 -> VIN
ADC2 -> VDD
ADC3 -> VISET
ADC4 -> unused
```

### 11

```text
Reserved
```

Never decode ADC values when MUX=11.

---

## ENC

```text
0 = ADC starts when ADC1 is read
1 = Continuous ADC updates
```

---

## CLR

```text
0 = Faults latched until read
1 = Real-time status
```

---

## Channel Enables

```text
EN1 -> CH1
EN2 -> CH2
EN3 -> CH3
EN4 -> CH4
```

Enabled channels:

```yaml
enabled_channels:
  - 1
  - 2
  - 4
```

Do not assume outputs are physically ON.

Actual operation also depends on external EN pin.

---

# 7. ID Register (0x02)

Bit layout:

```text
Bits 5:4 = device type
Bits 3:0 = revision
```

Device decode:

| ID[5:4] | Device |
|------|------|
| 00 | MAX20089 |
| 01 | MAX20088 |
| 10 | MAX20087 |
| 11 | MAX20086 |

Example:

```text
0x21 = 00100001
```

Result:

```text
Part     = MAX20087
Revision = 1
```

Display:

```text
MAX20087 rev 1 (0x21)
```

---

# 8. STAT1 Register (0x03)

Bit definitions:

| Bit | Meaning |
|------|------|
| 5 | ISET |
| 4 | ACC |
| 3 | OVIN |
| 2 | UVIN |
| 1 | OVDD |
| 0 | UVDD |

Description:

```text
ISET = ISET pin fault
ACC  = ADC conversion complete
OVIN = VIN overvoltage
UVIN = VIN undervoltage
OVDD = VDD overvoltage
UVDD = VDD undervoltage
```

Example:

```text
0x10 = 00010000
```

Result:

```text
ACC
```

For compatibility with existing reports:

```text
faults : ACC
```

---

# 9. STAT2 Register

STAT2 is split across two bytes.

## Lower Byte (0x04)

Channels 2 and 1.

| Bit | Meaning |
|------|------|
| 7 | TS2 |
| 6 | OC2 |
| 5 | OV2 |
| 4 | UV2 |
| 3 | TS1 |
| 2 | OC1 |
| 1 | OV1 |
| 0 | UV1 |

---

## Upper Byte (0x05)

Channels 4 and 3.

| Bit | Meaning |
|------|------|
| 7 | TS4 |
| 6 | OC4 |
| 5 | OV4 |
| 4 | UV4 |
| 3 | TS3 |
| 2 | OC3 |
| 1 | OV3 |
| 0 | UV3 |

---

## Fault Meanings

```text
TS = Thermal shutdown
OC = Overcurrent
OV = Overvoltage
UV = Undervoltage
```

Important:

- UV during startup may be normal.
- UV may indicate disabled output.
- OC is the strongest indicator of overload.
- OV may indicate short-to-battery.

Do not claim root cause from a single sample.

---

# 10. ADC Decoding

Interpretation depends entirely on CONFIG.MUX.

---

## CURRENT Mode (MUX=00)

Formula:

```text
Current (mA) = ADC * 3
```

Example:

```text
ADC = 72

72 * 3 = 216 mA
```

---

## VOLTAGE Mode (MUX=01)

Formula:

```text
Voltage = ADC * 70 mV
```

Example:

```text
ADC = 100

100 * 70 = 7000 mV
= 7.0 V
```

---

## SYSTEM MODE (MUX=10)

### ADC1

```text
VIN = ADC1 * 70 mV
```

### ADC2

```text
VDD = ADC2 * 25 mV
```

### ADC3

```text
VISET = ADC3 * 5 mV
```

### ADC4

```text
Unused
```

---

# 11. Camera Mapping

## CONFIG_1 (VCUv2)

```text
U1_120

CH1 OUT1 Short_Range_Front
CH2 OUT2 Short_Range_Left
CH3 OUT3 Short_Range_Right
CH4 OUT4 Short_Range_Back

U1_121

CH1 OUT1 Driver_Monitoring_D
CH2 OUT2 Driver_Monitoring_I
CH3 OUT3 NC
CH4 OUT4 Forward_Looking_Wide
```

---

## CONFIG_1_5 (VCUv2_HI)

```text
U1_120

CH1 Short_Range_Front
CH2 Short_Range_Left
CH3 Short_Range_Right
CH4 Short_Range_Back

U1_121

CH1 Driver_Monitoring_D
CH2 Driver_Monitoring_I
CH3 NC
CH4 Forward_Looking_Wide

U1_119

CH1 Long_Range_Back_Right
CH2 Long_Range_Back_Left
CH3 Long_Range_Intersection_Right
CH4 Long_Range_Intersection_Left
```

---

## CONFIG_2 (ADPM)

```text
U1_120

CH1 NC
CH2 NC
CH3 NC
CH4 NC

U1_121

CH1 Long_Range_Back_Left
CH2 Long_Range_Back_Right
CH3 NC
CH4 NC
```

---

# 12. Example Decode

Input:

```text
MAX20087 U120 = 7f:3b:21:10:00:01:0b:0b:00:0a
```

Output:

```text
dump      : 7f:3b:21:10:00:01:0b:0b:00:0a

device    : U120
config    : 0x3B (00111011)

mux       : 00 -> CURRENT

ctrl      :
  ENC=1
  CLR=1

channels  :
  enabled=[1,2,4]

id        :
  MAX20087 rev 1 (0x21)

faults    :
  ACC
  UV3

adc:
  CH1 current = 11 * 3 mA = 33 mA
  CH2 current = 11 * 3 mA = 33 mA
  CH3 current =  0 * 3 mA = 0 mA
  CH4 current = 10 * 3 mA = 30 mA
```

---

# 13. Example Decode

Input:

```text
MAX20087 U120 = 7f:3b:21:10:00:01:48:40:00:00
```

Output:

```text
dump      : 7f:3b:21:10:00:01:48:40:00:00

device    : U120

config    : 0x3B (00111011)

mux       : 00 -> CURRENT

ctrl      :
  ENC=1
  CLR=1

channels  :
  enabled=[1,2,4]

id        :
  MAX20087 rev 1 (0x21)

faults    :
  ACC
  UV3

adc:
  CH1 current = 72 * 3 mA = 216 mA
  CH2 current = 64 * 3 mA = 192 mA
  CH3 current = 0 * 3 mA = 0 mA
  CH4 current = 0 * 3 mA = 0 mA
```

---

# 14. Multi-Sample Analysis

When several records are present:

1. Sort by timestamp.
2. Group by device.
3. Compare consecutive dumps.
4. Highlight:
   - CONFIG changes
   - Channel enable changes
   - New faults
   - Cleared faults
   - ADC deltas

Preferred output:

| Time | Device | Faults | CH1 | CH2 | CH3 | CH4 |
|--------|--------|--------|--------|--------|--------|--------|
| 09:19:44.955385 | U120 | UV1 UV2 UV3 UV4 | 0 | 39 | 27 | 27 |
| 09:19:45.256940 | U120 | none | 0 | 21 | 30 | 27 |

Visual trend:

```text
CH2
39 mA  █████████████
21 mA  ███████
```

---

# 15. Validation Rules

The parser shall reject invalid dumps.

## Wrong Byte Count

Expected:

```text
10 bytes
```

Error:

```yaml
parse_status: invalid
reason: expected 10 bytes
```

---

## Reserved MUX

```text
MUX = 11
```

Output:

```yaml
adc_mode: reserved
adc_decoding: not possible
```

---

## Unknown Values

When uncertain:

```yaml
status: unknown
raw_value: 0xXX
```

Never invent interpretations.

---

# 16. Agent Response Rules

Always provide:

1. Device (U119/U120/U121)
2. Decoded CONFIG
3. Enabled channels
4. Decoded faults
5. ADC conversion
6. Camera names if configuration known
7. Timeline view when multiple records exist

Never provide:

- Hallucinated fault causes
- Guesses for reserved values
- Camera mappings without known configuration
- ADC engineering values when MUX=11
- Assumptions about external EN pin

Always preserve raw dumps.