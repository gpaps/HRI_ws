#!/usr/bin/env python
import rospy
import requests
from datetime import datetime

from std_msgs.msg import String, Float64
from hri_dm.msg import HRIDM2TaskExecution, TaskExecution2HRIDM, Pose2D
from forthHRIHealthPost import HRI_HealthStatePost
from WorkflowState_fiware import WorkFlowStatePost
from forthPlanePose import PlanePoseStatePost

HRI_health_jsonFName = r"/home/gpapo/Desktop/hri_ws/src/hri_dm/scripts/HRI_health.json"
ScenePerception_health_jsonFName = r"/home/gpapo/Desktop/hri_ws/src/hri_dm/scripts/ScenePerception_health.json"
PlanePose = "/home/gpapo/Desktop/hri_ws/src/hri_dm/scripts/PlanePose.json"
workFlow_json = "/home/gpapo/Desktop/hri_ws/src/hri_dm/scripts/HRI.json"

address = "25.45.111.204"
port = 1026

# navigate, grasp, releaseTool, handover
navigate_state, navigate_result = 0, 0
pickup_state, pickup_result = 0, 0
release_state, release_result = 0, 0
handover_state, handover_result = 0, 0
last_toolID=-1

def callback_task2exec(data):
    # navigate, grasp, releaseTool, handover
    global navigate_state, pickup_state, release_state, handover_state, last_toolID 
    
    rospy.loginfo('receiving message %s', data.error_type)
    if data.action == 'navigate':
        navigate_state = 1
        pickup_state = 0
        release_state = 0
        handover_state = 0

        WorkFlowState = WorkFlowStatePost(address, port, 'forth.hri.RobotAction', workFlow_json)
        WorkFlowState.updateStateMsg_nav(data.x, data.y, data.theta, navigate_state, data.result), '\n'

    elif data.action == 'pickup':
        navigate_state = 0
        pickup_state = 1
        release_state = 0
        handover_state = 0
        last_toolID = data.tool_id
    elif data.action == 'release':
        navigate_state = 0
        pickup_state = 0
        release_state = 1
        handover_state = 0
        last_toolID = data.tool_id
    elif data.action == 'handover':
        navigate_state = 0
        pickup_state = 0
        release_state = 0
        handover_state = 1
        last_toolID = data.tool_id



def callback_HRIhealth(data):
    print('callback_HRIhealth')
    rospy.loginfo('receiving message2222 %s',)# data.action)

    my_date = datetime.utcnow()  # utc time, this is used in FELICE
    hriStateTest = HRI_HealthStatePost(address, port, 'forth.HRI.SystemHealth:001', HRI_health_jsonFName)
    hriStateTest.updateStateMsg("OK", str(my_date.isoformat())), '\n'
    # print(data)


    #Get information about the result of robot action execution in ROS, to be forwarded to the Orchestrator 
def callback_TaskExResult(data):
    global navigate_state, pickup_state, release_state, handover_state, last_toolID 

    print('callback_TaskExResult')
    rospy.loginfo('receiving message2222 %s',data)
    
    # if "navigate" was the active action (i.e. under execution) provide an update for this action
    if navigate_state == 1:
        # it has cocompleted so it is not active anymore
        navigate_state = 0
        navigate_result = data.result # not sure if this line is needed
        WorkFlowState = WorkFlowStatePost(address, port, 'forth.hri.RobotAction', workFlow_json)
        WorkFlowState.updateStateMsg_nav(data.x, data.y, data.theta, navigate_state, data.result), '\n'

    # if "pickup" was the active action (i.e. under execution) provide an update for this action
    elif pickup_state == 1:
        # it has cocompleted so it is not active anymore
        pickup_state = 0
        pickup_result = data.result # not sure if this line is needed
        WorkFlowState = WorkFlowStatePost(address, port, 'forth.hri.RobotAction', workFlow_json)
        WorkFlowState.updateStateMsg_grasp(self, last_toolID, data.x, data.y, data.z, pickup_state,  data.result):

    # if "release" was the active action (i.e. under execution) provide an update for this action
    elif release_state == 1:
        # it has cocompleted so it is not active anymore
        release_state = 0 
        release_result = data.result # not sure if this line is needed
        WorkFlowState = WorkFlowStatePost(address, port, 'forth.hri.RobotAction', workFlow_json)
        fingerState=0
        armState=0
        WorkFlowState.updateStateMsg_release(self, last_toolID, fingerState, armState,  data.result):
            
            
def callback_ScenePHealth(data):
    # rospy.sleep(.5)
    print('callback_ScenePHealth')
    rospy.loginfo('receiving message2222 %s',)# data.action)

    my_date = datetime.utcnow()  # utc time, this is used in FELICE
    ScenePerceptionState = HRI_HealthStatePost(address, port, 'forth.ScenePerception.SystemHealth:001',
                                               ScenePerception_health_jsonFName)
    ScenePerceptionState.updateStateMsg("OK", str(my_date.isoformat())), '\n'

    PlanePoseState = PlanePoseStatePost(address, port, 'FORTH.ScenePerception.WorkFlow', PlanePose)
    PlanePoseState.updateStateMsg(data.x, data.y, data.theta), '\n'

def init_receiver():
    # rospy.init_node('receiver', anonymous=True)
    rospy.loginfo('receiver_all node started')
    print('init_receiver_all always awaits.. .')

    # this for taskExecution
    rospy.Subscriber('taskExec_2HRIDM', TaskExecution2HRIDM, callback_TaskExResult)
    # rospy.Subscriber('taskExec_2HRIDM', TaskExecution2HRIDM, callback_HRIhealth)
    
    # this for Localization
    rospy.Subscriber('Robot_Pose2D', Pose2D, callback_ScenePHealth)
    # this for FORTH/ Task2Execution
    rospy.Subscriber('Task2Execute', HRIDM2TaskExecution, callback_task2exec)


    # while
    rospy.spin()


if __name__ == '__main__':
    rospy.init_node('listen_all', anonymous=True)

    init_receiver()

    # except rospy.ROSInterruptException:
    #     pass
