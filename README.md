# hri_ws
/src/scripts/

__fiwareRos__\
listen_WFCommand.py (set to replace the fiwareFORTH_cleanTest.py)\
WorkflowState_fiware.py (fiware only, sends state about workflow-cmds)\
#listen_fiwareFORTH.py (pybullet integrated in script - beta_old)

__ros-com2fiware__\
listen_TaskExec.py (listen&respond, ROSsubs3topics->
Tas2Execute,
Robot_Pose2D,
tasExec_2HRIDM, and triggers WFState_fiware.py)\

__ros-fiware-test__\
localSender2.py (sends msg once)\
listenerSubscriber.py (ros2fiware?)\
localization_sender.py (ros)\

__Pybullet__\
handover_pos.py\
result3_humanoid.urdf (humanoid model)
humanoidFindLocation_withM.py(beta first script)\

__essential__\
logger.py (must exist in the sameDIR)\
sub.py (gpaps script for sub)
mix_sub.py (mich. script for sub)

__fcn__\
_eq.py\ (fcn: rotate, get_quaternion_from_euler,
quadratic_eq, linear_eq, euc_dist, find_pos_Rel2Hum, find_pos_0)
quatern_test.py\
#reader_wfc.py(test_script)

__Installation__\
_pip install pybullet_
