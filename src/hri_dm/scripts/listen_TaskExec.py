#!/usr/bin/env python
import re
import rospy
import requests
from datetime import datetime

from std_msgs.msg import String, Float64
from hri_dm.msg import HRIDM2TaskExecution, TaskExecution2HRIDM, Pose2D
from forthHRIHealthPost import HRI_HealthStatePost
from WorkflowState_fiware import WorkFlowStatePost
from forthPlanePose import PlanePoseStatePost

HRI_health_jsonFName = "./HRI_health.json"
ScenePerception_health_jsonFName = "./ScenePerception_health.json"
PlanePose = "./PlanePose.json"
workFlow_json = "./HRI.json"
Aegis_buttonPress = './Aegis_ButtonPress.json'
address = "25.45.111.204"
port = 1026

# navigate, grasp, releaseTool, handover
# ta state ta xreiazomaste, ta result mallon oxi
navigate_state, pickup_state, release_state, handover_state = 0, 0, 0, 0
last_toolID = -1

ACT_RES_FAIL = -1
ACT_RES_UNKNOWN = 0
ACT_RES_SUCCESS = 1

def callback_task2exec(data):
    # navigate, grasp, releaseTool, handover
    global navigate_state, pickup_state, release_state, handover_state, last_toolID

    workflow_state = WorkFlowStatePost(address, port, 'forth.hri.RobotAction', workFlow_json)

    if data.action == 'navigate':
        navigate_state = 1
        pickup_state = 0
        release_state = 0
        handover_state = 0
        # TODO to 8eloume to comment auto?Isxuei to provlima auto ?
        # to ACT_RES_UNKNOWN thelei allagh sthn updateStateMsg_nav giati einai 3 oi dynates times twra
        workflow_state.updateStateMsg_nav(data.navpos.x, data.navpos.y, data.navpos.theta,
                                         navigate_state, ACT_RES_UNKNOWN)
        rospy.loginfo('Navigate Starts..')

    elif data.action == 'pickup':
        navigate_state = 0
        pickup_state = 1
        release_state = 0
        handover_state = 0
        last_toolID = data.tool_id
        workflow_state.updateStateMsg_pickup(data.tool_id, data.location.x, data.location.y, data.location.z,
                                            pickup_state, ACT_RES_UNKNOWN)
        rospy.loginfo('Pickup Starts..')

    elif data.action == 'release':
        navigate_state = 0
        pickup_state = 0
        release_state = 1
        handover_state = 0
        last_toolID = data.tool_id
        workflow_state.updateStateMsg_release(data.tool_id, release_state, ACT_RES_UNKNOWN)
        rospy.loginfo('Release Starts..')

    elif data.action == 'handover':
        navigate_state = 0
        pickup_state = 0
        release_state = 0
        handover_state = 1
        last_toolID = data.tool_id
        workflow_state.updateStateMsg_handover(handover_state, ACT_RES_UNKNOWN)
        rospy.loginfo('Handover Starts..')


def callback_HRIhealth(data):
    print('callback_HRIhealth')
    rospy.loginfo('receiving message..., ')  #%s data.action)

    my_date = datetime.utcnow()  # utc time, this is used in FELICE
    hri_state_test = HRI_HealthStatePost(address, port, 'forth.HRI.SystemHealth:001', HRI_health_jsonFName)
    hri_state_test.updateStateMsg("OK", str(my_date.isoformat())), '\n'
    # print(data)

    #  Get information about the result of robot action execution in ROS, to be forwarded to the Orchestrator

def callback_TaskExResult(data):
    global navigate_state, pickup_state, release_state, handover_state, last_toolID
    print(data)
    print('callback_TaskExResult')
    rospy.loginfo('receiving message..')  # 2222 %s', data)
    workflow_state = WorkFlowStatePost(address, port, 'forth.hri.RobotAction', workFlow_json)
    
    # if no error is reported back by the module undertaking the execution  
    if re.findall('null', data.error_type):
        rslt = ACT_RES_SUCCESS

    # we need to synchronize ROS messages and FIWARE messages more carefully....
    # if "navigate" was the active action (i.e. under execution) provide an update for this action
    if navigate_state == 1:
        # it has completed so it is not active anymore
        navigate_state = 0
        workflow_state.updateStateMsg_nav(navigate_state, ACT_RES_SUCCESS)

    # if "pickup" was the active action (i.e. under execution) provide an update for this action
    elif pickup_state == 1:  # pickup == grasp
        # it has completed so it is not active anymore
        pickup_state = 0
        workflow_state.updateStateMsg_pickup(pickup_state, ACT_RES_SUCCESS)

    # if "release" was the active action (i.e. under execution) provide an update for this action
    elif release_state == 1:
        # it has completed so it is not active anymore
        release_state = 0
        workflow_state.updateStateMsg_release(release_state, ACT_RES_SUCCESS)

    elif handover_state == 1:
        handover_state = 0
        workflow_state.updateStateMsg_handover(handover_state, ACT_RES_SUCCESS)


def callback_ScenePHealth(data):
    # rospy.sleep(.5)
    print('callback_ScenePHealth')
    rospy.loginfo('receiving message.. ')  #%s data.action)

    my_date = datetime.utcnow()  # utc time, this is used in FELICE
    ScenePerceptionState = HRI_HealthStatePost(address, port, 'forth.ScenePerception.SystemHealth:001',
                                               ScenePerception_health_jsonFName)
    ScenePerceptionState.updateStateMsg("OK", str(my_date.isoformat())), '\n'

    PlanePoseState = PlanePoseStatePost(address, port, 'FORTH.ScenePerception.WorkFlow', PlanePose)
    PlanePoseState.updateStateMsg(data.x, data.y, data.theta), '\n'


def init_receiver():
    # rospy.init_node('receiver', anonymous=True)
    rospy.loginfo('receiver_all node started')

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
