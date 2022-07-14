from __future__ import print_function

import sys
import math
import time
import random
import numpy as np

import rospy
from std_msgs.msg import String

from _eq import *


CRED1 = '\033[31m'
CGR1 = '\033[32m'
CYEL1 = '\033[33m'
CBlUE1 = '\033[34m'
CMAG1 = '\033[35m'
COIL1 = '\033[36m'
CBRED1 = '\033[41m'
CBGR1 = '\033[42m'
CBYEL1 = '\033[43m'
CBBlUE1 = '\033[44m'
CBMAG1 = '\033[45m'
CBOIL1 = '\033[46m'
CRED2 = '\033[91m'
CGR2 = '\033[92m'
CYEL2 = '\033[93m'
CBLUE2 = '\033[94m'
CMAG2 = '\033[95m'
COIL2 = '\033[96m'
CEND = '\033[0m'

# mode is either "D" for degree, otherwise it assumes  radians or "R" for radians
def get_quaternion_from_euler(roll, pitch, yaw, mode):

    if mode == "D":
        roll = roll * np.pi / 180
        pitch = pitch * np.pi / 180
        yaw = yaw * np.pi / 180

    qx = np.sin(roll / 2) * np.cos(pitch / 2) * np.cos(yaw / 2) - np.cos(roll / 2) * np.sin(pitch / 2) * np.sin(yaw / 2)
    qy = np.cos(roll / 2) * np.sin(pitch / 2) * np.cos(yaw / 2) + np.sin(roll / 2) * np.cos(pitch / 2) * np.sin(yaw / 2)
    qz = np.cos(roll / 2) * np.cos(pitch / 2) * np.sin(yaw / 2) - np.sin(roll / 2) * np.sin(pitch / 2) * np.cos(yaw / 2)
    qw = np.cos(roll / 2) * np.cos(pitch / 2) * np.cos(yaw / 2) + np.sin(roll / 2) * np.sin(pitch / 2) * np.sin(yaw / 2)

    return [qx, qy, qz, qw]

# find_pos(loc_r, loc_h, d)
hpos=[74,44]
rpos=[20,20]
pos_found, xf, yf = find_pos_Rel2Hum(rpos, hpos, 4)
print("location:",pos_found, xf, yf)
if pos_found>0:
    sol_l, a, b = linear_eq([xf,yf], hpos)
    dir=np.arctan(a)
    print("direction=",dir)

# thetaDeg=90
# thetaR=thetaDeg*np.pi/180
# # thetaR=1.5708
#
# print(thetaDeg,"-->",thetaR)
# print("quaternion ", get_quaternion_from_euler(0, 0, thetaDeg, "D"))

# sys.exit(0)


# prevPos = pos
# prevPos1 = ls[4]
# hasPrevPose = 1
