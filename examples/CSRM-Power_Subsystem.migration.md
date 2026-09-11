# SysML v1 → v2 migration gap report: CSRM / Power Subsystem

Source: MagicDraw UML 2024x v6 export, 1704 model elements.  
Generated SysML v2: 40 lines, pilot-implementation validation **PASSED** (0 errors, 0 warnings).

## Summary

| Status | Elements | Share | Meaning |
|---|---:|---:|---|
| Clean | 12 | 86% | semantics preserved in the generated SysML v2 |
| Lossy | 0 | 0% | emitted, but some information was dropped or approximated (see note) |
| Needs decision | 1 | 7% | emitted in a provisional form; a systems engineer must choose the final v2 construct |
| No equivalent | 1 | 7% | no SysML v2 equivalent, or tool-specific; not emitted |

```
  v1 model ──► normalise ──► map ──► SysML v2 text ──► pilot validator
    1704 el.               12 clean          0 lossy
                                    1 decision       1 no equivalent
```

## Mapping table (per construct)

| v1 construct | v2 construct | n | clean | lossy | decision | none | notes |
|---|---|---:|---:|---:|---:|---:|---|
| PartProperty | part usage | 6 | 6 | 0 | 0 | 0 |  |
| Component | part def (stub) | 6 | 6 | 0 | 0 | 0 | outside the requested subset; declaration-only stub so references resolve |
| Subsystem (custom) | part def + metadata | 1 | 0 | 0 | 1 | 0 | specialises MagicDraw analysis pattern MassRollUpPattern: tool-specific; re-create as a v2 calc (e.g. total mass = sum of parts) or drop |
| Diagram: SysML Block Definition Diagram | - | 1 | 0 | 0 | 0 | 1 | v2 has no diagram-layout interchange; views/viewpoints must be re-authored in the target tool |

## Custom profile

Each stereotype resolves through its generalisation chain to a SysML base concept, which decides the v2 construct:

| Stereotype | Extends | SysML root | Tags | Applied | v2 |
|---|---|---|---|---:|---|
| Subsystem | Block | Block | - | 1 | part def + metadata |
| Component | Block | Block | - | 0 | part def + metadata |
| ComponentRequirement | ExtRequirement | Requirement | - | 0 | requirement + metadata |
| ConcernOf | - | Dependency | - | 0 | tagged dependency |
| CubeSat | Satellite | Block | - | 0 | part def + metadata |
| CubeSatDeployer | System | Block | - | 0 | part def + metadata |
| CubeSatRequirement | SatelliteRequirement | Requirement | - | 0 | requirement + metadata |
| DeployerRequirement | ExtRequirement | Requirement | - | 0 | requirement + metadata |
| Domain | Block | Block | - | 0 | part def + metadata |
| Equipment | Block | Block | - | 0 | part def + metadata |
| Explanation | - | Comment | - | 0 | comment + metadata |
| ExtRequirement | Requirement | Requirement | source, risk, validatedBy | 0 | requirement + metadata |
| Facility | Block | Block | - | 0 | part def + metadata |
| GroundSegment | Segment | Block | - | 0 | part def + metadata |
| GroundSegmentRequirement | SegmentRequirement | Requirement | - | 0 | requirement + metadata |
| Group | ExtRequirement | Requirement | - | 0 | requirement + metadata |
| HowTo | - | Comment | - | 0 | comment + metadata |
| KPP | - | Property | - | 0 | metadata on usage |
| MeasurementSpecification | Block | Block | summary, Id | 0 | part def + metadata |
| Mission | Block | Block | - | 0 | part def + metadata |
| MissionConstraint | ExtRequirement | Requirement | - | 0 | requirement + metadata |
| MissionNeed | ExtRequirement | Requirement | - | 0 | requirement + metadata |
| MissionObjective | ExtRequirement | Requirement | - | 0 | requirement + metadata |
| MissionRequirement | ExtRequirement | Requirement | - | 0 | requirement + metadata |
| MoE | - | Property | - | 0 | metadata on usage |
| Satellite | Spacecraft | Block | - | 0 | part def + metadata |
| SatelliteRequirement | SpacecraftRequirement | Requirement | - | 0 | requirement + metadata |
| Segment | SystemContext | Block | - | 0 | part def + metadata |
| SegmentRequirement | ExtRequirement | Requirement | - | 0 | requirement + metadata |
| SpaceSegment | Segment | Block | - | 0 | part def + metadata |
| SpaceSegmentRequirement | SegmentRequirement | Requirement | - | 0 | requirement + metadata |
| Spacecraft | System | Block | - | 0 | part def + metadata |
| SpacecraftRequirement | ExtRequirement | Requirement | - | 0 | requirement + metadata |
| Stakeholder | Block | Block | - | 0 | part def + metadata |
| StakeholderConcern | ExtRequirement | Requirement | - | 0 | requirement + metadata |
| SubsystemRequirement | ExtRequirement | Requirement | - | 0 | requirement + metadata |
| System | Block | Block | - | 0 | part def + metadata |
| SystemContext | Block | Block | - | 0 | part def + metadata |
| TPM | - | Property | - | 0 | metadata on usage |
| Validation | Trace | Trace | validated | 0 | tagged dependency |
| ValidationActivity | - | Behavior | A_Plan, B_Procedure, C_Conduct, D_Result, E_Status | 0 | action/verification def |
| Verification | Verify | Verify | verified | 0 | tagged dependency |
| VerificationActivity | - | Behavior | verificationMethod, verifies | 0 | action/verification def |
| kppRequirement | performanceRequirement | Requirement | - | 0 | requirement + metadata |
| kppSpecification | MeasurementSpecification | Block | - | 0 | part def + metadata |
| moeRequirement | performanceRequirement | Requirement | - | 0 | requirement + metadata |
| moeSpecification | MeasurementSpecification | Block | - | 0 | part def + metadata |
| mop | - | Property | - | 0 | metadata on usage |
| mopRequirement | performanceRequirement | Requirement | - | 0 | requirement + metadata |
| mopSpecification | MeasurementSpecification | Block | - | 0 | part def + metadata |
| performanceRequirement | ExtRequirement | Requirement | - | 0 | requirement + metadata |
| tpmRequirement | performanceRequirement | Requirement | - | 0 | requirement + metadata |
| tpmSpecification | MeasurementSpecification | Block | - | 0 | part def + metadata |

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

## Decisions required (1)

| Element | v1 | Proposed v2 | Why |
|---|---|---|---|
| 01 - CubeSat System Reference Model::5 - Architecture::L3_Subsystems::L3.1_CubeSat Subsystems::L3.1.2_Structures::Power Subsystem | Subsystem (custom) | part def + metadata | specialises MagicDraw analysis pattern MassRollUpPattern: tool-specific; re-create as a v2 calc (e.g. total mass = sum of parts) or drop |

## Not migrated

- Diagram: SysML Block Definition Diagram: 1
