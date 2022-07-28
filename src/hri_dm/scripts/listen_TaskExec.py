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
# from fiwareFORTH_cleanTest import send_ROSmsg_release

HRI_health_jsonFName = "./HRI_health.json"
ScenePerception_health_jsonFName = "./ScenePerception_health.json"
PlanePose = "./PlanePose.json"
workFlow_json = "./HRI.json"
Aegis_buttonPress = './Aegis_ButtonPress.json'
address = "25.45.111.204"
port = 1026

global navpos_x, navpos_y, navpos_theta, nmloc_x, nmloc_y, nmloc_theta

# navigate, grasp, releaseTool, handover
navigate_state, pickup_state, release_state, handover_state = 0, 0, 0, 0
last_toolID = -1

ACT_RES_FAIL = -1
ACT_RES_UNKNOWN = 0
ACT_RES_SUCCESS = 1


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
        workflow_state.updateStateMsg_nav(navigate_state, ACT_RES_UNKNOWN, data.navpos.x, data.navpos.y,
                                          data.navpos.theta)
        rospy.loginfo('Navigate Starts..')

    elif data.action == 'pickup':
        navigate_state = 0
        pickup_state = 1
        release_state = 0
        handover_state = 0
        last_toolID = data.tool_id
        workflow_state.updateStateMsg_pickup(pickup_state, ACT_RES_UNKNOWN, data.tool_id, data.location.x,
                                             data.location.y, data.location.z)
        rospy.loginfo('Pickup Starts..')

    elif data.action == 'release':
        navigate_state = 0
        pickup_state = 0
        release_state = 1
        handover_state = 0
        last_toolID = data.tool_id
        workflow_state.updateStateMsg_release(release_state, ACT_RES_UNKNOWN, data.tool_id)
        rospy.loginfo('Release Starts..')

    elif data.action == 'handover':
        navigate_state = 0
        pickup_state = 0
        release_state = 0
        handover_state = 1
        last_toolID = data.tool_id
        workflow_state.updateStateMsg_handover(handover_state, ACT_RES_UNKNOWN, data.tool_id, data.location.x,
                                               data.location.y, data.location.z)
        rospy.loginfo('Handover Starts..')

    # Inform FIWARE that the current script is alive
    send_HRIhealth()


def callback_TaskExResult(data):
    global navigate_state, pickup_state, release_state, handover_state, last_toolID
    print('callback_TaskExResult')
    rospy.loginfo('receiving message..')  # 2222 %s', data)
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
    rospy.loginfo(' callback_ScenePerception received message.. ')  # %s data.action)

    # send new location to FIWARE
    PlanePoseState = PlanePoseStatePost(address, port, 'FORTH.ScenePerception.WorkFlow', PlanePose)
    PlanePoseState.updateStateMsg(data.x, data.y, data.theta)

    # inform FIWARE that ScenePerception is alive
    my_date = datetime.utcnow()  # utc time, this is used in FELICE
    ScenePerceptionState = HRI_HealthStatePost(address, port, 'forth.ScenePerception.SystemHealth:001',
                                               ScenePerception_health_jsonFName)
    ScenePerceptionState.updateStateMsg("OK", str(my_date.isoformat()))

    # inform FIWARE that the current script is alive
    send_HRIhealth()

    # this listens the response of ICS-localization with Target to AEGIS-dynamic Position
    # if len(msg.data) == 0: rospy.logwarn("Message empty")
    global navpos_x, navpos_y, navpos_theta, nmloc_x, nmloc_y, nmloc_theta
    navpos_x, navpos_y, navpos_theta = data.x, data.y, data.theta  #, data.timestamp  # localization



def init_receiver():

    # this listens the commands send to the robot and informs FIWARE that they have received and get started
    rospy.Subscriber('Task2Execute', HRIDM2TaskExecution, callback_task2exec)

    # this listens the new Locations reported by ScenePerception
    rospy.Subscriber('Robot_Pose2D', Pose2D, callback_ScenePerc)

    # this listens the response of robot command execution (e.g success/failure)
    rospy.Subscriber('taskExec_2HRIDM', TaskExecution2HRIDM, callback_TaskExResult)

    rospy.loginfo('receiver_all subscriber nodes started')
    rospy.spin()

if __name__ == '__main__':
    rospy.init_node('listen_all', anonymous=True)
    init_receiver()

    # except rospy.ROSInterruptException:
    #     pass
