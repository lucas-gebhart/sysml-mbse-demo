# Conformance of `Beserker System Level Test Model` against the reference layer

Delivery scope: Berserker Allocated Baseline Model, Berserker Product Baseline Library, Beserker System Level Test Model, MQ-99 Berserker Functional System Architecture (34986 elements loaded across 11 projects).
Reference models: MissionArchitectureStyleGuide_Model_Version_1.0, Mission Meta Model, UML Test Profile v2_1, ClassificationProfileDistA.

## Summary

- 142 rules, 82 executable: **15 pass**, **22 fail**, 45 n.a. (nothing in the delivery to check); 60 not automatable
- failures by severity: error 8, info 6, warn 8

## Delivery completeness

| Project | Elements | In scope |
|---|---|---|
| Beserker System Level Test Model | 5035 | yes |
| Berserker Allocated Baseline Model | 4051 | yes |
| Berserker Product Baseline Library | 3418 | yes |
| UML Test Profile v2_1 | 3261 | reference / mounted |
| (U) CapyBARA | 5891 | reference / mounted |
| MQ-99 Berserker Functional System Architecture | 11285 | yes |
| OUSD Cyber Schema | 811 | reference / mounted |
| ClassificationProfileDistA | 12 | reference / mounted |
| Mission Meta Model | 588 | reference / mounted |
| CryptoProfileDistA | 580 | reference / mounted |
| BaseQueriesDistA | 54 | reference / mounted |
| MI Style Guide.mdzip | — | **MISSING** (mounted but not on disk) |

- **15 dangling references** (`health` dangling-ref: unresolved refs into unloaded/missing projects or broken ids) — counted as delivery-completeness warnings
- 1971 references into Cameo-bundled profiles / OMG spec XMI (library-ref, informational, not counted)
  - System Level::Behavior::Event Signals::external Event signals::Received::External Data Received::<Realization>: supplier -> Go Criteria - Met in unloaded project MI Style Guide.mdzip
  - System Level::Behavior::Event Signals::external Event signals::Sent::Data Sent to External::<Realization>: supplier ->  Damage Assessment in unloaded project MI Style Guide.mdzip
  - System Level::Structure::<Realization>: supplier -> Air Vehicle in unloaded project MI Style Guide.mdzip
  - System Level::Structure::<Realization>: supplier -> Confirm Target Destroyed in unloaded project MI Style Guide.mdzip
  - System Level::Structure::<Realization>: supplier -> Confirm Target Destroyed in unloaded project MI Style Guide.mdzip
  - System Level::Structure::<Realization>: supplier -> Confirm Target Destroyed in unloaded project MI Style Guide.mdzip
  - System Level::Structure::<Realization>: supplier -> Acquire Target in unloaded project MI Style Guide.mdzip
  - System Level::Structure::<Realization>: supplier -> Acquire Target in unloaded project MI Style Guide.mdzip
  - System Level::Structure::<Realization>: supplier -> Locate IRQ Target in unloaded project MI Style Guide.mdzip
  - System Level::Structure::<Realization>: supplier -> Locate IRQ Target in unloaded project MI Style Guide.mdzip

## Failed rules (22)

| Rule | Severity | Checked | Failed | Source | Text |
|---|---|---|---|---|---|
| SG-03 | warn | 123 | 123 | MissionArchitectureStyleGuide_Model_Ver… | Diagrams should follow the following naming schema: [diagram type - MET for activity flow, E2E for connectivity, SEQ for sequence] [short v… |
| SG-06 | warn | 279 | 276 | MissionArchitectureStyleGuide_Model_Ver… | Diagrams should use a Comment to capture the following information: Diagram Classification: The classification of the diagram as displayed … |
| SG-09 | warn | 8 | 7 | MissionArchitectureStyleGuide_Model_Ver… | Model Organization The containment browser should be organized as shown in the Package diagram. |
| SG-10 | info | 279 | 59 | MissionArchitectureStyleGuide_Model_Ver… | Diagram Titles should be succinct but provide information about the purpose of the diagram. A rule of thumb is to keep titles shorter than … |
| SG-14 | info | 1 | 1 | MissionArchitectureStyleGuide_Model_Ver… | A collection of resources against which the steps of the project/study's METs will be allocated against should be captured as a Resource Ar… |
| SG-17 | info | 11 | 11 | MissionArchitectureStyleGuide_Model_Ver… | All assets should have a Property asded named Country. |
| SG-23 | warn | 103 | 4 | MissionArchitectureStyleGuide_Model_Ver… | Horizontal swimlanes are be used to indicate which ResourcePerformer performs each activity. |
| SG-25 | warn | 872 | 145 | MissionArchitectureStyleGuide_Model_Ver… | The pins on each end should be typed using OperationalInformation. |
| SG-38 | error | 3 | 3 | MissionArchitectureStyleGuide_Model_Ver… | Legend «ME Study Views» marks these views as Required: Operational::Operational Processes, Operational::Operational Structure, Resources::R… |
| SG-39 | info | 3 | 3 | MissionArchitectureStyleGuide_Model_Ver… | Legend «ME Study Views» marks these views as Recommended: Strategy::Strategic Structure, Strategy::Strategic Roadmap, Strategy::Strategic T… |
| SG-40 | warn | 17 | 14 | MissionArchitectureStyleGuide_Model_Ver… | [observed in exemplar] The style guide exemplar provides these dependency matrices: 'Basic Unit Categories' (Dependency Matrix); 'Basic Uni… |
| CLS-01 | error | 279 | 276 | MissionArchitectureStyleGuide_Model_Ver… | Stereotype «Diagram Info» carries the diagram marking tags Drafter, Approver, Reviewer, Agency, Classification, Project Name, Brief Descrip… |
| MMM-01 | warn | 1 | 1 | Mission Meta Model | Profile «Mission Profile» defines the mission-level vocabulary: ActualMission, Defines, Mission, MissionThread, MissionTask, MissionEnginee… |
| UTP-03 | error | 1 | 1 | UML Test Profile v2_1 | Minimal TestConfiguration: A StructuredClassifier with «TestConfiguration» applied must at least specify one part having «TestItem» applied. |
| UTP-14 | error | 1 | 1 | UML Test Profile v2_1 | Each TestCase returns a Verdict statement: Any Behavior stereotyped as «TestCase» returns a ValueSpecification typed by verdict after arbit… |
| UTP-21 | error | 1 | 1 | UML Test Profile v2_1 | TestCase must invoke AT LEAST ONE main TestProcedure: If there is ONLY one TestProcedure invoked then the identification as the Main Proced… |
| UTP-22 | info | 1 | 1 | UML Test Profile v2_1 | Precondition is NOT specified for TestCase: DRTC03 |
| UTP-28 | error | 13 | 4 | UML Test Profile v2_1 | TestProcedure must prescribe the execution order of AT LEAST one AtomicProceduralElement |
| UTP-30 | info | 13 | 13 | UML Test Profile v2_1 | Precondition is NOT specified for TestProcedure |
| UTP-31 | error | 13 | 4 | UML Test Profile v2_1 | TestProcedure must prescribe the execution order of AT LEAST one ProceduralElement |
| UTP-33 | error | 13 | 13 | UML Test Profile v2_1 | TestProcedure operates on a TestConfiguration: A TestProcedure must always run on a (potentially implicit) TestConfiguration comprising at … |
| CLS-02 | warn | 18 | 18 | UML Test Profile v2_1 | Stereotype «Data Control Markings» carries the tags Authorized Audience, Reason for Control, Distribution Statement Date of Determination, … |

**SG-03** — Diagrams should follow the following naming schema: [diagram type - MET for activity flow, E2E for connectivity, SEQ for sequence] [short vignette ID] [Country Code of performer(s)] [Short name - les…  
source: `MASG Architecture Management::Comments`; activity/connectivity/sequence diagram names must start with one of ['E2E', 'MET', 'OOB', 'SEQ']  
- Basic Test Data::Berserker Operational Testing Configuration::Berserker Operational Testing Configuration::Berserker Operational Testing Configuration (SysML Internal Block Diagram)
- Basic Test Data::Berserker Operational Testing Configuration::Berserker System Level Operational Flight Test::Berserker System Level Operational Flight Test (SysML Activity Diagram)
- Basic Test Data::Berserker Operational Testing Configuration::Load OFPs Operational Test Procedue::Load OFPs Operational Test Procedue (SysML Activity Diagram)
- Basic Test Data::Berserker Operational Testing Configuration::Power Up Essential Systems Operational Test Procedure::Power Up Essential Systems Operational Test Procedure (SysML Activity Diagram)
- Basic Test Data::Berserker Operational Testing Configuration::Establish Navigation Operational Test Procedure::Establish Navigation Operational Test Procedure (SysML Activity Diagram)
- Basic Test Data::Berserker Operational Testing Configuration::Launch UAS Op Test Procedure::Launch UAS Op Test Procedure (SysML Activity Diagram)
- Basic Test Data::Berserker Operational Testing Configuration::Operational Communication Test Procedure::Operational Communication Test Procedure (SysML Activity Diagram)
- Basic Test Data::Berserker Operational Testing Configuration::Operational Semi Autonomous Flight Test Procedure::Operational Semi Autonomous Flight Test Procedure (SysML Activity Diagram)
- Basic Test Data::Berserker Operational Testing Configuration::Operational Target Detection Procedure::Operational Target Detection Procedure (SysML Activity Diagram)
- Basic Test Data::Berserker Operational Testing Configuration::Operational Target Desctruction Test Procedure::Operational Target Desctruction Test Procedure (SysML Activity Diagram)
- … 113 more

**SG-06** — Diagrams should use a Comment to capture the following information: Diagram Classification: The classification of the diagram as displayed in a read-only format. Narrative: Description of the purpose…  
source: `MASG Architecture Management::Comments`; diagrams without documentation / classification-narrative comment  
- Landing Page (SysML Package Diagram)
- Basic Test Data::Procedures (Generic Table)
- Basic Test Data::Berserker Operational Testing Configuration::Berserker Operational Testing Configuration::Berserker Operational Testing Configuration (SysML Internal Block Diagram)
- Basic Test Data::Berserker Operational Testing Configuration::Berserker System Level Operational Flight Test::Berserker System Level Operational Flight Test (SysML Activity Diagram)
- Basic Test Data::Berserker Operational Testing Configuration::Load OFPs Operational Test Procedue::Load OFPs Operational Test Procedue (SysML Activity Diagram)
- Basic Test Data::Berserker Operational Testing Configuration::Establish Navigation Operational Test Procedure::Establish Navigation Operational Test Procedure (SysML Activity Diagram)
- Basic Test Data::Berserker Operational Testing Configuration::Launch UAS Op Test Procedure::Launch UAS Op Test Procedure (SysML Activity Diagram)
- Basic Test Data::Berserker Operational Testing Configuration::Operational Communication Test Procedure::Operational Communication Test Procedure (SysML Activity Diagram)
- Basic Test Data::Berserker Operational Testing Configuration::Operational Semi Autonomous Flight Test Procedure::Operational Semi Autonomous Flight Test Procedure (SysML Activity Diagram)
- Basic Test Data::Berserker Operational Testing Configuration::Operational Target Detection Procedure::Operational Target Detection Procedure (SysML Activity Diagram)
- … 266 more

**SG-09** — Model Organization The containment browser should be organized as shown in the Package diagram.  
source: `MASG Architecture Management::Comments`; delivery top-level packages: Basic Test Data, Test Activities, Test Data, Test Signals, Base Classifiers, Allocated Behavior, Reporting Tables, Derived Properties, Allocated Blocks, Allocated Interfaces, Implementation Hardware, Implementation Software, Configurations, Derived Properties, Other Data, Unit Imports, Sub System Level, System Level  
- Architecture Management<<Architecture_Management>>
- Failure Analysis<<Security>>
- MASG Architecture Management<<ArchitecturalDescription>>
- MASG Architecture Management<<Info>>
- Operational<<Operational>>
- Strategy<<Strategy>>
- Summary & Overview<<Summary___Overview>>

**SG-10** — Diagram Titles should be succinct but provide information about the purpose of the diagram. A rule of thumb is to keep titles shorter than 30 characters.  
source: `MASG Architecture Management::Comments::<Comment>`; diagram titles longer than 30 characters  
- Basic Test Data::Berserker Operational Testing Configuration::Berserker Operational Testing Configuration::Berserker Operational Testing Configuration (43 chars)
- Basic Test Data::Berserker Operational Testing Configuration::Berserker System Level Operational Flight Test::Berserker System Level Operational Flight Test (46 chars)
- Basic Test Data::Berserker Operational Testing Configuration::Load OFPs Operational Test Procedue::Load OFPs Operational Test Procedue (35 chars)
- Basic Test Data::Berserker Operational Testing Configuration::Power Up Essential Systems Operational Test Procedure::Power Up Essential Systems Operational Test Procedure (53 chars)
- Basic Test Data::Berserker Operational Testing Configuration::Establish Navigation Operational Test Procedure::Establish Navigation Operational Test Procedure (47 chars)
- Basic Test Data::Berserker Operational Testing Configuration::Operational Communication Test Procedure::Operational Communication Test Procedure (40 chars)
- Basic Test Data::Berserker Operational Testing Configuration::Operational Semi Autonomous Flight Test Procedure::Operational Semi Autonomous Flight Test Procedure (49 chars)
- Basic Test Data::Berserker Operational Testing Configuration::Operational Target Detection Procedure::Operational Target Detection Procedure (38 chars)
- Basic Test Data::Berserker Operational Testing Configuration::Operational Target Desctruction Test Procedure::Operational Target Desctruction Test Procedure (46 chars)
- Basic Test Data::Berserker Operational Testing Configuration::Operational Target Damage Assessment Test::Operational Target Damage Assessment Test (41 chars)
- … 49 more

**SG-14** — A collection of resources against which the steps of the project/study's METs will be allocated against should be captured as a Resource Architecture.  
source: `Resources::Not Used::Orders of Battle::Operation DESERT STORM Baseline Study Assets`; 0 «ResourceArchitecture» in delivery  
- delivery defines no «ResourceArchitecture»

**SG-17** — All assets should have a Property asded named Country.  
source: `Resources::Not Used::Orders of Battle::Operation DESERT STORM Baseline Study Assets::USA Order of Battle::Country`; UAF assets without a 'Country' property  
- Basic Test Data::Resources::System Test Operator
- Basic Test Data::Resources::Ground Control Station Operator
- Basic Test Data::Resources::Ground Test Operator
- Basic Test Data::Resources::Test Lead
- Basic Test Data::Resources::Ground Control Station
- Basic Test Data::Resources::Launch System
- Basic Test Data::Resources::Cyber Test Operator
- Basic Test Data::Resources::Flight Control
- Basic Test Data::Resources::Rail Launch System
- Basic Test Data::Resources::Range Control
- … 1 more

**SG-23** — Horizontal swimlanes are be used to indicate which ResourcePerformer performs each activity.  
source: `MASG Architecture Management::Comments`; activities with actions but no swimlane (ActivityPartition)  
- Basic Test Data::Berserker Operational Testing Configuration::Berserker System Level Operational Flight Test
- Basic Test Data::Berserker Operational Testing Configuration::Operational Communication Test Procedure
- Sub System Level::Stores Management System::Missile Model Content::Behavior::Power On Missile
- Sub System Level::Navigation System::Behavior::Ingest Nav Sensor Parameters::Process Sensor Data::Provide Raw Heading Data

**SG-25** — The pins on each end should be typed using OperationalInformation.  
source: `MASG Architecture Management::Comments`; 727 pins typed, 250 of them by UAF Operational/ResourceInformation  
- Basic Test Data::Berserker Operational Testing Configuration::Berserker System Level Operational Flight Test::<InputPin>
- Basic Test Data::Berserker Operational Testing Configuration::Load OFPs Operational Test Procedue::input
- Basic Test Data::Berserker Operational Testing Configuration::Load OFPs Operational Test Procedue::input
- Basic Test Data::Berserker Operational Testing Configuration::Load OFPs Operational Test Procedue::output
- Basic Test Data::Berserker Operational Testing Configuration::Load OFPs Operational Test Procedue::input
- Basic Test Data::Berserker Operational Testing Configuration::Power Up Essential Systems Operational Test Procedure::input
- Basic Test Data::Berserker Operational Testing Configuration::Power Up Essential Systems Operational Test Procedure::result
- Basic Test Data::Berserker Operational Testing Configuration::Power Up Essential Systems Operational Test Procedure::output
- Basic Test Data::Berserker Operational Testing Configuration::Power Up Essential Systems Operational Test Procedure::input
- Basic Test Data::Berserker Operational Testing Configuration::Power Up Essential Systems Operational Test Procedure::input
- … 135 more

**SG-38** — Legend «ME Study Views» marks these views as Required: Operational::Operational Processes, Operational::Operational Structure, Resources::Resources Processes  
source: `MASG Architecture Management::Legends::ME Study Views::Required`; delivery diagram types: Class Diagram, Dependency Matrix, Free Form Diagram, Generic Table, Package Diagram, Relation Map Diagram, Requirement Diagram, Requirement Table, SysML Activity Diagram, SysML Allocation Matrix, SysML Block Definition Diagram, SysML Internal Block Diagram, SysML Package Diagram, SysML State Machine Diagram, SysML Use Case Diagram  
- Operational Processes
- Operational Structure
- Resources Processes

**SG-39** — Legend «ME Study Views» marks these views as Recommended: Strategy::Strategic Structure, Strategy::Strategic Roadmap, Strategy::Strategic Traceability  
source: `MASG Architecture Management::Legends::ME Study Views::Recommended`; delivery diagram types: Class Diagram, Dependency Matrix, Free Form Diagram, Generic Table, Package Diagram, Relation Map Diagram, Requirement Diagram, Requirement Table, SysML Activity Diagram, SysML Allocation Matrix, SysML Block Definition Diagram, SysML Internal Block Diagram, SysML Package Diagram, SysML State Machine Diagram, SysML Use Case Diagram  
- Strategic Structure
- Strategic Roadmap
- Strategic Traceability

**SG-40** — [observed in exemplar] The style guide exemplar provides these dependency matrices: 'Basic Unit Categories' (Dependency Matrix); 'Basic Units' (Dependency Matrix); 'Implementation Matrix' (Implementa…  
source: `MASG Architecture Management`; delivery has 11 matrix diagrams: Dependency Matrix, SysML Allocation Matrix  
- Implementation Matrix (Implementation Matrix)
- Functions to Operational Activities Mapping Matrix (Functions to Operational Activities Mapping Matrix)
- Resources to Operational Activities Mapping Matrix (Resources to Operational Activities Mapping Matrix)
- Resources Traceability (Dependency Matrix)
- Exchanges Implementation (Implementation Matrix)
- InformationElements (Dependency Matrix)
- OperationalInterfacestoResourceInterfaces Mapping (Dependency Matrix)
- Measures applied to behaviors (Dependency Matrix)
- Conduct SEAD Decomposition (Dependency Matrix)
- Generalization of measures (Dependency Matrix)
- … 4 more

**CLS-01** — Stereotype «Diagram Info» carries the diagram marking tags Drafter, Approver, Reviewer, Agency, Classification, Project Name, Brief Description, Designation Markings, MVersion; the exemplar applies i…  
source: `MASG Architecture Management::Diagram Properties Profile::Diagram Info`; diagrams without a classification marking  
- Landing Page (SysML Package Diagram)
- Basic Test Data::Procedures (Generic Table)
- Basic Test Data::Berserker Operational Testing Configuration::Berserker Operational Testing Configuration::Berserker Operational Testing Configuration (SysML Internal Block Diagram)
- Basic Test Data::Berserker Operational Testing Configuration::Berserker System Level Operational Flight Test::Berserker System Level Operational Flight Test (SysML Activity Diagram)
- Basic Test Data::Berserker Operational Testing Configuration::Load OFPs Operational Test Procedue::Load OFPs Operational Test Procedue (SysML Activity Diagram)
- Basic Test Data::Berserker Operational Testing Configuration::Establish Navigation Operational Test Procedure::Establish Navigation Operational Test Procedure (SysML Activity Diagram)
- Basic Test Data::Berserker Operational Testing Configuration::Launch UAS Op Test Procedure::Launch UAS Op Test Procedure (SysML Activity Diagram)
- Basic Test Data::Berserker Operational Testing Configuration::Operational Communication Test Procedure::Operational Communication Test Procedure (SysML Activity Diagram)
- Basic Test Data::Berserker Operational Testing Configuration::Operational Semi Autonomous Flight Test Procedure::Operational Semi Autonomous Flight Test Procedure (SysML Activity Diagram)
- Basic Test Data::Berserker Operational Testing Configuration::Operational Target Detection Procedure::Operational Target Detection Procedure (SysML Activity Diagram)
- … 266 more

**MMM-01** — Profile «Mission Profile» defines the mission-level vocabulary: ActualMission, Defines, Mission, MissionThread, MissionTask, MissionEngineeringThread, ActualMissionPhase, DesignationKind, MissionScen…  
source: `Mission Profile`; applied: none  
- delivery applies none of ActualMission, Defines, Mission, MissionThread, MissionTask, MissionEngineeringThread, ActualMissionPhase, DesignationKind…

**UTP-03** — Minimal TestConfiguration: A StructuredClassifier with «TestConfiguration» applied must at least specify one part having «TestItem» applied.  
source: `UML_Testing_Profile_v2.1::Test Architecture::TestConfiguration`; 11 parts across 1 TestConfiguration(s); offenders have no part with «TestItem»  
- Basic Test Data::Berserker Operational Testing Configuration::Berserker Operational Testing Configuration

**UTP-14** — Each TestCase returns a Verdict statement: Any Behavior stereotyped as «TestCase» returns a ValueSpecification typed by verdict after arbitration had happened.  
source: `UML_Testing_Profile_v2.1::Test Behavior::Test-specific Procedures::TestCase`; TestCases without an out/return Parameter typed by Verdict  
- Basic Test Data::Berserker Operational Testing Configuration::Berserker System Level Operational Flight Test

**UTP-21** — TestCase must invoke AT LEAST ONE main TestProcedure: If there is ONLY one TestProcedure invoked then the identification as the Main ProcedurePhaseKind is not necessary. If more than one TestProcedur…  
source: `UML_Testing_Profile_v2.1::Test Behavior::Test-specific Procedures::TestCase`; TestCases invoking several TestProcedures need one main ProcedureInvocation  
- Basic Test Data::Berserker Operational Testing Configuration::Berserker System Level Operational Flight Test invokes 13 TestProcedures, none marked «ProcedureInvocation» role=main

**UTP-22** — Precondition is NOT specified for TestCase: DRTC03  
source: `UML_Testing_Profile_v2.1::Test Behavior::Test-specific Procedures::TestCase`; «TestCase» without a precondition  
- Basic Test Data::Berserker Operational Testing Configuration::Berserker System Level Operational Flight Test

**UTP-28** — TestProcedure must prescribe the execution order of AT LEAST one AtomicProceduralElement  
source: `UML_Testing_Profile_v2.1::Test Behavior::Test-specific Procedures::TestProcedure`; TestProcedure activities without any action/node (empty procedure)  
- Basic Test Data::Berserker Operational Testing Configuration::Operational Flight Test Setup
- Basic Test Data::Berserker Operational Testing Configuration::Operational Flight Test Teardown
- Basic Test Data::Berserker Operational Testing Configuration::Operaitonal Power Test
- Basic Test Data::Berserker Operational Testing Configuration::Operational Landing Test Procedure

**UTP-30** — Precondition is NOT specified for TestProcedure  
source: `UML_Testing_Profile_v2.1::Test Behavior::Test-specific Procedures::TestProcedure`; «TestProcedure» without a precondition  
- Basic Test Data::Berserker Operational Testing Configuration::Operational Flight Test Setup
- Basic Test Data::Berserker Operational Testing Configuration::Operational Flight Test Teardown
- Basic Test Data::Berserker Operational Testing Configuration::Load OFPs Operational Test Procedue
- Basic Test Data::Berserker Operational Testing Configuration::Power Up Essential Systems Operational Test Procedure
- Basic Test Data::Berserker Operational Testing Configuration::Establish Navigation Operational Test Procedure
- Basic Test Data::Berserker Operational Testing Configuration::Launch UAS Op Test Procedure
- Basic Test Data::Berserker Operational Testing Configuration::Operaitonal Power Test
- Basic Test Data::Berserker Operational Testing Configuration::Operational Communication Test Procedure
- Basic Test Data::Berserker Operational Testing Configuration::Operational Semi Autonomous Flight Test Procedure
- Basic Test Data::Berserker Operational Testing Configuration::Operational Target Detection Procedure
- … 3 more

**UTP-31** — TestProcedure must prescribe the execution order of AT LEAST one ProceduralElement  
source: `UML_Testing_Profile_v2.1::Test Behavior::Test-specific Procedures::TestProcedure`; TestProcedure activities without any action/node (empty procedure)  
- Basic Test Data::Berserker Operational Testing Configuration::Operational Flight Test Setup
- Basic Test Data::Berserker Operational Testing Configuration::Operational Flight Test Teardown
- Basic Test Data::Berserker Operational Testing Configuration::Operaitonal Power Test
- Basic Test Data::Berserker Operational Testing Configuration::Operational Landing Test Procedure

**UTP-33** — TestProcedure operates on a TestConfiguration: A TestProcedure must always run on a (potentially implicit) TestConfiguration comprising at least one instance of a TestComponent connected to a TestIte…  
source: `UML_Testing_Profile_v2.1::Test Behavior::Test-specific Procedures::TestProcedure`; TestProcedures must run on a TestConfiguration with at least one TestItem  
- Basic Test Data::Berserker Operational Testing Configuration::Operational Flight Test Setup: TestConfiguration has no «TestItem» part
- Basic Test Data::Berserker Operational Testing Configuration::Operational Flight Test Teardown: TestConfiguration has no «TestItem» part
- Basic Test Data::Berserker Operational Testing Configuration::Load OFPs Operational Test Procedue: TestConfiguration has no «TestItem» part
- Basic Test Data::Berserker Operational Testing Configuration::Power Up Essential Systems Operational Test Procedure: TestConfiguration has no «TestItem» part
- Basic Test Data::Berserker Operational Testing Configuration::Establish Navigation Operational Test Procedure: TestConfiguration has no «TestItem» part
- Basic Test Data::Berserker Operational Testing Configuration::Launch UAS Op Test Procedure: TestConfiguration has no «TestItem» part
- Basic Test Data::Berserker Operational Testing Configuration::Operaitonal Power Test: TestConfiguration has no «TestItem» part
- Basic Test Data::Berserker Operational Testing Configuration::Operational Communication Test Procedure: TestConfiguration has no «TestItem» part
- Basic Test Data::Berserker Operational Testing Configuration::Operational Semi Autonomous Flight Test Procedure: TestConfiguration has no «TestItem» part
- Basic Test Data::Berserker Operational Testing Configuration::Operational Target Detection Procedure: TestConfiguration has no «TestItem» part
- … 3 more

**CLS-02** — Stereotype «Data Control Markings» carries the tags Authorized Audience, Reason for Control, Distribution Statement Date of Determination, Controlling Office, Declassify On, Reason for Security Class…  
source: `UML_Testing_Profile_v2.1::Data Rights and Dissemination Control Markings Profile::Data Control Markings Profile::Data Control Markings`; top-level packages without a marking stereotype/tag  
- Basic Test Data
- Test Activities
- Test Data
- Test Signals
- Base Classifiers
- Allocated Behavior
- Reporting Tables
- Derived Properties
- Allocated Blocks
- Allocated Interfaces
- … 8 more


## Passed rules (15)

| Rule | Severity | Checked | Failed | Source | Text |
|---|---|---|---|---|---|
| SG-41 | info | 18 | 0 | MissionArchitectureStyleGuide_Model_Ver… | [observed in exemplar] All 8 top-level packages use Title Case names: MASG Architecture Management, Architecture Management, Summary, Resou… |
| UTP-15 | error | 1 | 0 | UML Test Profile v2_1 | TestCase with owned UseCases NOT allowed: A BehavioredClassifier or Behavior with «TestCase» applied must not own UseCases with «TestCase» … |
| UTP-16 | error | 1 | 0 | UML Test Profile v2_1 | TestCase requires AT MOST ONE precondition: DRTC03 |
| UTP-17 | error | 1 | 0 | UML Test Profile v2_1 | Allowed TestCase invocation scheme: A TestCase must only invoke TestProcedure or procedures, but not other TestCases or TestExecutionSchedu… |
| UTP-18 | error | 1 | 0 | UML Test Profile v2_1 | TestCase guarantees AT MOST ONE post condition: DRTC06 |
| UTP-19 | error | 1 | 0 | UML Test Profile v2_1 | Behavior TestCase with nested Behavior TestCase NOT allowed: A Behavior with «TestCase» applied must not nest any other Behavior that has «… |
| UTP-23 | error | 1 | 0 | UML Test Profile v2_1 | TestCase must refer to AT MOST ONE arbitrationspecification: A TestCase must only invoke TestProcedure or procedures, but not other TestCas… |
| UTP-29 | error | 13 | 0 | UML Test Profile v2_1 | TestProcedure requires ATMOST ONE precondition defined |
| UTP-32 | error | 13 | 0 | UML Test Profile v2_1 | TestProcedure guarantees AT MOST ONE postcondition |
| UTP-34 | info | 13 | 0 | UML Test Profile v2_1 | Allowed TestProcedure invocation scheme: A TestProcedure must only invoke other TestProcedures or procedures. |
| UTP-35 | info | 13 | 0 | UML Test Profile v2_1 | TestProcedure use of ProcedureInvocation: A TestProcedure must not make use of the role attribute (i.e., main, setup, teardown) of «Procedu… |
| UTP-62 | info | 1 | 0 | UML Test Profile v2_1 | TestContext should specify AT MOST ONE TestLevel |
| UTP-63 | info | 1 | 0 | UML Test Profile v2_1 | TestContext should specify AT MOST ONE TestType |
| UTP-64 | info | 1 | 0 | UML Test Profile v2_1 | TestContext should NOT be applied to Profile metaclass |
| UTP-65 | info | 3 | 0 | UML Test Profile v2_1 | TestObjective should ONLY be applied to Class metaclass or extension thereof |

## Not applicable (nothing in the delivery to check) (45)

| Rule | Severity | Checked | Failed | Source | Text |
|---|---|---|---|---|---|
| SG-21 | warn | 0 | 0 | MissionArchitectureStyleGuide_Model_Ver… | USA METs and their related MTs should be linked using the Implements relationship. This could be done using a Resources Processes diagram o… |
| MMM-02 | error | 0 | 0 | Mission Meta Model | «ActualMission» extends metaclass InstanceSpecification; specializes «ActualEnterprisePhase» |
| MMM-03 | error | 0 | 0 | Mission Meta Model | «Defines» extends metaclass Abstraction; specializes «MeasurableElement», «Allocate» |
| MMM-04 | error | 0 | 0 | Mission Meta Model | «Mission» extends metaclass Class; specializes «StrategicPhase»; tags: MK: Mission Kind |
| MMM-05 | error | 0 | 0 | Mission Meta Model | «MissionThread» extends metaclass Activity; specializes «OperationalActivity» |
| MMM-06 | error | 0 | 0 | Mission Meta Model | «MissionTask» extends metaclass Activity; specializes «MissionThread» |
| MMM-07 | error | 0 | 0 | Mission Meta Model | «MissionEngineeringThread» extends metaclass Activity; specializes «Function» |
| MMM-08 | error | 0 | 0 | Mission Meta Model | «ActualMissionPhase» extends metaclass InstanceSpecification; specializes «ActualMission» |
| MMM-09 | error | 0 | 0 | Mission Meta Model | «DesignationKind» extends metaclass Enumeration; specializes «MeasurableElement», «ValueType» |
| MMM-10 | error | 0 | 0 | Mission Meta Model | «MissionScenario» extends metaclass DataType; specializes «Condition» |
| MMM-11 | error | 0 | 0 | Mission Meta Model | «MissionVignette» extends metaclass DataType; specializes «Condition» |
| MMM-12 | error | 0 | 0 | Mission Meta Model | «ActualMissionScenario» extends metaclass InstanceSpecification; specializes «ActualCondition» |
| MMM-13 | error | 0 | 0 | Mission Meta Model | «ActualMissionVignette» extends metaclass InstanceSpecification; specializes «ActualCondition» |
| MMM-14 | error | 0 | 0 | Mission Meta Model | «Opposes» extends metaclass Dependency; specializes «MeasurableElement» |
| MMM-15 | error | 0 | 0 | Mission Meta Model | «mop» extends metaclass Property. A measure of effectiveness (moe) represents a parameter whose value is critical for achieving the desired… |
| MMM-16 | error | 0 | 0 | Mission Meta Model | «mos» extends metaclass Property. A measure of effectiveness (moe) represents a parameter whose value is critical for achieving the desired… |
| MMM-17 | error | 0 | 0 | Mission Meta Model | «mosu» extends metaclass Property. A measure of effectiveness (moe) represents a parameter whose value is critical for achieving the desire… |
| MMM-18 | error | 0 | 0 | Mission Meta Model | «Conflicts With» extends metaclass Comment; specializes «Problem», «MeasurableElement» |
| MMM-19 | error | 0 | 0 | Mission Meta Model | «Doctrine» extends metaclass Class; specializes «Standard»; tags: createdBy: ActualOrganizationalResource, publishedBy: ActualOrganizationa… |
| MMM-20 | error | 0 | 0 | Mission Meta Model | «MissionThreadAction» extends metaclass CallBehaviorAction; specializes «OperationalActivityAction» |
| MMM-21 | error | 0 | 0 | Mission Meta Model | «OpposableElement» extends metaclass Element; tags: FD: ForceDesignation |
| MMM-22 | error | 0 | 0 | Mission Meta Model | Client is incorrect for Defines: OCL: self.client->forAll(e\| e.ocllsKindOf(Activity)) |
| MMM-23 | error | 0 | 0 | Mission Meta Model | Defines.client: Value for the client metaproperty must be stereotyped a specialization of «Activity». |
| MMM-24 | error | 0 | 0 | Mission Meta Model | Defines.supplier: Value for the supplier metaproperty must be a StrategicPhase. |
| MMM-25 | error | 0 | 0 | Mission Meta Model | Supplier is Incorrect for Defines: OCL: self.supplier->forAll(e\| e.oclIsKindOf(StrategicPhase)) |
| MMM-26 | error | 0 | 0 | Mission Meta Model | Client is incorrect for Opposes: OCL: self.client->forAll(e\| e.ocllsKindOf(OpposableElement)) |
| MMM-27 | error | 0 | 0 | Mission Meta Model | Opposes.client: Value for the client metaproperty must be an OpposableElement. |
| MMM-28 | error | 0 | 0 | Mission Meta Model | Opposes.supplier: Value for the supplier metaproperty must be an OpposableElement. |
| MMM-29 | error | 0 | 0 | Mission Meta Model | Supplier is Incorrect for Opposes: OCL: self.supplier->forAll(e\| e.oclIsKindOf(OpposableElement)) |
| UTP-25 | error | 0 | 0 | UML Test Profile v2_1 | TestExecutionSchedule requires ATMOST ONE precondition |
| UTP-26 | error | 0 | 0 | UML Test Profile v2_1 | TestExecutionSchedule should guarantee AT MOST one postcondition |
| UTP-27 | info | 0 | 0 | UML Test Profile v2_1 | Precondition is NOT specified for TestExecutionSchedule |
| UTP-39 | error | 0 | 0 | UML Test Profile v2_1 | Alternative application in Activities: In an Activity, «Alternative» must only be applied to ConditionalNode. |
| UTP-40 | error | 0 | 0 | UML Test Profile v2_1 | Loop application in Activities: In an Activity, «Loop» must only be applied to LoopNode. |
| UTP-42 | error | 0 | 0 | UML Test Profile v2_1 | Negative application in Activities: In an Activity, «Negative» must only be applied to StructuredActivityNode. |
| UTP-45 | error | 0 | 0 | UML Test Profile v2_1 | Parallel application in Activities: In an Activity, «Parallel» must only be applied to ConditionalNode. |
| UTP-47 | error | 0 | 0 | UML Test Profile v2_1 | Sequence application in Activities: If applied on a StructuredActivityNode, the StructuredActivityNode must be a SequenceNode. |
| UTP-51 | error | 0 | 0 | UML Test Profile v2_1 | DataProvider must have a DataSpecification for providing data: This is done through a refines relationship or the dataprovider owns the dat… |
| UTP-53 | error | 0 | 0 | UML Test Profile v2_1 | Restriction of Overrides client and supplier: As client and supplier of the underlying Dependency, only InstanceSpecification are allowed. |
| UTP-59 | error | 0 | 0 | UML Test Profile v2_1 | TestLogElement extended metaclass restriction: «TestLogElement» shall not be applied to EnumerationLiteral. |
| UTP-61 | error | 0 | 0 | UML Test Profile v2_1 | TestSet should have AT MOST one arbitration specification |
| UTP-66 | info | 0 | 0 | UML Test Profile v2_1 | TestRequirement should ONLY be applied to Class metaclass or extension thereof |
| UTP-67 | info | 0 | 0 | UML Test Profile v2_1 | TestSet should NOT be applied to Profile metaclass |
| CLS-03 | error | 0 | 0 | ClassificationProfileDistA | Enumeration «Classifications» defines the allowed values Unclassified, Confidential, Secret, Top Secret. Classification field represents th… |
| CLS-04 | error | 0 | 0 | ClassificationProfileDistA | Enumeration «HandlingCaveats» defines the allowed values CUI. Marking values are drawn from this enumeration. |

## Not automatable (60)

Listed with their text in `reference_rules.md`; ids: SG-01, SG-02, SG-04, SG-05, SG-07, SG-08, SG-11, SG-12, SG-13, SG-15, SG-16, SG-18, SG-19, SG-20, SG-22, SG-24, SG-26, SG-27, SG-28, SG-29, SG-30, SG-31, SG-32, SG-33, SG-34, SG-35, SG-36, SG-37, UTP-01, UTP-02, UTP-04, UTP-05, UTP-06, UTP-07, UTP-08, UTP-09, UTP-10, UTP-11, UTP-12, UTP-13, UTP-20, UTP-24, UTP-36, UTP-37, UTP-38, UTP-41, UTP-43, UTP-44, UTP-46, UTP-48, UTP-49, UTP-50, UTP-52, UTP-54, UTP-55, UTP-56, UTP-57, UTP-58, UTP-60, UTP-68
