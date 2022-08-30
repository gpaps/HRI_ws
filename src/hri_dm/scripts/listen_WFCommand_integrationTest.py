#!/usr/bin/env python
import rospy, re
import requests
from datetime import datetime

# import from files & fiware imports
from std_msgs.msg import String, Float64
from forthHRIHealthPost import HRI_HealthStatePost
from hri_dm.msg import HRIDM2TaskExecution, TaskExecution2HRIDM, Pose2D

address = "25.45.111.204"
port = 1026
last_send = 0

# publishers
# this Publishes the commands send to the robot (nav, handover, etc )
pub2TaskExec = rospy.Publisher('Task2Execute', HRIDM2TaskExecution, queue_size=100)
# this publishes the new Locations reported by ScenePerception
pub2Pose2D = rospy.Publisher('Robot_Pose2D', Pose2D, queue_size=100)
# this Publishes robot command execution (e.g success/failure)
pub2HRIDM = rospy.Publisher('taskExec_2HRIDM', TaskExecution2HRIDM, queue_size=100)


def callback_TaskExResult(data):
    global last_send
    print('callback_TaskExResult')
    rospy.loginfo('receiving message..')  # 2222 %s', data)
    # if no error is reported back by the module undertaking the execution
    if data.result:

        if last_send == 2:
            send_msg_rel()

            last_send = 3
            rospy.loginfo(last_send)

        if last_send == 1:
            send_msg_handover()
            last_send = 2
            rospy.loginfo(last_send)


    else:
        rospy.loginfo('error type', data.error_type)  # in that case an error is reported, and thus the action has failed


def send_msg_taskexec2hri():
    # PROFACTOR
    global pub2HRIDM
    task_exec = TaskExecution2HRIDM()
    # For synchronization
    task_exec.request_id = 32
    # True if success; False if not
    task_exec.result = True
    # Error type e.g. “null”, “ArmExtFailed”, “ObjLocFailed”, ReachFailed”, “GraspingFailed”, “ArmHomingFailed”, “ArmRecoveryFailed”, “HandOverReachFailed”, “HandOverReleaseFailed”, “NavigationFailed”
    task_exec.error_type = 'null'
    rospy.loginfo(task_exec)
    pub2HRIDM.publish(task_exec)
    print('end_of_message_  sendS_msg_TASKExec2HRI and pub2HRIDM', '\n')


def send_msg_nav():
    global last_send
    task_exec2 = HRIDM2TaskExecution()
    task_exec2.action = 'navigate'  # action
    task_exec2.tool_id = -1
    # location/vector3 geom_msgs location
    task_exec2.location.x = 99999
    task_exec2.location.y = 99999
    task_exec2.location.z = 99999
    # location/nav Pose2D
    task_exec2.navpos.x = 100.0
    task_exec2.navpos.y = 200.0
    task_exec2.navpos.theta = 90.0
    # synchronization
    task_exec2.request_id = 1
    rospy.loginfo(task_exec2)
    pub2TaskExec.publish(task_exec2)
    print('end_of_message_  send_msg_HRIDM2TaskEXEC and pub2TaskExec', '\n')
    # pub2task.publish(task_exec2)
    last_send = 1
    rospy.loginfo(last_send)

def send_msg_handover():
    task_exec2 = HRIDM2TaskExecution()
    task_exec2.action = 'handover'  # action
    task_exec2.tool_id = 1
    # location/vector3 geom_msgs location
    task_exec2.location.x = 256
    task_exec2.location.y = 520
    task_exec2.location.z = 100
    # location/nav Pose2D
    task_exec2.navpos.x = 99999
    task_exec2.navpos.y = 99999
    task_exec2.navpos.theta = 99999
    # synchronization
    task_exec2.request_id = 2
    rospy.loginfo(task_exec2)
    pub2TaskExec.publish(task_exec2)
    print('end_of_message_  send_msg_HRIDM2TaskEXEC and pub2TaskExec', '\n')
    # pub2task.publish(task_exec2)


def send_msg_rel():
    task_exec2 = HRIDM2TaskExecution()
    task_exec2.action = 'release'  # action
    task_exec2.tool_id = 1
    # location/vector3 geom_msgs location
    task_exec2.location.x = 99999
    task_exec2.location.y = 99999
    task_exec2.location.z = 99999
    # location/nav Pose2D
    task_exec2.navpos.x = 99999
    task_exec2.navpos.y = 99999
    task_exec2.navpos.theta = 99999
    # synchronization
    task_exec2.request_id = 3
    rospy.loginfo(task_exec2)
    pub2TaskExec.publish(task_exec2)
    print('end_of_message_  send_msg_HRIDM2TaskEXEC and pub2TaskExec', '\n')
    # pub2task.publish(task_exec2)


def firstTask_sender():
    global result
    rospy.loginfo('sender node starts..')
    send_msg_nav()

    # testing
    # send_msg_taskexec2hri()   # PROFACTOR does that,
    # send_msg_pose2d(), '\n'

def init_receiver():
    # rospy.init_node('receiver', anonymous=True)
    rospy.loginfo('receiver node started')
    print('init_receiver always awaits.. .')
    rospy.Subscriber('taskExec_2HRIDM', TaskExecution2HRIDM, callback_TaskExResult)
    # rospy.Subscriber('fiwareTest', TaskExecution2HRIDM, callback)
    # rospy.spin()


if __name__ == '__main__':
    # init the 1st publisher  or init the first pub-in
    rospy.init_node('TaskExecution2HRIDM', anonymous=True)

    # rospy.init_node('HRIDM2TaskExecution', anonymous=True)
    # pub1 = rospy.Publisher('HRIDM2_taskExec', HRIDM2TaskExecution, queue_size=10)

    # rate = rospy.Rate(0.5)  # t=1/f, where f =0.5 <-- rospyRate
    try:
        firstTask_sender()
        init_receiver()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
