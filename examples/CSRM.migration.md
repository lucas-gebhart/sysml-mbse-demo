# SysML v1 → v2 migration gap report: CSRM

Source: MagicDraw UML 2024x v6 export, 1704 model elements.  
Generated SysML v2: 1567 lines, pilot-implementation validation **PASSED** (0 errors, 0 warnings; PASSED means the text parses and resolves with no errors, warnings are listed under Validation diagnostics).

## Summary

| Status | Elements | Share | Meaning |
|---|---:|---:|---|
| Clean | 1040 | 77% | semantics preserved in the generated SysML v2 |
| Lossy | 12 | 1% | emitted, but some information was dropped or approximated (see note) |
| Needs decision | 42 | 3% | emitted in a provisional form; a systems engineer must choose the final v2 construct |
| No equivalent | 248 | 18% | no SysML v2 equivalent, or tool-specific; not emitted |

```
  v1 model ──► normalise ──► map ──► SysML v2 text ──► pilot validator
    1704 el.             1040 clean         12 lossy
                                   42 decision     248 no equivalent
```

## Mapping table (per construct)

| v1 construct | v2 construct | n | clean | lossy | decision | none | notes |
|---|---|---:|---:|---:|---:|---:|---|
| Package | package | 216 | 216 | 0 | 0 | 0 |  |
| Comment | doc, - | 173 | 172 | 0 | 0 | 1 | not reached by the transformer |
| PartProperty | part usage | 100 | 100 | 0 | 0 | 0 |  |
| Association (composite) | (part usage) | 100 | 100 | 0 | 0 | 0 | expressed by the owning block's part usage |
| Comment <<Explanation>> | doc, comment about, comment | 81 | 74 | 7 | 0 | 0 | <<Explanation>> stereotype on comment becomes metadata; annotated element not in this file |
| Diagram: Generic Table | - | 70 | 0 | 0 | 0 | 70 | v2 has no diagram-layout interchange; views/viewpoints must be re-authored in the target tool |
| Diagram: Requirement Table | - | 59 | 0 | 0 | 0 | 59 | v2 has no diagram-layout interchange; views/viewpoints must be re-authored in the target tool |
| Diagram: SysML Package Diagram | - | 58 | 0 | 0 | 0 | 58 | v2 has no diagram-layout interchange; views/viewpoints must be re-authored in the target tool |
| Component (custom) | part def + metadata | 58 | 28 | 0 | 30 | 0 | specialises MagicDraw analysis pattern MassRollUpPattern: tool-specific; re-create as a v2 calc (e.g. total mass = sum of parts) or drop |
| Group (custom) | requirement usage + metadata | 49 | 49 | 0 | 0 | 0 |  |
| Refine | #Refine dependency | 45 | 45 | 0 | 0 | 0 |  |
| Diagram: SysML Block Definition Diagram | - | 44 | 0 | 0 | 0 | 44 | v2 has no diagram-layout interchange; views/viewpoints must be re-authored in the target tool |
| Stakeholder (custom) | part def + metadata | 34 | 34 | 0 | 0 | 0 |  |
| Comment <<HowTo>> | doc | 27 | 27 | 0 | 0 | 0 |  |
| SubsystemRequirement (custom) | requirement usage + metadata | 20 | 20 | 0 | 0 | 0 |  |
| Subsystem (custom) | part def + metadata | 19 | 10 | 0 | 9 | 0 | specialises MagicDraw analysis pattern MassRollUpPattern: tool-specific; re-create as a v2 calc (e.g. total mass = sum of parts) or drop |
| ComponentRequirement (custom) | requirement usage + metadata | 18 | 18 | 0 | 0 | 0 |  |
| PackageImport | import | 16 | 16 | 0 | 0 | 0 |  |
| Block (SysML) | part def | 15 | 15 | 0 | 0 | 0 |  |
| DeployerRequirement (custom) | requirement usage + metadata | 14 | 14 | 0 | 0 | 0 |  |
| Facility (custom) | part def + metadata | 9 | 9 | 0 | 0 | 0 |  |
| DeriveReqt | #derivation connection | 8 | 8 | 0 | 0 | 0 |  |
| ValueProperty | attribute usage | 7 | 7 | 0 | 0 | 0 | untyped in the source model |
| Activity | action def | 6 | 6 | 0 | 0 | 0 |  |
| Diagram: Profile Diagram | - | 6 | 0 | 0 | 0 | 6 | v2 has no diagram-layout interchange; views/viewpoints must be re-authored in the target tool |
| Diagram: SysML Use Case Diagram | - | 5 | 0 | 0 | 0 | 5 | v2 has no diagram-layout interchange; views/viewpoints must be re-authored in the target tool |
| Trace | #Trace dependency | 5 | 5 | 0 | 0 | 0 |  |
| StakeholderConcern (custom) | requirement usage + metadata | 4 | 4 | 0 | 0 | 0 |  |
| moeSpecification (custom) | part def + metadata | 4 | 4 | 0 | 0 | 0 |  |
| mopSpecification (custom) | part def + metadata | 4 | 4 | 0 | 0 | 0 |  |
| tpmSpecification (custom) | part def + metadata | 4 | 4 | 0 | 0 | 0 |  |
| UseCase | use case def | 4 | 4 | 0 | 0 | 0 |  |
| Dependency | dependency | 4 | 4 | 0 | 0 | 0 |  |
| mount | - | 4 | 0 | 4 | 0 | 0 | relationship end not in this file |
| MissionNeed (custom) | requirement usage + metadata | 3 | 3 | 0 | 0 | 0 |  |
| MissionConstraint (custom) | requirement usage + metadata | 3 | 3 | 0 | 0 | 0 |  |
| MissionRequirement (custom) | requirement usage + metadata | 3 | 3 | 0 | 0 | 0 |  |
| MissionObjective (custom) | requirement usage + metadata | 3 | 3 | 0 | 0 | 0 |  |
| Segment (custom) | part def + metadata | 3 | 3 | 0 | 0 | 0 |  |
| Equipment (custom) | part def + metadata | 3 | 3 | 0 | 0 | 0 |  |
| CubeSatRequirement (custom) | requirement usage + metadata | 3 | 3 | 0 | 0 | 0 |  |
| kppSpecification (custom) | part def + metadata | 3 | 3 | 0 | 0 | 0 |  |
| Package (tool customisation) | - | 3 | 0 | 0 | 0 | 3 | MagicDraw derived-property / DSL customisation / unit-import package: re-create with v2 libraries (ISQ, SI) or drop |
| Actor | part def (actor) | 2 | 2 | 0 | 0 | 0 | v2 actors are parts; role assigned per use case |
| CubeSat (custom) | part def + metadata | 2 | 1 | 0 | 1 | 0 | specialises MagicDraw analysis pattern MassRollUpPattern: tool-specific; re-create as a v2 calc (e.g. total mass = sum of parts) or drop |
| GroundSegmentRequirement (custom) | requirement usage + metadata | 2 | 2 | 0 | 0 | 0 |  |
| moeRequirement (custom) | requirement usage + metadata | 2 | 2 | 0 | 0 | 0 |  |
| mopRequirement (custom) | requirement usage + metadata | 2 | 2 | 0 | 0 | 0 |  |
| tpmRequirement (custom) | requirement usage + metadata | 2 | 2 | 0 | 0 | 0 |  |
| kppRequirement (custom) | requirement usage + metadata | 2 | 2 | 0 | 0 | 0 |  |
| Activity <<ValidationActivity>> | verification def (validation) | 2 | 2 | 0 | 0 | 0 |  |
| Activity <<VerificationActivity>> | verification def | 2 | 2 | 0 | 0 | 0 |  |
| ValidationActivity (custom) | action def + metadata | 2 | 0 | 0 | 2 | 0 | behaviour stereotype applied to a class (not an activity): emitted as action def; confirm intent |
| Diagram: Dependency Matrix | - | 1 | 0 | 0 | 0 | 1 | v2 has no diagram-layout interchange; views/viewpoints must be re-authored in the target tool |
| Property (value) | attribute usage | 1 | 1 | 0 | 0 | 0 | untyped in the source model |
| Comment <<Rationale>> | comment about | 1 | 0 | 1 | 0 | 0 | <<Rationale>> stereotype on comment becomes metadata |
| SegmentRequirement (custom) | requirement usage + metadata | 1 | 1 | 0 | 0 | 0 |  |
| ProfileApplication | - | 1 | 0 | 0 | 0 | 1 | profile mechanics; see profile cell |

## Custom profile

Each stereotype resolves through its generalisation chain to a SysML base concept, which decides the v2 construct:

| Stereotype | Extends | SysML root | Tags | Applied | v2 |
|---|---|---|---|---:|---|
| Explanation | - | Comment | - | 81 | comment + metadata |
| Component | Block | Block | - | 58 | part def + metadata |
| Group | ExtRequirement | Requirement | - | 49 | requirement + metadata |
| Stakeholder | Block | Block | - | 34 | part def + metadata |
| HowTo | - | Comment | - | 27 | comment + metadata |
| SubsystemRequirement | ExtRequirement | Requirement | - | 20 | requirement + metadata |
| Subsystem | Block | Block | - | 19 | part def + metadata |
| ComponentRequirement | ExtRequirement | Requirement | - | 18 | requirement + metadata |
| DeployerRequirement | ExtRequirement | Requirement | - | 14 | requirement + metadata |
| Facility | Block | Block | - | 9 | part def + metadata |
| StakeholderConcern | ExtRequirement | Requirement | - | 4 | requirement + metadata |
| ValidationActivity | - | Behavior | A_Plan, B_Procedure, C_Conduct, D_Result, E_Status | 4 | action/verification def |
| moeSpecification | MeasurementSpecification | Block | - | 4 | part def + metadata |
| mopSpecification | MeasurementSpecification | Block | - | 4 | part def + metadata |
| tpmSpecification | MeasurementSpecification | Block | - | 4 | part def + metadata |
| CubeSatRequirement | SatelliteRequirement | Requirement | - | 3 | requirement + metadata |
| Equipment | Block | Block | - | 3 | part def + metadata |
| MissionConstraint | ExtRequirement | Requirement | - | 3 | requirement + metadata |
| MissionNeed | ExtRequirement | Requirement | - | 3 | requirement + metadata |
| MissionObjective | ExtRequirement | Requirement | - | 3 | requirement + metadata |
| MissionRequirement | ExtRequirement | Requirement | - | 3 | requirement + metadata |
| Segment | SystemContext | Block | - | 3 | part def + metadata |
| kppSpecification | MeasurementSpecification | Block | - | 3 | part def + metadata |
| CubeSat | Satellite | Block | - | 2 | part def + metadata |
| GroundSegmentRequirement | SegmentRequirement | Requirement | - | 2 | requirement + metadata |
| VerificationActivity | - | Behavior | verificationMethod, verifies | 2 | action/verification def |
| kppRequirement | performanceRequirement | Requirement | - | 2 | requirement + metadata |
| moeRequirement | performanceRequirement | Requirement | - | 2 | requirement + metadata |
| mopRequirement | performanceRequirement | Requirement | - | 2 | requirement + metadata |
| tpmRequirement | performanceRequirement | Requirement | - | 2 | requirement + metadata |
| SegmentRequirement | ExtRequirement | Requirement | - | 1 | requirement + metadata |
| ConcernOf | - | Dependency | - | 0 | tagged dependency |
| CubeSatDeployer | System | Block | - | 0 | part def + metadata |
| Domain | Block | Block | - | 0 | part def + metadata |
| ExtRequirement | Requirement | Requirement | source, risk, validatedBy | 0 | requirement + metadata |
| GroundSegment | Segment | Block | - | 0 | part def + metadata |
| KPP | - | Property | - | 0 | metadata on usage |
| MeasurementSpecification | Block | Block | summary, Id | 0 | part def + metadata |
| Mission | Block | Block | - | 0 | part def + metadata |
| MoE | - | Property | - | 0 | metadata on usage |
| Satellite | Spacecraft | Block | - | 0 | part def + metadata |
| SatelliteRequirement | SpacecraftRequirement | Requirement | - | 0 | requirement + metadata |
| SpaceSegment | Segment | Block | - | 0 | part def + metadata |
| SpaceSegmentRequirement | SegmentRequirement | Requirement | - | 0 | requirement + metadata |
| Spacecraft | System | Block | - | 0 | part def + metadata |
| SpacecraftRequirement | ExtRequirement | Requirement | - | 0 | requirement + metadata |
| System | Block | Block | - | 0 | part def + metadata |
| SystemContext | Block | Block | - | 0 | part def + metadata |
| TPM | - | Property | - | 0 | metadata on usage |
| Validation | Trace | Trace | validated | 0 | tagged dependency |
| Verification | Verify | Verify | verified | 0 | tagged dependency |
| mop | - | Property | - | 0 | metadata on usage |
| performanceRequirement | ExtRequirement | Requirement | - | 0 | requirement + metadata |

## Standing gaps (independent of this model)

- **Diagrams / layout** — SysML v2 interchange carries semantics, not diagram layout. Views must be re-authored in the target tool (Cameo 2026x v2 plugin generates views from the model).
- **Custom profile stereotypes** — Carried as `metadata def`s so every tagged element keeps its classification and tag values, but the tool-side behaviour (icons, validation rules, DSL customisations, derived properties, table definitions) is not expressible in v2 and has to be re-created.
- **Satisfy / Verify** — v2 `satisfy ... by` requires a part *usage*; v1 satisfies typically point at Blocks (definitions). Emitted as tagged dependencies until the satisfying usage is chosen.
- **Item flows between blocks** — v2 flows need a common part context; v1 InformationFlows drawn between features of unrelated blocks are kept as tagged dependencies.
- **Activity / state-machine internals** — Action and transition graphs are structurally different in v2 (succession-based). Signatures are migrated; bodies flagged for re-modelling.
- **Operations** — v2 has no operations; emitted as nested actions for review.
- **Units / quantity kinds** — MagicDraw ISO-80000 / SI library imports map to the v2 `ISQ` and `SI` libraries but need an explicit mapping table.
- **Instance specifications** — v2 has no instances; use individuals/snapshots or attribute defaults.
- **PackageMerge** — No v2 support (per the OMG transformation document).

## Decisions required (42)

| Element | v1 | Proposed v2 | Why |
|---|---|---|---|
| 01 - CubeSat System Reference Model::5 - Architecture::L4_Components::L4.1_CubeSat Subsystems Components::L4.1.1_Mission Payload Components::L4.1.1.2_Structures::Processor and Memory | Component (custom) | part def + metadata | specialises MagicDraw analysis pattern MassRollUpPattern: tool-specific; re-create as a v2 calc (e.g. total mass = sum of parts) or drop |
| 01 - CubeSat System Reference Model::5 - Architecture::L4_Components::L4.1_CubeSat Subsystems Components::L4.1.1_Mission Payload Components::L4.1.1.2_Structures::Instrument | Component (custom) | part def + metadata | specialises MagicDraw analysis pattern MassRollUpPattern: tool-specific; re-create as a v2 calc (e.g. total mass = sum of parts) or drop |
| 01 - CubeSat System Reference Model::5 - Architecture::L4_Components::L4.1_CubeSat Subsystems Components::L4.1.2_Command and Data Handling Components::L4.1.2.2_Structures::Processor and Memory | Component (custom) | part def + metadata | specialises MagicDraw analysis pattern MassRollUpPattern: tool-specific; re-create as a v2 calc (e.g. total mass = sum of parts) or drop |
| 01 - CubeSat System Reference Model::5 - Architecture::L4_Components::L4.1_CubeSat Subsystems Components::L4.1.2_Command and Data Handling Components::L4.1.2.2_Structures::Command, Telemetry, and Data Bus | Component (custom) | part def + metadata | specialises MagicDraw analysis pattern MassRollUpPattern: tool-specific; re-create as a v2 calc (e.g. total mass = sum of parts) or drop |
| 01 - CubeSat System Reference Model::5 - Architecture::L4_Components::L4.1_CubeSat Subsystems Components::L4.1.3_Communication Components::L4.1.3.2_Structures::Processor and Memory | Component (custom) | part def + metadata | specialises MagicDraw analysis pattern MassRollUpPattern: tool-specific; re-create as a v2 calc (e.g. total mass = sum of parts) or drop |
| 01 - CubeSat System Reference Model::5 - Architecture::L4_Components::L4.1_CubeSat Subsystems Components::L4.1.3_Communication Components::L4.1.3.2_Structures::Receive Antenna and Equipment | Component (custom) | part def + metadata | specialises MagicDraw analysis pattern MassRollUpPattern: tool-specific; re-create as a v2 calc (e.g. total mass = sum of parts) or drop |
| 01 - CubeSat System Reference Model::5 - Architecture::L4_Components::L4.1_CubeSat Subsystems Components::L4.1.3_Communication Components::L4.1.3.2_Structures::Transmit Antenna and Equipment | Component (custom) | part def + metadata | specialises MagicDraw analysis pattern MassRollUpPattern: tool-specific; re-create as a v2 calc (e.g. total mass = sum of parts) or drop |
| 01 - CubeSat System Reference Model::5 - Architecture::L4_Components::L4.1_CubeSat Subsystems Components::L4.1.4_Attitude Determination and Control Components::L4.1.4.2_Structures::Software | Component (custom) | part def + metadata | specialises MagicDraw analysis pattern MassRollUpPattern: tool-specific; re-create as a v2 calc (e.g. total mass = sum of parts) or drop |
| 01 - CubeSat System Reference Model::5 - Architecture::L4_Components::L4.1_CubeSat Subsystems Components::L4.1.4_Attitude Determination and Control Components::L4.1.4.2_Structures::Actuator | Component (custom) | part def + metadata | specialises MagicDraw analysis pattern MassRollUpPattern: tool-specific; re-create as a v2 calc (e.g. total mass = sum of parts) or drop |
| 01 - CubeSat System Reference Model::5 - Architecture::L4_Components::L4.1_CubeSat Subsystems Components::L4.1.4_Attitude Determination and Control Components::L4.1.4.2_Structures::Sensor | Component (custom) | part def + metadata | specialises MagicDraw analysis pattern MassRollUpPattern: tool-specific; re-create as a v2 calc (e.g. total mass = sum of parts) or drop |
| 01 - CubeSat System Reference Model::5 - Architecture::L4_Components::L4.1_CubeSat Subsystems Components::L4.1.5_Guidance Navigation and Control Components::L4.1.5.2_Structures::Software | Component (custom) | part def + metadata | specialises MagicDraw analysis pattern MassRollUpPattern: tool-specific; re-create as a v2 calc (e.g. total mass = sum of parts) or drop |
| 01 - CubeSat System Reference Model::5 - Architecture::L4_Components::L4.1_CubeSat Subsystems Components::L4.1.5_Guidance Navigation and Control Components::L4.1.5.2_Structures::Accelerometer | Component (custom) | part def + metadata | specialises MagicDraw analysis pattern MassRollUpPattern: tool-specific; re-create as a v2 calc (e.g. total mass = sum of parts) or drop |
| 01 - CubeSat System Reference Model::5 - Architecture::L4_Components::L4.1_CubeSat Subsystems Components::L4.1.5_Guidance Navigation and Control Components::L4.1.5.2_Structures::GNSS Receiver | Component (custom) | part def + metadata | specialises MagicDraw analysis pattern MassRollUpPattern: tool-specific; re-create as a v2 calc (e.g. total mass = sum of parts) or drop |
| 01 - CubeSat System Reference Model::5 - Architecture::L4_Components::L4.1_CubeSat Subsystems Components::L4.1.6_Structures and Mechanisms Components::L4.1.6.2_Structures::Static Mount | Component (custom) | part def + metadata | specialises MagicDraw analysis pattern MassRollUpPattern: tool-specific; re-create as a v2 calc (e.g. total mass = sum of parts) or drop |
| 01 - CubeSat System Reference Model::5 - Architecture::L4_Components::L4.1_CubeSat Subsystems Components::L4.1.6_Structures and Mechanisms Components::L4.1.6.2_Structures::Deployable Mount | Component (custom) | part def + metadata | specialises MagicDraw analysis pattern MassRollUpPattern: tool-specific; re-create as a v2 calc (e.g. total mass = sum of parts) or drop |
| 01 - CubeSat System Reference Model::5 - Architecture::L4_Components::L4.1_CubeSat Subsystems Components::L4.1.6_Structures and Mechanisms Components::L4.1.6.2_Structures::Actuated Mount | Component (custom) | part def + metadata | specialises MagicDraw analysis pattern MassRollUpPattern: tool-specific; re-create as a v2 calc (e.g. total mass = sum of parts) or drop |
| 01 - CubeSat System Reference Model::5 - Architecture::L4_Components::L4.1_CubeSat Subsystems Components::L4.1.7_Power Components::L4.1.7.2_Structures::Processor and Memory | Component (custom) | part def + metadata | specialises MagicDraw analysis pattern MassRollUpPattern: tool-specific; re-create as a v2 calc (e.g. total mass = sum of parts) or drop |
| 01 - CubeSat System Reference Model::5 - Architecture::L4_Components::L4.1_CubeSat Subsystems Components::L4.1.7_Power Components::L4.1.7.2_Structures::Software | Component (custom) | part def + metadata | specialises MagicDraw analysis pattern MassRollUpPattern: tool-specific; re-create as a v2 calc (e.g. total mass = sum of parts) or drop |
| 01 - CubeSat System Reference Model::5 - Architecture::L4_Components::L4.1_CubeSat Subsystems Components::L4.1.7_Power Components::L4.1.7.2_Structures::Solar Arrays | Component (custom) | part def + metadata | specialises MagicDraw analysis pattern MassRollUpPattern: tool-specific; re-create as a v2 calc (e.g. total mass = sum of parts) or drop |
| 01 - CubeSat System Reference Model::5 - Architecture::L4_Components::L4.1_CubeSat Subsystems Components::L4.1.7_Power Components::L4.1.7.2_Structures::Batteries | Component (custom) | part def + metadata | specialises MagicDraw analysis pattern MassRollUpPattern: tool-specific; re-create as a v2 calc (e.g. total mass = sum of parts) or drop |
| 01 - CubeSat System Reference Model::5 - Architecture::L4_Components::L4.1_CubeSat Subsystems Components::L4.1.7_Power Components::L4.1.7.2_Structures::Regulators and Converters | Component (custom) | part def + metadata | specialises MagicDraw analysis pattern MassRollUpPattern: tool-specific; re-create as a v2 calc (e.g. total mass = sum of parts) or drop |
| 01 - CubeSat System Reference Model::5 - Architecture::L4_Components::L4.1_CubeSat Subsystems Components::L4.1.7_Power Components::L4.1.7.2_Structures::Power Circuits and Switches | Component (custom) | part def + metadata | specialises MagicDraw analysis pattern MassRollUpPattern: tool-specific; re-create as a v2 calc (e.g. total mass = sum of parts) or drop |
| 01 - CubeSat System Reference Model::5 - Architecture::L4_Components::L4.1_CubeSat Subsystems Components::L4.1.8_Thermal Components::L4.1.8.2_Structures::Processor and Memory | Component (custom) | part def + metadata | specialises MagicDraw analysis pattern MassRollUpPattern: tool-specific; re-create as a v2 calc (e.g. total mass = sum of parts) or drop |
| 01 - CubeSat System Reference Model::5 - Architecture::L4_Components::L4.1_CubeSat Subsystems Components::L4.1.8_Thermal Components::L4.1.8.2_Structures::Software | Component (custom) | part def + metadata | specialises MagicDraw analysis pattern MassRollUpPattern: tool-specific; re-create as a v2 calc (e.g. total mass = sum of parts) or drop |
| 01 - CubeSat System Reference Model::5 - Architecture::L4_Components::L4.1_CubeSat Subsystems Components::L4.1.8_Thermal Components::L4.1.8.2_Structures::Thermal Sensors, Sources, and Sinks | Component (custom) | part def + metadata | specialises MagicDraw analysis pattern MassRollUpPattern: tool-specific; re-create as a v2 calc (e.g. total mass = sum of parts) or drop |
| 01 - CubeSat System Reference Model::5 - Architecture::L4_Components::L4.1_CubeSat Subsystems Components::L4.1.9_Propulsion Components::L4.1.9.2_Structures::Processor and Memory | Component (custom) | part def + metadata | specialises MagicDraw analysis pattern MassRollUpPattern: tool-specific; re-create as a v2 calc (e.g. total mass = sum of parts) or drop |
| 01 - CubeSat System Reference Model::5 - Architecture::L4_Components::L4.1_CubeSat Subsystems Components::L4.1.9_Propulsion Components::L4.1.9.2_Structures::Software | Component (custom) | part def + metadata | specialises MagicDraw analysis pattern MassRollUpPattern: tool-specific; re-create as a v2 calc (e.g. total mass = sum of parts) or drop |
| 01 - CubeSat System Reference Model::5 - Architecture::L4_Components::L4.1_CubeSat Subsystems Components::L4.1.9_Propulsion Components::L4.1.9.2_Structures::Propellant Storage | Component (custom) | part def + metadata | specialises MagicDraw analysis pattern MassRollUpPattern: tool-specific; re-create as a v2 calc (e.g. total mass = sum of parts) or drop |
| 01 - CubeSat System Reference Model::5 - Architecture::L4_Components::L4.1_CubeSat Subsystems Components::L4.1.9_Propulsion Components::L4.1.9.2_Structures::Propellant Control | Component (custom) | part def + metadata | specialises MagicDraw analysis pattern MassRollUpPattern: tool-specific; re-create as a v2 calc (e.g. total mass = sum of parts) or drop |
| 01 - CubeSat System Reference Model::5 - Architecture::L4_Components::L4.1_CubeSat Subsystems Components::L4.1.9_Propulsion Components::L4.1.9.2_Structures::Thrusters | Component (custom) | part def + metadata | specialises MagicDraw analysis pattern MassRollUpPattern: tool-specific; re-create as a v2 calc (e.g. total mass = sum of parts) or drop |
| 01 - CubeSat System Reference Model::5 - Architecture::L3_Subsystems::L3.1_CubeSat Subsystems::L3.1.2_Structures::Thermal Subsystem | Subsystem (custom) | part def + metadata | specialises MagicDraw analysis pattern MassRollUpPattern: tool-specific; re-create as a v2 calc (e.g. total mass = sum of parts) or drop |
| 01 - CubeSat System Reference Model::5 - Architecture::L3_Subsystems::L3.1_CubeSat Subsystems::L3.1.2_Structures::Propulsion Subsystem | Subsystem (custom) | part def + metadata | specialises MagicDraw analysis pattern MassRollUpPattern: tool-specific; re-create as a v2 calc (e.g. total mass = sum of parts) or drop |
| 01 - CubeSat System Reference Model::5 - Architecture::L3_Subsystems::L3.1_CubeSat Subsystems::L3.1.2_Structures::Structures and Mechanisms Subsystem | Subsystem (custom) | part def + metadata | specialises MagicDraw analysis pattern MassRollUpPattern: tool-specific; re-create as a v2 calc (e.g. total mass = sum of parts) or drop |
| 01 - CubeSat System Reference Model::5 - Architecture::L3_Subsystems::L3.1_CubeSat Subsystems::L3.1.2_Structures::Power Subsystem | Subsystem (custom) | part def + metadata | specialises MagicDraw analysis pattern MassRollUpPattern: tool-specific; re-create as a v2 calc (e.g. total mass = sum of parts) or drop |
| 01 - CubeSat System Reference Model::5 - Architecture::L3_Subsystems::L3.1_CubeSat Subsystems::L3.1.2_Structures::Attitude Determination and Control Subsystem | Subsystem (custom) | part def + metadata | specialises MagicDraw analysis pattern MassRollUpPattern: tool-specific; re-create as a v2 calc (e.g. total mass = sum of parts) or drop |
| 01 - CubeSat System Reference Model::5 - Architecture::L3_Subsystems::L3.1_CubeSat Subsystems::L3.1.2_Structures::Command and Data Handling Subsystem | Subsystem (custom) | part def + metadata | specialises MagicDraw analysis pattern MassRollUpPattern: tool-specific; re-create as a v2 calc (e.g. total mass = sum of parts) or drop |
| 01 - CubeSat System Reference Model::5 - Architecture::L3_Subsystems::L3.1_CubeSat Subsystems::L3.1.2_Structures::Communication Subsystem | Subsystem (custom) | part def + metadata | specialises MagicDraw analysis pattern MassRollUpPattern: tool-specific; re-create as a v2 calc (e.g. total mass = sum of parts) or drop |
| 01 - CubeSat System Reference Model::5 - Architecture::L3_Subsystems::L3.1_CubeSat Subsystems::L3.1.2_Structures::Guidance Navigation and Control Subsystem | Subsystem (custom) | part def + metadata | specialises MagicDraw analysis pattern MassRollUpPattern: tool-specific; re-create as a v2 calc (e.g. total mass = sum of parts) or drop |
| 01 - CubeSat System Reference Model::5 - Architecture::L3_Subsystems::L3.1_CubeSat Subsystems::L3.1.2_Structures::Mission Payload Subsystem | Subsystem (custom) | part def + metadata | specialises MagicDraw analysis pattern MassRollUpPattern: tool-specific; re-create as a v2 calc (e.g. total mass = sum of parts) or drop |
| 01 - CubeSat System Reference Model::5 - Architecture::L2_Segment::L2.1_Space Segment::L2.1.2_Structures::CubeSat | CubeSat (custom) | part def + metadata | specialises MagicDraw analysis pattern MassRollUpPattern: tool-specific; re-create as a v2 calc (e.g. total mass = sum of parts) or drop |
| 02 - CSRM Elements, Examples and Illustrations::7 - CSRM Population::7.2 - CSRM Elements::Verification Activity | ValidationActivity (custom) | action def + metadata | behaviour stereotype applied to a class (not an activity): emitted as action def; confirm intent |
| 02 - CSRM Elements, Examples and Illustrations::7 - CSRM Population::7.2 - CSRM Elements::Validation Activity | ValidationActivity (custom) | action def + metadata | behaviour stereotype applied to a class (not an activity): emitted as action def; confirm intent |

## Lossy mappings (12)

| Element | v1 | v2 | What was lost |
|---|---|---|---|
| 01 - CubeSat System Reference Model::4 - Requirements::L3 Subsystem Rqts::L3.2 Ground Subsystems Rqts::L3.2.1 Plan and Schedule Subsystem Rqts::<Comment> | Comment <<Rationale>> | comment about | <<Rationale>> stereotype on comment becomes metadata |
| 01 - CubeSat System Reference Model::0 - CSRM Overview and Navigation::<Comment> | Comment <<Explanation>> | comment about | <<Explanation>> stereotype on comment becomes metadata |
| 01 - CubeSat System Reference Model::0 - CSRM Overview and Navigation::<Comment> | Comment <<Explanation>> | comment about | <<Explanation>> stereotype on comment becomes metadata |
| 01 - CubeSat System Reference Model::0 - CSRM Overview and Navigation::<Comment> | Comment <<Explanation>> | comment about | <<Explanation>> stereotype on comment becomes metadata |
| 01 - CubeSat System Reference Model::0 - CSRM Overview and Navigation::<Comment> | Comment <<Explanation>> | comment about | <<Explanation>> stereotype on comment becomes metadata |
| 01 - CubeSat System Reference Model::0 - CSRM Overview and Navigation::<Comment> | Comment <<Explanation>> | comment about | <<Explanation>> stereotype on comment becomes metadata |
| 01 - CubeSat System Reference Model::0 - CSRM Overview and Navigation::<Comment> | Comment <<Explanation>> | comment about | <<Explanation>> stereotype on comment becomes metadata |
| 00 - CSRM Start Here::<Comment> | Comment <<Explanation>> | comment | annotated element not in this file |
| <Dependency> | mount | - | relationship end not in this file |
| <Dependency> | mount | - | relationship end not in this file |
| <Dependency> | mount | - | relationship end not in this file |
| <Dependency> | mount | - | relationship end not in this file |

## Not migrated

- Diagram: Generic Table: 70
- Diagram: Requirement Table: 59
- Diagram: SysML Package Diagram: 58
- Diagram: SysML Block Definition Diagram: 44
- Diagram: Profile Diagram: 6
- Diagram: SysML Use Case Diagram: 5
- Package (tool customisation): 3
- Diagram: Dependency Matrix: 1
- ProfileApplication: 1
- Comment: 1
