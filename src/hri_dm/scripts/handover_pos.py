import sys
import math
import time
import random

import pybullet as p
import pybullet_data
from pybullet import URDF_USE_SELF_COLLISION, URDF_MAINTAIN_LINK_ORDER, \
    URDF_USE_SELF_COLLISION_INCLUDE_PARENT

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

global end_effectorId


# end_effectorId = 37


##############################
def murry_checkAngles(allAngles, side):
    murry_err = 0
    for i in range(len(allAngles)):
        if i < 20:
            pass
        ang = math.degrees(allAngles[i])

        # print(i,ang)
        # L Shoulder1 on Y (Upper arm abduction/adduction)
        if ((i == 20 and side == 'L') or (i == 15 and side == 'R')) and 0.0 < ang < 20.1:
            # print(CGR1, str('ShoulderJ_X Ergonomically Acceptable'), math.degrees(newangle), CEND)
            print(CGR1, i, int(ang), CEND, end="   ")
        elif ((i == 20 and side == 'L') or (i == 15 and side == 'R')) and 20. < ang < 60.:
            # print(CYEL1, str('ShoulderJ_X Conditionally Acceptable '), math.degrees(newangle), CEND)
            print(CYEL1, i, int(ang), CEND, end="   ")
            if murry_err < 1:
                murry_err = 1
        elif (i == 20 and side == 'L') or (i == 15 and side == 'R'):  # and (ang < 0.0 or  60. < ang):
            # print(CRED1, str('ShoulderJ_X Unacceptable Pos.'), math.degrees(newangle), CEND)
            print(CRED1, i, int(ang), CEND, end="   ")
            if murry_err < 2:
                murry_err = 2

        # L Shoulder2 on X (Upper arm flexion/extension)
        if ((i == 21 and side == 'L') or (i == 16 and side == 'R')) and 0.0 < ang < 20.1:
            # print(CGR1, str('ShoulderJ_Y Ergonomically Acceptable'), math.degrees(newangle), CEND)
            print(CGR1, i, int(ang), CEND, end="   ")
        elif ((i == 21 and side == 'L') or (i == 16 and side == 'R')) and 20.1 < ang < 60.:
            # print(CYEL1, str('ShoulderJ_Y Conditionally Acceptable '), math.degrees(newangle), CEND)
            print(CYEL1, i, int(ang), CEND, end="   ")
            if murry_err < 1:
                murry_err = 1
        elif (i == 21 and side == 'L') or (i == 16 and side == 'R'):  # and (ang < 0.0 or 60. < ang ):
            # print(CRED1, str('ShoulderJ_Y Unacceptable Pos.'), math.degrees(newangle), CEND)
            print(CRED1, i, int(ang), CEND, end="   ")
            if murry_err < 2:
                murry_err = 2

        # TODO add orientation parameter for the end effector

        # # L Shoulder3 on Z ____ Rotation Z
        if ((i == 22 and side == 'L') or (i == 17 and side == 'R')) and -15 < ang < 30.:
            # print(CGR1, str('ShoulderJ_Z Ergonomically Acceptable'), math.degrees(newangle), CEND)
            print(CGR1, i, int(ang), CEND, end="   ")
        elif ((i == 22 and side == 'L') or (i == 17 and side == 'R')) and (
                -30. < ang < 60.):  # the if above, has covered the case of angle -15 < ang < 30.
            # print(CYEL1, str('ShoulderJ_Z Conditionally Acceptable '), math.degrees(newangle), CEND)
            print(CYEL1, i, int(ang), CEND, end="   ")
            if murry_err < 1:
                murry_err = 1
        elif (i == 22 and side == 'L') or (i == 17 and side == 'R'):  # and (ang < -30 or 60. < ang):
            # print(CRED1, str('ShoulderJ_Z Unacceptable Pos'), math.degrees(newangle), CEND)
            print(CRED1, i, int(ang), CEND, end="   ")
            if murry_err < 2:
                murry_err = 2

        # TODO add orientation parameter for the end effector(Palm) to lookUP
        #  to combine it to the result __ otherwise this init. as False !!!
        # ElbowJoint_L   ||  Forearm flexion/extension
        # if ((i == 23 and side=='L') or (i==18 and side=='R')) and 60.0 < ang+90 < 100.:
        #     # print(CGR1, str('ElbowJ_L flexion/extension Ergonomically Acceptable'), math.degrees(newangle), CEND)
        #     print(CGR1, i, int(ang), CEND, end="   ")
        # elif ((i == 23 and side=='L') or (i==18 and side=='R')): # and (ang+90 <60 or 100 < ang+90):
        #     # print(CRED1, str('ElbowJ_L flexion/extension Unacceptable Pos.'), math.degrees(newangle), CEND)
        #     print(CRED1, i, int(ang), CEND, end="   ")
        #     if murry_err < 2:
        #         murry_err = 2

        # ElbowJoint Left   ||   pronation/Supination
        if ((i == 24 and side == 'L') or (i == 19 and side == 'R')) and -30 < ang < 20.:
            # print(CBGR1, str('ElbowJ Pronation/Supination Ergonomically Acceptable'), math.degrees(newangle), CEND)
            print(CGR1, i, int(ang), CEND, end="   ")
        elif ((i == 24 and side == 'L') or (i == 19 and side == 'R')) and (
                -55. < ang < 40):  # the if above, has covered the case of angle -30 < ang < 20.
            # print(CYEL1, str('ElbowJ Pronation/Supination Conditionally Acceptable '), math.degrees(newangle), CEND)
            print(CYEL1, i, int(ang), CEND, end="   ")
            if murry_err < 1:
                murry_err = 1
        elif (i == 24 and side == 'L') or (i == 19 and side == 'R'):  # all other angles are bad!
            # print(CRED1, str('ElbowJ Pronation/Supination Unacceptable Pos'), math.degrees(newangle), CEND)
            print(CRED1, i, int(ang), CEND, end="   ")
            if murry_err < 2:
                murry_err = 2

    if murry_err == 0:
        print(CBGR1, "murry error      ", murry_err, CEND)
    elif murry_err == 1:
        print(CBYEL1, "murry error      ", murry_err, CEND)
    elif murry_err == 2:
        print(CBRED1, "murry error      ", murry_err, CEND)
    return murry_err


def get_humanPose_ws(ws):
    import requests
    import json
    """ ws = WorkStation-number, ex.int: 1,2,3 """
    obj = requests.get('http://25.45.111.204:1026/v2/entities/iccs.hbu.PoseEstimation.WorkerPose:00' + str(ws))
    orn = obj.json()['orientation']['value']
    x = obj.json()['position']['value']['x']['value']
    y = obj.json()['position']['value']['y']['value']
    return x, y, orn


def find_HandOver_pos():
    p.connect(p.GUI)
    # p.connect(p.DIRECT)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())

    obUid = p.loadURDF("result3_humanoid.urdf", [0, 0, 1.3],
                       p.getQuaternionFromEuler([0, 0, 0]),
                       useMaximalCoordinates=False,
                       useFixedBase=0,
                       flags=URDF_MAINTAIN_LINK_ORDER | URDF_USE_SELF_COLLISION_INCLUDE_PARENT | URDF_USE_SELF_COLLISION
                       )
    p.resetBasePositionAndOrientation(obUid, [0, 0, 1.3], [0.0, 0.0, 0.0, 1])
    humanoid = obUid

    # gravId = p.addUserDebugParameter(" Gravity ", 0, 1, -1)
    # gravId = p.addUserDebugParameter("gravity", -10, 10, -10)
    jointIds = []
    paramIds = []

    p.setPhysicsEngineParameter(numSolverIterations=10)
    p.changeDynamics(humanoid, -1, linearDamping=0, angularDamping=0)

    for j in range(p.getNumJoints(humanoid)):
        p.changeDynamics(humanoid, j, linearDamping=0, angularDamping=0)
        info = p.getJointInfo(humanoid, j)
        # print(info)
        jointName = info[1]
        jointType = info[2]
        if jointType == p.JOINT_REVOLUTE:
            jointIds.append(j)
            # paramIds.append(p.addUserDebugParameter(jointName.decode("utf-8"), -4, 4, 0))
            # print("j=", j, "  st=", p.getJointState(humanoid, j))

    p.setRealTimeSimulation(1)
    t = 0
    hasPrevPose = 0
    trailDuration = 1
    end_effectorId = 37
    t = t + 0.05
    pos = [0.3 + 0.1 * math.cos(2 * t), 0.2 + 0.2 * math.cos(t + 6), 1.1 - 0.1 * math.sin(t)]
    jointPoses1 = p.calculateInverseKinematics(humanoid, end_effectorId, pos, maxNumIterations=100)

    greenPoses = []
    poscount = 0
    while 1:
        # p.setGravity(0, 0, p.readUserDebugParameter(gravId))
        t = t + 0.05
        # pos = [0.3 + 0.1 *math.cos(3*t), 0.3 +0.2 * math.cos(t+6), 1.1-0.2 * math.cos(t)]

        pos = [random.uniform(0.1, 0.4), random.uniform(0.0, 0.3), random.uniform(1.0, 1.35)]
        jointAngles = p.calculateInverseKinematics(humanoid, end_effectorId, pos, maxNumIterations=100)

        # print(jointPoses1)
        # tempJointPoses = list(jointPoses1)
        # tempJointPoses[20] = 0
        # jointPoses1 = tuple(tempJointPoses)

        for kk in range(2):
            # print(kk)
            for i in range(len(jointAngles)):
                p.setJointMotorControl2(humanoid, jointIds[i], p.POSITION_CONTROL, jointAngles[i], force=.5 * 40.)
            ls = p.getLinkState(humanoid, end_effectorId)
            # print("ls=", ls[4], "    pos=", pos)

        dx = ls[4][0] - pos[0]
        dy = ls[4][1] - pos[1]
        dz = ls[4][2] - pos[2]
        dist = math.sqrt(dx * dx + dy * dy + dz * dz)
        # print(dist)
        if dist < 0.1:
            m_res = murry_checkAngles(jointAngles,
                                      "L")  # "L": for left side arm check,       "R": for right side arm check
            if m_res == 0:
                p.addUserDebugPoints([pos], [[0, 1., 0]], 5.0, trailDuration)  # Green
                greenPoses.append(ls[4])
                poscount = poscount + 1

            if m_res == 1:
                p.addUserDebugPoints([pos], [[1., 1., 0.]], 4.5, trailDuration)  # Yellow
            if m_res == 2:
                p.addUserDebugPoints([pos], [[1., 0, 0.]], 3.5, trailDuration)  # Red
            # time.sleep(1.0)
        # print("ls=", ls[4], "    pos=", pos)

        # if hasPrevPose:
        #   # addUserDebugLine( lineFrom(XYZ), lineToXYZ, lineColorRGB, lineWidth(1.5) )
        #   p.addUserDebugLine(prevPos, pos, [0, 0, 0.6], .6, trailDuration)
        #   p.addUserDebugLine(prevPos1, ls[4], [1, 0, 0], 2.6, trailDuration)  # elbow  or wannabe end-effector
        if poscount == 1:  # This finds the first 10 green p
            # ositions, but..... we may return the first one and stop!
            print(greenPoses)

            # p.disconnect()
            return greenPoses[0][0], greenPoses[0][1], greenPoses[0][2]
            # rr = random.randint(0, len(greenPoses))
            # print(greenPoses[rr])
            # break

    # return greenPoses


# sys.exit(0)
# pos1 = find_HO_pos()
##############################################
if __name__ == '__main__':
    # ws = 2
    # pos_x, pos_y, theta = get_humanPose_ws(ws)
    x, y, z = find_HandOver_pos()
