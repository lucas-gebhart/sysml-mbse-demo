# SysML v1 → v2 migration gap report: DELS

Source: MagicDraw UML 19.0 v9 export, 1610 model elements.  
Generated SysML v2: 740 lines, pilot-implementation validation **PASSED WITH WARNINGS** (0 errors, 47 warnings; PASSED means the text parses and resolves with no errors, warnings are listed under Validation diagnostics).

## Summary

| Status | Elements | Share | Meaning |
|---|---:|---:|---|
| Clean | 419 | 68% | semantics preserved in the generated SysML v2 |
| Lossy | 44 | 7% | emitted, but some information was dropped or approximated (see note) |
| Needs decision | 97 | 16% | emitted in a provisional form; a systems engineer must choose the final v2 construct |
| No equivalent | 54 | 9% | no SysML v2 equivalent, or tool-specific; not emitted |

```
  v1 model ──► normalise ──► map ──► SysML v2 text ──► pilot validator
    1610 el.              419 clean         44 lossy
                                   97 decision      54 no equivalent
```

## Mapping table (per construct)

| v1 construct | v2 construct | n | clean | lossy | decision | none | notes |
|---|---|---:|---:|---:|---:|---:|---|
| Block (SysML) | part def | 61 | 55 | 6 | 0 | 0 | generalization to external FlowNetwork dropped; generalization to external Commodity dropped |
| Association (reference) | (ref part usage) | 55 | 55 | 0 | 0 | 0 | expressed by the owning block's reference usage |
| Property (value) | attribute usage | 47 | 45 | 2 | 0 | 0 | untyped in the source model; multiplicity expression 'self.nDims * self.nDims'..'self.nDims * self.nDims' dropped; use a v2 calc/constraint; multiplicity expression 'self.nDims'..'self.nDims' dropped; use a v2 calc/constraint |
| ReferenceProperty | ref part | 40 | 39 | 1 | 0 | 0 | sibling name clash; emitted as 'resource_2' |
| Association (composite) | (part usage) | 36 | 36 | 0 | 0 | 0 | expressed by the owning block's part usage |
| Activity | action def | 32 | 25 | 7 | 0 | 0 | 7 action nodes and 0 flows not migrated (activity internals require manual re-modelling); 5 action nodes and 9 flows not migrated (activity internals require manual re-modelling); 8 action nodes and 10 flows not migrated (activity internals require manual re-modelling) |
| Operation | action (nested) | 31 | 0 | 0 | 31 | 0 | v2 has no operations; emitted as nested action, calls must be re-modelled; v2 has no operations; emitted as nested action, calls must be re-modelled; sibling name clash; emitted as 'sequencing_2' |
| Package | package | 30 | 30 | 0 | 0 | 0 |  |
| ValueProperty | attribute usage | 29 | 29 | 0 | 0 | 0 | untyped in the source model |
| Diagram: SysML Block Definition Diagram | - | 24 | 0 | 0 | 0 | 24 | v2 has no diagram-layout interchange; views/viewpoints must be re-authored in the target tool |
| Property | ref | 23 | 0 | 0 | 23 | 0 | typed by Activity; choose part/attribute/ref; typed by Interface; choose part/attribute/ref; typed by AssociationClass; choose part/attribute/ref |
| PartProperty | part usage | 21 | 19 | 2 | 0 | 0 | redefinition of 'controller' dropped: redefined feature has a different v2 kind |
| Class (unstereotyped) | part def | 18 | 0 | 0 | 18 | 0 | plain UML class: treated as part def; confirm it is structural; plain UML class: treated as part def; confirm it is structural; sibling name clash; emitted as 'DecisionSupport_2' |
| Connector | connect | 17 | 17 | 0 | 0 | 0 |  |
| ValueType | attribute def | 16 | 16 | 0 | 0 | 0 |  |
| ItemFlow / InformationFlow | #ItemFlow dependency | 16 | 0 | 0 | 16 | 0 | v2 flows need a common part context (connect a.port to b.port inside an owner); ends live in different definitions, so the flow is kept as a traced dependency; v2 flows need a common part context (connect a.port to b.port inside an owner); ends live in different definitions, so the flow is kept as a traced dependency; conveyed item type unresolved; v2 flows need a common part context (connect a.port to b.port inside an owner); ends live in different definitions, so the flow is kept as a traced dependency; sibling name clash; emitted as 'flow for Task_2' |
| Port | port usage | 13 | 13 | 0 | 0 | 0 |  |
| SharedProperty | ref part | 13 | 0 | 13 | 0 | 0 | shared aggregation semantics approximated by reference; shared aggregation semantics approximated by reference; redefinition of 'memberResource' dropped: redefined feature has a different v2 kind |
| ProxyPort | port usage | 11 | 11 | 0 | 0 | 0 |  |
| Comment | doc, - | 10 | 7 | 0 | 0 | 3 | not reached by the transformer |
| Diagram: Class Diagram | - | 10 | 0 | 0 | 0 | 10 | v2 has no diagram-layout interchange; views/viewpoints must be re-authored in the target tool |
| Interface (UML) | port def | 8 | 0 | 0 | 8 | 0 | UML interface with operations: v2 has no operations; port def with flows, or action defs, must be chosen |
| FlowProperty | out item, in item | 7 | 7 | 0 | 0 | 0 |  |
| Constraint (opaque) | constraint { doc } | 7 | 0 | 7 | 0 | 0 | expression kept as text; must be rewritten in KerML expression language |
| Diagram: SysML Internal Block Diagram | - | 6 | 0 | 0 | 0 | 6 | v2 has no diagram-layout interchange; views/viewpoints must be re-authored in the target tool |
| Constraint | - | 6 | 0 | 0 | 0 | 6 | not reached by the transformer |
| Enumeration | enum def | 5 | 5 | 0 | 0 | 0 |  |
| StateMachine | state def | 4 | 0 | 4 | 0 | 0 | 10 states / 11 transitions emitted; triggers, guards, effects and 1 pseudostates dropped; 11 states / 7 transitions emitted; triggers, guards, effects and 1 pseudostates dropped; 2 states / 6 transitions emitted; triggers, guards, effects and 3 pseudostates dropped |
| InterfaceBlock (SysML) | port def | 4 | 4 | 0 | 0 | 0 |  |
| AssociationClass | - | 3 | 0 | 0 | 0 | 3 | no mapping implemented |
| Property (composite) | part usage | 3 | 3 | 0 | 0 | 0 |  |
| Comment <<Problem>> | doc, comment about | 2 | 1 | 1 | 0 | 0 | <<Problem>> stereotype on comment becomes metadata |
| PackageImport | import | 2 | 2 | 0 | 0 | 0 |  |
| GeneralizationSet | - | 1 | 0 | 0 | 0 | 1 | no mapping implemented |
| Port (untyped) | port usage | 1 | 0 | 1 | 0 | 0 | no type; interface cannot be checked |
| Diagram: SysML Package Diagram | - | 1 | 0 | 0 | 0 | 1 | v2 has no diagram-layout interchange; views/viewpoints must be re-authored in the target tool |
| PackageImport (external) | import (v2 library) | 1 | 0 | 0 | 1 | 0 | imports 'CommodityFlowNetwork' from a v1 library/profile; map to the v2 standard library (ISQ, SI, ScalarValues) |

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

## Decisions required (97)

| Element | v1 | Proposed v2 | Why |
|---|---|---|---|
| PLANT::Resource::Resource::requiredByProcess | Property | ref | typed by Activity; choose part/attribute/ref |
| PLANT::Resource::ControlActuator::AdmissionGate::canExecute | Property | ref | typed by Activity; choose part/attribute/ref |
| PLANT::Resource::ControlActuator::AdmissionGate::admit | Operation | action (nested) | v2 has no operations; emitted as nested action, calls must be re-modelled |
| PLANT::Resource::ControlActuator::Queue::canExecute | Property | ref | typed by Activity; choose part/attribute/ref |
| PLANT::Resource::ControlActuator::Queue::sequence | Operation | action (nested) | v2 has no operations; emitted as nested action, calls must be re-modelled |
| PLANT::Resource::ControlActuator::ResourceAcquirer::canExecute | Property | ref | typed by Activity; choose part/attribute/ref |
| PLANT::Resource::ControlActuator::ResourceAcquirer::acquireResource | Operation | action (nested) | v2 has no operations; emitted as nested action, calls must be re-modelled |
| PLANT::Resource::ControlActuator::Router::canExecute | Property | ref | typed by Activity; choose part/attribute/ref |
| PLANT::Resource::ControlActuator::Router::Route | Operation | action (nested) | v2 has no operations; emitted as nested action, calls must be re-modelled |
| PLANT::Resource::ControlActuator::ChangeState::canExecute | Property | ref | typed by Activity; choose part/attribute/ref |
| PLANT::Resource::ControlActuator::ChangeState::ChangeState | Operation | action (nested) | v2 has no operations; emitted as nested action, calls must be re-modelled |
| PLANT::Resource::ControlActuator::ReadWriteProcessPlan::canExecute | Property | ref | typed by Activity; choose part/attribute/ref |
| PLANT::Resource::ControlActuator::ReadWriteProcessPlan::readProcessPlan | Operation | action (nested) | v2 has no operations; emitted as nested action, calls must be re-modelled |
| PLANT::Resource::ControlActuator::ReadWriteProcessPlan::updateProcessPlan | Operation | action (nested) | v2 has no operations; emitted as nested action, calls must be re-modelled |
| PLANT::Resource::ControlActuator::Scheduler::executeSchedule | Operation | action (nested) | v2 has no operations; emitted as nested action, calls must be re-modelled |
| PLANT::Resource::OZONEResourceDef::DiscreteStateResource::currentService | Property | ref | typed by Activity; choose part/attribute/ref |
| PLANT::Resource::OZONEResourceDef::DiscreteStateResource::changeState | Operation | action (nested) | v2 has no operations; emitted as nested action, calls must be re-modelled |
| PLANT::Resource::OZONEResourceDef::DiscreteStateResource::queryState | Operation | action (nested) | v2 has no operations; emitted as nested action, calls must be re-modelled |
| PLANT::Resource::OZONEResourceDef::DiscreteStateResource::assignTask | Operation | action (nested) | v2 has no operations; emitted as nested action, calls must be re-modelled |
| PLANT::Resource::OZONEResourceDef::MobileResource::queryState | Operation | action (nested) | v2 has no operations; emitted as nested action, calls must be re-modelled |
| PLANT::Resource::OZONEResourceDef::MobileResource::reposition | Operation | action (nested) | v2 has no operations; emitted as nested action, calls must be re-modelled |
| PLANT::Resource::OZONEResourceDef::CapacitatedResource::increaseCapacity | Operation | action (nested) | v2 has no operations; emitted as nested action, calls must be re-modelled |
| PLANT::Resource::OZONEResourceDef::CapacitatedResource::decreaseCapacity | Operation | action (nested) | v2 has no operations; emitted as nested action, calls must be re-modelled |
| PLANT::Resource::OZONEResourceDef::CapacitatedResource::allocateCapacity | Operation | action (nested) | v2 has no operations; emitted as nested action, calls must be re-modelled |
| PLANT::Resource::OZONEResourceDef::CapacitatedResource::deallocateCapacity | Operation | action (nested) | v2 has no operations; emitted as nested action, calls must be re-modelled |
| PLANT::Resource::OZONEResourceDef::ConsumableResource::deallocateCapacity | Operation | action (nested) | v2 has no operations; emitted as nested action, calls must be re-modelled |
| PLANT::Resource::ActiveResource::relationshipBetween | Property | ref | typed by AssociationClass; choose part/attribute/ref |
| PLANT::Resource::ActiveResource::canExecute | Property | ref | typed by Activity; choose part/attribute/ref |
| PLANT::Product::Product::createdBy | Property | ref | typed by Activity; choose part/attribute/ref |
| CONTROL::DecisionSupport::Admission::Propose | Class (unstereotyped) | part def | plain UML class: treated as part def; confirm it is structural |
| CONTROL::DecisionSupport::Admission::Propose::proposeLeadTime | Class (unstereotyped) | part def | plain UML class: treated as part def; confirm it is structural |
| CONTROL::DecisionSupport::Admission::Propose::proposeLeadTime::admission | Operation | action (nested) | v2 has no operations; emitted as nested action, calls must be re-modelled |
| CONTROL::DecisionSupport::Admission::Propose::proposePrice | Class (unstereotyped) | part def | plain UML class: treated as part def; confirm it is structural |
| CONTROL::DecisionSupport::Admission::Propose::proposePrice::admission | Operation | action (nested) | v2 has no operations; emitted as nested action, calls must be re-modelled |
| CONTROL::DecisionSupport::Admission::Propose::admission | Operation | action (nested) | v2 has no operations; emitted as nested action, calls must be re-modelled |
| CONTROL::DecisionSupport::Admission::simpleCapacity | Class (unstereotyped) | part def | plain UML class: treated as part def; confirm it is structural |
| CONTROL::DecisionSupport::Admission::simpleCapacity::admission | Operation | action (nested) | v2 has no operations; emitted as nested action, calls must be re-modelled |
| CONTROL::DecisionSupport::Admission::capacitatedPriority | Class (unstereotyped) | part def | plain UML class: treated as part def; confirm it is structural |
| CONTROL::DecisionSupport::Admission::capacitatedPriority::admission | Operation | action (nested) | v2 has no operations; emitted as nested action, calls must be re-modelled |
| CONTROL::DecisionSupport::Admission::Admission | Interface (UML) | port def | UML interface with operations: v2 has no operations; port def with flows, or action defs, must be chosen |
| CONTROL::DecisionSupport::Sequencing::FIFO | Class (unstereotyped) | part def | plain UML class: treated as part def; confirm it is structural |
| CONTROL::DecisionSupport::Sequencing::FIFO::sequencing | Operation | action (nested) | v2 has no operations; emitted as nested action, calls must be re-modelled; sibling name clash; emitted as 'sequencing_2' |
| CONTROL::DecisionSupport::Sequencing::prioritySequencing | Class (unstereotyped) | part def | plain UML class: treated as part def; confirm it is structural |
| CONTROL::DecisionSupport::Sequencing::Sequencing | Interface (UML) | port def | UML interface with operations: v2 has no operations; port def with flows, or action defs, must be chosen |
| CONTROL::DecisionSupport::Assignment::FirstAvailable | Class (unstereotyped) | part def | plain UML class: treated as part def; confirm it is structural |
| CONTROL::DecisionSupport::Assignment::utilizationBalancing | Class (unstereotyped) | part def | plain UML class: treated as part def; confirm it is structural |
| CONTROL::DecisionSupport::Assignment::ResourceAssignment | Interface (UML) | port def | UML interface with operations: v2 has no operations; port def with flows, or action defs, must be chosen |
| CONTROL::DecisionSupport::Scheduling::OptimalScheduling | Class (unstereotyped) | part def | plain UML class: treated as part def; confirm it is structural |
| CONTROL::DecisionSupport::Scheduling::ClarkWright_VRP | Class (unstereotyped) | part def | plain UML class: treated as part def; confirm it is structural |
| CONTROL::DecisionSupport::Scheduling::CLK_ITP | Class (unstereotyped) | part def | plain UML class: treated as part def; confirm it is structural |
| CONTROL::DecisionSupport::Scheduling::Scheduling | Interface (UML) | port def | UML interface with operations: v2 has no operations; port def with flows, or action defs, must be chosen |
| CONTROL::DecisionSupport::DynamicProcessPlanning::DynamicProcessPlanning | Interface (UML) | port def | UML interface with operations: v2 has no operations; port def with flows, or action defs, must be chosen |
| CONTROL::DecisionSupport::ChangeState::InventoryReordering | Class (unstereotyped) | part def | plain UML class: treated as part def; confirm it is structural |
| CONTROL::DecisionSupport::ChangeState::InventoryReordering::changeState | Operation | action (nested) | v2 has no operations; emitted as nested action, calls must be re-modelled |
| CONTROL::DecisionSupport::ChangeState::MachineSetup | Class (unstereotyped) | part def | plain UML class: treated as part def; confirm it is structural |
| CONTROL::DecisionSupport::ChangeState::MachineSetup::changeState | Operation | action (nested) | v2 has no operations; emitted as nested action, calls must be re-modelled |
| CONTROL::DecisionSupport::ChangeState::ChangeState | Interface (UML) | port def | UML interface with operations: v2 has no operations; port def with flows, or action defs, must be chosen |
| CONTROL::DecisionSupport::Routing::Routing | Interface (UML) | port def | UML interface with operations: v2 has no operations; port def with flows, or action defs, must be chosen |
| CONTROL::DecisionSupport::DecisionSupportStrategy | Interface (UML) | port def | UML interface with operations: v2 has no operations; port def with flows, or action defs, must be chosen |
| CONTROL::OperationalController | Class (unstereotyped) | part def | plain UML class: treated as part def; confirm it is structural |
| … 37 more in the JSON report | | | |

## Lossy mappings (44)

| Element | v1 | v2 | What was lost |
|---|---|---|---|
| PLANT::Resource::ISA95ResourceDef::Equipment::EquipmentStateModel | StateMachine | state def | 10 states / 11 transitions emitted; triggers, guards, effects and 1 pseudostates dropped |
| PLANT::Resource::ISA95ResourceDef::Equipment::controller | PartProperty | part usage | redefinition of 'controller' dropped: redefined feature has a different v2 kind |
| PLANT::Resource::OZONEResourceDef::DiscreteStateResource::DiscreteStateResourceModel | StateMachine | state def | 11 states / 7 transitions emitted; triggers, guards, effects and 1 pseudostates dropped |
| PLANT::Resource::OZONEResourceDef::HeterogeneousAggregateResource::<Property> | SharedProperty | ref part | shared aggregation semantics approximated by reference |
| PLANT::Resource::OZONEResourceDef::AggregateResource::resourcePool | SharedProperty | ref part | shared aggregation semantics approximated by reference; redefinition of 'memberResource' dropped: redefined feature has a different v2 kind |
| PLANT::Resource::OZONEResourceDef::AtomicResource::resourcePool | SharedProperty | ref part | shared aggregation semantics approximated by reference |
| PLANT::Resource::OZONEResourceDef::SimpleCapacityPool::resourcePool | SharedProperty | ref part | shared aggregation semantics approximated by reference |
| PLANT::Resource::OZONEResourceDef::StructuredCapacityPool::aggregateResourcePool | SharedProperty | ref part | shared aggregation semantics approximated by reference |
| PLANT::Resource::OZONEResourceDef::StructuredCapacityPool::batchResourcePool | SharedProperty | ref part | shared aggregation semantics approximated by reference |
| PLANT::Resource::ActiveResource | Block (SysML) | part def | generalization to external FlowNetwork dropped |
| PLANT::Resource::ActiveResource::resource | ReferenceProperty | ref part | sibling name clash; emitted as 'resource_2' |
| PLANT::Resource::PassiveResource | Block (SysML) | part def | generalization to external Commodity dropped |
| PLANT::Process::Control::Control | Activity | action def | 7 action nodes and 0 flows not migrated (activity internals require manual re-modelling) |
| PLANT::Process::Control::Implementations::RouteToResource | Activity | action def | 5 action nodes and 9 flows not migrated (activity internals require manual re-modelling) |
| PLANT::Process::Control::Implementations::AcceptJobIntoWorkCell | Activity | action def | 8 action nodes and 10 flows not migrated (activity internals require manual re-modelling) |
| PLANT::Process::Control | Activity | action def | sibling name clash; emitted as 'Control_2' |
| PLANT::Product::Product | Block (SysML) | part def | generalization to external Commodity dropped |
| PLANT::Facility::Facility | Block (SysML) | part def | generalization to external FlowNetwork dropped |
| PLANT::Facility::Layout::Geometry::SquareMatrixOfReals::elements | Property (value) | attribute usage | multiplicity expression 'self.nDims * self.nDims'..'self.nDims * self.nDims' dropped; use a v2 calc/constraint |
| PLANT::Facility::Layout::Geometry::VectorOfReals::elements | Property (value) | attribute usage | multiplicity expression 'self.nDims'..'self.nDims' dropped; use a v2 calc/constraint |
| PLANT::Facility::Layout::Placement::OffsetDimension_imported | Constraint (opaque) | constraint { doc } | expression kept as text; must be rewritten in KerML expression language |
| PLANT::Facility::Layout::Placement::OrientationDimension_imported | Constraint (opaque) | constraint { doc } | expression kept as text; must be rewritten in KerML expression language |
| PLANT::Facility::Layout::Layout Object For Movement::incidentTo | SharedProperty | ref part | shared aggregation semantics approximated by reference |
| PLANT::Facility::Layout::Interface Point::PointsDimension | Constraint (opaque) | constraint { doc } | expression kept as text; must be rewritten in KerML expression language |
| PLANT::Facility::Layout::LayoutSemanticsToAbstractANetwork::Endpoint Node::<Constraint> | Constraint (opaque) | constraint { doc } | expression kept as text; must be rewritten in KerML expression language |
| PLANT::Facility::Layout::LayoutSemanticsToAbstractANetwork::Rectangular Path Segment::<Constraint> | Constraint (opaque) | constraint { doc } | expression kept as text; must be rewritten in KerML expression language |
| PLANT::Facility::Layout::LayoutSemanticsToAbstractANetwork::Rectangular Path Segment::<Constraint> | Constraint (opaque) | constraint { doc } | expression kept as text; must be rewritten in KerML expression language |
| PLANT::Facility::Layout::LayoutSemanticsToAbstractANetwork::Rectangular Path Segment::endpoint | SharedProperty | ref part | shared aggregation semantics approximated by reference |
| PLANT::Facility::Layout::LayoutSemanticsToAbstractANetwork::Rectangular Path Segment::incidentTo | SharedProperty | ref part | shared aggregation semantics approximated by reference |
| PLANT::Facility::Layout::LayoutSemanticsToAbstractANetwork::Internal Node::<Constraint> | Constraint (opaque) | constraint { doc } | expression kept as text; must be rewritten in KerML expression language |
| PLANT::Facility::Layout::LayoutSemanticsToAbstractANetwork::PathIntersection::<Comment> | Comment <<Problem>> | comment about | <<Problem>> stereotype on comment becomes metadata |
| PLANT::Facility::Layout::LayoutSemanticsToAbstractANetwork::PathIntersection::Lshaped Intersection::endpoint | SharedProperty | ref part | shared aggregation semantics approximated by reference |
| PLANT::Facility::Layout::LayoutSemanticsToAbstractANetwork::PathIntersection::Tshaped Intersection::endpoint | SharedProperty | ref part | shared aggregation semantics approximated by reference |
| PLANT::Facility::Layout::LayoutSemanticsToAbstractANetwork::PathIntersection::+shaped Intersection::endpoint | SharedProperty | ref part | shared aggregation semantics approximated by reference |
| PLANT::Facility::Layout::LayoutSemanticsToAbstractANetwork::Rectangular Path::sharedSegment | SharedProperty | ref part | shared aggregation semantics approximated by reference |
| CONTROL::DecisionSupport::Admission::simpleCapacity::SimpleCapacity | StateMachine | state def | 2 states / 6 transitions emitted; triggers, guards, effects and 3 pseudostates dropped |
| CONTROL::DecisionSupport::Admission::simpleCapacity::SimpleCapacity | Activity | action def | sibling name clash; emitted as 'SimpleCapacity_2' |
| CONTROL::DecisionSupport::Admission::capacitatedPriority::capacitatedPriority | StateMachine | state def | 2 states / 8 transitions emitted; triggers, guards, effects and 4 pseudostates dropped |
| CONTROL::DecisionSupport::Admission::capacitatedPriority::capacitatedPriority | Activity | action def | sibling name clash; emitted as 'capacitatedPriority_2' |
| CONTROL::DecisionSupport::Sequencing::FIFO::sequencing | Activity | action def | 2 action nodes and 3 flows not migrated (activity internals require manual re-modelling) |
| CONTROL::OperationalController::messageInterface | Port (untyped) | port usage | no type; interface cannot be checked |
| CONTEXT::Task | Block (SysML) | part def | generalization to external Commodity dropped |
| DELS | Block (SysML) | part def | generalization to external FlowNetwork dropped |
| DELS::controller | PartProperty | part usage | redefinition of 'controller' dropped: redefined feature has a different v2 kind |

## Not migrated

- Diagram: SysML Block Definition Diagram: 24
- Diagram: Class Diagram: 10
- Diagram: SysML Internal Block Diagram: 6
- Constraint: 6
- AssociationClass: 3
- Comment: 3
- GeneralizationSet: 1
- Diagram: SysML Package Diagram: 1

## Validation diagnostics (47)

- WARNING cell 2 line 45:22 Duplicate of inherited member name 'controller' from ActiveResource
- WARNING cell 2 line 61:21 Duplicate of inherited member name 'canExecute' from ActiveResource
- WARNING cell 2 line 84:21 Duplicate of inherited member name 'canExecute' from ResourceAcquirer
- WARNING cell 2 line 85:22 Duplicate of inherited member name 'inTask' from ReadWriteProcessPlan, ResourceAcquirer
- WARNING cell 2 line 86:22 Duplicate of inherited member name 'outTask' from ReadWriteProcessPlan, ResourceAcquirer
- WARNING cell 2 line 83:13 Duplicate of inherited member name 'inTask' from ReadWriteProcessPlan, ResourceAcquirer
- WARNING cell 2 line 83:13 Duplicate of inherited member name 'outTask' from ReadWriteProcessPlan, ResourceAcquirer
- WARNING cell 2 line 92:22 Duplicate of inherited member name 'targetResource' from ActiveResource
- WARNING cell 2 line 108:13 Duplicate of inherited member name 'canExecute' from Queue, ResourceAcquirer
- WARNING cell 2 line 108:13 Duplicate of inherited member name 'inTask' from Queue, ResourceAcquirer
- WARNING cell 2 line 108:13 Duplicate of inherited member name 'outTask' from Queue, ResourceAcquirer
- WARNING cell 2 line 109:17 Duplicate of inherited member name 'canExecute' from ActiveResource, Queue
- WARNING cell 2 line 142:24 Duplicate of inherited member name 'queryState' from DiscreteStateResource
- WARNING cell 2 line 159:13 Duplicate of inherited member name 'deallocateCapacity' from CapacitatedResource, ConsumableResource
- WARNING cell 2 line 171:24 Duplicate of inherited member name 'deallocateCapacity' from CapacitatedResource
- WARNING cell 2 line 641:9 Duplicate of inherited member name 'controller' from ActiveResource, DELS
- WARNING cell 2 line 641:9 Duplicate of inherited member name 'relationshipBetween' from ActiveResource, DELS
- WARNING cell 2 line 672:14 Duplicate of inherited member name 'controller' from ActiveResource
- WARNING cell 2 line 687:13 Duplicate of inherited member name 'relationshipBetween' from ActiveResource
- WARNING cell 2 line 666:9 Duplicate of inherited member name 'canExecute' from ActiveResource, Queue
- WARNING cell 2 line 669:9 Duplicate of inherited member name 'canExecute' from ActiveResource, Queue
- WARNING cell 2 line 671:9 Duplicate of inherited member name 'canExecute' from ResourceAcquirer, Router
- WARNING cell 2 line 671:9 Duplicate of inherited member name 'inTask' from ReadWriteProcessPlan, ResourceAcquirer, Router
- WARNING cell 2 line 671:9 Duplicate of inherited member name 'outTask' from ReadWriteProcessPlan, ResourceAcquirer, Router
- WARNING cell 2 line 674:9 Duplicate of inherited member name 'targetResource' from ActiveResource, ChangeState
- WARNING cell 2 line 681:9 Duplicate of inherited member name 'controller' from ActiveResource, DELS
- WARNING cell 2 line 681:9 Duplicate of inherited member name 'relationshipBetween' from ActiveResource, DELS
- WARNING cell 2 line 682:9 Duplicate of inherited member name 'controller' from ActiveResource, DELS
- WARNING cell 2 line 682:9 Duplicate of inherited member name 'relationshipBetween' from ActiveResource, DELS
- WARNING cell 2 line 683:9 Duplicate of inherited member name 'controller' from ActiveResource, DELS
- WARNING cell 2 line 683:9 Duplicate of inherited member name 'relationshipBetween' from ActiveResource, DELS
- WARNING cell 2 line 691:9 Duplicate of inherited member name 'controller' from ActiveResource, DELS
- WARNING cell 2 line 691:9 Duplicate of inherited member name 'relationshipBetween' from ActiveResource, DELS
- WARNING cell 2 line 697:9 Duplicate of inherited member name 'canExecute' from Queue, ResourceAcquirer
- WARNING cell 2 line 697:9 Duplicate of inherited member name 'inTask' from Queue, ResourceAcquirer
- WARNING cell 2 line 697:9 Duplicate of inherited member name 'outTask' from Queue, ResourceAcquirer
- WARNING cell 2 line 703:17 Duplicate of inherited member name 'canExecute' from ResourceAcquirer, Router
- WARNING cell 2 line 703:17 Duplicate of inherited member name 'inTask' from ReadWriteProcessPlan, ResourceAcquirer, Router
- WARNING cell 2 line 703:17 Duplicate of inherited member name 'outTask' from ReadWriteProcessPlan, ResourceAcquirer, Router
- WARNING cell 2 line 703:28 Duplicate of inherited member name 'canExecute' from ActiveResource, Queue
- WARNING cell 2 line 704:17 Duplicate of inherited member name 'targetResource' from ActiveResource, ChangeState
- WARNING cell 2 line 718:26 Duplicate of other owned member name
- WARNING cell 2 line 719:26 Duplicate of other owned member name
- WARNING cell 2 line 720:26 Duplicate of other owned member name
- WARNING cell 2 line 721:26 Duplicate of other owned member name
- WARNING cell 2 line 724:26 Duplicate of other owned member name
- WARNING cell 2 line 727:26 Duplicate of other owned member name
