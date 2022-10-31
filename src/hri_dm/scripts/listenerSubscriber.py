#!/usr/bin/env python
import rospy
from datetime import datetime
from hri_dm.msg import HRIDM2TaskExecution, TaskExecution2HRIDM, Pose2D, PoseWithCovarianceStamped, arm_actuals

# # fiware imports
# from scripts.forthHRIHealthPost import HRI_HealthStatePost

robotAction_jsonFName = r"/home/gpaps/humanRob_ws/src/beginner_tutorials/scripts/fiware_v2/health.json"
address = "25.45.111.204"
port = 1026

pub2TaskExec = rospy. Publisher('HRIDM2_taskExec', HRIDM2TaskExecution, queue_size=100)


def callback(data):
    print('callback')
    rospy.loginfo('receiving message %s', data.error_type)
    if data.result == True:
        print("peirame TRUE")
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
    # hriStateTest = HRI_HealthStatePost(address, port, robotAction_jsonFName)
    # hriStateTest.updateStateMsg("-____________o.0____________-", str(my_date.isoformat()))


def callback_Recording(data):  # not used for now!
    print(type(data.FTS_Wrench))
    print(data.FTS_Wrench)
    # writer = csv.writer(f)
    # writer.writerow(list(data.FTS_Wrench))
    # Tx, Ty, Tz = FTS_Wrench[0], FTS_Wrench[1], FTS_Wrench[2] #E







def callback_armActuals(data):
    Tx, Ty, Tz, Fx, Fy, Fz = data.FTS_Wrench
    print(Tx, Ty, Tz,  Fx, Fy, Fz)
    print('listener_Subscriber-1 --/ end')
    print(data.FTS_Wrench)
    print('listener_Subscriber-2 --/ end')


def init_receiver():
    # rospy.init_node('receiver', anonymous=True)
    rospy.loginfo('receiver node started')
    print('init_receiver always awaits.. .')
    # rospy.Subscriber('taskExec_2HRIDM', TaskExecution2HRIDM, callback)

    # rospy.Subscriber('fiwareTest', TaskExecution2HRIDM, callback)
    rospy.Subscriber('arm_actuals', arm_actuals, callback_armActuals)
    rospy.spin()


if __name__ == '__main__':
    rospy.init_node('Listener_Subscriber_Test', anonymous=True)
    init_receiver()

    # except rospy.ROSInterruptException:
    #     pass
