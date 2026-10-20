# MIPI_CSI-2_V1.3

Source: C:\Users\JHARVEY\OneDrive - Volvo Cars\Documents\01_Resources\04_DatasheetsAndSpecification\MIPI_CSI-2_V1.3.pdf

**==> picture [15 x 679] intentionally omitted <==**

**==> picture [316 x 115] intentionally omitted <==**

## **Specification for Camera Serial Interface 2 (CSI-2)[SM]** 

## **Version 1.3** 

## **29 May 2014** 

MIPI Board Adopted 07 October 2014 

This document is subject to further editorial and technical development. 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

Specification for CSI-2 

Version 1.3 29-May-2014 

## **NOTICE OF DISCLAIMER** 

The material contained herein is not a license, either expressly or impliedly, to any IPR owned or controlled by any of the authors or developers of this material or MIPI[®] . The material contained herein is provided on an “AS IS” basis and to the maximum extent permitted by applicable law, this material is provided AS IS AND WITH ALL FAULTS, and the authors and developers of this material and MIPI hereby disclaim all other warranties and conditions, either express, implied or statutory, including, but not limited to, any (if any) implied warranties, duties or conditions of merchantability, of fitness for a particular purpose, of accuracy or completeness of responses, of results, of workmanlike effort, of lack of viruses, and of lack of negligence. 

All materials contained herein are protected by copyright laws, and may not be reproduced, republished, distributed, transmitted, displayed, broadcast or otherwise exploited in any manner without the express prior written permission of MIPI Alliance. MIPI, MIPI Alliance and the dotted rainbow arch and all related trademarks, tradenames, and other intellectual property are the exclusive property of MIPI Alliance and cannot be used without its express prior written permission. 

ALSO, THERE IS NO WARRANTY OF CONDITION OF TITLE, QUIET ENJOYMENT, QUIET POSSESSION, CORRESPONDENCE TO DESCRIPTION OR NON-INFRINGEMENT WITH REGARD TO THIS MATERIAL OR THE CONTENTS OF THIS DOCUMENT. IN NO EVENT WILL ANY AUTHOR OR DEVELOPER OF THIS MATERIAL OR THE CONTENTS OF THIS DOCUMENT OR MIPI BE LIABLE TO ANY OTHER PARTY FOR THE COST OF PROCURING SUBSTITUTE GOODS OR SERVICES, LOST PROFITS, LOSS OF USE, LOSS OF DATA, OR ANY INCIDENTAL, CONSEQUENTIAL, DIRECT, INDIRECT, OR SPECIAL DAMAGES WHETHER UNDER CONTRACT, TORT, WARRANTY, OR OTHERWISE, ARISING IN ANY WAY OUT OF THIS OR ANY OTHER AGREEMENT, SPECIFICATION OR DOCUMENT RELATING TO THIS MATERIAL, WHETHER OR NOT SUCH PARTY HAD ADVANCE NOTICE OF THE POSSIBILITY OF SUCH DAMAGES. 

Without limiting the generality of this Disclaimer stated above, the user of the contents of this Document is further notified that MIPI: (a) does not evaluate, test or verify the accuracy, soundness or credibility of the contents of this Document; (b) does not monitor or enforce compliance with the contents of this Document; and (c) does not certify, test, or in any manner investigate products or services or any claims of compliance with the contents of this Document. The use or implementation of the contents of this Document may involve or require the use of intellectual property rights (“IPR”) including (but not limited to) patents, patent applications, or copyrights owned by one or more parties, whether or not Members of MIPI. MIPI does not make any search or investigation for IPR, nor does MIPI require or request the disclosure of any IPR or claims of IPR as respects the contents of this Document or otherwise. 

Questions pertaining to this document, or the terms or conditions of its provision, should be addressed to: 

MIPI Alliance, Inc. c/o IEEE-ISTO 445 Hoes Lane Piscataway, NJ 08854 Attn: Board Secretary 

Copyright © 2005-2014 MIPI Alliance, Inc. 

ii 

All rights reserved. 

**Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

## **Contents** 

|**Contents**|**Contents**|**Contents**|
|---|---|---|
|**Contents ............................................................................................................................ iii**|||
|**Figures .............................................................................................................................. vii**|||
|**Tables ................................................................................................................................ xii**|||
|**Release History ............................................................................................................... xiii**|||
|**1**|**Introduction .................................................................................................................1**||
||1.1|Scope ............................................................................................................................... 1|
||1.2|Purpose ............................................................................................................................ 1|
|**2**|**Terminology .................................................................................................................2**||
||2.1|Use of Special Terms ....................................................................................................... 2|
||2.2|Definitions ....................................................................................................................... 2|
||2.3|Abbreviations ................................................................................................................... 3|
||2.4|Acronyms ......................................................................................................................... 3|
|**3**|**References ....................................................................................................................5**||
|**4**|**Overview of CSI-2 .......................................................................................................7**||
|**5**|**CSI-2 Layer Definitions ..............................................................................................9**||
|**6**|**Camera Control Interface (CCI) ............................................................................. 11**||
||6.1|Data Transfer Protocol ................................................................................................... 11|
||6.1.1|Message Type ............................................................................................................. 11|
||6.1.2|Read/Write Operations ............................................................................................... 12|
||6.2|CCI Slave Addresses ...................................................................................................... 15|
||6.3|CCI Multi-Byte Registers .............................................................................................. 15|
||6.3.1|Overview .................................................................................................................... 15|
||6.3.2|The Transmission Byte Order for Multi-byte Register Values ................................... 17|
||6.3.3|Multi-Byte Register Protocol...................................................................................... 18|
||6.4|Electrical Specifications and Timing for I/O Stages ...................................................... 22|
|**7**|**Physical Layer ...........................................................................................................26**||
||7.1|D-PHY Physical Layer Option ...................................................................................... 26|
||7.2|C-PHY Physical Layer Option ....................................................................................... 26|
|**8**|**Multi-Lane Distribution and Merging ....................................................................28**||
||8.1|Lane Distribution for the D-PHY Physical Layer Option .............................................. 31|
||8.2|Lane Distribution for the C-PHY Physical Layer Option .............................................. 35|
||8.3|Multi-Lane Interoperability ........................................................................................... 36|
|**9**|**Low**|**Level Protocol ....................................................................................................39**|
||9.1|Low Level Protocol Packet Format ............................................................................... 39|
||9.1.1|Low Level Protocol Long Packet Format ................................................................... 39|
||9.1.2|Low Level Protocol Short Packet Format .................................................................. 44|
||9.2|Data Identifier (DI) ........................................................................................................ 45|
||9.3|Virtual Channel Identifier .............................................................................................. 45|
||9.4|Data Type (DT) .............................................................................................................. 46|
||9.5|Packet Header Error Correction Code for D-PHY Physical Layer Option .................... 46|
||9.5.1|General Hamming Code Applied to Packet Header ................................................... 47|



Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

iii 

Specification for CSI-2 

Version 1.3 29-May-2014 

|9.5.2<br>Hamming-Modified Code .......................................................................................... 48|
|---|
|9.5.3<br>ECC Generation on TX Side ...................................................................................... 51|
|9.5.4<br>Applying ECC on RX Side ......................................................................................... 51|
|9.6<br>Checksum Generation .................................................................................................... 53|
|9.7<br>Packet Spacing ............................................................................................................... 55|
|9.8<br>Synchronization Short Packet Data Type Codes............................................................ 56|
|9.8.1<br>Frame Synchronization Packets.................................................................................. 56|
|9.8.2<br>Line Synchronization Packets .................................................................................... 57|
|9.9<br>Generic Short Packet Data Type Codes ......................................................................... 57|
|9.10<br>Packet Spacing Examples .............................................................................................. 57|
|9.11<br>Packet Data Payload Size Rules .................................................................................... 60|
|9.12<br>Frame Format Examples ................................................................................................ 61|
|9.13<br>Data Interleaving ........................................................................................................... 63|
|9.13.1<br>Data Type Interleaving ........................................................................................... 63|
|9.13.2<br>Virtual Channel Identifier Interleaving ................................................................... 66|
|**10**<br>**Color Spaces ...........................................................................................................68**|
|10.1<br>RGB Color Space Definition ......................................................................................... 68|
|10.2<br>YUV Color Space Definition ......................................................................................... 68|
|**11**<br>**Data Formats ..........................................................................................................69**|
|11.1<br>Generic 8-bit Long Packet Data Types .......................................................................... 70|
|11.1.1<br>Null and Blanking Data .......................................................................................... 70|
|11.1.2<br>Embedded Information ........................................................................................... 70|
|11.2<br>YUV Image Data ........................................................................................................... 71|
|11.2.1<br>Legacy YUV420 8-bit ............................................................................................ 72|
|11.2.2<br>YUV420 8-bit ......................................................................................................... 74|
|11.2.3<br>YUV420 10-bit ....................................................................................................... 76|
|11.2.4<br>YUV422 8-bit ......................................................................................................... 78|
|11.2.5<br>YUV422 10-bit ....................................................................................................... 80|
|11.3<br>RGB Image Data ............................................................................................................ 81|
|11.3.1<br>RGB888 .................................................................................................................. 82|
|11.3.2<br>RGB666 .................................................................................................................. 83|
|11.3.3<br>RGB565 .................................................................................................................. 84|
|11.3.4<br>RGB555 .................................................................................................................. 85|
|11.3.5<br>RGB444 .................................................................................................................. 86|
|11.4<br>RAW Image Data ........................................................................................................... 87|
|11.4.1<br>RAW6 ..................................................................................................................... 87|
|11.4.2<br>RAW7 ..................................................................................................................... 88|
|11.4.3<br>RAW8 ..................................................................................................................... 89|
|11.4.4<br>RAW10 ................................................................................................................... 90|
|11.4.5<br>RAW12 ................................................................................................................... 91|
|11.4.6<br>RAW14 ................................................................................................................... 92|
|11.5<br>User Defined Data Formats ........................................................................................... 93|
|**12**<br>**Recommended Memory Storage ...........................................................................96**|
|12.1<br>General/Arbitrary Data Reception ................................................................................. 96|
|12.2<br>RGB888 Data Reception ............................................................................................... 96|
|12.3<br>RGB666 Data Reception ............................................................................................... 97|
|12.4<br>RGB565 Data Reception ............................................................................................... 98|



Copyright © 2005-2014 MIPI Alliance, Inc. 

iv 

All rights reserved. **Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

|12.5|RGB555 Data Reception ............................................................................................... 98|
|---|---|
|12.6|RGB444 Data Reception ............................................................................................... 98|
|12.7|YUV422 8-bit Data Reception ...................................................................................... 99|
|12.8|YUV422 10-bit Data Reception .................................................................................... 99|
|12.9|YUV420 8-bit (Legacy) Data Reception ..................................................................... 100|
|12.10|YUV420 8-bit Data Reception .................................................................................... 101|
|12.11|YUV420 10-bit Data Reception .................................................................................. 102|
|12.12|RAW6 Data Reception ................................................................................................. 104|
|12.13|RAW7 Data Reception ................................................................................................. 104|
|12.14|RAW8 Data Reception ................................................................................................. 104|
|12.15|RAW10 Data Reception ............................................................................................... 105|
|12.16|RAW12 Data Reception ............................................................................................... 105|
|12.17|RAW14 Data Reception ............................................................................................... 106|
|**Annex A**|**JPEG8 Data Format (informative) .........................................................107**|
|A.1|Introduction.................................................................................................................. 107|
|A.2|JPEG Data Definition .................................................................................................. 107|
|A.3|Image Status Information ............................................................................................ 108|
|A.4|Embedded Images ........................................................................................................ 109|
|A.5|JPEG8 Non-standard Markers ..................................................................................... 110|
|A.6|JPEG8 Data Reception ................................................................................................ 111|
|**Annex B**|**CSI-2 Implementation Example (informative) ..................................... 112**|
|B.1|Overview...................................................................................................................... 112|
|B.2|CSI-2 Transmitter Detailed Block Diagram ................................................................ 112|
|B.3|CSI-2 Receiver Detailed Block Diagram ..................................................................... 113|
|B.4|Details on the D-PHY implementation ........................................................................ 114|
|B.4.1|CSI-2 Clock Lane Transmitter .............................................................................. 115|
|B.4.2|CSI-2 Clock Lane Receiver .................................................................................. 116|
|B.4.3|CSI-2 Data Lane Transmitter ................................................................................ 117|
|B.4.4|CSI-2 Data Lane Receiver .................................................................................... 119|
|**Annex C**|**CSI-2 Recommended Receiver Error Behavior (informative) ............121**|
|C.1|Overview...................................................................................................................... 121|
|C.2|D-PHY Level Error ...................................................................................................... 121|
|C.3|Packet Level Error ....................................................................................................... 122|
|C.4|Protocol Decoding Level Error .................................................................................... 123|
|**Annex D**|**CSI-2 Sleep Mode (informative) .............................................................124**|
|D.1|Overview...................................................................................................................... 124|
|D.2|SLM Command Phase ................................................................................................. 124|
|D.3|SLM Entry Phase ......................................................................................................... 124|
|D.4|SLM Exit Phase ........................................................................................................... 125|
|**Annex E**|**Data Compression for RAW Data Types (normative) ..........................126**|
|E.1|Predictors ..................................................................................................................... 127|
|E.1.1|Predictor1 ................................................................................................................. 128|
|E.1.2|Predictor2 ................................................................................................................. 128|
|E.2|Encoders ...................................................................................................................... 128|
|E.2.1|Coder for 10–8–10 Data Compression ..................................................................... 129|
|E.2.2|Coder for 10–7–10 Data Compression ..................................................................... 130|



Copyright © 2005-2014 MIPI Alliance, Inc. 

v 

All rights reserved. **Confidential** 

Specification for CSI-2 

Version 1.3 

29-May-2014 

|E.2.3|Coder for 10–6–10 Data Compression ..................................................................... 132|
|---|---|
|E.2.4|Coder for 12–8–12 Data Compression ..................................................................... 134|
|E.2.5|Coder for 12–7–12 Data Compression ..................................................................... 136|
|E.2.6|Coder for 12–6–12 Data Compression ..................................................................... 139|
|E.3|Decoders ...................................................................................................................... 141|
|E.3.1|Decoder for 10–8–10 Data Compression ................................................................. 141|
|E.3.2|Decoder for 10–7–10 Data Compression ................................................................. 143|
|E.3.3|Decoder for 10–6–10 Data Compression ................................................................. 145|
|E.3.4|Decoder for 12–8–12 Data Compression ................................................................. 148|
|E.3.5|Decoder for 12–7–12 Data Compression ................................................................. 150|
|E.3.6|Decoder for 12–6–12 Data Compression ................................................................. 153|
|**Annex F**|**JPEG Interleaving (informative) ...............................................................157**|



Copyright © 2005-2014 MIPI Alliance, Inc. 

vi 

All rights reserved. **Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

## **Figures** 

Figure 1 CSI-2 and CCI Transmitter and Receiver Interface for D-PHY ........................................ 7 Figure 2 CSI-2 and CCI Transmitter and Receiver Interface for C-PHY......................................... 8 Figure 3 CSI-2 Layer Definitions ..................................................................................................... 9 Figure 4 CCI Message Types .......................................................................................................... 12 Figure 5 CCI Single Read from Random Location ........................................................................ 12 Figure 6 CCI Single Read from Current Location ......................................................................... 13 Figure 7 CCI Sequential Read Starting from a Random Location ................................................. 13 Figure 8 CCI Sequential Read Starting from the Current Location ............................................... 14 Figure 9 CCI Single Write to a Random Location ......................................................................... 14 Figure 10 CCI Sequential Write Starting from a Random Location .............................................. 15 Figure 11 Corruption of a 32-bit Wide Register during a Read Message ....................................... 16 Figure 12 Corruption of a 32-bit Wide Register during a Write Message ...................................... 17 Figure 13 Example 16-bit Register Write ....................................................................................... 17 Figure 14 Example 32-bit Register Write (address not shown) ...................................................... 18 Figure 15 Example 64-bit Register Write (address not shown) ...................................................... 18 Figure 16 Example 16-bit Register Read ....................................................................................... 19 Figure 17 Example 32-bit Register Read ....................................................................................... 20 Figure 18 Example 16-bit Register Write ....................................................................................... 21 Figure 19 Example 32-bit Register Write ....................................................................................... 22 Figure 20 CCI Timing .................................................................................................................... 25 Figure 21 Conceptual Overview of the Lane Distributor Function for D-PHY ............................. 28 Figure 22 Conceptual Overview of the Lane Distributor Function for C-PHY ............................. 29 Figure 23 Conceptual Overview of the Lane Merging Function for D-PHY ................................. 30 Figure 24 Conceptual Overview of the Lane Merging Function for C-PHY ................................. 31 Figure 25 Two Lane Multi-Lane Example for D-PHY .................................................................. 32 Figure 26 Three Lane Multi-Lane Example for D-PHY ................................................................ 33 Figure 27 N-Lane Multi-Lane Example for D-PHY ...................................................................... 34 Figure 28 N-Lane Multi-Lane Example for D-PHY Short Packet Transmission ........................... 35 Figure 29 Two Lane Multi-Lane Example for C-PHY ................................................................... 36 Figure 30 Three Lane Multi-Lane Example for C-PHY ................................................................ 36 Figure 31 General N-Lane Multi-Lane Distribution for C-PHY .................................................... 36 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

vii 

Specification for CSI-2 

Version 1.3 29-May-2014 

Figure 32 One Lane Transmitter and N-Lane Receiver Example for D-PHY................................ 37 Figure 33 M-Lane Transmitter and N-Lane Receiver Example (M<N) for D-PHY ...................... 37 Figure 34 M-Lane Transmitter and One Lane Receiver Example for D-PHY ............................... 38 Figure 35 M-Lane Transmitter and N-Lane Receiver Example (N<M) for D-PHY ...................... 38 Figure 36 Low Level Protocol Packet Overview ........................................................................... 39 Figure 37 Long Packet Structure for D-PHY Physical Layer Option ............................................ 40 Figure 38 Long Packet Structure for C-PHY Physical Layer Option ............................................. 41 Figure 39 Packet Header Lane Distribution for C-PHY Physical Layer Option ............................ 41 Figure 40 Minimal Filler Byte Insertion Requirements for Three Lane C-PHY ............................ 43 Figure 41 Short Packet Structure for D-PHY Physical Layer Option ............................................ 44 Figure 42 Short Packet Structure for C-PHY Physical Layer Option ............................................ 44 Figure 43 Data Identifier Byte ........................................................................................................ 45 Figure 44 Logical Channel Block Diagram (Receiver) .................................................................. 45 Figure 45 Interleaved Video Data Streams Examples .................................................................... 46 Figure 46 24-bit ECC Generation Example ................................................................................... 47 Figure 47 64-bit ECC Generation on TX Side ............................................................................... 51 Figure 48 24-bit ECC Generation on TX Side ............................................................................... 51 Figure 49 64-bit ECC on RX Side Including Error Correction ...................................................... 52 Figure 50 24-bit ECC on RX Side Including Error Correction ...................................................... 53 Figure 51 Checksum Transmission Byte Order .............................................................................. 53 Figure 52 Checksum Generation for Long Packet Payload Data ................................................... 54 Figure 53 Definition of 16-bit CRC Shift Register ........................................................................ 54 Figure 54 16-bit CRC Software Implementation Example ............................................................ 55 Figure 55 Packet Spacing ............................................................................................................... 56 Figure 56 Multiple Packet Example ............................................................................................... 58 Figure 57 Single Packet Example ................................................................................................... 58 Figure 58 Line and Frame Blanking Definitions ............................................................................ 59 Figure 59 Vertical Sync Example ................................................................................................... 60 Figure 60 Horizontal Sync Example .............................................................................................. 60 Figure 61 General Frame Format Example .................................................................................... 61 Figure 62 Digital Interlaced Video Example .................................................................................. 62 Figure 63 Digital Interlaced Video with Accurate Synchronization Timing Information .............. 63 Figure 64 Interleaved Data Transmission using Data Type Value .................................................. 64 

Copyright © 2005-2014 MIPI Alliance, Inc. 

viii 

All rights reserved. **Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

Figure 65 Packet Level Interleaved Data Transmission ................................................................. 65 Figure 66 Frame Level Interleaved Data Transmission .................................................................. 66 Figure 67 Interleaved Data Transmission using Virtual Channels ................................................. 67 Figure 68 Byte Packing Pixel Data to C-PHY Symbol Illustration ................................................ 70 Figure 69 Frame Structure with Embedded Data at the Beginning and End of the Frame ............ 71 Figure 70 Legacy YUV420 8-bit Transmission .............................................................................. 72 Figure 71 Legacy YUV420 8-bit Pixel to Byte Packing Bitwise Illustration................................. 73 Figure 72 Legacy YUV420 Spatial Sampling for H.261, H.263 and MPEG 1 .............................. 73 Figure 73 Legacy YUV420 8-bit Frame Format ............................................................................ 74 Figure 74 YUV420 8-bit Data Transmission Sequence ................................................................. 74 Figure 75 YUV420 8-bit Pixel to Byte Packing Bitwise Illustration ............................................. 75 Figure 76 YUV420 Spatial Sampling for H.261, H.263 and MPEG 1 ........................................... 75 Figure 77 YUV420 Spatial Sampling for MPEG 2 and MPEG 4 .................................................. 76 Figure 78 YUV420 8-bit Frame Format ......................................................................................... 76 Figure 79 YUV420 10-bit Transmission ........................................................................................ 77 Figure 80 YUV420 10-bit Pixel to Byte Packing Bitwise Illustration ........................................... 77 Figure 81 YUV420 10-bit Frame Format ....................................................................................... 78 Figure 82 YUV422 8-bit Transmission .......................................................................................... 78 Figure 83 YUV422 8-bit Pixel to Byte Packing Bitwise Illustration ............................................. 79 Figure 84 YUV422 Co-sited Spatial Sampling .............................................................................. 79 Figure 85 YUV422 8-bit Frame Format ......................................................................................... 80 Figure 86 YUV422 10-bit Transmitted Bytes ................................................................................ 80 Figure 87 YUV422 10-bit Pixel to Byte Packing Bitwise Illustration ........................................... 81 Figure 88 YUV422 10-bit Frame Format ....................................................................................... 81 Figure 89 RGB888 Transmission ................................................................................................... 82 Figure 90 RGB888 Transmission in CSI-2 Bus Bitwise Illustration .............................................. 82 Figure 91 RGB888 Frame Format .................................................................................................. 83 Figure 92 RGB666 Transmission with 18-bit BGR Words ............................................................ 83 Figure 93 RGB666 Transmission on CSI-2 Bus Bitwise Illustration ............................................. 84 Figure 94 RGB666 Frame Format .................................................................................................. 84 Figure 95 RGB565 Transmission with 16-bit BGR Words ............................................................ 85 Figure 96 RGB565 Transmission on CSI-2 Bus Bitwise Illustration ............................................. 85 Figure 97 RGB565 Frame Format .................................................................................................. 85 

Copyright © 2005-2014 MIPI Alliance, Inc. ix All rights reserved. **Confidential** 

Specification for CSI-2 

Version 1.3 29-May-2014 

Figure 98 RGB555 Transmission on CSI-2 Bus Bitwise Illustration ............................................. 86 Figure 99 RGB444 Transmission on CSI-2 Bus Bitwise Illustration ............................................. 86 Figure 100 RAW6 Transmission .................................................................................................... 87 Figure 101 RAW6 Data Transmission on CSI-2 Bus Bitwise Illustration ..................................... 88 Figure 102 RAW6 Frame Format ................................................................................................... 88 Figure 103 RAW7 Transmission .................................................................................................... 88 Figure 104 RAW7 Data Transmission on CSI-2 Bus Bitwise Illustration ..................................... 89 Figure 105 RAW7 Frame Format ................................................................................................... 89 Figure 106 RAW8 Transmission .................................................................................................... 89 Figure 107 RAW8 Data Transmission on CSI-2 Bus Bitwise Illustration ..................................... 90 Figure 108 RAW8 Frame Format ................................................................................................... 90 Figure 109 RAW10 Transmission .................................................................................................. 90 Figure 110 RAW10 Data Transmission on CSI-2 Bus Bitwise Illustration .................................... 91 Figure 111 RAW10 Frame Format ................................................................................................. 91 Figure 112 RAW12 Transmission .................................................................................................. 92 Figure 113 RAW12 Transmission on CSI-2 Bus Bitwise Illustration ............................................ 92 Figure 114 RAW12 Frame Format ................................................................................................. 92 Figure 115 RAW14 Transmission .................................................................................................. 93 Figure 116 RAW14 Transmission on CSI-2 Bus Bitwise Illustration ............................................ 93 Figure 117 RAW14 Frame Format ................................................................................................. 93 Figure 118 User Defined 8-bit Data (128 Byte Packet) ................................................................. 94 Figure 119 User Defined 8-bit Data Transmission on CSI-2 Bus Bitwise Illustration ................... 94 Figure 120 Transmission of User Defined 8-bit Data ..................................................................... 94 Figure 121 General/Arbitrary Data Reception ............................................................................... 96 Figure 122 RGB888 Data Format Reception ................................................................................. 97 Figure 123 RGB666 Data Format Reception ................................................................................. 97 Figure 124 RGB565 Data Format Reception ................................................................................. 98 Figure 125 RGB555 Data Format Reception ................................................................................. 98 Figure 126 RGB444 Data Format Reception ................................................................................. 99 Figure 127 YUV422 8-bit Data Format Reception ........................................................................ 99 Figure 128 YUV422 10-bit Data Format Reception .................................................................... 100 Figure 129 YUV420 8-bit Legacy Data Format Reception .......................................................... 101 Figure 130 YUV420 8-bit Data Format Reception ...................................................................... 102 

x Copyright © 2005-2014 MIPI Alliance, Inc. 

All rights reserved. **Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

Figure 131 YUV420 10-bit Data Format Reception .................................................................... 103 Figure 132 RAW6 Data Format Reception .................................................................................. 104 Figure 133 RAW7 Data Format Reception .................................................................................. 104 Figure 134 RAW8 Data Format Reception .................................................................................. 105 Figure 135 RAW10 Data Format Reception ................................................................................ 105 Figure 136 RAW12 Data Format Reception ................................................................................ 106 Figure 137 RAW 14 Data Format Reception ............................................................................... 106 Figure 138 JPEG8 Data Flow in the Encoder .............................................................................. 107 Figure 139 JPEG8 Data Flow in the Decoder .............................................................................. 107 Figure 140 EXIF Compatible Baseline JPEG DCT Format ......................................................... 108 Figure 141 Status Information Field in the End of Baseline JPEG Frame ................................... 109 Figure 142 Example of TN Image Embedding Inside the Compressed JPEG Data Block .......... 110 Figure 143 JPEG8 Data Format Reception .................................................................................. 111 Figure 144 Implementation Example Block Diagram and Coverage ........................................... 112 Figure 145 CSI-2 Transmitter Block Diagram ............................................................................. 113 Figure 146 CSI-2 Receiver Block Diagram ................................................................................. 114 Figure 147 D-PHY Level Block Diagram .................................................................................... 115 Figure 148 CSI-2 Clock Lane Transmitter ................................................................................... 116 Figure 149 CSI-2 Clock Lane Receiver ....................................................................................... 117 Figure 150 CSI-2 Data Lane Transmitter ..................................................................................... 118 Figure 151 CSI-2 Data Lane Receiver ......................................................................................... 119 Figure 152 SLM Synchronization ................................................................................................ 125 Figure 153 Data Compression System Block Diagram ................................................................ 127 Figure 154 Pixel Order of the Original Image .............................................................................. 127 Figure 155 Example Pixel Order of the Original Image .............................................................. 127 Figure 156 Data Type Interleaving: Concurrent JPEG and YUV Image Data ............................. 157 Figure 157 Virtual Channel Interleaving: Concurrent JPEG and YUV Image Data .................... 158 Figure 158 Example JPEG and YUV Interleaving Use Cases ..................................................... 159 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

xi 

Specification for CSI-2 

Version 1.3 29-May-2014 

## **Tables** 

Table 1 CCI I/O Characteristics ..................................................................................................... 22 Table 2 CCI Timing Specification .................................................................................................. 24 Table 3 Data Type Classes .............................................................................................................. 46 Table 4 ECC Syndrome Association Matrix ................................................................................... 48 Table 5 ECC Parity Generation Rules ............................................................................................ 49 Table 6 Synchronization Short Packet Data Type Codes ............................................................... 56 Table 7 Generic Short Packet Data Type Codes ............................................................................. 57 Table 8 Primary and Secondary Data Formats Definitions ............................................................ 69 Table 9 Generic 8-bit Long Packet Data Types .............................................................................. 70 Table 10 YUV Image Data Types ................................................................................................... 71 Table 11 Legacy YUV420 8-bit Packet Data Size Constraints ...................................................... 72 Table 12 YUV420 8-bit Packet Data Size Constraints ................................................................... 74 Table 13 YUV420 10-bit Packet Data Size Constraints ................................................................. 77 Table 14 YUV422 8-bit Packet Data Size Constraints ................................................................... 78 Table 15 YUV422 10-bit Packet Data Size Constraints ................................................................. 80 Table 16 RGB Image Data Types ................................................................................................... 81 Table 17 RGB888 Packet Data Size Constraints ............................................................................ 82 Table 18 RGB666 Packet Data Size Constraints ............................................................................ 83 Table 19 RGB565 Packet Data Size Constraints ............................................................................ 84 Table 20 RAW Image Data Types .................................................................................................. 87 Table 21 RAW6 Packet Data Size Constraints ............................................................................... 87 Table 22 RAW7 Packet Data Size Constraints ............................................................................... 88 Table 23 RAW8 Packet Data Size Constraints ............................................................................... 89 Table 24 RAW10 Packet Data Size Constraints ............................................................................. 90 Table 25 RAW12 Packet Data Size Constraints ............................................................................. 91 Table 26 RAW14 Packet Data Size Constraints ............................................................................. 92 Table 27 User Defined 8-bit Data Types ........................................................................................ 94 Table 28 Status Data Padding ....................................................................................................... 109 Table 29 JPEG8 Additional Marker Codes Listing ...................................................................... 111 

Copyright © 2005-2014 MIPI Alliance, Inc. 

xii 

All rights reserved. **Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

## **Release History** 

||||
|---|---|---|
|**Date**|**Version**|**Description**|
|2005-11-29|v1.00|Initial Board-approved release.|
|2010-11-09|v1.01.00|Board-approved release.|
|2013-01-22|v1.1|Board approved release.|
|2014-09-10|v1.2|Board approved release.|
|2014-10-07|v1.3|Board approved release.|



Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

xiii 

Specification for CSI-2 

Version 1.3 29-May-2014 

This page intentionally left blank. 

Copyright © 2005-2014 MIPI Alliance, Inc. 

xiv 

All rights reserved. **Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

## **1 Introduction** 

## **1.1 Scope** 

- 1 The Camera Serial Interface 2 Specification defines an interface between a peripheral device (camera) and 2 a host processor (baseband, application engine). The purpose of this document is to specify a standard 3 interface between a camera and a host processor for mobile applications. 

- 4 This Revision of the Camera Serial Interface 2 Specification leverages [MIPI01] D-PHY 1.2 and introduces 5 [MIPI02] C-PHY 1.0, both with improved skew tolerance and higher data rates. These enhancements 6 enable higher interface bandwidth and more flexibility in channel layout. The CSI-2 1.3 Specification was 

- 7 designed to ensure interoperability with CSI-2 1.2 when the former uses the D-PHY physical layer. If the 8 C-PHY physical layer only is used, backwards compatibility cannot be maintained. 

- 9 A host processor in this document refers to the hardware and software that performs essential core 

- 10 functions for telecommunication or application tasks. The engine of a mobile terminal includes hardware 11 and the functions, which enable the basic operation of the mobile terminal. These include, for example, the 

- 12 printed circuit boards, RF components, basic electronics, and basic software, such as the digital signal 13 processing software. 

## **1.2 Purpose** 

- 14 Demand for increasingly higher image resolutions is pushing the bandwidth capacity of existing host 15 processor-to-camera sensor interfaces. Common parallel interfaces are difficult to expand, require many 16 interconnects and consume relatively large amounts of power. Emerging serial interfaces address many of 17 the shortcomings of parallel interfaces while introducing their own problems. Incompatible, proprietary 18 interfaces prevent devices from different manufacturers from working together. This can raise system costs 19 and reduce system reliability by requiring “hacks” to force the devices to interoperate. The lack of a clear 20 industry standard can slow innovation and inhibit new product market entry. 

- 21 CSI-2 provides the mobile industry a standard, robust, scalable, low-power, high-speed, cost-effective 22 interface that supports a wide range of imaging solutions for mobile devices. 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

1 

Specification for CSI-2 

Version 1.3 29-May-2014 

## **2 Terminology** 

## **2.1 Use of Special Terms** 

- 23 The MIPI Alliance has adopted Section 13.1 of the _IEEE Standards Style Manual_ , which dictates use of the 24 words “shall”, “should”, “may”, and “can” in the development of documentation, as follows: 

- 25 The word _shall_ is used to indicate mandatory requirements strictly to be followed in order 26 to conform to the Specification and from which no deviation is permitted ( _shall_ equals _is_ 27 _required to_ ). 

- 28 The use of the word _must_ is deprecated and shall not be used when stating mandatory 29 requirements; _must_ is used only to describe unavoidable situations. 

- 30 The use of the word _will_ is deprecated and shall not be used when stating mandatory 31 requirements; _will_ is only used in statements of fact. 

- 32 The word _should_ is used to indicate that among several possibilities one is recommended 33 as particularly suitable, without mentioning or excluding others; or that a certain course 34 of action is preferred but not necessarily required; or that (in the negative form) a certain 35 course of action is deprecated but not prohibited ( _should_ equals _is recommended that_ ). 

- 36 The word _may_ is used to indicate a course of action permissible within the limits of the 37 Specification ( _may_ equals _is permitted to_ ). 

- 38 The word _can_ is used for statements of possibility and capability, whether material, 39 physical, or causal ( _can_ equals _is able to_ ). 

- 40 All sections are normative, unless they are explicitly indicated to be informative. 

## **2.2 Definitions** 

- 41 **Lane:** A unidirectional, point-to-point, 2- or 3-wire interface used for high-speed serial clock or data 42 transmission; the number of wires is determined by the PHY specification in use (i.e. either D-PHY or C- 43 PHY, respectively). A CSI-2 camera interface using the D-PHY physical layer consists of one clock Lane 44 and one or more data Lanes. A CSI-2 camera interface using the C-PHY physical layer consists of one or 

- 45 more Lanes, each of which transmits both clock and data information. Note that when describing features 

- 46 or behavior applying to both D-PHY and C-PHY, this specification sometimes uses the term data Lane to 47 refer to both a D-PHY data Lane and a C-PHY Lane. 

- 48 **Packet:** A group of bytes organized in a specified way to transfer data across the interface. All packets have 49 a minimum specified set of components. The byte is the fundamental unit of data from which packets are 50 made. 

- 51 **Payload:** Application data only – with all sync, header, ECC and checksum and other protocol-related 52 information removed. This is the “core” of transmissions between application processor and peripheral. 

- 53 **Sleep Mode:** Sleep mode (SLM) is a leakage level only power consumption mode. 

- 54 **Transmission:** The time during which high-speed serial data is actively traversing the bus. A transmission 

- 55 is comprised of one or more packets. A transmission is bounded by SoT (Start of Transmission) and EoT 56 (End of Transmission) at beginning and end, respectively. 

- 57 **Virtual Channel:** Multiple independent data streams for up to four peripherals are supported by this 

- 58 Specification. The data stream for each peripheral is a Virtual Channel. These data streams may be 

- 59 interleaved and sent as sequential packets, with each packet dedicated to a particular peripheral or channel. 60 Packet protocol includes information that links each packet to its intended peripheral. 

Copyright © 2005-2014 MIPI Alliance, Inc. 

2 

All rights reserved. 

**Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

## **2.3 Abbreviations** 

- 61 

   - e.g. For example (Latin: exempli gratia) 

- 62 i.e. That is (Latin: id est) 

## **2.4 Acronyms** 

- 63 BER Bit Error Rate 

- 64 CCI Camera Control Interface 

- 65 

- 66 

- 67 

- 68 

- 69 

- 70 

- 71 

   - CIL Control and Interface Logic CRC Cyclic Redundancy Check 

   - CSI Camera Serial Interface 

   - CSPS Chroma Shifted Pixel Sampling 

   - DDR Dual Data Rate 

   - DI Data Identifier 

   - DT Data Type 

- 72 ECC Error Correction Code 

- 73 EoT End of Transmission 

- 74 

- 75 

- 76 

- 77 

   - EXIF Exchangeable Image File Format 

   - FE Frame End 

   - FS Frame Start 

   - HS High Speed; identifier for operation mode 

- 78 HS-RX High-Speed Receiver 

- 79 HS-TX High-Speed Transmitter 

- 80 

- 81 

   - I2C Inter-Integrated Circuit 

   - JFIF JPEG File Interchange Format 

- 82 JPEG Joint Photographic Expert Group 

- 83 LE Line End 

- 84 LLP Low Level Protocol 

- 85 

   - LS Line Start 

- 86 LSB Least Significant Bit 

- 87 LSS Least Significant Symbol 

- 88 LP Low-Power; identifier for operation mode 

- 89 LP-RX Low-Power Receiver (Large-Swing Single Ended) 

- 90 LP-TX Low-Power Transmitter (Large-Swing Single Ended) 

- 91 MSB Most Significant Bit 

- 92 MSS Most Significant Symbol 

Copyright © 2005-2014 MIPI Alliance, Inc. 

3 

All rights reserved. 

**Confidential** 

Specification for CSI-2 

Version 1.3 29-May-2014 

- 93 PF Packet Footer 94 PH Packet Header 95 PI Packet Identifier 96 PT Packet Type 97 PHY Physical Layer 98 PPI PHY Protocol Interface 

- 99 RGB Color representation (Red, Green, Blue) 

- 100 RX Receiver 101 SCL Serial Clock (for CCI) 102 SDA Serial Data (for CCI) 103 SLM Sleep Mode 104 SoT Start of Transmission 105 TX Transmitter 106 ULPS Ultra low Power State 107 VGA Video Graphics Array 108 YUV Color representation (Y for luminance, U & V for chrominance) 

Copyright © 2005-2014 MIPI Alliance, Inc. 

4 

All rights reserved. 

**Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

## **3 References** 

|109|[NXP01]|UM10204,_I2C-bus specification and user manual_, Revision 03, NXP B.V.,|
|---|---|---|
|110||19 June 2007.|
|111|[MIPI01]|_MIPI Alliance Specification for D PHY_, version 1.2, MIPI Alliance, Inc.,|
|112||10 September 2014.|
|113|[MIPI02]|_MIPI Alliance Specification for C PHY_, version 1.0, MIPI Alliance, Inc.,|
|114||07 October 2014.|



Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

5 

Specification for CSI-2 

Version 1.3 29-May-2014 

This page intentionally left blank. 

Copyright © 2005-2014 MIPI Alliance, Inc. 

6 

All rights reserved. **Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

## 115 **4 Overview of CSI-2** 

- 116 The CSI-2 Specification defines standard data transmission and control interfaces between transmitter and 117 receiver. Two high-speed serial data transmission interface options are defined. The first option, referred to 

- 118 in this specification as the “D-PHY physical layer option”, is a unidirectional differential interface with one 

- 119 2-wire clock Lane and one or more 2-wire data Lanes. The physical layer of this interface is defined by the 

- 120 _MIPI Alliance Specification for D-PHY_ [MIPI01]. Figure 1 illustrates the connections for this option 121 between a CSI-2 transmitter and receiver, which typically are a camera module and a receiver module, part 122 of the mobile phone engine. 

- 123 The second high-speed data transmission interface option, referred to in this specification as the “C-PHY 124 physical layer option”, consists of one or more unidirectional 3-wire serial data Lanes, each of which has its 125 own embedded clock. The physical layer of this interface is defined by the _MIPI Alliance Specification for_ 126 _C-PHY_ [MIPI02]. Figure 2 illustrates the CSI transmitter and receiver connections for this option. 

- 127 The Camera Control Interface (CCI) for both physical layer options is a bi-directional control interface 128 compatible with the I2C standard [NXP01]. 

129 

|**CSI Transmitter**<br>**Device e.g. a Camera containing the**<br>**CSI transmitter and CCI slave**<br>DataN+<br>DataN-<br>Clock+<br>Clock-<br>Data1+<br>Data1-<br>SCL<br>SDA<br>**CCI Slave**|N 2-wire Data Lanes<br>**Unidirectional High**<br>**Speed Data  Link**<br>**400kHz Bidirectional**<br>**Control Link**<br>One 2-wire Clock Lane|N 2-wire Data Lanes<br>**Unidirectional High**<br>**Speed Data  Link**<br>**400kHz Bidirectional**<br>**Control Link**<br>One 2-wire Clock Lane|**CSI Receiver**<br>**Device e.g. an application engine or**<br>**base band containing the CSI receiver**<br>**and the CCI master**<br>DataN+<br>DataN-<br>Clock+<br>Clock-<br>Data1+<br>Data1-<br>SCL<br>SDA<br>**CCI Master**|
|---|---|---|---|
|||||



**Figure 1 CSI-2 and CCI Transmitter and Receiver Interface for D-PHY** 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

7 

Specification for CSI-2 

Version 1.3 

29-May-2014 

130 

**==> picture [409 x 216] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device e.g. a Camera containing the  Device e.g. an application engine or<br>CSI transmitter and CCI slave base band containing the CSI receiver<br>and the CCI master<br>Unidirectional High<br>Speed Data  Link<br>CSI Transmitter CSI Receiver<br>N 3-Wire Lanes<br>DataN_A DataN_A<br>DataN_B DataN_B<br>DataN_C DataN_C<br>Data1_A Data1_A<br>Data1_B Data1_B<br>Data1_C Data1_C<br>400kHz Bidirectional<br>CCI Slave Control Link CCI Master<br>SCL SCL<br>SDA SDA<br>**----- End of picture text -----**<br>


**Figure 2 CSI-2 and CCI Transmitter and Receiver Interface for C-PHY** 

Copyright © 2005-2014 MIPI Alliance, Inc. 

8 

All rights reserved. **Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

## 131 **5 CSI-2 Layer Definitions** 

**==> picture [411 x 340] intentionally omitted <==**

**----- Start of picture text -----**<br>
Transmitter Receiver<br>Application Application<br>Pixel Control Pixel Control<br>6-, 7-, 8-, 10-, 12-, 14-, 15-, 16-, 18- or 24-bits<br>Pixel Control Data Formats Pixel Control<br>Pixel to Byte Byte to Pixel<br>Packing Formats Unpacking Formats<br>Data Control Data Control<br>8-bits 8-bits<br>Data Control Packet Based Protocol Data Control<br>Low Level Protocol Arbitrary Data Support Low Level Protocol<br>Data Control<br>Data Control<br>8-bits 8-bits<br>Lane Management  Lane Distribution/Lane Merging Lane Management<br>Layer Layer<br>N * n-bits  n =  8  for D-PHY; n = 16 for C-PHY  N * n-bits<br>Data Control Data Control<br>Generation / Detection of packet start<br>and stop signaling<br>PHY Layer Serializer / Deserializer PHY Layer<br>Clock Generation / Recovery (DDR)<br>Electrical Layer<br>High Speed Unidirectional Clock (only applies to D-PHY)<br>**----- End of picture text -----**<br>


High Speed Unidirectional Lane 1 

132 

High Speed Unidirectional Lane N 

## **Figure 3 CSI-2 Layer Definitions** 

- 133 Figure 3 defines the conceptual layer structure used in CSI-2. The layers can be characterized as follows: 

- 134 • **PHY Layer.** The PHY Layer specifies the transmission medium (electrical conductors), the 135 input/output circuitry and the clocking mechanism that captures “ones” and “zeroes” from the 136 serial bit stream. This part of the Specification documents the characteristics of the transmission 137 medium, electrical parameters for signaling and for the D-PHY physical layer option, the timing 138 relationship between clock and data Lanes. 

- 139 The mechanism for signaling Start of Transmission (SoT) and End of Transmission (EoT) is 140 specified as well as other “out of band” information that can be conveyed between transmitting 141 and receiving PHYs. Bit-level and byte-level synchronization mechanisms are included as part of 142 the PHY. 

- 143 The PHY layer is described in [MIPI01] and [MIPI02]. 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

9 

Specification for CSI-2 

Version 1.3 

29-May-2014 

- 144 • **Protocol Layer.** The Protocol layer is composed of several layers, each with distinct 145 responsibilities. The CSI-2 protocol enables multiple data streams using a single interface on the 146 host processor. The Protocol layer specifies how multiple data streams may be tagged and 147 interleaved so each data stream can be properly reconstructed. 148 • **Pixel/Byte Packing/Unpacking Layer.** The CSI-2 specification supports image applications 149 with varying pixel formats from six to twenty-four bits per pixel. In the transmitter this layer 150 packs pixels from the Application layer into bytes before sending the data to the Low Level 151 Protocol layer. In the receiver this layer unpacks bytes from the Low Level Protocol layer into 152 pixels before sending the data to the Application layer. Eight bits per pixel data is transferred 153 unchanged by this layer. 154 • **Low Level Protocol.** The Low Level Protocol (LLP) includes the means of establishing bit155 level and byte-level synchronization for serial data transferred between SoT (Start of 156 Transmission) and EoT (End of Transmission) events and for passing data to the next layer. The 157 minimum data granularity of the LLP is one byte. The LLP also includes assignment of bit-value 158 interpretation within the byte, i.e. the “Endian” assignment. 

- 159 • **Lane Management.** CSI-2 is Lane-scalable for increased performance. The number of data 160 Lanes is not limited by this specification and may be chosen depending on the bandwidth 161 requirements of the application. The transmitting side of the interface distributes (“distributor” 162 function) bytes from the outgoing data stream to one or more Lanes. On the receiving side, the 163 interface collects bytes from the Lanes and merges (“merger” function) them together into a 164 recombined data stream that restores the original stream sequence. For the C-PHY physical 165 layer option, this layer exclusively distributes or collects byte pairs (i.e. 16-bits) to or from the 166 data Lanes. 

- 167 Data within the Protocol layer is organized as packets. The transmitting side of the interface 168 appends header and error-checking information on to data to be transmitted at the Low Level 169 Protocol layer. On the receiving side, the header is stripped off at the Low Level Protocol layer 170 and interpreted by corresponding logic in the receiver. Error-checking information may be used to 171 test the integrity of incoming data. 172 • **Application Layer.** This layer describes higher-level encoding and interpretation of data 173 contained in the data stream and is beyond the scope of this specification. The CSI-2 Specification 174 describes the mapping of pixel values to bytes. 

- 175 The normative sections of the Specification only relate to the external part of the Link, e.g. the data and bit 176 patterns that are transferred across the Link. All internal interfaces and layers are purely informative. 

Copyright © 2005-2014 MIPI Alliance, Inc. 

10 

All rights reserved. 

**Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

## 177 **6 Camera Control Interface (CCI)** 

- 178 CCI is a two-wire, bi-directional, half duplex, serial interface for controlling the transmitter. CCI is 179 compatible with the fast mode variant of the I2C interface. CCI shall support 400kHz operation and 7-bit 180 Slave Addressing. 

- 181 A CSI-2 receiver shall be configured as a master and a CSI-2 transmitter shall be configured as a slave on 182 the CCI bus. CCI is capable of handling multiple slaves on the bus. However, multi-master mode is not 183 supported by CCI. Any I2C commands that are not described in this section shall be ignored and shall not 184 cause unintended device operation. Note that the terms master and slave, when referring to CCI, should not 185 be confused with similar terminology used for D-PHY’s operation; they are not related. 

- 186 Typically, there is a dedicated CCI interface between the transmitter and the receiver. 

- 187 CCI is a subset of the I2C protocol, including the minimum combination of obligatory features for I2C 188 slave devices specified in the I2C specification. Therefore, transmitters complying with the CCI 189 specification can also be connected to the system I2C bus. However, care must be taken so that I2C masters 190 do not try to utilize those I2C features that are not supported by CCI masters and CCI slaves 

- 191 Each CCI transmitter may have additional features to support I2C, but that is dependent on implementation. 192 Further details can be found on a particular device’s data sheet. 

- 193 This Specification does not attempt to define the contents of control messages sent by the CCI master. As 194 such, it is the responsibility of the CSI-2 implementer to define a set of control messages and corresponding 195 frame timing and I2C latency requirements, if any, that must be met by the CCI master when sending such 196 control messages to the CCI slave. 

- 197 The CCI defines an additional data protocol layer on top of I2C. The data protocol is presented in the 198 following sections. 

- 199 

## **6.1 Data Transfer Protocol** 

- 200 The data transfer protocol is according to I2C standard. The START, REPEATED START and STOP 201 conditions as well as data transfer protocol are specified in _The I_[2] _C Specification_ [NXP01]. 

## 202 **6.1.1 Message Type** 

- 203 A basic CCI message consists of START condition, slave address with read/write bit, acknowledge from 204 slave, sub address (index) for pointing at a register inside the slave device, acknowledge signal from slave, 205 in write operation data byte from master, acknowledge/negative acknowledge from slave and STOP 206 condition. In read operation data byte comes from slave and acknowledge/negative acknowledge from 207 master. This is illustrated in Figure 4. 

- 208 The slave address in the CCI is 7-bit. 

- 209 The CCI supports 8-bit index with 8-bit data or 16-bit index with 8-bit data. The slave device in question 210 defines what message type is used. 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

11 

Specification for CSI-2 

Version 1.3 29-May-2014 

Message type with 8-bit index and 8-bit data (7-bit address) 

|**S**|SLAVE<br>ADDRESS|R/<br>W|A|SUB<br>ADDRESS|A|DATA|A/<br>A|**P**|
|---|---|---|---|---|---|---|---|---|



INDEX[7:0] 

Message type with 16-bit index and 8-bit data (7-bit address) 

## 211 

|**S**|A<br>SLAVE<br>ADDRESS<br>R/<br>W<br>SUB ADDRESS|A<br>SUB ADDRESS|A|DATA|A/<br>A|**P**||
|---|---|---|---|---|---|---|---|
||INDEX[15:8]|INDEX[7:0]||||||
||From slave to master<br>S = START condition|||A = Acknowledge||||
||From master to slave<br>P = STOP condition|||A = Negative acknowledge||||
||Direction dependent on operation|||||||



## **Figure 4 CCI Message Types** 

## 212 **6.1.2 Read/Write Operations** 

- 213 The CCI compatible device shall be able to support four different read operations and two different write 214 operations; single read from random location, sequential read from random location, single read from 215 current location, sequential read from current location, single write to random location and sequential write 216 starting from random location. The read/write operations are presented in the following sections. 

- 217 The index in the slave device has to be auto incremented after each read/write operation. This is also 218 explained in the following sections. 

## 219 **6.1.2.1 Single Read from Random Location** 

220 In single read from random location the master does a dummy write operation to desired index, issues a 221 repeated start condition and then addresses the slave again with read operation. After acknowledging its 222 slave address, the slave starts to output data onto SDA line. This is illustrated in Figure 5. The master 223 terminates the read operation by setting a negative acknowledge and stop condition. 

224 

**==> picture [423 x 141] intentionally omitted <==**

**----- Start of picture text -----**<br>
Previous Index value, K Index M Index M +1<br>SLAVE  S  SLAVE<br>S 0 A SUB ADDRESS A 1 A DATA A P<br>ADDRESS r ADDRESS<br>INDEX, value M<br>From slave to master S = START condition A = Acknowledge Sr = REPEATED<br>START condition<br>From master to slave P = STOP condition A = Negative acknowledge<br>**----- End of picture text -----**<br>


**Figure 5 CCI Single Read from Random Location** 

Copyright © 2005-2014 MIPI Alliance, Inc. 

12 

All rights reserved. **Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

## 225 **6.1.2.2 Single Read from the Current Location** 

- 226 It is also possible to read from last used index by addressing the slave with read operation. The slave 227 responses by setting the data from last used index to SDA line. This is illustrated in Figure 6. The master 228 terminates the read operation by setting a negative acknowledge and stop condition. 

## 229 

**==> picture [430 x 133] intentionally omitted <==**

**----- Start of picture text -----**<br>
Previous Index value, K Index K+1 Index K +2<br>SLAVE  SLAVE<br>S 1 A DATA A P S 1 A DATA A P<br>ADDRESS ADDRESS<br>From slave to master S = START condition A = Acknowledge<br>From master to slave P = STOP condition A = Negative acknowledge<br>**----- End of picture text -----**<br>


## **Figure 6 CCI Single Read from Current Location** 

## 230 **6.1.2.3 Sequential Read Starting from a Random Location** 

- 231 The sequential read starting from a random location is illustrated in Figure 7. The master does a dummy 232 write to the desired index, issues a repeated start condition after an acknowledge from the slave and then 233 addresses the slave again with a read operation. If a master issues an acknowledge after received data it acts 234 as a signal to the slave that the read operation continues from the next index. When the master has read the 235 last data byte it issues a negative acknowledge and stop condition. 

236 

**==> picture [430 x 130] intentionally omitted <==**

**----- Start of picture text -----**<br>
Index Index<br>Previous Index value, K Index M<br>(M +L-1) M+L<br>SLAVE  SUB S  SLAVE<br>S 0 A A 1 A DATA A DATA A P<br>ADDRESS ADDRESS r ADDRESS<br>INDEX, value M L bytes of data<br>From slave to master S = START condition A = Acknowledge Sr = REPEATED<br>START condition<br>From master to slave P = STOP condition A = Negative acknowledge<br>**----- End of picture text -----**<br>


**Figure 7 CCI Sequential Read Starting from a Random Location** 

## 237 **6.1.2.4 Sequential Read Starting from the Current Location** 

- 238 A sequential read starting from the current location is similar to a sequential read from a random location. 239 The only exception is there is no dummy write operation. The command sequence is illustrated in Figure 8. 240 The master terminates the read operation by issuing a negative acknowledge and stop condition. 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

13 

Specification for CSI-2 

Version 1.3 

29-May-2014 

## 241 

**==> picture [381 x 145] intentionally omitted <==**

**----- Start of picture text -----**<br>
Index Index<br>Previous Index value, K Index K+1<br>(K +L-1) K+L<br>SLAVE<br>S 1 A DATA A DATA A DATA A P<br>ADDRESS<br>L bytes of data<br>From slave to master S = START condition A = Acknowledge<br>From master to slave P = STOP condition A = Negative acknowledge<br>**----- End of picture text -----**<br>


**Figure 8 CCI Sequential Read Starting from the Current Location** 

## 242 **6.1.2.5 Single Write to a Random Location** 

243 A write operation to a random location is illustrated in Figure 9. The master issues a write operation to the 244 slave then issues the index and data after the slave has acknowledged the write operation. The write 245 operation is terminated with a stop condition from the master. 

246 

**==> picture [353 x 141] intentionally omitted <==**

**----- Start of picture text -----**<br>
Previous Index value, K Index M Index M+1<br>SLAVE  SUB A/<br>S 0 A A DATA P<br>ADDRESS ADDRESS A<br>INDEX, value M<br>From slave to master S = START condition A = Acknowledge<br>From master to slave P = STOP condition A = Negative acknowledge<br>**----- End of picture text -----**<br>


**Figure 9 CCI Single Write to a Random Location** 

## 247 **6.1.2.6 Sequential Write** 

248 The sequential write operation is illustrated in Figure 10. The slave auto-increments the index after each 

249 data byte is received. The sequential write operation is terminated with a stop condition from the master. 

Copyright © 2005-2014 MIPI Alliance, Inc. 

14 

All rights reserved. 

**Confidential** 

Version 1.3 

Specification for CSI-2 

29-May-2014 

250 

|||Previous Index value, K|Previous Index value, K||Index M|Index<br>(M+L+1)||||Index<br>M+L|
|---|---|---|---|---|---|---|---|---|---|---|
||||||||||||
|**S**||SLAVE<br>ADDRESS|SUB<br>ADDRESS<br>0<br>A|A|DATA|DATA<br>A|A/<br>A||**P**||
||||INDEX, value M|||L bytes of data|||||
|||From slave to master<br>S = START condition||||A = Acknowledge|||||
|||From master to slave<br>P = STOP condition||||A = Negative acknowledge|||||



## **Figure 10 CCI Sequential Write Starting from a Random Location** 

## 251 **6.2 CCI Slave Addresses** 

- 252 For camera modules having only raw Bayer output the 7-bit slave address should be 011011Xb, where X = 253 0 or 1. For all other camera modules the 7-bit slave address should be 011110Xb. 

## 254 **6.3 CCI Multi-Byte Registers** 

## 255 **6.3.1 Overview** 

- 256 Peripherals contain a wide range of different register widths for various control and setup purposes. The 257 CSI-2 Specification supports the following register widths: 

- 258 • 8-bit – generic setup registers 

- 259 • 16-bit – parameters like line-length, frame-length and exposure values 

- 260 • 32-bit – high precision setup values 

- 261 • 64-bit – for needs of future sensors 

- 262 In general, the byte oriented access protocols described in the previous sections provide an efficient means 263 to access multi-byte registers. However, the registers should reside in a byte-oriented address space, and the 264 address of a multi-byte register should be the address of its first byte. Thus, addresses of contiguous multi265 byte registers will not be contiguous. For example, a 32-bit register with its first byte at address 0x8000 can 266 be read by means of a sequential read of four bytes, starting at random address 0x8000. If there is an 267 additional 4-byte register with its first byte at 0x8004, it could then be accessed using a four-byte 268 Sequential Read from the Current Location protocol. 

- 269 The motivation for a general multi-byte protocol rather than fixing the registers at 16-bits width is 270 flexibility. The protocol described in the following paragraphs provides a way of transferring 16-bit, 32-bit 271 or 64-bit values over a 16-bit index, 8-bit data, two-wire serial link while ensuring that the bytes of data 272 transferred for a multi-byte register value are always consistent (temporally coherent). 

- 273 Using this protocol a single CCI message can contain one, two or all of the different register widths used 274 within a device. 

- 275 The MS byte of a multi-byte register shall be located at the lowest address and the LS byte at the highest 276 address. 

- 277 The address of the first byte of a multi-byte register may, or may not be, aligned to the size of the register; 278 i.e., a multiple of the number of register bytes. The register alignment is an implementation choice between 279 processing optimized and bandwidth optimized organizations. There are no restrictions on the number or 280 mix of multi-byte registers within the available 64K by 8-bit index space, with the exception that rules for 281 the valid locations for the MS bytes and LS bytes of registers are followed. 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

15 

Specification for CSI-2 

Version 1.3 29-May-2014 

- 282 Partial access to multi-byte registers is not allowed. A multi-byte register shall only be accessed by a single 283 sequential message. When a multi-byte register is accessed, its first byte is accessed first; its second byte is 284 accessed second, etc. 

- 285 When a multi-byte register is accessed, the following re-timing rules must be followed: 

- 286 • For a Write operation, the updating of the register shall be deferred to a time when the last bit of 287 the last byte has been received 

- 288 • For a Read operation, the value read shall reflect the status of all bytes at the time that the first bit 289 of the first byte has been read 

- 290 Section 6.3.3 describes example behavior for the re-timing of multi-byte register accesses. 

- 291 Without re-timing, data may be corrupted as illustrated in Figure 11 and Figure 12. 

## Internal 32-bit Register Value (Locations M, M+1, M+2 and M+3) 

||||||||||||||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|292|0xFC FD FE FF|||||||0x01 02 03 04|||||||
|||||||||Register Values updated by internal logic|||||||
||Index M<br>Index<br>Register Index|||||||M+1<br>Index M+2<br>Index M+3<br> <br>(For example only)|||||||
||**S**|SLAVE<br>ADDRESS|1|A|DATA = 0xFC|A|DATA=0xFD||A|DATA=0x03|A|DATA=0x04||**P**|
||||||||||||||A||
||DATA[31:0]<br>From master to slave<br>From slave to master<br>S = START condition<br>P = STOP condition<br>A = Acknowledge<br>A = Negative acknowledge<br>_LS Data Byte_<br>_MS Data Byte_<br>0xFC<br>0x04<br>0xFD<br>0x03<br>DATA[31:24]<br>DATA[7:0]<br>DATA[23:16]<br>DATA[15:8]||||||||||||||



**Figure 11 Corruption of a 32-bit Wide Register during a Read Message** 

Copyright © 2005-2014 MIPI Alliance, Inc. 

16 

All rights reserved. 

**Confidential** 

Version 1.3 

Specification for CSI-2 

29-May-2014 

Internal 32-bit Register Value (Locations M, M+1, M+2 and M+3) 

293 

**==> picture [430 x 250] intentionally omitted <==**

**----- Start of picture text -----**<br>
0xFC FD FE FF 0x01 FD FE FF 0x01 02 FE FF 0x01 02 03 FF 0x01 02 03 04<br>Internal logic<br>reads register<br>value<br>(For example<br>Register Index only)<br>Index M Index M+1 Index M+2 Index M+3<br>SLAVE<br>S 0 A DATA=0x01 A DATA=0x02 A DATA=0x03 A DATA=0x04 A P<br>ADDRESS<br>MS Data Byte LS Data Byte<br>0x01 0x02 0x03 0x04<br>DATA[31:24] DATA[23:16] DATA[15:8] DATA[7:0]<br>DATA[31:0]<br>From slave to master S = START condition A = Acknowledge<br>From master to slave P = STOP condition A = Negative acknowledge<br>**----- End of picture text -----**<br>


**Figure 12 Corruption of a 32-bit Wide Register during a Write Message** 

294 **6.3.2 The Transmission Byte Order for Multi-byte Register Values** 

295 This is a normative section. 

296 The first byte of a CCI message is always the MS byte of a multi-byte register and the last byte is always 297 the LS byte. 

DATA[15:0] 

298 

|**S**|SLAVE<br>ADDRESS|0|A|SUB<br>ADDRESS<br>|A|DATA[15:8]|A|DATA[7:0]||**P**|
|---|---|---|---|---|---|---|---|---|---|---|
||||||||||A||
|_LS Data Byte_<br>_MS Data Byte_<br>_Index M_<br>_Index Value,_<br>_M_<br>_Index M+1_|||||||||||



**Figure 13 Example 16-bit Register Write** 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

17 

Specification for CSI-2 

Version 1.3 29-May-2014 

299 

**==> picture [329 x 144] intentionally omitted <==**

**----- Start of picture text -----**<br>
Register Index<br>Index M Index M+1 Index M+2 Index M+3<br>A/<br>A DATA A DATA A DATA A DATA<br>A<br>DATA[31:24] DATA[23:16] DATA[15:8] DATA[7:0]<br>DATA[31:0]<br>MS Data Byte LS Data Byte<br>**----- End of picture text -----**<br>


## **Figure 14 Example 32-bit Register Write (address not shown)** 

**==> picture [66 x 10] intentionally omitted <==**

**----- Start of picture text -----**<br>
Register Index<br>**----- End of picture text -----**<br>


## 300 

**==> picture [409 x 134] intentionally omitted <==**

**----- Start of picture text -----**<br>
Index M Index M+1 Index M+6 Index M+7<br>A/<br>A DATA A DATA A A DATA A DATA<br>A<br>DATA[63:56] DATA[55:48] DATA[15:8] DATA[7:0]<br>DATA[63:0]<br>MS Data Byte LS Data Byte<br>**----- End of picture text -----**<br>


## **Figure 15 Example 64-bit Register Write (address not shown)** 

## 301 **6.3.3 Multi-Byte Register Protocol** 

- 302 This is an informative section. 

- 303 Each device may have both single and multi-byte registers. Internally a device must understand what 304 addresses correspond to the different register widths. 

## 305 **6.3.3.1 Reading Multi-byte Registers** 

- 306 To ensure that the value read from a multi-byte register is consistent (i.e. all bytes are temporally coherent), 

- 307 the device internally transfers the contents of the register into a temporary buffer when the MS byte of the 

- 308 register is read. The contents of the temporary buffer are then output as a sequence of bytes on the SDA 309 line. Figure 16 and Figure 17 illustrate multi-byte register read operations. 

- 310 The temporary buffer is always updated unless the read operation is incremental within the same multi-byte 311 register. 

Copyright © 2005-2014 MIPI Alliance, Inc. 

18 

All rights reserved. **Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

## Internal 16-bit Register Value (Locations M and M+1) 

## 312 

|Internal 16-bit Register Value (Locations M and M+1)|Internal 16-bit Register Value (Locations M and M+1)|Internal 16-bit Register Value (Locations M and M+1)|Internal 16-bit Register Value (Locations M and M+1)|Internal 16-bit Register Value (Locations M and M+1)|Internal 16-bit Register Value (Locations M and M+1)|Internal 16-bit Register Value (Locations M and M+1)|Internal 16-bit Register Value (Locations M and M+1)|Internal 16-bit Register Value (Locations M and M+1)|Internal 16-bit Register Value (Locations M and M+1)|Internal 16-bit Register Value (Locations M and M+1)|Internal 16-bit Register Value (Locations M and M+1)|Internal 16-bit Register Value (Locations M and M+1)|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
||||||||||||||
|0xFC FD<br>0x01 02|||||||||||||
|Internal 16-bit Register Value (Locations M+2 and M+3)|||||||||||||
|0xFE FF<br>0x03 04<br>Register Values updated by internal logic|||||||||||||
|Register Index<br> <br>(For example only)|||||||||||||
|Index M<br>Index M+1<br>Index M+2<br>Index M+3|||||||||||||
|Temporary Buffer|||||||||||||
|0xFC FD<br>0x03 04<br>0x00 00|||||||||||||
||||||||||||||
|A read from MS byte of the register<br>causes the whole register value to<br>be transferred into a temporary<br>buffer<br>Incremental read within the same<br>multi-byte register.<br>Temporary Buffer not updated|||||||||||||
|**S**|SLAVE<br>ADDRESS|1|A|DATA = 0xFC|A|DATA=0xFD|A|DATA=0x03|A|DATA=0x04||**P**|
||||||||||||A||
|DATA[15:0]<br>From master to slave<br>From slave to master<br>S = START condition<br>P = STOP condition<br>A = Acknowledge<br>A = Negative acknowledge<br>_LS Data Byte_<br>_MS Data Byte_<br>0xFC<br>0x04<br>0xFD<br>0x03<br>DATA[7:0]<br>DATA[15:8]<br>DATA[7:0]<br>DATA[15:8]<br>DATA[15:0]<br>_LS Data Byte_<br>_MS Data Byte_|||||||||||||



## **Figure 16 Example 16-bit Register Read** 

- 313 In this definition there is no distinction made between whether the register is accessed incrementally via 314 separate, single byte read messages with no intervening data writes or via a single multi-location read 315 message. This protocol purely relates to the behavior of the index value. 

- 316 Examples of when the temporary buffer is updated are as follows: 

- 317 • The MS byte of a register is accessed 

- 318 • The index has crossed a multi-byte register boundary 

- 319 • Successive single byte reads from the same index location 

- 320 • The index value for the byte about to be read is the same or less than the previous index 

- 321 Unless the contents of a multi-byte register are accessed in an incremental manner the values read back are 322 not guaranteed to be consistent. 

- 323 The contents of the temporary buffer are reset to zero by START and STOP conditions. 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

19 

Specification for CSI-2 

Version 1.3 

29-May-2014 

## Internal 32-bit Register Value (Locations M, M+1, M+2 and M+3) 

## 324 

**==> picture [421 x 336] intentionally omitted <==**

**----- Start of picture text -----**<br>
0xFC FD FE FF 0x01 02 03 04<br>Register Values updated by internal logic<br>Register Index (For example only)<br>Index M Index M+1 Index M+2 Index M+3<br>Temporary Buffer<br>0x00 00 00 00 0xFC FD FE FF<br>A read from MS byte of the register  Incremental read within the same<br>causes the whole register value to  multi-byte register.<br>be transferred into a temporary  Temporary Buffer not updated<br>buffer<br>SLAVE<br>S 1 A DATA = 0xFC A DATA=0xFD A DATA=0xFE A DATA=0xFF A P<br>ADDRESS<br>MS Data Byte LS Data Byte<br>0xFC 0xFD 0xFE 0xFF<br>DATA[31:24] DATA[23:16] DATA[15:8] DATA[7:0]<br>DATA[31:0]<br>From slave to master S = START condition A = Acknowledge<br>From master to slave P = STOP condition A = Negative acknowledge<br>**----- End of picture text -----**<br>


## **Figure 17 Example 32-bit Register Read** 

## 325 **6.3.3.2 Writing Multi-byte Registers** 

- 326 To ensure that the value written is consistent, the bytes of data of a multi-byte register are written into a 327 temporary buffer. Only after the LS byte of the register is written is the full multi-byte value transferred 328 into the internal register location. 

- 329 Figure 18 and Figure 19 illustrate multi-byte register write operations. 

- 330 CCI messages that only write to the LS or MS byte of a multi-byte register are not allowed. Single byte 331 writes to a multi-byte register addresses may cause undesirable behavior in the device. 

Copyright © 2005-2014 MIPI Alliance, Inc. 

20 

All rights reserved. 

**Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

Internal 16-bit Register Value (Locations M and M+1) 

332 

**==> picture [430 x 335] intentionally omitted <==**

**----- Start of picture text -----**<br>
0xFC FD 0x01 02<br>Internal 16-bit Register Value (Locations M+2 and M+3)<br>0xFE FF 0x03 04<br>Register Index<br>Index M Index M+1 Index M+2 Index M+3<br>Temporary Buffer<br>0x00 00 0x01 00 0x00 00 0x03 00 0x00 00<br>A write to the LS byte of the<br>register causes the contents of the<br>temporary buffer to be transferred<br>onto the register location<br>SLAVE<br>S 0 A DATA=0x01 A DATA=0x02 A DATA=0x03 A DATA=0x04 A P<br>ADDRESS<br>MS Data Byte LS Data Byte MS Data Byte LS Data Byte<br>0x01 0x02 0x03 0x04<br>DATA[15:8] DATA[7:0] DATA[15:8] DATA[7:0]<br>DATA[15:0] DATA[15:0]<br>From slave to master S = START condition A = Acknowledge<br>From master to slave P = STOP condition A = Negative acknowledge<br>**----- End of picture text -----**<br>


**Figure 18 Example 16-bit Register Write** 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

21 

Specification for CSI-2 

Version 1.3 29-May-2014 

Internal 32-bit Register Value (Locations M, M+1, M+2 and  M+3) 

## 333 

|Internal 32-bit Register Value (Locations M, M+1, M+2 and  M+3)|Internal 32-bit Register Value (Locations M, M+1, M+2 and  M+3)|Internal 32-bit Register Value (Locations M, M+1, M+2 and  M+3)|Internal 32-bit Register Value (Locations M, M+1, M+2 and  M+3)|Internal 32-bit Register Value (Locations M, M+1, M+2 and  M+3)|Internal 32-bit Register Value (Locations M, M+1, M+2 and  M+3)|Internal 32-bit Register Value (Locations M, M+1, M+2 and  M+3)|Internal 32-bit Register Value (Locations M, M+1, M+2 and  M+3)|Internal 32-bit Register Value (Locations M, M+1, M+2 and  M+3)|Internal 32-bit Register Value (Locations M, M+1, M+2 and  M+3)|Internal 32-bit Register Value (Locations M, M+1, M+2 and  M+3)|Internal 32-bit Register Value (Locations M, M+1, M+2 and  M+3)|Internal 32-bit Register Value (Locations M, M+1, M+2 and  M+3)|Internal 32-bit Register Value (Locations M, M+1, M+2 and  M+3)|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|||||||||||||||
|0xFC FD FE FF|||||||||||0x01 02 03 04|||
|||||||||||||||
|Register Index||||||||||||||
|Index M|||||||Index M+1||Index M+2||Index M+3|||
|Temporary Buffer<br>0x00 00 00 00|||||||0x01 00 00 00|||||||
|||||||||||||||
|**S**|SLAVE<br>ADDRESS|0|A||DATA=0x01|A|DATA=0x02|A|DATA=0x03|A|DATA=0x04||**P**|
|||||||||||||A||
|||||||||||||||
|||||From master to slave<br>From slave to master<br>S = START condition<br>P = STOP condition<br>A = Acknowledge<br>A = Negative acknowledge<br>_LS Data Byte_<br>_MS Data Byte_<br>0x01<br>0x04<br>0x02<br>0x03<br>DATA[31:0]<br>DATA[31:24]<br>DATA[7:0]<br>DATA[23:16]<br>DATA[15:8]||||||||||
|||||||||||||||



## **Figure 19 Example 32-bit Register Write** 

## 334 **6.4 Electrical Specifications and Timing for I/O Stages** 

- 335 The electrical specification and timing for I/O stages conform to I[2] C Standard- and Fast-mode devices. 336 Information presented in Table 1 is from [NXP01]. 

## 337 

## **Table 1 CCI I/O Characteristics** 

|**Parameter**|**Symbol**|**Standard-mode**|**Standard-mode**|**Fast-mode**|**Fast-mode**|**Unit**|
|---|---|---|---|---|---|---|
|||**Min.**|**Max.**|**Min.**|**Max.**||
|LOW level input voltage|VIL|-0.5|0.3VDD|-0.5|0.3 VDD|V|
|HIGH level input voltage|VIH|0.7VDD|Note 1|0.7VDD|Note 1|V|
|Hysteresis of Schmitt trigger<br>inputs<br>VDD> 2V<br>VDD< 2V|VHYS|N/A<br>N/A|N/A<br>N/A|0.05VDD<br>0.1VDD|-<br>-|V|
|LOW level output voltage (open<br>drain) at 3mA sink current<br>VDD> 2V<br>VDD< 2V|VOL1<br>VOL3|0<br>N/A|0.4<br>N/A|0<br>0|0.4<br>0.2VDD|V|



Copyright © 2005-2014 MIPI Alliance, Inc. 

22 

All rights reserved. **Confidential** 

Version 1.3 

Specification for CSI-2 

29-May-2014 

|**Parameter**|**Symbol**|**Standard-mode**|**Standard-mode**|**Fast-mode**|**Fast-mode**|**Unit**|
|---|---|---|---|---|---|---|
|||**Min.**|**Max.**|**Min.**|**Max.**||
|HIGH level output voltage|VOH|N/A|N/A|0.8VDD||V|
|Output fall time from VIHminto<br>VILmaxwith bus capacitance from<br>10 pF to 400 pF|tOF|-|250|20+0.1CB<br>Note 2|250|ns|
|Pulse width of spikes which<br>shall be suppressed by the input<br>filter|tSP|N/A|N/A|0|50|ns|
|Input current each I/O pin with<br>an input voltage between 0.1<br>VDDand 0.9 VDD|II|-10|10|-10<br>Note 3|10<br>Note 3|μA|
|Input/Output capacitance (SDA)|CI/O|-|8|-|8|pF|
|Input capacitance (SCL)|CI|-|6|-|6|pF|



## _**Note:**_ 

_1. Maximum VIH = VDDmax + 0.5V_ 

_2. CB = capacitance of one bus line in pF_ 

_3. I/O pins of Fast-mode devices shall not obstruct the SDA and SCL line if VDD is switched off_ 

338 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

23 

Specification for CSI-2 

Version 1.3 

29-May-2014 

339 

**Table 2 CCI Timing Specification** 

|**Parameter**|**Symbol**|**Standard-mode**|**Standard-mode**|**Fast-mode**|**Fast-mode**|**Unit**|
|---|---|---|---|---|---|---|
|||**Min.**|**Max.**|**Min.**|**Max.**||
|SCL clock frequency|fSCL|0|100|0|400|kHz|
|Hold time (repeated) START<br>condition. After this period, the<br>first clock pulse is generated|tHD;STA|0.4|-|0.6|-|μs|
|LOW period of the SCL clock|tLOW|4.7|-|1.3|-|μs|
|HIGH period of the SCL clock|tHIGH|4.0|-|0.6|-|μs|
|Setup time for a repeated<br>START condition|tSU;STA|4.7|-|0.6|-|μs|
|Data hold time|tHD;DAT|0<br>Note 2|3.45<br>Note 3|0<br>Note 2|0.9<br>Note 3|μs|
|Data set-up time|tSU;DAT|250|-|100<br>Note 4|-|ns|
|Rise time of both SDA and SCL<br>signals|tR|-|1000|20+0.1CB<br>Note 5|300|ns|
|Fall time of both SDA and SCL<br>signals|tF|-|300|20+0.1CB<br>Note 5|300|ns|
|Set-up time for STOP condition|tSU;STO|4.0|-|0.6|-|μs|
|Bus free time between a STOP<br>and START condition|tBUF|4.7|-|1.3|-|μs|
|Capacitive load for each bus line|CB|-|400|-|400|pF|
|Noise margin at the LOW level<br>for each connected device<br>(including hysteresis)|VnL|0.1VDD|-|0.1VDD|-|V|
|Noise margin at the HIGH level<br>for each connected device<br>(including hysteresis)|VnH|0.2VDD|-|0.2VDD|-|V|



## _**Note:**_ 

_1. All values referred to VIHmin = 0.7VDD and VILmax = 0.3VDD_ 

_2. A device shall internally provide a hold time of at least 300 ns for the SDA signal (referred to the VIHmin of the SCL signal) to bridge the undefined region of the falling edge of SCL_ 

_3. The maximum tHD:DAT has only to be met if the device does not the LOW period (tLOW) of the SCL signal_ 

_4. A Fast-mode I2C-bus device can be used in a Standard-mode I2C-bus system, but the requirement tSU:DAT ≥ 250 ns shall be then met. This will be automatically the case if the device does not stretch the LOW period of the SCL signal. If such device does stretch the low period of SCL signal, it shall output the next data bit to the SDA line trMAX + tSU:DAT = 1000 + 250 = 1250 ns (according to the Standard-mode I2C bus specification) before the SCL line is released._ 

_5. CB = total capacitance of one bus line in pF._ 

340 

Copyright © 2005-2014 MIPI Alliance, Inc. 

24 

All rights reserved. **Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

341 The CCI timing is illustrated in Figure 20. 

**==> picture [466 x 206] intentionally omitted <==**

**----- Start of picture text -----**<br>
START Repeated-START STOP<br>tBUF<br>SDA<br>tR tF tSU;STA tSU;STO<br>tSU;DAT tHD;DAT tHD;STA<br>tLOW<br>SCL<br>tHIGH<br>tHD;STA<br>342  tSP<br>**----- End of picture text -----**<br>


**Figure 20 CCI Timing** 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

25 

Specification for CSI-2 

Version 1.3 29-May-2014 

## 343 **7 Physical Layer** 

- 344 The CSI-2 lane management layer interfaces with the D-PHY and/or C-PHY physical layers described in 345 [MIPI01] and [MIPI02], respectively. A device shall implement either the C-PHY 1.0 or the D-PHY 1.2 346 physical layer and may implement both. A practical constraint is that the PHY technologies used at both 347 ends of the Link need to match: a D-PHY transmitter cannot operate with a C-PHY receiver, or vice versa. 

## 348 **7.1 D-PHY Physical Layer Option** 

- 349 The D-PHY physical layer for a CSI-2 implementation is composed of a number of unidirectional data 

- 350 Lanes and one clock Lane. All CSI-2 transmitters and receivers implementing the D-PHY physical layer 

- 351 shall support continuous clock behavior on the Clock Lane, and optionally may support non-continuous 352 clock behavior. 

- 353 For continuous clock behavior the Clock Lane remains in high-speed mode, generating active clock signals 354 between the transmission of data packets. 

- 355 For non-continuous clock behavior the Clock Lane enters the LP-11 state between the transmission of data 356 packets. 

- 357 The minimum D-PHY physical layer requirement for a CSI-2 transmitter is 

- 358 • Data Lane Module: Unidirectional master, HS-TX, LP-TX and a CIL-MFEN function 

- 359 • Clock Lane Module: Unidirectional master, HS-TX, LP-TX and a CIL-MCNN function 

- 360 The minimum D-PHY physical layer requirement for a CSI-2 receiver is 

- 361 • Data Lane Module: Unidirectional slave, HS-RX, LP-RX, and a CIL-SFEN function 

- 362 • Clock Lane Module: Unidirectional slave, HS-RX, LP-RX, and a CIL-SCNN function 

- 363 All CSI-2 implementations supporting the D-PHY physical layer option shall support forward escape ULPS 364 on all D-PHY Data Lanes. 

- 365 To enable higher data rates and higher number of lanes the physical layer described in [MIPI01] includes an 

- 366 independent deskew mechanism in the Receive Data Lane Module. To facilitate deskew calibration at the 367 receiver the transmitter Data Lane Module provides a deskew sequence pattern. 

- 368 Since deskew calibration is only valid at a given transmit frequency: 

- 369 For initial calibration sequence the Transmitter shall be programmed with the desired frequency for 370 calibration. It will then transmit the deskew calibration pattern and the Receiver will autonomously detect 371 this pattern and tune the deskew function to achieve optimum performance. 

- 372 For any transmitter frequency changes the deskew calibration shall be rerun. 

- 373 Some transmitters and/or receiver may require deskew calibration to be rerun periodically and it is 374 suggested that it can be optimally done within vertical or frame blanking periods. 

- 375 For low transmit frequencies or when a receiver described in [MIPI01] is paired with a previous version 

- 376 transmitter not supporting the deskew calibration pattern the receiver may be instructed to bypass the 377 deskew mechanism. 

## 378 **7.2 C-PHY Physical Layer Option** 

- 379 The C-PHY physical layer for a CSI-2 implementation is composed of one or more unidirectional Lanes. 380 The minimum C-PHY physical layer requirement for a CSI-2 transmitter Lane module is: 

- 381 • Unidirectional master, HS-TX, LP-TX and a CIL-MFEN function 

- 382 • Support for Sync Word insertion during data payload transmission 

- 383 The minimum C-PHY physical layer requirement for a CSI-2 receiver Lane module is: 

Copyright © 2005-2014 MIPI Alliance, Inc. 

26 

All rights reserved. 

**Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

- 384 • Unidirectional slave, HS-RX, LP-RX, and a CIL-SFEN function 

- 385 • Support for Sync Word detection during data payload reception 

- 386 All CSI-2 implementations supporting the C-PHY physical layer option shall support forward escape ULPS 387 on all C-PHY Lanes. 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

27 

Specification for CSI-2 

Version 1.3 29-May-2014 

## 388 **8 Multi-Lane Distribution and Merging** 

- 389 CSI-2 is a Lane-scalable specification. Applications requiring more bandwidth than that provided by one 

- 390 data Lane, or those trying to avoid high clock rates, can expand the data path to a higher number of Lanes 391 and obtain approximately linear increases in peak bus bandwidth. The mapping between data at higher 392 layers and the serial bit or symbol stream is explicitly defined to ensure compatibility between host 393 processors and peripherals that make use of multiple data Lanes. 

- 394 Conceptually, between the PHY and higher functional layers is a layer that handles multi-Lane 395 configurations. As shown in Figure 21 and Figure 22 for the D-PHY and C-PHY physical layer options, 396 respectively, the CSI-2 transmitter incorporates a Lane Distribution Function (LDF) which accepts a 397 sequence of packet bytes from the low level protocol layer and distributes them across N Lanes, where each 398 Lane is an independent unit of physical-layer logic (serializers, etc.) and transmission circuitry. Similarly, 399 as shown in Figure 23 and Figure 24 for the D-PHY and C-PHY physical layer options, respectively, the 400 CSI-2 receiver incorporates a Lane Merging Function (LMF) which collects incoming bytes from N Lanes 401 and consolidates (merges) them into complete packets to pass into the packet decomposer in the receiver’s 402 low level protocol layer. 

|• • • •|• • • •||||||||||• • • •|• • • •|||||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Byte 5|||||||||||Byte 5||||||||
|Byte 4|||Byte Stream||||||||Byte 4||||||||
|Byte 3|||(Conceptual)||||||||Byte 3||||||||
|Byte 2|||||||||||Byte 2||||||||
|Byte 1|||||||||||Byte 1||||||||
|Byte 0|||||||||||Byte 0||||||||
||||||||||||||||||||
|LDF||||||||Lane Distribution Function (LDF)|||||||||||
|Byte 3|||||||||||||||||||
|Byte 2||||• • • •||||• • • •||||||• • • •|||• • • •||
|Byte 1||||Byte N||||Byte|N+1||• • • •|||Byte|2N-2||Byte|2N-1|
|Byte 0||||Byte 0||||Byte 1||||||Byte N-2|||Byte N-1||
||||||||||||||||||||
|SerDes||||SerDes||||SerDes|||• • • •|||SerDes|||SerDes||
||||||||||||||||||||
|Lane 1||||Lane 1||||Lane 2|||• • • •|||Lane N-1|||Lane N||
||||||||||||||||||||



Single Lane Link 

N Lane Link 

## **Figure 21 Conceptual Overview of the Lane Distributor Function for D-PHY** 

403 

Copyright © 2005-2014 MIPI Alliance, Inc. 

28 

All rights reserved. **Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

404 

**==> picture [357 x 346] intentionally omitted <==**

**----- Start of picture text -----**<br>
• • • • • • • •<br>Byte 5 Byte 5<br>Byte 4 Conceptual Byte Stream  Byte 4<br>Byte 3 From Low Level Protocol Byte 3<br>Byte 2 Byte 2<br>Byte 1 Byte 1<br>Byte 0 Byte 0<br>LDF Lane Distribution Function (LDF)<br>Byte 7<br>Byte 6<br>Byte 5<br>Byte 4 • • • • • • • • • • • • • • • •<br>Byte 3Byte 2 Byte 2N +1Byte 2N Byte 2N +3Byte 2N +2 • • • Byte 4N -3Byte 4N -4 Byte 4N -1Byte 4N -2<br>Byte 1 Byte 1 Byte 3 Byte 2N -3 Byte 2N -1<br>Byte 0 Byte 0 Byte 2 Byte 2N -4 Byte 2N -2<br>SerDes SerDes SerDes • • • SerDes SerDes<br>Lane 1 Lane 1 Lane 2 Lane N-1 Lane N<br>• • •<br>N  Lane Link<br>Single Lane Link<br>**----- End of picture text -----**<br>


**Figure 22 Conceptual Overview of the Lane Distributor Function for C-PHY** 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

29 

Specification for CSI-2 

Version 1.3 29-May-2014 

405 

|Single Lane|Single Lane|Single Lane|Single Lane|||||||||||||||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||Link||||||||||N Lane Link|||||||||
||Lane 1||||Lane 1||||Lane 2|||• • • •|||Lane N-1|||Lane N||
|||||||||||||||||||||
||SerDes||||SerDes||||SerDes|||• • • •|||SerDes|||SerDes||
|||||||||||||||||||||
||• • • •||||• • • •||||• • • •||||||• • • •|||• • • •||
||Byte 3||||Byte N||||Byte|N+1||• • • •|||Byte|2N-2||Byte|2N-1|
||Byte 2||||Byte 0||||Byte 1||||||Byte N-2|||Byte N-1||
||Byte 1|||||||||||||||||||
||Byte 0||||||||Lane Merging Function (LMF)|||||||||||
|||||||||||||||||||||
||LMF|||||||||||• • • •||||||||
||Byte 5|||||||||||Byte 5||||||||
||Byte 4|||Byte Stream||||||||Byte 4||||||||
||Byte 3|||(Conceptual)||||||||Byte 3||||||||
||Byte 2|||||||||||Byte 2||||||||
||Byte 1|||||||||||Byte 1||||||||
||Byte 0|||||||||||Byte 0||||||||



**Figure 23 Conceptual Overview of the Lane Merging Function for D-PHY** 

Copyright © 2005-2014 MIPI Alliance, Inc. 

30 

All rights reserved. **Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

## Single Lane Link 

## N Lane Link 

406 

**==> picture [358 x 331] intentionally omitted <==**

**----- Start of picture text -----**<br>
• • •<br>Lane 1 Lane 1 Lane 2 Lane N-1 Lane N<br>SerDes SerDes SerDes • • •  SerDes SerDes<br>• • • • • • • • • • • • • • • • • • • •<br>Byte 7 Byte 2N +1 Byte 2N +3 • • •  Byte 4N -3 Byte 4N -1<br>Byte 6 Byte 2N Byte 2N +2 Byte 4N -4 Byte 4N -2<br>Byte 5 Byte 1 Byte 3 Byte 2N -3 Byte 2N -1<br>Byte 4 Byte 0 Byte 2 Byte 2N -4 Byte 2N -2<br>Byte 3<br>Byte 2<br>Byte 1<br>Lane Merging Function (LMF)<br>Byte 0<br>LMF • • • •<br>Byte 5 Byte 5<br>Byte 4 Conceptual Byte Stream  Byte 4<br>To Low Level Protocol<br>Byte 3 Byte 3<br>Byte 2 Byte 2<br>Byte 1 Byte 1<br>Byte 0 Byte 0<br>**----- End of picture text -----**<br>


## **Figure 24 Conceptual Overview of the Lane Merging Function for C-PHY** 

- 407 The Lane distributor takes a transmission of arbitrary byte length, buffers up N*b bytes (where N = number 408 of Lanes and b = 1 or 2 for the D-PHY or C-PHY physical layer option, respectively), and then sends 409 groups of N*b bytes in parallel across N Lanes with each Lane receiving b bytes. Before sending data, all 410 Lanes perform the SoT sequence in parallel to indicate to their corresponding receiving units that the first 411 byte of a packet is beginning. After SoT, the Lanes send groups of successive bytes from the first packet in 412 parallel, following a round-robin process. 

## 413 **8.1 Lane Distribution for the D-PHY Physical Layer Option** 

- 414 Examples are shown in Figure 25, Figure 26, Figure 27, and Figure 28: 

- 415 • 2-Lane system (Figure 25): byte 0 of the packet goes to Lane 1, byte 1 goes to Lane 2, byte 2 to 416 Lane 1, byte 3 goes to Lane 2, byte 4 goes to Lane 1, and so on. 

- 417 • 3-Lane system (Figure 26): byte 0 of the packet goes to Lane 1, byte 1 goes to Lane 2, byte 2 to 418 Lane 3, byte 3 goes to Lane 1, byte 4 goes to Lane 2, and so on. 

- 419 • N-Lane system (Figure 27): byte 0 of the packet goes to Lane 1, byte 1 goes to Lane 2, byte N-1 420 goes to Lane N, byte N goes to Lane 1, byte N+1 goes to Lane 2, and so on. 

- 421 • N-lane system (Figure 28) with N>4 short packet (4 bytes) transmission: byte 0 of the packet goes 422 to Lane 1, byte 1 goes to Lane 2, byte 2 goes to Lane 3, byte 3 goes to Lane 4, and Lanes 5 to N 423 do not receive bytes and stay in LPS state. 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

31 

Specification for CSI-2 

Version 1.3 29-May-2014 

- 424 At the end of the transmission, there may be “extra” bytes since the total byte count may not be an integer 425 multiple of the number of Lanes, N. One or more Lanes may send their last bytes before the others. The 426 Lane distributor, as it buffers up the final set of less-than-N bytes in parallel for sending to N data Lanes, 427 de-asserts its “valid data” signal into all Lanes for which there is no further data. For systems with more 428 than 4 data Lanes sending a short packet constituted of 4 bytes the Lanes which do not receive a byte for 429 transmission shall stay in LPS state. 

- 430 Each D-PHY data Lane operates autonomously. 

- 431 Although multiple Lanes all start simultaneously with parallel “start packet” codes, they may complete the 432 transaction at different times, sending “end packet” codes one cycle (byte) apart. 

- 433 The N PHYs on the receiving end of the link collect bytes in parallel, and feed them into the Lane-merging 434 layer. This reconstitutes the original sequence of bytes in the transmission, which can then be partitioned 435 into individual packets for the packet decoder layer. 

## **Number of Bytes, B, transmitted is an integer multiple of the number of lanes:** 

|||||||||||All Data Lanes finish at the same time|All Data Lanes finish at the same time||
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**LANE**|**1:**|SoT|Byte 0||Byte 2||Byte 4<br>Byte B-6<br>Byte B-4<br>Byte B-2||||EoT||
|**LANE**|**2:**|SoT|Byte 1||Byte 3||Byte 5<br>Byte B-5<br>Byte B-3<br>Byte B-1||||EoT||



## **Number of Bytes, B, transmitted is NOT an integer multiple of the number of lanes:** 

**==> picture [457 x 121] intentionally omitted <==**

**----- Start of picture text -----**<br>
Data Lane 2 finishes 1 byte earlier than Data Lane 1<br>LANE 1: SoT Byte 0 Byte 2 Byte 4 Byte B-5 Byte B-3 Byte B-1 EoT<br>LANE 2: SoT Byte 1 Byte 3 Byte 5 Byte B-4 Byte B-2 EoT LPS<br>KEY :<br>LPS – Low Power State SoT – Start of Transmission EoT – End of Transmission<br>436<br>**----- End of picture text -----**<br>


**==> picture [243 x 11] intentionally omitted <==**

**----- Start of picture text -----**<br>
Figure 25 Two Lane Multi-Lane Example for D-PHY<br>**----- End of picture text -----**<br>


Copyright © 2005-2014 MIPI Alliance, Inc. 

32 

All rights reserved. 

**Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

## **Number of Bytes, B, transmitted is an integer multiple of the number of lanes:** 

**==> picture [410 x 131] intentionally omitted <==**

**----- Start of picture text -----**<br>
All Data Lanes finish at the same time<br>LANE 1: SoT Byte 0 Byte 3 Byte 6 Byte B-9 Byte B-6 Byte B-3 EoT<br>LANE 2: SoT Byte 1 Byte 4 Byte 7 Byte B-8 Byte B-5 Byte B-2 EoT<br>LANE 3: SoT Byte 2 Byte 5 Byte 8 Byte B-7 Byte B-4 Byte B-1 EoT<br>**----- End of picture text -----**<br>


**==> picture [424 x 151] intentionally omitted <==**

**----- Start of picture text -----**<br>
Number of Bytes, B, transmitted is NOT an integer multiple of the number of lanes (Example 1):<br>Data Lanes 2 & 3  finish 1 byte earlier than Data Lane 1<br>LANE 1: SoT Byte 0 Byte 3 Byte 6 Byte B-7 Byte B-4 Byte B-1 EoT<br>LANE 2: SoT Byte 1 Byte 4 Byte 7 Byte B-6 Byte B-3 EoT LPS<br>LANE 3: SoT Byte 2 Byte 5 Byte 8 Byte B-5 Byte B-2 EoT LPS<br>**----- End of picture text -----**<br>


**Number of Bytes, B, transmitted is NOT an integer multiple of the number of lanes (Example 2):** 

**==> picture [20 x 9] intentionally omitted <==**

**----- Start of picture text -----**<br>
437<br>**----- End of picture text -----**<br>


**==> picture [412 x 163] intentionally omitted <==**

**----- Start of picture text -----**<br>
Data Lane 3 finishes 1 byte earlier than Data Lanes 1 & 2<br>LANE 1: SoT Byte 0 Byte 3 Byte 6 Byte B-8 Byte B-5 Byte B-2 EoT<br>LANE 2: SoT Byte 1 Byte 4 Byte 7 Byte B-7 Byte B-4 Byte B-1 EoT<br>LANE 3: SoT Byte 2 Byte 5 Byte 8 Byte B-6 Byte B-3 EoT LPS<br>KEY :<br>LPS – Low Power State SoT – Start of Transmission EoT – End of Transmission<br>**----- End of picture text -----**<br>


**==> picture [251 x 10] intentionally omitted <==**

**----- Start of picture text -----**<br>
Figure 26 Three Lane Multi-Lane Example for D-PHY<br>**----- End of picture text -----**<br>


Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

33 

Specification for CSI-2 

Version 1.3 

29-May-2014 

## **Number of Bytes, B, transmitted is an integer multiple of the number of lanes, N:** 

**==> picture [408 x 177] intentionally omitted <==**

**----- Start of picture text -----**<br>
All Data Lanes finish at the same time<br>LANE 1: SoT Byte 0 Byte N Byte B-2N Byte B-N EoT<br>LANE 2: SoT Byte 1 Byte N+1 Byte B-2N+1 Byte B-N+1 EoT<br>LANE N-1: SoT Byte N-2 Byte 2N-2 Byte B-N-2 Byte B-2 EoT<br>LANE N: SoT Byte N-1 Byte 2N-1 Byte B-N-1 Byte B-1 EoT<br>• • • • • • • • • • • • • • •<br>**----- End of picture text -----**<br>


**==> picture [429 x 16] intentionally omitted <==**

**----- Start of picture text -----**<br>
Number of Bytes, B, transmitted is NOT an integer multiple of the number of lanes, N:<br>**----- End of picture text -----**<br>


**==> picture [412 x 175] intentionally omitted <==**

**----- Start of picture text -----**<br>
Data Lanes K+1 to N finish 1 byte earlier than Data Lanes 1 to K<br>LANE 1: SoT Byte 0 Byte N Byte B-N-K Byte B-K EoT<br>LANE K: SoT Byte K-1 Byte N+K-1 Byte B-N-1 Byte B-1 EoT<br>LANE K+1: SoT Byte K Byte N+K Byte B-N EoT LPS<br>LANE N: SoT Byte N-1 Byte 2N-1 Byte B-K-1 EoT LPS<br>• • • • • • • • • • • • • • •<br>• • • • • • • • • • • • • • •<br>**----- End of picture text -----**<br>


438 

**==> picture [387 x 19] intentionally omitted <==**

**----- Start of picture text -----**<br>
KEY :<br>LPS – Low Power State SoT – Start of Transmission EoT – End of Transmission<br>**----- End of picture text -----**<br>


**Figure 27 N-Lane Multi-Lane Example for D-PHY** 

Copyright © 2005-2014 MIPI Alliance, Inc. 

34 

All rights reserved. **Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

## 439 

**==> picture [418 x 254] intentionally omitted <==**

**----- Start of picture text -----**<br>
Short packet of 4 bytes Transmitted on N lanes > 4<br>Bytes distributed on Lanes 1 to 4,<br>Lanes 5 to N stay in LPS<br>LANE 1: SoT Byte 0 EoT LPS<br>LANE 4: SoT Byte 3 EoT LPS<br>LANE 5: LPS<br>LPS<br>LANE N:<br>KEY :<br>LPS – Low Power State SoT – Start of Transmission EoT – End of Transmission<br>• • •<br>• • •<br>**----- End of picture text -----**<br>


## **Figure 28 N-Lane Multi-Lane Example for D-PHY Short Packet Transmission** 

## 440 **8.2 Lane Distribution for the C-PHY Physical Layer Option** 

- 441 Examples are shown in Figure 29 and Figure 30: 

- 442 • 2-Lane system (Figure 29): bytes 1 and 0 of the packet are sent as a 16-bit word to the Lane 1 C- 443 PHY module, bytes 3 and 2 are sent to Lane 2, bytes 5 and 4 are sent to Lane 1, bytes 7 and 6 are 444 sent to Lane 2, bytes 9 and 8 are sent to Lane 1, and so on. 

- 445 • 3-Lane system (Figure 30): bytes 1 and 0 of the packet are sent as a 16-bit word to the Lane 1 C- 446 PHY module, bytes 3 and 2 are sent to Lane 2, bytes 5 and 4 are sent to Lane 3, bytes 7 and 6 are 447 sent to Lane 1, bytes 9 and 8 are sent to Lane 2, and so on. 

- 448 Figure 31 illustrates normative behavior for an N-Lane system where N ≥ 1: bytes 1 and 0 of the packet are 449 sent as a 16-bit word to the Lane 1 C-PHY module, bytes 3 and 2 are sent to Lane 2, bytes 2N-1 and 2N-2 450 are sent to Lane N, bytes 2N+1 and 2N are sent to Lane 1, and so on. The last two bytes B-1 and B-2 are 451 sent to Lane N, where B is the total number of bytes in the packet. 

- 452 For an N-Lane transmitter, the C-PHY module for Lane n (1 ≤ n ≤ N) shall transmit the following 453 sequence of {ms byte : ls byte} byte pairs from a B-byte packet generated by the low level protocol layer: 454 {Byte 2*(k*N+n)-1 : Byte 2*(k*N+n)-2}, for k = 0, 1, 2, …, B/(2N) - 1, where Byte 0 is the first byte in 455 the packet. The low level protocol shall guarantee that B is an integer multiple of 2N. 

- 456 That is, at the end of the packet transmission, there shall be no “extra” bytes since the total byte count is 457 always an even multiple of the number of Lanes, N.  The Lane distributor, after sending the final set of 2N 458 bytes in parallel to the N Lanes, simultaneously de-asserts its “valid data” signal to all Lanes, signaling to 459 each C-PHY Lane module that it may start its EoT sequence. 

- 460 Each C-PHY Lane module operates autonomously, but packet data transmission starts and stops at the same 461 time on all Lanes. 

- 462 The N C-PHY receiver modules on the receiving end of the link collect byte pairs in parallel, and feed them 463 into the Lane-merging layer. This reconstitutes the original sequence of bytes in the transmission, which 464 can then be partitioned into individual packets for the packet decoder layers. 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

35 

Specification for CSI-2 

Version 1.3 

29-May-2014 

**==> picture [455 x 120] intentionally omitted <==**

**----- Start of picture text -----**<br>
All Lanes start and stop at the same time<br>LANE 1: SoT Bytes 1:0 Bytes 5:4 Bytes 9:8 Bytes B-11:B-12 Bytes B-7:B-8 Bytes B-3:B-4 EoT<br>LANE 2: SoT Bytes 3:2 Bytes 7:6 Bytes 11:10 Bytes B-9:B-10 Bytes B-5:B-6 Bytes B-1:B-2 EoT<br>KEY :<br>LPS – Low Power State SoT – Start of Transmission EoT – End of Transmission<br>465<br>**----- End of picture text -----**<br>


**Figure 29 Two Lane Multi-Lane Example for C-PHY** 

**==> picture [456 x 164] intentionally omitted <==**

**----- Start of picture text -----**<br>
All Lanes start and stop at the same time<br>LANE 1: SoT Bytes 1:0 Bytes 7:6 Bytes 13:12 Bytes B-17:B-18 Bytes B-11:B-12 Bytes B-5:B-6 EoT<br>LANE 2: SoT Bytes 3:2 Bytes 9:8 Bytes 15:14 Bytes B-15:B-16 Bytes B-9:B-10 Bytes B-3:B-4 EoT<br>LANE 3: SoT Bytes 5:4 Bytes 11:10 Bytes 17:16 Bytes B-13:B-14 Bytes B-7:B-8 Bytes B-1:B-2 EoT<br>KEY :<br>LPS – Low Power State SoT – Start of Transmission EoT – End of Transmission<br>466<br>**----- End of picture text -----**<br>


## **Figure 30 Three Lane Multi-Lane Example for C-PHY** 

**==> picture [456 x 206] intentionally omitted <==**

**----- Start of picture text -----**<br>
All Lanes start and stop at the same time<br>LANE 1: SoT Bytes 1:0 Bytes 2N+1:2N Bytes 4N+1:4N Bytes B-6N+1:B-6N Bytes B-4N+1:B-4N Bytes B-2N+1:B-2N EoT<br>LANE 2: SoT Bytes 3:2 Bytes 2N+3:2N+2 Bytes 4N+3:4N+2 Bytes B-6N+3:B-6N+2 Bytes B-4N+3:B-4N+2 Bytes B-2N+3:B-2N+2 EoT<br>LANE N-1: SoT Bytes 2N-3:2N-4 Bytes 4N-3:4N-4 Bytes 6N-3:6N-4 Bytes B-4N-3:B-4N-4 Bytes B-2N-3:B-2N-4 Bytes B-3:B-4 EoT<br>LANE N: SoT Bytes 2N-1:2N-2 Bytes 4N-1:4N-2 Bytes 6N-1:6N-2 Bytes B-4N-1:B-4N-2 Bytes B-2N-1:B-2N-2 Bytes B-1:B-2 EoT<br>KEY :<br>LPS – Low Power State SoT – Start of Transmission EoT – End of Transmission<br>467<br>• • • • • • • • • • • • • • • • • •<br>**----- End of picture text -----**<br>


**Figure 31 General N-Lane Multi-Lane Distribution for C-PHY** 

## 468 **8.3 Multi-Lane Interoperability** 

469 The Lane distribution and merging layers shall be reconfigurable via the Camera Control Interface when 470 more than one data Lane is used. 

Copyright © 2005-2014 MIPI Alliance, Inc. 

36 

All rights reserved. **Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

471 An "N" data Lane receiver shall be connected with an "M" data Lane transmitter, by CCI configuration of 472 the Lane distribution and merging layers within the CSI-2 transmitter and receiver when more than one data 473 Lane is used. Thus, if M<=N a receiver with N data Lanes shall work with transmitters with M data Lanes. 474 Likewise, if M>=N a transmitter with M Lanes shall work with receivers with N data Lanes. Transmitter 475 Lanes 1 to M shall be connected to the receiver Lanes 1 to N. 

476 Two cases: 

- 477 • If M<=N then there is no loss of performance – the receiver has sufficient data Lanes to match the 478 transmitter (Figure 32 and Figure 33). 

- 479 • If M> N then there may be a loss of performance (e.g. frame rate) as the receiver has fewer data 480 Lanes than the transmitter (Figure 34 and Figure 35). 

- 481 • Note that while the examples shown are for the D-PHY physical layer option, the C-PHY physical 482 layer option is handled similarly, except there is no clock Lane. 

483 

484 

**==> picture [393 x 355] intentionally omitted <==**

**----- Start of picture text -----**<br>
1 lane N lane<br>Transmitter PHY Receiver PHY<br>SerDes 8-bit<br>8-bit SerDes Lane 1 SerDes 8-bit<br>Clock DDR Clock Clock<br>Byte  Byte<br>Clock Clock<br>Figure 32 One Lane Transmitter and N-Lane Receiver Example for D-PHY<br>M lane N lane<br>Transmitter PHY Receiver  PHY<br>SerDes 8-bit<br>8-bit SerDes Lane M SerDes 8-bit<br>8-bit SerDes Lane 1 SerDes 8-bit<br>Clock DDR Clock Clock<br>Byte  Byte<br>Clock Clock<br>• • • • • • • • •<br>Lane Merging Function<br>Lane Distribution Function<br>• • • • • • • • •<br>• • • • • • • • • • • • • • • • • • • • •<br>Lane Merging Function<br>Lane Distribution Function<br>**----- End of picture text -----**<br>


**Figure 33 M-Lane Transmitter and N-Lane Receiver Example (M<N) for D-PHY** 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

37 

Specification for CSI-2 

Version 1.3 29-May-2014 

485 

486 

**==> picture [393 x 363] intentionally omitted <==**

**----- Start of picture text -----**<br>
M lane 1 lane<br>Transmitter PHY Receiver  PHY<br>8-bit SerDes<br>8-bit SerDes Lane 1 SerDes 8-bit<br>Clock DDR Clock Clock<br>Byte  Byte<br>Clock Clock<br>Figure 34 M-Lane Transmitter and One Lane Receiver Example for D-PHY<br>M lane N lane<br>Transmitter PHY Receiver  PHY<br>8-bit SerDes<br>8-bit SerDes Lane N SerDes 8-bit<br>8-bit SerDes Lane 1 SerDes 8-bit<br>Clock DDR Clock Clock<br>Byte  Byte<br>Clock Clock<br>• • • • • • • • •<br>Lane Merging Function<br>Lane Distribution Function<br>• • • • • • • • •<br>• • • • • • • • • • • • • • • • • • • • •<br>Lane Merging Function<br>Lane Distribution Function<br>**----- End of picture text -----**<br>


**Figure 35 M-Lane Transmitter and N-Lane Receiver Example (N<M) for D-PHY** 

Copyright © 2005-2014 MIPI Alliance, Inc. 

38 

All rights reserved. **Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

## 487 **9 Low Level Protocol** 

- 488 The Low Level Protocol (LLP) is a byte orientated, packet based protocol that supports the transport of 489 arbitrary data using Short and Long packet formats. For simplicity, all examples in this section are single 490 Lane configurations unless specified otherwise. 

- 491 Low Level Protocol Features: 

- 492 • Transport of arbitrary data (Payload independent) 

- 493 • 8-bit word size 

- 494 • Support for up to four interleaved virtual channels on the same link 

- 495 • Special packets for frame start, frame end, line start and line end information 

- 496 • Descriptor for the type, pixel depth and format of the Application Specific Payload data 

- 497 • 16-bit Checksum Code for error detection. 

- 498 • 8-bit Error Correction Code for error detection and correction (D-PHY physical layer only) 

## **DATA** : 

499 

**==> picture [409 x 100] intentionally omitted <==**

**----- Start of picture text -----**<br>
Short  Long  Long  Short<br>Packet Packet Packet Packet<br>ST SP ET LPS ST PH DATA PF ET LPS ST PH DATA PF ET LPS ST SP ET<br>KEY :<br>LPS – Low Power State PH – Packet Header<br>ET – End of Transmission PF – Packet Footer + Filler (if applicable)<br>ST – Start of Transmission<br>**----- End of picture text -----**<br>


## **Figure 36 Low Level Protocol Packet Overview** 

## 500 **9.1 Low Level Protocol Packet Format** 

- 501 As shown in Figure 36, two packet structures are defined for low-level protocol communication: Long 502 packets and Short packets. The format and length of Short and Long Packets depends on the choice of 503 physical layer. For each packet structure, exit from the low power state followed by the Start of 504 Transmission (SoT) sequence indicates the start of the packet. The End of Transmission (EoT) sequence 505 followed by the low power state indicates the end of the packet. 

## 506 **9.1.1 Low Level Protocol Long Packet Format** 

- 507 Figure 37 shows the structure of the Low Level Protocol Long Packet for the D-PHY physical layer option. 508 A Long Packet shall be identified by Data Types 0x10 to 0x37. See Table 3 for a description of the Data 509 Types. A Long Packet for the D-PHY physical layer option shall consist of three elements: a 32-bit Packet 510 Header (PH), an application specific Data Payload with a variable number of 8-bit data words, and a 16-bit 511 Packet Footer (PF). The Packet Header is further composed of three elements: an 8-bit Data Identifier, a 16512 bit Word Count field and an 8-bit ECC. The Packet footer has one element, a 16-bit checksum (CRC). See 513 Section 9.2 through Section 9.5 for further descriptions of the packet elements. 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

39 

Specification for CSI-2 

Version 1.3 29-May-2014 

## **DATA IDENTIFIER (DI):** 

Contains the Virtual Channel Identifier and the Data Type Information Data Type denotes the format/content of the Application Specific Payload Data. Used by the application specific layer. 

## **16-bit WORD COUNT (WC):** 

The receiver reads the next WC data words independent of their values. The receiver is NOT looking for any embedded sync sequences within the payload data. The receiver uses the WC value to determine the end End of the Packet 

## **8-bit Error Correction Code (ECC) for the Packet Header:** 

8-bit ECC code for the Packet Header. Allows 1-bit errors with the packet header to be corrected and 2-bit errors to be detected 

514 

**APPLICATION SPECIFIC PAYLOAD CHECKSUM/CRC (CS)** LPS SoT EoT LPS **32-bit PACKET DATA: 16-bit PACKET** Length = Word Count (WC) * Data Word **PACKET HEADER** Width (8-bits). There are NO restrictions **FOOTER (PH)** on the values of the data words **(PF)** 

**Figure 37 Long Packet Structure for D-PHY Physical Layer Option** 

515 Figure 38 shows the Long Packet structure for the C-PHY physical layer option; it shall consist of four 516 elements: a Packet Header (PH), an application specific Data Payload with a variable number of 8-bit data 517 words, a 16-bit Packet Footer (PF), and zero or more Filler bytes (FILLER). The Packet Header is 6N x 16518 bits long, where N is the number of C-PHY physical layer Lanes. As shown in Figure 38, the Packet Header 519 consists of two identical 6N-byte halves, where each half consists of N sequential copies of each of the 520 following fields: a 16-bit field containing eight Reserved bits plus the 8-bit Data Identifier (DI); the 16-bit 521 Packet Data Word Count (WC); and a 16-bit Packet Header checksum (PH-CRC) which is computed over 522 the previous four bytes. The value of each Reserved bit shall be zero. The Packet Footer consists of a 16-bit 523 checksum (CRC) computed over the Packet Data using the same CRC polynomial as the Packet Header 524 CRC and the Packet Footer used in the D-PHY physical layer option. Packet Filler bytes are inserted after 525 the Packet Footer, if needed, to ensure that the Packet Footer ends on a 16-bit word boundary and that each 526 C-PHY physical layer Lane transports the same number of 16-bit words (i.e. byte pairs). 

Copyright © 2005-2014 MIPI Alliance, Inc. 

40 

All rights reserved. 

**Confidential** 

Version 1.3 

Specification for CSI-2 

29-May-2014 

527 

**==> picture [431 x 208] intentionally omitted <==**

**----- Start of picture text -----**<br>
8-bit DATA IDENTIFIER (DI):<br>Contains the Virtual Channel Identifier and the Data Type Information;<br>Data Type denotes the format/content of the Application Specific Payload Data.<br>Used by the application specific layer.<br>16-bit WORD COUNT (WC):<br>The receiver reads the next WC 8-bit data words following the Packet Header.<br>The receiver uses the WC value to determine the end of the Packet Payload.<br>16-bit Cyclic Redundancy Check Code (PH-CRC):<br>16-bit CRC code for the Packet Header; computed over the<br>Reserved, Data ID, and Word Count fields (4 bytes). Enables<br>multi-bit errors to be detected. 16-Bit Packet Data CRC:<br>Computed over WC<br>CSI-2 “Insert Sync Word” PPI Command: Packet Data Words<br>The physical layer simultaneously inserts an Sync Word on all N<br>Set to  Lanes at this point as a result of executing a CSI-2 PPI command. Set to  Set to<br>“0” “0” “0”<br>WC PH-CRC APPLICATION SPECIFIC PAYLOAD<br>LPS SoT EoT LPS<br>N Copies N Copies N Copies N Copies N Copies N Copies PACKET DATA: 16-bit  FILLER:<br>Length = Word Count (WC) * Data Word  PACKET  FC 8-bit bytes added to<br>PACKET HEADER (PH): 6N x 16-bits Width (8-bits). There are NO restrictions  FOOTER  ensure that all Lanes<br>(N = Physical Layer Lane Count) on the values of the data words (PF) transport the same number of<br>16-bit words; FC may be 0.<br>Reserved Data ID 16-Bit Word Count (l.s. byte first) 16-Bit PH Checksum (l.s. byte first) Reserved Data ID 16-Bit Word Count (l.s. byte first) 16-Bit PH Checksum (l.s. byte first) Data 0 Data 1 Data 2 Data 3 Data WC-4 Data WC-3 Data WC-2 Data WC-1 16-Bit PD Checksum (l.s. byte first) Filler 0 Filler FC-1<br>**----- End of picture text -----**<br>


**Figure 38 Long Packet Structure for C-PHY Physical Layer Option** 

- 528 As shown in Figure 39, the Packet Header structure depicted in Figure 38 effectively results in the C-PHY 529 Lane Distributor broadcasting the same six 16-bit words to each of N Lanes. Furthermore, the six words per 530 Lane are split into two identical three-word groups which are separated by a mandatory C-PHY Sync Word 531 as described in [MIPI02]. The Sync Word is inserted by the C-PHY physical layer in response to a CSI-2 532 protocol transmitter PPI command. 

## ~~**16-BIT WORD TRANSMISSION ORDER TO C-PHY PHYSICAL LAYER**~~ 

**==> picture [467 x 104] intentionally omitted <==**

**----- Start of picture text -----**<br>
WORD 1 WORD 2 WORD 3 WORD 4 WORD 5 WORD 6<br>LANE 1: Data ID Reserved Word Count  Word Count  Checksum  Checksum  Data ID Reserved Word Count  Word Count  Checksum  Checksum<br>(MS Byte) (LS Byte) (MS Byte) (LS Byte) (MS Byte) (LS Byte) (MS Byte) (LS Byte)<br>ms bit ls bit ms bit ls bit<br>● ●<br>To Lane 1 C-PHY TX ● here on each Lane in response to a CSI-2 PPI commandC-PHY physical layer inserts a 7-symbol Sync Word  ● To Lane 1 C-PHY TX<br>● ●<br>LANE N: Data ID Reserved Word Count  Word Count  Checksum  Checksum  Data ID Reserved Word Count  Word Count  Checksum  Checksum<br>(MS Byte) (LS Byte) (MS Byte) (LS Byte) (MS Byte) (LS Byte) (MS Byte) (LS Byte)<br>ms bit ls bit ms bit ls bit<br>533  To Lane N C-PHY TX To Lane N C-PHY TX<br>**----- End of picture text -----**<br>


## **Figure 39 Packet Header Lane Distribution for C-PHY Physical Layer Option** 

- 534 For both physical layer options, the 8-bit Data Identifier field defines the Virtual Channel for the data and 535 the Data Type for the application specific payload data. 

- 536 For both physical layer options, the 16-bit Word Count (WC) field defines the number of 8-bit data words 537 in the Data Payload between the end of the Packet Header and the start of the Packet Footer. No Packet 538 Header, Packet Footer, or Packet Filler bytes shall be included in the Word Count. 

- 539 For the D-PHY physical layer option, the Error Correction Code (ECC) byte allows single-bit errors to be 540 corrected and 2-bit errors to be detected in the Packet Header. This includes both the Data Identifier value 541 and the Word Count value. 

- 542 The ECC byte is not used by the C-PHY physical layer option because a single symbol error on a C-PHY 543 physical link can cause multiple bit errors in the received CSI-2 Packet Header, rendering an ECC 544 ineffective. Instead, a CSI-2 protocol transmitter for the C-PHY physical layer option computes a 16-bit 545 CRC over the four bytes composing the Reserved, Data Identifier, and Word Count Packet Header fields 546 and then transmits multiple copies of all these fields, including the CRC, to facilitate their recovery by the 547 CSI-2 protocol receiver in the event of one or more C-PHY physical link errors. The multiple Sync Words 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

41 

Specification for CSI-2 

Version 1.3 29-May-2014 

- 548 inserted into the Packet Header by the C-PHY physical layer (as shown in Figure 39) also facilitate Packet 549 Header data recovery by enabling the C-PHY receiver to recover from lost symbol clocks; see [MIPI02] for 550 further information about the C-PHY Sync Word and symbol clock recovery. 

- 551 For both physical layer options, the CSI-2 receiver reads the next WC 8-bit data words of the Data Payload 552 following the Packet Header. While reading the Data Payload the receiver shall not look for any embedded 553 sync codes. Therefore, there are no limitations on the value of an 8-bit payload data word. In the generic 554 case, the length of the Data Payload shall always be a multiple of 8-bit data words. In addition, each Data 555 Type may impose additional restrictions on the length of the Data Payload, e.g. require a multiple of four 556 bytes. 

- 557 For both physical layer options, once the CSI-2 receiver has read the Data Payload, it then reads the 16-bit 558 checksum (CRC) in the Packet Footer and compares it against its own calculated checksum to determine if 559 any Data Payload errors have occurred. 

- 560 Filler bytes are only inserted by the CSI-2 transmitter’s low level protocol layer in conjunction with the C- 561 PHY physical layer option. The value of any Filler byte shall be zero. If the Packet Data Word Count (WC) 562 is an odd number (i.e. LSB is “1”), the CSI-2 transmitter shall insert one Packet Filler byte after the Packet 563 Footer to ensure that the Packet Footer ends on a 16-bit word boundary. The CSI-2 transmitter shall also 564 insert additional Filler bytes, if needed, to ensure that each C-PHY Lane transports the same number of 16565 bit words. The latter rules require the total number of Filler bytes, FC, to be greater than or equal to (WC 566 mod 2) + {{N - (([WC + 2 + (WC mod 2)] / 2) mod N)} mod N} * 2, where N is the number of Lanes. 567 Note that it is possible for FC to be zero. 

- 568 Figure 40 illustrates the Lane distribution of the minimal number of Filler bytes required for packets of 569 various lengths transmitted over three C-PHY Lanes. The total number of Filler bytes required per packet 570 ranges from 0 to 5, depending on the value of the Packet Data Word Count (WC). In general, the minimal 571 number of Filler bytes required per packet ranges from 0 to 2N-1 for an N-Lane C-PHY system. 

- 572 For the D-PHY physical layer option, the CSI-2 Lane Distributor function shall pass each byte to the 573 physical layer which then serially transmits it least significant bit first. 

- 574 For the C-PHY physical layer option, the Lane Distributor function shall group each pair of consecutive 575 bytes 2n and 2n+1 (for n ≥ 0) received from the Low Level Protocol into a 16-bit word (whose least 576 significant byte is byte 2n) and then pass this word to a physical layer Lane module. The C-PHY Lane 577 module maps each 16-bit word into a 7-symbol word which it then serially transmits least significant 578 symbol first. 

- 579 For both physical layer options, payload data may be presented to the Lane Distributor function in any byte 580 order restricted only by data format requirements. Multi-byte protocol elements such as Word Count, 581 Checksum and the Short packet 16-bit Data Field shall be presented to the Lane Distributor function least 582 significant byte first. 

- 583 After the EoT sequence the receiver begins looking for the next SoT sequence. 

Copyright © 2005-2014 MIPI Alliance, Inc. 

42 

All rights reserved. 

**Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

## Total Packet Data Word Count (WC) = 6n 

|Byte 1<br>EoT<br>Byte 0<br>Byte 6n-5<br>Byte 6n-6<br>Byte 6n+1<br>Byte 6n<br>EoT<br>Byte 3<br>Byte 2<br>Byte 6n-3<br>Byte 6n-4<br>Byte 6n+3<br>Byte 6n+2<br>EoT<br>Byte 5<br>Byte 4<br>Byte 6n-1<br>Byte 6n-2<br>PF (MSB)<br>PF (LSB)<br>Byte 1<br>EoT<br>Byte 0<br>Byte 6n+1<br>Byte 6n<br>PF (MSB)<br>Filler<br>EoT<br>Byte 3<br>Byte 2<br>Byte 6n+3<br>Byte 6n+2<br>Byte 5<br>Byte 4<br>PF (LSB)<br>Byte 6n+4<br>Byte 1<br>EoT<br>Byte 0<br>Byte 6n-5<br>Byte 6n-6<br>PF (MSB)<br>PF (LSB)<br>Byte 3<br>Byte 2<br>Byte 6n-3<br>Byte 6n-4<br>Byte 5<br>Byte 4<br>Byte 6n-1<br>Byte 6n-2<br>Byte 1<br>EoT<br>Byte 0<br>Byte 6n-5<br>Byte 6n-6<br>PF (LSB)<br>Byte 6n<br>EoT<br>Byte 3<br>Byte 2<br>Byte 6n-3<br>Byte 6n-4<br>PF (MSB)<br>Filler<br>Byte 5<br>Byte 4<br>Byte 6n-1<br>Byte 6n-2<br>Byte 1<br>EoT<br>Byte 0<br>Byte 6n-5<br>Byte 6n-6<br>Byte 6n+1<br>Byte 6n<br>EoT<br>Byte 3<br>Byte 2<br>Byte 6n-3<br>Byte 6n-4<br>PF (MSB)<br>PF (LSB)<br>Byte 5<br>Byte 4<br>Byte 6n-1<br>Byte 6n-2<br>Byte 1<br>EoT<br>Byte 0<br>Byte 6n-5<br>Byte 6n-6<br>Byte 6n+1<br>Byte 6n<br>EoT<br>Byte 3<br>Byte 2<br>Byte 6n-3<br>Byte 6n-4<br>PF (LSB)<br>Byte 6n+2<br>EoT<br>Byte 5<br>Byte 4<br>Byte 6n-1<br>Byte 6n-2<br>PF (MSB)<br>Filler<br>Total Packet Data Word Count (WC) = 6n+4<br>Total Packet Data Word Count (WC) = 6n+5<br>Total Packet Data Word Count (WC) = 6n+1<br>Total Packet Data Word Count (WC) = 6n+2<br>Total Packet Data Word Count (WC) = 6n+3<br>Filler<br>Filler<br>EoT<br>Filler<br>Filler<br>EoT<br>Filler<br>Filler<br>EoT<br>Filler<br>Filler<br>EoT<br>Filler<br>Filler<br>EoT<br>Filler<br>Filler<br>PH<br>Lane 1<br>Lane 2<br>SYN<br>PH<br>SoT<br>PH<br>SYN<br>PH<br>SoT<br>Lane 3<br>PH<br>SYN<br>PH<br>SoT<br>PH<br>Lane 1<br>Lane 2<br>SYN<br>PH<br>SoT<br>PH<br>SYN<br>PH<br>SoT<br>Lane 3<br>PH<br>SYN<br>PH<br>SoT<br>PH<br>Lane 1<br>Lane 2<br>SYN<br>PH<br>SoT<br>PH<br>SYN<br>PH<br>SoT<br>Lane 3<br>PH<br>SYN<br>PH<br>SoT<br>PH<br>Lane 1<br>Lane 2<br>SYN<br>PH<br>SoT<br>PH<br>SYN<br>PH<br>SoT<br>Lane 3<br>PH<br>SYN<br>PH<br>SoT<br>PH<br>Lane 1<br>Lane 2<br>SYN<br>PH<br>SoT<br>PH<br>SYN<br>PH<br>SoT<br>Lane 3<br>PH<br>SYN<br>PH<br>SoT<br>PH<br>Lane 1<br>Lane 2<br>SYN<br>PH<br>SoT<br>PH<br>SYN<br>PH<br>SoT<br>Lane 3<br>PH<br>SYN<br>PH<br>SoT<br>**KEY**:<br>SoT – Start of Transmission<br>EoT – End of Transmission<br>PF – Packet Footer<br>SYN – 7-Symbol Sync Word<br>PH – Packet Header (6 Bytes)<br>(2 Bytes)|SoT|PH|SYN|PH|Byte 1<br>Byte 0||Byte 6n-5<br>Byte 6n-6|PF (MSB)<br>PF (LSB)|EoT|
|---|---|---|---|---|---|---|---|---|---|
|||||||||||
||SoT|PH|SYN|PH|Byte 3<br>Byte 2||Byte 6n-3<br>Byte 6n-4|Filler<br>Filler|EoT|
|||||||||||
||SoT|PH|SYN|PH|Byte 5<br>Byte 4||Byte 6n-1<br>Byte 6n-2|Filler<br>Filler|EoT|



**Figure 40 Minimal Filler Byte Insertion Requirements for Three Lane C-PHY** 

584 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

43 

Specification for CSI-2 

Version 1.3 29-May-2014 

## 585 **9.1.2 Low Level Protocol Short Packet Format** 

- 586 Figure 41 and Figure 42 show the Low Level Protocol Short Packet structures for the D-PHY and C-PHY 587 physical layer options, respectively. For each option, the Short Packet structure matches the Packet Header 

- 588 of the corresponding Low Level Protocol Long Packet structure with the exception that the Packet Header 

- 589 Word Count (WC) field shall be replaced by the Short Packet Data Field. A Short Packet shall be identified 590 by Data Types 0x00 to 0x0F. See Table 3 for a description of the Data Types. A Short Packet shall contain 591 only a Packet Header; neither Packet Footer nor Packet Filler bytes shall be present. 

- 592 For Frame Synchronization Data Types the Short Packet Data Field shall be the frame number. For Line 593 Synchronization Data Types the Short Packet Data Field shall be the line number. See Table 6 for a 594 description of the Frame and Line synchronization Data Types. 

- 595 For Generic Short Packet Data Types the content of the Short Packet Data Field shall be user defined. 

- 596 For the D-PHY physical layer option, the Error Correction Code (ECC) byte allows single-bit errors to be 597 corrected and 2-bit errors to be detected in the Short Packet. For the C-PHY physical layer option, the 16598 bit Checksum (CRC) allows one or more bit errors to be detected in the Short Packet but does not support 599 error correction; the latter is facilitated by transmitting multiple copies of the various Short Packet fields 600 and by C-PHY Sync Word insertion on all Lanes. 

601 

602 

|EoT<br>LPS<br>SoT<br>16-Bit<br>Short Packet<br>Data Field<br>ECC<br>Data ID<br>**32-bit SHORT PACKET (SH)**<br>Data Type (DT) = 0x00 – 0x0F<br>LPS<br>**Figure 41 Short Packet Structure for D-PHY Physical Layer Option**<br>**CSI-2 “Insert Sync Word” PPI Command:**<br>The physical layer simultaneously inserts a 7-symbol Sync Word on all<br>N Lanes at this point in response to a single CSI-2 PPI command.<br>Set to “0”<br>Set to “0”|EoT<br>LPS<br>SoT<br>16-Bit<br>Short Packet<br>Data Field<br>ECC<br>Data ID<br>**32-bit SHORT PACKET (SH)**<br>Data Type (DT) = 0x00 – 0x0F<br>LPS<br>**Figure 41 Short Packet Structure for D-PHY Physical Layer Option**<br>**CSI-2 “Insert Sync Word” PPI Command:**<br>The physical layer simultaneously inserts a 7-symbol Sync Word on all<br>N Lanes at this point in response to a single CSI-2 PPI command.<br>Set to “0”<br>Set to “0”|EoT<br>LPS<br>SoT<br>16-Bit<br>Short Packet<br>Data Field<br>ECC<br>Data ID<br>**32-bit SHORT PACKET (SH)**<br>Data Type (DT) = 0x00 – 0x0F<br>LPS<br>**Figure 41 Short Packet Structure for D-PHY Physical Layer Option**<br>**CSI-2 “Insert Sync Word” PPI Command:**<br>The physical layer simultaneously inserts a 7-symbol Sync Word on all<br>N Lanes at this point in response to a single CSI-2 PPI command.<br>Set to “0”<br>Set to “0”|EoT<br>LPS<br>SoT<br>16-Bit<br>Short Packet<br>Data Field<br>ECC<br>Data ID<br>**32-bit SHORT PACKET (SH)**<br>Data Type (DT) = 0x00 – 0x0F<br>LPS<br>**Figure 41 Short Packet Structure for D-PHY Physical Layer Option**<br>**CSI-2 “Insert Sync Word” PPI Command:**<br>The physical layer simultaneously inserts a 7-symbol Sync Word on all<br>N Lanes at this point in response to a single CSI-2 PPI command.<br>Set to “0”<br>Set to “0”|EoT<br>LPS<br>SoT<br>16-Bit<br>Short Packet<br>Data Field<br>ECC<br>Data ID<br>**32-bit SHORT PACKET (SH)**<br>Data Type (DT) = 0x00 – 0x0F<br>LPS<br>**Figure 41 Short Packet Structure for D-PHY Physical Layer Option**<br>**CSI-2 “Insert Sync Word” PPI Command:**<br>The physical layer simultaneously inserts a 7-symbol Sync Word on all<br>N Lanes at this point in response to a single CSI-2 PPI command.<br>Set to “0”<br>Set to “0”|EoT<br>LPS<br>SoT<br>16-Bit<br>Short Packet<br>Data Field<br>ECC<br>Data ID<br>**32-bit SHORT PACKET (SH)**<br>Data Type (DT) = 0x00 – 0x0F<br>LPS<br>**Figure 41 Short Packet Structure for D-PHY Physical Layer Option**<br>**CSI-2 “Insert Sync Word” PPI Command:**<br>The physical layer simultaneously inserts a 7-symbol Sync Word on all<br>N Lanes at this point in response to a single CSI-2 PPI command.<br>Set to “0”<br>Set to “0”|EoT<br>LPS<br>SoT<br>16-Bit<br>Short Packet<br>Data Field<br>ECC<br>Data ID<br>**32-bit SHORT PACKET (SH)**<br>Data Type (DT) = 0x00 – 0x0F<br>LPS<br>**Figure 41 Short Packet Structure for D-PHY Physical Layer Option**<br>**CSI-2 “Insert Sync Word” PPI Command:**<br>The physical layer simultaneously inserts a 7-symbol Sync Word on all<br>N Lanes at this point in response to a single CSI-2 PPI command.<br>Set to “0”<br>Set to “0”|EoT<br>LPS<br>SoT<br>16-Bit<br>Short Packet<br>Data Field<br>ECC<br>Data ID<br>**32-bit SHORT PACKET (SH)**<br>Data Type (DT) = 0x00 – 0x0F<br>LPS<br>**Figure 41 Short Packet Structure for D-PHY Physical Layer Option**<br>**CSI-2 “Insert Sync Word” PPI Command:**<br>The physical layer simultaneously inserts a 7-symbol Sync Word on all<br>N Lanes at this point in response to a single CSI-2 PPI command.<br>Set to “0”<br>Set to “0”|EoT<br>LPS<br>SoT<br>16-Bit<br>Short Packet<br>Data Field<br>ECC<br>Data ID<br>**32-bit SHORT PACKET (SH)**<br>Data Type (DT) = 0x00 – 0x0F<br>LPS<br>**Figure 41 Short Packet Structure for D-PHY Physical Layer Option**<br>**CSI-2 “Insert Sync Word” PPI Command:**<br>The physical layer simultaneously inserts a 7-symbol Sync Word on all<br>N Lanes at this point in response to a single CSI-2 PPI command.<br>Set to “0”<br>Set to “0”|EoT<br>LPS<br>SoT<br>16-Bit<br>Short Packet<br>Data Field<br>ECC<br>Data ID<br>**32-bit SHORT PACKET (SH)**<br>Data Type (DT) = 0x00 – 0x0F<br>LPS<br>**Figure 41 Short Packet Structure for D-PHY Physical Layer Option**<br>**CSI-2 “Insert Sync Word” PPI Command:**<br>The physical layer simultaneously inserts a 7-symbol Sync Word on all<br>N Lanes at this point in response to a single CSI-2 PPI command.<br>Set to “0”<br>Set to “0”|EoT<br>LPS<br>SoT<br>16-Bit<br>Short Packet<br>Data Field<br>ECC<br>Data ID<br>**32-bit SHORT PACKET (SH)**<br>Data Type (DT) = 0x00 – 0x0F<br>LPS<br>**Figure 41 Short Packet Structure for D-PHY Physical Layer Option**<br>**CSI-2 “Insert Sync Word” PPI Command:**<br>The physical layer simultaneously inserts a 7-symbol Sync Word on all<br>N Lanes at this point in response to a single CSI-2 PPI command.<br>Set to “0”<br>Set to “0”|EoT<br>LPS<br>SoT<br>16-Bit<br>Short Packet<br>Data Field<br>ECC<br>Data ID<br>**32-bit SHORT PACKET (SH)**<br>Data Type (DT) = 0x00 – 0x0F<br>LPS<br>**Figure 41 Short Packet Structure for D-PHY Physical Layer Option**<br>**CSI-2 “Insert Sync Word” PPI Command:**<br>The physical layer simultaneously inserts a 7-symbol Sync Word on all<br>N Lanes at this point in response to a single CSI-2 PPI command.<br>Set to “0”<br>Set to “0”|
|---|---|---|---|---|---|---|---|---|---|---|---|
|LPS|SoT|Reserved|Data ID|16-Bit<br>Short Packet<br>Data Field*|16-Bit<br>Checksum*<br>(PH-CRC)|Reserved|Data ID|16-Bit<br>Short Packet<br>Data Field*|16-Bit<br>Checksum*<br>(PH-CRC)|EoT|LPS|



> *16-bit word which is **SHORT PACKET: 6N x 16-bits** presented l.s. byte first to the Lane Distributor function (N = Physical Layer Lane Count) 

## **Figure 42 Short Packet Structure for C-PHY Physical Layer Option** 

Copyright © 2005-2014 MIPI Alliance, Inc. 

44 

All rights reserved. **Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

## 603 **9.2 Data Identifier (DI)** 

- 604 The Data Identifier byte contains the Virtual Channel Identifier (VC) value and the Data Type (DT) value 605 as illustrated in Figure 43. The Virtual Channel Identifier is contained in the two MS bits of the Data 606 Identifier Byte. The Data Type value is contained in the six LS bits of the Data Identifier Byte. 

## **Data Identifier (DI) Byte** 

## 607 

**==> picture [193 x 83] intentionally omitted <==**

**----- Start of picture text -----**<br>
DI7 DI6 DI5 DI4 DI3 DI2 DI1 DI0<br>VC DT<br>Virtual Channel  Data Type<br>Indentifier (DT)<br>(VC)<br>**----- End of picture text -----**<br>


**Figure 43 Data Identifier Byte** 

## 608 **9.3 Virtual Channel Identifier** 

- 609 The purpose of the Virtual Channel Identifier is to provide separate channels for different data flows that 610 are interleaved in the data stream. 

- 611 The Virtual channel identifier number is in the most significant two bits of the Data Identifier Byte. The 612 Receiver will monitor the virtual channel identifier and de-multiplex the interleaved video streams to their 

- 613 appropriate channel. A maximum of four data streams is supported; valid channel identifiers are 0 to 3. The 614 virtual channel identifiers in the peripherals should be programmable to allow the host processor to control 615 how the data streams are de-multiplexed. The principle of logical channels is presented in the Figure 44. 

616 

**==> picture [351 x 167] intentionally omitted <==**

**----- Start of picture text -----**<br>
Channel Identifier Channel Configuration<br>Channel 0<br>Data In Channel 1<br>Channel<br>Detect<br>Channel 2<br>Logical Channel Control Channel 3<br>**----- End of picture text -----**<br>


**Figure 44 Logical Channel Block Diagram (Receiver)** 

- 617 Figure 45 illustrates an example of data streams utilizing virtual channel support. 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

45 

Specification for CSI-2 

**==> picture [49 x 8] intentionally omitted <==**

**----- Start of picture text -----**<br>
Version 1.3<br>**----- End of picture text -----**<br>


**==> picture [470 x 270] intentionally omitted <==**

**----- Start of picture text -----**<br>
29-May-2014<br>SoT PH RGB 6:6:6 PF EoT LPS SoT PH YUV 4:2:2 PF EoT LPS SoT PH RGB 6:6:6 PF EoT<br>Virtual Channel 0 Virtual Channel 1 Virtual Channel 0<br>SoT PH RGB 5:6:5 PF EoT LPS SoT PH JPEG8 PF EoT LPS SoT PH RGB 5:6:5 PF EoT<br>Virtual Channel 0 Virtual Channel 1 Virtual Channel 0<br>SoT PH RGB 6:6:6 PF EoT LPS SoT PH MPEG4 PF EoT LPS SoT PH RGB 6:6:6 PF EoT<br>Virtual Channel 0 Virtual Channel 1 Virtual Channel 0<br>KEY :<br>LPS – Low Power State PH – Packet Header<br>SoT – Start of Transmission PF – Packet Footer + Filler (if applicable)<br>EoT – End of Transmission<br>618<br>**----- End of picture text -----**<br>


## **Figure 45 Interleaved Video Data Streams Examples** 

## 619 **9.4 Data Type (DT)** 

- 620 The Data Type value specifies the format and content of the payload data. A maximum of sixty-four data 621 types are supported. 

- 622 There are eight different data type classes as shown in Table 3. Within each class there are up to eight 

- 623 different data type definitions. The first two classes denote short packet data types. The remaining six 624 classes denote long packet data types. 

- 625 For details on the short packet data type classes refer to Section 9.8. 

- 626 For details on the five long packet data type classes refer to Section 11. 

## 627 **Table 3 Data Type Classes** 

|**Data Type**|**Description**|
|---|---|
|0x00 to 0x07|Synchronization Short Packet Data Types|
|0x08 to 0x0F|Generic Short Packet Data Types|
|0x10 to 0x17|Generic Long Packet Data Types|
|0x18 to 0x1F|YUV Data|
|0x20 to 0x27|RGB Data|
|0x28 to 0x2F|RAW Data|
|0x30 to 0x37|User Defined Byte-based Data|
|0x38 to 0x3F|Reserved|



## 628 **9.5 Packet Header Error Correction Code for D-PHY Physical Layer** 629 **Option** 

- 630 The correct interpretation of the data identifier and word count values is vital to the packet structure. The 631 Packet Header Error Correction Code (ECC) byte allows single-bit errors in the data identifier and the word 

Copyright © 2005-2014 MIPI Alliance, Inc. 

46 

All rights reserved. **Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

- 632 count to be corrected and two-bit errors to be detected for the D-PHY physical layer option; the ECC is not 

- 633 available for the C-PHY physical layer option.. The 24-bit subset of the code described in Section 9.5.2 

- 634 shall be used. Therefore, bits 7 and 6 of the ECC byte shall be zero. The error state based on ECC decoding 635 shall be available at the Application layer in the receiver. 

- 636 The Data Identifier field DI[7:0] shall map to D[7:0] of the ECC input, the Word Count LS Byte (WC[7:0]) 

- 637 to D[15:8] and the Word Count MS Byte (WC[15:8]) to D[23:16]. This mapping is shown in Figure 46, 638 which also serves as an ECC calculation example. 

**==> picture [430 x 246] intentionally omitted <==**

**----- Start of picture text -----**<br>
32-bit<br>PACKET HEADER<br>(PH)<br>LPS SoT<br>Data ID = 0x37 WC LS Byte = 0xF0 WC MS Byte = 0x01 ECC = 0x3F<br>DOUT 1 1 1 0 1 1 0 0 0 0 0 0 1 1 1 1 1 0 0 0 0 0 0 0 1 1 1 1 1 1 0 0<br>L M L M L M L M<br>S S S S S S S S<br>B B B B B B B B<br>ECC Calculation ECC<br>1 1 1 0 1 1 0 0 0 0 0 0 1 1 1 1 1 0 0 0 0 0 0 0 1 1 1 1 1 1 0 0<br>D D P0 P1 P2 P3 P4 P5<br>0 2<br>3<br>Data ID (WC) ECC Data 0<br>Word Count<br>**----- End of picture text -----**<br>


## 639 

**Figure 46 24-bit ECC Generation Example** 

## 640 **9.5.1 General Hamming Code Applied to Packet Header** 

- 641 The number of parity or error check bits required is given by the Hamming rule, and is a function of the 642 number of bits of information transmitted. The Hamming rule is expressed by the following inequality: 

- 643 _d_ + _p_ + 1 ≤ 2 _[p]_ , where _d_ is the number of data bits and _p_ is the number of parity bits. 

- 644 The result of appending the computed parity bits to the data bits is called the Hamming code word. The size 645 of the code word _c_ is obviously _d_ + _p_ , and a Hamming code word is described by the ordered set ( _c_ , _d_ ). A 646 Hamming code word is generated by multiplying the data bits by a generator matrix **G** . The resulting 

- 647 product is the code-word vector (c1, c2, c3 … cn), consisting of the original data bits and the calculated 648 parity bits. The generator matrix **G** used in constructing Hamming codes consists of **I** (the identity matrix) 649 and a parity generation matrix **A** : 

- 650 **G** = [ **I** | **A** ] 

- 651 The packet header plus the ECC code can be obtained as: PH = p* **G** where p represents the header (24 or 652 64 bits) and **G** is the corresponding generator matrix. 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

47 

Specification for CSI-2 

Version 1.3 

29-May-2014 

- 653 Validating the received code word r, involves multiplying it by a parity check to form s, the syndrome or 654 parity check vector: s = **H** *PH where PH is the received packet header and **H** is the parity check matrix: 

- 655 

## **H** = [ **A[T]** | **I** ] 

- 656 If all elements of s are zero, the code word was received correctly. If s contains non-zero elements, then at 657 least one error is present. If a single bit error is encountered then the syndrome s is one of the elements of **H** 658 which will point to the bit in error. Further, in this case, if the bit in error is one of the parity bits, then the 659 syndrome will be one of the elements on **I** , else it will be the data bit identified by the position of the 660 syndrome in **A[T]** . 

- 661 **9.5.2 Hamming-Modified Code** 

- 662 The error correcting code used is a 7+1 bits Hamming-modified code (72,64) and the subset of it is 5+1bits 663 or (30,24). Hamming codes use parity to correct one error or detect two errors, but they are not capable of 664 doing both simultaneously, thus one extra parity bit is added. The code used allows the same 6-bit 665 syndromes to correct the first 24-bits of a 64-bit sequence. To specify a compact encoding of parity and 666 decoding of syndromes, the following matrix is used: 

- 667 

- 668 

**Table 4 ECC Syndrome Association Matrix** 

|||||**d2d1d0**|**d2d1d0**||||
|---|---|---|---|---|---|---|---|---|
|d5d4d3|**0b000**|**0b001**|**0b010**|**0b011**|**0b100**|**0b101**|**0b110**|**0b111**|
|0b000|0x07|0x0B|0x0D|0x0E|0x13|0x15|0x16|0x19|
|0b001|0x1A|0x1C|0x23|0x25|0x26|0x29|0x2A|0x2C|
|0b010|0x31|0x32|0x34|0x38|0x1F|0x2F|0x37|0x3B|
|0b011|0x43|0x45|0x46|0x49|0x4A|0x4C|0x51|0x52|
|0b100|0x54|0x58|0x61|0x62|0x64|0x68|0x70|0x83|
|0b101|0x85|0x86|0x89|0x8A|0x3D|0x3E|0x4F|0x57|
|0b110|0x8C|0x91|0x92|0x94|0x98|0xA1|0xA2|0xA4|
|0b111|0xA8|0xB0|0xC1|0xC2|0xC4|0xC8|0xD0|0xE0|



- 669 Each cell in the matrix represents a syndrome and the first twenty-four cells (the orange rows) are using the 

- 670 first three or five bits to build the syndrome. Each syndrome in the matrix is MSB left aligned: 

- 671 e.g. 0x07=0b0000_0111=P7P6P5P4P3P2P1P0 

- 672 The top row defines the three LSB of data position bit, and the left column defines the three MSB of data 673 position bit (there are 64-bit positions in total). 

- 674 e.g. 37th bit position is encoded 0b100_101 and has the syndrome 0x68. 

- 675 To derive the parity P0 for 24-bits, the P0’s in the orange rows will define if the corresponding bit position 676 is used in P0 parity or not. 

- 677 e.g. P024-bits = D0^D1^D2^D4^D5^D7^D10^D11^D13^D16^D20^D21^D22^D23 

48 Copyright © 2005-2014 MIPI Alliance, Inc. 

All rights reserved. 

**Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

- 678 Similar, to derive the parity P0 for 64-bits, all P0’s in Table 5 will define the corresponding bit positions to 679 be used. 

- 680 To correct a single-bit error, the syndrome has to be one of the syndromes Table 4, which will identify the 681 bit position in error. The syndrome is calculated as: 

- 682 S = PSEND^PRECEIVED where PSEND is the 8/6-bit ECC field in the header and PRECEIVED is the 683 calculated parity of the received header. 

- 684 Table 5 represents the same information as the matrix in Table 4, organized such that will give a better 685 insight on the way parity bits are formed out of data bits. The orange area of the table has to be used to 686 form the ECC to protect a 24-bit header, whereas the whole table has to be used to protect a 64-bit header. 

- 687 

**Table 5 ECC Parity Generation Rules** 

|**Bit**|**P7**|**P6**|**P5**|**P4**|**P3**|**P2**|**P1**|**P0**|**Hex**|
|---|---|---|---|---|---|---|---|---|---|
|**0**|0|0|0|0|0|1|1|1|0x07|
|**1**|0|0|0|0|1|0|1|1|0x0B|
|**2**|0|0|0|0|1|1|0|1|0x0D|
|**3**|0|0|0|0|1|1|1|0|0x0E|
|**4**|0|0|0|1|0|0|1|1|0x13|
|**5**|0|0|0|1|0|1|0|1|0x15|
|**6**|0|0|0|1|0|1|1|0|0x16|
|**7**|0|0|0|1|1|0|0|1|0x19|
|**8**|0|0|0|1|1|0|1|0|0x1A|
|**9**|0|0|0|1|1|1|0|0|0x1C|
|**10**|0|0|1|0|0|0|1|1|0x23|
|**11**|0|0|1|0|0|1|0|1|0x25|
|**12**|0|0|1|0|0|1|1|0|0x26|
|**13**|0|0|1|0|1|0|0|1|0x29|
|**14**|0|0|1|0|1|0|1|0|0x2A|
|**15**|0|0|1|0|1|1|0|0|0x2C|
|**16**|0|0|1|1|0|0|0|1|0x31|
|**17**|0|0|1|1|0|0|1|0|0x32|
|**18**|0|0|1|1|0|1|0|0|0x34|
|**19**|0|0|1|1|1|0|0|0|0x38|
|**20**|0|0|0|1|1|1|1|1|0x1F|
|**21**|0|0|1|0|1|1|1|1|0x2F|
|**22**|0|0|1|1|0|1|1|1|0x37|
|**23**|0|0|1|1|1|0|1|1|0x3B|
|**24**|0|1|0|0|0|0|1|1|0x43|
|**25**|0|1|0|0|0|1|0|1|0x45|
|**26**|0|1|0|0|0|1|1|0|0x46|
|**27**|0|1|0|0|1|0|0|1|0x49|



Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

49 

Specification for CSI-2 

Version 1.3 

29-May-2014 

|**Bit**|**P7**|**P6**|**P5**|**P4**|**P3**|**P2**|**P1**|**P0**|**Hex**|
|---|---|---|---|---|---|---|---|---|---|
|**28**|0|1|0|0|1|0|1|0|0x4A|
|**29**|0|1|0|0|1|1|0|0|0x4C|
|**30**|0|1|0|1|0|0|0|1|0x51|
|**31**|0|1|0|1|0|0|1|0|0x52|
|**32**|0|1|0|1|0|1|0|0|0x54|
|**33**|0|1|0|1|1|0|0|0|0x58|
|**34**|0|1|1|0|0|0|0|1|0x61|
|**35**|0|1|1|0|0|0|1|0|0x62|
|**36**|0|1|1|0|0|1|0|0|0x64|
|**37**|0|1|1|0|1|0|0|0|0x68|
|**38**|0|1|1|1|0|0|0|0|0x70|
|**39**|1|0|0|0|0|0|1|1|0x83|
|**40**|1|0|0|0|0|1|0|1|0x85|
|**41**|1|0|0|0|0|1|1|0|0x86|
|**42**|1|0|0|0|1|0|0|1|0x89|
|**43**|1|0|0|0|1|0|1|0|0x8A|
|**44**|0|0|1|1|1|1|0|1|0x3D|
|**45**|0|0|1|1|1|1|1|0|0x3E|
|**46**|0|1|0|0|1|1|1|1|0x4F|
|**47**|0|1|0|1|0|1|1|1|0x57|
|**48**|1|0|0|0|1|1|0|0|0x8C|
|**49**|1|0|0|1|0|0|0|1|0x91|
|**50**|1|0|0|1|0|0|1|0|0x92|
|**51**|1|0|0|1|0|1|0|0|0x94|
|**52**|1|0|0|1|1|0|0|0|0x98|
|**53**|1|0|1|0|0|0|0|1|0xA1|
|**54**|1|0|1|0|0|0|1|0|0xA2|
|**55**|1|0|1|0|0|1|0|0|0xA4|
|**56**|1|0|1|0|1|0|0|0|0xA8|
|**57**|1|0|1|1|0|0|0|0|0xB0|
|**58**|1|1|0|0|0|0|0|1|0xC1|
|**59**|1|1|0|0|0|0|1|0|0xC2|
|**60**|1|1|0|0|0|1|0|0|0xC4|
|**61**|1|1|0|0|1|0|0|0|0xC8|
|**62**|1|1|0|1|0|0|0|0|0xD0|
|**63**|1|1|1|0|0|0|0|0|0xE0|



688 

50 

Copyright © 2005-2014 MIPI Alliance, Inc. 

All rights reserved. **Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

## 689 **9.5.3 ECC Generation on TX Side** 

- 690 This is an informative section. 

- 691 The ECC can be easily implemented using a parallel approach as depicted in Figure 47 for a 64-bit header. 

## 692 

**==> picture [205 x 103] intentionally omitted <==**

**----- Start of picture text -----**<br>
P 7 6 5 4 3 2 1 0<br>Parity Generator<br>**----- End of picture text -----**<br>


**Figure 47 64-bit ECC Generation on TX Side** 

- 693 And Figure 48 for a 24-bit header: 

- 694 

**==> picture [92 x 103] intentionally omitted <==**

**----- Start of picture text -----**<br>
P 2 1 0<br>Parity<br>Generator<br>**----- End of picture text -----**<br>


**Figure 48 24-bit ECC Generation on TX Side** 

- 695 The parity generators are based on Table 5. 

- 696 e.g. P324-bit = D1^D2^D3^D7^D8^D9^D13^D14^D15^D19^D20^D21^D23 

## 697 **9.5.4 Applying ECC on RX Side** 

- 698 Applying ECC on RX side involves generating a new ECC for the received packet, computing the 699 syndrome using the new ECC and the received ECC, decoding the syndrome to find if a single-error has 700 occurred and if so, correct it. 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

51 

Specification for CSI-2 

Version 1.3 

29-May-2014 

**==> picture [466 x 280] intentionally omitted <==**

**----- Start of picture text -----**<br>
Combinational<br>Received ECC Logic Block<br>Rec’d  No error<br>ECC<br>Byte Interface In  XOR SYN Syndrome Decoder Corrected Error<br>to ECC block Error<br>Parity  Calc’d<br>Generator ECC<br>Corrected Data<br>ECC<br>8 XOR 8<br>7 XOR 7<br>Received Packet<br>6 XOR 6<br>Header<br>5 XOR 5<br>4 XOR 4<br>3 XOR 3<br>2 XOR 2<br>1 XOR 1<br>Byte Interface<br>out from ECC<br>701  Block<br>**----- End of picture text -----**<br>


## **Figure 49 64-bit ECC on RX Side Including Error Correction** 

- 702 Decoding the syndrome has three aspects: 

- 703 

   - Finding if the packet has any errors (if syndrome is 0, no errors are present) 

- 704 • Checking if a single error has occurred by searching Table 5, if the syndrome is one of the entries 705 in the table, then a single bit error has occurred and the corresponding bit is affected, thus this 706 position in the data stream is complemented. Also, if the syndrome is one of the rows of the 707 identity matrix I, then one of the parity bits are in error. If the syndrome cannot be identified, then 708 a higher order error has occurred and the error flag will be set (the stream is corrupted and cannot 709 be restored). 

- 710 • Correcting the single error detected, as previously indicated. 

- 711 The 24-bit implementation uses fewer terms to calculate the parity and thus the syndrome decoding block is 712 much simpler than the 64-bit implementation. 

52 

Copyright © 2005-2014 MIPI Alliance, Inc. 

All rights reserved. 

**Confidential** 

Version 1.3 

Specification for CSI-2 

29-May-2014 

**==> picture [466 x 204] intentionally omitted <==**

**----- Start of picture text -----**<br>
Combinational<br>Received ECC Logic Block<br>Rec’d  No error<br>ECC<br>XOR SYN Syndrome  Corrected Error<br>Byte Interface In  Decoder<br>to ECC block Error<br>Parity  Calc’d<br>Generator ECC<br>Corrected Data<br>ECC<br>Received Packet<br>3 XOR 3<br>Header<br>2 XOR 2<br>1 XOR 1<br>Byte Interface<br>out from ECC<br>713  Block<br>**----- End of picture text -----**<br>


**Figure 50 24-bit ECC on RX Side Including Error Correction** 

## 714 **9.6 Checksum Generation** 

- 715 To detect possible errors in transmission, a checksum is calculated over the WC bytes composing the 716 Packet Data of every Long Packet; a similar checksum is calculated over the four bytes composing the 717 Reserved, Data Identifier, and Word Count fields of every Packet Header for the C-PHY physical layer 718 option. In all cases, the checksum is realized as 16-bit CRC based on the generator polynomial 719 x[16] +x[12] +x[5] +x[0] and is computed over bytes in the order in which they are presented to the Lane Distributor 720 function by the low level protocol layer as shown in Figure 37, Figure 38, and Figure 42. 

- 721 The order in which the checksum bytes are presented to the Lane Distributor function is illustrated in 722 Figure 51. 

## 16-bit Checksum 

- 723 

CRC LS Byte CRC MS Byte 

**Figure 51 Checksum Transmission Byte Order** 

- 724 When computed over the Packet Data words of a Long Packet, the 16-bit checksum sequence is transmitted 725 as part of the Packet Footer. When the Word Count is zero, the CRC shall be 0xFFFF. When computed over 726 the Reserved, Data Identifier, and Word Count fields of a Packet Header for the C-PHY physical layer 727 option, the 16-bit checksum sequence is transmitted as part of the Packet Header CRC (PH-CRC) field. 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

53 

Specification for CSI-2 

Version 1.3 

29-May-2014 

Included in the Checksum Checksum 

728 

|DI|DI|WC|WC|ECC|ECC|Payload Data – Packet 1|Payload Data – Packet 1|CS|
|---|---|---|---|---|---|---|---|---|
|DI||WC||ECC||Payload Data – Packet 2||CS|
||||||||||
|DI||WC||ECC||Payload Data – Packet N||CS|



## **Figure 52 Checksum Generation for Long Packet Payload Data** 

729 The definition of a serial CRC implementation is presented in Figure 53. The CRC implementation shall be 730 functionally equivalent with the C code presented in Figure 54. The CRC shift register is initialized to 731 0xFFFF at the beginning of each packet. Note that for the C-PHY physical layer option, if the same 732 circuitry is used to compute both the Packet Header and Packet Footer CRC, the CRC shift register shall be 733 initialized twice per packet, i.e. once at the beginning of the packet and then again following the 734 computation of the Packet Header CRC. After all payload data has passed through the CRC circuitry, the 735 CRC circuitry contains the checksum. The 16-bit checksum produced by the C code in Figure 54 equals the 736 final contents of the C[15:0] shift register shown in Figure 53. The checksum is then transmitted by the 737 CSI-2 physical layer to the CSI-2 receiver to verify that no errors have occurred in the transmission. 

**==> picture [386 x 43] intentionally omitted <==**

**----- Start of picture text -----**<br>
C15 C14 C13 C12 C11 C10 C9 C8 C7 C6 C5 C4 C3 C2 C1 C0<br>**----- End of picture text -----**<br>


738 

**Polynomial: x[16] + x[12] + x[5] + x[0]** Note: C15 represents x[0] , C0 represents x[15] 

**Figure 53 Definition of 16-bit CRC Shift Register** 

54 

Copyright © 2005-2014 MIPI Alliance, Inc. 

All rights reserved. **Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

```
#define POLY 0x8408   /* 1021H bit reversed */
```

```
unsigned short crc16(char *data_p, unsigned short length)
{
```

```
unsigned char i;
unsigned int data;
unsigned int crc = 0xffff;
```

```
if (length == 0)
return (unsigned short)(crc);
do
{
for (i=0, data=(unsigned int)0xff & *data_p++;
  i < 8;i++, data >>= 1)
{
if ((crc & 0x0001) ^ (data & 0x0001))
crc = (crc >> 1) ^ POLY;
else
crc >>= 1;
}
} while (--length);
```

```
// Uncomment to change from little to big Endian
//crc = ((crc & 0xff) << 8) | ((crc & 0xff00) >> 8);
```

```
return (unsigned short)(crc);
```

- 739 

## **`}`** 

## **Figure 54 16-bit CRC Software Implementation Example** 

- 740 Beginning with index 0, the contents of the input data array in Figure 54 are given by WC 8-bit payload 

- 741 data words for packet data CRC computations and by the four 8-bit Reserved, Data Identifier, WC (LS 742 byte), and WC (MS byte) fields for packet header CRC computations. 

- 743 

- 744 CRC computation examples: 

- 745 `Input Data Bytes:` 

746 `FF 00 00 02 B9 DC F3 72 BB D4 B8 5A C8 75 C2 7C 81 F8 05 DF FF 00 00 01` 747 `Checksum LS byte and MS byte:` 748 `F0 00` 

- 749 

- 750 `Input Data Bytes:` 

- 751 `FF 00 00 00 1E F0 1E C7 4F 82 78 C5 82 E0 8C 70 D2 3C 78 E9 FF 00 00 01` 752 `Checksum LS byte and MS byte:` 

- 753 `69 E5` 

## 754 **9.7 Packet Spacing** 

- 755 Between Low Level Protocol packets there must always be a transition into and out of the Low Power State 756 (LPS). Figure 55 illustrates the packet spacing with the LPS. 

- 757 The packet spacing does not have to be a multiple of 8-bit data words as the receiver will resynchronize to 

- 758 the correct byte boundary during the SoT sequence prior to the Packet Header of the next packet. 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

55 

Specification for CSI-2 

Version 1.3 29-May-2014 

## **SHORT / LONG PACKET SPACING** : 

Variable - always a LPS between packets 

**==> picture [348 x 137] intentionally omitted <==**

**----- Start of picture text -----**<br>
ST PH DATA PF ET LPS ST PH DATA PF ET<br>ST SP ET LPS ST SP ET LPS ST PH DATA PF ET<br>**----- End of picture text -----**<br>


**KEY** : 

## 759 

LPS – Low Power State PH – Packet Header ST – Start of Transmission PF – Packet Footer + Filler (if applicable) ET – End of Transmission SP – Short Packet 

**Figure 55 Packet Spacing** 

## 760 **9.8 Synchronization Short Packet Data Type Codes** 

- 761 Short Packet Data Types shall be transmitted using only the Short Packet format. See Section 9.1.2 for a 762 format description. 

- 763 **Table 6 Synchronization Short Packet Data Type Codes** 

|**Data Type**|**Description**|
|---|---|
|0x00|Frame Start Code|
|0x01|Frame End Code|
|0x02|Line Start Code (Optional)|
|0x03|Line End Code (Optional)|
|0x04 to 0x07|Reserved|



## 764 **9.8.1 Frame Synchronization Packets** 

- 765 Each image frame shall begin with a Frame Start (FS) Packet containing the Frame Start Code. The FS 766 Packet shall be followed by one or more long packets containing image data and zero or more short packets 

- 767 containing synchronization codes. Each image frame shall end with a Frame End (FE) Packet containing 768 the Frame End Code. See Table 6 for a description of the synchronization code data types. 

- 769 For FS and FE synchronization packets the Short Packet Data Field shall contain a 16-bit frame number. 770 This frame number shall be the same for the FS and FE synchronization packets corresponding to a given 771 frame. 

- 772 The 16-bit frame number, when used, shall be non-zero to distinguish it from the use-case where frame 773 number is inoperative and remains set to zero. 

- 774 The behavior of the 16-bit frame number shall be as one of the following 

- 775 

   - Frame number is always zero – frame number is inoperative. 

- 776 • Frame number increments by 1 for every FS packet with the same Virtual Channel and is 777 periodically reset to one e.g. 1, 2, 1, 2, 1, 2, 1, 2 or 1, 2, 3, 4, 1, 2, 3, 4 

56 

Copyright © 2005-2014 MIPI Alliance, Inc. 

All rights reserved. 

**Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

- 778 The frame number must be a non-zero value. 

## 779 **9.8.2 Line Synchronization Packets** 

- 780 

   - Line synchronization packets are optional. 

- 781 For Line Start (LS) and Line End (LE) synchronization packets the Short Packet Data Field shall contain a 782 16-bit line number. This line number shall be the same for the LS and LE packets corresponding to a given 783 line. Line numbers are logical line numbers and are not necessarily equal to the physical line numbers 

- 784 The 16-bit line number, when used, shall be non-zero to distinguish it from the case where line number is 785 inoperative and remains set to zero. 

- 786 The behavior of the 16-bit line number shall be as one of the following: 

- 787 

   - Line number is always zero – line number is inoperative. 

- 788 • Line number increments by one for every LS packet within the same Virtual Channel and the same 789 Data Type. The line number is periodically reset to one for the first LS packet after a FS packet. 790 The intended usage is for progressive scan (non- interlaced) video data streams. The line number 791 must be a non-zero value. 

- 792 • Line number increments by the same arbitrary step value greater than one for every LS packet 793 within the same Virtual Channel and the same Data Type. The line number is periodically reset to 794 a non-zero arbitrary start value for the first LS packet after a FS packet. The arbitrary start value 795 may be different between successive frames. The intended usage is for interlaced video data 796 streams. 

## 797 **9.9 Generic Short Packet Data Type Codes** 

- 798 Table 7 lists the Generic Short Packet Data Types. 

## 799 

**Table 7 Generic Short Packet Data Type Codes** 

|**Data Type**|**Description**|
|---|---|
|0x08|Generic Short Packet Code 1|
|0x09|Generic Short Packet Code 2|
|0x0A|Generic Short Packet Code 3|
|0x0B|Generic Short Packet Code 4|
|0x0C|Generic Short Packet Code 5|
|0x0D|Generic Short Packet Code 6|
|0x0E|Generic Short Packet Code 7|
|0x0F|Generic Short Packet Code 8|



800 The intention of the Generic Short Packet Data Types is to provide a mechanism for including timing 801 information for the opening/closing of shutters, triggering of flashes, etc. within the data stream. The intent 802 of the 16-bit User defined data field in the generic short packets is to pass a data type value and a 16-bit 803 data value from the transmitter to application layer in the receiver. The CSI-2 receiver shall pass the data 804 type value and the associated 16-bit data value to the application layer. 

## 805 

## **9.10 Packet Spacing Examples** 

806 Packets are separated by an EoT, LPS, SoT sequence as defined in [MIPI01] for the D-PHY physical layer 807 option and [MIPI02] for the C-PHY physical layer option. 

808 Figure 56 and Figure 57 contain examples of data frames composed of multiple packets and a single 809 packet, respectively. 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

57 

Specification for CSI-2 

Version 1.3 

29-May-2014 

810 Note that the VVALID, HVALID and DVALID signals in the figures in this section are only concepts to 811 help illustrate the behavior of the frame start/end and line start/end packets. The VVALID, HVALID and 812 DVALID signals do not form part of the Specification. 

**==> picture [466 x 193] intentionally omitted <==**

**----- Start of picture text -----**<br>
Frame Start  First Packet  Last Packet  Frame End<br>Packet of Data of Data Packet<br>SoT FS EoT LPS SoT PH Data PF EoT SoT PH Data PF EoT LPS SoT FE EoT<br>VVALID<br>HVALID<br>DVALID<br>KEY :<br>SoT – Start of Transmission EoT – End of Transmission LPS – Low Power State<br>PH – Packet Header PF – Packet Footer + Filler (if applicable)<br>FS – Frame Start  FE – Frame End<br>LS – Line Start  LE – Line End<br>813<br>**----- End of picture text -----**<br>


**Figure 56 Multiple Packet Example** 

**==> picture [466 x 196] intentionally omitted <==**

**----- Start of picture text -----**<br>
Frame Start  Frame End<br>Packet Packet<br>SoT FS EoT LPS SoT PH Data PF EoT LPS SoT FE EoT<br>VVALID<br>HVALID<br>DVALID<br>KEY :<br>SoT – Start of Transmission EoT – End of Transmission LPS – Low Power State<br>PH – Packet Header PF – Packet Footer + Filler (if applicable)<br>FS – Frame Start  FE – Frame End<br>LS – Line Start  LE – Line End<br>814<br>**----- End of picture text -----**<br>


**Figure 57 Single Packet Example** 

58 

Copyright © 2005-2014 MIPI Alliance, Inc. 

All rights reserved. **Confidential** 

Version 1.3 

Specification for CSI-2 

29-May-2014 

**==> picture [410 x 181] intentionally omitted <==**

**----- Start of picture text -----**<br>
1 Line 1 Line<br>SoT PH Data PF EoT LPS SoT PH Data PF EoT LPS SoT PH Data PF EoT<br>Long Packet Long Packet Long Packet<br>Line Blanking Line Blanking<br>Last Packet of  Frame End  Frame Start  First Packet of<br>Data Packet Packet Data<br>SoT PH Data PF EoT LPS SoT FE EoT LPS SoT FS EoT LPS SoT PH Data PF EoT<br>Long Packet Long Packet<br>Frame Blanking<br>**----- End of picture text -----**<br>


- 815 

**KEY** : SoT – Start of Transmission EoT – End of Transmission LPS – Low Power State PH – Packet Header PF – Packet Footer + Filler (if applicable) FS – Frame Start FE – Frame End LS – Line Start LE – Line End 

**Figure 58 Line and Frame Blanking Definitions** 

- 816 The period between the end of the Packet Footer (or the Packet Filler, if present) of one long packet and the 817 Packet Header of the next long packet is called the Line Blanking Period. 

- 818 The period between the Frame End packet in frame N and the Frame Start packet in frame N+1 is called the 819 Frame Blanking Period (Figure 58). 

- 820 The Line Blanking Period is not fixed and may vary in length. The receiver should be able to cope with a 821 near zero Line Blanking Period as defined by the minimum inter-packet spacing defined in [MIPI01] or 822 [MIPI02], as appropriate. The transmitter defines the minimum time for the Frame Blanking Period. The 823 Frame Blanking Period duration should be programmable in the transmitter. 

- 824 Frame Start and Frame End packets shall be used. 

- 825 Recommendations (informative) for frame start and end packet spacing: 

- 826 • The Frame Start packet to first data packet spacing should be as close as possible to the minimum 827 packet spacing 

- 828 • The last data packet to Frame End packet spacing should be as close as possible to the minimum 829 packet spacing 

- 830 The intention is to ensure that the Frame Start and Frame End packets accurately denote the start and end of 831 a frame of image data. A valid exception is when the positions of the Frame Start and Frame End packets 832 are being used to convey pixel level accurate vertical synchronization timing information. 

- 833 The positions of the Frame Start and Frame End packets can be varied within the Frame Blanking Period in 834 order to provide pixel level accurate vertical synchronization timing information. See Figure 59. 

- 835 Line Start and Line End packets shall be used for pixel level accurate horizontal synchronization timing 836 information. 

- 837 The positions of the Line Start and Line End packets, if present, can be varied within the Line Blanking 838 Period in order to provide pixel accurate horizontal synchronization timing information. See Figure 60. 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

59 

Specification for CSI-2 

Version 1.3 29-May-2014 

**==> picture [466 x 216] intentionally omitted <==**

**----- Start of picture text -----**<br>
VIDEO<br>DATA<br>Black Level<br>Blanking Level<br>Sync Level<br>DVALID<br>VVALID<br>SoT FE EoT LPS SoT FS EoT LPS SoT PH Data PF EoT LPS SoT PH Data PF EoT<br>Frame End  Frame Start  Valid Video Data Valid Video Data<br>839  Packet Packet<br>**----- End of picture text -----**<br>


**Figure 59 Vertical Sync Example** 

**==> picture [466 x 186] intentionally omitted <==**

**----- Start of picture text -----**<br>
VIDEO<br>DATA<br>Black Level<br>Blanking Level<br>Sync Level<br>DVALID<br>HVALID<br>PF EoT LPS SoT LE EoT LPS SoT LS EoT LPS SoT PH Data PF EoT LPS SoT LE EoT<br>Line End  Line Start  Valid Video Data Line End<br>840  Packet Packet Packet<br>**----- End of picture text -----**<br>


**Figure 60 Horizontal Sync Example** 

## 841 **9.11 Packet Data Payload Size Rules** 

- 842 For YUV, RGB or RAW data types, one long packet shall contain one line of image data. Each long packet 

- 843 of the same Data Type shall have equal length when packets are within the same Virtual Channel and when 844 packets are within the same frame. An exception to this rule is the YUV420 data type which is defined in 845 Section 11.2.2. 

- 846 For User Defined Byte-based Data Types, long packets can have arbitrary length. The spacing between 847 packets can also vary. 

- 848 The total size of payload data within a long packet for all data types shall be a multiple of eight bits. 849 However, it is also possible that a data type's payload data transmission format, as defined elsewhere in this 850 Specification, imposes additional constraints on payload size. In order to meet these constraints it may 851 sometimes be necessary to add some number of "padding" pixels to the end of a payload e.g., when a 852 packet with the RAW10 data type contains an image line whose length is not a multiple of four pixels as 

Copyright © 2005-2014 MIPI Alliance, Inc. 

60 

All rights reserved. **Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

- 853 required by the RAW10 transmission format as described in Section 11.4.4. The values of such padding 854 pixels are not specified. 

- 855 **9.12 Frame Format Examples** 

- 856 This is an informative section. 

- 857 This section contains three examples to illustrate how the CSI-2 features can be used. 

- 858 • General Frame Format Example, Figure 61 

- 859 • Digital Interlaced Video Example, Figure 62 

- 860 • Digital Interlaced Video with accurate synchronization timing information, Figure 63 

**==> picture [271 x 388] intentionally omitted <==**

**----- Start of picture text -----**<br>
Frame Blanking<br>FS Zero or more lines of embedded data<br>Line Blanking Frame of Arbitrary Pixel and/or User-<br>Defined Byte-Based Data<br>Zero or more lines of embedded data<br>FE<br>Frame Blanking<br>FS Zero or more lines of embedded data<br>Frame of Arbitrary Pixel and/or User-<br>Line Blanking<br>Defined Byte-Based Data<br>Zero or more lines of embedded data<br>FE<br>Frame Blanking<br>Data per line is a multiple of 8-bits<br>KEY :<br>PH – Packet Header PF – Packet Footer + Filler (if applicable)<br>FS – Frame Start  FE – Frame End<br>LS – Line Start  LE – Line End<br>Packet Header, PH<br>Packet Footer, PF<br>Packet Header, PH<br>Packet Footer, PF<br>**----- End of picture text -----**<br>


861 

**Figure 61 General Frame Format Example** 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

61 

Specification for CSI-2 

Version 1.3 

29-May-2014 

**==> picture [244 x 351] intentionally omitted <==**

**----- Start of picture text -----**<br>
Blanking Lines<br>FS<br>Frame 1<br>Line Blanking (Odd, Frame Number = 1)<br>YUV422 Image Data<br>FE<br>Blanking Lines<br>FS<br>Frame 2<br>Line Blanking (Even, Frame Number = 2)<br>YUV422 Image Data<br>FE<br>Blanking Lines<br>Data per line is a multiple of 16-bits (YUV422)<br>Packet Footer, PF Packet Header, PH<br>**----- End of picture text -----**<br>


**==> picture [273 x 34] intentionally omitted <==**

**----- Start of picture text -----**<br>
KEY :<br>PH – Packet Header PF – Packet Footer + Filler (if applicable)<br>FS – Frame Start  FE – Frame End<br>LS – Line Start  LE – Line End<br>**----- End of picture text -----**<br>


**Figure 62 Digital Interlaced Video Example** 

862 

Copyright © 2005-2014 MIPI Alliance, Inc. 

62 

All rights reserved. **Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

**==> picture [244 x 351] intentionally omitted <==**

**----- Start of picture text -----**<br>
Blanking Lines<br>FS<br>Frame 1<br>(Odd, Frame Number = 1)<br>YUV422 Image Data<br>FE<br>Blanking Lines<br>FS<br>Frame 2<br>(Even, Frame Number = 2)<br>YUV422 Image Data<br>FE<br>Blanking Lines<br>Data per line is a multiple of 16-bits (YUV422)<br>Line Blanking<br>Line End, LE Line Start, LS<br>Packet Footer, PF Packet Header, PH<br>Line Blanking<br>**----- End of picture text -----**<br>


**KEY** : 

PH – Packet Header PF – Packet Footer + Filler (if applicable) FS – Frame Start FE – Frame End LS – Line Start LE – Line End 

## 863 

## **Figure 63 Digital Interlaced Video with Accurate Synchronization Timing Information** 

## 864 

## **9.13 Data Interleaving** 

- 865 The CSI-2 supports the interleaved transmission of different image data formats within the same video data 866 stream. 

- 867 There are two methods to interleave the transmission of different image data formats: 

- 868 • Data Type 

- 869 • Virtual Channel Identifier 

- 870 The preceding methods of interleaved data transmission can be combined in any manner. 

## 871 **9.13.1 Data Type Interleaving** 

- 872 The Data Type value uniquely defines the data format for that packet of data. The receiver uses the Data 

- 873 Type value in the packet header to de-multiplex data packets containing different data formats as illustrated 874 in Figure 64. Note, in the figure the Virtual Channel Identifier is the same in each Packet Header. 

- 875 The packet payload data format shall agree with the Data Type code in the Packet Header as follows: 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

63 

Specification for CSI-2 

Version 1.3 29-May-2014 

- 876 • For defined image data types – any non-reserved codes in the range 0x18 to 0x3F – only the single 877 corresponding MIPI-defined packet payload data format shall be considered correct 

- 878 • Reserved image data types – any reserved codes in the range 0x18 to 0x3F – shall not be used. No 879 packet payload data format shall be considered correct for reserved image data types 

- 880 • For generic long packet data types (codes 0x10 thru 0x17) and user-defined, byte-based (codes 881 0x30 – 0x37), any packet payload data format shall be considered correct 

- 882 • Generic long packet data types (codes 0x10 thru 0x17) and user-defined, byte-based (codes 0x30 – 883 0x37), should not be used with packet payloads that meet any MIPI image data format definition 

- 884 • Synchronization short packet data types (codes 0x00 thru 0x07) shall consist of only the header 885 and shall not include payload data bytes 

- 886 • Generic short packet data types (codes 0x08 thru 0x0F) shall consist of only the header and shall 887 not include payload data bytes 

- 888 Data formats are defined further in Section 11. 

889 

|Embedded Data<br>Embedded Data<br>Data Type 1 Image Data<br>Frame Start Packet|Embedded Data<br>Embedded Data<br>Data Type 1 Image Data<br>Frame Start Packet|Embedded Data<br>Embedded Data<br>Data Type 1 Image Data<br>Frame Start Packet|
|---|---|---|
|So|||
||||
|Data Type 1<br>Data Type 2<br>PF<br>PH<br>PF<br>PH<br>LPS<br>Data Type 1<br>PF<br>PH<br>SoT<br>EoT<br>SoT<br>LPS<br>EoT<br>EoT<br>SoT<br>LPS<br>Data Type 1 Image Data<br>Data Type 2 Image Data<br>Data Type 1 Image Data|||
||||
|FE<br>EoT<br>EoT<br>SoT<br>LPS<br>Data Type 1<br>Data Type 2<br>PF<br>PH<br>PF<br>PH<br>SoT<br>LPS<br>EoT<br>SoT<br>LPS<br>Frame End Packet<br>Data Type 2 Image Data<br>Data Type 1 Image Data|||
|**KEY**:<br>LPS – Low Power State<br>FS – Frame Start Packet<br>PH – Packet Header<br>SoT – Start of Transmission<br>FE – Frame End Packet<br>PF – Packet Footer + Filler (if applicable)<br>EoT – End of Transmission|||



## **Figure 64 Interleaved Data Transmission using Data Type Value** 

- 890 All of the packets within the same virtual channel, independent of the Data Type value, share the same 891 frame start/end and line start/end synchronization information. By definition, all of the packets, 892 independent of data type, between a Frame Start and a Frame End packet within the same virtual channel 893 belong to the same frame. 

- 894 Packets of different data types may be interleaved at either the packet level as illustrated in Figure 65 or the 895 frame level as illustrated in Figure 66. Data formats are defined in Section 11. 

Copyright © 2005-2014 MIPI Alliance, Inc. 

64 

All rights reserved. 

**Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

**==> picture [365 x 545] intentionally omitted <==**

**----- Start of picture text -----**<br>
FS ED Zero or more lines of Embedded Data PF<br>D1  Data Type 1 Image Data PF<br>D2  Data Type 2 Image Data PF<br>D1  Data Type 1 Image Data PF<br>Line<br>Blanking<br>D2  Data Type 2 Image Data PF<br>D1  Data Type 1 Image Data PF<br>ED Zero or more lines of Embedded Data PF FE<br>Frame Blanking<br>FS ED Zero or more lines of Embedded Data PF<br>D1  Data Type 1 Image Data PF<br>Line<br>Blanking<br>D2  Data Type 2 Image Data PF<br>ED Zero or more lines of Embedded Data PF FE<br>Frame Blanking<br>Data Type 1 Payload Size<br>Data Type 2 Payload Size<br>Embedded Data Payload Size<br>**----- End of picture text -----**<br>


## **KEY** : 

LPS – Low Power State FS – Frame Start FE – Frame End 

ED – Packet Header containing Embedded Data type code D1 – Packet Header containing Data Type 1 Image Data Code D2 – Packet Header containing Data Type 2 Image Data Code PF – Packet Footer + Filler (if applicable) 

## **Figure 65 Packet Level Interleaved Data Transmission** 

896 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

65 

Specification for CSI-2 

Version 1.3 29-May-2014 

**==> picture [365 x 483] intentionally omitted <==**

**----- Start of picture text -----**<br>
FS ED Zero or more lines of Embedded Data PF<br>Line<br>D1  Data Type 1 Image Data PF<br>Blanking<br>ED Zero or more lines of Embedded Data PF FE<br>Frame Blanking<br>FS ED Zero or more lines of Embedded Data PF<br>Line<br>D2  Data Type 2 Image Data PF<br>Blanking<br>ED Zero of more lines of Embedded Data PF FE<br>Frame Blanking<br>Data Type 1 Payload Size<br>Data Type 2 Payload Size<br>Embedded Data Payload Size<br>**----- End of picture text -----**<br>


## **KEY** : 

897 

LPS – Low Power State ED – Packet Header containing Embedded Data type code FS – Frame Start D1 – Packet Header containing Data Type 1 Image Data Code FE – Frame End D2 – Packet Header containing Data Type 2 Image Data Code PF – Packet Footer + Filler (if applicable) 

## **Figure 66 Frame Level Interleaved Data Transmission** 

## 898 **9.13.2 Virtual Channel Identifier Interleaving** 

- 899 The Virtual Channel Identifier allows different data types within a single data stream to be logically 900 separated from each other. Figure 67 illustrates data interleaving using the Virtual Channel Identifier. 

Copyright © 2005-2014 MIPI Alliance, Inc. 

66 

All rights reserved. **Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

- 901 Each virtual channel has its own Frame Start and Frame End packet. Therefore, it is possible for different 902 virtual channels to have different frame rates, though the data rate for both channels would remain the 903 same. 

- 904 In addition, Data Type value Interleaving can be used for each virtual channel, allowing different data types 905 within a virtual channel and a second level of data interleaving. 

- 906 Therefore, receivers should be able to de-multiplex different data packets based on the combination of the 907 Virtual Channel Identifier and the Data Type value. For example, data packets containing the same Data 908 Type value but transmitted on different virtual channels are considered to belong to different frames 909 (streams) of image data. 

||Frame Start Packet|Frame Start Packet|Embedded|Embedded|Embedded|Data|Data||Frame Start Packet|Frame Start Packet|Embedded Data|||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||Virtual Channel 0||Virtual Channel 0||||||Virtual Channel 1||Virtual Channel 1|||
||SoT<br>EoT<br>LPS<br>FS<br>SoT<br>Embedded<br>PH|||||Data||EoT<br>SoT<br>LPS<br>PF<br>EoT<br>FS||Embedded Data<br>PH<br>SoT<br>LPS|||EoT<br>PF|
||Data||Type 1 Image|Data|||||Data Type 2 Image Data||Data Type|1 Image|Data|
||Virtual Channel 0||||||||Virtual Channel 1||Virtual Channel 0|||
||LPS<br>PH<br>SoT||Data Type 1|PF|EoT|LPS||PH<br>SoT|Data Type 2||Data<br>PF<br>PH<br>EoT<br>SoT<br>LPS|Type 1|PF<br>EoT|
||||Data Type 2 Image Data|||||Frame End Packet|||Data Type 1 Image Data|Frame End Packet||
||||Virtual Channel||1||||Virtual Channel 1||Virtual Channel 0|Virtual Channel 0||
||PH<br>SoT<br>LPS||Data Type 2||||PF|EoT<br>LPS<br>FE<br>EoT<br>SoT<br>LPS||EoT<br>Data Type 1<br>PF<br>PH<br>SoT||FE<br>EoT<br>SoT<br>LPS||
||**KEY**:|||||||||||||
||LPS – Low Power State|||||||FS – Frame Start Packet|||PH – Packet Header|||
||SoT – Start of||Transmission|||||FE – Frame End Packet|||PF – Packet Footer + Filler (if applicable)|||
|910|EoT – End of|Transmission||||||||||||



**Figure 67 Interleaved Data Transmission using Virtual Channels** 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

67 

Specification for CSI-2 

Version 1.3 29-May-2014 

## 911 

## **10 Color Spaces** 

- 912 The color space definitions in this section are simply references to other standards. The references are 913 included only for informative purposes and not for compliance. The color space used is not limited to the 914 references given. 

- 915 

## **10.1 RGB Color Space Definition** 

- 916 In this Specification, the abbreviation RGB means the nonlinear sR'G'B' color space in 8-bit representation 917 based on the definition of sRGB in IEC 61966. 

- 918 The 8-bit representation results as RGB888. The conversion to the more commonly used RGB565 format is 

- 919 achieved by scaling the 8-bit values to five bits (blue and red) and six bits (green). The scaling can be done 920 either by simply dropping the LSBs or rounding. 

- 921 

## **10.2 YUV Color Space Definition** 

- 922 In this Specification, the abbreviation YUV refers to the 8-bit gamma corrected Y'CBCR color space 923 defined in ITU-R BT601.4. 

Copyright © 2005-2014 MIPI Alliance, Inc. 

68 

All rights reserved. **Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

## 924 

## **11 Data Formats** 

925 The intent of this section is to provide a definitive reference for data formats typically used in CSI-2 926 applications. Table 8 summarizes the formats, followed by individual definitions for each format. Generic 927 data types not shown in the table are described in Section 11.1. For simplicity, all examples are single Lane 928 configurations. 

- 929 The formats most widely used in CSI-2 applications are distinguished by a “primary” designation in Table 930 8. Transmitter implementations of CSI-2 should support at least one of these primary formats. Receiver 931 implementations of CSI-2 should support all of the primary formats. 

- 932 The packet payload data format shall agree with the Data Type value in the Packet Header. See Section 9.4 933 for a description of the Data Type values. 

934 

**Table 8 Primary and Secondary Data Formats Definitions** 

|**Data Format**|**Primary**|**Secondary**|
|---|---|---|
|YUV420 8-bit (legacy)||S|
|YUV420 8-bit||S|
|YUV420 10-bit||S|
|YUV420 8-bit (CSPS)||S|
|YUV420 10-bit (CSPS)||S|
|YUV422 8-bit|P||
|YUV422 10-bit||S|
|RGB888|P||
|RGB666||S|
|RGB565|P||
|RGB555||S|
|RGB444||S|
|RAW6||S|
|RAW7||S|
|RAW8|P||
|RAW10|P||
|RAW12||S|
|RAW14||S|
|Generic 8-bit Long Packet Data Types|P||
|User Defined Byte-based Data (Note 1)|P||



## _**Note:**_ 

   _1. Compressed image data should use the user defined, byte-based data type codes_ 

- 935 For clarity the Start of Transmission and End of Transmission sequences in the figures in this section have 936 been omitted. 

- 937 The balance of this section details how sequences of pixels and other application data conforming to each 938 of the data types listed in Table 8 are converted into equivalent byte sequences by the CSI-2 Pixel to Byte 939 Packing Formats layer shown in Figure 3. 

- 940 Various figures in this section depict these byte sequences as shown at the top of Figure 68, where Byte n 941 always precedes Byte m for n < m. Also note that even though each byte is shown in LSB-first order, this is 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

69 

Specification for CSI-2 

Version 1.3 

29-May-2014 

- 942 not meant to imply that the bytes themselves are bit-reversed by the Pixel to Byte Packing Formats layer 943 prior to output. 

- 944 For the D-PHY physical layer option, each byte in the sequence is serially transmitted LSB-first, whereas 945 for the C-PHY physical layer option, successive byte pairs in the sequence are encoded and then serially 946 transmitted LSS-first. Figure 68 illustrates these options for a single-Lane system. 

## 947 

**==> picture [431 x 112] intentionally omitted <==**

**----- Start of picture text -----**<br>
||||||||||||||||||||||||||||||||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Formatted Pixel/Application Data Bytes Generated By Upper CSI-2 Layers|
|(b0 = Least Significant Bit)|
|D-PHY Physical Layer|Byte n*|Byte n+1|Byte n+2|Byte n+3|
|serializes each byte|b0|b1|b2|b3|b4|b5|b6|b7|b0|b1|b2|b3|b4|b5|b6|b7|b0|b1|b2|b3|b4|b5|b6|b7|b0|b1|b2|b3|b4|b5|b6|b7|
|and transmits it least|
|significant bit first|
|C-PHY Physical Layer|B0|C-PHY 16 bit to 7 Symbol Mapper|B15|B0|C-PHY 16 bit to 7 Symbol Mapper|B15|
|Mapper composes 7|
|(B0 = Input LSB, S0 = Output LSS)|(B0 = Input LSB, S0 = Output LSS)|
|symbols from 16-bit|
|word and transmits|S0|S1|S2|S3|S4|S5|S6|S0|S1|S2|S3|S4|S5|S6|
|least significant symbol|* For the C-PHY physical layer option, n = 2k, for k = 0, 1, 2, ...|
|first|

**----- End of picture text -----**<br>


## **Figure 68 Byte Packing Pixel Data to C-PHY Symbol Illustration** 

## 948 **11.1 Generic 8-bit Long Packet Data Types** 

- 949 Table 9 defines the generic 8-bit Long packet data types. 

950 **Table 9 Generic 8-bit Long Packet Data Types** 

**==> picture [444 x 140] intentionally omitted <==**

**----- Start of picture text -----**<br>
|||
|---|---|
|Data Type|Description|
|0x10|Null|
|0x11|Blanking Data|
|0x12|Embedded 8-bit non Image Data|
|0x13|Reserved|
|0x14|Reserved|
|0x15|Reserved|
|0x16|Reserved|
|0x17|Reserved|

**----- End of picture text -----**<br>


## 951 **11.1.1 Null and Blanking Data** 

- 952 For both the null and blanking data types the receiver must ignore the content of the packet payload data. 

- 953 A blanking packet differs from a null packet in terms of its significance within a video data stream. A null 954 packet has no meaning whereas the blanking packet may be used, for example, as the blanking lines 955 between frames in an ITU-R BT.656 style video stream. 

## 956 **11.1.2 Embedded Information** 

- 957 It is possible to embed extra lines containing additional information to the beginning and to the end of each 958 picture frame as presented in the Figure 69. If embedded information exists, then the lines containing the 959 embedded data must use the embedded data code in the data identifier. 

- 960 There may be zero or more lines of embedded data at the start of the frame. These lines are termed the 961 frame header. 

- 962 There may be zero or more line of embedded data at the end of the frame. These lines are termed the frame 963 footer. 

Copyright © 2005-2014 MIPI Alliance, Inc. 

70 

All rights reserved. 

**Confidential** 

Version 1.3 

Specification for CSI-2 

29-May-2014 

**==> picture [344 x 238] intentionally omitted <==**

**----- Start of picture text -----**<br>
FS Zero or more lines of Embedded Data<br>Frame of Arbitrary Pixel and/or  Line<br>User-Defined Byte-Based Data  Blanking<br>Zero or more lines of Embedded Data FE<br>Frame Blanking<br>CS (Checksum)<br>PH (Packet Header)<br>(and Filler if required for C-PHY)<br>**----- End of picture text -----**<br>


Payload Data per packet must be a multiple of 8-bits 

**KEY** : 

LPS – Low Power State DI – Data Identifier WC – Word Count ECC – Error Correction Code CS – Checksum FS – Frame Start FE – Frame End LS – Line Start LE – Line End 

## 964 

## **Figure 69 Frame Structure with Embedded Data at the Beginning and End of the Frame** 

- 965 **11.2 YUV Image Data** 

- 966 Table 10 defines the data type codes for YUV data formats described in this section. The number of lines 967 transmitted for the YUV420 data type shall be even. 

- 968 YUV420 data formats are divided into legacy and non-legacy data formats. The legacy YUV420 data 

- 969 format is for compatibility with existing systems. The non-legacy YUV420 data formats enable lower cost 970 implementations. 

971 

**Table 10 YUV Image Data Types** 

|**Data Type**|**Description**|
|---|---|
|0x18|YUV420 8-bit|
|0x19|YUV420 10-bit|
|0x1A|Legacy YUV420 8-bit|
|0x1B|Reserved|
|0x1C|YUV420 8-bit (Chroma Shifted Pixel Sampling)|
|0x1D|YUV420 10-bit (Chroma Shifted Pixel Sampling)|
|0x1E|YUV422 8-bit|
|0x1F|YUV422 10-bit|



Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

71 

Specification for CSI-2 

Version 1.3 

29-May-2014 

## 972 **11.2.1 Legacy YUV420 8-bit** 

- 973 Legacy YUV420 8-bit data transmission is performed by transmitting UYY… / VYY… sequences in odd / 974 even lines. U component is transferred in odd lines (1, 3, 5 …) and V component is transferred in even lines 975 (2, 4, 6 …). This sequence is illustrated in Figure 70. 

- 976 Table 11 specifies the packet size constraints for YUV420 8-bit packets. Each packet must be a multiple of 977 the values in the table. 

## 978 **Table 11 Legacy YUV420 8-bit Packet Data Size Constraints** 

|979<br>980<br>981|**Pixels**|**Bytes**|**Bits**|
|---|---|---|---|
||2|3|24|
||Bit order in transmission follows the general CSI-2 rule, LSB first. The pixel to byte mapping is illustrated<br>in Figure 71.<br>**U1[7:0]**<br>Packet Header<br>Packet Footer<br>Y640[7:0]<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**U3[7:0]**<br>Y639[7:0]<br>**_V639[7:0]_**<br>Y638[7:0]<br>Line Start:<br>(Odd line)<br>Line Start:<br>(Even Line)<br>Packet Header<br>Y1[7:0]<br>**_V3[7:0]_**<br>Y2[7:0]<br>Line End:<br>(Even Line)<br>Y3[7:0]<br>Y3[7:0]<br>Y637[7:0]<br>Y4[7:0]<br>Y4[7:0]<br>**_V637[7:0]_**<br>Packet Footer<br>Y640[7:0]<br>Y639[7:0]<br>**U639[7:0]**<br>Y638[7:0]<br>Line End:<br>(Odd Line)<br>Y637[7:0]<br>**U637[7:0]**|||



## **Figure 70 Legacy YUV420 8-bit Transmission** 

Copyright © 2005-2014 MIPI Alliance, Inc. 

72 

All rights reserved. 

**Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

982 

|Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>B0<br>B7 B0<br>B7 B0<br>B7<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**_V1[7:0]_**<br>Y1[7:0]<br>B7<br>B0 B7<br>B0 B7<br>B0<br>Pixel to Byte Data Packing<br>Data Transmitted LS Bit First<br>**Data**<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**Pixel Data**<br>**Byte Data**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**_V3[7:0]_**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**_V3[7:0]_**<br>Y2[7:0]<br>Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>**_V0_**<br>**_V1_**<br>**_V2_**<br>**_V3_**<br>**_V4_**<br>**_V5_**<br>**_V6_**<br>**_V7_**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>B0<br>B7 B0<br>B7 B0<br>B7<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**_V1[7:0]_**<br>Y1[7:0]<br>B7<br>B0 B7<br>B0 B7<br>B0<br>Pixel to Byte Data Packing<br>Data Transmitted LS Bit First<br>**Data**<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**Pixel Data**<br>**Byte Data**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**_V3[7:0]_**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**_V3[7:0]_**<br>Y2[7:0]<br>Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>**_V0_**<br>**_V1_**<br>**_V2_**<br>**_V3_**<br>**_V4_**<br>**_V5_**<br>**_V6_**<br>**_V7_**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>B0<br>B7 B0<br>B7 B0<br>B7<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**_V1[7:0]_**<br>Y1[7:0]<br>B7<br>B0 B7<br>B0 B7<br>B0<br>Pixel to Byte Data Packing<br>Data Transmitted LS Bit First<br>**Data**<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**Pixel Data**<br>**Byte Data**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**_V3[7:0]_**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**_V3[7:0]_**<br>Y2[7:0]<br>Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>**_V0_**<br>**_V1_**<br>**_V2_**<br>**_V3_**<br>**_V4_**<br>**_V5_**<br>**_V6_**<br>**_V7_**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>B0<br>B7 B0<br>B7 B0<br>B7<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**_V1[7:0]_**<br>Y1[7:0]<br>B7<br>B0 B7<br>B0 B7<br>B0<br>Pixel to Byte Data Packing<br>Data Transmitted LS Bit First<br>**Data**<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**Pixel Data**<br>**Byte Data**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**_V3[7:0]_**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**_V3[7:0]_**<br>Y2[7:0]<br>Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>**_V0_**<br>**_V1_**<br>**_V2_**<br>**_V3_**<br>**_V4_**<br>**_V5_**<br>**_V6_**<br>**_V7_**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>B0<br>B7 B0<br>B7 B0<br>B7<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**_V1[7:0]_**<br>Y1[7:0]<br>B7<br>B0 B7<br>B0 B7<br>B0<br>Pixel to Byte Data Packing<br>Data Transmitted LS Bit First<br>**Data**<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**Pixel Data**<br>**Byte Data**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**_V3[7:0]_**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**_V3[7:0]_**<br>Y2[7:0]<br>Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>**_V0_**<br>**_V1_**<br>**_V2_**<br>**_V3_**<br>**_V4_**<br>**_V5_**<br>**_V6_**<br>**_V7_**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>B0<br>B7 B0<br>B7 B0<br>B7<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**_V1[7:0]_**<br>Y1[7:0]<br>B7<br>B0 B7<br>B0 B7<br>B0<br>Pixel to Byte Data Packing<br>Data Transmitted LS Bit First<br>**Data**<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**Pixel Data**<br>**Byte Data**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**_V3[7:0]_**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**_V3[7:0]_**<br>Y2[7:0]<br>Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>**_V0_**<br>**_V1_**<br>**_V2_**<br>**_V3_**<br>**_V4_**<br>**_V5_**<br>**_V6_**<br>**_V7_**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>B0<br>B7 B0<br>B7 B0<br>B7<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**_V1[7:0]_**<br>Y1[7:0]<br>B7<br>B0 B7<br>B0 B7<br>B0<br>Pixel to Byte Data Packing<br>Data Transmitted LS Bit First<br>**Data**<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**Pixel Data**<br>**Byte Data**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**_V3[7:0]_**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**_V3[7:0]_**<br>Y2[7:0]<br>Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>**_V0_**<br>**_V1_**<br>**_V2_**<br>**_V3_**<br>**_V4_**<br>**_V5_**<br>**_V6_**<br>**_V7_**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>B0<br>B7 B0<br>B7 B0<br>B7<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**_V1[7:0]_**<br>Y1[7:0]<br>B7<br>B0 B7<br>B0 B7<br>B0<br>Pixel to Byte Data Packing<br>Data Transmitted LS Bit First<br>**Data**<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**Pixel Data**<br>**Byte Data**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**_V3[7:0]_**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**_V3[7:0]_**<br>Y2[7:0]<br>Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>**_V0_**<br>**_V1_**<br>**_V2_**<br>**_V3_**<br>**_V4_**<br>**_V5_**<br>**_V6_**<br>**_V7_**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>B0<br>B7 B0<br>B7 B0<br>B7<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**_V1[7:0]_**<br>Y1[7:0]<br>B7<br>B0 B7<br>B0 B7<br>B0<br>Pixel to Byte Data Packing<br>Data Transmitted LS Bit First<br>**Data**<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**Pixel Data**<br>**Byte Data**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**_V3[7:0]_**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**_V3[7:0]_**<br>Y2[7:0]<br>Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>**_V0_**<br>**_V1_**<br>**_V2_**<br>**_V3_**<br>**_V4_**<br>**_V5_**<br>**_V6_**<br>**_V7_**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>B0<br>B7 B0<br>B7 B0<br>B7<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**_V1[7:0]_**<br>Y1[7:0]<br>B7<br>B0 B7<br>B0 B7<br>B0<br>Pixel to Byte Data Packing<br>Data Transmitted LS Bit First<br>**Data**<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**Pixel Data**<br>**Byte Data**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**_V3[7:0]_**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**_V3[7:0]_**<br>Y2[7:0]<br>Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>**_V0_**<br>**_V1_**<br>**_V2_**<br>**_V3_**<br>**_V4_**<br>**_V5_**<br>**_V6_**<br>**_V7_**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>B0<br>B7 B0<br>B7 B0<br>B7<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**_V1[7:0]_**<br>Y1[7:0]<br>B7<br>B0 B7<br>B0 B7<br>B0<br>Pixel to Byte Data Packing<br>Data Transmitted LS Bit First<br>**Data**<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**Pixel Data**<br>**Byte Data**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**_V3[7:0]_**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**_V3[7:0]_**<br>Y2[7:0]<br>Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>**_V0_**<br>**_V1_**<br>**_V2_**<br>**_V3_**<br>**_V4_**<br>**_V5_**<br>**_V6_**<br>**_V7_**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>B0<br>B7 B0<br>B7 B0<br>B7<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**_V1[7:0]_**<br>Y1[7:0]<br>B7<br>B0 B7<br>B0 B7<br>B0<br>Pixel to Byte Data Packing<br>Data Transmitted LS Bit First<br>**Data**<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**Pixel Data**<br>**Byte Data**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**_V3[7:0]_**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**_V3[7:0]_**<br>Y2[7:0]<br>Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>**_V0_**<br>**_V1_**<br>**_V2_**<br>**_V3_**<br>**_V4_**<br>**_V5_**<br>**_V6_**<br>**_V7_**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>B0<br>B7 B0<br>B7 B0<br>B7<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**_V1[7:0]_**<br>Y1[7:0]<br>B7<br>B0 B7<br>B0 B7<br>B0<br>Pixel to Byte Data Packing<br>Data Transmitted LS Bit First<br>**Data**<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**Pixel Data**<br>**Byte Data**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**_V3[7:0]_**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**_V3[7:0]_**<br>Y2[7:0]<br>Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>**_V0_**<br>**_V1_**<br>**_V2_**<br>**_V3_**<br>**_V4_**<br>**_V5_**<br>**_V6_**<br>**_V7_**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>B0<br>B7 B0<br>B7 B0<br>B7<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**_V1[7:0]_**<br>Y1[7:0]<br>B7<br>B0 B7<br>B0 B7<br>B0<br>Pixel to Byte Data Packing<br>Data Transmitted LS Bit First<br>**Data**<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**Pixel Data**<br>**Byte Data**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**_V3[7:0]_**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**_V3[7:0]_**<br>Y2[7:0]<br>Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>**_V0_**<br>**_V1_**<br>**_V2_**<br>**_V3_**<br>**_V4_**<br>**_V5_**<br>**_V6_**<br>**_V7_**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>B0<br>B7 B0<br>B7 B0<br>B7<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**_V1[7:0]_**<br>Y1[7:0]<br>B7<br>B0 B7<br>B0 B7<br>B0<br>Pixel to Byte Data Packing<br>Data Transmitted LS Bit First<br>**Data**<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**Pixel Data**<br>**Byte Data**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**_V3[7:0]_**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**_V3[7:0]_**<br>Y2[7:0]<br>Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>**_V0_**<br>**_V1_**<br>**_V2_**<br>**_V3_**<br>**_V4_**<br>**_V5_**<br>**_V6_**<br>**_V7_**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>B0<br>B7 B0<br>B7 B0<br>B7<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**_V1[7:0]_**<br>Y1[7:0]<br>B7<br>B0 B7<br>B0 B7<br>B0<br>Pixel to Byte Data Packing<br>Data Transmitted LS Bit First<br>**Data**<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**Pixel Data**<br>**Byte Data**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**_V3[7:0]_**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**_V3[7:0]_**<br>Y2[7:0]<br>Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>**_V0_**<br>**_V1_**<br>**_V2_**<br>**_V3_**<br>**_V4_**<br>**_V5_**<br>**_V6_**<br>**_V7_**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>B0<br>B7 B0<br>B7 B0<br>B7<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**_V1[7:0]_**<br>Y1[7:0]<br>B7<br>B0 B7<br>B0 B7<br>B0<br>Pixel to Byte Data Packing<br>Data Transmitted LS Bit First<br>**Data**<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**Pixel Data**<br>**Byte Data**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**_V3[7:0]_**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**_V3[7:0]_**<br>Y2[7:0]<br>Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>**_V0_**<br>**_V1_**<br>**_V2_**<br>**_V3_**<br>**_V4_**<br>**_V5_**<br>**_V6_**<br>**_V7_**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>B0<br>B7 B0<br>B7 B0<br>B7<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**_V1[7:0]_**<br>Y1[7:0]<br>B7<br>B0 B7<br>B0 B7<br>B0<br>Pixel to Byte Data Packing<br>Data Transmitted LS Bit First<br>**Data**<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**Pixel Data**<br>**Byte Data**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**_V3[7:0]_**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**_V3[7:0]_**<br>Y2[7:0]<br>Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>**_V0_**<br>**_V1_**<br>**_V2_**<br>**_V3_**<br>**_V4_**<br>**_V5_**<br>**_V6_**<br>**_V7_**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>B0<br>B7 B0<br>B7 B0<br>B7<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**_V1[7:0]_**<br>Y1[7:0]<br>B7<br>B0 B7<br>B0 B7<br>B0<br>Pixel to Byte Data Packing<br>Data Transmitted LS Bit First<br>**Data**<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**Pixel Data**<br>**Byte Data**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**_V3[7:0]_**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**_V3[7:0]_**<br>Y2[7:0]<br>Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>**_V0_**<br>**_V1_**<br>**_V2_**<br>**_V3_**<br>**_V4_**<br>**_V5_**<br>**_V6_**<br>**_V7_**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>B0<br>B7 B0<br>B7 B0<br>B7<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**_V1[7:0]_**<br>Y1[7:0]<br>B7<br>B0 B7<br>B0 B7<br>B0<br>Pixel to Byte Data Packing<br>Data Transmitted LS Bit First<br>**Data**<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**Pixel Data**<br>**Byte Data**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**_V3[7:0]_**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**_V3[7:0]_**<br>Y2[7:0]<br>Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>**_V0_**<br>**_V1_**<br>**_V2_**<br>**_V3_**<br>**_V4_**<br>**_V5_**<br>**_V6_**<br>**_V7_**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>B0<br>B7 B0<br>B7 B0<br>B7<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**_V1[7:0]_**<br>Y1[7:0]<br>B7<br>B0 B7<br>B0 B7<br>B0<br>Pixel to Byte Data Packing<br>Data Transmitted LS Bit First<br>**Data**<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**Pixel Data**<br>**Byte Data**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**_V3[7:0]_**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**_V3[7:0]_**<br>Y2[7:0]<br>Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>**_V0_**<br>**_V1_**<br>**_V2_**<br>**_V3_**<br>**_V4_**<br>**_V5_**<br>**_V6_**<br>**_V7_**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>B0<br>B7 B0<br>B7 B0<br>B7<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**_V1[7:0]_**<br>Y1[7:0]<br>B7<br>B0 B7<br>B0 B7<br>B0<br>Pixel to Byte Data Packing<br>Data Transmitted LS Bit First<br>**Data**<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**Pixel Data**<br>**Byte Data**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**_V3[7:0]_**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**_V3[7:0]_**<br>Y2[7:0]<br>Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>**_V0_**<br>**_V1_**<br>**_V2_**<br>**_V3_**<br>**_V4_**<br>**_V5_**<br>**_V6_**<br>**_V7_**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>B0<br>B7 B0<br>B7 B0<br>B7<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**_V1[7:0]_**<br>Y1[7:0]<br>B7<br>B0 B7<br>B0 B7<br>B0<br>Pixel to Byte Data Packing<br>Data Transmitted LS Bit First<br>**Data**<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**Pixel Data**<br>**Byte Data**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**_V3[7:0]_**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**_V3[7:0]_**<br>Y2[7:0]<br>Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>**_V0_**<br>**_V1_**<br>**_V2_**<br>**_V3_**<br>**_V4_**<br>**_V5_**<br>**_V6_**<br>**_V7_**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>B0<br>B7 B0<br>B7 B0<br>B7<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**_V1[7:0]_**<br>Y1[7:0]<br>B7<br>B0 B7<br>B0 B7<br>B0<br>Pixel to Byte Data Packing<br>Data Transmitted LS Bit First<br>**Data**<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**Pixel Data**<br>**Byte Data**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**_V3[7:0]_**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**_V3[7:0]_**<br>Y2[7:0]<br>Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>**_V0_**<br>**_V1_**<br>**_V2_**<br>**_V3_**<br>**_V4_**<br>**_V5_**<br>**_V6_**<br>**_V7_**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>B0<br>B7 B0<br>B7 B0<br>B7<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**_V1[7:0]_**<br>Y1[7:0]<br>B7<br>B0 B7<br>B0 B7<br>B0<br>Pixel to Byte Data Packing<br>Data Transmitted LS Bit First<br>**Data**<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**Pixel Data**<br>**Byte Data**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**_V3[7:0]_**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**_V3[7:0]_**<br>Y2[7:0]<br>Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>**_V0_**<br>**_V1_**<br>**_V2_**<br>**_V3_**<br>**_V4_**<br>**_V5_**<br>**_V6_**<br>**_V7_**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>B7<br>B0 B7<br>B0 B7<br>B0<br>Pixel to Byte Data Packing<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**_V3[7:0]_**||||||||||||||||||||||||
||**_V1[7:0]_**||||||||Y1[7:0]||||||||Y2[7:0]||||||||
||B0<br>B7||||||||B0<br>B7 <br>Data Tran||||||||B0<br>B7<br>smitted LS Bit First||||||||
||**_V0_**|**_V1_**|**_V2_**|**_V3_**|**_V4_**|**_V5_**|**_V6_**|**_V7_**|Y0|Y1|Y2|Y3|Y4|Y5|Y6|Y7|Y0|Y1|Y2|Y3|Y4|Y5|Y6|Y7|
||Byte n||||||||Byte n+1||||||||Byte n+2||||||||
||b0|b1|b2|b3|b4|b5|b6|b7|b0|b1|b2|b3|b4|b5|b6|b7|b0|b1|b2|b3|b4|b5|b6|b7|



**Figure 71 Legacy YUV420 8-bit Pixel to Byte Packing Bitwise Illustration** 

983 There is one spatial sampling option 

984 • H.261, H.263 and MPEG1 Spatial Sampling (Figure 72). 

985 

**==> picture [324 x 223] intentionally omitted <==**

**----- Start of picture text -----**<br>
Y1 Y2 Y3 Y4 Y5 Y6 Y7 Y8<br>Line 1<br>Line 2<br>Line 3<br>Line 4<br>Line 5<br>Luminance Sample, Y Calculated Chrominance sample, Cb & Cr<br>**----- End of picture text -----**<br>


**Figure 72 Legacy YUV420 Spatial Sampling for H.261, H.263 and MPEG 1** 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

73 

Specification for CSI-2 

Version 1.3 

29-May-2014 

986 

|FS|Packet Header, PH|**U**|Y|Y|**U**|Y|Y|….|**U**|Y|Y|Packet Footer, PF||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|||**_V_**|Y|Y|**_V_**|Y|Y|….|**_V_**|Y|Y|||
|||**U**|Y|Y|**U**|Y|Y|….|**U**|Y|Y|||
|||**_V_**|Y|Y|**_V_**|Y|Y|….|**_V_**|Y|Y|||
|||**U**|Y|Y|**U**|Y|Y|….|**U**|Y|Y|||
|||**_V_**|Y|Y|**_V_**|Y|Y|….|**_V_**|Y|Y|||
|||**U**|Y|Y|**U**|Y|Y|….|**U**|Y|Y|||
|||**_V_**|Y|Y|**_V_**|Y|Y|….|**_V_**|Y|Y|||
|||**U**|Y|Y|**U**|Y|Y|….|**U**|Y|Y|||
|||**_V_**|Y|Y|**_V_**|Y|Y|….|**_V_**|Y|Y|||
|||**U**|Y|Y|**U**|Y|Y|….|**U**|Y|Y|||
|||**_V_**|Y|Y|**_V_**|Y|Y|….|**_V_**|Y|Y||FE|



**Figure 73 Legacy YUV420 8-bit Frame Format** 

## 987 **11.2.2 YUV420 8-bit** 

- 988 YUV420 8-bit data transmission is performed by transmitting YYYY… / UYVYUYVY… sequences in 

- 989 odd / even lines. Only the luminance component (Y) is transferred for odd lines (1, 3, 5…) and both 990 luminance (Y) and chrominance (U and V) components are transferred for even lines (2, 4, 6…). The 991 format for the even lines (UYVY) is identical to the YUV422 8-bit data format. The data transmission 992 sequence is illustrated in Figure 74. 

- 993 The payload data size, in bytes, for even lines (UYVY) is double the payload data size for odd lines (Y). 994 This is exception to the general CSI-2 rule that each line shall have an equal length. 

- 995 Table 12 specifies the packet size constraints for YUV420 8-bit packets. Each packet must be a multiple of 996 the values in the table. 

997 **Table 12 YUV420 8-bit Packet Data Size Constraints** 

|**Odd Lines (1, 3, 5...)**<br>**Luminance Only, Y**|**Odd Lines (1, 3, 5...)**<br>**Luminance Only, Y**|**Odd Lines (1, 3, 5...)**<br>**Luminance Only, Y**|**Even Lines (2, 4, 6…)**<br>**Luminance and Chrominance, UYVY**|**Even Lines (2, 4, 6…)**<br>**Luminance and Chrominance, UYVY**|**Even Lines (2, 4, 6…)**<br>**Luminance and Chrominance, UYVY**|
|---|---|---|---|---|---|
|**Pixels**|**Bytes**|**Bits**|**Pixels**|**Bytes**|**Bits**|
|2|2|16|2|4|32|
|Bit order in transmission follows the general CSI-2 rule, LSB first. The pixel to byte mapping is illustrated<br>in Figure 75.<br>**U1[7:0]**<br>Packet<br>Footer<br>Y640[7:0]<br>**_V1[7:0]_**<br>**U3[7:0]**<br>Y639[7:0]<br>**_V639[7:0]_**<br>Y638[7:0]<br>Packet<br>Header<br>Y1[7:0]<br>**_V3[7:0]_**<br>Y2[7:0]<br>Y3[7:0]<br>Y637[7:0]<br>**_V637[7:0]_**<br>**U639[7:0]**<br>Packet<br>Header<br>Y1[7:0]<br>Y2[7:0]<br>**Line Start:**<br>**(Odd line)**<br>**Line Start:**<br>**(Even Line)**<br>**Line End:**<br>**(Even Line)**<br>Y3[7:0]<br>Y4[7:0]<br>Packet<br>Footer<br>Y640[7:0]<br>Y639[7:0]<br>Y638[7:0]<br>**Line End:**<br>**(Odd Line)**<br>Y637[7:0]||||||



998 Bit order in transmission follows the general CSI-2 rule, LSB first. The pixel to byte mapping is illustrated 999 in Figure 75. 

1000 

## **Figure 74 YUV420 8-bit Data Transmission Sequence** 

Copyright © 2005-2014 MIPI Alliance, Inc. 

74 

All rights reserved. **Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

## **Odd lines:** 

|**Odd lines:**|**Odd lines:**|**Odd lines:**|**Odd lines:**|**Odd lines:**|**Odd lines:**|**Odd lines:**|**Odd lines:**|**Odd lines:**|**Odd lines:**|**Odd lines:**|**Odd lines:**|**Odd lines:**|**Odd lines:**|**Odd lines:**|**Odd lines:**|**Odd lines:**|**Odd lines:**|**Odd lines:**|**Odd lines:**|**Odd lines:**|**Odd lines:**|**Odd lines:**|**Odd lines:**|**Odd lines:**|**Odd lines:**|**Odd lines:**|**Odd lines:**|**Odd lines:**|**Odd lines:**|**Odd lines:**|**Odd lines:**|**Odd lines:**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Byte Values Transmitted LS Bit First<br>**Data**<br>Y2[7:0] (B)<br>B6<br>B7<br>B4<br>B5<br>B0<br>B1<br>**_C6_**<br>**_C7_**<br>**_C4_**<br>**_C5_**<br>**_C0_**<br>**_C1_**<br>Y3[7:0] (C)<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>Y4[7:0] (D)<br>D6<br>D7<br>D4<br>D5<br>D0<br>D1<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**_A6_**<br>**_A7_**<br>**_A4_**<br>**_A5_**<br>**_A0_**<br>**_A1_**<br>Y1[7:0] (A)<br>**_A2_**<br>**_A3_**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+3<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|||||||||||||||||||||||||||||||||
||||||||||||||||||||||||||||||||||
||**_A0_**|**_A1_**|**_A2_**|**_A3_**|**_A4_**|**_A5_**|**_A6_**|**_A7_**|B0|B1|B2|B3|B4|B5|B6|B7|**_C0_**|**_C1_**|**_C2_**|**_C3_**|**_C4_**|**_C5_**|**_C6_**|**_C7_**|D0|D1|D2|D3|D4|D5|D6|D7|
||~~8-bits~~<br>Byte n||||||||Byte Values Trans<br>~~8-bits~~<br>Byte n+1||||||||mitted LS Bit First<br>~~8-bits~~<br>Byte n+2||||||||~~8-bits~~<br>Byte n+3||||||||
||b0|b1|b2|b3|b4|b5|b6|b7|b0|b1|b2|b3|b4|b5|b6|b7|b0|b1|b2|b3|b4|b5|b6|b7|b0|b1|b2|b3|b4|b5|b6|b7|



## **Even lines:** 

1001 

|**Even lines:**|**Even lines:**|**Even lines:**|**Even lines:**|**Even lines:**|**Even lines:**|**Even lines:**|**Even lines:**|**Even lines:**|**Even lines:**|**Even lines:**|**Even lines:**|**Even lines:**|**Even lines:**|**Even lines:**|**Even lines:**|**Even lines:**|**Even lines:**|**Even lines:**|**Even lines:**|**Even lines:**|**Even lines:**|**Even lines:**|**Even lines:**|**Even lines:**|**Even lines:**|**Even lines:**|**Even lines:**|**Even lines:**|**Even lines:**|**Even lines:**|**Even lines:**|**Even lines:**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|B6<br>B7<br>B4<br>B5<br>B0<br>B1<br>**_C6_**<br>**_C7_**<br>**_C4_**<br>**_C5_**<br>**_C0_**<br>**_C1_**<br>D6<br>D7<br>D4<br>D5<br>D0<br>D1<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**A6**<br>**A7**<br>**A4**<br>**A5**<br>**A0**<br>**A1**<br>**A2**<br>**A3**<br>Byte Values Transmitted LS Bit First<br>**Data**<br>Y1[7:0] (B)<br>**_V1[7:0] (C)_**<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>Y2[7:0] (D)<br>**U1[7:0] (A)**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+3<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|||||||||||||||||||||||||||||||||
||||||||||||||||||||||||||||||||||
||**A0**|**A1**|**A2**|**A3**|**A4**|**A5**|**A6**|**A7**|B0|B1|B2|B3|B4|B5|B6|B7|**_C0_**|**_C1_**|**_C2_**|**_C3_**|**_C4_**|**_C5_**|**_C6_**|**_C7_**|D0|D1|D2|D3|D4|D5|D6|D7|
||~~8-bits~~<br>Byte n||||||||Byte Values Trans<br>~~8-bits~~<br>Byte n+1||||||||mitted LS Bit First<br>~~8-bits~~<br>Byte n+2||||||||~~8-bits~~<br>Byte n+3||||||||
||b0|b1|b2|b3|b4|b5|b6|b7|b0|b1|b2|b3|b4|b5|b6|b7|b0|b1|b2|b3|b4|b5|b6|b7|b0|b1|b2|b3|b4|b5|b6|b7|



## **Figure 75 YUV420 8-bit Pixel to Byte Packing Bitwise Illustration** 

1002 There are two spatial sampling options 1003 • H.261, H.263 and MPEG1 Spatial Sampling (Figure 76). 1004 • Chroma Shifted Pixel Sampling (CSPS) for MPEG2, MPEG4 (Figure 77). 1005 Figure 78 shows the YUV420 frame format. 

1006 

**==> picture [324 x 223] intentionally omitted <==**

**----- Start of picture text -----**<br>
Y1 Y2 Y3 Y4 Y5 Y6 Y7 Y8<br>Line 1<br>Line 2<br>Line 3<br>Line 4<br>Line 5<br>Luminance Sample, Y Calculated Chrominance sample, Cb & Cr<br>**----- End of picture text -----**<br>


**Figure 76 YUV420 Spatial Sampling for H.261, H.263 and MPEG 1** 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. 

75 

**Confidential** 

Specification for CSI-2 

Version 1.3 29-May-2014 

1007 

**==> picture [324 x 222] intentionally omitted <==**

**----- Start of picture text -----**<br>
Y1 Y2 Y3 Y4 Y5 Y6 Y7 Y8<br>Line 1<br>Line 2<br>Line 3<br>Line 4<br>Line 5<br>Luminance Sample, Y Calculated Chrominance sample, Cb & Cr<br>**----- End of picture text -----**<br>


**Figure 77 YUV420 Spatial Sampling for MPEG 2 and MPEG 4** 

1008 

|FS||Y|Y|Y|Y|….|Y||||**U**|Y|**_V_**|Y|**U**|Y|**_V_**|Y|….|**_V_**|Y|Packet Footer, PF||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||Packet Header, PH|Y|Y|Y|Y|….|Y||||**U**|Y|**_V_**|Y|**U**|Y|**_V_**|Y|….|**_V_**|Y|||
|||Y|Y|Y|Y|….|Y||||**U**|Y|**_V_**|Y|**U**|Y|**_V_**|Y|….|**_V_**|Y|||
|||Y|Y|Y|Y|….|Y|PF||PH|**U**|Y|**_V_**|Y|**U**|Y|**_V_**|Y|….|**_V_**|Y|||
|||Y|Y|Y|Y|….|Y|er,||er,|**U**|Y|**_V_**|Y|**U**|Y|**_V_**|Y|….|**_V_**|Y|||
|||Y|Y|Y|Y|….|Y|oot||ead|**U**|Y|**_V_**|Y|**U**|Y|**_V_**|Y|….|**_V_**|Y|||
|||Y|Y|Y|Y|….|Y|t F||t H|**U**|Y|**_V_**|Y|**U**|Y|**_V_**|Y|….|**_V_**|Y|||
|||Y|Y|Y|Y|….|Y|cke||cke|**U**|Y|**_V_**|Y|**U**|Y|**_V_**|Y|….|**_V_**|Y|||
|||Y|Y|Y|Y|….|Y|Pa||Pa|**U**|Y|**_V_**|Y|**U**|Y|**_V_**|Y|….|**_V_**|Y|||
|||Y|Y|Y|Y|….|Y||||**U**|Y|**_V_**|Y|**U**|Y|**_V_**|Y|….|**_V_**|Y|||
|||Y|Y|Y|Y|….|Y||||**U**|Y|**_V_**|Y|**U**|Y|**_V_**|Y|….|**_V_**|Y|||
|||Y|Y|Y|Y|….|Y||||**U**|Y|**_V_**|Y|**U**|Y|**_V_**|Y|….|**_V_**|Y||FE|
|**Odd lines (1, 3, 5, ..):**<br>Luminance only, Y<br>**Even lines (2, 4, 6, ..):**<br>Luminance and Chrominance, UYVY||||||||||||||||||||||||



**Figure 78 YUV420 8-bit Frame Format** 

1009 **11.2.3 YUV420 10-bit** 

1010 YUV420 10-bit data transmission is performed by transmitting YYYY… / UYVYUYVY… sequences in 1011 odd / even lines. Only the luminance component (Y) is transferred in odd lines (1, 3, 5…) and both 1012 luminance (Y) and chrominance (U and V) components transferred in even lines (2, 4, 6…). The format for 1013 the even lines (UYVY) is identical to the YUV422 –10-bit data format. The sequence is illustrated in 1014 Figure 79. 

1015 The payload data size, in bytes, for even lines (UYVY) is double the payload data size for odd lines (Y). 1016 This is exception to the general CSI-2 rule that each line shall have an equal length. 

1017 Table 13 specifies the packet size constraints for YUV420 10-bit packets. The length of each packet must 1018 be a multiple of the values in the table. 

Copyright © 2005-2014 MIPI Alliance, Inc. 

76 

All rights reserved. **Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

1019 

**Table 13 YUV420 10-bit Packet Data Size Constraints** 

|**Odd Lines (1, 3, 5...)**<br>**Luminance Only, Y**|**Odd Lines (1, 3, 5...)**<br>**Luminance Only, Y**|**Odd Lines (1, 3, 5...)**<br>**Luminance Only, Y**|**Even Lines (2, 4, 6…)**<br>**Luminance and Chrominance, UYVY**|**Even Lines (2, 4, 6…)**<br>**Luminance and Chrominance, UYVY**|**Even Lines (2, 4, 6…)**<br>**Luminance and Chrominance, UYVY**|
|---|---|---|---|---|---|
|**Pixels**|**Bytes**|**Bits**|**Pixels**|**Bytes**|**Bits**|
|4|5|40|4|10|80|



1020 Bit order in transmission follows the general CSI-2 rule, LSB first. The pixel-to-byte mapping is illustrated 1021 in Figure 80. 

|**U1[**9:2**]**<br>Packet<br>Footer<br>Y640[9:2]<br>**_V1[_**9:2**_]_**<br>**U3[**9:2**]**<br>Y639[9:2]<br>**_V639[_**9:2**_]_**<br>Packet<br>Header<br>Y1[9:2]<br>Y2[9:2]<br>**U639[**9:2**]**<br>Y2<br>[1:0]<br>**_V1_**<br>**_[1:0]_**<br>**U1**<br>**[1:0]**<br>Y1<br>[1:0]<br>Y640<br>[1:0]<br>**_V639_**<br>**_[1:0]_**<br>**U639**<br>**[1:0]**<br>Y639<br>[1:0]<br>Y638<br>[1:0]<br>**_V637_**<br>**_[1:0]_**<br>**U637**<br>**[1:0]**<br>Y637<br>[1:0]<br>LSB’s<br>Y4<br>[1:0]<br>Y3<br>[1:0]<br>Y2<br>[1:0]<br>Y1<br>[1:0]<br>Packet<br>Header<br>Y1[9:2]<br>Y2[9:2]<br>**Line Start:**<br>**(Odd line)**<br>**Line Start:**<br>**(Even Line)**<br>**Line End:**<br>**(Even Line)**<br>Y3[9:2]<br>Y4[9:2]<br>Packet<br>Footer<br>Y640[9:2]<br>Y639[9:2]<br>Y638[9:2]<br>**Line End:**<br>**(Odd Line)**<br>Y637[9:2]<br>LSB’s<br>Y640<br>[1:0]<br>_Y639_<br>_[1:0]_<br>Y637<br>[1:0]<br>Y638<br>[1:0]<br>LSB’s<br>LSB’s<br>LSB’s<br>1022<br>**Figure 79 YUV420 10-bit Transmission**<br>**_C6_**<br>**_C7_**<br>**_C4_**<br>**_C5_**<br>**_C8_**<br>**_C9_**<br>**A0**<br>**A1**<br>B0<br>B1<br>D6<br>D7<br>D4<br>D5<br>D8<br>D9<br>**_C0_**<br>**_C1_**<br>D0<br>D1<br>D2<br>D3<br>**_C2_**<br>**_C3_**<br>**_C6_**<br>**_C7_**<br>**_C4_**<br>**_C5_**<br>**_C8_**<br>**_C9_**<br>**A0**<br>**A1**<br>B0<br>B1<br>D6<br>D7<br>D4<br>D5<br>D8<br>D9<br>**_C0_**<br>**_C1_**<br>D0<br>D1<br>D2<br>D3<br>**_C2_**<br>**_C3_**<br>B6<br>B7<br>B4<br>B5<br>B8<br>B9<br>B2<br>B3<br>B6<br>B7<br>B4<br>B5<br>B8<br>B9<br>B2<br>B3<br>**_A6_**<br>**_A7_**<br>**_A4_**<br>**_A5_**<br>**_A8_**<br>**_A9_**<br>**_A2_**<br>**_A3_**<br>**_A6_**<br>**_A7_**<br>**_A4_**<br>**_A5_**<br>**_A8_**<br>**_A9_**<br>**_A2_**<br>**_A3_**<br>Y1<br>[1:0]<br>Y2<br>[1:0]<br>Byte Values Transmitted LS Bit First<br>Y3[9:2] (C)<br>Y4[9:2] (D)<br>Y3<br>[1:0]<br>Y4<br>[1:0]<br>Byte Values Transmitted LS Bit First<br>**Odd lines:**<br>**Data**<br>**Data**<br>**Even lines:**<br>Y1[9:2] (A)<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>**U1**<br>**[1:0]**<br>Y1<br>[1:0]<br>**_V1[9:2] (C)_**<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>Y2[9:2] (D)<br>**_V1_**<br>**_[1:0]_**<br>Y2<br>[1:0]<br>Y2[9:2] (B)<br>~~8-bits~~<br>Y1[9:2] (B)<br>~~8-bits~~<br>~~8-bits~~<br>**_U1[9:2] (A)_**<br>~~8-bits~~<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+3<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+4<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+3<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+4<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>1023|**U1[**9:2**]**<br>Packet<br>Footer<br>Y640[9:2]<br>**_V1[_**9:2**_]_**<br>**U3[**9:2**]**<br>Y639[9:2]<br>**_V639[_**9:2**_]_**<br>Packet<br>Header<br>Y1[9:2]<br>Y2[9:2]<br>**U639[**9:2**]**<br>Y2<br>[1:0]<br>**_V1_**<br>**_[1:0]_**<br>**U1**<br>**[1:0]**<br>Y1<br>[1:0]<br>Y640<br>[1:0]<br>**_V639_**<br>**_[1:0]_**<br>**U639**<br>**[1:0]**<br>Y639<br>[1:0]<br>Y638<br>[1:0]<br>**_V637_**<br>**_[1:0]_**<br>**U637**<br>**[1:0]**<br>Y637<br>[1:0]<br>LSB’s<br>Y4<br>[1:0]<br>Y3<br>[1:0]<br>Y2<br>[1:0]<br>Y1<br>[1:0]<br>Packet<br>Header<br>Y1[9:2]<br>Y2[9:2]<br>**Line Start:**<br>**(Odd line)**<br>**Line Start:**<br>**(Even Line)**<br>**Line End:**<br>**(Even Line)**<br>Y3[9:2]<br>Y4[9:2]<br>Packet<br>Footer<br>Y640[9:2]<br>Y639[9:2]<br>Y638[9:2]<br>**Line End:**<br>**(Odd Line)**<br>Y637[9:2]<br>LSB’s<br>Y640<br>[1:0]<br>_Y639_<br>_[1:0]_<br>Y637<br>[1:0]<br>Y638<br>[1:0]<br>LSB’s<br>LSB’s<br>LSB’s<br>1022<br>**Figure 79 YUV420 10-bit Transmission**<br>**_C6_**<br>**_C7_**<br>**_C4_**<br>**_C5_**<br>**_C8_**<br>**_C9_**<br>**A0**<br>**A1**<br>B0<br>B1<br>D6<br>D7<br>D4<br>D5<br>D8<br>D9<br>**_C0_**<br>**_C1_**<br>D0<br>D1<br>D2<br>D3<br>**_C2_**<br>**_C3_**<br>**_C6_**<br>**_C7_**<br>**_C4_**<br>**_C5_**<br>**_C8_**<br>**_C9_**<br>**A0**<br>**A1**<br>B0<br>B1<br>D6<br>D7<br>D4<br>D5<br>D8<br>D9<br>**_C0_**<br>**_C1_**<br>D0<br>D1<br>D2<br>D3<br>**_C2_**<br>**_C3_**<br>B6<br>B7<br>B4<br>B5<br>B8<br>B9<br>B2<br>B3<br>B6<br>B7<br>B4<br>B5<br>B8<br>B9<br>B2<br>B3<br>**_A6_**<br>**_A7_**<br>**_A4_**<br>**_A5_**<br>**_A8_**<br>**_A9_**<br>**_A2_**<br>**_A3_**<br>**_A6_**<br>**_A7_**<br>**_A4_**<br>**_A5_**<br>**_A8_**<br>**_A9_**<br>**_A2_**<br>**_A3_**<br>Y1<br>[1:0]<br>Y2<br>[1:0]<br>Byte Values Transmitted LS Bit First<br>Y3[9:2] (C)<br>Y4[9:2] (D)<br>Y3<br>[1:0]<br>Y4<br>[1:0]<br>Byte Values Transmitted LS Bit First<br>**Odd lines:**<br>**Data**<br>**Data**<br>**Even lines:**<br>Y1[9:2] (A)<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>**U1**<br>**[1:0]**<br>Y1<br>[1:0]<br>**_V1[9:2] (C)_**<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>Y2[9:2] (D)<br>**_V1_**<br>**_[1:0]_**<br>Y2<br>[1:0]<br>Y2[9:2] (B)<br>~~8-bits~~<br>Y1[9:2] (B)<br>~~8-bits~~<br>~~8-bits~~<br>**_U1[9:2] (A)_**<br>~~8-bits~~<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+3<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+4<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+3<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+4<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>1023|**U1[**9:2**]**<br>Packet<br>Footer<br>Y640[9:2]<br>**_V1[_**9:2**_]_**<br>**U3[**9:2**]**<br>Y639[9:2]<br>**_V639[_**9:2**_]_**<br>Packet<br>Header<br>Y1[9:2]<br>Y2[9:2]<br>**U639[**9:2**]**<br>Y2<br>[1:0]<br>**_V1_**<br>**_[1:0]_**<br>**U1**<br>**[1:0]**<br>Y1<br>[1:0]<br>Y640<br>[1:0]<br>**_V639_**<br>**_[1:0]_**<br>**U639**<br>**[1:0]**<br>Y639<br>[1:0]<br>Y638<br>[1:0]<br>**_V637_**<br>**_[1:0]_**<br>**U637**<br>**[1:0]**<br>Y637<br>[1:0]<br>LSB’s<br>Y4<br>[1:0]<br>Y3<br>[1:0]<br>Y2<br>[1:0]<br>Y1<br>[1:0]<br>Packet<br>Header<br>Y1[9:2]<br>Y2[9:2]<br>**Line Start:**<br>**(Odd line)**<br>**Line Start:**<br>**(Even Line)**<br>**Line End:**<br>**(Even Line)**<br>Y3[9:2]<br>Y4[9:2]<br>Packet<br>Footer<br>Y640[9:2]<br>Y639[9:2]<br>Y638[9:2]<br>**Line End:**<br>**(Odd Line)**<br>Y637[9:2]<br>LSB’s<br>Y640<br>[1:0]<br>_Y639_<br>_[1:0]_<br>Y637<br>[1:0]<br>Y638<br>[1:0]<br>LSB’s<br>LSB’s<br>LSB’s<br>1022<br>**Figure 79 YUV420 10-bit Transmission**<br>**_C6_**<br>**_C7_**<br>**_C4_**<br>**_C5_**<br>**_C8_**<br>**_C9_**<br>**A0**<br>**A1**<br>B0<br>B1<br>D6<br>D7<br>D4<br>D5<br>D8<br>D9<br>**_C0_**<br>**_C1_**<br>D0<br>D1<br>D2<br>D3<br>**_C2_**<br>**_C3_**<br>**_C6_**<br>**_C7_**<br>**_C4_**<br>**_C5_**<br>**_C8_**<br>**_C9_**<br>**A0**<br>**A1**<br>B0<br>B1<br>D6<br>D7<br>D4<br>D5<br>D8<br>D9<br>**_C0_**<br>**_C1_**<br>D0<br>D1<br>D2<br>D3<br>**_C2_**<br>**_C3_**<br>B6<br>B7<br>B4<br>B5<br>B8<br>B9<br>B2<br>B3<br>B6<br>B7<br>B4<br>B5<br>B8<br>B9<br>B2<br>B3<br>**_A6_**<br>**_A7_**<br>**_A4_**<br>**_A5_**<br>**_A8_**<br>**_A9_**<br>**_A2_**<br>**_A3_**<br>**_A6_**<br>**_A7_**<br>**_A4_**<br>**_A5_**<br>**_A8_**<br>**_A9_**<br>**_A2_**<br>**_A3_**<br>Y1<br>[1:0]<br>Y2<br>[1:0]<br>Byte Values Transmitted LS Bit First<br>Y3[9:2] (C)<br>Y4[9:2] (D)<br>Y3<br>[1:0]<br>Y4<br>[1:0]<br>Byte Values Transmitted LS Bit First<br>**Odd lines:**<br>**Data**<br>**Data**<br>**Even lines:**<br>Y1[9:2] (A)<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>**U1**<br>**[1:0]**<br>Y1<br>[1:0]<br>**_V1[9:2] (C)_**<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>Y2[9:2] (D)<br>**_V1_**<br>**_[1:0]_**<br>Y2<br>[1:0]<br>Y2[9:2] (B)<br>~~8-bits~~<br>Y1[9:2] (B)<br>~~8-bits~~<br>~~8-bits~~<br>**_U1[9:2] (A)_**<br>~~8-bits~~<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+3<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+4<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+3<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+4<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>1023|**U1[**9:2**]**<br>Packet<br>Footer<br>Y640[9:2]<br>**_V1[_**9:2**_]_**<br>**U3[**9:2**]**<br>Y639[9:2]<br>**_V639[_**9:2**_]_**<br>Packet<br>Header<br>Y1[9:2]<br>Y2[9:2]<br>**U639[**9:2**]**<br>Y2<br>[1:0]<br>**_V1_**<br>**_[1:0]_**<br>**U1**<br>**[1:0]**<br>Y1<br>[1:0]<br>Y640<br>[1:0]<br>**_V639_**<br>**_[1:0]_**<br>**U639**<br>**[1:0]**<br>Y639<br>[1:0]<br>Y638<br>[1:0]<br>**_V637_**<br>**_[1:0]_**<br>**U637**<br>**[1:0]**<br>Y637<br>[1:0]<br>LSB’s<br>Y4<br>[1:0]<br>Y3<br>[1:0]<br>Y2<br>[1:0]<br>Y1<br>[1:0]<br>Packet<br>Header<br>Y1[9:2]<br>Y2[9:2]<br>**Line Start:**<br>**(Odd line)**<br>**Line Start:**<br>**(Even Line)**<br>**Line End:**<br>**(Even Line)**<br>Y3[9:2]<br>Y4[9:2]<br>Packet<br>Footer<br>Y640[9:2]<br>Y639[9:2]<br>Y638[9:2]<br>**Line End:**<br>**(Odd Line)**<br>Y637[9:2]<br>LSB’s<br>Y640<br>[1:0]<br>_Y639_<br>_[1:0]_<br>Y637<br>[1:0]<br>Y638<br>[1:0]<br>LSB’s<br>LSB’s<br>LSB’s<br>1022<br>**Figure 79 YUV420 10-bit Transmission**<br>**_C6_**<br>**_C7_**<br>**_C4_**<br>**_C5_**<br>**_C8_**<br>**_C9_**<br>**A0**<br>**A1**<br>B0<br>B1<br>D6<br>D7<br>D4<br>D5<br>D8<br>D9<br>**_C0_**<br>**_C1_**<br>D0<br>D1<br>D2<br>D3<br>**_C2_**<br>**_C3_**<br>**_C6_**<br>**_C7_**<br>**_C4_**<br>**_C5_**<br>**_C8_**<br>**_C9_**<br>**A0**<br>**A1**<br>B0<br>B1<br>D6<br>D7<br>D4<br>D5<br>D8<br>D9<br>**_C0_**<br>**_C1_**<br>D0<br>D1<br>D2<br>D3<br>**_C2_**<br>**_C3_**<br>B6<br>B7<br>B4<br>B5<br>B8<br>B9<br>B2<br>B3<br>B6<br>B7<br>B4<br>B5<br>B8<br>B9<br>B2<br>B3<br>**_A6_**<br>**_A7_**<br>**_A4_**<br>**_A5_**<br>**_A8_**<br>**_A9_**<br>**_A2_**<br>**_A3_**<br>**_A6_**<br>**_A7_**<br>**_A4_**<br>**_A5_**<br>**_A8_**<br>**_A9_**<br>**_A2_**<br>**_A3_**<br>Y1<br>[1:0]<br>Y2<br>[1:0]<br>Byte Values Transmitted LS Bit First<br>Y3[9:2] (C)<br>Y4[9:2] (D)<br>Y3<br>[1:0]<br>Y4<br>[1:0]<br>Byte Values Transmitted LS Bit First<br>**Odd lines:**<br>**Data**<br>**Data**<br>**Even lines:**<br>Y1[9:2] (A)<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>**U1**<br>**[1:0]**<br>Y1<br>[1:0]<br>**_V1[9:2] (C)_**<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>Y2[9:2] (D)<br>**_V1_**<br>**_[1:0]_**<br>Y2<br>[1:0]<br>Y2[9:2] (B)<br>~~8-bits~~<br>Y1[9:2] (B)<br>~~8-bits~~<br>~~8-bits~~<br>**_U1[9:2] (A)_**<br>~~8-bits~~<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+3<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+4<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+3<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+4<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>1023||||||LSB’s<br>Y4<br>[1:0]<br>Y3<br>[1:0]<br>Y2<br>[1:0]<br>Y1<br>[1:0]<br>Y1[9:2]<br>Y2[9:2]<br>Y3[9:2]<br>Y4[9:2]<br>Packet<br>Footer<br>Y640[9:2]<br>Y639[9:2]<br>Y638[9:2]<br>Y637[9:2]<br>LSB’s<br>Y640<br>[1:0]<br>_Y639_<br>_[1:0]_<br>Y637<br>[1:0]<br>Y638<br>[1:0]|LSB’s<br>Y4<br>[1:0]<br>Y3<br>[1:0]<br>Y2<br>[1:0]<br>Y1<br>[1:0]<br>Y1[9:2]<br>Y2[9:2]<br>Y3[9:2]<br>Y4[9:2]<br>Packet<br>Footer<br>Y640[9:2]<br>Y639[9:2]<br>Y638[9:2]<br>Y637[9:2]<br>LSB’s<br>Y640<br>[1:0]<br>_Y639_<br>_[1:0]_<br>Y637<br>[1:0]<br>Y638<br>[1:0]|LSB’s<br>Y4<br>[1:0]<br>Y3<br>[1:0]<br>Y2<br>[1:0]<br>Y1<br>[1:0]<br>Y1[9:2]<br>Y2[9:2]<br>Y3[9:2]<br>Y4[9:2]<br>Packet<br>Footer<br>Y640[9:2]<br>Y639[9:2]<br>Y638[9:2]<br>Y637[9:2]<br>LSB’s<br>Y640<br>[1:0]<br>_Y639_<br>_[1:0]_<br>Y637<br>[1:0]<br>Y638<br>[1:0]|LSB’s<br>Y4<br>[1:0]<br>Y3<br>[1:0]<br>Y2<br>[1:0]<br>Y1<br>[1:0]<br>Y1[9:2]<br>Y2[9:2]<br>Y3[9:2]<br>Y4[9:2]<br>Packet<br>Footer<br>Y640[9:2]<br>Y639[9:2]<br>Y638[9:2]<br>Y637[9:2]<br>LSB’s<br>Y640<br>[1:0]<br>_Y639_<br>_[1:0]_<br>Y637<br>[1:0]<br>Y638<br>[1:0]|LSB’s<br>Y4<br>[1:0]<br>Y3<br>[1:0]<br>Y2<br>[1:0]<br>Y1<br>[1:0]<br>Y1[9:2]<br>Y2[9:2]<br>Y3[9:2]<br>Y4[9:2]<br>Packet<br>Footer<br>Y640[9:2]<br>Y639[9:2]<br>Y638[9:2]<br>Y637[9:2]<br>LSB’s<br>Y640<br>[1:0]<br>_Y639_<br>_[1:0]_<br>Y637<br>[1:0]<br>Y638<br>[1:0]|LSB’s<br>Y4<br>[1:0]<br>Y3<br>[1:0]<br>Y2<br>[1:0]<br>Y1<br>[1:0]<br>Y1[9:2]<br>Y2[9:2]<br>Y3[9:2]<br>Y4[9:2]<br>Packet<br>Footer<br>Y640[9:2]<br>Y639[9:2]<br>Y638[9:2]<br>Y637[9:2]<br>LSB’s<br>Y640<br>[1:0]<br>_Y639_<br>_[1:0]_<br>Y637<br>[1:0]<br>Y638<br>[1:0]|LSB’s<br>Y4<br>[1:0]<br>Y3<br>[1:0]<br>Y2<br>[1:0]<br>Y1<br>[1:0]<br>Y1[9:2]<br>Y2[9:2]<br>Y3[9:2]<br>Y4[9:2]<br>Packet<br>Footer<br>Y640[9:2]<br>Y639[9:2]<br>Y638[9:2]<br>Y637[9:2]<br>LSB’s<br>Y640<br>[1:0]<br>_Y639_<br>_[1:0]_<br>Y637<br>[1:0]<br>Y638<br>[1:0]|LSB’s<br>Y4<br>[1:0]<br>Y3<br>[1:0]<br>Y2<br>[1:0]<br>Y1<br>[1:0]<br>Y1[9:2]<br>Y2[9:2]<br>Y3[9:2]<br>Y4[9:2]<br>Packet<br>Footer<br>Y640[9:2]<br>Y639[9:2]<br>Y638[9:2]<br>Y637[9:2]<br>LSB’s<br>Y640<br>[1:0]<br>_Y639_<br>_[1:0]_<br>Y637<br>[1:0]<br>Y638<br>[1:0]|LSB’s<br>Y4<br>[1:0]<br>Y3<br>[1:0]<br>Y2<br>[1:0]<br>Y1<br>[1:0]<br>Y1[9:2]<br>Y2[9:2]<br>Y3[9:2]<br>Y4[9:2]<br>Packet<br>Footer<br>Y640[9:2]<br>Y639[9:2]<br>Y638[9:2]<br>Y637[9:2]<br>LSB’s<br>Y640<br>[1:0]<br>_Y639_<br>_[1:0]_<br>Y637<br>[1:0]<br>Y638<br>[1:0]|LSB’s<br>Y4<br>[1:0]<br>Y3<br>[1:0]<br>Y2<br>[1:0]<br>Y1<br>[1:0]<br>Y1[9:2]<br>Y2[9:2]<br>Y3[9:2]<br>Y4[9:2]<br>Packet<br>Footer<br>Y640[9:2]<br>Y639[9:2]<br>Y638[9:2]<br>Y637[9:2]<br>LSB’s<br>Y640<br>[1:0]<br>_Y639_<br>_[1:0]_<br>Y637<br>[1:0]<br>Y638<br>[1:0]|LSB’s<br>Y4<br>[1:0]<br>Y3<br>[1:0]<br>Y2<br>[1:0]<br>Y1<br>[1:0]<br>Y1[9:2]<br>Y2[9:2]<br>Y3[9:2]<br>Y4[9:2]<br>Packet<br>Footer<br>Y640[9:2]<br>Y639[9:2]<br>Y638[9:2]<br>Y637[9:2]<br>LSB’s<br>Y640<br>[1:0]<br>_Y639_<br>_[1:0]_<br>Y637<br>[1:0]<br>Y638<br>[1:0]|LSB’s<br>Y4<br>[1:0]<br>Y3<br>[1:0]<br>Y2<br>[1:0]<br>Y1<br>[1:0]<br>Y1[9:2]<br>Y2[9:2]<br>Y3[9:2]<br>Y4[9:2]<br>Packet<br>Footer<br>Y640[9:2]<br>Y639[9:2]<br>Y638[9:2]<br>Y637[9:2]<br>LSB’s<br>Y640<br>[1:0]<br>_Y639_<br>_[1:0]_<br>Y637<br>[1:0]<br>Y638<br>[1:0]|LSB’s<br>Y4<br>[1:0]<br>Y3<br>[1:0]<br>Y2<br>[1:0]<br>Y1<br>[1:0]<br>Y1[9:2]<br>Y2[9:2]<br>Y3[9:2]<br>Y4[9:2]<br>Packet<br>Footer<br>Y640[9:2]<br>Y639[9:2]<br>Y638[9:2]<br>Y637[9:2]<br>LSB’s<br>Y640<br>[1:0]<br>_Y639_<br>_[1:0]_<br>Y637<br>[1:0]<br>Y638<br>[1:0]|LSB’s<br>Y4<br>[1:0]<br>Y3<br>[1:0]<br>Y2<br>[1:0]<br>Y1<br>[1:0]<br>Y1[9:2]<br>Y2[9:2]<br>Y3[9:2]<br>Y4[9:2]<br>Packet<br>Footer<br>Y640[9:2]<br>Y639[9:2]<br>Y638[9:2]<br>Y637[9:2]<br>LSB’s<br>Y640<br>[1:0]<br>_Y639_<br>_[1:0]_<br>Y637<br>[1:0]<br>Y638<br>[1:0]|LSB’s<br>Y4<br>[1:0]<br>Y3<br>[1:0]<br>Y2<br>[1:0]<br>Y1<br>[1:0]<br>Y1[9:2]<br>Y2[9:2]<br>Y3[9:2]<br>Y4[9:2]<br>Packet<br>Footer<br>Y640[9:2]<br>Y639[9:2]<br>Y638[9:2]<br>Y637[9:2]<br>LSB’s<br>Y640<br>[1:0]<br>_Y639_<br>_[1:0]_<br>Y637<br>[1:0]<br>Y638<br>[1:0]|LSB’s<br>Y4<br>[1:0]<br>Y3<br>[1:0]<br>Y2<br>[1:0]<br>Y1<br>[1:0]<br>Y1[9:2]<br>Y2[9:2]<br>Y3[9:2]<br>Y4[9:2]<br>Packet<br>Footer<br>Y640[9:2]<br>Y639[9:2]<br>Y638[9:2]<br>Y637[9:2]<br>LSB’s<br>Y640<br>[1:0]<br>_Y639_<br>_[1:0]_<br>Y637<br>[1:0]<br>Y638<br>[1:0]|LSB’s<br>Y4<br>[1:0]<br>Y3<br>[1:0]<br>Y2<br>[1:0]<br>Y1<br>[1:0]<br>Y1[9:2]<br>Y2[9:2]<br>Y3[9:2]<br>Y4[9:2]<br>Packet<br>Footer<br>Y640[9:2]<br>Y639[9:2]<br>Y638[9:2]<br>Y637[9:2]<br>LSB’s<br>Y640<br>[1:0]<br>_Y639_<br>_[1:0]_<br>Y637<br>[1:0]<br>Y638<br>[1:0]|LSB’s<br>Y4<br>[1:0]<br>Y3<br>[1:0]<br>Y2<br>[1:0]<br>Y1<br>[1:0]<br>Y1[9:2]<br>Y2[9:2]<br>Y3[9:2]<br>Y4[9:2]<br>Packet<br>Footer<br>Y640[9:2]<br>Y639[9:2]<br>Y638[9:2]<br>Y637[9:2]<br>LSB’s<br>Y640<br>[1:0]<br>_Y639_<br>_[1:0]_<br>Y637<br>[1:0]<br>Y638<br>[1:0]|LSB’s<br>Y4<br>[1:0]<br>Y3<br>[1:0]<br>Y2<br>[1:0]<br>Y1<br>[1:0]<br>Y1[9:2]<br>Y2[9:2]<br>Y3[9:2]<br>Y4[9:2]<br>Packet<br>Footer<br>Y640[9:2]<br>Y639[9:2]<br>Y638[9:2]<br>Y637[9:2]<br>LSB’s<br>Y640<br>[1:0]<br>_Y639_<br>_[1:0]_<br>Y637<br>[1:0]<br>Y638<br>[1:0]|LSB’s<br>Y4<br>[1:0]<br>Y3<br>[1:0]<br>Y2<br>[1:0]<br>Y1<br>[1:0]<br>Y1[9:2]<br>Y2[9:2]<br>Y3[9:2]<br>Y4[9:2]<br>Packet<br>Footer<br>Y640[9:2]<br>Y639[9:2]<br>Y638[9:2]<br>Y637[9:2]<br>LSB’s<br>Y640<br>[1:0]<br>_Y639_<br>_[1:0]_<br>Y637<br>[1:0]<br>Y638<br>[1:0]|LSB’s<br>Y4<br>[1:0]<br>Y3<br>[1:0]<br>Y2<br>[1:0]<br>Y1<br>[1:0]<br>Y1[9:2]<br>Y2[9:2]<br>Y3[9:2]<br>Y4[9:2]<br>Packet<br>Footer<br>Y640[9:2]<br>Y639[9:2]<br>Y638[9:2]<br>Y637[9:2]<br>LSB’s<br>Y640<br>[1:0]<br>_Y639_<br>_[1:0]_<br>Y637<br>[1:0]<br>Y638<br>[1:0]|LSB’s<br>Y4<br>[1:0]<br>Y3<br>[1:0]<br>Y2<br>[1:0]<br>Y1<br>[1:0]<br>Y1[9:2]<br>Y2[9:2]<br>Y3[9:2]<br>Y4[9:2]<br>Packet<br>Footer<br>Y640[9:2]<br>Y639[9:2]<br>Y638[9:2]<br>Y637[9:2]<br>LSB’s<br>Y640<br>[1:0]<br>_Y639_<br>_[1:0]_<br>Y637<br>[1:0]<br>Y638<br>[1:0]|LSB’s<br>Y4<br>[1:0]<br>Y3<br>[1:0]<br>Y2<br>[1:0]<br>Y1<br>[1:0]<br>Y1[9:2]<br>Y2[9:2]<br>Y3[9:2]<br>Y4[9:2]<br>Packet<br>Footer<br>Y640[9:2]<br>Y639[9:2]<br>Y638[9:2]<br>Y637[9:2]<br>LSB’s<br>Y640<br>[1:0]<br>_Y639_<br>_[1:0]_<br>Y637<br>[1:0]<br>Y638<br>[1:0]|LSB’s<br>Y4<br>[1:0]<br>Y3<br>[1:0]<br>Y2<br>[1:0]<br>Y1<br>[1:0]<br>Y1[9:2]<br>Y2[9:2]<br>Y3[9:2]<br>Y4[9:2]<br>Packet<br>Footer<br>Y640[9:2]<br>Y639[9:2]<br>Y638[9:2]<br>Y637[9:2]<br>LSB’s<br>Y640<br>[1:0]<br>_Y639_<br>_[1:0]_<br>Y637<br>[1:0]<br>Y638<br>[1:0]|LSB’s<br>Y4<br>[1:0]<br>Y3<br>[1:0]<br>Y2<br>[1:0]<br>Y1<br>[1:0]<br>Y1[9:2]<br>Y2[9:2]<br>Y3[9:2]<br>Y4[9:2]<br>Packet<br>Footer<br>Y640[9:2]<br>Y639[9:2]<br>Y638[9:2]<br>Y637[9:2]<br>LSB’s<br>Y640<br>[1:0]<br>_Y639_<br>_[1:0]_<br>Y637<br>[1:0]<br>Y638<br>[1:0]|LSB’s<br>Y4<br>[1:0]<br>Y3<br>[1:0]<br>Y2<br>[1:0]<br>Y1<br>[1:0]<br>Y1[9:2]<br>Y2[9:2]<br>Y3[9:2]<br>Y4[9:2]<br>Packet<br>Footer<br>Y640[9:2]<br>Y639[9:2]<br>Y638[9:2]<br>Y637[9:2]<br>LSB’s<br>Y640<br>[1:0]<br>_Y639_<br>_[1:0]_<br>Y637<br>[1:0]<br>Y638<br>[1:0]|LSB’s<br>Y4<br>[1:0]<br>Y3<br>[1:0]<br>Y2<br>[1:0]<br>Y1<br>[1:0]<br>Y1[9:2]<br>Y2[9:2]<br>Y3[9:2]<br>Y4[9:2]<br>Packet<br>Footer<br>Y640[9:2]<br>Y639[9:2]<br>Y638[9:2]<br>Y637[9:2]<br>LSB’s<br>Y640<br>[1:0]<br>_Y639_<br>_[1:0]_<br>Y637<br>[1:0]<br>Y638<br>[1:0]|LSB’s<br>Y4<br>[1:0]<br>Y3<br>[1:0]<br>Y2<br>[1:0]<br>Y1<br>[1:0]<br>Y1[9:2]<br>Y2[9:2]<br>Y3[9:2]<br>Y4[9:2]<br>Packet<br>Footer<br>Y640[9:2]<br>Y639[9:2]<br>Y638[9:2]<br>Y637[9:2]<br>LSB’s<br>Y640<br>[1:0]<br>_Y639_<br>_[1:0]_<br>Y637<br>[1:0]<br>Y638<br>[1:0]|LSB’s<br>Y4<br>[1:0]<br>Y3<br>[1:0]<br>Y2<br>[1:0]<br>Y1<br>[1:0]<br>Y1[9:2]<br>Y2[9:2]<br>Y3[9:2]<br>Y4[9:2]<br>Packet<br>Footer<br>Y640[9:2]<br>Y639[9:2]<br>Y638[9:2]<br>Y637[9:2]<br>LSB’s<br>Y640<br>[1:0]<br>_Y639_<br>_[1:0]_<br>Y637<br>[1:0]<br>Y638<br>[1:0]|LSB’s<br>Y4<br>[1:0]<br>Y3<br>[1:0]<br>Y2<br>[1:0]<br>Y1<br>[1:0]<br>Y1[9:2]<br>Y2[9:2]<br>Y3[9:2]<br>Y4[9:2]<br>Packet<br>Footer<br>Y640[9:2]<br>Y639[9:2]<br>Y638[9:2]<br>Y637[9:2]<br>LSB’s<br>Y640<br>[1:0]<br>_Y639_<br>_[1:0]_<br>Y637<br>[1:0]<br>Y638<br>[1:0]|LSB’s<br>Y4<br>[1:0]<br>Y3<br>[1:0]<br>Y2<br>[1:0]<br>Y1<br>[1:0]<br>Y1[9:2]<br>Y2[9:2]<br>Y3[9:2]<br>Y4[9:2]<br>Packet<br>Footer<br>Y640[9:2]<br>Y639[9:2]<br>Y638[9:2]<br>Y637[9:2]<br>LSB’s<br>Y640<br>[1:0]<br>_Y639_<br>_[1:0]_<br>Y637<br>[1:0]<br>Y638<br>[1:0]|LSB’s<br>Y4<br>[1:0]<br>Y3<br>[1:0]<br>Y2<br>[1:0]<br>Y1<br>[1:0]<br>Y1[9:2]<br>Y2[9:2]<br>Y3[9:2]<br>Y4[9:2]<br>Packet<br>Footer<br>Y640[9:2]<br>Y639[9:2]<br>Y638[9:2]<br>Y637[9:2]<br>LSB’s<br>Y640<br>[1:0]<br>_Y639_<br>_[1:0]_<br>Y637<br>[1:0]<br>Y638<br>[1:0]|LSB’s<br>Y4<br>[1:0]<br>Y3<br>[1:0]<br>Y2<br>[1:0]<br>Y1<br>[1:0]<br>Y1[9:2]<br>Y2[9:2]<br>Y3[9:2]<br>Y4[9:2]<br>Packet<br>Footer<br>Y640[9:2]<br>Y639[9:2]<br>Y638[9:2]<br>Y637[9:2]<br>LSB’s<br>Y640<br>[1:0]<br>_Y639_<br>_[1:0]_<br>Y637<br>[1:0]<br>Y638<br>[1:0]|LSB’s<br>Y4<br>[1:0]<br>Y3<br>[1:0]<br>Y2<br>[1:0]<br>Y1<br>[1:0]<br>Y1[9:2]<br>Y2[9:2]<br>Y3[9:2]<br>Y4[9:2]<br>Packet<br>Footer<br>Y640[9:2]<br>Y639[9:2]<br>Y638[9:2]<br>Y637[9:2]<br>LSB’s<br>Y640<br>[1:0]<br>_Y639_<br>_[1:0]_<br>Y637<br>[1:0]<br>Y638<br>[1:0]|LSB’s<br>Y4<br>[1:0]<br>Y3<br>[1:0]<br>Y2<br>[1:0]<br>Y1<br>[1:0]<br>Y1[9:2]<br>Y2[9:2]<br>Y3[9:2]<br>Y4[9:2]<br>Packet<br>Footer<br>Y640[9:2]<br>Y639[9:2]<br>Y638[9:2]<br>Y637[9:2]<br>LSB’s<br>Y640<br>[1:0]<br>_Y639_<br>_[1:0]_<br>Y637<br>[1:0]<br>Y638<br>[1:0]|LSB’s<br>Y4<br>[1:0]<br>Y3<br>[1:0]<br>Y2<br>[1:0]<br>Y1<br>[1:0]<br>Y1[9:2]<br>Y2[9:2]<br>Y3[9:2]<br>Y4[9:2]<br>Packet<br>Footer<br>Y640[9:2]<br>Y639[9:2]<br>Y638[9:2]<br>Y637[9:2]<br>LSB’s<br>Y640<br>[1:0]<br>_Y639_<br>_[1:0]_<br>Y637<br>[1:0]<br>Y638<br>[1:0]|LSB’s<br>Y4<br>[1:0]<br>Y3<br>[1:0]<br>Y2<br>[1:0]<br>Y1<br>[1:0]<br>Y1[9:2]<br>Y2[9:2]<br>Y3[9:2]<br>Y4[9:2]<br>Packet<br>Footer<br>Y640[9:2]<br>Y639[9:2]<br>Y638[9:2]<br>Y637[9:2]<br>LSB’s<br>Y640<br>[1:0]<br>_Y639_<br>_[1:0]_<br>Y637<br>[1:0]<br>Y638<br>[1:0]|LSB’s<br>Y4<br>[1:0]<br>Y3<br>[1:0]<br>Y2<br>[1:0]<br>Y1<br>[1:0]<br>Y1[9:2]<br>Y2[9:2]<br>Y3[9:2]<br>Y4[9:2]<br>Packet<br>Footer<br>Y640[9:2]<br>Y639[9:2]<br>Y638[9:2]<br>Y637[9:2]<br>LSB’s<br>Y640<br>[1:0]<br>_Y639_<br>_[1:0]_<br>Y637<br>[1:0]<br>Y638<br>[1:0]|LSB’s<br>Y4<br>[1:0]<br>Y3<br>[1:0]<br>Y2<br>[1:0]<br>Y1<br>[1:0]<br>Y1[9:2]<br>Y2[9:2]<br>Y3[9:2]<br>Y4[9:2]<br>Packet<br>Footer<br>Y640[9:2]<br>Y639[9:2]<br>Y638[9:2]<br>Y637[9:2]<br>LSB’s<br>Y640<br>[1:0]<br>_Y639_<br>_[1:0]_<br>Y637<br>[1:0]<br>Y638<br>[1:0]|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|||||Packet<br>Header|||||Y1[9:2]|||||||Y2[9:2]||||Y3[9:2]|||||Y4[9:2]|||||Y4<br>[1:0]||Y3<br>[1:0]|Y2<br>[1:0]||Y1<br>[1:0]|||||||||||||
|||||||||||||||||||||||||||||||||||||||||||||||||
|||||Packet<br>Header|||||**U1[**9:2**]**|||||||Y1[9:2]||||**_V1[_**9:2**_]_**|||||Y2[9:2]|||||Y2<br>[1:0]<br>||**_V1_**<br>**_[1:0]_**|Y1<br>[1:0]||**U1**<br>**[1:0]**||**U3[**9:2**]**|||||||||||
||||||||||LSB’s|||||||||||||||||||||||||||||||||||||||
|||||||||Y638<br>[1:0]||**_V637_**<br>**_[1:0]_**||Y637<br>[1:0]||**U637**<br>**[1:0]**||**U639[**9:2**]**||||Y639[9:2]|||||**_V639[_**9:2**_]_**|||||Y640[9:2]<br>||||||Y64<br>[1:0]|0<br><br>**_V639_**<br>**_[1:0]_**||Y639<br>[1:0]||**U639**<br>**[1:0]**||Packet<br>Footer|||||
|||||||||||||||||||||||||||||||||||||||||||||||||
||**_A2_**|**_A3_**|**_A4_**||**_A5_**|**_A6_**|**_A7_**|**_A8_**|**_A9_**||B2|B3|B4||B5|B6<br>|B7|B8|B9|**_C2_**|**_C3_**|**_C4_**|**_C5_**|**_C6_**|**_C7_**|**_C8_**|**_C9_**|D2|D3||D4|D5|D6|D7||D8|D9|**A0**<br>||**A1**|B0|B1||**_C0_**|**_C1_**|D0|D1|
||~~8-bits~~<br>Byte n||||||||||Byte V<br>~~8-bits~~<br>Byte n+1|||||||||alues Transmitted LS Bit<br>~~8-bits~~<br>Byte n+2||||||||~~8-bits~~||||||||||~~8-bits~~<br>Byte n+4||||||||||
|||||||||||||||||||||||||||||First<br>Byte n+3||||||||||||||||||||
||b0|b1|b2||b3|b4|b5|b6|b7||b0|b1|b2||b3|b4|b5|b6|b7|b0|b1|b2|b3|b4|b5|b6|b7|b0|b1||b2|b3|b4|b5||b6|b7|b0||b1|b2|b3||b4|b5|b6|b7|
||||||||||||Y1[9:2] (B)|||||||||**U1**<br>**[1:0]**<br>Y1<br>[1:0]<br>**_V1[9:2] (C)_**<br>Y2[9:2] (D)<br>**_V1_**<br>**_[1:0]_**<br>Y2<br>[1:0]||||||||||||||||||||||||||||
|||||||||||||||||||||||||||||||||||||||||||||||||
||**_A2_**|**_A3_**|**_A4_**||**_A5_**|**_A6_**|**_A7_**|**_A8_**|**_A9_**||B2|B3|B4||B5|B6<br>|B7|B8|B9|**_C2_**|**_C3_**|**_C4_**|**_C5_**|**_C6_**|**_C7_**|**_C8_**|**_C9_**|D2|D3||D4|D5|D6|D7||D8|D9|**A0**<br>||**A1**|B0|B1||**_C0_**|**_C1_**|D0|D1|
||~~8-bits~~<br>Byte n||||||||||Byte V<br>~~8-bits~~<br>Byte n+1|||||||||alues Transmitted LS Bit<br>~~8-bits~~<br>Byte n+2||||||||~~8-bits~~||||||||||~~8-bits~~<br>Byte n+4||||||||||
|||||||||||||||||||||||||||||First<br>Byte n+3||||||||||||||||||||
||b0|b1|b2||b3|b4|b5|b6|b7||b0|b1|b2||b3|b4|b5|b6|b7|b0|b1|b2|b3|b4|b5|b6|b7|b0|b1||b2|b3|b4|b5||b6|b7|b0||b1|b2|b3||b4|b5|b6|b7|



## **Figure 80 YUV420 10-bit Pixel to Byte Packing Bitwise Illustration** 

1024 The pixel spatial sampling options are the same as for the YUV420 8-bit data format. 

77 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

Specification for CSI-2 

Version 1.3 

29-May-2014 

|FS<br>**U**<br>Y<br>FE<br>Packet Header, PH<br>Packet Footer, PF<br>….<br>Y<br>Y<br>**_V_**<br>Y<br>Y<br>Y<br>Y<br>Y<br>Y<br>Y<br>Y<br>Y<br>Y<br>Y<br>Y<br>Y<br>Y<br>Y<br>Y<br>Y<br>Y<br>Y<br>Y<br>Y<br>Y<br>Y<br>….<br>….<br>….<br>….<br>….<br>….<br>….<br>….<br>….<br>….<br>….<br>….<br>Packet Footer, PF<br>Y<br>Y<br>Y<br>Y<br>Y<br>Y<br>Y<br>Y<br>Y<br>Y<br>Y<br>Y<br>Y<br>Y<br>Y<br>Y<br>Y<br>Y<br>Y<br>Y<br>Y<br>Y<br>Y<br>Y<br>**U**<br>Y<br>Y<br>**_V_**<br>Packet Header, PH<br>**U**<br>Y<br>….<br>Y<br>**_V_**<br>**U**<br>Y<br>Y<br>**_V_**<br>**U**<br>Y<br>….<br>Y<br>**_V_**<br>**U**<br>Y<br>Y<br>**_V_**<br>**U**<br>Y<br>….<br>Y<br>**_V_**<br>**U**<br>Y<br>Y<br>**_V_**<br>**U**<br>Y<br>….<br>Y<br>**_V_**<br>**U**<br>Y<br>Y<br>**_V_**<br>**U**<br>Y<br>….<br>Y<br>**_V_**<br>**U**<br>Y<br>Y<br>**_V_**<br>**U**<br>Y<br>….<br>Y<br>**_V_**<br>**U**<br>Y<br>Y<br>**_V_**<br>**U**<br>Y<br>….<br>Y<br>**_V_**<br>**U**<br>Y<br>Y<br>**_V_**<br>**U**<br>Y<br>….<br>Y<br>**_V_**<br>**U**<br>Y<br>Y<br>**_V_**<br>**U**<br>Y<br>….<br>Y<br>**_V_**<br>**U**<br>Y<br>Y<br>**_V_**<br>**U**<br>Y<br>….<br>Y<br>**_V_**<br>**U**<br>Y<br>Y<br>**_V_**<br>**U**<br>Y<br>….<br>Y<br>**_V_**<br>**U**<br>Y<br>Y<br>**_V_**<br>Y<br>Y<br>Y<br>Y<br>Y<br>Y<br>Y<br>Y<br>Y<br>Y<br>Y<br>Y<br>Y<br>**_V_**<br>Y<br>**_V_**<br>Y<br>**_V_**<br>Y<br>**_V_**<br>Y<br>**_V_**<br>Y<br>**_V_**<br>Y<br>**_V_**<br>Y<br>**_V_**<br>Y<br>**_V_**<br>Y<br>**_V_**<br>Y<br>**_V_**<br>Y<br>**_V_**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**LSB**<br>**Odd lines (1, 3, 5, ..):**<br>Luminance only, Y<br>**Even lines (2, 4, 6, ..):**<br>Luminance and Chrominance, UYVY<br>1025|FS||Y|Y|Y|Y|**LSB**|….|Y|**LSB**||||**U**|Y|**_V_**|Y|**LSB**|**U**|Y|**_V_**|Y|**LSB**|….|**_V_**|Y|**LSB**|Packet Footer, PF||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|||Packet Header, PH|Y|Y|Y|Y|**LSB**|….|Y|**LSB**||||**U**|Y|**_V_**|Y|**LSB**|**U**|Y|**_V_**|Y|**LSB**|….|**_V_**|Y|**LSB**|||
||||Y|Y|Y|Y|**LSB**|….|Y|**LSB**||||**U**|Y|**_V_**|Y|**LSB**|**U**|Y|**_V_**|Y|**LSB**|….|**_V_**|Y|**LSB**|||
||||Y|Y|Y|Y|**LSB**|….|Y|**LSB**|PF||PH|**U**|Y|**_V_**|Y|**LSB**|**U**|Y|**_V_**|Y|**LSB**|….|**_V_**|Y|**LSB**|||
||||Y|Y|Y|Y|**LSB**|….|Y|**LSB**|er,||er,|**U**|Y|**_V_**|Y|**LSB**|**U**|Y|**_V_**|Y|**LSB**|….|**_V_**|Y|**LSB**|||
||||Y|Y|Y|Y|**LSB**|….|Y|**LSB**|oot||ead|**U**|Y|**_V_**|Y|**LSB**|**U**|Y|**_V_**|Y|**LSB**|….|**_V_**|Y|**LSB**|||
||||Y|Y|Y|Y|**LSB**|….|Y|**LSB**|t F||t H|**U**|Y|**_V_**|Y|**LSB**|**U**|Y|**_V_**|Y|**LSB**|….|**_V_**|Y|**LSB**|||
||||Y|Y|Y|Y|**LSB**|….|Y|**LSB**|cke||cke|**U**|Y|**_V_**|Y|**LSB**|**U**|Y|**_V_**|Y|**LSB**|….|**_V_**|Y|**LSB**|||
||||Y|Y|Y|Y|**LSB**|….|Y|**LSB**|Pa||Pa|**U**|Y|**_V_**|Y|**LSB**|**U**|Y|**_V_**|Y|**LSB**|….|**_V_**|Y|**LSB**|||
||||Y|Y|Y|Y|**LSB**|….|Y|**LSB**||||**U**|Y|**_V_**|Y|**LSB**|**U**|Y|**_V_**|Y|**LSB**|….|**_V_**|Y|**LSB**|||
||||Y|Y|Y|Y|**LSB**|….|Y|**LSB**||||**U**|Y|**_V_**|Y|**LSB**|**U**|Y|**_V_**|Y|**LSB**|….|**_V_**|Y|**LSB**|||
||||Y|Y|Y|Y|**LSB**|….|Y|**LSB**||||**U**|Y|**_V_**|Y|**LSB**|**U**|Y|**_V_**|Y|**LSB**|….|**_V_**|Y|**LSB**||FE|



## **Figure 81 YUV420 10-bit Frame Format** 

|1026<br>1027<br>1028<br>1029<br>1030<br>1031<br>1032<br>1033<br>1034|**11.2.4**<br>**YUV422 8-bit**<br>YUV422 8-bit data transmission is performed by transmitting a UYVY sequence. This sequence is<br>illustrated in Figure 82.<br>Table 14 specifies the packet size constraints for YUV422 8-bit packet. The length of each packet must be a<br>multiple of the values in the table.<br>**Table 14 YUV422 8-bit Packet Data Size Constraints**|**11.2.4**<br>**YUV422 8-bit**<br>YUV422 8-bit data transmission is performed by transmitting a UYVY sequence. This sequence is<br>illustrated in Figure 82.<br>Table 14 specifies the packet size constraints for YUV422 8-bit packet. The length of each packet must be a<br>multiple of the values in the table.<br>**Table 14 YUV422 8-bit Packet Data Size Constraints**|**11.2.4**<br>**YUV422 8-bit**<br>YUV422 8-bit data transmission is performed by transmitting a UYVY sequence. This sequence is<br>illustrated in Figure 82.<br>Table 14 specifies the packet size constraints for YUV422 8-bit packet. The length of each packet must be a<br>multiple of the values in the table.<br>**Table 14 YUV422 8-bit Packet Data Size Constraints**|**11.2.4**<br>**YUV422 8-bit**<br>YUV422 8-bit data transmission is performed by transmitting a UYVY sequence. This sequence is<br>illustrated in Figure 82.<br>Table 14 specifies the packet size constraints for YUV422 8-bit packet. The length of each packet must be a<br>multiple of the values in the table.<br>**Table 14 YUV422 8-bit Packet Data Size Constraints**|
|---|---|---|---|---|
||**Pixels**||**Bytes**|**Bits**|
||2||4|32|
||Bit order in transmission follows the general CSI-2 rule, LSB first. The pixel to byte mapping is illustrated<br>in Figure 83.<br>**U1[7:0]**<br>Packet Header<br>Packet Footer<br>Y640[7:0]<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**U3[7:0]**<br>**U639[7:0]**<br>Y639[7:0]<br>**_V639[7:0]_**<br>Y638[7:0]<br>Line Start:<br>Line End:||||



**Figure 82 YUV422 8-bit Transmission** 

Copyright © 2005-2014 MIPI Alliance, Inc. 

78 

All rights reserved. 

**Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

1035 

|**U1[7:0]**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**U0**<br>**U1**<br>**U2**<br>**U3**<br>**U4**<br>**U5**<br>**U6**<br>**U7**<br>Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>**_V0_**<br>**_V1_**<br>**_V2_**<br>**_V3_**<br>**_V4_**<br>**_V5_**<br>**_V6_**<br>**_V7_**<br>B0<br>B7 B0<br>B7 B0<br>B7<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**_V1[7:0]_**<br>Y1[7:0]<br>B7<br>B0 B7<br>B0 B7<br>B0<br>**U1[7:0]**<br>Pixel to Byte Data Packing<br>Data Transmitted LS Bit First<br>**Data**<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**Pixel Data**<br>**Byte Data**<br>**U1[7:0]**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|**U1[7:0]**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**U0**<br>**U1**<br>**U2**<br>**U3**<br>**U4**<br>**U5**<br>**U6**<br>**U7**<br>Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>**_V0_**<br>**_V1_**<br>**_V2_**<br>**_V3_**<br>**_V4_**<br>**_V5_**<br>**_V6_**<br>**_V7_**<br>B0<br>B7 B0<br>B7 B0<br>B7<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**_V1[7:0]_**<br>Y1[7:0]<br>B7<br>B0 B7<br>B0 B7<br>B0<br>**U1[7:0]**<br>Pixel to Byte Data Packing<br>Data Transmitted LS Bit First<br>**Data**<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**Pixel Data**<br>**Byte Data**<br>**U1[7:0]**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|**U1[7:0]**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**U0**<br>**U1**<br>**U2**<br>**U3**<br>**U4**<br>**U5**<br>**U6**<br>**U7**<br>Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>**_V0_**<br>**_V1_**<br>**_V2_**<br>**_V3_**<br>**_V4_**<br>**_V5_**<br>**_V6_**<br>**_V7_**<br>B0<br>B7 B0<br>B7 B0<br>B7<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**_V1[7:0]_**<br>Y1[7:0]<br>B7<br>B0 B7<br>B0 B7<br>B0<br>**U1[7:0]**<br>Pixel to Byte Data Packing<br>Data Transmitted LS Bit First<br>**Data**<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**Pixel Data**<br>**Byte Data**<br>**U1[7:0]**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|**U1[7:0]**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**U0**<br>**U1**<br>**U2**<br>**U3**<br>**U4**<br>**U5**<br>**U6**<br>**U7**<br>Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>**_V0_**<br>**_V1_**<br>**_V2_**<br>**_V3_**<br>**_V4_**<br>**_V5_**<br>**_V6_**<br>**_V7_**<br>B0<br>B7 B0<br>B7 B0<br>B7<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**_V1[7:0]_**<br>Y1[7:0]<br>B7<br>B0 B7<br>B0 B7<br>B0<br>**U1[7:0]**<br>Pixel to Byte Data Packing<br>Data Transmitted LS Bit First<br>**Data**<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**Pixel Data**<br>**Byte Data**<br>**U1[7:0]**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|**U1[7:0]**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**U0**<br>**U1**<br>**U2**<br>**U3**<br>**U4**<br>**U5**<br>**U6**<br>**U7**<br>Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>**_V0_**<br>**_V1_**<br>**_V2_**<br>**_V3_**<br>**_V4_**<br>**_V5_**<br>**_V6_**<br>**_V7_**<br>B0<br>B7 B0<br>B7 B0<br>B7<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**_V1[7:0]_**<br>Y1[7:0]<br>B7<br>B0 B7<br>B0 B7<br>B0<br>**U1[7:0]**<br>Pixel to Byte Data Packing<br>Data Transmitted LS Bit First<br>**Data**<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**Pixel Data**<br>**Byte Data**<br>**U1[7:0]**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|**U1[7:0]**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**U0**<br>**U1**<br>**U2**<br>**U3**<br>**U4**<br>**U5**<br>**U6**<br>**U7**<br>Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>**_V0_**<br>**_V1_**<br>**_V2_**<br>**_V3_**<br>**_V4_**<br>**_V5_**<br>**_V6_**<br>**_V7_**<br>B0<br>B7 B0<br>B7 B0<br>B7<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**_V1[7:0]_**<br>Y1[7:0]<br>B7<br>B0 B7<br>B0 B7<br>B0<br>**U1[7:0]**<br>Pixel to Byte Data Packing<br>Data Transmitted LS Bit First<br>**Data**<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**Pixel Data**<br>**Byte Data**<br>**U1[7:0]**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|**U1[7:0]**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**U0**<br>**U1**<br>**U2**<br>**U3**<br>**U4**<br>**U5**<br>**U6**<br>**U7**<br>Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>**_V0_**<br>**_V1_**<br>**_V2_**<br>**_V3_**<br>**_V4_**<br>**_V5_**<br>**_V6_**<br>**_V7_**<br>B0<br>B7 B0<br>B7 B0<br>B7<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**_V1[7:0]_**<br>Y1[7:0]<br>B7<br>B0 B7<br>B0 B7<br>B0<br>**U1[7:0]**<br>Pixel to Byte Data Packing<br>Data Transmitted LS Bit First<br>**Data**<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**Pixel Data**<br>**Byte Data**<br>**U1[7:0]**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|**U1[7:0]**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**U0**<br>**U1**<br>**U2**<br>**U3**<br>**U4**<br>**U5**<br>**U6**<br>**U7**<br>Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>**_V0_**<br>**_V1_**<br>**_V2_**<br>**_V3_**<br>**_V4_**<br>**_V5_**<br>**_V6_**<br>**_V7_**<br>B0<br>B7 B0<br>B7 B0<br>B7<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**_V1[7:0]_**<br>Y1[7:0]<br>B7<br>B0 B7<br>B0 B7<br>B0<br>**U1[7:0]**<br>Pixel to Byte Data Packing<br>Data Transmitted LS Bit First<br>**Data**<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**Pixel Data**<br>**Byte Data**<br>**U1[7:0]**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|**U1[7:0]**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**U0**<br>**U1**<br>**U2**<br>**U3**<br>**U4**<br>**U5**<br>**U6**<br>**U7**<br>Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>**_V0_**<br>**_V1_**<br>**_V2_**<br>**_V3_**<br>**_V4_**<br>**_V5_**<br>**_V6_**<br>**_V7_**<br>B0<br>B7 B0<br>B7 B0<br>B7<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**_V1[7:0]_**<br>Y1[7:0]<br>B7<br>B0 B7<br>B0 B7<br>B0<br>**U1[7:0]**<br>Pixel to Byte Data Packing<br>Data Transmitted LS Bit First<br>**Data**<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**Pixel Data**<br>**Byte Data**<br>**U1[7:0]**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|**U1[7:0]**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**U0**<br>**U1**<br>**U2**<br>**U3**<br>**U4**<br>**U5**<br>**U6**<br>**U7**<br>Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>**_V0_**<br>**_V1_**<br>**_V2_**<br>**_V3_**<br>**_V4_**<br>**_V5_**<br>**_V6_**<br>**_V7_**<br>B0<br>B7 B0<br>B7 B0<br>B7<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**_V1[7:0]_**<br>Y1[7:0]<br>B7<br>B0 B7<br>B0 B7<br>B0<br>**U1[7:0]**<br>Pixel to Byte Data Packing<br>Data Transmitted LS Bit First<br>**Data**<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**Pixel Data**<br>**Byte Data**<br>**U1[7:0]**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|**U1[7:0]**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**U0**<br>**U1**<br>**U2**<br>**U3**<br>**U4**<br>**U5**<br>**U6**<br>**U7**<br>Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>**_V0_**<br>**_V1_**<br>**_V2_**<br>**_V3_**<br>**_V4_**<br>**_V5_**<br>**_V6_**<br>**_V7_**<br>B0<br>B7 B0<br>B7 B0<br>B7<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**_V1[7:0]_**<br>Y1[7:0]<br>B7<br>B0 B7<br>B0 B7<br>B0<br>**U1[7:0]**<br>Pixel to Byte Data Packing<br>Data Transmitted LS Bit First<br>**Data**<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**Pixel Data**<br>**Byte Data**<br>**U1[7:0]**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|**U1[7:0]**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**U0**<br>**U1**<br>**U2**<br>**U3**<br>**U4**<br>**U5**<br>**U6**<br>**U7**<br>Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>**_V0_**<br>**_V1_**<br>**_V2_**<br>**_V3_**<br>**_V4_**<br>**_V5_**<br>**_V6_**<br>**_V7_**<br>B0<br>B7 B0<br>B7 B0<br>B7<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**_V1[7:0]_**<br>Y1[7:0]<br>B7<br>B0 B7<br>B0 B7<br>B0<br>**U1[7:0]**<br>Pixel to Byte Data Packing<br>Data Transmitted LS Bit First<br>**Data**<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**Pixel Data**<br>**Byte Data**<br>**U1[7:0]**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|**U1[7:0]**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**U0**<br>**U1**<br>**U2**<br>**U3**<br>**U4**<br>**U5**<br>**U6**<br>**U7**<br>Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>**_V0_**<br>**_V1_**<br>**_V2_**<br>**_V3_**<br>**_V4_**<br>**_V5_**<br>**_V6_**<br>**_V7_**<br>B0<br>B7 B0<br>B7 B0<br>B7<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**_V1[7:0]_**<br>Y1[7:0]<br>B7<br>B0 B7<br>B0 B7<br>B0<br>**U1[7:0]**<br>Pixel to Byte Data Packing<br>Data Transmitted LS Bit First<br>**Data**<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**Pixel Data**<br>**Byte Data**<br>**U1[7:0]**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|**U1[7:0]**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**U0**<br>**U1**<br>**U2**<br>**U3**<br>**U4**<br>**U5**<br>**U6**<br>**U7**<br>Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>**_V0_**<br>**_V1_**<br>**_V2_**<br>**_V3_**<br>**_V4_**<br>**_V5_**<br>**_V6_**<br>**_V7_**<br>B0<br>B7 B0<br>B7 B0<br>B7<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**_V1[7:0]_**<br>Y1[7:0]<br>B7<br>B0 B7<br>B0 B7<br>B0<br>**U1[7:0]**<br>Pixel to Byte Data Packing<br>Data Transmitted LS Bit First<br>**Data**<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**Pixel Data**<br>**Byte Data**<br>**U1[7:0]**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|**U1[7:0]**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**U0**<br>**U1**<br>**U2**<br>**U3**<br>**U4**<br>**U5**<br>**U6**<br>**U7**<br>Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>**_V0_**<br>**_V1_**<br>**_V2_**<br>**_V3_**<br>**_V4_**<br>**_V5_**<br>**_V6_**<br>**_V7_**<br>B0<br>B7 B0<br>B7 B0<br>B7<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**_V1[7:0]_**<br>Y1[7:0]<br>B7<br>B0 B7<br>B0 B7<br>B0<br>**U1[7:0]**<br>Pixel to Byte Data Packing<br>Data Transmitted LS Bit First<br>**Data**<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**Pixel Data**<br>**Byte Data**<br>**U1[7:0]**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|**U1[7:0]**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**U0**<br>**U1**<br>**U2**<br>**U3**<br>**U4**<br>**U5**<br>**U6**<br>**U7**<br>Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>**_V0_**<br>**_V1_**<br>**_V2_**<br>**_V3_**<br>**_V4_**<br>**_V5_**<br>**_V6_**<br>**_V7_**<br>B0<br>B7 B0<br>B7 B0<br>B7<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**_V1[7:0]_**<br>Y1[7:0]<br>B7<br>B0 B7<br>B0 B7<br>B0<br>**U1[7:0]**<br>Pixel to Byte Data Packing<br>Data Transmitted LS Bit First<br>**Data**<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**Pixel Data**<br>**Byte Data**<br>**U1[7:0]**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|**U1[7:0]**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**U0**<br>**U1**<br>**U2**<br>**U3**<br>**U4**<br>**U5**<br>**U6**<br>**U7**<br>Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>**_V0_**<br>**_V1_**<br>**_V2_**<br>**_V3_**<br>**_V4_**<br>**_V5_**<br>**_V6_**<br>**_V7_**<br>B0<br>B7 B0<br>B7 B0<br>B7<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**_V1[7:0]_**<br>Y1[7:0]<br>B7<br>B0 B7<br>B0 B7<br>B0<br>**U1[7:0]**<br>Pixel to Byte Data Packing<br>Data Transmitted LS Bit First<br>**Data**<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**Pixel Data**<br>**Byte Data**<br>**U1[7:0]**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|**U1[7:0]**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**U0**<br>**U1**<br>**U2**<br>**U3**<br>**U4**<br>**U5**<br>**U6**<br>**U7**<br>Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>**_V0_**<br>**_V1_**<br>**_V2_**<br>**_V3_**<br>**_V4_**<br>**_V5_**<br>**_V6_**<br>**_V7_**<br>B0<br>B7 B0<br>B7 B0<br>B7<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**_V1[7:0]_**<br>Y1[7:0]<br>B7<br>B0 B7<br>B0 B7<br>B0<br>**U1[7:0]**<br>Pixel to Byte Data Packing<br>Data Transmitted LS Bit First<br>**Data**<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**Pixel Data**<br>**Byte Data**<br>**U1[7:0]**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|**U1[7:0]**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**U0**<br>**U1**<br>**U2**<br>**U3**<br>**U4**<br>**U5**<br>**U6**<br>**U7**<br>Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>**_V0_**<br>**_V1_**<br>**_V2_**<br>**_V3_**<br>**_V4_**<br>**_V5_**<br>**_V6_**<br>**_V7_**<br>B0<br>B7 B0<br>B7 B0<br>B7<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**_V1[7:0]_**<br>Y1[7:0]<br>B7<br>B0 B7<br>B0 B7<br>B0<br>**U1[7:0]**<br>Pixel to Byte Data Packing<br>Data Transmitted LS Bit First<br>**Data**<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**Pixel Data**<br>**Byte Data**<br>**U1[7:0]**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|**U1[7:0]**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**U0**<br>**U1**<br>**U2**<br>**U3**<br>**U4**<br>**U5**<br>**U6**<br>**U7**<br>Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>**_V0_**<br>**_V1_**<br>**_V2_**<br>**_V3_**<br>**_V4_**<br>**_V5_**<br>**_V6_**<br>**_V7_**<br>B0<br>B7 B0<br>B7 B0<br>B7<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**_V1[7:0]_**<br>Y1[7:0]<br>B7<br>B0 B7<br>B0 B7<br>B0<br>**U1[7:0]**<br>Pixel to Byte Data Packing<br>Data Transmitted LS Bit First<br>**Data**<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**Pixel Data**<br>**Byte Data**<br>**U1[7:0]**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|**U1[7:0]**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**U0**<br>**U1**<br>**U2**<br>**U3**<br>**U4**<br>**U5**<br>**U6**<br>**U7**<br>Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>**_V0_**<br>**_V1_**<br>**_V2_**<br>**_V3_**<br>**_V4_**<br>**_V5_**<br>**_V6_**<br>**_V7_**<br>B0<br>B7 B0<br>B7 B0<br>B7<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**_V1[7:0]_**<br>Y1[7:0]<br>B7<br>B0 B7<br>B0 B7<br>B0<br>**U1[7:0]**<br>Pixel to Byte Data Packing<br>Data Transmitted LS Bit First<br>**Data**<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**Pixel Data**<br>**Byte Data**<br>**U1[7:0]**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|**U1[7:0]**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**U0**<br>**U1**<br>**U2**<br>**U3**<br>**U4**<br>**U5**<br>**U6**<br>**U7**<br>Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>**_V0_**<br>**_V1_**<br>**_V2_**<br>**_V3_**<br>**_V4_**<br>**_V5_**<br>**_V6_**<br>**_V7_**<br>B0<br>B7 B0<br>B7 B0<br>B7<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**_V1[7:0]_**<br>Y1[7:0]<br>B7<br>B0 B7<br>B0 B7<br>B0<br>**U1[7:0]**<br>Pixel to Byte Data Packing<br>Data Transmitted LS Bit First<br>**Data**<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**Pixel Data**<br>**Byte Data**<br>**U1[7:0]**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|**U1[7:0]**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**U0**<br>**U1**<br>**U2**<br>**U3**<br>**U4**<br>**U5**<br>**U6**<br>**U7**<br>Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>**_V0_**<br>**_V1_**<br>**_V2_**<br>**_V3_**<br>**_V4_**<br>**_V5_**<br>**_V6_**<br>**_V7_**<br>B0<br>B7 B0<br>B7 B0<br>B7<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**_V1[7:0]_**<br>Y1[7:0]<br>B7<br>B0 B7<br>B0 B7<br>B0<br>**U1[7:0]**<br>Pixel to Byte Data Packing<br>Data Transmitted LS Bit First<br>**Data**<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**Pixel Data**<br>**Byte Data**<br>**U1[7:0]**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|**U1[7:0]**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**U0**<br>**U1**<br>**U2**<br>**U3**<br>**U4**<br>**U5**<br>**U6**<br>**U7**<br>Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>**_V0_**<br>**_V1_**<br>**_V2_**<br>**_V3_**<br>**_V4_**<br>**_V5_**<br>**_V6_**<br>**_V7_**<br>B0<br>B7 B0<br>B7 B0<br>B7<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**_V1[7:0]_**<br>Y1[7:0]<br>B7<br>B0 B7<br>B0 B7<br>B0<br>**U1[7:0]**<br>Pixel to Byte Data Packing<br>Data Transmitted LS Bit First<br>**Data**<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**Pixel Data**<br>**Byte Data**<br>**U1[7:0]**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|**U1[7:0]**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>**U0**<br>**U1**<br>**U2**<br>**U3**<br>**U4**<br>**U5**<br>**U6**<br>**U7**<br>Y0<br>Y1<br>Y2<br>Y3<br>Y4<br>Y5<br>Y6<br>Y7<br>**_V0_**<br>**_V1_**<br>**_V2_**<br>**_V3_**<br>**_V4_**<br>**_V5_**<br>**_V6_**<br>**_V7_**<br>B0<br>B7 B0<br>B7 B0<br>B7<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**_V1[7:0]_**<br>Y1[7:0]<br>B7<br>B0 B7<br>B0 B7<br>B0<br>**U1[7:0]**<br>Pixel to Byte Data Packing<br>Data Transmitted LS Bit First<br>**Data**<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>**Pixel Data**<br>**Byte Data**<br>**U1[7:0]**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||**U1[7:0]**<br>Y1[7:0]<br>**_V1[7:0]_**<br>Y2[7:0]<br>B7<br>B0 B7<br>B0 B7<br>B0 B7<br>B0<br>B7<br>B0 B7<br>B0 B7<br>B0<br>Pixel to Byte Data Packing||||||||||||||||||||||||
||**U1[7:0]**||||||||Y1[7:0]||||||||**_V1[7:0]_**||||||||
||B0<br>B7||||||||B0<br>B7 <br>Data Trans||||||||B0<br>B7<br>mitted LS Bit First||||||||
||**U0**|**U1**|**U2**|**U3**|**U4**|**U5**|**U6**|**U7**|Y0|Y1|Y2|Y3|Y4|Y5|Y6|Y7|**_V0_**|**_V1_**|**_V2_**|**_V3_**|**_V4_**|**_V5_**|**_V6_**|**_V7_**|
||Byte n||||||||Byte n+1||||||||Byte n+2||||||||
||b0|b1|b2|b3|b4|b5|b6|b7|b0|b1|b2|b3|b4|b5|b6|b7|b0|b1|b2|b3|b4|b5|b6|b7|



**Figure 83 YUV422 8-bit Pixel to Byte Packing Bitwise Illustration** 

1036 

**==> picture [324 x 223] intentionally omitted <==**

**----- Start of picture text -----**<br>
Y1 Y2 Y3 Y4 Y5 Y6 Y7 Y8<br>Line 1<br>Line 2<br>Line 3<br>Line 4<br>Line 5<br>Luminance Sample, Y Calculated Chrominance sample, Cb & Cr<br>**----- End of picture text -----**<br>


**Figure 84 YUV422 Co-sited Spatial Sampling** 

1037 The pixel spatial alignment is the same as in CCIR-656 standard. The frame format for YUV422 is 1038 presented in Figure 85. 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

79 

Specification for CSI-2 

Version 1.3 29-May-2014 

## 1039 

|FS||**U**|Y|**_V_**|Y|**U**|….|Y|**U**|Y|**_V_**|Y|Packet Footer, PF||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||Packet Header, PH|**U**|Y|**_V_**|Y|**U**|….|Y|**U**|Y|**_V_**|Y|||
|||**U**|Y|**_V_**|Y|**U**|….|Y|**U**|Y|**_V_**|Y|||
|||**U**|Y|**_V_**|Y|**U**|….|Y|**U**|Y|**_V_**|Y|||
|||**U**|Y|**_V_**|Y|**U**|….|Y|**U**|Y|**_V_**|Y|||
|||**U**|Y|**_V_**|Y|**U**|….|Y|**U**|Y|**_V_**|Y|||
|||**U**|Y|**_V_**|Y|**U**|….|Y|**U**|Y|**_V_**|Y|||
|||**U**|Y|**_V_**|Y|**U**|….|Y|**U**|Y|**_V_**|Y|||
|||**U**|Y|**_V_**|Y|**U**|….|Y|**U**|Y|**_V_**|Y|||
|||**U**|Y|**_V_**|Y|**U**|….|Y|**U**|Y|**_V_**|Y|||
|||**U**|Y|**_V_**|Y|**U**|….|Y|**U**|Y|**_V_**|Y|||
|||**U**|Y|**_V_**|Y|**U**|….|Y|**U**|Y|**_V_**|Y||FE|



**Figure 85 YUV422 8-bit Frame Format** 

1040 **11.2.5 YUV422 10-bit** 1041 YUV422 10-bit data transmission is performed by transmitting a UYVY sequence. This sequence is 1042 illustrated in Figure 86. 

1043 Table 15 specifies the packet size constraints for YUV422 10-bit packet. The length of each packet must be 1044 a multiple of the values in the table. 

## 1045 **Table 15 YUV422 10-bit Packet Data Size Constraints** 

|**Pixels**|**Bytes**|**Bits**|
|---|---|---|
|2|5|40|
|Bit order in transmission follows the general CSI-2 rule, LSB first. The pixel to byte mapping is illustrated<br>in Figure 87.<br>**U1[9:2]**<br>Packet Header<br>Packet Footer<br>Y640[9:2]<br>Y1[9:2]<br>**_V1[9:2]_**<br>Y2[9:2]<br>**U639[9:2]**<br>Y639[9:2]<br>**_V639[9:2]_**<br>Line Start<br>Line End<br>LSB’s<br>LSB’s|||



1046 Bit order in transmission follows the general CSI-2 rule, LSB first. The pixel to byte mapping is illustrated 1047 in Figure 87. 

1048 

**Figure 86 YUV422 10-bit Transmitted Bytes** 

Copyright © 2005-2014 MIPI Alliance, Inc. 

80 

All rights reserved. **Confidential** 

Version 1.3 

Specification for CSI-2 

29-May-2014 

1049 

**==> picture [430 x 302] intentionally omitted <==**

**----- Start of picture text -----**<br>
Pixel Data:<br>B9 B0 B9 B0 B9 B0 B9 B0<br>U1[9:0] Y1[9:0] V1[9:0] Y2[9:0]<br>Pixel to Byte Data Packing<br>Byte Data:<br>B7 B0 B7 B0 B7 B0 B7 B0 B7 B0<br>U1[9:2] Y1[9:2] V1[9:2] Y2[9:2] Y2[1:0] V1[1:0] Y1[1:0] U1[1:0]<br>LSB’s<br>B7 B0 B7 B0 B7 B6 B5 B4 B3 B2 B1 B0<br>V1[9:2] Y2[9:2] Y2[1:0] V1[1:0] Y1[1:0] U1[1:0]<br>Data Transmitted LS Bit First<br>B0 B7 B0 B7 B0 B7<br>Data V2 V3 V4 V5 V6 V7 V8 V9 Y2 Y3 Y4 Y5 Y6 Y7 Y8 Y9 U0 U1 Y0 Y1 V0 V1 Y0 Y1<br>Byte n Byte n+1 Byte n+2<br>b0 b1 b2 b3 b4 b5 b6 b7 b0 b1 b2 b3 b4 b5 b6 b7 b0 b1 b2 b3 b4 b5 b6 b7<br>**----- End of picture text -----**<br>


**Figure 87 YUV422 10-bit Pixel to Byte Packing Bitwise Illustration** 

1050 The pixel spatial alignment is the same as in the YUV422 8-bit data case. The frame format for YUV422 is 1051 presented in the Figure 88. 

1052 

**==> picture [342 x 138] intentionally omitted <==**

**----- Start of picture text -----**<br>
FS U Y V Y LSBs U …. U Y V Y LSBs<br>U Y V Y LSBs U …. U Y V Y LSBs<br>U Y V Y LSBs U …. U Y V Y LSBs<br>U Y V Y LSBs U …. U Y V Y LSBs<br>U Y V Y LSBs U …. U Y V Y LSBs<br>U Y V Y LSBs U …. U Y V Y LSBs<br>U Y V Y LSBs U …. U Y V Y LSBs<br>U Y V Y LSBs U …. U Y V Y LSBs<br>U Y V Y LSBs U …. U Y V Y LSBs<br>U Y V Y LSBs U …. U Y V Y LSBs<br>U Y V Y LSBs U …. U Y V Y LSBs<br>U Y V Y LSBs U …. U Y V Y LSBs FE<br>Packer Header, PH Packer Footer, PF<br>**----- End of picture text -----**<br>


**Figure 88 YUV422 10-bit Frame Format** 

## 1053 **11.3 RGB Image Data** 

1054 Table 16 defines the data type codes for RGB data formats described in this section. 

1055 

**Table 16 RGB Image Data Types** 

|**Data Type**|**Description**|
|---|---|
|0x20|RGB444|



81 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

Specification for CSI-2 

Version 1.3 29-May-2014 

|**Data Type**|**Description**|
|---|---|
|0x21|RGB555|
|0x22|RGB565|
|0x23|RGB666|
|0x24|RGB888|
|0x25|Reserved|
|0x26|Reserved|
|0x27|Reserved|



## 1056 **11.3.1 RGB888** 

1057 RGB888 data transmission is performed by transmitting a BGR byte sequence. This sequence is illustrated 1058 in Figure 89. The RGB888 frame format is illustrated in Figure 91. 

1059 Table 17 specifies the packet size constraints for RGB888 packets. The length of each packet must be a 1060 multiple of the values in the table. 

1061 

## **Table 17 RGB888 Packet Data Size Constraints** 

|**Pixels**|**Bytes**|**Bits**|
|---|---|---|
|1|3|24|



1062 Bit order in transmission follows the general CSI-2 rule, LSB first. The pixel to byte mapping is illustrated 1063 in Figure 90. 

Line Start Packet Header **B1[7:0]** G1[7:0] _**R1[7:0]**_ **B2[7:0]** G2[7:0] _**R2[7:0]**_ Line End **B639[7:0]** G639[7:0] _**R639[7:0]**_ **B640[7:0]** G640[7:0] _**R640[7:0]**_ Packet Footer 1064 

## **Figure 89 RGB888 Transmission** 

24-bit RGB pixel 

|**Data**<br>1065|B7<br>B0|B7<br>B0|B7<br>B0|B7<br>B0|B7<br>B0|B7<br>B0|B7<br>B0|B7<br>B0|B7<br>B0|B7<br>B0|B7<br>B0|B7<br>B0|B7<br>B0|B7<br>B0|B7<br>B0|B7<br>B0|B7<br>B0|B7<br>B0|B7<br>B0|B7<br>B0|B7<br>B0|B7<br>B0|B7<br>B0|B7<br>B0|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||**B1[7:0]**||||||||G1[7:0]||||||||**_R1[7:0]_**||||||||
||B0<br>B7||||||||B0<br>B7 <br>Data Trans||||||||B0<br>B7<br>mitted LS Bit First||||||||
||**B0**|**B1**|**B2**|**B3**|**B4**|**B5**|**B6**|**B7**|G0|G1|G2|G3|G4|G5|G6|G7|**_R0_**|**_R1_**|**_R2_**|**_R3_**|**_R4_**|**_R5_**|**_R6_**|**_R7_**|
||Byte n||||||||Byte n+1||||||||Byte n+2||||||||
||b0|b1|b2|b3|b4|b5|b6|b7|b0|b1|b2|b3|b4|b5|b6|b7|b0|b1|b2|b3|b4|b5|b6|b7|



**Figure 90 RGB888 Transmission in CSI-2 Bus Bitwise Illustration** 

Copyright © 2005-2014 MIPI Alliance, Inc. 

82 

All rights reserved. **Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

1066 

**==> picture [298 x 161] intentionally omitted <==**

**----- Start of picture text -----**<br>
24-bit<br>FS B G R B G R …. B G R<br>B G R B G R …. B G R<br>B G R B G R …. B G R<br>B G R B G R …. B G R<br>B G R B G R …. B G R<br>…. …. …. …. …. …. …. …. …. ….<br>…. …. …. …. …. …. …. …. …. ….<br>B G R B G R …. B G R<br>B G R B G R …. B G R<br>B G R B G R …. B G R<br>B G R B G R …. B G R<br>B G R B G R …. B G R FE<br>Packet Header, PH Packet Footer, PF<br>**----- End of picture text -----**<br>


**Figure 91 RGB888 Frame Format** 

1067 **11.3.2 RGB666** 1068 RGB666 data transmission is performed by transmitting a B0…5, G0…5, and R0…5 (18-bit) sequence. 1069 This sequence is illustrated in Figure 92. The frame format for RGB666 is presented in the Figure 94. 

1070 Table 18 specifies the packet size constraints for RGB666 packets. The length of each packet must be a 1071 multiple of the values in the table. 

1072 **Table 18 RGB666 Packet Data Size Constraints** 

|**Pixels**|**Bytes**|**Bits**|
|---|---|---|
|4|9|72|



|1073|Bit order in|transmission follows|the general CSI-2 rule, LSB first. In RGB666 case the length of one data|the general CSI-2 rule, LSB first. In RGB666 case the length of one data|the general CSI-2 rule, LSB first. In RGB666 case the length of one data|the general CSI-2 rule, LSB first. In RGB666 case the length of one data|the general CSI-2 rule, LSB first. In RGB666 case the length of one data|the general CSI-2 rule, LSB first. In RGB666 case the length of one data|
|---|---|---|---|---|---|---|---|---|
|1074|word is 18-bits, not eight bits. The word-wise flip is done for 18-bit BGR words; i.e. instead of flipping||||||||
|1075|each byte (8-bits), each 18-bits pixel value is flipped. This is illustrated in Figure||||93.||||
||Line Start|Packet Header||**BGR1[17:0]**<br>**BGR2[17:0]**||**BGR3[17:0]**|||
||||||||||
|1076|Line End|**BGR638[17:0]**||**BGR639[17:0]**<br>**BGR640[17:0]**||Packet Footer|||



**Figure 92 RGB666 Transmission with 18-bit BGR Words** 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

83 

Specification for CSI-2 

Version 1.3 29-May-2014 

1077 

|B17<br>B12|B17<br>B12|B17<br>B12|B17<br>B12|B17<br>B12|B17<br>B12|B11<br>B6|B11<br>B6|B11<br>B6|B11<br>B6|B11<br>B6|B11<br>B6|B0<br> B5|B0<br> B5|B0<br> B5|B0<br> B5|B0<br> B5|B0<br> B5|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**_R1[5:0]_**||||||G1[5:0]||||||**B1[5:0]**||||||
|B0<br>B17<br>18-bit Data Transmitted LS Bit First<br>B12<br>B11<br>B6<br>B5||||||||||||||||||
|||||||||||||B17<br>B12||||||
|**B0**|**B1**|**B2**|**B3**|**B4**|**B5**|G0|G1<br>|G2|G3|G4|G5|**_R0_**|**_R1_**|**_R2_**|**_R3_**|**_R4_**|**_R5_**|
|Byte n||||||||Byte n+1||||||||By||
|b0|b1|b2|b3|b4|b5|b6|b7|b0|b1|b2|b3|b4|b5|b6|b7|b0|b1|



**Figure 93 RGB666 Transmission on CSI-2 Bus Bitwise Illustration** 

1078 

|||8b|8b|8b|8b|8b|8b|8b|8b|8b|8b|FE<br>….<br>Packer Footer, PF<br>….<br>….<br>….<br>….<br>….<br>….<br>….<br>….<br>….<br>….<br>….<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>….<br>….<br>….<br>….|FE<br>….<br>Packer Footer, PF<br>….<br>….<br>….<br>….<br>….<br>….<br>….<br>….<br>….<br>….<br>….<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>….<br>….<br>….<br>….|FE<br>….<br>Packer Footer, PF<br>….<br>….<br>….<br>….<br>….<br>….<br>….<br>….<br>….<br>….<br>….<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>….<br>….<br>….<br>….|FE<br>….<br>Packer Footer, PF<br>….<br>….<br>….<br>….<br>….<br>….<br>….<br>….<br>….<br>….<br>….<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>….<br>….<br>….<br>….|FE<br>….<br>Packer Footer, PF<br>….<br>….<br>….<br>….<br>….<br>….<br>….<br>….<br>….<br>….<br>….<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>BGR<br>….<br>….<br>….<br>….|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||||||||||||||||||
|FS|Packer Header, PH|BGR||BGR|||BGR|||BGR||….|BGR|BGR|Packer Footer, PF||
|||BGR||BGR|||BGR|||BGR||….|BGR|BGR|||
|||BGR||BGR|||BGR|||BGR||….|BGR|BGR|||
|||BGR||BGR|||BGR|||BGR||….|BGR|BGR|||
|||BGR||BGR|||BGR|||BGR||….|BGR|BGR|||
|||….||….|||….|||….||….|….|….|||
|||….||….|||….|||….||….|….|….|||
|||BGR||BGR|||BGR|||BGR||….|BGR|BGR|||
|||BGR||BGR|||BGR|||BGR||….|BGR|BGR|||
|||BGR||BGR|||BGR|||BGR||….|BGR|BGR|||
|||BGR||BGR|||BGR|||BGR||….|BGR|BGR|||
|||BGR||BGR|||BGR|||BGR||….|BGR|BGR||FE|
|18-bit|||||||||||||||||



**Figure 94 RGB666 Frame Format** 

## 1079 **11.3.3 RGB565** 

1080 RGB565 data transmission is performed by transmitting B0…B4, G0…G5, R0…R4 in a 16-bit sequence. 1081 This sequence is illustrated in Figure 95. The frame format for RGB565 is presented in the Figure 97. 

1082 Table 19 specifies the packet size constraints for RGB565 packets. The length of each packet must be a 1083 multiple of the values in the table. 

1084 

**Table 19 RGB565 Packet Data Size Constraints** 

|**Pixels**|**Bytes**|**Bits**|
|---|---|---|
|1|2|16|



1085 Bit order in transmission follows the general CSI-2 rule, LSB first. In RGB565 case the length of one data 1086 word is 16-bits, not eight bits. The word-wise flip is done for 16-bit BGR words; i.e. instead of flipping 1087 each byte (8-bits), each two bytes (16-bits) are flipped. This is illustrated in Figure 96. 

Copyright © 2005-2014 MIPI Alliance, Inc. 

84 

All rights reserved. **Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

1088 

|**BGR1[15:0]**<br>Packet Header<br>Packet Footer<br>Line Start<br>Line End<br>**BGR2[15:0]**<br>**BGR3[15:0]**<br>**BGR638[15:0]**<br>**BGR639[15:0]**<br>**BGR640[15:0]**|Packet Header|Packet Header|**BGR1[15:0]**|**BGR1[15:0]**|**BGR2[15:0]**|**BGR2[15:0]**|**BGR3[15:0]**|**BGR3[15:0]**||
|---|---|---|---|---|---|---|---|---|---|
|||**BGR638[15:0]**||**BGR639[15:0]**||**BGR640[15:0]**||Packet Footer||



## **Figure 95 RGB565 Transmission with 16-bit BGR Words** 

16-bit RGB pixel 

1089 

|**Data**|B15<br>B11|B15<br>B11|B15<br>B11|B15<br>B11|B15<br>B11|B10<br>B5|B10<br>B5|B10<br>B5|B10<br>B5|B10<br>B5|B10<br>B5|B0<br> B4|B0<br> B4|B0<br> B4|B0<br> B4|B0<br> B4|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||**_R1[4:0]_**|||||G1[5:0]||||||**B1[4:0]**|||||
||B0<br>B15<br>16-bit Data Transmitted LS<br>Bit First<br>B11<br>B10<br>B5<br>B4||||||||||||||||
||**B0**|**B1**|**B2**|**B3**|**B4**|G0|G1|G2|G3|G4|G5|**_R0_**|**_R1_**|**_R2_**|**_R3_**|**_R4_**|
||Byte n||||||||Byte n+1||||||||
||b0|b1|b2|b3|b4|b5|b6|b7|b0|b1|b2|b3|b4|b5|b6|b7|



**Figure 96 RGB565 Transmission on CSI-2 Bus Bitwise Illustration** 

1090 

|**Figure 96 RGB565 Transmission on CSI-2 Bus Bitwise Illustration**|**Figure 96 RGB565 Transmission on CSI-2 Bus Bitwise Illustration**|**Figure 96 RGB565 Transmission on CSI-2 Bus Bitwise Illustration**|**Figure 96 RGB565 Transmission on CSI-2 Bus Bitwise Illustration**|**Figure 96 RGB565 Transmission on CSI-2 Bus Bitwise Illustration**|**Figure 96 RGB565 Transmission on CSI-2 Bus Bitwise Illustration**|**Figure 96 RGB565 Transmission on CSI-2 Bus Bitwise Illustration**|**Figure 96 RGB565 Transmission on CSI-2 Bus Bitwise Illustration**|**Figure 96 RGB565 Transmission on CSI-2 Bus Bitwise Illustration**|**Figure 96 RGB565 Transmission on CSI-2 Bus Bitwise Illustration**|
|---|---|---|---|---|---|---|---|---|---|
|16-bit||||||||||
|FS|Packer Header, PH|BGR|BGR|BGR|….|BGR|BGR|Packer Footer, PF||
|||BGR|BGR|BGR|….|BGR|BGR|||
|||BGR|BGR|BGR|….|BGR|BGR|||
|||BGR|BGR|BGR|….|BGR|BGR|||
|||BGR|BGR|BGR|….|BGR|BGR|||
|||….|….|….|….|….|….|||
|||….|….|….|….|….|….|||
|||BGR|BGR|BGR|….|BGR|BGR|||
|||BGR|BGR|BGR|….|BGR|BGR|||
|||BGR|BGR|BGR|….|BGR|BGR|||
|||BGR|BGR|BGR|….|BGR|BGR|||
|||BGR|BGR|BGR|….|BGR|BGR||FE|



**Figure 97 RGB565 Frame Format** 

## 1091 **11.3.4 RGB555** 

1092 RGB555 data can be transmitted over a CSI-2 bus with some special arrangements. The RGB555 data 1093 should be made to look like RGB565 data. This can be accomplished by inserting padding bits to the LSBs 1094 of the green color component as illustrated in Figure 98. 

1095 

Both the frame format and the package size constraints are the same as the RGB565 case. 

1096 Bit order in transmission follows the general CSI-2 rule, LSB first. In RGB555 case the length of one data 1097 word is 16-bits, not eight bits. The word-wise flip is done for 16-bit BGR words; i.e. instead of flipping 1098 each byte (8-bits), each two bytes (16-bits) are flipped. This is illustrated in Figure 98. 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. 

85 

**Confidential** 

Specification for CSI-2 

Version 1.3 29-May-2014 

## 15-bit RGB pixel padded to 16-bits 

1099 

|**Data**<br>|B15<br>B11|B15<br>B11|B15<br>B11|B15<br>B11|B15<br>B11|B10<br>B5|B10<br>B5|B10<br>B5|B10<br>B5|B10<br>B5|B10<br>B5|B0<br> B4|B0<br> B4|B0<br> B4|B0<br> B4|B0<br> B4|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||**_R1[4:0]_**|||||G1[4:0]|||||0|**B1[4:0]**|||||
||B0<br>B15<br>16-bit Data Transmitted<br>LS Bit First<br>B11<br>B10<br>B5<br>B4||||||||||||||||
||**B0**|**B1**|**B2**|**B3**|**B4**|0|G0|G1|G2|G3|G4|**_R0_**|**_R1_**|**_R2_**|**_R3_**|**_R4_**|
||Byte n||||||||Byte n+1||||||||
||b0|b1|b2|b3|b4|b5|b6|b7|b0|b1|b2|b3|b4|b5|b6|b7|



**Figure 98 RGB555 Transmission on CSI-2 Bus Bitwise Illustration** 

## 1100 **11.3.5 RGB444** 

- 1101 RGB444 data can be transmitted over a CSI-2 bus with some special arrangements. The RGB444 data 1102 should be made to look like RGB565 data. This can be accomplished by inserting padding bits to the LSBs 1103 of each color component as illustrated in Figure 99. 

- 1104 

Both the frame format and the package size constraints are the same as the RGB565 case. 

1105 Bit order in transmission follows the general CSI-2 rule, LSB first. In RGB444 case the length of one data 1106 word is 16-bits, not eight bits. The word-wise flip is done for 16-bit BGR words; i.e. instead of flipping 1107 each byte (8-bits), each two bytes (16-bits) are flipped. This is illustrated in Figure 99. 

## 12-bit RGB pixel padded to 16-bits 

|**Data**|B15<br>B11|B15<br>B11|B15<br>B11|B15<br>B11|B15<br>B11|B10<br>B5|B10<br>B5|B10<br>B5|B10<br>B5|B10<br>B5|B10<br>B5|B0<br> B4|B0<br> B4|B0<br> B4|B0<br> B4|B0<br> B4|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||**_R1[3:0]_**||||**_1_**|G1[3:0]||||1|0|**B1[3:0]**||||**1**|
||B0<br>B15<br>16-bit Data Transmitted<br>LS Bit First<br>B10B11<br>B5<br>B4||||||||||||||||
||**1**|**B0**|**B1**|**B2**|**B3**|0|1|G0|G1|G2|G3|**_1_**|**_R0_**|**_R1_**|**_R2_**|**_R3_**|
||Byte n||||||||Byte n+1||||||||
||b0|b1|b2|b3|b4|b5|b6|b7|b0|b1|b2|b3|b4|b5|b6|b7|



**Figure 99 RGB444 Transmission on CSI-2 Bus Bitwise Illustration** 

1108 

Copyright © 2005-2014 MIPI Alliance, Inc. 

86 

All rights reserved. **Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

## 1109 **11.4 RAW Image Data** 

- 1110 The RAW 6/7/8/10/12/14 modes are used for transmitting Raw image data from the image sensor. 

1111 The intent is that Raw image data is unprocessed image data (i.e. Raw Bayer data) or complementary color 1112 data, but RAW image data is not limited to these data types. 

1113 It is possible to transmit e.g. light shielded pixels in addition to effective pixels. This leads to a situation 1114 where the line length is longer than sum of effective pixels per line. The line length, if not specified 1115 otherwise, has to be a multiple of word (32 bits). 

1116 Table 20 defines the data type codes for RAW data formats described in this section. 

1117 

**Table 20 RAW Image Data Types** 

|**Data Type**|**Description**|
|---|---|
|0x28|RAW6|
|0x29|RAW7|
|0x2A|RAW8|
|0x2B|RAW10|
|0x2C|RAW12|
|0x2D|RAW14|
|0x2E|Reserved|
|0x2F|Reserved|



## 1118 **11.4.1 RAW6** 

1119 The 6-bit Raw data transmission is done by transmitting the pixel data over CSI-2 bus. Each line is 1120 separated by line start / end synchronization codes. This sequence is illustrated in Figure 100 (VGA case). 1121 Table 21 specifies the packet size constraints for RAW6 packets. The length of each packet must be a 1122 multiple of the values in the table. 

1123 

**Table 21 RAW6 Packet Data Size Constraints** 

|**Pixels**|**Bytes**|**Bits**|
|---|---|---|
|4|3|24|



1124 Each 6-bit pixel is sent LSB first. This is an exception to general CSI-2 rule byte wise LSB first. 

1125 

|**Line Start**<br>**Line End**|Packet<br>Header|Packet<br>Header|**P1[5:0]**|**P1[5:0]**|P2[5:0]|P2[5:0]|**_P3[5:0]_**|**_P3[5:0]_**|P4[5:0]|P4[5:0]|**P5[5:0]**|**P5[5:0]**|P6[5:0]|P6[5:0]|**_P7[5:0]_**|**_P7[5:0]_**||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|||||||||||||||||||
|||P634[5:0]||**_P635[5:0]_**||P636[5:0]||**P637[5:0]**||P638[5:0]||**_P639[5:0]_**||P640[5:0]||Packet<br>Footer||



## **Figure 100 RAW6 Transmission** 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

87 

Specification for CSI-2 

Version 1.3 29-May-2014 

1126 

|B4<br>B5<br>B0<br>B1<br>**_C4_**<br>**_C5_**<br>**_C0_**<br>**_C1_**<br>D4<br>D0<br>D1<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**A4**<br>**A5**<br>**A0**<br>**A1**<br>**A2**<br>**A3**<br>**Data**<br>P2[5:0] (B)<br>**_P3[5:0] (C)_**<br>~~6-bits~~<br>~~6-bits~~<br>~~6-bits~~<br>~~6-bits~~<br>P4[5:0] (D)<br>D5<br>**P1[5:0] (A)**<br>6-bit Pixel Values Transmitted LS Bit First<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|B4<br>B5<br>B0<br>B1<br>**_C4_**<br>**_C5_**<br>**_C0_**<br>**_C1_**<br>D4<br>D0<br>D1<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**A4**<br>**A5**<br>**A0**<br>**A1**<br>**A2**<br>**A3**<br>**Data**<br>P2[5:0] (B)<br>**_P3[5:0] (C)_**<br>~~6-bits~~<br>~~6-bits~~<br>~~6-bits~~<br>~~6-bits~~<br>P4[5:0] (D)<br>D5<br>**P1[5:0] (A)**<br>6-bit Pixel Values Transmitted LS Bit First<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|B4<br>B5<br>B0<br>B1<br>**_C4_**<br>**_C5_**<br>**_C0_**<br>**_C1_**<br>D4<br>D0<br>D1<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**A4**<br>**A5**<br>**A0**<br>**A1**<br>**A2**<br>**A3**<br>**Data**<br>P2[5:0] (B)<br>**_P3[5:0] (C)_**<br>~~6-bits~~<br>~~6-bits~~<br>~~6-bits~~<br>~~6-bits~~<br>P4[5:0] (D)<br>D5<br>**P1[5:0] (A)**<br>6-bit Pixel Values Transmitted LS Bit First<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|B4<br>B5<br>B0<br>B1<br>**_C4_**<br>**_C5_**<br>**_C0_**<br>**_C1_**<br>D4<br>D0<br>D1<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**A4**<br>**A5**<br>**A0**<br>**A1**<br>**A2**<br>**A3**<br>**Data**<br>P2[5:0] (B)<br>**_P3[5:0] (C)_**<br>~~6-bits~~<br>~~6-bits~~<br>~~6-bits~~<br>~~6-bits~~<br>P4[5:0] (D)<br>D5<br>**P1[5:0] (A)**<br>6-bit Pixel Values Transmitted LS Bit First<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|B4<br>B5<br>B0<br>B1<br>**_C4_**<br>**_C5_**<br>**_C0_**<br>**_C1_**<br>D4<br>D0<br>D1<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**A4**<br>**A5**<br>**A0**<br>**A1**<br>**A2**<br>**A3**<br>**Data**<br>P2[5:0] (B)<br>**_P3[5:0] (C)_**<br>~~6-bits~~<br>~~6-bits~~<br>~~6-bits~~<br>~~6-bits~~<br>P4[5:0] (D)<br>D5<br>**P1[5:0] (A)**<br>6-bit Pixel Values Transmitted LS Bit First<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|B4<br>B5<br>B0<br>B1<br>**_C4_**<br>**_C5_**<br>**_C0_**<br>**_C1_**<br>D4<br>D0<br>D1<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**A4**<br>**A5**<br>**A0**<br>**A1**<br>**A2**<br>**A3**<br>**Data**<br>P2[5:0] (B)<br>**_P3[5:0] (C)_**<br>~~6-bits~~<br>~~6-bits~~<br>~~6-bits~~<br>~~6-bits~~<br>P4[5:0] (D)<br>D5<br>**P1[5:0] (A)**<br>6-bit Pixel Values Transmitted LS Bit First<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|B4<br>B5<br>B0<br>B1<br>**_C4_**<br>**_C5_**<br>**_C0_**<br>**_C1_**<br>D4<br>D0<br>D1<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**A4**<br>**A5**<br>**A0**<br>**A1**<br>**A2**<br>**A3**<br>**Data**<br>P2[5:0] (B)<br>**_P3[5:0] (C)_**<br>~~6-bits~~<br>~~6-bits~~<br>~~6-bits~~<br>~~6-bits~~<br>P4[5:0] (D)<br>D5<br>**P1[5:0] (A)**<br>6-bit Pixel Values Transmitted LS Bit First<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|B4<br>B5<br>B0<br>B1<br>**_C4_**<br>**_C5_**<br>**_C0_**<br>**_C1_**<br>D4<br>D0<br>D1<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**A4**<br>**A5**<br>**A0**<br>**A1**<br>**A2**<br>**A3**<br>**Data**<br>P2[5:0] (B)<br>**_P3[5:0] (C)_**<br>~~6-bits~~<br>~~6-bits~~<br>~~6-bits~~<br>~~6-bits~~<br>P4[5:0] (D)<br>D5<br>**P1[5:0] (A)**<br>6-bit Pixel Values Transmitted LS Bit First<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|B4<br>B5<br>B0<br>B1<br>**_C4_**<br>**_C5_**<br>**_C0_**<br>**_C1_**<br>D4<br>D0<br>D1<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**A4**<br>**A5**<br>**A0**<br>**A1**<br>**A2**<br>**A3**<br>**Data**<br>P2[5:0] (B)<br>**_P3[5:0] (C)_**<br>~~6-bits~~<br>~~6-bits~~<br>~~6-bits~~<br>~~6-bits~~<br>P4[5:0] (D)<br>D5<br>**P1[5:0] (A)**<br>6-bit Pixel Values Transmitted LS Bit First<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|B4<br>B5<br>B0<br>B1<br>**_C4_**<br>**_C5_**<br>**_C0_**<br>**_C1_**<br>D4<br>D0<br>D1<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**A4**<br>**A5**<br>**A0**<br>**A1**<br>**A2**<br>**A3**<br>**Data**<br>P2[5:0] (B)<br>**_P3[5:0] (C)_**<br>~~6-bits~~<br>~~6-bits~~<br>~~6-bits~~<br>~~6-bits~~<br>P4[5:0] (D)<br>D5<br>**P1[5:0] (A)**<br>6-bit Pixel Values Transmitted LS Bit First<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|B4<br>B5<br>B0<br>B1<br>**_C4_**<br>**_C5_**<br>**_C0_**<br>**_C1_**<br>D4<br>D0<br>D1<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**A4**<br>**A5**<br>**A0**<br>**A1**<br>**A2**<br>**A3**<br>**Data**<br>P2[5:0] (B)<br>**_P3[5:0] (C)_**<br>~~6-bits~~<br>~~6-bits~~<br>~~6-bits~~<br>~~6-bits~~<br>P4[5:0] (D)<br>D5<br>**P1[5:0] (A)**<br>6-bit Pixel Values Transmitted LS Bit First<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|B4<br>B5<br>B0<br>B1<br>**_C4_**<br>**_C5_**<br>**_C0_**<br>**_C1_**<br>D4<br>D0<br>D1<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**A4**<br>**A5**<br>**A0**<br>**A1**<br>**A2**<br>**A3**<br>**Data**<br>P2[5:0] (B)<br>**_P3[5:0] (C)_**<br>~~6-bits~~<br>~~6-bits~~<br>~~6-bits~~<br>~~6-bits~~<br>P4[5:0] (D)<br>D5<br>**P1[5:0] (A)**<br>6-bit Pixel Values Transmitted LS Bit First<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|B4<br>B5<br>B0<br>B1<br>**_C4_**<br>**_C5_**<br>**_C0_**<br>**_C1_**<br>D4<br>D0<br>D1<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**A4**<br>**A5**<br>**A0**<br>**A1**<br>**A2**<br>**A3**<br>**Data**<br>P2[5:0] (B)<br>**_P3[5:0] (C)_**<br>~~6-bits~~<br>~~6-bits~~<br>~~6-bits~~<br>~~6-bits~~<br>P4[5:0] (D)<br>D5<br>**P1[5:0] (A)**<br>6-bit Pixel Values Transmitted LS Bit First<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|B4<br>B5<br>B0<br>B1<br>**_C4_**<br>**_C5_**<br>**_C0_**<br>**_C1_**<br>D4<br>D0<br>D1<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**A4**<br>**A5**<br>**A0**<br>**A1**<br>**A2**<br>**A3**<br>**Data**<br>P2[5:0] (B)<br>**_P3[5:0] (C)_**<br>~~6-bits~~<br>~~6-bits~~<br>~~6-bits~~<br>~~6-bits~~<br>P4[5:0] (D)<br>D5<br>**P1[5:0] (A)**<br>6-bit Pixel Values Transmitted LS Bit First<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|B4<br>B5<br>B0<br>B1<br>**_C4_**<br>**_C5_**<br>**_C0_**<br>**_C1_**<br>D4<br>D0<br>D1<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**A4**<br>**A5**<br>**A0**<br>**A1**<br>**A2**<br>**A3**<br>**Data**<br>P2[5:0] (B)<br>**_P3[5:0] (C)_**<br>~~6-bits~~<br>~~6-bits~~<br>~~6-bits~~<br>~~6-bits~~<br>P4[5:0] (D)<br>D5<br>**P1[5:0] (A)**<br>6-bit Pixel Values Transmitted LS Bit First<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|B4<br>B5<br>B0<br>B1<br>**_C4_**<br>**_C5_**<br>**_C0_**<br>**_C1_**<br>D4<br>D0<br>D1<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**A4**<br>**A5**<br>**A0**<br>**A1**<br>**A2**<br>**A3**<br>**Data**<br>P2[5:0] (B)<br>**_P3[5:0] (C)_**<br>~~6-bits~~<br>~~6-bits~~<br>~~6-bits~~<br>~~6-bits~~<br>P4[5:0] (D)<br>D5<br>**P1[5:0] (A)**<br>6-bit Pixel Values Transmitted LS Bit First<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|B4<br>B5<br>B0<br>B1<br>**_C4_**<br>**_C5_**<br>**_C0_**<br>**_C1_**<br>D4<br>D0<br>D1<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**A4**<br>**A5**<br>**A0**<br>**A1**<br>**A2**<br>**A3**<br>**Data**<br>P2[5:0] (B)<br>**_P3[5:0] (C)_**<br>~~6-bits~~<br>~~6-bits~~<br>~~6-bits~~<br>~~6-bits~~<br>P4[5:0] (D)<br>D5<br>**P1[5:0] (A)**<br>6-bit Pixel Values Transmitted LS Bit First<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|B4<br>B5<br>B0<br>B1<br>**_C4_**<br>**_C5_**<br>**_C0_**<br>**_C1_**<br>D4<br>D0<br>D1<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**A4**<br>**A5**<br>**A0**<br>**A1**<br>**A2**<br>**A3**<br>**Data**<br>P2[5:0] (B)<br>**_P3[5:0] (C)_**<br>~~6-bits~~<br>~~6-bits~~<br>~~6-bits~~<br>~~6-bits~~<br>P4[5:0] (D)<br>D5<br>**P1[5:0] (A)**<br>6-bit Pixel Values Transmitted LS Bit First<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|B4<br>B5<br>B0<br>B1<br>**_C4_**<br>**_C5_**<br>**_C0_**<br>**_C1_**<br>D4<br>D0<br>D1<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**A4**<br>**A5**<br>**A0**<br>**A1**<br>**A2**<br>**A3**<br>**Data**<br>P2[5:0] (B)<br>**_P3[5:0] (C)_**<br>~~6-bits~~<br>~~6-bits~~<br>~~6-bits~~<br>~~6-bits~~<br>P4[5:0] (D)<br>D5<br>**P1[5:0] (A)**<br>6-bit Pixel Values Transmitted LS Bit First<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|B4<br>B5<br>B0<br>B1<br>**_C4_**<br>**_C5_**<br>**_C0_**<br>**_C1_**<br>D4<br>D0<br>D1<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**A4**<br>**A5**<br>**A0**<br>**A1**<br>**A2**<br>**A3**<br>**Data**<br>P2[5:0] (B)<br>**_P3[5:0] (C)_**<br>~~6-bits~~<br>~~6-bits~~<br>~~6-bits~~<br>~~6-bits~~<br>P4[5:0] (D)<br>D5<br>**P1[5:0] (A)**<br>6-bit Pixel Values Transmitted LS Bit First<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|B4<br>B5<br>B0<br>B1<br>**_C4_**<br>**_C5_**<br>**_C0_**<br>**_C1_**<br>D4<br>D0<br>D1<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**A4**<br>**A5**<br>**A0**<br>**A1**<br>**A2**<br>**A3**<br>**Data**<br>P2[5:0] (B)<br>**_P3[5:0] (C)_**<br>~~6-bits~~<br>~~6-bits~~<br>~~6-bits~~<br>~~6-bits~~<br>P4[5:0] (D)<br>D5<br>**P1[5:0] (A)**<br>6-bit Pixel Values Transmitted LS Bit First<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|B4<br>B5<br>B0<br>B1<br>**_C4_**<br>**_C5_**<br>**_C0_**<br>**_C1_**<br>D4<br>D0<br>D1<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**A4**<br>**A5**<br>**A0**<br>**A1**<br>**A2**<br>**A3**<br>**Data**<br>P2[5:0] (B)<br>**_P3[5:0] (C)_**<br>~~6-bits~~<br>~~6-bits~~<br>~~6-bits~~<br>~~6-bits~~<br>P4[5:0] (D)<br>D5<br>**P1[5:0] (A)**<br>6-bit Pixel Values Transmitted LS Bit First<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|B4<br>B5<br>B0<br>B1<br>**_C4_**<br>**_C5_**<br>**_C0_**<br>**_C1_**<br>D4<br>D0<br>D1<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**A4**<br>**A5**<br>**A0**<br>**A1**<br>**A2**<br>**A3**<br>**Data**<br>P2[5:0] (B)<br>**_P3[5:0] (C)_**<br>~~6-bits~~<br>~~6-bits~~<br>~~6-bits~~<br>~~6-bits~~<br>P4[5:0] (D)<br>D5<br>**P1[5:0] (A)**<br>6-bit Pixel Values Transmitted LS Bit First<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|B4<br>B5<br>B0<br>B1<br>**_C4_**<br>**_C5_**<br>**_C0_**<br>**_C1_**<br>D4<br>D0<br>D1<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**A4**<br>**A5**<br>**A0**<br>**A1**<br>**A2**<br>**A3**<br>**Data**<br>P2[5:0] (B)<br>**_P3[5:0] (C)_**<br>~~6-bits~~<br>~~6-bits~~<br>~~6-bits~~<br>~~6-bits~~<br>P4[5:0] (D)<br>D5<br>**P1[5:0] (A)**<br>6-bit Pixel Values Transmitted LS Bit First<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|B4<br>B5<br>B0<br>B1<br>**_C4_**<br>**_C5_**<br>**_C0_**<br>**_C1_**<br>D4<br>D0<br>D1<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**A4**<br>**A5**<br>**A0**<br>**A1**<br>**A2**<br>**A3**<br>**Data**<br>P2[5:0] (B)<br>**_P3[5:0] (C)_**<br>~~6-bits~~<br>~~6-bits~~<br>~~6-bits~~<br>~~6-bits~~<br>P4[5:0] (D)<br>D5<br>**P1[5:0] (A)**<br>6-bit Pixel Values Transmitted LS Bit First<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||||||||||||||||||||||||||
||**A0**|**A1**|**A2**|**A3**|**A4**|**A5**|B0|B1|B2|B3|B4|B5|**_C0_**|**_C1_**|**_C2_**|**_C3_**|**_C4_**|**_C5_**|D0|D1|D2|D3|D4|D5|
||~~6-bits~~<br>~~6-bits~~<br>~~6-bits~~<br>~~6-bits~~<br>6-bit Pixel Values Transmitted LS Bit First<br>Byte n<br>Byte n+1<br>Byte n+2||||||||||||||||||||||||
||b0|b1|b2|b3|b4|b5|b6|b7|b0|b1|b2|b3|b4|b5|b6|b7|b0|b1|b2|b3|b4|b5|b6|b7|



## **Figure 101 RAW6 Data Transmission on CSI-2 Bus Bitwise Illustration** 

8-b 8-b 8-b 

||||||||FE<br>….<br>**P5**<br>Packer Footer, PF<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**|FE<br>….<br>**P5**<br>Packer Footer, PF<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**|FE<br>….<br>**P5**<br>Packer Footer, PF<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**|FE<br>….<br>**P5**<br>Packer Footer, PF<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**|FE<br>….<br>**P5**<br>Packer Footer, PF<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**|FE<br>….<br>**P5**<br>Packer Footer, PF<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**|FE<br>….<br>**P5**<br>Packer Footer, PF<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**|FE<br>….<br>**P5**<br>Packer Footer, PF<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||**P1**|P2||**_P3_**||P4|**P5**|….|**P637**|P638|**_P639_**|P640|Packer Footer, PF||
|Packer Header, PH|**P1**|P2||**_P3_**||P4|**P5**|….|**P637**|P638|**_P639_**|P640|||
||**P1**|P2||**_P3_**||P4|**P5**|….|**P637**|P638|**_P639_**|P640|||
||**P1**|P2||**_P3_**||P4|**P5**|….|**P637**|P638|**_P639_**|P640|||
||**P1**|P2||**_P3_**||P4|**P5**|….|**P637**|P638|**_P639_**|P640|||
||**P1**|P2||**_P3_**||P4|**P5**|….|**P637**|P638|**_P639_**|P640|||
||**P1**|P2||**_P3_**||P4|**P5**|….|**P637**|P638|**_P639_**|P640|||
||**P1**|P2||**_P3_**||P4|**P5**|….|**P637**|P638|**_P639_**|P640|||
||**P1**|P2||**_P3_**||P4|**P5**|….|**P637**|P638|**_P639_**|P640|||
||**P1**|P2||**_P3_**||P4|**P5**|….|**P637**|P638|**_P639_**|P640|||
||**P1**|P2||**_P3_**||P4|**P5**|….|**P637**|P638|**_P639_**|P640|||
||**P1**|P2||**_P3_**||P4|**P5**|….|**P637**|P638|**_P639_**|P640||FE|



1127 

6-bit Pixel Value 

## **Figure 102 RAW6 Frame Format** 

1128 **11.4.2 RAW7** 

1129 The 7-bit Raw data transmission is done by transmitting the pixel data over CSI-2 bus. Each line is 1130 separated by line start / end synchronization codes. This sequence is illustrated in Figure 103 (VGA case). 1131 Table 22 specifies the packet size constraints for RAW7 packets. The length of each packet must be a 1132 multiple of the values in the table. 

1133 **Table 22 RAW7 Packet Data Size Constraints** 

|**Pixels**||**Bytes**|**Bits**|
|---|---|---|---|
|8||7|56|
|Each 7-bit pixel is sent LSB first. This is an exception to general CSI-2 rule byte-wise LSB first.<br>**_P7[6:0]_**<br>**P1[6:0]**<br>Packet<br>Header<br>Packet<br>Footer<br>P640[6:0]<br>P2[6:0]<br>**_P3[6:0]_**<br>P4[6:0]<br>**P5[6:0]**<br>**P637[6:0]**<br>P638[6:0]<br>**_P639[6:0]_**<br>P636[6:0]<br>**Line Start**<br>**Line End**<br>P6[6:0]<br>**_P635[6:0]_**<br>P634[6:0]<br>**Figure 103 RAW7 Transmission**||||



1134 Each 7-bit pixel is sent LSB first. This is an exception to general CSI-2 rule byte-wise LSB first. 

1135 

88 Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

|||||**P1[6:0] (A)**|**P1[6:0] (A)**|**P1[6:0] (A)**|**P1[6:0] (A)**|**P1[6:0] (A)**|**P1[6:0] (A)**|**P1[6:0] (A)**|**P1[6:0] (A)**|**P1[6:0] (A)**|**P1[6:0] (A)**|||||||P2[6:0] (B)|P2[6:0] (B)|P2[6:0] (B)|P2[6:0] (B)|P2[6:0] (B)|P2[6:0] (B)|||||||**_P3[6:0] (C)_**|**_P3[6:0] (C)_**|**_P3[6:0] (C)_**|**_P3[6:0] (C)_**|**_P3[6:0] (C)_**|**_P3[6:0] (C)_**||||P4[6:0]|P4[6:0]|P4[6:0]|P4[6:0]|(D)|(D)|(D)||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||**Data**|**A0**||**A1**|**A2**||**A3**||**A4**|||**A5**|||**A6**||B0||B1||B2|B4<br>B3|||B5||B6|||**_C0_**|**_C1_**<br>**_C2_**|||**_C3_**|**_C6_**<br>**_C4_**<br>**_C5_**<br>D0||||||D1<br>D2||D3||D4||D5||D6||
|||||||~~7-bits~~|||||||||||||||~~7-bits~~||||||||||||~~7-bits~~||||||||~~7-bits~~||||||||||
||||||||||||||||||7-bit||||Pixel Values Transmitted LS Bit First||||||||||||||||||||||||||||||
||||||||Byte n||||||||||||||||Byte n+1||||||||||||||Byte||n+2|||||||||Byte n+3|||
|1136||b0||b1|b2||b3||b4||||b5||b6||b7||b0||b1||b3<br>b2||b4||b5|||b6|b7<br>b0|||b1|b3<br>b4<br>b2<br>b5||||||b7<br>b6||b0||b1||b2||b3|...|
|||||**Figure 104**|||||||||**RAW7 Data Transmission on CSI-2 Bus Bitwise**||||||||||||||||||||||||||||**Illustration**||||||||||
||||||||||8-b|||||8-b|||8-b||||8-b<br>8-b||||||||8-b|||8-b|||||||||||||||||||
||||||||||||||||||||||||||||||||||||||||||||||||||||
|||||FS|||||**P1**|||||P2|||**_P3_**||||P4||**P5**||P6|||||**_P7_**||P8||….|||P638||**_P639_**||P640||||||||||
||||||||||**P1**|||||P2|||**_P3_**||||P4||**P5**||P6|||||**_P7_**||P8||….|||P638||**_P639_**||P640||||||||||
||||||||||**P1**|||||P2|||**_P3_**||||P4||**P5**||P6|||||**_P7_**||P8||….|||P638||**_P639_**||P640||||||||||
|||||||Packer Header, PH|||**P1**<br>**P1**<br>**P1**<br>**P1**<br>**P1**<br>**P1**|||||P2<br>P2<br>P2<br>P2<br>P2<br>P2|||**_P3_**<br>**_P3_**<br>**_P3_**<br>**_P3_**<br>**_P3_**<br>**_P3_**||||P4<br>P4<br>P4<br>P4<br>P4<br>P4||**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**||P6<br>P6<br>P6<br>P6<br>P6<br>P6|||||**_P7_**<br>**_P7_**<br>**_P7_**<br>**_P7_**<br>**_P7_**<br>**_P7_**||P8<br>P8<br>P8<br>P8<br>P8<br>P8||….<br>….<br>….<br>….<br>….<br>….|||P638<br>P638<br>P638<br>P638<br>P638<br>P638||**_P639_**<br>**_P639_**<br>**_P639_**<br>**_P639_**<br>**_P639_**<br>**_P639_**||P640<br>P640<br>P640<br>P640<br>P640<br>P640||Packer Footer, PF||||||||
||||||||||**P1**|||||P2|||**_P3_**||||P4||**P5**||P6|||||**_P7_**||P8||….|||P638||**_P639_**||P640||||||||||
||||||||||**P1**|||||P2|||**_P3_**||||P4||**P5**||P6|||||**_P7_**||P8||….|||P638||**_P639_**||P640||||||||||
||||||||||**P1**|||||P2|||**_P3_**||||P4||**P5**||P6|||||**_P7_**||P8||….|||P638||**_P639_**||P640||||FE||||||



## 1137 

7-bit Pixel Value 

## **Figure 105 RAW7 Frame Format** 

1138 **11.4.3 RAW8** 1139 The 8-bit Raw data transmission is done by transmitting the pixel data over a CSI-2 bus. Table 23 specifies 1140 the packet size constraints for RAW8 packets. The length of each packet must be a multiple of the values in 1141 the table. 

## 1142 **Table 23 RAW8 Packet Data Size Constraints** 

|1143<br>1144<br>1145|**Pixels**|**Bytes**|**Bits**|
|---|---|---|---|
||1|1|8|
||This sequence is illustrated in Figure 106 (VGA case).<br>Bit order in transmission follows the general CSI-2 rule, LSB first.<br>**_P7[7:0]_**<br>**P1[7:0]**<br>Packet<br>Header<br>Packet<br>Footer<br>P640[7:0]<br>P2[7:0]<br>**_P3[7:0]_**<br>P4[7:0]<br>**P5[7:0]**<br>**P637[7:0]**<br>P638[7:0]<br>**_P639[7:0]_**<br>P636[7:0]<br>**Line Start**<br>**Line End**<br>P6[7:0]<br>**_P635[7:0]_**<br>P634[7:0]<br>**Figure 106 RAW8 Transmission**|||



Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

89 

Specification for CSI-2 

Version 1.3 

29-May-2014 

**==> picture [472 x 57] intentionally omitted <==**

**----- Start of picture text -----**<br>
P1[7:0] (A) P2[7:0] (B) P3[7:0] (C) P4[7:0] (D)<br>Data A0 A1 A2 A3 A4 A5 A6 A7 B0 B1 B2 B3 B4 B5 B6 B7 C0 C1 C2 C3 C4 C5 C6 C7 D0 D1 D2 D3 D4 D5 D6 D7<br>8-bits 8-bits 8-bits 8-bits<br>**----- End of picture text -----**<br>


||||||||||||||||||||||||||||||||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||**A0**|**A1**|**A2**|**A3**|**A4**|**A5**|**A6**|**A7**|B0|B1|B2<br>|B3|B4|B5|B6|B7|**_C0_**|**_C1_**|**_C2_**|**_C3_**|**_C_**|**_4_**<br>**_C5_**|**_C6_**|**_C7_**|D0|D1|D2|D3|D4|D5|D6|D7|
||~~8-bits~~||||||||~~8-bits~~||||||||~~8-bits~~||||||||~~8-bits~~||||||||
|Byte Values Transmitted LS Bit First<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+3<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>1146<br>**Figure 107 RAW8 Data Transmission on CSI-2 Bus Bitwise Illustration**<br>FS<br>**P1**<br>P2<br>FE<br>P4<br>**_P3_**<br>Packer Header, PH<br>….<br>**P5**<br>Packer Footer, PF<br>**P637**<br>P638<br>P640<br>**_P639_**<br>**P1**<br>P2<br>P4<br>**_P3_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>**P1**<br>P2<br>P4<br>**_P3_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>**P1**<br>P2<br>P4<br>**_P3_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>**P1**<br>P2<br>P4<br>**_P3_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>**P1**<br>P2<br>P4<br>**_P3_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>**P1**<br>P2<br>P4<br>**_P3_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>**P1**<br>P2<br>P4<br>**_P3_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>**P1**<br>P2<br>P4<br>**_P3_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>**P1**<br>P2<br>P4<br>**_P3_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>**P1**<br>P2<br>P4<br>**_P3_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>**P1**<br>P2<br>P4<br>**_P3_**<br>….<br>**P637**<br>P638<br>P640<br>**_P639_**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>**P5**<br>1147|Byte n||||||||Byte Values Trans<br>Byte n+1||||||||mitted LS Bit First<br>Byte n+2||||||||Byte n+3||||||||
||b0|b1|b2|b3|b4|b5|b6|b7|b0|b1|b2|b3|b4|b5|b6|b7<br>|b0|b1|b2|b3|b|4<br>b5|b6|b7|b0|b1|b2|b3<br>|b4|b5|b6|b7|



## **Figure 108 RAW8 Frame Format** 

1148 **11.4.4 RAW10** 1149 The transmission of 10-bit Raw data is done by packing the 10-bit pixel data to look like 8-bit data format. 1150 Table 24 specifies the packet size constraints for RAW10 packets. The length of each packet must be a 1151 multiple of the values in the table. 

1152 **Table 24 RAW10 Packet Data Size Constraints** 

|**Pixels**|**Bytes**|**Bits**|
|---|---|---|
|4|5|40|



1153 This sequence is illustrated in Figure 109 (VGA case). 

1154 Bit order in transmission follows the general CSI-2 rule, LSB first. 

LSB’s 

|Line Start<br>Line End<br>1155<br>90|Packet<br>Header|**P1[9:2]**|**P1[9:2]**|**P1[9:2]**|**P1[9:2]**|P2[9:2]|P2[9:2]|**_P3[9:2]_**|**_P3[9:2]_**|P4[9:2]|P4[9:2]|P4<br>[1:0]|P4<br>[1:0]|**_P3_**<br>**_[1:0]_**|P2<br>[1:0]|**P1**<br>**[1:0]**|**P1**<br>**[1:0]**|**P5[9:2]**|**P5[9:2]**|**P5[9:2]**|**P5[9:2]**|P6[9:2]|P6[9:2]||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||||||||||||||||||||||||||
||P<br>[|636<br>1:0]|**_P635_**<br>**_[1:0]_**|<br>P634<br>[1:0]|**P633**<br>**[1:0]**<br>||**P637[9:2]**||P638[9:2]||**_P639[9:2]_**||P640[9:2]||||P640<br>[1:0]||**_P639_**<br>**_[1:0]_**|P638<br>[1:0]|**P637**<br>**[1:0]**||Packet<br>Footer||
||LSB’s<br>LSB’s<br>**Figure 109 RAW10 Transmission**<br>Copyright © 2005-2014 MIPI Alliance, Inc.<br>All rights reserved.<br>**Confidential**||||||||||||||||||||||||



Version 1.3 29-May-2014 

Specification for CSI-2 

|F8<br>F9<br>B8<br>B9<br>**A9**<br>**P1**<br>**[1:0]**<br>P2<br>[1:0]<br>Byte Values Transmitted LS Bit First<br>**Data**<br>P2[9:2] (B)<br>B6<br>B7<br>B4<br>B5<br>**_C6_**<br>**_C7_**<br>**_C4_**<br>**_C5_**<br>**_C8_**<br>**_C9_**<br>**_P3[9:2] (C)_**<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>P4[9:2] (D)<br>D6<br>D7<br>D4<br>D5<br>D8<br>D9<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**_P3_**<br>**_[1:0]_**<br>P4<br>[1:0]<br>**A0**<br>**A1**<br>B0<br>B1<br>**_C0_**<br>**_C1_**<br>D0<br>D1<br>**A6**<br>**A7**<br>**A4**<br>**A5**<br>**A8**<br>**A2**<br>**A3**<br>**P1[9:2] (A)**<br>P6[9:2] (F)<br>F6<br>F7<br>F4<br>F5<br>**_G6_**<br>**_G7_**<br>**_G4_**<br>**_G5_**<br>**_G8_**<br>**_G9_**<br>**_P7[9:2] (G)_**<br>F2<br>F3<br>**_G2_**<br>**_G3_**<br>**E6**<br>**E7**<br>**E4**<br>**E5**<br>**E8**<br>**E9**<br>**E2**<br>**E3**<br>**P5[9:2] (E)**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+3<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>1156|F8<br>F9<br>B8<br>B9<br>**A9**<br>**P1**<br>**[1:0]**<br>P2<br>[1:0]<br>Byte Values Transmitted LS Bit First<br>**Data**<br>P2[9:2] (B)<br>B6<br>B7<br>B4<br>B5<br>**_C6_**<br>**_C7_**<br>**_C4_**<br>**_C5_**<br>**_C8_**<br>**_C9_**<br>**_P3[9:2] (C)_**<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>P4[9:2] (D)<br>D6<br>D7<br>D4<br>D5<br>D8<br>D9<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**_P3_**<br>**_[1:0]_**<br>P4<br>[1:0]<br>**A0**<br>**A1**<br>B0<br>B1<br>**_C0_**<br>**_C1_**<br>D0<br>D1<br>**A6**<br>**A7**<br>**A4**<br>**A5**<br>**A8**<br>**A2**<br>**A3**<br>**P1[9:2] (A)**<br>P6[9:2] (F)<br>F6<br>F7<br>F4<br>F5<br>**_G6_**<br>**_G7_**<br>**_G4_**<br>**_G5_**<br>**_G8_**<br>**_G9_**<br>**_P7[9:2] (G)_**<br>F2<br>F3<br>**_G2_**<br>**_G3_**<br>**E6**<br>**E7**<br>**E4**<br>**E5**<br>**E8**<br>**E9**<br>**E2**<br>**E3**<br>**P5[9:2] (E)**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+3<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>1156|F8<br>F9<br>B8<br>B9<br>**A9**<br>**P1**<br>**[1:0]**<br>P2<br>[1:0]<br>Byte Values Transmitted LS Bit First<br>**Data**<br>P2[9:2] (B)<br>B6<br>B7<br>B4<br>B5<br>**_C6_**<br>**_C7_**<br>**_C4_**<br>**_C5_**<br>**_C8_**<br>**_C9_**<br>**_P3[9:2] (C)_**<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>P4[9:2] (D)<br>D6<br>D7<br>D4<br>D5<br>D8<br>D9<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**_P3_**<br>**_[1:0]_**<br>P4<br>[1:0]<br>**A0**<br>**A1**<br>B0<br>B1<br>**_C0_**<br>**_C1_**<br>D0<br>D1<br>**A6**<br>**A7**<br>**A4**<br>**A5**<br>**A8**<br>**A2**<br>**A3**<br>**P1[9:2] (A)**<br>P6[9:2] (F)<br>F6<br>F7<br>F4<br>F5<br>**_G6_**<br>**_G7_**<br>**_G4_**<br>**_G5_**<br>**_G8_**<br>**_G9_**<br>**_P7[9:2] (G)_**<br>F2<br>F3<br>**_G2_**<br>**_G3_**<br>**E6**<br>**E7**<br>**E4**<br>**E5**<br>**E8**<br>**E9**<br>**E2**<br>**E3**<br>**P5[9:2] (E)**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+3<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>1156|F8<br>F9<br>B8<br>B9<br>**A9**<br>**P1**<br>**[1:0]**<br>P2<br>[1:0]<br>Byte Values Transmitted LS Bit First<br>**Data**<br>P2[9:2] (B)<br>B6<br>B7<br>B4<br>B5<br>**_C6_**<br>**_C7_**<br>**_C4_**<br>**_C5_**<br>**_C8_**<br>**_C9_**<br>**_P3[9:2] (C)_**<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>P4[9:2] (D)<br>D6<br>D7<br>D4<br>D5<br>D8<br>D9<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**_P3_**<br>**_[1:0]_**<br>P4<br>[1:0]<br>**A0**<br>**A1**<br>B0<br>B1<br>**_C0_**<br>**_C1_**<br>D0<br>D1<br>**A6**<br>**A7**<br>**A4**<br>**A5**<br>**A8**<br>**A2**<br>**A3**<br>**P1[9:2] (A)**<br>P6[9:2] (F)<br>F6<br>F7<br>F4<br>F5<br>**_G6_**<br>**_G7_**<br>**_G4_**<br>**_G5_**<br>**_G8_**<br>**_G9_**<br>**_P7[9:2] (G)_**<br>F2<br>F3<br>**_G2_**<br>**_G3_**<br>**E6**<br>**E7**<br>**E4**<br>**E5**<br>**E8**<br>**E9**<br>**E2**<br>**E3**<br>**P5[9:2] (E)**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+3<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>1156|F8<br>F9<br>B8<br>B9<br>**A9**<br>**P1**<br>**[1:0]**<br>P2<br>[1:0]<br>Byte Values Transmitted LS Bit First<br>**Data**<br>P2[9:2] (B)<br>B6<br>B7<br>B4<br>B5<br>**_C6_**<br>**_C7_**<br>**_C4_**<br>**_C5_**<br>**_C8_**<br>**_C9_**<br>**_P3[9:2] (C)_**<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>P4[9:2] (D)<br>D6<br>D7<br>D4<br>D5<br>D8<br>D9<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**_P3_**<br>**_[1:0]_**<br>P4<br>[1:0]<br>**A0**<br>**A1**<br>B0<br>B1<br>**_C0_**<br>**_C1_**<br>D0<br>D1<br>**A6**<br>**A7**<br>**A4**<br>**A5**<br>**A8**<br>**A2**<br>**A3**<br>**P1[9:2] (A)**<br>P6[9:2] (F)<br>F6<br>F7<br>F4<br>F5<br>**_G6_**<br>**_G7_**<br>**_G4_**<br>**_G5_**<br>**_G8_**<br>**_G9_**<br>**_P7[9:2] (G)_**<br>F2<br>F3<br>**_G2_**<br>**_G3_**<br>**E6**<br>**E7**<br>**E4**<br>**E5**<br>**E8**<br>**E9**<br>**E2**<br>**E3**<br>**P5[9:2] (E)**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+3<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>1156|F8<br>F9<br>B8<br>B9<br>**A9**<br>**P1**<br>**[1:0]**<br>P2<br>[1:0]<br>Byte Values Transmitted LS Bit First<br>**Data**<br>P2[9:2] (B)<br>B6<br>B7<br>B4<br>B5<br>**_C6_**<br>**_C7_**<br>**_C4_**<br>**_C5_**<br>**_C8_**<br>**_C9_**<br>**_P3[9:2] (C)_**<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>P4[9:2] (D)<br>D6<br>D7<br>D4<br>D5<br>D8<br>D9<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**_P3_**<br>**_[1:0]_**<br>P4<br>[1:0]<br>**A0**<br>**A1**<br>B0<br>B1<br>**_C0_**<br>**_C1_**<br>D0<br>D1<br>**A6**<br>**A7**<br>**A4**<br>**A5**<br>**A8**<br>**A2**<br>**A3**<br>**P1[9:2] (A)**<br>P6[9:2] (F)<br>F6<br>F7<br>F4<br>F5<br>**_G6_**<br>**_G7_**<br>**_G4_**<br>**_G5_**<br>**_G8_**<br>**_G9_**<br>**_P7[9:2] (G)_**<br>F2<br>F3<br>**_G2_**<br>**_G3_**<br>**E6**<br>**E7**<br>**E4**<br>**E5**<br>**E8**<br>**E9**<br>**E2**<br>**E3**<br>**P5[9:2] (E)**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+3<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>1156|F8<br>F9<br>B8<br>B9<br>**A9**<br>**P1**<br>**[1:0]**<br>P2<br>[1:0]<br>Byte Values Transmitted LS Bit First<br>**Data**<br>P2[9:2] (B)<br>B6<br>B7<br>B4<br>B5<br>**_C6_**<br>**_C7_**<br>**_C4_**<br>**_C5_**<br>**_C8_**<br>**_C9_**<br>**_P3[9:2] (C)_**<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>P4[9:2] (D)<br>D6<br>D7<br>D4<br>D5<br>D8<br>D9<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**_P3_**<br>**_[1:0]_**<br>P4<br>[1:0]<br>**A0**<br>**A1**<br>B0<br>B1<br>**_C0_**<br>**_C1_**<br>D0<br>D1<br>**A6**<br>**A7**<br>**A4**<br>**A5**<br>**A8**<br>**A2**<br>**A3**<br>**P1[9:2] (A)**<br>P6[9:2] (F)<br>F6<br>F7<br>F4<br>F5<br>**_G6_**<br>**_G7_**<br>**_G4_**<br>**_G5_**<br>**_G8_**<br>**_G9_**<br>**_P7[9:2] (G)_**<br>F2<br>F3<br>**_G2_**<br>**_G3_**<br>**E6**<br>**E7**<br>**E4**<br>**E5**<br>**E8**<br>**E9**<br>**E2**<br>**E3**<br>**P5[9:2] (E)**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+3<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>1156|F8<br>F9<br>B8<br>B9<br>**A9**<br>**P1**<br>**[1:0]**<br>P2<br>[1:0]<br>Byte Values Transmitted LS Bit First<br>**Data**<br>P2[9:2] (B)<br>B6<br>B7<br>B4<br>B5<br>**_C6_**<br>**_C7_**<br>**_C4_**<br>**_C5_**<br>**_C8_**<br>**_C9_**<br>**_P3[9:2] (C)_**<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>P4[9:2] (D)<br>D6<br>D7<br>D4<br>D5<br>D8<br>D9<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**_P3_**<br>**_[1:0]_**<br>P4<br>[1:0]<br>**A0**<br>**A1**<br>B0<br>B1<br>**_C0_**<br>**_C1_**<br>D0<br>D1<br>**A6**<br>**A7**<br>**A4**<br>**A5**<br>**A8**<br>**A2**<br>**A3**<br>**P1[9:2] (A)**<br>P6[9:2] (F)<br>F6<br>F7<br>F4<br>F5<br>**_G6_**<br>**_G7_**<br>**_G4_**<br>**_G5_**<br>**_G8_**<br>**_G9_**<br>**_P7[9:2] (G)_**<br>F2<br>F3<br>**_G2_**<br>**_G3_**<br>**E6**<br>**E7**<br>**E4**<br>**E5**<br>**E8**<br>**E9**<br>**E2**<br>**E3**<br>**P5[9:2] (E)**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+3<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>1156|F8<br>F9<br>B8<br>B9<br>**A9**<br>**P1**<br>**[1:0]**<br>P2<br>[1:0]<br>Byte Values Transmitted LS Bit First<br>**Data**<br>P2[9:2] (B)<br>B6<br>B7<br>B4<br>B5<br>**_C6_**<br>**_C7_**<br>**_C4_**<br>**_C5_**<br>**_C8_**<br>**_C9_**<br>**_P3[9:2] (C)_**<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>P4[9:2] (D)<br>D6<br>D7<br>D4<br>D5<br>D8<br>D9<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**_P3_**<br>**_[1:0]_**<br>P4<br>[1:0]<br>**A0**<br>**A1**<br>B0<br>B1<br>**_C0_**<br>**_C1_**<br>D0<br>D1<br>**A6**<br>**A7**<br>**A4**<br>**A5**<br>**A8**<br>**A2**<br>**A3**<br>**P1[9:2] (A)**<br>P6[9:2] (F)<br>F6<br>F7<br>F4<br>F5<br>**_G6_**<br>**_G7_**<br>**_G4_**<br>**_G5_**<br>**_G8_**<br>**_G9_**<br>**_P7[9:2] (G)_**<br>F2<br>F3<br>**_G2_**<br>**_G3_**<br>**E6**<br>**E7**<br>**E4**<br>**E5**<br>**E8**<br>**E9**<br>**E2**<br>**E3**<br>**P5[9:2] (E)**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+3<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>1156|F8<br>F9<br>B8<br>B9<br>**A9**<br>**P1**<br>**[1:0]**<br>P2<br>[1:0]<br>Byte Values Transmitted LS Bit First<br>**Data**<br>P2[9:2] (B)<br>B6<br>B7<br>B4<br>B5<br>**_C6_**<br>**_C7_**<br>**_C4_**<br>**_C5_**<br>**_C8_**<br>**_C9_**<br>**_P3[9:2] (C)_**<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>P4[9:2] (D)<br>D6<br>D7<br>D4<br>D5<br>D8<br>D9<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**_P3_**<br>**_[1:0]_**<br>P4<br>[1:0]<br>**A0**<br>**A1**<br>B0<br>B1<br>**_C0_**<br>**_C1_**<br>D0<br>D1<br>**A6**<br>**A7**<br>**A4**<br>**A5**<br>**A8**<br>**A2**<br>**A3**<br>**P1[9:2] (A)**<br>P6[9:2] (F)<br>F6<br>F7<br>F4<br>F5<br>**_G6_**<br>**_G7_**<br>**_G4_**<br>**_G5_**<br>**_G8_**<br>**_G9_**<br>**_P7[9:2] (G)_**<br>F2<br>F3<br>**_G2_**<br>**_G3_**<br>**E6**<br>**E7**<br>**E4**<br>**E5**<br>**E8**<br>**E9**<br>**E2**<br>**E3**<br>**P5[9:2] (E)**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+3<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>1156|F8<br>F9<br>B8<br>B9<br>**A9**<br>**P1**<br>**[1:0]**<br>P2<br>[1:0]<br>Byte Values Transmitted LS Bit First<br>**Data**<br>P2[9:2] (B)<br>B6<br>B7<br>B4<br>B5<br>**_C6_**<br>**_C7_**<br>**_C4_**<br>**_C5_**<br>**_C8_**<br>**_C9_**<br>**_P3[9:2] (C)_**<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>P4[9:2] (D)<br>D6<br>D7<br>D4<br>D5<br>D8<br>D9<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**_P3_**<br>**_[1:0]_**<br>P4<br>[1:0]<br>**A0**<br>**A1**<br>B0<br>B1<br>**_C0_**<br>**_C1_**<br>D0<br>D1<br>**A6**<br>**A7**<br>**A4**<br>**A5**<br>**A8**<br>**A2**<br>**A3**<br>**P1[9:2] (A)**<br>P6[9:2] (F)<br>F6<br>F7<br>F4<br>F5<br>**_G6_**<br>**_G7_**<br>**_G4_**<br>**_G5_**<br>**_G8_**<br>**_G9_**<br>**_P7[9:2] (G)_**<br>F2<br>F3<br>**_G2_**<br>**_G3_**<br>**E6**<br>**E7**<br>**E4**<br>**E5**<br>**E8**<br>**E9**<br>**E2**<br>**E3**<br>**P5[9:2] (E)**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+3<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>1156|F8<br>F9<br>B8<br>B9<br>**A9**<br>**P1**<br>**[1:0]**<br>P2<br>[1:0]<br>Byte Values Transmitted LS Bit First<br>**Data**<br>P2[9:2] (B)<br>B6<br>B7<br>B4<br>B5<br>**_C6_**<br>**_C7_**<br>**_C4_**<br>**_C5_**<br>**_C8_**<br>**_C9_**<br>**_P3[9:2] (C)_**<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>P4[9:2] (D)<br>D6<br>D7<br>D4<br>D5<br>D8<br>D9<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**_P3_**<br>**_[1:0]_**<br>P4<br>[1:0]<br>**A0**<br>**A1**<br>B0<br>B1<br>**_C0_**<br>**_C1_**<br>D0<br>D1<br>**A6**<br>**A7**<br>**A4**<br>**A5**<br>**A8**<br>**A2**<br>**A3**<br>**P1[9:2] (A)**<br>P6[9:2] (F)<br>F6<br>F7<br>F4<br>F5<br>**_G6_**<br>**_G7_**<br>**_G4_**<br>**_G5_**<br>**_G8_**<br>**_G9_**<br>**_P7[9:2] (G)_**<br>F2<br>F3<br>**_G2_**<br>**_G3_**<br>**E6**<br>**E7**<br>**E4**<br>**E5**<br>**E8**<br>**E9**<br>**E2**<br>**E3**<br>**P5[9:2] (E)**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+3<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>1156|F8<br>F9<br>B8<br>B9<br>**A9**<br>**P1**<br>**[1:0]**<br>P2<br>[1:0]<br>Byte Values Transmitted LS Bit First<br>**Data**<br>P2[9:2] (B)<br>B6<br>B7<br>B4<br>B5<br>**_C6_**<br>**_C7_**<br>**_C4_**<br>**_C5_**<br>**_C8_**<br>**_C9_**<br>**_P3[9:2] (C)_**<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>P4[9:2] (D)<br>D6<br>D7<br>D4<br>D5<br>D8<br>D9<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**_P3_**<br>**_[1:0]_**<br>P4<br>[1:0]<br>**A0**<br>**A1**<br>B0<br>B1<br>**_C0_**<br>**_C1_**<br>D0<br>D1<br>**A6**<br>**A7**<br>**A4**<br>**A5**<br>**A8**<br>**A2**<br>**A3**<br>**P1[9:2] (A)**<br>P6[9:2] (F)<br>F6<br>F7<br>F4<br>F5<br>**_G6_**<br>**_G7_**<br>**_G4_**<br>**_G5_**<br>**_G8_**<br>**_G9_**<br>**_P7[9:2] (G)_**<br>F2<br>F3<br>**_G2_**<br>**_G3_**<br>**E6**<br>**E7**<br>**E4**<br>**E5**<br>**E8**<br>**E9**<br>**E2**<br>**E3**<br>**P5[9:2] (E)**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+3<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>1156|F8<br>F9<br>B8<br>B9<br>**A9**<br>**P1**<br>**[1:0]**<br>P2<br>[1:0]<br>Byte Values Transmitted LS Bit First<br>**Data**<br>P2[9:2] (B)<br>B6<br>B7<br>B4<br>B5<br>**_C6_**<br>**_C7_**<br>**_C4_**<br>**_C5_**<br>**_C8_**<br>**_C9_**<br>**_P3[9:2] (C)_**<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>P4[9:2] (D)<br>D6<br>D7<br>D4<br>D5<br>D8<br>D9<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**_P3_**<br>**_[1:0]_**<br>P4<br>[1:0]<br>**A0**<br>**A1**<br>B0<br>B1<br>**_C0_**<br>**_C1_**<br>D0<br>D1<br>**A6**<br>**A7**<br>**A4**<br>**A5**<br>**A8**<br>**A2**<br>**A3**<br>**P1[9:2] (A)**<br>P6[9:2] (F)<br>F6<br>F7<br>F4<br>F5<br>**_G6_**<br>**_G7_**<br>**_G4_**<br>**_G5_**<br>**_G8_**<br>**_G9_**<br>**_P7[9:2] (G)_**<br>F2<br>F3<br>**_G2_**<br>**_G3_**<br>**E6**<br>**E7**<br>**E4**<br>**E5**<br>**E8**<br>**E9**<br>**E2**<br>**E3**<br>**P5[9:2] (E)**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+3<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>1156|F8<br>F9<br>B8<br>B9<br>**A9**<br>**P1**<br>**[1:0]**<br>P2<br>[1:0]<br>Byte Values Transmitted LS Bit First<br>**Data**<br>P2[9:2] (B)<br>B6<br>B7<br>B4<br>B5<br>**_C6_**<br>**_C7_**<br>**_C4_**<br>**_C5_**<br>**_C8_**<br>**_C9_**<br>**_P3[9:2] (C)_**<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>P4[9:2] (D)<br>D6<br>D7<br>D4<br>D5<br>D8<br>D9<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**_P3_**<br>**_[1:0]_**<br>P4<br>[1:0]<br>**A0**<br>**A1**<br>B0<br>B1<br>**_C0_**<br>**_C1_**<br>D0<br>D1<br>**A6**<br>**A7**<br>**A4**<br>**A5**<br>**A8**<br>**A2**<br>**A3**<br>**P1[9:2] (A)**<br>P6[9:2] (F)<br>F6<br>F7<br>F4<br>F5<br>**_G6_**<br>**_G7_**<br>**_G4_**<br>**_G5_**<br>**_G8_**<br>**_G9_**<br>**_P7[9:2] (G)_**<br>F2<br>F3<br>**_G2_**<br>**_G3_**<br>**E6**<br>**E7**<br>**E4**<br>**E5**<br>**E8**<br>**E9**<br>**E2**<br>**E3**<br>**P5[9:2] (E)**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+3<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>1156|F8<br>F9<br>B8<br>B9<br>**A9**<br>**P1**<br>**[1:0]**<br>P2<br>[1:0]<br>Byte Values Transmitted LS Bit First<br>**Data**<br>P2[9:2] (B)<br>B6<br>B7<br>B4<br>B5<br>**_C6_**<br>**_C7_**<br>**_C4_**<br>**_C5_**<br>**_C8_**<br>**_C9_**<br>**_P3[9:2] (C)_**<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>P4[9:2] (D)<br>D6<br>D7<br>D4<br>D5<br>D8<br>D9<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**_P3_**<br>**_[1:0]_**<br>P4<br>[1:0]<br>**A0**<br>**A1**<br>B0<br>B1<br>**_C0_**<br>**_C1_**<br>D0<br>D1<br>**A6**<br>**A7**<br>**A4**<br>**A5**<br>**A8**<br>**A2**<br>**A3**<br>**P1[9:2] (A)**<br>P6[9:2] (F)<br>F6<br>F7<br>F4<br>F5<br>**_G6_**<br>**_G7_**<br>**_G4_**<br>**_G5_**<br>**_G8_**<br>**_G9_**<br>**_P7[9:2] (G)_**<br>F2<br>F3<br>**_G2_**<br>**_G3_**<br>**E6**<br>**E7**<br>**E4**<br>**E5**<br>**E8**<br>**E9**<br>**E2**<br>**E3**<br>**P5[9:2] (E)**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+3<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>1156|F8<br>F9<br>B8<br>B9<br>**A9**<br>**P1**<br>**[1:0]**<br>P2<br>[1:0]<br>Byte Values Transmitted LS Bit First<br>**Data**<br>P2[9:2] (B)<br>B6<br>B7<br>B4<br>B5<br>**_C6_**<br>**_C7_**<br>**_C4_**<br>**_C5_**<br>**_C8_**<br>**_C9_**<br>**_P3[9:2] (C)_**<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>P4[9:2] (D)<br>D6<br>D7<br>D4<br>D5<br>D8<br>D9<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**_P3_**<br>**_[1:0]_**<br>P4<br>[1:0]<br>**A0**<br>**A1**<br>B0<br>B1<br>**_C0_**<br>**_C1_**<br>D0<br>D1<br>**A6**<br>**A7**<br>**A4**<br>**A5**<br>**A8**<br>**A2**<br>**A3**<br>**P1[9:2] (A)**<br>P6[9:2] (F)<br>F6<br>F7<br>F4<br>F5<br>**_G6_**<br>**_G7_**<br>**_G4_**<br>**_G5_**<br>**_G8_**<br>**_G9_**<br>**_P7[9:2] (G)_**<br>F2<br>F3<br>**_G2_**<br>**_G3_**<br>**E6**<br>**E7**<br>**E4**<br>**E5**<br>**E8**<br>**E9**<br>**E2**<br>**E3**<br>**P5[9:2] (E)**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+3<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>1156|F8<br>F9<br>B8<br>B9<br>**A9**<br>**P1**<br>**[1:0]**<br>P2<br>[1:0]<br>Byte Values Transmitted LS Bit First<br>**Data**<br>P2[9:2] (B)<br>B6<br>B7<br>B4<br>B5<br>**_C6_**<br>**_C7_**<br>**_C4_**<br>**_C5_**<br>**_C8_**<br>**_C9_**<br>**_P3[9:2] (C)_**<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>P4[9:2] (D)<br>D6<br>D7<br>D4<br>D5<br>D8<br>D9<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**_P3_**<br>**_[1:0]_**<br>P4<br>[1:0]<br>**A0**<br>**A1**<br>B0<br>B1<br>**_C0_**<br>**_C1_**<br>D0<br>D1<br>**A6**<br>**A7**<br>**A4**<br>**A5**<br>**A8**<br>**A2**<br>**A3**<br>**P1[9:2] (A)**<br>P6[9:2] (F)<br>F6<br>F7<br>F4<br>F5<br>**_G6_**<br>**_G7_**<br>**_G4_**<br>**_G5_**<br>**_G8_**<br>**_G9_**<br>**_P7[9:2] (G)_**<br>F2<br>F3<br>**_G2_**<br>**_G3_**<br>**E6**<br>**E7**<br>**E4**<br>**E5**<br>**E8**<br>**E9**<br>**E2**<br>**E3**<br>**P5[9:2] (E)**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+3<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>1156|F8<br>F9<br>B8<br>B9<br>**A9**<br>**P1**<br>**[1:0]**<br>P2<br>[1:0]<br>Byte Values Transmitted LS Bit First<br>**Data**<br>P2[9:2] (B)<br>B6<br>B7<br>B4<br>B5<br>**_C6_**<br>**_C7_**<br>**_C4_**<br>**_C5_**<br>**_C8_**<br>**_C9_**<br>**_P3[9:2] (C)_**<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>P4[9:2] (D)<br>D6<br>D7<br>D4<br>D5<br>D8<br>D9<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**_P3_**<br>**_[1:0]_**<br>P4<br>[1:0]<br>**A0**<br>**A1**<br>B0<br>B1<br>**_C0_**<br>**_C1_**<br>D0<br>D1<br>**A6**<br>**A7**<br>**A4**<br>**A5**<br>**A8**<br>**A2**<br>**A3**<br>**P1[9:2] (A)**<br>P6[9:2] (F)<br>F6<br>F7<br>F4<br>F5<br>**_G6_**<br>**_G7_**<br>**_G4_**<br>**_G5_**<br>**_G8_**<br>**_G9_**<br>**_P7[9:2] (G)_**<br>F2<br>F3<br>**_G2_**<br>**_G3_**<br>**E6**<br>**E7**<br>**E4**<br>**E5**<br>**E8**<br>**E9**<br>**E2**<br>**E3**<br>**P5[9:2] (E)**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+3<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>1156|F8<br>F9<br>B8<br>B9<br>**A9**<br>**P1**<br>**[1:0]**<br>P2<br>[1:0]<br>Byte Values Transmitted LS Bit First<br>**Data**<br>P2[9:2] (B)<br>B6<br>B7<br>B4<br>B5<br>**_C6_**<br>**_C7_**<br>**_C4_**<br>**_C5_**<br>**_C8_**<br>**_C9_**<br>**_P3[9:2] (C)_**<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>P4[9:2] (D)<br>D6<br>D7<br>D4<br>D5<br>D8<br>D9<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**_P3_**<br>**_[1:0]_**<br>P4<br>[1:0]<br>**A0**<br>**A1**<br>B0<br>B1<br>**_C0_**<br>**_C1_**<br>D0<br>D1<br>**A6**<br>**A7**<br>**A4**<br>**A5**<br>**A8**<br>**A2**<br>**A3**<br>**P1[9:2] (A)**<br>P6[9:2] (F)<br>F6<br>F7<br>F4<br>F5<br>**_G6_**<br>**_G7_**<br>**_G4_**<br>**_G5_**<br>**_G8_**<br>**_G9_**<br>**_P7[9:2] (G)_**<br>F2<br>F3<br>**_G2_**<br>**_G3_**<br>**E6**<br>**E7**<br>**E4**<br>**E5**<br>**E8**<br>**E9**<br>**E2**<br>**E3**<br>**P5[9:2] (E)**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+3<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>1156|F8<br>F9<br>B8<br>B9<br>**A9**<br>**P1**<br>**[1:0]**<br>P2<br>[1:0]<br>Byte Values Transmitted LS Bit First<br>**Data**<br>P2[9:2] (B)<br>B6<br>B7<br>B4<br>B5<br>**_C6_**<br>**_C7_**<br>**_C4_**<br>**_C5_**<br>**_C8_**<br>**_C9_**<br>**_P3[9:2] (C)_**<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>P4[9:2] (D)<br>D6<br>D7<br>D4<br>D5<br>D8<br>D9<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**_P3_**<br>**_[1:0]_**<br>P4<br>[1:0]<br>**A0**<br>**A1**<br>B0<br>B1<br>**_C0_**<br>**_C1_**<br>D0<br>D1<br>**A6**<br>**A7**<br>**A4**<br>**A5**<br>**A8**<br>**A2**<br>**A3**<br>**P1[9:2] (A)**<br>P6[9:2] (F)<br>F6<br>F7<br>F4<br>F5<br>**_G6_**<br>**_G7_**<br>**_G4_**<br>**_G5_**<br>**_G8_**<br>**_G9_**<br>**_P7[9:2] (G)_**<br>F2<br>F3<br>**_G2_**<br>**_G3_**<br>**E6**<br>**E7**<br>**E4**<br>**E5**<br>**E8**<br>**E9**<br>**E2**<br>**E3**<br>**P5[9:2] (E)**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+3<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>1156|F8<br>F9<br>B8<br>B9<br>**A9**<br>**P1**<br>**[1:0]**<br>P2<br>[1:0]<br>Byte Values Transmitted LS Bit First<br>**Data**<br>P2[9:2] (B)<br>B6<br>B7<br>B4<br>B5<br>**_C6_**<br>**_C7_**<br>**_C4_**<br>**_C5_**<br>**_C8_**<br>**_C9_**<br>**_P3[9:2] (C)_**<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>P4[9:2] (D)<br>D6<br>D7<br>D4<br>D5<br>D8<br>D9<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**_P3_**<br>**_[1:0]_**<br>P4<br>[1:0]<br>**A0**<br>**A1**<br>B0<br>B1<br>**_C0_**<br>**_C1_**<br>D0<br>D1<br>**A6**<br>**A7**<br>**A4**<br>**A5**<br>**A8**<br>**A2**<br>**A3**<br>**P1[9:2] (A)**<br>P6[9:2] (F)<br>F6<br>F7<br>F4<br>F5<br>**_G6_**<br>**_G7_**<br>**_G4_**<br>**_G5_**<br>**_G8_**<br>**_G9_**<br>**_P7[9:2] (G)_**<br>F2<br>F3<br>**_G2_**<br>**_G3_**<br>**E6**<br>**E7**<br>**E4**<br>**E5**<br>**E8**<br>**E9**<br>**E2**<br>**E3**<br>**P5[9:2] (E)**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+3<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>1156|F8<br>F9<br>B8<br>B9<br>**A9**<br>**P1**<br>**[1:0]**<br>P2<br>[1:0]<br>Byte Values Transmitted LS Bit First<br>**Data**<br>P2[9:2] (B)<br>B6<br>B7<br>B4<br>B5<br>**_C6_**<br>**_C7_**<br>**_C4_**<br>**_C5_**<br>**_C8_**<br>**_C9_**<br>**_P3[9:2] (C)_**<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>P4[9:2] (D)<br>D6<br>D7<br>D4<br>D5<br>D8<br>D9<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**_P3_**<br>**_[1:0]_**<br>P4<br>[1:0]<br>**A0**<br>**A1**<br>B0<br>B1<br>**_C0_**<br>**_C1_**<br>D0<br>D1<br>**A6**<br>**A7**<br>**A4**<br>**A5**<br>**A8**<br>**A2**<br>**A3**<br>**P1[9:2] (A)**<br>P6[9:2] (F)<br>F6<br>F7<br>F4<br>F5<br>**_G6_**<br>**_G7_**<br>**_G4_**<br>**_G5_**<br>**_G8_**<br>**_G9_**<br>**_P7[9:2] (G)_**<br>F2<br>F3<br>**_G2_**<br>**_G3_**<br>**E6**<br>**E7**<br>**E4**<br>**E5**<br>**E8**<br>**E9**<br>**E2**<br>**E3**<br>**P5[9:2] (E)**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+3<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>1156|F8<br>F9<br>B8<br>B9<br>**A9**<br>**P1**<br>**[1:0]**<br>P2<br>[1:0]<br>Byte Values Transmitted LS Bit First<br>**Data**<br>P2[9:2] (B)<br>B6<br>B7<br>B4<br>B5<br>**_C6_**<br>**_C7_**<br>**_C4_**<br>**_C5_**<br>**_C8_**<br>**_C9_**<br>**_P3[9:2] (C)_**<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>P4[9:2] (D)<br>D6<br>D7<br>D4<br>D5<br>D8<br>D9<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**_P3_**<br>**_[1:0]_**<br>P4<br>[1:0]<br>**A0**<br>**A1**<br>B0<br>B1<br>**_C0_**<br>**_C1_**<br>D0<br>D1<br>**A6**<br>**A7**<br>**A4**<br>**A5**<br>**A8**<br>**A2**<br>**A3**<br>**P1[9:2] (A)**<br>P6[9:2] (F)<br>F6<br>F7<br>F4<br>F5<br>**_G6_**<br>**_G7_**<br>**_G4_**<br>**_G5_**<br>**_G8_**<br>**_G9_**<br>**_P7[9:2] (G)_**<br>F2<br>F3<br>**_G2_**<br>**_G3_**<br>**E6**<br>**E7**<br>**E4**<br>**E5**<br>**E8**<br>**E9**<br>**E2**<br>**E3**<br>**P5[9:2] (E)**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+3<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>1156|F8<br>F9<br>B8<br>B9<br>**A9**<br>**P1**<br>**[1:0]**<br>P2<br>[1:0]<br>Byte Values Transmitted LS Bit First<br>**Data**<br>P2[9:2] (B)<br>B6<br>B7<br>B4<br>B5<br>**_C6_**<br>**_C7_**<br>**_C4_**<br>**_C5_**<br>**_C8_**<br>**_C9_**<br>**_P3[9:2] (C)_**<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>P4[9:2] (D)<br>D6<br>D7<br>D4<br>D5<br>D8<br>D9<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**_P3_**<br>**_[1:0]_**<br>P4<br>[1:0]<br>**A0**<br>**A1**<br>B0<br>B1<br>**_C0_**<br>**_C1_**<br>D0<br>D1<br>**A6**<br>**A7**<br>**A4**<br>**A5**<br>**A8**<br>**A2**<br>**A3**<br>**P1[9:2] (A)**<br>P6[9:2] (F)<br>F6<br>F7<br>F4<br>F5<br>**_G6_**<br>**_G7_**<br>**_G4_**<br>**_G5_**<br>**_G8_**<br>**_G9_**<br>**_P7[9:2] (G)_**<br>F2<br>F3<br>**_G2_**<br>**_G3_**<br>**E6**<br>**E7**<br>**E4**<br>**E5**<br>**E8**<br>**E9**<br>**E2**<br>**E3**<br>**P5[9:2] (E)**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+3<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>1156|F8<br>F9<br>B8<br>B9<br>**A9**<br>**P1**<br>**[1:0]**<br>P2<br>[1:0]<br>Byte Values Transmitted LS Bit First<br>**Data**<br>P2[9:2] (B)<br>B6<br>B7<br>B4<br>B5<br>**_C6_**<br>**_C7_**<br>**_C4_**<br>**_C5_**<br>**_C8_**<br>**_C9_**<br>**_P3[9:2] (C)_**<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>P4[9:2] (D)<br>D6<br>D7<br>D4<br>D5<br>D8<br>D9<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**_P3_**<br>**_[1:0]_**<br>P4<br>[1:0]<br>**A0**<br>**A1**<br>B0<br>B1<br>**_C0_**<br>**_C1_**<br>D0<br>D1<br>**A6**<br>**A7**<br>**A4**<br>**A5**<br>**A8**<br>**A2**<br>**A3**<br>**P1[9:2] (A)**<br>P6[9:2] (F)<br>F6<br>F7<br>F4<br>F5<br>**_G6_**<br>**_G7_**<br>**_G4_**<br>**_G5_**<br>**_G8_**<br>**_G9_**<br>**_P7[9:2] (G)_**<br>F2<br>F3<br>**_G2_**<br>**_G3_**<br>**E6**<br>**E7**<br>**E4**<br>**E5**<br>**E8**<br>**E9**<br>**E2**<br>**E3**<br>**P5[9:2] (E)**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+3<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>1156|F8<br>F9<br>B8<br>B9<br>**A9**<br>**P1**<br>**[1:0]**<br>P2<br>[1:0]<br>Byte Values Transmitted LS Bit First<br>**Data**<br>P2[9:2] (B)<br>B6<br>B7<br>B4<br>B5<br>**_C6_**<br>**_C7_**<br>**_C4_**<br>**_C5_**<br>**_C8_**<br>**_C9_**<br>**_P3[9:2] (C)_**<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>P4[9:2] (D)<br>D6<br>D7<br>D4<br>D5<br>D8<br>D9<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**_P3_**<br>**_[1:0]_**<br>P4<br>[1:0]<br>**A0**<br>**A1**<br>B0<br>B1<br>**_C0_**<br>**_C1_**<br>D0<br>D1<br>**A6**<br>**A7**<br>**A4**<br>**A5**<br>**A8**<br>**A2**<br>**A3**<br>**P1[9:2] (A)**<br>P6[9:2] (F)<br>F6<br>F7<br>F4<br>F5<br>**_G6_**<br>**_G7_**<br>**_G4_**<br>**_G5_**<br>**_G8_**<br>**_G9_**<br>**_P7[9:2] (G)_**<br>F2<br>F3<br>**_G2_**<br>**_G3_**<br>**E6**<br>**E7**<br>**E4**<br>**E5**<br>**E8**<br>**E9**<br>**E2**<br>**E3**<br>**P5[9:2] (E)**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+3<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>1156|F8<br>F9<br>B8<br>B9<br>**A9**<br>**P1**<br>**[1:0]**<br>P2<br>[1:0]<br>Byte Values Transmitted LS Bit First<br>**Data**<br>P2[9:2] (B)<br>B6<br>B7<br>B4<br>B5<br>**_C6_**<br>**_C7_**<br>**_C4_**<br>**_C5_**<br>**_C8_**<br>**_C9_**<br>**_P3[9:2] (C)_**<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>P4[9:2] (D)<br>D6<br>D7<br>D4<br>D5<br>D8<br>D9<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**_P3_**<br>**_[1:0]_**<br>P4<br>[1:0]<br>**A0**<br>**A1**<br>B0<br>B1<br>**_C0_**<br>**_C1_**<br>D0<br>D1<br>**A6**<br>**A7**<br>**A4**<br>**A5**<br>**A8**<br>**A2**<br>**A3**<br>**P1[9:2] (A)**<br>P6[9:2] (F)<br>F6<br>F7<br>F4<br>F5<br>**_G6_**<br>**_G7_**<br>**_G4_**<br>**_G5_**<br>**_G8_**<br>**_G9_**<br>**_P7[9:2] (G)_**<br>F2<br>F3<br>**_G2_**<br>**_G3_**<br>**E6**<br>**E7**<br>**E4**<br>**E5**<br>**E8**<br>**E9**<br>**E2**<br>**E3**<br>**P5[9:2] (E)**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+3<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>1156|F8<br>F9<br>B8<br>B9<br>**A9**<br>**P1**<br>**[1:0]**<br>P2<br>[1:0]<br>Byte Values Transmitted LS Bit First<br>**Data**<br>P2[9:2] (B)<br>B6<br>B7<br>B4<br>B5<br>**_C6_**<br>**_C7_**<br>**_C4_**<br>**_C5_**<br>**_C8_**<br>**_C9_**<br>**_P3[9:2] (C)_**<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>P4[9:2] (D)<br>D6<br>D7<br>D4<br>D5<br>D8<br>D9<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**_P3_**<br>**_[1:0]_**<br>P4<br>[1:0]<br>**A0**<br>**A1**<br>B0<br>B1<br>**_C0_**<br>**_C1_**<br>D0<br>D1<br>**A6**<br>**A7**<br>**A4**<br>**A5**<br>**A8**<br>**A2**<br>**A3**<br>**P1[9:2] (A)**<br>P6[9:2] (F)<br>F6<br>F7<br>F4<br>F5<br>**_G6_**<br>**_G7_**<br>**_G4_**<br>**_G5_**<br>**_G8_**<br>**_G9_**<br>**_P7[9:2] (G)_**<br>F2<br>F3<br>**_G2_**<br>**_G3_**<br>**E6**<br>**E7**<br>**E4**<br>**E5**<br>**E8**<br>**E9**<br>**E2**<br>**E3**<br>**P5[9:2] (E)**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+3<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>1156|F8<br>F9<br>B8<br>B9<br>**A9**<br>**P1**<br>**[1:0]**<br>P2<br>[1:0]<br>Byte Values Transmitted LS Bit First<br>**Data**<br>P2[9:2] (B)<br>B6<br>B7<br>B4<br>B5<br>**_C6_**<br>**_C7_**<br>**_C4_**<br>**_C5_**<br>**_C8_**<br>**_C9_**<br>**_P3[9:2] (C)_**<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>P4[9:2] (D)<br>D6<br>D7<br>D4<br>D5<br>D8<br>D9<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**_P3_**<br>**_[1:0]_**<br>P4<br>[1:0]<br>**A0**<br>**A1**<br>B0<br>B1<br>**_C0_**<br>**_C1_**<br>D0<br>D1<br>**A6**<br>**A7**<br>**A4**<br>**A5**<br>**A8**<br>**A2**<br>**A3**<br>**P1[9:2] (A)**<br>P6[9:2] (F)<br>F6<br>F7<br>F4<br>F5<br>**_G6_**<br>**_G7_**<br>**_G4_**<br>**_G5_**<br>**_G8_**<br>**_G9_**<br>**_P7[9:2] (G)_**<br>F2<br>F3<br>**_G2_**<br>**_G3_**<br>**E6**<br>**E7**<br>**E4**<br>**E5**<br>**E8**<br>**E9**<br>**E2**<br>**E3**<br>**P5[9:2] (E)**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+3<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>1156|F8<br>F9<br>B8<br>B9<br>**A9**<br>**P1**<br>**[1:0]**<br>P2<br>[1:0]<br>Byte Values Transmitted LS Bit First<br>**Data**<br>P2[9:2] (B)<br>B6<br>B7<br>B4<br>B5<br>**_C6_**<br>**_C7_**<br>**_C4_**<br>**_C5_**<br>**_C8_**<br>**_C9_**<br>**_P3[9:2] (C)_**<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>P4[9:2] (D)<br>D6<br>D7<br>D4<br>D5<br>D8<br>D9<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**_P3_**<br>**_[1:0]_**<br>P4<br>[1:0]<br>**A0**<br>**A1**<br>B0<br>B1<br>**_C0_**<br>**_C1_**<br>D0<br>D1<br>**A6**<br>**A7**<br>**A4**<br>**A5**<br>**A8**<br>**A2**<br>**A3**<br>**P1[9:2] (A)**<br>P6[9:2] (F)<br>F6<br>F7<br>F4<br>F5<br>**_G6_**<br>**_G7_**<br>**_G4_**<br>**_G5_**<br>**_G8_**<br>**_G9_**<br>**_P7[9:2] (G)_**<br>F2<br>F3<br>**_G2_**<br>**_G3_**<br>**E6**<br>**E7**<br>**E4**<br>**E5**<br>**E8**<br>**E9**<br>**E2**<br>**E3**<br>**P5[9:2] (E)**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+3<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>1156|F8<br>F9<br>B8<br>B9<br>**A9**<br>**P1**<br>**[1:0]**<br>P2<br>[1:0]<br>Byte Values Transmitted LS Bit First<br>**Data**<br>P2[9:2] (B)<br>B6<br>B7<br>B4<br>B5<br>**_C6_**<br>**_C7_**<br>**_C4_**<br>**_C5_**<br>**_C8_**<br>**_C9_**<br>**_P3[9:2] (C)_**<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>P4[9:2] (D)<br>D6<br>D7<br>D4<br>D5<br>D8<br>D9<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**_P3_**<br>**_[1:0]_**<br>P4<br>[1:0]<br>**A0**<br>**A1**<br>B0<br>B1<br>**_C0_**<br>**_C1_**<br>D0<br>D1<br>**A6**<br>**A7**<br>**A4**<br>**A5**<br>**A8**<br>**A2**<br>**A3**<br>**P1[9:2] (A)**<br>P6[9:2] (F)<br>F6<br>F7<br>F4<br>F5<br>**_G6_**<br>**_G7_**<br>**_G4_**<br>**_G5_**<br>**_G8_**<br>**_G9_**<br>**_P7[9:2] (G)_**<br>F2<br>F3<br>**_G2_**<br>**_G3_**<br>**E6**<br>**E7**<br>**E4**<br>**E5**<br>**E8**<br>**E9**<br>**E2**<br>**E3**<br>**P5[9:2] (E)**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+3<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>1156|F8<br>F9<br>B8<br>B9<br>**A9**<br>**P1**<br>**[1:0]**<br>P2<br>[1:0]<br>Byte Values Transmitted LS Bit First<br>**Data**<br>P2[9:2] (B)<br>B6<br>B7<br>B4<br>B5<br>**_C6_**<br>**_C7_**<br>**_C4_**<br>**_C5_**<br>**_C8_**<br>**_C9_**<br>**_P3[9:2] (C)_**<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>P4[9:2] (D)<br>D6<br>D7<br>D4<br>D5<br>D8<br>D9<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**_P3_**<br>**_[1:0]_**<br>P4<br>[1:0]<br>**A0**<br>**A1**<br>B0<br>B1<br>**_C0_**<br>**_C1_**<br>D0<br>D1<br>**A6**<br>**A7**<br>**A4**<br>**A5**<br>**A8**<br>**A2**<br>**A3**<br>**P1[9:2] (A)**<br>P6[9:2] (F)<br>F6<br>F7<br>F4<br>F5<br>**_G6_**<br>**_G7_**<br>**_G4_**<br>**_G5_**<br>**_G8_**<br>**_G9_**<br>**_P7[9:2] (G)_**<br>F2<br>F3<br>**_G2_**<br>**_G3_**<br>**E6**<br>**E7**<br>**E4**<br>**E5**<br>**E8**<br>**E9**<br>**E2**<br>**E3**<br>**P5[9:2] (E)**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+3<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>1156|F8<br>F9<br>B8<br>B9<br>**A9**<br>**P1**<br>**[1:0]**<br>P2<br>[1:0]<br>Byte Values Transmitted LS Bit First<br>**Data**<br>P2[9:2] (B)<br>B6<br>B7<br>B4<br>B5<br>**_C6_**<br>**_C7_**<br>**_C4_**<br>**_C5_**<br>**_C8_**<br>**_C9_**<br>**_P3[9:2] (C)_**<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>P4[9:2] (D)<br>D6<br>D7<br>D4<br>D5<br>D8<br>D9<br>D2<br>D3<br>B2<br>B3<br>**_C2_**<br>**_C3_**<br>**_P3_**<br>**_[1:0]_**<br>P4<br>[1:0]<br>**A0**<br>**A1**<br>B0<br>B1<br>**_C0_**<br>**_C1_**<br>D0<br>D1<br>**A6**<br>**A7**<br>**A4**<br>**A5**<br>**A8**<br>**A2**<br>**A3**<br>**P1[9:2] (A)**<br>P6[9:2] (F)<br>F6<br>F7<br>F4<br>F5<br>**_G6_**<br>**_G7_**<br>**_G4_**<br>**_G5_**<br>**_G8_**<br>**_G9_**<br>**_P7[9:2] (G)_**<br>F2<br>F3<br>**_G2_**<br>**_G3_**<br>**E6**<br>**E7**<br>**E4**<br>**E5**<br>**E8**<br>**E9**<br>**E2**<br>**E3**<br>**P5[9:2] (E)**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+3<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>1156|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|||||||||||||||||||||||||||||||||||
||**A2**|**A3**|**A4**|**A5**|**A6**|**A7**|**A8**|**A9**|B2|B3|B4|B5|B6|B7|B8<br>|B9|**_C2_**|**_C3_**|**_C4_**|**_C5_**|**_C6_**|**_C7_**|**_C8_**|**_C9_**|D2|D3|D4|D5|D6|D7|D8|D9||
|||||||||||||||||||||||||||||||||||
|||||||||||||||||||||||||||||||||||
||**P1**<br>**[1:0]**<br>P2<br>[1:0]<br>**_P3_**<br>**_[1:0]_**<br>P4<br>[1:0]||||||||**P5[9:2] (E)**||||||||P6[9:2] (F)||||||||**_P7[9:2] (G)_**|||||||||
||**A0**|**A1**|B0|B1|**_C0_**|**_C1_**|D0|D1|**E2**|**E3**|**E4**|**E5**|**E6**|**E7**|**E8**<br>|**E9**|F2|F3|F4|F5|F6|F7|F8|F9|**_G2_**|**_G3_**|**_G4_**|**_G5_**|**_G6_**<br>|**_G7_**|**_G8_**|**_G9_**||
||~~8-bits~~<br>Byte n||||||||Byte Values Trans<br>~~8-bits~~<br>Byte n+1||||||||mitted LS Bit First<br>~~8-bits~~<br>Byte n+2||||||||~~8-bits~~<br>Byte n+3|||||||||
||b0|b1|b2|b3|b4|b5|b6|b7|b0|b1|b2|b3|b4|b5|b6|b7|b0|b1|b2|b3|b4|b5|b6|b7|b0|b1|b2|b3|b4|b5|b6|b7||



## **Figure 110 RAW10 Data Transmission on CSI-2 Bus Bitwise Illustration** 

1157 

|FS||**P1**|P2|**_P3_**|P4|**LSBs**|**P5**|….|**P637**|P638|**_P639_**|P640|**LSBs**|Packer Footer, PF||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||Packer Header, PH|**P1**|P2|**_P3_**|P4|**LSBs**|**P5**|….|**P637**|P638|**_P639_**|P640|**LSBs**|||
|||**P1**|P2|**_P3_**|P4|**LSBs**|**P5**|….|**P637**|P638|**_P639_**|P640|**LSBs**|||
|||**P1**|P2|**_P3_**|P4|**LSBs**|**P5**|….|**P637**|P638|**_P639_**|P640|**LSBs**|||
|||**P1**|P2|**_P3_**|P4|**LSBs**|**P5**|….|**P637**|P638|**_P639_**|P640|**LSBs**|||
|||**P1**|P2|**_P3_**|P4|**LSBs**|**P5**|….|**P637**|P638|**_P639_**|P640|**LSBs**|||
|||**P1**|P2|**_P3_**|P4|**LSBs**|**P5**|….|**P637**|P638|**_P639_**|P640|**LSBs**|||
|||**P1**|P2|**_P3_**|P4|**LSBs**|**P5**|….|**P637**|P638|**_P639_**|P640|**LSBs**|||
|||**P1**|P2|**_P3_**|P4|**LSBs**|**P5**|….|**P637**|P638|**_P639_**|P640|**LSBs**|||
|||**P1**|P2|**_P3_**|P4|**LSBs**|**P5**|….|**P637**|P638|**_P639_**|P640|**LSBs**|||
|||**P1**|P2|**_P3_**|P4|**LSBs**|**P5**|….|**P637**|P638|**_P639_**|P640|**LSBs**|||
|||**P1**|P2|**_P3_**|P4|**LSBs**|**P5**|….|**P637**|P638|**_P639_**|P640|**LSBs**||FE|



**Figure 111 RAW10 Frame Format** 

1158 **11.4.5 RAW12** 1159 The transmission of 12-bit Raw data is done by packing the 12-bit pixel data to look like 8-bit data format. 1160 Table 25 specifies the packet size constraints for RAW12 packets. The length of each packet must be a 1161 multiple of the values in the table. 

1162 

## **Table 25 RAW12 Packet Data Size Constraints** 

|**Pixels**|**Bytes**|**Bits**|
|---|---|---|
|2|3|24|



1163 This sequence is illustrated in Figure 112 (VGA case). 

1164 Bit order in transmission follows the general CSI-2 rule, LSB first. 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

91 

Specification for CSI-2 

Version 1.3 29-May-2014 

||||||||||||||||||LSB’s||||||LSB’s|LSB’s|LSB’s|LSB’s|LSB’s|||||||||||||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||**Line Start**||||Packet<br>Header|||**P1[11:4]**||||||||P2[11:4]|P2<br>[3:0]<br>**P1**<br>**[3:0]**<br>**_P3[11:4]_**||P4[11:4]||||P4<br>[3:0]||**_P3_**<br>**_[3:0]_**|||||**P5[11:4]**||||||||||||
|||||||||||||||||||||||||||||||||||||||||||
||**Line End**|||||**P635**<br>**[3:0]**<br>P636<br>[3:0]|||||P638[11:4]<br>**_P639[11:4]_**<br>P640[11:4]<br>**P637[11:4]**<br>**P637**<br>**[3:0]**<br>P638<br>[3:0]<br>P640<br>[3:0]||||||||||||||||**_P639_**<br>**_[3:0]_**||||||||Packet<br>Footer|||||||
|1165|||||||LSB’s||||||||||LSB’s||||||LSB’s|||||||||||||||||||
||||||||||||||||**Figure 112 RAW12 Transmission**|||||||||||||||||||||||||||
||||||**P1[11:4] (A)**|||||||||||**P1[3:0] (A)** <br>P2[11:4] (B)|||P2[3:0 (B)]|||||||**_P3[11:4] (C)_**||||||||||||||||
||**Data**|**A4**|**A5**||**A6**<br>**A7**<br>**A8**<br>**A9**|||||||**A10**||**A2**<br>**A3**<br>**A0**<br>**A1**<br>B6<br>B7<br>B4<br>B5<br>B8<br>B9<br>B10<br>B11<br>**A11**||||B0<br>B1||B2<br>B3|||**_C4_**<br>**_C5_**|||**_C6_**|||**_C7_**|||**_C8_**|||**_C9_**|**_C10_**||**_C11_**||||
||||||||~~8-bits~~|||||||||~~8-bits~~<br>~~8-bits~~|||||||||||||~~8-bits~~|||||||||||||
|||||||||||||||||Byte Values Transmitted LS Bit|||First|||||||||||||||||||||||
||||||||Byte n|||||||||Byte n+1<br>Byte|||n+2|||||||||Byte|||||n+3|||||||||
|1166||b0|b1||b3<br>b4<br>b2<br>b5|||||||b6||b7<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>b3<br>b0<br>b1<br>b2||||b4<br>b5|||b7<br>b6||b0<br>b1|||b2|||b3|||b4|||b5||b6||b7|||
|||||||**Figure 113 RAW12 Transmission on CSI-2 Bus Bitwise Illustration**||||||||||||||||||||||||||||||||||||
|||||FS|||**P1**|||||P2|||**LSBs**|P4<br>**_P3_**|**LSBs**<br>….<br>P638<br>**LSBs**||**_P639_**||P640||**LSBs**|||||||||||||||||||
||||||||**P1**|||||P2|||**LSBs**|P4<br>**_P3_**|**LSBs**<br>….<br>P638<br>**LSBs**||**_P639_**||P640||**LSBs**|||||||||||||||||||
||||||||**P1**|||||P2|||**LSBs**|P4<br>**_P3_**|**LSBs**<br>….<br>P638<br>**LSBs**||**_P639_**||P640||**LSBs**|||||||||||||||||||
||||||||Packer Header, PH<br>**P1**<br>**P1**<br>**P1**<br>**P1**<br>**P1**<br>**P1**|||||P2<br>P2<br>P2<br>P2<br>P2<br>P2|||**LSBs**<br>**LSBs**<br>**LSBs**<br>**LSBs**<br>**LSBs**<br>**LSBs**|P4<br>**_P3_**<br>P4<br>**_P3_**<br>P4<br>**_P3_**<br>P4<br>**_P3_**<br>P4<br>**_P3_**<br>P4<br>**_P3_**|**LSBs**<br>….<br>P638<br>**LSBs**<br>….<br>P638<br>**LSBs**<br>….<br>P638<br>**LSBs**<br>….<br>P638<br>**LSBs**<br>….<br>P638<br>**LSBs**<br>….<br>P638<br>**LSBs**<br>**LSBs**<br>**LSBs**<br>**LSBs**<br>**LSBs**<br>**LSBs**||**_P639_**<br>**_P639_**<br>**_P639_**<br>**_P639_**<br>**_P639_**<br>**_P639_**||P640<br>P640<br>P640<br>P640<br>P640<br>P640||**LSBs**<br>**LSBs**<br>**LSBs**<br>**LSBs**<br>**LSBs**<br>**LSBs**|||Packer Footer, PF||||||||||||||||
||||||||**P1**|||||P2|||**LSBs**|P4<br>**_P3_**|**LSBs**<br>….<br>P638<br>**LSBs**||**_P639_**||P640||**LSBs**|||||||||||||||||||
||||||||**P1**|||||P2|||**LSBs**|P4<br>**_P3_**|**LSBs**<br>….<br>P638<br>**LSBs**||**_P639_**||P640||**LSBs**|||||||||||||||||||
|1167|||||||**P1**|||||P2|||**LSBs**|P4<br>**_P3_**|**LSBs**<br>….<br>P638<br>**LSBs**||**_P639_**||P640||**LSBs**||||||FE|||||||||||||
||||||||||||||||**Figure 114**||**RAW12 Frame Format**|||||||||||||||||||||||||
|1168|**11.4.6**|||**RAW14**||||||||||||||||||||||||||||||||||||||
|1169|The transmission of 14-bit Raw data is done by packing the 14-bit pixel data in 8-bit slices.|||||||||||||||||||||||||||||For every four||||||||||||
|1170|pixels, seven bytes of data is|||||||||||||generated. Table|||26 specifies the packet||size constraints for RAW14 packets.|||||||||||||||||||||||
|1171|The length||of||each packet||||||must be a multiple of the values in the table.|||||||||||||||||||||||||||||||
|1172||||||||||||**Ta**||**b**|**le 26**|**RAW14**|**Packet Data Size Co**||**nstra**||**ints**|||||||||||||||||||||



**Table 26 RAW14 Packet Data Size Constraints** 

|**Pixels**|**Bytes**|**Bits**|
|---|---|---|
|4|7|56|



1173 The sequence is illustrated in Figure 115 (VGA case). 1174 The LS bits for P1, P2, P3 and P4 are distributed in three bytes as shown in Figure 116. The same is true for 1175 the LS bits for P637, P638, P639 and P640. The bit order during transmission follows the general CSI-2 1176 rule, i.e. LSB first. 

Copyright © 2005-2014 MIPI Alliance, Inc. 

92 

All rights reserved. **Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

LSB’s 

1177 

## 1178 

|Packet<br>Footer<br>P638[13:6]<br>**_P639[13:6]_**<br>P640[13:6]<br>**P637[13:6]**<br>**P637**<br>**[5:0]**<br>P638<br>[5:0]<br>P640<br>[5:0]<br>**_P639_**<br>**_[5:0]_**<br>**P1**<br>**[5:0]**<br>**P1[13:6]**<br>Packet<br>Header<br>P2[13:6]<br>**_P3[13:6]_**<br>P4[13:6]<br>P2<br>[5:0]<br>P4<br>[5:0]<br>**_P3_**<br>**_[5:0]_**<br>**Line Start**<br>**Line End**<br>LSB’s<br>**Figure 115 RAW14 Transmission**<br>D8<br>D9<br>D6<br>D7<br>D10<br>D11<br>D12<br>D13<br>**_C2_**<br>**_C3_**<br>**_C0_**<br>**_C1_**<br>**_C4_**<br>**_C5_**<br>**A2**<br>**A3**<br>**A0**<br>**A1**<br>B2<br>B3<br>B0<br>B1<br>**A4**<br>**A5**<br>B4<br>B5<br>D2<br>D3<br>D0<br>D1<br>D4<br>D5<br>B10<br>B11<br>B8<br>B9<br>B12<br>B13<br>**_C10_**<br>**_C11_**<br>**_C8_**<br>**_C9_**<br>**_C12_**<br>**_C13_**<br>B6<br>B7<br>**_C6_**<br>**_C7_**<br>**A10**<br>**A11**<br>**A8**<br>**A9**<br>**A12**<br>**A13**<br>**A6**<br>**A7**<br>**E10**<br>**E11**<br>**E8**<br>**E9**<br>**E12**<br>**E13**<br>**E6**<br>**E7**<br>**P1[5:0] (A)**<br>Byte Values Transmitted LS Bit First<br>**Data**<br>P4[5:0] (D)<br>P4[13:6] (D)<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>P2[13:6] (B)<br>**_P3[13:6] (C)_**<br>**P1[13:6] (A)**<br>**P5[13:6] (E)**<br>P2[5:0]  (B)<br>**_P3[5:0] (C)_**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+3<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|Packet<br>Footer<br>P638[13:6]<br>**_P639[13:6]_**<br>P640[13:6]<br>**P637[13:6]**<br>**P637**<br>**[5:0]**<br>P638<br>[5:0]<br>P640<br>[5:0]<br>**_P639_**<br>**_[5:0]_**<br>**P1**<br>**[5:0]**<br>**P1[13:6]**<br>Packet<br>Header<br>P2[13:6]<br>**_P3[13:6]_**<br>P4[13:6]<br>P2<br>[5:0]<br>P4<br>[5:0]<br>**_P3_**<br>**_[5:0]_**<br>**Line Start**<br>**Line End**<br>LSB’s<br>**Figure 115 RAW14 Transmission**<br>D8<br>D9<br>D6<br>D7<br>D10<br>D11<br>D12<br>D13<br>**_C2_**<br>**_C3_**<br>**_C0_**<br>**_C1_**<br>**_C4_**<br>**_C5_**<br>**A2**<br>**A3**<br>**A0**<br>**A1**<br>B2<br>B3<br>B0<br>B1<br>**A4**<br>**A5**<br>B4<br>B5<br>D2<br>D3<br>D0<br>D1<br>D4<br>D5<br>B10<br>B11<br>B8<br>B9<br>B12<br>B13<br>**_C10_**<br>**_C11_**<br>**_C8_**<br>**_C9_**<br>**_C12_**<br>**_C13_**<br>B6<br>B7<br>**_C6_**<br>**_C7_**<br>**A10**<br>**A11**<br>**A8**<br>**A9**<br>**A12**<br>**A13**<br>**A6**<br>**A7**<br>**E10**<br>**E11**<br>**E8**<br>**E9**<br>**E12**<br>**E13**<br>**E6**<br>**E7**<br>**P1[5:0] (A)**<br>Byte Values Transmitted LS Bit First<br>**Data**<br>P4[5:0] (D)<br>P4[13:6] (D)<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>P2[13:6] (B)<br>**_P3[13:6] (C)_**<br>**P1[13:6] (A)**<br>**P5[13:6] (E)**<br>P2[5:0]  (B)<br>**_P3[5:0] (C)_**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+3<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|Packet<br>Footer<br>P638[13:6]<br>**_P639[13:6]_**<br>P640[13:6]<br>**P637[13:6]**<br>**P637**<br>**[5:0]**<br>P638<br>[5:0]<br>P640<br>[5:0]<br>**_P639_**<br>**_[5:0]_**<br>**P1**<br>**[5:0]**<br>**P1[13:6]**<br>Packet<br>Header<br>P2[13:6]<br>**_P3[13:6]_**<br>P4[13:6]<br>P2<br>[5:0]<br>P4<br>[5:0]<br>**_P3_**<br>**_[5:0]_**<br>**Line Start**<br>**Line End**<br>LSB’s<br>**Figure 115 RAW14 Transmission**<br>D8<br>D9<br>D6<br>D7<br>D10<br>D11<br>D12<br>D13<br>**_C2_**<br>**_C3_**<br>**_C0_**<br>**_C1_**<br>**_C4_**<br>**_C5_**<br>**A2**<br>**A3**<br>**A0**<br>**A1**<br>B2<br>B3<br>B0<br>B1<br>**A4**<br>**A5**<br>B4<br>B5<br>D2<br>D3<br>D0<br>D1<br>D4<br>D5<br>B10<br>B11<br>B8<br>B9<br>B12<br>B13<br>**_C10_**<br>**_C11_**<br>**_C8_**<br>**_C9_**<br>**_C12_**<br>**_C13_**<br>B6<br>B7<br>**_C6_**<br>**_C7_**<br>**A10**<br>**A11**<br>**A8**<br>**A9**<br>**A12**<br>**A13**<br>**A6**<br>**A7**<br>**E10**<br>**E11**<br>**E8**<br>**E9**<br>**E12**<br>**E13**<br>**E6**<br>**E7**<br>**P1[5:0] (A)**<br>Byte Values Transmitted LS Bit First<br>**Data**<br>P4[5:0] (D)<br>P4[13:6] (D)<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>~~8-bits~~<br>P2[13:6] (B)<br>**_P3[13:6] (C)_**<br>**P1[13:6] (A)**<br>**P5[13:6] (E)**<br>P2[5:0]  (B)<br>**_P3[5:0] (C)_**<br>Byte n<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+1<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+2<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5<br>Byte n+3<br>b7<br>b6<br>b3<br>b4<br>b0<br>b1<br>b2<br>b5|Packet<br>Footer<br>P638[13:6]<br>**_P639[13:6]_**<br>P640[13:6]<br>**P637[13:6]**<br>**P637**<br>**[5:0]**<br>P638<br>[5:0]<br>P640<br>[5:0]<br>**_P639_**<br>**_[5:0]_**<br>**P1**<br>**[5:0]**<br>**P1[13:6]**<br>Packet<br>Header<br>P2[13:6]<br>**_P3[13:6]_**<br>P4[13:6]<br>P2<br>[5:0]<br>P4<br>[5:0]<br>**_P3_**<br>**_[5:0]_**<br>LSB’s<br>**Figure 115 RAW14 Transmission**<br>D8<br>D9<br>D6<br>D7<br>D10<br>D11<br>D12<br>D13<br>B10<br>B11<br>B8<br>B9<br>B12<br>B13<br>**_C10_**<br>**_C11_**<br>**_C8_**<br>**_C9_**<br>**_C12_**<br>**_C13_**<br>B6<br>B7<br>**_C6_**<br>**_C7_**<br>**A10**<br>**A11**<br>**A8**<br>**A9**<br>**A12**<br>**A13**<br>**7**<br>P4[13:6] (D)<br>P2[13:6] (B)<br>**_P3[13:6] (C)_**<br>**P1[13:6] (A)**|Packet<br>Footer<br>P638[13:6]<br>**_P639[13:6]_**<br>P640[13:6]<br>**P637[13:6]**<br>**P637**<br>**[5:0]**<br>P638<br>[5:0]<br>P640<br>[5:0]<br>**_P639_**<br>**_[5:0]_**<br>**P1**<br>**[5:0]**<br>**P1[13:6]**<br>Packet<br>Header<br>P2[13:6]<br>**_P3[13:6]_**<br>P4[13:6]<br>P2<br>[5:0]<br>P4<br>[5:0]<br>**_P3_**<br>**_[5:0]_**<br>LSB’s<br>**Figure 115 RAW14 Transmission**<br>D8<br>D9<br>D6<br>D7<br>D10<br>D11<br>D12<br>D13<br>B10<br>B11<br>B8<br>B9<br>B12<br>B13<br>**_C10_**<br>**_C11_**<br>**_C8_**<br>**_C9_**<br>**_C12_**<br>**_C13_**<br>B6<br>B7<br>**_C6_**<br>**_C7_**<br>**A10**<br>**A11**<br>**A8**<br>**A9**<br>**A12**<br>**A13**<br>**7**<br>P4[13:6] (D)<br>P2[13:6] (B)<br>**_P3[13:6] (C)_**<br>**P1[13:6] (A)**|Packet<br>Footer<br>P638[13:6]<br>**_P639[13:6]_**<br>P640[13:6]<br>**P637[13:6]**<br>**P637**<br>**[5:0]**<br>P638<br>[5:0]<br>P640<br>[5:0]<br>**_P639_**<br>**_[5:0]_**<br>**P1**<br>**[5:0]**<br>**P1[13:6]**<br>Packet<br>Header<br>P2[13:6]<br>**_P3[13:6]_**<br>P4[13:6]<br>P2<br>[5:0]<br>P4<br>[5:0]<br>**_P3_**<br>**_[5:0]_**<br>LSB’s<br>**Figure 115 RAW14 Transmission**<br>D8<br>D9<br>D6<br>D7<br>D10<br>D11<br>D12<br>D13<br>B10<br>B11<br>B8<br>B9<br>B12<br>B13<br>**_C10_**<br>**_C11_**<br>**_C8_**<br>**_C9_**<br>**_C12_**<br>**_C13_**<br>B6<br>B7<br>**_C6_**<br>**_C7_**<br>**A10**<br>**A11**<br>**A8**<br>**A9**<br>**A12**<br>**A13**<br>**7**<br>P4[13:6] (D)<br>P2[13:6] (B)<br>**_P3[13:6] (C)_**<br>**P1[13:6] (A)**|Packet<br>Footer<br>P638[13:6]<br>**_P639[13:6]_**<br>P640[13:6]<br>**P637[13:6]**<br>**P637**<br>**[5:0]**<br>P638<br>[5:0]<br>P640<br>[5:0]<br>**_P639_**<br>**_[5:0]_**<br>**P1**<br>**[5:0]**<br>**P1[13:6]**<br>Packet<br>Header<br>P2[13:6]<br>**_P3[13:6]_**<br>P4[13:6]<br>P2<br>[5:0]<br>P4<br>[5:0]<br>**_P3_**<br>**_[5:0]_**<br>LSB’s<br>**Figure 115 RAW14 Transmission**<br>D8<br>D9<br>D6<br>D7<br>D10<br>D11<br>D12<br>D13<br>B10<br>B11<br>B8<br>B9<br>B12<br>B13<br>**_C10_**<br>**_C11_**<br>**_C8_**<br>**_C9_**<br>**_C12_**<br>**_C13_**<br>B6<br>B7<br>**_C6_**<br>**_C7_**<br>**A10**<br>**A11**<br>**A8**<br>**A9**<br>**A12**<br>**A13**<br>**7**<br>P4[13:6] (D)<br>P2[13:6] (B)<br>**_P3[13:6] (C)_**<br>**P1[13:6] (A)**|Packet<br>Footer<br>P638[13:6]<br>**_P639[13:6]_**<br>P640[13:6]<br>**P637[13:6]**<br>**P637**<br>**[5:0]**<br>P638<br>[5:0]<br>P640<br>[5:0]<br>**_P639_**<br>**_[5:0]_**<br>**P1**<br>**[5:0]**<br>**P1[13:6]**<br>Packet<br>Header<br>P2[13:6]<br>**_P3[13:6]_**<br>P4[13:6]<br>P2<br>[5:0]<br>P4<br>[5:0]<br>**_P3_**<br>**_[5:0]_**<br>LSB’s<br>**Figure 115 RAW14 Transmission**<br>D8<br>D9<br>D6<br>D7<br>D10<br>D11<br>D12<br>D13<br>B10<br>B11<br>B8<br>B9<br>B12<br>B13<br>**_C10_**<br>**_C11_**<br>**_C8_**<br>**_C9_**<br>**_C12_**<br>**_C13_**<br>B6<br>B7<br>**_C6_**<br>**_C7_**<br>**A10**<br>**A11**<br>**A8**<br>**A9**<br>**A12**<br>**A13**<br>**7**<br>P4[13:6] (D)<br>P2[13:6] (B)<br>**_P3[13:6] (C)_**<br>**P1[13:6] (A)**|**P1[13:6]**|**P1[13:6]**|**P1[13:6]**|**P1[13:6]**|P2[13:6]|P2[13:6]|P2[13:6]|P2[13:6]|**_P3[13:6]_**|**_P3[13:6]_**|**_P3[13:6]_**|**_P3[13:6]_**|P4[13:6]|P4[13:6]|P4[13:6]|P4[13:6]|P4[13:6]|P4[13:6]|**P1**<br>**[5:0]**|**P1**<br>**[5:0]**|P2<br>[5:0]|P2<br>[5:0]|P2<br>[5:0]|**_P3_**<br>**_[5:0]_**|**_P3_**<br>**_[5:0]_**|**_P3_**<br>**_[5:0]_**|P4<br>[5:0]|P4<br>[5:0]|P4<br>[5:0]||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|||||||||||||||||||||||||||||||||||||||
||||||**P637[13:6]**||||P638[13:6]<br>||||**_P639[13:6]_**||||P640[13:6]|||||**P637**<br>**[5:0]**||||P638<br>[5:0]||**_P639_**<br>**_[5:0]_**|||P640<br>[5:0]|||Packet<br>Footer||||
|||||||||||||||||||||||||||||||||||||||
|||**A6**<br>|**7**|**A8**||**A9**|**A10**<br>|**11**|**A12**|**A1**|B6<br>|B7|B8|B9|B10|B11|B12|B13|**_C6_**||**_C7_**||**_C8_**|**_C9_**|**_C1_**|**_C11_**<br>|**_12_**<br>**_C_**|**_3_**|D6|D7|8|D9|D10<br>|D11|D12|D13||
|||||||||||||||||||||||||||||||||||||||
|||||||||||||||||||||||||||||||||||||||
|||**P1[5:0] (A)**<br>P|||||||||||||||||P4[5:0] (D)<br>**_C)_**||||||||||**P5[13:6] (E)**|||||||||
||||||||||||2[5:0]  (B)<br>**_P3[5:0] (_**|||||||||||||||||||||||||||
|||||||||||||||||||||||||||||||||||||||
|||**A0**<br>|**1**|**A2**||**A3**|**A4**<br>|**A5**|B0|B1|B2<br>|B3|B4|B5|**_C0_**|**_C1_**|**_C2_**|**_C3_**|**_C4_**||**_C5_**||D0|D1|D|D3<br>|D4<br>|5|**E6**|**E7**|**8**|**E9**|**E10**<br>|**E11**|**E12**|**E13**||
|||||||||||||||||||||||||||||||||||||||
|||~~8-bits~~<br>Byte n|||||||||||||||||||||||||||~~8-bits~~<br>Byte n+3|||||||||
||||||||||||~~8-bits~~||||||||~~8-bits~~|||||||||||||||||||
||||||||||||Byte Values Trans<br>Byte n+1||||||||mitted LS Bit First<br>Byte n+2|||||||||||||||||||
|||b0<br>|b1|b2||b3|b4|b5|b6|b7|b0|b1|b2|b3|b4|b5|b6|b7|b0||b1||b2|b3|b4|b5|b<br>b6|7|b0|b1<br>|b2|b3|b4|b5|b6|b7||



## **Figure 116 RAW14 Transmission on CSI-2 Bus Bitwise Illustration** 

## 1179 

|||||||8-b<br>8-b<br>8-b<br>8-b<br>8-b<br>8-b|8-b<br>8-b<br>8-b<br>8-b<br>8-b<br>8-b|8-b<br>8-b<br>8-b<br>8-b<br>8-b<br>8-b|8-b<br>8-b<br>8-b<br>8-b<br>8-b<br>8-b|8-b<br>8-b<br>8-b<br>8-b<br>8-b<br>8-b|8-b<br>8-b<br>8-b<br>8-b<br>8-b<br>8-b|8-b<br>8-b<br>8-b<br>8-b<br>8-b<br>8-b|8-b<br>8-b<br>8-b<br>8-b<br>8-b<br>8-b|8-b<br>8-b<br>8-b<br>8-b<br>8-b<br>8-b|8-b<br>8-b<br>8-b<br>8-b<br>8-b<br>8-b|8-b<br>8-b<br>8-b<br>8-b<br>8-b<br>8-b|8-b<br>8-b<br>8-b<br>8-b<br>8-b<br>8-b|8-b<br>8-b<br>8-b<br>8-b<br>8-b<br>8-b|8-b<br>8-b<br>8-b<br>8-b<br>8-b<br>8-b|8-b<br>8-b<br>8-b<br>8-b<br>8-b<br>8-b|8-b<br>8-b<br>8-b<br>8-b<br>8-b<br>8-b|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|||||||||||||||||||||FE<br>Packer Footer, PF<br><br><br><br><br><br><br><br><br><br><br><br>||
|FS|Packer Header, PH|**P1**|P2|**_P3_**|P4|**LSBs**|**LSBs**||**LSBs**||**LSBs**|….|P640|**LSBs**|**LSBs**||**LSBs**||**LSBs**|Packer Footer, PF<br><br><br><br><br><br><br><br><br><br><br><br>||
|||**P1**|P2|**_P3_**|P4|**LSBs**|**LSBs**||**LSBs**||**LSBs**|….|P640|**LSBs**|**LSBs**||**LSBs**||**LSBs**|||
|||**P1**|P2|**_P3_**|P4|**LSBs**|**LSBs**||**LSBs**||**LSBs**|….|P640|**LSBs**|**LSBs**||**LSBs**||**LSBs**|||
|||**P1**|P2|**_P3_**|P4|**LSBs**|**LSBs**||**LSBs**||**LSBs**|….|P640|**LSBs**|**LSBs**||**LSBs**||**LSBs**|||
|||**P1**|P2|**_P3_**|P4|**LSBs**|**LSBs**||**LSBs**||**LSBs**|….|P640|**LSBs**|**LSBs**||**LSBs**||**LSBs**|||
|||**P1**|P2|**_P3_**|P4|**LSBs**|**LSBs**||**LSBs**||**LSBs**|….|P640|**LSBs**|**LSBs**||**LSBs**||**LSBs**|||
|||**P1**|P2|**_P3_**|P4|**LSBs**|**LSBs**||**LSBs**||**LSBs**|….|P640|**LSBs**|**LSBs**||**LSBs**||**LSBs**|||
|||**P1**|P2|**_P3_**|P4|**LSBs**|**LSBs**||**LSBs**||**LSBs**|….|P640|**LSBs**|**LSBs**||**LSBs**||**LSBs**|||
|||**P1**|P2|**_P3_**|P4|**LSBs**|**LSBs**||**LSBs**||**LSBs**|….|P640|**LSBs**|**LSBs**||**LSBs**||**LSBs**|||
|||**P1**|P2|**_P3_**|P4|**LSBs**|**LSBs**||**LSBs**||**LSBs**|….|P640|**LSBs**|**LSBs**||**LSBs**||**LSBs**|||
|||**P1**|P2|**_P3_**|P4|**LSBs**|**LSBs**||**LSBs**||**LSBs**|….|P640|**LSBs**|**LSBs**||**LSBs**||**LSBs**|||
|||**P1**|P2|**_P3_**|P4|**LSBs**|**LSBs**||**LSBs**||**LSBs**|….|P640|**LSBs**|**LSBs**||**LSBs**||**LSBs**||FE|



**Figure 117 RAW14 Frame Format** 

## 1180 **11.5 User Defined Data Formats** 

1181 The User Defined Data Type values shall be used to transmit arbitrary data, such as JPEG and MPEG4 1182 data, over the CSI-2 bus. Data shall be packed so that the data length is divisible by eight bits. If data 1183 padding is required, the padding shall be added before data is presented to the CSI-2 protocol interface. 

1184 Bit order in transmission follows the general CSI-2 rule, LSB first. 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

93 

Specification for CSI-2 

Version 1.3 29-May-2014 

1185 

Packet **Line Start** Header **B1[7:0]** B2[7:0] _**B3[7:0]**_ B4[7:0] **B5[7:0]** B6[7:0] _**B7[7:0]**_ Packet **Line End B121[7:0]** B122[7:0] _**B123[7:0]**_ B124[7:0] **B125[7:0]** B126[7:0] _**B127[7:0]**_ Footer 

## **Figure 118 User Defined 8-bit Data (128 Byte Packet)** 

1186 

**==> picture [430 x 121] intentionally omitted <==**

**----- Start of picture text -----**<br>
Byte1[7:0] (A) Byte2[7:0] (B) Byte3[7:0] (C) Byte4[7:0] (D)<br>Data A0 A1 A2 A3 A4 A5 A6 A7 B0 B1 B2 B3 B4 B5 B6 B7 C0 C1 C2 C3 C4 C5 C6 C7 D0 D1 D2 D3 D4 D5 D6 D7<br>8-bits 8-bits 8-bits 8-bits<br>Byte Values Transmitted LS Bit First<br>Byte n Byte n+1 Byte n+2 Byte n+3<br>b0 b1 b2 b3 b4 b5 b6 b7 b0 b1 b2 b3 b4 b5 b6 b7 b0 b1 b2 b3 b4 b5 b6 b7 b0 b1 b2 b3 b4 b5 b6 b7<br>**----- End of picture text -----**<br>


## **Figure 119 User Defined 8-bit Data Transmission on CSI-2 Bus Bitwise Illustration** 

1187 The packet data size in bits shall be divisible by eight, i.e. a whole number of bytes shall be transmitted. 1188 For User Defined data: 

- 1189 • The frame is transmitted as a sequence of arbitrary sized packets. 1190 • The packet size may vary from packet to packet. 1191 • The packet spacing may vary between packets. 

**==> picture [472 x 191] intentionally omitted <==**

**----- Start of picture text -----**<br>
Variable Packet Spacing<br>Frame Start  Frame End<br>Packet Variable Packet Size Packet<br>SoT FS EoT LPS SoT PH Data PF EoT LPS SoT PH Data PF EoT LPS SoT FE EoT<br>VVALID<br>HVALID<br>DVALID<br>KEY :<br>SoT – Start of Transmission EoT – End of Transmission LPS – Low Power State<br>PH – Packet Header PF – Packet Footer<br>FS – Frame Start  FE – Frame End<br>1192  LE – Line End<br>**----- End of picture text -----**<br>


**Figure 120 Transmission of User Defined 8-bit Data** 

1193 Eight different User Defined data type codes are available as shown in Table 27. 

1194 

**Table 27 User Defined 8-bit Data Types** 

|**Data Type**|**Description**|
|---|---|
|0x30|User Defined 8-bit Data Type 1|
|0x31|User Defined 8-bit Data Type 2|



94 Copyright © 2005-2014 MIPI Alliance, Inc. 

All rights reserved. **Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

|**Data Type**|**Description**|
|---|---|
|0x32|User Defined 8-bit Data Type 3|
|0x33|User Defined 8-bit Data Type 4|
|0x34|User Defined 8-bit Data Type 5|
|0x35|User Defined 8-bit Data Type 6|
|0x36|User Defined 8-bit Data Type 7|
|0x37|User Defined 8-bit Data Type 8|



Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

95 

Specification for CSI-2 

Version 1.3 29-May-2014 

## 1195 

## **12 Recommended Memory Storage** 

- 1196 This section is informative. 

1197 The CSI-2 data protocol requires certain behavior from the receiver connected to the CSI transmitter. The 1198 following sections describe how different data formats should be stored inside the receiver. While 1199 informative, this section is provided to ease application software development by suggesting a common 1200 data storage format among different receivers. 

## 1201 

## **12.1 General/Arbitrary Data Reception** 

1202 In the generic case and for arbitrary data the first byte of payload data transmitted maps the LS byte of the 1203 32-bit memory word and the fourth byte of payload data transmitted maps to the MS byte of the 32-bit 1204 memory word. 

1205 Figure 121 shows the generic CSI-2 byte to 32-bit memory word mapping rule. 

## **Data on CSI-2 bus** 

|||||**Byte1[7:0]**|||||||Byte2[7:0]|||||**_Byte3[7:0]_**|||||Byte4[7:0]||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Data||**a0**|**a1**|**a2**<br>**a3**<br>**a4**<br>**a5**||**a6**|**a7**||b0|b1|b2<br>b3<br>b4<br>b5|b6|b7|**_c0_**|**_c1_**|**_c2_**<br>**_c3_**<br>**_c4_**<br>**_c5_**|**_c6_**|**_c7_**|d0|d1|d2<br>d3<br>d4<br>d5|d6|d7||
|||||**Byte5[7:0]**|||||||Byte6[7:0]|||||**_Byte7[7:0]_**|||||Byte8[7:0]||||
|||**e0**|**e1**|**e2**<br>**e3**<br>**e4**<br>**e5**||**e6**|**e7**||f0|f1|f2<br>f3<br>f4<br>f5|f6|f7|**_g0_**|**_g1_**|**_g2_**<br>**_g3_**<br>**_g4_**<br>**_g5_**|**_g6_**|**_g7_**|h0|h1|h2<br>h3<br>h4<br>h5|h6|h7||
|||||**Byte9[7:0]**|||||||Byte10[7:0]|||||**_Byte11[7:0]_**|||||Byte12[7:0]||||
|||**i0**|**i1**|**i5**<br>**i4**<br>**i3**<br>**i2**||**i6**|**i7**||j0|j1|j5<br>j4<br>j3<br>j2|j6|j7|**_k0_**|**_k1_**|**_k5_**<br>**_k4_**<br>**_k3_**<br>**_k2_**|**_k6_**|**_k7_**|l0|l1|l5<br>l4<br>l3<br>l2|l6|l7||
|Buffer||**Data in receiver's**|||**buffer**||||||||||||||||||||
|Addr|**MSB**|||Byte4[7:0]|||||||**_Byte3[7:0]_**|||||Byte2[7:0]|||||**Byte1[7:0]**|**LSB**|||
|00h||d7|d6|d5<br>d4<br>d3<br>d2||d1|d0||**_c7_**|**_c6_**|**_c5_**<br>**_c4_**<br>**_c3_**<br>**_c2_**|**_c1_**|**_c0_**|b7|b6|b5<br>b4<br>b3<br>b2|b1|b0|**a7**|**a6**|**a5**<br>**a4**<br>**a3**<br>**a2**|**a1**|**a0**||
|||||Byte8[7:0]|||||||**_Byte7[7:0]_**|||||Byte6[7:0]|||||**Byte5[7:0]**||||
|01h||h7|h6|h5<br>h4<br>h3<br>h2||h1|h0||**_g7_**|**_g6_**|**_g5_**<br>**_g4_**<br>**_g3_**<br>**_g2_**|**_g1_**|**_g0_**|f7|f6|f5<br>f4<br>f3<br>f2|f1|f0|**e7**|**e6**|**e5**<br>**e4**<br>**e3**<br>**e2**|**e1**|**e0**||
|||||Byte12[7:0]|||||||**_Byte11[7:0]_**|||||Byte10[7:0]|||||**Byte9[7:0]**||||
|02h||l7|l6|l5<br>l4<br>l3<br>l2||l1|l0||**_k7_**|**_k6_**|**_k5_**<br>**_k4_**<br>**_k3_**<br>**_k2_**|**_k1_**|**_k0_**|j7|j6|j5<br>j4<br>j3<br>j2|j1|j0|**i7**|**i6**|**i5**<br>**i4**<br>**i3**<br>**i2**|**i1**|**i0**||



1206 

32-bit standard memory width 

## **Figure 121 General/Arbitrary Data Reception** 

## 1207 

## **12.2 RGB888 Data Reception** 

1208 The RGB888 data format byte to 32-bit memory word mapping follows the generic CSI-2 rule. 

Copyright © 2005-2014 MIPI Alliance, Inc. 

96 

All rights reserved. **Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

|||**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**||||||||||||||||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|||||**B1[7:0]**||||||G1[7:0]|||||**_R1[7:0]_**|||||**B2[7:0]**||||
|Data||**a0**|**a1**|**a2**<br>**a3**<br>**a4**|**a5**|**a6**|**a7**|b0|b1|b2<br>b3<br>b4<br>b5|b6|b7|**_c0_**|**_c1_**|**_c2_**<br>**_c3_**<br>**_c4_**<br>**_c5_**|**_c6_**|**_c7_**|**d0**|**d1**|**d2**<br>**d3**<br>**d4**<br>**d5**|**d6**|**d7**||
|||||G2[7:0]||||||**_R2[7:0]_**|||||**B3[7:0]**|||||G3[7:0]||||
|||e0|e1|e2<br>e3<br>e4|e5|e6|e7|**_f0_**|**_f1_**|**_f2_**<br>**_f3_**<br>**_f4_**<br>**_f5_**|**_f6_**|**_f7_**|**g0**|**g1**|**g2**<br>**g3**<br>**g4**<br>**g5**|**g6**|**g7**|h0|h1|h2<br>h3<br>h4<br>h5|h6|h7||
|Buffer||**Data in receiver's**||||**buffer**||||||||||||||||||
|Addr|**MSB**|||**B2[7:0]**||||||**_R1[7:0]_**|||||G1[7:0]|||||**B1[7:0]**|**LSB**|||
|00h||**d7**|**d6**|**d5**<br>**d4**<br>**d3**|**d2**|**d1**|**d0**|**_c7_**|**_c6_**|**_c5_**<br>**_c4_**<br>**_c3_**<br>**_c2_**|**_c1_**|**_c0_**|b7|b6|b5<br>b4<br>b3<br>b2|b1|b0|**a7**|**a6**|**a5**<br>**a4**<br>**a3**<br>**a2**|**a1**|**a0**||
|||||G3[7:0]||||||**B3[7:0]**|||||**_R2[7:0]_**|||||G2[7:0]||||
|01h||h7|h6|h5<br>h4<br>h3|h2|h1|h0|**g7**|**g6**|**g5**<br>**g4**<br>**g3**<br>**g2**|**g1**|**g0**|**_f7_**|**_f6_**|**_f5_**<br>**_f4_**<br>**_f3_**<br>**_f2_**|**_f1_**|**_f0_**|e7|e6|e5<br>e4<br>e3<br>e2|e1|e0||



1209 

32-bit standard memory width 

## **Figure 122 RGB888 Data Format Reception** 

## 1210 **12.3 RGB666 Data Reception** 

|||**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**||||||||||||||||||||||||||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||||**B1[5:0]**||||G1[5:0]|||||||**_R1[5:0]_**||||||**B2[5:0]**||||||G2[5:0]|||||**_R2_**|||
|Data||**a0**|**a1**<br>**a2**|**a3**<br>**a4**|**a5**|b0|b1||b2|b3|b4|b5|**_c0_**|**_c1_**|**_c2_**|**_c3_**|**_c4_**|**_c5_**|**d0**|**d1**|**d2**|**d3**|**d4**|**d5**|e0|e1|e2|e3|e4|e5|**_f0_**|**_f1_**||
||||**_R2_**||**B3[5:0]**|||||||G3[5:0]||||||**_R3[5:0]_**||||||**B4[5:0]**||||||G4||||
|||**_f2_**|**_f3_**<br>**_f4_**|**_f5_**<br>**g0**|**g1**|**g2**|**g3**||**g4**|**g5**|h0|h1|h2|h3|h4|h5|**_i0_**|**_i1_**|**_i2_**|**_i3_**|**_i4_**|**_i5_**|**j0**|**j1**|**j2**|**j3**|**j4**|**j5**|k0|k1|k2|k3||
|||G4||**_R4[5:0]_**||||||**B5[5:0]**||||||G5[5:0]||||||**_R5[5:0]_**||||||**B6[5:0]**||||||
|||k4|k5<br>**_l0_**|**_l1_**<br>**_l2_**|**_l3_**|**_l4_**|**_l5_**||**m0**<br>**m1**<br>**m2**<br>**m3**<br>**m4**<br>**m5**||||||n0|n1|n2|n3|n4|n5|**_o0_**|**_o1_**|**_o2_**|**_o3_**|**_o4_**|**_o5_**|**p0**|**p1**|**p2**|**p3**|**p4**|**p5**||
|Buffer||**Data in receiver's**||||**buffer**||||||||||||||||||||||||||||
|Addr|**MSB**<br>**_R2_**|||G2[5:0]||||||**B2[5:0]**||||||**_R1[5:0]_**||||||G1[5:0]||||||**LSB**<br>**B1[5:0]**||||||
|00h||**_f1_**|**_f0_**<br>e5|e3<br>e4|e2|e1|e0||**d5**|**d4**|**d3**|**d2**|**d1**|**d0**|**_c5_**|**_c4_**|**_c3_**|**_c2_**|**_c1_**|**_c0_**|b5|b4|b3|b2|b1|b0|**a5**|**a4**|**a3**|**a2**|**a1**|**a0**||
||||G4||**B4[5:0]**|||||||**_R3[5:0]_**||||||G3[5:0]||||||**B3[5:0]**||||||**_R2_**||||
|01h||k3|k1<br>k2|k0<br>**j5**|**j4**|**j3**|**j2**||**j1**|**j0**|**_i5_**|**_i4_**|**_i3_**|**_i2_**|**_i1_**|**_i0_**|h5|h4|h3|h2|h1|h0|**g5**|**g4**|**g3**|**g2**|**g1**|**g0**|**_f5_**|**_f4_**|**_f3_**|**_f2_**||
||||**B6[5:0]**||||**_R5[5:0]_**|||||||G5[5:0]||||||**B5[5:0]**||||||**_R4[5:0]_**|||||G4|||
|02h||**p5**|**p3**<br>**p4**|**p1**<br>**p2**|**p0**|**_o5_**|**_o4_**||**_o3_**|**_o2_**|**_o1_**|**_o0_**|n5|n4|n3|n2|n1|n0|**m5**|**m4**|**m3**|**m2**|**m1**|**m0**|**_l5_**|**_l4_**|**_l3_**|**_l2_**|**_l1_**|**_l0_**|k5|k4||



1211 

32-bit standard memory width 

## **Figure 123 RGB666 Data Format Reception** 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

97 

Specification for CSI-2 

Version 1.3 29-May-2014 

## 1212 **12.4 RGB565 Data Reception** 

## **Data on CSI-2 bus** 

|||||**B1[4:0]**|||||G1[5:0]|||**_R1[4:0]_**|**_R1[4:0]_**|||**B2[4:0]**|||G2[5:0]|||**_R2[4:0]_**||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Data||**a0**|**a1**<br>**a2**<br>**a3**|||**a4**|b0|b1|b2<br>b3<br>b4|b5|**_c0_**|**_c1_**<br>**_c2_**<br>**_c3_**||**_c4_**|**d0**|**d1**<br>**d2**<br>**d3**|**d4**|e0|e1<br>e2<br>e3<br>e4|e5|**_f0_**|**_f1_**<br>**_f2_**<br>**_f3_**||**_f4_**||
|||||**B3[4:0]**|||||G3[5:0]|||**_R3[4:0]_**||||**B4[4:0]**|||G4[5:0]|||**_R4[4:0]_**||||
|||**g0**|**g1**<br>**g2**<br>**g3**|||**g4**|h0|h1|h2<br>h3<br>h4|h5|**_i0_**|**_i1_**<br>**_i2_**<br>**_i3_**||**_i4_**|**j0**|**j1**<br>**j2**<br>**j3**|**j4**|k0|k1<br>k2<br>k3<br>k4|k5|**_l0_**|**_l1_**<br>**_l2_**<br>**_l3_**||**_l4_**||
|Buffer||**Data in receiver's**||||||**buffer**||||||||||||||||||
|Addr|**MSB**|||**_R2[4:0]_**||||G2[5:0]||||**B2[4:0]**||||**_R1[4:0]_**|||G1[5:0]|||**B1[4:0]**|**LSB**|||
|00h||**_f4_**||**_f3_**<br>**_f2_**<br>**_f1_**||**_f0_**|e5|e4|e3<br>e2<br>e1|e0|**d4**|**d3**<br>**d2**<br>**d1**||**d0**|**_c4_**|**_c3_**<br>**_c2_**<br>**_c1_**|**_c0_**|b5|b4<br>b3<br>b2<br>b1|b0|**a4**|**a3**<br>**a2**<br>**a1**||**a0**||
|||||**_R4[4:0]_**||||G4[5:0]||||**B4[4:0]**||||**_R3[4:0]_**|||G3[5:0]|||**B3[4:0]**||||
|01h||**_l4_**||**_l3_**<br>**_l2_**<br>**_l1_**||**_l0_**|k5|k4|k3<br>k2<br>k1|k0|**j4**|**j3**<br>**j2**<br>**j1**||**j0**|**_i4_**|**_i3_**<br>**_i2_**<br>**_i1_**|**_i0_**|h5|h4<br>h3<br>h2<br>h1|h0|**g4**|**g3**<br>**g2**<br>**g1**||**g0**||



1213 

32-bit standard memory width 

## **Figure 124 RGB565 Data Format Reception** 

## 1214 **12.5 RGB555 Data Reception** 

|||**Data on CSI-2**|**Data on CSI-2**|**Data on CSI-2**|**Data on CSI-2**|**bus**|**bus**|**bus**|||||||||||||||||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||||**B1[4:0]**||||||G1[4:0]||||**_R1[4:0]_**||||**B2[4:0]**|||G2[4:0]|||**_R2[4:0]_**||||
|Data||**a0**|**a1**<br>**a2**|**a3**|**a4**||0|b0|b1<br>b2|b3|b4|**_c0_**|**_c1_**<br>**_c2_**<br>**_c3_**||**_c4_**|**d0**|**d1**<br>**d2**<br>**d3**|**d4**|0|e0<br>e1<br>e2<br>e3|e4|**_f0_**|**_f1_**<br>**_f2_**<br>**_f3_**||**_f4_**||
||||**B3[4:0]**||||||G3[4:0]||||**_R3[4:0]_**||||**B4[4:0]**|||G4[4:0]|||**_R4[4:0]_**||||
|||**g0**|**g1**<br>**g2**|**g3**|**g4**||0|h0|h1<br>h2|h3|h4|**_i0_**|**_i1_**<br>**_i2_**<br>**_i3_**||**_i4_**|**j0**|**j1**<br>**j2**<br>**j3**|**j4**|0|k0<br>k1<br>k2<br>k3|k4|**_l0_**|**_l1_**<br>**_l2_**<br>**_l3_**||**_l4_**||
|Buffer||**Data in receiver's**||||||**buffer**|||||||||||||||||||
|Addr|**_R2[4:0]_**<br>**MSB**|||||||G2[4:0]|||||**B2[4:0]**||||**_R1[4:0]_**|||G1[4:0]|||**B1[4:0]**|**LSB**|||
|00h||**_f4_**|**_f3_**<br>**_f2_**|**_f1_**|**_f0_**||e4|e3|e2<br>e1|e0|0|**d4**|**d3**<br>**d2**<br>**d1**||**d0**|**_c4_**|**_c3_**<br>**_c2_**<br>**_c1_**|**_c0_**|b4|b3<br>b2<br>b1<br>b0|0|**a4**|**a3**<br>**a2**<br>**a1**||**a0**||
||||**_R4[4:0]_**|||||G4[4:0]|||||**B4[4:0]**||||**_R3[4:0]_**|||G3[4:0]|||**B3[4:0]**||||
|01h||**_l4_**|**_l3_**<br>**_l2_**|**_l1_**|**_l0_**||k4|k3|k2<br>k1|k0|0|**j4**|**j3**<br>**j2**<br>**j1**||**j0**|**_i4_**|**_i3_**<br>**_i2_**<br>**_i1_**|**_i0_**|h4|h3<br>h2<br>h1<br>h0|0|**g4**|**g3**<br>**g2**<br>**g1**||**g0**||



1215 

32-bit standard memory width 

## **Figure 125 RGB555 Data Format Reception** 

## **12.6 RGB444 Data Reception** 

1216 **12.6 RGB444 Data Reception** 1217 The RGB444 data format byte to 32-bit memory word mapping has a special transform as shown in Figure 1218 126. 

Copyright © 2005-2014 MIPI Alliance, Inc. 

98 

All rights reserved. **Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

## **Data on CSI-2 bus** 

||||**B1[3:0]**|**B1[3:0]**|**B1[3:0]**|**B1[3:0]**|||G1[3:0]|G1[3:0]||**_R1[3:0]_**||**B2[3:0]**|**B2[3:0]**|**B2[3:0]**|**B2[3:0]**||||G2[3:0]|G2[3:0]|||**_R2[3:0]_**||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Data||1|**a0**|**a1**|**a2**|**a3**|0|1|b0|b1<br>b2<br>b3|1|**_c0_**<br>**_c1_**<br>**_c2_**<br>**_c3_**|1|**d0**|**d1**|**d2**||**d3**|0|1|e0|e1<br>e2|e3|1|**_f0_**<br>**_f1_**<br>**_f2_**<br>**_f3_**||
||||**B3[3:0]**||||||G3[3:0]|||**_R3[3:0]_**||**B4[3:0]**|||||||G4[3:0]||||**_R4[3:0]_**||
|||1|**g0**|**g1**|**g2**|**g3**|0|1|h0|h1<br>h2<br>h3|1|**_i0_**<br>**_i1_**<br>**_i2_**<br>**_i3_**|1|**j0**|**j1**|**j2**||**j3**|0|1|k0|k1<br>k2|k3|1|**_l0_**<br>**_l1_**<br>**_l2_**<br>**_l3_**||
|Buffer||**Data in receiver's**||||||**buffer**|||||||||||||||||||
|Addr|**MSB**|||||**R2[3:0]**||||G2[3:0]||**_B2[3:0]_**||||||**_R1[3:0]_**||||G1[3:0]|||**B1[3:0]**<br>**LSB**||
|00h||X|X|X|X|**f3**|**f2**|**f1**|**f0**|e3<br>e2<br>e1|e0|**_d3_**<br>**_d2_**<br>**_d1_**<br>**_d0_**|X|X|X|X||**_c3_**|**_c2_**|**_c1_**|**_c0_**|b3<br>b2|b1|b0|**a3**<br>**a2**<br>**a1**<br>**a0**||
|||||||**R4[3:0]**||||G4[3:0]||**_B4[3:0]_**||||||**_R3[3:0]_**||||G3[3:0]|||**B3[3:0]**||
|01h||X|X|X|X|**l3**|**l2**|**l1**|**l0**|k3<br>k2<br>k1|k0|**_j3_**<br>**_j2_**<br>**_j1_**<br>**_j0_**|X|X|X|X||**_i3_**|**_i2_**|**_i1_**|**_i0_**|h3<br>h2|h1|h0|**g3**<br>**g2**<br>**g1**<br>**g0**||



## 1219 

32-bit standard memory width 

## **Figure 126 RGB444 Data Format Reception** 

## 1220 **12.7 YUV422 8-bit Data Reception** 

1221 The YUV422 8-bit data format the byte to 32-bit memory word mapping does not follow the generic CSI-2 1222 rule. 

1223 For YUV422 8-bit data format the first byte of payload data transmitted maps the MS byte of the 32-bit 1224 memory word and the fourth byte of payload data transmitted maps to the LS byte of the 32-bit memory 1225 word. 

## **Data on CSI-2 bus** 

||||||**U1**|||||||Y1|||||||**_V1_**|||||||Y2|||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Data||**a0**|**a1**|**a2**|**a3**<br>**a4**|**a5**|**a6**|**a7**|b0|b1|b2|b3<br>b4|b5|b6|b7|**_c0_**|**_c1_**|**_c2_**|**_c3_**<br>**_c4_**|**_c5_**|**_c6_**|**_c7_**|d0|d1|d2|d3<br>d4|d5|d6|d7||
||||||**U3**|||||||Y3|||||||**_V3_**|||||||Y4|||||
|||**e0**|**e1**|**e2**|**e3**<br>**e4**|**e5**|**e6**|**e7**|f0|f1|f2|f3<br>f4|f5|f6|f7|**_g0_**|**_g1_**|**_g2_**|**_g3_**<br>**_g4_**|**_g5_**|**_g6_**|**_g7_**|h0|h1|h2|h3<br>h4|h5|h6|h7||
|Buffer||**Data in receiver's**|||||**buffer**||||||||||||||||||||||||
|Addr|**MSB**||||**U1**|||||||Y1|||||||**_V1_**|||||||Y2||**LSB**|||
|00h||**a7**|**a6**|**a5**|**a4**<br>**a3**|**a2**|**a1**|**a0**|b7|b6|b5|b4<br>b3|b2|b1|b0|**_c7_**|**_c6_**|**_c5_**|**_c4_**<br>**_c3_**|**_c2_**|**_c1_**|**_c0_**|d7|d6|d5|d4<br>d3|d2|d1|d0||
||||||**U3**|||||||Y3|||||||**_V3_**|||||||Y4|||||
|01h||**e7**|**e6**|**e5**|**e4**<br>**e3**|**e2**|**e1**|**e0**|f7|f6|f5|f4<br>f3|f2|f1|f0|**_g7_**|**_g6_**|**_g5_**|**_g4_**<br>**_g3_**|**_g2_**|**_g1_**|**_g0_**|h7|h6|h5|h4<br>h3|h2|h1|h0||



1226 

32-bit standard memory width 

## **Figure 127 YUV422 8-bit Data Format Reception** 

## 1227 

## **12.8 YUV422 10-bit Data Reception** 

1228 The YUV422 10-bit data format the byte to 32-bit memory word mapping follows the generic CSI-2 rule. 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

99 

Specification for CSI-2 

Version 1.3 

29-May-2014 

## **Data on CSI-2 bus** 

|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Data<br>**a2**<br>**a3**<br>**a4**<br>**a5**<br>**a6**<br>**a7**<br>**a8**<br>**a9**<br>b2<br>b3<br>b4<br>b5<br>b6<br>b7<br>b8<br>b9<br>**_c2_**<br>**_c3_**<br>**_c4_**<br>**_c5_**<br>**_c6_**<br>**_c7_**<br>**_c8_**<br>**_c9_**<br>d2<br>d3<br>d4<br>d5<br>d6<br>d7<br>d8<br>d9<br>**a0**<br>**a1**<br>b0<br>b1<br>**_c0_**<br>**_c1_**<br>d0<br>d1<br>f8<br>f9<br>f2<br>f3<br>f4<br>f5<br>f6<br>f7<br>**_g8_**<br>**_g9_**<br>**_g2_**<br>**_g3_**<br>**_g4_**<br>**_g5_**<br>**_g6_**<br>**_g7_**<br>h8<br>h9<br>h2<br>h3<br>h4<br>h5<br>h6<br>h7<br>**U1[9:2]**<br>Y1[9:2]<br>**e8**<br>**e9**<br>**e2**<br>**e3**<br>**e4**<br>**e5**<br>**e6**<br>**e7**<br>**e0**<br>**e1**<br>f0<br>f1<br>**_g0_**<br>**_g1_**<br>h0<br>h1<br>**_V1[9:2]_**<br>Y2[9:2]<br>**U1[1:0]**Y1[1:0]**_V1[1:0]_**Y2[1:0]<br>**U3[9:2]**<br>Y3[9:2]<br>**_V3[9:2]_**<br>Y4[9:2]<br>**U3[1:0]**<br>Y3[1:0]<br>**_V3[1:0]_**<br>Y4[1:0]<br>**i2**<br>**i3**<br>**i4**<br>**i5**<br>**i6**<br>**i7**<br>**i8**<br>**i9**<br>j2<br>j3<br>j4<br>j5<br>j6<br>j7<br>j8<br>j9<br>**U5[9:2]**<br>Y5[9:2]|||||||||||||||||||||||||||||||||
||h2|h3|h4|h5|h6|h7|h8|h9|**e0**|**e1**|f0|f1|**_g0_**|**_g1_**|h0|h1|**i2**|**i3**|**i4**|**i5**|**i6**|**i7**|**i8**|**i9**|j2|j3|j4|j5|j6|j7|j8|j9|



|Buffer||**Data in receiver's**|**Data in receiver's**|**Data in receiver's**|**Data in receiver's**|**buffer**|**buffer**|**buffer**||||||||||||||||||||||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Addr|**MSB**|||Y2[9:2]|||||||**_V1[9:2]_**||||||Y1[9:2]||||||||**U1[9:2]**||||**LSB**|||
|00h||d9|d8|d7<br>d6<br>d5|d4|d3|d2||**_c9_**|**_c8_**|**_c7_**<br>**_c6_**<br>**_c5_**|**_c4_**|**_c3_**|**_c2_**|b9|b8|b7<br>b6|b5|b4||b3|b2|**a9**|**a8**|**a7**|**a6**|**a5**|**a4**|**a3**|**a2**||
|||||**_V3[9:2]_**|||||||Y3[9:2]||||||**U3[9:2]**||||||Y2[1:0]||V1[1:0]||Y1[1:0]||U1[1:0]|||
|01h||**_g9_**|**_g8_**|**_g7_**<br>**_g6_**<br>**_g5_**|**_g4_**|**_g3_**|**_g2_**||f9|f8|f7<br>f6<br>f5|f4|f3|f2|**e9**|**e8**|**e7**<br>**e6**|**e5**|**e4**||**e3**|**e2**|d1|d0|c1|c0|b1|b0|a1|a0||
|||||Y5[9:2]|||||||**U5[9:2]**||||Y4[1:0]||**_V3[1:0]_**|Y3[1:0]||**U3[1:0]**|||||Y4[9:2]|||||||
|02h||j9|j8|j5<br>j6<br>j7|j4|j3|j2||**i9**|**i8**|**i5**<br>**i6**<br>**i7**|**i4**|**i3**|**i2**|h1|h0|**_g1_**<br>**_g0_**|f1|f0||**e1**|**e0**|h9|h8|h7|h6|h5|h4|h3|h2||



1229 

32-bit standard memory width 

## **Figure 128 YUV422 10-bit Data Format Reception** 

## 1230 **12.9 YUV420 8-bit (Legacy) Data Reception** 

1231 The YUV420 8-bit (legacy) data format the byte to 32-bit memory word mapping does not follow the 1232 generic CSI-2 rule. 

1233 For YUV422 8-bit (legacy) data format the first byte of payload data transmitted maps the MS byte of the 1234 32-bit memory word and the fourth byte of payload data transmitted maps to the LS byte of the 32-bit 1235 memory word. 

Copyright © 2005-2014 MIPI Alliance, Inc. 

100 

All rights reserved. 

**Confidential** 

Version 1.3 

Specification for CSI-2 

29-May-2014 

## **Data on CSI-2 bus  (Odd Line)** 

|||||||**U1**|||||||Y1|||||||Y2|||||||**U3**||||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Data||**a0**|**a1**||**a2**|**a3**<br>**a4**|**a5**|**a6**|**a7**|b0|b1|b2|b3<br>b4|b5|b6|b7|c0|c1|c2|c3<br>c4|c5|c6|c7|**d0**|**d1**|**d2**|**d3**<br>**d4**|**d5**|**d6**||**d7**||
|||||||Y3|||||||Y4|||||||**U5**|||||||Y5||||||
|||e0|e1||e2|e3<br>e4|e5|e6|e7|f0|f1|f2|f3<br>f4|f5|f6|f7|**g0**|**g1**|**g2**|**g3**<br>**g4**|**g5**|**g6**|**g7**|h0|h1|h2|h3<br>h4|h5|h6||h7||
|Buffer<br>Addr|**Data**<br>**MSB**|||**in receiver's**<br>**U1**||||**buffer**|||||Y1|||||||Y2|||||||**U3**|||**LSB**|||
|00h||**a7**|**a6**||**a5**|**a4**<br>**a3**|**a2**|**a1**|**a0**|b7|b6|b5|b4<br>b3|b2|b1|b0|c7|c6|c5|c4<br>c3|c2|c1|c0|**d7**|**d6**|**d5**|**d4**<br>**d3**|**d2**|**d1**||**d0**||
|||||||Y3|||||||Y4|||||||U5|||||||Y5||||||
|01h||e7|e6||e5|e4<br>e3|e2|e1|e0|f7|f6|f5|f4<br>f3|f2|f1|f0|**g7**|**g6**|**g5**|**g4**<br>**g3**|**g2**|**g1**|**g0**|h7|h6|h5|h4<br>h3|h2|h1||h0||



32-bit standard memory width 

## **Data on CSI-2 bus  (Even Line)** 

|||||||**_V1_**|||||||Y1|||||||Y2|||||||**_V3_**||||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Data||**_a0_**|**_a1_**||**_a2_**|**_a3_**<br>**_a4_**|**_a5_**|**_a6_**|**_a7_**|b0|b1|b2|b3<br>b4|b5|b6|b7|c0|c1|c2|c3<br>c4|c5|c6|c7|**_d0_**|**_d1_**|**_d2_**|**_d3_**<br>**_d4_**|**_d5_**|**_d6_**||**_d7_**||
|||||||Y3|||||||Y4|||||||**_V5_**|||||||Y5||||||
|||e<br>0|e1||e2|e3<br>e4|e5|e6|e7|f0|f1|f2|f3<br>f4|f5|f6|f7|**_g0_**|**_g1_**|**_g2_**|**_g3_**<br>**_g4_**|**_g5_**|**_g6_**|**_g7_**|h0|h1|h2|h3<br>h4|h5|h6||h7||
|Buffer<br>Addr|**Data**<br>**MSB**|||**in receiver's**<br>**_V1_**||||**buffer**|||||Y1|||||||Y2|||||||**_V3_**|||**LSB**|||
|N||**_a7_**|**_a6_**||**_a5_**|**_a4_**<br>**_a3_**|**_a2_**|**_a1_**|**_a0_**|b7|b6|b5|b4<br>b3|b2|b1|b0|c7|c6|c5|c4<br>c3|c2|c1|c0|**_d7_**|**_d6_**|**_d5_**|**_d4_**<br>**_d3_**|**_d2_**|**_d1_**||**_d0_**||
|||||||Y3|||||||Y4|||||||**_V5_**|||||||Y5||||||
|N+1||e7|e6||e5|e4<br>e3|e2|e1|e0|f7|f6|f5|f4<br>f3|f2|f1|f0|**_g7_**|**_g6_**|**_g5_**|**_g4_**<br>**_g3_**|**_g2_**|**_g1_**|**_g0_**|h7|h6|h5|h4<br>h3|h2|h1||h0||



## 1236 

32-bit standard memory width 

## **Figure 129 YUV420 8-bit Legacy Data Format Reception** 

1237 **12.10 YUV420 8-bit Data Reception** 

1238 The YUV420 8-bit data format the byte to 32-bit memory word mapping follows the generic CSI-2 rule. 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

101 

Specification for CSI-2 

Version 1.3 

29-May-2014 

## **Data on CSI-2 bus (Odd Line)** 

||||||Y1||||||||Y2|||||||Y3|||||||Y4|||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Data||a0|a1|a2|a3<br>a4|a5|a6|a7||b0|b1|b2|b3<br>b4|b5|b6|b7||c0|c1|c2<br>c3<br>c4|c5|c6|c7|d0|d1|d2|d3<br>d4|d5|d6|d7||
||||||Y5||||||||Y6|||||||Y7|||||||Y8|||||
|||e0|e1|e2|e3<br>e4|e5|e6|e7||f0|f1|f2|f3<br>f4|f5|f6|f7||g0|g1|g2<br>g3<br>g4|g5|g6|g7|h0|h1|h2|h3<br>h4|h5|h6|h7||
|Buffer||**Data in receiver's**|||||**buffer**|||||||||||||||||||||||||
|Addr|**MSB**||||Y4||||||||Y3|||||||Y2|||||||Y1||**LSB**|||
|00h||d7|d6|d5|d4<br>d3|d2|d1|d0||c7|c6|c5|c4<br>c3|c2|c1|c0||b7|b6|b5<br>b4<br>b3|b2|b1|b0|a7|a6|a5|a4<br>a3|a2|a1|a0||
||||||Y8||||||||Y7|||||||Y6|||||||Y5|||||
|01h||h7|h6|h5|h4<br>h3|h2|h1|h0||g7|g6|g5|g4<br>g3|g2|g1|g0||f7|f6|f5<br>f4<br>f3|f2|f1|f0|e7|e6|e5|e4<br>e3|e2|e1|e0||
||||||||||||||32-bit standard|||||memory width||||||||||||||



|||**Data on CSI-2**|**Data on CSI-2**|**Data on CSI-2**|**bus (Even Line)**|**bus (Even Line)**|**bus (Even Line)**|**bus (Even Line)**|**bus (Even Line)**|**bus (Even Line)**|**bus (Even Line)**||||||||||||||||||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|||||**U1**||||||||Y1|||||||**_V1_**|||||||Y2|||||
|Data||**a0**|**a1**|**a2**<br>**a3**<br>**a4**||**a5**|**a6**|**a7**|b0|b1|b2|b3<br>b4|b5|b6|b7|**_c0_**|**_c1_**|**_c2_**|**_c3_**<br>**_c4_**|**_c5_**|**_c6_**|**_c7_**|d0|d1|d2|d3<br>d4|d5|d6|d7||
|||||**U3**||||||||Y3|||||||**_V3_**|||||||Y4|||||
|||**e0**|**e1**|**e2**<br>**e3**<br>**e4**||**e5**|**e6**|**e7**|f0|f1|f2|f3<br>f4|f5|f6|f7|**_g0_**|**_g1_**|**_g2_**|**_g3_**<br>**_g4_**|**_g5_**|**_g6_**|**_g7_**|h0|h1|h2|h3<br>h4|h5|h6|h7||
|Buffer||**Data in receiver's**|||||**buffer**||||||||||||||||||||||||
|Addr|**MSB**|||Y2||||||||**_V1_**|||||||Y1|||||||**U1**||**LSB**|||
|N||d7|d6|d5<br>d4<br>d3||d2|d1|d0|**_c7_**|**_c6_**|**_c5_**|**_c4_**<br>**_c3_**|**_c2_**|**_c1_**|**_c0_**|b7|b6|b5|b4<br>b3|b2|b1|b0|**a7**|**a6**|**a5**|**a4**<br>**a3**|**a2**|**a1**|**a0**||
|||||Y4||||||||**_V3_**|||||||Y3|||||||**U3**|||||
|N+1||h7|h6|h5<br>h4<br>h3||h2|h1|h0|**_g7_**|**_g6_**|**_g5_**|**_g4_**<br>**_g3_**|**_g2_**|**_g1_**|**_g0_**|f7|f6|f5|f4<br>f3|f2|f1|f0|**e7**|**e6**|**e5**|**e4**<br>**e3**|**e2**|**e1**|**e0**||



1239 

32-bit standard memory width 

## **Figure 130 YUV420 8-bit Data Format Reception** 

1240 **12.11 YUV420 10-bit Data Reception** 

1241 The YUV420 10-bit data format the byte to 32-bit memory word mapping follows the generic CSI-2 rule. 

Copyright © 2005-2014 MIPI Alliance, Inc. 

102 

All rights reserved. **Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

## **Data on CSI-2 bus (Odd Line)** 

|||||Y1[9:2]|Y1[9:2]||||||Y2[9:2]|Y2[9:2]|||||Y3[9:2]|Y3[9:2]|||||Y4[9:2]|Y4[9:2]||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Data||a2|a3|a4<br>a5<br>a6|a7|a8|a9||b2|b3|b4<br>b5<br>b6|b7|b8|b9|c2|c3|c4<br>c5<br>c6|c7|c8|c9|d2|d3|d4<br>d5<br>d6|d7|d8|d9||
|||Y1[1:0]||Y2[1:0] Y3[1:0]||Y4[1:0]|||||Y5[9:2]||||||Y6[9:2]||||||Y7[9:2]|||||
|||a0|a1|b0<br>b1<br>c0|c1|d0|d1||e2|e3|e4<br>e5<br>e6|e7|e8|e9|f2|f3|f4<br>f5<br>f6|f7|f8|f9|g2|g3|g4<br>g5<br>g6|g7|g8|g9||
|||||Y8[9:2]|||||Y5[1:0]||Y6[1:0] Y7[1:0]||Y8[1:0]||||Y9[9:2]||||||Y10[9:2]|||||
|||h2|h3|h4<br>h5<br>h6|h7|h8|h9||e0|e1|f0<br>f1<br>g0|g1|h0|h1|i2|i3|i4<br>i5<br>i6|i7|i8|i9|j2|j3|j4<br>j5<br>j6|j7|j8|j9||
|Buffer||**Data in receiver's**||||**buffer**||||||||||||||||||||||
|Addr|**MSB**|||Y4[9:2]|||||||Y3[9:2]||||||Y2[9:2]||||||Y1[9:2]||**LSB**|||
|00h||d9|d8|d7<br>d6<br>d5|d4|d3|d2||c9|c8|c7<br>c6<br>c5|c4|c3|c2|b9|b8|b7<br>b6<br>b5|b4|b3|b2|a9|a8|a7<br>a6<br>a5|a4|a3|a2||
|||||Y7[9:2]|||||||Y6[9:2]||||||Y5[9:2]||||Y4[1:0]||Y21:0]<br>Y3[1:0]||Y1[1:0]|||
|01h||g9|g8|g7<br>g6<br>g5|g4|g3|g2||f9|f8|f7<br>f6<br>f5|f4|f3|f2|e9|e8|e7<br>e6<br>e5|e4|e3|e2|d1|d0|b1<br>c1<br>c0|b0|a1|a0||
|||||Y10[9:2]|||||||Y9[9:2]||||Y8[1:0]||Y6[1:0]<br>Y7[1:0]||Y5[1:0]||||Y8[9:2]|||||
|02h||j9|j8|j5<br>j6<br>j7|j4|j3|j2||i9|i8|i5<br>i6<br>i7|i4|i3|i2|h1|h0|f1<br>g1<br>g0|f0|e1|e0|h9|h8|h7<br>h6<br>h5|h4|h3|h2||



32-bit standard memory width 

## **Data on CSI-2 bus (Even Line)** 

|||||**U1[9:2]**|**U1[9:2]**||||||Y1[9:2]|Y1[9:2]|||||**_V1[9:2]_**|**_V1[9:2]_**||||||Y2[9:2]|Y2[9:2]||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Data||**a2**|**a3**|**a4**<br>**a5**<br>**a6**|**a7**|**a8**|**a9**||b2|b3|b4<br>b5<br>b6|b7|b8|b9|**_c2_**|**_c3_**|**_c4_**<br>**_c5_**<br>**_c6_**|**_c7_**||**_c8_**|**_c9_**|d2|d3|d4<br>d5<br>d6|d7|d8|d9||
|||**U1[1:0]**||Y1[1:0]**_V1[1:0]_**||Y2[1:0]|||||**U3[9:2]**||||||Y3[9:2]|||||||**_V3[9:2]_**|||||
|||**a0**|**a1**|b0<br>b1<br>**_c0_**|**_c1_**|d0|d1||**e2**|**e3**|**e4**<br>**e5**<br>**e6**|**e7**|**e8**|**e9**|f2|f3|f4<br>f5<br>f6|f7||f8|f9|**_g2_**|**_g3_**|**_g4_**<br>**_g5_**<br>**_g6_**|**_g7_**|**_g8_**|**_g9_**||
|||||Y4[9:2]|||||**U3[1:0]**||Y3[1:0]**_V3[1:0]_**||Y4[1:0]||||**U5[9:2]**|||||||Y5[9:2]|||||
|||h2|h3|h4<br>h5<br>h6|h7|h8|h9||**e0**|**e1**|f0<br>f1<br>**_g0_**|**_g1_**|h0|h1|**i2**|**i3**|**i4**<br>**i5**<br>**i6**|**i7**||**i8**|**i9**|j2|j3|j4<br>j5<br>j6|j7|j8|j9||
|Buffer||**Data in receiver's**||||**buffer**|||||||||||||||||||||||
|Addr|**MSB**|||Y2[9:2]|||||||**_V1[9:2]_**||||||Y1[9:2]|||||||**U1[9:2]**||**LSB**|||
|N||d9|d8|d7<br>d6<br>d5|d4|d3|d2||**_c9_**|**_c8_**|**_c7_**<br>**_c6_**<br>**_c5_**|**_c4_**|**_c3_**|**_c2_**|b9|b8|b7<br>b6<br>b5|b4||b3|b2|**a9**|**a8**|**a7**<br>**a6**<br>**a5**|**a4**|**a3**|**a2**||
|||||**_V3[9:2]_**|||||||Y3[9:2]||||||**U3[9:2]**|||||Y2[1:0]||Y1[1:0]<br>**_V1[1:0]_**||**U1[1:0]**|||
|N+1||**_g9_**|**_g8_**|**_g7_**<br>**_g6_**<br>**_g5_**|**_g4_**|**_g3_**|**_g2_**||f9|f8|f7<br>f6<br>f5|f4|f3|f2|**e9**|**e8**|**e7**<br>**e6**<br>**e5**|**e4**||**e3**|**e2**|d1|d0|b1<br>c1<br>c0|b0|a1|a0||
|||||Y5[9:2]|||||||**U5[9:2]**||||Y4[1:0]||Y3[1:0]<br>**_V3[1:0]_**||**U3[1:0]**|||||Y4[9:2]|||||
|N+2||j9|j8|j5<br>j6<br>j7|j4|j3|j2||**i9**|**i8**|**i5**<br>**i6**<br>**i7**|**i4**|**i3**|**i2**|h1|h0|f1<br>**_g1_**<br>**_g0_**|f0||**e1**|**e0**|h9|h8|h7<br>h6<br>h5|h4|h3|h2||



1242 

32-bit standard memory width 

**Figure 131 YUV420 10-bit Data Format Reception** 

Copyright © 2005-2014 MIPI Alliance, Inc. 103 All rights reserved. **Confidential** 

Specification for CSI-2 

Version 1.3 

29-May-2014 

## 1243 **12.12 RAW6 Data Reception** 

## **Data on CSI-2 bus** 

||||**P1**|**P1**|||||P2|P2|||||**_P3_**|**_P3_**|||||P4|P4|||||**P5**|**P5**|||P6|P6||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Data||**a0**|**a1**<br>**a2**|**a3**|**a4**|**a5**|b0|b1|b2|b3|b4|b5|**_c0_**|**_c1_**|**_c2_**|**_c3_**|**_c4_**|**_c5_**|d0|d1|d2|d3|d4|d5|**e0**|**e1**|**e2**|**e3**|**e4**|**e5**|f0|f1||
||||P6||||**_P7_**||||||P8||||||**P9**||||||P10|||||**_P11_**||||
|||f2|f3<br>f4|f5|**_g0_**|**_g1_**|**_g2_**|**_g3_**|**_g4_**|**_g5_**|h0|h1|h2|h3|h4|h5|**i0**|**i1**|**i2**|**i3**|**i4**|**i5**|j0|j1|j2|j3|j4|**j5**|**_k0_**|**_k1_**|**_k2_**|**_k3_**||
|Buffer||**Data in receiver's**|||||**buffer**|||||||||||||||||||||||||||
|Addr|**MSB**||||**P5**||||||P4||||||**_P3_**||||||P2||||||**P1**||**LSB**|||
|00h||f1|f0<br>**e5**|**e4**|**e3**|**e2**|**e1**|**e0**|d5|d4|d3|d2|d1|d0|**_c5_**|**_c4_**|**_c3_**|**_c2_**|**_c1_**|**_c0_**|b5|b4|b3|b2|b1|b0|**a5**|**a4**|**a3**|**a2**|**a1**|**a0**||
||||**_P11_**||||P10||||||**P9**||||||P8||||||**_P7_**|||||P6||||
|01h||**_k3_**|**_k2_**<br>**_k1_**|**_k0_**|j5|j4|j3|j2|j1|j0|**i5**|**i4**|**i3**|**i2**|**i1**|**i0**|h5|h4|h3|h2|h1|h0|**_g5_**|**_g4_**|**_g3_**|**_g2_**|**_g1_**|**_g0_**|f5|f4|f3|f2||



1244 

32-bit standard memory width 

## **Figure 132 RAW6 Data Format Reception** 

## 1245 **12.13 RAW7 Data Reception** 

## **Data on CSI-2 bus** 

||||||**P1**|||||||P2||||||||**_P3_**|**_P3_**||||||||P4|||||||**P5**|**P5**|||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Data||**a0**|**a1**|**a2**|**a3**|**a4**|**a5**|**a6**|b0|b1|b2|b3|b4|b5||b6|**_c0_**|**_c1_**|**_c2_**|**_c3_**||**_c4_**|**_c5_**|**_c6_**||d0|d1|d2|d3|d4|d5||d6||**e0**|**e1**|**e2**|**e3**||
|||**P5**||||||P6||||||**_P7_**||||||||||P8|||||||**_P9_**||||||P10|||
|||**e4**|**e5**|**e6**|f0|f1|f2|f3|f4|f5|f6|**_g0_**|**_g1_**|**_g2_**||**_g3_**|**_g4_**|**_g5_**|**_g6_**|h0||h1|h2|h3||h4|h5|h6|**_i0_**|**_i1_**|**_i2_**||**_i3_**||**_i4_**|**_i5_**|**_i6_**|j0||
|Buffer||**Data in receiver's**||||||**buffer**||||||||||||||||||||||||||||||||
|Addr|**MSB**<br>**P5**||||||||P4||||||||**_P3_**|||||||||P2|||||||**P1**||||**LSB**|||
|00h||**e3**|**e2**|**e1**|**e0**|d6|d5|d4|d3|d2|d1|d0|**_c6_**|**_c5_**||**_c4_**|**_c3_**|**_c2_**|**_c1_**|**_c0_**||b6|b5|b4||b3|b2|b1|b0|**a6**|**a5**||**a4**||**a3**|**a2**|**a1**|**a0**||
||P10|||||**_P9_**|||||||P8|||||||||**_P7_**||||||||P6|||||||**P5**|||
|01h||j0|**_i6_**|**_i5_**|**_i4_**|**_i3_**|**_i2_**|**_i1_**|**i0**|h6|h5|h4|h3|h2||h1|h0|**_g6_**|**_g5_**|**_g4_**||**_g3_**|**_g2_**|**_g1_**||**_g0_**|f6|f5|f4|f3|f2||f1||f0|**e6**|**e5**|**e4**||



1246 

32-bit standard memory width 

## **Figure 133 RAW7 Data Format Reception** 

## 1247 **12.14 RAW8 Data Reception** 

1248 

The RAW8 data format the byte to 32-bit memory word mapping follows the generic CSI-2 rule. 

Copyright © 2005-2014 MIPI Alliance, Inc. 

104 

All rights reserved. **Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

**Data on CSI-2 bus P1** P2 _**P3**_ P4 Data **a0 a1 a2 a3 a4 a5 a6 a7** b0 b1 b2 b3 b4 b5 b6 b7 _**c0 c1 c2 c3 c4 c5 c6 c7**_ d0 d1 d2 d3 d4 d5 d6 d7 **P5** P6 _**P7**_ P8 **e0 e1 e2 e3 e4 e5 e6 e7** f0 f1 f2 f3 f4 f5 f6 f7 _**g0 g1 g2 g3 g4 g5 g6 g7**_ h0 h1 h2 h3 h4 h5 h6 h7 Buffer **Data in receiver's buffer** Addr **MSB** P4 _**P3**_ P2 **P1 LSB** 00h d7 d6 d5 d4 d3 d2 d1 d0 _**c7 c6 c5 c4 c3 c2 c1 c0**_ b7 b6 b5 b4 b3 b2 b1 b0 **a7 a6 a5 a4 a3 a2 a1 a0** P8 _**P7**_ P6 **P5** 01h h7 h6 h5 h4 h3 h2 h1 h0 _**g7 g6 g5 g4 g3 g2 g1 g0**_ f7 f6 f5 f4 f3 f2 f1 f0 **e7 e6 e5 e4 e3 e2 e1 e0** 

1249 

32-bit standard memory width 

## **Figure 134 RAW8 Data Format Reception** 

## 1250 **12.15 RAW10 Data Reception** 

1251 The RAW10 data format the byte to 32-bit memory word mapping follows the generic CSI-2 rule. 

## **Data on CSI-2 bus:** 

|||||**P1[9:2]**|||||P2[9:2]|P2[9:2]|||||**_P3[9:2]_**|**_P3[9:2]_**|||||P4[9:2]|P4[9:2]||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Data||**a2**|**a3**|**a4**<br>**a5**<br>**a6**<br>**a7**|**a8**|**a9**|b2|b3|b4<br>b5<br>b6|b7|b8|b9|**_c2_**|**_c3_**|**_c4_**<br>**_c5_**<br>**_c6_**|**_c7_**|**_c8_**|**_c9_**|d2|d3|d4<br>d5<br>d6|d7|d8|d9||
|||**P1[1:0]**||P2[1:0]**_P3[1:0]_**|P4[1:0]||||**P5[9:2]**||||||P6[9:2]||||||**_P7[9:2]_**|||||
|||**a0**|**a1**|b0<br>b1<br>**_c0_**<br>**_c1_**|d0|d1|**e2**|**e3**|**e4**<br>**e5**<br>**e6**|**e7**|**e8**|**e9**|f2|f3|f4<br>f5<br>f6|f7|f8|f9|**_g2_**|**_g3_**|**_g4_**<br>**_g5_**<br>**_g6_**|**_g7_**|**_g8_**|**_g9_**||
|||||P8[9:2]|||**P5[1:0]**||P6[1:0]**_P7[1:0]_**||P8[1:0]||||**P9[9:2]**||||||P10[9:2]|||||
|||h2|h3|h4<br>h5<br>h6<br>h7|h8|h9|**e0**|**e1**|f0<br>f1<br>**_g0_**|**_g1_**|h0|h1|**i2**|**i3**|**i4**<br>**i5**<br>**i6**|**i7**|**i8**|**i9**|j2|j3|j4<br>j5<br>j6|j7|j8|j9||
|Buffer<br>Addr|**Data in receiver's**<br>**MSB**<br>P4[9:2]||||**buffer:**||||**_P3[9:2]_**||||||P2[9:2]||||||**P1[9:2]**||**LSB**|||
|00h||d9|d8|d7<br>d6<br>d5<br>d4|d3|d2|**_c9_**|**_c8_**|**_c7_**<br>**_c6_**<br>**_c5_**|**_c4_**|**_c3_**|**_c2_**|b9|b8|b7<br>b6<br>b5|b4|b3|b2|**a9**|**a8**|**a7**<br>**a6**<br>**a5**|**a4**|**a3**|**a2**||
|||||**_P7[9:2]_**|||||P6[9:2]||||||**P5[9:2]**||||P4[1:0]||P2[1:0]<br>**_P3[1:0]_**||**P1[1:0]**|||
|01h||**_g9_**|**_g8_**|**_g7_**<br>**_g6_**<br>**_g5_**<br>**_g4_**|**_g3_**|**_g2_**|f9|f8|f7<br>f6<br>f5|f4|f3|f2|**e9**|**e8**|**e7**<br>**e6**<br>**e5**|**e4**|**e3**|**e2**|d1|d0|b1<br>**_c1_**<br>**_c0_**|b0|**a1**|**a0**||
|||||P10[9:2]|||||**P9[9:2]**||||P8[1:0]||P6[1:0]<br>**_P7[1:0]_**||**P5[1:0]**||||P8[9:2]|||||
|02h||j9|j8|j4<br>j5<br>j6<br>j7|j3|j2|**i9**|**i8**|**i5**<br>**i6**<br>**i7**|**i4**|**i3**|**i2**|h1|h0|f1<br>**_g1_**<br>**_g0_**|f0|**e1**|**e0**|h9|h8|h7<br>h6<br>h5|h4|h3|h2||



1252 

32-bit standard memory width 

## **Figure 135 RAW10 Data Format Reception** 

1253 

1254 

## **12.16 RAW12 Data Reception** 

The RAW12 data format the byte to 32-bit memory word mapping follows the generic CSI-2 rule. 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

105 

Specification for CSI-2 

Version 1.3 

29-May-2014 

## **Data on CSI-2 bus** 

||||**P1[11:4]**|**P1[11:4]**||||||||P2[11:4]|P2[11:4]|P2[11:4]|||||**P1[3:0]**|**P1[3:0]**|**P1[3:0]**|**P1[3:0]**|**P1[3:0]**|P2[3:0]|P2[3:0]|P2[3:0]|P2[3:0]|||||**_P3[11:4]_**|**_P3[11:4]_**|**_P3[11:4]_**||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Data|**a4**|**a5**|**a6**<br>**a7**<br>**a8**|**a9**||**a10**<br>**a11**||||b4|b5|b6<br>b7|b8|b9|b10<br>b11||||**a0**||**a1**||**a2**<br>**a3**|b0|b1|b2|b3|||**_c4_**|**_c5_**|**_c6_**<br>**_c7_**|**_c8_**|**_c9_**|**_c10_**<br>**_c11_**|||
||||P4[11:4]|||||||**_P3[3:0]_**|||P4[3:0]||||||||||**P5[11:4]**|||||||||P6[11:4]||||||
||d4|d5|d6<br>d7<br>d8|d9||d10<br>d11||||**_c0_**|**_c1_**|**_c2_**<br>**_c3_**|d0|d1|d2|d3|||**e4**||**e5**||**e6**<br>**e7**|**e8**|**e9**|**e10**<br>**e11**||||f4|f5|f6<br>f7|f8|f9|f 10<br>f 11|||
||**P5[3:0]**<br>P6[3:0]|||||||||||**_P7[11:4]_**|||||||||||P8[11:4]|||||||**_P7[3:0]_**|||P8[3:0]|||||
||**e0**|**e1**|f0<br>**e2**<br>**e3**|f1||f2|f3|||**_g4_**|**_g5_**|**_g6_**<br>**_g7_**|**_g8_**|**_g9_**|**_g10_**<br>**_g11_**||||h4||h5||h6<br>h7|h8|j2<br>h9|h10<br>h11||||**_g0_**|**_g1_**|**_g2_**<br>**_g3_**|h0|h1|h2|h3||
|Buffer|**Data in receiver's**||||**buffer**|||||||||||||||||||||||||||||||||
|Addr|**MSB**||**_P3[11:4]_**|||||||P2[3:0]|||**P1[3:0]**||||||||||P2[11:4]|||||||||**P1[11:4]**|||**LSB**|||
|00h|**_c11_**<br>**_c10_**||**_c7_**<br>**_c9_**<br>**_c8_**|**_c6_**||**_c5_**|**_c4_**|||b3|b2|b0<br>b1|**a3**|**a2**|**a1**|**a0**||b11<br>b10|||||b9<br>b8|b7|b6|b5|b4||**a11**<br>**a10**|||**a9**<br>**a8**|**a7**|**a6**|**a5**|**a4**||
||||P6[11:4]|||||||||**P5[11:4]**|||||||P4[3:0]|||||**_P3[3:0]_**||||||||P4[11:4]||||||
|01h|f 11<br>f 10||f7<br>f9<br>f8|f6||f5|f4||**e11**<br>**e10**|||**e9**<br>**e8**|**e7**|**e6**|**e5**|**e4**|||d3||d2||d0<br>d1|**_c3_**|**_c2_**|**_c1_**|**_c0_**||d11<br>d10|||d9<br>d8|d7|d6|d5|d4||
||**_P7[3:0]_**<br>P8[3:0]|||||||||||P8[11:4]|||||||||||**_P7[11:4]_**|||||||P6[3:0]|||**P5[3:0]**|||||
|02h|h3|h2|h0<br>h1<br>**_g3_**|**_g2_**||**_g1_**|**_g0_**||h11<br>h10|||h9<br>h8|h7|h6|h5|h4||**_g11_**<br>**_g10_**|||||**_g9_**<br>**_g8_**|**_g7_**|**_g6_**|**_g5_**|**_g4_**|||f3|f2|f0<br>f1|**e3**|**e2**|**e1**|**e0**||



1255 

32-bit standard memory width 

## **Figure 136 RAW12 Data Format Reception** 

## 1256 **12.17 RAW14 Data Reception** 

||**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|||||||||||||||||||||||||||||||||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||||**P1[13:6]**|||||||P2[13:6]||||||||||**_P3[13:6]_**||||||||||P4[13:6]||||||||||
|Data|**a6**|**a7**|**a8**<br>**a9**<br>**a10**<br>**a11**||**a12**<br>**a13**|||b6|b7|b8|b9||b10<br>b11|||b12<br>b13||**_c6_**|**_c7_**|**_c8_**||**_c9_**||**_c10_**<br>**_c11_**||**_c12_**<br>**_c13_**||d6|d7|d8|d9||d10<br>d11||||d12<br>d13|||
|||**P1[5:0]**||||P2[5:0]|||||||||**_P3[5:0]_**|||||||P4[5:0]||||||||**P5[13:6]**||||||||||
||**a0**|**a1**|**a2**<br>**a3**<br>**a4**<br>**a5**||b0|b1||b2|b3|b4|b5||**_c0_**||**_c1_**|**_c2_**|**_c3_**|**_c4_**|**_c5_**|d0||d1||d2|d3|d4|d5|**e6**|**e7**|**e8**|**e9**||**e10**<br>**e11**||||**e12**<br>**e13**|||
||||P6[13:6]|||||||**_P7[13:6]_**||||||||||P8[13:6]|||||||||**P5[5:0]**|||||||P6[5:0]||||
||f6|f7|f11<br>f10<br>f9<br>f8||f12|f13||**_g6_**|**_g7_**|**_g8_**|**_g9_**||**_g10_**||**_g11_**|**_g12_**|**_g13_**|h6|h7|h8||h9||h10|h11|h12|h13|**e0**|**e1**|**e2**|**e3**||**e4**|||**e5**|f0|f1||
||**_P7[5:0]_**<br>P6[5:0]||||||||||P8[5:0]|||||||||||||||||||||||||||||
||f2|f3|f5<br>f4<br>**_g1_**<br>**_g0_**||**_g2_**|**_g3_**||**_g4_**|**_g5_**|h0|h1||h2||h3|h4|h5|||||||||||||||||||||||
|Buffer|<br>**Data in receiver's**|||**buffer**||||||||||||||||||||||||||||||||||||
|Addr|**MSB**||P4[13:6]|||||||**_P3[13:6]_**||||||||||P2[13:6]||||||||||**P1[13:6]**|||||||**LSB**|||
|00h|d13|d12|d8<br>d9<br>d10<br>d11||d7|d6||**_c13_**|**_c12_**|**_c11_**|**_c10_**||**_c9_**||**_c8_**|**_c7_**|**_c6_**|b13|b12|b11||b10||b9|b8|b7|b6|**a13**|**a12**|**a11**|**a10**||**a9**|||**a8**|**a7**|**a6**||
||||**P5[13:6]**||||||P4[5:0]||||||||**_P3[5:0]_**||||||||P2[5:0]||||||**P1[5:0]**|||||||||
|01h|**e13**|**e12**|**e8**<br>**e9**<br>**e10**<br>**e11**||**e7**|**e6**||d5|d4|d3|d2||d1||d0|**_c5_**|**_c4_**|**_c3_**|**_c2_**|**_c1_**||**_c0_**||b5|b4|b3|b2|b1|b0|**a5**|**a4**||**a3**|||**a2**|**a1**|**a0**||
||**P5[5:0]**<br>P6[5:0]|||||||||P8[13:6]||||||||||**_P7[13:6]_**||||||||||P6[13:6]||||||||||
|02h|f1|f0|**e5**<br>**e4**<br>**e2**<br>**e3**||**e1**|**e0**||h13<br>h12||h11<br>h10|||h9||h8|h7|h6|**_g13_**<br>**_g12_**||**_g11_**<br>**_g10_**||||**_g9_**|**_g8_**|**_g7_**|**_g6_**|f13|f12|f11|f10||f9|||f8|f7|f6||
||||||||||||||||||||P8[5:0]||||||||**_P7[5:0]_**||||||P6[5:0]|||||||
|03h||||||||||||||||||h5|h4|h3||h2||h1|h0|**_g5_**|**_g4_**|**_g3_**|**_g2_**|**_g1_**|**_g0_**||f5|||f4|f3|f2||



1257 

32-bit standardmemory width 

**Figure 137 RAW 14 Data Format Reception** 

Copyright © 2005-2014 MIPI Alliance, Inc. 

106 

All rights reserved. **Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

## **Annex A JPEG8 Data Format (informative)** 

## **A.1 Introduction** 

1258 This Annex contains an informative example of the transmission of compressed image data format using 1259 the arbitrary Data Type values. 

- 1260 JPEG8 has two non-standard extensions: 

- 1261 

- 1262 

- Status information (mandatory) 

- Embedded Image information e.g. a thumbnail image (optional) 

1263 Any non-standard or additional data inside the baseline JPEG data structure has to be removed from JPEG8 1264 data before it is compliant with e.g. standard JPEG image viewers in e.g. a personal computer. 

- 1265 

The JPEG8 data flow is illustrated in the Figure 138 and Figure 139. 

## 1266 

**==> picture [359 x 178] intentionally omitted <==**

**----- Start of picture text -----**<br>
JPEG encoding<br>Camera image  according to  SOSI, EOSI, SOEI and<br>data processing  baseline JPEG  EOEI marker application CSI<br>(color separation,  DCT with JPEG8  and additional data  transmitter<br>AWB, etc.) additional  embedding<br>definitions<br>Thumbnail image<br>scaling and sRGB<br>conversion<br>Image status<br>information<br>**----- End of picture text -----**<br>


**Figure 138 JPEG8 Data Flow in the Encoder** 

## 1267 

**==> picture [275 x 179] intentionally omitted <==**

**----- Start of picture text -----**<br>
Additional data<br>Addition of EXIF<br>CSI  extraction based on<br>information,<br>receiver SOSI, EOSI, SOEI<br>Storing into a file<br>and EOEI markers<br>Thumbnail image<br>Image status<br>information<br>**----- End of picture text -----**<br>


**Figure 139 JPEG8 Data Flow in the Decoder** 

## **A.2 JPEG Data Definition** 

1268 The JPEG data generated in camera module is baseline JPEG DCT format defined in ISO/IEC 10918-1, 1269 with following additional definitions or modifications: 

Copyright © 2005-2014 MIPI Alliance, Inc. 107 All rights reserved. **Confidential** 

Specification for CSI-2 

Version 1.3 29-May-2014 

- 1270 • sRGB color space shall be used. The JPEG is generated from YCbCr format after sRGB to YCbCr 1271 conversion. 

- 1272 • The JPEG metadata has to be EXIF compatible, i.e. metadata within application segments has to 1273 be placed in beginning of file, in the order illustrated in Figure 140. 

- 1274 • A status line is added in the end of JPEG data as defined in Section A.3. 

- 1275 • If needed, an embedded image is interlaced in order which is free of choice as defined in Section 1276 A.4. 

- 1277 • Prior to storing into a file, the CSI-2 JPEG data is processed by the data separation process 1278 described in Section A.1. 

1279 

Start of Image (SOI) JFIF / EXIF Data Quantization Table (DQT) Huffman Table (DHT) Frame Header (SOF) Scan Header Compressed Data End Of Image (EOI) 

## **Figure 140 EXIF Compatible Baseline JPEG DCT Format** 

## **A.3 Image Status Information** 

1280 Information of at least the following items has to be stored in the end of the JPEG sequence as illustrated in 1281 Figure 141: 

- 1282 • Image exposure time 

- 1283 • Analog & digital gains used 

- 1284 • White balancing gains for each color component 

- 1285 • Camera version number 

- 1286 • Camera register settings 

- 1287 • Image resolution and possible thumbnail resolution 

- 1288 The camera register settings may include a subset of camera’s registers. The essential information needed 1289 for JPEG8 image is the information needed for converting the image back to linear space. This is necessary 1290 e.g. for printing service. An example of register settings is following: 

- 1291 • Sample frequency 

- 1292 • Exposure 

- 1293 • Analog and digital gain 

- 1294 • Gamma 

Copyright © 2005-2014 MIPI Alliance, Inc. 

108 

All rights reserved. 

**Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

- 1295 • Color gamut conversion matrix 

- 1296 • Contrast 

- 1297 • Brightness 

- 1298 • Pre-gain 

- 1299 The status information content has to be defined in the product specification of each camera module 1300 containing the JPEG8 feature. The format and content is manufacturer specific. 

- 1301 The image status data should be arranged so that each byte is split into two 4-bit nibbles and “1010” 1302 padding sequence is added to MSB, as presented in the Table 28. This ensures that no JPEG escape 1303 sequences (0xFF 0x00) are present in the status data. 

1304 The SOSI and EOSI markers are defined in Section A.5. 

1305 

## 1306 

**Table 28 Status Data Padding** 

|**Data Word**|**After Padding**|
|---|---|
|D7D6D5D4 D3D2D1D0|1010D7D6D5D4 1010D3D2D1D0|
|Start of Image (SOI)<br>JFIF / EXIF Data<br>Quantization Table (DQT)<br>Huffman Table (DHT)<br>Frame Header (SOF)<br>Scan Header<br>Compressed Data<br>End Of Image (EOI)<br>Start of Status Information (SOSI)<br>Image Status Information<br>End of Status Information (EOSI)||



## **Figure 141 Status Information Field in the End of Baseline JPEG Frame** 

## **A.4 Embedded Images** 

1307 An image may be embedded inside the JPEG data, if needed. The embedded image feature is not 1308 compulsory for each camera module containing the JPEG8 feature. An example of embedded data is a 241309 bit RGB thumbnail image. 

1310 The philosophy of embedded / interleaved thumbnail additions is to minimize the needed frame memory. 1311 The EI (Embedded Image) data can be included in any part of the compressed image data segment and in as 1312 many pieces as needed. See Figure 142. 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. 

109 

**Confidential** 

Specification for CSI-2 

Version 1.3 

29-May-2014 

- 1313 Embedded Image data is separated from compressed data by SOEI (Start Of Embedded Image) and EOEI 1314 (End Of Embedded Image) non-standard markers, which are defined in Section A.5. The amount of fields 1315 separated by SOEI and EOEI is not limited. 

- 1316 The pixel to byte packing for image data within an EI data field should be as specified for the equivalent 1317 CSI-2 data format. However there is an additional restriction; the embedded image data must not generate 1318 any false JPEG marker sequences (0xFFXX). 

- 1319 The suggested method of preventing false JPEG marker codes from occurring within the embedded image 1320 data it to limit the data range for the pixel values. For example 

- 1321 • For RGB888 data the suggested way to solve the false synchronization code issue is to constrain 1322 the numerical range of R, G and B values from 1 to 254. 

- 1323 • For RGB565 data the suggested way to solve the false synchronization code issue is to constrain 1324 the numerical range of G component from 1-62 and R component from 1-30. 

- 1325 Each EI data field is separated by the SOEI / EOEI markers, and has to contain an equal amount bytes and 1326 a complete number of pixels. An EI data field may contain multiple lines or a full frame of image data. 

- 1327 The embedded image data is decoded and removed apart from the JPEG compressed data prior to writing 1328 the JPEG into a file. In the process, EI data fields are appended one after each other, in order of occurrence 1329 in the received JPEG data. 

## 1330 

**==> picture [309 x 235] intentionally omitted <==**

**----- Start of picture text -----**<br>
Start of Image (SOI)<br>JFIF / EXIF Data<br>Quantization Table (DQT)<br>Compressed Data<br>Huffman Table (DHT)<br>Frame Header (SOF)<br>SOEI<br>Scan Header<br>Embedded Image data<br>EOEI<br>Compressed Data Compressed Data<br>SOEI<br>Embedded Image data<br>End Of Image (EOI)<br>EOEI<br>Start of Status Information (SOSI)<br>Compressed Data<br>Image Status Information<br>End of Status Information (EOSI)<br>**----- End of picture text -----**<br>


## **Figure 142 Example of TN Image Embedding Inside the Compressed JPEG Data Block** 

## **A.5 JPEG8 Non-standard Markers** 

- 1331 JPEG8 uses the reserved JPEG data markers for special purposes, marking the additional segments inside 1332 the data file. These segments are not part of the JPEG, JFIF [0], EXIF [0] or any other specifications; 1333 instead their use is specified in this document in Section A.3 and Section A.4. 

- 1334 The use of the non-standard markers is always internal to a product containing the JPEG8 camera module, 1335 and these markers are always removed from the JPEG data before storing it into a file. 

Copyright © 2005-2014 MIPI Alliance, Inc. 

110 

All rights reserved. **Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

1336 

**Table 29 JPEG8 Additional Marker Codes Listing** 

|**Non-standard Marker Symbol**|**Marker Data Code**|
|---|---|
|SOSI|0xFF 0xBC|
|EOSI|0xFF 0xBD|
|SOEI|0xFF 0xBE|
|EOEI|0xFF 0xBF|



## **A.6 JPEG8 Data Reception** 

1337 The compressed data format the byte to 32-bit memory word mapping follows the generic CSI-2 rule. 

## **Data on CSI-2 bus** 

|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|**Data on CSI-2 bus**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Data<br>00h<br>01h<br>Buffer<br>Addr<br>**Data in receiver's buffer**<br>**MSB**<br>**LSB**<br>**a0**<br>**a1**<br>**a2**<br>**a3**<br>**a4**<br>**a5**<br>**a6**<br>**a7**<br>b0<br>b1<br>b2<br>b3<br>b4<br>b5<br>b6<br>b7<br>**_c0_**<br>**_c1_**<br>**_c2_**<br>**_c3_**<br>**_c4_**<br>**_c5_**<br>**_c6_**<br>**_c7_**<br>d0<br>d1<br>d2<br>d3<br>d4<br>d5<br>d6<br>d7<br>**e0**<br>**e1**<br>**e2**<br>**e3**<br>**e4**<br>**e5**<br>**e6**<br>**e7**<br>f0<br>f1<br>f2<br>f3<br>f4<br>f5<br>f6<br>f7<br>**_g0_**<br>**_g1_**<br>**_g2_**<br>**_g3_**<br>**_g4_**<br>**_g5_**<br>**_g6_**<br>**_g7_**<br>h0<br>h1<br>h2<br>h3<br>h4<br>h5<br>h6<br>h7<br>d7<br>d6<br>d5<br>d4<br>d3<br>d2<br>d1<br>d0<br>b7<br>b6<br>b5<br>b4<br>b3<br>b2<br>b1<br>b0<br>**_c7_**<br>**_c6_**<br>**_c5_**<br>**_c4_**<br>**_c3_**<br>**_c2_**<br>**_c1_**<br>**_c0_**<br>h7<br>h6<br>h5<br>h4<br>h3<br>h2<br>h1<br>h0<br>f7<br>f6<br>f5<br>f4<br>f3<br>f2<br>f1<br>f0<br>**_g7_**<br>**_g6_**<br>**_g5_**<br>**_g4_**<br>**_g3_**<br>**_g2_**<br>**_g1_**<br>**_g0_**<br>**e7**<br>**e6**<br>**e5**<br>**e4**<br>**e3**<br>**e2**<br>**e1**<br>**e0**<br>**B1**<br>B2<br>**_B3_**<br>B4<br>**B5**<br>B6<br>**_B7_**<br>B8<br>B4<br>B8<br>B2<br>**_B7_**<br>**_B3_**<br>B6<br>**B1**<br>**B5**<br>**a7**<br>**a6**<br>**a5**<br>**a4**<br>**a3**<br>**a2**<br>**a1**<br>**a0**|||||||||||||||||||||||||||||||||
||h7|h6|h5|h4|h3|h2|h1|h0|**_g7_**|**_g6_**|**_g5_**|**_g4_**|**_g3_**|**_g2_**|**_g1_**|**_g0_**|f7|f6|f5|f4|f3|f2|f1|f0|**e7**|**e6**|**e5**|**e4**|**e3**|**e2**|**e1**|**e0**|



1338 

32-bit standard memory width 

**Figure 143 JPEG8 Data Format Reception** 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

111 

Specification for CSI-2 

Version 1.3 29-May-2014 

## **Annex B CSI-2 Implementation Example (informative)** 

## **B.1 Overview** 

1339 The CSI-2 implementation example assumes that the interface comprises of D-PHY unidirectional Clock 1340 and Data, with forward escape mode and optional deskew functionality. The scope in this implementation 1341 example refers only to the unidirectional data link without any references to the CCI interface, as it can be 1342 seen in Figure 144. This implementation example varies from the informative PPI example in [MIPI01]. 

1343 

**==> picture [431 x 180] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device e.g. Camera containing the  Device e.g. an application Engine or<br>CSI transmitter and CCI slave Unidirectional High  a Base Band containing the CSI<br>Speed Data Link receiver and CCI master<br>Coverage of this<br>CSI Transmitter 2 Data Lanes  CSI Receiver<br>implementation<br>Data2+ Data2+ example<br>Data2- Data2-<br>Data1+ Data1+<br>Data1- Data1-<br>Clock+ Clock+<br>Clock- Clock-<br>400kHz Bidirectional<br>CCI Slave CCI Master<br>Control Link<br>SCL SCL<br>SDA SDA<br>**----- End of picture text -----**<br>


## **Figure 144 Implementation Example Block Diagram and Coverage** 

1344 For this implementation example a layered structure is described with the following parts: 

- 1345 • D-PHY implementation details 

- 1346 • Multi-lane merger details 

- 1347 • Protocol layer details 

1348 This implementation example refers to a RAW8 data type only; hence no packing/unpacking or byte 1349 clock/pixel clock timing will be referenced as for this type of implementation they are not needed. 

1350 No error recovery mechanism or error processing details will be presented, as the intent of the document is 1351 to present an implementation from the data flow perspective. 

## **B.2 CSI-2 Transmitter Detailed Block Diagram** 

1352 Using the layered structure described in the overview the CSI-2 transmitter could have the block diagram in 1353 Figure 145. 

Copyright © 2005-2014 MIPI Alliance, Inc. 

112 

All rights reserved. 

**Confidential** 

Version 1.3 

Specification for CSI-2 

29-May-2014 

1354 

**==> picture [430 x 266] intentionally omitted <==**

**----- Start of picture text -----**<br>
TxDDRClkHS-Q<br>TxDDRClkHS-I TxDDRClkHS-Q LP-TX Cp<br>management unitClock  TxByteClkHSTxByteClk TxRequestHSTxReadyHS HS-TXCIL-MCNN Cn<br>TxClkEsc D-PHY<br>ShutdownClk<br>PHY Handshake  TxUlpmClk<br>elasticity FIFO Clock Lane<br>TxByteClk<br>FrameValid Protocol level<br>LineValid control logic TxDDRClkHS-I LP-TXHS-TX D2p<br>TxByteClkHS CIL-MFEN D2n<br>Fixed ID  TxByteDataHS[7:0] TxDataHS[7:0]<br>(RAW8) ECC generator ECC[7:0] TxWriteHS TxRequestHSTxReadyHS D-PHY<br>Shutdown2<br>WC[15:0]VC[1:0] CSI2 packet header (PH) PH[7:0] TxWrite TxClkEscTxUlpm<br>TxByteData[7:0] Data Lane 2<br>TxDDRClkHS-I LP-TX D1p<br>RAW8_Data[7:0] Payload[7:0] TxByteClkHS HS-TXCIL-MFEN D1n<br>TxByteDataHS[7:0] TxDataHS[7:0]<br>TxWriteHS D-PHY<br>TxReadyHS<br>16bit MISR (LFSR)<br>Packet header insertion  Payload  CRC[7:0] distributor Lane  Shutdown1TxClkEscTxUlpm<br>elasticity FIFO CRC control logic<br>Data Lane 1<br>CSI-2 Protocol Level Lane Distributor Level D-PHY Level<br>If two Data Lanes<br>TxByteClkHs=TxByteClk/2<br>**----- End of picture text -----**<br>


**Figure 145 CSI-2 Transmitter Block Diagram** 

## **B.3 CSI-2 Receiver Detailed Block Diagram** 

1355 Using the layered structure described in the overview, the CSI-2 receiver could have the block diagram in 1356 Figure 146. 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

113 

Specification for CSI-2 

Version 1.3 29-May-2014 

**==> picture [431 x 317] intentionally omitted <==**

**----- Start of picture text -----**<br>
Cp LP-RX RxDDRClkHS<br>HS-RX<br>Cn CIL-SCNN<br>RxClkActiveHS<br>D-PHY<br>StopstateClk<br>ShutdownClk<br>RxUlpmClk<br>PHY delay FIFO<br>Clock Lane<br>LP-RX RxDDRClkHS<br>D2p HS-RXCIL-SFEN RxByteClkHS<br>D2n RxDataHS[7:0] RxByteDataHS[7:0]<br>RxSyncHS<br>RxValidHS<br>RxActiveHS<br>Packet header ECC<br>D-PHY Stopstate2 ECC decode  elasticity FIFO<br>Shutdown2 and correct<br>ErrSotHS<br>ErrSotSyncHS<br>ErrControl RxByteDataHS[7:0] RAW8_Data[7:0]<br>RxUlpmEsc<br>ErrEsc CSI2 packet  VC[1:0]<br>Data Lane 2 header/footer  WC[15:0]<br>ECC generator processing<br>LP-RX RxDDRClkHS<br>D1pD1n HS-RXCIL-SFEN RxBRxDataHS[7:0]yteClkHS RxByteDataHS[7:0] 16-bit MISR (LFSR)<br>RxVRxSyanlidcHHSS Receiver  Payload  CRC error<br>RxActiveHS Error control  CRC detect<br>D-PHY Stopstate1 block AppErrors[n:0]<br>Shutdown1<br>ErrSotHS Stopstate<br>ErrSotSyncHS Lane merger  ErrSotSyncHS RxByteClk<br>ErrControlRxUlpmEscErrEsc error signals)PHY control/control logic (including  RxValidHS2RxValidHS1ErrSotHSErrControl Protocol level control logic FrameValidLineValid<br>Data Lane 1 RxBErrEscyteClk<br>D-PHY level Lane Merger Level CSI2 Protocol Level<br>If two Data Lanes<br>ECC WC1 WC0 ID<br>**----- End of picture text -----**<br>


## 1357 

**==> picture [59 x 6] intentionally omitted <==**

**----- Start of picture text -----**<br>
RxByteClk=RxByteClkHS*2<br>**----- End of picture text -----**<br>


## **Figure 146 CSI-2 Receiver Block Diagram** 

## **B.4 Details on the D-PHY implementation** 

## 1358 

The PHY level of implementation has the top level structure as seen in Figure 147. 

Copyright © 2005-2014 MIPI Alliance, Inc. 

114 

All rights reserved. 

**Confidential** 

Version 1.3 

Specification for CSI-2 

29-May-2014 

1359 

**==> picture [430 x 435] intentionally omitted <==**

**----- Start of picture text -----**<br>
TxDDRClkHS-Q LP-TX Cp Cp LP-RX RxDDRClkHS<br>HS-TX HS-RX<br>TxRequestHS CIL-MCNN Cn Cn CIL-SCNN<br>TxReadyHS D-PHY D-PHY RxUlpmClkRxClkActiveHS<br>Shutdown Stopstate<br>TxUlpmClk Shutdown<br>Clock Lane<br>LP-RX RxDDRClkHS<br>TxDDRClkHS-I LP-TXHS-TX D1p D1p HS-RXCIL-SFEN RxByteClkHS<br>TxByteClkHS CIL-MFEN D1n D1n RxDataHS[7:0]<br>TxDataHS[7:0] RxSyncHS<br>RxValidHS<br>TxRequestHS D-PHY RxActiveHS<br>TxReadyHS D-PHY RxUlpmEsc<br>Shutdown Stopstate<br>TxUlpm Shutdown<br>TxClkEsc<br>ErrSotHS<br>ErrSotSyncHS<br>ErrEsc<br>ErrControl<br>Data Lane 1<br>LP-RX RxDDRClkHS<br>TxDDRClkHS-ITxByteClkHS LP-TXHS-TXCIL-MFEN D2pD2n D2pD2n HS-RXCIL-SFEN RxBRxDataHS[7:0]yteClkHS<br>TxDataHS[7:0] RxSyncHS<br>RxValidHS<br>TxRequestHS D-PHY RxActiveHS<br>TxReadyHS D-PHY RxUlpmEsc<br>Shutdown Stopstate<br>TxUlpm Shutdown<br>TxClkEsc<br>ErrSotHS<br>ErrSotSyncHS<br>ErrEsc<br>ErrControl<br>Data Lane 2<br>CSI-2 Transmitter Side CSI-2 Receiver Side<br>**----- End of picture text -----**<br>


**Figure 147 D-PHY Level Block Diagram** 

1360 The components can be categorized as: 

- 1361 • CSI-2 Transmitter side: 

1362 

1363 

1364 

   - Clock lane (Transmitter) 

   - Data1 lane (Transmitter) 

   - Data2 lane (Transmitter) 

- 1365 • CSI-2 Receiver side: 

1366 

1367 

   - Clock lane (Receiver) 

   - Data1 lane (Receiver) 

- 1368 • Data2 lane (Receiver) 

## **B.4.1 CSI-2 Clock Lane Transmitter** 

1369 The suggested implementation can be seen in Figure 148. 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. 

115 

**Confidential** 

Specification for CSI-2 

Version 1.3 

29-May-2014 

1370 

**==> picture [402 x 213] intentionally omitted <==**

**----- Start of picture text -----**<br>
Low-power Function<br>Cp<br>TX Ctrl Logic<br>LP-TX<br>Cn<br>TxDDRClkHS-Q<br>HS-TX<br>TxRequestHS<br>TxReadyHS High-speed Function<br>TX State<br>Shutdown<br>Machine<br>TxUlpmClk<br>CIL-MCNN<br>Lane Control and Interface Logic<br>TX Ctrl IF Logic<br>**----- End of picture text -----**<br>


**Figure 148 CSI-2 Clock Lane Transmitter** 

- 1371 The modular D-PHY components used to build a CSI-2 clock lane transmitter are: 

- 1372 • **LP-TX** for the Low-power function 

- 1373 

- 1374 

   - **HS-TX** for the High-speed function 

   - **CIL-MCNN** for the Lane control and interface logic 

- 1375 The PPI interface signals to the CSI-2 clock lane transmitter are: 

- 1376 

   - **TxDDRClkHS-Q** (Input): High-Speed Transmit DDR Clock (Quadrature). 

- 1377 • **TxRequestHS** (Input): High-Speed Transmit Request. This active high signal causes the lane 1378 module to begin transmitting a high-speed clock. 

- 1379 • **TxReadyHS** (Output): High-Speed Transmit Ready. This active high signal indicates that the 1380 clock lane is transmitting HS clock. 

- 1381 • **Shutdown** (Input): Shutdown Lane Module. This active high signal forces the lane module into 1382 “shutdown”, disabling all activity. All line drivers, including terminators, are turned off when 1383 Shutdown is asserted. When Shutdown is high, all other PPI inputs are ignored and all PPI outputs 1384 are driven to the default inactive state. Shutdown is a level sensitive signal and does not depend on 1385 any clock. 

- 1386 • **TxUlpmClk** (Input): Transmit Ultra Low-Power mode on Clock Lane This active high signal is 1387 asserted to cause a Clock Lane module to enter the Ultra Low-Power mode. The lane module 1388 remains in this mode until TxUlpmClk is de-asserted. 

## **B.4.2 CSI-2 Clock Lane Receiver** 

1389 The suggested implementation can be seen in Figure 149. 

Copyright © 2005-2014 MIPI Alliance, Inc. 

116 

All rights reserved. 

**Confidential** 

Version 1.3 

Specification for CSI-2 

29-May-2014 

1390 

**==> picture [409 x 208] intentionally omitted <==**

**----- Start of picture text -----**<br>
High-speed Function<br>RxDDRClkHS<br>HS-RX RT<br>Cp<br>RX Ctrl Decoder<br>LP-RX<br>Cn<br>RxUlpmEsc RX State<br>RxClkActiveHS Machine Low-power Function<br>Stopstate<br>Shutdown<br>CIL-SCNN<br>Lane Control and Interface Logic<br>RX Ctrl IF Logic<br>**----- End of picture text -----**<br>


**Figure 149 CSI-2 Clock Lane Receiver** 

- 1391 The modular D-PHY components used to build a CSI-2 clock lane receiver are: 

- 1392 

- 1393 

- 1394 

   - **LP-RX** for the Low-power function 

   - **HS-RX** for the High-speed function 

   - **CIL-SCNN** for the Lane control and interface logic 

- 1395 The PPI interface signals to the CSI-2 clock lane receiver are: 

- 1396 • **RxDDRClkHS** (Output): High-Speed Receive DDR Clock used to sample the data in all data 1397 lanes. 

- 1398 • **RxClkActiveHS** (Output): High-Speed Reception Active. This active high signal indicates that the 1399 clock lane is receiving valid clock. This signal is asynchronous. 

- 1400 • **Stopstate** (Output): Lane is in Stop state. This active high signal indicates that the lane module is 1401 currently in Stop state. This signal is asynchronous. 

- 1402 • **Shutdown** (Input): Shutdown Lane Module. This active high signal forces the lane module into 1403 “shutdown”, disabling all activity. All line drivers, including terminators, are turned off when 1404 Shutdown is asserted. When Shutdown is high, all PPI outputs are driven to the default inactive 1405 state. Shutdown is a level sensitive signal and does not depend on any clock. 

- 1406 • **RxUlpmEsc** (Output): Escape Ultra Low-Power (Receive) mode. This active high signal is 1407 asserted to indicate that the lane module has entered the Ultra Low-Power mode. The lane module 1408 remains in this mode with RxUlpmEsc asserted until a Stop state is detected on the lane 1409 interconnect. 

## **B.4.3 CSI-2 Data Lane Transmitter** 

1410 The suggested implementation can be seen in Figure 150. 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

117 

Specification for CSI-2 

Version 1.3 

29-May-2014 

1411 

**==> picture [429 x 247] intentionally omitted <==**

**----- Start of picture text -----**<br>
Low-power Function<br>Esc ULPS Encoder<br>TX Ctrl Logic<br>Dp<br>LP-TX<br>TxDDRClkHS-I<br>Dn<br>TxByteClkHS<br>HS-Serialize<br>TxDataHS[7:0]<br>Sync sequence HS-TX<br>Deskew sequence<br>High-speed Function<br>TxRequestHS<br>TxReadyHS<br>Shutdown<br>TxRequestEsc TX State<br>Machine<br>TxUlpm TxUlpmEsc<br>TxClkEsc<br>CIL-MFEN<br>Lane Control and Interface Logic<br>TX Data IF Logic<br>TX Ctrl IF Logic<br>**----- End of picture text -----**<br>


**Figure 150 CSI-2 Data Lane Transmitter** 

- 1412 The modular D-PHY components used to build a CSI-2 data lane transmitter are: 

- 1413 • **LP-TX** for the Low-power function 

- 1414 • **HS-TX** for the High-speed function 

- 1415 • **CIL-MFEN** for the Lane control and interface logic. For optional deskew calibration support, the 1416 data lane transmitter transmits a deskew sequence. The deskew sequence transmission is enabled 1417 by a mechanism out of the scope of this specification. 

- 1418 The PPI interface signals to the CSI-2 data lane transmitter are: 

- 1419 

   - **TxDDRClkHS-I** (Input): High-Speed Transmit DDR Clock (in-phase). 

- 1420 • **TxByteClkHS** (Input): High-Speed Transmit Byte Clock. This is used to synchronize PPI signals 1421 in the high-speed transmit clock domain. It is recommended that both transmitting data lane 1422 modules share one TxByteClkHS signal. The frequency of TxByteClkHS must be exactly 1/8 the 1423 high-speed bit rate. 

- 1424 • **TxDataHS[7:0]** (Input): High-Speed Transmit Data. Eight bit high-speed data to be transmitted. 1425 The signal connected to TxDataHS[0] is transmitted first. Data is registered on rising edges of 1426 TxByteClkHS. 

- 1427 • **TxRequestHS** (Input): High-Speed Transmit Request. A low-to-high transition on TxRequestHS 1428 causes the lane module to initiate a Start-of-Transmission sequence. A high-to-low transition on 1429 TxRequest causes the lane module to initiate an End-of-Transmission sequence. This active high 1430 signal also indicates that the protocol is driving valid data on TxByteDataHS to be transmitted. 1431 The lane module accepts the data when both TxRequestHS and TxReadyHS are active on the same 1432 rising TxByteClkHS clock edge. The protocol always provides valid transmit data when 1433 TxRequestHS is active. Once asserted, TxRequestHS should remain high until the all the data has 1434 been accepted. 

- 1435 • **TxReadyHS** (Output): High-Speed Transmit Ready. This active high signal indicates that 1436 TxDataHS is accepted by the lane module to be serially transmitted. TxReadyHS is valid on rising 1437 edges of TxByteClkHS. Valid data has to be provided for the whole duration of active 1438 TxReadyHS. 

Copyright © 2005-2014 MIPI Alliance, Inc. 

118 

All rights reserved. 

**Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

- 1439 • **Shutdown** (Input): Shutdown Lane Module. This active high signal forces the lane module into 1440 “shutdown”, disabling all activity. All line drivers, including terminators, are turned off when 1441 Shutdown is asserted. When Shutdown is high, all other PPI inputs are ignored and all PPI outputs 1442 are driven to the default inactive state. Shutdown is a level sensitive signal and does not depend on 1443 any clock. 

- 1444 • **TxUlpmEsc** (Input): Escape mode Transmit Ultra Low Power. This active high signal is asserted 1445 with TxRequestEsc to cause the lane module to enter the Ultra Low-Power mode. The lane 1446 module remains in this mode until TxRequestEsc is de-asserted. 

- 1447 • **TxRequestEsc** (Input): This active high signal, asserted together with TxUlpmEsc is used to 1448 request entry into escape mode. Once in escape mode, the lane stays in escape mode until 1449 TxRequestEsc is de-asserted. TxRequestEsc is only asserted by the protocol while TxRequestHS 1450 is low. 

- 1451 • **TxClkEsc** (Input): Escape mode Transmit Clock. This clock is directly used to generate escape 1452 sequences. The period of this clock determines the symbol time for low power signals. It is 1453 therefore constrained by the normative part of the [MIPI01]. 

## **B.4.4 CSI-2 Data Lane Receiver** 

- 1454 The suggested implementation can be seen in Figure 151. 

1455 

**==> picture [415 x 293] intentionally omitted <==**

**----- Start of picture text -----**<br>
High-speed Function<br>RxDDRClkHS<br>RxByteClkHS<br>HS-Deskew<br>RxDataHS[7:0]<br>HS-Deserialize HS-RX RT<br>RxUlpmEsc Dp<br>RX Esc ULPS Decoder<br>LP-RX<br>RX Ctrl Decoder Dn<br>RxValidHS<br>RxActiveHS<br>Low-power Function<br>RxSyncHS<br>RX State<br>Stopstate Machine<br>Shutdown<br>ErrSotHS<br>ErrSotSyncHS<br>ErrControl<br>ErrEsc<br>CIL-SFEN<br>Lane Control and Interface Logic<br>RX Data IF Logic<br>RX Ctrl IF Logic<br>**----- End of picture text -----**<br>


**Figure 151 CSI-2 Data Lane Receiver** 

- 1456 The modular D-PHY components used to build a CSI-2 data lane receiver are: 

- 1457 • **LP-RX** for the Low-power function 

- 1458 • **HS-RX** for the High-speed function 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

119 

Specification for CSI-2 

Version 1.3 29-May-2014 

- 1459 • **CIL-SFEN** for the Lane control and interface logic. For optional deskew calibration support the 1460 data lane receiver detects a transmitted deskew calibration pattern and performs optimum deskew 1461 of the Data with respect to the RxDDRClkHS Clock. 

- 1462 The PPI interface signals to the CSI-2 data lane receiver are: 1463 • **RxDDRClkHS** (Input): High-Speed Receive DDR Clock used to sample the date in all data lanes. 1464 This signal is supplied by the CSI-2 clock lane receiver. 1465 • **RxByteClkHS** (Output): High-Speed Receive Byte Clock. This signal is used to synchronize 1466 signals in the high-speed receive clock domain. The RxByteClkHS is generated by dividing the 1467 received RxDDRClkHS. 1468 • **RXDataHS[7:0]** (Output): High-Speed Receive Data. Eight bit high-speed data received by the 1469 lane module. The signal connected to RxDataHS[0] was received first. Data is transferred on 1470 rising edges of RxByteClkHS. 1471 • **RxValidHS** (Output): High-Speed Receive Data Valid. This active high signal indicates that the 1472 lane module is driving valid data to the protocol on the RxDataHS output. There is no 1473 “RxReadyHS” signal, and the protocol is expected to capture RxDataHS on every rising edge of 1474 RxByteClkHS where RxValidHS is asserted. There is no provision for the protocol to slow down 1475 (“throttle”) the receive data. 1476 • **RxActiveHS** (Output): High-Speed Reception Active. This active high signal indicates that the 1477 lane module is actively receiving a high-speed transmission from the lane interconnect. 1478 • **RxSyncHS** (Output): Receiver Synchronization Observed. This active high signal indicates that 1479 the lane module has seen an appropriate synchronization event. In a typical high-speed 1480 transmission, RxSyncHS is high for one cycle of RxByteClkHS at the beginning of a high-speed 1481 transmission when RxActiveHS is first asserted. This signal missing is signaled using 1482 ErrSotSyncHS. 

- 1483 • **RxUlpmEsc** (Output): Escape Ultra Low Power (Receive) mode. This active high signal is 1484 asserted to indicate that the lane module has entered the Ultra Low-Power mode. The lane module 1485 remains in this mode with RxUlpmEsc asserted until a Stop state is detected on the lane 1486 interconnect. 

- 1487 • **Stopstate** (Output): Lane is in Stop state. This active high signal indicates that the lane module is 1488 currently in Stop state. This signal is asynchronous. 1489 • **Shutdown** (Input): Shutdown Lane Module. This active high signal forces the lane module into 1490 “shutdown”, disabling all activity. All line drivers, including terminators, are turned off when 1491 Shutdown is asserted. When Shutdown is high, all PPI outputs are driven to the default inactive 1492 state. Shutdown is a level sensitive signal and does not depend on any clock. 

- 1493 • **ErrSotHS** (Output): Start-of-Transmission (SoT) Error. If the high-speed SoT leader sequence is 1494 corrupted, but in such a way that proper synchronization can still be achieved, this error signal is 1495 asserted for one cycle of RxByteClkHS. This is considered to be a “soft error” in the leader 1496 sequence and confidence in the payload data is reduced. 

- 1497 • **ErrSotSyncHS** (Output): Start-of-Transmission Synchronization Error. If the high-speed SoT 1498 leader sequence is corrupted in a way that proper synchronization cannot be expected, this error is 1499 asserted for one cycle of RxByteClkHS. 

- 1500 • **ErrControl** (Output): Control Error. This signal is asserted when an incorrect line state sequence 1501 is detected. 1502 • **ErrEsc** (Output): Escape Entry Error. If an unrecognized escape entry command is received, this 1503 signal is asserted and remains high until the next change in line state. The only escape entry 1504 command supported by the receiver is the ULPS. 

Copyright © 2005-2014 MIPI Alliance, Inc. 

120 

All rights reserved. 

**Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

## **Annex C CSI-2 Recommended Receiver Error Behavior (informative)** 

## **C.1 Overview** 

1505 This section proposes one approach to handling error conditions at the receiving side of a CSI-2 Link. 1506 Although the section is informative and therefore does not affect compliance for CSI-2, the approach is 1507 offered by the MIPI Camera Working Group as a recommended approach. The CSI-2 receiver assumes the 1508 case of a CSI-2 Link comprised of unidirectional Lanes for D-PHY Clock and Data Lanes with Escape 1509 Mode functionality on the Data Lanes and a continuously running clock. This Annex does not discuss other 1510 cases, including those that differ widely in implementation, where the implementer should consider other 1511 potential error situations. 

1512 Because of the layered structure of a compliant CSI-2 receiver implementation, the error behavior is 1513 described in a similar way with several “levels” where errors could occur, each requiring some 1514 implementation at the appropriate functional layer of the design: 

- 1515 • _D-PHY Level errors_ 1516 Refers to any PHY related transmission error and is unrelated to the transmission’s contents: 

- 1517 • Start of Transmission (SoT) errors, which can be: 

- 1518 • Recoverable, if the PHY successfully identifies the Sync code but an error was detected. 

- 1519 • Unrecoverable, if the PHY does not successfully identify the sync code but does detect a HS 1520 transmission. 

- 1521 • _Control Error,_ which signals that the PHY has detected a control sequence that should not be 1522 present in this implementation of the Link. 

- 1523 • _Packet Level errors_ 

1524 This type of error refers strictly to data integrity of the received Packet Header and payload data: 

- 1525 • _Packet Header errors_ , signaled through the ECC code, that result in: 

- 1526 • A single bit-error, which can be detected and corrected by the ECC code 

- 1527 • Two bit-errors in the header, which can be detected but not corrected by the ECC code, 1528 resulting in a corrupt header 

- 1529 • _Packet payload errors_ , signaled through the CRC code 

1530 • _Protocol Decoding Level errors_ 1531 This type of error refers to errors present in the decoded Packet Header or errors resulting from an 1532 incomplete sequence of events: 

- 1533 • _Frame Sync Error_ , caused when a FS could not be successfully paired with a FE on a given 1534 virtual channel 

- 1535 • _Unrecognized ID,_ caused by the presence of an unimplemented or unrecognized ID in the 1536 header 

1537 The proposed methodology for handling errors is signal based, since it offers an easy path to a viable CSI-2 1538 implementation that handles all three error levels. Even so, error handling at the Protocol Decoding Level 1539 should implement sequential behavior using a state machine for proper operation. 

## **C.2 D-PHY Level Error** 

1540 The recommended behavior for handling this error level covers only those errors generated by the Data 1541 Lane(s), since an implementation can assume that the Clock Lane is running reliably as provided by the 1542 expected BER of the Link, as discussed in [MIPI01]. Note that this error handling behavior assumes 1543 unidirectional Data Lanes without escape mode functionality. Considering this, and using the signal names 1544 and descriptions from the [MIPI01], PPI Annex, signal errors at the PHY-Protocol Interface (PPI) level 1545 consists of the following: 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

121 

Specification for CSI-2 

Version 1.3 29-May-2014 

- 1546 • **ErrSotHS:** Start-of-Transmission (SoT) Error. If the high-speed SoT leader sequence is corrupted, 1547 but in such a way that proper synchronization can still be achieved, this error signal is asserted for 1548 one cycle of RxByteClkHS. This is considered to be a “soft error” in the leader sequence and 1549 confidence in the payload data is reduced. 

- 1550 • **ErrSotSyncHS:** Start-of-Transmission Synchronization Error. If the high-speed SoT leader 1551 sequence is corrupted in a way that proper synchronization cannot be expected, this error signal is 1552 asserted for one cycle of RxByteClkHS. 

- 1553 • **ErrControl:** Control Error. This signal is asserted when an incorrect line state sequence is 1554 detected. For example, if a Turn-around request or Escape Mode request is immediately followed 1555 by a Stop state instead of the required Bridge state, this signal is asserted and remains high until 1556 the next change in line state. 

- 1557 The recommended receiver error behavior for this level is: 

- 1558 • **ErrSotHS** should be passed to the Application Layer. Even though the error was detected and 1559 corrected and the Sync mechanism was unaffected, confidence in the data integrity is reduced and 1560 the application should be informed. This signal should be referenced to the corresponding data 1561 packet. 

- 1562 • **ErrSotSyncHS** should be passed to the Protocol Decoding Level, since this is an unrecoverable 1563 error. An unrecoverable type of error should also be signaled to the Application Layer, since the 1564 whole transmission until the first D-PHY Stop state should be ignored if this type of error occurs. 

- 1565 • **ErrControl** should be passed to the Application Layer, since this type of error doesn’t normally 1566 occur if the interface is configured to be unidirectional. Even so, the application should be aware 1567 of the error and configure the interface accordingly through other, implementation specific-means 1568 that are out of scope for this specification. 

- 1569 Also, it is recommended that the PPI StopState signal for each implemented Lane should be propagated to 1570 the Application Layer during configuration or initialization to indicate the Lane is ready. 

## **C.3 Packet Level Error** 

1571 The recommended behavior for this error level covers only errors recognized by decoding the Packet 1572 Header’s ECC byte and computing the CRC of the data payload. 

- 1573 Decoding and applying the ECC byte of the Packet Header should signal the following errors: 

- 1574 • **ErrEccDouble:** Asserted when an ECC syndrome was computed and two bit-errors are detected 1575 in the received Packet Header. 

- 1576 • **ErrEccCorrected:** Asserted when an ECC syndrome was computed and a single bit-error in the 1577 Packet Header was detected and corrected. 

- 1578 • **ErrEccNoError:** Asserted when an ECC syndrome was computed and the result is zero 1579 indicating a Packet Header that is considered to be without errors or has more than two bit-errors. 1580 CSI-2’s ECC mechanism cannot detect this type of error. 

- 1581 Also, computing the CRC code over the whole payload of the received packet could generate the following 1582 errors: 

- 1583 • **ErrCrc:** Asserted when the computed CRC code is different than the received CRC code. 

- 1584 • **ErrID:** Asserted when a Packet Header is decoded with an unrecognized or unimplemented data 1585 ID. 

- 1586 The recommended receiver error behavior for this level is: 

- 1587 • **ErrEccDouble** should be passed to the Application Layer since assertion of this signal proves that 1588 the Packet Header information is corrupt, and therefore the WC is not usable, and thus the packet 1589 end cannot be estimated. Commonly, this type of error will be accompanied with an ErrCrc. This 1590 type of error should also be passed to the Protocol Decoding Level, since the whole transmission 1591 until D-PHY Stop state should be ignored. 

Copyright © 2005-2014 MIPI Alliance, Inc. 

122 

All rights reserved. 

**Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

- 1592 • **ErrEccCorrected** should be passed to the Application Layer since the application should be 1593 informed that an error had occurred but was corrected, so the received Packet Header was 1594 unaffected, although the confidence in the data integrity is reduced. 

- 1595 • **ErrEccNoError** can be passed to the Protocol Decoding Level to signal the validity of the current 1596 Packet Header. 

- 1597 • **ErrCrc** should be passed to the Protocol Decoding Level to indicate that the packet’s payload data 1598 might be corrupt. 

- 1599 • **ErrID** should be passed to the Application Layer to indicate that the data packet is unidentified 1600 and cannot be unpacked by the receiver. This signal should be asserted after the ID has been 1601 identified and de-asserted on the first Frame End (FE) on same virtual channel. 

## **C.4 Protocol Decoding Level Error** 

- 1602 The recommended behavior for this error level covers errors caused by decoding the Packet Header 1603 information and detecting a sequence that is not allowed by the CSI-2 protocol or a sequence of detected 1604 errors by the previous layers. CSI-2 implementers will commonly choose to implement this level of error 1605 handling using a state machine that should be paired with the corresponding virtual channel. The state 1606 machine should generate at least the following error signals: 

- 1607 • **ErrFrameSync:** Asserted when a Frame End (FE) is not paired with a Frame Start (FS) on the 1608 same virtual channel. An ErrSotSyncHS should also generate this error signal. 

- 1609 • **ErrFrameData:** Asserted after a FE when the data payload received between FS and FE contains 1610 errors. 

- 1611 The recommended receiver error behavior for this level is: 

- 1612 • **ErrFrameSync** should be passed to the Application Layer with the corresponding virtual channel, 1613 since the frame could not be successfully identified. Several error cases on the same virtual 1614 channel can be identified for this type of error. 

- 1615 • If a FS is followed by a second FS on the same virtual channel, the frame corresponding to the 1616 first FS is considered in error. 

- 1617 • If a Packet Level ErrEccDouble was signaled from the Protocol Layer, the whole transmission 1618 until the first D-PHY Stop-state should be ignored since it contains no information that can be 1619 safely decoded and cannot be qualified with a data valid signal. 

- 1620 • If a FE is followed by a second FE on the same virtual channel, the frame corresponding to the 1621 second FE is considered in error. 

- 1622 • If an ErrSotSyncHS was signaled from the PHY Layer, the whole transmission until the first D- 1623 PHY Stop state should be ignored since it contains no information that can be safely decoded 1624 and cannot be qualified with a data valid signal. 

- 1625 • **ErrFrameData** : should be passed to the Application Layer to indicate that the frame contains data 1626 errors. This signal should be asserted on any ErrCrc and de-asserted on the first FE. 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

123 

Specification for CSI-2 

Version 1.3 29-May-2014 

## **Annex D CSI-2 Sleep Mode (informative)** 

## **D.1 Overview** 

1627 Since a camera in a mobile terminal spends most of its time in an inactive state, implementers need a way 1628 to put the CSI-2 Link into a low power mode that approaches, or may be as low as, the leakage level. This 1629 section proposes one approach for putting a CSI-2 Link in a “Sleep Mode” (SLM). Although the section is 1630 informative and therefore does not affect compliance for CSI-2, the approach is offered by the MIPI 1631 Camera Working Group as a recommended approach. 

- 1632 This approach relies on an aspect of a D-PHY or C-PHY transmitter’s behavior that permits regulators to be 1633 disabled safely when LP-00 (Space state) is on the Link. Accordingly, this will be the output state for a 1634 CSI-2 camera transmitter in SLM. 

- 1635 

SLM can be thought of as a three-phase process: 

- 1636 1. SLM Command Phase. The ‘ENTER SLM’ command is issued to the TX side only, or to both 1637 sides of the Link. 

- 1638 2. SLM Entry Phase. The CSI-2 Link has entered, or is entering, the SLM in a controlled or 1639 synchronized manner. This phase is also part of the power-down process. 

- 1640 3. SLM Exit Phase. The CSI-2 Link has exited the SLM and the interface/device is operational. This 1641 phase is also part of the power-up process. 

1642 In general, when in SLM, both sides of the interface will be in ULPS, as defined in [MIPI01] or [MIPI02]. 

## **D.2 SLM Command Phase** 

1643 For the first phase, initiation of SLM occurs by a mechanism outside the scope of CSI-2. Of the many 1644 mechanisms available, two examples would be: 

- 1645 1. An External SLEEP signal input to the CSI-2 transmitter and optionally also to the CSI-2 1646 Receiver. When at logic 0, the CSI-2 Transmitter and the CSI Receiver (if connected) will enter 1647 Sleep mode. When at logic 1, normal operation will take place. 

- 1648 2. A CCI control command, provided on the I2C control Link, is used to trigger ULPS. 

## **D.3 SLM Entry Phase** 

1649 

For the second phase, consider one option: 

1650 Only the TX side enters SLM and propagates the ULPS to the RX side by sending a D-PHY or C-PHY 1651 ‘ULPS’ command on each Lane. In Figure 152, only the Data Lane ‘ULPS’ command is used as an 1652 example. The D-PHY Dp, Dn, and C-PHY Data_A, Data_C are logical signal names and do not imply 1653 specific multiplexing on dual mode (combined D-PHY and C-PHY) implementations. 

Copyright © 2005-2014 MIPI Alliance, Inc. 

124 

All rights reserved. 

**Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

## **Using signal XSHUTDOWN to confirm entry and exit from “Sleep” mode** 

|External Signal<br>(XSHUTDOWN)<br>**_Or_**<br>CCI Command<br>External Signal<br>(XSHUTDOWN)<br>**_Or_**<br>CCI Command<br>External Signal<br>(XSHUTDOWN)<br>**_Or_**<br>CCI Command<br>**Dp (D-PHY) or**<br>**Data_A (C-PHY)**<br>LP-00<br>Space<br>State<br>Exit<br>Sequence<br>LP-11<br>Stop<br>State<br>Escape<br>Mode<br>Entry<br>Ultra-Low Power<br>State Command<br>00011110<br>LP-00<br>Space<br>State<br>Exit<br>Sequence<br>LP-11<br>Stop<br>State<br>“Normal”<br>Operation<br>“Sleep”<br>Mode<br>“Sleep”<br>Mode<br>“Normal”<br>Operation<br>**Using the ULPS Sequence on Data Lane to confirm entry and exit from “Sleep” mode**<br>**Dn (D-PHY) or**<br>**Data_C (C-PHY)**<br>LP-000<br>Space<br>State<br>**_Initial_**<br>**_State_**<br>Exit<br>Sequence<br>LP-111<br>Stop<br>State<br>Escape<br>Mode<br>Entry<br>Ultra-Low Power<br>State Command<br>00011110<br>LP-000<br>Space<br>State<br>Exit<br>Sequence<br>LP-111<br>Stop<br>State<br>**D-PHY**<br>**C-PHY**<br>1654||||||||||||
|---|---|---|---|---|---|---|---|---|---|---|---|
|||||||||||||
||“Sleep”<br>Mode|Ex<br>(XS<br>CC|ternal Signal<br>HUTDOWN)<br>**_Or_**<br>I Command|Exte<br>(XSH<br>CCI||rnal Signal<br>UTDOWN)<br>**_Or_**<br>Command|||Ex<br>(XS<br>CC|ternal Signal<br>HUTDOWN)<br>**_Or_**<br>I Command||
||||“Normal”<br>Operation|||||“Sleep”<br>Mode<br>**rom “Sleep” mode**||“Normal”<br>Operation||
||<br>**Using the**|**ULPS**|**Sequence on Data Lane t**|**o conf**||**irm entry and exit f**||||||
||**D-PHY) or**<br>**_A (C-PHY)**|||||||||||
||**D-PHY) or**<br>**_C (C-PHY)**|||||||||||
|||||||||||||
|||||||||||||



## **Figure 152 SLM Synchronization** 

## **D.4 SLM Exit Phase** 

1655 For the third phase, three options are presented and assume the camera peripheral is in ULPS or Sleep 1656 mode at power-up: 1657 1. Use a SLEEP signal to power-up both sides of the interface. 

- 1658 2. Detect any CCI activity on the I2C control Link, which was in the 00 state ({SCL, SDA}), after 1659 receiving the I2C instruction to enter ULPS command as per Section D.2, option 2. Any change on 1660 those lines should wake up the camera peripheral. The drawback of this method is that I2C lines 1661 are used exclusively for control of the camera. 

- 1662 3. Detect a wake-up sequence on the I2C lines. This sequence, which may vary by implementation, 1663 shall not disturb the I2C interface so that it can be used by other devices. One example sequence 1664 is: StopI2C-StartI2C-StopI2C. See Section 6 for details on CCI. 

1665 A handshake using the ‘ULPS’ mechanism as described in [MIPI01] or [MIPI02], as appropriate, should be 1666 used for powering up the interface. 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

125 

Specification for CSI-2 

Version 1.3 29-May-2014 

## **Annex E Data Compression for RAW Data Types (normative)** 

- 1667 A CSI-2 implementation using RAW data types may support compression on the interface to reduce the 1668 data bandwidth requirements between the host processor and a camera module. Data compression is not 1669 mandated by this Specification. However, if data compression is used, it shall be implemented as described 1670 in this annex. 

- 1671 Data compression schemes use an X–Y–Z naming convention where X is the number of bits per pixel in 1672 the original image, Y is the encoded (compressed) bits per pixel and Z is the decoded (uncompressed) bits 1673 per pixel. 

- 1674 The following data compression schemes are defined: 

- 1675 • 12–8–12 

- 1676 • 12–7–12 

- 1677 • 12–6–12 

- 1678 • 10–8–10 

- 1679 • 10–7–10 

- 1680 • 10–6–10 

- 1681 To identify the type of data on the CSI-2 interface, packets with compressed data shall have a User Defined 1682 Data Type value as indicated in Table 27. Note that User Defined data type codes are not reserved for 1683 compressed data types. Therefore, a CSI-2 device shall be able to communicate over the CCI the data 1684 compression scheme represented by a particular User Defined data type code for each scheme supported by 1685 the device. Note that the method to communicate the data compression scheme to Data Type code mapping 1686 is beyond the scope of this document. 

- 1687 The number of bits in a packet shall be a multiple of eight. Therefore, implementations with data 1688 compression schemes that result in each pixel having less than eight encoded bits per pixel shall transfer the 1689 encoded data in a packed pixel format. For example, the 12–7–12 data compression scheme uses a packed 1690 pixel format as described in Section 11.4.2 except the Data Type value in the Packet Header is a User 1691 Defined data type code. 

- 1692 The data compression schemes in this annex are lossy and designed to encode each line independent of the 1693 other lines in the image. 

- 1694 The following definitions are used in the description of the data compression schemes: 

- 1695 • **Xorig** is the original pixel value 

- 1696 • **Xpred** is the predicted pixel value 

- 1697 • **Xdiff** is the difference value ( **Xorig** - **Xpred** ) 

- 1698 • **Xenco** is the encoded value 

- 1699 • **Xdeco** is the decoded pixel value 

- 1700 The data compression system consists of encoder, decoder and predictor blocks as shown in Figure 153. 

Copyright © 2005-2014 MIPI Alliance, Inc. 

126 

All rights reserved. 

**Confidential** 

Version 1.3 

Specification for CSI-2 

29-May-2014 

1701 

**==> picture [430 x 136] intentionally omitted <==**

**----- Start of picture text -----**<br>
Transmitter Receiver<br>Codec<br>Selector and<br>Encoded  Encoded<br>Encoder<br>Symbols Symbols Decoded<br>+ DPCM1 Symbols<br>Unencoded  Σ DPCMN... Decoder<br>- PCM<br>Symbols M-pixel<br>Memory<br>M-pixel<br>Predictor Decoder<br>Memory Predictor<br>**----- End of picture text -----**<br>


**Figure 153 Data Compression System Block Diagram** 

- 1702 The encoder uses a simple algorithm to encode the pixel values. A fixed number of pixel values at the 1703 beginning of each line are encoded without using prediction. These first few values are used to initialize the 1704 predictor block. The remaining pixel values on the line are encoded using prediction. 

- 1705 If the predicted value of the pixel ( **Xpred)** is close enough to the original value of the pixel ( **Xorig** ) 1706 (abs( **Xorig - Xpred** ) < difference limit), its difference value ( **Xdiff** ) is quantized using a DPCM codec. 1707 Otherwise, **Xorig** is quantized using a PCM codec. The quantized value is combined with a code word 1708 describing the codec used to quantize the pixel and the sign bit, if applicable, to create the encoded value 1709 ( **Xenco** ). 

## **E.1 Predictors** 

1710 In order to have meaningful data transfer, both the transmitter and the receiver need to use the same 1711 predictor block. 

1712 

The order of pixels in a raw image is shown in Figure 154. 

- 1713 

|C00|C11|C02|C13|C04|C15|C06|C17|||
|---|---|---|---|---|---|---|---|---|---|
|C20|C31|C22|C33|C24|C35|C26|C37|||
|||||||||||
|||||||||||



**Figure 154 Pixel Order of the Original Image** 

1714 Figure 155 shows an example of the pixel order with RGB data. 

1715 

|G0|R1|G2|R3|G4|R5|G6|R7|||
|---|---|---|---|---|---|---|---|---|---|
|B0|G1|B2|G3|B4|G5|B6|G7|||
|||||||||||
|||||||||||



## **Figure 155 Example Pixel Order of the Original Image** 

- 1716 Two predictors are defined for use in the data compression schemes. 

- 1717 Predictor1 uses a very simple algorithm and is intended to minimize processing power and memory size 1718 requirements. Typically, this predictor is used when the compression requirements are modest and the 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

127 

Specification for CSI-2 

Version 1.3 

29-May-2014 

- 1719 original image quality is high. Predictor1 should be used with 10–8–10, 10–7–10 and 12–8–12 data 1720 compression schemes. 

- 1721 The second predictor, Predictor2, is more complex than Predictor1. This predictor provides slightly better 

- 1722 prediction than Predictor1 and therefore the decoded image quality can be improved compared to 1723 Predictor1. Predictor2 should be used with 10–6–10, 12–7–12, and 12–6–12 data compression schemes. 

- 1724 Both receiver and transmitter shall support Predictor1 for all data compression schemes. 

## **E.1.1 Predictor1** 

- 1725 Predictor1 uses only the previous same color component value as the prediction value. Therefore, only a 1726 two-pixel deep memory is required. 

- 1727 The first two pixels (C00, C11 / C20, C31 or as in example G0, R1 / B0, G1) in a line are encoded without 1728 prediction. 

- 1729 The prediction values for the remaining pixels in the line are calculated using the previous same color 1730 decoded value, **Xdeco** . Therefore, the predictor equation can be written as follows: 

- 1731 `Xpred( n ) =` **`Xdeco`** `(` **`n-2`** `)` 

## **E.1.2 Predictor2** 

- 1732 Predictor2 uses the four previous pixel values, when the prediction value is evaluated. This means that also 1733 the other color component values are used, when the prediction value has been defined. The predictor 1734 equations can be written as shown in the following formulas. 

- 1735 Predictor2 uses all color components of the four previous pixel values to create the prediction value. 1736 Therefore, a four-pixel deep memory is required. 

- 1737 The first pixel (C00 / C20, or as in example G0 / B0) in a line is coded without prediction. 

- 1738 The second pixel (C11 / C31 or as in example R1 / G1) in a line is predicted using the previous decoded 1739 different color value as a prediction value. The second pixel is predicted with the following equation: 

- 1740 **`Xpred`** `(` **`n`** `) =` **`Xdeco`** `(` **`n-1`** `)` 

- 1741 The third pixel (C02 / C22 or as in example G2 / B2) in a line is predicted using the previous decoded same 1742 color value as a prediction value. The third pixel is predicted with the following equation: 

- 1743 **`Xpred`** `(` **`n`** `) =` **`Xdeco`** `(` **`n-2`** `)` 

- 1744 The fourth pixel (C13 / C33 or as in example R3 / G3) in a line is predicted using the following equation: 1745 `if ((` **`Xdeco`** `(` **`n-1`** `) <=` **`Xdeco`** `(` **`n-2`** `) AND` **`Xdeco`** `(` **`n-2`** `) <=` **`Xdeco`** `(` **`n-3`** `)) OR` 1746 `(` **`Xdeco`** `(` **`n-1`** `) >=` **`Xdeco`** `(` **`n-2`** `) AND` **`Xdeco`** `(` **`n-2`** `) >=` **`Xdeco`** `(` **`n-3`** `))) then` 1747 **`Xpred`** `(` **`n`** `) =` **`Xdeco`** `(` **`n-1`** `)` 1748 `else` 1749 **`Xpred`** `(` **`n`** `) =` **`Xdeco`** `(` **`n-2`** `)` 1750 `endif` 

- 1751 Other pixels in all lines are predicted using the equation: 

- 1752 `if ((` **`Xdeco`** `(` **`n-1`** `) <=` **`Xdeco`** `(` **`n-2`** `) AND` **`Xdeco`** `(` **`n-2`** `) <=` **`Xdeco`** `(` **`n-3`** `)) OR` 

- 1753 `(` **`Xdeco`** `(` **`n-1`** `) >=` **`Xdeco`** `(` **`n-2`** `) AND` **`Xdeco`** `(` **`n-2`** `) >=` **`Xdeco`** `(` **`n-3`** `))) then` 1754 **`Xpred`** `(` **`n`** `) =` **`Xdeco`** `(` **`n-1`** `)` 

- 1755 `else if ((` **`Xdeco`** `(` **`n-1`** `) <=` **`Xdeco`** `(` **`n-3`** `) AND` **`Xdeco`** `(` **`n-2`** `) <=` **`Xdeco`** `(` **`n-4`** `)) OR` 

- 1756 `(` **`Xdeco`** `(` **`n-1`** `) >=` **`Xdeco`** `(` **`n-3`** `) AND` **`Xdeco`** `(` **`n-2`** `) >=` **`Xdeco`** `(` **`n-4`** `))) then` 1757 **`Xpred`** `(` **`n`** `) =` **`Xdeco`** `(` **`n-2`** `)` 1758 `else` 

- 1759 **`Xpred`** `(` **`n`** `) = (` **`Xdeco`** `(` **`n-2`** `) +` **`Xdeco`** `(` **`n-4`** `) + 1) / 2` 1760 `endif` 

## **E.2 Encoders** 

1761 There are six different encoders available, one for each data compression scheme. 

128 Copyright © 2005-2014 MIPI Alliance, Inc. 

All rights reserved. 

**Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

1762 For all encoders, the formula used for non-predicted pixels (beginning of lines) is different than the formula 1763 for predicted pixels. 

   - **E.2.1 Coder for 10–8–10 Data Compression** 

- 1764 The 10–8–10 coder offers a 20% bit rate reduction with very high image quality. 

1765 Pixels without prediction are encoded using the following formula: 1766 **`Xenco`** `(` **`n`** `) =` **`Xorig`** `(` **`n`** `) / 4` 1767 To avoid a full-zero encoded value, the following check is performed: 1768 `if (` **`Xenco`** `(` **`n`** `) == 0) then` 1769 **`Xenco`** `(` **`n`** `) = 1` 1770 `endif` 1771 Pixels with prediction are encoded using the following formula: 1772 `if (abs(` **`Xdiff`** `(` **`n`** `)) < 32) then` 1773 `use` **`DPCM1`** 1774 `else if (abs(` **`Xdiff`** `(` **`n`** `)) < 64) then` 1775 `use` **`DPCM2`** 1776 `else if (abs(` **`Xdiff`** `(` **`n`** `)) < 128) then` 1777 `use` **`DPCM3`** 1778 `else` 1779 `use` **`PCM`** 1780 `endif` 

## **E.2.1.1 DPCM1 for 10–8–10 Coder** 

1781 **Xenco** ( **n** ) has the following format: 1782 **`Xenco`** `(` **`n`** `) = “00 s xxxxx”` 1783 where, 1784 `“00” is the code word` 1785 `“s” is the` **`sign`** `bit` 1786 `“xxxxx” is the five bit` **`value`** `field` 1787 The coder equation is described as follows: 1788 `if (` **`Xdiff`** `(` **`n`** `) <= 0) then` 1789 **`sign`** `= 1` 1790 `else` 1791 **`sign`** `= 0` 1792 `endif` 1793 **`value`** `= abs(` **`Xdiff`** `(` **`n`** `))` 1794 _Note: Zero code has been avoided (0 is sent as -0)._ 

## **E.2.1.2 DPCM2 for 10–8–10 Coder** 

1795 **Xenco** ( **n** ) has the following format: 1796 **`Xenco`** `(` **`n`** `) = “010 s xxxx”` 1797 where, 1798 `“010” is the code word` 1799 `“s” is the` **`sign`** `bit` 1800 `“xxxx” is the four bit` **`value`** `field` 1801 The coder equation is described as follows: 1802 `if (` **`Xdiff`** `(` **`n`** `) < 0) then` 1803 **`sign`** `= 1` 1804 `else` 1805 **`sign`** `= 0` 

129 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. 

**Confidential** 

Specification for CSI-2 

Version 1.3 29-May-2014 

1806 `endif` 1807 **`value`** `= (abs(` **`Xdiff`** `(` **`n`** `)) - 32) / 2` 

## **E.2.1.3 DPCM3 for 10–8–10 Coder** 

1808 **Xenco** ( **n** ) has the following format: 1809 **`Xenco`** `(` **`n`** `) = “011 s xxxx”` 1810 where, 1811 `“011” is the code word` 1812 `“s” is the` **`sign`** `bit` 1813 `“xxxx” is the four bit` **`value`** `field` 1814 The coder equation is described as follows: 1815 `if (` **`Xdiff`** `(` **`n`** `) < 0) then` 1816 **`sign`** `= 1` 1817 `else` 1818 **`sign`** `= 0` 1819 `endif` 1820 **`value`** `= (abs(` **`Xdiff`** `(` **`n`** `)) - 64) / 4` 

**E.2.1.4 PCM for 10–8–10 Coder** 1821 **Xenco** ( **n** ) has the following format: 1822 **`Xenco`** `(` **`n`** `) = “1 xxxxxxx”` 

1823 where, 1824 `“1” is the code word` 1825 `the` **`sign`** `bit is not used` 1826 `“xxxxxxx” is the seven bit` **`value`** `field` 1827 The coder equation is described as follows: 

1828 **`value`** `=` **`Xorig`** `(` **`n`** `) / 8` 

## **E.2.2 Coder for 10–7–10 Data Compression** 

1829 The 10–7–10 coder offers 30% bit rate reduction with high image quality. 1830 Pixels without prediction are encoded using the following formula: 1831 **`Xenco`** `(` **`n`** `) =` **`Xorig`** `(` **`n`** `) / 8` 1832 To avoid a full-zero encoded value, the following check is performed: 1833 `if (` **`Xenco`** `(` **`n`** `) == 0) then` 1834 **`Xenco`** `(` **`n`** `) = 1` 1835 Pixels with prediction are encoded using the following formula: 1836 `if (abs(` **`Xdiff`** `(` **`n`** `)) < 8) then` 1837 `use` **`DPCM1`** 1838 `else if (abs(` **`Xdiff`** `(` **`n`** `)) < 16) then` 1839 `use` **`DPCM2`** 1840 `else if (abs(` **`Xdiff`** `(` **`n`** `)) < 32) then` 1841 `use` **`DPCM3`** 1842 `else if (abs(` **`Xdiff`** `(` **`n`** `)) < 160) then` 1843 `use` **`DPCM4`** 1844 `else` 1845 `use` **`PCM`** 1846 `endif` 

**E.2.2.1 DPCM1 for 10–7–10 Coder** 

1847 **Xenco** ( **n** ) has the following format: 

130 Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

1848 **`Xenco`** `(` **`n`** `) = “000 s xxx”` 1849 where, 1850 `“000” is the code word` 1851 `“s” is the` **`sign`** `bit` 1852 `“xxx” is the three bit` **`value`** `field` 1853 The coder equation is described as follows: 1854 `if (` **`Xdiff`** `(` **`n`** `) <= 0) then` 1855 **`sign`** `= 1` 1856 `else` 1857 **`sign`** `= 0` 1858 `endif` 1859 **`value`** `= abs(` **`Xdiff`** `(` **`n`** `))` 1860 _Note: Zero code has been avoided (0 is sent as -0)._ 

## **E.2.2.2 DPCM2 for 10–7–10 Coder** 

1861 **Xenco** ( **n** ) has the following format: 1862 **`Xenco`** `(` **`n`** `) = “0010 s xx”` 1863 where, 1864 `“0010” is the code word` 1865 `“s” is the` **`sign`** `bit` 1866 `“xx” is the two bit` **`value`** `field` 1867 The coder equation is described as follows: 1868 `if (` **`Xdiff`** `(` **`n`** `) < 0) then` 1869 **`sign`** `= 1` 1870 `else` 1871 **`sign`** `= 0` 1872 `endif` 1873 **`value`** `= (abs(` **`Xdiff`** `(` **`n`** `)) - 8) / 2` 

## **E.2.2.3 DPCM3 for 10–7–10 Coder** 

1874 **Xenco** ( **n** ) has the following format: 1875 **`Xenco`** `(` **`n`** `) = “0011 s xx”` 1876 where, 1877 `“0011” is the code word` 1878 `“s” is the` **`sign`** `bit` 1879 `“xx” is the two bit` **`value`** `field` 1880 The coder equation is described as follows: 1881 `if (` **`Xdiff`** `(` **`n`** `) < 0) then` 1882 **`sign`** `= 1` 1883 `else` 1884 **`sign`** `= 0` 1885 `endif` 1886 **`value`** `= (abs(` **`Xdiff`** `(` **`n`** `)) - 16) / 4` 

## **E.2.2.4 DPCM4 for 10–7–10 Coder** 

1887 **Xenco** ( **n** ) has the following format: 1888 **`Xenco`** `(` **`n`** `) = “01 s xxxx”` 1889 where, 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

131 

Specification for CSI-2 

Version 1.3 29-May-2014 

1890 `“01” is the code word` 1891 `“s” is the` **`sign`** `bit` 1892 `“xxxx” is the four bit` **`value`** `field` 1893 The coder equation is described as follows: 1894 `if (` **`Xdiff`** `(` **`n`** `) < 0) then` 1895 **`sign`** `= 1` 1896 `else` 1897 **`sign`** `= 0` 1898 `endif` 1899 **`value`** `= (abs(` **`Xdiff`** `(` **`n`** `)) - 32) / 8` **E.2.2.5 PCM for 10–7–10 Coder** 1900 **Xenco** ( **n** ) has the following format: 1901 **`Xenco`** `(` **`n`** `) = “1 xxxxxx”` 1902 where, 1903 `“1” is the code word` 1904 `the` **`sign`** `bit is not used` 1905 `“xxxxxx” is the six bit` **`value`** `field` 1906 The coder equation is described as follows: 1907 **`value`** `=` **`Xorig`** `(` **`n`** `) / 16` **E.2.3 Coder for 10–6–10 Data Compression** 1908 The 10–6–10 coder offers 40% bit rate reduction with acceptable image quality. 1909 Pixels without prediction are encoded using the following formula: 1910 **`Xenco`** `(` **`n`** `) =` **`Xorig`** `(` **`n`** `) / 16` 1911 To avoid a full-zero encoded value, the following check is performed: 1912 `if (` **`Xenco`** `(` **`n`** `) == 0) then` 1913 **`Xenco`** `(` **`n`** `) = 1` 1914 `endif` 1915 Pixels with prediction are encoded using the following formula: 1916 `if (abs(` **`Xdiff`** `(` **`n`** `)) < 1) then` 1917 `use` **`DPCM1`** 1918 `else if (abs(` **`Xdiff`** `(` **`n`** `)) < 3) then` 1919 `use` **`DPCM2`** 1920 `else if (abs(` **`Xdiff`** `(` **`n`** `)) < 11) then` 1921 `use` **`DPCM3`** 1922 `else if (abs(` **`Xdiff`** `(` **`n`** `)) < 43) then` 1923 `use` **`DPCM4`** 1924 `else if (abs(` **`Xdiff`** `(` **`n`** `)) < 171) then` 1925 `use` **`DPCM5`** 1926 `else` 1927 `use` **`PCM`** 1928 `endif` 

## **E.2.3.1 DPCM1 for 10–6–10 Coder** 

1929 **Xenco** ( **n** ) has the following format: 1930 **`Xenco`** `(` **`n`** `) = “00000 s”` 1931 where, 

Copyright © 2005-2014 MIPI Alliance, Inc. 

132 

All rights reserved. 

**Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

1932 `“00000” is the code word` 1933 `“s” is the` **`sign`** `bit` 1934 `the` **`value`** `field is not used` 1935 The coder equation is described as follows: 1936 **`sign`** `= 1` 1937 `Note: Zero code has been avoided (0 is sent as -0).` **E.2.3.2 DPCM2 for 10–6–10 Coder** 1938 **Xenco** ( **n** ) has the following format: 1939 **`Xenco`** `(` **`n`** `) = “00001 s”` 1940 where, 1941 `“00001” is the code word` 1942 `“s” is the` **`sign`** `bit` 1943 `the` **`value`** `field is not used` 1944 The coder equation is described as follows: 1945 `if (` **`Xdiff`** `(` **`n`** `) < 0) then` 1946 **`sign`** `= 1` 1947 `else` 1948 **`sign`** `= 0` 1949 `endif` **E.2.3.3 DPCM3 for 10–6–10 Coder** 1950 **Xenco** ( **n** ) has the following format: 1951 **`Xenco`** `(` **`n`** `) = “0001 s x”` 1952 where, 1953 `“0001” is the code word` 1954 `“s” is the` **`sign`** `bit` 1955 `“x” is the one bit` **`value`** `field` 1956 The coder equation is described as follows: 1957 `if (` **`Xdiff`** `(` **`n`** `) < 0) then` 1958 **`sign`** `= 1` 1959 `else` 1960 **`sign`** `= 0` 1961 **`value`** `= (abs(` **`Xdiff`** `(` **`n`** `)) - 3) / 4` 1962 `endif` **E.2.3.4 DPCM4 for 10–6–10 Coder** 1963 **Xenco** ( **n** ) has the following format: 1964 **`Xenco`** `(` **`n`** `) = “001 s xx”` 1965 where, 1966 `“001” is the code word` 1967 `“s” is the` **`sign`** `bit` 1968 `“xx” is the two bit` **`value`** `field` 1969 The coder equation is described as follows: 1970 `if (` **`Xdiff`** `(` **`n`** `) < 0) then` 1971 **`sign`** `= 1` 1972 `else` 1973 **`sign`** `= 0` 1974 `endif` 1975 **`value`** `= (abs(` **`Xdiff`** `(` **`n`** `)) - 11) / 8` 

Copyright © 2005-2014 MIPI Alliance, Inc. 

133 

All rights reserved. **Confidential** 

Specification for CSI-2 

Version 1.3 29-May-2014 

**E.2.3.5 DPCM5 for 10–6–10 Coder** 1976 **Xenco** ( **n** ) has the following format: 1977 **`Xenco`** `(` **`n`** `) = “01 s xxx”` 1978 where, 1979 `“01” is the code word` 1980 `“s” is the` **`sign`** `bit` 1981 `“xxx” is the three bit` **`value`** `field` 1982 The coder equation is described as follows: 1983 `if (` **`Xdiff`** `(` **`n`** `) < 0) then` 1984 **`sign`** `= 1` 1985 `else` 1986 **`sign`** `= 0` 1987 `endif` 1988 **`value`** `= (abs(` **`Xdiff`** `(` **`n`** `)) - 43) / 16` **E.2.3.6 PCM for 10–6–10 Coder** 1989 **Xenco** ( **n** ) has the following format: 1990 **`Xenco`** `(` **`n`** `) = “1 xxxxx”` 1991 where, 1992 `“1” is the code word` 1993 `the` **`sign`** `bit is not used` 1994 `“xxxxx” is the five bit` **`value`** `field` 1995 The coder equation is described as follows: 1996 **`value`** `=` **`Xorig`** `(` **`n`** `) / 32` **E.2.4 Coder for 12–8–12 Data Compression** 1997 The 12–8–12 coder offers 33% bit rate reduction with very high image quality. 1998 Pixels without prediction are encoded using the following formula: 1999 **`Xenco`** `(` **`n`** `) =` **`Xorig`** `(` **`n`** `) / 16` 2000 To avoid a full-zero encoded value, the following check is performed: 2001 `if (` **`Xenco`** `(` **`n`** `) == 0) then` 2002 **`Xenco`** `(` **`n`** `) = 1` 2003 `endif` 2004 Pixels with prediction are encoded using the following formula: 2005 `if (abs(` **`Xdiff`** `(` **`n`** `)) < 8) then` 2006 `use` **`DPCM1`** 2007 `else if (abs(` **`Xdiff`** `(` **`n`** `)) < 40) then` 2008 `use` **`DPCM2`** 2009 `else if (abs(` **`Xdiff`** `(` **`n`** `)) < 104) then` 2010 `use` **`DPCM3`** 2011 `else if (abs(` **`Xdiff`** `(` **`n`** `)) < 232) then` 2012 `use` **`DPCM4`** 2013 `else if (abs(` **`Xdiff`** `(` **`n`** `)) < 360) then` 2014 `use` **`DPCM5`** 2015 `else` 2016 `use` **`PCM`** 

## **E.2.4.1 DPCM1 for 12–8–12 Coder** 

2017 **Xenco** ( **n** ) has the following format: 2018 **`Xenco`** `(` **`n`** `) = “0000 s xxx”` 

134 Copyright © 2005-2014 MIPI Alliance, Inc. 

All rights reserved. 

**Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

2019 where, 2020 `“0000” is the code word` 2021 `“s” is the` **`sign`** `bit` 2022 `“xxx” is the three bit` **`value`** `field` 2023 The coder equation is described as follows: 2024 `if (` **`Xdiff`** `(` **`n`** `) <= 0) then` 2025 **`sign`** `= 1` 2026 `else` 2027 **`sign`** `= 0` 2028 `endif` 2029 **`value`** `= abs(` **`Xdiff`** `(` **`n`** `))` 2030 _Note: Zero code has been avoided (0 is sent as -0)._ 

## **E.2.4.2 DPCM2 for 12–8–12 Coder** 

2031 **Xenco** ( **n** ) has the following format: 2032 **`Xenco`** `(` **`n`** `) = “011 s xxxx”` 2033 where, 2034 `“011” is the code word` 2035 `“s” is the` **`sign`** `bit` 2036 `“xxxx” is the four bit` **`value`** `field` 2037 The coder equation is described as follows: 2038 `if (` **`Xdiff`** `(` **`n`** `) < 0) then` 2039 **`sign`** `= 1` 2040 `else` 2041 **`sign`** `= 0` 2042 `endif` 2043 **`value`** `= (abs(` **`Xdiff`** `(` **`n`** `)) - 8) / 2` 

## **E.2.4.3 DPCM3 for 12–8–12 Coder** 

2044 **Xenco** ( **n** ) has the following format: 2045 **`Xenco`** `(` **`n`** `) = “010 s xxxx”` 2046 where, 2047 `“010” is the code word` 2048 `“s” is the` **`sign`** `bit` 2049 `“xxxx” is the four bit` **`value`** `field` 2050 The coder equation is described as follows: 2051 `if (` **`Xdiff`** `(` **`n`** `) < 0) then` 2052 **`sign`** `= 1` 2053 `else` 2054 **`sign`** `= 0` 2055 `endif` 2056 **`value`** `= (abs(` **`Xdiff`** `(` **`n`** `)) - 40) / 4` 

## **E.2.4.4 DPCM4 for 12–8–12 Coder** 

2057 **Xenco** ( **n** ) has the following format: 2058 **`Xenco`** `(` **`n`** `) = “001 s xxxx”` 

2059 where, 2060 `“001” is the code word` 2061 `“s” is the` **`sign`** `bit` 2062 `“xxxx” is the four bit` **`value`** `field` 

Copyright © 2005-2014 MIPI Alliance, Inc. 

135 

All rights reserved. **Confidential** 

Specification for CSI-2 

Version 1.3 29-May-2014 

2063 The coder equation is described as follows: 2064 `if (` **`Xdiff`** `(` **`n`** `) < 0) then` 2065 **`sign`** `= 1` 2066 `else` 2067 **`sign`** `= 0` 2068 `endif` 2069 **`value`** `= (abs(` **`Xdiff`** `(` **`n`** `)) - 104) / 8` 

## **E.2.4.5 DPCM5 for 12–8–12 Coder** 

2070 **Xenco** ( **n** ) has the following format: 2071 **`Xenco`** `(` **`n`** `) = “0001 s xxx”` 2072 where, 2073 `“0001” is the code word` 2074 `“s” is the` **`sign`** `bit` 2075 `“xxx” is the three bit` **`value`** `field` 2076 The coder equation is described as follows: 2077 `if (` **`Xdiff`** `(` **`n`** `) < 0) then` 2078 **`sign`** `= 1` 2079 `else` 2080 **`sign`** `= 0` 2081 `endif` 2082 **`value`** `= (abs(` **`Xdiff`** `(` **`n`** `)) - 232) / 16` 

**E.2.4.6 PCM for 12–8–12 Coder** 

2083 **Xenco** ( **n** ) has the following format: 2084 **`Xenco`** `(` **`n`** `) = “1 xxxxxxx”` 2085 where, 2086 `“1” is the code word` 2087 `the` **`sign`** `bit is not used` 2088 `“xxxxxxx” is the seven bit` **`value`** `field` 2089 The coder equation is described as follows: 2090 **`value`** `=` **`Xorig`** `(` **`n`** `) / 32` 

**E.2.5 Coder for 12–7–12 Data Compression** 2091 The 12–7–12 coder offers 42% bit rate reduction with high image quality. 2092 Pixels without prediction are encoded using the following formula: 2093 **`Xenco`** `(` **`n`** `) =` **`Xorig`** `(` **`n`** `) / 32` 2094 To avoid a full-zero encoded value, the following check is performed: 2095 `if (` **`Xenco`** `(` **`n`** `) == 0) then` 2096 **`Xenco`** `(` **`n`** `) = 1` 2097 `endif` 2098 Pixels with prediction are encoded using the following formula: 2099 `if (abs(` **`Xdiff`** `(` **`n`** `)) < 4) then` 2100 `use` **`DPCM1`** 2101 `else if (abs(` **`Xdiff`** `(` **`n`** `)) < 12) then` 2102 `use` **`DPCM2`** 2103 `else if (abs(` **`Xdiff`** `(` **`n`** `)) < 28) then` 2104 `use` **`DPCM3`** 2105 `else if (abs(` **`Xdiff`** `(` **`n`** `)) < 92) then` 2106 `use` **`DPCM4`** 

Copyright © 2005-2014 MIPI Alliance, Inc. 

136 

All rights reserved. 

**Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

2107 `else if (abs(` **`Xdiff`** `(` **`n`** `)) < 220) then` 2108 `use` **`DPCM5`** 2109 `else if (abs(` **`Xdiff`** `(` **`n`** `)) < 348) then` 2110 `use` **`DPCM6`** 2111 `else` 2112 `use` **`PCM`** 2113 `endif` 

## **E.2.5.1 DPCM1 for 12–7–12 Coder** 

2114 **Xenco** ( **n** ) has the following format: 2115 **`Xenco`** `(` **`n`** `) = “0000 s xx”` 2116 where, 2117 `“0000” is the code word` 2118 `“s” is the` **`sign`** `bit` 2119 `“xx” is the two bit` **`value`** `field` 2120 The coder equation is described as follows: 2121 `if (` **`Xdiff`** `(` **`n`** `) <= 0) then` 2122 **`sign`** `= 1` 2123 `else` 2124 **`sign`** `= 0` 2125 `endif` 2126 **`value`** `= abs(` **`Xdiff`** `(` **`n`** `))` 2127 _Note: Zero code has been avoided (0 is sent as -0)._ 

## **E.2.5.2 DPCM2 for 12–7–12 Coder** 

2128 **Xenco** ( **n** ) has the following format: 2129 **`Xenco`** `(` **`n`** `) = “0001 s xx”` 2130 where, 2131 `“0001” is the code word` 2132 `“s” is the` **`sign`** `bit` 2133 `“xx” is the two bit` **`value`** `field` 2134 The coder equation is described as follows: 2135 `if (` **`Xdiff`** `(` **`n`** `) < 0) then` 2136 **`sign`** `= 1` 2137 `else` 2138 **`sign`** `= 0` 2139 `endif` 2140 **`value`** `= (abs(` **`Xdiff`** `(` **`n`** `)) - 4) / 2` **E.2.5.3 DPCM3 for 12–7–12 Coder** 2141 **Xenco** ( **n** ) has the following format: 2142 **`Xenco`** `(` **`n`** `) = “0010 s xx”` 2143 where, 2144 `“0010” is the code word` 2145 `“s” is the` **`sign`** `bit` 2146 `“xx” is the two bit` **`value`** `field` 2147 The coder equation is described as follows: 2148 `if (` **`Xdiff`** `(` **`n`** `) < 0) then` 2149 **`sign`** `= 1` 2150 `else` 

Copyright © 2005-2014 MIPI Alliance, Inc. 

137 

All rights reserved. **Confidential** 

Specification for CSI-2 

Version 1.3 29-May-2014 

2151 **`sign`** `= 0` 2152 `endif` 2153 **`value`** `= (abs(` **`Xdiff`** `(` **`n`** `)) - 12) / 4` 

**E.2.5.4 DPCM4 for 12–7–12 Coder** 

2154 **Xenco** ( **n** ) has the following format: 2155 **`Xenco`** `(` **`n`** `) = “010 s xxx”` 2156 where, 2157 `“010” is the code word` 2158 `“s” is the` **`sign`** `bit` 2159 `“xxx” is the three bit` **`value`** `field` 2160 The coder equation is described as follows: 2161 `if (` **`Xdiff`** `(` **`n`** `) < 0) then` 2162 **`sign`** `= 1` 2163 `else` 2164 **`sign`** `= 0` 2165 `endif` 2166 **`value`** `= (abs(` **`Xdiff`** `(` **`n`** `)) - 28) / 8` 

## **E.2.5.5 DPCM5 for 12–7–12 Coder** 

2167 **Xenco** ( **n** ) has the following format: 2168 **`Xenco`** `(` **`n`** `) = “011 s xxx”` 2169 where, 2170 `“011” is the code word` 2171 `“s” is the` **`sign`** `bit` 2172 `“xxx” is the three bit` **`value`** `field` 2173 The coder equation is described as follows: 2174 `if (` **`Xdiff`** `(` **`n`** `) < 0) then` 2175 **`sign`** `= 1` 2176 `else` 2177 **`sign`** `= 0` 2178 `endif` 2179 **`value`** `= (abs(` **`Xdiff`** `(` **`n`** `)) - 92) / 16` 

## **E.2.5.6 DPCM6 for 12–7–12 Coder** 

2180 **Xenco** ( **n** ) has the following format: 2181 **`Xenco`** `(` **`n`** `) = “0011 s xx”` 2182 where, 2183 `“0011” is the code word` 2184 `“s” is the` **`sign`** `bit` 2185 `“xx” is the two bit` **`value`** `field` 2186 The coder equation is described as follows: 2187 `if (` **`Xdiff`** `(` **`n`** `) < 0) then` 2188 **`sign`** `= 1` 2189 `else` 2190 **`sign`** `= 0` 2191 `endif` 2192 **`value`** `= (abs(` **`Xdiff`** `(` **`n`** `)) - 220) / 32` 

Copyright © 2005-2014 MIPI Alliance, Inc. 

138 

All rights reserved. **Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

## **E.2.5.7 PCM for 12–7–12 Coder** 

2193 **Xenco** ( **n** ) has the following format: 2194 **`Xenco`** `(` **`n`** `) = “1 xxxxxx”` 2195 where, 2196 `“1” is the code word` 2197 `the` **`sign`** `bit is not used` 2198 `“xxxxxx” is the six bit` **`value`** `field` 2199 The coder equation is described as follows: 2200 **`value`** `=` **`Xorig`** `(` **`n`** `) / 64` **E.2.6 Coder for 12–6–12 Data Compression** 2201 The 12–6–12 coder offers 50% bit rate reduction with acceptable image quality. 2202 Pixels without prediction are encoded using the following formula: 2203 **`Xenco`** `(` **`n`** `) =` **`Xorig`** `(` **`n`** `) / 64` 2204 To avoid a full-zero encoded value, the following check is performed: 2205 `if (` **`Xenco`** `(` **`n`** `) == 0) then` 2206 **`Xenco`** `(` **`n`** `) = 1` 2207 `endif` 2208 Pixels with prediction are encoded using the following formula: 2209 `if (abs(` **`Xdiff`** `(` **`n`** `)) < 2) then` 2210 `use` **`DPCM1`** 2211 `else if (abs(` **`Xdiff`** `(` **`n`** `)) < 10) then` 2212 `use` **`DPCM3`** 2213 `else if (abs(` **`Xdiff`** `(` **`n`** `)) < 42) then` 2214 `use` **`DPCM4`** 2215 `else if (abs(` **`Xdiff`** `(` **`n`** `)) < 74) then` 2216 `use` **`DPCM5`** 2217 `else if (abs(` **`Xdiff`** `(` **`n`** `)) < 202) then` 2218 `use` **`DPCM6`** 2219 `else if (abs(` **`Xdiff`** `(` **`n`** `)) < 330) then` 2220 `use` **`DPCM7`** 2221 `else` 2222 `use` **`PCM`** 2223 `endif` 2224 _Note:_ _**DPCM2** is not used._ 

## **E.2.6.1 DPCM1 for 12–6–12 Coder** 

2225 **Xenco** ( **n** ) has the following format: 2226 **`Xenco`** `(` **`n`** `) = “0000 s x”` 2227 where, 2228 `“0000” is the code word` 2229 `“s” is the` **`sign`** `bit` 2230 `“x” is the one bit` **`value`** `field` 2231 The coder equation is described as follows: 2232 `if (` **`Xdiff`** `(` **`n`** `) <= 0) then` 2233 **`sign`** `= 1` 2234 `else` 2235 **`sign`** `= 0` 2236 `endif` 2237 **`value`** `= abs(` **`Xdiff`** `(` **`n`** `))` 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. 

139 

**Confidential** 

Specification for CSI-2 

Version 1.3 29-May-2014 

2238 _Note: Zero code has been avoided (0 is sent as -0)._ 

**E.2.6.2 DPCM3 for 12–6–12 Coder** 

2239 **Xenco** ( **n** ) has the following format: 2240 **`Xenco`** `(` **`n`** `) = “0001 s x”` 2241 where, 2242 `“0001” is the code word` 2243 `“s” is the` **`sign`** `bit` 2244 `“x” is the one bit` **`value`** `field` 2245 The coder equation is described as follows: 2246 `if (` **`Xdiff`** `(` **`n`** `) < 0) then` 2247 **`sign`** `= 1` 2248 `else` 2249 **`sign`** `= 0` 2250 `endif` 2251 **`value`** `= (abs(` **`Xdiff`** `(` **`n`** `)) - 2) / 4` **E.2.6.3 DPCM4 for 12–6–12 Coder** 2252 **Xenco** ( **n** ) has the following format: 2253 **`Xenco`** `(` **`n`** `) = “010 s xx”` 2254 where, 2255 `“010” is the code word` 2256 `“s” is the` **`sign`** `bit` 2257 `“xx” is the two bit` **`value`** `field` 2258 The coder equation is described as follows: 2259 `if (` **`Xdiff`** `(` **`n`** `) < 0) then` 2260 **`sign`** `= 1` 2261 `else` 2262 **`sign`** `= 0` 2263 `endif` 2264 **`value`** `= (abs(` **`Xdiff`** `(` **`n`** `)) - 10) / 8` 

## **E.2.6.4 DPCM5 for 12–6–12 Coder** 

2265 **Xenco** ( **n** ) has the following format: 2266 **`Xenco`** `(` **`n`** `) = “0010 s x”` 2267 where, 2268 `“0010” is the code word` 2269 `“s” is the` **`sign`** `bit` 2270 `“x” is the one bit` **`value`** `field` 2271 The coder equation is described as follows: 2272 `if (` **`Xdiff`** `(` **`n`** `) < 0) then` 2273 **`sign`** `= 1` 2274 `else` 2275 **`sign`** `= 0` 2276 `endif` 2277 **`value`** `= (abs(` **`Xdiff`** `(` **`n`** `)) - 42) / 16` 

## **E.2.6.5 DPCM6 for 12–6–12 Coder** 

2278 **Xenco** ( **n** ) has the following format: 2279 **`Xenco`** `(` **`n`** `) = “011 s xx”` 

140 Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

2280 where, 2281 `“011” is the code word` 2282 `“s” is the` **`sign`** `bit` 2283 `“xx” is the two bit` **`value`** `field` 2284 The coder equation is described as follows: 2285 `if (` **`Xdiff`** `(` **`n`** `) < 0) then` 2286 **`sign`** `= 1` 2287 `else` 2288 **`sign`** `= 0` 2289 `endif` 2290 **`value`** `= (abs(` **`Xdiff`** `(` **`n`** `)) - 74) / 32` **E.2.6.6 DPCM7 for 12–6–12 Coder** 2291 **Xenco** ( **n** ) has the following format: 2292 **`Xenco`** `(` **`n`** `) = “0011 s x”` 2293 where, 2294 `“0011” is the code word` 2295 `“s” is the` **`sign`** `bit` 2296 `“x” is the one bit` **`value`** `field` 2297 The coder equation is described as follows: 2298 `if (` **`Xdiff`** `(` **`n`** `) < 0) then` 2299 **`sign`** `= 1` 2300 `else` 2301 **`sign`** `= 0` 2302 `endif` 2303 **`value`** `= (abs(` **`Xdiff`** `(` **`n`** `)) - 202) / 64` 

## **E.2.6.7 PCM for 12–6–12 Coder** 

2304 **Xenco** ( **n** ) has the following format: 2305 **`Xenco`** `(` **`n`** `) = “1 xxxxx”` 

2306 where, 2307 `“1” is the code word` 2308 `the` **`sign`** `bit is not used` 2309 `“xxxxx” is the five bit` **`value`** `field` 2310 The coder equation is described as follows: 2311 **`value`** `=` **`Xorig`** `(` **`n`** `) / 128` 

## **E.3 Decoders** 

2312 There are six different decoders available, one for each data compression scheme. 

2313 For all decoders, the formula used for non-predicted pixels (beginning of lines) is different than the formula 2314 for predicted pixels. 

**E.3.1 Decoder for 10–8–10 Data Compression** 

2315 Pixels without prediction are decoded using the following formula: 

2316 **`Xdeco`** `(` **`n`** `) = 4 *` **`Xenco`** `(` **`n`** `) + 2` 

2317 Pixels with prediction are decoded using the following formula: 

2318 `if (` **`Xenco`** `(` **`n`** `) & 0xc0 == 0x00) then` 2319 `use` **`DPCM1`** 2320 `else if (` **`Xenco`** `(` **`n`** `) & 0xe0 == 0x40) then` 

Copyright © 2005-2014 MIPI Alliance, Inc. 141 All rights reserved. **Confidential** 

Specification for CSI-2 

Version 1.3 29-May-2014 

2321 `use` **`DPCM2`** 2322 `else if (` **`Xenco`** `(` **`n`** `) & 0xe0 == 0x60) then` 2323 `use` **`DPCM3`** 2324 `else` 2325 `use` **`PCM`** 2326 `endif` 

## **E.3.1.1 DPCM1 for 10–8–10 Decoder** 

2327 **Xenco** ( **n** ) has the following format: 2328 **`Xenco`** `(` **`n`** `) = “00 s xxxxx”` 2329 where, 2330 `“00” is the code word` 2331 `“s” is the` **`sign`** `bit` 2332 `“xxxxx” is the five bit` **`value`** `field` 2333 The decoder equation is described as follows: 2334 **`sign`** `=` **`Xenco`** `(` **`n`** `) & 0x20` 2335 **`value`** `=` **`Xenco`** `(` **`n`** `) & 0x1f` 2336 `if (` **`sign`** `> 0) then` 2337 **`Xdeco`** `(` **`n`** `) =` **`Xpred`** `(` **`n`** `) -` **`value`** 2338 `else` 2339 **`Xdeco`** `(` **`n`** `) =` **`Xpred`** `(` **`n`** `) +` **`value`** 2340 `endif` 

## **E.3.1.2 DPCM2 for 10–8–10 Decoder** 

2341 **Xenco** ( **n** ) has the following format: 2342 **`Xenco`** `(` **`n`** `) = “010 s xxxx”` 2343 where, 2344 `“010” is the code word` 2345 `“s” is the` **`sign`** `bit` 2346 `“xxxx” is the four bit` **`value`** `field` 2347 The decoder equation is described as follows: 2348 **`sign`** `=` **`Xenco`** `(` **`n`** `) & 0x10` 2349 **`value`** `= 2 * (` **`Xenco`** `(` **`n`** `) & 0xf) + 32` 2350 `if (` **`sign`** `> 0) then` 2351 **`Xdeco`** `(` **`n`** `) =` **`Xpred`** `(` **`n`** `) -` **`value`** 2352 `else` 2353 **`Xdeco`** `(` **`n`** `) =` **`Xpred`** `(` **`n`** `) +` **`value`** 2354 `endif` 

## **E.3.1.3 DPCM3 for 10–8–10 Decoder** 

2355 **Xenco** ( **n** ) has the following format: 2356 **`Xenco`** `(` **`n`** `) = “011 s xxxx”` 2357 where, 2358 `“011” is the code word` 2359 `“s” is the` **`sign`** `bit` 2360 `“xxxx” is the four bit` **`value`** `field` 2361 The decoder equation is described as follows: 2362 **`sign`** `=` **`Xenco`** `(` **`n`** `) & 0x10` 2363 **`value`** `= 4 * (` **`Xenco`** `(` **`n`** `) & 0xf) + 64 + 1` 2364 `if (` **`sign`** `> 0) then` 2365 **`Xdeco`** `(` **`n`** `) =` **`Xpred`** `(` **`n`** `) -` **`value`** 142 Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

2366 `if (` **`Xdeco`** `(` **`n`** `) < 0) then` 2367 **`Xdeco`** `(` **`n`** `) = 0` 2368 `endif` 2369 `else` 2370 **`Xdeco`** `(` **`n`** `) =` **`Xpred`** `(` **`n`** `) +` **`value`** 2371 `if (` **`Xdeco`** `(` **`n`** `) > 1023) then` 2372 **`Xdeco`** `(` **`n`** `) = 1023` 2373 `endif` 2374 `endif` 

**E.3.1.4 PCM for 10–8–10 Decoder** 

2375 **Xenco** ( **n** ) has the following format: 2376 **`Xenco`** `(` **`n`** `) = “1 xxxxxxx”` 2377 where, 2378 `“1” is the code word` 2379 `the` **`sign`** `bit is not used` 2380 `“xxxxxxx” is the seven bit` **`value`** `field` 2381 The codec equation is described as follows: 2382 **`value`** `= 8 * (` **`Xenco`** `(` **`n`** `) & 0x7f)` 2383 `if (` **`value`** `>` **`Xpred`** `(` **`n`** `)) then` 2384 **`Xdeco`** `(` **`n`** `) =` **`value`** `+ 3` 2385 `endif` 2386 `else` 2387 **`Xdeco`** `(` **`n`** `) =` **`value`** `+ 4` 2388 `endif` 

**E.3.2 Decoder for 10–7–10 Data Compression** 

2389 Pixels without prediction are decoded using the following formula: 2390 **`Xdeco`** `(` **`n`** `) = 8 *` **`Xenco`** `(` **`n`** `) + 4` 2391 Pixels with prediction are decoded using the following formula: 2392 `if (` **`Xenco`** `(` **`n`** `) & 0x70 == 0x00) then` 2393 `use` **`DPCM1`** 2394 `else if (` **`Xenco`** `(` **`n`** `) & 0x78 == 0x10) then` 2395 `use` **`DPCM2`** 2396 `else if (` **`Xenco`** `(` **`n`** `) & 0x78 == 0x18) then` 2397 `use` **`DPCM3`** 2398 `else if (` **`Xenco`** `(` **`n`** `) & 0x60 == 0x20) then` 2399 `use` **`DPCM4`** 2400 `else` 2401 `use` **`PCM`** 2402 `endif` 

**E.3.2.1 DPCM1 for 10–7–10 Decoder** 

2403 **Xenco** ( **n** ) has the following format: 2404 **`Xenco`** `(` **`n`** `) = “000 s xxx”` 2405 where, 2406 `“000” is the code word` 2407 `“s” is the` **`sign`** `bit` 2408 `“xxx” is the three bit` **`value`** `field` 

2409 The codec equation is described as follows: 2410 **`sign`** `=` **`Xenco`** `(` **`n`** `) & 0x8` 

Copyright © 2005-2014 MIPI Alliance, Inc. 

143 

All rights reserved. **Confidential** 

Specification for CSI-2 

Version 1.3 29-May-2014 

2411 **`value`** `=` **`Xenco`** `(` **`n`** `) & 0x7` 2412 `if (` **`sign`** `> 0) then` 2413 **`Xdeco`** `(` **`n`** `) =` **`Xpred`** `(` **`n`** `) -` **`value`** 2414 `else` 2415 **`Xdeco`** `(` **`n`** `) =` **`Xpred`** `(` **`n`** `) +` **`value`** 2416 `endif` 

## **E.3.2.2 DPCM2 for 10–7–10 Decoder** 

2417 **Xenco** ( **n** ) has the following format: 2418 **`Xenco`** `(` **`n`** `) = “0010 s xx”` 2419 where, 2420 `“0010” is the code word` 2421 `“s” is the` **`sign`** `bit` 2422 `“xx” is the two bit` **`value`** `field` 2423 The codec equation is described as follows: 2424 **`sign`** `=` **`Xenco`** `(` **`n`** `) & 0x4` 2425 **`value`** `= 2 * (` **`Xenco`** `(` **`n`** `) & 0x3) + 8` 2426 `if (` **`sign`** `> 0) then` 2427 **`Xdeco`** `(` **`n`** `) =` **`Xpred`** `(` **`n`** `) -` **`value`** 2428 `else` 2429 **`Xdeco`** `(` **`n`** `) =` **`Xpred`** `(` **`n`** `) +` **`value`** 2430 `endif` 

**E.3.2.3 DPCM3 for 10–7–10 Decoder** 

2431 **Xenco** ( **n** ) has the following format: 2432 **`Xenco`** `(` **`n`** `) = “0011 s xx”` 2433 where, 2434 `“0011” is the code word` 2435 `“s” is the` **`sign`** `bit` 2436 `“xx” is the two bit` **`value`** `field` 2437 The codec equation is described as follows: 2438 **`sign`** `=` **`Xenco`** `(` **`n`** `) & 0x4` 2439 **`value`** `= 4 * (` **`Xenco`** `(` **`n`** `) & 0x3) + 16 + 1` 2440 `if (` **`sign`** `> 0) then` 2441 **`Xdeco`** `(` **`n`** `) =` **`Xpred`** `(` **`n`** `) -` **`value`** 2442 `if (` **`Xdeco`** `(` **`n`** `) < 0) then` 2443 **`Xdeco`** `(` **`n`** `) = 0` 2444 `endif` 2445 `else` 2446 **`Xdeco`** `(` **`n`** `) =` **`Xpred`** `(` **`n`** `) +` **`value`** 2447 `if (` **`Xdeco`** `(` **`n`** `) > 1023) then` 2448 **`Xdeco`** `(` **`n`** `) = 1023` 2449 `endif` 2450 `endif` 

**E.3.2.4 DPCM4 for 10–7–10 Decoder** 

2451 **Xenco** ( **n** ) has the following format: 2452 **`Xenco`** `(` **`n`** `) = “01 s xxxx”` 2453 where, 

Copyright © 2005-2014 MIPI Alliance, Inc. 

144 

All rights reserved. **Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

2454 `“01” is the code word` 2455 `“s” is the` **`sign`** `bit` 2456 `“xxxx” is the four bit` **`value`** `field` 2457 The codec equation is described as follows: 2458 **`sign`** `=` **`Xenco`** `(` **`n`** `) & 0x10` 2459 **`value`** `= 8 * (` **`Xenco`** `(` **`n`** `) & 0xf) + 32 + 3` 2460 `if (` **`sign`** `> 0) then` 2461 **`Xdeco`** `(` **`n`** `) =` **`Xpred`** `(` **`n`** `) -` **`value`** 2462 `if (` **`Xdeco`** `(` **`n`** `) < 0) then` 2463 **`Xdeco`** `(` **`n`** `) = 0` 2464 `endif` 2465 `else` 2466 **`Xdeco`** `(` **`n`** `) =` **`Xpred`** `(` **`n`** `) +` **`value`** 2467 `if (` **`Xdeco`** `(` **`n`** `) > 1023) then` 2468 **`Xdeco`** `(` **`n`** `) = 1023` 2469 `endif` 2470 `endif` 

**E.3.2.5 PCM for 10–7–10 Decoder** 

2471 **Xenco** ( **n** ) has the following format: 2472 **`Xenco`** `(` **`n`** `) = “1 xxxxxx”` 2473 where, 2474 `“1” is the code word` 2475 `the` **`sign`** `bit is not used` 2476 `“xxxxxx” is the six bit` **`value`** `field` 2477 The codec equation is described as follows: 2478 **`value`** `= 16 * (` **`Xenco`** `(` **`n`** `) & 0x3f)` 2479 `if (` **`value`** `>` **`Xpred`** `(` **`n`** `)) then` 2480 **`Xdeco`** `(` **`n`** `) =` **`value`** `+ 7` 2481 `else` 2482 **`Xdeco`** `(` **`n`** `) =` **`value`** `+ 8` 2483 `endif` 

## **E.3.3 Decoder for 10–6–10 Data Compression** 

2484 Pixels without prediction are decoded using the following formula: 2485 **`Xdeco`** `(` **`n`** `) = 16 *` **`Xenco`** `(` **`n`** `) + 8` 2486 Pixels with prediction are decoded using the following formula: 2487 `if (` **`Xenco`** `(` **`n`** `) & 0x3e == 0x00) then` 2488 `use` **`DPCM1`** 2489 `else if (` **`Xenco`** `(` **`n`** `) & 0x3e == 0x02) then` 2490 `use` **`DPCM2`** 2491 `else if (` **`Xenco`** `(` **`n`** `) & 0x3c == 0x04) then` 2492 `use` **`DPCM3`** 2493 `else if (` **`Xenco`** `(` **`n`** `) & 0x38 == 0x08) then` 2494 `use` **`DPCM4`** 2495 `else if (` **`Xenco`** `(` **`n`** `) & 0x30 == 0x10) then` 2496 `use` **`DPCM5`** 2497 `else` 2498 `use` **`PCM`** 2499 `endif` 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

145 

Specification for CSI-2 

Version 1.3 29-May-2014 

## **E.3.3.1 DPCM1 for 10–6–10 Decoder** 

2500 **Xenco** ( **n** ) has the following format: 2501 **`Xenco`** `(` **`n`** `) = “00000 s”` 2502 where, 2503 `“00000” is the code word` 2504 `“s” is the` **`sign`** `bit` 2505 `the` **`value`** `field is not used` 2506 The codec equation is described as follows: 2507 `Xdeco( n ) = Xpred( n )` 

## **E.3.3.2 DPCM2 for 10–6–10 Decoder** 

2508 **Xenco** ( **n** ) has the following format: 2509 **`Xenco`** `(` **`n`** `) = “00001 s”` 2510 where, 2511 `“00001” is the code word` 2512 `“s” is the` **`sign`** `bit` 2513 `the` **`value`** `field is not used` 2514 The codec equation is described as follows: 2515 **`sign`** `=` **`Xenco`** `(` **`n`** `) & 0x1` 2516 **`value`** `= 1` 2517 `if (` **`sign`** `> 0) then` 2518 **`Xdeco`** `(` **`n`** `) =` **`Xpred`** `(` **`n`** `) -` **`value`** 2519 `else` 2520 **`Xdeco`** `(` **`n`** `) =` **`Xpred`** `(` **`n`** `) +` **`value`** 2521 `endif` 

## **E.3.3.3 DPCM3 for 10–6–10 Decoder** 

2522 **Xenco** ( **n** ) has the following format: 2523 **`Xenco`** `(` **`n`** `) = “0001 s x”` 2524 where, 2525 `“0001” is the code word` 2526 `“s” is the` **`sign`** `bit` 2527 `“x” is the one bit` **`value`** `field` 2528 The codec equation is described as follows: 2529 **`sign`** `=` **`Xenco`** `(` **`n`** `) & 0x2` 2530 **`value`** `= 4 * (` **`Xenco`** `(` **`n`** `) & 0x1) + 3 + 1` 2531 `if (` **`sign`** `> 0) then` 2532 **`Xdeco`** `(` **`n`** `) =` **`Xpred`** `(` **`n`** `) -` **`value`** 2533 `if (` **`Xdeco`** `(` **`n`** `) < 0) then` 2534 **`Xdeco`** `(` **`n`** `) = 0` 2535 `endif` 2536 `else` 2537 **`Xdeco`** `(` **`n`** `) =` **`Xpred`** `(` **`n`** `) +` **`value`** 2538 `if (` **`Xdeco`** `(` **`n`** `) > 1023) then` 2539 **`Xdeco`** `(` **`n`** `) = 1023` 2540 `endif` 2541 `endif` 

## **E.3.3.4 DPCM4 for 10–6–10 Decoder** 

2542 **Xenco** ( **n** ) has the following format: 

146 Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

2543 **`Xenco`** `(` **`n`** `) = “001 s xx”` 2544 where, 2545 `“001” is the code word` 2546 `“s” is the` **`sign`** `bit` 2547 `“xx” is the two bit` **`value`** `field` 2548 The codec equation is described as follows: 2549 **`sign`** `=` **`Xenco`** `(` **`n`** `) & 0x4` 2550 **`value`** `= 8 * (` **`Xenco`** `(` **`n`** `) & 0x3) + 11 + 3` 2551 `if (` **`sign`** `> 0) then` 2552 **`Xdeco`** `(` **`n`** `) =` **`Xpred`** `(` **`n`** `) -` **`value`** 2553 `if (` **`Xdeco`** `(` **`n`** `) < 0) then` 2554 **`Xdeco`** `(` **`n`** `) = 0` 2555 `endif` 2556 `else` 2557 **`Xdeco`** `(` **`n`** `) =` **`Xpred`** `(` **`n`** `) +` **`value`** 2558 `if (` **`Xdeco`** `(` **`n`** `) > 1023) then` 2559 **`Xdeco`** `(` **`n`** `) = 1023` 2560 `endif` 2561 `endif` 

**E.3.3.5 DPCM5 for 10–6–10 Decoder** 2562 **Xenco** ( **n** ) has the following format: 2563 **`Xenco`** `(` **`n`** `) = “01 s xxx”` 2564 where, 2565 `“01” is the code word` 2566 `“s” is the` **`sign`** `bit` 2567 `“xxx” is the three bit` **`value`** `field` 2568 The codec equation is described as follows: 2569 **`sign`** `=` **`Xenco`** `(` **`n`** `) & 0x8` 2570 **`value`** `= 16 * (` **`Xenco`** `(` **`n`** `) & 0x7) + 43 + 7` 2571 `if (` **`sign`** `> 0) then` 2572 **`Xdeco`** `(` **`n`** `) =` **`Xpred`** `(` **`n`** `) -` **`value`** 2573 `if (` **`Xdeco`** `(` **`n`** `) < 0) then` 2574 **`Xdeco`** `(` **`n`** `) = 0` 2575 `endif` 2576 `else` 2577 **`Xdeco`** `(` **`n`** `) =` **`Xpred`** `(` **`n`** `) +` **`value`** 2578 `if (` **`Xdeco`** `(` **`n`** `) > 1023) then` 2579 **`Xdeco`** `(` **`n`** `) = 1023` 2580 `endif` 2581 `endif` 

**E.3.3.6 PCM for 10–6–10 Decoder** 2582 **Xenco** ( **n** ) has the following format: 2583 **`Xenco`** `(` **`n`** `) = “1 xxxxx”` 2584 where, 2585 `“1” is the code word` 2586 `the` **`sign`** `bit is not used` 2587 `“xxxxx” is the five bit` **`value`** `field` 2588 The codec equation is described as follows: 2589 **`value`** `= 32 * (` **`Xenco`** `(` **`n`** `) & 0x1f)` 

Copyright © 2005-2014 MIPI Alliance, Inc. 

147 

All rights reserved. **Confidential** 

Specification for CSI-2 

Version 1.3 29-May-2014 

2590 `if (` **`value`** `>` **`Xpred`** `(` **`n`** `)) then` 2591 **`Xdeco`** `(` **`n`** `) =` **`value`** `+ 15` 2592 `else` 2593 **`Xdeco`** `(` **`n`** `) =` **`value`** `+ 16` 2594 `endif` 

## **E.3.4 Decoder for 12–8–12 Data Compression** 

2595 Pixels without prediction are decoded using the following formula: 2596 **`Xdeco`** `(` **`n`** `) = 16 *` **`Xenco`** `(` **`n`** `) + 8` 2597 Pixels with prediction are decoded using the following formula: 2598 `if (` **`Xenco`** `(` **`n`** `) & 0xf0 == 0x00) then` 2599 `use` **`DPCM1`** 2600 `else if (` **`Xenco`** `(` **`n`** `) & 0xe0 == 0x60) then` 2601 `use` **`DPCM2`** 2602 `else if (` **`Xenco`** `(` **`n`** `) & 0xe0 == 0x40) then` 2603 `use` **`DPCM3`** 2604 `else if (` **`Xenco`** `(` **`n`** `) & 0xe0 == 0x20) then` 2605 `use` **`DPCM4`** 2606 `else if (` **`Xenco`** `(` **`n`** `) & 0xf0 == 0x10) then` 2607 `use` **`DPCM5`** 2608 `else` 2609 `use` **`PCM`** 2610 `endif` 

**E.3.4.1 DPCM1 for 12–8–12 Decoder** 

2611 **Xenco** ( **n** ) has the following format: 2612 **`Xenco`** `(` **`n`** `) = “0000 s xxx”` 2613 where, 2614 `“0000” is the code word` 2615 `“s” is the` **`sign`** `bit` 2616 `“xxx” is the three bit` **`value`** `field` 2617 The codec equation is described as follows: 2618 **`sign`** `=` **`Xenco`** `(` **`n`** `) & 0x8` 2619 **`value`** `=` **`Xenco`** `(` **`n`** `) & 0x7` 2620 `if (` **`sign`** `> 0) then` 2621 **`Xdeco`** `(` **`n`** `) =` **`Xpred`** `(` **`n`** `) -` **`value`** 2622 `else` 2623 **`Xdeco`** `(` **`n`** `) =` **`Xpred`** `(` **`n`** `) +` **`value`** 2624 `endif` 

## **E.3.4.2 DPCM2 for 12–8–12 Decoder** 

2625 **Xenco** ( **n** ) has the following format: 2626 **`Xenco`** `(` **`n`** `) = “011 s xxxx”` 2627 where, 2628 `“011” is the code word` 2629 `“s” is the` **`sign`** `bit` 2630 `“xxxx” is the four bit` **`value`** `field` 2631 The codec equation is described as follows: 2632 **`sign`** `=` **`Xenco`** `(` **`n`** `) & 0x10` 2633 **`value`** `= 2 * (` **`Xenco`** `(` **`n`** `) & 0xf) + 8` 2634 `if (` **`sign`** `> 0) then` 

Copyright © 2005-2014 MIPI Alliance, Inc. 

148 

All rights reserved. **Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

2635 **`Xdeco`** `(` **`n`** `) =` **`Xpred`** `(` **`n`** `) -` **`value`** 2636 `else` 2637 **`Xdeco`** `(` **`n`** `) =` **`Xpred`** `(` **`n`** `) +` **`value`** 2638 `endif` **E.3.4.3 DPCM3 for 12–8–12 Decoder** 2639 **Xenco** ( **n** ) has the following format: 2640 **`Xenco`** `(` **`n`** `) = “010 s xxxx”` 2641 where, 2642 `“010” is the code word` 2643 `“s” is the` **`sign`** `bit` 2644 `“xxxx” is the four bit` **`value`** `field` 2645 The codec equation is described as follows: 2646 **`sign`** `=` **`Xenco`** `(` **`n`** `) & 0x10` 2647 **`value`** `= 4 * (` **`Xenco`** `(` **`n`** `) & 0xf) + 40 + 1` 2648 `if (` **`sign`** `> 0) then` 2649 **`Xdeco`** `(` **`n`** `) =` **`Xpred`** `(` **`n`** `) -` **`value`** 2650 `if (` **`Xdeco`** `(` **`n`** `) < 0) then` 2651 **`Xdeco`** `(` **`n`** `) = 0` 2652 `endif` 2653 `else` 2654 **`Xdeco`** `(` **`n`** `) =` **`Xpred`** `(` **`n`** `) +` **`value`** 2655 `if (` **`Xdeco`** `(` **`n`** `) > 4095) then` 2656 **`Xdeco`** `(` **`n`** `) = 4095` 2657 `endif` 2658 `endif` **E.3.4.4 DPCM4 for 12–8–12 Decoder** 2659 **Xenco** ( **n** ) has the following format: 2660 **`Xenco`** `(` **`n`** `) = “001 s xxxx”` 2661 where, 2662 `“001” is the code word` 2663 `“s” is the` **`sign`** `bit` 2664 `“xxxx” is the four bit` **`value`** `field` 2665 The codec equation is described as follows: 2666 **`sign`** `=` **`Xenco`** `(` **`n`** `) & 0x10` 2667 **`value`** `= 8 * (` **`Xenco`** `(` **`n`** `) & 0xf) + 104 + 3` 2668 `if (` **`sign`** `> 0) then` 2669 **`Xdeco`** `(` **`n`** `) =` **`Xpred`** `(` **`n`** `) -` **`value`** 2670 `if (` **`Xdeco`** `(` **`n`** `) < 0) then` 2671 **`Xdeco`** `(` **`n`** `) = 0` 2672 `endif` 2673 `else` 2674 **`Xdeco`** `(` **`n`** `) =` **`Xpred`** `(` **`n`** `) +` **`value`** 2675 `if (` **`Xdeco`** `(` **`n`** `) > 4095)` 2676 **`Xdeco`** `(` **`n`** `) = 4095` 2677 `endif` 2678 `endif` 

**E.3.4.5 DPCM5 for 12–8–12 Decoder** 

2679 **Xenco** ( **n** ) has the following format: 2680 **`Xenco`** `(` **`n`** `) = “0001 s xxx”` 

Copyright © 2005-2014 MIPI Alliance, Inc. 

149 

All rights reserved. **Confidential** 

Specification for CSI-2 

Version 1.3 29-May-2014 

2681 where, 2682 `“0001” is the code word` 2683 `“s” is the` **`sign`** `bit` 2684 `“xxx” is the three bit` **`value`** `field` 2685 The codec equation is described as follows: 2686 **`sign`** `=` **`Xenco`** `(` **`n`** `) & 0x8` 2687 **`value`** `= 16 * (` **`Xenco`** `(` **`n`** `) & 0x7) + 232 + 7` 2688 `if (` **`sign`** `> 0) then` 2689 **`Xdeco`** `(` **`n`** `) =` **`Xpred`** `(` **`n`** `) -` **`value`** 2690 `if (` **`Xdeco`** `(` **`n`** `) < 0) then` 2691 **`Xdeco`** `(` **`n`** `) = 0` 2692 `endif` 2693 `else` 2694 **`Xdeco`** `(` **`n`** `) =` **`Xpred`** `(` **`n`** `) +` **`value`** 2695 `if (` **`Xdeco`** `(` **`n`** `) > 4095) then` 2696 **`Xdeco`** `(` **`n`** `) = 4095` 2697 `endif` 2698 `endif` 

**E.3.4.6 PCM for 12–8–12 Decoder** 

2699 **Xenco** ( **n** ) has the following format: 2700 **`Xenco`** `(` **`n`** `) = “1 xxxxxxx”` 2701 where, 2702 `“1” is the code word` 2703 `the` **`sign`** `bit is not used` 2704 `“xxxxxxx” is the seven bit` **`value`** `field` 2705 The codec equation is described as follows: 2706 **`value`** `= 32 * (` **`Xenco`** `(` **`n`** `) & 0x7f)` 2707 `if (` **`value`** `>` **`Xpred`** `(` **`n`** `)) then` 2708 **`Xdeco`** `(` **`n`** `) =` **`value`** `+ 15` 2709 `else` 2710 **`Xdeco`** `(` **`n`** `) =` **`value`** `+ 16` 2711 `endif` 

**E.3.5 Decoder for 12–7–12 Data Compression** 2712 Pixels without prediction are decoded using the following formula: 2713 **`Xdeco`** `(` **`n`** `) = 32 *` **`Xenco`** `(` **`n`** `) + 16` 2714 Pixels with prediction are decoded using the following formula: 2715 `if (` **`Xenco`** `(` **`n`** `) & 0x78 == 0x00) then` 2716 `use` **`DPCM1`** 2717 `else if (` **`Xenco`** `(` **`n`** `) & 0x78 == 0x08) then` 2718 `use` **`DPCM2`** 2719 `else if (` **`Xenco`** `(` **`n`** `) & 0x78 == 0x10) then` 2720 `use` **`DPCM3`** 2721 `else if (` **`Xenco`** `(` **`n`** `) & 0x70 == 0x20) then` 2722 `use` **`DPCM4`** 2723 `else if (` **`Xenco`** `(` **`n`** `) & 0x70 == 0x30) then` 2724 `use` **`DPCM5`** 2725 `else if (` **`Xenco`** `(` **`n`** `) & 0x78 == 0x18) then` 2726 `use` **`DPCM6`** 2727 `else` 2728 `use` **`PCM`** 2729 `endif` 

Copyright © 2005-2014 MIPI Alliance, Inc. 

150 

All rights reserved. 

**Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

## **E.3.5.1 DPCM1 for 12–7–12 Decoder** 

2730 **Xenco** ( **n** ) has the following format: 2731 **`Xenco`** `(` **`n`** `) = “0000 s xx”` 2732 where, 2733 `“0000” is the code word` 2734 `“s” is the` **`sign`** `bit` 2735 `“xx” is the two bit` **`value`** `field` 2736 The codec equation is described as follows: 2737 **`sign`** `=` **`Xenco`** `(` **`n`** `) & 0x4` 2738 **`value`** `=` **`Xenco`** `(` **`n`** `) & 0x3` 2739 `if (` **`sign`** `> 0) then` 2740 **`Xdeco`** `(` **`n`** `) =` **`Xpred`** `(` **`n`** `) -` **`value`** 2741 `else` 2742 **`Xdeco`** `(` **`n`** `) =` **`Xpred`** `(` **`n`** `) +` **`value`** 2743 `endif` 

## **E.3.5.2 DPCM2 for 12–7–12 Decoder** 

2744 **Xenco** ( **n** ) has the following format: 2745 **`Xenco`** `(` **`n`** `) = “0001 s xx”` 2746 where, 2747 `“0001” is the code word` 2748 `“s” is the` **`sign`** `bit` 2749 `“xx” is the two bit` **`value`** `field` 2750 The codec equation is described as follows: 2751 **`sign`** `=` **`Xenco`** `(` **`n`** `) & 0x4` 2752 **`value`** `= 2 * (` **`Xenco`** `(` **`n`** `) & 0x3) + 4` 2753 `if (` **`sign`** `> 0) then` 2754 **`Xdeco`** `(` **`n`** `) =` **`Xpred`** `(` **`n`** `) -` **`value`** 2755 `else` 2756 **`Xdeco`** `(` **`n`** `) =` **`Xpred`** `(` **`n`** `) +` **`value`** 2757 `endif` 

**E.3.5.3 DPCM3 for 12–7–12 Decoder** 

2758 **Xenco** ( **n** ) has the following format: 2759 **`Xenco`** `(` **`n`** `) = “0010 s xx”` 2760 where, 2761 `“0010” is the code word` 2762 `“s” is the` **`sign`** `bit` 2763 `“xx” is the two bit` **`value`** `field` 2764 The codec equation is described as follows: 2765 **`sign`** `=` **`Xenco`** `(` **`n`** `) & 0x4` 2766 **`value`** `= 4 * (` **`Xenco`** `(` **`n`** `) & 0x3) + 12 + 1` 2767 `if (` **`sign`** `> 0) then` 2768 **`Xdeco`** `(` **`n`** `) =` **`Xpred`** `(` **`n`** `) -` **`value`** 2769 `if (` **`Xdeco`** `(` **`n`** `) < 0) then` 2770 **`Xdeco`** `(` **`n`** `) = 0` 2771 `endif` 2772 `else` 2773 **`Xdeco`** `(` **`n`** `) =` **`Xpred`** `(` **`n`** `) +` **`value`** 2774 `if (` **`Xdeco`** `(` **`n`** `) > 4095) then` 2775 **`Xdeco`** `(` **`n`** `) = 4095` 

Copyright © 2005-2014 MIPI Alliance, Inc. 

151 

All rights reserved. 

**Confidential** 

Specification for CSI-2 

Version 1.3 29-May-2014 

2776 `endif` 2777 `endif` 

**E.3.5.4 DPCM4 for 12–7–12 Decoder** 

2778 **Xenco** ( **n** ) has the following format: 2779 **`Xenco`** `(` **`n`** `) = “010 s xxx”` 2780 where, 2781 `“010” is the code word` 2782 `“s” is the` **`sign`** `bit` 2783 `“xxx” is the three bit` **`value`** `field` 2784 The codec equation is described as follows: 2785 **`sign`** `=` **`Xenco`** `(` **`n`** `) & 0x8` 2786 **`value`** `= 8 * (` **`Xenco`** `(` **`n`** `) & 0x7) + 28 + 3` 2787 `if (` **`sign`** `> 0) then` 2788 **`Xdeco`** `(` **`n`** `) =` **`Xpred`** `(` **`n`** `) -` **`value`** 2789 `if (` **`Xdeco`** `(` **`n`** `) < 0) then` 2790 **`Xdeco`** `(` **`n`** `) = 0` 2791 `endif` 2792 `else` 2793 **`Xdeco`** `(` **`n`** `) =` **`Xpred`** `(` **`n`** `) +` **`value`** 2794 `if (` **`Xdeco`** `(` **`n`** `) > 4095) then` 2795 **`Xdeco`** `(` **`n`** `) = 4095` 2796 `endif` 2797 `endif` 

**E.3.5.5 DPCM5 for 12–7–12 Decoder** 2798 **Xenco** ( **n** ) has the following format: 2799 **`Xenco`** `(` **`n`** `) = “011 s xxx”` 2800 where, 2801 `“011” is the code word` 2802 `“s” is the` **`sign`** `bit` 2803 `“xxx” is the three bit` **`value`** `field` 2804 The codec equation is described as follows: 2805 **`sign`** `=` **`Xenco`** `(` **`n`** `) & 0x8` 2806 **`value`** `= 16 * (` **`Xenco`** `(` **`n`** `) & 0x7) + 92 + 7` 2807 `if (` **`sign`** `> 0) then` 2808 **`Xdeco`** `(` **`n`** `) =` **`Xpred`** `(` **`n`** `) -` **`value`** 2809 `if (` **`Xdeco`** `(` **`n`** `) < 0) then` 2810 **`Xdeco`** `(` **`n`** `) = 0` 2811 `endif` 2812 `else` 2813 **`Xdeco`** `(` **`n`** `) =` **`Xpred`** `(` **`n`** `) +` **`value`** 2814 `if (` **`Xdeco`** `(` **`n`** `) > 4095) then` 2815 **`Xdeco`** `(` **`n`** `) = 4095` 2816 `endif` 2817 `endif` **E.3.5.6 DPCM6 for 12–7–12 Decoder** 2818 **Xenco** ( **n** ) has the following format: 2819 **`Xenco`** `(` **`n`** `) = “0011 s xx”` 2820 where, 

152 Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. 

**Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

2821 `“0011” is the code word` 2822 `“s” is the` **`sign`** `bit` 2823 `“xx” is the two bit` **`value`** `field` 2824 The codec equation is described as follows: 2825 **`sign`** `=` **`Xenco`** `(` **`n`** `) & 0x4` 2826 **`value`** `= 32 * (` **`Xenco`** `(` **`n`** `) & 0x3) + 220 + 15` 2827 `if (` **`sign`** `> 0) then` 2828 **`Xdeco`** `(` **`n`** `) =` **`Xpred`** `(` **`n`** `) -` **`value`** 2829 `if (` **`Xdeco`** `(` **`n`** `) < 0) then` 2830 **`Xdeco`** `(` **`n`** `) = 0` 2831 `endif` 2832 `else` 2833 **`Xdeco`** `(` **`n`** `) =` **`Xpred`** `(` **`n`** `) +` **`value`** 2834 `if (` **`Xdeco`** `(` **`n`** `) > 4095) then` 2835 **`Xdeco`** `(` **`n`** `) = 4095` 2836 `endif` 2837 `endif` 

**E.3.5.7 PCM for 12–7–12 Decoder** 2838 **Xenco** ( **n** ) has the following format: 2839 **`Xenco`** `(` **`n`** `) = “1 xxxxxx”` 2840 where, 2841 `“1” is the code word` 2842 `the` **`sign`** `bit is not used` 2843 `“xxxxxx” is the six bit` **`value`** `field` 2844 The codec equation is described as follows: 2845 **`value`** `= 64 * (` **`Xenco`** `(` **`n`** `) & 0x3f)` 2846 `if (` **`value`** `>` **`Xpred`** `(` **`n`** `)) then` 2847 **`Xdeco`** `(` **`n`** `) =` **`value`** `+ 31` 2848 `else` 2849 **`Xdeco`** `(` **`n`** `) =` **`value`** `+ 32` 2850 `endif` 

**E.3.6 Decoder for 12–6–12 Data Compression** 2851 Pixels without prediction are decoded using the following formula: 2852 **`Xdeco`** `(` **`n`** `) = 64 *` **`Xenco`** `(` **`n`** `) + 32` 2853 Pixels with prediction are decoded using the following formula: 2854 `if (` **`Xenco`** `(` **`n`** `) & 0x3c == 0x00) then` 2855 `use` **`DPCM1`** 2856 `else if (` **`Xenco`** `(` **`n`** `) & 0x3c == 0x04) then` 2857 `use` **`DPCM3`** 2858 `else if (` **`Xenco`** `(` **`n`** `) & 0x38 == 0x10) then` 2859 `use` **`DPCM4`** 2860 `else if (` **`Xenco`** `(` **`n`** `) & 0x3c == 0x08) then` 2861 `use` **`DPCM5`** 2862 `else if (` **`Xenco`** `(` **`n`** `) & 0x38 == 0x18) then` 2863 `use` **`DPCM6`** 2864 `else if (` **`Xenco`** `(` **`n`** `) & 0x3c == 0x0c) then` 2865 `use` **`DPCM7`** 2866 `else` 2867 `use` **`PCM`** 2868 `endif` 2869 _Note:_ _**DPCM2** is not used._ 

Copyright © 2005-2014 MIPI Alliance, Inc. 

153 

All rights reserved. 

**Confidential** 

Specification for CSI-2 

Version 1.3 29-May-2014 

## **E.3.6.1 DPCM1 for 12–6–12 Decoder** 

2870 **Xenco** ( **n** ) has the following format: 2871 **`Xenco`** `(` **`n`** `) = “0000 s x”` 2872 where, 2873 `“0000” is the code word` 2874 `“s” is the` **`sign`** `bit` 2875 `“x” is the one bit` **`value`** `field` 2876 The codec equation is described as follows: 2877 **`sign`** `=` **`Xenco`** `(` **`n`** `) & 0x2` 2878 **`value`** `=` **`Xenco`** `(` **`n`** `) & 0x1` 2879 `if (` **`sign`** `> 0) then` 2880 **`Xdeco`** `(` **`n`** `) =` **`Xpred`** `(` **`n`** `) -` **`value`** 2881 `else` 2882 **`Xdeco`** `(` **`n`** `) =` **`Xpred`** `(` **`n`** `) +` **`value`** 2883 `endif` 

**E.3.6.2 DPCM3 for 12–6–12 Decoder** 

2884 **Xenco** ( **n** ) has the following format: 2885 **`Xenco`** `(` **`n`** `) = “0001 s x”` 2886 where, 2887 `“0001” is the code word` 2888 `“s” is the` **`sign`** `bit` 2889 `“x” is the one bit` **`value`** `field` 2890 The codec equation is described as follows: 2891 **`sign`** `=` **`Xenco`** `(` **`n`** `) & 0x2` 2892 **`value`** `= 4 * (` **`Xenco`** `(` **`n`** `) & 0x1) + 2 + 1` 2893 `if (` **`sign`** `> 0) then` 2894 **`Xdeco`** `(` **`n`** `) =` **`Xpred`** `(` **`n`** `) -` **`value`** 2895 `if (` **`Xdeco`** `(` **`n`** `) < 0) then` 2896 **`Xdeco`** `(` **`n`** `) = 0` 2897 `endif` 2898 `else` 2899 **`Xdeco`** `(` **`n`** `) =` **`Xpred`** `(` **`n`** `) +` **`value`** 2900 `if (` **`Xdeco`** `(` **`n`** `) > 4095) then` 2901 **`Xdeco`** `(` **`n`** `) = 4095` 2902 `endif` 2903 `endif` 

**E.3.6.3 DPCM4 for 12–6–12 Decoder** 2904 **Xenco** ( **n** ) has the following format: 2905 **`Xenco`** `(` **`n`** `) = “010 s xx”` 2906 where, 2907 `“010” is the code word` 2908 `“s” is the` **`sign`** `bit` 2909 `“xx” is the two bit` **`value`** `field` 2910 The codec equation is described as follows: 2911 **`sign`** `=` **`Xenco`** `(` **`n`** `) & 0x4` 2912 **`value`** `= 8 * (` **`Xenco`** `(` **`n`** `) & 0x3) + 10 + 3` 2913 `if (` **`sign`** `> 0) then` 2914 **`Xdeco`** `(` **`n`** `) =` **`Xpred`** `(` **`n`** `) -` **`value`** 2915 `if (` **`Xdeco`** `(` **`n`** `) < 0) then` 154 Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. 

**Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

2916 **`Xdeco`** `(` **`n`** `) = 0` 2917 `endif` 2918 `else` 2919 **`Xdeco`** `(` **`n`** `) =` **`Xpred`** `(` **`n`** `) +` **`value`** 2920 `if (` **`Xdeco`** `(` **`n`** `) > 4095) then` 2921 **`Xdeco`** `(` **`n`** `) = 4095` 2922 `endif` 2923 `endif` 

**E.3.6.4 DPCM5 for 12–6–12 Decoder** 

2924 **Xenco** ( **n** ) has the following format: 2925 **`Xenco`** `(` **`n`** `) = “0010 s x”` 2926 where, 2927 `“0010” is the code word` 2928 `“s” is the` **`sign`** `bit` 2929 `“x” is the one bit` **`value`** `field` 2930 The codec equation is described as follows: 2931 **`sign`** `=` **`Xenco`** `(` **`n`** `) & 0x2` 2932 **`value`** `= 16 * (` **`Xenco`** `(` **`n`** `) & 0x1) + 42 + 7` 2933 `if (` **`sign`** `> 0) then` 2934 **`Xdeco`** `(` **`n`** `) =` **`Xpred`** `(` **`n`** `) -` **`value`** 2935 `if (` **`Xdeco`** `(` **`n`** `) < 0) then` 2936 **`Xdeco`** `(` **`n`** `) = 0` 2937 `endif` 2938 `else` 2939 **`Xdeco`** `(` **`n`** `) =` **`Xpred`** `(` **`n`** `) +` **`value`** 2940 `if (` **`Xdeco`** `(` **`n`** `) > 4095) then` 2941 **`Xdeco`** `(` **`n`** `) = 4095` 2942 `endif` 2943 `endif` 

**E.3.6.5 DPCM6 for 12–6–12 Decoder** 2944 **Xenco** ( **n** ) has the following format: 2945 **`Xenco`** `(` **`n`** `) = “011 s xx”` 2946 where, 2947 `“011” is the code word` 2948 `“s” is the` **`sign`** `bit` 2949 `“xx” is the two bit` **`value`** `field` 2950 The codec equation is described as follows: 2951 **`sign`** `=` **`Xenco`** `(` **`n`** `) & 0x4` 2952 **`value`** `= 32 * (` **`Xenco`** `(` **`n`** `) & 0x3) + 74 + 15` 2953 `if (` **`sign`** `> 0) then` 2954 **`Xdeco`** `(` **`n`** `) =` **`Xpred`** `(` **`n`** `) -` **`value`** 2955 `if (` **`Xdeco`** `(` **`n`** `) < 0) then` 2956 **`Xdeco`** `(` **`n`** `) = 0` 2957 `endif` 2958 `else` 2959 **`Xdeco`** `(` **`n`** `) =` **`Xpred`** `(` **`n`** `) +` **`value`** 2960 `if (` **`Xdeco`** `(` **`n`** `) > 4095) then` 2961 **`Xdeco`** `(` **`n`** `) = 4095` 2962 `endif` 2963 `endif` 

Copyright © 2005-2014 MIPI Alliance, Inc. 

155 

All rights reserved. 

**Confidential** 

Specification for CSI-2 

Version 1.3 29-May-2014 

**E.3.6.6 DPCM7 for 12–6–12 Decoder** 2964 **Xenco** ( **n** ) has the following format: 2965 **`Xenco`** `(` **`n`** `) = “0011 s x”` 2966 where, 2967 `“0011” is the code word` 2968 `“s” is the` **`sign`** `bit` 2969 `“x” is the one bit` **`value`** `field` 2970 The codec equation is described as follows: 2971 **`sign`** `=` **`Xenco`** `(` **`n`** `) & 0x2` 2972 **`value`** `= 64 * (` **`Xenco`** `(` **`n`** `) & 0x1) + 202 + 31` 2973 `if (` **`sign`** `> 0) then` 2974 **`Xdeco`** `(` **`n`** `) =` **`Xpred`** `(` **`n`** `) -` **`value`** 2975 `if (` **`Xdeco`** `(` **`n`** `) < 0) then` 2976 **`Xdeco`** `(` **`n`** `) = 0` 2977 `endif` 2978 `else` 2979 **`Xdeco`** `(` **`n`** `) =` **`Xpred`** `(` **`n`** `) +` **`value`** 2980 `if (` **`Xdeco`** `(` **`n`** `) > 4095) then` 2981 **`Xdeco`** `(` **`n`** `) = 4095` 2982 `endif` 2983 `endif` 

**E.3.6.7 PCM for 12–6–12 Decoder** 2984 **Xenco** ( **n** ) has the following format: 2985 **`Xenco`** `(` **`n`** `) = “1 xxxxx”` 2986 where, 2987 `“1” is the code word` 2988 `the` **`sign`** `bit is not used` 2989 `“xxxxx” is the five bit` **`value`** `field` 2990 The codec equation is described as follows: 2991 **`value`** `= 128 * (` **`Xenco`** `(` **`n`** `) & 0x1f)` 2992 `if (` **`value`** `>` **`Xpred`** `(` **`n`** `)) then` 2993 **`Xdeco`** `(` **`n`** `) =` **`value`** `+ 63` 2994 `else` 2995 **`Xdeco`** `(` **`n`** `) =` **`value`** `+ 64` 2996 `endif` 

156 

Copyright © 2005-2014 MIPI Alliance, Inc. 

All rights reserved. 

**Confidential** 

Version 1.3 29-May-2014 

Specification for CSI-2 

## **Annex F JPEG Interleaving (informative)** 

2997 This annex illustrates how the standard features of the CSI-2 protocol should be used to interleave 2998 (multiplex) JPEG image data with other types of image data, e.g. RGB565 or YUV422, without requiring a 2999 custom JPEG format such as JPEG8. 

3000 The Virtual Channel Identifier and Data Type value in the CSI-2 Packet Header provide simple methods of 3001 interleaving multiple data streams or image data types at the packet level. Interleaving at the packet level 3002 minimizes the amount of buffering required in the system. 

3003 The Data Type value in the CSI-2 Packet Header should be used to multiplex different image data types at 3004 the CSI-2 transmitter and de-multiplex the data types at the CSI-2 receiver. 

3005 The Virtual Channel Identifier in the CSI-2 Packet Header should be used to multiplex different data 3006 streams (channels) at the CSI-2 transmitter and de-multiplex the streams at the CSI-2 receiver. 

3007 

3007 The main difference between the two interleaving methods is that images with different Data Type values 3008 within the same Virtual Channel use the same frame and line synchronization information, whereas 3009 multiple Virtual Channels (data streams) each have their own independent frame and line synchronization 3010 information and thus potentially each channel may have different frame rates. 

3011 Since the predefined Data Type values represent only YUV, RGB and RAW data types, one of the User 3012 Defined Data Type values should be used to represent JPEG image data. 

3013 

Figure 156 illustrates interleaving JPEG image data with YUV422 image data using Data Type values. 

3014 Figure 157 illustrates interleaving JPEG image data with YUV422 image data using both Data Type values 3015 and Virtual Channel Identifiers. 

**==> picture [462 x 202] intentionally omitted <==**

**----- Start of picture text -----**<br>
Frame Start Packet YUV422 Data Type User Defined Data Type<br>LPS SoT FS EoT LPS SoT PH YUV422 Data PF EoT LPS SoT PH JPEG Data PF EoT<br>YUV422 Data Type YUV422 Data Type User Defined Data Type<br>LPS SoT PH YUV422 Data PF EoT LPS SoT PH YUV422 Data PF EoT LPS SoT PH JPEG Data PF EoT<br>YUV422 Data Type User Defined Data Type Frame End Packet<br>LPS SoT PH YUV422 Data PF EoT LPS SoT PH JPEG Data PF EoT LPS SoT FE EoT LPS<br>KEY :<br>LPS – Low Power State PH – Packet Header FS – Frame Start Packet<br>SoT – Start of Transmission PF – Packet Footer FE – Frame End Packet<br>EoT – End of Transmission<br>3016<br>**----- End of picture text -----**<br>


**Figure 156 Data Type Interleaving: Concurrent JPEG and YUV Image Data** 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

157 

Specification for CSI-2 

Version 1.3 

29-May-2014 

**==> picture [454 x 206] intentionally omitted <==**

**----- Start of picture text -----**<br>
Virtual Channel 0 Virtual Channel 0 Virtual Channel 1 Virtual Channel 1<br>Frame Start Packet User Defined Data Type Frame Start Packet YUV422 Data Type<br>SoT FS EoT LPS SoT PH JPEG Data PF EoT LPS SoT FS EoT LPS SoT PH YUV422 Data PF EoT<br>Virtual Channel 0 Virtual Channel 1 Virtual Channel 0<br>User Defined Data Type YUV422 Data Type User Defined Data Type<br>LPS SoT PH JPEG Data PF EoT LPS SoT PH YUV422 Data PF EoT LPS SoT PH JPEG Data PF EoT<br>Virtual Channel 1 Virtual Channel 1 Virtual Channel 0 Virtual Channel 0<br>YUV422 Data Type Frame End Packet User Defined Data Type Frame End Packet<br>LPS SoT PH YUV422 Data PF EoT LPS SoT FE EoT LPS SoT PH JPEG Data PF EoT LPS SoT FE EoT<br>KEY :<br>LPS – Low Power State PH – Packet Header FS – Frame Start Packet<br>SoT – Start of Transmission PF – Packet Footer FE – Frame End Packet<br>EoT – End of Transmission<br>3017<br>**----- End of picture text -----**<br>


## **Figure 157 Virtual Channel Interleaving: Concurrent JPEG and YUV Image Data** 

3018 Both Figure 156 and Figure 157 can be similarly extended to the interleaving of JPEG image data with any 3019 other type of image data, e.g. RGB565. 

- 3020 Figure 158 illustrates the use of Virtual Channels to support three different JPEG interleaving usage cases: 

- 3021 • Concurrent JPEG and YUV422 image data. 

- 3022 • Alternating JPEG and YUV422 output - one frame JPEG, then one frame YUV 

- 3023 • Streaming YUV22 with occasional JPEG for still capture 

3024 Again, these examples could also represent interleaving JPEG data with any other image data type. 

158 

Copyright © 2005-2014 MIPI Alliance, Inc. 

All rights reserved. 

**Confidential** 

Version 1.3 

Specification for CSI-2 

29-May-2014 

## **Use Case 1: Concurrent JPEG output with YUV data** 

|Packe<br>CSI-2 TX<br>JPEG<br>Frame<br>YUV<br>Frame<br>JPEG<br>Frame<br>YUV<br>Frame<br>JPEG<br>Frame<br>YUV<br>Frame<br>JPEG<br>Frame<br>YUV<br>Frame<br>**Y**<br>**J**<br>**Y**<br>**J**<br>VC0<br>VC1|Packe<br>CSI-2 TX<br>JPEG<br>Frame<br>YUV<br>Frame<br>JPEG<br>Frame<br>YUV<br>Frame<br>JPEG<br>Frame<br>YUV<br>Frame<br>JPEG<br>Frame<br>YUV<br>Frame<br>**Y**<br>**J**<br>**Y**<br>**J**<br>VC0<br>VC1|JPEG<br>Frame||JPEG<br>Frame||JPEG<br>Frame||JPEG<br>Frame||2 TX|**Y**<br>**J**<br>**Y**<br>**J**|**Y**<br>**J**<br>**Y**<br>**J**|**Y**<br>**J**<br>**Y**<br>**J**<br>1 Frame|**Y**<br>**J**<br>**Y**<br>**J**<br>1 Frame|**Y**<br>**J**<br>**Y**<br>**J**|2 RX||JPEG<br>Frame||JPEG<br>Frame||JPEG<br>Frame||JPEG<br>Frame|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|||YUV<br>Frame||YUV<br>Frame||YUV<br>Frame||YUV<br>Frame||CSI-|Packe<br><br><br><br>||||G and<br><br><br><br>|CSI-||YUV<br>Frame||YUV<br>Frame||YUV<br>Frame||YUV<br>Frame|
||||||||||||||t interlea<br>YUV|ved JPE<br>data|||||||||||
||||||||||||||||||||||||||
||||||||||||||||||||||||||
|**se Case 2: Alternating JPEG  and YUV output –**|||||||||||||**one fra**|**me JPE**|||||||||||
|CSI-2 TX<br>YUV<br>Frame<br>YUV<br>Frame<br>JPEG<br>Frame<br>JPEG<br>Frame<br>**YUV**<br>VC0<br>VC1<br>CSI-2<br>Cha<br>codes|||||||||||||||||||||||||
|||||JPEG<br>Frame||||JPEG<br>Frame||2 TX|**YUV**||**JPEG**|**YUV**|**JPEG**|2 RX||||JPEG<br>Frame||||JPEG<br>Frame|
|||YUV<br>Frame||||YUV<br>Frame||||CSI-|CSI-2<br>Cha||RX use<br>nnel and<br>|s the Virt<br>Data Ty<br>|ual<br>pe<br>|CSI-||YUV<br>Frame||||YUV<br>Frame|||
||<br>codes||||||||||||<br>to de-m|<br>ultiplex d|<br>ata||||||||||
||||||||||||||||||||||||||
|**se Case 3: Streaming YUV with occasional JPE**|||||||||||||**G still c**|**apture**|||||||||||
|CSI-2 TX<br>YUV<br>Frame<br>JPEG<br>Frame<br>YUV<br>Frame<br>YUV<br>Frame<br>VC0<br>VC1<br>**YUV**|||||||||||||||||||||||||
|||||||||||2 TX|**YUV**||||**YUV**|2 RX|||||||||
|||||||||||||**YUV**|**YUV**|**JPEG**|**YUV**||||||||||
|||YUV<br>Frame||YUV<br>Frame||||YUV<br>Frame||CSI-||||||CSI-||YUV<br>Frame||YUV<br>Frame||||YUV<br>Frame|



## **Use Case 2: Alternating JPEG  and YUV output – one frame JPEG, then one frame YUV** 

## **Use Case 3: Streaming YUV with occasional JPEG still capture** 

3025 

**Figure 158 Example JPEG and YUV Interleaving Use Cases** 

Copyright © 2005-2014 MIPI Alliance, Inc. All rights reserved. **Confidential** 

159 

