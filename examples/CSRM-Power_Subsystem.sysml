package '01 - CubeSat System Reference Model' {
    private import 'CSRM Profile'::*;
    private import RequirementDerivation::*;
    package '5 - Architecture' {
        package L3_Subsystems {
            package 'L3.1_CubeSat Subsystems' {
                package 'L3.1.2_Structures' {
                    #Subsystem part def 'Power Subsystem' {
                        part batteries : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.1_CubeSat Subsystems Components'::'L4.1.7_Power Components'::'L4.1.7.2_Structures'::Batteries;
                        part 'regulators and Converters' : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.1_CubeSat Subsystems Components'::'L4.1.7_Power Components'::'L4.1.7.2_Structures'::'Regulators and Converters';
                        part 'solar Arrays' : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.1_CubeSat Subsystems Components'::'L4.1.7_Power Components'::'L4.1.7.2_Structures'::'Solar Arrays';
                        part 'power Circuits and Switches' : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.1_CubeSat Subsystems Components'::'L4.1.7_Power Components'::'L4.1.7.2_Structures'::'Power Circuits and Switches';
                        part 'processor and Memory' : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.1_CubeSat Subsystems Components'::'L4.1.7_Power Components'::'L4.1.7.2_Structures'::'Processor and Memory';
                        part software : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.1_CubeSat Subsystems Components'::'L4.1.7_Power Components'::'L4.1.7.2_Structures'::Software;
                    }
                }
            }
        }
        package L4_Components {
            package 'L4.1_CubeSat Subsystems Components' {
                package 'L4.1.7_Power Components' {
                    package 'L4.1.7.2_Structures' {
                        part def Batteries;
                        part def Software;
                        part def 'Processor and Memory';
                        part def 'Regulators and Converters';
                        part def 'Solar Arrays';
                        part def 'Power Circuits and Switches';
                    }
                }
            }
        }
    }
}