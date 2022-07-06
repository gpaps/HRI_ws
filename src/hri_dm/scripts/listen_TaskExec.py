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

def callback_task2exec(data):
    # navigate, grasp, releaseTool, handover
    rospy.loginfo('receiving message %s', data.error_type)
    if data.action == 'navigate':
        navigate_state = 1

        WorkFlowState = WorkFlowStatePost(address, port, 'forth.hri.RobotAction', workFlow_json)
        WorkFlowState.updateStateMsg_nav(data.x, data.y, data.theta, navigate_state, data.result), '\n'


    elif data.action == 'pickup':
        pickup_state = 1
    elif data.action == 'release':
        release_state = 1
    elif data.action == 'handover':
        handover_state = 1



def callback_HRIhealth(data):
    print('callback_HRIhealth')
    rospy.loginfo('receiving message2222 %s',)# data.action)

    my_date = datetime.utcnow()  # utc time, this is used in FELICE
    hriStateTest = HRI_HealthStatePost(address, port, 'forth.HRI.SystemHealth:001', HRI_health_jsonFName)
    hriStateTest.updateStateMsg("OK", str(my_date.isoformat())), '\n'
    # print(data)

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
    rospy.Subscriber('taskExec_2HRIDM', TaskExecution2HRIDM, callback_HRIhealth)
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
