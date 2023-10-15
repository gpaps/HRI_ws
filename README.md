# Human-Robot-Interaction_ws

![Feliche](https://github.com/gpaps/HRI_ws/assets/29929836/7ced04e1-c761-479b-8d61-7380718f7609)

**About the Project**

The **Felice** project is a part of the European Horizon initiative, aimed at enhancing human-robot interaction and collaboration. It combines multidisciplinary research in various fields, including collaborative robotics, AI, computer vision, IoT, machine learning, data analytics, cyber-physical systems, process optimization, and ergonomics.

**My Contribution**

While I was affiliated with the project, I developed and contribute to the codebase found in this repository. This code represents my efforts in the areas of human-robot interaction and automation within the Feliche project.

**Project Objectives**

The primary goal of Felice is to create a modular platform that seamlessly integrates and harmonizes an array of autonomous and cognitive technologies. This platform is designed to increase the agility and productivity of manual assembly production systems, ensuring the safety and improving the physical and mental well-being of factory workers.

**Code Overview**

Within this repository, you will find a collection of scripts and utilities related to human-robot interaction, ROS (Robot Operating System) communication, Fiware integration, Pybullet simulations, and essential utilities. These scripts were developed to support the objectives of the Felice project, emphasizing the coordination and combination of human and robot skills.

**Current Status**

Please note that the Felice project is ongoing, and my affiliation with the project may have concluded. Nevertheless, this repository represents my contributions and ongoing efforts in the field of human-robot interaction within the context of Felice.

**Installation**

To use the code in this repository, ensure you have the necessary dependencies installed. You can install Pybullet using the following command:

/src/scripts/
__Fiware-Ros__\
listen_WFCommand.py (set to replace the fiwareFORTH_cleanTest.py)\
WorkflowState_fiware.py (fiware only, sends state's about workflow-cmds)\
PlanePose_fiware.py (fiware only, sends xyTheta)\
#listen_fiwareFORTH.py (pybullet integrated in script - beta_old)

__Ros-Comm2fFware__\
listen_TaskExec.py (listen&respond, ROSsubs3topics->
    Tas2Execute, Robot_Pose2D, tasExec_2HRIDM, 
    and triggers WFState_fiware.py, PlanePose_fiware)

__Ros-Fiware-test's__\
localSender2.py (sends msg once)\
listenerSubscriber.py (ros2fiware?)\
localization_sender.py (ros)

__Pybullet__\
handover_pos.py\
result3_humanoid.urdf (humanoid model)
humanoidFindLocation_withM.py(beta first script)

__Essential-Utils__\
logger.py (must exist in the sameDIR)\
sub.py (gpaps script for sub)\
mix_sub.py (mich. script for sub)

__Fcn-w/-math__\
_eq.py\ (fcn: rotate, get_quaternion_from_euler,
quadratic_eq, linear_eq, euc_dist, find_pos_Rel2Hum, find_pos_0)
quatern_test.py\
#reader_wfc.py(test_script)

__Installation__\
_pip install pybullet_


__This README provides a concise overview of your work on the Felice project while acknowledging that the project is still ongoing and that you may no longer be directly affiliated with it.__



```bash
pip install pybullet


