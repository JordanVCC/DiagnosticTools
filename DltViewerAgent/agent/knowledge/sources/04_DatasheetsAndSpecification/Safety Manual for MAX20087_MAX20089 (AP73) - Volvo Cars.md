# Safety Manual for MAX20087_MAX20089 (AP73) - Volvo Cars

Source: C:\Users\JHARVEY\OneDrive - Volvo Cars\Documents\01_Resources\04_DatasheetsAndSpecification\Safety Manual for MAX20087_MAX20089 (AP73) - Volvo Cars.pdf

**==> picture [125 x 36] intentionally omitted <==**

**==> picture [105 x 108] intentionally omitted <==**

# **DOCUMENT TITLE: Safety Manual for MAX20087/MAX20089 (AP73)** 

# **DOC ID #     32-100049            NEW REV: F** 

# **ECN#:   1164712 EFFECTIVE DATE:   6/10/2022** 

**ORIGINATOR:   Bernardi, Jacob** 

**==> picture [40 x 38] intentionally omitted <==**

## **MOST RECENT CHANGES** 

Rev E 

**FROM** 

**TO Rev F:** Added references to MAX20087B (section 1) Added WETQFN package type (section 3.1) 

## **Table of Contents** 

|**TITLE:**Safety Manual for MAX20087/MAX20089 (AP73)<br>**DOCUMENT I.D.**<br>32-100049<br>**REVISION**<br>F<br>**PAGE**<br>2<br>**1.**<br>**SCOPE ........................................................................................................................................... 3**<br>**2.**<br>**DISCLAIMER ............................................................................................................................... 3**<br>**3.**<br>**PRODUCT DESCRIPTION .................................................................................................................. 3**<br>**3.1.**<br>**Product Features ...................................................................................................................................................................... 4**<br>**3.2.**<br>**Software / Firmware ................................................................................................................................................................. 4**<br>**4.**<br>**ITEM DEFINITION ........................................................................................................................... 4**<br>**5.**<br>**SYSTEM FUNCTIONS (ITEM LEVEL) ................................................................................................... 5**<br>**6.**<br>**HAZARD ANALYSIS (ITEM LEVEL) ..................................................................................................... 6**<br>**6.1.**<br>**Hazard Analysis for System Function 1 ..................................................................................................................................... 6**<br>**7.**<br>**ASIL DECOMPOSITION FROM ITEM TO ELEMENT LEVEL .................................................................... 7**<br>**8.**<br>**FUNCTIONAL SAFETY CONCEPT (ITEM LEVEL) ................................................................................... 9**<br>**9.**<br>**TECHNICAL SAFETY CONCEPT ........................................................................................................ 11**<br>**9.1.**<br>**Technical Safety Requirements for MAX20087 ...................................................................................................................... 12**<br>**9.2.**<br>**Dependent Failure Analysis .................................................................................................................................................... 13**<br>**9.3.**<br>**Safety Measures for MAX20087 ............................................................................................................................................. 14**<br>**9.4.**<br>**Assumptions of Use ................................................................................................................................................................. 16**<br>**9.5.**<br>**Fault Indication and Communication...................................................................................................................................... 17**<br>**10.**<br>**VERIFICATION OF ASIL LEVEL......................................................................................................... 18**<br>**10.1.**<br>**FTA of MAX20087 ................................................................................................................................................................ 18**<br>**10.2.**<br>**FMEDA of MAX20087 .......................................................................................................................................................... 19**<br>**10.2.1.**<br>**FMEDA Example for Function EF 2.1, Block FB1**............................................................................................................. 20<br>**10.3.**<br>**Verification results of Safety Measures .............................................................................................................................. 20**<br>**10.4.**<br>**FMEDA Summary ................................................................................................................................................................. 21**|**TITLE:**Safety Manual for MAX20087/MAX20089 (AP73)<br>**DOCUMENT I.D.**<br>32-100049<br>**REVISION**<br>F<br>**PAGE**<br>2<br>**1.**<br>**SCOPE ........................................................................................................................................... 3**<br>**2.**<br>**DISCLAIMER ............................................................................................................................... 3**<br>**3.**<br>**PRODUCT DESCRIPTION .................................................................................................................. 3**<br>**3.1.**<br>**Product Features ...................................................................................................................................................................... 4**<br>**3.2.**<br>**Software / Firmware ................................................................................................................................................................. 4**<br>**4.**<br>**ITEM DEFINITION ........................................................................................................................... 4**<br>**5.**<br>**SYSTEM FUNCTIONS (ITEM LEVEL) ................................................................................................... 5**<br>**6.**<br>**HAZARD ANALYSIS (ITEM LEVEL) ..................................................................................................... 6**<br>**6.1.**<br>**Hazard Analysis for System Function 1 ..................................................................................................................................... 6**<br>**7.**<br>**ASIL DECOMPOSITION FROM ITEM TO ELEMENT LEVEL .................................................................... 7**<br>**8.**<br>**FUNCTIONAL SAFETY CONCEPT (ITEM LEVEL) ................................................................................... 9**<br>**9.**<br>**TECHNICAL SAFETY CONCEPT ........................................................................................................ 11**<br>**9.1.**<br>**Technical Safety Requirements for MAX20087 ...................................................................................................................... 12**<br>**9.2.**<br>**Dependent Failure Analysis .................................................................................................................................................... 13**<br>**9.3.**<br>**Safety Measures for MAX20087 ............................................................................................................................................. 14**<br>**9.4.**<br>**Assumptions of Use ................................................................................................................................................................. 16**<br>**9.5.**<br>**Fault Indication and Communication...................................................................................................................................... 17**<br>**10.**<br>**VERIFICATION OF ASIL LEVEL......................................................................................................... 18**<br>**10.1.**<br>**FTA of MAX20087 ................................................................................................................................................................ 18**<br>**10.2.**<br>**FMEDA of MAX20087 .......................................................................................................................................................... 19**<br>**10.2.1.**<br>**FMEDA Example for Function EF 2.1, Block FB1**............................................................................................................. 20<br>**10.3.**<br>**Verification results of Safety Measures .............................................................................................................................. 20**<br>**10.4.**<br>**FMEDA Summary ................................................................................................................................................................. 21**|**TITLE:**Safety Manual for MAX20087/MAX20089 (AP73)<br>**DOCUMENT I.D.**<br>32-100049<br>**REVISION**<br>F<br>**PAGE**<br>2<br>**1.**<br>**SCOPE ........................................................................................................................................... 3**<br>**2.**<br>**DISCLAIMER ............................................................................................................................... 3**<br>**3.**<br>**PRODUCT DESCRIPTION .................................................................................................................. 3**<br>**3.1.**<br>**Product Features ...................................................................................................................................................................... 4**<br>**3.2.**<br>**Software / Firmware ................................................................................................................................................................. 4**<br>**4.**<br>**ITEM DEFINITION ........................................................................................................................... 4**<br>**5.**<br>**SYSTEM FUNCTIONS (ITEM LEVEL) ................................................................................................... 5**<br>**6.**<br>**HAZARD ANALYSIS (ITEM LEVEL) ..................................................................................................... 6**<br>**6.1.**<br>**Hazard Analysis for System Function 1 ..................................................................................................................................... 6**<br>**7.**<br>**ASIL DECOMPOSITION FROM ITEM TO ELEMENT LEVEL .................................................................... 7**<br>**8.**<br>**FUNCTIONAL SAFETY CONCEPT (ITEM LEVEL) ................................................................................... 9**<br>**9.**<br>**TECHNICAL SAFETY CONCEPT ........................................................................................................ 11**<br>**9.1.**<br>**Technical Safety Requirements for MAX20087 ...................................................................................................................... 12**<br>**9.2.**<br>**Dependent Failure Analysis .................................................................................................................................................... 13**<br>**9.3.**<br>**Safety Measures for MAX20087 ............................................................................................................................................. 14**<br>**9.4.**<br>**Assumptions of Use ................................................................................................................................................................. 16**<br>**9.5.**<br>**Fault Indication and Communication...................................................................................................................................... 17**<br>**10.**<br>**VERIFICATION OF ASIL LEVEL......................................................................................................... 18**<br>**10.1.**<br>**FTA of MAX20087 ................................................................................................................................................................ 18**<br>**10.2.**<br>**FMEDA of MAX20087 .......................................................................................................................................................... 19**<br>**10.2.1.**<br>**FMEDA Example for Function EF 2.1, Block FB1**............................................................................................................. 20<br>**10.3.**<br>**Verification results of Safety Measures .............................................................................................................................. 20**<br>**10.4.**<br>**FMEDA Summary ................................................................................................................................................................. 21**|
|---|---|---|
|**TITLE:**Safety Manual for MAX20087/MAX20089 (AP73)|||
|**DOCUMENT I.D.**<br>32-100049|**REVISION**<br>F|**PAGE**<br>2|



**APPENDIX ............................................................................................................................................. 22** 

**TERMS AND DEFINITIONS ...................................................................................................................... 23** 

**==> picture [46 x 49] intentionally omitted <==**

## **1. Scope** 

The scope of this document is to provide information about the fail-safe functionality of the product MAX20087/B & MAX20089. In the following chapters certain functionality of the MAX20087 has been selected to be shown as an example.  Because MAX20087 has a superset of features (i.e. MAX20087B & MAX20089 has a subset of the features of MAX20087), this Safety Manual will provide all information from the perspective of MAX20087 and will apply by extension to MAX20087B & MAX20089. All the details can be reviewed as part of the Safety Case. 

**==> picture [69 x 61] intentionally omitted <==**

## **2. Disclaimer** 

Maxim Integrated provides documentation for functional safety products. Within this documentation, Maxim Integrated has defined assumptions of use and operational boundary conditions. Based on these assumptions and boundary conditions, the capability of a product specific ASIL level has been assessed. Maxim’s goal is to support customers to design and create their own end-product solutions that meet applicable functional safety standards and requirements. For this reason, Maxim Integrated does not guarantee ASIL compliance on a system level.  The customer is fully responsible to perform the integration testing to confirm ASIL compliance on a system level.  Maxim Integrated will not be liable for any claim or damage arising from customer’s use of a Maxim Integrated product in a life support, life critical, or safety critical system, equipment or application. Customer will indemnify, defend and hold Maxim Integrated harmless from and against any and all claims, damages, losses, costs, expenses, and liabilities arising out of the use of any Maxim Integrated product in any of these any such system, equipment or application. Maxim Integrated does not make any warranty as to the accuracy or completeness of this documentation and shall have no liability for its content. 

## **3. Product description** 

The MAX20087 is a product specifically designed for automotive application including fail safe functionality based on ISO26262. It is a quad-channel (dual-channel for MAX20089) power protector for power-over-coax applications, specifically intended for remote-camera applications. It is compliant with ASIL-B ratings as a standalone unit. It also has a digital interface to allow an external MCU or SoC to access advanced diagnostic and measurement functions in the MAX20087 IC for compliance with up to ASIL-D rating. 

**TITLE:** Safety Manual for MAX20087/MAX20089 (AP73) 

**==> picture [82 x 23] intentionally omitted <==**

**DOCUMENT I.D. REVISION PAGE** 32-100049 F 3 

## **3.1. Product Features** 

The MAX20087 provides the following features: 

- Small Solution 

   - Up to four 600mA protection switches 

   - 3V to 15V input supply 

   - 3V to 5.5V device supply 

   - 26V short-to-battery isolation 

   - Adjustable current limit (100mA to 600mA) 

   - Selectable I²C addresses 

   - Small (4mm x 4mm) 20-pin SWTQFN and WETQFN packages 

- Precision 

   - ±8% current limit 

   - 0.5ms soft-start 

   - 0.25ms soft-shutdown 

   - 0.3µA shutdown current 

   - 110mV drop at 300mA 

- Designed for Safety Applications 

   - ASIL B/D compliant 

   - Short to VBAT / GND diagnostics 

   - Differential output over/undervoltage diagnostics 

   - Input over/undervoltage diagnostics 

   - Individual 8-bit current, output voltage, and supply readings over I²C 

- AEC-Q100, -40°C to +125°C 

## **3.2. Software / Firmware** 

The MAX20087 has a digital interface for use with an external MCU or SoC which may contain specialized software and/or firmware. (This is required to meet ASIL D performance metrics.) However, the IC itself does not contain any software or firmware. 

## **4. Item Definition** 

The product MAX20087 is defined as an element and consists of components which are identical to the individual functional blocks of the design. One or more elements grouped together build an item. On the Item level the Hazard analysis is performed, and Safety Goals are defined. 

A block diagram of the Item of Product MAX20087 is shown in the figure below. 

**==> picture [82 x 23] intentionally omitted <==**

**TITLE:** Safety Manual for MAX20087/MAX20089 (AP73) **DOCUMENT I.D. REVISION PAGE** 32-100049 F 4 

**==> picture [471 x 277] intentionally omitted <==**

**==> picture [59 x 62] intentionally omitted <==**

_Figure 1: Item with element MAX20087_ 

**==> picture [91 x 96] intentionally omitted <==**

The elements of the Item are defined as follows: 

Element 1: “DC-DC Converter” Function EF1.1: Generate input supply voltage 

Element 2: “MAX20087” 

Function EF2.1: Provide output supply voltage to cameras on channels OUT1/2/3/4 

Element 3: “Host CPU” Function EF3.1: Control ADAS camera system Function EF3.2: Process and provide ADAS support to driver interface 

Elements 4/5/6/7: “Cameras 1/2/3/4” 

Function: Perform camera sensor function 

**==> picture [35 x 33] intentionally omitted <==**

## **5. System Functions (Item Level)** 

The MAX20087 supports System Functions as listed below: 

System Function 1 ( **SF1** ): _“Provide protected power to cameras on output supply channels OUT1/2/3/4”_ 

In this document the relevant System Functions will be considered in the Hazard Analysis, Functional Safety Concept, Technical Safety Concept and FMEDA. 

**TITLE:** Safety Manual for MAX20087/MAX20089 (AP73) 

**==> picture [82 x 23] intentionally omitted <==**

**DOCUMENT I.D. REVISION PAGE** 32-100049 F 5 

## **6. Hazard Analysis (item level)** 

The Hazard Analysis is performed for each safety related System Function of Item. 

## **6.1. Hazard Analysis for System Function 1** 

**==> picture [37 x 34] intentionally omitted <==**

The following **Malfunctions** (MF) are considered in combined situations with specific road conditions for SF1: 

Malfunction 1 ( **MF1** ): _No power provided to cameras on output supply channels OUT1/2/3/4”_ Malfunction 2 ( **MF2** ): _Improper power provided to cameras on output supply channels OUT1/2/3/4”_ 

The applicable road conditions for the Item are as follows: 

Road Condition 1: Parking Road Condition 2: Stop & Go in the City Road Condition 3: Driving in Highway 

**TITLE:** Safety Manual for MAX20087/MAX20089 (AP73) 

**==> picture [82 x 23] intentionally omitted <==**

**DOCUMENT I.D.** 32-100049 

**REVISION PAGE** F 6 

The maximum ASIL level from the Hazard analysis is applicable for the System Function. 

||||||
|---|---|---|---|---|
||Road Condition 1|Road Condition 2|Road Condition 3||
|**MF1:**<br>Malfunction 1<br>No power<br>provided to<br>cameras on<br>output supply<br>channels<br>OUT1/2/3/4|S: 2<br>E: 4<br>C: 3<br>**ASIL C**|S: 3<br>E: 4<br>C: 3<br>**ASIL D**|S: 3<br>E: 4<br>C: 2<br>**ASIL C**||
|**MF2:**<br>Malfunction 2<br>Improper power<br>provided to<br>cameras on<br>output supply<br>channels<br>OUT1/2/3/4|S: 2<br>E: 4<br>C: 3<br>**ASIL C**|S: 3<br>E: 4<br>C: 3<br>**ASIL D**|S: 3<br>E: 4<br>C: 2<br>**ASIL C**||



**==> picture [59 x 62] intentionally omitted <==**

_Table 1: Hazard Analysis for System Function 1_ 

**==> picture [45 x 45] intentionally omitted <==**

S - Severity to drivers Health or Life (S0, S1, S2, S3) 

- E - Exposure:  Probability to drive under those conditions (E0, E1, E2, E3, E4) 

- C - Controllability of car in case of malfunction under specific exposure condition (C0,C1,C2,C3) 

The results of the hazard analysis show that the required Item Level compliance be ASIL D. 

## **7. ASIL Decomposition from Item to Element level** 

If redundancy is used, the ISO 26262 allows de-rating of the ASIL-Level under certain conditions. This procedure is known as ASIL decomposition. 

The MAX20087 supports ASIL decomposition. The part itself is compliant with ASIL B rating. When combined with a supervisor system of ASIL B rating or higher (enabling additional voltage and current readings through the ADC), the combination of the two meet the required ASIL D level per the hazard analysis above. 

**==> picture [57 x 48] intentionally omitted <==**

**TITLE:** Safety Manual for MAX20087/MAX20089 (AP73) 

**==> picture [82 x 23] intentionally omitted <==**

**DOCUMENT I.D. REVISION PAGE** 32-100049 F 7 

**==> picture [540 x 365] intentionally omitted <==**

_Figure 2: ASIL Decomposition at Item Level, Including MAX20087_ 

**==> picture [456 x 230] intentionally omitted <==**

_Figure 3: ASIL Decomposition per ISO26262_ 

**TITLE:** Safety Manual for MAX20087/MAX20089 (AP73) 

**==> picture [82 x 23] intentionally omitted <==**

**DOCUMENT I.D.** 32-100049 

**REVISION PAGE** F 8 

## **8. Functional Safety Concept (Item Level)** 

The Functional Safety Concept describes the Safety Goals and the Safe States for the relevant System Functions. Furthermore, the Fault Tolerant Time, which defines the time until the system goes in to safe state, has to be considered. 

**==> picture [59 x 62] intentionally omitted <==**

The Safety Goals (SG) of SF1 are as follow: 

## **SG1:** Voltage loss on output channels 1/2/3/4 should be detected 

|**G1:**Voltage loss on output channels 1/2/3/4 should be detected|**G1:**Voltage loss on output channels 1/2/3/4 should be detected|**G1:**Voltage loss on output channels 1/2/3/4 should be detected|**G1:**Voltage loss on output channels 1/2/3/4 should be detected|**G1:**Voltage loss on output channels 1/2/3/4 should be detected|**G1:**Voltage loss on output channels 1/2/3/4 should be detected|**G1:**Voltage loss on output channels 1/2/3/4 should be detected|||
|---|---|---|---|---|---|---|---|---|
|<br>**G2:**Out-of-bounds power on output channels 1/2/3/4 should be detected|||||||||
|||**Item Level Hazard Analysis**|||**Element**||**Level**||
|**System**<br>**Function**|**ASIL**|**Safety**<br>**Goal**|**Fault**<br>**Tolerant**<br>**Time**|**Safe State**|**Element**<br>**and/or**<br>**Component**<br>**Function**|**ASIL**|**Safety**<br>**Goal**|**Fault**<br>**Tolerant**<br>**Time**|
|SF1|D|SG1|<40ms|The corresponding channel is<br>switched off and a fault signal<br>asserted|EF2.1|B|**SG1**|<40ms|
||D|SG2|<40ms|The corresponding channel is<br>switched off and a fault signal<br>asserted|EF2.1|B|**SG2**|<40ms|
|_able 2: Functional_||_Safety Concept_|||||||



**SG2:** Out-of-bounds power on output channels 1/2/3/4 should be detected 

_Table 2: Functional Safety Concept_ 

The Functional Tree corresponding to the defined Functional Safety Concept for MAX20087 is given in the figure below: 

**==> picture [192 x 186] intentionally omitted <==**

**TITLE:** Safety Manual for MAX20087/MAX20089 (AP73) 

**==> picture [82 x 23] intentionally omitted <==**

**DOCUMENT I.D.** 32-100049 

**REVISION PAGE** F 9 

**==> picture [531 x 552] intentionally omitted <==**

**----- Start of picture text -----**<br>
CF1.1: Connect Input to Output Channels<br>EF1: Provide power to cameras Allocation: OCP FET, RB FET, OCP Charge Pump & Driver, RB<br>Charge Pump & Driver, Control & Diagnostic Logic, Clock, OTP,<br>Bandgap, Current Set Loop & SW Common<br>SF1: Provide protected  CF2.1: Detect Over/Undervoltage on Input Channel<br>power to cameras on output  Allocation: IN OV Comp, IN UV Comp, Control & Diagnostics<br>supply channels OUT1/2/3/4 Logic, Clock, OTP, Bandgap<br>EF2: Detect overvoltage,  CF2.2: Detect Over/Undervoltage on Output Channels<br>undervoltage, and overcurrent  Allocation: OUT OV Comp, OUT UV Comp, Control &<br>conditions Diagnostics Logic, Clock, OTP, Bandgap<br>CF2.3: Detect Overcurrent on Output Channels<br>Allocation: Current Sense Amplifier, Current Set Loop, Control<br>& Diagnostics Logic, Clock, OTP, Bandgap, Current Set Loop &<br>SW Common<br>CF2.4: Communicate Fault Status to Host Controller<br>Allocation: Control & Diagnostics Logic, I²C Interface, Clock,<br>OTP<br>CF3.1: Disconnect on Over/Undervoltage on Input Channel<br>Allocation: OCP FET, OCP Charge Pump & Drivers, Current Set<br>Loop & SW Common, Control & Diagnostics Logic, Clock, OTP<br>EF3: Disconnect channel upon  CF3.2: Disconnect on Over/Undervoltage on Output Channels<br>detection of fault condition Allocation: RB FET, RB Charge Pump & Drivers, Current Set<br>Loop & SW Common, Control & Diagnostics Logic, Clock, OTP<br>CF3.3: Disconnect on Overcurrent on Output Channels<br>Allocation: OCP FET, OCP Charge Pump & Drivers, Current Set<br>Loop & SW Common, Control & Diagnostics Logic, Clock, OTP<br>CF4.1: Measure Voltage on Input Channel<br>Allocation: Control & Diagnostics Logic, Clock, OTP, Bandgap<br>ADC & Analog Sense Circuitry<br>EF4: Measure voltages and  CF4.2: Measure Voltage on Output Channels<br>currents and communicate  Allocation: Control & Diagnostics Logic, Clock, OTP, Bandgap<br>measurements to host  ADC & Analog Sense Circuitry<br>controller<br>CF4.3: Measure Current on Output Channels<br>Allocation: Current Sense Amplifier, Current Set Loop & SW<br>Common, Control & Diagnostics Logic, Clock, OTP, Bandgap,<br>ADC & Analog Sense Circuitry<br>CF4.4: Communicate Measurement Results to Host Controller<br>Allocation: Control & Diagnostics Logic, I²C Interface, Clock,<br>OTP<br>**----- End of picture text -----**<br>


_Figure 4: Functional Tree for MAX20087_ 

**==> picture [41 x 40] intentionally omitted <==**

**TITLE:** Safety Manual for MAX20087/MAX20089 (AP73) 

**==> picture [82 x 23] intentionally omitted <==**

**DOCUMENT I.D.** 32-100049 

**REVISION PAGE** F 10 

## **9. Technical Safety Concept** 

Technical Safety Concept specifies how the required functionality of the IC is implemented. Special focus is on diagnostics and safety measures. To show the basic principles of the technical safety concept, partitioning of item into elements is done and each element has certain and separate functionality within the Item. Each element is made up of various components and functional blocks. This safety manual focuses on Element 2: MAX20087. 

The Technical Safety Concept describes the realization of Functional Safety Concept at hardware (Item) level and is shown in the following block diagram. 

**==> picture [540 x 441] intentionally omitted <==**

_Figure 5: Technical Safety Concept for MAX20087, including the Block Diagram_ 

The Technical Safety Concept is described as follows: 

**TITLE:** Safety Manual for MAX20087/MAX20089 (AP73) 

**==> picture [82 x 23] intentionally omitted <==**

**DOCUMENT I.D.** 32-100049 

**REVISION PAGE** F 11 

**“Power loss and out-of-bounds power on input and all output channels are detected through built-in Safety Mechanisms. As a consequence of out-of-bounds power, the corresponding channels are switched off and the fault status is communicated to external elements.”** 

## **9.1. Technical Safety Requirements for MAX20087** 

**==> picture [81 x 84] intentionally omitted <==**

The specific Technical Safety Requirements with respect to Safety Mechanism for detection of internal failures (ISO26262-4/6.4.2.2) for MAX20087 are specified in the table below for all element functions EF2, EF3, and EF4. 

|EF4.|||||||||
|---|---|---|---|---|---|---|---|---|
||||||||||
|**Element**<br>**Function**||||||**Diagnostic**|**Diagnostic**||
||**Functional**|**Fault**|**Faults to be**|**Safety**|||||
||||||**Description**|<br>**Test**|<br>**Limit**|**Fault Reaction State**|
||<br>**Blocks**|**Type**|**Detected**|**Measures**|||||
|||||||**Interval**|**Window**||
||||||||||
|EF2, EF3|FB1, FB9,<br>FB10,FB16|External|Overcurrent on<br>Output Channel 1|SM1|Overcurrent<br>detection|< 40 msec|±8%|Channel 1 switched<br>off,fault asserted(1)|
|EF2, EF3|FB1, FB9,<br>FB10, FB16|External|Overcurrent on<br>Output Channel 2|SM1|Overcurrent<br>detection|< 40 msec|±8%|Channel 2 switched<br>off, fault asserted|
|EF2, EF3|FB1, FB9,<br>FB10, FB16|External|Overcurrent on<br>Output Channel 3|SM1|Overcurrent<br>detection|< 40 msec|±8%|Channel 3 switched<br>off, fault asserted|
|EF2, EF3|FB1, FB9,<br>FB10,FB16|External|Overcurrent on<br>Output Channel 4|SM1|Overcurrent<br>detection|< 40 msec|±8%|Channel 4 switched<br>off,fault asserted|
|EF2, EF3|FB2, FB10,<br>FB16|External|Overvoltage on<br>Input Channel|SM6|Input voltage<br>monitor|Continuous|0.70V ±<br>170mV|All channels switched<br>off, fault asserted|
|EF2, EF3|FB5, FB10,<br>FB16|External|Overvoltage on<br>Output Channel 1|SM2|Overvoltage<br>detection|< 10 µsec|0.15V ±<br>150mV|Channel 1 switched<br>off, fault asserted|
|EF2, EF3|FB5, FB10,<br>FB16|External|Overvoltage on<br>Output Channel 2|SM2|Overvoltage<br>detection|< 10 µsec|0.15V ±<br>150mV|Channel 2 switched<br>off,fault asserted|
|EF2, EF3|FB5, FB10,<br>FB16|External|Overvoltage on<br>Output Channel 3|SM2|Overvoltage<br>detection|< 10 µsec|0.15V ±<br>150mV|Channel 3 switched<br>off, fault asserted|
|EF2, EF3|FB5, FB10,<br>FB16|External|Overvoltage on<br>Output Channel 4|SM2|Overvoltage<br>detection|< 10 µsec|0.15V ±<br>150mV|Channel 4 switched<br>off, fault asserted|
|EF2, EF3|FB2, FB10,<br>FB16|External|Undervoltage on<br>Input Channel|SM7|Input voltage<br>monitor|Continuous|0.20V ±<br>150mV|All channels switched<br>off, fault asserted|
|EF2, EF3|FB6, FB10,<br>FB16|External|Undervoltage on<br>Output Channel 1|SM3|Undervoltage<br>detection|< 10 µsec|0.55V ±<br>40mV|Channel 1 switched<br>off, fault asserted|
|EF2, EF3|FB6, FB10,<br>FB16|External|Undervoltage on<br>Output Channel 2|SM3|Undervoltage<br>detection|< 10 µsec|0.55V ±<br>40mV|Channel 2 switched<br>off, fault asserted|
|EF2, EF3|FB6, FB10,<br>FB16|External|Undervoltage on<br>Output Channel 3|SM3|Undervoltage<br>detection|< 10 µsec|0.55V ±<br>40mV|Channel 3 switched<br>off, fault asserted|
|EF2, EF3|FB6, FB10,<br>FB16|External|Undervoltage on<br>Output Channel 4|SM3|Undervoltage<br>detection|< 10 µsec|0.55V ±<br>40mV|Channel 4 switched<br>off, fault asserted|
|EF2, EF3|FB5, FB10,<br>FB11|Internal|Stuck high/low(2)|SM4|OV comparator<br>diagnostics|Start up|Pass/Fail|Fault asserted|
|EF2, EF3|FB6, FB10,<br>FB11|Internal|Stuck high/low(2)|SM5|UV comparator<br>diagnostics|Start up|Pass/Fail|Fault asserted|
|EF2,<br>EF3, EF4|FB13|Internal|Single bit fault|SM8|ECC on OTP|Continuous|Pass/Fail|IC safe state<br>maintained|
|EF4|FB11, FB17|Internal|Stuck high/low,<br>offset, and gain<br>errors(2)|SM9|ADC diagnostics|Start up|Pass/Fail|None|



_Table 3: Technical Safety Requirements for MAX20087_ 

## _**Notes:**_ 

**TITLE:** Safety Manual for MAX20087/MAX20089 (AP73) 

**==> picture [82 x 23] intentionally omitted <==**

**DOCUMENT I.D. REVISION PAGE** 32-100049 F 12 

- (1) Fault assertion is accomplished in two ways: In a standalone implementation (no host controller), any detected fault condition will set a bit in an I²C register that is mirrored to a digital output pin. When used in conjunction with a host controller, the register that contains the fault can be read directly through the I²C communication interface. The host controller can also configure the behavior of the digital output pin, masking certain faults on or off. (By default, all faults will still trigger the output pin as described previously.) 

- (2) Requires host controller & software to conduct test / detect fault 

- (3) Technical Safety Requirements have been determined from the Technical Safety Concepts. Additional Safety Mechanisms are applicable to reach a certain ASIL level (refer to sections 9.3 and 9.4) 

## **9.2. Dependent Failure Analysis** 

**==> picture [92 x 95] intentionally omitted <==**

Dependent failures are described in the following table. An entry in the corresponding cell indicates the dependent functional block. For any dependent failure it is indicated which Safety Measure detects this failure. 

**==> picture [555 x 267] intentionally omitted <==**

**----- Start of picture text -----**<br>
Name FB FB1 FB2 FB3 FB4 FB5 FB6 FB7 FB8 FB9 FB10 FB11 FB12 FB13 FB14 FB15 FB16 FB17<br>SM1,<br>Current Sense Amplifier FB1 SM5 SM3<br>SM4,  SM4,<br>Input OV/UV Comparator FB2 SM10 SM10<br>Overcurrent Protection FET FB3<br>Reverse Blocking FET FB4<br>SM4,<br>Output OV Comparator FB5 SM10<br>Output UV Comparator FB6 SM10<br>SM5,<br>OCP FET Charge Pump & Drivers FB7 SM10<br>SM3,<br>RB FET Charge Pump & Drivers FB8 SM11<br>SM3,  SM3,<br>Current Set Loop & Switches Common FB9 SM11 SM11<br>Control & Diagnostics Logic FB10 SM5 SM5 SM5<br>I²C Interface FB11 SM5<br>Clock FB12 SM5 SM5 SM5 SM5<br>OTP FB13 SM7 SM7 SM7<br>Thermal Shutdown FB14<br>IC Supply UVLO FB15 SM8 SM8 SM8<br>Bandgap FB16 SM8 SM8 SM8 SM8 SM8 SM8 SM8 SM8 SM8 SM8<br>ADC & Analog Sense Circuitry FB17<br>**----- End of picture text -----**<br>


_Table 4: Common Mode interaction Matrix_ 

_**Note 1 :** The dependent failure analysis is based on the Technical Safety Concept (refer to section 9.1)_ 

**==> picture [76 x 76] intentionally omitted <==**

**TITLE:** Safety Manual for MAX20087/MAX20089 (AP73) 

**==> picture [82 x 23] intentionally omitted <==**

**DOCUMENT I.D.** 32-100049 

**REVISION PAGE** F 13 

## **9.3. Safety Measures for MAX20087** 

**==> picture [59 x 62] intentionally omitted <==**

The list of defined Safety Measures for MAX20087 as a part of the Technical Safety Concept is described in the table below. 

|**Safety**<br>**Mechanism**|**Description**|**Fault to be**<br>**detected**|**Circuit**<br>**Block**|**Operational**<br>**Mode and**<br>**DTI**|**Operational**<br>**Mode and**<br>**DTI**|**Fault Reaction state**|**Comment**|
|---|---|---|---|---|---|---|---|
|**SM1**|Over-current<br>detection on<br>Channels<br>1/2/3/4|Over-current<br>output channels|External<br>fault|Continuous<br>< 30 ms||I2C register set|Built In - diagnostics<br>(ASIL B)|
||Over-voltage<br>detection on|Over-voltage on|External|Continuous||Channel switched off|Built - In diagnostics|
|**SM2**|<br>Channels<br>1/2/3/4|<br>output channels|<br>fault|<br>< 10 us||,<br>I2C register set|<br>(ASIL B)|
|**SM3**|Under-<br>voltage<br>detection on<br>Channels<br>1/2/3/4|Under-voltage on<br>output channels|External<br>fault|Continuous<br>< 10 us||Channel switched off I2C<br>register set|Built - In diagnostics<br>(ASIL B)|
|**SM4**|OV<br>comparator<br>diagnostics|Stuck at<br>High/Low|OV<br>Comparator|Start up||I2C register set|Built - In diagnostics<br>(ASIL B)|
|**SM5**|UV<br>comparator<br>diagnostics|Stuck at High/Low|UV<br>Comparator|Start up||I2C register set|Built - In diagnostics<br>(ASIL B)|
|**SM6**|Input Voltage<br>Monitor|Under-Voltage on<br>Input Channel|External|Continuous<br>< 10 us||All Channels switched off,<br>I2Cregisterset|Built - In diagnostics<br>(ASIL B)|
|**SM7**|ECC on OTP|Single Bit Fault|OTP|Continuous||1-bit error correction|Built - In diagnostics<br>(ASIL B)|
|**SM8**|ADC<br>Diagnostics<br>(requires host<br>uC)|Stuck, offset and<br>gain errors|ADC|Start Up||Safe state at item level|Needed to support<br>ASIL D(*2)|
|**SM9**|Current<br>readings<br>through ADC<br>(requires host<br>uC)|Output channel<br>open detection<br>(zero current)|External|once per FTTI<br><1.1ms(time<br>for a current<br>reading)<br>As needed by<br>application||Safe state at item level|Needed to support<br>ASIL D(*2)|
|**SM10**|Voltage<br>readings<br>through ADC<br>(requires host<br>uC)|OV and UV on<br>output channels,<br>input channels|External|once per FTTI<br><1.1ms(time<br>for a voltage<br>reading)<br>As needed by<br>application||Safe state at item level|Needed to support<br>ASIL D(*2)|
|**SM11**|Iset<br>comparator<br>diagnostics|Verify comparator<br>for current limit<br>setting|Iset Loop|once per FTTI||Safe state at item level|Needed to support<br>ASIL D(*2)|
|**TITLE:**Safety Manual for MAX20087/MAX20089 (AP73)<br>**DOCUMENT I.D.**<br>32-100049<br>**REVISION**<br>F<br>**PAGE**<br>14||||||||
|**DOCUMENT I.D.**<br>32-100049|||||**REVISION**<br>F|||



**TITLE:** Safety Manual for MAX20087/MAX20089 (AP73) 

**==> picture [82 x 23] intentionally omitted <==**

**DOCUMENT I.D. REVISION PAGE** 32-100049 F 14 

||(requires host<br>uC)|||<1.1ms(time<br>for verification)<br>As needed by<br>application|||
|---|---|---|---|---|---|---|
|**SM12**|ACK on I2C|Verify peer<br>recognition (every<br>data packet)|Internal/<br>External|Continuous<br>< 50us (time for<br>NACK)|Safe state at item level|Standard feature of<br>I2C interface,<br>Needed to support<br>ASIL D( *2)|
|**SM13**|Verification of<br>UVLO<br>comparator|Verify ADC voltage<br>reading: voltage<br>readings will be<br>zero in case of<br>stuck high. In case<br>of UVLO stuck low,<br>no effect in normal<br>operation (dual<br>pointfault)|Internal|once per FTTI<br><1.1ms(time<br>for a voltage<br>reading)<br>As needed by<br>application|Safe state at item level|Needed to support<br>ASIL D(*2)|
|**SM14**|Verification of<br>thermal limit<br>on output<br>channels|In case of thermal<br>limit reached for a<br>specific channel,<br>the channel is<br>turned off|Internal|Continuous<br>< 10us (time for<br>turning off the<br>channels)|Thermal limited channel<br>switched off, I2C register set|Individual thermal<br>sensors for each<br>channel|
|**SM15**|Monitoring of<br>INT Pin|A fault can be<br>recognized by<br>monitoring the INT<br>pin. The INT pin<br>will be high when<br>EN is low and then<br>go low as soon as<br>EN goes high.  If<br>there are no faults<br>INT will go high<br>after all four<br>outputs are up and<br>running.|Internal|Continuous<br><10us|Safe state at item level|Needed to support<br>ASIL D(*2)|
|**SM16**|I2C<br>Diagnostics|Time Related<br>Redundancy:<br>Any write<br>confirmed with a<br>read, any read<br>confirmed by a 2nd<br>readwithin FTTI|Internal/<br>External|Continuous<br>< 100us (time<br>for one register<br>read or write)|Safe state at item level|Needed to support<br>ASIL D(*2)|
|**SM17**|OCP FET<br>Switching<br>Diagnostics|Measure output<br>current with the<br>ADC during power-<br>up.<br>During power up<br>the channels are<br>open and there<br>should be no<br>output current.<br>Also this can be<br>read via the (VIN-<br>VOUT) reading as<br>there should be <<br>1V drop, when<br>there should be<br>maximum drop<br>(0xFF) (>3V).|Internal|Start up|Safe state at item level|Needed to support<br>ASIL D(*2)|
|**SM18**|Reverse<br>Blocking FET<br>switch<br>diagnostics|The following<br>procedure can be<br>applied to detect<br>that the Reverse<br>Blocking FET is<br>stuck closed:<br>During an output to<br>VBAT (14V) short<br>condition, 14V will<br>be back fed to the|Internal|once per  FTTI<br>< 1.1ms (time<br>for volage read<br>of VIN)<br>As needed by<br>application|Safe state at item level|Needed to support<br>ASIL D(*2)|



**TITLE:** Safety Manual for MAX20087/MAX20089 (AP73) 

**==> picture [82 x 23] intentionally omitted <==**

**DOCUMENT I.D.** 32-100049 

**REVISION PAGE** F 15 

**==> picture [73 x 146] intentionally omitted <==**

**----- Start of picture text -----**<br>
input supply and<br>will be detectable<br>via ADC reading of<br>IN.<br>The VIN<br>measurement<br>should be at a rate<br>considerable faster<br>than FTTI to<br>prevent damage. In<br>case of a fault<br>condition, the<br>device needs to be<br>externally disabled<br>and channels<br>switched off.<br>**----- End of picture text -----**<br>


_Table 5: Safety Measures for MAX20087_ 

**==> picture [92 x 95] intentionally omitted <==**

**Note 1:** Safety Mechanisms indicated as “ASIL B” (SM1-SM7) shall be enabled to achieve ASIL B target according to section 10.4, Table 9/11. 

**Note 2:** To achieve ASIL D target metrics as described in section 10.4, Table 10/12 the following Safety Mechanisms shall be enabled and implemented: SM8, SM9, SM10, SM11, SM12, SM13, SM15, SM16, SM17 and SM18. SM13 (optional) provides additional coverage for UVLO since UVLO condition would also lead to NACK on the I2C (SM12). 

**Note 3:** For implementation specific details related to Safety Mechanisms as indicated above, please refer to the Safety Mechanism Implementation Guide 32-100395 A. 

**==> picture [93 x 101] intentionally omitted <==**

## **9.4. Assumptions of Use** 

The following product specific assumptions are applicable: 

AoU1: For achievement of ASIL D compliance, the ADC readback functionality needs to be activated to evaluate OUT1/2/3/4 current and voltages per I2C. The current/voltage readings shall be performed at least once per FTTI as indicated in section 9.3. The ADC readback is applicable for Safety Mechanisms SM8, SM9, SM10, SM11, SM13, SM17 and SM18. 

AoU2: For verification of data integrity related to the I2C bus is within the integrator’s responsibility to implement system level measures related to readback after write and redundant read-back (SM14) for any safety related transaction on the bus. 

AoU3: If the INT pin is used to communicate the fault status, an external monitoring of the INT pin at start up is required to verify for potential stuck at communication (refer to SM15). 

AoU4: For SM18 (Verification of Reverse Blocking FET) it is assumed that VIN is sufficiently lower than VBAT (battery voltage). 

**==> picture [76 x 76] intentionally omitted <==**

**TITLE:** Safety Manual for MAX20087/MAX20089 (AP73) 

**==> picture [82 x 23] intentionally omitted <==**

**DOCUMENT I.D.** 32-100049 

**REVISION PAGE** F 16 

## **9.5. Fault Indication and Communication** 

**==> picture [105 x 109] intentionally omitted <==**

As part of the Technical Safety Concept it is described how the status on faults is indicated and communicated to the host via the appropriate interface. This fault indication is provided for any Safety Measure individually and listed in the table below. 

|||||||
|---|---|---|---|---|---|
|**Safety**<br>**Measure**|**Description**|**Fault to be**<br>**detected**|**Configuration**<br>**Requirements**|**Fault Indication**|**Fault Communication**<br>**(I2C Interface)**|
|**SM1**|Over-current<br>detection on<br>Channels 1/2/3/4|Over-current<br>output channels|NA|I2C Register Set, /INT\ Pin Asserted|Read STAT2:OC[4:1]|
|**SM2**|Over-voltage<br>detection on<br>Channels 1/2/3/4|Over-voltage on<br>output channels|NA|I2C Register Set, /INT\ Pin Asserted|Read STAT2:OV[4:1]|
|**SM3**|Under-voltage<br>detection on<br>Channels 1/2/3/4|Under-voltage<br>on output<br>channels|NA|I2C Register Set, /INT\ Pin Asserted|Read STAT2:UV[4:1]|
|**SM4**|OV comparator<br>diagnostics|Stuck at<br>High/Low|NA|I2C Register Set|Read STAT1:OVIN and<br>STAT2:OV[4:1]|
|**SM5**|UV comparator<br>diagnostics|Stuck at<br>High/Low|NA|I2C Register Set|Read STAT2:UV[4:1]|
|**SM6**|Input Voltage<br>Monitor|Under-Voltage<br>on Input<br>Channel|NA|I2C Register Set, /INT\ Pin Asserted|Read STAT1:UVIN|
|**SM7**|ECC on OTP|Single Bit Fault|NA|Fault automatically corrected|N/A|
|**SM8**<br>(Note 2)|ADC Diagnostics<br>(requires host<br>uC)|Stuck, offset<br>and gain errors|NA|I2C Register Set (requires<br>diagnostic subroutine at host uC1)|NA|
|**SM9**<br>(Note 2)|Current readings<br>through ADC<br>(requires host<br>uC)|Output channel<br>open detection<br>(zero current)|Set CONFIG.MUX[1:0] =<br>2b00|I2C Register Set (requires<br>diagnostic subroutine at host uC1)|Read ADC1-4|
|**SM10**<br>(Note 2)|Voltage readings<br>through ADC<br>(requires host<br>uC)|OV and UV on<br>output channels,<br>input channels|Set CONFIG.MUX[1:0]<br>=2b01<br>Set CONFIG.MUX[1:0]<br>=2b10|I2C Register Set (requires<br>diagnostic subroutine at host uC1)|Read ADC1-4.<br>Change MUX setting read<br>ADC1.|
|**SM11**<br>(Note 2)|Iset comparator<br>diagnostics<br>(requires host<br>uC)|Verify<br>comparator for<br>current limit<br>setting|(optional) Set<br>CONFIG.MUX[1:0] = 2b10|I2C Register Set (requires<br>diagnostic subroutine at host uC1)|Read STAT1.ISET<br>Read ADC3 (optional)|



**TITLE:** Safety Manual for MAX20087/MAX20089 (AP73) 

**==> picture [82 x 23] intentionally omitted <==**

**DOCUMENT I.D. REVISION PAGE** 32-100049 F 17 

|**SM12**<br>(Note 2)|ACK on I2C|I2C<br>communication<br>error|NA|I2C Register Set, ACK/NACK bit<br>during communication|Any I2C Register|
|---|---|---|---|---|---|
|**SM13**<br>(Note 2)|Verification of<br>UVLO<br>comparator|Verify<br>comparator for<br>UVLO detection|NA|ADC reading mismatch between<br>ULO comparator indication and<br>correspondingexpected value|Read STAT1.UVDD|
|**SM14**|Verification of<br>thermal limit on<br>output channels|Thermal limit of<br>output channels|NA|Output of channel with thermal limit<br>is shut down|Read STAT2:TS[4:1]|
|**SM15**<br>(Note 2)|Monitoring of INT<br>Pin|Errors mapped<br>to INT Pin<br>through I2C|NA|INT Pin Asserted|Verify INT pin changes<br>state at EN high.|
|**SM16**<br>(Note 2)|I2C Diagnostics|I2C read/write<br>fault|NA|Write fault indicated by mismatch in<br>the readback, Read fault indicated<br>by mismatch between redundant<br>readback|Any I2C Write/Readback|
|**SM17**<br>(Note 2)|OCP FET<br>Switching<br>Diagnostics|Over-current<br>output channels|EN[4:1]=0<br>Set CONFIG.MUX[1:0] =<br>2b00|ADC indicates load current during<br>power up|Read ADC1-4|
|**SM18**<br>(Note 2)|Reverse Blocking<br>FET switch<br>diagnostics|Reverse<br>blocking FET<br>stuck closed|Set CONFIG.MUX[1:0] =<br>2b10|ADC reading of VIN|Read ADC1|
|_Table 6: Fault Indication and Communication_||||||



**Note 1** : For SM1 – SM6, the I2C register setting is a fault flag, and is trivial for a host uC to use as a diagnostic flag. SM8-SM11 are measurements reported to the host, and require additional computation / logic beyond simply checking a fault flag. 

**Note 2:** Needed to support ASIL D. 

**Note 3:** For implementation specific details related to Safety Mechanisms as indicated above, please refer to the Safety Mechanism Implementation Guide 32-100395 A. 

## **10. Verification of ASIL level** 

## **10.1. FTA of MAX20087** 

The FTA (Fault Tree Analysis) for MAX20087 has been performed starting from the failure “Unprotected Power on Channel 1/2/3/4” and continuing down through to the component level. 

**==> picture [140 x 140] intentionally omitted <==**

**TITLE:** Safety Manual for MAX20087/MAX20089 (AP73) 

**==> picture [82 x 23] intentionally omitted <==**

**DOCUMENT I.D.** 32-100049 

**REVISION PAGE** F 18 

**==> picture [499 x 375] intentionally omitted <==**

_Figure 6: Chart of Fault Tree Analysis for MAX20087_ 

## **10.2. FMEDA of MAX20087** 

The FMEDA for MAX20087 has been performed considering all relevant functional blocks and is described in the FMEDA document. 

For all used components within the element MAX20087 attributed for the various functions, the individual malfunctions are defined 

- The Root Causes of those malfunctions are identical to the FMEDA Failure Modes 

- A failure split is defined with respect to the Root Causes for a malfunction taking into account different probabilities 

- The corresponding diagnostic functions (safety measures) are defined to detect a specific Root Cause/FMEDA Failure Mode 

- The Failure Rates (FIT Rates) are defined for the individual components / Functional Blocks of the element MAX20087 

- Furthermore, the diagnostic coverage is defined for any safety relevant Failure Mode 

- Single point as well as latent failures has been considered. 

**TITLE:** Safety Manual for MAX20087/MAX20089 (AP73) 

**==> picture [82 x 23] intentionally omitted <==**

**DOCUMENT I.D.** 32-100049 

**REVISION PAGE** F 19 

In this Safety Manual FMEDA examples for Element Function 1 (“Provide power to cameras”) with selected Functional Block 1 (“Isense_amplifier”) are provided: The complete FMEDA includes all Functional Blocks according to the Technical Safety Concept. 

## **10.2.1. FMEDA Example for Function EF 2.1, Block FB1** 

To present the FMEDA for one Block, the following Table is used, which is part of the more detailed FMEDA table, which includes also Latent Fault section and Metrics per System Function. 

**==> picture [560 x 217] intentionally omitted <==**

**----- Start of picture text -----**<br>
SRC  Output Stuck Low  Current limit not detected  1  1.405379115<br>1.405379115  0  0.702689558  50<br>Output Stuck High  Channel always turned off  0<br>1.405379115  100  0  0.702689558  50  x  SM3<br>(NSR)  Effect<br>SRC = True<br>Failure Modes  SRC - Block FIT<br>(Boolean Internal)<br>Calculation (Internal)<br>Failure rate Distribution (%)<br>NSR FIT in SRC Element (Internal)  SRC FIT in SRC Elements (Internal)<br>Relevant Block Failure Rate for FIT Rate<br>Safety Related Hardware Component (SRC) or   Non Safety Related Hardware Component  Failure mode that has a potential to violate the  safety goal in absence of Safety Mechanisms  Safety mechanism(s) allowing to prevent the  failure mode from violating the safety goal<br>**----- End of picture text -----**<br>


_Table 7: FMEDA for Function 1 and Block FB1 (Single Point Section)_ 

The full FMEDA for MAX20087 can be found in a separate Maxim-controlled document (32-0091). 

## **10.3. Verification results of Safety Measures** 

Based on the Hardware Design Specification, Technical Safety Concept and Validation Plan, the functionality of the Product MAX20087 has been evaluated with special consideration of Safety Measures. The results of the verification of Safety Measures 1 and 2 for MAX20087 are shown in the table below. 

**==> picture [554 x 142] intentionally omitted <==**

**----- Start of picture text -----**<br>
Safety  Test<br>Safety  Test Case  Board  Sample  Sample<br>Measure  Case  Test Case Description  Test Method  Comment<br>Measure  Type  Requirements  Sizes  Type<br>Name  Number<br>A resistive load is applied to<br>Overcurrent  each output channel such<br>detection  that the current drawn by  Fault<br>Standard EV  ATE  HW<br>SM1  on output  TC1  the load exceeds the  Injection  1  Pass<br>kit  pass  Measurement<br>channels  overcurrent limit. Check for  Hardware<br>OUT1/2/3/4  current limiting and OC flag<br>assertion<br>**----- End of picture text -----**<br>


**TITLE:** Safety Manual for MAX20087/MAX20089 (AP73) 

**==> picture [82 x 23] intentionally omitted <==**

**DOCUMENT I.D.** 32-100049 

**REVISION PAGE** F 20 

**==> picture [539 x 78] intentionally omitted <==**

**----- Start of picture text -----**<br>
An external supply is used<br>Overvoltage  on each of the output<br>detection  channels to raise the  Fault<br>Standard EV  ATE  HW<br>SM2  on output  TC2  voltage above that of the  Injection  1  Pass<br>kit  pass  Measurement<br>channels  input voltage. Check for the  Hardware<br>OUT1/2/3/4  channel shutting off and<br>output OV flag assertion<br>**----- End of picture text -----**<br>


_Table 8: Verification results of Safety Measures for MAX20087_ 

All safety measures have been fully tested and validated. The full test report and results are given in a separate controlled document (32-100048). 

## **10.4. FMEDA Summary** 

**==> picture [46 x 47] intentionally omitted <==**

As a result, from the FMEDA an ASIL summary is created and contains the following information: 

- Summary of the random HW-Metrics for the IC 

- Summary of the random HW-Metrics for the combined function of both the IC and a host uC 

**==> picture [32 x 31] intentionally omitted <==**

- Summary of the random HW-Metrics for every System Function. 

|**SPFM**|**LFM**|**ASIL**|**FIT – Whole**<br>**IC**|**Residual FIT**<br>**Single Point**|**Residual FIT**<br>**Latent**|**PMHF**|
|---|---|---|---|---|---|---|
|99.09%|72.49%|B|14.5087|0.1320|3.9551|0.1325|
||||||||



_Table 9: ASIL Summary for the whole IC (not including separate host uC) based on Safety Mechanisms needed for ASIL B compliance (refer to Section 9.3)_ 

||||||||
|---|---|---|---|---|---|---|
|**SPFM**|**LFM**|**ASIL**|**FIT – Whole**<br>**IC**|**Residual FIT**<br>**Single Point**|**Residual FIT**<br>**Latent**|**PMHF**|
|99.75%|97.28%|D|14.5087|0.0358|0.3943|0.0358|



_Table 10: ASIL Summary for the combination of the IC and a host uC based on Safety Mechanisms needed for ASIL D compliance (refer to Section 9.3)_ 

|_to Section 9.3)_||||
|---|---|---|---|
|||||
|**System**<br>**Function**|||**Residual FIT Single Point**|
||**System Function Description**|**SPFM**||
|SF1|Detect over-current on<br>OUT1/2/3/4|98.20%|0.0903|
|SF2|Short to Battery<br>Detection/Detect overvoltage<br>on OUT1/2/3/4|97.90%|0.0814|
|SF3|Short to Gnd Detection/Detect<br>undervoltage on OUT1/2/3/4|96.87%|0.0739|
|SF4|Detect over/under voltage on IN<br>(Input Supply)|97.04%|0.0747|



_Table 11: ASIL Metrics per System Functions  based on Safety Mechanisms needed for ASIL B compliance (refer to Section 9.3)_ 

**TITLE:** Safety Manual for MAX20087/MAX20089 (AP73) 

**==> picture [82 x 23] intentionally omitted <==**

**DOCUMENT I.D. REVISION PAGE** 32-100049 F 21 

|**System**<br>**Function**|||**Residual FIT Single Point**|
|---|---|---|---|
||**System Function Description**|**SPFM**||
|SF1|Detect over-current on<br>OUT1/2/3/4|99.83|0.0069|
|SF2|Short to Battery<br>Detection/Detect overvoltage<br>on OUT1/2/3/4|99.77|0.007|
|SF3|Short to Gnd Detection/Detect<br>undervoltage on OUT1/2/3/4|99.69|0.0098|
|SF4|Detect over/under voltage on IN<br>(Input Supply)|99-79|0.0071|



_Table 12: ASIL Metrics per System Functions  based on Safety Mechanisms needed for ASIL  D compliance (refer to Section 9.3)_ 

**Note 1:** Base failure rates have been determined from empirical data with a confidence level of 60´%. **Note 2:** The full FMEDA contents is included in a separate document ( Doc-ID 32-0091) and may be reviewed on request. 

**==> picture [290 x 296] intentionally omitted <==**

## **Appendix** 

## **Rating Tables for Severity, Controllability and Exposure** 

|**Class**|**S0**|**S1**|**S2**|**S3**|
|---|---|---|---|---|
|**Description**|No injuries|Light and moderate<br>Injuries|Severe and life-<br>threatening injuries<br>(survival probable)|Life-threatening injuries<br>(survival uncertain), fatal<br>injuries|



_Table 2: Classes of Severity_ 

|**Class**|**C0**|**C1 **||**C2 **||**C3**|
|---|---|---|---|---|---|---|
|||||||**PAGE**<br>22|
|**TITLE:**Safety Manual for MAX20087/MAX20089 (AP73)|||||||
|**DOCUMENT I.D.**<br>32-100049||||**REVISION**<br>F||**PAGE**<br>22|



**==> picture [82 x 23] intentionally omitted <==**

**Description**[Controllable in ] Simply controllable Normally controllable[Difficult to control ] general or uncontrollable 

_Table 3: Classes of Controllability_ 

|**Class**|**E0**|**E1**|**E2**|**E3**|**E4**|
|---|---|---|---|---|---|
|**Description**|Incredible|Very low probability|Low probability|Medium probability|High probability|



_Table 4: Classes of probability of exposure regarding operational situations_ 

## **ASIL Classification Table** 

|**Severity**<br>**class**|**Probabillity**<br>**class**|**C1**|**C2**<br>**C3**|**C2**<br>**C3**|
|---|---|---|---|---|
|**S1**|**E1**|QM|QM|QM|
||**E2**|QM|QM|QM|
||**E3**|QM|QM|A|
||**E4**|QM|A|B|
||**E1**|QM|QM|QM|
|**S2**|**E2**|QM|QM|A|
||**E3**|QM|A|B|
||**E4**|A|B|C|
||**E1**|QM|QM|A|
|**S3**|**E2**|QM|A|B|
||**E3**|A|B|C|
||**E4**|B|C|D|
|_Table 5: ASIL_|_determination_||||



_Table 5: ASIL determination_ 

_ASIL A - lowest safety integrity level ASIL D - highest safety integrity level. QM (quality management) - no requirement to comply with ISO 26262_ 

## **Terms and Definitions** 

## **ASIL (Automotive Safety Integrity Level)** 

One of four levels to specify the item's or element's necessary requirements of ISO 26262 and safety measures to apply for avoiding an unreasonable residual risk with D representing the most stringent and A the least stringent level. 

## **Component** 

Non-system level element that is logically and technically separable and is comprised of more than one hardware part or of one or more software units. 

## **Controllability (C)** 

Ability to avoid a specified harm or damage through the timely reactions of the persons involved, possibly with support from external measures. 

**TITLE:** Safety Manual for MAX20087/MAX20089 (AP73) 

**==> picture [82 x 23] intentionally omitted <==**

**DOCUMENT I.D. REVISION PAGE** 32-100049 F 23 

Note: Persons involved can include the driver, passengers or persons in the vicinity of the vehicle's exterior. 

## **Diagnostic coverage** 

Proportion of the hardware element failure rate that is detected or controlled by the implemented safety mechanisms. 

Note: Diagnostic coverage can be assessed with regard to residual faults or with regard to latent multiplepoint faults that might occur in a hardware element. 

## **Element** 

System or part of a system including components, hardware, software, hardware parts, and software units. 

## **Exposure (E)** 

State of being in an operational situation that can be hazardous if coincident with the failure mode under analysis. 

## **Failure rate** 

Probability density of failure divided by probability of survival for a hardware element. Note: The failure rate is assumed to be constant. 

## **FMEDA Failure Modes Effects and Diagnostic Analysis** 

Procedure for the detailed determination of error causes and their impact on the system and is used in the early stages of systems development for the purpose of early identification of weaknesses. The requirements of safety standards are the avoidance of errors within a safety-relevant system and to reduce them to a reliable residual error probability or a residual error rate. 

## **Fault reaction time and fault tolerant time interval** 

**==> picture [306 x 149] intentionally omitted <==**

## **Harm** 

Physical injury or damage to the health of persons. 

## **Hazard** 

Potential source of harm caused by malfunctioning behavior of the item. 

## **Hazard analysis and risk assessment** 

Method to identify and categorize hazardous events of items and to specify safety goals and ASILs related to the prevention or mitigation of the associated hazards in order to avoid unreasonable risk. 

**TITLE:** Safety Manual for MAX20087/MAX20089 (AP73) 

**==> picture [82 x 23] intentionally omitted <==**

**DOCUMENT I.D. REVISION PAGE** 32-100049 F 24 

## **Hazardous event** 

Combination of a hazard and an operational situation. 

## **Item** 

System or array of systems to implement a function at the vehicle level, to which ISO 26262 is applied. 

**==> picture [92 x 95] intentionally omitted <==**

## **Latent fault** 

Multiple-point fault whose presence is not detected by a safety mechanism nor perceived by the driver within the multiple-point fault detection interval. 

## **Operational situation** 

Scenario that can occur during a vehicle's life. For example:  driving, parking, maintenance. 

## **Residual fault** 

Portion of a fault that by itself leads to the violation of a safety goal, occurring in a hardware element, where that portion of the fault is not covered by safety mechanisms. 

Note: This presumes that the hardware element has safety mechanism coverage for only a portion of its faults. 

Example: If low (60 %) coverage is claimed for a failure mode, the other 40 % of that same failure mode is the residual fault. 

## **Residual Risk** 

Risk remaining after the deployment of safety measures. 

## **Risk** 

Combination of the probability of occurrence of harm(1.56) and the severity(1.120) of that harm. 

## **Safety goal** 

Top-level safety requirement as a result of the hazard analysis and risk assessment. 

Note: One safety goal can be related to several hazards, and several safety goals can be related to a single hazard. 

**==> picture [33 x 33] intentionally omitted <==**

## **Safety measures** 

Activity or technical solution to avoid or control systematic failure and to detect random hardware failures or control random hardware failures, or mitigate their harmful effects 

Note 1: Examples of safety measures are FMEA (Failure Mode and Effects Analysis) and software without the use of global variables. 

Note 2: Safety measures include safety mechanisms. 

## **Safety mechanism** 

Technical solution implemented by E/E functions or elements, or by other technologies, to detect faults or control failures in order to achieve or maintain a safe state. 

Note 1 Safety mechanisms are implemented within the item to prevent faults from leading to single-point failures or to reduce residual failures and to prevent faults from being latent. Note 2 The safety mechanism is either 

**TITLE:** Safety Manual for MAX20087/MAX20089 (AP73) 

**==> picture [82 x 23] intentionally omitted <==**

**DOCUMENT I.D. REVISION PAGE** 32-100049 F 25 

- a) able to transition to, or maintain, the item in a safe state, or 

b) able to alert the driver such that the driver is expected to control the effect of the failure, as defined in the functional safety concept. 

## **Severity (S)** 

Estimate of the extent of harm to one or more individuals that can occur in a potentially hazardous situation. 

## **Single-point fault** 

Fault in an element that is not covered by a safety mechanism and that leads directly to the violation of a safety goal. 

## **System** 

**==> picture [79 x 85] intentionally omitted <==**

Set of elements that relate at least a sensor, a controller and an actuator with one another. _[Summary for all ISO-related terms and definitions to be added here.]_ 

**==> picture [402 x 396] intentionally omitted <==**

**TITLE:** Safety Manual for MAX20087/MAX20089 (AP73) 

**==> picture [82 x 23] intentionally omitted <==**

**DOCUMENT I.D.** 32-100049 

**REVISION PAGE** F 26 

## **REVISION HISTORY** 

**==> picture [549 x 636] intentionally omitted <==**

**----- Start of picture text -----**<br>
REV  CHANGES MADE  DATE  INIT.<br>A  CN# 1021693.  INITIAL RELEASE.  10/24/17  RS<br>B  CN 1060507.  Functional Safety Disclaimer added.  6/19/19  JW<br>C  CN 1069548. Section 9.3 on “Safety Measures for MAX20087” updated to include safety measures  10/22/19  VC<br>SM12-SM18. Section 9.4 on “Fault Indication and Communication” updated to include safety measures<br>SM12-SM18.<br>D  CN 1100978. Added information on diagnostic time for additional safety mechanisms.  9/29/20  VC<br>E  CN 1156865. Added Assumptions of Use (section 9.4). Updated DTI time involving ADC read to 1.1ms  3/29/2022  VC<br>(section 9.3).<br>F  CN 1164712. Added references to MAX20087B (section 1). Added WETQFN package type (section 3.1)  6/10/2022  JB<br>**----- End of picture text -----**<br>


**TITLE:** Safety Manual for MAX20087/MAX20089 (AP73) 

**==> picture [82 x 23] intentionally omitted <==**

**DOCUMENT I.D.** 32-100049 

**REVISION PAGE** F 27 

