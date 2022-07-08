import json
import requests
# import random
# import uuid
from datetime import datetime, timedelta
import time
import sys
import rospy
# import argparse
import numpy as np

CB_HEADER = {'Content-Type': 'application/json'}
CB_BASE_URL = None

# '25.28.118.246'

address = '25.45.111.204'
port = 1026


class WorkFlow:

    def __init__(self):
        pass


class WorkFlowStatePost(WorkFlow):

    def __init__(self, address, port, entity_path, json_fname):

        self.address = address
        self.port = port
        self.CB_BASE_URL = "http://{}:{}/v2/".format(self.address, self.port)
        self.uuid = []

        self.json_action_message = []
        self.json_message = []

        f = open(json_fname, 'r')  # encoding="cp866")
        self.json_message = json.load(f)
        self.json_message['id'] = entity_path
        self.json_message['type'] = 'RobotAction'

    def updateStateMsg_pickup(self, state, result, toolID=None, x=None, y=None, z=None):
        if toolID is not None:
            self.json_message['a_grasp']['value']['toolID']['value'] = toolID
        else:
            print("PEIRA NONE _______PICKUP______")
        if x is not None:
            self.json_message['a_grasp']['value']['x']['value'] = x
        if y is not None:
            self.json_message['a_grasp']['value']['y']['value'] = y
        if z is not None:
            self.json_message['a_grasp']['value']['z']['value'] = z

        if state is True:
            self.json_message['a_grasp']['value']['state']['value'] = 'active'
        else:
            self.json_message['a_grasp']['value']['state']['value'] = 'inactive'
        if result > 0:
            self.json_message['a_grasp']['value']['result']['value'] = 'success'
        elif result < 0:
            self.json_message['a_grasp']['value']['result']['value'] = 'fail'
        else:
            self.json_message['a_grasp']['value']['result']['value'] = 'unknown'
        # print(x, y, z, state, result)

        self.json_action_message = {"actionType": "append", "entities": [self.json_message]}
        # self.json_action_message = {"actionType": "update", "entities": [self.json_message]}
        msg = json.dumps(self.json_action_message)
        # print(msg)
        response = requests.post(self.CB_BASE_URL + "op/update", data=msg, headers=CB_HEADER)

        if response.ok:  # response successful
            print("CB response -> status " + response.status_code.__str__())
        else:  # response ok
            print("CB response -> " + response.text)

    def updateStateMsg_nav(self, state, result, x=None, y=None, theta=None):
        if x is not None:
            self.json_message['a_navigate']['value']['x']['value'] = x
        else:
            print("PEIRA NONE ______NAVIGATION________")
        if y is not None:
            self.json_message['a_navigate']['value']['y']['value'] = y
        if theta is not None:
            self.json_message['a_navigate']['value']['theta']['value'] = theta

        if state is True:
            self.json_message['a_navigate']['value']['state']['value'] = 'active'
        else:
            self.json_message['a_navigate']['value']['state']['value'] = 'inactive'
        if result > 0:
            self.json_message['a_navigate']['value']['result']['value'] = 'success'
        elif result < 0:
            self.json_message['a_navigate']['value']['result']['value'] = 'fail'
        else:
            self.json_message['a_navigate']['value']['result']['value'] = 'unknown'
        # print(x, y, theta, state, result)

        self.json_action_message = {"actionType": "append", "entities": [self.json_message]}
        # self.json_action_message = {"actionType": "update", "entities": [self.json_message]}
        msg = json.dumps(self.json_action_message)
        # print(msg)
        response = requests.post(self.CB_BASE_URL + "op/update", data=msg, headers=CB_HEADER)

        if response.ok:  # response successful
            print("CB response -> status " + response.status_code.__str__())
        else:  # response ok
            print("CB response -> " + response.text)

    def updateStateMsg_handover(self, state, result, toolID=None, x=None, y=None, z=None):
        if toolID is not None:
            self.json_message['a_handover']['value']['toolID']['value'] = toolID
        else:
            print('PEIRA NONE ___________HANDOVER__________')
        if x is not None:
            self.json_message['a_handover']['value']['x']['value'] = x
        if y is not None:
            self.json_message['a_handover']['value']['y']['value'] = y
        if z is not None:
            self.json_message['a_handover']['value']['z']['value'] = z

        if state is True:
            self.json_message['a_handover']['value']['state']['value'] = 'active'
        else:
            self.json_message['a_handover']['value']['state']['value'] = 'inactive'
        if result > 0:
            self.json_message['a_handover']['value']['result']['value'] = 'success'
        elif result < 0:
            self.json_message['a_handover']['value']['result']['value'] = 'fail'
        else:
            self.json_message['a_handover']['value']['result']['value'] = 'unknown'
        # print(x, y, z, state, result)

        self.json_action_message = {"actionType": "append", "entities": [self.json_message]}
        # self.json_action_message = {"actionType": "update", "entities": [self.json_message]}
        msg = json.dumps(self.json_action_message)
        # print(msg)
        response = requests.post(self.CB_BASE_URL + "op/update", data=msg, headers=CB_HEADER)

        if response.ok:  # response successful
            print("CB response -> status " + response.status_code.__str__())
        else:  # response ok
            print("CB response -> " + response.text)

    def updateStateMsg_release(self, state, result, tool_id=None):
        if tool_id is not None:
            self.json_message['a_releaseTool']['value']['toolID']['value'] = tool_id
        else:
            print('PEIRA NONE ___________ReleaseEEE__________')

        if state is True:
            self.json_message['a_releaseTool']['value']['state']['value'] = 'active'
        else:
            self.json_message['a_releaseTool']['value']['state']['value'] = 'inactive'

        if result > 0:
            self.json_message['a_releaseTool']['value']['result']['value'] = 'success'
        elif result < 0:
            self.json_message['a_releaseTool']['value']['result']['value'] = 'fail'
        else:
            self.json_message['a_releaseTool']['value']['result']['value'] = 'unknown'


        self.json_action_message = {"actionType": "append", "entities": [self.json_message]}
        # self.json_action_message = {"actionType": "update", "entities": [self.json_message]}
        msg = json.dumps(self.json_action_message)
        # print(msg)
        response = requests.post(self.CB_BASE_URL + "op/update", data=msg, headers=CB_HEADER)

        if response.ok:  # response successful
            print("CB response -> status " + response.status_code.__str__())
        else:  # response ok
            print("CB response -> " + response.text)

    # # TODO Do we need it @Michalis? Same as the above!
    # def updateState_release(self, state, result, tool_id=None):
    #     if state is True:
    #         self.json_message['a_releaseTool']['value']['state']['value'] = 'active'
    #     else:
    #         self.json_message['a_releaseTool']['value']['state']['value'] = 'inactive'
    #
    #     if result > 0:
    #         self.json_message['a_releaseTool']['value']['result']['value'] = 'success'
    #     elif result < 0:
    #         self.json_message['a_releaseTool']['value']['result']['value'] = 'fail'
    #     else:
    #         self.json_message['a_releaseTool']['value']['result']['value'] = 'unknown'
    #
    #
    #     self.json_action_message = {"actionType": "append", "entities": [self.json_message]}
    #     # self.json_action_message = {"actionType": "update", "entities": [self.json_message]}
    #     msg = json.dumps(self.json_action_message)
    #     # print(msg)
    #     response = requests.post(self.CB_BASE_URL + "op/update", data=msg, headers=CB_HEADER)
    #
    #     if response.ok:  # response successful
    #         print("CB response -> status " + response.status_code.__str__())
    #     else:  # response ok
    #         print("CB response -> " + response.text)

if __name__ == "__main__":
    pass
