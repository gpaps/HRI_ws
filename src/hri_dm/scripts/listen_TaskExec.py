#!/usr/bin/env python
import rospy
import requests
from datetime import datetime

from std_msgs.msg import String, Float64
from hri_dm.msg import HRIDM2TaskExecution, TaskExecution2HRIDM, Pose2D
from forthHRIHealthPost import HRI_HealthStatePost
HRI_health_jsonFName = r"/home/gpapo/Desktop/hri_ws/src/hri_dm/scripts/HRI_health.json"
ScenePerception_health_jsonFName = r"/home/gpapo/Desktop/hri_ws/src/hri_dm/scripts/ScenePerception_health.json"
address = "25.45.111.204"
port = 1026
my_date = datetime.utcnow()  # utc time, this is used in FELICE

def callback1(data):
    print('______________________________________________callback____1')
    rospy.loginfo('receiving message %s', data.error_type)

    if data.result == True:
        print('  Received TRUE')
    #     rospy.loginfo('loginfo --> msg_from_callback1'), '\n'
    #     newtask = HRIDM2TaskExecution()
    #     newtask.action = 'newtask.action --> msg_from_callback1,', '\n'
    #     rospy.loginfo(newtask)
    else:
        print('  Received FALSE')
        # newtask = HRIDM2TaskExecution()
        # newtask.action = 'newtask.action from else --> msg_from_callback1'
        # rospy.loginfo(newtask)

def msge_decode_Pose2D(data):
    global pub2Pose2D
    pose_task = Pose2D()
    pose_task.x = 1.1
    pose_task.y = 2.2
    pose_task.theta = 60.3
    pose_task.timestamp = my_date.isoformat()
    rospy.loginfo(pose_task)
    # pub2Pose2D.publish(pose_task)
    print('___msgDecode_Pose2D    end_of_message_', '\n')


def callback_HRIhealth(data):
    # rospy.sleep(.5)
    print('callback_HRIhealth')
    rospy.loginfo('receiving message2222 %s',)# data.action)

    hriStateTest = HRI_HealthStatePost(address, port, 'forth.HRI.SystemHealth:001', HRI_health_jsonFName)
    hriStateTest.updateStateMsg("OK", str(my_date.isoformat())) , '\n'

def callback_ScenePHealth(data):
    # rospy.sleep(.5)
    print('callback_ScenePHealth')
    rospy.loginfo('receiving message2222 %s',)# data.action)

    ScenePerceptionState = HRI_HealthStatePost(address, port, 'forth.ScenePerception.SystemHealth:001',
                                               ScenePerception_health_jsonFName)
    ScenePerceptionState.updateStateMsg("OK", str(my_date.isoformat())), '\n'

def init_receiver():
    # rospy.init_node('receiver', anonymous=True)
    rospy.loginfo('receiver_all node started')
    print('init_receiver_all always awaits.. .')

    # this for taskExecution
    rospy.Subscriber('taskExec_2HRIDM', TaskExecution2HRIDM, callback_HRIhealth)

    # this for Localization
    rospy.Subscriber('Robot_Pose2D', Pose2D, callback_ScenePHealth)

    # this Papo-test, mine personal test,
    rospy.Subscriber('Robot_Pose2D', Pose2D, msge_decode_Pose2D)

    # while
    rospy.spin()


if __name__ == '__main__':
    rospy.init_node('listen_all', anonymous=True)

    init_receiver()

    # except rospy.ROSInterruptException:
    #     pass
