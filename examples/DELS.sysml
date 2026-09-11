package PLANT {
    private import 'DELS Profile'::*;
    private import RequirementDerivation::*;
    package Resource {
        part def Resource {
            ref part isLocatedIn : PLANT::Facility::Facility;
            attribute operatingState : ScalarValues::String;
            attribute utilization : ScalarValues::Real[0];
            attribute measure : ScalarValues::Real[0..*];
            part memberResource : PLANT::Resource::Resource[0..*];
            ref part resourceGroup : PLANT::Resource::Resource[0..*];
            ref part requiredByProduct : PLANT::Product::Product[0..*];
            ref requiredByProcess[0..*];
            connect memberResource to memberResource;
        }
        package ISA95ResourceDef {
            part def Material :> PLANT::Resource::Resource, PLANT::Resource::PassiveResource {
                ref part requiredBy : PLANT::Product::Product[0..*];
            }
            part def Personnel :> PLANT::Resource::Resource {
            }
            part def Equipment :> PLANT::Resource::Resource, PLANT::Resource::ActiveResource {
                state def EquipmentStateModel {
                    state Ready;
                    state Processing;
                    state Executing;
                    state Active;
                    state Idle;
                    state Starved;
                    state Blocked;
                    state Down;
                    state Setup;
                    state Off;
                    transition Down then Ready;
                    transition Setup then Ready;
                    transition Ready then Setup;
                    transition Ready then Down;
                    transition Down then Off;
                    transition Off then Setup;
                    transition Setup then Down;
                    transition Down then Setup;
                    transition Processing then Idle;
                    transition Idle then Processing;
                }
                part controller : PLANT::Resource::ISA95ResourceDef::Equipment::RealtimeController;
                part def RealtimeController {
                }
            }
            part def Information :> PLANT::Resource::Resource {
            }
        }
        package ControlActuator {
            part def AdmissionGate :> PLANT::Resource::ControlActuator::Actuator {
                ref canExecute :>> canExecute;
                port incomingTask : CONTEXT::inDELSTask[0..*];
                port availableTask : CONTEXT::outDELSTask[0..*];
                port rejectedTask : CONTEXT::outDELSTask[0..*];
                action admit { in incomingTasks; out availableTasks; in admissionDecision; out rejectedTasks; }
            }
            part def Queue :> PLANT::Resource::ControlActuator::Actuator {
                ref canExecute;
                port outTask : CONTEXT::outDELSTask[0..*];
                port inTask : CONTEXT::inDELSTask[0..*];
                action sequence { in availableTasks; in index; out orderedTasks; }
            }
            part def ResourceAcquirer :> PLANT::Resource::ControlActuator::Actuator {
                ref canExecute :>> canExecute;
                port inTask : CONTEXT::inDELSTask[0..*];
                port acquiredResource : CONTEXT::outDELSResource[0..*];
                port availableResource : CONTEXT::inDELSResource[0..*];
                port outTask : CONTEXT::outDELSTask[0..*];
                part def SendTaskToResource :> PLANT::Resource::ControlActuator::ResourceAcquirer {
                }
                part def ResourceToTask :> PLANT::Resource::ControlActuator::ResourceAcquirer {
                }
                action acquireResource { in targetTask; in resourceAssignment; in availableResources; out acquiredResources; }
            }
            part def Release :> PLANT::Resource::Resource {
                port releasedResource : CONTEXT::outDELSResource[0..*];
                port completedTask : CONTEXT::outDELSTask;
                port resource : CONTEXT::inDELSResource[0..*];
            }
            part def Router :> PLANT::Resource::ControlActuator::Actuator, PLANT::Resource::ControlActuator::ReadWriteProcessPlan, PLANT::Resource::ControlActuator::ResourceAcquirer::SendTaskToResource {
                ref canExecute :>> canExecute;
                port inTask : CONTEXT::inDELSTask[0..*];
                port outTask : CONTEXT::outDELSTask[0..*];
                part readWriteProcessPlan : PLANT::Resource::ControlActuator::ReadWriteProcessPlan[0..*];
                part resourceAcquirer : PLANT::Resource::ControlActuator::ResourceAcquirer[0..*];
                action Route { in inTask; in assignedResource; out outTask; in updatedProcessPlan; }
            }
            part def ChangeState :> PLANT::Resource::ControlActuator::Actuator {
                port targetResource : CONTEXT::inDELSResource[0];
                port auxillaryResources : CONTEXT::inDELSResource[0..*];
                port releasedResources : CONTEXT::outDELSResource[0..*];
                ref canExecute :>> canExecute;
                port overheadTask : CONTEXT::outDELSTask[0..*];
                action ChangeState { in targetResource; in newState; out overheadTask; }
            }
            part def Actuator :> PLANT::Resource::ActiveResource {
            }
            part def ReadWriteProcessPlan :> PLANT::Resource::ControlActuator::Actuator {
                port inTask : CONTEXT::inDELSTask[0..*];
                ref canExecute :>> canExecute;
                port outTask : CONTEXT::outDELSTask[0..*];
                action readProcessPlan { in inTask; out outTask; in nextProcess; in processPlan; }
                action updateProcessPlan { in inTask; out outTask; in processPlan; }
            }
            part def Scheduler :> PLANT::Resource::ControlActuator::Queue, PLANT::Resource::ControlActuator::ResourceAcquirer {
                part queue : PLANT::Resource::ControlActuator::Queue[0..*];
                part resourceAcquirer : PLANT::Resource::ControlActuator::ResourceAcquirer[0..*];
                action executeSchedule;
            }
        }
        package OZONEResourceDef {
            part def DiscreteStateResource :> PLANT::Resource::Resource {
                state def DiscreteStateResourceModel {
                    state available;
                    state Ready;
                    state Processing;
                    state Executing;
                    state Active;
                    state Idle;
                    state Starved;
                    state Blocked;
                    state Down;
                    state Setup;
                    state unavailable;
                    transition available then unavailable;
                    transition unavailable then available;
                    transition unavailable then Setup;
                    transition Processing then Idle;
                    transition Idle then Processing;
                }
                ref currentService[0];
                attribute currentState[0..*] = "off/unavailable";
                action changeState;
                action queryState;
                action assignTask;
            }
            part def MobileResource :> PLANT::Resource::OZONEResourceDef::DiscreteStateResource {
                attribute CurrentLocation : PLANT::Facility::Location[0];
                action queryState;
                action reposition;
            }
            part def HeterogeneousAggregateResource :> PLANT::Resource::OZONEResourceDef::AggregateResource {
                ref part Property_1 : PLANT::Resource::Resource;
            }
            part def AggregateResource :> PLANT::Resource::Resource {
                ref part resourcePool : PLANT::Resource::Resource[0..*];
            }
            part def AtomicResource :> PLANT::Resource::Resource {
                ref part resourcePool : PLANT::Resource::Resource[0..1];
                part memberResource :>> memberResource : PLANT::Resource::Resource[0..1];
            }
            part def BatchCapacityResource :> PLANT::Resource::OZONEResourceDef::AtomicResource {
            }
            part def HomogenousAggregateResource :> PLANT::Resource::OZONEResourceDef::AggregateResource {
            }
            part def PerishableResource :> PLANT::Resource::OZONEResourceDef::ConsumableResource {
                attribute perishableLifetime;
            }
            part def CapacitatedResource :> PLANT::Resource::Resource {
                attribute capacityMeasure[0..*];
                attribute currentCapacity[0..*];
                action increaseCapacity;
                action decreaseCapacity;
                action allocateCapacity;
                action deallocateCapacity;
            }
            part def ConsumableResource :> PLANT::Resource::OZONEResourceDef::CapacitatedResource {
                action deallocateCapacity;
            }
            part def UnitCapacityResource :> PLANT::Resource::OZONEResourceDef::AtomicResource {
            }
            part def StationaryResource :> PLANT::Resource::OZONEResourceDef::DiscreteStateResource {
                attribute CurrentLocation : PLANT::Facility::Location[0];
            }
            part def ReusableResource :> PLANT::Resource::OZONEResourceDef::CapacitatedResource {
            }
            part def SimpleCapacityPool :> PLANT::Resource::OZONEResourceDef::HomogenousAggregateResource {
                ref part resourcePool :>> resourcePool : PLANT::Resource::OZONEResourceDef::UnitCapacityResource[0..*];
            }
            part def StructuredCapacityPool :> PLANT::Resource::OZONEResourceDef::HomogenousAggregateResource {
                ref part aggregateResourcePool :>> resourcePool : PLANT::Resource::OZONEResourceDef::AggregateResource[0..*];
                ref part batchResourcePool :>> resourcePool : PLANT::Resource::OZONEResourceDef::BatchCapacityResource[0..*];
            }
        }
        package Subsystems {
            doc /* Subsystems, especially those that are DELS, are resources to the parent DELS. Therefore the subsystem decomposition should live in the Resource package. */
        }
        part def ActiveResource :> PLANT::Resource::Resource {
            ref part resource : PLANT::Resource::ActiveResource[0..*];
            ref part resource_2 : PLANT::Resource::ActiveResource[0..*];
            ref relationshipBetween[0..*];
            ref canExecute[0..*];
            out item produces : PLANT::Product::Product[0..*];
            out item outputResources : PLANT::Resource::PassiveResource[0..*];
            in item inputResources : PLANT::Resource::PassiveResource[0..*];
            attribute controller;
            attribute capacityRegion : ScalarValues::Integer[0..*];
            part memberActiveResource : PLANT::Resource::ActiveResource[0..*];
            ref part sourceResource : PLANT::Resource::ActiveResource[0..*];
            ref part targetResource : PLANT::Resource::ActiveResource[0..*];
        }
        part def PassiveResource :> PLANT::Resource::Resource {
        }
    }
    package Process {
        enum def DependencyType { 'SS (Start to Start)'; 'SF (Start to Finish)'; 'FS (Finish to Start)'; 'FF (Finish to Finish)'; }
        package ISA95ProcessDef {
            action def ManualProcess;
            action def AutomatedProcess;
            action def SemiAutomatedProcess;
            action def NonMaterialProcess;
        }
        package Control {
            action def ChangeState { in targetResource : PLANT::Resource::Resource; in newState; out overheadTask : CONTEXT::Task; }
            action def Control;
            action def Admit { in incomingTasks : CONTEXT::Task; out availableTasks : CONTEXT::Task; in admissionDecision : ScalarValues::Boolean; out rejectedTasks : CONTEXT::Task; }
            action def Route { in inTask : CONTEXT::Task; in assignedResource : PLANT::Resource::Resource; out outTask : CONTEXT::Task; in updatedProcessPlan; }
            action def Sequence { in availableTasks : CONTEXT::Task; in index : ScalarValues::Integer; out orderedTasks : CONTEXT::Task; }
            action def ResourceAcquire { in targetTask : CONTEXT::Task; in resourceAssignment : PLANT::Resource::Resource; in availableResources : PLANT::Resource::Resource; out acquiredResources : PLANT::Resource::Resource; }
            action def UpdateProcessPlan { in inTask : CONTEXT::Task; out outTask : CONTEXT::Task; in processPlan; }
            package Implementations {
                action def RouteToResource { in inTask : CONTEXT::Task; in assignedResource : PLANT::Resource::Resource; out outTask : CONTEXT::Task; in updatedProcessPlan; }
                action def RouteToTask;
                action def MoveTaskToResource { in input; out output : CONTEXT::Task; }
                action def SeizeResourceForTask;
                action def RequestResourceForTask;
                action def AcceptJobIntoWorkCell { in incomingTask : CONTEXT::Task; out availableTasks : CONTEXT::Task; in admissionDecision : ScalarValues::Boolean; out rejectedTasks : CONTEXT::Task; }
            }
            action def ExecuteSchedule { in resourceAssignment : PLANT::Resource::Resource; in availableResources : PLANT::Resource::Resource; out acquiredResources : PLANT::Resource::Resource; in availableTasks : CONTEXT::Task; in index : ScalarValues::Integer; out orderedTasks : CONTEXT::Task; }
        }
        action def Process;
        action def Make;
        action def Control_2;
        action def Move { inout targetItem; in destination; in origin; }
        action def Store;
        action def MeasureTest;
        action def Load;
        action def Unload;
        action def Get { out output : CONTEXT::Task; }
        action def Put;
    }
    package Product {
        part def Product :> PLANT::Resource::ISA95ResourceDef::Material {
            ref part billOfMaterial : PLANT::Resource::ISA95ResourceDef::Material[0..*];
            ref part components : PLANT::Product::Product[0..*];
            ref part authorizedBy : CONTEXT::Task[0..*];
            ref part requiredInputResources : PLANT::Resource::Resource[0..*];
            ref createdBy[0..*];
        }
        part def AssembledProduct :> PLANT::Product::Product {
        }
        part def AggregatedProduct :> PLANT::Product::Product {
        }
        part def HomogeneousAggregatedProduct :> PLANT::Product::AggregatedProduct {
        }
        part def HeterogeneousAggregatedProduct :> PLANT::Product::AggregatedProduct {
        }
    }
    package Facility {
        part def Facility {
            ref part containedResources : PLANT::Resource::Resource[0..*];
            attribute isPhysical : ScalarValues::Boolean = true;
            ref part hasActualLayout : PLANT::Facility::Layout::Layout[0];
            attribute location : PLANT::Facility::Location[0];
        }
        package Layout {
            package Geometry {
                attribute def '3Dgeometry' {
                    attribute referenceFrame : PLANT::Facility::Layout::Geometry::ReferenceFrame::'3DreferenceFrame';
                    attribute boundary : PLANT::Facility::Layout::Geometry::Boundary::'3Dboundary';
                }
                package ReferenceFrame {
                    attribute def '2DRefFrameNesting' {
                        attribute whichRefFrame : PLANT::Facility::Layout::Geometry::ReferenceFrame::'2DreferenceFrame';
                        attribute offset : PLANT::Facility::Layout::Geometry::VectorOfReals;
                        attribute orientation : PLANT::Facility::Layout::Geometry::SquareMatrixOfReals;
                    }
                    attribute def '3DreferenceFrame' {
                        attribute parentRefFrame : PLANT::Facility::Layout::Geometry::ReferenceFrame::'3DRefFrameNesting'[0];
                        attribute baseCase : ScalarValues::Boolean[0];
                    }
                    attribute def '2DreferenceFrame' {
                        attribute parentRefFrame : PLANT::Facility::Layout::Geometry::ReferenceFrame::'2DRefFrameNesting'[0];
                        attribute baseCase : ScalarValues::Boolean[0];
                    }
                    attribute def '3DRefFrameNesting' {
                        attribute whichRefFrame : PLANT::Facility::Layout::Geometry::ReferenceFrame::'3DreferenceFrame';
                        attribute offset : PLANT::Facility::Layout::Geometry::VectorOfReals;
                        attribute orientation : PLANT::Facility::Layout::Geometry::SquareMatrixOfReals;
                    }
                }
                attribute def '2Dgeometry' {
                    attribute referenceFrame : PLANT::Facility::Layout::Geometry::ReferenceFrame::'2DreferenceFrame';
                    attribute boundary : PLANT::Facility::Layout::Geometry::Boundary::'2Dboundary';
                }
                package Boundary {
                    package BoundaryByShapes {
                        attribute def Circle {
                            attribute radius;
                        }
                        attribute def Sphere {
                            attribute radius;
                        }
                        attribute def Rectangle {
                            attribute length;
                            attribute width;
                        }
                        enum def '2Dshape' {  }
                        enum def '3Dshape' {  }
                    }
                    attribute def '3Dboundary' {
                        attribute shape : PLANT::Facility::Layout::Geometry::Boundary::BoundaryByShapes::'3Dshape'[0];
                        attribute setOfPoints : PLANT::Facility::Layout::Geometry::Boundary::BoundaryByPoints::'3DBoundaryPoints'[0];
                    }
                    package BoundaryByPoints {
                        enum def InterpolationMethod { linear; }
                        attribute def '2DBoundaryPoints' {
                            attribute points : PLANT::Facility::Layout::Geometry::VectorOfReals[3..*];
                            attribute interpolation : PLANT::Facility::Layout::Geometry::Boundary::BoundaryByPoints::InterpolationMethod;
                        }
                        attribute def '3DBoundaryPoints' {
                            attribute points : PLANT::Facility::Layout::Geometry::VectorOfReals[4..*];
                            attribute interpolation : PLANT::Facility::Layout::Geometry::Boundary::BoundaryByPoints::InterpolationMethod;
                        }
                    }
                    attribute def '2Dboundary' {
                        attribute shape : PLANT::Facility::Layout::Geometry::Boundary::BoundaryByShapes::'2Dshape'[0];
                        attribute setOfPoints : PLANT::Facility::Layout::Geometry::Boundary::BoundaryByPoints::'2DBoundaryPoints'[0];
                    }
                }
                attribute def SquareMatrixOfReals {
                    attribute nDims;
                    attribute elements : ScalarValues::Real;
                    attribute elementOrdering : PLANT::Facility::Layout::Geometry::'2DmatrixElementOrdering';
                }
                attribute def VectorOfReals {
                    attribute nDims;
                    attribute elements : ScalarValues::Real;
                }
                enum def '2DmatrixElementOrdering' { 'row-major'; 'column-major'; }
            }
            part def Placement {
                doc /* This is the semantic for an actual allocation of space in a LAYOUT. Specifically, it is an offset and orientation of a LAYOUT OBJECT's reference frame within a LAYOUT SPACE's reference frame. */
                constraint OffsetDimension_imported {
                    doc /* self.offset.nDims == Layout.dimensions */
                }
                constraint OrientationDimension_imported {
                    doc /* self.orientation.nDims == Layout.dimensions */
                }
                ref part object : PLANT::Facility::Layout::'Layout Object';
                ref part space : PLANT::Facility::Layout::'Physical Space';
                attribute offset : PLANT::Facility::Layout::Geometry::VectorOfReals;
                attribute orientation : PLANT::Facility::Layout::Geometry::SquareMatrixOfReals;
                ref part parentLayout : PLANT::Facility::Layout::Layout;
            }
            part def 'Process-Oriented Layout' :> PLANT::Facility::Layout::Layout {
            }
            part def Layout {
                doc /* A LAYOUT requires two ingredients: Space, and objects requesting space allocation. An example may be 5000 square feet within a facility, and various machines needing arrangement. Given these ingredients, a layout is a collection of placements - a reference frame attached to each layout object is offset and oriented within a reference frame attached to the space. A boundary decision was to focus exclusively on manufacturing, so we care about movement of physical goods throughout a manufacturing process, hence the semantic LAYOUT FOR MOVEMENT AND ACCESS. */
                ref part layoutForSpace : PLANT::Facility::Layout::'Physical Space';
                ref part actualLayoutOfSpace : PLANT::Facility::Facility;
                attribute dimensions : ScalarValues::Integer = 2;
                ref part placements : PLANT::Facility::Layout::Placement[0..*];
            }
            part def 'Product-Oriented Layout' :> PLANT::Facility::Layout::Layout {
            }
            part def 'Layout Object' {
                doc /* In the context of a Layout for Movement and Access, LAYOUT OBJECT is an abstract superclass for its 'forMovement' and 'withAccess' subclasses. It is one of two layout ingredients - these are objects requesting space allocation. Any Layout Object has a GEOMETRY, which comes with a reference frame, needed for the placement. */
                attribute '2Dgeometry' : PLANT::Facility::Layout::Geometry::'2Dgeometry'[0];
                attribute '3Dgeometry' : PLANT::Facility::Layout::Geometry::'3Dgeometry'[0];
            }
            part def 'Layout Object With Access' :> PLANT::Facility::Layout::'Layout Object' {
                doc /* A Layout Object With Access may be a department or a workstation ... any object which has input/output of material moving from/to other such objects. The interface between a Layout Object For Movement (e.g. aisle) and a Layout Object With Access (e.g. department) is modeled by an INTERFACE POINT. */
                part accessAt : PLANT::Facility::Layout::'Interface Point'[0..*];
            }
            part def 'Layout Object For Movement' :> PLANT::Facility::Layout::'Layout Object' {
                doc /* A Layout Object For Movement may be an aisle, conveyor, overhead crane path ... any object enabling material movement among Layout Objects With Access. The interface between a Layout Object For Movement (e.g. aisle) and a Layout Object With Access (e.g. department) is modeled by an INTERFACE POINT. */
                ref part incidentTo : PLANT::Facility::Layout::'Interface Point'[0..*];
            }
            part def 'Interface Point' {
                doc /* An Interface Point is a simplification of the notion of "access" to a single point. It is a composite part of a Layout Object With Access, and its location is defined in that object's reference frame. An Interface Point is the interface between 'withAccess' and 'forMovement' Layout Objects, and any Layout Object For Movement should reference all incident Interface Points. */
                constraint PointsDimension {
                    doc /* self.point.nDims == LayoutForMovementAndAccess.dimensionality */
                }
                ref part Property_2 : PLANT::Facility::Layout::'Layout Object With Access';
                ref part Property_3 : PLANT::Facility::Layout::'Layout Object For Movement';
                ref part Property_4 : PLANT::Facility::Layout::LayoutSemanticsToAbstractANetwork::'Rectangular Path Segment';
                attribute point : PLANT::Facility::Layout::Geometry::VectorOfReals;
            }
            package LayoutSemanticsToAbstractANetwork {
                doc /* Suppose an analysis is searching for geometric overlap of aisles, and when overlap is found partitioning an Aisle into AisleSegments and AisleIntersections. There may be multiple overlaps, so they will likely be iterated through one-by-one. However, this creates the possibility of an Aisle and an AisleSegment overlapping. => For implementation purposes, do I need a superclass for both Aisle and AisleSegment? */
                part def 'Endpoint Node' {
                    constraint Constraint_1 {
                        doc /* self.point.nDims == StaticLayout.dimensionality */
                    }
                    attribute point : PLANT::Facility::Layout::Geometry::VectorOfReals;
                    ref part endpointOfSegment : PLANT::Facility::Layout::LayoutSemanticsToAbstractANetwork::'Rectangular Path Segment';
                    ref part L_Intersection : PLANT::Facility::Layout::LayoutSemanticsToAbstractANetwork::PathIntersection::'Lshaped Intersection'[0];
                    ref part T_intersection : PLANT::Facility::Layout::LayoutSemanticsToAbstractANetwork::PathIntersection::'Tshaped Intersection'[0];
                    ref part '+_intersection' : PLANT::Facility::Layout::LayoutSemanticsToAbstractANetwork::PathIntersection::'+shaped Intersection'[0];
                }
                part def 'Rectangular Path Segment' {
                    constraint Constraint_1 {
                        doc /* self.width == RectangularAisle.width */
                    }
                    constraint Constraint_2 {
                        doc /* size(set(self.internalNode)) == size(set(self.incidentTo)) */
                    }
                    part internalNode : PLANT::Facility::Layout::LayoutSemanticsToAbstractANetwork::'Internal Node'[0..*];
                    ref part owningPath : PLANT::Facility::Layout::LayoutSemanticsToAbstractANetwork::'Rectangular Path';
                    ref part endpoint : PLANT::Facility::Layout::LayoutSemanticsToAbstractANetwork::'Endpoint Node'[2];
                    ref part incidentTo : PLANT::Facility::Layout::'Interface Point'[0..*];
                    attribute width;
                }
                part def 'Internal Node' {
                    constraint Constraint_1 {
                        doc /* self.point.nDims == StaticLayout.dimensionality */
                    }
                    ref part Property_2 : PLANT::Facility::Layout::LayoutSemanticsToAbstractANetwork::'Rectangular Path Segment';
                    attribute point : PLANT::Facility::Layout::Geometry::VectorOfReals;
                }
                package PathIntersection {
                    comment about PLANT::Facility::Layout::LayoutSemanticsToAbstractANetwork::PathIntersection::'Two Rectangular Path Intersection' /* A Rectangular Path Intersection is referenced by [2..*] Rectangular Path. For the subclass TwoRectangularPathIntersection, that multiplicity can be narrowed to exactly 2. How to override multiplicities on inherited reference attributes in MD 17.0? */
                    part def 'Lshaped Intersection' :> PLANT::Facility::Layout::LayoutSemanticsToAbstractANetwork::PathIntersection::'Two Rectangular Path Intersection' {
                        ref part endpoint : PLANT::Facility::Layout::LayoutSemanticsToAbstractANetwork::'Endpoint Node'[2];
                    }
                    part def 'Two Rectangular Path Intersection' :> PLANT::Facility::Layout::LayoutSemanticsToAbstractANetwork::PathIntersection::'Rectangular Path Intersection' {
                    }
                    part def 'Tshaped Intersection' :> PLANT::Facility::Layout::LayoutSemanticsToAbstractANetwork::PathIntersection::'Two Rectangular Path Intersection' {
                        ref part endpoint : PLANT::Facility::Layout::LayoutSemanticsToAbstractANetwork::'Endpoint Node'[3];
                    }
                    part def 'Rectangular Path Intersection' {
                        ref part intersectingObject : PLANT::Facility::Layout::LayoutSemanticsToAbstractANetwork::'Rectangular Path'[2..*];
                    }
                    part def '+shaped Intersection' :> PLANT::Facility::Layout::LayoutSemanticsToAbstractANetwork::PathIntersection::'Two Rectangular Path Intersection' {
                        ref part endpoint : PLANT::Facility::Layout::LayoutSemanticsToAbstractANetwork::'Endpoint Node'[4];
                    }
                }
                part def 'Rectangular Path' :> PLANT::Facility::Layout::'Layout Object For Movement' {
                    attribute length;
                    attribute width;
                    part ownedSegment : PLANT::Facility::Layout::LayoutSemanticsToAbstractANetwork::'Rectangular Path Segment'[0..*];
                    ref part sharedSegment : PLANT::Facility::Layout::LayoutSemanticsToAbstractANetwork::PathIntersection::'Rectangular Path Intersection'[0..*];
                }
            }
            part def 'Physical Space' {
                attribute geometry : PLANT::Facility::Layout::Geometry::'2Dgeometry';
                ref part hasLayout : PLANT::Facility::Layout::Layout[0];
                ref part parentFacility : PLANT::Facility::Facility[0];
            }
        }
        attribute def Location {
            attribute Longitude : ScalarValues::Real;
            attribute Latitude : ScalarValues::Real;
            attribute Country_Code : ScalarValues::String;
        }
    }
}
package CONTROL {
    private import 'DELS Profile'::*;
    private import RequirementDerivation::*;
    package DecisionSupport {
        package Admission {
            part def Propose {
                action def Propose_PriceLeadTime { out LeadTime; in Price; }
                part def proposeLeadTime {
                    action admission { in incomingTask; in price; out leadTime; }
                }
                part def proposePrice {
                    action admission { in incomingTask; out price; in leadTime; }
                }
                action admission { in incomingTask; inout price; inout leadTime; }
            }
            part def simpleCapacity {
                state def SimpleCapacity {
                    state AdmitTask;
                    state RejectTask;
                }
                action def SimpleCapacity_2 { in incomingTask : CONTEXT::Task; out admissionResult : ScalarValues::Boolean; }
                attribute threshold : ScalarValues::Integer;
                action admission { in incomingTask; }
            }
            part def capacitatedPriority {
                state def capacitatedPriority {
                    state AdmitTask;
                    state RejectTask;
                }
                action def capacitatedPriority_2 { in incomingTask : CONTEXT::Task; out admissionResult : ScalarValues::Boolean; }
                attribute capacityThreshold : ScalarValues::Integer;
                attribute priorityThreshold : ScalarValues::Integer;
                action admission { in incomingTask; }
            }
            port def Admission;
        }
        package Sequencing {
            part def FIFO {
                action def sequencing { out sequenceIndex : ScalarValues::Integer; in taskList : CONTEXT::Task; }
                attribute sortKey = "task.ageInQueue";
                action sequencing_2 { out sequenceIndex; in taskSet; }
            }
            part def prioritySequencing {
            }
            port def Sequencing;
        }
        package Assignment {
            part def FirstAvailable {
            }
            part def utilizationBalancing {
            }
            port def ResourceAssignment;
        }
        package Scheduling {
            part def OptimalScheduling {
            }
            part def ClarkWright_VRP {
            }
            part def CLK_ITP {
            }
            port def Scheduling;
        }
        package DynamicProcessPlanning {
            private import CONTEXT::*;
            private import PLANT::Process::*;
            port def DynamicProcessPlanning;
        }
        package ChangeState {
            part def InventoryReordering {
                attribute inventoryPolicy[0..*];
                action changeState { in resource; out newState; out overheadTask; }
            }
            part def MachineSetup {
                attribute productionPolicy[0..*];
                attribute maintenancePolicy[0..*];
                action changeState { in resource; out newState; out overheadTask; }
            }
            port def ChangeState;
        }
        package Routing {
            port def Routing;
        }
        port def DecisionSupportStrategy;
    }
    part def OperationalController {
        part monitor : CONTROL::Monitoring[0..*];
        part decisionSupport : CONTROL::DecisionSupport_2;
        port messageInterface;
        connect monitor to decisionSupport;
        connect messageInterface to monitor;
    }
    part def Monitoring {
    }
    part def Optimization {
    }
    part def DecisionSupport_2 {
        ref admissionInterface[0..*];
        ref assignmentInterface[0..*];
        ref sequencingInterface[0..*];
        ref processPlanningInterface[0..*];
        ref changeStateInterface[0..*];
        ref routingInterface[0..*];
        ref schedulingInterface[0..*];
        action contextInterface;
    }
}
package CONTEXT {
    private import 'DELS Profile'::*;
    private import RequirementDerivation::*;
    part def Task {
        ref part targetProduct : PLANT::Product::Product[0];
        ref authorizesExecuting;
        part subTask : CONTEXT::Task[0..*];
        attribute measure : ScalarValues::Real[0..*];
        ref part currentDELS : 'DELS Root'::DELS;
    }
    port def inDELSResource {
        in item inResource : PLANT::Resource::Resource[0..*];
        ref action receiveResource;
    }
    port def inDELSTask {
        in item inTask : CONTEXT::Task[0..*];
        ref action receiveTask;
    }
    port def outDELSResource {
        out item outResource : PLANT::Resource::Resource[0..*];
        ref action outputResource;
    }
    port def outDELSTask {
        out item outTask : CONTEXT::Task[0..*];
        ref action outputTask { out outTask; }
    }
    part def MaterialHandlingChannel {
    }
}
package 'DELS Root' {
    private import 'DELS Profile'::*;
    part def DELS :> PLANT::Resource::ActiveResource {
        part Property_1 : PLANT::Resource::ControlActuator::AdmissionGate;
        part availableTaskStore : PLANT::Resource::ControlActuator::Queue[0..*];
        part acquireResources : PLANT::Resource::ControlActuator::ResourceAcquirer;
        ref functionalCapability[0..*];
        part completedTaskStore : PLANT::Resource::ControlActuator::Queue[0..*];
        part releaseResources : PLANT::Resource::ControlActuator::Release;
        part routing : PLANT::Resource::ControlActuator::Router;
        part controller : CONTROL::OperationalController;
        port inResource : CONTEXT::inDELSResource[0..*];
        part setUp : PLANT::Resource::ControlActuator::ChangeState;
        port incomingTasks : CONTEXT::inDELSTask[0..*];
        ref part completedTasks : CONTEXT::Task[0..*];
        port outgoingTasks : CONTEXT::outDELSTask[0..*];
        ref part availableTasks : CONTEXT::Task[0..*];
        port outResource : CONTEXT::outDELSResource[0..*];
        attribute location : PLANT::Facility::Location;
        ref part serviceProvider :>> resource : 'DELS Root'::DELS[0..*];
        ref part serviceRequestor :>> resource_2 : 'DELS Root'::DELS[0..*];
        part childDELS : 'DELS Root'::DELS[0..*];
        attribute totalOperatingCost : ScalarValues::Real[0];
        attribute fixedOperatingCost : ScalarValues::Real[0];
        attribute variableOperatingCost : ScalarValues::Real[0];
        ref relationshipBetween[0..*];
        ref part inprocessTasks : CONTEXT::Task[0..*];
        attribute taskFulfillmentCycleTime : ScalarValues::Real[0];
        attribute perfectTaskFulfillment : ScalarValues::Real[0];
        ref part parentDELS : 'DELS Root'::DELS[0..*];
        ref mhc[0..*];
        attribute maker[0..*];
        attribute mover[0..*];
        attribute storer[0..*];
        ref Property_32;
        part Property_33 : PLANT::Resource::ControlActuator::Scheduler;
        connect Property_1.availableTask to availableTaskStore.inTask;
        connect availableTaskStore.outTask to acquireResources.inTask;
        connect acquireResources.acquiredResource to functionalCapability;
        connect releaseResources.resource to functionalCapability;
        connect completedTaskStore.inTask to releaseResources.completedTask;
        connect routing to completedTaskStore;
        connect setUp to acquireResources;
        connect inResource to acquireResources.availableResource;
        connect outResource to releaseResources.releasedResource;
        connect incomingTasks to Property_1.incomingTask;
        connect routing.outTask to outgoingTasks;
        connect Property_1.rejectedTask to routing.inTask;
        connect memberActiveResource to memberActiveResource;
        connect completedTaskStore.outTask to routing.inTask;
    }
}

package 'DELS Relationships' {
    private import 'DELS Profile'::*;
    private import RequirementDerivation::*;
    #ItemFlow dependency 'flow for Task' from PLANT::Resource::ControlActuator::ResourceAcquirer::acquiredResource to 'DELS Root'::DELS::functionalCapability; /* conveys PLANT::Resource::Resource */
    #ItemFlow dependency 'flow for Resource' from PLANT::Resource::ControlActuator::Release::releasedResource to 'DELS Root'::DELS::outResource; /* conveys PLANT::Resource::Resource */
    #ItemFlow dependency completedTasks from PLANT::Resource::ControlActuator::Release::completedTask to PLANT::Resource::ControlActuator::Queue::inTask; /* conveys CONTEXT::Task */
    #ItemFlow dependency 'flow for Task' from 'DELS Root'::DELS::releaseResources to 'DELS Root'::DELS::functionalCapability;
    #ItemFlow dependency 'flow for Task_2' from 'DELS Root'::DELS::functionalCapability to PLANT::Resource::ControlActuator::Release::resource; /* conveys CONTEXT::Task */
    #ItemFlow dependency 'flow for Task_3' from 'DELS Root'::DELS::releaseResources to 'DELS Root'::DELS::completedTaskStore;
    #ItemFlow dependency 'flow for Resource' from 'DELS Root'::DELS::setUp to 'DELS Root'::DELS::acquireResources; /* conveys PLANT::Resource::Resource */
    #ItemFlow dependency 'flow for Task_4' from PLANT::Resource::ControlActuator::ResourceAcquirer::acquiredResource to 'DELS Root'::DELS::functionalCapability; /* conveys CONTEXT::Task */
    #ItemFlow dependency 'flow for Task_5' from PLANT::Resource::ControlActuator::Queue::outTask to PLANT::Resource::ControlActuator::ResourceAcquirer::inTask; /* conveys CONTEXT::Task */
    #ItemFlow dependency completedTasks from 'DELS Root'::DELS::completedTaskStore to 'DELS Root'::DELS::releaseResources;
    #ItemFlow dependency 'flow for Task_6' from 'DELS Root'::DELS::releaseResources to 'DELS Root'::DELS::completedTaskStore;
    #ItemFlow dependency availableTasks from PLANT::Resource::ControlActuator::AdmissionGate::availableTask to PLANT::Resource::ControlActuator::Queue::inTask; /* conveys CONTEXT::Task */
    #ItemFlow dependency 'flow for Task_7' from 'DELS Root'::DELS::completedTaskStore to 'DELS Root'::DELS::routing; /* conveys CONTEXT::Task */
    #ItemFlow dependency 'flow for Task_8' from 'DELS Root'::DELS::Property_1 to 'DELS Root'::DELS::availableTaskStore;
    #ItemFlow dependency 'flow for Task_9' from 'DELS Root'::DELS::availableTaskStore to 'DELS Root'::DELS::acquireResources;
    #ItemFlow dependency 'flow for Task_10' from PLANT::Resource::ControlActuator::Queue::outTask to PLANT::Resource::ControlActuator::Router::inTask; /* conveys CONTEXT::Task */
}