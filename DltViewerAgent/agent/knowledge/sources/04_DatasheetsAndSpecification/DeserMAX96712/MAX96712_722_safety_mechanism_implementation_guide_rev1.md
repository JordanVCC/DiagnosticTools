# MAX96712_722_safety_mechanism_implementation_guide_rev1

Source: C:\Users\JHARVEY\OneDrive - Volvo Cars\Documents\01_Resources\04_DatasheetsAndSpecification\DeserMAX96712\MAX96712_722_safety_mechanism_implementation_guide_rev1.xlsx

## Implementation Guide

|  | Product (Part Number) | MAX96712/MAX96722 |  |  |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|  | ASIL Level: | B |  |  |  |  |  |  |  |  |  |  |  |
|  | Reference to Hardware Integration and Testing Report: | 32-100307 C |  |  |  |  |  |  |  |  |  |  |  |
|  | Originator: | Craig Sakamoto |  |  |  |  |  |  |  |  |  |  |  |
|  | Date: | 2021-04-30 00:00:00 |  |  |  |  |  |  |  |  |  |  |  |
| Safetey Measure Number | Safety Measure Name | Safety Measure Description | Fault to be detected | Test Case Number | Diagnostic  Test Interval | Operational Mode | Optimized SM  (Default/Optional) | Routed to ERRB? | Bits to enable routing to ERRB and default values | Bits to read to clear this error | Main Error Flag Bit | Register(s) to read to clear, or to detect if SM not routed to ERRB | General Comments |
| SM1 | BIST for Serial Link (BER Testing using PRBS) | Built in PRBS Checker for BER Testing of the full-duplex Serial Link for forward and reverse direction | Data Corruption - Video Channel, Bit Error Detection, Link Issues | TC1 Bit Error on Forward Video (Forward Video PRBS) TC2 Bit Error on GMSL link (GMSL Link PRBS) TC3 MIPI Loopback PRBS Test | <10 us | startup | Optional | YES (Does not go to ERRB by default) | DEC_ERR_OEN__ = 1, IDLE_ERR_OEN__ = 0, VPRBS_ERR_OEN = 1 | DEC_ERR_A/B/C/D (0x0035-0x0038)   (VPRBS_ERR_0/1/2/3/4/5/6/7) | DEC_ERR_FLAG__,IDLE_ERR_FLAG_A/B/C/D (0x002C)  VPRBS_ERR_FLAG (0x002A) | DEC_ERR_A/B/C/D (0x0035-0x0038)   IDLE_ERR_FLAG_A/B/C/D (0x002C)  VPRBS_ERR_FLAG (0x002A)  (VPRBS_ERR_0/1/2/3/4/5/6/7) | SM1 Test Cases as written are intended as a latent check of the PRBS and is not a BER test. TC1 requires MFP0 connected to MFP2. TC2 requires a uC in the serializer module. |
| SM2 | Line fault detection on Deserializer Output | Line faults (short to Batt/Gnd or open) are detected on the GMSL 2 input pins SIO_P and SIO_N. The result is flagged on the LFLTB pin. | Line Faults on the Serial Link Output (Short to Bat/Gnd/Open) | SM2_TC_1 SIOA+ Short to Battery SM2_TC_2 SIOA- Short to Battery SM2_TC_3 SIOB+ Short to Battery SM2_TC_4 SIOB- Short to Battery SM2_TC_5 SIOC+ Short to Battery SM2_TC_6 SIOC- Short to Battery SM2_TC_7 SIOD+ Short to Battery SM2_TC_8 SIOD- Short to Battery SM2_TC_9 SIOA+ Short to GND SM2_TC_10 SIOA- Short to GND SM2_TC_11 SIOB+ Short to GND SM2_TC_12 SIOB- Short to GND SM2_TC_13 SIOC+ Short to GND SM2_TC_14 SIOC- Short to GND SM2_TC_15 SIOD+ Short to GND SM2_TC_16 SIOD- Short to GND SM2_TC_17 SIOA+ Line Open SM2_TC_18 SIOA- Line Open SM2_TC_19 SIOB+ Line Open SM2_TC_20 SIOB- Line Open SM2_TC_21 SIOC+ Line Open SM2_TC_22 SIOC- Line Open SM2_TC_23 SIOD+ Line Open SM2_TC_24 SIOD- Line Open SM2_TC_25 SIOA+/SIOA- Line-to-Line Short SM2_TC_26 SIOB+/SIOB- Line-to-Line Short SM2_TC_27 SIOC+/SIOC- Line-to-Line Short SM2_TC_28 SIOD+/SIOD- Line-to-Line Short | <10 us | continuous | Optional | YES | LFLT_INT_OEN = 1 | LFLT_INT_FLAG | LFLT_INT | LFLT_INT (0x0028)   (LFLT_INT_FLAG[7:0]) |  |
| SM3 | CRC for Control Channel | CRC for Control Channel (UART/I2C/GPIO/SPI) in Forward and Reverse Mode, 16 BIT Packet CRC | Data corruption on the control channel | SM3_TC1 Forward GPIO CRC SM3_TC2 Reverse GPIO CRC SM3_TC3 Forward SPI CRC SM3_TC4 Reverse SPI CRC SM3_TC5 Forward control I2C/UART CRC SM3_TC6 Reverse Control I2C/UART CRC | Single retransmission  <10 us (forward)  I2C @ 1MHz  <100us (reverse) | continuous | Default | YES  (Does not go to ERRB by default) | MAX_RT_OEN__ = 1, MAX_RT_ERR_OEN__ = 1, RT_CNT_OEN = 0 | RT_CNT, MAX_RT_ERR | MAX_RT_FLAG__, RT_CNT_FLAG | MAX_RT_FLAG_A/B/C/D (0x002E)  RT_CNT_FLAG_A/B/C/D (0x002E) |  |
| SM4 | CRC for Forward Video Channel | CRC for Forward Video Channel  (32 BIT VIDEO LINE CRC AND 16 BIT PACKET CRC) | Data corruption on the  forward video channel | SM4_TC1 Bit error on GMSL Link (Link CRC) SM4_TC2 Bit error on Forward Video (Packet CRC) | <10 us | continuous | Default | YES | LCRC_ERR_OEN (0x0029)  VID_PXL_CRC_ERR_OEN__(0x0045) | LCRC_ERR__   VID_PXL_CRC_ERR__ (0x0045) | LCRC_ERR_FLAG, VID_PXL_CRC_ERR__ | LCRC_ERR_FLAG (0x002A)  (LCRC_ERR_0/1/2/3/4/5/6/7)  VID_PXL_CRC_ERR_A/B/C/D (0x0045) |  |
| SM5 | Error Correction through Re-transmission on Control Channel | (UART/I2C/GPIO/SPI) in Forward and Reverse Mode. Correction of up to 16 Bit Errors in each packet. | Re-transmission in case of:  -incorrect CRC  -Dropped packets | SM5_TC1 Error in control channel | Single retransmission  <10 us (forward)   I2C @ 1MHz   <100 us (reverse) | continuous | Default | YES  (Does not go to ERRB by default) | MAX_RT_OEN__ = 1, MAX_RT_ERR_OEN__ = 1, RT_CNT_OEN = 0 | RT_CNT, MAX_RT_ERR | MAX_RT_FLAG__, RT_CNT_FLAG | MAX_RT_FLAG_A/B/C/D (0x002E)  RT_CNT_FLAG_A/B/C/D (0x002E) |  |
| SM6 | LOCK indicator of Forward Channel | (LOCK pin raised in case of timing errors or no lock at the deserializer side) | PLL Lock error  Timing errors | SM6_TC1 PLL lock of Forward Link | <200 ms | continuous | Default | NO | No OEN bits | N/A | N/A | LOCKED (0x001A)   LOCKED_B (0x000A)   LOCKED_C (0x000B)  LOCKED_D (0x000C) |  |
| SM7 | ERRB indicator of Forward Channel | (In case of CRC errors, they are flagged on the deserializer ERRB output) | Forward data transmission errors | SM7_TC1 Loss of  Forward Link | <10 us after ERRB  asserted on serializer | continuous | Default | N/A | No OEN bits | N/A | N/A | ERRB pin  ERROR (0x001A) |  |
| SM8 | Lock Indicator of Reverse channel | LOCK pin asserted in case of timing errors or no lock at the serializer side | LOCK pin raised in case of timing errors, Continuous Mode. A "no LOCK"  at the serializer side will also be flagged at the deserializer. The lock info frame is exchanged between serializer and deserializer to verify that the remote IC has locked. | SM8_TC1 PLL lock of Rerverse Link | <200 ms | continuous | Optional | NO | No OEN bits | N/A | N/A | LOCKED register on serializer |  |
| SM9 | ERRB indicator of Reverse Channel | Indicate reverse data transmission errors | Verify reverse data transmission errors | SM9_TC1 Loss of  Reverse Link | <10 us after ERRB  asserted on serializer | continuous | Optional | YES (Does not go to ERRB by default) | REM_ERR_OEN = 0, ERR_RX_EN__ = 1, | ERR_RX_RECVED__ | REM_ERR_FLAG | ERRB pin  ERROR (0x001A)   REM_ERR_FLAG (0x002A) |  |
| SM10 | Error generator (serializer) | Fault injection generator at serializer side | Error in CRC generator | SM10_TC1 Verification of error generator | <15 ms @ 1-bit error per 20M bits | startup | Optional | YES (Does not go to ERRB by default) | DEC_ERR_OEN__ = 1, | DEC_ERR_A/B/C/D (0x0035-0x0038) | DEC_ERR_FLAG__ | DEC_ERR_FLAG_A/B/C/D (0x0026)   IDLE_ERR_FLAG_A/B/C/D (0x002C) |  |
| SM11 | Video Sequence Number | There is an alternating one-bit video packet sequence number to detect a video packet dropped and fill-in to sustain continuity. Error will be flagged through CRC. This sequence number is also valid for the  control channel. | Dropped video packets  Dropped control packets | SM11_TC1 Dropped video packets | <10 us | continuous | Optional | VID_SEQ: NO…. LCRC: YES | No OEN bits | VID_SEQ_ERR: 0x108,0x11A,0x12C,0x13E,0x150,0x168,0x17A,0x18C | N/A | VID_SEQ_ERR_0 (0x0108)  VID_SEQ_ERR_1 (0x011A)  VID_SEQ_ERR_2 (0x012C)  VID_SEQ_ERR_3 (0x013E)  VID_SEQ_ERR_4 (0x0150) VID_SEQ_ERR_5 (0x0168) VID_SEQ_ERR_6 (0x017A)  VID_SEQ_ERR_7 (0x018C)  LCRC_ERR_FLAG (0x002A) |  |
| SM12 | Acknowledge of UART or I2C | Host feature, SoC should check for ACK/NAKs | Peer failure | SM12_TC1 Peer Failure | <10 us (forward)  I2C @ 1MHz  <100us (reverse) | continuous | Default | NO | No OEN bits | N/A | N/A |  |  |
| SM13 | Watermark Detector and Watermark Generator | (A watermark sequence is generated at the serializer/deserializer, which is evaluated at the deserializer/serializer) --- UCAP is YUV --- Maybe not useful for the system. UCAP uses line buffers so not useful. | Frozen Frame | SM13_TC1 Generation of Watermark SM13_TC2 Detection of Watermark | <500mS | continuous | Optional | YES (WM is OFF by default) | WM_ERR_OEN = 1,WM1_ERR_OEN = 1 (0x27) | WM_ERROR(0x1205) WM1_ERROR(0x1225) | WM_ERR_FLAG(0x28) WM1_ERR_FLAG(0x28) | WM_ERR_FLAG (0x0028)  WM1_ERR_FLAG (0x0028) |  |
| SM14 | Eye Opening Monitor Measure the link budget. | Devices have ability to monitor vertical/horizontal eye opening. | Loss of lock  Cable signal integrity | SM14_TC1 Visual verification of video checkboard. | <10 us after  bad bit detected  by deserializer | continuous | Optional | YES (Does not go to ERRB by default) | EOM_ERR_OEN__(0x27) = 0 | EOM_ERR_FLAG__(0x28) | EOM_ERR_FLAG__(0x28) | EOM_ERR_FLAG_A (0x0028) EOM_ERR_FLAG_B (0x0028)  EOM_ERR_FLAG_C (0x0028)  EOM_ERR_FLAG_D (0x0028) |  |
| SM15 | Undervoltage and/or Overvoltage Monitoring  on external/internal supplies. | Measure voltage and determine OV and UV on input supply and internal supplies. | The following failure modes are detected: -OV and UV on VDD -UV on VDD18, VDDIO and VTERM | SM15_TC1 Status Register readback | <10 us | continuous | Default | YES (Does not go to ERRB by default) | VDD_OV_OEN = 0 (0x49) VDDBAD_INT_OEN(0x46) = 1 PORZ_INT_OEN(0x46) = 1 VDDCMP_INT_OEN(0x46) = 1 | VDD_OV_FLAG (0x49) VDD_BAD_INT_FLAG(0x47) PORZ_INT_FLAG(0x47) VDDCMP_INT_FLAG(0x47) | VDD_OV_FLAG (0x49) VDD_BAD_INT_FLAG(0x47) PORZ_INT_FLAG(0x47) VDDCMP_INT_FLAG(0x47) | VDDBAD_INT_FLAG (0x0047)   VDDCMP_INT_FLAG (0x0047)   VDD_OV_FLAG (0x004A) |  |
| SM18 | Register Reading for Line Fault, ERRB or LOCK through I2C and UART |  | Readback Line Fault, ERRB and LOCK status through status registers  (redundant to pin level indication) | SM18_TC1 Status Register readback | <60 us I2C @ 1MHz | continuous | Default | N/A | N/A | N/A | N/A | LFLT_INT (0x0028)  ERRB Pin  ERROR (0x001A)  LOCKED (0x001A)  LOCKED_B (0x000A) LOCKED_C (0x000B)  LOCKED_D (0x000C) |  |
| SM19 | Packet Counter for GPIO, I2C, SPI and UART packets | Packet counters for GPIO, I2C, SPI and UART verify correct generation of control data packets and sequence | Packet counters for GPIO, I2C, SPI and UART verifies correct generation of   control data packets and sequence and can detect packet loss. | SM19_TC1 Status Register readback | N/A | continuous | Optional | YES (Does not go to ERRB by default) | PKT_CNT_OEN__(0x2B) = 0 | PKT_CNT__(0x40-0x43) | PKT_CNT_FLAG__(0x2C) | PKT_CNT_FLAG_A/B/C/D (0x002C) |  |
| SM20 | 9b/10b illegal symbol check, running disparity | Check for illegal symbols after decoding | 9b/10b decoding errors are detected through running disparity check | SM20_TC1 Link Failure | <10 us | continuous | Default | YES (Does not go to ERRB by default) | DEC_ERR_OEN__ = 1, IDLE_ERR_OEN__ = 0, VPRBS_ERR_OEN = 1 | DEC_ERR_A/B/C/D (0x0035-0x0038)   (VPRBS_ERR_0/1/2/3/4/5/6/7) | DEC_ERR_FLAG__,IDLE_ERR_FLAG_A/B/C/D (0x002C)  VPRBS_ERR_FLAG (0x002A) | DEC_ERR_FLAG_A/B/C/D (0x0026)  IDLE_ERR_FLAG_A/B/C/D (0x002C) |  |
| SM22 | CRC on configuration data for data retention memory | Configuration registers are protected through CRC in sleep mode | Configuration registers are protected through CRC in sleep mode | SM22_TC1 Status Register readback | <2 ms  (check retention sim)  1150 regs x 140n/reg-access + skipping address = 200us  1.3ms from wakeup to orstb | continuous | Optional | YES (Does not go to ERRB by default) | MEM_ERR_OEN(0x2F) = 0 | MEM_ERR__(0x438) | MEM_ERR__(0x438) | RTTN_CRC_INT (0x0028) |  |
| SM26 | Readback of logic state for GPIO | GPO pin state can be read back and compared to last data written to the GPO | Readback of logic state for all GPIO inputs and outputs in order to detect   short conditions | SM26_TC1 Status Register readback | <60 us I2C @ 1MHz  While in pin is in GPIO mode | on demand | Default | NO | No OEN bits | N/A | N/A | GPIO_IN_0 (0x0300)  GPIO_IN_1 (0x0303)  GPIO_IN_2 (0x0306)  GPIO_IN_3 (0x0309)  GPIO_IN_4 (0x030C)  GPIO_IN_5 (0x0310)  GPIO_IN_6 (0x0313)  GPIO_IN_7 (0x0316)  GPIO_IN_8 (0x0319)  GPIO_IN_9 (0x031C)  GPIO_IN_10 (0x0320)  GPIO_IN_11 (0x0323)  GPIO_IN_12 (0x0326)  GPIO_IN_13 (0x0329)  GPIO_IN_14 (0x032C)  GPIO_IN_15 (0x0330)  GPIO_IN_16 (0x0333) |  |
| SM27 | DPLL status registers reflect the DPLL LOCK state | Verify if the DPLL/MIPI clock locks | DPLL status registers for indication of the DPLL lock | SM27_TC1 Status Register readback | <300 us after power up | continuous | Default | NO | No OEN bits | N/A | N/A | CSIPLL0_LOCK (0x00400) CSIPLL1_LOCK (0x00400)  CSIPLL2_LOCK (0x00400)  CSIPLL3_LOCK (0x00400) |  |
| SM28 | CSI Controller & Dphy/Cphy Handshake |  | If the Handshake is broken, the BackTop memories would overflow and reported in the Status Registers | SM28_TC1 Wrong Conversion of Pixel Data to CSI 2 | <300 us (8k addr x pclk+ buffer) | continuous | Default | NO | No OEN bits | N/A | N/A | LMO_1 (0x040A)  LMO_2 (0x040A)  LMO_3 (0x040A)  LMO_4 (0x040A)  LMO_5 (0x042A)  LMO_6 (0x042A)  LMO_7 (0x042A)  LMO_8 (0x042A) |  |
| SM30 | Command / Line Buffer Overflow |  | Checks if  requested packets are not created and detects errors in the Backtop Write blocks | SM30_TC1 "Status Register readback | <500 us  (16 x 13us line time  + buffer) | continuous | Default | NO | No OEN bits | N/A | N/A | cmd_overflow1 (0x040A)  cmd_overflow2 (0x040A)  cmd_overflow3 (0x040A)  cmd_overflow4 (0x040A)  cmd_overflow5 (0x042A)  cmd_overflow6 (0x042A)  cmd_overflow7 (0x042A)  cmd_overflow8 (0x042A) |  |
| SM33 | PRBS Synchronization and Validation |  | There is PRBS synchronization and validation | _x000D_SM33_TC1 PRBS not synced_x000D_SM34_TC1 Error in information of Video Line CRC_x000D_SM35_TC1 I2C/UART , Error in packet re-trial_x000D_SM36_TC1 Status Register readback | <100 us for synchronization | start up | Optional | YES | No OEN bits | N/A | N/A | DEC_ERR_A/B/C/D (0x0035-0x0038) |  |
| SM34 | CRC protection of info frames | CRC for Infoframes | Info frames are sent periodically and are CRC protected |  | <10 us | continuous | Default | YES | LCRC_ERR_OEN (0x0029) | LCRC_ERR__ | LCRC_ERR_FLAG, | LCRC_ERR_FLAG (0x002A) |  |
| SM35 | Readback of status register informing on ARQ retrials |  | Number of ARQ retrials is stored in status registers and can be read.  This can detect a broken ARQ channel (increase of trial number without packets being sent). |  | <10 us | on demand | Default | YES (Does not go to ERRB by default) | MAX_RT_OEN_A/B/C/D (0x002D)  RT_CNT_OEN_A/B/C/D (0x002D) | RT_CNT SPI: 0x87, 0x97 CC: 0x507, 0x517, 0x527, 0x537 CC: 0x567, 0x577, 0x587, 0x597 CC: 0x5A7, 0x5B7, 0x5C7, 0x5D7 GPIO: 0xA7,0xAF,0xB7,0xBF | RT_CNT_FLAG__(0x2E) | MAX_RT_FLAG_A/B/C/D (0x002E)  RT_CNT_FLAG_A/B/C/D (0x002E) |  |
| SM36 | GPIO open detection | Input Pins: Internal pull-ups and pull-downs are exercised in a sequential manner to detect if input is driven Output Pins: Temporarily reconfigure the pin as an input, then use the internal pull/up/pull downs to detect the presence of an external pull up/pull-down resistor | GPIO open is detected using internal pull ups and pull downs in a sequential procedure |  | <10 us per GPIO | on demand | Default | NO | No OEN bits | N/A | N/A | GPIO_IN_0 (0x0300)  GPIO_IN_1 (0x0303)  GPIO_IN_2 (0x0306)  GPIO_IN_3 (0x0309)  GPIO_IN_4 (0x030C)  GPIO_IN_5 (0x0310)  GPIO_IN_6 (0x0313)  GPIO_IN_7 (0x0316)  GPIO_IN_8 (0x0319)  GPIO_IN_9 (0x031C)  GPIO_IN_10 (0x0320)  GPIO_IN_11 (0x0323)  GPIO_IN_12 (0x0326)  GPIO_IN_13 (0x0329)  GPIO_IN_14 (0x032C)  GPIO_IN_15 (0x0330)  GPIO_IN_16 (0x0333) |  |
| SM37 | Evaluate MIPI CRC |  | The receiver is evaluating CSI2 data sent from MAX96712 according to  MIPI specification Appendix C1-C4 | _x000D_SM37_TC1 Check CRC error _x000D_SM40_TC1 Status Register readback | N/A   DES not evaluate incoming MIPI CRC | on demand | Default | NO | No OEN bits | N/A | N/A | System level verification; Use host receiver to check MIPI CRC error on data coming out of MAX96712 |  |
| SM40 | Frame Sync Lost LOCK |  | Frame Synch Lost Lock - detects if cameras run unsynchronized. The status is visible on the Register and if there is an error it is mapped to ERRB |  | <10 us after frame sync is lost | continuous | Optional | YES | FSYNC_ERR_OEN (0x29) = 1 | FSYNC_ERR_CNT (0x4B0), FSYNC_LOSS_OF_LOCK (0x4B6) | FSYNC_ERR_FLAG (0x2A) | FSYNC_LOCKED (0x04B6) |  |
| SM41 | Memory ECC | CSI-2 ECC is evaluated and internal register needs to be set to monitor ECC | ECC (single bit error correction and dual bit error detection) | _x000D_SM41_TC1 1-bit error correction and 2-bit error reporting_x000D_ | <10 us after ECC error occurs | continuous | Default | YES  (Does not go to ERRB by default) | MEM_ECC_ERR1_OEN(0x44) = 0 MEM_ECC_ERR2_OEN(0x44) = 1 | RESET_MEM_ECC_ERR1_CNT (0x1250) RESET_MEM_ECC_ERR2_CNT (0x1250) | MEM_ECC_ERR1_INT(0x45) MEM_ECC_ERR2_INT(0x45) | MEM_ECC_ERR2_INT (0x045)  MEM_ECC_ERR1_INT (0x045) |  |

## SM1_TC_1

| Optional Safety Measure |  |
|---|---|
| SM1=BIST for Serial Link (BER Testing using PRBS), Video PRBS 6G NRZ |  |
| Safety Measure Goal: Use built in PRBS checker for BER testing and data corruption diagnostics. (decode/idle errors) |  |
| VPRBS |  |
| Notes:  1) Run device PHY errata scripts before test 2) User can either use internal SER RCLKOUT to provide PCLK or use external source. If using SER RCLKOUT as source, connect MFP2 to MFP0. 3) This test is only needed to run on start-up. |  |
| // HW, Mar 2019 |  |
| // SM1_TC_1 Setup |  |
| // MAX9295A (Pattern Gen) -> MAX96712 (DUT) |  |
| // MAX9295A MFP2 and MFP0 connected |  |
| // ---------------- MAX96712 (DUT) setup --------------------- |  |
| // Link A only GMSL2 |  |
| 0x04,0x52,0x00,0x06,0xF1, |  |
| // Pipe 0 stream Link A pipe X only |  |
| 0x04,0x52,0x00,0xF0,0xF0, |  |
| 0x04,0x52,0x00,0xF1,0xFF, |  |
| // Enable VPRBS24 checker on pipe 0 |  |
| 0x04,0x52,0x01,0xDC,0x90, |  |
| // ---------------- MAX9295A (Pattern Gen 1920x1200) setup --------------------- |  |
| // Parallel mode and PCLK input enable |  |
| 0x04,0x80,0x00,0x07,0xF7, // MFP0 - PCLK input |  |
| // Connect MFP2 to MFP0 if using internal PCLK. Otherwise feed external clock on MFP0 and comment out below. |  |
| // Enable PCLK output |  |
| 0x04,0x80,0x00,0x06,0xBF, |  |
| // MFP2 - ref clock out |  |
| 0x04,0x80,0x00,0x03,0x07, |  |
| // Set ref PLL clock = 74.25MHz |  |
| 0x04,0x80,0x03,0xF0,0x71, |  |
| // Enable VPRBS |  |
| 0x04,0x80,0x01,0xE5,0x80, |  |
| /* ---------------- Test Method --------------------- |  |
| - Check PCLKDET on Ser pipe X (0x102); |  |
| - Check VIDEO_LOCK on Des pipe 0 (0x1DC); |  |
| *No MIPI data output as this is focusing on GMSL2 link VPRBS |  |
| - Enable ERR generation on MAX9295A (TX1 0x29 bit 4 or 5), the one generates pattern; |  |
| - ERR rate can be changed from TX1 0x2A[5:4]; |  |
| //0x04,0x80,0x00,0x2A,0x33, |  |
| //0x04,0x80,0x00,0x29,0x10, |  |
| - Check ERRB will output low on DUT MAX96712. |  |
| - Check 0x1DB (VPRBS_ERR) error count will come up. |  |
| *****************************************************/ |  |
|  | Pass |

## SM1_TC_2

| Optional Safety Measure |  |
|---|---|
| SM1=BIST for Serial Link (BER Testing using PRBS), Link PRBS 6G NRZ |  |
| Safety Measure Goal: Use built in PRBS checker for BER testing and data corruption diagnostics. (decode/idle errors) |  |
| Link PRBS |  |
| Notes:  1) Link PRBS requries manual handshake. This means you will need separate uC on each side or connect Ser I2C lines to Des I2C lines. 2) clear errors after every script (read ERRB status in tools or read 0x1A to 0x25 on Ser and Des). 3) Ensure that results are matching with expected results after every script. 4) Run device PHY errata scripts before test. 5) This test is only needed to run on start-up. |  |
| This test requires a uC/I2C on both sides of the link (SER & DES), this may be difficult to implement with a camera module. |  |
| // HW, MAY 2018 |  |
| // SM1_TC_2 Link PRBS Setup |  |
| // MAX9295A -> MAX96712 (DUT) |  |
| /***** |  |
| Link PRBS is performed under manual handshake; Remote CC cannot be accessed through the link: |  |
| - Each side has its own MCU connection as a master for register access; |  |
| - Jump wire Ser/Des I2C connection externally to share one MCU for register access (below example). |  |
| *****/ |  |
| 0x04,0x80,0x14,0xA7,0x81, |  |
| 0x04,0x80,0x00,0x17,0x81, |  |
| 0x04,0x52,0x14,0xA7,0x81, |  |
| 0x04,0x52,0x00,0x1E,0x81, |  |
| //0x04,0x80,0x00,0x10,0x11, |  |
| 0x04,0x80,0x00,0x17,0xA1, |  |
| 0x04,0x52,0x00,0x1E,0xA1, |  |
| 0x04,0x80,0x14,0xA7,0xC1, |  |
| 0x04,0x52,0x14,0xA7,0xC1, |  |
| 0x04,0x80,0x14,0xA7,0xE1, |  |
| 0x04,0x80,0x00,0x17,0xB1, |  |
| 0x04,0x52,0x14,0xA7,0xE1, |  |
| 0x04,0x52,0x00,0x1E,0xb1, |  |
| 0x04,0x80,0x14,0xA7,0xF1, |  |
| 0x04,0x52,0x14,0xA7,0xF1, |  |
| 0x04,0x80,0x00,0x17,0xB9, |  |
| 0x04,0x52,0x00,0x1E,0xB9, |  |
| 0x00,0x0F, |  |
| 0x04,0x80,0x00,0x17,0xBD, |  |
| 0x04,0x52,0x00,0x1E,0xBD, |  |
| /* ---------------- Test Method --------------------- |  |
| Forward Link: |  |
| - Enable LINK_PRBS_CHK on MAX96712 link A (bit7 of 0x1005 RX1): |  |
| 0x1005 = 0xA8 |  |
| - Enable LINK_PRBS_GEN on MAX9295A link A (bit7 of 0x29 TX1): |  |
| 0x29 = 0x80 |  |
| - Check PRBS_SYNCED on MAX96712 link A (bit3 of 0x1007 RX3) is asserted. |  |
| Reverse Link: |  |
| - Enable LINK_PRBS_CHK on MAX9259A link A (bit7 of 0x2D RX1): |  |
| 0x29 = 0xA8 |  |
| - Enable LINK_PRBS_GEN on MAX96712 link A (bit7 of 0x1001 TX1): |  |
| 0x1001 = 0x80 |  |
| - Check PRBS_SYNCED on MAX9295A link A (bit 3 of 0x2F RX3) is asserted. |  |
| *****************************************************/ |  |
|  | Pass |
| `PASSED("Detected number of errors is fine %g",RdData); |  |
| `FAILED("Detected number of errors is not fine"); |  |
| `PASSED("Detected number of errors is fine %g",RdData); |  |
| `FAILED("Detected number of errors is not fine"); |  |

## SM1_TC_3

| Optional Safety Measure |  |  |
|---|---|---|
| SM1=BIST for Serial Link (BER Testing using PRBS), Video PRBS 6G NRZ |  |  |
| Safety Measure Goal: Use built in PRBS checker for BER testing and data corruption diagnostics. (decode/idle errors) |  |  |
| MIPI Loopback PRBS Test |  |  |
| Notes:  1) Run device PHY errata scripts before test 2) Requires the deserializer output to be connected to the input. 3) This test is only needed to run on start-up. |  |  |
| // HW, MAY 2018 |  |  |
| // SM1_TC_3 Setup |  |  |
| // Example: Generate Packetized PRBS24 pattern from Video Pipe 1, and check pattern on Video Pipe 0/1 |  |  |
| /*** Loopback hardware connection |  |  |
| ----------->MAX96712 (DUT)  ---MIPI DPHY 1x4 port A--->  MAX9295A --------> |  |  |
| \| |  | \| |
| \| |  | \| |
| <---------------------------- GMSL2 link A <------------------------------------- |  |  |
| ****/ |  |  |
| // Disable lock cc (for evkit connection) since link will be established |  |  |
| // 0x04,0x52,0x00,0x01,0x18, |  |  |
| // ---------- MAX96712 (DUT) Setup----------- |  |  |
| // Only Enable GMSL PHY A, keep GMSL2 =1 setting for all GMSL PHYs |  |  |
| 0x04,0x52,0x00,0x06,0xF1, |  |  |
| // Set Video Pipe Selection |  |  |
| // Pipe 0 - Link A, stream X |  |  |
| // Pipe 1 - Link A, stream X |  |  |
| 0x04,0x52,0x00,0xF0,0x00, |  |  |
| // Enable Video Pipe 0 and 1 |  |  |
| 0x04,0x52,0x00,0xF4,0x03, |  |  |
| // Set VRX muxes for Video PRBS,, |  |  |
| // Set 75MHz PCLK for test pattern,, |  |  |
| 0x04,0x52,0x00,0x09,0x01, |  |  |
| // Set 1.0G DPLL frequency,, |  |  |
| 0x04,0x52,0x04,0x15,0x2A, |  |  |
| 0x04,0x52,0x04,0x18,0x2A, |  |  |
| 0x04,0x52,0x04,0x1B,0x2A, |  |  |
| 0x04,0x52,0x04,0x1E,0x2A, |  |  |
| // Force CSI clock w/ MIPI PHY 2x4 configuration,, |  |  |
| 0x04,0x52,0x08,0xA0,0x84, |  |  |
| // Set Lane Count - 4 lane DPHY |  |  |
| 0x04,0x52,0x09,0x0A,0xC0, |  |  |
| 0x04,0x52,0x09,0x4A,0xC0, |  |  |
| 0x04,0x52,0x09,0x8A,0xC0, |  |  |
| 0x04,0x52,0x09,0xCA,0xC0, |  |  |
| // Set Phy lane Map for all MIPI PHYs 2x4 |  |  |
| 0x04,0x52,0x08,0xA3,0xE4, |  |  |
| 0x04,0x52,0x08,0xA4,0xE4, |  |  |
| // Enable PRBS generator/checker PRBS24 on Video Pipe 1; enable PRBS checker PRBS7 on Video Pipe 0 (for comparison) |  |  |
| 0x04,0x52,0x01,0xDC,0x88, |  |  |
| 0x04,0x52,0x01,0xFC,0x90, |  |  |
| // Change PCLK = 150MHz |  |  |
| //0x04,0x52,0x00,0x09,0x02, |  |  |
| // Link reset |  |  |
| 0x04,0x52,0x00,0x18,0x0F, |  |  |
| // Delay 255ms |  |  |
| 0x00,0xFF, |  |  |
| // ---------- MAX9295A Setup ----------- |  |  |
| // Use default MIPI settings. |  |  |
| // Set lane numbers = 4 lane |  |  |
| 0x04,0x80,0x03,0x31,0x33, |  |  |
| // Swap stream ID to have pipe Z stream video out as X |  |  |
| 0x04,0x80,0x00,0x53,0x12, |  |  |
| 0x04,0x80,0x00,0x57,0x11, |  |  |
| 0x04,0x80,0x00,0x5B,0x10, |  |  |
| 0x04,0x80,0x00,0x5F,0x13, |  |  |
| /* ---------------- Test Method --------------------- |  |  |
| - Check VIDEO_LOCK on pipe 0 (bit0 of 0x1DC) is asserted; |  |  |
| - Check VPRBS_ERR on pipe 0 (0x1DB) is reporting errors since pipe 0 is expecting PRBS7; |  |  |
| - Check VIDEO_LOCK on pipe 1 (bit0 of 0x1FC) is asserted; |  |  |
| - Check VPRBS_ERR on pipe 1 (0x1FB) has no errors since PRBS24 is being generated and checked; |  |  |
| - Enable ERRG_EN_A on MAX9295A (bit4 of 0x29) to insert errors on GMSL link A directly; |  |  |
| - Check both pipe 0 and 1 (0x1DB/0x1FB) are reporting errors now. |  |  |
| *****************************************************/ |  |  |
|  | Pass |  |

## SM2_TC_1-8

| Optional Safety Measure |  |
|---|---|
| SM2=Line fault detection on GMSL Pins |  |
| Safety Measure Goal: To ensure that Line Fault events can be detected |  |
| SIOA+/-, SIOB+/-, SIOC+/-, SIOD+/- Short to Battery |  |
| Hardware Setup |  |
| MAX9295A or any GMSL2 serializer has LF resistor Rpd populated; |  |
| MAX96712 DUT has LF Rext populated and connected to corresponding GPIOs (check DS) |  |
| Establish GMSL2 Link Between MAX9295A/MAX96712 |  |
| Configuration |  |
| Enable Line Fault Monitoring for all channels |  |
| 0xE0 = 0xFF |  |
| Fault Injection to SIOA+/-, SIOB+/-, SIOC+/-, SIOD+/- (Short to Battery) |  |
| Connect SIOA+/-, SIOB+/-, SIOC+/-, SIOD+/- to VDD |  |
| Verification |  |
| Read ERRB for errors |  |
| Read LFM registers on DUT link(s) and compare readings with decode table |  |
| 0xE1 - 0xE4 |  |
| Remove Fault Injection |  |
| Verify ERRB and LFM register is cleared |  |
|  | Pass |

## SM2_TC_9-16

| Optional Safety Measure |  |
|---|---|
| SM2=Line fault detection on GMSL Pins |  |
| Safety Measure Goal: To ensure that Line Fault events can be detected |  |
| SIOA+/-, SIOB+/-, SIOC+/-, SIOD+/- Short to GND |  |
| Hardware Setup |  |
| MAX9295A or any GMSL2 serializer has LF resistor Rpd populated; |  |
| MAX96712 DUT has LF Rext populated and connected to corresponding GPIOs (check DS) |  |
| Establish GMSL2 Link Between MAX9295A/MAX96712 |  |
| Configuration |  |
| Enable Line Fault Monitoring for all channels |  |
| 0xE0 = 0xFF |  |
| Fault Injection to SIOA+/-, SIOB+/-, SIOC+/-, SIOD+/- (Short to GND) |  |
| Connect SIOA+/-, SIOB+/-, SIOC+/-, SIOD+/- to GND |  |
| Verification |  |
| Read ERRB for errors |  |
| Read LFM registers on DUT link(s) and compare readings with decode table |  |
| 0xE1 - 0xE4 |  |
| Remove Fault Injection |  |
| Verify ERRB and LFM register is cleared |  |
|  | Pass |

## SM2_TC_17-24

| Optional Safety Measure |  |
|---|---|
| SM2=Line fault detection on GMSL Pins |  |
| Safety Measure Goal: To ensure that Line Fault events can be detected |  |
| SIOA+/-, SIOB+/-, SIOC+/-, SIOD+/- Line open |  |
| Hardware Setup |  |
| MAX9295A or any GMSL2 serializer has LF resistor Rpd populated; |  |
| MAX96712 DUT has LF Rext populated and connected to corresponding GPIOs (check DS) |  |
| Establish GMSL2 Link Between MAX9295A/MAX96712 |  |
| Configuration |  |
| Enable Line Fault Monitoring for all channels |  |
| 0xE0 = 0xFF |  |
| Fault Injection to SIOA+/-, SIOB+/-, SIOC+/-, SIOD+/- (Line open) |  |
| Open SIOA+/-, SIOB+/-, SIOC+/-, SIOD+/- |  |
| Verification |  |
| Read ERRB for errors |  |
| Read LFM registers on DUT link(s) and compare readings with decode table |  |
| 0xE1 - 0xE4 |  |
| Remove Fault Injection |  |
| Verify ERRB and LFM register is cleared |  |
|  | Pass |

## SM2_TC_25-28

| Optional Safety Measure |  |
|---|---|
| SM2=Line fault detection on GMSL Pins |  |
| Safety Measure Goal: To ensure that Line Fault events can be detected |  |
| SIOA+/SIOA-, SIOB+/SIOB-, SIOC+/SIOC-, SIOD+/SIOD- line to line short |  |
| Hardware Setup |  |
| MAX9295A or any GMSL2 serializer has LF resistor Rpd populated; |  |
| MAX96712 DUT has LF Rext populated and connected to corresponding GPIOs (check DS) |  |
| Establish GMSL2 Link Between MAX9295A/MAX96712 in STP link |  |
| Configuration |  |
| Enable Line Fault Monitoring for all channels |  |
| 0xE0 = 0xFF |  |
| Fault Injection (Line Short in Twisted Pair Mode) |  |
| Short SIOA+/SIOA-, SIOB+/SIOB-, SIOC+/SIOC-, SIOD+/SIOD- |  |
| Verification |  |
| Read ERRB for errors |  |
| Read LFM registers on DUT link(s) and compare readings with decode table |  |
| 0xE1 - 0xE4 |  |
| Remove Fault Injection |  |
| Verify ERRB and LFM register is cleared |  |
|  | Pass |

## SM3_TC1

| Default Safety Measure |  |  |  |
|---|---|---|---|
| SM3=CRC for Control Channel, GPIO Forward Channel CRC |  |  |  |
| Safety Measure Goal: Ensure that low bandwidth control channel is covered by CRC |  |  |  |
| GPIO Forward CRC |  |  |  |
|  | CRC_EN bits of both sides should match, otherwise it's invalid settings. However, CRC_EN mismatches may still get GPIO to work, in which TX sends GPIO packet with CRC enabled, but RX disables CRC so doesn't check for CRC. |  |  |
|  | MAX9295A connected to MAX96712 Link A |  |  |
| Step | Action | Register Value |  |
| Setup | Power up and access MAX9295A through I2C/UART locally; |  |  |
|  | Ser MAX9295A GPIO0 as TX | 0x2BE=0x83 |  |
|  | Des MAX96712 GPIO0 (Link A) as RX | 0x300=0x04 |  |
|  | Feed 1kHz signal on MAX9295A GPIO0 |  |  |
|  | Turn on GPIO CRC | Default |  |
| Verify | Observe GPIO signal is forwarded to MAX96712 GPIO0 |  |  |
|  | Turn off GPIO TX_CRC_EN at MAX9295A | 0x90=0x70 |  |
|  | Observe ERRB bar is low; |  |  |
|  | Observe Re-transmission count is overflow at MAX9295A; | 0x97=0xFF |  |
|  | Observe GPIO signal is no longer forwarding. |  |  |
|  |  |  | Pass |

## SM3_TC2

| Default Safety Measure |  |  |  |
|---|---|---|---|
| SM3=CRC for Control Channel, GPIO Forward Channel CRC |  |  |  |
| Safety Measure Goal: Ensure that low bandwidth control channel is covered by CRC |  |  |  |
| GPIO Reverse CRC |  |  |  |
|  | CRC_EN bits of both sides should match, otherwise it's invalid settings. However, CRC_EN mismatches may still get GPIO to work, in which TX sends GPIO packet with CRC enabled, but RX disables CRC so doesn't check for CRC. |  |  |
|  | MAX9295A connected to MAX96712 Link A |  |  |
| Step | Action | Register Value |  |
| Setup | Power up and access MAX96712 through I2C/UART locally; |  |  |
|  | Des MAX96712 GPIO0 (Link A) as TX | Default |  |
|  | Ser MAX9295a as RX | Default |  |
|  | Feed 1kHz signal on MAX96712 GPIO0 |  |  |
|  | Turn on GPIO CRC | Default |  |
| Verify | Observe GPIO signal is forwarded to MAX9295A GPIO0 |  |  |
|  | Turn off GPIO TX_CRC_EN at MAX96712 Link A | 0xA0=0x70 |  |
|  | Observe ERRB bar is low; |  |  |
|  | Observe Re-transmission count is overflow at MAX96712; | 0xA7=0xFF |  |
|  | Observe GPIO signal is no longer forwarding. |  |  |
|  |  |  | Pass |

## SM3_TC3

| Default Safety Measure |  |  |  |
|---|---|---|---|
| SM3=CRC for Control Channel, SPI Forward Channel CRC |  |  |  |
| Safety Measure Goal: Ensure that low bandwidth control channel is covered by CRC |  |  |  |
| SPI Forward CRC |  |  |  |
|  | CRC_EN bits of both sides should match, otherwise it's invalid settings. However, CRC_EN mismatches may still get SPI to work, in which TX sends SPI packet with CRC enabled, but RX disables CRC so doesn't check for CRC. |  |  |
|  | MAX9295A connected to MAX96712 Link A |  |  |
| Step | Action | Register Value |  |
| Setup | Power up and access MAX9295A through I2C/UART locally |  |  |
|  | Have SPI communication from Ser to Des |  |  |
|  | Turn on SPI CRC | Default |  |
| Verify | Observe normal operation |  |  |
|  | Turn off SPI TX_CRC_EN at MAX9295A | 0x80=0x70 |  |
|  | Observe ERRB bar is low; |  |  |
|  | Observe Re-transmission count is overflow at MAX9295A; | 0x87=0xFF |  |
|  | Observe SPI communication is break. |  |  |
|  |  |  | Pass |

## SM3_TC4

| Default Safety Measure |  |  |  |  |
|---|---|---|---|---|
| SM3=CRC for Control Channel, SPI Reverse Channel CRC |  |  |  |  |
| Safety Measure Goal: Ensure that low bandwidth control channel is covered by CRC |  |  |  |  |
| SPI Reverse CRC |  |  |  |  |
|  | CRC_EN bits of both sides should match, otherwise it's invalid settings. However, CRC_EN mismatches may still get SPI to work, in which TX sends SPI packet with CRC enabled, but RX disables CRC so doesn't check for CRC. |  |  |  |
|  | MAX9295A connected to MAX96712 Link A |  |  |  |
| Step | Action | Register Value |  |  |
| Setup | Power up and access MAX96712 through I2C/UART locally |  |  |  |
|  | Have SPI communication from Des to Ser |  |  |  |
|  | Turn on SPI CRC | Default |  |  |
| Verify | Observe normal operation |  |  |  |
|  | Turn off SPI TX_CRC_EN at MAX96712 | 0x80/0x90=0x70 | SPI1/SPI2 |  |
|  | Observe ERRB bar is low; |  |  |  |
|  | Observe Re-transmission count is overflow at MAX96712; | 0x87/0x97=0xFF | SPI1/SPI2 |  |
|  | Observe SPI communication is break. |  |  |  |
|  |  |  |  | Pass |

## SM3_TC5

| Default Safety Measure |  |  |  |
|---|---|---|---|
| SM3=CRC for Control Channel, I2C Forward Channel CRC |  |  |  |
| Safety Measure Goal: Ensure that low bandwidth control channel is covered by CRC |  |  |  |
| Control Channel I2C or UART Forward CRC |  |  |  |
|  | CRC_EN bits of both sides should match, otherwise it's invalid settings and won't work. |  |  |
|  | MAX9295A connected to MAX96712 Link A |  |  |
| Step | Action | Register Value |  |
| Setup | Power up and access MAX9295A through I2C/UART locally |  |  |
|  | Accessing MAX96712 remotely |  |  |
|  | Turn on CC CRC | Default |  |
| Verify | Observe normal operation |  |  |
|  | Turn off CC TX_CRC_EN at MAX9295A | 0x88=0x70 |  |
|  | Observe ERRB bar is low; |  |  |
|  | Observe Re-transmission count is overflow at MAX9295A; | 0x8F=0xFF |  |
|  | Observe control channel I2C/UART is break talking to remote. |  |  |
|  |  |  | Pass |

## SM3_TC6

| Default Safety Measure |  |  |  |
|---|---|---|---|
| SM3=CRC for Control Channel, I2C Forward Channel CRC |  |  |  |
| Safety Measure Goal: Ensure that low bandwidth control channel is covered by CRC |  |  |  |
| Control Channel I2C or UART Reverse CRC |  |  |  |
|  | CRC_EN bits of both sides should match, otherwise it's invalid settings and won't work. |  |  |
|  | MAX9295A connected to MAX96712 Link A |  |  |
| Step | Action | Register Value |  |
| Setup | Power up and access MAX96712 through I2C/UART locally |  |  |
|  | Accessing MAX9295A remotely |  |  |
|  | Turn on CC CRC | Default |  |
| Verify | Observe normal operation |  |  |
|  | Turn off CC TX_CRC_EN at MAX96712 Link A | 0x500=0x70 |  |
|  | Observe ERRB bar is low; |  |  |
|  | Observe Re-transmission count is overflow at MAX96712; | 0x507=0xFF |  |
|  | Observe control channel I2C/UART is break talking to remote. |  |  |
|  |  |  | Pass |

## SM4_TC1

| Default Safety Measure |  |
|---|---|
| SM4=CRC for Forward Video Channel |  |
| Safety Measure Goal: Used to evaluate Line CRC Errors for Forward Video Channel (Evaluated at DES) |  |
| Forward Channel Line CRC |  |
| LINE_CRC_EN bits of both sides should match, otherwise it's invalid settings and won't work. |  |
| // HW, MAY 2018 |  |
| // SM4_TC_1 Forward LCRC Setup |  |
| // MAX9295A (Pattern Gen) -> MAX96712 (DUT) |  |
| // MAX9295A MFP2 and MFP0 connected |  |
| // User can use other video source instead of the Pattern gen inside MAX9295A |  |
| // ---------------- MAX96712 (DUT) setup --------------------- |  |
| // Link A only GMSL2 |  |
| 0x04,0x52,0x00,0x06,0xF1, |  |
| // Pipe |  |
| 0x04,0x52,0x00,0xF0,0x04, |  |
| // MIPI |  |
| 0x04,0x52,0x04,0x15,0x26, |  |
| 0x04,0x52,0x04,0x18,0x26, |  |
| 0x04,0x52,0x08,0xA0,0x04, |  |
| 0x04,0x52,0x08,0xA3,0xE4, |  |
| 0x04,0x52,0x08,0xA4,0xE4, |  |
| // ---------------- MAX9295A (Pattern Gen 1920x1200) setup --------------------- |  |
| // Pattern Generator Settings |  |
| 0x04,0x80,0x01,0xC9,0x19, |  |
| // Set VS Delay |  |
| 0x04,0x80,0x01,0xCA,0x00, |  |
| 0x04,0x80,0x01,0xCB,0x00, |  |
| 0x04,0x80,0x01,0xCC,0x00, |  |
| // Set VS High |  |
| 0x04,0x80,0x01,0xCD,0x00, |  |
| 0x04,0x80,0x01,0xCE,0x1F, |  |
| 0x04,0x80,0x01,0xCF,0x94, |  |
| // Set VS Low |  |
| 0x04,0x80,0x01,0xD0,0x26, |  |
| 0x04,0x80,0x01,0xD1,0x05, |  |
| 0x04,0x80,0x01,0xD2,0xF5, |  |
| // Set HS Delay |  |
| 0x04,0x80,0x01,0xD3,0x00, |  |
| 0x04,0x80,0x01,0xD4,0xEC, |  |
| 0x04,0x80,0x01,0xD5,0x94, |  |
| // Set HS High |  |
| 0x04,0x80,0x01,0xD6,0x07, |  |
| 0x04,0x80,0x01,0xD7,0xDB, |  |
| // Set HS Low |  |
| 0x04,0x80,0x01,0xD8,0x00, |  |
| 0x04,0x80,0x01,0xD9,0x0A, |  |
| // Set HS Cnt |  |
| 0x04,0x80,0x01,0xDA,0x04, |  |
| 0x04,0x80,0x01,0xDB,0xD5, |  |
| // Set V2D |  |
| 0x04,0x80,0x01,0xDC,0x00, |  |
| 0x04,0x80,0x01,0xDD,0xEC, |  |
| 0x04,0x80,0x01,0xDE,0xD6, |  |
| // Set DE High |  |
| 0x04,0x80,0x01,0xDF,0x07, |  |
| 0x04,0x80,0x01,0xE0,0x80, |  |
| // Set DE Low |  |
| 0x04,0x80,0x01,0xE1,0x00, |  |
| 0x04,0x80,0x01,0xE2,0x65, |  |
| // Set DE Cnt |  |
| 0x04,0x80,0x01,0xE3,0x04, |  |
| 0x04,0x80,0x01,0xE4,0xB0, |  |
| // Enable pattern gen [1:0], 2b01 = checkerboard, 2b10 = color gradient |  |
| 0x04,0x80,0x01,0xE5,0x01, |  |
| // Set color gradient increment |  |
| 0x04,0x80,0x01,0xE6,0x06, |  |
| // Set color depth for checkerboard |  |
| 0x04,0x80,0x01,0xE7,0x80, |  |
| 0x04,0x80,0x01,0xE8,0x00, |  |
| 0x04,0x80,0x01,0xE9,0x04, |  |
| 0x04,0x80,0x01,0xEA,0x00, |  |
| 0x04,0x80,0x01,0xEB,0x08, |  |
| 0x04,0x80,0x01,0xEC,0x80, |  |
| 0x04,0x80,0x01,0xED,0x50, |  |
| 0x04,0x80,0x01,0xEE,0xA0, |  |
| 0x04,0x80,0x01,0xEF,0x50, |  |
| 0x04,0x80,0x01,0xC8,0xE3, |  |
| // Done Pattern gen setting |  |
| // Parallel mode and PCLK input enable |  |
| 0x04,0x80,0x00,0x07,0xF7, // MFP0 - PCLK input |  |
| // Connect MFP2 to MFP0 if using internal PCLK. Otherwise feed external clock on MFP0 and comment out below. |  |
| // Enable PCLK output |  |
| 0x04,0x80,0x00,0x06,0xBF, |  |
| // MFP2 - ref clock out |  |
| 0x04,0x80,0x00,0x03,0x07, |  |
| // Set ref PLL clock = 74.25MHz | Pass |
| 0x04,0x80,0x03,0xF0,0x71, |  |
| // Optional Setup for visual check |  |
| // ---------------- oLDI deserializer setup --------------------- |  |
| //0x04,0x94,0x01,0xCE,0x5F, |  |
| // ---------------- MAX9295A setup --------------------- |  |
| //0x04,0x84,0x00,0x53,0x12, |  |
| //0x04,0x84,0x00,0x57,0x11, |  |
| //0x04,0x84,0x00,0x5B,0x10, |  |
| //0x04,0x84,0x00,0x5F,0x13, |  |
| /* ---------------- Test Method --------------------- |  |
| 1. LCRC is by default enabled (per video pipe based): |  |
| Bit 1 (LINE_CRC_EN) of 0x100/0x112/0x124/0x136/0x148/0x160/0x172/0x184 |  |
| 2. LCRC ERR is by default enabled for ERRB: |  |
| Bit 3 (LCRC_ERR_OEN) of 0x29 |  |
| Procedures: |  |
| - Establish the link; |  |
| - Apply forward video (through Pattern Gen from Ser in this example); |  |
| - Enable LINE_CRC_EN and LCRC_ERR_OEN (by default on); |  |
| - Inject error from Ser MAX9295A (ERRG_EN_A): |  |
| 0x29 = 0x10 |  |
| - Check LCRC_ERR that is asserted on video pipe (pipe 1 in this example): |  |
| Bit 7 of 0x112 |  |
| - Check LCRC_ERR_FLAG that is asserted: |  |
| Bit 3 of 0x2A |  |
| - Check ERROR bit that is asserted and ERRB pin goes low: |  |
| Bit 2 of 0x1A; |  |
| *****************************************************/ |  |

## SM4_TC2

| Default Safety Measure |  |
|---|---|
| SM4=CRC for GMSL Link Pixel Mode |  |
| Safety Measure Goal: Used to evaluate pixel CRC Errors of GMSL link (Evaluated at DES) |  |
| Forward Channel Packet CRC |  |
| TX/RX_CRC_EN__ bits of both sides should match, otherwise it's invalid settings and won't work. |  |
| Software Configuration |  |
| Enable TX_CRC_EN on Ser. (e.g. 0x50 bit 7 in MAX9295A for pipe X) |  |
| Enable RX_CRC_EN_x on MAX96712 accordingly. (e.g. 0x60 bit 0 in MAX96712 for Link A pipe X) |  |
| *0x60 for port A/B; 0x61 for port C/D |  |
| Enable Video Pixel CRC error counter interupt output to ERRB. (default on) |  |
| 0x44 bit[3:0] |  |
| Fault Injection |  |
| Enable ERRG on serializer |  |
| e.g. MAX9295A 0x2A = 0x30; 0x29 = 0x10 to enable ERRG port A |  |
| Verification |  |
| VID_PXL_CRC_ERR_A/B/C/D flags for each link |  |
| 0x45 bit[3:0] |  |
| Total # of video pixel CRC errors detected on each pipe from each link |  |
| VID_PXL_CRC_ERR_AX/Y/Z/U |  |
| VID_PXL_CRC_ERR_BX/Y/Z/U |  |
| VID_PXL_CRC_ERR_CX/Y/Z/U |  |
| VID_PXL_CRC_ERR_DX/Y/Z/U |  |
| refer to register 0x11D0 - 0x11EC |  |
|  | Pass |

## SM5_TC1

| Default Safety Measure |  |
|---|---|
| SM5=Error correction through re-transmission of control channel |  |
| Safety Measure Goal: If error occurs on low bandwidth control channel, device will re-transmit packet. |  |
| Error Correction Through Re-transmission |  |
| Hardware Setup |  |
| 0.Preapare a MAX9295A or any GMSL2 serializer, and MAX96712 DUT. |  |
| 1. Have I2C access to MAX96712 locally. |  |
| 2.Establish GMSL2 Link Between MAX9295A and MAX96712 (Link A) error-free. |  |
| - Check ERRB pin and LOCK pin or register 0x1A bit 3 on MAX96712 |  |
| 3. Apply 10k square wave at MAX96712 MFP0 (for testing purpose). |  |
| - Check MAX9295A MFP0 on scope is forwarding the signal |  |
| Software Configuration |  |
| ARQ is by default on. |  |
| GPIO0 is by default forwarding. |  |
| To customize Link A GPIO ARQ settings: |  |
| 0xA6 = 0x12, # Enable MAX_RT_ERR_OEN (to ERRB) and lower MAX_RT for Link A GPIO |  |
| To customize Link A CC ARQ settings: |  |
| 0x506 = 0x12, # Enable MAX_RT_ERR_OEN (to ERRB) and lower MAX_RT for Link A CC |  |
| 0x2D = 0x01, # Enable MAX_RT_ERR_OEN_A (to ERRB) for link A in general |  |
| *if 0x2D bit 4 is set, one single RT on Link A will trig the ERRB output; Work together with GPIO or CC ARQ1 bit 0 |  |
| Fault Injection |  |
| Enable ERRG in MAX96712 Link A: |  |
| 0x1002 = 0x18, # Increase ERRG_BURST to 8; Increase ERRG_RATE to 1/81920 bits |  |
| 0x1001 = 0x10, # Enable ERRG |  |
| Verification |  |
| Read 0xA7 and check Link A GPIO re-transmission counter is increasing; |  |
| Read 0x507 and check Link A CC re-transmission counter is increasing if keep having i2c activities (may need to adjust ERRG_RATE); |  |
| Read 0x2E bit 4 and check Link A re-transmission flag is asserted; |  |
| Observe the forwarded GPIO signal on MAX9295A MFP0 is still in good shape; |  |
| Observe the I2C control channel is still working as usual. |  |
| After tens sec, or depending on ERRG_RATE and activities: |  |
| Observe ERRB pin goes low (ERRB LED on if applicable); |  |
| Read 0x2E bit 0 and check Link A max RT flag is also asserted; |  |
| *MAX_RT_ERR (0xA7 bit7, read and clean) has been reached once. |  |
| Forwared GPIO signal on MAX9295A MFP0 may be corrupted or distorted once when MAX RT is reached; |  |
| I2C may break once when MAX RT is reached. |  |
| Remove ARQ |  |
| If GPIO ARQ is removed from either side, the forwarded GPIO signal on MAX9295A MFP0 will be corrupted or distorted. |  |
| If CC ARQ is removed from either side, the I2C will break. |  |
| To disable MAX9295A GPIO ARQ: 0x95 bit 3 = 0 |  |
| To disable MAX96712 LinkA GPIO ARQ: 0xA5 bit 3 = 0 |  |
|  | Pass |

## SM6_TC1

| Default Safety Measure |  |
|---|---|
| SM6=LOCK indicator of Forward Channel |  |
| Safety Measure Goal: Verify that GMSL link can be established, and LOCK pin goes high. |  |
| Lock Indicator of Forward Channel |  |
| Notes:  1) Setup a link between MAX9295A and MAX96712 and verify link is LOCKED. |  |
| Hardware Setup |  |
| Preapare a MAX9295A or any GMSL2 serializer, and MAX96712 DUT. |  |
| Have I2C access to MAX96712 locally. |  |
| Software Configuration |  |
| 0x06[3:0] each bit is to enable Link D/C/B/A |  |
| 0x06[7:4] each bit is to select GMSL1 or 2 for each link |  |
| 0x10/0x11 to set link rate for each link (Tx/Rx rate) |  |
| *Link mode and rate can also be set up at CFG pins during power up |  |
| *Refer to register map or programming guide for details |  |
| Paired serializer to have same link mode and rate |  |
| Verification |  |
| If Link A is locked, 0x1A bit 3 will asserted; |  |
| If Link B is locked, 0x0A bit 3 will asserted; |  |
| If Link C is locked, 0x0B bit 3 will asserted; |  |
| If Link D is locked, 0x0C bit 3 will asserted; |  |
| If all enabled link(s) are locked, LOCK Pin will drive high. |  |
| *Same for the seralizer side. |  |
| Fault Injection |  |
| If change forward link rate on either serializer (Tx rate) or deserializer (Rx rate) side only followed by link reset, the link will lose lock due to link rate mismatch. And LOCK Pin goes low. |  |
|  | Pass |

## SM7_TC1

| Default Safety Measure |  |
|---|---|
| SM7=ERRB indicator of Forward Channel |  |
| Safety Measure Goal: Verify that if there is an error on the link the DES ERRB pin will be active. |  |
| ERRB Indicator of Forward Channel |  |
| Notes:  1) Setup a link between MAX9295A and MAX96712 and verify link is LOCKED. 2) Forward channel errors are reported on the DES. |  |
| Hardware Setup |  |
| Preapare a MAX9295A or any GMSL2 serializer, and MAX96712 DUT. |  |
| Have I2C access to MAX96712 locally. |  |
| Verification |  |
| If Link A is locked, 0x1A bit 3 will asserted; |  |
| If Link B is locked, 0x0A bit 3 will asserted; |  |
| If Link C is locked, 0x0B bit 3 will asserted; |  |
| If Link D is locked, 0x0C bit 3 will asserted; |  |
| If all enabled link(s) are locked, LOCK Pin will drive high; ERRB Pin stays low. |  |
| *Same for the seralizer side. |  |
| Fault Injection |  |
| Turn on ERRG on seralizer to assert errors, MAX96712 ERRB pin will output low (ERROR register bit asserts). |  |
|  | Pass |

## SM8_TC1

| Optional Safety Measure |  |
|---|---|
| SM8=LOCK indicator of Reverse Channel |  |
| Safety Measure Goal: Verify that GMSL link can be established, and LOCK pin goes high. |  |
| Lock Indicator of Reverse Channel |  |
| Notes:  1) Setup a link between MAX9295A and MAX96712 and verify link is LOCKED. |  |
| Hardware Setup |  |
| Preapare a MAX9295A or any GMSL2 serializer, and MAX96712 DUT. |  |
| Have I2C access to MAX96712 locally. |  |
| Software Configuration |  |
| 0x06[3:0] each bit is to enable Link D/C/B/A |  |
| 0x06[7:4] each bit is to select GMSL1 or 2 for each link |  |
| 0x10/0x11 to set link rate for each link (Tx/Rx rate) |  |
| *Link mode and rate can also be set up at CFG pins during power up |  |
| *Refer to register map or programming guide for details |  |
| Paired serializer to have same link mode and rate |  |
| Verification |  |
| If Link A is locked, 0x1A bit 3 will asserted; |  |
| If Link B is locked, 0x0A bit 3 will asserted; |  |
| If Link C is locked, 0x0B bit 3 will asserted; |  |
| If Link D is locked, 0x0C bit 3 will asserted; |  |
| If all enabled link(s) are locked, LOCK Pin will drive high. |  |
| *Same for the seralizer side. |  |
| Fault Injection |  |
| If change forward link rate on either serializer (Tx rate) or deserializer (Rx rate) side only followed by link reset, the link will lose lock due to link rate mismatch. And LOCK Pin goes low. |  |
|  | Pass |

## SM9_TC1

| Optional Safety Measure |  |
|---|---|
| SM9=ERRB indicator of Reverse Channel |  |
| Safety Measure Goal: Verify that if there is an error on the link the DES ERRB pin will be active. |  |
| ERRB Indicator of Forward Channel |  |
| Notes:  1) Setup a link between MAX9296A and MAX96712 and verify link is LOCKED. 2) Reverse channel errors are reported on the SER. |  |
| ERRB Indicator of Reverse Channel |  |
| Hardware Setup |  |
| Preapare a MAX9295A or any GMSL2 serializer, and MAX96712 DUT. |  |
| Have I2C access to MAX96712 locally. |  |
| Verification |  |
| If Link A is locked, 0x1A bit 3 will asserted; |  |
| If Link B is locked, 0x0A bit 3 will asserted; |  |
| If Link C is locked, 0x0B bit 3 will asserted; |  |
| If Link D is locked, 0x0C bit 3 will asserted; |  |
| If all enabled link(s) are locked, LOCK Pin will drive high; ERRB Pin stays low. |  |
| *Same for the seralizer side. |  |
| Fault Injection |  |
| Turn on ERRG on MAX96712 to assert errors, MAX9295A ERRB pin will output low (ERROR register bit asserts). |  |
| *0x1001/0x1011/0x1021/0x1031 to enable ERRG on Link A/B/C/D |  |
| *MAX9295A 0x05 = 0xC0 to enable ERRB and LOCK output |  |
|  | Pass |

## SM10_TC1

| Optional Safety Measure |  |
|---|---|
| SM10=Error Generator |  |
| Safety Measure Goal: Verify that when DES sends errors on the reverse channel the SER will see errors and report to ERRB. |  |
| Notes:  1) Setup a link between MAX9295A and MAX96712 and verify link is LOCKED. 2) Enabling error generator on the DES will inject errors on the SER. And enabling error generator on the SER will inject errors on the DES |  |
| Error Generator |  |
| Hardware Setup |  |
| 0.Preapare a MAX9295A with MAX96712 |  |
| 1. Have I2C access to MAX96712 locally. |  |
| 2.Establish GMSL2 Link Between MAX9295A and MAX96712 (Link A) error-free. |  |
| - Check ERRB pin and LOCK pin on Ser or Des |  |
| Software Configuration |  |
| For FWD channel, enable ERRG in MAX9295A: |  |
| 0x29 bit 4 to enable ERRG on link A |  |
| 0x2A to config ERRG burst length, error rate and error counts |  |
| For Back channel, enable ERRG in MAX96712 |  |
| 0x1001/0x1011/0x1021/0x1031 bit 4 to enable ERRG on link A/B/C/D |  |
| 0x1002/0x1012/0x1022/0x1032 to config ERRG burst length, error rate and error counts |  |
| Verification |  |
| - For back channel |  |
| ERRB goes low; |  |
| 0x1A bit 2 ERROR asserts on MAX96712; |  |
| 0x26[3:0] DEC_ERR_FLAG asserts on enabled link; |  |
| 0x2C[3:0] IDLE_ERR_FLAG asserts on enabled link. |  |
| - For back channel |  |
| ERRB goes low; |  |
| 0x1A bit 2 ERROR asserts on MAX96712; |  |
| 0x26[3:0] DEC_ERR_FLAG asserts on enabled link; |  |
| 0x2C[3:0] IDLE_ERR_FLAG asserts on enabled link. |  |
|  | Pass |

## SM11_TC1

| Optional Safety Measure |  |
|---|---|
| SM11=Video Sequence Number |  |
| Safety Measure Goal: Sequence number is added to any video packet, this safety mechanism can be used to detect frame loss or dropped video packets. |  |
| Video Sequence Number |  |
| Notes:  1) Setup a link between MAX96717 and MAX96716 and verify link is LOCKED. |  |
| A sequence number is added to any video packet, this safety mechanisms can be used to detect frame loss or insertion. |  |
| This SM requires a valid MIPI video data through the SerDes link |  |
| Verification - on DUT MAX96712 |  |
| When error occurs, VIDEO_RX8, bit 4, VID_SEQ_ERR would assert; This register is per video pipe based. |  |
| Additionally, Line CRC error will trigger and so is ERRB pin; Refer SM4. |  |
| Fault Injection |  |
| Enable SEQ_MISS_EN bit for desired pipe, e.g 0x100 bit 4 for pipe 0; |  |
| Turn on ERRG on MAX96712 to assert errors, MAX9295A ERRB pin will output low (ERROR register bit asserts). |  |
|  | Pass |

## SM12_TC1

| Default Safety Measure |  |  |  |
|---|---|---|---|
| SM12=Acknowledge of UART or I2C |  |  |  |
| Safety Measure Goal: To ensure that uC that programs the SerDes devices has the ability to recognize ACK's vs. NAK's. This does not have to deal with the SerDes devices, but rather the overall communication protocol. If NAK occurs, SoC should act accordingly. |  |  |  |
| Notes:  1) Setup a link between MAX9295A and MAX96712 |  |  |  |
| Acknowledge of UART or I2C |  |  |  |
| Hardware Setup |  |  |  |
| MAX96712 is connecting to master MCU/SoC |  |  |  |
| Slave device (0x52) is responding to master under I2C protocol |  |  |  |
| I2C Write 0x0006 = 0xF1 |  |  |  |
| I2C Read 0x0006 = 0xF1 |  |  |  |
| Slave device (0x52) is responding to master under I2C protocol | 0x79 | UART sync word |  |
| UART Write 0x0006 = 0xF1 | 0xC3 | UART ACK word |  |
| UART Read 0x0006 = 0xF1 |  |  |  |
|  |  |  | Pass |

## SM13_TC1

| Optional Safety Measure |  |
|---|---|
| SM13_TC1= Generator of Watermark |  |
| Safety Goal- A watermark sequence is optionally generated at the serializer/deserializer, which is evaluated at the deserializer/serializer |  |
| Note- MAX96712 can be used as watermark generator or checker, this feature can only be used with parts that support watermarking. MAX96717/93 do not support watermark feature. |  |
| Generator of Watermark |  |
| Note- MAX96712 can be used as watermark generator or checker, this feature can only be used with parts that support watermarking. MAX96717/93 do not support watermark feature. |  |
| Watermarking feature is only supported on pipes 0 and 4 on MAX96712, for datatypes RGB888 and YUV444 |  |
| Hardware Setup |  |
| HDMI - MAX96751/777 - MAX96712(Watermark Gen on pipe 0 and 4)-MAX9295A - MAX96752/780(Watermark Det) - Display |  |
| * Watermark is designed mainly for RGB888 |  |
| Software Configuration |  |
| .csv Script attached below |  |
| Verfification |  |
| Read 0x18D bit 1 (WM_DETOUT) asserts on MAX96752; |  |
| Observe no difference visually on display pannel; |  |
| If image frozen, WM_DETOUT cleans. |  |
| Script |  |
| # This script must be run AFTER all devices are linked up,, |  |
| # Reset all |  |
| 0x84,0x10,0x91 |  |
| 0x52,0x13,0x75 |  |
| 0x80,0x10,0x81 |  |
| 0x90,0x10,0x91 |  |
| # |  |
| # |  |
| # ------------ MAX96752 Setup -------------- |  |
| # Set up dual oLDI output,, |  |
| 0x90,0x01CE,0x5F |  |
| # VID_INFO_MAN to a 1,, |  |
| 0x90,0x100,0x3B |  |
| # RX BPP to 24 (0x18) for RGB888 and RX encoding mode to 2,, |  |
| 0x90,0x109,0x98 |  |
| # RX FB_DIV,, |  |
| 0x90,0x10A,0x28 |  |
| # RX FB_DIV_FRAC,, |  |
| 0x90,0x10B,0x00 |  |
| # RX VID_ODIV_L,, |  |
| 0x90,0x10C,0x12 |  |
| # Speed Det (Speed_lim),, |  |
| 0x90,0x10E,0x40 |  |
| # |  |
| # ------------ MAX9295A Setup -------------- |  |
| # Disable PRBS test mode |  |
| 0x80,0x370,0x08 |  |
| # Set MIPI port configuration - 1x4 mode |  |
| 0x80,0x330,0x00 |  |
| # Lane Mapping - turn on all lanes on CTRL 0 and 1 |  |
| 0x80,0x331,0x33 |  |
| # Controller to Pipe Mapping |  |
| # |  |
| # Enable all video pipelines from used CSI input port (start_portax/y/z/u = 0, start_portbx/y/z/u = 1, clk_selx/y/z/u = 1 ) |  |
| 0x80,0x0311,0xF0 |  |
| 0x80,0x0308,0x7F |  |
| # |  |
| # Route RGB888 DT=0x24 to VIDEO_X (MSB enable) |  |
| 0x80,0x0314,0xE4 |  |
| # Unused VIDEO_Y |  |
| 0x80,0x0316,0x62 |  |
| # Unused VIDEO_Z |  |
| 0x80,0x0318,0x62 |  |
| # Unused VIDEO_U |  |
| #0x80,0x031A,0x62 |  |
| # |  |
| # |  |
| # ------------ MAX96712(DUT) Setup --------------,, |  |
| # Turn on PHY A; GMSL2 mode |  |
| 0x52,0x06,0xF1 |  |
| # 0x52,0x06,0xF2 |  |
| # 0x52,0x06,0xF4 |  |
| # 0x52,0x06,0xF8 |  |
| # Set des in 2x4 mode |  |
| 0x52,0x8A0,0x04 |  |
| # Select pipe 0 and 4 to stream PHY A Pipe X |  |
| 0x52,0xF0,0x40 |  |
| #0x52,0xF1,0x62 |  |
| 0x52,0xF2,0x80 |  |
| # 0x52,0xF3,0xE2 |  |
| # Enable Video Pipe 0 and 4 only |  |
| 0x52,0xF4,0x11 |  |
| # |  |
| # Mapping Pipe 0 to Ctrl 1 |  |
| #0x52,0x90B,0x07 |  |
| #0x52,0x92D,0x15 |  |
| #0x52,0x90D,0x24 |  |
| #0x52,0x90E,0x24 |  |
| #0x52,0x90F,0x00 | Pass |
| #0x52,0x910,0x00 |  |
| #0x52,0x911,0x01 |  |
| #0x52,0x912,0x01 |  |
| # |  |
| # Mapping Pipe 4 to Ctrl 1 |  |
| 0x52,0xA0B,0x07 |  |
| 0x52,0xA2D,0x15 |  |
| 0x52,0xA0D,0x24 |  |
| 0x52,0xA0E,0x24 |  |
| 0x52,0xA0F,0x00 |  |
| 0x52,0xA10,0x00 |  |
| 0x52,0xA11,0x01 |  |
| 0x52,0xA12,0x01 |  |
| # |  |
| # Set Lane Mapping |  |
| 0x52,0x8A3,0xE4 |  |
| 0x52,0x8A4,0xE4 |  |
| # Set 4 lanes for deserializer |  |
| 0x52,0x90A,0xC0 |  |
| 0x52,0x94A,0xC0 |  |
| 0x52,0x98A,0xC0 |  |
| 0x52,0x9CA,0xC0 |  |
| # Turn on all PHYs |  |
| 0x52,0x8A2,0xF0 |  |
| # Set Data rate to be 1000Mbps |  |
| 0x52,0x415,0x2A |  |
| 0x52,0x418,0x2A |  |
| #0x52,0x41B,0x2A |  |
| #0x52,0x41E,0x2A |  |
| # Apply Reset for changes ------------------------------------ |  |
| 0x52,0x18,0x0F |  |
| # |  |
| # ------------ MAX96777 Setup --------------,, |  |
| # Script to set up Video Feedthrough HDMI-CSI,, |  |
| # Clean LFLT error,, |  |
| 0x84,0x1A,0x03 |  |
| # Invert VSYNC |  |
| 0x84,0x1C8,0x03 |  |
| # Hot Plug Detect OFF,, |  |
| 0x84,0x20F5,0x00 |  |
| # HDMI_Enable,, |  |
| 0x84,0x01,0x88 |  |
| # Stream select 0 for port A,, |  |
| 0x84,0x53,0x10 |  |
| #,, |  |
| # Load EDID Table for 1920x1200 10in Display; Needed if not using HDMI generator |  |
| # 0x84,0x2E00,0x00 |  |
| # 0x84,0x2E01,0xFF |  |
| # 0x84,0x2E02,0xFF |  |
| # 0x84,0x2E03,0xFF |  |
| # 0x84,0x2E04,0xFF |  |
| # 0x84,0x2E05,0xFF |  |
| # 0x84,0x2E06,0xFF |  |
| # 0x84,0x2E07,0x00 |  |
| # 0x84,0x2E08,0x37 |  |
| # 0x84,0x2E09,0x0D |  |
| # 0x84,0x2E0A,0x20 |  |
| # 0x84,0x2E0B,0x19 |  |
| # 0x84,0x2E0C,0xB0 |  |
| # 0x84,0x2E0D,0xFC |  |
| # 0x84,0x2E0E,0x24 |  |
| # 0x84,0x2E0F,0x01 |  |
| # 0x84,0x2E10,0x01 |  |
| # 0x84,0x2E11,0x1B |  |
| # 0x84,0x2E12,0x01 |  |
| # 0x84,0x2E13,0x03 |  |
| # 0x84,0x2E14,0x81 |  |
| # 0x84,0x2E15,0x16 |  |
| # 0x84,0x2E16,0x0E |  |
| # 0x84,0x2E17,0x78 |  |
| # 0x84,0x2E18,0xEA |  |
| # 0x84,0x2E19,0x2C |  |
| # 0x84,0x2E1A,0xC5 |  |
| # 0x84,0x2E1B,0xA4 |  |
| # 0x84,0x2E1C,0x56 |  |
| # 0x84,0x2E1D,0x50 |  |
| # 0x84,0x2E1E,0xA1 |  |
| # 0x84,0x2E1F,0x28 |  |
| # 0x84,0x2E20,0x0F |  |
| # 0x84,0x2E21,0x50 |  |
| # 0x84,0x2E22,0x54 |  |
| # 0x84,0x2E23,0x00 |  |
| # 0x84,0x2E24,0x00 |  |
| # 0x84,0x2E25,0x00 |  |
| # 0x84,0x2E26,0xD1 |  |
| # 0x84,0x2E27,0x00 |  |
| # 0x84,0x2E28,0x01 |  |
| # 0x84,0x2E29,0x00 |  |
| # 0x84,0x2E2A,0x01 |  |
| # 0x84,0x2E2B,0x00 |  |
| # 0x84,0x2E2C,0x01 |  |
| # 0x84,0x2E2D,0x00 |  |
| # 0x84,0x2E2E,0x01 |  |
| # 0x84,0x2E2F,0x00 |  |
| # 0x84,0x2E30,0x01 |  |
| # 0x84,0x2E31,0x00 |  |
| # 0x84,0x2E32,0x01 |  |
| # 0x84,0x2E33,0x00 |  |
| # 0x84,0x2E34,0x01 |  |
| # 0x84,0x2E35,0x01 |  |
| # 0x84,0x2E36,0xB8 |  |
| # 0x84,0x2E37,0x3D |  |
| # 0x84,0x2E38,0x80 |  |
| # 0x84,0x2E39,0x18 |  |
| # 0x84,0x2E3A,0x71 |  |
| # 0x84,0x2E3B,0xB0 |  |
| # 0x84,0x2E3C,0x2D |  |
| # 0x84,0x2E3D,0x40 |  |
| # 0x84,0x2E3E,0x58 |  |
| # 0x84,0x2E3F,0x2C |  |
| # 0x84,0x2E40,0x45 |  |
| # 0x84,0x2E41,0x00 |  |
| # 0x84,0x2E42,0x13 |  |
| # 0x84,0x2E43,0x2B |  |
| # 0x84,0x2E44,0x21 |  |
| # 0x84,0x2E45,0x00 |  |
| # 0x84,0x2E46,0x00 |  |
| # 0x84,0x2E47,0x1E |  |
| # 0x84,0x2E48,0x00 |  |
| # 0x84,0x2E49,0x00 |  |
| # 0x84,0x2E4A,0x00 |  |
| # 0x84,0x2E4B,0xFD |  |
| # 0x84,0x2E4C,0x00 |  |
| # 0x84,0x2E4D,0x32 |  |
| # 0x84,0x2E4E,0x4C |  |
| # 0x84,0x2E4F,0x1E |  |
| # 0x84,0x2E50,0x53 |  |
| # 0x84,0x2E51,0x11 |  |
| # 0x84,0x2E52,0x00 |  |
| # 0x84,0x2E53,0x0A |  |
| # 0x84,0x2E54,0x20 |  |
| # 0x84,0x2E55,0x20 |  |
| # 0x84,0x2E56,0x20 |  |
| # 0x84,0x2E57,0x20 |  |
| # 0x84,0x2E58,0x20 |  |
| # 0x84,0x2E59,0x20 |  |
| # 0x84,0x2E5A,0x00 |  |
| # 0x84,0x2E5B,0x00 |  |
| # 0x84,0x2E5C,0x00 |  |
| # 0x84,0x2E5D,0xFC |  |
| # 0x84,0x2E5E,0x00 |  |
| # 0x84,0x2E5F,0x47 |  |
| # 0x84,0x2E60,0x4D |  |
| # 0x84,0x2E61,0x53 |  |
| # 0x84,0x2E62,0x4C |  |
| # 0x84,0x2E63,0x31 |  |
| # 0x84,0x2E64,0x39 |  |
| # 0x84,0x2E65,0x32 |  |
| # 0x84,0x2E66,0x30 |  |
| # 0x84,0x2E67,0x78 |  |
| # 0x84,0x2E68,0x31 |  |
| # 0x84,0x2E69,0x32 |  |
| # 0x84,0x2E6A,0x30 |  |
| # 0x84,0x2E6B,0x30 |  |
| # 0x84,0x2E6C,0x00 |  |
| # 0x84,0x2E6D,0x00 |  |
| # 0x84,0x2E6E,0x00 |  |
| # 0x84,0x2E6F,0xFF |  |
| # 0x84,0x2E70,0x00 |  |
| # 0x84,0x2E71,0x36 |  |
| # 0x84,0x2E72,0x36 |  |
| # 0x84,0x2E73,0x36 |  |
| # 0x84,0x2E74,0x36 |  |
| # 0x84,0x2E75,0x36 |  |
| # 0x84,0x2E76,0x36 |  |
| # 0x84,0x2E77,0x36 |  |
| # 0x84,0x2E78,0x36 |  |
| # 0x84,0x2E79,0x36 |  |
| # 0x84,0x2E7A,0x36 |  |
| # 0x84,0x2E7B,0x36 |  |
| # 0x84,0x2E7C,0x36 |  |
| # 0x84,0x2E7D,0x36 |  |
| # 0x84,0x2E7E,0x00 |  |
| # 0x84,0x2E7F,0xE6 |  |
| # 0x84,0x2E80,0x00 |  |
| # 0x84,0x2E81,0x00 |  |
| # 0x84,0x2E82,0x00 |  |
| # 0x84,0x2E83,0x00 |  |
| # 0x84,0x2E84,0x00 |  |
| # 0x84,0x2E85,0x00 |  |
| # 0x84,0x2E86,0x00 |  |
| # 0x84,0x2E87,0x00 |  |
| # 0x84,0x2E88,0x00 |  |
| # 0x84,0x2E89,0x00 |  |
| # 0x84,0x2E8A,0x00 |  |
| # 0x84,0x2E8B,0x00 |  |
| # 0x84,0x2E8C,0x00 |  |
| # 0x84,0x2E8D,0x00 |  |
| # 0x84,0x2E8E,0x00 |  |
| # 0x84,0x2E8F,0x00 |  |
| # 0x84,0x2E90,0x00 |  |
| # 0x84,0x2E91,0x00 |  |
| # 0x84,0x2E92,0x00 |  |
| # 0x84,0x2E93,0x00 |  |
| # 0x84,0x2E94,0x00 |  |
| # 0x84,0x2E95,0x00 |  |
| # 0x84,0x2E96,0x00 |  |
| # 0x84,0x2E97,0x00 |  |
| # 0x84,0x2E98,0x00 |  |
| # 0x84,0x2E99,0x00 |  |
| # 0x84,0x2E9A,0x00 |  |
| # 0x84,0x2E9B,0x00 |  |
| # 0x84,0x2E9C,0x00 |  |
| # 0x84,0x2E9D,0x00 |  |
| # 0x84,0x2E9E,0x00 |  |
| # 0x84,0x2E9F,0x00 |  |
| # 0x84,0x2EA0,0x00 |  |
| # 0x84,0x2EA1,0x00 |  |
| # 0x84,0x2EA2,0x00 |  |
| # 0x84,0x2EA3,0x00 |  |
| # 0x84,0x2EA4,0x00 |  |
| # 0x84,0x2EA5,0x00 |  |
| # 0x84,0x2EA6,0x00 |  |
| # 0x84,0x2EA7,0x00 |  |
| # 0x84,0x2EA8,0x00 |  |
| # 0x84,0x2EA9,0x00 |  |
| # 0x84,0x2EAA,0x00 |  |
| # 0x84,0x2EAB,0x00 |  |
| # 0x84,0x2EAC,0x00 |  |
| # 0x84,0x2EAD,0x00 |  |
| # 0x84,0x2EAE,0x00 |  |
| # 0x84,0x2EAF,0x00 |  |
| # 0x84,0x2EB0,0x00 |  |
| # 0x84,0x2EB1,0x00 |  |
| # 0x84,0x2EB2,0x00 |  |
| # 0x84,0x2EB3,0x00 |  |
| # 0x84,0x2EB4,0x00 |  |
| # 0x84,0x2EB5,0x00 |  |
| # 0x84,0x2EB6,0x00 |  |
| # 0x84,0x2EB7,0x00 |  |
| # 0x84,0x2EB8,0x00 |  |
| # 0x84,0x2EB9,0x00 |  |
| # 0x84,0x2EBA,0x00 |  |
| # 0x84,0x2EBB,0x00 |  |
| # 0x84,0x2EBC,0x00 |  |
| # 0x84,0x2EBD,0x00 |  |
| # 0x84,0x2EBE,0x00 |  |
| # 0x84,0x2EBF,0x00 |  |
| # 0x84,0x2EC0,0x00 |  |
| # 0x84,0x2EC1,0x00 |  |
| # 0x84,0x2EC2,0x00 |  |
| # 0x84,0x2EC3,0x00 |  |
| # 0x84,0x2EC4,0x00 |  |
| # 0x84,0x2EC5,0x00 |  |
| # 0x84,0x2EC6,0x00 |  |
| # 0x84,0x2EC7,0x00 |  |
| # 0x84,0x2EC8,0x00 |  |
| # 0x84,0x2EC9,0x00 |  |
| # 0x84,0x2ECA,0x00 |  |
| # 0x84,0x2ECB,0x00 |  |
| # 0x84,0x2ECC,0x00 |  |
| # 0x84,0x2ECD,0x00 |  |
| # 0x84,0x2ECE,0x00 |  |
| # 0x84,0x2ECF,0x00 |  |
| # 0x84,0x2ED0,0x00 |  |
| # 0x84,0x2ED1,0x00 |  |
| # 0x84,0x2ED2,0x00 |  |
| # 0x84,0x2ED3,0x00 |  |
| # 0x84,0x2ED4,0x00 |  |
| # 0x84,0x2ED5,0x00 |  |
| # 0x84,0x2ED6,0x00 |  |
| # 0x84,0x2ED7,0x00 |  |
| # 0x84,0x2ED8,0x00 |  |
| # 0x84,0x2ED9,0x00 |  |
| # 0x84,0x2EDA,0x00 |  |
| # 0x84,0x2EDB,0x00 |  |
| # 0x84,0x2EDC,0x00 |  |
| # 0x84,0x2EDD,0x00 |  |
| # 0x84,0x2EDE,0x00 |  |
| # 0x84,0x2EDF,0x00 |  |
| # 0x84,0x2EE0,0x00 |  |
| # 0x84,0x2EE1,0x00 |  |
| # 0x84,0x2EE2,0x00 |  |
| # 0x84,0x2EE3,0x00 |  |
| # 0x84,0x2EE4,0x00 |  |
| # 0x84,0x2EE5,0x00 |  |
| # 0x84,0x2EE6,0x00 |  |
| # 0x84,0x2EE7,0x00 |  |
| # 0x84,0x2EE8,0x00 |  |
| # 0x84,0x2EE9,0x00 |  |
| # 0x84,0x2EEA,0x00 |  |
| # 0x84,0x2EEB,0x00 |  |
| # 0x84,0x2EEC,0x00 |  |
| # 0x84,0x2EED,0x00 |  |
| # 0x84,0x2EEE,0x00 |  |
| # 0x84,0x2EEF,0x00 |  |
| # 0x84,0x2EF0,0x00 |  |
| # 0x84,0x2EF1,0x00 |  |
| # 0x84,0x2EF2,0x00 |  |
| # 0x84,0x2EF3,0x00 |  |
| # 0x84,0x2EF4,0x00 |  |
| # 0x84,0x2EF5,0x00 |  |
| # 0x84,0x2EF6,0x00 |  |
| # 0x84,0x2EF7,0x00 |  |
| # 0x84,0x2EF8,0x00 |  |
| # 0x84,0x2EF9,0x00 |  |
| # 0x84,0x2EFA,0x00 |  |
| # 0x84,0x2EFB,0x00 |  |
| # 0x84,0x2EFC,0x00 |  |
| # 0x84,0x2EFD,0x00 |  |
| # 0x84,0x2EFE,0x00 |  |
| # 0x84,0x2EFF,0x00 |  |
| # |  |
| # Hot Plug Detect ON,, |  |
| 0x84,0x20F5,0x01 |  |
| # End of Script,, |  |
| # |  |
| # |  |
| # ----------- Watermark Gen setting on MAX96712 ---------------- |  |
| # Unlock watermark block 0 and 1 |  |
| #0x52,0x121E,0xBA |  |
| #0x52,0x121F,0xDC |  |
| 0x52,0x123E,0xBA |  |
| 0x52,0x123F,0xDC |  |
| # Configure as a generator |  |
| #0x52,0x1200,0x05 |  |
| 0x52,0x1220,0x01 |  |
| # Invert the VS polarity |  |
| 0x52,0x1222,0x54 |  |
| # set detector threshold (default is too high) |  |
| #0x52,0x1203,0x04 |  |
| #0x52,0x1223,0x04 |  |
| # Configure for blank on error |  |
| #0x52,0x120C,0x11 |  |
| #0x52,0x122C,0x11 |  |
| # lock the block |  |
| #0x52,0x121E,0x00 |  |
| #0x52,0x121F,0x00 |  |
| #0x52,0x123E,0x00 |  |
| #0x52,0x123F,0x00 |  |
| # |  |
| # ----------- Watermark Det setting on MAX96752 ---------------- |  |
| # Unlock watermark block |  |
| 0x90,0x01AE,0xBA |  |
| 0x90,0x01AF,0xDC |  |
| # configure as a detector |  |
| 0x90,0x188,0x05 |  |
| # set detector threshold (default is too high) |  |
| 0x90,0x18B,0x04 |  |
| # Invert the VS polarity |  |
| 0x90,0x18A,0x54 |  |
| # lock the block |  |
| #0x90,0x01AE,0x00 |  |
| #0x90,0x01AF,0x00 |  |
| # |  |
| # |  |
| # ------------ Check WM_DETOUT ------------- |  |
| # 0x90,0x18D, Bit 1 |  |

## SM13_TC2

| Optional Safety Measure |  |
|---|---|
| SM13_TC2= Checker of Watermark |  |
| Safety Goal- A watermark sequence is optionally generated at the serializer/deserializer, which is evaluated at the deserializer/serializer |  |
| Detection of Watermark |  |
| Note- MAX96712 can be used as watermark generator or checker, this feature can only be used with parts that support watermarking. MAX96717/93 do not support watermark feature. |  |
| Watermarking feature is only supported on pipes 0 and 4 on MAX96712, for datatypes RGB888 and YUV444 |  |
| Hardware Setup |  |
| HDMI - MAX96751/777(Watermark Gen) - MAX96712(Watermark Det on pipe 4)-MAX9295A - MAX96752/780 - Display |  |
| * Watermark is designed mainly for RGB888 |  |
| Software Configuration |  |
| .csv Script attached below |  |
| Verfification |  |
| Read 0x1225 bit 1 (WM_DETOUT) asserts on MAX96712; |  |
| Observe no difference visually on display pannel; |  |
| If image frozen, WM_DETOUT cleans. |  |
| Script |  |
| # This script must be run AFTER all devices are linked up,, |  |
| # Reset all |  |
| 0x84,0x10,0x91 |  |
| 0x52,0x13,0x75 |  |
| 0x80,0x10,0x81 |  |
| 0x90,0x10,0x91 |  |
| # |  |
| # |  |
| # ------------ MAX96752 Setup -------------- |  |
| # Set up dual oLDI output,, |  |
| 0x90,0x01CE,0x5F |  |
| # VID_INFO_MAN to a 1,, |  |
| 0x90,0x100,0x3B |  |
| # RX BPP to 24 (0x18) for RGB888 and RX encoding mode to 2,, |  |
| 0x90,0x109,0x98 |  |
| # RX FB_DIV,, |  |
| 0x90,0x10A,0x28 |  |
| # RX FB_DIV_FRAC,, |  |
| 0x90,0x10B,0x00 |  |
| # RX VID_ODIV_L,, |  |
| 0x90,0x10C,0x12 |  |
| # Speed Det (Speed_lim),, |  |
| 0x90,0x10E,0x40 |  |
| # |  |
| # ------------ MAX9295A Setup -------------- |  |
| # Disable PRBS test mode |  |
| 0x80,0x370,0x08 |  |
| # Set MIPI port configuration - 1x4 mode |  |
| 0x80,0x330,0x00 |  |
| # Lane Mapping - turn on all lanes on CTRL 0 and 1 |  |
| 0x80,0x331,0x33 |  |
| # Controller to Pipe Mapping |  |
| # |  |
| # Enable all video pipelines from used CSI input port (start_portax/y/z/u = 0, start_portbx/y/z/u = 1, clk_selx/y/z/u = 1 ) |  |
| 0x80,0x0311,0xF0 |  |
| 0x80,0x0308,0x7F |  |
| # |  |
| # Route RGB888 DT=0x24 to VIDEO_X (MSB enable) |  |
| 0x80,0x0314,0xE4 |  |
| # Unused VIDEO_Y |  |
| 0x80,0x0316,0x62 |  |
| # Unused VIDEO_Z |  |
| 0x80,0x0318,0x62 |  |
| # Unused VIDEO_U |  |
| #0x80,0x031A,0x62 |  |
| # |  |
| # |  |
| # ------------ MAX96712 Setup --------------,, |  |
| # Turn on PHY A; GMSL2 mode |  |
| 0x52,0x06,0xF1 |  |
| # 0x52,0x06,0xF2 |  |
| # 0x52,0x06,0xF4 |  |
| # 0x52,0x06,0xF8 |  |
| # Set des in 2x4 mode |  |
| 0x52,0x8A0,0x04 |  |
| # Select pipe 0 and 4 to stream PHY A Pipe X |  |
| 0x52,0xF0,0x40 |  |
| #0x52,0xF1,0x62 |  |
| 0x52,0xF2,0x80 |  |
| # 0x52,0xF3,0xE2 |  |
| # Enable Video Pipe 0 and 4 only |  |
| 0x52,0xF4,0x11 |  |
| # |  |
| # Mapping Pipe 0 to Ctrl 1 |  |
| #0x52,0x90B,0x07 |  |
| #0x52,0x92D,0x15 |  |
| #0x52,0x90D,0x24 |  |
| #0x52,0x90E,0x24 |  |
| #0x52,0x90F,0x00 | Pass |
| #0x52,0x910,0x00 |  |
| #0x52,0x911,0x01 |  |
| #0x52,0x912,0x01 |  |
| # |  |
| # Mapping Pipe 4 to Ctrl 1 |  |
| 0x52,0xA0B,0x07 |  |
| 0x52,0xA2D,0x15 |  |
| 0x52,0xA0D,0x24 |  |
| 0x52,0xA0E,0x24 |  |
| 0x52,0xA0F,0x00 |  |
| 0x52,0xA10,0x00 |  |
| 0x52,0xA11,0x01 |  |
| 0x52,0xA12,0x01 |  |
| # |  |
| # Set Lane Mapping |  |
| 0x52,0x8A3,0xE4 |  |
| 0x52,0x8A4,0xE4 |  |
| # Set 4 lanes for deserializer |  |
| 0x52,0x90A,0xC0 |  |
| 0x52,0x94A,0xC0 |  |
| 0x52,0x98A,0xC0 |  |
| 0x52,0x9CA,0xC0 |  |
| # Turn on all PHYs |  |
| 0x52,0x8A2,0xF0 |  |
| # Set Data rate to be 1000Mbps |  |
| 0x52,0x415,0x2A |  |
| 0x52,0x418,0x2A |  |
| #0x52,0x41B,0x2A |  |
| #0x52,0x41E,0x2A |  |
| # Apply Reset for changes ------------------------------------ |  |
| 0x52,0x18,0x0F |  |
| # |  |
| # ------------ MAX96777 Setup --------------,, |  |
| # Script to set up Video Feedthrough HDMI-CSI,, |  |
| # Clean LFLT error,, |  |
| 0x84,0x1A,0x03 |  |
| # Invert VSYNC |  |
| 0x84,0x1C8,0x03 |  |
| # Hot Plug Detect OFF,, |  |
| 0x84,0x20F5,0x00 |  |
| # HDMI_Enable,, |  |
| 0x84,0x01,0x88 |  |
| # Stream select 0 for port A,, |  |
| 0x84,0x53,0x10 |  |
| #,, |  |
| # Load EDID Table for 1920x1200 10in Display; Needed if not using HDMI generator |  |
| # 0x84,0x2E00,0x00 |  |
| # 0x84,0x2E01,0xFF |  |
| # 0x84,0x2E02,0xFF |  |
| # 0x84,0x2E03,0xFF |  |
| # 0x84,0x2E04,0xFF |  |
| # 0x84,0x2E05,0xFF |  |
| # 0x84,0x2E06,0xFF |  |
| # 0x84,0x2E07,0x00 |  |
| # 0x84,0x2E08,0x37 |  |
| # 0x84,0x2E09,0x0D |  |
| # 0x84,0x2E0A,0x20 |  |
| # 0x84,0x2E0B,0x19 |  |
| # 0x84,0x2E0C,0xB0 |  |
| # 0x84,0x2E0D,0xFC |  |
| # 0x84,0x2E0E,0x24 |  |
| # 0x84,0x2E0F,0x01 |  |
| # 0x84,0x2E10,0x01 |  |
| # 0x84,0x2E11,0x1B |  |
| # 0x84,0x2E12,0x01 |  |
| # 0x84,0x2E13,0x03 |  |
| # 0x84,0x2E14,0x81 |  |
| # 0x84,0x2E15,0x16 |  |
| # 0x84,0x2E16,0x0E |  |
| # 0x84,0x2E17,0x78 |  |
| # 0x84,0x2E18,0xEA |  |
| # 0x84,0x2E19,0x2C |  |
| # 0x84,0x2E1A,0xC5 |  |
| # 0x84,0x2E1B,0xA4 |  |
| # 0x84,0x2E1C,0x56 |  |
| # 0x84,0x2E1D,0x50 |  |
| # 0x84,0x2E1E,0xA1 |  |
| # 0x84,0x2E1F,0x28 |  |
| # 0x84,0x2E20,0x0F |  |
| # 0x84,0x2E21,0x50 |  |
| # 0x84,0x2E22,0x54 |  |
| # 0x84,0x2E23,0x00 |  |
| # 0x84,0x2E24,0x00 |  |
| # 0x84,0x2E25,0x00 |  |
| # 0x84,0x2E26,0xD1 |  |
| # 0x84,0x2E27,0x00 |  |
| # 0x84,0x2E28,0x01 |  |
| # 0x84,0x2E29,0x00 |  |
| # 0x84,0x2E2A,0x01 |  |
| # 0x84,0x2E2B,0x00 |  |
| # 0x84,0x2E2C,0x01 |  |
| # 0x84,0x2E2D,0x00 |  |
| # 0x84,0x2E2E,0x01 |  |
| # 0x84,0x2E2F,0x00 |  |
| # 0x84,0x2E30,0x01 |  |
| # 0x84,0x2E31,0x00 |  |
| # 0x84,0x2E32,0x01 |  |
| # 0x84,0x2E33,0x00 |  |
| # 0x84,0x2E34,0x01 |  |
| # 0x84,0x2E35,0x01 |  |
| # 0x84,0x2E36,0xB8 |  |
| # 0x84,0x2E37,0x3D |  |
| # 0x84,0x2E38,0x80 |  |
| # 0x84,0x2E39,0x18 |  |
| # 0x84,0x2E3A,0x71 |  |
| # 0x84,0x2E3B,0xB0 |  |
| # 0x84,0x2E3C,0x2D |  |
| # 0x84,0x2E3D,0x40 |  |
| # 0x84,0x2E3E,0x58 |  |
| # 0x84,0x2E3F,0x2C |  |
| # 0x84,0x2E40,0x45 |  |
| # 0x84,0x2E41,0x00 |  |
| # 0x84,0x2E42,0x13 |  |
| # 0x84,0x2E43,0x2B |  |
| # 0x84,0x2E44,0x21 |  |
| # 0x84,0x2E45,0x00 |  |
| # 0x84,0x2E46,0x00 |  |
| # 0x84,0x2E47,0x1E |  |
| # 0x84,0x2E48,0x00 |  |
| # 0x84,0x2E49,0x00 |  |
| # 0x84,0x2E4A,0x00 |  |
| # 0x84,0x2E4B,0xFD |  |
| # 0x84,0x2E4C,0x00 |  |
| # 0x84,0x2E4D,0x32 |  |
| # 0x84,0x2E4E,0x4C |  |
| # 0x84,0x2E4F,0x1E |  |
| # 0x84,0x2E50,0x53 |  |
| # 0x84,0x2E51,0x11 |  |
| # 0x84,0x2E52,0x00 |  |
| # 0x84,0x2E53,0x0A |  |
| # 0x84,0x2E54,0x20 |  |
| # 0x84,0x2E55,0x20 |  |
| # 0x84,0x2E56,0x20 |  |
| # 0x84,0x2E57,0x20 |  |
| # 0x84,0x2E58,0x20 |  |
| # 0x84,0x2E59,0x20 |  |
| # 0x84,0x2E5A,0x00 |  |
| # 0x84,0x2E5B,0x00 |  |
| # 0x84,0x2E5C,0x00 |  |
| # 0x84,0x2E5D,0xFC |  |
| # 0x84,0x2E5E,0x00 |  |
| # 0x84,0x2E5F,0x47 |  |
| # 0x84,0x2E60,0x4D |  |
| # 0x84,0x2E61,0x53 |  |
| # 0x84,0x2E62,0x4C |  |
| # 0x84,0x2E63,0x31 |  |
| # 0x84,0x2E64,0x39 |  |
| # 0x84,0x2E65,0x32 |  |
| # 0x84,0x2E66,0x30 |  |
| # 0x84,0x2E67,0x78 |  |
| # 0x84,0x2E68,0x31 |  |
| # 0x84,0x2E69,0x32 |  |
| # 0x84,0x2E6A,0x30 |  |
| # 0x84,0x2E6B,0x30 |  |
| # 0x84,0x2E6C,0x00 |  |
| # 0x84,0x2E6D,0x00 |  |
| # 0x84,0x2E6E,0x00 |  |
| # 0x84,0x2E6F,0xFF |  |
| # 0x84,0x2E70,0x00 |  |
| # 0x84,0x2E71,0x36 |  |
| # 0x84,0x2E72,0x36 |  |
| # 0x84,0x2E73,0x36 |  |
| # 0x84,0x2E74,0x36 |  |
| # 0x84,0x2E75,0x36 |  |
| # 0x84,0x2E76,0x36 |  |
| # 0x84,0x2E77,0x36 |  |
| # 0x84,0x2E78,0x36 |  |
| # 0x84,0x2E79,0x36 |  |
| # 0x84,0x2E7A,0x36 |  |
| # 0x84,0x2E7B,0x36 |  |
| # 0x84,0x2E7C,0x36 |  |
| # 0x84,0x2E7D,0x36 |  |
| # 0x84,0x2E7E,0x00 |  |
| # 0x84,0x2E7F,0xE6 |  |
| # 0x84,0x2E80,0x00 |  |
| # 0x84,0x2E81,0x00 |  |
| # 0x84,0x2E82,0x00 |  |
| # 0x84,0x2E83,0x00 |  |
| # 0x84,0x2E84,0x00 |  |
| # 0x84,0x2E85,0x00 |  |
| # 0x84,0x2E86,0x00 |  |
| # 0x84,0x2E87,0x00 |  |
| # 0x84,0x2E88,0x00 |  |
| # 0x84,0x2E89,0x00 |  |
| # 0x84,0x2E8A,0x00 |  |
| # 0x84,0x2E8B,0x00 |  |
| # 0x84,0x2E8C,0x00 |  |
| # 0x84,0x2E8D,0x00 |  |
| # 0x84,0x2E8E,0x00 |  |
| # 0x84,0x2E8F,0x00 |  |
| # 0x84,0x2E90,0x00 |  |
| # 0x84,0x2E91,0x00 |  |
| # 0x84,0x2E92,0x00 |  |
| # 0x84,0x2E93,0x00 |  |
| # 0x84,0x2E94,0x00 |  |
| # 0x84,0x2E95,0x00 |  |
| # 0x84,0x2E96,0x00 |  |
| # 0x84,0x2E97,0x00 |  |
| # 0x84,0x2E98,0x00 |  |
| # 0x84,0x2E99,0x00 |  |
| # 0x84,0x2E9A,0x00 |  |
| # 0x84,0x2E9B,0x00 |  |
| # 0x84,0x2E9C,0x00 |  |
| # 0x84,0x2E9D,0x00 |  |
| # 0x84,0x2E9E,0x00 |  |
| # 0x84,0x2E9F,0x00 |  |
| # 0x84,0x2EA0,0x00 |  |
| # 0x84,0x2EA1,0x00 |  |
| # 0x84,0x2EA2,0x00 |  |
| # 0x84,0x2EA3,0x00 |  |
| # 0x84,0x2EA4,0x00 |  |
| # 0x84,0x2EA5,0x00 |  |
| # 0x84,0x2EA6,0x00 |  |
| # 0x84,0x2EA7,0x00 |  |
| # 0x84,0x2EA8,0x00 |  |
| # 0x84,0x2EA9,0x00 |  |
| # 0x84,0x2EAA,0x00 |  |
| # 0x84,0x2EAB,0x00 |  |
| # 0x84,0x2EAC,0x00 |  |
| # 0x84,0x2EAD,0x00 |  |
| # 0x84,0x2EAE,0x00 |  |
| # 0x84,0x2EAF,0x00 |  |
| # 0x84,0x2EB0,0x00 |  |
| # 0x84,0x2EB1,0x00 |  |
| # 0x84,0x2EB2,0x00 |  |
| # 0x84,0x2EB3,0x00 |  |
| # 0x84,0x2EB4,0x00 |  |
| # 0x84,0x2EB5,0x00 |  |
| # 0x84,0x2EB6,0x00 |  |
| # 0x84,0x2EB7,0x00 |  |
| # 0x84,0x2EB8,0x00 |  |
| # 0x84,0x2EB9,0x00 |  |
| # 0x84,0x2EBA,0x00 |  |
| # 0x84,0x2EBB,0x00 |  |
| # 0x84,0x2EBC,0x00 |  |
| # 0x84,0x2EBD,0x00 |  |
| # 0x84,0x2EBE,0x00 |  |
| # 0x84,0x2EBF,0x00 |  |
| # 0x84,0x2EC0,0x00 |  |
| # 0x84,0x2EC1,0x00 |  |
| # 0x84,0x2EC2,0x00 |  |
| # 0x84,0x2EC3,0x00 |  |
| # 0x84,0x2EC4,0x00 |  |
| # 0x84,0x2EC5,0x00 |  |
| # 0x84,0x2EC6,0x00 |  |
| # 0x84,0x2EC7,0x00 |  |
| # 0x84,0x2EC8,0x00 |  |
| # 0x84,0x2EC9,0x00 |  |
| # 0x84,0x2ECA,0x00 |  |
| # 0x84,0x2ECB,0x00 |  |
| # 0x84,0x2ECC,0x00 |  |
| # 0x84,0x2ECD,0x00 |  |
| # 0x84,0x2ECE,0x00 |  |
| # 0x84,0x2ECF,0x00 |  |
| # 0x84,0x2ED0,0x00 |  |
| # 0x84,0x2ED1,0x00 |  |
| # 0x84,0x2ED2,0x00 |  |
| # 0x84,0x2ED3,0x00 |  |
| # 0x84,0x2ED4,0x00 |  |
| # 0x84,0x2ED5,0x00 |  |
| # 0x84,0x2ED6,0x00 |  |
| # 0x84,0x2ED7,0x00 |  |
| # 0x84,0x2ED8,0x00 |  |
| # 0x84,0x2ED9,0x00 |  |
| # 0x84,0x2EDA,0x00 |  |
| # 0x84,0x2EDB,0x00 |  |
| # 0x84,0x2EDC,0x00 |  |
| # 0x84,0x2EDD,0x00 |  |
| # 0x84,0x2EDE,0x00 |  |
| # 0x84,0x2EDF,0x00 |  |
| # 0x84,0x2EE0,0x00 |  |
| # 0x84,0x2EE1,0x00 |  |
| # 0x84,0x2EE2,0x00 |  |
| # 0x84,0x2EE3,0x00 |  |
| # 0x84,0x2EE4,0x00 |  |
| # 0x84,0x2EE5,0x00 |  |
| # 0x84,0x2EE6,0x00 |  |
| # 0x84,0x2EE7,0x00 |  |
| # 0x84,0x2EE8,0x00 |  |
| # 0x84,0x2EE9,0x00 |  |
| # 0x84,0x2EEA,0x00 |  |
| # 0x84,0x2EEB,0x00 |  |
| # 0x84,0x2EEC,0x00 |  |
| # 0x84,0x2EED,0x00 |  |
| # 0x84,0x2EEE,0x00 |  |
| # 0x84,0x2EEF,0x00 |  |
| # 0x84,0x2EF0,0x00 |  |
| # 0x84,0x2EF1,0x00 |  |
| # 0x84,0x2EF2,0x00 |  |
| # 0x84,0x2EF3,0x00 |  |
| # 0x84,0x2EF4,0x00 |  |
| # 0x84,0x2EF5,0x00 |  |
| # 0x84,0x2EF6,0x00 |  |
| # 0x84,0x2EF7,0x00 |  |
| # 0x84,0x2EF8,0x00 |  |
| # 0x84,0x2EF9,0x00 |  |
| # 0x84,0x2EFA,0x00 |  |
| # 0x84,0x2EFB,0x00 |  |
| # 0x84,0x2EFC,0x00 |  |
| # 0x84,0x2EFD,0x00 |  |
| # 0x84,0x2EFE,0x00 |  |
| # 0x84,0x2EFF,0x00 |  |
| # |  |
| # Hot Plug Detect ON,, |  |
| 0x84,0x20F5,0x01 |  |
| # End of Script,, |  |
| # |  |
| # |  |
| # |  |
| # |  |
| # ----------- Watermark Gen setting on MAX96751 ---------------- |  |
| # Unlock watermark block |  |
| 0x84,0x01AE,0xBA |  |
| 0x84,0x01AF,0xDC |  |
| # configure as a detector |  |
| 0x84,0x188,0x01 |  |
| # set detector threshold (default is too high) |  |
| #0x90,0x18B,0x04 |  |
| # Increase the gain |  |
| #0x84,0x189,0x79 |  |
| # Invert the VS polarity |  |
| 0x84,0x18A,0x54 |  |
| # lock the block |  |
| #0x90,0x01AE,0x00 |  |
| #0x90,0x01AF,0x00 |  |
| # |  |
| # |  |
| # ----------- Watermark Det setting on MAX96712 ---------------- |  |
| # Unlock watermark block 0 and 1 |  |
| #0x52,0x121E,0xBA |  |
| #0x52,0x121F,0xDC |  |
| 0x52,0x123E,0xBA |  |
| 0x52,0x123F,0xDC |  |
| # Configure as a Detector |  |
| #0x52,0x1200,0x05 |  |
| 0x52,0x1220,0x05 |  |
| # Invert the VS polarity |  |
| 0x52,0x1222,0x54 |  |
| # set detector threshold (default is too high) |  |
| #0x52,0x1203,0x04 |  |
| 0x52,0x1223,0x04 |  |
| # lock the block |  |
| #0x52,0x121E,0x00 |  |
| #0x52,0x121F,0x00 |  |
| #0x52,0x123E,0x00 |  |
| #0x52,0x123F,0x00 |  |
| # |  |
| # |  |
| # ------------ Check WM_DETOUT ------------- |  |
| # 0x52,0x1225, Bit 1 |  |

## SM14_TC1

| Optional Safety Measure |  |
|---|---|
| SM14=Eye Opening Monitor |  |
| Safety Measure Goal: SerDes devices have built in Eye Opening Monitor that can be used to observe the signal integrity of the link. |  |
| Eye Opening Monitor |  |
| Notes:  1) Setup a link between MAX96717 and MAX96712 and ensure it is LOCKED. 2) GMSL2 offers EOM (on by default) for horizontal width measurement AND EOM for vertical height measurement. EOM_ERR_FLAG will assert if eye opening falls below a desired threshold. (Default EOM threshold is 0.25UI) 3) EOM values can also be used to create bathtub curves. For more details regarding EOM, please reference the User Guide.   4) Run devices errata writes before using SI tools 5) The below test steps is to validate EOM Flag operates correctly, it is not recommend to change the default EOM threshold value. |  |
| Test Setup: |  |
| 1) uC can be connected to SER or DES. |  |
| 2) Power up MAX96717/MAX96716A devices and establish GMSL link with no errors. |  |
| 3) Enable ERRB/LOCK pins |  |
| 3) EOM feature is enabled by default, but flag is not. Enable EOM failure flag to ERRB Pin, DES Register 0x1C--> EOM_ERR_OEN_A=1, EOM_ERR_OEN_B=1 |  |
| Fault Injection: |  |
| 1) Increase EOM threshold from its default 0.25UI to 1.0UI, DES Register 0x1405-->0x7F, 0x1505-->0x7F |  |
| 2) Verify that DES ERRB pin is active and the flag is EOM_ERR_FLAG_A or EOM_ERR_FLAG_B. |  |
| Fault Clearing: |  |
| 1) Decrease EOM threshold back to its default value, DES Register 0x1405-->0x10, 0x1505-->0x10 |  |
| 2) Read EOM_ERR_FLAG_A and EOM_ERR_FLAG_B in DES Register 0x1D to clear ERRB pin. |  |
| 3) Verify that ERRB is not active. |  |
|  | Pass |

## SM15_TC1

| Default Safety Measure |  |  |  |
|---|---|---|---|
| SM15_TC1= OverVoltage/UnderVoltage comparators for Des |  |  |  |
| Safety Measure Goal: Verify that DES ERR flags will activate when there is a undervoltage or overvoltage event. |  |  |  |
| Notes:  1) Setup a link between MAX9295A and MAX96712 and verify link is LOCKED and set adequate CSI input/output signal. 2) SER and DES need to have valid video signal through in order for OV flags to work properly. |  |  |  |
| 3) Hysteresis is set to default value for all (3) supplies for OV. |  |  |  |
| 4) In the case of VDDCMP_INT and/or PORZ_INT, you must clear PWR0/PWR1 error status registers to clear ERRB. |  |  |  |
| 5) In the case there is a VDDCMP_INT & PORZ_INT, you must clear PW0 before PWR1 to properly clear ERRB. |  |  |  |
| 6) Undervoltage- When an undervoltage event occurs, I2C communication may be lost.   When power is restored, UV status registers can be read to determine which power supply experienced the undervoltage event.  Registers will be reset upon loss of power so device re-configuration may be necessary. |  |  |  |
| Voltage Measurement and Overvoltage/Undervoltage Monitoring |  |  |  |
| Hardware Setup |  |  |  |
| MAX96712(DUT) |  |  |  |
| Verfification |  |  |  |
| 0x12 | Default value | Description |  |
| Bit 7 | 0 | PU_LDO error flag register |  |
| Bit 6 | 0 |  |  |
| Bit 5 | 0 | VDDA_bad (VDDD_sw) error flag register |  |
| Bit 4 | 0 | Assert when VREG/VDD > 1.1V |  |
| Bit 3 | 0 | Assert when VDD_sw > 1.05V |  |
| Bit 2 | 1 |  |  |
| Bit 1 | 1 | Latched low when VDDIO < 1.617V |  |
| Bit 0 | 1 | Latched low when VDD18 < 1.617V |  |
|  |  | *VDDD_sw is internal; USER can monitor CAPVDD pin |  |
| C |  | *Expect coarse comparison result as the internal comparator is not trimmed |  |
|  |  |  | Pass |

## SM18_TC1

| Default Safety Measure |  |
|---|---|
| SM18_TC1= Readback of status for LOCK, ERRB and LFLT through I2C or UART register |  |
| Safety Measure Goal: read the status of LFLT and ERRB registers using I2C or UART |  |
| Note- If you are not monitoring the ERRB or LFLT MFP pins externally or would like to poll the register bits, it is possible to read the status of these on registers using I2C or UART |  |
| Register Reading for Line Fault, ERRB or LOCK through I2C and UART |  |
| For Line Fault, refer to SM2 for details; |  |
| For ERRB, refer to SM7/SM9 for details; |  |
| For LOCK, refer to SM6/SM8 for details. |  |
|  | Pass |

## SM19_TC1

| Optional Safety Measure |  |  |  |
|---|---|---|---|
| SM19=Packet Counter for GPIO, I2C, SPI and UART packet |  |  |  |
| Safety Measure Goal: SerDes devices have ability to monitor/count the number of packets of specific low bandwith control signals (GPIO, I2C, UART, SPI) |  |  |  |
| Packet Counter |  |  |  |
| Notes:  1) Must pick which low bandwidth control signal (GPIO, I2C, UART, SPI) to monitor with the packet counter. |  |  |  |
| Hardware Setup |  |  |  |
| MAX9295A - MAX96712(DUT) |  |  |  |
| Software Configuration |  |  |  |
| Packet counter is off by default; |  |  |  |
| To enable Packet counter for each link A/B/C/D: | 0x1004/0x1014/0x1024/0x1034 | Bits [3:0] = 0 |  |
| To specifiy the counting packets: | 4'b0100: SPI |  |  |
|  | 4'b0101: I2C |  |  |
|  | 4'b0110: UART |  |  |
|  | 4'b0111: GPIO |  |  |
| Verfification |  |  |  |
| Working as expected. |  |  |  |
| To check the counter value for each link A/B/C/D: | 0x40/0x41/0x42/0x43 | *reads clean |  |
| To check counter flag: | 0x2C | Bits [7:4] |  |
| To enable ERRB pin reporting counter flag: | 0x2B | Bits [7:4] |  |
| To set packet count threshold | 0x24 | Bits [2:0] |  |
|  |  |  | Pass |

## SM20_TC1

| Default Safety Measure |  |
|---|---|
| SM20=9b/10b illegal symbol check, running disparity |  |
| Safety Measure Goal: Monitor errors on SerDes in the case devices loses 9b/10b encoding/scrambler. |  |
| Notes:  1) These tests are only for safety measure testing, not to be done in normal/production operation. |  |
| 9b/10b illegal symbol check, running disparity |  |
| Hardware Setup |  |
| 0.Preapare a MAX9295A or any GMSL2 serializer, and MAX96712 DUT. |  |
| 1. Have I2C access to MAX96712 locally. |  |
| 2.Establish GMSL2 Link Between MAX9295A and MAX96712 (Link A) error-free. |  |
| - Check ERRB pin and LOCK pin or register 0x1A bit 3 on MAX96712 |  |
| Fault Injection |  |
| Disable 9b/10b encoding in MAX9295A: |  |
| 0x29 Bit 0 = 1 |  |
| Verification |  |
| Link breaks; |  |
| MAX96712 0x26 Bit 0 (DEC_ERR_FLAG_A) asserted as decoding error detected; |  |
| ERRB pin goes low. |  |
| *0x26 [3:0] is the flag bit for each link. |  |
| *0x25 [3:0] is to enable error reports to ERRB pin. |  |
|  | Pass |

## SM22_TC1

| Optional Safety Measure |  |  |  |
|---|---|---|---|
| SM22= CRC on configuration data for data retention memory |  |  |  |
| Safety Measure Goal: Configuration registers are protected by CRC. This safety measure checks if there are errors in the retention memory CRC and cannot actively force an error. Only needed if using sleep mode. |  |  |  |
| Notes:  1) These tests are only for safety measure testing, not to be done in normal/production operation. |  |  |  |
| CRC on configuration data for data retention memory |  |  |  |
| When going to sleep, all register data are saved to 1.8V memory to allow the 1.0V digital core voltage to be removed (either internal LDO disabled or main power switch opened). |  |  |  |
| After storing all saved register data, a CRC is calculated based on all the registers and is stored in a separate register. |  |  |  |
| Upon wake up, we restore the all register data from the 1.8V memory to the normal 1.0V digital core registers and re-calculate / match the stored value of the CRC. |  |  |  |
| If the re-calculated value of the CRC and the stored CRC do not match, ERRB is asserted. |  |  |  |
| Verfification |  |  |  |
| To check the error flag (RTTN_CRC_INT) | 0x28 | Bit 3 |  |
| To enable ERRB pin reporting this error (default off) | 0x27 |  |  |
|  |  |  | Pass |

## SM26_TC1

| Default Safety Measure |  |  |  |  |
|---|---|---|---|---|
| SM26_TC1 =GPIO Readback |  |  |  |  |
| Safety Measure Goal: Each GPIO has status bit returning current state of the pin (high or low). This test will force VDDIO voltage on GPIO pin and read back the status. |  |  |  |  |
| Readback of logic state for GPIO |  |  |  |  |
| Notes:  1) If wanting to test MFP pins that have multiple functions, ensure proper GPIO configuration is selected. 2) Each GPIO pin has three registers that are used for programming (A, B, C). For this test we will only need to use register 'A'. 3) There are two ways to test this. One is with internal voltage (see below test setup) or with external voltage. |  |  |  |  |
| There are two ways of testing this functionality,  1) Set GPIO_OUT_DIS=0 and use internal GPIO_OUT=1 bit to force the MFP pin high.  2) Set GPIO_OUT_DIS=1 and provide an external high/low signal on MFP pin.  The status can be read on register GPIO_A, bit 3 (GPIO_IN) |  |  |  |  |
|  | Step | Action | Register Value |  |
|  | 1 | MFP0 GPIO_A Drive bit4 High (GPIO_OUT=1, GPIO_TX_EN=0, GPIO_RX_EN=0, GPIO_OUT_DIS=0) | 0x98, 0x300, 0x10 |  |
|  | 2 | Read GPIO_IN | Bit 3 goes 1 |  |
|  | 3 | GPIO_A Drive bit 4 Low  (GPIO_OUT=0) | 0x98, 0x300, 0x00 |  |
|  | 4 | Read GPIO_IN | Bit 3 goes 0 |  |
|  | 5 | repeat for all the MFPs using respective GPIO_A registers |  |  |
|  |  |  |  | Pass |

## SM27_TC1

| Default Safety Measure |  |
|---|---|
| SM27_TC1= DPLL Lock Detection |  |
| Safety Measure Goal: PLL status registers reflected on the CSIPLLY_LOCK register, this register will lock or unlock depending on if we have valid video source |  |
| DPLL status registers reflect the DPLL LOCK state |  |
| Digital PLL lock indication. CSIPLL_LOCK bit set indicating PLL lock on MIPI controllers. |  |
| Starting on rev C, PLL lock happens at power up and CSIPLL_LOCK bits (for different controllers) are working in accordance with MIPI PHY mode selection (reg 0x8A0). |  |
| Hardware Setup |  |
| Camera/CSI data -> MAX9295A -> MAX96712 |  |
| 1. Have I2C access to MAX96712 locally. |  |
| 2.Establish GMSL2 Link Between MAX9295A and MAX96712 (Link A) error-free. |  |
| - Check ERRB pin and LOCK pin or register 0x1A bit 3 on MAX96712 |  |
| Software Configuration |  |
| Config data path and use video pipe 1 and MIPI control 1 for port A output in 2x4 mode |  |
| Verification |  |
| 0x400 bit 5/6 (CSIPLL1/2_LOCK) bits are asserted for MIPI control 1/2 under 2x4 mode by default; |  |
| Change to 4x2 mode (0x8A0 = 0x01), all 4 CSIPLLx_LOCK bits are asserted. |  |
| Refer to SM28 for buffer overflow indication. |  |
| * 0x400 [7:4] is for CSIPLL_LOCK check on each controller. |  |
| * 0x40A [3:0] Line buffer overflow for pipe 3 - 0; [7:4] command buffer overflow for pipe 3 - 0. |  |
| * 0x42A [3:0] Line buffer overflow for pipe 7 - 4; [7:4] command buffer overflow for pipe 7 - 4. |  |
|  | Pass |

## SM28_TC1

| Default Safety Measure |  |
|---|---|
| SM28_TC1= CSI Controller & DPHY/CPHY Handshake |  |
| Safety Measure Goal: If the Handshake is broken, the Backtop memories would overflow and will be reported in the Status Registers |  |
| CSI Controller & DPHY/CPHY Handshake |  |
| This test requires a valid CSI video through the SerDes. We will reduce the MIPI output clock until the pipeline memory overflows |  |
| Hardware Setup |  |
| Camera/CSI data -> MAX9295A -> MAX96712 |  |
| 1. Have I2C access to MAX96712 locally. |  |
| 2.Establish GMSL2 Link Between MAX9295A and MAX96712 (Link A) error-free. |  |
| - Check ERRB pin and LOCK pin or register 0x1A bit 3 on MAX96712 |  |
| Software Configuration |  |
| Config data path and use video pipe 1 and MIPI control 1 for port A output in 2x4 mode |  |
| Verification |  |
| 0x40A bit 1 (LMO_2) and bit 5 (cmd_overflow2) is clean for data coming out on video pipe 1. |  |
| * 0x40A [3:0] Line buffer overflow for pipe 3 - 0; [7:4] command buffer overflow for pipe 3 - 0. |  |
| * 0x42A [3:0] Line buffer overflow for pipe 7 - 4; [7:4] command buffer overflow for pipe 7 - 4. |  |
| Fault Injection |  |
| If video data from pipe to controller mapping is incorrect, Line buffer and command buffer overflow register bit would set at desired pipe. And if so, no MIPI data would comes out. |  |
|  | Pass |

## SM30_TC1

| Default Safety Measure |  |
|---|---|
| SM30_TC1= Command and Line Memory Overflow |  |
| Safety Measure Goal: If the Video path is broken, the Backtop memories would overflow and will be reported in the Status Registers |  |
| Command / line buffer Overflow |  |
| Command/line buffer overflow indicates received short/long packets are not being sent out from memory to CSI output properly or not fast enough. |  |
| This overflow flag does NOT output to ERRB |  |
| Hardware Setup |  |
| Camera/CSI data -> MAX9295A -> MAX96712 |  |
| 1. Have I2C access to MAX96712 locally. |  |
| 2.Establish GMSL2 Link Between MAX9295A and MAX96712 (Link A) error-free. |  |
| - Check ERRB pin and LOCK pin or register 0x1A bit 3 on MAX96712 |  |
| Software Configuration |  |
| Config data path and use video pipe 1 and MIPI control 1 for port A output in 2x4 mode |  |
| Verification |  |
| 0x40A bit 1 (LMO_2) and bit 5 (cmd_overflow2) is clean for data coming out on video pipe 1. |  |
| * 0x40A [3:0] Line buffer overflow for pipe 3 - 0; [7:4] command buffer overflow for pipe 3 - 0. |  |
| * 0x42A [3:0] Line buffer overflow for pipe 7 - 4; [7:4] command buffer overflow for pipe 7 - 4. |  |
| If MIPI data is correctly configured from video pipe to controllor, LMO and cmd_overflow registers should not assert. |  |
| If the overflow registers are asserted, MIPI data rate could be too low to send out the data, or video pipe to controllor mapping is configured wrong. |  |
| Fault Injection |  |
| Lower the MIPI output data rate. |  |
|  | Pass |

## SM33_TC1

| Optional Safety Measure |  |
|---|---|
| SM33=PRBS Sync an Validation |  |
| Safety Measure Goal: To ensure that PRBS is synchronized |  |
| PRBS Synchronsiation and Validation |  |
| Covered by SM1_TC2 |  |
|  | Pass |

## SM34_TC1

| Default Safety Measure |  |
|---|---|
| SM34_TC1= CRC protection of info frames |  |
| Safety Measure Goal: Infoframes are sent periodically and are CRC protected |  |
| Info frame is sent periodically and checked at receiver, CRC protected |  |
| Info frame is sent periodically and checked at receiver, CRC protected |  |
| Verified through simulation |  |
| The red colored periodic info frame requests are sent to the other side using the gmsl2 link. Valid signal shows that the info frame is sent. |  |
| If error occur, Line CRC error flag would assert. Refer to SM4 for details. |  |
|  | Pass |

## SM35_TC1

| Default Safety Measure |  |
|---|---|
| SM35_TC1= Readback of status for ERRB and LFLT through I2C or UART register |  |
| Safety Measure Goal: read the status of LFLT and ERRB registers using I2C or UART |  |
| Readback of status register informing on ARQ retrials |  |
| Note- If you are not monitoring the ERRB or LFLT MFP pins externally or would like to poll the register bits, it is possible to read the status of these on registers using I2C or UART |  |
| Covered by SM5 |  |
|  | Pass |

## SM36_TC1

| Default Safety Measure |  |
|---|---|
| SM36= GPIO Open Detection |  |
| Safety Measure Goal: To verify whether GPIO pin is being externall driven. |  |
| GPIO open detection |  |
| Notes:  1) Before testing, ensure that desired pin is setup for GPIO operation. Some pins have multiple functions, so GPIO operation must be enabled. 2) If you are able to succesfully read both pull-up/pull-down status of GPIO pin, this means GPIO pin is NOT externaly driven. |  |
| Setup |  |
| 0) GPIO initialization. |  |
| GPIO_A: bit 7 = 1; bit 0 = 1. |  |
| GPIO_B: bit 5 = 0. |  |
| 1) Turn on 1Mohm pull up. |  |
| GPIO_B: bit[7:6] = 2'b01 |  |
| 2) Read back high. |  |
| GPIO_A bit 3 asserts. |  |
| 3) Turn on 1Mohm pull down. |  |
| GPIO_B: bit[7:6] = 2'b10 |  |
| 4) Read back low. |  |
| GPIO_A bit 3 deasserts. |  |
| 5) This GPIO is not driven externally for the fact that its status is changing according to weak 1Mohm pull-up/down. |  |
|  | Pass |

## SM37_Host

| Default Safety Measure |  |
|---|---|
| SM37= Evaluate Mipi CRC |  |
| Safety Measure Goal: verify MIPI CRC at Host |  |
| Evaluate MIPI CRC |  |
| System level verification; Use host recever to check MIPI CRC error on data coming out of MAX96712 |  |
|  | Pass |

## SM40_TC1

| Optional Safety Measure |  |
|---|---|
| SM40=FSYNC Lost of lock |  |
| Safety Measure Goal: Use FSYNC loss of lock to detect changes or loss of video stream |  |
| Frame Sync Lost LOCK |  |
| Notes:  1) Requires a system with an internal FSYNC. |  |
| Hardware Setup |  |
| Camera/CSI data -> MAX9295A -> MAX96712 |  |
| 1. Have I2C access to MAX96712 locally. |  |
| 2.Establish GMSL2 Link Between MAX9295A and MAX96712 (Link A/B/C/D) error-free. |  |
| Software Configuration |  |
| Configure properly with MIPI output in 2x4 mode with internal Frame Sync mode. |  |
| Verification |  |
| Read back 0x4B6 bit 6 (FSYNC_LOCKED) is asserted. |  |
| Fault Injection |  |
| Adjust the threshold at register 0x4AC; |  |
| FSYNC_LOCKED deasserts if lose lock. |  |
|  | Pass |

## SM41_TC1

| Default Safety Measure |  |
|---|---|
| SM41=Memory ECC |  |
| Safety Measure Goal: Verify backtop memory is protected by ECC. |  |
| Notes:  1) Must use I2C driver that has CRC & Message Counter enabled  2) Maxim used GMSL GUI for this test. 3) ERRB asserts when I2C/UART message counter/CRC error is seen  4) ERRB asserts after first message counter/CRC error is seen. Can be programmed to accept more than 1 error before activating ERRB. |  |
| ECC for Back-top Memories |  |
| ECC memories have been included for the line buffer memories. |  |
| 1-bit error is being corrected; 2-bit error is being flagged. |  |
| Hardware Setup |  |
| Camera/CSI data -> MAX9295A -> MAX96712 |  |
| 1. Have I2C access to MAX96712 locally. |  |
| 2.Establish GMSL2 Link Between MAX9295A and MAX96712 (Link A) error-free. |  |
| - Check ERRB pin and LOCK pin or register 0x1A bit 3 on MAX96712 |  |
| Software Configuration |  |
| 0x44 bit 6, MEM_ECC_ERR1_OEN |  |
| output 1-bit ECC error detection to ERRB (default off) |  |
| 0x44 bit 7, MEM_ECC_ERR2_OEN |  |
| output 2-bit ECC error detection to ERRB (default on) |  |
| Verification |  |
| 0x1251, MEM_ECC1 |  |
| Number of 1 bit correctable memory ECC error counts. |  |
| 0x1252, MEM_ECC2 |  |
| Number of 2 bit correctable memory ECC error counts |  |
| 0x1254, MEM_FLUSH (ECC_ERR_FLAG) |  |
| Flag asserts when entire memory has been written to and ECC error report is enabled for each pipe. Type of ECC errors is set by BACKTOP_ECC_ERR_SEL register bit at 0x12A1. |  |
| 0x12A1, SPARE_DIGITAL |  |
| Bit 1: RESET_MEM_FLUSH. Reset all error flags. |  |
| Bit 0: BACKTOP_ECC_ERR_SEL. Default 0x0 is set to 2-bit ECC error; 0x1 to set 1-bit ECC error. |  |
| Fault Injection |  |
| 0x1253, MEM_ECC_ERR_INJ |  |
| Bit 1: Inject 2 error bits for every 39-bit write into ECC memories. |  |
| Bit 0: Inject 1 error bit for every 39-bit write into ECC memories. |  |
|  | Pass |

