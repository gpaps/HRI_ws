import sys
import math
import time
import random

# from future.backports.socketserver import UDPServer
from matplotlib import pyplot as plt
import numpy as np
import pybullet as p
import pybullet_data
from pybullet import URDF_USE_SELF_COLLISION, URDF_MAINTAIN_LINK_ORDER, \
    URDF_USE_SELF_COLLISION_INCLUDE_PARENT


class color:
    """COLORS 4 Debug"""
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


global end_effectorId, mass_matrix  # end_effectorId = 37


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
            print(color.CGR1, i, int(ang), color.CEND, end="   ")
        elif ((i == 20 and side == 'L') or (i == 15 and side == 'R')) and 20. < ang < 60.:
            # print(CYEL1, str('ShoulderJ_X Conditionally Acceptable '), math.degrees(newangle), CEND)
            print(color.CYEL1, i, int(ang), color.CEND, end="   ")
            if murry_err < 1:
                murry_err = 1
        elif (i == 20 and side == 'L') or (i == 15 and side == 'R'):  # and (ang < 0.0 or  60. < ang):
            # print(CRED1, str('ShoulderJ_X Unacceptable Pos.'), math.degrees(newangle), CEND)
            print(color.CRED1, i, int(ang), color.CEND, end="   ")
            if murry_err < 2:
                murry_err = 2

        # L Shoulder2 on X (Upper arm flexion/extension)
        if ((i == 21 and side == 'L') or (i == 16 and side == 'R')) and 0.0 < ang < 20.1:
            # print(CGR1, str('ShoulderJ_Y Ergonomically Acceptable'), math.degrees(newangle), CEND)
            print(color.CGR1, i, int(ang), color.CEND, end="   ")
        elif ((i == 21 and side == 'L') or (i == 16 and side == 'R')) and 20.1 < ang < 60.:
            # print(CYEL1, str('ShoulderJ_Y Conditionally Acceptable '), math.degrees(newangle), CEND)
            print(color.CYEL1, i, int(ang), color.CEND, end="   ")
            if murry_err < 1:
                murry_err = 1
        elif (i == 21 and side == 'L') or (i == 16 and side == 'R'):  # and (ang < 0.0 or 60. < ang ):
            # print(CRED1, str('ShoulderJ_Y Unacceptable Pos.'), math.degrees(newangle), CEND)
            print(color.CRED1, i, int(ang), color.CEND, end="   ")
            if murry_err < 2:
                murry_err = 2

        # TODO add orientation parameter for the end effector

        # # L Shoulder3 on Z ____ Rotation Z
        if ((i == 22 and side == 'L') or (i == 17 and side == 'R')) and -15 < ang < 30.:
            # print(CGR1, str('ShoulderJ_Z Ergonomically Acceptable'), math.degrees(newangle), CEND)
            print(color.CGR1, i, int(ang), color.CEND, end="   ")
        elif ((i == 22 and side == 'L') or (i == 17 and side == 'R')) and (
                -30. < ang < 60.):  # the if above, has covered the case of angle -15 < ang < 30.
            # print(CYEL1, str('ShoulderJ_Z Conditionally Acceptable '), math.degrees(newangle), CEND)
            print(color.CYEL1, i, int(ang), color.CEND, end="   ")
            if murry_err < 1:
                murry_err = 1
        elif (i == 22 and side == 'L') or (i == 17 and side == 'R'):  # and (ang < -30 or 60. < ang):
            # print(CRED1, str('ShoulderJ_Z Unacceptable Pos'), math.degrees(newangle), CEND)
            print(color.CRED1, i, int(ang), color.CEND, end="   ")
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
            print(color.CGR1, i, int(ang), color.CEND, end="   ")
        elif ((i == 24 and side == 'L') or (i == 19 and side == 'R')) and (
                -55. < ang < 40):  # the if above, has covered the case of angle -30 < ang < 20.
            # print(CYEL1, str('ElbowJ Pronation/Supination Conditionally Acceptable '), math.degrees(newangle), CEND)
            print(color.CYEL1, i, int(ang), color.CEND, end="   ")
            if murry_err < 1:
                murry_err = 1
        elif (i == 24 and side == 'L') or (i == 19 and side == 'R'):  # all other angles are bad!
            # print(CRED1, str('ElbowJ Pronation/Supination Unacceptable Pos'), math.degrees(newangle), CEND)
            print(color.CRED1, i, int(ang), color.CEND, end="   ")
            if murry_err < 2:
                murry_err = 2

    if murry_err == 0:
        print(color.CBGR1, "murry error      ", murry_err, color.CEND)
    elif murry_err == 1:
        print(color.CBYEL1, "murry error      ", murry_err, color.CEND)
    elif murry_err == 2:
        print(color.CBRED1, "murry error      ", murry_err, color.CEND)
    return murry_err


def find_handover_pos():
    # Connect to Physics-Server
    p.connect(p.GUI)  # for time debug,
    if p.getConnectionInfo():
        # p.connect(p.DIRECT)

        p.setAdditionalSearchPath(pybullet_data.getDataPath())  # Pybullet_data package
        humanoid = p.loadURDF("result3_humanoid_mass.urdf", [0.0, .7, 1.3], p.getQuaternionFromEuler([0.0, 0.0, 0.0]),
                              useFixedBase=1, globalScaling=1,  # useMaximalCoordinates=True,
                              flags=URDF_MAINTAIN_LINK_ORDER | URDF_USE_SELF_COLLISION_INCLUDE_PARENT | URDF_USE_SELF_COLLISION,
                              )
        p.loadURDF("plane100.urdf", [0, 0, -0.01], )

        # environment constants
        timestep = (1. / 240.)
        p.setGravity(0, 0, -10)

        shoulder_motors = [31, 32, 33, 38]  # enable sensor in specified link for record/tracking
        [p.enableJointForceTorqueSensor(humanoid, i, True) for i in shoulder_motors]  # #returns None
        [p.changeDynamics(humanoid, i, mass=2.0) for i in shoulder_motors]  # change mass for ech link to 2

        L_end_effectorId, R_end_effectorId = 38, 30
        fm_list, fm_list_31, fm_list_32, fm_list_33 = [], [], [], []
        # links and joiIds[is to locate revolut joints] --> List's
        jointIds, paramIds = [], []
        for i_joints in range(p.getNumJoints(humanoid)):  # find all the joints in humanoid
            # p.changeDynamics(humanoid, i, )  # linearDamping=0, angularDamping=0)
            info = p.getJointInfo(humanoid, i_joints)  # get all_info from joints
            print(info)
            jointName, jointType = info[1], info[2]  # store jointInfo into list
            if jointType == p.JOINT_REVOLUTE:  # iterate to find specific joints
                jointIds.append(i_joints)

        pos = [1, 1, 1.3]  # pos = [random.uniform(0.2, 0.4), random.uniform(0.1, 0.3), random.uniform(3.0, 2)]

        # simulation start's
        jointAngles = p.calculateInverseKinematics(humanoid, L_end_effectorId, pos, maxNumIterations=100)
        for sims in range(100):
            p.stepSimulation()
            for jj in range(1):
                for i in range(len(jointAngles)):
                    p.setJointMotorControl2(humanoid, jointIds[i], p.POSITION_CONTROL, jointAngles[i], force=.1 * 100)

                p.stepSimulation()
                time.sleep(timestep)
                p.setGravity(0, 0, -10)
                # invariant
                p.changeDynamics(humanoid, R_end_effectorId, mass=2.0)  # right end effector
                p.changeDynamics(humanoid, L_end_effectorId, mass=1.4)  # left end-effector
                p.changeDynamics(humanoid, 13, mass=13.5)  # left_feet
                p.changeDynamics(humanoid, 22, mass=13.5)  # right_feet
                # [link index == joint index] for JointIds,
                if sims > 50:
                    p.changeDynamics(humanoid, L_end_effectorId, mass=3.0)
                    print(f'sims = {sims}')
                # mass_matrix  w/dim dofCount*dofCount, stored as a list of rows, each row is a list of mass Matrix elements
                mass_matrix = p.calculateMassMatrix(humanoid, jointAngles)
                ls = p.getLinkState(humanoid, L_end_effectorId)

                # p.getLinkState(humanoid, L_end_effectorId)  # l_state =
                # add to a list, the jointState
                [fm_list_31.append(np.array(p.getJointState(humanoid, i)[2])) for i in range(shoulder_motors[0])]
                [fm_list_32.append(np.array(p.getJointState(humanoid, i)[2])) for i in range(shoulder_motors[1])]
                [fm_list_33.append(np.array(p.getJointState(humanoid, i)[2])) for i in range(shoulder_motors[2])]

                # j_state = np.array(p.getJointState(humanoid, L_end_effectorId)[2])  # [Fx, Fy, Fz, Mx, My, Mz]
                # fm_list.append(j_state)

    # plots on L-arm
    list_size = len(fm_list_32)
    fig = plt.figure(figsize=(20, 7))
    ax = fig.add_subplot(111)
    plt.plot(range(list_size), np.array([elem[0] for elem in fm_list_32]), label='fm_fx')
    plt.plot(range(list_size), np.array([elem[1] for elem in fm_list_32]), label='fm_fy')
    plt.plot(range(list_size), np.array([elem[2] for elem in fm_list_32]), label='fm_fz')
    # plt.plot(range(list_size), np.array([elem[3] for elem in fm_list]), label='fm_mx')
    # plt.plot(range(list_size), np.array([elem[4] for elem in fm_list]), label='fm_my')
    # plt.plot(range(list_size), np.array([elem[5] for elem in fm_list]), label='fm_mz')
    plt.title("measured force/torque link32(Shoulder)")
    plt.legend()
    plt.show()

    # plots on L-arm
    list_size = len(fm_list_33)
    fig = plt.figure(figsize=(20, 7))
    ax = fig.add_subplot(111)
    plt.plot(range(list_size), np.array([elem[0] for elem in fm_list_33]), label='fm_fx')
    plt.plot(range(list_size), np.array([elem[1] for elem in fm_list_33]), label='fm_fy')
    plt.plot(range(list_size), np.array([elem[2] for elem in fm_list_33]), label='fm_fz')
    # plt.plot(range(list_size), np.array([elem[3] for elem in fm_list]), label='fm_mx')
    # plt.plot(range(list_size), np.array([elem[4] for elem in fm_list]), label='fm_my')
    # plt.plot(range(list_size), np.array([elem[5] for elem in fm_list]), label='fm_mz')
    plt.title("measured force/torque- link33(Shoulder)")
    plt.legend()
    plt.show()

    p.disconnect()
    return fm_list


if __name__ == '__main__':
    # x, y, z = find_HandOver_pos()
    fm_list = find_handover_pos()
    print(len(fm_list))
