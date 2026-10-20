# DS5396_CoaxFIUModule_ComponentManual

Source: C:\Users\JHARVEY\OneDrive - Volvo Cars\Documents\01_Resources\04_DatasheetsAndSpecification\FIU Module DS5396\DS5396_CoaxFIUModule_ComponentManual.pdf

DS5396 Coax FIU Module 

## Component Manual 

December 2024 

## How to Contact dSPACE 

Mail: dSPACE GmbH Rathenaustraße 26 33102 Paderborn Germany Tel.: +49 5251 1638-0 E-mail: info@dspace.de Web: https://www.dspace.com 

## How to Contact dSPACE Support 

If you encounter a problem when using dSPACE products, contact your local dSPACE representative: 

- § Local dSPACE companies and distributors: https://www.dspace.com/go/locations 

- § For countries not listed, contact dSPACE GmbH in Paderborn, Germany. Tel.: +49 5251 1638-941 or e-mail: support@dspace.de 

You can also use the support request form: https://www.dspace.com/go/supportrequest. If you are logged on to mydSPACE, you are automatically identified and do not have to add your contact details manually. 

If possible, always provide the serial number of the hardware, the relevant dSPACE License ID, or the serial number of the CmContainer in your support request. 

## Software Updates and Patches 

dSPACE strongly recommends that you download and install the most recent patches for your current dSPACE installation. Visit https://www.dspace.com/go/patches for the software updates and patches themselves and for more information, such as how to receive an automatic notification when an update or a patch is available for your dSPACE software. 

## Important Notice 

This publication contains proprietary information that is protected by copyright. All rights are reserved. The publication may be printed for personal or internal use provided all the proprietary markings are retained on all printed copies. In all other cases, the publication must not be copied, photocopied, reproduced, translated, or reduced to any electronic medium or machine-readable form, in whole or in part, without the prior written consent of dSPACE GmbH. 

© 2024 by: dSPACE GmbH Rathenaustraße 26 33102 Paderborn Germany 

This publication and the contents hereof are subject to change without notice. 

AURELION, AUTERA, ConfigurationDesk, ControlDesk, MicroAutoBox, MicroLabBox, SCALEXIO, SIMPHERA, SYNECT, SystemDesk, TargetLink, and VEOS are registered trademarks of dSPACE GmbH in the United States or other countries, or both. Other brand names or product names are trademarks or registered trademarks of their respective companies or organizations. 

Contents 

## Contents 

|About This Document<br>5|
|---|
|User Qualification and Intended Use<br>7|
|User Qualification and Intended Use................................................................ 7|
|Safety Precautions<br>9|
|Safety Precautions for Installing and Connecting the Hardware........................ 9|
|Safety Precautions for Disposing of dSPACE Hardware................................... 10|
|Introduction to DS5396 Coax FIU Module<br>11|
|Basics on the DS5396 Coax FIU Module........................................................ 11|
|Configuring the DS5396 Coax FIU Module<br>13|
|Configuring the Module Address for Tool CAN Control................................. 13|
|Configuring the Baud Rate for Tool CAN Control........................................... 14|
|Installing and Connecting the DS5396 Coax FIU Module<br>15|
|Installing the DS5396 Coax FIU Module......................................................... 15|
|Connecting the DS5396 Coax FIU Module.................................................... 16|
|Using the DS5396 Coax FIU Module<br>19|
|Powering Up the DS5396 Coax FIU Module.................................................. 19|
|Controlling the DS5396 Coax FIU Module..................................................... 20|
|Maintenance<br>21|
|Updating a DS5396 Coax FIU Module........................................................... 21|
|Data Sheets<br>23|
|Controls and Connectors............................................................................... 23|
|LED and Error State Descriptions.................................................................... 25|
|Connector Pinouts and Interface Descriptions................................................ 26|



3 DS5396 Coax FIU Module - Component Manual 

December 2024 

Contents 

Schematic..................................................................................................... 28 Technical Data............................................................................................... 30 

4 DS5396 Coax FIU Module - Component Manual 

December 2024 

About This Document 

## About This Document 

## Content 

This document introduces you to configuring, installing, and using the DS5396 Coax FIU Module. 

Additionally, it provides reference information such as: 

- § Connector pin assignments 

- § Schematics 

- § LED and operating states 

- § Error states 

- § Electrical and physical data 

## Required knowledge 

To use a DS5396 Coax FIU Module, you must be familiar with the following: 

- § SCALEXIO hardware, especially processing hardware configuration via ConfigurationDesk 

Symbols 

dSPACE user documentation uses the following symbols: 

|Symbol|Description|
|---|---|
|**DANGER**<br>`�`|Indicates a hazardous situation that, if not avoided,<br>will result in death or serious injury.|
|**WARNING**<br>`�`|Indicates a hazardous situation that, if not avoided,<br>could result in death or serious injury.|
|**CAUTION**<br>`�`|Indicates a hazardous situation that, if not avoided,<br>could result in minor or moderate injury.|
|**_NOTICE_**|Indicates a hazard that, if not avoided, could result in<br>property damage.|
|**Note**|Indicates important information that you should take<br>into account to avoid malfunctions.|
|**Tip**|Indicates tips that can make your work easier.|
||Indicates a link that refers to a definition in the<br>glossary, which you can find at the end of the<br>document unless stated otherwise.|



5 DS5396 Coax FIU Module - Component Manual 

December 2024 

About This Document 

Naming conventions 

Symbol Description Follows the document title in a link that refers to another document. dSPACE user documentation uses the following naming conventions: %name% Names enclosed in percent signs refer to environment variables for file and path names. < > Angle brackets contain wildcard characters or placeholders for variable file and path names, etc. 

6 DS5396 Coax FIU Module - Component Manual 

December 2024 

User Qualification and Intended Use 

## User Qualification and Intended Use 

## User Qualification and Intended Use 

User qualification Only qualified persons with experience in installing computer hardware and electric devices are allowed to install or uninstall hardware. Connecting the device, especially to the power supply, must be carried out only by a skilled electrician or by instructed persons under the supervision and guidance of a skilled electrician, and in accordance with electrical engineering rules and regulations. A skilled electrician is a person with sufficient technical training, comprehension, experience, and knowledge of the relevant regulations to assess the tasks assigned to them and to recognize possible dangers. 

Intended use of DS5396 Coax The intended use of the DS5396 Coax FIU Module is to simulate faults on coaxial FIU Module signal lines within a SCALEXIO system. Using a DS5396 Coax FIU Module for purposes other than this is considered to be improper and non-contractual use. You are not allowed to modify the DS5396 Coax FIU Module unless the required instructions are explicitly stated in the user documentation or were sent to you by dSPACE in writing. Perform the instructions only if you have the required skills. 

7 DS5396 Coax FIU Module - Component Manual 

December 2024 

User Qualification and Intended Use 

8 DS5396 Coax FIU Module - Component Manual 

December 2024 

Safety Precautions 

## Safety Precautions 

|Introduction||To avoid risk of injury and/or damage to the dSPACE hardware, read and ensure|To avoid risk of injury and/or damage to the dSPACE hardware, read and ensure|To avoid risk of injury and/or damage to the dSPACE hardware, read and ensure|To avoid risk of injury and/or damage to the dSPACE hardware, read and ensure||
|---|---|---|---|---|---|---|
|||that you comply with the following safety precautions. These precautions must|||||
|||be observed during all phases of system operation.|||||
|dSPACE General Safety||In|addition to the safety precautions given in this document, it is recommended||||
|Precautions||to|read the dSPACE General Safety Precautions. This document describes the||||
|||risks of injury and damage to the dSPACE hardware in general.|||||
|||A|printed document of the dSPACE General Safety Precautions is delivered||||
|||together with your hardware.|||||
|Where to go from here||Information in this section|||||
||||||||
||||||||
||||Safety Precautions for Installing and Connecting the Hardware..................9||||
||||Safety Precautions for Disposing of dSPACE Hardware.............................10||||
||||||||
||||||||



## Safety Precautions for Installing and Connecting the Hardware 

|Connecting to power supply|An overload of the DS5396 Coax FIU Module might cause a fire with the risks of|
|---|---|
||material damage and personal injury.|
||§ Do not supply the DS5396 Coax FIU Module with a voltage level above the|
||maximum ratings. Refer toTechnical Dataon page 30.|
|Using the module in wet|The DS5396 Coax FIU Module is not moisture-proof and is not intended for use|
|locations|in wet locations according to IEC 61010-1 (product safety).|
||§ Use the DS5396 Coax FIU Module only in dry locations and avoid|
||condensation.|



9 DS5396 Coax FIU Module - Component Manual 

December 2024 

Safety Precautions 

Installing or uninstalling hardware 

You install and uninstall dSPACE hardware at your own risk. Any damage to or malfunction of dSPACE hardware caused by improper installation or uninstallation is not covered by the warranty, unless the handling and installation instructions are shown to be defective. 

Before installing or uninstalling, make sure that: 

- § The power supply is switched off and the power supply cable is disconnected. 

- § No external devices are connected to the dSPACE system. 

In case of a fault, connected external devices might feed dangerously high voltage to the dSPACE system or parts of the circuitry. 

Connecting and disconnecting devices 

To prevent damage to the hardware: 

- § Do not apply voltages or currents outside the specified ranges to the connector pins. Refer to Technical Data on page 30. 

- § Do not connect or disconnect any signals to the DS5396 module while the dSPACE system is powered up and/or external devices are switched on. Make sure that external devices are turned off beforehand. 

- § Make sure that only intended faults/voltages are inserted when FIU rail voltages and currents are connected to the coaxial signal lines. 

- § Make sure that all the connected devices and cables can withstand the inserted FIU rail voltages and currents. 

- § If more than one DS5396 module is connected to an ECU with internally connected input connector shieldings, short circuits might be created by inserting different faults on the shieldings at the same time. 

## Safety Precautions for Disposing of dSPACE Hardware 

Disposing of a DS5396 Coax FIU Module 

You must ensure that dSPACE hardware is disposed of in accordance with the applicable regional rules and regulations. You are strongly recommended to contact the regional waste management authorities to find a disposal or recycling center for the proper and environmentally sound disposal of dSPACE hardware (e-waste). Recycle or reuse dSPACE hardware whenever possible. 

10 DS5396 Coax FIU Module - Component Manual 

December 2024 

Introduction to DS5396 Coax FIU Module 

## Introduction to DS5396 Coax FIU Module 

## Basics on the DS5396 Coax FIU Module 

Overview 

The DS5396 module provides fault insertion functions on up to four coaxial signal lines. 

**==> picture [256 x 126] intentionally omitted <==**

**==> picture [256 x 127] intentionally omitted <==**

**==> picture [256 x 126] intentionally omitted <==**

11 DS5396 Coax FIU Module - Component Manual 

December 2024 

Introduction to DS5396 Coax FIU Module 

The module can insert the following faults: 

- § Line break 

- § Shielding break 

- § Short to Vbat 

- § Short to GND 

- § Short to COM or to other line 

The module is controlled by CAN using the dSPACE Tool CAN protocol. The module is usually part of a SCALEXIO system and attached on a DIN rail (NS35). 

12 DS5396 Coax FIU Module - Component Manual 

December 2024 

Configuring the DS5396 Coax FIU Module 

## Configuring the DS5396 Coax FIU Module 

Introduction 

For controlling the DS5396 Coax FIU Module via the dSPACE Tool CAN protocol, you have to set the module address and the CAN baud rate properly. 

Where to go from here 

Information in this section Configuring the Module Address for Tool CAN Control...........................13 Configuring the Baud Rate for Tool CAN Control.....................................14 

## Configuring the Module Address for Tool CAN Control 

Overview 

The address of a DS5396 Coax FIU Module is set by the three hexadecimal rotary switches at the front of the module. 

**==> picture [74 x 85] intentionally omitted <==**

**==> picture [74 x 85] intentionally omitted <==**

**==> picture [75 x 85] intentionally omitted <==**

**==> picture [38 x 85] intentionally omitted <==**

You have to set the address for each DS5396 Coax FIU Module in the system. 

## Note 

Using 0 (zero) for any of the three digits (= switches) of the address causes conflicts with broadcast addresses of the Tool CAN protocol. § Do not set any of the address switches to 0 (zero). 

13 DS5396 Coax FIU Module - Component Manual 

December 2024 

Configuring the DS5396 Coax FIU Module 

The selected address is also used by the custom I/O function block in ConfigurationDesk, which is designated to control this particular DS5396 Coax FIU Module. 

## Configuring the Baud Rate for Tool CAN Control 

Overview 

The CAN baud rate is set by the DIP switch at the front of the module. 

**==> picture [66 x 75] intentionally omitted <==**

**==> picture [66 x 75] intentionally omitted <==**

**==> picture [66 x 75] intentionally omitted <==**

**==> picture [33 x 75] intentionally omitted <==**

Changing the baud rate 

By default, the Tool CAN control baud rate is set to 125 kBd. If you have to change it, set switch 1 and 2 according to the following table: 

|Tool CAN Baud Rate|Switch 1|Switch 2|
|---|---|---|
|125 kBd (default)|0|0|
|250 kBd|0|1|
|500 kBd|1|0|
|1 MBd|1|1|



14 DS5396 Coax FIU Module - Component Manual 

December 2024 

Installing and Connecting the DS5396 Coax FIU Module 

## Installing and Connecting the DS5396 Coax FIU Module 

Where to go from here 

## Information in this section 

Installing the DS5396 Coax FIU Module...................................................15 Connecting the DS5396 Coax FIU Module...............................................16 

## Installing the DS5396 Coax FIU Module 

Overview 

DS5396 Coax FIU Modules are designed to be attached to DIN rails (NS35). Additionally, TBUS connectors can be attached between the DIN rail and the modules to interconnect neighbored Tool CAN modules. The following illustrations show the principle (from left to right): 

**==> picture [97 x 97] intentionally omitted <==**

**==> picture [97 x 97] intentionally omitted <==**

**==> picture [97 x 97] intentionally omitted <==**

15 DS5396 Coax FIU Module - Component Manual 

December 2024 

Installing and Connecting the DS5396 Coax FIU Module 

## Note 

The following rules apply for the installation: 

- § Do not connect more than 25 modules to maintain signal integrity and to avoid a current overload. 

- § The maximum number of modules depends on the supply voltage and the Tool CAN system in general (e.g., cables, other modules, etc.) and might be higher or slightly lower than 25. 

## Connecting the DS5396 Coax FIU Module 

Overview You have to connect the DS5396 Coax FIU Module to the power supply, Tool CAN control, FIU rail signals, and coaxial signal lines by the following connectors. CTRL/PWR connector The CTRL/PWR connector lets you connect the module to the power supply and the CAN bus for Tool CAN control. The signals of the CTRL/PWR connector are internally looped through to the TBUS connector. Therefore, you need to connect only one module of the TBUS to the power supply and Tool CAN signals via the CTRL/PWR connector. RAIL connector The RAIL connector lets you connect the module to the FIU rail signals. The signals of the RAIL connector are internally looped through to the TBUS connector. Therefore, you need to connect only one module of the TBUS to the FIU rail signals via the RAIL connector. 

16 DS5396 Coax FIU Module - Component Manual 

December 2024 

Connecting the DS5396 Coax FIU Module 

COAX1 … COAX4 IN/OUT connectors 

The SMA coaxial connectors let you connect the module to four signals between the SCALEXIO system and ECUs to insert specific faults. 

## Note 

## Potential short circuits via the shieldings of ECU input connectors 

If more than one DS5396 module is connected to an ECU with internally connected input connector shieldings, short circuits might be created by inserting different faults on the shieldings at the same time, e. g., short to GND and short to Vbat. Refer to the following illustration: 

**==> picture [199 x 199] intentionally omitted <==**

**----- Start of picture text -----**<br>
DS5396 (1) ECU<br>Line<br>Shield<br>Vbat<br>GND<br>COM<br>DS5396 (2)<br>Line<br>Shield<br>Vbat<br>GND<br>COM<br>**----- End of picture text -----**<br>


## TBUS connector 

## Additional information 

The TBUS connector lets you connect the module to neighboring Tool CAN modules. The signals of the TBUS connector are internally looped through to the RAIL connector and the CTRL/PWR connector. 

For more information on the module connectors, refer as follows: 

- § For a general graphical overview, refer to Schematic on page 28. 

- § For connector locations, refer to Controls and Connectors on page 23. 

- § For pin assignments, refer to Connector Pinouts and Interface Descriptions on page 26. 

17 DS5396 Coax FIU Module - Component Manual 

December 2024 

Installing and Connecting the DS5396 Coax FIU Module 

18 DS5396 Coax FIU Module - Component Manual 

December 2024 

Using the DS5396 Coax FIU Module 

## Using the DS5396 Coax FIU Module 

Where to go from here 

## Information in this section 

Powering Up the DS5396 Coax FIU Module.............................................19 Controlling the DS5396 Coax FIU Module...............................................20 

## Powering Up the DS5396 Coax FIU Module 

Introduction 

DS5396 Coax FIU Modules do not provide an On/Off switch. They are powered up just by applying the supply voltage. 

Power-up procedure 

Powering up a DS5396 module is performed as follows: 

1. Applying the supply voltage: The module starts operating as soon as the minimum supply voltage is applied. A hysteresis ensures a stable power-up procedure. 

2. Bootloader phase: The module firmware includes a bootloader. This allows for updating the module via Tool CAN protocol (refer to Updating a DS5396 Coax FIU Module on page 21). The bootloader is active for at least three seconds. 

3. Initialization phase: After the bootloader phase, the initialization starts and all relays are reset. To limit the inrush current, the reset phase is delayed depending on the module's address. This prevents the relays of multiple modules from being reset simultaneously. Powering up might therefore take up to eight seconds. 

The power-up phases are indicated by the LEDs on the front of the module. Refer to LED and Error State Descriptions on page 25. 

19 DS5396 Coax FIU Module - Component Manual 

December 2024 

Using the DS5396 Coax FIU Module 

## Controlling the DS5396 Coax FIU Module 

## Overview 

DS5396 Coax FIU Modules are controlled via dSPACE Tool CAN protocol, for example via ConfigurationDesk using a custom I/O function. 

dSPACE Tool CAN protocol The dSPACE Tool CAN protocol allows for complete control of the module functions, error handling, and using functions such as temperature control. 

ConfigurationDesk custom I/O function The custom I/O function implements the dSPACE Tool CAN protocol and provides FIU functionality. For more information on the custom I/O function, refer to the following document: ApplToolsSolution CCHDS5396CoaxFIUModule.pdf 

## Note 

Potential short circuits via the shieldings of ECU input connectors. For details, refer to COAX1 … COAX4 IN/OUT connectors on page 17. 

Operating state monitoring Two LEDs on the front of the DS5396 module inform about power and operating states. For information about possible LED states and their meaning, refer to LED and Error State Descriptions on page 25. 

20 DS5396 Coax FIU Module - Component Manual 

December 2024 

Maintenance 

## Maintenance 

## Updating a DS5396 Coax FIU Module 

## Overview 

DS5396 Coax FIU Modules can be updated by the dSPACE Tool CAN protocol. A set of specific commands can be used to enter the bootloader, update the firmware in the memory, and reboot the module. 

## Note 

If the update is not completely performed, the module cannot operate normally. It will remain in the bootloader state until a valid firmware is installed. 

For more information on updating the module and to obtain the documentation of the dSPACE Tool CAN protocol, contact dSPACE Support (https://www.dspace.com/go/supportrequest). 

21 DS5396 Coax FIU Module - Component Manual 

December 2024 

Maintenance 

22 DS5396 Coax FIU Module - Component Manual 

December 2024 

Data Sheets 

## Data Sheets 

Where to go from here 

## Information in this section 

Controls and Connectors.........................................................................23 LED and Error State Descriptions..............................................................25 Connector Pinouts and Interface Descriptions..........................................26 Schematic................................................................................................28 Technical Data.........................................................................................30 

## Controls and Connectors 

Introduction 

Gives you detailed information on the controls and connectors of the DS5396 Coax FIU Module. 

23 DS5396 Coax FIU Module - Component Manual 

December 2024 

Data Sheets 

Location of controls and connectors 

**==> picture [101 x 97] intentionally omitted <==**

**==> picture [101 x 97] intentionally omitted <==**

**==> picture [101 x 97] intentionally omitted <==**

**==> picture [101 x 97] intentionally omitted <==**

|Component|Component|Function|
|---|---|---|
|1|ADRESSswitches (HIGH, MID, LOW)|To set the module address for Tool CAN control.1)|
|2|CONFIGswitch|To set the CAN bus baud rate for the module.2)|
|3|STATUSLED|To indicate the operating and error states of the module.3)|
||POWERLED|To indicate the on and off states of the module.3)|
|4|COAX1 IN…COAX4 INconnectors|To connect up to four coaxial signal lines coming from the SCALEXIO<br>HIL.4)|
|5|RAILconnector|To connect FIU rail signals.4)|
|6|TBUSconnector|To provide or receive power supply, Tool CAN control, and FIU rail signals<br>for or from neighboring modules.4)|
|7|CTRL/PWRconnector|To connect Tool CAN control signals.4)|
|8|COAX1 OUT…COAX4 OUT<br>connectors|To connect up to four coaxial signal lines connecting the module to the<br>ECU(s).4)|
||1)<br>Refer toConfiguring the Module Address for Tool CAN Controlon page 13.<br>2)<br>Refer toConfiguring the Baud Rate for Tool CAN Controlon page 14.<br>3)<br>Refer toLED and Error State Descriptionson page 25.<br>4)<br>Refer toConnector Pinouts and Interface Descriptionson page 26.||



24 DS5396 Coax FIU Module - Component Manual 

December 2024 

LED and Error State Descriptions 

## LED and Error State Descriptions 

## Overview 

Two LEDs on the front of DS5396 Coax FIU Modules provide information about power and operating states. 

**==> picture [74 x 85] intentionally omitted <==**

**==> picture [74 x 85] intentionally omitted <==**

**==> picture [75 x 85] intentionally omitted <==**

**==> picture [38 x 85] intentionally omitted <==**

- § STATUS: The red LED indicates the operating and error states of the module. 

- § POWER: The green LED lights up when the supply voltage is sufficiently high. 

## LED states 

The following table lists the possible LED states. 

|POWER<br>LED|STATUS LED|Meaning|
|---|---|---|
|Off|Off|The module is not connected to a power<br>supply or the supply voltage is too low.|
|On|On|§ During power-up: The firmware is<br>initializing.<br>§ After power-up: Lock error1).|
|On|Flashing regularly at<br>1 Hz|Bootloader active (at least for three<br>seconds after powering-up and initializing<br>the bootloader).|
|On|Off|Module operating. No errors and no relay<br>activity.|
|On|Single flash (0.25 s)|Setting relays.|
|On|Flashing (with short<br>off) at 1 Hz|Software error1).|
|On|Flashing regularly at<br>2 Hz|Hardware error1).|



> 1) For more information, refer to Error states on page 25 

Error states 

Depending on specific events, the module enters different error states. The ConfigurationDesk custom I/O function lets you read out the errors via Tool CAN. 

Software error The module is still working. The cause should be checked. Possible causes for software errors: 

- § CAN bus transmitter stopped working due to repeated CAN errors. 

- § Recoverable execution issue. 

- § Temperature margin violation. 

25 DS5396 Coax FIU Module - Component Manual 

December 2024 

Data Sheets 

Hardware error The module is still working. A hardware, firmware, or configuration error occurred that might have led to incorrect behavior or prevents CAN accessibility. 

Possible causes for hardware errors: 

- § Invalid Tool CAN baud rate configuration. 

- § Invalid Tool CAN address configuration. 

- § Critical execution fault. 

Lock error Module stopped operating due to a potentially critical execution error that might cause any type of incorrect behavior. In this state, the module is not accessible via Tool CAN. 

Possible cause for lock errors: 

- § Fatal execution fault. 

## Connector Pinouts and Interface Descriptions 

## Coaxial connectors 

The following illustration shows the SMA coaxial connector's front view and pinout. For the location of the connectors, refer to Controls and Connectors on page 23. 

|page 23.|page 23.|page 23.|page 23.|||
|---|---|---|---|---|---|
|Connector||||Pin|Signal|
|||||1|Data|
|||||Connector housing|Shielding|
|The following table shows the description of the connector pins and signals.||||||
|Pin||Signal|Description/Function|||
|1||Data|The following faults can be inserted by the FIU:<br>§ None<br>§ Line break/open circuit<br>§ Short to FIU rail1), 2)|||
|Connector<br>housing||Shielding|The following faults can be inserted by the FIU:<br>§ None<br>§ Shielding break/open circuit<br>§ Short to FIU rail1), 3)<br>Note<br>Potential short circuits via the shieldings of ECU input<br>connectors. For details, refer toCOAX1 … COAX4<br>IN/OUT connectorson page 17.|||



- 1) FIU rail potential can be floating, Vbat, GND, or COM. 

- 2) Available only on OUT signals and only for line break = true. 

- 3) Available only on OUT signals and only for shielding break = true. 

26 DS5396 Coax FIU Module - Component Manual 

December 2024 

Connector Pinouts and Interface Descriptions 

## CTRL/PWR connector 

The following illustration shows the CTRL/PWR connector. For the location of the connector, refer to Controls and Connectors on page 23. 

|Connector|Pin|Signal|
|---|---|---|
||1|Tool CAN low|
||2|Tool CAN high|
||3, 4|Power GND|
||5|Power Vin|



The following table shows the description of the connector pins and signals. 

|Pin|Signal|Description/Function|
|---|---|---|
|1|Tool CAN<br>low|Tool CAN bus line to control the DS5396 module. Connect these pins<br>to the CAN bus meant for controlling the DS5396 Coax FIU Module.<br>Note<br>The Tool CAN signal is not terminated internally. It must be<br>terminated externally by the user.|
|2|Tool CAN<br>high||
|3, 4|Power<br>GND|Module power supply return. Connect this pin to the negative<br>terminal of the module power supply.|
|5|Power Vin|Module power supply input. Connect this pin to the positive terminal<br>of the module power supply.|



## RAIL connector 

The following illustration shows the RAIL connector. For the location of the connector, refer to Controls and Connectors on page 23. 

|connector, refer toControls and Connectorson|page 23.||
|---|---|---|
|Connector|Pin|Signal|
|RAIL|1, 4|RAIL Vbat|
||2, 5|RAIL GND|
||3|RAIL COM|



The following table shows the description of the connector pins and signals. 

|Pin|Signal|Description/Function|
|---|---|---|
|1, 4|RAIL Vbat|FIU rail connection to the main power supply input. This pin is typically<br>connected to the positive terminal of your vehicle battery or power<br>supply.|



27 DS5396 Coax FIU Module - Component Manual 

December 2024 

Data Sheets 

|Pin|Signal|Description/Function|
|---|---|---|
|2, 5|RAIL GND|FIU rail connection to the main power supply return. This pin is typically<br>connected to the negative terminal of your vehicle battery or vehicle<br>power supply.|
|3|RAIL COM|FIU rail connection to a COM signal. Connect this pin to another<br>potential designated for fault insertion.|



## TBUS connector 

The following illustration shows the TBUS connector. For the location of the connector, refer to Controls and Connectors on page 23. 

## Note 

The marking for pin 1 on the connector insert does not match the documented pinout. 

§ Use the numbering given in the table. 

|Connector|Pin|Signal1)|
|---|---|---|
||1|RAIL COM|
||2|RAIL Vbat|
||3|RAIL GND|
||4|Tool CAN low|
||5|Tool CAN high|
||6, 7|Power GND|
||8|Power Vin|



- 1) For the signal descriptions, refer to CTRL/PWR connector on page 27 and RAIL connector on page 27. 

## Schematic 

Schematic 

The following illustration shows the FIU circuit for the coaxial signal lines of the DS5396 module. 

28 DS5396 Coax FIU Module - Component Manual 

December 2024 

Schematic 

**Rail relays Break relays** 

**==> picture [283 x 447] intentionally omitted <==**

Relays are shown in the reset state of the module. 

29 DS5396 Coax FIU Module - Component Manual 

December 2024 

Data Sheets 

## Technical Data 

## Electrical data 

The following table provides the electrical data of the DS5396 Coax FIU Module. 

|Item|Parameter|Specification|
|---|---|---|
|Power supply<br>Operating voltage range<br>12 … 24 V ±10%<br>Power consumption (typ.)<br>1.1 W<br>Idle operating current @24 V (typ.)<br>13 mA<br>Operating current @24 V (typ.)<br>46 mA<br>Operating current @12 V (typ.)<br>90 mA<br>Max. operating current @24 V, 10 ms<br>138 mA<br>Protected voltage range<br>±30 V|||
||Operating voltage range|12 … 24 V ±10%|
||Power consumption (typ.)|1.1 W|
||Idle operating current @24 V (typ.)|13 mA|
||Operating current @24 V (typ.)|46 mA|
||Operating current @12 V (typ.)|90 mA|
||Max. operating current @24 V, 10 ms|138 mA|
||Protected voltage range|±30 V|
|RAIL inputs and COAX inputs and outputs<br>Maximum voltage<br>±60 V<br>Maximum current<br>1 A|||
||Maximum voltage|±60 V|
||Maximum current|1 A|
|Tool CAN input<br>Maximum voltage<br>±12 V<br>Absolute maximum voltage<br>±58 V|||
||Maximum voltage|±12 V|
||Absolute maximum voltage|±58 V|
|CTRL/PWR and RAIL connectors<br>Wire cross-section range (flexible wire, ferrule with<br>plastic sleeve)<br>0.25 … 0.5 mm²|||
||Wire cross-section range (flexible wire, ferrule with<br>plastic sleeve)|0.25 … 0.5 mm²|
|TBUS connector<br>Maximum current<br>6 A|||
||Maximum current|6 A|



## Note 

Operating current increases while relays are switching. 

- § The connected power supply unit must be able to supply peak currents required during switching, especially if several modules are connected in parallel to one unit. 

30 DS5396 Coax FIU Module - Component Manual 

December 2024 

Technical Data 

## Physical dimensions 

**==> picture [313 x 236] intentionally omitted <==**

**----- Start of picture text -----**<br>
The following illustration shows the dimensions of the module.<br>78 mm 25 mm<br>95 mm<br>88 mm<br>95 mm<br>**----- End of picture text -----**<br>


31 DS5396 Coax FIU Module - Component Manual 

December 2024 

Data Sheets 

32 DS5396 Coax FIU Module - Component Manual 

December 2024 

