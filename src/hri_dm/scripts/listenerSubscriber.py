#!/usr/bin/env python
from datetime import datetime
import rospy
from std_msgs.msg import String
from hri_dm.msg import HRIDM2TaskExecution, TaskExecution2HRIDM

# fiware imports
from fiware_v2.forthHRIHealthPost import HRI_HealthStatePost, HRI_Health
robotAction_jsonFName = r"/home/gpaps/humanRob_ws/src/beginner_tutorials/scripts/fiware_v2/health.json"
address = "25.45.111.204"
port = 1026

pub2TaskExec = rospy.Publisher('HRIDM2_taskExec', HRIDM2TaskExecution, queue_size=100)

def callback(data):
    print('callback')
    rospy.loginfo('receiving message %s', data.error_type)
    if data.result == True:
        print ("peirame TRUE")
        rospy.loginfo('we got Truesszz')
        newtask = HRIDM2TaskExecution()
        newtask.action = 'next_task'
        rospy.loginfo(newtask)
        pub2TaskExec.publish(newtask)
    else:
        print('FALSE')
        newtask = HRIDM2TaskExecution()
        newtask.action = 'please try again'
        pub2TaskExec.publish(newtask)
        rospy.loginfo(newtask)
    my_date = datetime.utcnow()  # utc time, this is used in FELICE
    print(my_date.isoformat())
    hriStateTest = HRI_HealthStatePost(address, port, robotAction_jsonFName)
    hriStateTest.updateStateMsg("-____________o.0____________-", str(my_date.isoformat()))


def init_receiver():
    # rospy.init_node('receiver', anonymous=True)
    rospy.loginfo('receiver node started')
    print('init_receiver always awaits.. .')
    # rospy.Subscriber('taskExec_2HRIDM', TaskExecution2HRIDM, callback)
    rospy.Subscriber('fiwareTest', TaskExecution2HRIDM, callback)
    rospy.spin()


if __name__ == '__main__':
    rospy.init_node('HRIDM2TaskExecution', anonymous=True)
    init_receiver()


    # except rospy.ROSInterruptException:
    #     pass