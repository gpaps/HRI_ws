#!/usr/bin/env python3

import requests
import rospy

from std_msgs.msg import String
from hri_dm.msg import HRIDM2TaskExecution, TaskExecution2HRIDM


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


def callback2(data):
    # rospy.sleep(.5)
    print('callback___2')
    rospy.loginfo('receiving message2222 %s', data.action)


def init_receiver():
    # rospy.init_node('receiver', anonymous=True)
    rospy.loginfo('receiver_all node started')
    print('init_receiver_all always awaits.. .')
    rospy.Subscriber('taskExec_2HRIDM', TaskExecution2HRIDM, callback1)
    # rospy.Subscriber('HRIDM2_taskExec', HRIDM2TaskExecution, callback2)

    rospy.spin()


if __name__ == '__main__':
    rospy.init_node('listen_all', anonymous=True)

    init_receiver()

    # except rospy.ROSInterruptException:
    #     pass
