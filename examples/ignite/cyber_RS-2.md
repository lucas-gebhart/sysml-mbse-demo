# Cyber resiliency gap analysis — RS-2 Adversary flies AV to adversary selected location

Model: `Berserker Cyber Res. Model` (77408 elements from 9 project(s); missing: MI Style Guide.mdzip)  
Command: `python -m sysml_demo cyber "Berserker Cyber Res. Model.mdzip" --federate`  
Coverage threshold: proposals below **medium** confidence are listed but not counted as coverage.

> Everything in the *STPA-Sec chain* and *requirement (direct / allocation)* columns is read from model relationships. ATT&CK, D3FEND, lexical-requirement and NIST lines are **heuristic proposals** with a confidence and a rationale; none of them exists in the model.

## Summary

| leaves | with cyber requirement | with D3FEND countermeasure | both | neither |
|---|---|---|---|---|
| 18 | 6 | 17 | 5 | 0 |

D3FEND stereotypes applied to non-D3FEND (Berserker) elements: **0** — the D3FEND profile is mounted but unused.

## STPA-Sec chain

- Risk scenario: **RS-2 Adversary flies AV to adversary selected location** (12 loss scenarios roll up to it)
- Attack tree: **R2 - Adversary flies AV to adversary selected location** ← And ← R2 - Adversary Flies AV to Selected Location Probability of Attack Success; EML: Mission_Impact_High=1.0, Mission_Impact_Low=0.9, Percent_Systems_Impacted_High=0.15, Percent_Systems_Impacted_Low=0.05, Probability_of_Adv__Attack_High=1.0, Probability_of_Adv__Attack_Low=0.95
- Losses: L-1 Loss of life or injury to friendly or neutral people; L-2 Significant damage to friendly or neutral objects; L-3 Unable to destroy assigned targets; L-4 Unable to decoy hostile air defenses when required
- Hazards: H-1 MQ-99 targets friendly or neutral objects or personnel; H-2 MQ-99 employs weapons too close to friendly or neutral objects or personnel; H-3 MQ-99 does not successfully strike assigned targets; H-4 MQ-99 does not fly required profile to stimulate desired hostile defense response; H-5 MQ-99 operates outside of established operational envelope; H-6 MQ-99 presents electrical, chemical, or kinetic hazards to friendly personnel or objects in the vehicle’s immediate vicinity
- Security constraints: SC-1 The MQ-99 will only target hostile objects or personnel; SC-2 The MQ-99 will prevent unacceptable collateral damage to friendly or neutral objects or personnel; SC-3 MQ-99 must successfully strike assigned targets; SC-4 MQ-99 must execute the required profile as directed by warfighters in accordance with CONOPS and mission timelines; SC-5 The MQ-99 will only operate inside the established operational envelope; SC-6 The MQ-99 will not present electrical, chemical, or kinetic hazards to friendly personnel or objects in the vehicle’s immediate vicinity
- Controllers (11): C-2 Operator, C-3 Flight Lead, C-4 Ground Control Station, C-5 Maintenance System, C-7 Mission Computer, C-8 Autopilot, C-9 Flight Control Computer, C-10 Navigation Controller, C-11 Communications Controller, C-15 Stores Controller, C-30 Cyber Sentinel
- Hazardous control actions: 166; controller constraints: 90

```text
RS-2  Adversary flies AV to adversary selected location
│  loss scenarios 12 → HCAs 166 → hazards 6 → losses 4   controllers 11   security constraints 6
│  Loss   L-1 Loss of life or injury to friendly or neutral people
│  Loss   L-2 Significant damage to friendly or neutral objects
│  Loss   L-3 Unable to destroy assigned targets
│  Loss   L-4 Unable to decoy hostile air defenses when required
│  Hazard H-1 MQ-99 targets friendly or neutral objects or personnel   mitigated by SC-1
│  Hazard H-2 MQ-99 employs weapons too close to friendly or neutral objects or personnel   mitigated by SC-2
│  Hazard H-3 MQ-99 does not successfully strike assigned targets   mitigated by SC-3
│  Hazard H-4 MQ-99 does not fly required profile to stimulate desired hostile defense response   mitigated by SC-4
│  Hazard H-5 MQ-99 operates outside of established operational envelope   mitigated by SC-5
│  Hazard H-6 MQ-99 presents electrical, chemical, or kinetic hazards to friendly personnel or obje…   mitigated by SC-6
│  Controllers: C-2 Operator, C-3 Flight Lead, C-4 Ground Control Station, C-5 Maintenance System, C-7 Mission Computer, C-8 Autopilot, C-9 Flight Control Computer, C-10 Navigation Controller, C-11 Communications Controller, C-15 Stores Controller …
│  EML: Mission_Impact_High=1.0, Mission_Impact_Low=0.9, Percent_Systems_Impacted_High=0.15, Percent_Systems_Impacted_Low=0.05, Probability_of_Adv__Attack_High=1.0, Probability_of_Adv__Attack_Low=0.95
│
├─ [And] R2 - Adversary Flies AV to Selected Location Probability of Attack Success  <<Probability_of_Attack_Success>>
│  ├─ [Or] Adversary successfully spoofs nav solution to fly AV to adversary selected location
│  │  ├─ [Or] ● MIL GPS spoofing to fly AV to adversary selected location                      P=0.001–0.02 sens=0.005893 [·D]
│  │  └─ [Or] ● Other NAV sensor spoofing to fly AV to adversary selected location             P=0.005–0.05 sens=0.015775 [·D]
│  ├─ [Or] Device on 1553 bus sends adversary spoofed message to fly AV to adversary selected location
│  │  ├─ [And] ● Adversary control of device on 1553 bus via supply chain to fly AV to adversar P=0.0001–0.05 sens=0.018931 [·D]
│  │  └─ [And] ● Device on 1553 bus successfully sends adversary spoofed message to fly AV to a P=0.18–0.43 sens=0.008393 [·D]
│  └─ [Or] Adversary sends malicious commands to AV to fly AV to adversary selected location
│     ├─ [Or] Adversary gains control of ground station to fly AV to adversary selected location
│     │  ├─ [Or] ● Adversary supply chain attack on logistics system provides logical access to f P=0.0001–0.001 sens=0.000657 [·D]
│     │  ├─ [Or] ● SIPR connected Traditional-IT cyber attack on ground station to fly AV to adve P=0.01–0.15 sens=0.147437 [·D]
│     │  └─ [Or] ● Operator insider gains access to ground station to fly AV to adversary selecte P=0.0002–0.002 sens=0.003412 [·D]
│     └─ [Or] Adversary gets into the middle of ground station & UAS communications link to fly AV to adversary selected location
│        ├─ [Or] ● Adversary gets link to shift into unencrypted mode to fly AV to adversary sele P=0.0–0.001 sens=0.000835 [R·]
│        └─ [Or] Adversary gets encryption key to fly AV to adversary selected location
│           ├─ [Or] ● Adversary gets insider to give them the command link key to fly AV to adversar P=5e-05–0.0005 sens=0.000459 [·D]
│           ├─ [Or] ● Adversary steals key from SIPR connected ground station to fly AV to adversary P=0.01–0.1 sens=0.031985 [·D]
│           └─ [Or] ● Adversary breaks encryption to determine the command link key to fly UAS to ad P=0.001–0.04 sens=0.020969 [RD]
├─ leaves reached from this scenario's loss scenarios but sitting in other trees:
│  ● SIPR connected DoS cyber attack to degrade UAS operations                      P=0.02–0.2 sens=0 [·D]
│  ● Adversary maliciously modifies flight-critical software during distribution to P=0.02–0.15 sens=0.00845 [RD]
│  ● Adversary substitutes flight-critical hardware during distribution to alter AV P=0.01–0.15 sens=0.003858 [RD]
│  ● SIPR connected Traditional-IT cyber attack on ground station to gain mission p P=0.01–0.15 sens=0.147437 [·D]
│  ● SIPR connected Traditional-IT cyber attack to employ ordnance on a target of t P=0.01–0.15 sens=0.147437 [·D]
│  ● Adversary maliciously modifies flight-critical software during development to  P=0.01–0.12 sens=0.005746 [RD]
│  ● Adversary supply chain attack on MX system provides logical access to maliciou P=0.0001–0.001 sens=0.000799 [RD]
│
└─ coverage @≥medium: 18 leaves (11 in this tree) — requirement 6 (of which 0 by a direct model relationship), D3FEND countermeasure 17, both 5, neither 0
```

## Leaf gap table (ranked by P(success) × no-requirement × no-countermeasure)

| # | status | leaf | P(success) 90% CI | sensitivity | loss scenario | cyber requirement(s) | ATT&CK (confidence) | D3FEND countermeasure (confidence) |
|---|---|---|---|---|---|---|---|---|
| 1 | countermeasure-only | Device on 1553 bus successfully sends adversary spoofed message to fly AV to adversary selected location | 0.18–0.43 | 0.008393 | LS-61 | **GAP** | Masquerading:T1036 [medium]<br/>Adversary-in-the-Middle:T1557 [medium]<br/>Email Spoofing:T1672 [low] | Client-server Payload Profiling (Detect) [medium]<br/>Network Isolation (Isolate) [medium]<br/>Network Traffic Analysis (Detect) [medium]<br/>Network Traffic Community Deviation (Detect) [medium] |
| 2 | countermeasure-only | SIPR connected DoS cyber attack to degrade UAS operations | 0.02–0.2 | 0.0 | LS-6 | **GAP** | External Remote Services:T1133 [medium]<br/>Exploit Public-Facing Application:T1190 [medium]<br/>Network Denial of Service:T1498 [medium] | Application Hardening (Harden) [medium]<br/>Client-server Payload Profiling (Detect) [medium]<br/>Database Query String Analysis (Detect) [medium]<br/>Inbound Session Volume Analysis (Detect) [medium] |
| 3 | countermeasure-only | SIPR connected Traditional-IT cyber attack on ground station to fly AV to adversary selected location | 0.01–0.15 | 0.147437 | LS-1 | **GAP** | External Remote Services:T1133 [medium]<br/>Exploit Public-Facing Application:T1190 [medium]<br/>Data Manipulation:T1565 [medium] | Application Hardening (Harden) [medium]<br/>Client-server Payload Profiling (Detect) [medium]<br/>Database Query String Analysis (Detect) [medium]<br/>Inbound Session Volume Analysis (Detect) [medium] |
| 4 | countermeasure-only | SIPR connected Traditional-IT cyber attack on ground station to gain mission planning and AV location data | 0.01–0.15 | 0.147437 | LS-7 | **GAP** | External Remote Services:T1133 [medium]<br/>Exploit Public-Facing Application:T1190 [medium] | Application Hardening (Harden) [medium]<br/>Client-server Payload Profiling (Detect) [medium]<br/>Database Query String Analysis (Detect) [medium]<br/>Inbound Session Volume Analysis (Detect) [medium] |
| 5 | countermeasure-only | SIPR connected Traditional-IT cyber attack to employ ordnance on a target of their choice | 0.01–0.15 | 0.147437 | LS-5 | **GAP** | External Remote Services:T1133 [medium]<br/>Exploit Public-Facing Application:T1190 [medium]<br/>Link Target:T1608.005 [low] | Application Hardening (Harden) [medium]<br/>Client-server Payload Profiling (Detect) [medium]<br/>Database Query String Analysis (Detect) [medium]<br/>Inbound Session Volume Analysis (Detect) [medium] |
| 6 | countermeasure-only | Adversary steals key from SIPR connected ground station to fly AV to adversary selected location | 0.01–0.1 | 0.031985 | LS-62 | **GAP** | Private Keys:T1552.004 [medium] | Access Mediation (Isolate) [medium]<br/>Agent Authentication (Harden) [medium]<br/>Authentication Cache Invalidation (Evict) [medium]<br/>Certificate Rotation (Harden) [medium] |
| 7 | countermeasure-only | Other NAV sensor spoofing to fly AV to adversary selected location | 0.005–0.05 | 0.015775 | LS-34 | **GAP** | Masquerading:T1036 [medium]<br/>Adversary-in-the-Middle:T1557 [medium]<br/>Email Spoofing:T1672 [low] | Client-server Payload Profiling (Detect) [medium]<br/>Network Isolation (Isolate) [medium]<br/>Network Traffic Analysis (Detect) [medium]<br/>Network Traffic Community Deviation (Detect) [medium] |
| 8 | countermeasure-only | Adversary control of device on 1553 bus via supply chain to fly AV to adversary selected location | 0.0001–0.05 | 0.018931 | LS-60 | **GAP** | Supply Chain Compromise:T1195 [medium]<br/>Compromise Software Supply Chain:T1195.002 [medium]<br/>Compromise Hardware Supply Chain:T1195.003 [low] | Asset Inventory (Model) [medium]<br/>Asset Vulnerability Enumeration (Model) [medium]<br/>Container Image Analysis (Model) [medium]<br/>Platform Hardening (Harden) [medium] |
| 9 | countermeasure-only | MIL GPS spoofing to fly AV to adversary selected location | 0.001–0.02 | 0.005893 | LS-33 | **GAP** | Masquerading:T1036 [medium]<br/>Adversary-in-the-Middle:T1557 [medium]<br/>Email Spoofing:T1672 [low] | Client-server Payload Profiling (Detect) [medium]<br/>Network Isolation (Isolate) [medium]<br/>Network Traffic Analysis (Detect) [medium]<br/>Network Traffic Community Deviation (Detect) [medium] |
| 10 | countermeasure-only | Operator insider gains access to ground station to fly AV to adversary selected location | 0.0002–0.002 | 0.003412 | LS-2 | **GAP** | Valid Accounts:T1078 [medium]<br/>Data Manipulation:T1565 [medium] | Access Modeling (Model) [medium]<br/>Access Policy Administration (Isolate) [medium]<br/>Account Locking (Evict) [medium]<br/>Agent Authentication (Harden) [medium] |
| 11 | countermeasure-only | Adversary supply chain attack on logistics system provides logical access to fly UAS to adversary selected location | 0.0001–0.001 | 0.000657 | LS-37 | **GAP** | Supply Chain Compromise:T1195 [medium]<br/>Valid Accounts:T1078 [medium]<br/>External Remote Services:T1133 [medium] | Access Modeling (Model) [medium]<br/>Access Policy Administration (Isolate) [medium]<br/>Account Locking (Evict) [medium]<br/>Agent Authentication (Harden) [medium] |
| 12 | requirement-only | Adversary gets link to shift into unencrypted mode to fly AV to adversary selected location | 0.0–0.001 | 0.000835 | LS-11 | MR - 26.1.1.14/1.1.1.14 Communications System Cryptographic  [medium]<br/>MR - 26.1.6/1.1.6 Communications Encryption [medium]<br/>MR - 26.2.1.3.1/1.2.1.3.1 Navigation System Backup Mode Swit [medium]<br/>MR - 26.2.1.7.1/1.2.1.7.1 Communications System Backup Mode  [medium] | Impair Defenses:T1562 [medium]<br/>Weaken Encryption:T1600 [medium]<br/>Data Encrypted:T1022 [low] | **GAP** |
| 13 | countermeasure-only | Adversary gets insider to give them the command link key to fly AV to adversary selected location | 5e-05–0.0005 | 0.000459 | LS-59 | **GAP** | Valid Accounts:T1078 [medium]<br/>Private Keys:T1552.004 [medium]<br/>Adversary-in-the-Middle:T1557 [medium] | Agent Authentication (Harden) [medium]<br/>Credential Eviction (Evict) [medium]<br/>Credential Hardening (Harden) [medium]<br/>Multi-factor Authentication (Harden) [medium] |
| 14 | both | Adversary maliciously modifies flight-critical software during distribution to modify AV mission computer | 0.02–0.15 | 0.00845 | LS-15 | MR - 26.1.1.1/1.1.1.1 Mission Computer Secure Boot [medium]<br/>MR - 26.1.1.2/1.1.1.2 Flight Control system Secure Boot [medium]<br/>MR - 26.1.1.8/1.1.1.8 Mission Computer Cryptographic Module [medium]<br/>MR - 26.1.1.9/1.1.1.9 Flight Control System Cryptographic Mo [medium] | Compromise Hardware Supply Chain:T1195.003 [medium]<br/>Compromise Software Supply Chain:T1195.002 [medium]<br/>Supply Chain Compromise:T1195 [medium] | Asset Inventory (Model) [medium]<br/>Asset Vulnerability Enumeration (Model) [medium]<br/>Container Image Analysis (Model) [medium]<br/>Hardware Component Inventory (Model) [medium] |
| 15 | both | Adversary substitutes flight-critical hardware during distribution to alter AV navigation system | 0.01–0.15 | 0.003858 | LS-25 | MR - 26.1.1.10/1.1.1.10 Navigation System Cryptographic Modu [medium]<br/>MR - 26.1.1.3/1.1.1.3 Navigation System Secure Boot [medium]<br/>MR - 26.1.1/1.1.1 Flight Critical Hardware Assurance [medium]<br/>MR - 26.2.1.3.1/1.2.1.3.1 Navigation System Backup Mode Swit [medium] | Compromise Hardware Supply Chain:T1195.003 [medium]<br/>Masquerading:T1036 [medium]<br/>Supply Chain Compromise:T1195 [medium] | Asset Inventory (Model) [medium]<br/>Hardware Component Inventory (Model) [medium] |
| 16 | both | Adversary maliciously modifies flight-critical software during development to alter AV mission computer | 0.01–0.12 | 0.005746 | LS-16 | MR - 26.1.1/1.1.1 Flight Critical Hardware Assurance [medium]<br/>MR - 26.2.1.1.1/1.2.1.1.1 Mission Computer Backup Mode Switc [medium]<br/>MR - 26.2.1/1.2.1 Flight Critical Subsystem Backup Mode [medium]<br/>MR - 26.4.1.1/1.4.1.1 Software Loading [medium] | Masquerading:T1036 [medium]<br/>Adversary-in-the-Middle:T1557 [medium]<br/>Software:T1592.002 [low] | Client-server Payload Profiling (Detect) [medium]<br/>Network Isolation (Isolate) [medium]<br/>Network Traffic Analysis (Detect) [medium]<br/>Network Traffic Community Deviation (Detect) [medium] |
| 17 | both | Adversary breaks encryption to determine the command link key to fly UAS to adversary selected location | 0.001–0.04 | 0.020969 | LS-8 | MR - 26.1.1.10/1.1.1.10 Navigation System Cryptographic Modu [medium]<br/>MR - 26.1.1.14/1.1.1.14 Communications System Cryptographic  [medium]<br/>MR - 26.1.1.8/1.1.1.8 Mission Computer Cryptographic Module [medium] | Data Encrypted:T1022 [medium]<br/>Private Keys:T1552.004 [medium]<br/>Adversary-in-the-Middle:T1557 [medium] | User Behavior Analysis (Detect) [medium]<br/>Access Mediation (Isolate) [medium]<br/>Agent Authentication (Harden) [medium]<br/>Authentication Cache Invalidation (Evict) [medium] |
| 18 | both | Adversary supply chain attack on MX system provides logical access to maliciously alter AV mission computer | 0.0001–0.001 | 0.000799 | LS-14 | MR - 26.1.1.1/1.1.1.1 Mission Computer Secure Boot [medium]<br/>MR - 26.1.1.15/1.1.1.15 Mission Computer Maintenance Ports [medium]<br/>MR - 26.1.1.8/1.1.1.8 Mission Computer Cryptographic Module [medium]<br/>MR - 26.1.1/1.1.1 Flight Critical Hardware Assurance [medium] | Compromise Hardware Supply Chain:T1195.003 [medium]<br/>Compromise Software Supply Chain:T1195.002 [medium]<br/>Masquerading:T1036 [medium] | Asset Inventory (Model) [medium]<br/>Asset Vulnerability Enumeration (Model) [medium]<br/>Container Image Analysis (Model) [medium]<br/>Hardware Component Inventory (Model) [medium] |

## Leaf details

### 1. Device on 1553 bus successfully sends adversary spoofed message to fly AV to adversary selected location

- P=0.18–0.43, TotalRiskSensitivity=0.008393, gate path: Or Device on 1553 bus sends adversary spoofed message to fly AV to adversary selected location
- Loss scenario(s): LS-61 Device on 1553 bus successfully sends adversary spoofed message to fly AV to adversary selected location
- HCAs: HCA-122, HCA-21, HCA-40, HCA-55, HCA-126; hazards: H-1, H-2, H-3, H-4; losses: L-1, L-2, L-3, L-4
- Controllers: C-7 Mission Computer, C-2 Operator, C-8 Autopilot
- Requirements (159 further non-cyber requirements share the same allocation paths):
  - [low] **MR - 26.1.1.1/1.1.1.1 Mission Computer Secure Boot** — allocation: LS-61 traces to function 'Set New Flight Path' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.10/1.1.1.10 Navigation System Cryptographic Module** — allocation: LS-61 traces to function 'Set New Flight Path' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.15/1.1.1.15 Mission Computer Maintenance Ports** — allocation: LS-61 traces to function 'Set New Flight Path' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.16/1.1.1.16 Flight Control System Maintenance Ports** — allocation: LS-61 traces to function 'Set New Flight Path' allocated to block 'Flight Controlller'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.17/1.1.1.17 Navigation System Maintenance Ports** — allocation: LS-61 traces to function 'Set New Flight Path' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.2/1.1.1.2 Flight Control system Secure Boot** — allocation: LS-61 traces to function 'Set New Flight Path' allocated to block 'Flight Controlller'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.3/1.1.1.3 Navigation System Secure Boot** — allocation: LS-61 traces to function 'Set New Flight Path' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.8/1.1.1.8 Mission Computer Cryptographic Module** — allocation: LS-61 traces to function 'Set New Flight Path' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.9/1.1.1.9 Flight Control System Cryptographic Module** — allocation: LS-61 traces to function 'Set New Flight Path' allocated to block 'Flight Controlller'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1/1.1.1 Flight Critical Hardware Assurance** — allocation: LS-61 traces to function 'Conduct Waypoint Communications' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.1.1/1.2.1.1.1 Mission Computer Backup Mode Switching** — allocation: LS-61 traces to function 'Set New Flight Path' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.1/1.2.1.1 Mission Computer Backup Mode** — allocation: LS-61 traces to function 'Set New Flight Path' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.2.1/1.2.1.2.1 Flight Control System Backup Mode Switching** — allocation: LS-61 traces to function 'Set New Flight Path' allocated to block 'Flight Controlller'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.2/1.2.1.2 Flight Control System Backup Mode** — allocation: LS-61 traces to function 'Set New Flight Path' allocated to block 'Flight Controlller'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.3.1/1.2.1.3.1 Navigation System Backup Mode Switching** — allocation: LS-61 traces to function 'Set New Flight Path' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.3/1.2.1.3 Navigation System Backup Mode** — allocation: LS-61 traces to function 'Set New Flight Path' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1/1.2.1 Flight Critical Subsystem Backup Mode** — allocation: LS-61 traces to function 'Conduct Waypoint Communications' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.2/1.2.2 Communications Loss Response** — allocation: LS-61 traces to function 'Set New Flight Path' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.4.1/1.2.4.1 ELINT Sensors on when Needed** — allocation: LS-61 traces to function 'Set New Flight Path' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.4/1.2.4 Mission Critical Subsystem Resilience** — allocation: LS-61 traces to function 'Conduct Waypoint Communications' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.3.4/1.3.4 System Zeroize** — allocation: LS-61 traces to function 'Conduct Waypoint Communications' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.4.1.1/1.4.1.1 Software Loading** — allocation: LS-61 traces to function 'Conduct Waypoint Communications' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.4.1.2/1.4.1.2 Software Loading Switch** — allocation: LS-61 traces to function 'Conduct Waypoint Communications' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.4.1/1.4.1 Single Maintenance Port** — allocation: LS-61 traces to function 'Conduct Waypoint Communications' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 29/59 HT-3 Report Unauthorized Data Detection** — allocation: LS-61 traces to function 'Conduct Waypoint Communications' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
- ATT&CK techniques (heuristic):
  - [medium 0.6] **Masquerading:T1036** — curated hint in cyber.py: phrase 'spoof' → T1036 (heuristic)
  - [medium 0.6] **Adversary-in-the-Middle:T1557** — curated hint in cyber.py: phrase 'spoof' → T1557 (heuristic)
  - [low 0.53] **Email Spoofing:T1672** — name tokens ['spoof'] overlap
- D3FEND countermeasures (heuristic, via D3FEND associations):
  - [medium] **Client-server Payload Profiling** (Detect, direct) — D3FEND: 'Client-server Payload Profiling' May Detect T1557
  - [medium] **Network Isolation** (Isolate, direct) — D3FEND: 'Network Isolation' May Isolate T1557
  - [medium] **Network Traffic Analysis** (Detect, direct) — D3FEND: 'Network Traffic Analysis' May Detect T1557
  - [medium] **Network Traffic Community Deviation** (Detect, direct) — D3FEND: 'Network Traffic Community Deviation' May Detect T1557
  - [medium] **Network Traffic Filtering** (Isolate, direct) — D3FEND: 'Network Traffic Filtering' May Isolate T1557
  - [medium] **Network Traffic Signature Analysis** (Detect, direct) — D3FEND: 'Network Traffic Signature Analysis' May Detect T1557
- D3FEND artifacts the Allocated Baseline already traces to on this path (model Trace links): Actuator (1), Bus Message (1), Bus Network (1), Bus Network Frame (1), Bus Network Traffic (1), Call Stack (1), Central Processing Unit (1), Client Computer (1) from block(s) Allocated Flight Control Computer
- Candidate NIST SP 800-53r5 controls: AC-4, AU-6, SC-32, SC-7, SC-7(21), SC-7(5), SI-3, SI-4, SI-4(11), SI-4(4)

### 2. SIPR connected DoS cyber attack to degrade UAS operations

- P=0.02–0.2, TotalRiskSensitivity=0.0, gate path: (linked from LS-6, outside the tree)
- Loss scenario(s): LS-6 Adversary gains access to the ground station through a traditional-IT data connection and sends malicious waypoint data to degrade UAS operations
- HCAs: HCA-40, HCA-9, HCA-21, HCA-55; hazards: H-1, H-2, H-3, H-4; losses: L-1, L-2, L-3, L-4
- Controllers: C-2 Operator, C-4 Ground Control Station
- Requirements (76 further non-cyber requirements share the same allocation paths):
  - [low] **MR - 26.1.1.1/1.1.1.1 Mission Computer Secure Boot** — allocation: LS-6 traces to function 'Process Waypoint Update Package' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.10/1.1.1.10 Navigation System Cryptographic Module** — allocation: LS-6 traces to function 'Set New Flight Path' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.14/1.1.1.14 Communications System Cryptographic Module** — allocation: LS-6 traces to function 'Transmit Waypoint Route Update' allocated to block 'Communications System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.15/1.1.1.15 Mission Computer Maintenance Ports** — allocation: LS-6 traces to function 'Process Waypoint Update Package' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.16/1.1.1.16 Flight Control System Maintenance Ports** — allocation: LS-6 traces to function 'Set New Flight Path' allocated to block 'Flight Controlller'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.17/1.1.1.17 Navigation System Maintenance Ports** — allocation: LS-6 traces to function 'Set New Flight Path' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.2/1.1.1.2 Flight Control system Secure Boot** — allocation: LS-6 traces to function 'Set New Flight Path' allocated to block 'Flight Controlller'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.21/1.1.1.21 Communications System Mainteanance Ports** — allocation: LS-6 traces to function 'Transmit Waypoint Route Update' allocated to block 'Communications System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.3/1.1.1.3 Navigation System Secure Boot** — allocation: LS-6 traces to function 'Set New Flight Path' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.7/1.1.1.7 Communications System Secure Boot** — allocation: LS-6 traces to function 'Transmit Waypoint Route Update' allocated to block 'Communications System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.8/1.1.1.8 Mission Computer Cryptographic Module** — allocation: LS-6 traces to function 'Process Waypoint Update Package' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.9/1.1.1.9 Flight Control System Cryptographic Module** — allocation: LS-6 traces to function 'Set New Flight Path' allocated to block 'Flight Controlller'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1/1.1.1 Flight Critical Hardware Assurance** — allocation: LS-6 traces to function 'Conduct Waypoint Communications' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.6/1.1.6 Communications Encryption** — allocation: LS-6 traces to function 'Transmit Waypoint Route Update' allocated to block 'Communications System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.1.1/1.2.1.1.1 Mission Computer Backup Mode Switching** — allocation: LS-6 traces to function 'Process Waypoint Update Package' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.1/1.2.1.1 Mission Computer Backup Mode** — allocation: LS-6 traces to function 'Process Waypoint Update Package' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.2.1/1.2.1.2.1 Flight Control System Backup Mode Switching** — allocation: LS-6 traces to function 'Set New Flight Path' allocated to block 'Flight Controlller'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.2/1.2.1.2 Flight Control System Backup Mode** — allocation: LS-6 traces to function 'Set New Flight Path' allocated to block 'Flight Controlller'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.3.1/1.2.1.3.1 Navigation System Backup Mode Switching** — allocation: LS-6 traces to function 'Set New Flight Path' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.3/1.2.1.3 Navigation System Backup Mode** — allocation: LS-6 traces to function 'Set New Flight Path' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.7.1/1.2.1.7.1 Communications System Backup Mode Switching** — allocation: LS-6 traces to function 'Transmit Waypoint Route Update' allocated to block 'Communications System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.7/1.2.1.7 Communications System Backup Mode** — allocation: LS-6 traces to function 'Transmit Waypoint Route Update' allocated to block 'Communications System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1/1.2.1 Flight Critical Subsystem Backup Mode** — allocation: LS-6 traces to function 'Conduct Waypoint Communications' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.2/1.2.2 Communications Loss Response** — allocation: LS-6 traces to function 'Process Waypoint Update Package' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.3/1.2.3 Communications Redundancy** — allocation: LS-6 traces to function 'Transmit Waypoint Route Update' allocated to block 'Communications System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.4.1/1.2.4.1 ELINT Sensors on when Needed** — allocation: LS-6 traces to function 'Process Waypoint Update Package' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.4/1.2.4 Mission Critical Subsystem Resilience** — allocation: LS-6 traces to function 'Conduct Waypoint Communications' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.3.4/1.3.4 System Zeroize** — allocation: LS-6 traces to function 'Conduct Waypoint Communications' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.4.1.1/1.4.1.1 Software Loading** — allocation: LS-6 traces to function 'Conduct Waypoint Communications' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.4.1.2/1.4.1.2 Software Loading Switch** — allocation: LS-6 traces to function 'Conduct Waypoint Communications' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.4.1/1.4.1 Single Maintenance Port** — allocation: LS-6 traces to function 'Conduct Waypoint Communications' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 29/59 HT-3 Report Unauthorized Data Detection** — allocation: LS-6 traces to function 'Conduct Waypoint Communications' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.5.2.1/1.1.5.2.1 Ground Station MFA** — lexical: proposed: shared terms ['acces', 'data', 'ground', 'station'] (text overlap, not a model relationship)
  - [low] **MR - 26.1.5.2.2/1.1.5.2.2 Ground Station Role Based Access Control** — lexical: proposed: shared terms ['acces', 'ground', 'station'] (text overlap, not a model relationship)
  - [low] **MR - 26.1.5.2.4/1.1.5.2.4 Ground Station Access Logging** — lexical: proposed: shared terms ['acces', 'ground', 'station'] (text overlap, not a model relationship)
  - [low] **MR - 26.1.5.2/1.1.5.2 Ground Station Access Control** — lexical: proposed: shared terms ['acces', 'ground', 'station'] (text overlap, not a model relationship)
  - [low] **MR - 26.3.2.2/1.3.2.2 Ground Station IPS** — lexical: proposed: shared terms ['acces', 'ground', 'station'] (text overlap, not a model relationship)
- ATT&CK techniques (heuristic):
  - [medium 0.6] **External Remote Services:T1133** — curated hint in cyber.py: phrase 'traditional-it' → T1133 (heuristic)
  - [medium 0.6] **Exploit Public-Facing Application:T1190** — curated hint in cyber.py: phrase 'traditional-it' → T1190 (heuristic)
  - [medium 0.6] **Network Denial of Service:T1498** — curated hint in cyber.py: phrase 'dos' → T1498 (heuristic)
- D3FEND countermeasures (heuristic, via D3FEND associations):
  - [medium] **Application Hardening** (Harden, direct) — D3FEND: 'Application Hardening' May Harden T1190
  - [medium] **Client-server Payload Profiling** (Detect, direct) — D3FEND: 'Client-server Payload Profiling' May Detect T1190
  - [medium] **Database Query String Analysis** (Detect, direct) — D3FEND: 'Database Query String Analysis' May Detect T1190
  - [medium] **Inbound Session Volume Analysis** (Detect, direct) — D3FEND: 'Inbound Session Volume Analysis' May Detect T1190
  - [medium] **Inbound Traffic Filtering** (Isolate, direct) — D3FEND: 'Inbound Traffic Filtering' May Isolate T1190
  - [medium] **Network Isolation** (Isolate, direct) — D3FEND: 'Network Isolation' May Isolate T1190
- D3FEND artifacts the Allocated Baseline already traces to on this path (model Trace links): Bus Message (2), Bus Network (2), Bus Network Frame (2), Bus Network Traffic (2), Call Stack (2), Central Processing Unit (2), Client Computer (2), Command (2) from block(s) Allocated Communications Controller, Allocated Flight Control Computer
- Candidate NIST SP 800-53r5 controls: AC-4, AU-6, SA-15, SC-32, SC-7, SC-7(11), SC-7(21), SC-7(5), SI-16, SI-4, SI-4(11), SI-4(24), SI-4(4)

### 3. SIPR connected Traditional-IT cyber attack on ground station to fly AV to adversary selected location

- P=0.01–0.15, TotalRiskSensitivity=0.147437, gate path: Or Adversary sends malicious commands to AV to fly AV to adversary selected location → Or Adversary gains control of ground station to fly AV to adversary selected location
- Loss scenario(s): LS-1 Adversary gains access to the ground station through a traditional-IT data connection and alters mission data sent to the AV resulting in the AV flying to an adversary selected location
- HCAs: HCA-28, HCA-40, HCA-126, HCA-9, HCA-21, HCA-55; hazards: H-1, H-2, H-3, H-4; losses: L-1, L-2, L-3, L-4
- Controllers: C-2 Operator, C-4 Ground Control Station, C-7 Mission Computer, C-8 Autopilot
- Requirements (159 further non-cyber requirements share the same allocation paths):
  - [low] **MR - 26.1.1.1/1.1.1.1 Mission Computer Secure Boot** — allocation: LS-1 traces to function 'Load OFP Data' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.10/1.1.1.10 Navigation System Cryptographic Module** — allocation: LS-1 traces to function 'Provide Required Waypoint Navigation Path' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.15/1.1.1.15 Mission Computer Maintenance Ports** — allocation: LS-1 traces to function 'Load OFP Data' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.16/1.1.1.16 Flight Control System Maintenance Ports** — allocation: LS-1 traces to function 'Set New Flight Path' allocated to block 'Flight Controlller'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.17/1.1.1.17 Navigation System Maintenance Ports** — allocation: LS-1 traces to function 'Provide Required Waypoint Navigation Path' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.2/1.1.1.2 Flight Control system Secure Boot** — allocation: LS-1 traces to function 'Set New Flight Path' allocated to block 'Flight Controlller'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.3/1.1.1.3 Navigation System Secure Boot** — allocation: LS-1 traces to function 'Provide Required Waypoint Navigation Path' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.8/1.1.1.8 Mission Computer Cryptographic Module** — allocation: LS-1 traces to function 'Load OFP Data' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.9/1.1.1.9 Flight Control System Cryptographic Module** — allocation: LS-1 traces to function 'Set New Flight Path' allocated to block 'Flight Controlller'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1/1.1.1 Flight Critical Hardware Assurance** — allocation: LS-1 traces to function 'Load OFPs' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.1.1/1.2.1.1.1 Mission Computer Backup Mode Switching** — allocation: LS-1 traces to function 'Load OFP Data' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.1/1.2.1.1 Mission Computer Backup Mode** — allocation: LS-1 traces to function 'Load OFP Data' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.2.1/1.2.1.2.1 Flight Control System Backup Mode Switching** — allocation: LS-1 traces to function 'Set New Flight Path' allocated to block 'Flight Controlller'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.2/1.2.1.2 Flight Control System Backup Mode** — allocation: LS-1 traces to function 'Set New Flight Path' allocated to block 'Flight Controlller'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.3.1/1.2.1.3.1 Navigation System Backup Mode Switching** — allocation: LS-1 traces to function 'Provide Required Waypoint Navigation Path' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.3/1.2.1.3 Navigation System Backup Mode** — allocation: LS-1 traces to function 'Provide Required Waypoint Navigation Path' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1/1.2.1 Flight Critical Subsystem Backup Mode** — allocation: LS-1 traces to function 'Load OFPs' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.2/1.2.2 Communications Loss Response** — allocation: LS-1 traces to function 'Load OFP Data' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.4.1/1.2.4.1 ELINT Sensors on when Needed** — allocation: LS-1 traces to function 'Load OFP Data' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.4/1.2.4 Mission Critical Subsystem Resilience** — allocation: LS-1 traces to function 'Load OFPs' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.3.4/1.3.4 System Zeroize** — allocation: LS-1 traces to function 'Load OFPs' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.4.1.1/1.4.1.1 Software Loading** — allocation: LS-1 traces to function 'Load OFPs' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.4.1.2/1.4.1.2 Software Loading Switch** — allocation: LS-1 traces to function 'Load OFPs' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.4.1/1.4.1 Single Maintenance Port** — allocation: LS-1 traces to function 'Load OFPs' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 29/59 HT-3 Report Unauthorized Data Detection** — allocation: LS-1 traces to function 'Load OFPs' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.5.2.1/1.1.5.2.1 Ground Station MFA** — lexical: proposed: shared terms ['acces', 'data', 'ground', 'station'] (text overlap, not a model relationship)
  - [low] **MR - 26.1.5.2.2/1.1.5.2.2 Ground Station Role Based Access Control** — lexical: proposed: shared terms ['acces', 'ground', 'station'] (text overlap, not a model relationship)
  - [low] **MR - 26.1.5.2.4/1.1.5.2.4 Ground Station Access Logging** — lexical: proposed: shared terms ['acces', 'ground', 'station'] (text overlap, not a model relationship)
  - [low] **MR - 26.1.5.2/1.1.5.2 Ground Station Access Control** — lexical: proposed: shared terms ['acces', 'ground', 'station'] (text overlap, not a model relationship)
  - [low] **MR - 26.3.2.2/1.3.2.2 Ground Station IPS** — lexical: proposed: shared terms ['acces', 'ground', 'station'] (text overlap, not a model relationship)
- ATT&CK techniques (heuristic):
  - [medium 0.6] **External Remote Services:T1133** — curated hint in cyber.py: phrase 'cyber attack on ground station' → T1133 (heuristic)
  - [medium 0.6] **Exploit Public-Facing Application:T1190** — curated hint in cyber.py: phrase 'cyber attack on ground station' → T1190 (heuristic)
  - [medium 0.6] **Data Manipulation:T1565** — curated hint in cyber.py: phrase 'alters' → T1565 (heuristic)
- D3FEND countermeasures (heuristic, via D3FEND associations):
  - [medium] **Application Hardening** (Harden, direct) — D3FEND: 'Application Hardening' May Harden T1190
  - [medium] **Client-server Payload Profiling** (Detect, direct) — D3FEND: 'Client-server Payload Profiling' May Detect T1190
  - [medium] **Database Query String Analysis** (Detect, direct) — D3FEND: 'Database Query String Analysis' May Detect T1190
  - [medium] **Inbound Session Volume Analysis** (Detect, direct) — D3FEND: 'Inbound Session Volume Analysis' May Detect T1190
  - [medium] **Inbound Traffic Filtering** (Isolate, direct) — D3FEND: 'Inbound Traffic Filtering' May Isolate T1190
  - [medium] **Network Isolation** (Isolate, direct) — D3FEND: 'Network Isolation' May Isolate T1190
- D3FEND artifacts the Allocated Baseline already traces to on this path (model Trace links): Actuator (1), Bus Message (1), Bus Network (1), Bus Network Frame (1), Bus Network Traffic (1), Call Stack (1), Central Processing Unit (1), Client Computer (1) from block(s) Allocated Flight Control Computer
- Candidate NIST SP 800-53r5 controls: AC-4, AU-6, SA-15, SC-32, SC-7, SC-7(11), SC-7(21), SC-7(5), SI-16, SI-4, SI-4(11), SI-4(24), SI-4(4)

### 4. SIPR connected Traditional-IT cyber attack on ground station to gain mission planning and AV location data

- P=0.01–0.15, TotalRiskSensitivity=0.147437, gate path: (linked from LS-7, outside the tree)
- Loss scenario(s): LS-7 Adversary gains access to the ground station through a traditional-IT data connection and gains mission planning and AV location data
- HCAs: HCA-355; hazards: -; losses: -
- Controllers: C-7 Mission Computer, C-10 Navigation Controller, C-8 Autopilot, C-11 Communications Controller
- Requirements (162 further non-cyber requirements share the same allocation paths):
  - [low] **MR - 26.1.1.1/1.1.1.1 Mission Computer Secure Boot** — allocation: LS-7 traces to function 'Load Flight Plan and Mission Parameters' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.10/1.1.1.10 Navigation System Cryptographic Module** — allocation: LS-7 traces to function 'Transmit Position Data' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.15/1.1.1.15 Mission Computer Maintenance Ports** — allocation: LS-7 traces to function 'Load Flight Plan and Mission Parameters' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.17/1.1.1.17 Navigation System Maintenance Ports** — allocation: LS-7 traces to function 'Transmit Position Data' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.3/1.1.1.3 Navigation System Secure Boot** — allocation: LS-7 traces to function 'Transmit Position Data' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.8/1.1.1.8 Mission Computer Cryptographic Module** — allocation: LS-7 traces to function 'Load Flight Plan and Mission Parameters' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1/1.1.1 Flight Critical Hardware Assurance** — allocation: LS-7 traces to function 'Launch UAV' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.1.1/1.2.1.1.1 Mission Computer Backup Mode Switching** — allocation: LS-7 traces to function 'Load Flight Plan and Mission Parameters' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.1/1.2.1.1 Mission Computer Backup Mode** — allocation: LS-7 traces to function 'Load Flight Plan and Mission Parameters' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.3.1/1.2.1.3.1 Navigation System Backup Mode Switching** — allocation: LS-7 traces to function 'Transmit Position Data' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.3/1.2.1.3 Navigation System Backup Mode** — allocation: LS-7 traces to function 'Transmit Position Data' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1/1.2.1 Flight Critical Subsystem Backup Mode** — allocation: LS-7 traces to function 'Launch UAV' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.2/1.2.2 Communications Loss Response** — allocation: LS-7 traces to function 'Load Flight Plan and Mission Parameters' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.4.1/1.2.4.1 ELINT Sensors on when Needed** — allocation: LS-7 traces to function 'Load Flight Plan and Mission Parameters' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.4/1.2.4 Mission Critical Subsystem Resilience** — allocation: LS-7 traces to function 'Launch UAV' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.3.4/1.3.4 System Zeroize** — allocation: LS-7 traces to function 'Launch UAV' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.4.1.1/1.4.1.1 Software Loading** — allocation: LS-7 traces to function 'Launch UAV' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.4.1.2/1.4.1.2 Software Loading Switch** — allocation: LS-7 traces to function 'Launch UAV' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.4.1/1.4.1 Single Maintenance Port** — allocation: LS-7 traces to function 'Launch UAV' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 29/59 HT-3 Report Unauthorized Data Detection** — allocation: LS-7 traces to function 'Launch UAV' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.5.2.1/1.1.5.2.1 Ground Station MFA** — lexical: proposed: shared terms ['acces', 'data', 'ground', 'station'] (text overlap, not a model relationship)
  - [low] **MR - 26.1.5.2.2/1.1.5.2.2 Ground Station Role Based Access Control** — lexical: proposed: shared terms ['acces', 'ground', 'station'] (text overlap, not a model relationship)
  - [low] **MR - 26.1.5.2.4/1.1.5.2.4 Ground Station Access Logging** — lexical: proposed: shared terms ['acces', 'ground', 'station'] (text overlap, not a model relationship)
  - [low] **MR - 26.1.5.2/1.1.5.2 Ground Station Access Control** — lexical: proposed: shared terms ['acces', 'ground', 'station'] (text overlap, not a model relationship)
  - [low] **MR - 26.3.2.2/1.3.2.2 Ground Station IPS** — lexical: proposed: shared terms ['acces', 'ground', 'station'] (text overlap, not a model relationship)
- ATT&CK techniques (heuristic):
  - [medium 0.6] **External Remote Services:T1133** — curated hint in cyber.py: phrase 'cyber attack on ground station' → T1133 (heuristic)
  - [medium 0.6] **Exploit Public-Facing Application:T1190** — curated hint in cyber.py: phrase 'cyber attack on ground station' → T1190 (heuristic)
- D3FEND countermeasures (heuristic, via D3FEND associations):
  - [medium] **Application Hardening** (Harden, direct) — D3FEND: 'Application Hardening' May Harden T1190
  - [medium] **Client-server Payload Profiling** (Detect, direct) — D3FEND: 'Client-server Payload Profiling' May Detect T1190
  - [medium] **Database Query String Analysis** (Detect, direct) — D3FEND: 'Database Query String Analysis' May Detect T1190
  - [medium] **Inbound Session Volume Analysis** (Detect, direct) — D3FEND: 'Inbound Session Volume Analysis' May Detect T1190
  - [medium] **Inbound Traffic Filtering** (Isolate, direct) — D3FEND: 'Inbound Traffic Filtering' May Isolate T1190
  - [medium] **Network Isolation** (Isolate, direct) — D3FEND: 'Network Isolation' May Isolate T1190
- Candidate NIST SP 800-53r5 controls: AC-4, AU-6, SA-15, SC-32, SC-7, SC-7(11), SC-7(21), SC-7(5), SI-16, SI-4, SI-4(11), SI-4(24), SI-4(4)

### 5. SIPR connected Traditional-IT cyber attack to employ ordnance on a target of their choice

- P=0.01–0.15, TotalRiskSensitivity=0.147437, gate path: (linked from LS-5, outside the tree)
- Loss scenario(s): LS-5 Adversary gains access to the ground station through a traditional-IT data connection and sends a malicious weapons release command
- HCAs: HCA-36, HCA-17, HCA-50; hazards: H-1, H-2, H-3; losses: L-1, L-2, L-3
- Controllers: C-2 Operator, C-3 Flight Lead
- Requirements (39 further non-cyber requirements share the same allocation paths):
  - [low] **MR - 26.1.1.14/1.1.1.14 Communications System Cryptographic Module** — allocation: LS-5 traces to function 'Relay Munition Launch' allocated to block 'Communications System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.21/1.1.1.21 Communications System Mainteanance Ports** — allocation: LS-5 traces to function 'Relay Munition Launch' allocated to block 'Communications System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.7/1.1.1.7 Communications System Secure Boot** — allocation: LS-5 traces to function 'Relay Munition Launch' allocated to block 'Communications System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1/1.1.1 Flight Critical Hardware Assurance** — allocation: LS-5 traces to function 'Launch Weapon' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.6/1.1.6 Communications Encryption** — allocation: LS-5 traces to function 'Relay Munition Launch' allocated to block 'Communications System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.7.1/1.2.1.7.1 Communications System Backup Mode Switching** — allocation: LS-5 traces to function 'Relay Munition Launch' allocated to block 'Communications System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.7/1.2.1.7 Communications System Backup Mode** — allocation: LS-5 traces to function 'Relay Munition Launch' allocated to block 'Communications System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1/1.2.1 Flight Critical Subsystem Backup Mode** — allocation: LS-5 traces to function 'Launch Weapon' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.3/1.2.3 Communications Redundancy** — allocation: LS-5 traces to function 'Relay Munition Launch' allocated to block 'Communications System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.4/1.2.4 Mission Critical Subsystem Resilience** — allocation: LS-5 traces to function 'Launch Weapon' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.3.4/1.3.4 System Zeroize** — allocation: LS-5 traces to function 'Launch Weapon' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.4.1.1/1.4.1.1 Software Loading** — allocation: LS-5 traces to function 'Launch Weapon' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.4.1.2/1.4.1.2 Software Loading Switch** — allocation: LS-5 traces to function 'Launch Weapon' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.4.1/1.4.1 Single Maintenance Port** — allocation: LS-5 traces to function 'Launch Weapon' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 29/59 HT-3 Report Unauthorized Data Detection** — allocation: LS-5 traces to function 'Launch Weapon' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.5.2.1/1.1.5.2.1 Ground Station MFA** — lexical: proposed: shared terms ['acces', 'data', 'ground', 'station'] (text overlap, not a model relationship)
  - [low] **MR - 26.3.1.5/1.3.1.5 Cyber Sentinel Resetting Components on Command** — lexical: proposed: shared terms ['command', 'ground', 'station'] (text overlap, not a model relationship)
  - [low] **MR - 26.3.1.7/1.3.1.7 Cyber Sentinel Switching Components to Backup Mode on Command** — lexical: proposed: shared terms ['command', 'ground', 'station'] (text overlap, not a model relationship)
  - [low] **MR - 26.1.5.2.2/1.1.5.2.2 Ground Station Role Based Access Control** — lexical: proposed: shared terms ['acces', 'ground', 'station'] (text overlap, not a model relationship)
  - [low] **MR - 26.1.5.2.4/1.1.5.2.4 Ground Station Access Logging** — lexical: proposed: shared terms ['acces', 'ground', 'station'] (text overlap, not a model relationship)
- ATT&CK techniques (heuristic):
  - [medium 0.6] **External Remote Services:T1133** — curated hint in cyber.py: phrase 'traditional-it' → T1133 (heuristic)
  - [medium 0.6] **Exploit Public-Facing Application:T1190** — curated hint in cyber.py: phrase 'traditional-it' → T1190 (heuristic)
  - [low 0.63] **Link Target:T1608.005** — name tokens ['target'] overlap; documentation also mentions ['maliciou', 'acces']
- D3FEND countermeasures (heuristic, via D3FEND associations):
  - [medium] **Application Hardening** (Harden, direct) — D3FEND: 'Application Hardening' May Harden T1190
  - [medium] **Client-server Payload Profiling** (Detect, direct) — D3FEND: 'Client-server Payload Profiling' May Detect T1190
  - [medium] **Database Query String Analysis** (Detect, direct) — D3FEND: 'Database Query String Analysis' May Detect T1190
  - [medium] **Inbound Session Volume Analysis** (Detect, direct) — D3FEND: 'Inbound Session Volume Analysis' May Detect T1190
  - [medium] **Inbound Traffic Filtering** (Isolate, direct) — D3FEND: 'Inbound Traffic Filtering' May Isolate T1190
  - [medium] **Network Isolation** (Isolate, direct) — D3FEND: 'Network Isolation' May Isolate T1190
- Candidate NIST SP 800-53r5 controls: AC-4, AU-6, SA-15, SC-32, SC-7, SC-7(11), SC-7(21), SC-7(5), SI-16, SI-4, SI-4(11), SI-4(24), SI-4(4)

### 6. Adversary steals key from SIPR connected ground station to fly AV to adversary selected location

- P=0.01–0.1, TotalRiskSensitivity=0.031985, gate path: Or Adversary sends malicious commands to AV to fly AV to adversary selected location → Or Adversary gets into the middle of ground station & UAS communications link to fly AV to adversary selected location → Or Adversary gets encryption key to fly AV to adversary selected location
- Loss scenario(s): LS-62 Adversary steals key from SIPR connected ground station to fly AV to adversary selected location
- HCAs: HCA-122, HCA-21, HCA-40, HCA-55, HCA-126; hazards: H-1, H-2, H-3, H-4; losses: L-1, L-2, L-3, L-4
- Controllers: C-7 Mission Computer, C-2 Operator, C-8 Autopilot
- Requirements (200 further non-cyber requirements share the same allocation paths):
  - [low] **MR - 26.1.1.10/1.1.1.10 Navigation System Cryptographic Module** — allocation: LS-62 traces to function 'Update Blue Force Map Points' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.14/1.1.1.14 Communications System Cryptographic Module** — allocation: LS-62 traces to function 'Activate GCS Interface' allocated to block 'Communications System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.17/1.1.1.17 Navigation System Maintenance Ports** — allocation: LS-62 traces to function 'Update Blue Force Map Points' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.21/1.1.1.21 Communications System Mainteanance Ports** — allocation: LS-62 traces to function 'Activate GCS Interface' allocated to block 'Communications System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.3/1.1.1.3 Navigation System Secure Boot** — allocation: LS-62 traces to function 'Update Blue Force Map Points' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.7/1.1.1.7 Communications System Secure Boot** — allocation: LS-62 traces to function 'Activate GCS Interface' allocated to block 'Communications System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1/1.1.1 Flight Critical Hardware Assurance** — allocation: LS-62 traces to function 'Establish Communications' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.6/1.1.6 Communications Encryption** — allocation: LS-62 traces to function 'Activate GCS Interface' allocated to block 'Communications System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.3.1/1.2.1.3.1 Navigation System Backup Mode Switching** — allocation: LS-62 traces to function 'Update Blue Force Map Points' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.3/1.2.1.3 Navigation System Backup Mode** — allocation: LS-62 traces to function 'Update Blue Force Map Points' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.7.1/1.2.1.7.1 Communications System Backup Mode Switching** — allocation: LS-62 traces to function 'Activate GCS Interface' allocated to block 'Communications System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.7/1.2.1.7 Communications System Backup Mode** — allocation: LS-62 traces to function 'Activate GCS Interface' allocated to block 'Communications System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1/1.2.1 Flight Critical Subsystem Backup Mode** — allocation: LS-62 traces to function 'Establish Communications' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.3/1.2.3 Communications Redundancy** — allocation: LS-62 traces to function 'Activate GCS Interface' allocated to block 'Communications System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.4/1.2.4 Mission Critical Subsystem Resilience** — allocation: LS-62 traces to function 'Establish Communications' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.3.4/1.3.4 System Zeroize** — allocation: LS-62 traces to function 'Establish Communications' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.4.1.1/1.4.1.1 Software Loading** — allocation: LS-62 traces to function 'Establish Communications' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.4.1.2/1.4.1.2 Software Loading Switch** — allocation: LS-62 traces to function 'Establish Communications' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.4.1/1.4.1 Single Maintenance Port** — allocation: LS-62 traces to function 'Establish Communications' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 29/59 HT-3 Report Unauthorized Data Detection** — allocation: LS-62 traces to function 'Establish Communications' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.5.2.1/1.1.5.2.1 Ground Station MFA** — lexical: proposed: shared terms ['ground', 'station'] (text overlap, not a model relationship)
  - [low] **MR - 26.1.5.2.2/1.1.5.2.2 Ground Station Role Based Access Control** — lexical: proposed: shared terms ['ground', 'station'] (text overlap, not a model relationship)
  - [low] **MR - 26.1.5.2.3/1.1.5.2.3 Ground Station Network Segmentation** — lexical: proposed: shared terms ['ground', 'station'] (text overlap, not a model relationship)
  - [low] **MR - 26.1.5.2.4/1.1.5.2.4 Ground Station Access Logging** — lexical: proposed: shared terms ['ground', 'station'] (text overlap, not a model relationship)
  - [low] **MR - 26.1.5.2/1.1.5.2 Ground Station Access Control** — lexical: proposed: shared terms ['ground', 'station'] (text overlap, not a model relationship)
- ATT&CK techniques (heuristic):
  - [medium 0.6] **Private Keys:T1552.004** — curated hint in cyber.py: phrase 'steals key' → T1552.004 (heuristic)
- D3FEND countermeasures (heuristic, via D3FEND associations):
  - [medium] **Access Mediation** (Isolate, direct) — D3FEND: 'Access Mediation' May Isolate T1552.004 (via parent technique T1552)
  - [medium] **Agent Authentication** (Harden, direct) — D3FEND: 'Agent Authentication' May Harden T1552.004 (via parent technique T1552)
  - [medium] **Authentication Cache Invalidation** (Evict, direct) — D3FEND: 'Authentication Cache Invalidation' May Evict T1552.004 (via parent technique T1552)
  - [medium] **Certificate Rotation** (Harden, direct) — D3FEND: 'Certificate Rotation' May Harden T1552.004 (via parent technique T1552)
  - [medium] **Credential Compromise Scope Analysis** (Detect, direct) — D3FEND: 'Credential Compromise Scope Analysis' May Detect T1552.004 (via parent technique T1552)
  - [medium] **Credential Eviction** (Evict, direct) — D3FEND: 'Credential Eviction' May Evict T1552.004 (via parent technique T1552)
- Candidate NIST SP 800-53r5 controls: AC-2(1), AC-2(12), AC-3, AC-6, AU-6, IA-11, IA-2, IA-3, IA-5, IA-5(1), IA-8, SI-4(13)

### 7. Other NAV sensor spoofing to fly AV to adversary selected location

- P=0.005–0.05, TotalRiskSensitivity=0.015775, gate path: Or Adversary successfully spoofs nav solution to fly AV to adversary selected location
- Loss scenario(s): LS-34 Adversary spoofs other NAV sensor to fly AV to a location of the adversary's choosing
- HCAs: HCA-122; hazards: H-1, H-2, H-3, H-4; losses: L-1, L-2, L-3, L-4
- Controllers: C-7 Mission Computer
- Requirements (159 further non-cyber requirements share the same allocation paths):
  - [low] **MR - 26.1.1.1/1.1.1.1 Mission Computer Secure Boot** — allocation: LS-34 traces to function 'Process No Fly Zone Update' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.10/1.1.1.10 Navigation System Cryptographic Module** — allocation: LS-34 traces to function 'Transmit Nav System Configuration' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.15/1.1.1.15 Mission Computer Maintenance Ports** — allocation: LS-34 traces to function 'Process No Fly Zone Update' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.17/1.1.1.17 Navigation System Maintenance Ports** — allocation: LS-34 traces to function 'Transmit Nav System Configuration' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.3/1.1.1.3 Navigation System Secure Boot** — allocation: LS-34 traces to function 'Transmit Nav System Configuration' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.8/1.1.1.8 Mission Computer Cryptographic Module** — allocation: LS-34 traces to function 'Process No Fly Zone Update' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1/1.1.1 Flight Critical Hardware Assurance** — allocation: LS-34 traces to function 'Establish Navigation' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.1.1/1.2.1.1.1 Mission Computer Backup Mode Switching** — allocation: LS-34 traces to function 'Process No Fly Zone Update' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.1/1.2.1.1 Mission Computer Backup Mode** — allocation: LS-34 traces to function 'Process No Fly Zone Update' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.3.1/1.2.1.3.1 Navigation System Backup Mode Switching** — allocation: LS-34 traces to function 'Transmit Nav System Configuration' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.3/1.2.1.3 Navigation System Backup Mode** — allocation: LS-34 traces to function 'Transmit Nav System Configuration' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1/1.2.1 Flight Critical Subsystem Backup Mode** — allocation: LS-34 traces to function 'Establish Navigation' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.2/1.2.2 Communications Loss Response** — allocation: LS-34 traces to function 'Process No Fly Zone Update' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.4.1/1.2.4.1 ELINT Sensors on when Needed** — allocation: LS-34 traces to function 'Process No Fly Zone Update' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.4/1.2.4 Mission Critical Subsystem Resilience** — allocation: LS-34 traces to function 'Establish Navigation' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.3.4/1.3.4 System Zeroize** — allocation: LS-34 traces to function 'Establish Navigation' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.4.1.1/1.4.1.1 Software Loading** — allocation: LS-34 traces to function 'Establish Navigation' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.4.1.2/1.4.1.2 Software Loading Switch** — allocation: LS-34 traces to function 'Establish Navigation' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.4.1/1.4.1 Single Maintenance Port** — allocation: LS-34 traces to function 'Establish Navigation' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 29/59 HT-3 Report Unauthorized Data Detection** — allocation: LS-34 traces to function 'Establish Navigation' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
- ATT&CK techniques (heuristic):
  - [medium 0.6] **Masquerading:T1036** — curated hint in cyber.py: phrase 'spoof' → T1036 (heuristic)
  - [medium 0.6] **Adversary-in-the-Middle:T1557** — curated hint in cyber.py: phrase 'spoof' → T1557 (heuristic)
  - [low 0.53] **Email Spoofing:T1672** — name tokens ['spoof'] overlap
- D3FEND countermeasures (heuristic, via D3FEND associations):
  - [medium] **Client-server Payload Profiling** (Detect, direct) — D3FEND: 'Client-server Payload Profiling' May Detect T1557
  - [medium] **Network Isolation** (Isolate, direct) — D3FEND: 'Network Isolation' May Isolate T1557
  - [medium] **Network Traffic Analysis** (Detect, direct) — D3FEND: 'Network Traffic Analysis' May Detect T1557
  - [medium] **Network Traffic Community Deviation** (Detect, direct) — D3FEND: 'Network Traffic Community Deviation' May Detect T1557
  - [medium] **Network Traffic Filtering** (Isolate, direct) — D3FEND: 'Network Traffic Filtering' May Isolate T1557
  - [medium] **Network Traffic Signature Analysis** (Detect, direct) — D3FEND: 'Network Traffic Signature Analysis' May Detect T1557
- Candidate NIST SP 800-53r5 controls: AC-4, AU-6, SC-32, SC-7, SC-7(21), SC-7(5), SI-3, SI-4, SI-4(11), SI-4(4)

### 8. Adversary control of device on 1553 bus via supply chain to fly AV to adversary selected location

- P=0.0001–0.05, TotalRiskSensitivity=0.018931, gate path: Or Device on 1553 bus sends adversary spoofed message to fly AV to adversary selected location
- Loss scenario(s): LS-60 Adversary control of device on 1553 bus via supply chain to fly AV to adversary selected location
- HCAs: HCA-122, HCA-21, HCA-40, HCA-55, HCA-126; hazards: H-1, H-2, H-3, H-4; losses: L-1, L-2, L-3, L-4
- Controllers: C-7 Mission Computer, C-2 Operator, C-8 Autopilot
- Requirements (159 further non-cyber requirements share the same allocation paths):
  - [low] **MR - 26.1.1.1/1.1.1.1 Mission Computer Secure Boot** — allocation: LS-60 traces to function 'Set New Flight Path' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.10/1.1.1.10 Navigation System Cryptographic Module** — allocation: LS-60 traces to function 'Set New Flight Path' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.15/1.1.1.15 Mission Computer Maintenance Ports** — allocation: LS-60 traces to function 'Set New Flight Path' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.16/1.1.1.16 Flight Control System Maintenance Ports** — allocation: LS-60 traces to function 'Set New Flight Path' allocated to block 'Flight Controlller'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.17/1.1.1.17 Navigation System Maintenance Ports** — allocation: LS-60 traces to function 'Set New Flight Path' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.2/1.1.1.2 Flight Control system Secure Boot** — allocation: LS-60 traces to function 'Set New Flight Path' allocated to block 'Flight Controlller'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.3/1.1.1.3 Navigation System Secure Boot** — allocation: LS-60 traces to function 'Set New Flight Path' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.8/1.1.1.8 Mission Computer Cryptographic Module** — allocation: LS-60 traces to function 'Set New Flight Path' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.9/1.1.1.9 Flight Control System Cryptographic Module** — allocation: LS-60 traces to function 'Set New Flight Path' allocated to block 'Flight Controlller'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1/1.1.1 Flight Critical Hardware Assurance** — allocation: LS-60 traces to function 'Conduct Waypoint Communications' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.1.1/1.2.1.1.1 Mission Computer Backup Mode Switching** — allocation: LS-60 traces to function 'Set New Flight Path' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.1/1.2.1.1 Mission Computer Backup Mode** — allocation: LS-60 traces to function 'Set New Flight Path' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.2.1/1.2.1.2.1 Flight Control System Backup Mode Switching** — allocation: LS-60 traces to function 'Set New Flight Path' allocated to block 'Flight Controlller'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.2/1.2.1.2 Flight Control System Backup Mode** — allocation: LS-60 traces to function 'Set New Flight Path' allocated to block 'Flight Controlller'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.3.1/1.2.1.3.1 Navigation System Backup Mode Switching** — allocation: LS-60 traces to function 'Set New Flight Path' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.3/1.2.1.3 Navigation System Backup Mode** — allocation: LS-60 traces to function 'Set New Flight Path' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1/1.2.1 Flight Critical Subsystem Backup Mode** — allocation: LS-60 traces to function 'Conduct Waypoint Communications' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.2/1.2.2 Communications Loss Response** — allocation: LS-60 traces to function 'Set New Flight Path' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.4.1/1.2.4.1 ELINT Sensors on when Needed** — allocation: LS-60 traces to function 'Set New Flight Path' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.4/1.2.4 Mission Critical Subsystem Resilience** — allocation: LS-60 traces to function 'Conduct Waypoint Communications' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.3.4/1.3.4 System Zeroize** — allocation: LS-60 traces to function 'Conduct Waypoint Communications' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.4.1.1/1.4.1.1 Software Loading** — allocation: LS-60 traces to function 'Conduct Waypoint Communications' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.4.1.2/1.4.1.2 Software Loading Switch** — allocation: LS-60 traces to function 'Conduct Waypoint Communications' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.4.1/1.4.1 Single Maintenance Port** — allocation: LS-60 traces to function 'Conduct Waypoint Communications' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 29/59 HT-3 Report Unauthorized Data Detection** — allocation: LS-60 traces to function 'Conduct Waypoint Communications' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 90/120 CSA-10 Actively Manage System's Configurations to Achieve and Maintain an Operationally relevant Cyber Risk Posture** — lexical: proposed: shared terms ['chain', 'supply'] (text overlap, not a model relationship)
  - [low] **MR - 26.1.5.1/1.1.5.1 Cyber Sentinel as 1553 Bus Controller** — lexical: proposed: shared terms ['bus', 'control'] (text overlap, not a model relationship)
- ATT&CK techniques (heuristic):
  - [medium 0.6] **Supply Chain Compromise:T1195** — curated hint in cyber.py: phrase 'supply chain' → T1195 (heuristic)
  - [medium 0.6] **Compromise Software Supply Chain:T1195.002** — curated hint in cyber.py: phrase 'supply chain' → T1195.002 (heuristic)
  - [low 0.58] **Compromise Hardware Supply Chain:T1195.003** — name tokens ['chain', 'supply'] overlap; documentation also mentions ['control']
- D3FEND countermeasures (heuristic, via D3FEND associations):
  - [medium] **Asset Inventory** (Model, direct) — D3FEND: 'Asset Inventory' May Model T1195.002
  - [medium] **Asset Vulnerability Enumeration** (Model, direct) — D3FEND: 'Asset Vulnerability Enumeration' May Model T1195.002
  - [medium] **Container Image Analysis** (Model, direct) — D3FEND: 'Container Image Analysis' May Model T1195.002
  - [medium] **Platform Hardening** (Harden, direct) — D3FEND: 'Platform Hardening' May Harden T1195.002
  - [medium] **Restore Object** (Restore, direct) — D3FEND: 'Restore Object' May Restore T1195.002
  - [medium] **Restore Software** (Restore, direct) — D3FEND: 'Restore Software' May Restore T1195.002
- D3FEND artifacts the Allocated Baseline already traces to on this path (model Trace links): Actuator (1), Bus Message (1), Bus Network (1), Bus Network Frame (1), Bus Network Traffic (1), Call Stack (1), Central Processing Unit (1), Client Computer (1) from block(s) Allocated Flight Control Computer
- Candidate NIST SP 800-53r5 controls: CM-2, CM-6, CM-7, CM-8, CM-8(1), CP-10, CP-9, RA-5, RA-5(2), SI-7

### 9. MIL GPS spoofing to fly AV to adversary selected location

- P=0.001–0.02, TotalRiskSensitivity=0.005893, gate path: Or Adversary successfully spoofs nav solution to fly AV to adversary selected location
- Loss scenario(s): LS-33 Adversary spoofs GPS data to fly AV to a location of the adversary's choosing
- HCAs: HCA-122; hazards: H-1, H-2, H-3, H-4; losses: L-1, L-2, L-3, L-4
- Controllers: C-7 Mission Computer
- Requirements (86 further non-cyber requirements share the same allocation paths):
  - [low] **MR - 26.1.1.10/1.1.1.10 Navigation System Cryptographic Module** — allocation: LS-33 traces to function 'Receive GPS Signal' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.17/1.1.1.17 Navigation System Maintenance Ports** — allocation: LS-33 traces to function 'Receive GPS Signal' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.3/1.1.1.3 Navigation System Secure Boot** — allocation: LS-33 traces to function 'Receive GPS Signal' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1/1.1.1 Flight Critical Hardware Assurance** — allocation: LS-33 traces to function 'Fly UAS Based on Waypoint Data' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.3.1/1.2.1.3.1 Navigation System Backup Mode Switching** — allocation: LS-33 traces to function 'Receive GPS Signal' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.3/1.2.1.3 Navigation System Backup Mode** — allocation: LS-33 traces to function 'Receive GPS Signal' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1/1.2.1 Flight Critical Subsystem Backup Mode** — allocation: LS-33 traces to function 'Fly UAS Based on Waypoint Data' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.4/1.2.4 Mission Critical Subsystem Resilience** — allocation: LS-33 traces to function 'Fly UAS Based on Waypoint Data' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.3.4/1.3.4 System Zeroize** — allocation: LS-33 traces to function 'Fly UAS Based on Waypoint Data' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.4.1.1/1.4.1.1 Software Loading** — allocation: LS-33 traces to function 'Fly UAS Based on Waypoint Data' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.4.1.2/1.4.1.2 Software Loading Switch** — allocation: LS-33 traces to function 'Fly UAS Based on Waypoint Data' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.4.1/1.4.1 Single Maintenance Port** — allocation: LS-33 traces to function 'Fly UAS Based on Waypoint Data' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 29/59 HT-3 Report Unauthorized Data Detection** — allocation: LS-33 traces to function 'Fly UAS Based on Waypoint Data' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.9/1.1.9 Military GPS Only** — lexical: proposed: shared terms ['data', 'gps'] (text overlap, not a model relationship)
- ATT&CK techniques (heuristic):
  - [medium 0.6] **Masquerading:T1036** — curated hint in cyber.py: phrase 'spoof' → T1036 (heuristic)
  - [medium 0.6] **Adversary-in-the-Middle:T1557** — curated hint in cyber.py: phrase 'spoof' → T1557 (heuristic)
  - [low 0.53] **Email Spoofing:T1672** — name tokens ['spoof'] overlap
- D3FEND countermeasures (heuristic, via D3FEND associations):
  - [medium] **Client-server Payload Profiling** (Detect, direct) — D3FEND: 'Client-server Payload Profiling' May Detect T1557
  - [medium] **Network Isolation** (Isolate, direct) — D3FEND: 'Network Isolation' May Isolate T1557
  - [medium] **Network Traffic Analysis** (Detect, direct) — D3FEND: 'Network Traffic Analysis' May Detect T1557
  - [medium] **Network Traffic Community Deviation** (Detect, direct) — D3FEND: 'Network Traffic Community Deviation' May Detect T1557
  - [medium] **Network Traffic Filtering** (Isolate, direct) — D3FEND: 'Network Traffic Filtering' May Isolate T1557
  - [medium] **Network Traffic Signature Analysis** (Detect, direct) — D3FEND: 'Network Traffic Signature Analysis' May Detect T1557
- Candidate NIST SP 800-53r5 controls: AC-4, AU-6, SC-32, SC-7, SC-7(21), SC-7(5), SI-3, SI-4, SI-4(11), SI-4(4)

### 10. Operator insider gains access to ground station to fly AV to adversary selected location

- P=0.0002–0.002, TotalRiskSensitivity=0.003412, gate path: Or Adversary sends malicious commands to AV to fly AV to adversary selected location → Or Adversary gains control of ground station to fly AV to adversary selected location
- Loss scenario(s): LS-2 Adversary gains access to the ground station through insider physical access and alters mission data sent to the AV resulting in the AV flying to an adversary selected location
- HCAs: HCA-28, HCA-40, HCA-126, HCA-9, HCA-21, HCA-55; hazards: H-1, H-2, H-3, H-4; losses: L-1, L-2, L-3, L-4
- Controllers: C-2 Operator, C-4 Ground Control Station, C-7 Mission Computer, C-8 Autopilot
- Requirements (598 further non-cyber requirements share the same allocation paths):
  - [low] **MR - 26.1.1.1/1.1.1.1 Mission Computer Secure Boot** — allocation: LS-2 traces to function 'Receive Current Nav Status/Config' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.10/1.1.1.10 Navigation System Cryptographic Module** — allocation: LS-2 traces to function 'Provide Required Waypoint Navigation Path' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.15/1.1.1.15 Mission Computer Maintenance Ports** — allocation: LS-2 traces to function 'Receive Current Nav Status/Config' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.16/1.1.1.16 Flight Control System Maintenance Ports** — allocation: LS-2 traces to function 'Set New Flight Path' allocated to block 'Flight Controlller'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.17/1.1.1.17 Navigation System Maintenance Ports** — allocation: LS-2 traces to function 'Provide Required Waypoint Navigation Path' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.2/1.1.1.2 Flight Control system Secure Boot** — allocation: LS-2 traces to function 'Set New Flight Path' allocated to block 'Flight Controlller'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.3/1.1.1.3 Navigation System Secure Boot** — allocation: LS-2 traces to function 'Provide Required Waypoint Navigation Path' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.8/1.1.1.8 Mission Computer Cryptographic Module** — allocation: LS-2 traces to function 'Receive Current Nav Status/Config' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.9/1.1.1.9 Flight Control System Cryptographic Module** — allocation: LS-2 traces to function 'Set New Flight Path' allocated to block 'Flight Controlller'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1/1.1.1 Flight Critical Hardware Assurance** — allocation: LS-2 traces to function 'Establish Navigation' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.1.1/1.2.1.1.1 Mission Computer Backup Mode Switching** — allocation: LS-2 traces to function 'Receive Current Nav Status/Config' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.1/1.2.1.1 Mission Computer Backup Mode** — allocation: LS-2 traces to function 'Receive Current Nav Status/Config' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.2.1/1.2.1.2.1 Flight Control System Backup Mode Switching** — allocation: LS-2 traces to function 'Set New Flight Path' allocated to block 'Flight Controlller'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.2/1.2.1.2 Flight Control System Backup Mode** — allocation: LS-2 traces to function 'Set New Flight Path' allocated to block 'Flight Controlller'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.3.1/1.2.1.3.1 Navigation System Backup Mode Switching** — allocation: LS-2 traces to function 'Provide Required Waypoint Navigation Path' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.3/1.2.1.3 Navigation System Backup Mode** — allocation: LS-2 traces to function 'Provide Required Waypoint Navigation Path' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1/1.2.1 Flight Critical Subsystem Backup Mode** — allocation: LS-2 traces to function 'Establish Navigation' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.2/1.2.2 Communications Loss Response** — allocation: LS-2 traces to function 'Receive Current Nav Status/Config' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.4.1/1.2.4.1 ELINT Sensors on when Needed** — allocation: LS-2 traces to function 'Receive Current Nav Status/Config' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.4/1.2.4 Mission Critical Subsystem Resilience** — allocation: LS-2 traces to function 'Establish Navigation' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.3.4/1.3.4 System Zeroize** — allocation: LS-2 traces to function 'Establish Navigation' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.4.1.1/1.4.1.1 Software Loading** — allocation: LS-2 traces to function 'Establish Navigation' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.4.1.2/1.4.1.2 Software Loading Switch** — allocation: LS-2 traces to function 'Establish Navigation' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.4.1/1.4.1 Single Maintenance Port** — allocation: LS-2 traces to function 'Establish Navigation' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 29/59 HT-3 Report Unauthorized Data Detection** — allocation: LS-2 traces to function 'Establish Navigation' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.5.2.1/1.1.5.2.1 Ground Station MFA** — lexical: proposed: shared terms ['acces', 'data', 'ground', 'station'] (text overlap, not a model relationship)
  - [low] **MR - 26.3.1.5/1.3.1.5 Cyber Sentinel Resetting Components on Command** — lexical: proposed: shared terms ['ground', 'operator', 'station'] (text overlap, not a model relationship)
  - [low] **MR - 26.3.1.7/1.3.1.7 Cyber Sentinel Switching Components to Backup Mode on Command** — lexical: proposed: shared terms ['ground', 'operator', 'station'] (text overlap, not a model relationship)
  - [low] **MR - 26.1.5.2.2/1.1.5.2.2 Ground Station Role Based Access Control** — lexical: proposed: shared terms ['acces', 'ground', 'station'] (text overlap, not a model relationship)
  - [low] **MR - 26.1.5.2.4/1.1.5.2.4 Ground Station Access Logging** — lexical: proposed: shared terms ['acces', 'ground', 'station'] (text overlap, not a model relationship)
- ATT&CK techniques (heuristic):
  - [medium 0.6] **Valid Accounts:T1078** — curated hint in cyber.py: phrase 'insider' → T1078 (heuristic)
  - [medium 0.6] **Data Manipulation:T1565** — curated hint in cyber.py: phrase 'alters' → T1565 (heuristic)
- D3FEND countermeasures (heuristic, via D3FEND associations):
  - [medium] **Access Modeling** (Model, direct) — D3FEND: 'Access Modeling' May Model T1078
  - [medium] **Access Policy Administration** (Isolate, direct) — D3FEND: 'Access Policy Administration' May Isolate T1078
  - [medium] **Account Locking** (Evict, direct) — D3FEND: 'Account Locking' May Evict T1078
  - [medium] **Agent Authentication** (Harden, direct) — D3FEND: 'Agent Authentication' May Harden T1078
  - [medium] **Biometric Authentication** (Harden, direct) — D3FEND: 'Biometric Authentication' May Harden T1078
  - [medium] **Certificate-based Authentication** (Harden, direct) — D3FEND: 'Certificate-based Authentication' May Harden T1078
- D3FEND artifacts the Allocated Baseline already traces to on this path (model Trace links): Actuator (1), Bus Message (1), Bus Network (1), Bus Network Frame (1), Bus Network Traffic (1), Call Stack (1), Central Processing Unit (1), Client Computer (1) from block(s) Allocated Flight Control Computer
- Candidate NIST SP 800-53r5 controls: AC-2, AC-6, AC-7, CP-2, IA-2, IA-3, IA-5(12), IA-5(2), IA-8, RA-3, SC-17

### 11. Adversary supply chain attack on logistics system provides logical access to fly UAS to adversary selected location

- P=0.0001–0.001, TotalRiskSensitivity=0.000657, gate path: Or Adversary sends malicious commands to AV to fly AV to adversary selected location → Or Adversary gains control of ground station to fly AV to adversary selected location
- Loss scenario(s): LS-37 Adversary supply chain attack on ground station provides logical access which adversary uses to manipulate mission data causing the UAS to fly to a adversary selected location
- HCAs: HCA-28, HCA-40, HCA-58, HCA-183, HCA-180, HCA-176, HCA-178, HCA-177 (+148); hazards: H-1, H-2, H-3, H-4, H-6, H-5; losses: L-1, L-2, L-3, L-4
- Controllers: C-2 Operator, C-4 Ground Control Station, C-7 Mission Computer, C-15 Stores Controller, C-8 Autopilot, C-10 Navigation Controller, C-30 Cyber Sentinel, C-3 Flight Lead, C-9 Flight Control Computer, C-11 Communications Controller, C-14 Fuel Controller, C-13 Electrical Controller
- Requirements (159 further non-cyber requirements share the same allocation paths):
  - [low] **MR - 26.1.1.1/1.1.1.1 Mission Computer Secure Boot** — allocation: LS-37 traces to function 'Load Flight Plan and Mission Parameters' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.10/1.1.1.10 Navigation System Cryptographic Module** — allocation: LS-37 traces to function 'Provide Required Waypoint Navigation Path' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.15/1.1.1.15 Mission Computer Maintenance Ports** — allocation: LS-37 traces to function 'Load Flight Plan and Mission Parameters' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.16/1.1.1.16 Flight Control System Maintenance Ports** — allocation: LS-37 traces to function 'Set New Flight Path' allocated to block 'Flight Controlller'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.17/1.1.1.17 Navigation System Maintenance Ports** — allocation: LS-37 traces to function 'Provide Required Waypoint Navigation Path' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.2/1.1.1.2 Flight Control system Secure Boot** — allocation: LS-37 traces to function 'Set New Flight Path' allocated to block 'Flight Controlller'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.3/1.1.1.3 Navigation System Secure Boot** — allocation: LS-37 traces to function 'Provide Required Waypoint Navigation Path' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.8/1.1.1.8 Mission Computer Cryptographic Module** — allocation: LS-37 traces to function 'Load Flight Plan and Mission Parameters' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.9/1.1.1.9 Flight Control System Cryptographic Module** — allocation: LS-37 traces to function 'Set New Flight Path' allocated to block 'Flight Controlller'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1/1.1.1 Flight Critical Hardware Assurance** — allocation: LS-37 traces to function 'Launch UAV' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.1.1/1.2.1.1.1 Mission Computer Backup Mode Switching** — allocation: LS-37 traces to function 'Load Flight Plan and Mission Parameters' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.1/1.2.1.1 Mission Computer Backup Mode** — allocation: LS-37 traces to function 'Load Flight Plan and Mission Parameters' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.2.1/1.2.1.2.1 Flight Control System Backup Mode Switching** — allocation: LS-37 traces to function 'Set New Flight Path' allocated to block 'Flight Controlller'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.2/1.2.1.2 Flight Control System Backup Mode** — allocation: LS-37 traces to function 'Set New Flight Path' allocated to block 'Flight Controlller'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.3.1/1.2.1.3.1 Navigation System Backup Mode Switching** — allocation: LS-37 traces to function 'Provide Required Waypoint Navigation Path' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.3/1.2.1.3 Navigation System Backup Mode** — allocation: LS-37 traces to function 'Provide Required Waypoint Navigation Path' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1/1.2.1 Flight Critical Subsystem Backup Mode** — allocation: LS-37 traces to function 'Launch UAV' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.2/1.2.2 Communications Loss Response** — allocation: LS-37 traces to function 'Load Flight Plan and Mission Parameters' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.4.1/1.2.4.1 ELINT Sensors on when Needed** — allocation: LS-37 traces to function 'Load Flight Plan and Mission Parameters' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.4/1.2.4 Mission Critical Subsystem Resilience** — allocation: LS-37 traces to function 'Launch UAV' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.3.4/1.3.4 System Zeroize** — allocation: LS-37 traces to function 'Launch UAV' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.4.1.1/1.4.1.1 Software Loading** — allocation: LS-37 traces to function 'Launch UAV' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.4.1.2/1.4.1.2 Software Loading Switch** — allocation: LS-37 traces to function 'Launch UAV' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.4.1/1.4.1 Single Maintenance Port** — allocation: LS-37 traces to function 'Launch UAV' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 29/59 HT-3 Report Unauthorized Data Detection** — allocation: LS-37 traces to function 'Launch UAV' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.5.2.1/1.1.5.2.1 Ground Station MFA** — lexical: proposed: shared terms ['acces', 'data', 'ground', 'station'] (text overlap, not a model relationship)
  - [low] **MR - 81/111 CSA-01 Control Access** — lexical: proposed: shared terms ['acces', 'logical', 'maintenance'] (text overlap, not a model relationship)
  - [low] **MR - 26.1.5.3.1/1.1.5.3.1 Maintenance System MFA** — lexical: proposed: shared terms ['acces', 'data', 'maintenance'] (text overlap, not a model relationship)
  - [low] **MR - 26.1.5.2.2/1.1.5.2.2 Ground Station Role Based Access Control** — lexical: proposed: shared terms ['acces', 'ground', 'station'] (text overlap, not a model relationship)
  - [low] **MR - 26.1.5.2.4/1.1.5.2.4 Ground Station Access Logging** — lexical: proposed: shared terms ['acces', 'ground', 'station'] (text overlap, not a model relationship)
- ATT&CK techniques (heuristic):
  - [medium 0.8] **Supply Chain Compromise:T1195** — name tokens ['chain', 'supply'] overlap; documentation also mentions ['data', 'manipulate']
  - [medium 0.6] **Valid Accounts:T1078** — curated hint in cyber.py: phrase 'logical access' → T1078 (heuristic)
  - [medium 0.6] **External Remote Services:T1133** — curated hint in cyber.py: phrase 'logical access' → T1133 (heuristic)
- D3FEND countermeasures (heuristic, via D3FEND associations):
  - [medium] **Access Modeling** (Model, direct) — D3FEND: 'Access Modeling' May Model T1078
  - [medium] **Access Policy Administration** (Isolate, direct) — D3FEND: 'Access Policy Administration' May Isolate T1078
  - [medium] **Account Locking** (Evict, direct) — D3FEND: 'Account Locking' May Evict T1078
  - [medium] **Agent Authentication** (Harden, direct) — D3FEND: 'Agent Authentication' May Harden T1078
  - [medium] **Biometric Authentication** (Harden, direct) — D3FEND: 'Biometric Authentication' May Harden T1078
  - [medium] **Certificate-based Authentication** (Harden, direct) — D3FEND: 'Certificate-based Authentication' May Harden T1078
- D3FEND artifacts the Allocated Baseline already traces to on this path (model Trace links): Actuator (1), Bus Message (1), Bus Network (1), Bus Network Frame (1), Bus Network Traffic (1), Call Stack (1), Central Processing Unit (1), Client Computer (1) from block(s) Allocated Flight Control Computer
- Candidate NIST SP 800-53r5 controls: AC-2, AC-6, AC-7, CP-2, IA-2, IA-3, IA-5(12), IA-5(2), IA-8, RA-3, SC-17

### 12. Adversary gets link to shift into unencrypted mode to fly AV to adversary selected location

- P=0.0–0.001, TotalRiskSensitivity=0.000835, gate path: Or Adversary sends malicious commands to AV to fly AV to adversary selected location → Or Adversary gets into the middle of ground station & UAS communications link to fly AV to adversary selected location
- Loss scenario(s): LS-11 Adversary gets the AV communications system to shift to an unencrypted mode enabling them to send commands to fly the AV to a location of their choice
- HCAs: HCA-9, HCA-21, HCA-28, HCA-40, HCA-55; hazards: H-1, H-2, H-3, H-4; losses: L-1, L-2, L-3, L-4
- Controllers: C-2 Operator, C-4 Ground Control Station
- Requirements (43 further non-cyber requirements share the same allocation paths):
  - [low] **MR - 26.1.1.10/1.1.1.10 Navigation System Cryptographic Module** — allocation: LS-11 traces to function 'Provide Required Waypoint Navigation Path' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [medium] **MR - 26.1.1.14/1.1.1.14 Communications System Cryptographic Module** — allocation+text: LS-11 traces to function 'Activate Encryption' allocated to block 'Communications System'; requirement Allocate → that block (same subsystem only); proposed: the requirement text shares ['communication', 'encryption'] with the leaf (heuristic, not a model link)
  - [low] **MR - 26.1.1.17/1.1.1.17 Navigation System Maintenance Ports** — allocation: LS-11 traces to function 'Provide Required Waypoint Navigation Path' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.21/1.1.1.21 Communications System Mainteanance Ports** — allocation: LS-11 traces to function 'Activate Encryption' allocated to block 'Communications System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.3/1.1.1.3 Navigation System Secure Boot** — allocation: LS-11 traces to function 'Provide Required Waypoint Navigation Path' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.7/1.1.1.7 Communications System Secure Boot** — allocation: LS-11 traces to function 'Activate Encryption' allocated to block 'Communications System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1/1.1.1 Flight Critical Hardware Assurance** — allocation: LS-11 traces to function 'Fly UAS Based on Waypoint Data' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [medium] **MR - 26.1.6/1.1.6 Communications Encryption** — allocation+text: LS-11 traces to function 'Activate Encryption' allocated to block 'Communications System'; requirement Allocate → that block (same subsystem only); proposed: the requirement text shares ['communication', 'encryption'] with the leaf (heuristic, not a model link)
  - [medium] **MR - 26.2.1.3.1/1.2.1.3.1 Navigation System Backup Mode Switching** — allocation+text: LS-11 traces to function 'Provide Required Waypoint Navigation Path' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only); proposed: the requirement text shares ['command', 'mode'] with the leaf (heuristic, not a model link)
  - [low] **MR - 26.2.1.3/1.2.1.3 Navigation System Backup Mode** — allocation: LS-11 traces to function 'Provide Required Waypoint Navigation Path' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [medium] **MR - 26.2.1.7.1/1.2.1.7.1 Communications System Backup Mode Switching** — allocation+text: LS-11 traces to function 'Activate Encryption' allocated to block 'Communications System'; requirement Allocate → that block (same subsystem only); proposed: the requirement text shares ['command', 'communication', 'mode'] with the leaf (heuristic, not a model link)
  - [medium] **MR - 26.2.1.7/1.2.1.7 Communications System Backup Mode** — allocation+text: LS-11 traces to function 'Activate Encryption' allocated to block 'Communications System'; requirement Allocate → that block (same subsystem only); proposed: the requirement text shares ['communication', 'mode'] with the leaf (heuristic, not a model link)
  - [low] **MR - 26.2.1/1.2.1 Flight Critical Subsystem Backup Mode** — allocation: LS-11 traces to function 'Fly UAS Based on Waypoint Data' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.3/1.2.3 Communications Redundancy** — allocation: LS-11 traces to function 'Activate Encryption' allocated to block 'Communications System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.4/1.2.4 Mission Critical Subsystem Resilience** — allocation: LS-11 traces to function 'Fly UAS Based on Waypoint Data' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.3.4/1.3.4 System Zeroize** — allocation: LS-11 traces to function 'Fly UAS Based on Waypoint Data' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.4.1.1/1.4.1.1 Software Loading** — allocation: LS-11 traces to function 'Fly UAS Based on Waypoint Data' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.4.1.2/1.4.1.2 Software Loading Switch** — allocation: LS-11 traces to function 'Fly UAS Based on Waypoint Data' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.4.1/1.4.1 Single Maintenance Port** — allocation: LS-11 traces to function 'Fly UAS Based on Waypoint Data' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 29/59 HT-3 Report Unauthorized Data Detection** — allocation: LS-11 traces to function 'Fly UAS Based on Waypoint Data' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 83/113 CSA-03 Secure Transmissions and Communications** — lexical: proposed: shared terms ['communication', 'encryption'] (text overlap, not a model relationship)
  - [low] **MR - 26.2.1.1.1/1.2.1.1.1 Mission Computer Backup Mode Switching** — lexical: proposed: shared terms ['command', 'mode'] (text overlap, not a model relationship)
  - [low] **MR - 26.2.1.2.1/1.2.1.2.1 Flight Control System Backup Mode Switching** — lexical: proposed: shared terms ['command', 'mode'] (text overlap, not a model relationship)
  - [low] **MR - 26.2.1.4.1/1.2.1.4.1 Propulsion System Backup Mode Switching** — lexical: proposed: shared terms ['command', 'mode'] (text overlap, not a model relationship)
  - [low] **MR - 26.2.1.5.1/1.2.1.5.1 Fuel System Backup Mode Switching** — lexical: proposed: shared terms ['command', 'mode'] (text overlap, not a model relationship)
- ATT&CK techniques (heuristic):
  - [medium 0.6] **Impair Defenses:T1562** — curated hint in cyber.py: phrase 'unencrypted mode' → T1562 (heuristic)
  - [medium 0.6] **Weaken Encryption:T1600** — curated hint in cyber.py: phrase 'unencrypted mode' → T1600 (heuristic)
  - [low 0.59] **Data Encrypted:T1022** — name tokens ['encryption'] overlap; documentation also mentions ['command']
- D3FEND countermeasures (heuristic, via D3FEND associations):
  - none reachable
- D3FEND artifacts the Allocated Baseline already traces to on this path (model Trace links): Bus Message (2), Bus Network (2), Bus Network Frame (2), Bus Network Traffic (2), Central Processing Unit (2), Client Computer (2), Command (2), Computer Platform (2) from block(s) Allocated Communications Controller, Allocated Nav Controller

### 13. Adversary gets insider to give them the command link key to fly AV to adversary selected location

- P=5e-05–0.0005, TotalRiskSensitivity=0.000459, gate path: Or Adversary sends malicious commands to AV to fly AV to adversary selected location → Or Adversary gets into the middle of ground station & UAS communications link to fly AV to adversary selected location → Or Adversary gets encryption key to fly AV to adversary selected location
- Loss scenario(s): LS-59 Adversary gets insider to give them the command link key to fly AV to adversary selected location
- HCAs: HCA-122, HCA-21, HCA-40, HCA-55, HCA-126; hazards: H-1, H-2, H-3, H-4; losses: L-1, L-2, L-3, L-4
- Controllers: C-7 Mission Computer, C-2 Operator, C-8 Autopilot
- Requirements (159 further non-cyber requirements share the same allocation paths):
  - [low] **MR - 26.1.1.1/1.1.1.1 Mission Computer Secure Boot** — allocation: LS-59 traces to function 'Load Flight Plan and Mission Parameters' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.10/1.1.1.10 Navigation System Cryptographic Module** — allocation: LS-59 traces to function 'Provide Required Waypoint Navigation Path' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.15/1.1.1.15 Mission Computer Maintenance Ports** — allocation: LS-59 traces to function 'Load Flight Plan and Mission Parameters' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.16/1.1.1.16 Flight Control System Maintenance Ports** — allocation: LS-59 traces to function 'Set New Flight Path' allocated to block 'Flight Controlller'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.17/1.1.1.17 Navigation System Maintenance Ports** — allocation: LS-59 traces to function 'Provide Required Waypoint Navigation Path' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.2/1.1.1.2 Flight Control system Secure Boot** — allocation: LS-59 traces to function 'Set New Flight Path' allocated to block 'Flight Controlller'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.3/1.1.1.3 Navigation System Secure Boot** — allocation: LS-59 traces to function 'Provide Required Waypoint Navigation Path' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.8/1.1.1.8 Mission Computer Cryptographic Module** — allocation: LS-59 traces to function 'Load Flight Plan and Mission Parameters' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.9/1.1.1.9 Flight Control System Cryptographic Module** — allocation: LS-59 traces to function 'Set New Flight Path' allocated to block 'Flight Controlller'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1/1.1.1 Flight Critical Hardware Assurance** — allocation: LS-59 traces to function 'Launch UAV' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.1.1/1.2.1.1.1 Mission Computer Backup Mode Switching** — allocation: LS-59 traces to function 'Load Flight Plan and Mission Parameters' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.1/1.2.1.1 Mission Computer Backup Mode** — allocation: LS-59 traces to function 'Load Flight Plan and Mission Parameters' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.2.1/1.2.1.2.1 Flight Control System Backup Mode Switching** — allocation: LS-59 traces to function 'Set New Flight Path' allocated to block 'Flight Controlller'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.2/1.2.1.2 Flight Control System Backup Mode** — allocation: LS-59 traces to function 'Set New Flight Path' allocated to block 'Flight Controlller'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.3.1/1.2.1.3.1 Navigation System Backup Mode Switching** — allocation: LS-59 traces to function 'Provide Required Waypoint Navigation Path' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.3/1.2.1.3 Navigation System Backup Mode** — allocation: LS-59 traces to function 'Provide Required Waypoint Navigation Path' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1/1.2.1 Flight Critical Subsystem Backup Mode** — allocation: LS-59 traces to function 'Launch UAV' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.2/1.2.2 Communications Loss Response** — allocation: LS-59 traces to function 'Load Flight Plan and Mission Parameters' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.4.1/1.2.4.1 ELINT Sensors on when Needed** — allocation: LS-59 traces to function 'Load Flight Plan and Mission Parameters' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.4/1.2.4 Mission Critical Subsystem Resilience** — allocation: LS-59 traces to function 'Launch UAV' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.3.4/1.3.4 System Zeroize** — allocation: LS-59 traces to function 'Launch UAV' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.4.1.1/1.4.1.1 Software Loading** — allocation: LS-59 traces to function 'Launch UAV' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.4.1.2/1.4.1.2 Software Loading Switch** — allocation: LS-59 traces to function 'Launch UAV' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.4.1/1.4.1 Single Maintenance Port** — allocation: LS-59 traces to function 'Launch UAV' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 29/59 HT-3 Report Unauthorized Data Detection** — allocation: LS-59 traces to function 'Launch UAV' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
- ATT&CK techniques (heuristic):
  - [medium 0.6] **Valid Accounts:T1078** — curated hint in cyber.py: phrase 'insider' → T1078 (heuristic)
  - [medium 0.6] **Private Keys:T1552.004** — curated hint in cyber.py: phrase 'command link key' → T1552.004 (heuristic)
  - [medium 0.6] **Adversary-in-the-Middle:T1557** — curated hint in cyber.py: phrase 'command link key' → T1557 (heuristic)
- D3FEND countermeasures (heuristic, via D3FEND associations):
  - [medium] **Agent Authentication** (Harden, direct) — D3FEND: 'Agent Authentication' May Harden T1078
  - [medium] **Credential Eviction** (Evict, direct) — D3FEND: 'Credential Eviction' May Evict T1078
  - [medium] **Credential Hardening** (Harden, direct) — D3FEND: 'Credential Hardening' May Harden T1078
  - [medium] **Multi-factor Authentication** (Harden, direct) — D3FEND: 'Multi-factor Authentication' May Harden T1078
  - [medium] **Restore Access** (Restore, direct) — D3FEND: 'Restore Access' May Restore T1078
  - [medium] **User Behavior Analysis** (Detect, direct) — D3FEND: 'User Behavior Analysis' May Detect T1552.004 (via parent technique T1552)
- D3FEND artifacts the Allocated Baseline already traces to on this path (model Trace links): Actuator (1), Bus Message (1), Bus Network (1), Bus Network Frame (1), Bus Network Traffic (1), Call Stack (1), Central Processing Unit (1), Client Computer (1) from block(s) Allocated Flight Control Computer
- Candidate NIST SP 800-53r5 controls: AC-2, AC-2(1), AC-2(12), AU-6, CP-10, IA-11, IA-2, IA-2(1), IA-2(2), IA-2(6), IA-3, IA-5, IA-5(1), IA-8, SI-4(13)

### 14. Adversary maliciously modifies flight-critical software during distribution to modify AV mission computer

- P=0.02–0.15, TotalRiskSensitivity=0.00845, gate path: (linked from LS-15, outside the tree)
- Loss scenario(s): LS-15 Adversary gains access to the mission computer through a supply chain attack during distribution and maliciously alters hardware or firmware
- HCAs: HCA-183, HCA-121, HCA-122, HCA-123, HCA-124, HCA-125, HCA-126, HCA-127 (+133); hazards: H-2, H-6, H-1, H-3, H-4, H-5; losses: L-1, L-2, L-3, L-4
- Controllers: C-7 Mission Computer, C-15 Stores Controller, C-8 Autopilot, C-30 Cyber Sentinel, C-9 Flight Control Computer, C-2 Operator, C-3 Flight Lead, C-10 Navigation Controller, C-11 Communications Controller, C-4 Ground Control Station
- Requirements (500 further non-cyber requirements share the same allocation paths):
  - [medium] **MR - 26.1.1.1/1.1.1.1 Mission Computer Secure Boot** — allocation+text: LS-15 traces to function 'Power up Mission Computer Components' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only); proposed: the requirement text shares ['computer', 'firmware'] with the leaf (heuristic, not a model link)
  - [low] **MR - 26.1.1.13/1.1.1.13 Electrical System Cryptographic Module** — allocation: LS-15 traces to function 'Power up Mission Computer Components' allocated to block 'Electrical System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.15/1.1.1.15 Mission Computer Maintenance Ports** — allocation: LS-15 traces to function 'Power up Mission Computer Components' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.16/1.1.1.16 Flight Control System Maintenance Ports** — allocation: LS-15 traces to function 'Provide Engine Thrust Requirements' allocated to block 'Flight Controlller'; requirement Allocate → that block (same subsystem only)
  - [medium] **MR - 26.1.1.2/1.1.1.2 Flight Control system Secure Boot** — allocation+text: LS-15 traces to function 'Provide Engine Thrust Requirements' allocated to block 'Flight Controlller'; requirement Allocate → that block (same subsystem only); proposed: the requirement text shares ['firmware', 'flight'] with the leaf (heuristic, not a model link)
  - [low] **MR - 26.1.1.20/1.1.1.20 Electrical System Maintenance Ports** — allocation: LS-15 traces to function 'Power up Mission Computer Components' allocated to block 'Electrical System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.6/1.1.1.6 Electrical System Secure Boot** — allocation: LS-15 traces to function 'Power up Mission Computer Components' allocated to block 'Electrical System'; requirement Allocate → that block (same subsystem only)
  - [medium] **MR - 26.1.1.8/1.1.1.8 Mission Computer Cryptographic Module** — allocation+text: LS-15 traces to function 'Power up Mission Computer Components' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only); proposed: the requirement text shares ['computer', 'hardware'] with the leaf (heuristic, not a model link)
  - [medium] **MR - 26.1.1.9/1.1.1.9 Flight Control System Cryptographic Module** — allocation+text: LS-15 traces to function 'Provide Engine Thrust Requirements' allocated to block 'Flight Controlller'; requirement Allocate → that block (same subsystem only); proposed: the requirement text shares ['flight', 'hardware'] with the leaf (heuristic, not a model link)
  - [medium] **MR - 26.1.1/1.1.1 Flight Critical Hardware Assurance** — allocation+text: LS-15 traces to function 'Power Up Essential Systems' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only); proposed: the requirement text shares ['critical', 'flight', 'hardware'] with the leaf (heuristic, not a model link)
  - [low] **MR - 26.2.1.1.1/1.2.1.1.1 Mission Computer Backup Mode Switching** — allocation: LS-15 traces to function 'Power up Mission Computer Components' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.1/1.2.1.1 Mission Computer Backup Mode** — allocation: LS-15 traces to function 'Power up Mission Computer Components' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.2.1/1.2.1.2.1 Flight Control System Backup Mode Switching** — allocation: LS-15 traces to function 'Provide Engine Thrust Requirements' allocated to block 'Flight Controlller'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.2/1.2.1.2 Flight Control System Backup Mode** — allocation: LS-15 traces to function 'Provide Engine Thrust Requirements' allocated to block 'Flight Controlller'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.6.1/1.2.1.6.1 Electrical System Backup Mode Switching** — allocation: LS-15 traces to function 'Power up Mission Computer Components' allocated to block 'Electrical System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.6/1.2.1.6 Electrical System Backup Mode** — allocation: LS-15 traces to function 'Power up Mission Computer Components' allocated to block 'Electrical System'; requirement Allocate → that block (same subsystem only)
  - [medium] **MR - 26.2.1/1.2.1 Flight Critical Subsystem Backup Mode** — allocation+text: LS-15 traces to function 'Power Up Essential Systems' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only); proposed: the requirement text shares ['critical', 'flight'] with the leaf (heuristic, not a model link)
  - [low] **MR - 26.2.2/1.2.2 Communications Loss Response** — allocation: LS-15 traces to function 'Power up Mission Computer Components' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.4.1/1.2.4.1 ELINT Sensors on when Needed** — allocation: LS-15 traces to function 'Power up Mission Computer Components' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.4/1.2.4 Mission Critical Subsystem Resilience** — allocation: LS-15 traces to function 'Power Up Essential Systems' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.3.4/1.3.4 System Zeroize** — allocation: LS-15 traces to function 'Power Up Essential Systems' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [medium] **MR - 26.4.1.1/1.4.1.1 Software Loading** — allocation+text: LS-15 traces to function 'Power Up Essential Systems' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only); proposed: the requirement text shares ['firmware', 'flight', 'software'] with the leaf (heuristic, not a model link)
  - [medium] **MR - 26.4.1.2/1.4.1.2 Software Loading Switch** — allocation+text: LS-15 traces to function 'Power Up Essential Systems' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only); proposed: the requirement text shares ['flight', 'software'] with the leaf (heuristic, not a model link)
  - [low] **MR - 26.4.1/1.4.1 Single Maintenance Port** — allocation: LS-15 traces to function 'Power Up Essential Systems' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 29/59 HT-3 Report Unauthorized Data Detection** — allocation: LS-15 traces to function 'Power Up Essential Systems' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 113/143 CSA-10 10.1** — lexical: proposed: shared terms ['firmware', 'hardware', 'software'] (text overlap, not a model relationship)
  - [low] **MR - 98/128 CSA-04 4.3** — lexical: proposed: shared terms ['firmware', 'hardware', 'software'] (text overlap, not a model relationship)
  - [low] **MR - 26.1.3/1.1.3 Software Bill of Materials** — lexical: proposed: shared terms ['firmware', 'software'] (text overlap, not a model relationship)
  - [low] **MR - 26.4.2.1/1.4.2.1 Maintenance System Complete Load** — lexical: proposed: shared terms ['firmware', 'software'] (text overlap, not a model relationship)
  - [low] **MR - 26.4.2.2/1.4.2.2 Maintenance System Partial Load** — lexical: proposed: shared terms ['firmware', 'software'] (text overlap, not a model relationship)
- ATT&CK techniques (heuristic):
  - [medium 0.87] **Compromise Hardware Supply Chain:T1195.003** — name tokens ['chain', 'hardware', 'supply'] overlap; documentation also mentions ['firmware', 'modify']
  - [medium 0.86] **Compromise Software Supply Chain:T1195.002** — name tokens ['chain', 'software', 'supply'] overlap; documentation also mentions ['distribution', 'modifi']
  - [medium 0.6] **Supply Chain Compromise:T1195** — curated hint in cyber.py: phrase 'supply chain' → T1195 (heuristic)
- D3FEND countermeasures (heuristic, via D3FEND associations):
  - [medium] **Asset Inventory** (Model, direct) — D3FEND: 'Asset Inventory' May Model T1195.003
  - [medium] **Asset Vulnerability Enumeration** (Model, direct) — D3FEND: 'Asset Vulnerability Enumeration' May Model T1195.002
  - [medium] **Container Image Analysis** (Model, direct) — D3FEND: 'Container Image Analysis' May Model T1195.002
  - [medium] **Hardware Component Inventory** (Model, direct) — D3FEND: 'Hardware Component Inventory' May Model T1195.003
  - [medium] **Platform Hardening** (Harden, direct) — D3FEND: 'Platform Hardening' May Harden T1195.002
  - [medium] **Restore Object** (Restore, direct) — D3FEND: 'Restore Object' May Restore T1195.002
- D3FEND artifacts the Allocated Baseline already traces to on this path (model Trace links): Actuator (1), Bus Message (1), Bus Network (1), Bus Network Frame (1), Bus Network Traffic (1), Call Stack (1), Central Processing Unit (1), Client Computer (1) from block(s) Allocated Flight Control Computer
- Candidate NIST SP 800-53r5 controls: CM-2, CM-6, CM-7, CM-8, CM-8(1), CP-10, CP-9, RA-5, RA-5(2), SI-7

### 15. Adversary substitutes flight-critical hardware during distribution to alter AV navigation system

- P=0.01–0.15, TotalRiskSensitivity=0.003858, gate path: (linked from LS-25, outside the tree)
- Loss scenario(s): LS-25 Adversary gains access to the navigation controller through a supply chain distribution attack and maliciously alters hardware or firmware to spoof or tamper navigation controller commands
- HCAs: HCA-228, HCA-241, HCA-240, HCA-239, HCA-238, HCA-237, HCA-236, HCA-235 (+13); hazards: H-1, H-2, H-3, H-4; losses: L-1, L-2, L-3, L-4
- Controllers: C-10 Navigation Controller, C-30 Cyber Sentinel, C-7 Mission Computer
- Requirements (86 further non-cyber requirements share the same allocation paths):
  - [medium] **MR - 26.1.1.10/1.1.1.10 Navigation System Cryptographic Module** — allocation+text: LS-25 traces to function 'Provide Required Waypoint Navigation Path' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only); proposed: the requirement text shares ['hardware', 'navigation'] with the leaf (heuristic, not a model link)
  - [low] **MR - 26.1.1.17/1.1.1.17 Navigation System Maintenance Ports** — allocation: LS-25 traces to function 'Provide Required Waypoint Navigation Path' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [medium] **MR - 26.1.1.3/1.1.1.3 Navigation System Secure Boot** — allocation+text: LS-25 traces to function 'Provide Required Waypoint Navigation Path' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only); proposed: the requirement text shares ['firmware', 'navigation'] with the leaf (heuristic, not a model link)
  - [medium] **MR - 26.1.1/1.1.1 Flight Critical Hardware Assurance** — allocation+text: LS-25 traces to function 'Fly UAS Based on Waypoint Data' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only); proposed: the requirement text shares ['critical', 'flight', 'hardware'] with the leaf (heuristic, not a model link)
  - [medium] **MR - 26.2.1.3.1/1.2.1.3.1 Navigation System Backup Mode Switching** — allocation+text: LS-25 traces to function 'Provide Required Waypoint Navigation Path' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only); proposed: the requirement text shares ['command', 'navigation'] with the leaf (heuristic, not a model link)
  - [low] **MR - 26.2.1.3/1.2.1.3 Navigation System Backup Mode** — allocation: LS-25 traces to function 'Provide Required Waypoint Navigation Path' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [medium] **MR - 26.2.1/1.2.1 Flight Critical Subsystem Backup Mode** — allocation+text: LS-25 traces to function 'Fly UAS Based on Waypoint Data' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only); proposed: the requirement text shares ['critical', 'flight'] with the leaf (heuristic, not a model link)
  - [low] **MR - 26.2.4/1.2.4 Mission Critical Subsystem Resilience** — allocation: LS-25 traces to function 'Fly UAS Based on Waypoint Data' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.3.4/1.3.4 System Zeroize** — allocation: LS-25 traces to function 'Fly UAS Based on Waypoint Data' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.4.1.1/1.4.1.1 Software Loading** — allocation: LS-25 traces to function 'Fly UAS Based on Waypoint Data' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.4.1.2/1.4.1.2 Software Loading Switch** — allocation: LS-25 traces to function 'Fly UAS Based on Waypoint Data' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.4.1/1.4.1 Single Maintenance Port** — allocation: LS-25 traces to function 'Fly UAS Based on Waypoint Data' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 29/59 HT-3 Report Unauthorized Data Detection** — allocation: LS-25 traces to function 'Fly UAS Based on Waypoint Data' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 98/128 CSA-04 4.3** — lexical: proposed: shared terms ['firmware', 'hardware', 'tamper'] (text overlap, not a model relationship)
  - [low] **MR - 26.3.1.7/1.3.1.7 Cyber Sentinel Switching Components to Backup Mode on Command** — lexical: proposed: shared terms ['command', 'critical', 'flight'] (text overlap, not a model relationship)
  - [low] **MR - 26.1.5.2.4/1.1.5.2.4 Ground Station Access Logging** — lexical: proposed: shared terms ['acces', 'critical', 'tamper'] (text overlap, not a model relationship)
  - [low] **MR - 26.1.5.3.4/1.1.5.3.4 Maintenance System Access Logging** — lexical: proposed: shared terms ['acces', 'critical', 'tamper'] (text overlap, not a model relationship)
  - [low] **MR - 81/111 CSA-01 Control Access** — lexical: proposed: shared terms ['acces', 'critical', 'tamper'] (text overlap, not a model relationship)
- ATT&CK techniques (heuristic):
  - [medium 0.82] **Compromise Hardware Supply Chain:T1195.003** — name tokens ['chain', 'hardware', 'supply'] overlap; documentation also mentions ['firmware']
  - [medium 0.6] **Masquerading:T1036** — curated hint in cyber.py: phrase 'spoof' → T1036 (heuristic)
  - [medium 0.6] **Supply Chain Compromise:T1195** — curated hint in cyber.py: phrase 'supply chain' → T1195 (heuristic)
- D3FEND countermeasures (heuristic, via D3FEND associations):
  - [medium] **Asset Inventory** (Model, direct) — D3FEND: 'Asset Inventory' May Model T1195.003
  - [medium] **Hardware Component Inventory** (Model, direct) — D3FEND: 'Hardware Component Inventory' May Model T1195.003
- D3FEND artifacts the Allocated Baseline already traces to on this path (model Trace links): Bus Message (1), Bus Network (1), Bus Network Frame (1), Bus Network Traffic (1), Central Processing Unit (1), Client Computer (1), Command (1), Computer Platform (1) from block(s) Allocated Nav Controller
- Candidate NIST SP 800-53r5 controls: CM-8, CM-8(1)

### 16. Adversary maliciously modifies flight-critical software during development to alter AV mission computer

- P=0.01–0.12, TotalRiskSensitivity=0.005746, gate path: (linked from LS-16, outside the tree)
- Loss scenario(s): LS-16 Adversary maliciously modifies the mission computer's OFP during development to spoof or tamper mission computer commands
- HCAs: HCA-183, HCA-121, HCA-122, HCA-123, HCA-124, HCA-125, HCA-126, HCA-127 (+133); hazards: H-2, H-6, H-1, H-3, H-4, H-5; losses: L-1, L-2, L-3, L-4
- Controllers: C-7 Mission Computer, C-15 Stores Controller, C-8 Autopilot, C-30 Cyber Sentinel, C-9 Flight Control Computer, C-2 Operator, C-3 Flight Lead, C-10 Navigation Controller, C-11 Communications Controller, C-4 Ground Control Station
- Requirements (119 further non-cyber requirements share the same allocation paths):
  - [low] **MR - 26.1.1.1/1.1.1.1 Mission Computer Secure Boot** — allocation: LS-16 traces to function 'Initialize OFP Transfer Process' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.13/1.1.1.13 Electrical System Cryptographic Module** — allocation: LS-16 traces to function 'Power up Mission Computer Components' allocated to block 'Electrical System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.15/1.1.1.15 Mission Computer Maintenance Ports** — allocation: LS-16 traces to function 'Initialize OFP Transfer Process' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.20/1.1.1.20 Electrical System Maintenance Ports** — allocation: LS-16 traces to function 'Power up Mission Computer Components' allocated to block 'Electrical System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.6/1.1.1.6 Electrical System Secure Boot** — allocation: LS-16 traces to function 'Power up Mission Computer Components' allocated to block 'Electrical System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.8/1.1.1.8 Mission Computer Cryptographic Module** — allocation: LS-16 traces to function 'Initialize OFP Transfer Process' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [medium] **MR - 26.1.1/1.1.1 Flight Critical Hardware Assurance** — allocation+text: LS-16 traces to function 'Load OFPs' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only); proposed: the requirement text shares ['critical', 'flight'] with the leaf (heuristic, not a model link)
  - [medium] **MR - 26.2.1.1.1/1.2.1.1.1 Mission Computer Backup Mode Switching** — allocation+text: LS-16 traces to function 'Initialize OFP Transfer Process' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only); proposed: the requirement text shares ['command', 'computer'] with the leaf (heuristic, not a model link)
  - [low] **MR - 26.2.1.1/1.2.1.1 Mission Computer Backup Mode** — allocation: LS-16 traces to function 'Initialize OFP Transfer Process' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.6.1/1.2.1.6.1 Electrical System Backup Mode Switching** — allocation: LS-16 traces to function 'Power up Mission Computer Components' allocated to block 'Electrical System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.6/1.2.1.6 Electrical System Backup Mode** — allocation: LS-16 traces to function 'Power up Mission Computer Components' allocated to block 'Electrical System'; requirement Allocate → that block (same subsystem only)
  - [medium] **MR - 26.2.1/1.2.1 Flight Critical Subsystem Backup Mode** — allocation+text: LS-16 traces to function 'Load OFPs' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only); proposed: the requirement text shares ['critical', 'flight'] with the leaf (heuristic, not a model link)
  - [low] **MR - 26.2.2/1.2.2 Communications Loss Response** — allocation: LS-16 traces to function 'Initialize OFP Transfer Process' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.4.1/1.2.4.1 ELINT Sensors on when Needed** — allocation: LS-16 traces to function 'Initialize OFP Transfer Process' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.4/1.2.4 Mission Critical Subsystem Resilience** — allocation: LS-16 traces to function 'Load OFPs' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.3.4/1.3.4 System Zeroize** — allocation: LS-16 traces to function 'Load OFPs' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [medium] **MR - 26.4.1.1/1.4.1.1 Software Loading** — allocation+text: LS-16 traces to function 'Load OFPs' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only); proposed: the requirement text shares ['flight', 'software'] with the leaf (heuristic, not a model link)
  - [medium] **MR - 26.4.1.2/1.4.1.2 Software Loading Switch** — allocation+text: LS-16 traces to function 'Load OFPs' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only); proposed: the requirement text shares ['flight', 'software', 'spoof'] with the leaf (heuristic, not a model link)
  - [low] **MR - 26.4.1/1.4.1 Single Maintenance Port** — allocation: LS-16 traces to function 'Load OFPs' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 29/59 HT-3 Report Unauthorized Data Detection** — allocation: LS-16 traces to function 'Load OFPs' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.3.1.7/1.3.1.7 Cyber Sentinel Switching Components to Backup Mode on Command** — lexical: proposed: shared terms ['command', 'critical', 'flight'] (text overlap, not a model relationship)
  - [low] **MR - 26.3.1.5/1.3.1.5 Cyber Sentinel Resetting Components on Command** — lexical: proposed: shared terms ['command', 'critical'] (text overlap, not a model relationship)
  - [low] **MR - 26.1.5.2.4/1.1.5.2.4 Ground Station Access Logging** — lexical: proposed: shared terms ['critical', 'tamper'] (text overlap, not a model relationship)
  - [low] **MR - 26.1.5.3.4/1.1.5.3.4 Maintenance System Access Logging** — lexical: proposed: shared terms ['critical', 'tamper'] (text overlap, not a model relationship)
  - [low] **MR - 26.1.8/1.1.8 Digital Signatures on OFPs** — lexical: proposed: shared terms ['flight', 'software'] (text overlap, not a model relationship)
- ATT&CK techniques (heuristic):
  - [medium 0.6] **Masquerading:T1036** — curated hint in cyber.py: phrase 'spoof' → T1036 (heuristic)
  - [medium 0.6] **Adversary-in-the-Middle:T1557** — curated hint in cyber.py: phrase 'spoof' → T1557 (heuristic)
  - [low 1.0] **Software:T1592.002** — name tokens ['software'] overlap (single-word technique name: capped at low)
- D3FEND countermeasures (heuristic, via D3FEND associations):
  - [medium] **Client-server Payload Profiling** (Detect, direct) — D3FEND: 'Client-server Payload Profiling' May Detect T1557
  - [medium] **Network Isolation** (Isolate, direct) — D3FEND: 'Network Isolation' May Isolate T1557
  - [medium] **Network Traffic Analysis** (Detect, direct) — D3FEND: 'Network Traffic Analysis' May Detect T1557
  - [medium] **Network Traffic Community Deviation** (Detect, direct) — D3FEND: 'Network Traffic Community Deviation' May Detect T1557
  - [medium] **Network Traffic Filtering** (Isolate, direct) — D3FEND: 'Network Traffic Filtering' May Isolate T1557
  - [medium] **Network Traffic Signature Analysis** (Detect, direct) — D3FEND: 'Network Traffic Signature Analysis' May Detect T1557
- Candidate NIST SP 800-53r5 controls: AC-4, AU-6, SC-32, SC-7, SC-7(21), SC-7(5), SI-3, SI-4, SI-4(11), SI-4(4)

### 17. Adversary breaks encryption to determine the command link key to fly UAS to adversary selected location

- P=0.001–0.04, TotalRiskSensitivity=0.020969, gate path: Or Adversary sends malicious commands to AV to fly AV to adversary selected location → Or Adversary gets into the middle of ground station & UAS communications link to fly AV to adversary selected location → Or Adversary gets encryption key to fly AV to adversary selected location
- Loss scenario(s): LS-8 Adversary gains access to the ground station AV link through breaking encryption and performs a man-in-the-middle attack to alter commands and data sent to the AV to fly AV to a location of the adversary's choosing
- HCAs: HCA-40, HCA-28, HCA-9, HCA-21, HCA-55, HCA-126; hazards: H-1, H-2, H-3, H-4; losses: L-1, L-2, L-3, L-4
- Controllers: C-2 Operator, C-4 Ground Control Station, C-7 Mission Computer, C-8 Autopilot
- Requirements (412 further non-cyber requirements share the same allocation paths):
  - [low] **MR - 26.1.1.1/1.1.1.1 Mission Computer Secure Boot** — allocation: LS-8 traces to function 'Process Waypoint Path' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [medium] **MR - 26.1.1.10/1.1.1.10 Navigation System Cryptographic Module** — allocation+text: LS-8 traces to function 'Provide Required Waypoint Navigation Path' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only); proposed: the requirement text shares ['encryption', 'key'] with the leaf (heuristic, not a model link)
  - [medium] **MR - 26.1.1.14/1.1.1.14 Communications System Cryptographic Module** — allocation+text: LS-8 traces to function 'Activate GCS Interface' allocated to block 'Communications System'; requirement Allocate → that block (same subsystem only); proposed: the requirement text shares ['encryption', 'key'] with the leaf (heuristic, not a model link)
  - [low] **MR - 26.1.1.15/1.1.1.15 Mission Computer Maintenance Ports** — allocation: LS-8 traces to function 'Process Waypoint Path' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.17/1.1.1.17 Navigation System Maintenance Ports** — allocation: LS-8 traces to function 'Provide Required Waypoint Navigation Path' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.21/1.1.1.21 Communications System Mainteanance Ports** — allocation: LS-8 traces to function 'Activate GCS Interface' allocated to block 'Communications System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.3/1.1.1.3 Navigation System Secure Boot** — allocation: LS-8 traces to function 'Provide Required Waypoint Navigation Path' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.7/1.1.1.7 Communications System Secure Boot** — allocation: LS-8 traces to function 'Activate GCS Interface' allocated to block 'Communications System'; requirement Allocate → that block (same subsystem only)
  - [medium] **MR - 26.1.1.8/1.1.1.8 Mission Computer Cryptographic Module** — allocation+text: LS-8 traces to function 'Process Waypoint Path' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only); proposed: the requirement text shares ['encryption', 'key'] with the leaf (heuristic, not a model link)
  - [low] **MR - 26.1.1/1.1.1 Flight Critical Hardware Assurance** — allocation: LS-8 traces to function 'Fly UAS Based on Waypoint Data' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.6/1.1.6 Communications Encryption** — allocation: LS-8 traces to function 'Activate GCS Interface' allocated to block 'Communications System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.1.1/1.2.1.1.1 Mission Computer Backup Mode Switching** — allocation: LS-8 traces to function 'Process Waypoint Path' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.1/1.2.1.1 Mission Computer Backup Mode** — allocation: LS-8 traces to function 'Process Waypoint Path' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.3.1/1.2.1.3.1 Navigation System Backup Mode Switching** — allocation: LS-8 traces to function 'Provide Required Waypoint Navigation Path' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.3/1.2.1.3 Navigation System Backup Mode** — allocation: LS-8 traces to function 'Provide Required Waypoint Navigation Path' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.7.1/1.2.1.7.1 Communications System Backup Mode Switching** — allocation: LS-8 traces to function 'Activate GCS Interface' allocated to block 'Communications System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.7/1.2.1.7 Communications System Backup Mode** — allocation: LS-8 traces to function 'Activate GCS Interface' allocated to block 'Communications System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1/1.2.1 Flight Critical Subsystem Backup Mode** — allocation: LS-8 traces to function 'Fly UAS Based on Waypoint Data' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.2/1.2.2 Communications Loss Response** — allocation: LS-8 traces to function 'Process Waypoint Path' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.3/1.2.3 Communications Redundancy** — allocation: LS-8 traces to function 'Activate GCS Interface' allocated to block 'Communications System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.4.1/1.2.4.1 ELINT Sensors on when Needed** — allocation: LS-8 traces to function 'Process Waypoint Path' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.4/1.2.4 Mission Critical Subsystem Resilience** — allocation: LS-8 traces to function 'Fly UAS Based on Waypoint Data' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.3.4/1.3.4 System Zeroize** — allocation: LS-8 traces to function 'Fly UAS Based on Waypoint Data' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.4.1.1/1.4.1.1 Software Loading** — allocation: LS-8 traces to function 'Fly UAS Based on Waypoint Data' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.4.1.2/1.4.1.2 Software Loading Switch** — allocation: LS-8 traces to function 'Fly UAS Based on Waypoint Data' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.4.1/1.4.1 Single Maintenance Port** — allocation: LS-8 traces to function 'Fly UAS Based on Waypoint Data' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 29/59 HT-3 Report Unauthorized Data Detection** — allocation: LS-8 traces to function 'Fly UAS Based on Waypoint Data' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.5.2.1/1.1.5.2.1 Ground Station MFA** — lexical: proposed: shared terms ['acces', 'data', 'ground', 'station'] (text overlap, not a model relationship)
  - [low] **MR - 26.3.1.5/1.3.1.5 Cyber Sentinel Resetting Components on Command** — lexical: proposed: shared terms ['command', 'ground', 'station'] (text overlap, not a model relationship)
  - [low] **MR - 26.3.1.7/1.3.1.7 Cyber Sentinel Switching Components to Backup Mode on Command** — lexical: proposed: shared terms ['command', 'ground', 'station'] (text overlap, not a model relationship)
  - [low] **MR - 26.1.5.2.2/1.1.5.2.2 Ground Station Role Based Access Control** — lexical: proposed: shared terms ['acces', 'ground', 'station'] (text overlap, not a model relationship)
  - [low] **MR - 26.1.5.2.4/1.1.5.2.4 Ground Station Access Logging** — lexical: proposed: shared terms ['acces', 'ground', 'station'] (text overlap, not a model relationship)
- ATT&CK techniques (heuristic):
  - [medium 1.05] **Data Encrypted:T1022** — name tokens ['data', 'encryption'] overlap; documentation also mentions ['command']
  - [medium 0.6] **Private Keys:T1552.004** — curated hint in cyber.py: phrase 'command link key' → T1552.004 (heuristic)
  - [medium 0.6] **Adversary-in-the-Middle:T1557** — curated hint in cyber.py: phrase 'man-in-the-middle' → T1557 (heuristic)
- D3FEND countermeasures (heuristic, via D3FEND associations):
  - [medium] **User Behavior Analysis** (Detect, direct) — D3FEND: 'User Behavior Analysis' May Detect T1552.004 (via parent technique T1552)
  - [medium] **Access Mediation** (Isolate, direct) — D3FEND: 'Access Mediation' May Isolate T1552.004 (via parent technique T1552)
  - [medium] **Agent Authentication** (Harden, direct) — D3FEND: 'Agent Authentication' May Harden T1552.004 (via parent technique T1552)
  - [medium] **Authentication Cache Invalidation** (Evict, direct) — D3FEND: 'Authentication Cache Invalidation' May Evict T1552.004 (via parent technique T1552)
  - [medium] **Certificate Rotation** (Harden, direct) — D3FEND: 'Certificate Rotation' May Harden T1552.004 (via parent technique T1552)
  - [medium] **Client-server Payload Profiling** (Detect, direct) — D3FEND: 'Client-server Payload Profiling' May Detect T1557
- D3FEND artifacts the Allocated Baseline already traces to on this path (model Trace links): Application Layer Link (1), Asymmetric Key (1), Bus Message (1), Bus Network (1), Bus Network Frame (1), Bus Network Traffic (1), CA Certificate File (1), Call Stack (1) from block(s) Allocated Communications Controller
- Candidate NIST SP 800-53r5 controls: AC-2(12), AC-3, AC-6, AU-6, IA-11, IA-2, IA-3, IA-5, IA-5(1), IA-8, SI-4(11), SI-4(13), SI-4(4)

### 18. Adversary supply chain attack on MX system provides logical access to maliciously alter AV mission computer

- P=0.0001–0.001, TotalRiskSensitivity=0.000799, gate path: (linked from LS-14, outside the tree)
- Loss scenario(s): LS-14 Adversary gains access to the MX system through a supply chain attack and maliciously alters hardware or firmware to spoof or tamper OFPs loaded in the AV to modify the mission computer
- HCAs: HCA-303, HCA-304; hazards: H-1, H-2, H-3, H-4, H-5, H-6; losses: L-1, L-2, L-3, L-4
- Controllers: C-5 Maintenance System
- Requirements (234 further non-cyber requirements share the same allocation paths):
  - [medium] **MR - 26.1.1.1/1.1.1.1 Mission Computer Secure Boot** — allocation+text: LS-14 traces to function 'Initialize OFP Transfer Process' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only); proposed: the requirement text shares ['computer', 'firmware'] with the leaf (heuristic, not a model link)
  - [low] **MR - 26.1.1.10/1.1.1.10 Navigation System Cryptographic Module** — allocation: LS-14 traces to function 'Provide Processed Sensor Data to Mission Computer' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.13/1.1.1.13 Electrical System Cryptographic Module** — allocation: LS-14 traces to function 'Power up Mission Computer Components' allocated to block 'Electrical System'; requirement Allocate → that block (same subsystem only)
  - [medium] **MR - 26.1.1.15/1.1.1.15 Mission Computer Maintenance Ports** — allocation+text: LS-14 traces to function 'Initialize OFP Transfer Process' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only); proposed: the requirement text shares ['computer', 'maintenance'] with the leaf (heuristic, not a model link)
  - [low] **MR - 26.1.1.17/1.1.1.17 Navigation System Maintenance Ports** — allocation: LS-14 traces to function 'Provide Processed Sensor Data to Mission Computer' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.20/1.1.1.20 Electrical System Maintenance Ports** — allocation: LS-14 traces to function 'Power up Mission Computer Components' allocated to block 'Electrical System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.3/1.1.1.3 Navigation System Secure Boot** — allocation: LS-14 traces to function 'Provide Processed Sensor Data to Mission Computer' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.1.1.6/1.1.1.6 Electrical System Secure Boot** — allocation: LS-14 traces to function 'Power up Mission Computer Components' allocated to block 'Electrical System'; requirement Allocate → that block (same subsystem only)
  - [medium] **MR - 26.1.1.8/1.1.1.8 Mission Computer Cryptographic Module** — allocation+text: LS-14 traces to function 'Initialize OFP Transfer Process' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only); proposed: the requirement text shares ['computer', 'hardware'] with the leaf (heuristic, not a model link)
  - [medium] **MR - 26.1.1/1.1.1 Flight Critical Hardware Assurance** — allocation+text: LS-14 traces to function 'Load OFPs' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only); proposed: the requirement text shares ['hardware', 'maintenance'] with the leaf (heuristic, not a model link)
  - [low] **MR - 26.2.1.1.1/1.2.1.1.1 Mission Computer Backup Mode Switching** — allocation: LS-14 traces to function 'Initialize OFP Transfer Process' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.1/1.2.1.1 Mission Computer Backup Mode** — allocation: LS-14 traces to function 'Initialize OFP Transfer Process' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.3.1/1.2.1.3.1 Navigation System Backup Mode Switching** — allocation: LS-14 traces to function 'Provide Processed Sensor Data to Mission Computer' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.3/1.2.1.3 Navigation System Backup Mode** — allocation: LS-14 traces to function 'Provide Processed Sensor Data to Mission Computer' allocated to block 'Navigation System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.6.1/1.2.1.6.1 Electrical System Backup Mode Switching** — allocation: LS-14 traces to function 'Power up Mission Computer Components' allocated to block 'Electrical System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1.6/1.2.1.6 Electrical System Backup Mode** — allocation: LS-14 traces to function 'Power up Mission Computer Components' allocated to block 'Electrical System'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.1/1.2.1 Flight Critical Subsystem Backup Mode** — allocation: LS-14 traces to function 'Load OFPs' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.2/1.2.2 Communications Loss Response** — allocation: LS-14 traces to function 'Initialize OFP Transfer Process' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.4.1/1.2.4.1 ELINT Sensors on when Needed** — allocation: LS-14 traces to function 'Initialize OFP Transfer Process' allocated to block 'Executive Control Subsystem'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.2.4/1.2.4 Mission Critical Subsystem Resilience** — allocation: LS-14 traces to function 'Load OFPs' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.3.4/1.3.4 System Zeroize** — allocation: LS-14 traces to function 'Load OFPs' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [medium] **MR - 26.4.1.1/1.4.1.1 Software Loading** — allocation+text: LS-14 traces to function 'Load OFPs' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only); proposed: the requirement text shares ['firmware', 'load', 'maintenance', 'software'] with the leaf (heuristic, not a model link)
  - [medium] **MR - 26.4.1.2/1.4.1.2 Software Loading Switch** — allocation+text: LS-14 traces to function 'Load OFPs' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only); proposed: the requirement text shares ['load', 'maintenance', 'software', 'spoof'] with the leaf (heuristic, not a model link)
  - [low] **MR - 26.4.1/1.4.1 Single Maintenance Port** — allocation: LS-14 traces to function 'Load OFPs' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 29/59 HT-3 Report Unauthorized Data Detection** — allocation: LS-14 traces to function 'Load OFPs' allocated to block 'MQ-99 Berserker Air Vehicle'; requirement Allocate → that block (same subsystem only)
  - [low] **MR - 26.4.2.1/1.4.2.1 Maintenance System Complete Load** — lexical: proposed: shared terms ['firmware', 'load', 'maintenance', 'software'] (text overlap, not a model relationship)
  - [low] **MR - 26.4.2.2/1.4.2.2 Maintenance System Partial Load** — lexical: proposed: shared terms ['firmware', 'load', 'maintenance', 'software'] (text overlap, not a model relationship)
  - [low] **MR - 98/128 CSA-04 4.3** — lexical: proposed: shared terms ['firmware', 'hardware', 'software', 'tamper'] (text overlap, not a model relationship)
  - [low] **MR - 81/111 CSA-01 Control Access** — lexical: proposed: shared terms ['acces', 'logical', 'maintenance', 'tamper'] (text overlap, not a model relationship)
  - [low] **MR - 113/143 CSA-10 10.1** — lexical: proposed: shared terms ['firmware', 'hardware', 'software'] (text overlap, not a model relationship)
- ATT&CK techniques (heuristic):
  - [medium 0.87] **Compromise Hardware Supply Chain:T1195.003** — name tokens ['chain', 'hardware', 'supply'] overlap; documentation also mentions ['firmware', 'modify']
  - [medium 0.76] **Compromise Software Supply Chain:T1195.002** — name tokens ['chain', 'software', 'supply'] overlap
  - [medium 0.6] **Masquerading:T1036** — curated hint in cyber.py: phrase 'spoof' → T1036 (heuristic)
- D3FEND countermeasures (heuristic, via D3FEND associations):
  - [medium] **Asset Inventory** (Model, direct) — D3FEND: 'Asset Inventory' May Model T1195.003
  - [medium] **Asset Vulnerability Enumeration** (Model, direct) — D3FEND: 'Asset Vulnerability Enumeration' May Model T1195.002
  - [medium] **Container Image Analysis** (Model, direct) — D3FEND: 'Container Image Analysis' May Model T1195.002
  - [medium] **Hardware Component Inventory** (Model, direct) — D3FEND: 'Hardware Component Inventory' May Model T1195.003
  - [medium] **Platform Hardening** (Harden, direct) — D3FEND: 'Platform Hardening' May Harden T1195.002
  - [medium] **Restore Object** (Restore, direct) — D3FEND: 'Restore Object' May Restore T1195.002
- Candidate NIST SP 800-53r5 controls: CM-2, CM-6, CM-7, CM-8, CM-8(1), CP-10, CP-9, RA-5, RA-5(2), SI-7

## Assurance case

37 requirement(s) in the chain; 37 with no assurance-case Goal/Evidence reference.

For context, the assurance case references 11 requirement(s) model-wide: G-10 System has sufficient and appropri… Satisfy 145 ; G-8 Appropriate CSAs have been built in… Satisfy 111 CSA-01 Control Access; G-8 Appropriate CSAs have been built in… Satisfy 112 CSA-02 Reduce System's Cyber Detectability; G-8 Appropriate CSAs have been built in… Satisfy 113 CSA-03 Secure Transmissions and Communications; G-8 Appropriate CSAs have been built in… Satisfy 114 CSA-04 Protect System's Information from Exploitation; G-8 Appropriate CSAs have been built in… Satisfy 115 CSA-05 Partition and Ensure Critical Functions at Missi…; G-8 Appropriate CSAs have been built in… Satisfy 116 CSA-06 Minimize and Harden Attack Surfaces; G-8 Appropriate CSAs have been built in… Satisfy 117 CSA-07 Baseline & Monitor Systems and Detect Anomalies; G-8 Appropriate CSAs have been built in… Satisfy 118 CSA-08 Manage System Performance and Enable Cyberspace …; G-8 Appropriate CSAs have been built in… Satisfy 119 CSA-09 Recover System Capabilities; G-8 Appropriate CSAs have been built in… Satisfy 120 CSA-10 Actively Manage System's Configurations to Achie….

| requirement | supported | by |
|---|---|---|
| MR - 26.1.1.1/1.1.1.1 Mission Computer Secure Boot | **no** | - |
| MR - 26.1.1.10/1.1.1.10 Navigation System Cryptographic Module | **no** | - |
| MR - 26.1.1.15/1.1.1.15 Mission Computer Maintenance Ports | **no** | - |
| MR - 26.1.1.16/1.1.1.16 Flight Control System Maintenance Ports | **no** | - |
| MR - 26.1.1.17/1.1.1.17 Navigation System Maintenance Ports | **no** | - |
| MR - 26.1.1.2/1.1.1.2 Flight Control system Secure Boot | **no** | - |
| MR - 26.1.1.3/1.1.1.3 Navigation System Secure Boot | **no** | - |
| MR - 26.1.1.8/1.1.1.8 Mission Computer Cryptographic Module | **no** | - |
| MR - 26.1.1.9/1.1.1.9 Flight Control System Cryptographic Module | **no** | - |
| MR - 26.1.1/1.1.1 Flight Critical Hardware Assurance | **no** | - |
| MR - 26.2.1.1.1/1.2.1.1.1 Mission Computer Backup Mode Switching | **no** | - |
| MR - 26.2.1.1/1.2.1.1 Mission Computer Backup Mode | **no** | - |
| MR - 26.2.1.2.1/1.2.1.2.1 Flight Control System Backup Mode Switching | **no** | - |
| MR - 26.2.1.2/1.2.1.2 Flight Control System Backup Mode | **no** | - |
| MR - 26.2.1.3.1/1.2.1.3.1 Navigation System Backup Mode Switching | **no** | - |
| MR - 26.2.1.3/1.2.1.3 Navigation System Backup Mode | **no** | - |
| MR - 26.2.1/1.2.1 Flight Critical Subsystem Backup Mode | **no** | - |
| MR - 26.2.2/1.2.2 Communications Loss Response | **no** | - |
| MR - 26.2.4.1/1.2.4.1 ELINT Sensors on when Needed | **no** | - |
| MR - 26.2.4/1.2.4 Mission Critical Subsystem Resilience | **no** | - |
| MR - 26.3.4/1.3.4 System Zeroize | **no** | - |
| MR - 26.4.1.1/1.4.1.1 Software Loading | **no** | - |
| MR - 26.4.1.2/1.4.1.2 Software Loading Switch | **no** | - |
| MR - 26.4.1/1.4.1 Single Maintenance Port | **no** | - |
| MR - 29/59 HT-3 Report Unauthorized Data Detection | **no** | - |
| MR - 26.1.1.14/1.1.1.14 Communications System Cryptographic Module | **no** | - |
| MR - 26.1.1.21/1.1.1.21 Communications System Mainteanance Ports | **no** | - |
| MR - 26.1.1.7/1.1.1.7 Communications System Secure Boot | **no** | - |
| MR - 26.1.6/1.1.6 Communications Encryption | **no** | - |
| MR - 26.2.1.7.1/1.2.1.7.1 Communications System Backup Mode Switching | **no** | - |
| MR - 26.2.1.7/1.2.1.7 Communications System Backup Mode | **no** | - |
| MR - 26.2.3/1.2.3 Communications Redundancy | **no** | - |
| MR - 26.1.1.13/1.1.1.13 Electrical System Cryptographic Module | **no** | - |
| MR - 26.1.1.20/1.1.1.20 Electrical System Maintenance Ports | **no** | - |
| MR - 26.1.1.6/1.1.1.6 Electrical System Secure Boot | **no** | - |
| MR - 26.2.1.6.1/1.2.1.6.1 Electrical System Backup Mode Switching | **no** | - |
| MR - 26.2.1.6/1.2.1.6 Electrical System Backup Mode | **no** | - |

## Method and assumptions

- Attack tree: `<<Risk>>` element that depends on the risk scenario → `And` children with `<<Probability_of_Attack_Success>>` → `And`/`Or` dependencies down to `<<PAT_Leaf_Node>>`. P(success) is the leaf's `_90CI_Low`–`_90CI_High` tag pair; the ranking uses the CI midpoint.
- Leaves linked from the scenario's loss scenarios but living in another risk's tree are included and marked.
- Requirement coverage counts only requirements whose package path contains 'cyber' or 'security'; other requirements on the same paths are counted separately.
- `direct` = Trace/Satisfy/Refine/Allocate/Dependency between the requirement and the leaf, loss scenario, HCA or controller. `allocation` = loss scenario –Trace– action → activity –Allocate→ block ←Allocate/Satisfy– requirement (all model links, medium).
- ATT&CK matching is lexical (explicit Txxxx id > verbatim technique name > IDF-weighted name-token overlap with documentation support > curated phrase hints listed in `cyber.py`). D3FEND countermeasures follow the profile's `May Harden/Detect/Isolate/…` associations and offensive→artifact←defensive paths; sub-techniques fall back to their parent.
- NIST candidates come from `sysml_demo/data/nist80053_d3fend.json` (authored starting point, see its header).
