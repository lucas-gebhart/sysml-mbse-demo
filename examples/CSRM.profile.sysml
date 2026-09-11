package 'CSRM Profile' {
    doc /* Custom stereotypes from the v1 profile, carried over as SysML v2 metadata definitions.
           Tag definitions become attributes; the tool-side behaviour (icons, validation rules,
           derived properties, table customisations) is NOT carried and must be re-created. */
    metadata def Component;
    metadata def ComponentRequirement :> ExtRequirement;
    metadata def CubeSat :> Satellite;
    metadata def CubeSatRequirement :> SatelliteRequirement;
    metadata def DeployerRequirement :> ExtRequirement;
    metadata def Equipment;
    metadata def Explanation;
    metadata def ExtRequirement { attribute Id : ScalarValues::String; attribute Text : ScalarValues::String; attribute risk : ScalarValues::String; attribute source : ScalarValues::String; attribute validatedBy : ScalarValues::String; }
    metadata def Facility;
    metadata def GroundSegmentRequirement :> SegmentRequirement;
    metadata def Group :> ExtRequirement;
    metadata def MeasurementSpecification { attribute Id : ScalarValues::String; attribute summary : ScalarValues::String; }
    metadata def MissionConstraint :> ExtRequirement;
    metadata def MissionNeed :> ExtRequirement;
    metadata def MissionObjective :> ExtRequirement;
    metadata def MissionRequirement :> ExtRequirement;
    metadata def Refine;
    metadata def Satellite :> Spacecraft;
    metadata def SatelliteRequirement :> SpacecraftRequirement;
    metadata def Segment :> SystemContext;
    metadata def SegmentRequirement :> ExtRequirement;
    metadata def Spacecraft :> System;
    metadata def SpacecraftRequirement :> ExtRequirement;
    metadata def Stakeholder;
    metadata def StakeholderConcern :> ExtRequirement;
    metadata def Subsystem;
    metadata def SubsystemRequirement :> ExtRequirement;
    metadata def System;
    metadata def SystemContext;
    metadata def Trace;
    metadata def ValidationActivity { attribute A_Plan : ScalarValues::String; attribute B_Procedure : ScalarValues::String; attribute C_Conduct : ScalarValues::String; attribute D_Result : ScalarValues::String; attribute E_Status : ScalarValues::String; }
    metadata def VerificationActivity { attribute verificationMethod : ScalarValues::String; attribute verifies : ScalarValues::String; }
    metadata def kppRequirement :> performanceRequirement;
    metadata def kppSpecification :> MeasurementSpecification;
    metadata def moeRequirement :> performanceRequirement;
    metadata def moeSpecification :> MeasurementSpecification;
    metadata def mopRequirement :> performanceRequirement;
    metadata def mopSpecification :> MeasurementSpecification;
    metadata def performanceRequirement :> ExtRequirement;
    metadata def tpmRequirement :> performanceRequirement;
    metadata def tpmSpecification :> MeasurementSpecification;
}