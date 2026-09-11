package '01 - CubeSat System Reference Model' {
    private import 'CSRM Profile'::*;
    private import RequirementDerivation::*;
    package '1 - Stakeholders' {
        doc /* p {padding:0px; margin:0px;} Stakeholders are any entities that have an interest or role in the system such as regulatory agencies, the deployer system, and mission system development and operations personnel. &#160;Representative stakeholders are included in the model and can be extended as appropriate. &#160; There can be a number of stakeholders with varying interests. &#160;Mission needs, objectives, constraints, and Rqts result from review, assessment, and integration of the varied interests. Double-click on on the individual Regulatory Agency Stakeholders to navigate to the stakeholder web sites Double-click on the stakeholder packages to navigate to the individual stakeholders. p {padding:0px; margin:0px;} A stakeholder is any entity that has an interest in the system. Some are interested in the models themselves and others are interested in the missions that can be realized from the mission-specific instantiations of the model, and some have interests in both. There are two modeling efforts. One is the SSWG developing a CubeSat Reference Model with its logical architecture. The other is a team eventually taking the CubeSat Reference Model as a basis for its mission-specific logical and physical architectures. Stakeholders */
        package '1.1 Regulatory Agency Stakeholders' {
            doc /* p {padding:0px; margin:0px;} CubeSat projects are pursued internationally, but the licenses and regulations that cover their activities are administered at the national level. The timelines and procedures for requesting and receiving approval must be well understood and part of the model. CubeSat projects are pursued internationally, but the licenses and regulations that cover their activities are administered at the national level. The timelines and procedures for requesting and receiving approval must be well understood and part of the model. A double click on these elements links to the web sites A mission specific team will add Regulatory Agencies as applicable Double-click on a table and add and delete elements as needed. Click on Add New to add a new element to the containment tree and to the table. Right click the new element in the table then left click Select in Containment Tree to navigate to the new element. Select an element and click on Delete to delete from the element table and the Containment Tree. Regulatory Agency Stakeholders and Concerns - Population */
            package '1.1.2 - Regulatory Agency Stakeholders Concerns' {
                doc /* p {padding:0px; margin:0px;} A mission specific team will add Regulatory Agencies stakeholder concerns as applicable */
                #Group requirement <RegAgcyCons_1> 'Regulatory Agency Stakeholder Concerns' {
                    doc /* This Group provides the prefix and numbering scheme. */
                    #StakeholderConcern requirement <'RegAgcyCons_1.1'> 'Regulatory Agency Stakeholder Concern Name' {
                    }
                }
            }
            package '1.1.1 - Regulatory Agency Stakeholders' {
                doc /* p {padding:0px; margin:0px;} A mission specific team will add Regulatory Agencies stakeholders as applicable. */
                #Stakeholder part def 'Regulatory Agency Name' {
                }
            }
        }
        package '1.3 CubeSat Deployer Systems' {
            doc /* p {padding:0px; margin:0px;} The design and development of the mission specific CubeSat must satisfy the Rqts for interfacing with a CubeSat Deployer. */
        }
        package '1.2 Mission Stakeholders' {
            doc /* Mission Constraint - A limitation placed on cost, schedule, or implementation techniques Mission Need - A concise description of a need or service that the system must provide. Mission Objective - A broad set of goals that must be achieved in order to successfully satisfy the stated mission need, Mission Requirement - Statements of fact and assumptions that define the expectations of the system in terms of mission objectives, environment, constraints, and measures of effectiveness Stakeholder Concern - Interest in a system relevant to one or more of its stakeholders. Mission Stakeholders -Those with an interest in the mission-specific CubeSat space and ground system. Double-click on a table and add and delete elements as needed. Click on Add New to add a new element to the containment tree and to the table. Right click the new element in the table then left click Select in Containment Tree to navigate to the new element. Select an element and click on Delete to delete from the element table and the Containment Tree. Mission Stakeholders and Requirements - Population Mission Stakeholders */
            package '1.2.1 - Mission Stakeholders' {
                #Stakeholder part def 'Mission Stakeholder A' {
                    doc /* Description */
                }
                #Stakeholder part def 'Mission Stakeholder B' {
                    doc /* Description */
                }
            }
            package '1.2.3 - Mission Needs' {
                #Group requirement <MN_1> 'Mission Needs Group' {
                    doc /* The Group provides the prefix and numbering scheme which is easy to change. */
                    #MissionNeed requirement <'MN_1.1'> 'Mission Need Name' {
                        doc /* Statement of need */
                    }
                }
            }
            package '1.2.5 - Mission Constraints' {
                #Group requirement <MC_1> 'Mission Constraints Group' {
                    doc /* The Group provides the prefix and numbering scheme which is easy to change. */
                    #MissionConstraint requirement <'MC_1.1'> 'Mission Constraint Name' {
                        doc /* Statement of constraint */
                    }
                }
            }
            package '1.2.6 - Mission Rqts' {
                #Group requirement <MR_1> 'Mission Rqts Group' {
                    doc /* The Group provides the prefix and numbering scheme which is easy to change. */
                    #MissionRequirement requirement <'MR_1.1'> 'Requirement Name' {
                        doc /* Shall statement */
                    }
                }
            }
            package '1.2.4 - Mission Objectives' {
                #Group requirement <MO_1> 'Mission Objectives Group' {
                    doc /* The Group provides the prefix and numbering scheme which is easy to change. */
                    #MissionObjective requirement <'MO_1.1'> 'Mission Objective Name' {
                        doc /* Statement of Objective */
                    }
                }
            }
            package '1.2.2 - Mission Stakeholder Concerns' {
                #Group requirement <SC_1> 'Mission Stakeholder Concerns' {
                    doc /* The Group provides the prefix and numbering scheme which is easy to change. */
                    #StakeholderConcern requirement <'SC_1.1'> 'Mission Stakeholder A Concern 1' {
                        doc /* Statement of concern */
                    }
                }
            }
        }
    }
    package '5 - Architecture' {
        doc /* p {padding:0px; margin:0px;} The CSRM provides a CubeSat logical architecture. The logical components are abstractions of the physical components that perform the system functionality without imposing implementation constraints. The physical architecture defines physical components of the system including hardware, software, persistent data, and operational procedures. The CSRM logical elements are a starting point for a mission-specific CubeSat logical architecture, followed by the physical architecture and the CubeSat development. &#160; The architecture hierarchy starts at the CubeSat Domain and CubeSat Enterprise which consists of the CubeSat space segment and Ground segment. The CubeSat and Ground subsystems are generically and loosely defined as a starting point for the mission specific CubeSat team. The CubeSat team determines what subsystem capabilities are needed and whether they are provided by software, hardware, persistent data, or operator procedures. The Rqts and logical architecture hierarchies are parallel constructs. The subsystem architectures decompose to component architectures with notional example components. The mission-specific architecture team will replace these notional components with identified logical components which will be eventually be replaced with physical components. The enterprise, segment, and subsystem packages contain packages for behaviors, structures. Behaviors include use case, activity, sequence, and state diagrams. Structures include block definition diagrams and internal block definition diagrams. The CRM provides a CubeSat logical architecture. The logical components are abstractions of the physical components that perform the system functionality without imposing implementation constraints. The physical architecture defines physical components of the system including hardware, software, persistent data, and operational procedures. The CRM logical elements are a starting point for a mission-specific CubeSat logical architecture, followed by the physical architecture and the CubeSat development. The enterprise, segment, and subsystem packages contain packages for behaviors, structures. Behaviors include use case, activity, sequence, and state diagrams. Structures include block definition diagrams and internal block definition diagrams. Double-click on the Domain, Enterprise, Segment, and Subsystem packages to navigate to their structure block definition diagrams. The CubeSat Component package contain representative components. The mission-specific CubeSat team populates the CubeSat and Ground System Component packages with their mission-specific components. The CubeSat and Ground subsystems are broadly defined as a starting point for the mission-specific CubeSat team. The CubeSat team determines what subsystem capabilities are needed and whether they are provided by software, hardware, persistent data, or operator procedures Subsystems can be eliminated if not needed,e.g. Propulsion. Subsystems can be combined, e.g. Attitude Determination and Control subsystem and Guidance, Navigation, and Control. */
        package L0_Domain {
            doc /* p {padding:0px; margin:0px;} Domain represents the scope of the model. &#160;&#160; The CubeSat Domain consists of the CubeSat Enterprise, Stakeholders, External Environment, and External Constraints. &#160; External Environment consists of the Space Environment and Earth Environment. The External Constraints include such things as Licenses and Regulations. */
            part def 'CubeSat Reference Model Stakeholder';
            package 'L0.1_Behaviors' {
            }
            package 'L0.2_Structures' {
                part def 'CubeSat Domain' {
                    part 'external Constraints' : '01 - CubeSat System Reference Model'::'5 - Architecture'::L0_Domain::'L0.2_Structures'::'External Constraints';
                    part 'external Environment' : '01 - CubeSat System Reference Model'::'5 - Architecture'::L0_Domain::'L0.2_Structures'::'External Environment';
                    part 'cubeSat Mission Enterprise' : '01 - CubeSat System Reference Model'::'5 - Architecture'::L1_Enterprise::'L1.2_Structures'::'CubeSat Mission Enterprise';
                }
                part def 'External Constraints' {
                }
                part def 'External Environment' {
                }
            }
        }
        package L4_Components {
            doc /* p {padding:0px; margin:0px;} Package of CubeSat subsystems components and of Ground systems components. &#160; The subsystem architectures decompose to component architectures with notional example components. The mission-specific architecture team will replace these notional components with identified logical components which will be eventually be replaced with physical components. Master - Update Component and Subsystem bdd Select Components Table / Select in Containment Tree to locate Components pkg in the Containment tree Open the Components Table Select Add New to add a new component to the containment tree and to the table Open Components bdd Drag the new components element from the containment tree do to the Components bdd. Open the Subsystem bdd Drag the new component element from the containment tree to the Subsystems bdd – to the Components pkg – to the Structure pkg Right click the Subsystem block, select the directed composition relationship, and drag to the new component element Return to the Component Population pkg. Open the Ground Subsystems Structures Table to see the components associated with the Subsystem */
            package 'L4.1_CubeSat Subsystems Components' {
                doc /* p {padding:0px; margin:0px;} Package for CubeSat subsystems components. &#160;To be populated by a mission specific team. CubeSat Subsystems Components - Population */
                package 'L4.1.1_Mission Payload Components' {
                    doc /* p {padding:0px; margin:0px;} Package for CubeSat Mission Payload components. &#160;To be populated by a mission specific team. */
                    package 'L4.1.1.2_Structures' {
                        #Component part def 'Processor and Memory' {
                        }
                        #Component part def Instrument {
                        }
                    }
                    package 'L4.1.1.1_Behaviors' {
                    }
                }
                package 'L4.1.2_Command and Data Handling Components' {
                    doc /* p {padding:0px; margin:0px;} Package for CubeSat Command and Data Handling components. &#160;To be populated by a mission specific team. */
                    package 'L4.1.2.2_Structures' {
                        #Component part def 'Processor and Memory' {
                        }
                        #Component part def 'Command, Telemetry, and Data Bus' {
                        }
                    }
                    package 'L4.1.2.1_Behaviors' {
                    }
                }
                package 'L4.1.3_Communication Components' {
                    doc /* p {padding:0px; margin:0px;} Package for CubeSat Communication components. &#160;To be populated by a mission specific team. */
                    package 'L4.1.3.2_Structures' {
                        #Component part def 'Processor and Memory' {
                        }
                        #Component part def 'Receive Antenna and Equipment' {
                        }
                        #Component part def 'Transmit Antenna and Equipment' {
                        }
                    }
                    package 'L4.1.3.1_Behaviors' {
                    }
                }
                package 'L4.1.4_Attitude Determination and Control Components' {
                    doc /* p {padding:0px; margin:0px;} Package for CubeSat Attitude Determination and Control components. &#160;To be populated by a mission specific team. */
                    package 'L4.1.4.2_Structures' {
                        #Component part def Software {
                        }
                        #Component part def Actuator {
                        }
                        #Component part def Sensor {
                        }
                    }
                    package 'L4.1.4.1_Behaviors' {
                    }
                }
                package 'L4.1.5_Guidance Navigation and Control Components' {
                    doc /* p {padding:0px; margin:0px;} Package for CubeSat Guidance Navigation and Control components. &#160;To be populated by a mission specific team. */
                    package 'L4.1.5.2_Structures' {
                        #Component part def Software {
                        }
                        #Component part def Accelerometer {
                        }
                        #Component part def 'GNSS Receiver' {
                        }
                    }
                    package 'L4.1.5.1_Behaviors' {
                    }
                }
                package 'L4.1.6_Structures and Mechanisms Components' {
                    doc /* p {padding:0px; margin:0px;} Package for CubeSat Structures and Mechanisms components. &#160;To be populated by a mission specific team. */
                    package 'L4.1.6.1_Behaviors' {
                    }
                    package 'L4.1.6.2_Structures' {
                        #Component part def 'Static Mount' {
                        }
                        #Component part def 'Deployable Mount' {
                        }
                        #Component part def 'Actuated Mount' {
                        }
                    }
                }
                package 'L4.1.7_Power Components' {
                    doc /* p {padding:0px; margin:0px;} Package for CubeSat Power components. &#160;To be populated by a mission specific team. */
                    package 'L4.1.7.2_Structures' {
                        #Component part def 'Processor and Memory' {
                        }
                        #Component part def Software {
                        }
                        #Component part def 'Solar Arrays' {
                        }
                        #Component part def Batteries {
                        }
                        #Component part def 'Regulators and Converters' {
                        }
                        #Component part def 'Power Circuits and Switches' {
                        }
                    }
                    package 'L4.1.7.1_Behaviors' {
                    }
                }
                package 'L4.1.8_Thermal Components' {
                    doc /* p {padding:0px; margin:0px;} Package for CubeSat Mission Thermal components. &#160;To be populated by a mission specific team. */
                    package 'L4.1.8.2_Structures' {
                        #Component part def 'Processor and Memory' {
                        }
                        #Component part def Software {
                        }
                        #Component part def 'Thermal Sensors, Sources, and Sinks' {
                        }
                    }
                    package 'L4.1.8.1_Behaviors' {
                    }
                }
                package 'L4.1.9_Propulsion Components' {
                    doc /* p {padding:0px; margin:0px;} Package for CubeSat Propulsion components. &#160;To be populated by a mission specific team. */
                    package 'L4.1.9.2_Structures' {
                        #Component part def 'Processor and Memory' {
                        }
                        #Component part def Software {
                        }
                        #Component part def 'Propellant Storage' {
                        }
                        #Component part def 'Propellant Control' {
                        }
                        #Component part def Thrusters {
                        }
                    }
                    package 'L4.1.9.1_Behaviors' {
                    }
                }
                package 'L4.1.0_Shared Components' {
                    doc /* p {padding:0px; margin:0px;} Package for CubeSat subsystem Shared components. &#160;To be populated by a mission specific team. */
                    package 'L4.1.0.2_Structures' {
                        #Component part def 'Shared Processor and Memory' {
                        }
                    }
                    package 'L4.1.0.1_Behaviors' {
                    }
                }
            }
            package 'L4.2_Ground Subsystems Components' {
                doc /* p {padding:0px; margin:0px;} The package for Ground subsystems components. &#160;To be populated by a mission specific team. Ground Subsystems Components - Population */
                package 'L4.2.1_Plan and Schedule Components' {
                    doc /* p {padding:0px; margin:0px;} Package for Ground Plan and Schedule subsystem components. &#160;To be populated by a mission specific team. */
                    package 'L4.2.1.2_Structures' {
                        #Component part def Software {
                        }
                        #Component part def Hardware {
                        }
                        #Component part def Procedures {
                        }
                    }
                    package 'L4.2.1.1_Behaviors' {
                    }
                }
                package 'L4.2.3_Ground Equipment Control Components' {
                    doc /* p {padding:0px; margin:0px;} Package for Ground Equipment Control subsystem components. &#160;To be populated by a mission specific team. */
                    package 'L4.2.3.1_Behaviors' {
                    }
                    package 'L4.2.3.2_Structures' {
                        #Component part def Software {
                        }
                        #Component part def Hardware {
                        }
                        #Component part def Procedures {
                        }
                    }
                }
                package 'L4.2.4_Space-Ground Communication Components' {
                    doc /* p {padding:0px; margin:0px;} Package for Ground Space-Ground&#160;Communication subsystem components. &#160;To be populated by a mission specific team. */
                    package 'L4.2.4.1_Behaviors' {
                    }
                    package 'L4.2.4.2_Structures' {
                        #Component part def Software {
                        }
                        #Component part def Hardware {
                        }
                        #Component part def Procedures {
                        }
                    }
                }
                package 'L4.2.2_Spacecraft Command Components' {
                    doc /* p {padding:0px; margin:0px;} Package for Ground Spacecraft&#160;Command subsystem components. &#160;To be populated by a mission specific team. */
                    package 'L4.2.2.2_Structures' {
                        #Component part def Software {
                        }
                        #Component part def Hardware {
                        }
                        #Component part def Procedures {
                        }
                    }
                    package 'L4.2.2.1_Behaviors' {
                    }
                }
                package 'L4.2.5_Mission Data Processing Components' {
                    doc /* p {padding:0px; margin:0px;} Package for Ground Mission Data&#160;Processing subsystem components. &#160;To be populated by a mission specific team. */
                    package 'L4.2.5.1_Behaviors' {
                    }
                    package 'L4.2.5.2_Structures' {
                        #Component part def Software {
                        }
                        #Component part def Hardware {
                        }
                        #Component part def Procedures {
                        }
                    }
                }
                package 'L4.2.6_Mission Data Dissemination Components' {
                    doc /* p {padding:0px; margin:0px;} Package for Ground Mission&#160;Data&#160;Dissemination subsystem components. &#160;To be populated by a mission specific team. */
                    package 'L4.2.6.1_Behaviors' {
                    }
                    package 'L4.2.6.2_Structures' {
                        #Component part def Software {
                        }
                        #Component part def Hardware {
                        }
                        #Component part def Procedures {
                        }
                    }
                }
                package 'L4.2.7_Network Components' {
                    doc /* p {padding:0px; margin:0px;} Package for Ground Network subsystem components. &#160;To be populated by a mission specific team. */
                    package 'L4.2.7.1_Behaviors' {
                    }
                    package 'L4.2.7.2_Structures' {
                        #Component part def Hardware {
                        }
                        #Component part def Procedures {
                        }
                        #Component part def Software {
                        }
                    }
                }
                package 'L4.2.8_Facilities Components' {
                    package 'L4.2.8.1_Behaviors' {
                    }
                    package 'L4.2.8.2_Structures' {
                        #Component part def Room {
                        }
                        #Component part def 'Room 2' {
                        }
                    }
                }
                package 'L4.2.9_Telemetry Processing Components' {
                    package 'L4.2.9.1_Behaviors' {
                    }
                    package 'L4.2.9.2_Structures' {
                        doc /* Select Components Table / Select in Containment Tree to locate Components pkg in the Containment tree Open the Components Table Select Add New to add a new component to the containment tree and to the table Open Components bdd Drag the new components element from the containment tree do to the Components bdd. Open the Subsystem bdd Drag the new component element from the containment tree to the Subsystems bdd – to the Components pkg – to the Structure pkg Right click the Subsystem block, select the directed composition relationship, and drag to the new component element Return to the Component Population pkg. Open the Ground Subsystems Structures Table to see the components associated with the Subsystem */
                        #Component part def Hardware {
                        }
                        #Component part def Software {
                        }
                        #Component part def Procedures {
                        }
                    }
                }
            }
        }
        package L3_Subsystems {
            doc /* p {padding:0px; margin:0px;} The package for CubeSat subsystems and Ground subsystems. &#160; The CubeSat and Ground subsystems are generically and loosely defined as a starting point for the mission specific CubeSat team. The CubeSat team determines what subsystem capabilities are needed and whether they are provided by software, hardware, persistent data, or operator procedures. */
            package 'L3.1_CubeSat Subsystems' {
                doc /* p {padding:0px; margin:0px;} The package of CubeSat subsystems behaviors and structures. */
                package 'L3.1.2_Structures' {
                    doc /* p {padding:0px; margin:0px;} The package of CubeSat subsystems structures:&#160; Mission Payload Command and Data Handling Communication Attitude Determination and Control Guidance Navigation and&#160;Control Structures and Mechanisms Power Thermal Propulsion Select CubeSat Subsystems Structures Table / Select in Containment Tree to locate Subsystems pkg in the Containment tree Open the CubeSat Subsystems Structures table and select Add New to add a new subsystem the containment tree and to the table. Drag the new subsystem element from the containment tree to the CubeSat Subsystems bdd Drag the new subsystem element from the containment tree to the Space Segment bdd. Right click the Cubesat block and select directed composition and drag to the new subsystem element. Open the CubeSat Structures Table and right click on Refresh to make the new subsystem a CubeSat part. CubeSat Subsystems - Population */
                    #Subsystem part def 'Thermal Subsystem' {
                        part Property_1 : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.1_CubeSat Subsystems Components'::'L4.1.8_Thermal Components'::'L4.1.8.2_Structures'::'Thermal Sensors, Sources, and Sinks';
                        part 'processor and Memory' : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.1_CubeSat Subsystems Components'::'L4.1.8_Thermal Components'::'L4.1.8.2_Structures'::'Processor and Memory';
                        part software : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.1_CubeSat Subsystems Components'::'L4.1.8_Thermal Components'::'L4.1.8.2_Structures'::Software;
                    }
                    #Subsystem part def 'Propulsion Subsystem' {
                        part 'propellant Storage' : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.1_CubeSat Subsystems Components'::'L4.1.9_Propulsion Components'::'L4.1.9.2_Structures'::'Propellant Storage';
                        part 'propellant Control' : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.1_CubeSat Subsystems Components'::'L4.1.9_Propulsion Components'::'L4.1.9.2_Structures'::'Propellant Control';
                        part thrusters : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.1_CubeSat Subsystems Components'::'L4.1.9_Propulsion Components'::'L4.1.9.2_Structures'::Thrusters;
                        part 'processor and Memory' : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.1_CubeSat Subsystems Components'::'L4.1.9_Propulsion Components'::'L4.1.9.2_Structures'::'Processor and Memory';
                        part software : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.1_CubeSat Subsystems Components'::'L4.1.9_Propulsion Components'::'L4.1.9.2_Structures'::Software;
                    }
                    #Subsystem part def 'Structures and Mechanisms Subsystem' {
                        part 'deployable Mount' : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.1_CubeSat Subsystems Components'::'L4.1.6_Structures and Mechanisms Components'::'L4.1.6.2_Structures'::'Deployable Mount';
                        part 'static Mount' : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.1_CubeSat Subsystems Components'::'L4.1.6_Structures and Mechanisms Components'::'L4.1.6.2_Structures'::'Static Mount';
                        part 'actuated Mount' : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.1_CubeSat Subsystems Components'::'L4.1.6_Structures and Mechanisms Components'::'L4.1.6.2_Structures'::'Actuated Mount';
                    }
                    #Subsystem part def 'Power Subsystem' {
                        part batteries : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.1_CubeSat Subsystems Components'::'L4.1.7_Power Components'::'L4.1.7.2_Structures'::Batteries;
                        part 'regulators and Converters' : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.1_CubeSat Subsystems Components'::'L4.1.7_Power Components'::'L4.1.7.2_Structures'::'Regulators and Converters';
                        part 'solar Arrays' : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.1_CubeSat Subsystems Components'::'L4.1.7_Power Components'::'L4.1.7.2_Structures'::'Solar Arrays';
                        part 'power Circuits and Switches' : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.1_CubeSat Subsystems Components'::'L4.1.7_Power Components'::'L4.1.7.2_Structures'::'Power Circuits and Switches';
                        part 'processor and Memory' : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.1_CubeSat Subsystems Components'::'L4.1.7_Power Components'::'L4.1.7.2_Structures'::'Processor and Memory';
                        part software : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.1_CubeSat Subsystems Components'::'L4.1.7_Power Components'::'L4.1.7.2_Structures'::Software;
                    }
                    #Subsystem part def 'Attitude Determination and Control Subsystem' {
                        part software : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.1_CubeSat Subsystems Components'::'L4.1.4_Attitude Determination and Control Components'::'L4.1.4.2_Structures'::Software;
                        part actuator : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.1_CubeSat Subsystems Components'::'L4.1.4_Attitude Determination and Control Components'::'L4.1.4.2_Structures'::Actuator;
                        part sensor : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.1_CubeSat Subsystems Components'::'L4.1.4_Attitude Determination and Control Components'::'L4.1.4.2_Structures'::Sensor;
                        part 'shared Processor and Memory' : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.1_CubeSat Subsystems Components'::'L4.1.0_Shared Components'::'L4.1.0.2_Structures'::'Shared Processor and Memory';
                    }
                    #Subsystem part def 'Command and Data Handling Subsystem' {
                        part Property_1 : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.1_CubeSat Subsystems Components'::'L4.1.2_Command and Data Handling Components'::'L4.1.2.2_Structures'::'Command, Telemetry, and Data Bus';
                        part 'processor and Memory' : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.1_CubeSat Subsystems Components'::'L4.1.2_Command and Data Handling Components'::'L4.1.2.2_Structures'::'Processor and Memory';
                    }
                    #Subsystem part def 'Communication Subsystem' {
                        part 'processor and Memory' : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.1_CubeSat Subsystems Components'::'L4.1.3_Communication Components'::'L4.1.3.2_Structures'::'Processor and Memory';
                        part 'receive Antenna and Equipment' : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.1_CubeSat Subsystems Components'::'L4.1.3_Communication Components'::'L4.1.3.2_Structures'::'Receive Antenna and Equipment';
                        part 'transmit Antenna and Equipment' : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.1_CubeSat Subsystems Components'::'L4.1.3_Communication Components'::'L4.1.3.2_Structures'::'Transmit Antenna and Equipment';
                    }
                    #Subsystem part def 'Guidance Navigation and Control Subsystem' {
                        part accelerometer : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.1_CubeSat Subsystems Components'::'L4.1.5_Guidance Navigation and Control Components'::'L4.1.5.2_Structures'::Accelerometer;
                        part 'gNSS Receiver' : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.1_CubeSat Subsystems Components'::'L4.1.5_Guidance Navigation and Control Components'::'L4.1.5.2_Structures'::'GNSS Receiver';
                        part software : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.1_CubeSat Subsystems Components'::'L4.1.5_Guidance Navigation and Control Components'::'L4.1.5.2_Structures'::Software;
                        part 'shared Processor and Memory' : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.1_CubeSat Subsystems Components'::'L4.1.0_Shared Components'::'L4.1.0.2_Structures'::'Shared Processor and Memory';
                    }
                    #Subsystem part def 'Mission Payload Subsystem' {
                        part instrument : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.1_CubeSat Subsystems Components'::'L4.1.1_Mission Payload Components'::'L4.1.1.2_Structures'::Instrument;
                        part 'processor and Memory' : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.1_CubeSat Subsystems Components'::'L4.1.1_Mission Payload Components'::'L4.1.1.2_Structures'::'Processor and Memory';
                    }
                }
                package 'L3.1.1_Behaviors' {
                    doc /* p {padding:0px; margin:0px;} The package of CubeSat subsystems behaviors, use cases, and activities. &#160;To be populated by a mission specific team. */
                    package 'L3.1.1.1_CubeSat Subsystems Behaviors' {
                        doc /* The repository for CubeSat subsystems behaviors. To be populated by a mission-specific team. */
                        package 'CubeSat Subsystem Behavior A' {
                            doc /* Example / placeholder / template for CubeSat Subsystems Behaviors */
                        }
                    }
                    package 'L3.1.1.3_CubeSat Subsystems Activities' {
                        doc /* The repository for CubeSat subsystems activities. To be populated by a mission-specific team. */
                        package 'CubeSat Subsystem Activity A' {
                            doc /* Example / placeholder / template for CubeSat Subsystems Activities */
                            action def 'CubeSat Subsystem Activity A';
                        }
                    }
                    package 'L3.1.1.2_CubeSat Subsystems Use Cases' {
                        doc /* The repository for CubeSat subsystems use cases. To be populated by a mission-specific team. */
                        package 'CubeSat Subsystem Use Case A' {
                            doc /* Example / placeholder / template for CubeSat Subsystems Use Cases */
                        }
                    }
                }
            }
            package 'L3.2_Ground Subsystems' {
                doc /* p {padding:0px; margin:0px;} The package of Ground subsystems behaviors and structures. */
                package 'L3.2.1_Behaviors' {
                    doc /* p {padding:0px; margin:0px;} The package of Ground subsystems behaviors, use cases, and activities. &#160;To be populated by a mission specific team. */
                    package 'L3.2.1.1_Ground Subsystems Behaviors' {
                        doc /* The repository for Ground subsystems behaviors. To be populated by a mission-specific team */
                        package 'Ground Subsystems Behavior A' {
                            doc /* Example / placeholder / template for Ground Subsystems Behaviors */
                        }
                    }
                    package 'L3.2.1.3_Ground Subsystems Activities' {
                        doc /* The repository for Ground subsystems activities. To be populated by a mission-specific team */
                        package 'Ground Subsystem Activity A' {
                            doc /* Example / placeholder / template for Ground Subsystems Activities. */
                            action def 'Ground Subsystem Activity A';
                        }
                    }
                    package 'L3.2.1.2_Ground Subsystems Use Cases' {
                        doc /* The repository for Ground subsystems use cases. To be populated by a mission-specific team. */
                        package 'Ground Subsystem Use Case A' {
                            doc /* Example / placeholder / template for Ground Subsystems Use Cases */
                        }
                    }
                }
                package 'L3.2.2_Structures' {
                    doc /* p {padding:0px; margin:0px;} The package of Ground subsystems structures: Plan and Schedule Spacecraft&#160;Command Ground Equipment Control Space - Ground&#160;Communication Mission Data Processing Mission Data Dissemination Network &#160; &#160; Select Ground Subsystems Structures Table / Select in Containment Tree to locate Subsystems pkg in the Containment tree Open the Ground Subsystems Structures Table and select Add New to add a new subsystem to the containment tree and to the table. Drag the new subsystem element from the containment tree to the Ground Subsystems bdd Drag the new subsystem element from the containment tree to the Ground Segment bdd. Right click the Ground Segment block and select directed composition and drag to the new subsystem element. Open the Ground Segment Structures Table and right click on Refresh to make the new subsystem a Ground Segment part. Ground Subsystems - Popuation */
                    #Subsystem part def 'Spacecraft Command Subsystem' {
                        part hardware : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.2_Ground Subsystems Components'::'L4.2.2_Spacecraft Command Components'::'L4.2.2.2_Structures'::Hardware;
                        part software : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.2_Ground Subsystems Components'::'L4.2.2_Spacecraft Command Components'::'L4.2.2.2_Structures'::Software;
                        part procedures : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.2_Ground Subsystems Components'::'L4.2.2_Spacecraft Command Components'::'L4.2.2.2_Structures'::Procedures;
                    }
                    #Subsystem part def 'Mission Data Dissemination Subsystem' {
                        part hardware : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.2_Ground Subsystems Components'::'L4.2.6_Mission Data Dissemination Components'::'L4.2.6.2_Structures'::Hardware;
                        part software : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.2_Ground Subsystems Components'::'L4.2.6_Mission Data Dissemination Components'::'L4.2.6.2_Structures'::Software;
                        part procedures : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.2_Ground Subsystems Components'::'L4.2.6_Mission Data Dissemination Components'::'L4.2.6.2_Structures'::Procedures;
                    }
                    #Subsystem part def 'Network Subsystem' {
                        part hardware : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.2_Ground Subsystems Components'::'L4.2.7_Network Components'::'L4.2.7.2_Structures'::Hardware;
                        part software : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.2_Ground Subsystems Components'::'L4.2.7_Network Components'::'L4.2.7.2_Structures'::Software;
                        part procedures : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.2_Ground Subsystems Components'::'L4.2.7_Network Components'::'L4.2.7.2_Structures'::Procedures;
                    }
                    #Subsystem part def 'Space - Ground Communication Subsystem' {
                        part hardware : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.2_Ground Subsystems Components'::'L4.2.4_Space-Ground Communication Components'::'L4.2.4.2_Structures'::Hardware;
                        part software : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.2_Ground Subsystems Components'::'L4.2.4_Space-Ground Communication Components'::'L4.2.4.2_Structures'::Software;
                        part procedures : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.2_Ground Subsystems Components'::'L4.2.4_Space-Ground Communication Components'::'L4.2.4.2_Structures'::Procedures;
                    }
                    #Subsystem part def 'Mission Data Processing Subsystem' {
                        part harware : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.2_Ground Subsystems Components'::'L4.2.5_Mission Data Processing Components'::'L4.2.5.2_Structures'::Hardware;
                        part software : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.2_Ground Subsystems Components'::'L4.2.5_Mission Data Processing Components'::'L4.2.5.2_Structures'::Software;
                        part procedures : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.2_Ground Subsystems Components'::'L4.2.5_Mission Data Processing Components'::'L4.2.5.2_Structures'::Procedures;
                    }
                    #Subsystem part def 'Plan and Schedule Subsystem' {
                        part hardware : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.2_Ground Subsystems Components'::'L4.2.1_Plan and Schedule Components'::'L4.2.1.2_Structures'::Hardware;
                        part procedures : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.2_Ground Subsystems Components'::'L4.2.1_Plan and Schedule Components'::'L4.2.1.2_Structures'::Procedures;
                        part software : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.2_Ground Subsystems Components'::'L4.2.1_Plan and Schedule Components'::'L4.2.1.2_Structures'::Software;
                    }
                    #Subsystem part def 'Ground Equipment Control Subsystem' {
                        part hardware : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.2_Ground Subsystems Components'::'L4.2.3_Ground Equipment Control Components'::'L4.2.3.2_Structures'::Hardware;
                        part software : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.2_Ground Subsystems Components'::'L4.2.3_Ground Equipment Control Components'::'L4.2.3.2_Structures'::Software;
                        part procedures : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.2_Ground Subsystems Components'::'L4.2.3_Ground Equipment Control Components'::'L4.2.3.2_Structures'::Procedures;
                    }
                    #Subsystem part def 'Facilities Subsystem' {
                        part room : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.2_Ground Subsystems Components'::'L4.2.8_Facilities Components'::'L4.2.8.2_Structures'::Room;
                        part 'room 2' : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.2_Ground Subsystems Components'::'L4.2.8_Facilities Components'::'L4.2.8.2_Structures'::'Room 2';
                    }
                    #Subsystem part def 'Telemetry Processing Subsystem' {
                        part procedures : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.2_Ground Subsystems Components'::'L4.2.9_Telemetry Processing Components'::'L4.2.9.2_Structures'::Procedures;
                        part software : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.2_Ground Subsystems Components'::'L4.2.9_Telemetry Processing Components'::'L4.2.9.2_Structures'::Software;
                        part hardware : '01 - CubeSat System Reference Model'::'5 - Architecture'::L4_Components::'L4.2_Ground Subsystems Components'::'L4.2.9_Telemetry Processing Components'::'L4.2.9.2_Structures'::Hardware;
                    }
                }
            }
        }
        package L2_Segment {
            doc /* p {padding:0px; margin:0px;} Package of Space Segment and Ground Segment packages. */
            package 'L2.2_Ground Segment' {
                doc /* p {padding:0px; margin:0px;} Package of Ground segment behaviors and structures &#160; The Ground Segment consists of the CubeSat Mission Operations and one or more Ground Stations. &#160; Mission Operations includes the software, data, procedures, and personnel used to operate the CubeSat mission. Mission Operations activities include mission planning and scheduling, command and control of the CubeSat, control of the ground equipment, mission telemetry processing, and mission data processing and distribution. &#160; The Ground Station consists of the computers, network, communication equipment, and associated control infrastructure hosted in ground facilities. Communication equipment includes the space-ground antennas. */
                package 'L2.2.2_Structures' {
                    #Segment part def 'Ground Segment' {
                        part 'plan and Schedule Subsystem' : '01 - CubeSat System Reference Model'::'5 - Architecture'::L3_Subsystems::'L3.2_Ground Subsystems'::'L3.2.2_Structures'::'Plan and Schedule Subsystem';
                        part 'spacecraft Command Subsystem' : '01 - CubeSat System Reference Model'::'5 - Architecture'::L3_Subsystems::'L3.2_Ground Subsystems'::'L3.2.2_Structures'::'Spacecraft Command Subsystem';
                        part 'ground Equipment Control Subsystem' : '01 - CubeSat System Reference Model'::'5 - Architecture'::L3_Subsystems::'L3.2_Ground Subsystems'::'L3.2.2_Structures'::'Ground Equipment Control Subsystem';
                        part 'space - Ground Communication Subsystem' : '01 - CubeSat System Reference Model'::'5 - Architecture'::L3_Subsystems::'L3.2_Ground Subsystems'::'L3.2.2_Structures'::'Space - Ground Communication Subsystem';
                        part 'mission Data Processing Subsystem' : '01 - CubeSat System Reference Model'::'5 - Architecture'::L3_Subsystems::'L3.2_Ground Subsystems'::'L3.2.2_Structures'::'Mission Data Processing Subsystem';
                        part 'network Subsystem' : '01 - CubeSat System Reference Model'::'5 - Architecture'::L3_Subsystems::'L3.2_Ground Subsystems'::'L3.2.2_Structures'::'Network Subsystem';
                        part 'mission Data Dissemination Subsystem' : '01 - CubeSat System Reference Model'::'5 - Architecture'::L3_Subsystems::'L3.2_Ground Subsystems'::'L3.2.2_Structures'::'Mission Data Dissemination Subsystem';
                        part 'facilities Subsystem' : '01 - CubeSat System Reference Model'::'5 - Architecture'::L3_Subsystems::'L3.2_Ground Subsystems'::'L3.2.2_Structures'::'Facilities Subsystem';
                        part 'telemetry Processing Subsystem' : '01 - CubeSat System Reference Model'::'5 - Architecture'::L3_Subsystems::'L3.2_Ground Subsystems'::'L3.2.2_Structures'::'Telemetry Processing Subsystem';
                    }
                }
                package 'L2.2.1_Behaviors' {
                    doc /* Package of Ground Segment behaviors, use cases, and activities. For population by a mission-specific team. */
                    package 'L2.2.1.1_Ground Segment Behaviors' {
                        doc /* Repository for Ground Segment behaviors. To be populated by a mission-specific team */
                        package 'Ground Segment Behavior A' {
                            doc /* Example / placeholder / template for Ground Segment Behaviors */
                        }
                    }
                    package 'L2.2.1.2_Ground Segment Use Cases' {
                        doc /* Repository for Ground Segment use cases. To be populated by a mission-specific team */
                        package 'Ground Segment Use Case A' {
                            doc /* Example / placeholder / template for Ground Segment Use Cases. */
                        }
                    }
                    package 'L2.2.1.3_Ground Segment Activities' {
                        doc /* Repository for Ground Segment activities. To be populated by a mission-specific team */
                        package 'Ground Segment Activity A' {
                            doc /* Example / placeholder / template for Ground Segment Activities. */
                            action def 'Ground Segment Activity A';
                        }
                    }
                }
            }
            package 'L2.1_Space Segment' {
                doc /* p {padding:0px; margin:0px;} Package of Space&#160;Segment behaviors and structures. &#160; The CubeSat Space Segment consists of one or more CubeSats with their orbits and subsystems. &#160; The Space Segment includes designs, interfaces, and operations to comply with the Rqts and constraints of the Transport, Launch, and Deploy Services. */
                package 'L2.1.1_Behaviors' {
                    doc /* p {padding:0px; margin:0px;} Package of CubeSat behaviors. use cases, and activities. &#160;For population by a mission-specific team. */
                    package 'L2.1.1.1_CubeSat Behaviors' {
                        doc /* Repository for CubeSat behaviors. To be populated by a mission-specific team. */
                        package 'CubeSat Behavior A' {
                            doc /* Example / placeholder / template for Cubesat Behaviors */
                        }
                    }
                    package 'L2.1.1.3_CubeSat Activities' {
                        doc /* The repository for CubeSat activities. To be populated by a mission specific team. */
                        package 'CubeSat Activity A' {
                            doc /* Example / placeholder / template for Cubesat Activities */
                            action def 'CubeSat Activity A';
                        }
                    }
                    package 'L2.1.1.2_CubeSat Use Cases' {
                        doc /* The repository for CubeSat use cases. To be populated by a mission specific team. */
                        package 'CubeSat Use Case A' {
                            doc /* An example / placeholder / template for CubeSat Use Cases. */
                        }
                    }
                }
                package 'L2.1.2_Structures' {
                    doc /* p {padding:0px; margin:0px;} Package of Space Segment structures. */
                    #Segment part def 'Space Segment' {
                        part cubeSat : '01 - CubeSat System Reference Model'::'5 - Architecture'::L2_Segment::'L2.1_Space Segment'::'L2.1.2_Structures'::CubeSat[0..*];
                        part 'cubeSat Orbit' : '01 - CubeSat System Reference Model'::'5 - Architecture'::L2_Segment::'L2.1_Space Segment'::'L2.1.2_Structures'::'CubeSat Orbit'[0..*];
                    }
                    #CubeSat part def CubeSat {
                        attribute Orbit;
                        part 'mission Payload1' : '01 - CubeSat System Reference Model'::'5 - Architecture'::L3_Subsystems::'L3.1_CubeSat Subsystems'::'L3.1.2_Structures'::'Mission Payload Subsystem';
                        part 'command and Data Handling Subsystem1' : '01 - CubeSat System Reference Model'::'5 - Architecture'::L3_Subsystems::'L3.1_CubeSat Subsystems'::'L3.1.2_Structures'::'Command and Data Handling Subsystem';
                        part 'communication Subsystem1' : '01 - CubeSat System Reference Model'::'5 - Architecture'::L3_Subsystems::'L3.1_CubeSat Subsystems'::'L3.1.2_Structures'::'Communication Subsystem';
                        part 'attitude Determination and Control Subsystem1' : '01 - CubeSat System Reference Model'::'5 - Architecture'::L3_Subsystems::'L3.1_CubeSat Subsystems'::'L3.1.2_Structures'::'Attitude Determination and Control Subsystem';
                        part 'guidance Navigation and Control Subsystem' : '01 - CubeSat System Reference Model'::'5 - Architecture'::L3_Subsystems::'L3.1_CubeSat Subsystems'::'L3.1.2_Structures'::'Guidance Navigation and Control Subsystem';
                        part 'structures and Mechanisms Subsystem1' : '01 - CubeSat System Reference Model'::'5 - Architecture'::L3_Subsystems::'L3.1_CubeSat Subsystems'::'L3.1.2_Structures'::'Structures and Mechanisms Subsystem';
                        part 'power Subsystem1' : '01 - CubeSat System Reference Model'::'5 - Architecture'::L3_Subsystems::'L3.1_CubeSat Subsystems'::'L3.1.2_Structures'::'Power Subsystem';
                        part 'propulsion Subsystem1' : '01 - CubeSat System Reference Model'::'5 - Architecture'::L3_Subsystems::'L3.1_CubeSat Subsystems'::'L3.1.2_Structures'::'Propulsion Subsystem';
                        part 'thermal Subsystem1' : '01 - CubeSat System Reference Model'::'5 - Architecture'::L3_Subsystems::'L3.1_CubeSat Subsystems'::'L3.1.2_Structures'::'Thermal Subsystem';
                    }
                    part def 'CubeSat Orbit' {
                        attribute eccentricity;
                        attribute 'semi-major axis';
                        attribute inclination;
                        attribute 'longitude of ascending node';
                        attribute 'argument of perigee';
                        attribute 'true anomaly at epoch';
                        attribute 'time of epoch';
                    }
                }
            }
        }
        package L1_Enterprise {
            doc /* p {padding:0px; margin:0px;} Package of Enterprise behaviors and structures. &#160; &#160; Enterprise is an aggregation of systems and users that work together to accomplish a goal. &#160; At its most basic the CubeSat Mission Enterprise consists of the CubeSat Space Segment and the CubeSat Ground Segment. */
            package 'L1.1_Behaviors' {
                doc /* p {padding:0px; margin:0px;} The package of Enterprise behaviors, use cases, and activities. */
                package 'L1.1.1_Enterprise Behaviors' {
                    doc /* The respository for Enterprise behaviors. To be populated by a mission specific team. */
                    package 'Enterprise Behavior A' {
                        doc /* An example / placeholder / template for Enterprise Behaviors */
                    }
                }
                package 'L1.1.3_Enterprise Activities' {
                    doc /* The repository for Enterprise activities. To be populated by a mission specific team. */
                    package 'Enterprise Activity A' {
                        doc /* An example / placeholder / template for Enterprise Activities */
                        action def 'Enterprise Activity A';
                    }
                }
                package 'L1.1.2_Enterprise Use Cases' {
                    doc /* The repository for Enterprise use cases. To be populated by a mission specific team. */
                    package 'Enterprise Use Case A' {
                        doc /* An example / placeholder / template for Enterprise Use Cases */
                    }
                }
            }
            package 'L1.2_Structures' {
                doc /* p {padding:0px; margin:0px;} The package of Enterprise structures. */
                part def 'CubeSat Mission Enterprise' {
                    part 'ground Station Services' : '01 - CubeSat System Reference Model'::'5 - Architecture'::L1_Enterprise::'L1.2_Structures'::'Ground Station Services';
                    part Property_2 : '01 - CubeSat System Reference Model'::'5 - Architecture'::L1_Enterprise::'L1.2_Structures'::'Transport, Launch, and Deploy Services';
                    part 'space Segment' : '01 - CubeSat System Reference Model'::'5 - Architecture'::L2_Segment::'L2.1_Space Segment'::'L2.1.2_Structures'::'Space Segment';
                    part 'ground Segment' : '01 - CubeSat System Reference Model'::'5 - Architecture'::L2_Segment::'L2.2_Ground Segment'::'L2.2.2_Structures'::'Ground Segment';
                    part GPS : '01 - CubeSat System Reference Model'::'5 - Architecture'::L1_Enterprise::'L1.2_Structures'::GNSS;
                }
                part def 'Ground Station Services' {
                }
                part def 'Transport, Launch, and Deploy Services' {
                }
                part def GNSS {
                }
            }
        }
        package Facilities {
            doc /* p {padding:0px; margin:0px;} A mission-specific team will populate the Facilities package with facilities, equipment, properties, and part relationships Just a start at how to accommodate Faciliities The mission-specific team will populate the Facilities package with facilities, equipment, properties, and part relationships */
            #Facility part def 'Development Facility' {
                part 'design Facility' : '01 - CubeSat System Reference Model'::'5 - Architecture'::Facilities::'Design Facility';
                part 'production Facility' : '01 - CubeSat System Reference Model'::'5 - Architecture'::Facilities::'Production Facility';
                part 'integration Facility' : '01 - CubeSat System Reference Model'::'5 - Architecture'::Facilities::'Integration Facility';
                part 'test Facility' : '01 - CubeSat System Reference Model'::'5 - Architecture'::Facilities::'Test Facility';
            }
            #Facility part def 'Operations Facility' {
            }
            #Facility part def 'Design Facility' {
                part offices : '01 - CubeSat System Reference Model'::'5 - Architecture'::Facilities::Offices;
            }
            #Facility part def 'Production Facility' {
                part 'clean Room' : '01 - CubeSat System Reference Model'::'5 - Architecture'::Facilities::'Clean Room';
            }
            #Facility part def 'Integration Facility' {
            }
            #Facility part def 'Test Facility' {
                part 'thermal Vacuum Chamber' : '01 - CubeSat System Reference Model'::'5 - Architecture'::Facilities::'Thermal Vacuum Chamber';
                part 'helmoltz Cage' : '01 - CubeSat System Reference Model'::'5 - Architecture'::Facilities::'Helmoltz Cage';
            }
            #Equipment part def 'Thermal Vacuum Chamber' {
            }
            #Facility part def 'Clean Room' {
            }
            #Facility part def Offices {
            }
            #Equipment part def 'Helmoltz Cage' {
            }
        }
    }
    package '4 - Requirements' {
        doc /* p {padding:0px; margin:0px;} The Rqts and logical architecture hierarchies are parallel constructs. Requirement packages are numbered to be consistent with the corresponding architecture packages. Individual Rqts are numbered uniquely according to a prefix based on the name of the Rqts packages. &#160;The modeler can easily change the prefix. The CSRM provides for tracing Rqts from stakeholders, behaviors, and technical measures down to subsystems and components and then to validation and verification activities. &#160; The requirement element properties include:&#160;&#160;&#160; Rationale &#160;&#160;&#160;Traced To &#160;&#160;&#160;&#160;Traced From &#160;&#160;&#160;Derived From &#160;&#160;&#160;Refined By &#160;&#160;&#160;Verify Method &#160;&#160;&#160;Verified By &#160;&#160;&#160;Satisfied By The modeler can easily change the prefix by Select a requirement in the containment tree and Select Element Numbering Double-click on table and add and delete requirements as needed Click on Add New to add a new requirement to the containment tree and to the table. Right click the new requirement in the table then left click Select in Containment Tree to navigate to the new element. Select an requirement and click on Delete to delete from the requirement table and the Containment Tree. Double-click on the CubeSat, Ground Segment, CubeSat Subsystem, and Ground Subsystem requirement packages to navigate to the requirement tables. The requirement element properties include: Rationale Traced To Traced From Derived From Verify Method Verified By Satisfied By Requirement packages are numbered to be consistent with the corresponding architecture packages. Individual requirements are numbered uniquely according to a prefix based on the name of the requirements packages. The requirement elements reside in the containment tree. The requirement tables are views of the requirement elements. A table can be deleted but the requirement elements and their hierarchy remains. Requirements are added to the table using “Add New or “Add Nested” and the requirement Ids are automatically updated. Requirements Hierarchy - Population */
        package 'L2 Segment Rqts' {
            doc /* p {padding:0px; margin:0px;} The package for Segment Rqts. &#160;To be populated by a mission-specific team. */
            package 'L2.1 Space Segment Rqts' {
                doc /* p {padding:0px; margin:0px;} Package for Space Segment Rqts */
                package 'L2.1.1 CubeSat Rqts' {
                    doc /* p {padding:0px; margin:0px;} Repository for CubeSat Rqts. &#160;To be populated by a mission-specific team. Double-click on the requirements table and then click on Add New to add a new requirement to the containment tree and to the table. Right click the new element in the table then left click Select in Containment Tree to navigate to the new element. The table can also be used to modify and delete requirements. CubeSat Rqts - Population */
                    #CubeSatRequirement requirement <CSat_1> 'CubeSat Rqts Group' {
                        doc /* The Group provides the prefix and numbering scheme - which is easy to change. */
                        #CubeSatRequirement requirement <'CSat_1.1'> 'Requirement Name' {
                            doc /* Shall Statement */
                        }
                    }
                }
            }
            package 'L2.2 Ground Segment Rqts' {
                doc /* p {padding:0px; margin:0px;} Repository for ground segment Rqts. Double-click on the requirements table and then click on Add New to add a new requirement to the containment tree and to the table. Right click the new element in the table then left click Select in Containment Tree to navigate to the new element. The table can also be used to modify and delete requirements. Ground Segment Rqts - Population */
                #Group requirement <GSeg_1> 'Ground Segment Rqts Group' {
                    doc /* The Group provides the prefix and numbering scheme - which is easy to change. */
                    #GroundSegmentRequirement requirement <'GSeg_1.2'> 'Ground Segment Requirement A' {
                        doc /* Shall statement */
                    }
                }
            }
        }
        package 'L4 Component Rqts' {
            doc /* p {padding:0px; margin:0px;} Package for CubeSat and Ground subsystems components Rqts. &#160;To be populated by a mission-specific team. */
            package 'L4.1 CubeSat Subsystems Components Rqts' {
                doc /* p {padding:0px; margin:0px;} The package is for CubeSat subsystem components Rqts. &#160;To be populated by a mission-specific team. Double-click on a requirements table and then click on Add New to add a new requirement to the containment tree and to the table. Right click the new element in the table then left click Select in Containment Tree to navigate to the new element. The table can also be used to modify and delete requirements. CubeSat Components Rqts - Population */
                package 'L4.1.1 Mission Payload Component Rqts' {
                    doc /* p {padding:0px; margin:0px;} The repository for&#160;Mission Payload components Rqts. &#160;To be populated by a mission-specific team. */
                    #Group requirement <MpCmp_1> 'Mission Payload Component Rqts Breaker' {
                        doc /* The breaker provides the prefix and number scheme. */
                        #ComponentRequirement requirement <'MpCmp_1.1'> 'Requirement Name' {
                            doc /* Shall statement */
                        }
                    }
                }
                package 'L4.1.2 Command and Data Handling Component Rqts' {
                    doc /* p {padding:0px; margin:0px;} The repository for&#160;Command and Data Handling components requirement. &#160;To be populated by a mission-specific team. */
                    #Group requirement <CdCmp__1> 'Command and Data Handling Component Rqts Breaker' {
                        doc /* The breaker provides the prefix and number scheme. */
                        #ComponentRequirement requirement <'CdCmp__1.1'> 'Requirement Name' {
                            doc /* Shall statement */
                        }
                    }
                }
                package 'L4.1.3 Communication Component Rqts' {
                    doc /* p {padding:0px; margin:0px;} The repository for Communication components Rqts. &#160;To be populated by a mission-specific team. */
                    #Group requirement <CmCmp_1> 'Communication Component Rqts Breaker' {
                        doc /* The breaker provides the prefix and number scheme. */
                        #ComponentRequirement requirement <'CmCmp_1.1'> 'Requirement Name' {
                            doc /* Shall statement */
                        }
                    }
                }
                package 'L4.1.4 Attitude Determination and Control Component Rqts' {
                    doc /* p {padding:0px; margin:0px;} The repository for Attitude Determination and Control components Rqts. &#160;To be populated by a mission-specific team. */
                    #Group requirement <AdCmp_1> 'Attitude Determination and Control Component Rqts Breaker' {
                        doc /* The breaker Group the prefix and number scheme. */
                        #ComponentRequirement requirement <'AdCmp_1.1'> 'Requirement Name' {
                            doc /* Shall statement */
                        }
                    }
                }
                package 'L4.1.5 Guidance Navigation and Control Component Rqts' {
                    doc /* p {padding:0px; margin:0px;} The repository for Guidance Navigation and Control components Rqts. &#160;To be populated by a mission-specific team. */
                    #Group requirement <GnCmp_1> 'Guidance Navigation and Control Component Rqts Group' {
                        doc /* The group provides the prefix and number scheme. */
                        #ComponentRequirement requirement <'GnCmp_1.1'> 'Requirement Name' {
                            doc /* Shall statement */
                        }
                    }
                }
                package 'L4.1.6 Structures and Mechanisms Component Rqts' {
                    doc /* p {padding:0px; margin:0px;} The repository for&#160;Structures and Mechanisms components Rqts. &#160;To be populated by a mission-specific team. */
                    #Group requirement <SmCmp_1> 'Structures and Mechanisms Component Rqts Group' {
                        doc /* The breaker provides the prefix and number scheme. */
                        #ComponentRequirement requirement <'SmCmp_1.1'> 'Requirement Name' {
                            doc /* Shall statement */
                        }
                    }
                }
                package 'L4.1.7 Power Component Rqts' {
                    doc /* p {padding:0px; margin:0px;} Repository for&#160;Power&#160;components Rqts. &#160;To be populated by a mission-specific team. */
                    #Group requirement <PoCmp_1> 'Power Component Rqts Breaker' {
                        doc /* The breaker provides the prefix and number scheme. */
                        #ComponentRequirement requirement <'PoCmp_1.1'> 'Requirement Name' {
                            doc /* Shall statement */
                        }
                    }
                }
                package 'L4.1.8 Thermal Component Rqts' {
                    doc /* p {padding:0px; margin:0px;} Repository for&#160;Thermal components Rqts. &#160;To be populated by a mission-specific team. */
                    #Group requirement <ThCmp_1> 'Thermal Component Rqts Group' {
                        doc /* The breaker provides the prefix and number scheme. */
                        #ComponentRequirement requirement <'ThCmp_1.1'> 'Requirement Name' {
                            doc /* Shall statement */
                        }
                    }
                }
                package 'L4.1.9 Propulsion Component Rqts' {
                    doc /* p {padding:0px; margin:0px;} The repository for Propulsion components Rqts. &#160;To be populated by a mission-specific team. */
                    #Group requirement <PrCmp_1> 'Propulsion Component Rqts Group' {
                        doc /* The breaker provides the prefix and number scheme. */
                        #ComponentRequirement requirement <'PrCmp_1.1'> 'Requirement Name' {
                            doc /* Shall statement */
                        }
                    }
                }
            }
            package 'L4.2 Ground Subsystems Components Rqts' {
                doc /* p {padding:0px; margin:0px;} This package is for the Ground subsystems components Rqts. &#160;To be populated by a mission-specific team. Double-click on a requirements table and then click on Add New to add a new requirement to the containment tree and to the table. Right click the new element in the table then left click Select in Containment Tree to navigate to the new element. The table can also be used to modify and delete requirements. Ground Components Rqts - Population */
                package 'L4.2.1 Plan and Schedule Component Rqts' {
                    doc /* p {padding:0px; margin:0px;} Repository for&#160;Plan and Schedule components Rqts. &#160;To be populated by a mission-specific team. */
                    #Group requirement <PsCmp_1> 'Plan and Schedule Component Rqts Group' {
                        doc /* The Group provides the prefix and number scheme. */
                        #ComponentRequirement requirement <'PsCmp_1.1'> 'Requirement Name' {
                            doc /* Shall statement */
                        }
                    }
                }
                package 'L4.2.2 Spacecraft Command Component Rqts' {
                    doc /* p {padding:0px; margin:0px;} Repository for&#160;Spacecraft Command compoents Rqts. &#160;To be populated by a mission-specific team. */
                    #Group requirement <ScCmp_1> 'Spacecraft Command Component Rqts Breaker' {
                        doc /* The breaker provides the prefix and number scheme. */
                        #ComponentRequirement requirement <'ScCmp_1.1'> 'Requirement Name' {
                            doc /* Shall statement */
                        }
                    }
                }
                package 'L4.2.3 Ground Equipment Control Component Rqts' {
                    doc /* p {padding:0px; margin:0px;} A repository for&#160;Gound&#160;Equipment Control components. &#160;To be populated by a mission-specific team. */
                    #Group requirement <GeCmp_1> 'Ground Equipment Control Component Rqts Breaker' {
                        doc /* The breaker provides the prefix and number scheme. */
                        #ComponentRequirement requirement <'GeCmp_1.1'> 'Requirement Name' {
                            doc /* Shall statement */
                        }
                    }
                }
                package 'L4.2.4 Space-Ground Communication Component Rqts' {
                    doc /* p {padding:0px; margin:0px;} A repository for Space-Ground Communication components Rqts. &#160;To be populated by a mission-specific team. */
                    #Group requirement <SgCmp_1> 'Space-Ground Communication Component Rqts Breaker' {
                        doc /* The breaker provides the prefix and number scheme. */
                        #ComponentRequirement requirement <'SgCmp_1.1'> 'Requirement Name' {
                            doc /* Shall statement */
                        }
                    }
                }
                package 'L4.2.5 Mission Data Processing Component Rqts' {
                    doc /* p {padding:0px; margin:0px;} A repository for Mission&#160;Data Processing components Rqts. &#160;To be populated by a mission-specific team. */
                    #Group requirement <DpCmp_1> 'Mission Data Processing Components Rqts Breaker' {
                        doc /* The breaker provides the prefix and number scheme. */
                        #ComponentRequirement requirement <'DpCmp_1.1'> 'Requirement Name' {
                            doc /* Shall statement */
                        }
                    }
                }
                package 'L4.2.6 Mission Data Dissemination Component Rqts' {
                    doc /* p {padding:0px; margin:0px;} A repository for&#160;Mission Data Dissemination components Rqts. &#160;To be populated by a mission-specific team. */
                    #Group requirement <DdCmp_1> 'Mission Data Dissemination Component Rqts Group' {
                        doc /* The breaker provides the prefix and number scheme. */
                        #ComponentRequirement requirement <'DdCmp_1.1'> 'Requirement Name' {
                            doc /* Shall statement */
                        }
                    }
                }
                package 'L4.2.7 Network Component Rqts' {
                    doc /* p {padding:0px; margin:0px;} A repository for Network components Rqts. &#160;To be populated by a mission-specific team. */
                }
                package 'L4.2.8 Facilities Component Rqts' {
                    doc /* p {padding:0px; margin:0px;} A repository for&#160;Facility components Rqts. &#160;To be populated by a mission-specific team. */
                    #Group requirement <FaCmp_1> 'FacilitiesComponent Rqts Group' {
                        doc /* The breaker provides the prefix and number scheme. */
                        #ComponentRequirement requirement <'FaCmp_1.1'> 'Requirement Name' {
                            doc /* Shall statement */
                        }
                    }
                }
                package 'L4.2.9 Telemetry Components Rqts' {
                    #Group requirement <TpCmp_1> 'Telemetry Components Rqts Group' {
                        doc /* The breaker provides the prefix and number scheme. */
                        #ComponentRequirement requirement <'TpCmp_1.1'> 'Requirement Name' {
                            doc /* Shall statement */
                        }
                    }
                }
            }
        }
        package 'L3 Subsystem Rqts' {
            doc /* p {padding:0px; margin:0px;} The package for Subsystem Rqts. &#160;To be populated by a mission-specific team. */
            package 'L3.2 Ground Subsystems Rqts' {
                doc /* p {padding:0px; margin:0px;} Repository for Ground&#160;Subsystem Rqts. &#160;To be populated by a mission-specific team. Double-click on the requirements table and then click on Add New to add a new requirement to the containment tree and to the table. Right click the new element in the table then left click Select in Containment Tree to navigate to the new element. The table can also be used to modify and delete requirements. Ground Subsystems Rqts - Population */
                package 'L3.2.1 Plan and Schedule Subsystem Rqts' {
                    doc /* p {padding:0px; margin:0px;} The repository for Plan and Schedule subsystem Rqts. &#160;To be populated by a mission-specific team. */
                    comment about '01 - CubeSat System Reference Model'::'4 - Requirements'::'L3 Subsystem Rqts'::'L3.2 Ground Subsystems Rqts'::'L3.2.1 Plan and Schedule Subsystem Rqts'::'Plan and Schedule Subsystem Rqts Group'::'Plan and Schedule Requirement A' /* The rationale model element can be associated with a requirement, a requirement relationship, or any other model element. It is intended to capture the reason for a particular decision. It is based on the comment element. */
                    #Group requirement <PsSub_1> 'Plan and Schedule Subsystem Rqts Group' {
                        doc /* The Group provides the prefix and numbering scheme - which is easy to change. */
                        #SubsystemRequirement requirement <'PsSub_1.1'> 'Plan and Schedule Requirement A' {
                            doc /* Shall statement */
                        }
                    }
                }
                package 'L3.2.2 Spacecraft Command Subsystem Rqts' {
                    doc /* p {padding:0px; margin:0px;} The repository for Spacecraft Command subsystem Rqts. &#160;To be populated by a mission-specific team. */
                    #Group requirement <ScSub_1> 'Spacecraft Command Subsystem Rqts Group' {
                        doc /* The Group provides the prefix and numbering scheme - which is easy to change. */
                        #SubsystemRequirement requirement <'ScSub_1.1'> 'Requirement Name' {
                            doc /* Shall statement */
                        }
                    }
                }
                package 'L3.2.3 Ground Equipment Control Subsystem Rqts' {
                    doc /* p {padding:0px; margin:0px;} The repository for Ground&#160;Equipment Control subsystem Rqts. &#160;To be populated by a mission-specific team. */
                    #Group requirement <GeSub_1> 'Ground Equipment Control Subsystem Rqts Group' {
                        doc /* The Group provides the prefix and numbering scheme - which is easy to change. */
                        #SubsystemRequirement requirement <'GeSub_1.1'> 'Requirement Name' {
                            doc /* Shall statement */
                        }
                    }
                }
                package 'L3.2.4 Space-Ground Communication Subsystem Rqts' {
                    doc /* p {padding:0px; margin:0px;} The repository for Space-Ground Communication subsystem Rqts. &#160;To be populated by a mission-specific team. */
                    #Group requirement <SgSub_1> 'Space-Ground Communications Subsystem Rqts Group' {
                        doc /* The Group provides the prefix and numbering scheme - which is easy to change. */
                        #SubsystemRequirement requirement <'SgSub_1.1'> 'Requirement Name' {
                            doc /* Shall statement */
                        }
                    }
                }
                package 'L3.2.5 Mission Data Processing Subsystem Rqts' {
                    doc /* p {padding:0px; margin:0px;} The repository for Mission Data Processing subsystem Rqts. &#160;To be populated by a mission-specific team. */
                    #Group requirement <DpSub_1> 'Mission Data Processing Subsystem Rqts Group' {
                        doc /* The Group provides the prefix and numbering scheme - which is easy to change. */
                        #SubsystemRequirement requirement <'DpSub_1.1'> 'Requirement Name' {
                            doc /* Shall statement */
                        }
                    }
                }
                package 'L3.2.6 Mission Data Dissemination Subsystem Rqts' {
                    doc /* p {padding:0px; margin:0px;} The repository for Mission Data Dissemination subsystem Rqts. &#160;To be populated by a mission-specific team. */
                    #Group requirement <DdSub_1> 'Mission Data Dissemination Rqts Group' {
                        doc /* The Group provides the prefix and numbering scheme - which is easy to change. */
                        #SubsystemRequirement requirement <'DdSub_1.1'> 'Requirement Name' {
                            doc /* Shall statement */
                        }
                    }
                }
                package 'L3.2.7 Network Subsystem Rqts' {
                    doc /* p {padding:0px; margin:0px;} The repository for&#160;Network subsystem Rqts. &#160;To be populated by a mission-specific team. */
                    #Group requirement <NeSub_1> 'Network Subsystem Rqts Group' {
                        doc /* The Group provides the prefix and numbering scheme - which is easy to change. */
                        #SubsystemRequirement requirement <'NeSub_1.1'> 'Requirement Name' {
                            doc /* Shall statement */
                        }
                    }
                }
                package 'L3.2.8 Facility Subsystem Rqts' {
                    doc /* p {padding:0px; margin:0px;} The repository for Facility subsystem Rqts. &#160;To be populated by a mission-specific team. */
                    #Group requirement <FaSub_1> 'Facility Subsystem Rqts Group' {
                        doc /* The Group provides the prefix and numbering scheme - which is easy to change. */
                        #SubsystemRequirement requirement <'FaSub_1.1'> 'Requirement Name' {
                            doc /* Shall statement */
                        }
                    }
                }
                package 'L3.2.9 Telemetry Processing Subsystem Rqts' {
                    #Group requirement <TpSub_1> 'Telemetry Processing Subsystem Rqt Group' {
                        doc /* The Group provides the prefix and numbering scheme - which is easy to change. */
                        #SubsystemRequirement requirement <'TpSub_1.1'> 'Requirement Name' {
                            doc /* Shall statement */
                        }
                    }
                }
            }
            package 'L3.1 CubeSat Subsystems Rqts' {
                doc /* p {padding:0px; margin:0px;} Repository for CubeSat Subsystem Rqts. &#160;To be populated by a mission-specific team. Double-click on the requirements table and then click on Add New to add a new requirement to the containment tree and to the table. Right click the new element in the table then left click Select in Containment Tree to navigate to the new element. The table can also be used to modify and delete requirements. CubeSat Subsystems Rqts - Popuation */
                package 'L3.1.1 Mission Payload Rqts' {
                    doc /* p {padding:0px; margin:0px;} The repository for Mission Payload Rqts. To be populated by a mission-specific team.&#160; */
                    #Group requirement <MpSub_1> 'Mission Payload Rqts Group' {
                        doc /* The Group provides the prefix and numbering scheme - which is easy to change. */
                        #SubsystemRequirement requirement <'MpSub_1.1'> 'Requirement Name' {
                            doc /* Shall statement */
                        }
                    }
                }
                package 'L3.1.2 Command and Data Handling Subsystem Rqts' {
                    doc /* p {padding:0px; margin:0px;} The repository for Command and&#160;Data&#160;Handling subsystem Rqts. &#160;To be populated by a mission-specific team. */
                    #Group requirement <CdSub_1> 'Command and Data Handling Subsystem Rqts Group' {
                        doc /* The Group provides the prefix and numbering scheme - which is easy to change. */
                        #SubsystemRequirement requirement <'CdSub_1.1'> 'Requirement Name' {
                            doc /* Shall statement */
                        }
                    }
                }
                package 'L3.1.3 Communication Subsystem Rqts' {
                    doc /* p {padding:0px; margin:0px;} The repository for Commuication subsystem Rqts. &#160;To be populated by a mission-specific team. */
                    #Group requirement <CmSub_1> 'Communication Subsystem Rqts Group' {
                        doc /* The Group provides the prefix and numbering scheme - which is easy to change. */
                        #SubsystemRequirement requirement <'CmSub_1.1'> 'Requirement Name' {
                            doc /* Shall statement */
                        }
                    }
                }
                package 'L3.1.4 Attitude Determination and Control Subsystem Rqts' {
                    doc /* p {padding:0px; margin:0px;} The repository for Attitude Determination and Control subsystem Rqts. &#160;To be populated by a mission-specific team. */
                    #Group requirement <AdSub_1> 'Attitude Determination and Control Subsystem Rqts Group' {
                        doc /* The Group provides the prefix and numbering scheme - which is easy to change. */
                        #SubsystemRequirement requirement <'AdSub_1.1'> 'Requirement Name' {
                            doc /* Shall statement */
                        }
                    }
                }
                package 'L3.1.5 Guidance Navigation and Control Subsystem Rqts' {
                    doc /* p {padding:0px; margin:0px;} The repository for Guidance Navigation and Control subsystem Rqts. &#160;To be populated by a mission-specific team. */
                    #Group requirement <GnSub_1> 'Guidance Navigation and  Control Subsystem Rqts Group' {
                        doc /* The Group provides the prefix and numbering scheme - which is easy to change. */
                        #SubsystemRequirement requirement <'GnSub_1.1'> 'Requirement Name' {
                            doc /* Shall statement */
                        }
                    }
                }
                package 'L3.1.6 Structures and Mechanisms Subsystem Rqts' {
                    doc /* p {padding:0px; margin:0px;} The repository for Structures and Mechanisms subsystem Rqts. &#160;To be populated by a mission-specific team. */
                    #Group requirement <SmSub_1> 'Structures and Mechanisms Subsystem Rqts Group' {
                        doc /* The Group provides the prefix and numbering scheme - which is easy to change. */
                        #SubsystemRequirement requirement <'SmSub_1.1'> 'Requirement Name' {
                            doc /* Shall statement */
                        }
                    }
                }
                package 'L3.1.7 Power Subsystem Rqts' {
                    doc /* p {padding:0px; margin:0px;} The repository for&#160;Power subsystem Rqts. &#160;To be populated by a mission-specific team. */
                    #Group requirement <PoSub_1> 'Power Subsystems Rqts Group' {
                        doc /* The Group provides the prefix and numbering scheme - which is easy to change. */
                        #SubsystemRequirement requirement <'PoSub_1.1'> 'Requirement Name' {
                            doc /* Shall statement */
                        }
                    }
                }
                package 'L3.1.8 Thermal Subsystem Rqts' {
                    doc /* p {padding:0px; margin:0px;} The repository for&#160;Thermal subsystem Rqts. &#160;To be populated by a mission-specific team. */
                    #Group requirement <ThSub_1> 'Thermal Subsystem Rqts Group' {
                        doc /* The Group provides the prefix and numbering scheme - which is easy to change. */
                        #SubsystemRequirement requirement <'ThSub_1.1'> 'Requirement Name' {
                            doc /* Shall statement */
                        }
                    }
                }
                package 'L3.1.9 Propulsion Subsystem Rqts' {
                    doc /* p {padding:0px; margin:0px;} The repository for Propulsion subsystem Rqts. &#160;To be populated by a mission-specific team. */
                    #Group requirement <PrSub_1> 'Propulsion Subsystem Rqts Group' {
                        doc /* The Group provides the prefix and numbering scheme - which is easy to change. */
                        #SubsystemRequirement requirement <'PrSub_1.1'> 'Requirement Name' {
                            doc /* Shall statement */
                        }
                    }
                }
            }
        }
        package 'L1 Mission Rqts' {
            doc /* p {padding:0px; margin:0px;} Repository for Enterprise Rqts. &#160;To be populated by a mission-specific team. */
        }
        package 'L5 CubeSat Deployer Interface Rqts' {
            doc /* p {padding:0px; margin:0px;} The design and development of the mission specific CubeSat must satisfy the Rqts for interfacing with a CubeSat Deployer. The CubeSat team must document incorporation and satisfaction of the interface Rqts. The design and development of the mission specific CubeSat must satisfy the requirements for interfacing with a CubeSat Deployer. The CubeSat team must document incorporation and satisfaction of the interface requirements. Typically, this would be a verification matrix that lists requirements with information such as id, description, source, verification method, verification status, and verification results. Typically, verification matrices are implemented with a spreadsheet. However, this verification information can be incorporated into attributes of a SysML requirement element and exported as a spreadsheet. So … the mission-specific team needs to determine how to document and populate these interface requirements. . These requirements use the DeployerInterfaceRequirement stereotype with the following properties: Id Name Text Source Document - CubeSat Deployer System interface specification Source Paragraph Satisfaction Status Satisfied By - The satisfy relationship is used to assert that a model element corresponding to the design or implementation satisfies a particular requirement. Verify Method - Verification methods include inspection, analysis, demonstration, and test. Verified By - The verify relationship is between a requirement and a test case or other model element that is used to verify the requirement is satisfied. These requirements are to be populated based on / extracted from The CubeSat Deployer System interface specification. For example: Cal Poly CubeSat Design Specification or NanoRacks Interface Design Document The interface requirement categories and Ids can modified as needed to be consistent with the interface specifications. Having CubeSat Deployer Systems provide SysML models that contain the interface requirements would be very beneficial and will be pursued. We have created SysML model of the Cal Poly CubeSat Design Specification, but it is not a Cal Poly product. CubeSat Deployer Interface Rqts - Population */
            #Group requirement <CubeDplr_1> General {
                doc /* Breaker */
                #DeployerRequirement requirement <'CubeDplr_1.1'> TBP {
                    doc /* To be populated */
                }
            }
            #Group requirement <CubeDplr_2> Mechanical {
                doc /* Breaker */
                #DeployerRequirement requirement <'CubeDplr_2.1'> Structure {
                    doc /* Breaker */
                    #DeployerRequirement requirement <'CubeDplr_2.1.1'> TBP {
                        doc /* To be populated */
                    }
                }
                #DeployerRequirement requirement <'CubeDplr_2.2'> Mass {
                    doc /* Breaker */
                    #DeployerRequirement requirement <'CubeDplr_2.2.1'> TBP {
                        doc /* To be populated */
                    }
                }
            }
            #Group requirement <CubeDplr_3> Electrical {
                doc /* Breaker */
                #DeployerRequirement requirement <'CubeDplr_3.1'> TBP {
                    doc /* To be populated */
                }
            }
            #Group requirement <CubeDplr_4> Environmental {
                doc /* Breaker */
                #DeployerRequirement requirement <'CubeDplr_4.1'> Thermal {
                    doc /* Breaker */
                    #DeployerRequirement requirement <'CubeDplr_4.1.1'> TBP {
                        doc /* To be populated */
                    }
                }
                #DeployerRequirement requirement <'CubeDplr_4.2'> Vibration {
                    doc /* Breaker */
                    #DeployerRequirement requirement <'CubeDplr_4.2.1'> TBP {
                        doc /* To be populated */
                    }
                }
            }
            #Group requirement <CubeDplr_6> Safety {
                doc /* Breaker */
                #DeployerRequirement requirement <'CubeDplr_6.1'> TBP {
                    doc /* To be populated */
                }
            }
            #Group requirement <CubeDplr_7> Deployment {
                doc /* Breaker */
                #DeployerRequirement requirement <'CubeDplr_7.1'> TBP {
                    doc /* To be populated */
                }
            }
            #Group requirement <CubeDplr_5> Materials {
                doc /* Breaker */
                #DeployerRequirement requirement <'CubeDplr_5.1'> TBP {
                    doc /* To be populated */
                }
            }
        }
    }
    package '2 - Technical Measures' {
        doc /* p {padding:0px; margin:0px;} Technical measures are an established set of measures based on the expectations and Rqts that are tracked and assessed to determine overall system effectiveness and stakeholder satisfaction. Stakeholders will likely describe their technical measures as text and captured in Technical Measure Specifications. &#160; Technical Measure Specifications have Traced To, Traced From, and Allocated To&#160;properties. They will communicate and negotiate these descriptions with engineers who will transform them into measures that can be tracked and assessed. Validation activities provide data to the technical measurement process that are used to assess how well the measures are either projected to meet, or are meeting, their stated value. */
        package '2.1 - Technical Measures - Specifications and Requirements - Population' {
            doc /* p {padding:0px; margin:0px;} A Technical Measure provides a stakeholder insight into the definition and development of a technical solution. Verification activities provide data to the technical measurement process that is used to assess how well the technical measure is either projected to meet, or is meeting, its stated value. Common terms for these measures are MOEs, MOPs, and TPMs &#160; MOEs are operational measures of success closely related to the achievement of the mission objective in the intended operational environment under a specified set of conditions. &#160; MOPs are measures that characterize physical or functional attributes relating to system operation, measured or estimated under specified testing and/or operational environment conditions. &#160; TPMs measure attributes of a system element to determine how well that element is satisfying, or expected to satisfy, a technical requirement. &#160; &#160; xxxx A Technical Measure is incorporated in to CubeSat Reference Model as a block value property based on the Technical Measure as specified by a stakeholder. A stakeholder is going to most likely “describe” their Technical Measure in a document. A stakeholder will communicate and negotiate their Technical Measure with the engineers and engineers will transform those descriptions into a value property. These stakeholder specified TMs are captured in the Technical Measures Specification package. MOPs are measures that characterize physical or functional attributes relating to system operation, measured or estimated under specified testing and/or operational environment conditions A Technical Measure provides a stakeholder insight into the definition and development of a technical solution. Verification activities provide data to the technical measurement process that is used to assess how well the technical measure is either projected to meet, or is meeting, its stated value. Common terms for these measures are: - MOE - Measure of Effectiveness - MOP - Measure of Performance - TPM - Technical Performance Measure - KPP - Key Performance Parameter xxxx Technical Measure Specifications have Traced To, Traced From, Allocated To properties. MOEs are operational measures of success closely related to the achievement of the mission objective in the intended operational environment under a specified set of conditions Double-click on a Technical Measure table and then click on Add New to add a new Technical Measure to the containment tree and to the table. Right click the new element in the table then left click Select in Containment Tree to navigate to the new element. TPMs measure attributes of a system element to determine how well that element is satisfying, or expected to satisfy, a technical requirement xxxx Allocated To: Block (Enterprise, Segment, Subsystem), if a qualitative Technical Measure xxxx Traced From: Block (Enterprise, Segment, Subsystem) Threshold _Value, if a quantitative Technical Measure KPPs are measures that are critical and failure to meet threshold performance will result in reevaluation of a technical solution and with the possibility of project termination. Technical Measures - Specifications and Requirements - Population A Technical Measure is incorporated in to CubeSat System Reference Model as a block value property based on the Technical Measure as specified by a stakeholder A stakeholder is going to most likely “describe” their Technical Measure in a document. A stakeholder will communicate and negotiate their Technical Measure with the engineers and engineers will transform the description into a value property, and methods for calculating the value property. The Technical Measures are captured in Technical Measures Specification packages and Technical Measurers Requirement packages. Technical Measures Specification package diagrams are used to establish the relationships of Specifications, Methods, and Requirements. The Technical Measures Methods document iis part of the model and can be edited within the model. It can be created externally and copy/pasted into a Technical Measure package diagram for populatiion into the containment tree. The Methods can be be incorporated into the Constraint block Constraints and Parameters compartments. Parametric diagrams show how the constraint properties are connected. */
            package '2.1.1 MOE' {
                doc /* Repository for MOEs */
                package '2.1.1.1 MOE Specifications' {
                    part def 'MoeA Specification' {
                        doc /* Technical measure description */
                        @moeSpecification { summary = "The system shall exhibit the property \"MOE Name\" that has a minimum of x and maximum of y,"; }
                    }
                    #moeSpecification part def 'MoeB Specification' {
                        doc /* Technical measure description */
                    }
                }
                package '2.1.1.2 MOE Requirements' {
                    #moeRequirement requirement <'1'> 'MoeA Requirement' {
                        doc /* Shall statement */
                    }
                    #moeRequirement requirement <'2'> 'MoeB Requirement' {
                        doc /* Shall statement */
                    }
                }
            }
            package '2.1.2 MOP' {
                doc /* p {padding:0px; margin:0px;} Repository for MOPs. */
                package '2.1.2.2 MOP Requirements' {
                    #mopRequirement requirement <'1'> 'MopA Requirement' {
                        doc /* Shall statement */
                    }
                    #mopRequirement requirement <'2'> 'MopB Requirement' {
                        doc /* Shall statement */
                    }
                }
                package '2.1.2.1 MOP Specifications' {
                    #mopSpecification part def 'MopA Specification' {
                        doc /* Technical measure description */
                    }
                    #mopSpecification part def 'MopB Specification' {
                        doc /* Technical measure description */
                    }
                }
            }
            package '2.1.3 TPM' {
                doc /* p {padding:0px; margin:0px;} Repository for TPMs */
                package '2.1.3.1 TPM Specifications' {
                    #tpmSpecification part def 'TpmA Specification' {
                        doc /* Technical measure description */
                    }
                    #tpmSpecification part def 'TpmB Specification' {
                        doc /* Technical measure description */
                    }
                }
                package '2.1.3.2 TPM Requirements' {
                    #tpmRequirement requirement <'1'> 'TpmA Requirement' {
                        doc /* Shall statement */
                    }
                    #tpmRequirement requirement <'2'> 'TpmB Requirement' {
                        doc /* Shall statement */
                    }
                }
            }
            package '2.1.4 KPP' {
                package '2.1.4.1 KPP Specifications' {
                    #kppSpecification part def 'KppA Specification' {
                        doc /* Technical measure description */
                    }
                    #kppSpecification part def 'KppB Specification' {
                        doc /* Technical measure description */
                    }
                }
                package '2.1.4.2 KPP Requirements' {
                    #kppRequirement requirement <'1'> 'KppA Requirement' {
                        doc /* Shall statement */
                    }
                    #kppRequirement requirement <'2'> 'KppB Requirement' {
                        doc /* Shall statement */
                    }
                }
                #kppSpecification part def 'KppB Spedification' {
                }
            }
        }
    }
    package '3 - Behaviors' {
        doc /* p {padding:0px; margin:0px;} Behaviors describe the functionality of a system in terms of how it is used to achieve the goals of its various users. The behaviors are the concepts of operations and operation concepts. A behavior can be specified by a Use Case description, a Use Case diagram, or an Activity diagram. The Behavior architecture levels are Enterprise, CubeSat, Ground System, CubeSat Subsystems, and Ground Subsystems. Behavior Architectures and Population */
        package '3.1 Behaviors - Use Cases - Activities - Population' {
            doc /* p {padding:0px; margin:0px;} This package provides artifacts for establishing a relationship between a requirement and a behavior that refines the requirement. The behavior can be: Expressed a by text-based Use Case Description. Captured in a Use Case Diagram Refined by an Activity Diagram. A Use Case Description can be simple narrative or have a more detailed format such as presented in our 2017 IEEE Aerospace paper: Use Case Name, Scope, Primary Actor, Supporting Actor &#160;&#160;&#160;&#160;&#160; Stakeholder, Precondition, Trigger, Postconditions At each level there are: Behavior packages containing Use Case Description and their listing table Use Case packages containing Use Cases Diagrams and their listing table Activity packages containing Activity Diagrams and their listing table At each level there are: &#160;Behavior packages containing Use Case Description documents and their listing table &#160;Use Case packages containing Use Cases Diagrams and their listing table &#160;Activity packages containing Activity Diagrams and their listing table The package provides artifacts for establishing a relationship between a requirement and a behavior that refines the requirement. The behavior can be: Expressed a by text-baed Behavior Description. Captured in a Use Case Diagram Refined by an Activity Diagram. A Behavior Description can be simple narrative or have a more detailed format such as presented in our 2017 IEEE Aerospace paper: Use Case Name Scope Primary Actor Supporting Actor Stakeholder Precondition Trigger Postconditions At each level there are: Behavior packages containing Behavior Description and their listing table Use Case packages containing Use Cases Diagrams and their listing table Activity packages containing Activity Diagrams and their listing table As presented here, the CSRM has an example of population and relationships of requirements, behaviors, use cases, and activities. They are only examples. Mission modelers can populate and establish relationships to best serve their missions. To navigate to a package: Right click on package icon Scroll down to Selct in Containment Tree To open table: Double left click on table icon Behaviors - Use Cases - Activities - Population */
        }
    }
    package '6 - Validation Verification' {
        doc /* p {padding:0px; margin:0px;} The verification activity element can be populated to describe the process for verifying an element, e.g. a requirement. For example, the process could include verification plans, procedures, execution, results, and status. The validation activity element can be populated to describe the process for validating an element, e.g. a Technical Measure or a Mission Objective */
        package '6.1 - Validation Activities' {
            doc /* p {padding:0px; margin:0px;} Repository for validation activities. Instructions for adding a new Validation Activity Double-click on Activities table and then click on Add New to add a new Activity to the containment tree and to the table. Right click the new element in the table then left click Select in Containment Tree to navigate to the new element. Validation confirms, by providing objective evidence, that the system, as-built (or as it will be built), satisfies the stakeholders’ needs, objectives, and moes. That is, the right system has been (or will be) built. Instructions for establishing a relationship between a Technical Measure and a Validation Activity Open the Validation Activities Table Add a new Validation Activity or locate an existing one Either: Double click in the Validated By cell of the Technical Measure element to reveal three ellipses. Click on the ellipses. Search for the applicable Validation Activity. Click on the Plus Sign to move the Validation Activity from the List Tab to the Selected Elements column. Click on OK to populate the ValidatedBy cell of the Technical Measure element. Or: Double click in the Validates cell of the Validation Activity element to reveal three ellipses. Click on the ellipses. Search for the applicable Technical Measure. Click on the Plus Sign to move the Technical Measure from the List Tab to the Selected Elements column. Click on OK to populate the Validates cell of the Validation Activity element. Validation Activites - Population */
            #ValidationActivity verification def 'Validation Activity 1';
            #ValidationActivity verification def 'Validation Activity 2';
        }
        package '6.2 - Verification Activities' {
            doc /* p {padding:0px; margin:0px;} Repository for verification activities. Instructions for adding a new Verification Activity Double-click on the Activities table and then click on Add New to add a new Activity to the containment tree and to the table. Right click the new element in the table then left click Select in Containment Tree to navigate to the new element. Verification confirms, by providing objective evidence, that the system and all its elements perform their intended functions and satisfy the requirements allocated to them. That is, the system has been built right. Instructions for establishing a relationship between a Requirement and a Verification Activity Open Verification Activities Table below. Add a new Verification Activity or locate an existing one. Either Double click in the VerifiedBy cell of the Requirement element to reveal three ellipses. Click on the ellipses. Search for the applicable Verification Activity. Click on the Plus Sign to move the Verification Activity from the List Tab to the Selected Elements column. Click on OK to populate the VerifiedBy cell of the Requirement element Or Double click in the Verifies cell of the Verification Activity element to reveal three ellipses. Click on the ellipses. Search for the applicable Requirement. Click on the Plus Sign to move the Requirement from the List Tab to the Selected Elements column. Click on OK to populate the Verifies cell of the Verification Activity element. Verification Activities - Population */
            #VerificationActivity verification def 'Verification Activity 1';
            #VerificationActivity verification def 'Verification Activity 2';
        }
    }
    package '0 - CSRM Overview and Navigation' {
        doc /* p {padding:0px; margin:0px;} CSRM landing overview and navigation package */
        #Explanation comment about '01 - CubeSat System Reference Model' /* This package contains the CSRM core. Additoinally, there are links to the examples and illustrations. You are free to use the elements or delete them if they do not apply to your design. */
        #Explanation comment about '01 - CubeSat System Reference Model', '02 - CSRM Elements, Examples and Illustrations' /* This package contains CSRM examples and illustrations. This is provided to aid in development and to explain how to use the CSRM. Be careful to not use the elements in this package as part of your design. We suggest copying any element to the primary model. This section should be removed when not required for reference. */
        #Explanation comment about 'Derived Properties' /* This package is used by the Dassault Systems tool to add properties used in Tables. */
        #Explanation comment about 'Derived Properties', 'Unit Imports' /* This package is used by the Dassault Systems tool. */
        #Explanation comment about 'Derived Properties', 'Unit Imports', 'CSRM Extentions' /* This package contains the extentions used by the CSRM. */
        #Explanation comment about 'Derived Properties', 'Unit Imports' /* This package contains the glossary terms and acronyms used by the CSRM. */
    }
    package '7 - CSRM Population' {
        doc /* p {padding:0px; margin:0px;} CSRM&#160;elements to be populated by missoin team */
        package '7.1 - CSRM Population' {
            doc /* Each population package contains the associated CSRM elements and tables residing in the containment tree. &#160;&#160;&#160;The tables are used to add, delete, and modify the individual elements and to establish relationships between the elements. */
        }
    }
}
package '02 - CSRM Elements, Examples and Illustrations' {
    private import 'CSRM Profile'::*;
    private import RequirementDerivation::*;
    doc /* This package is used to segragate examples and population diagrams from the core of CSRM. */
    package '1 - Stakeholders' {
        doc /* Stakeholder Examples and Illustrations */
        package '1.1 Regulatory Agency Stakeholders' {
            package '1.1.1 - Regulatory Agency Stakeholders - Examples' {
                doc /* p {padding:0px; margin:0px;} A mission specific team will add Regulatory Agencies Stakeholders as applicable. */
                #Stakeholder part def '18th Space Control Squadron' {
                    doc /* 18th Space Control Squadron (18SPCS) provides the capability to register a satellite with 18SPCS in support of identification, tracking, and conjunction services. */
                }
                #Stakeholder part def 'FAA Commercial Space Transportation' {
                }
                #Stakeholder part def 'Federal Communications Commission (FCC)' {
                    doc /* Non-federal users apply for spectrum certification through the Federal Communication Commission (FCC). The FCC maintains one integrated policy and position on spectrum when representing the United States internationally with respect to the International Telecommunication Union- Radiocommunication Sector (ITU-R) and World Radio Conferences (WRC). */
                }
                #Stakeholder part def 'International Amateur Radio Union (IARU)' {
                    doc /* An international confederation of national amateur radio organizations that works closely with ITU to allocate frequency spectrum to amateur radio and amateur-radio satellite services. */
                }
                #Stakeholder part def 'International Telecommunication Union - Radiocommunication Sector (ITU-R)' {
                    doc /* An international confederation of national amateur radio organizations that works closely with ITU to allocate frequency spectrum to amateur radio and amateur-radio satellite services. */
                }
                #Stakeholder part def 'International Traffic in Arm Regulation (ITAR)' {
                }
                #Stakeholder part def 'Laser Clearinghouse (LCH)' {
                }
                #Stakeholder part def 'NASA Orbital Debris Program Office' {
                    doc /* U.S. Government orbital debris mitigation standard practices. NASA Orbital Debris Program Office - glossary description U.S. Government orbital debris mitigation standard practices. */
                }
                #Stakeholder part def 'NASA Spectrum Guidance for Small Satellite Missions' {
                    doc /* The Spectrum Guidance document, applicable to all NASA small satellite missions (orbiting systems < 180 kg), provides spectrum policy and process guidance for NASA small satellite missions requiring the use of the electromagnetic spectrum for transmission, reception, or both.. NASA Spectrum Guidance for Small Satellite Missions - glossary description */
                }
                #Stakeholder part def 'NOAA Commercial Remote Sensing Regulatory Affairs Office' {
                    doc /* U.S. laws, regulations, policies, and related information pertaining to the operation of private and commercial remote sensing satellite systems. NOAA Commercial Remote Sensing Regulatory Affairs Office - glossary description */
                }
                #Stakeholder part def 'Space-Track' {
                    doc /* Space-Track.org promotes space flight safety, protection of the space environment and the peaceful use of space worldwide by sharing space situational awareness services and information. with U.S. and international satellite owners/operators, academia and other entities. Services include Launch Conjunction Assessment, Launch Early Orbit Determination, Early Orbit Conjunction Assessment, Advanced Conjunction Assessment (On-Orbit), Advance Collision Avoidance (On-Orbit), Disposal/End-of-Life Support, Deorbit and Reentry Support. */
                }
                #Stakeholder part def 'United Nations Office for Outer Space Affairs (UNOOSA)' {
                }
            }
        }
        package '1.2 Mission Stakeholders' {
            package '1.2.1 - Mission Stakeholders - Examples' {
                doc /* A mission specific team will add Mission Stakeholders as applicable. */
                #Stakeholder part def Tester {
                    doc /* An individual or group responsible for the verification and validation processes. Verification is the confirmation, through the provision of objective evidence, that specified Rqts have been fulfilled. Validation is the confirmation, through the provision of objective evidence, that the Rqts for a specified intented use in the intended operational environment have been fulfilled. */
                }
                #Stakeholder part def Supplier {
                    doc /* An individual or organization that enters into an agreement with the acquirer for the supply of a product or service. [1/ App. C] */
                }
                #Stakeholder part def Sponsor {
                    doc /* An individual or organization that provides funding. */
                }
                #Stakeholder part def 'Satellite Tracking Service' {
                }
                #Stakeholder part def 'Satellite Shipping Service' {
                }
                #Stakeholder part def 'Project Manager' {
                    doc /* The indivdual responsible for managing project attributes including project plans; estimates; schedule; budget; project structure; staffing; resources; infrastructure; and risk factors. [7/ Pg. 834] */
                }
                #Stakeholder part def 'Project Engineer' {
                    doc /* The individual responsible for managing product attributes including items such as Rqts allocation and flow-down; system architecture; structure of and interactions among technical teams; specialty engineering; integration; verification; and validation. [7/ Pg. 834] */
                }
                #Stakeholder part def 'Mission Engineer' {
                    doc /* The individual responsible for specifying mission data collection and analysis that fulfills the needs and objectives of the stakeholders. Data collection is specified by Rqts, constraints, quality, and quantity. */
                }
                #Stakeholder part def 'Launch Provider' {
                }
                #Stakeholder part def 'Launch Operator' {
                }
                #Stakeholder part def 'Launch Integrator' {
                }
                #Stakeholder part def Integrator {
                }
                #Stakeholder part def 'End User' {
                }
                #Stakeholder part def 'Chief Scientist' {
                }
                #Stakeholder part def Developer {
                    doc /* An individual or group responsible for the development process. The development process creates or fabricates a system element confirming to that element's detailed description (Rqts, architecture, design, interfaces). [1/ Para. 4.7] */
                }
                #Stakeholder part def Acquirer {
                    doc /* An individual or organization that acquires a product or service from a supplier. [1/ App. C] */
                }
                #Stakeholder part def 'Development Facility Guidelines Regulations Policies' {
                }
                #Stakeholder part def Operator {
                    doc /* An individual who contributes to the functionality of a system and draws on knowledge, skills, and procedures to contribute the function. [1/ App. C] */
                }
            }
            package '1.2.2 - Mission Stakeholders - Requirements, Technical Measures, Use Cases - Illustration' {
                doc /* p {padding:0px; margin:0px;} The CubeSat System Reference Model has model elements for: &#160;- stakeholder(s), concern(s) &#160;- mission need(s), mission objective(s), mission constraint(s) &#160;- mission requirement(s) These model elements and their relationships are mission and engineering methodology specific. The mission and methodology may dictate starting with stakeholder concerns. Or starting with mission objectives and mission constraints. Or a simpler approach of starting with just mission Rqts. &#160; This terminology is consistent with a number of well established and accepted references. &#160;The user of the CSRM should establish terminology (and then model elements) as needed for their stakeholders and mission. &#160; The CSRM provides a library of model elements but does not dictate what model elements and relationships to use A stakeholder concern can be manifest in many forms, such as in relation to one or more stakeholder needs, goals, expectations, responsibilities, requirements, design constraints, assumptions, dependencies, quality attributes, architecture decisions, risks or other issues pertaining to the system. There can be a number of stakeholders and a number of concerns. The needs, objectives, constraints, and requirements result from review, assessment, and integration of the varied concerns. The CubeSat System Reference Model has model elements for: - stakeholder(s), concern(s) - mission need(s), mission objective(s), mission constraint(s) - mission requirement(s) These model elements and their relationships are mission and engineering methodology specific. The mission and methodology may dictate starting with stakeholder concerns Or starting with mission objectives and mission constraints Or a simpler approach of starting with just mission requirements This terminology is consistent with a number of well established and accepted references. The user of the CSRM should establish terminology (and then model elements) as needed for their stakeholders and mission. . The CSRM provides a library of model elements but does not dictate what model elements and relationships to use MoeSpecification, MopSpecification, and TpmSpecification stereotypes have been created for the CSRM StakeholderConcern, MissionNeed, MissionObjective, MissionConstraint, and MissionRequirement stereotypes have been created for the CSRM Technical Measures are based on the expectations and requirements that are assessed to determine system effectiveness and stakeholder satisfaction. Use Cases describes the functionality of a system in terms of how it is used to achieve the goals of its various users. p {padding:0px; margin:0px;} Use of Derive Relationship Derived requirements generally correspond to requirements at the next level of the system hierarchy. A simple example would be a vehicle acceleration requirement that is analyzed to derive requirements for engine power, etc. A rrow points from derived retirement to source requirement It is also used to represent a relationship between requirements at the same level of the hierarchy but at different levels of abstraction. For example, the hardware or software requirements that are originally specified by the systems engineering team may be analyzed by the hardware or software team to derive more detailed requirements that reflect additional implementation considerations or constraints. The more detailed requirements from the hardware or the software team may be related to the original requirements, specified by the system team, through derive relationships. Mission Stakeholders - Requirements, Technical Measures, Use Cases - Illustration A refine relationship reduces ambiguity in an element. The arrow points from the element with the more detailed representation to the elememt that is being refined. Derive relationship. Arrow points to the source requirement. The relationship between a derived requirement and source requirement is intended to be based on analysis The relationships between elements are captured in the element specifications and containment tree. Those relationships are displayed and maintained in diagrams and tables as shown below */
                #MissionConstraint requirement <'4'> 'Mission Constraint Name' {
                }
                #SegmentRequirement requirement <'6'> 'Segment Requirement Name' {
                }
                #SubsystemRequirement requirement <'7'> 'Subsystem Requirement Name' {
                }
                #moeSpecification part def 'Measure of Effectiveness Name' {
                }
                #mopSpecification part def 'Measure of Performance Name' {
                }
                #tpmSpecification part def 'Technical Performance Measure Name' {
                }
                #MissionRequirement requirement <'5'> 'Mission Requirement Name' {
                }
                use case def 'Mission Use Case';
                use case def 'Segment Use Case';
                use case def 'Subsystem Use Case';
                #Stakeholder part def 'Stakeholder Name' {
                }
                #StakeholderConcern requirement <'1'> 'Stakeholder Concern Name' {
                }
                #MissionNeed requirement <'2'> 'Mission Need Name' {
                }
                #MissionObjective requirement <'3'> 'Mission Objective Name' {
                }
            }
        }
    }
    package '2 - Technical Measures' {
    }
    package '3 - Behaviors' {
    }
    package '5 - Architecture' {
    }
    package '4 - Requirememts' {
    }
    package '6 - Validation Verification' {
    }
    package '7 - CSRM Population' {
        doc /* p {padding:0px; margin:0px;} Package containing an illustration of the CSRM elements along with CSRM element population package diagrams . */
        package '7.2 - CSRM Elements' {
            doc /* Select Architectural Element Select Edit Compartments Select Element Properties Select Part Move from Hidden to Selected Select Architectural Element Select Part property Select Directed Composition Drag to Part element Set font size Select Element Select Symbol Properties Select Font Select Ellipses Select 14 Select Show Stereotypes Select Text, or ..... A Technical Measure Specification captures the descriptions of technical measures in textual form. Stakeholders will likely describe their technical measures as text. They will communicate and negotiate these descriptions with engineers who will transform them into measures that can be tracked and assessed The Technical Measure is specified as a value property of an enterprise, segment or subsystem element.. The CSRM is a logical model consisting of model elements and diagrams. Shown below are CSRM elements and example element properties. The Mission-specific CubeSat Model (MCM) is based on the CSRM. The MCM provide the basis for design and development of the mission-specific CubeSat. The mission team identifies the systems engineering methodology to be followed and then updates the MCM organization, elements, element properties, relationships, and diagrams as follows: 1) Determine if the CSRM elements are necessary and sufficient. If not, modify accordingly. 2) Identify stakeholders and stakeholder terminology such as concerns, needs, objectives, and constraints, as they relate to establishing mission requirements. 3) Establish the relationships between use cases, technical measures, and space and ground segment and subsystems requirements. These relationships can be exhibited in model artifacts such as requirement tables, requirement diagrams, and dependency matrices. 4) Identify the model artifacts that are needed such as for: stakeholder buy-off, internal and external design reviews, and design specifications. A Behavior can be specified by a Behavior description, a Use Case diagram, or an Activity diagram The validation process can be captured in a: 1) Validation Activity element properties, or 2) Validation Activity Diagram, or 3) Validation Activity Word document Select CSRM Elements Select Create Element Select Element Select Properties Select Element Select Edit Compartments Select Element Properties Select form Hidden and move to Selected Populate element properties Select element Select specification Select a property Select "emptyt box" to reveal eipses Select ellipses and depending on the property enter text or use the search function to locate and populate relational element */
            #Subsystem part def Subsystem {
                part component : '02 - CSRM Elements, Examples and Illustrations'::'7 - CSRM Population'::'7.2 - CSRM Elements'::Component;
            }
            #Component part def Component {
            }
            #Segment part def Segment {
                part cubeSat : '02 - CSRM Elements, Examples and Illustrations'::'7 - CSRM Population'::'7.2 - CSRM Elements'::CubeSat;
            }
            #CubeSat part def CubeSat {
                part subsystem : '02 - CSRM Elements, Examples and Illustrations'::'7 - CSRM Population'::'7.2 - CSRM Elements'::Subsystem;
            }
            #StakeholderConcern requirement <'11'> 'Stakeholder Concern' {
            }
            #MissionObjective requirement <'13'> 'Mission Objective' {
            }
            #MissionNeed requirement <'15'> 'Mission Need' {
            }
            #MissionConstraint requirement <'16'> 'Mission Constraint' {
            }
            #MissionRequirement requirement <'17'> 'Mission Requirement' {
            }
            #CubeSatRequirement requirement <'18'> 'CubeSat Requirement' {
            }
            #GroundSegmentRequirement requirement <'19'> 'Ground Segment Requirement' {
            }
            #SubsystemRequirement requirement <'20'> 'Subsystem Requirement' {
            }
            #ComponentRequirement requirement <'21'> 'Component Requirement' {
            }
            #DeployerRequirement requirement <'22'> 'Deployer Interface Requirement' {
            }
            #moeSpecification part def 'MOE Specification' {
            }
            #mopSpecification part def 'MOP Specification' {
            }
            #tpmSpecification part def 'TPM Specification' {
            }
            part def Stakeholder;
            part def Enterprise {
                part segment : '02 - CSRM Elements, Examples and Illustrations'::'7 - CSRM Population'::'7.2 - CSRM Elements'::Segment;
            }
            part def Domain {
                part enterprise : '02 - CSRM Elements, Examples and Illustrations'::'7 - CSRM Population'::'7.2 - CSRM Elements'::Enterprise;
            }
            #ValidationActivity action def 'Verification Activity';
            #ValidationActivity action def 'Validation Activity';
            #Facility part def Facility {
                part equipment : '02 - CSRM Elements, Examples and Illustrations'::'7 - CSRM Population'::'7.2 - CSRM Elements'::Equipment;
            }
            #Equipment part def Equipment {
            }
            part def 'KPP Specification' {
            }
            part def 'MOE Requirement' {
            }
            part def 'MOP Requrement' {
            }
            part def 'TPM Requirement' {
            }
            part def 'KPP Requirement' {
            }
            package Behaviors {
            }
            package Activities {
                action def Activities;
            }
            package 'Use Cases' {
                use case def 'Use Cases';
            }
        }
    }
    package '0 - Examples and Illustrations' {
    }
}
package '00 - CSRM Start Here' {
    private import 'CSRM Profile'::*;
    private import RequirementDerivation::*;
    doc /* p {padding:0px; margin:0px;} CubeSat System Reference Model by INCOSE Space Systems Working Group (SSWG) and OMG Space Domain Task Force (SDTF) is licensed under Attribution 4.0 International CC LINK */
    comment /* The CSRM Profile contains the sub-profiles of the CubeSat System Reference Model (CSRM) Profile. The purpose of extensions is to add metadata, aid in dynamic reporting/analysis, validate a model's composition, and aid in grouping. */
    package 'CSRM Profile Diagrams' {
    }
}
package 'CSRM Root' {
    private import 'CSRM Profile'::*;
    private import 'Unit Imports'::'Basic Units'::'Basic Amount of Substance'::*;
    private import 'Unit Imports'::'Basic Units'::'Basic Acceleration'::*;
    private import 'Unit Imports'::'Basic Units'::'Basic Amount of Substance Concentration'::*;
    private import 'Unit Imports'::'Basic Units'::'Basic Area'::*;
    private import 'Unit Imports'::'Basic Units'::'Basic Electric Current'::*;
    private import 'Unit Imports'::'Basic Units'::'Basic Electric Current Density'::*;
    private import 'Unit Imports'::'Basic Units'::'Basic Length'::*;
    private import 'Unit Imports'::'Basic Units'::'Basic Luminance'::*;
    private import 'Unit Imports'::'Basic Units'::'Basic Luminous Intensity'::*;
    private import 'Unit Imports'::'Basic Units'::'Basic Magnetic Field Strength'::*;
    private import 'Unit Imports'::'Basic Units'::'Basic Mass'::*;
    private import 'Unit Imports'::'Basic Units'::'Basic Speed and Velocity'::*;
    private import 'Unit Imports'::'Basic Units'::'Basic Mass Density'::*;
    private import 'Unit Imports'::'Basic Units'::'Basic Time'::*;
    private import 'Unit Imports'::'Basic Units'::'Basic Thermodynamic Temperature'::*;
    private import 'Unit Imports'::'Basic Units'::'Basic Volume'::*;
}

package 'CSRM Relationships' {
    private import 'CSRM Profile'::*;
    private import RequirementDerivation::*;
    dependency from '01 - CubeSat System Reference Model'::'1 - Stakeholders'::'1.2 Mission Stakeholders'::'1.2.4 - Mission Objectives'::'Mission Objectives Table' to '01 - CubeSat System Reference Model'::'1 - Stakeholders'::'1.2 Mission Stakeholders'::'1.2.1 - Mission Stakeholders'::'Mission Stakeholders Table';
    #Trace dependency from '01 - CubeSat System Reference Model'::'1 - Stakeholders'::'1.2 Mission Stakeholders'::'1.2.2 - Mission Stakeholder Concerns'::'Mission Stakeholder Concerns'::'Mission Stakeholder A Concern 1' to '01 - CubeSat System Reference Model'::'1 - Stakeholders'::'1.2 Mission Stakeholders'::'1.2.1 - Mission Stakeholders'::'Mission Stakeholder A';
    #Trace dependency from '01 - CubeSat System Reference Model'::'1 - Stakeholders'::'1.2 Mission Stakeholders'::'1.2.2 - Mission Stakeholder Concerns'::'Mission Stakeholder Concerns'::'Mission Stakeholder A Concern 1' to '01 - CubeSat System Reference Model'::'1 - Stakeholders'::'1.2 Mission Stakeholders'::'1.2.6 - Mission Rqts'::'Mission Rqts Group'::'Requirement Name';
    #Refine dependency from '01 - CubeSat System Reference Model'::'5 - Architecture'::L3_Subsystems::'L3.1_CubeSat Subsystems'::'L3.1.1_Behaviors'::'L3.1.1.1_CubeSat Subsystems Behaviors'::'CubeSat Subsystem Behavior A' to '01 - CubeSat System Reference Model'::'4 - Requirements'::'L3 Subsystem Rqts'::'L3.1 CubeSat Subsystems Rqts'::'L3.1.1 Mission Payload Rqts'::'Mission Payload Rqts Group'::'Requirement Name';
    #Refine dependency from '01 - CubeSat System Reference Model'::'5 - Architecture'::L3_Subsystems::'L3.1_CubeSat Subsystems'::'L3.1.1_Behaviors'::'L3.1.1.3_CubeSat Subsystems Activities'::'CubeSat Subsystem Activity A' to '01 - CubeSat System Reference Model'::'5 - Architecture'::L3_Subsystems::'L3.1_CubeSat Subsystems'::'L3.1.1_Behaviors'::'L3.1.1.2_CubeSat Subsystems Use Cases'::'CubeSat Subsystem Use Case A';
    #Refine dependency from '01 - CubeSat System Reference Model'::'5 - Architecture'::L3_Subsystems::'L3.1_CubeSat Subsystems'::'L3.1.1_Behaviors'::'L3.1.1.2_CubeSat Subsystems Use Cases'::'CubeSat Subsystem Use Case A' to '01 - CubeSat System Reference Model'::'5 - Architecture'::L3_Subsystems::'L3.1_CubeSat Subsystems'::'L3.1.1_Behaviors'::'L3.1.1.1_CubeSat Subsystems Behaviors'::'CubeSat Subsystem Behavior A';
    #Refine dependency from '01 - CubeSat System Reference Model'::'5 - Architecture'::L3_Subsystems::'L3.2_Ground Subsystems'::'L3.2.1_Behaviors'::'L3.2.1.1_Ground Subsystems Behaviors'::'Ground Subsystems Behavior A' to '01 - CubeSat System Reference Model'::'4 - Requirements'::'L3 Subsystem Rqts'::'L3.2 Ground Subsystems Rqts'::'L3.2.1 Plan and Schedule Subsystem Rqts'::'Plan and Schedule Subsystem Rqts Group'::'Plan and Schedule Requirement A';
    #Refine dependency from '01 - CubeSat System Reference Model'::'5 - Architecture'::L3_Subsystems::'L3.2_Ground Subsystems'::'L3.2.1_Behaviors'::'L3.2.1.3_Ground Subsystems Activities'::'Ground Subsystem Activity A' to '01 - CubeSat System Reference Model'::'5 - Architecture'::L3_Subsystems::'L3.2_Ground Subsystems'::'L3.2.1_Behaviors'::'L3.2.1.2_Ground Subsystems Use Cases'::'Ground Subsystem Use Case A';
    #Refine dependency from '01 - CubeSat System Reference Model'::'5 - Architecture'::L3_Subsystems::'L3.2_Ground Subsystems'::'L3.2.1_Behaviors'::'L3.2.1.2_Ground Subsystems Use Cases'::'Ground Subsystem Use Case A' to '01 - CubeSat System Reference Model'::'5 - Architecture'::L3_Subsystems::'L3.2_Ground Subsystems'::'L3.2.1_Behaviors'::'L3.2.1.1_Ground Subsystems Behaviors'::'Ground Subsystems Behavior A';
    #Refine dependency from '01 - CubeSat System Reference Model'::'5 - Architecture'::L2_Segment::'L2.2_Ground Segment'::'L2.2.1_Behaviors'::'L2.2.1.1_Ground Segment Behaviors'::'Ground Segment Behavior A' to '01 - CubeSat System Reference Model'::'4 - Requirements'::'L2 Segment Rqts'::'L2.2 Ground Segment Rqts'::'Ground Segment Rqts Group'::'Ground Segment Requirement A';
    #Refine dependency from '01 - CubeSat System Reference Model'::'5 - Architecture'::L2_Segment::'L2.2_Ground Segment'::'L2.2.1_Behaviors'::'L2.2.1.2_Ground Segment Use Cases'::'Ground Segment Use Case A' to '01 - CubeSat System Reference Model'::'5 - Architecture'::L2_Segment::'L2.2_Ground Segment'::'L2.2.1_Behaviors'::'L2.2.1.1_Ground Segment Behaviors'::'Ground Segment Behavior A';
    #Refine dependency from '01 - CubeSat System Reference Model'::'5 - Architecture'::L2_Segment::'L2.2_Ground Segment'::'L2.2.1_Behaviors'::'L2.2.1.3_Ground Segment Activities'::'Ground Segment Activity A' to '01 - CubeSat System Reference Model'::'5 - Architecture'::L2_Segment::'L2.2_Ground Segment'::'L2.2.1_Behaviors'::'L2.2.1.2_Ground Segment Use Cases'::'Ground Segment Use Case A';
    #Refine dependency from '01 - CubeSat System Reference Model'::'5 - Architecture'::L2_Segment::'L2.1_Space Segment'::'L2.1.1_Behaviors'::'L2.1.1.1_CubeSat Behaviors'::'CubeSat Behavior A' to '01 - CubeSat System Reference Model'::'4 - Requirements'::'L2 Segment Rqts'::'L2.1 Space Segment Rqts'::'L2.1.1 CubeSat Rqts'::'CubeSat Rqts Group'::'Requirement Name';
    #Refine dependency from '01 - CubeSat System Reference Model'::'5 - Architecture'::L2_Segment::'L2.1_Space Segment'::'L2.1.1_Behaviors'::'L2.1.1.3_CubeSat Activities'::'CubeSat Activity A' to '01 - CubeSat System Reference Model'::'5 - Architecture'::L2_Segment::'L2.1_Space Segment'::'L2.1.1_Behaviors'::'L2.1.1.2_CubeSat Use Cases'::'CubeSat Use Case A';
    #Refine dependency from '01 - CubeSat System Reference Model'::'5 - Architecture'::L2_Segment::'L2.1_Space Segment'::'L2.1.1_Behaviors'::'L2.1.1.2_CubeSat Use Cases'::'CubeSat Use Case A' to '01 - CubeSat System Reference Model'::'5 - Architecture'::L2_Segment::'L2.1_Space Segment'::'L2.1.1_Behaviors'::'L2.1.1.1_CubeSat Behaviors'::'CubeSat Behavior A';
    #Refine dependency from '01 - CubeSat System Reference Model'::'5 - Architecture'::L1_Enterprise::'L1.1_Behaviors'::'L1.1.1_Enterprise Behaviors'::'Enterprise Behavior A' to '01 - CubeSat System Reference Model'::'1 - Stakeholders'::'1.2 Mission Stakeholders'::'1.2.6 - Mission Rqts'::'Mission Rqts Group'::'Requirement Name';
    #Refine dependency from '01 - CubeSat System Reference Model'::'5 - Architecture'::L1_Enterprise::'L1.1_Behaviors'::'L1.1.3_Enterprise Activities'::'Enterprise Activity A' to '01 - CubeSat System Reference Model'::'5 - Architecture'::L1_Enterprise::'L1.1_Behaviors'::'L1.1.2_Enterprise Use Cases'::'Enterprise Use Case A';
    #Refine dependency from '01 - CubeSat System Reference Model'::'5 - Architecture'::L1_Enterprise::'L1.1_Behaviors'::'L1.1.2_Enterprise Use Cases'::'Enterprise Use Case A' to '01 - CubeSat System Reference Model'::'5 - Architecture'::L1_Enterprise::'L1.1_Behaviors'::'L1.1.1_Enterprise Behaviors'::'Enterprise Behavior A';
    #Refine dependency from '01 - CubeSat System Reference Model'::'2 - Technical Measures'::'2.1 - Technical Measures - Specifications and Requirements - Population'::'2.1.1 MOE'::'2.1.1.1 MOE Specifications'::'MoeA Specification' to '01 - CubeSat System Reference Model'::'2 - Technical Measures'::'2.1 - Technical Measures - Specifications and Requirements - Population'::'2.1.1 MOE'::'2.1.1.2 MOE Requirements'::'MoeA Requirement';
    #Refine dependency from '01 - CubeSat System Reference Model'::'2 - Technical Measures'::'2.1 - Technical Measures - Specifications and Requirements - Population'::'2.1.1 MOE'::'2.1.1.1 MOE Specifications'::'MoeB Specification' to '01 - CubeSat System Reference Model'::'2 - Technical Measures'::'2.1 - Technical Measures - Specifications and Requirements - Population'::'2.1.1 MOE'::'2.1.1.2 MOE Requirements'::'MoeB Requirement';
    #Refine dependency from '01 - CubeSat System Reference Model'::'2 - Technical Measures'::'2.1 - Technical Measures - Specifications and Requirements - Population'::'2.1.1 MOE'::'2.1.1.1 MOE Specifications'::'MoeA Specification' to '01 - CubeSat System Reference Model'::'2 - Technical Measures'::'2.1 - Technical Measures - Specifications and Requirements - Population'::'2.1.1 MOE'::'2.1.1.2 MOE Requirements'::'MoeA Requirement';
    #Refine dependency from '01 - CubeSat System Reference Model'::'2 - Technical Measures'::'2.1 - Technical Measures - Specifications and Requirements - Population'::'2.1.1 MOE'::'2.1.1.1 MOE Specifications'::'MoeB Specification' to '01 - CubeSat System Reference Model'::'2 - Technical Measures'::'2.1 - Technical Measures - Specifications and Requirements - Population'::'2.1.1 MOE'::'2.1.1.2 MOE Requirements'::'MoeB Requirement';
    #Refine dependency from '01 - CubeSat System Reference Model'::'2 - Technical Measures'::'2.1 - Technical Measures - Specifications and Requirements - Population'::'2.1.2 MOP'::'2.1.2.1 MOP Specifications'::'MopA Specification' to '01 - CubeSat System Reference Model'::'2 - Technical Measures'::'2.1 - Technical Measures - Specifications and Requirements - Population'::'2.1.2 MOP'::'2.1.2.2 MOP Requirements'::'MopA Requirement';
    #Refine dependency from '01 - CubeSat System Reference Model'::'2 - Technical Measures'::'2.1 - Technical Measures - Specifications and Requirements - Population'::'2.1.2 MOP'::'2.1.2.1 MOP Specifications'::'MopA Specification' to '01 - CubeSat System Reference Model'::'2 - Technical Measures'::'2.1 - Technical Measures - Specifications and Requirements - Population'::'2.1.2 MOP'::'2.1.2.2 MOP Requirements'::'MopA Requirement';
    #Refine dependency from '01 - CubeSat System Reference Model'::'2 - Technical Measures'::'2.1 - Technical Measures - Specifications and Requirements - Population'::'2.1.2 MOP'::'2.1.2.1 MOP Specifications'::'MopB Specification' to '01 - CubeSat System Reference Model'::'2 - Technical Measures'::'2.1 - Technical Measures - Specifications and Requirements - Population'::'2.1.2 MOP'::'2.1.2.2 MOP Requirements'::'MopB Requirement';
    #Refine dependency from '01 - CubeSat System Reference Model'::'2 - Technical Measures'::'2.1 - Technical Measures - Specifications and Requirements - Population'::'2.1.2 MOP'::'2.1.2.1 MOP Specifications'::'MopB Specification' to '01 - CubeSat System Reference Model'::'2 - Technical Measures'::'2.1 - Technical Measures - Specifications and Requirements - Population'::'2.1.2 MOP'::'2.1.2.2 MOP Requirements'::'MopB Requirement';
    #Refine dependency from '01 - CubeSat System Reference Model'::'2 - Technical Measures'::'2.1 - Technical Measures - Specifications and Requirements - Population'::'2.1.3 TPM'::'2.1.3.1 TPM Specifications'::'TpmA Specification' to '01 - CubeSat System Reference Model'::'2 - Technical Measures'::'2.1 - Technical Measures - Specifications and Requirements - Population'::'2.1.3 TPM'::'2.1.3.2 TPM Requirements'::'TpmA Requirement';
    #Refine dependency from '01 - CubeSat System Reference Model'::'2 - Technical Measures'::'2.1 - Technical Measures - Specifications and Requirements - Population'::'2.1.3 TPM'::'2.1.3.1 TPM Specifications'::'TpmA Specification' to '01 - CubeSat System Reference Model'::'2 - Technical Measures'::'2.1 - Technical Measures - Specifications and Requirements - Population'::'2.1.3 TPM'::'2.1.3.2 TPM Requirements'::'TpmA Requirement';
    #Refine dependency from '01 - CubeSat System Reference Model'::'2 - Technical Measures'::'2.1 - Technical Measures - Specifications and Requirements - Population'::'2.1.3 TPM'::'2.1.3.1 TPM Specifications'::'TpmB Specification' to '01 - CubeSat System Reference Model'::'2 - Technical Measures'::'2.1 - Technical Measures - Specifications and Requirements - Population'::'2.1.3 TPM'::'2.1.3.2 TPM Requirements'::'TpmB Requirement';
    #Refine dependency from '01 - CubeSat System Reference Model'::'2 - Technical Measures'::'2.1 - Technical Measures - Specifications and Requirements - Population'::'2.1.3 TPM'::'2.1.3.1 TPM Specifications'::'TpmB Specification' to '01 - CubeSat System Reference Model'::'2 - Technical Measures'::'2.1 - Technical Measures - Specifications and Requirements - Population'::'2.1.3 TPM'::'2.1.3.2 TPM Requirements'::'TpmB Requirement';
    #Refine dependency from '01 - CubeSat System Reference Model'::'2 - Technical Measures'::'2.1 - Technical Measures - Specifications and Requirements - Population'::'2.1.4 KPP'::'2.1.4.1 KPP Specifications'::'KppA Specification' to '01 - CubeSat System Reference Model'::'2 - Technical Measures'::'2.1 - Technical Measures - Specifications and Requirements - Population'::'2.1.4 KPP'::'2.1.4.2 KPP Requirements'::'KppA Requirement';
    #Refine dependency from '01 - CubeSat System Reference Model'::'2 - Technical Measures'::'2.1 - Technical Measures - Specifications and Requirements - Population'::'2.1.4 KPP'::'2.1.4.1 KPP Specifications'::'KppA Specification' to '01 - CubeSat System Reference Model'::'2 - Technical Measures'::'2.1 - Technical Measures - Specifications and Requirements - Population'::'2.1.4 KPP'::'2.1.4.2 KPP Requirements'::'KppA Requirement';
    #Refine dependency from '01 - CubeSat System Reference Model'::'2 - Technical Measures'::'2.1 - Technical Measures - Specifications and Requirements - Population'::'2.1.4 KPP'::'2.1.4.1 KPP Specifications'::'KppA Specification' to '01 - CubeSat System Reference Model'::'2 - Technical Measures'::'2.1 - Technical Measures - Specifications and Requirements - Population'::'2.1.4 KPP'::'2.1.4.2 KPP Requirements'::'KppA Requirement';
    #Refine dependency from '01 - CubeSat System Reference Model'::'2 - Technical Measures'::'2.1 - Technical Measures - Specifications and Requirements - Population'::'2.1.4 KPP'::'2.1.4.1 KPP Specifications'::'KppB Specification' to '01 - CubeSat System Reference Model'::'2 - Technical Measures'::'2.1 - Technical Measures - Specifications and Requirements - Population'::'2.1.4 KPP'::'2.1.4.2 KPP Requirements'::'KppB Requirement';
    #Refine dependency from '01 - CubeSat System Reference Model'::'2 - Technical Measures'::'2.1 - Technical Measures - Specifications and Requirements - Population'::'2.1.4 KPP'::'2.1.4.1 KPP Specifications'::'KppB Specification' to '01 - CubeSat System Reference Model'::'2 - Technical Measures'::'2.1 - Technical Measures - Specifications and Requirements - Population'::'2.1.4 KPP'::'2.1.4.2 KPP Requirements'::'KppB Requirement';
    dependency from '01 - CubeSat System Reference Model'::'6 - Validation Verification'::'6.1 - Validation Activities' to '01 - CubeSat System Reference Model'::'1 - Stakeholders'::'1.2 Mission Stakeholders'::'1.2.4 - Mission Objectives'::'Mission Objectives Table';
    dependency from '01 - CubeSat System Reference Model'::'6 - Validation Verification'::'6.2 - Verification Activities'::'Verification Activities Table' to '01 - CubeSat System Reference Model'::'4 - Requirements'::'L2 Segment Rqts'::'L2.1 Space Segment Rqts'::'L2.1.1 CubeSat Rqts'::'L2.1.1 CubeSat Rqts Table';
    dependency from '01 - CubeSat System Reference Model'::'6 - Validation Verification'::'6.2 - Verification Activities'::'Verification Activities Table' to '01 - CubeSat System Reference Model'::'4 - Requirements'::'L2 Segment Rqts'::'L2.1 Space Segment Rqts'::'L2.1.1 CubeSat Rqts'::'L2.1.1 CubeSat Rqts Table';
    #derivation connection { end #original ::> '02 - CSRM Elements, Examples and Illustrations'::'1 - Stakeholders'::'1.2 Mission Stakeholders'::'1.2.2 - Mission Stakeholders - Requirements, Technical Measures, Use Cases - Illustration'::'Stakeholder Concern Name'; end #derive ::> '02 - CSRM Elements, Examples and Illustrations'::'1 - Stakeholders'::'1.2 Mission Stakeholders'::'1.2.2 - Mission Stakeholders - Requirements, Technical Measures, Use Cases - Illustration'::'Mission Constraint Name'; }
    #Refine dependency from '02 - CSRM Elements, Examples and Illustrations'::'1 - Stakeholders'::'1.2 Mission Stakeholders'::'1.2.2 - Mission Stakeholders - Requirements, Technical Measures, Use Cases - Illustration'::'Measure of Performance Name' to '02 - CSRM Elements, Examples and Illustrations'::'1 - Stakeholders'::'1.2 Mission Stakeholders'::'1.2.2 - Mission Stakeholders - Requirements, Technical Measures, Use Cases - Illustration'::'Measure of Effectiveness Name';
    #Refine dependency from '02 - CSRM Elements, Examples and Illustrations'::'1 - Stakeholders'::'1.2 Mission Stakeholders'::'1.2.2 - Mission Stakeholders - Requirements, Technical Measures, Use Cases - Illustration'::'Technical Performance Measure Name' to '02 - CSRM Elements, Examples and Illustrations'::'1 - Stakeholders'::'1.2 Mission Stakeholders'::'1.2.2 - Mission Stakeholders - Requirements, Technical Measures, Use Cases - Illustration'::'Measure of Performance Name';
    #Refine dependency from '02 - CSRM Elements, Examples and Illustrations'::'1 - Stakeholders'::'1.2 Mission Stakeholders'::'1.2.2 - Mission Stakeholders - Requirements, Technical Measures, Use Cases - Illustration'::'Measure of Performance Name' to '02 - CSRM Elements, Examples and Illustrations'::'1 - Stakeholders'::'1.2 Mission Stakeholders'::'1.2.2 - Mission Stakeholders - Requirements, Technical Measures, Use Cases - Illustration'::'Segment Requirement Name';
    #Refine dependency from '02 - CSRM Elements, Examples and Illustrations'::'1 - Stakeholders'::'1.2 Mission Stakeholders'::'1.2.2 - Mission Stakeholders - Requirements, Technical Measures, Use Cases - Illustration'::'Technical Performance Measure Name' to '02 - CSRM Elements, Examples and Illustrations'::'1 - Stakeholders'::'1.2 Mission Stakeholders'::'1.2.2 - Mission Stakeholders - Requirements, Technical Measures, Use Cases - Illustration'::'Subsystem Requirement Name';
    #derivation connection { end #original ::> '02 - CSRM Elements, Examples and Illustrations'::'1 - Stakeholders'::'1.2 Mission Stakeholders'::'1.2.2 - Mission Stakeholders - Requirements, Technical Measures, Use Cases - Illustration'::'Mission Requirement Name'; end #derive ::> '02 - CSRM Elements, Examples and Illustrations'::'1 - Stakeholders'::'1.2 Mission Stakeholders'::'1.2.2 - Mission Stakeholders - Requirements, Technical Measures, Use Cases - Illustration'::'Segment Requirement Name'; }
    #Refine dependency from '02 - CSRM Elements, Examples and Illustrations'::'1 - Stakeholders'::'1.2 Mission Stakeholders'::'1.2.2 - Mission Stakeholders - Requirements, Technical Measures, Use Cases - Illustration'::'Measure of Effectiveness Name' to '02 - CSRM Elements, Examples and Illustrations'::'1 - Stakeholders'::'1.2 Mission Stakeholders'::'1.2.2 - Mission Stakeholders - Requirements, Technical Measures, Use Cases - Illustration'::'Mission Requirement Name';
    #derivation connection { end #original ::> '02 - CSRM Elements, Examples and Illustrations'::'1 - Stakeholders'::'1.2 Mission Stakeholders'::'1.2.2 - Mission Stakeholders - Requirements, Technical Measures, Use Cases - Illustration'::'Mission Objective Name'; end #derive ::> '02 - CSRM Elements, Examples and Illustrations'::'1 - Stakeholders'::'1.2 Mission Stakeholders'::'1.2.2 - Mission Stakeholders - Requirements, Technical Measures, Use Cases - Illustration'::'Mission Requirement Name'; }
    #derivation connection { end #original ::> '02 - CSRM Elements, Examples and Illustrations'::'1 - Stakeholders'::'1.2 Mission Stakeholders'::'1.2.2 - Mission Stakeholders - Requirements, Technical Measures, Use Cases - Illustration'::'Mission Constraint Name'; end #derive ::> '02 - CSRM Elements, Examples and Illustrations'::'1 - Stakeholders'::'1.2 Mission Stakeholders'::'1.2.2 - Mission Stakeholders - Requirements, Technical Measures, Use Cases - Illustration'::'Mission Requirement Name'; }
    #Refine dependency from '02 - CSRM Elements, Examples and Illustrations'::'1 - Stakeholders'::'1.2 Mission Stakeholders'::'1.2.2 - Mission Stakeholders - Requirements, Technical Measures, Use Cases - Illustration'::'Mission Use Case' to '02 - CSRM Elements, Examples and Illustrations'::'1 - Stakeholders'::'1.2 Mission Stakeholders'::'1.2.2 - Mission Stakeholders - Requirements, Technical Measures, Use Cases - Illustration'::'Mission Requirement Name';
    #Trace dependency from '02 - CSRM Elements, Examples and Illustrations'::'1 - Stakeholders'::'1.2 Mission Stakeholders'::'1.2.2 - Mission Stakeholders - Requirements, Technical Measures, Use Cases - Illustration'::'Segment Requirement Name' to '02 - CSRM Elements, Examples and Illustrations'::'1 - Stakeholders'::'1.2 Mission Stakeholders'::'1.2.2 - Mission Stakeholders - Requirements, Technical Measures, Use Cases - Illustration'::'Mission Use Case';
    #Refine dependency from '02 - CSRM Elements, Examples and Illustrations'::'1 - Stakeholders'::'1.2 Mission Stakeholders'::'1.2.2 - Mission Stakeholders - Requirements, Technical Measures, Use Cases - Illustration'::'Segment Use Case' to '02 - CSRM Elements, Examples and Illustrations'::'1 - Stakeholders'::'1.2 Mission Stakeholders'::'1.2.2 - Mission Stakeholders - Requirements, Technical Measures, Use Cases - Illustration'::'Segment Requirement Name';
    #Trace dependency from '02 - CSRM Elements, Examples and Illustrations'::'1 - Stakeholders'::'1.2 Mission Stakeholders'::'1.2.2 - Mission Stakeholders - Requirements, Technical Measures, Use Cases - Illustration'::'Subsystem Requirement Name' to '02 - CSRM Elements, Examples and Illustrations'::'1 - Stakeholders'::'1.2 Mission Stakeholders'::'1.2.2 - Mission Stakeholders - Requirements, Technical Measures, Use Cases - Illustration'::'Segment Use Case';
    #Refine dependency from '02 - CSRM Elements, Examples and Illustrations'::'1 - Stakeholders'::'1.2 Mission Stakeholders'::'1.2.2 - Mission Stakeholders - Requirements, Technical Measures, Use Cases - Illustration'::'Subsystem Use Case' to '02 - CSRM Elements, Examples and Illustrations'::'1 - Stakeholders'::'1.2 Mission Stakeholders'::'1.2.2 - Mission Stakeholders - Requirements, Technical Measures, Use Cases - Illustration'::'Subsystem Requirement Name';
    #Trace dependency from '02 - CSRM Elements, Examples and Illustrations'::'1 - Stakeholders'::'1.2 Mission Stakeholders'::'1.2.2 - Mission Stakeholders - Requirements, Technical Measures, Use Cases - Illustration'::'Stakeholder Concern Name' to '02 - CSRM Elements, Examples and Illustrations'::'1 - Stakeholders'::'1.2 Mission Stakeholders'::'1.2.2 - Mission Stakeholders - Requirements, Technical Measures, Use Cases - Illustration'::'Stakeholder Name';
    #derivation connection { end #original ::> '02 - CSRM Elements, Examples and Illustrations'::'1 - Stakeholders'::'1.2 Mission Stakeholders'::'1.2.2 - Mission Stakeholders - Requirements, Technical Measures, Use Cases - Illustration'::'Stakeholder Concern Name'; end #derive ::> '02 - CSRM Elements, Examples and Illustrations'::'1 - Stakeholders'::'1.2 Mission Stakeholders'::'1.2.2 - Mission Stakeholders - Requirements, Technical Measures, Use Cases - Illustration'::'Mission Need Name'; }
    #Refine dependency from '02 - CSRM Elements, Examples and Illustrations'::'1 - Stakeholders'::'1.2 Mission Stakeholders'::'1.2.2 - Mission Stakeholders - Requirements, Technical Measures, Use Cases - Illustration'::'Mission Objective Name' to '02 - CSRM Elements, Examples and Illustrations'::'1 - Stakeholders'::'1.2 Mission Stakeholders'::'1.2.2 - Mission Stakeholders - Requirements, Technical Measures, Use Cases - Illustration'::'Measure of Effectiveness Name';
    #derivation connection { end #original ::> '02 - CSRM Elements, Examples and Illustrations'::'1 - Stakeholders'::'1.2 Mission Stakeholders'::'1.2.2 - Mission Stakeholders - Requirements, Technical Measures, Use Cases - Illustration'::'Mission Need Name'; end #derive ::> '02 - CSRM Elements, Examples and Illustrations'::'1 - Stakeholders'::'1.2 Mission Stakeholders'::'1.2.2 - Mission Stakeholders - Requirements, Technical Measures, Use Cases - Illustration'::'Mission Objective Name'; }
    #derivation connection { end #original ::> '02 - CSRM Elements, Examples and Illustrations'::'1 - Stakeholders'::'1.2 Mission Stakeholders'::'1.2.2 - Mission Stakeholders - Requirements, Technical Measures, Use Cases - Illustration'::'Stakeholder Concern Name'; end #derive ::> '02 - CSRM Elements, Examples and Illustrations'::'1 - Stakeholders'::'1.2 Mission Stakeholders'::'1.2.2 - Mission Stakeholders - Requirements, Technical Measures, Use Cases - Illustration'::'Mission Objective Name'; }
    #derivation connection { end #original ::> '02 - CSRM Elements, Examples and Illustrations'::'1 - Stakeholders'::'1.2 Mission Stakeholders'::'1.2.2 - Mission Stakeholders - Requirements, Technical Measures, Use Cases - Illustration'::'Segment Requirement Name'; end #derive ::> '02 - CSRM Elements, Examples and Illustrations'::'1 - Stakeholders'::'1.2 Mission Stakeholders'::'1.2.2 - Mission Stakeholders - Requirements, Technical Measures, Use Cases - Illustration'::'Subsystem Requirement Name'; }
    #Refine dependency from '02 - CSRM Elements, Examples and Illustrations'::'1 - Stakeholders'::'1.2 Mission Stakeholders'::'1.2.2 - Mission Stakeholders - Requirements, Technical Measures, Use Cases - Illustration'::'Measure of Effectiveness Name' to '02 - CSRM Elements, Examples and Illustrations'::'1 - Stakeholders'::'1.2 Mission Stakeholders'::'1.2.2 - Mission Stakeholders - Requirements, Technical Measures, Use Cases - Illustration'::'Mission Requirement Name';
    #Refine dependency from '02 - CSRM Elements, Examples and Illustrations'::'1 - Stakeholders'::'1.2 Mission Stakeholders'::'1.2.2 - Mission Stakeholders - Requirements, Technical Measures, Use Cases - Illustration'::'Mission Use Case' to '02 - CSRM Elements, Examples and Illustrations'::'1 - Stakeholders'::'1.2 Mission Stakeholders'::'1.2.2 - Mission Stakeholders - Requirements, Technical Measures, Use Cases - Illustration'::'Mission Requirement Name';
    #Refine dependency from '02 - CSRM Elements, Examples and Illustrations'::'1 - Stakeholders'::'1.2 Mission Stakeholders'::'1.2.2 - Mission Stakeholders - Requirements, Technical Measures, Use Cases - Illustration'::'Segment Use Case' to '02 - CSRM Elements, Examples and Illustrations'::'1 - Stakeholders'::'1.2 Mission Stakeholders'::'1.2.2 - Mission Stakeholders - Requirements, Technical Measures, Use Cases - Illustration'::'Segment Requirement Name';
    #Refine dependency from '02 - CSRM Elements, Examples and Illustrations'::'1 - Stakeholders'::'1.2 Mission Stakeholders'::'1.2.2 - Mission Stakeholders - Requirements, Technical Measures, Use Cases - Illustration'::'Subsystem Use Case' to '02 - CSRM Elements, Examples and Illustrations'::'1 - Stakeholders'::'1.2 Mission Stakeholders'::'1.2.2 - Mission Stakeholders - Requirements, Technical Measures, Use Cases - Illustration'::'Subsystem Requirement Name';
}