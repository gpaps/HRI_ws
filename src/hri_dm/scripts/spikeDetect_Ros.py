#!/usr/bin/env python
import re

import csv
import rospy
import requests
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

from std_msgs.msg import String, Float64
from hri_dm.msg import HRIDM2TaskExecution, TaskExecution2HRIDM, Pose2D, PoseWithCovarianceStamped, arm_actuals
from forthHRIHealthPost import HRI_HealthStatePost
from WorkflowState_fiware import WorkFlowStatePost
from PlanePose_fiware import PlanePoseStatePost
from handover_pos import *

# from felice_arm.msg import arm_actuals

# IP & address
# address = "25.45.111.204" # Orch/
# address = '192.168.2.106'  # DemoIP
# port = 1026
# workFlow_json = "./HRI.json"

# global navpos_x, navpos_y, navpos_theta, nmloc_x, nmloc_y, nmloc_theta

# navigate, grasp, releaseTool, handover
# navigate_state, pickup_state, release_state, handover_state = 0, 0, 0, 0
# last_toolID = -1

# function lists, test's for out of the scope #not_to_be_removed_as_it_is!
spikes_tx, diff_sample_tx = list(), list()
tx_list, ty_list, tz_list = list(), list(), list()
original_signal, first_derivative, spikes, = list(), list(), list()


def rec_data2csv(data, name):  # to keep data while script is dead
    """data=file, name=(string)"""
    temp = open(f'./tempList_FTs_{name}.csv', 'a')
    writer = csv.writer(temp)
    writer.writerow(data)
    temp.close()



def diff_finder(data, threshold):
    """ Differentiation, between prev_value and current value """
    # original_signal, first_derivative, spikes = list(), list(), list()
    # column_id = 0
    for i in data:
        # grab the spikes above the threshold value (threshold = 5)

        for k in range(len(data)):  # changes on range(1, len(data)
            sample = data[:][k]  # grab each value for every iter in the data[:]
            # print('sample(1)', k, sample)

            original_signal.append(sample)  # create variable with the original signal
            std = np.std(original_signal)  # standard deviation of the Original_signal

            # differentiation sequence
            for row_id in range(len(data)):  # changes on range(1, len(data)
                # for every value from the originalSignal :
                prev_sample = data[:][row_id - 1]  # previous_value
                sample = data[:][row_id]  # current_value
                # print('sample(2)', sample)

                # find the difference, [differentiation]1PA
                diff_sample = sample - prev_sample
                # first_derivative.append(diff_sample)
                # Grab Spike,
                if (sample < std) and (abs(diff_sample) < threshold):
                    diff_sample = 0  # set 0 value difference
                    spikes.append(0)  # cast value to 0
                    # print('___________________________________________________spikes0:', spikes)
                else:
                    spikes.append(1)  # cast value to 10.

                first_derivative.append(diff_sample)
                # print('diff_sample==', first_derivative)

                return spikes, first_derivative



# Decode the forces on Torque forces of the hand,
def callback_arm_actuals(data):
    global diff_sample_ty, diff_sample_tz
    workflow_state = WorkFlowStatePost(address, port, 'forth.hri.RobotAction', workFlow_json)

    # unpack values
    tx, ty, tz, fx, fy, fz = data.FTS_Wrench
    # print(tx, ty, tz, fx, fy, fz, '\n', ' dataFTS_Wrench :', data.FTS_Wrench)

    if tx:
        tx_list.append(tx)  # create list to iter and to rec
        if len(tx_list) > 3:
            tx_list.pop()
            spikes_tx, diff_sample_tx = diff_finder(data=tx_list, threshold=5)

    if ty:
        ty_list.append(ty)
        if len(ty_list) > 3:
            spikes_ty, diff_sample_ty = diff_finder(data=ty_list, threshold=5)
            ty_list.pop()
    if tz:
        tz_list.append(tz)
        if len(tz_list) > 3:
            spikes_tz, diff_sample_tz = diff_finder(data=tz_list, threshold=5)
            tz_list.pop()

    # recording for debug, set-to-0 stop rec
    if 1:
        pass
        rec_data2csv(diff_sample_tx, 'diff_sample')
        rec_data2csv(spikes_tx, 'spikes')


    samples = [diff_sample_tx, diff_sample_ty, diff_sample_tz]
    spikes = [spikes_tx, spikes_ty, spikes_tz]
    # method-1-fcn_Trigger
    sum_samples(samples[0],samples[1], samples[2], threshold=7)
    return samples, spikes

# Method 1 - sum(all_samples) # threshold = 7
def sum_samples(xi, yi, zi, threshold):

    # sample_list = [sum(diff_sample_tx), sum(diff_sample_ty), sum(diff_sample_tz)]
    sample_list = [sum(xi), sum(yi), sum(zi)]
    if sum(sample_list) > threshold:
        ai = True
        print('sum_samples= ', True)
    else:
        ai = False
        print('sum_samples= ', False)

    return ai


# function call
a = sum_samples(samples[0], diff_sample_ty, diff_sample_tz, threshold=7)
if a: print(a)


# Method 2(votes)
def spike_vote(*args, state):
    global release_state
    if release_state:
        ones = spikes_tx.count(1)
        zeros = spikes_tx.count(0)
        if len(ones) > len(zeros):
            pass

    # spike_vote(diff_sample_tx, tate=release_state)

# # call functions
spike_vote(spikes_tx, spikes_ty, spikes_tz)
########################################################
# Method 3( count binaries, 1)
# TODO how many ones(1) I have to count, i need to know how much(aprox)time
#  does it take to complete a move !
if len(bin) > 50 and handover_state==True:  # where 50 might be 5secs to complete a movement
    release_state=True


###################################
# def init_receiver():
#     # this listen  the response of release-command, and starts a spike detection
#     rospy.Subscriber('arm_actuals', arm_actuals, callback_arm_actuals)
#     rospy.loginfo("listen's arm_actual")
#     print(CMAG2, 'armActual_SpikeDetect', CEND)
#     rospy.spin()
#
#
# if __name__ == '__main__':
#     rospy.init_node('listen_armActual_SpikeDetect', anonymous=True)
#     init_receiver()
