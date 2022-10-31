#!/usr/bin/env python
import re, os
import rospy
import requests
from datetime import datetime

from std_msgs.msg import String, Float64
from hri_dm.msg import HRIDM2TaskExecution, TaskExecution2HRIDM, Pose2D, PoseWithCovarianceStamped
from forthHRIHealthPost import HRI_HealthStatePost
from WorkflowState_fiware import WorkFlowStatePost
from PlanePose_fiware import PlanePoseStatePost
from handover_pos import *
import spikeDetect_Ros

# json files
HRI_health_jsonFName = "./HRI_health.json"
ScenePerception_health_jsonFName = "./ScenePerception_health.json"
PlanePose = "./PlanePose.json"
workFlow_json = "./HRI.json"
Aegis_buttonPress = './Aegis_ButtonPress.json'
# IP & address
# address = "25.45.111.204" # Orch/
address = '25.85.76.1'  # DemoIP
port = 1026

global navpos_x, navpos_y, navpos_theta, nmloc_x, nmloc_y, nmloc_theta

# navigate, grasp, releaseTool, handover
navigate_state, pickup_state, release_state, handover_state = 0, 0, 0, 0
last_toolID = -1

# ACTION RESULT | Status
ACT_RES_SUCCESS = 1
ACT_RES_UNKNOWN = 0
ACT_RES_FAIL = -1


# This function informs FIWARE that the current script is still alive
# This should be executed in all callbacks
def send_HRIhealth():
    my_date = datetime.utcnow()  # utc time, this is used in FELICE
    hri_state_test = HRI_HealthStatePost(address, port, 'forth.HRI.SystemHealth:002', HRI_health_jsonFName)
    hri_state_test.updateStateMsg("OK", str(my_date.isoformat())), '\n'


def callback_task2exec(data):
    # print(data, 'callback_task2exec')
    """
    This function listens the commands send to the robot.
    It keeps track of the command that is currently executed by the robot and informs FIWARE they started
    """
    global navigate_state, pickup_state, release_state, handover_state, last_toolID, nmloc_x, nmloc_y, nmloc_theta

    workflow_state = WorkFlowStatePost(address, port, 'forth.hri.RobotAction', workFlow_json)

    if data.action == 'navigate':
        print(data)
        navigate_state = 1
        pickup_state = 0
        release_state = 0
        handover_state = 0
        workflow_state.updateStateMsg_nav(navigate_state, ACT_RES_UNKNOWN,
                                          data.navpos.x, data.navpos.y, data.navpos.theta)
        rospy.loginfo('Navigate Starts..')
        print(CRED1, 'Navigate Starts..', CEND)

    elif data.action == 'pickup':
        navigate_state = 0
        pickup_state = 1
        release_state = 0
        handover_state = 0
        last_toolID = data.tool_id
        workflow_state.updateStateMsg_pickup(pickup_state, ACT_RES_UNKNOWN, data.tool_id,
                                             data.location.x, data.location.y, data.location.z)
        rospy.loginfo('Pickup Starts..')
        print(CRED1, 'Pickup Starts..', CEND)

    elif data.action == 'release':
        navigate_state = 0
        pickup_state = 0
        release_state = 1
        handover_state = 0
        last_toolID = data.tool_id
        workflow_state.updateStateMsg_release(release_state, ACT_RES_UNKNOWN, data.tool_id)
        rospy.loginfo('Release Starts..')
        print(CRED1, 'Release Starts..', CEND)

    elif data.action == 'handover':
        navigate_state = 0
        pickup_state = 0
        release_state = 0
        handover_state = 1
        last_toolID = data.tool_id
        workflow_state.updateStateMsg_handover(handover_state, ACT_RES_UNKNOWN, data.tool_id,
                                               data.location.x, data.location.y, data.location.z)
        rospy.loginfo('Handover Starts..')
        print(CRED1, 'Handover Starts..', CEND)
    # Inform FIWARE that the current script is alive
    send_HRIhealth()


def callback_TaskExResult(data):
    global navigate_state, pickup_state, release_state, handover_state, last_toolID
    print('callback_TaskExResult')
    rospy.loginfo('receiving message..')  # 2222 %s', data)
    print('callBack2TaskEx, data received :', data)
    workflow_state = WorkFlowStatePost(address, port, 'forth.hri.RobotAction', workFlow_json)
    # if no error is reported back by the module undertaking the execution  
    if re.findall('null', data.error_type):
        rslt = ACT_RES_SUCCESS
    else:  # in that case an error is reported, and thus the action has failed
        rslt = ACT_RES_FAIL

    # we need to synchronize ROS messages and FIWARE messages more carefully....
    # if "navigate" was the active action (i.e. under execution) provide an update for this action
    if navigate_state == 1:
        # it has completed so it is not active anymore
        navigate_state = 0
        workflow_state.updateStateMsg_nav(navigate_state, rslt)

    # if "pickup" was the active action (i.e. under execution) provide an update for this action
    elif pickup_state == 1:  # pickup == grasp
        # it has completed so it is not active anymore
        pickup_state = 0
        workflow_state.updateStateMsg_pickup(pickup_state, rslt)

    # if "release" was the active action (i.e. under execution) provide an update for this action
    elif release_state == 1:
        # it has completed so it is not active anymore
        release_state = 0
        workflow_state.updateStateMsg_release(release_state, rslt)

    elif handover_state == 1:
        handover_state = 0
        workflow_state.updateStateMsg_handover(handover_state, rslt)

    # Inform FIWARE that the current script is alive
    send_HRIhealth()


def callback_ScenePerc(data):
    """ Callback for ScenePerception ROS messages
        It sends to FIWARE
        (1)  new location
        (2)  ScenePerception.SystemHealth message
    """
    # rospy.sleep(.5)
    print(data.pose.pose.orientation.w)
    rospy.loginfo(' callback_ScenePerception received message.. ')  # %s data.action)
    print(CRED2, 'callback_ScenePerception received message.. ', CEND)
    # send new location to FIWARE
    PlanePoseState = PlanePoseStatePost(address, port, 'FORTH.ScenePerception.WorkFlow', PlanePose)
    th = 2*math.atan2(data.pose.pose.orientation.z, data.pose.pose.orientation.w)
    PlanePoseState.updateStateMsg(data.pose.pose.position.x, data.pose.pose.position.y, th)

    # inform FIWARE that ScenePerception is alive
    my_date = datetime.utcnow()  # utc time, this is used in FELICE
    ScenePerceptionState = HRI_HealthStatePost(address, port, 'forth.ScenePerception.SystemHealth:001',
                                               ScenePerception_health_jsonFName)
    ScenePerceptionState.updateStateMsg("OK", str(my_date.isoformat()))

    # inform FIWARE that the current script is alive
    send_HRIhealth()

    ####

    # this listens the response of ICS-localization with Target to AEGIS-dynamic Position
    # if len(msg.data) == 0: rospy.logwarn("Message empty")
    # test
    # global navpos_x, navpos_y, navpos_theta, nmloc_x, nmloc_y, nmloc_theta, navigate_state
    # navpos_x, navpos_y, navpos_theta = data.x, data.y, data.theta  # , data.timestamp  # localization
    # navpos_x, navpos_y, navpos_theta, nmloc_x, nmloc_y, nmloc_theta = 2., 3., 30, 6., 8., 60.  # for DEBUG
    #
    # if (nmloc_x and navpos_x) and (nmloc_x and navpos_y) and (navpos_theta and nmloc_theta):  # or if 1: always true
    #     diff_x = nmloc_x - navpos_x
    #     diff_y = nmloc_y - navpos_y
    #     diff_theta = nmloc_theta - navpos_theta
    #
    #     rslt = ACT_RES_SUCCESS
    #
    #     if (diff_x < 0.5) and (diff_y < 0.5) and (diff_theta < 0.5):
    #         print(navigate_state)
    #         if navigate_state == 1:
    #             # it has completed so it is not active anymore
    #             navigate_state = 0
    #             workflow_state = WorkFlowStatePost(address, port, 'forth.hri.RobotAction', workFlow_json)
    #             workflow_state.updateStateMsg_nav(navigate_state, rslt)
    #             rospy.loginfo('Location Reached')
    #             # fiware publish position reached
    #     else:
    #         pass
    #         # rslt = ACT_RES_FAIL # send the current or location difference?
    # # send smth else?

    spikeDetect_Ros.callback_arm_actuals()

def init_receiver():
    # this listens the commands send to the robot and informs FIWARE that they have received and get started
    rospy.Subscriber('Task2Execute', HRIDM2TaskExecution, callback_task2exec, queue_size=100)

    # this listens the new Locations reported by ScenePerception
    rospy.Subscriber('Robot_Pose2D', PoseWithCovarianceStamped, callback_ScenePerc, queue_size=100) #Pose2D

    # this listens the response of robot command execution (e.g success/failure)
    rospy.Subscriber('taskExec_2HRIDM', TaskExecution2HRIDM, callback_TaskExResult, queue_size=100)

    # this listen  the response of release-command, and starts a spike detection
    # NOTE:! arm_actuals msg file is init. in different local.msg.file than the rest.
    rospy.Subscriber('arm_actuals', arm_actuals, callback_arm_actuals)
    rospy.loginfo("listen's arm_actual")

    rospy.loginfo('receiver_all subscriber nodes started')
    print(CMAG2, 'receiver_all subscriber nodes started', CEND)

    rospy.spin()


if __name__ == '__main__':
    rospy.init_node('listen_all', anonymous=True)
    init_receiver()

    # except rospy.ROSInterruptException:
    #     pass
