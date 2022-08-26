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


class PlanePose:

    def __init__(self):
        pass


class PlanePoseStatePost(PlanePose):

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
        self.json_message['type'] = 'WorkFlow'

    def updateStateMsg(self, x, y, theta):

        self.json_message['position']['value']['x']['value'] = x
        self.json_message['position']['value']['y']['value'] = y
        self.json_message['orientation']['value'] = theta

        # print(x, y, theta)

        self.json_action_message = {"actionType": "append", "entities": [self.json_message]}
        # self.json_action_message = {"actionType": "update", "entities": [self.json_message]}
        msg = json.dumps(self.json_action_message)
        # print(msg)
        response = requests.post(self.CB_BASE_URL + "op/update", data=msg, headers=CB_HEADER)

        if response.ok:  # response successful
            print("CB response -> status " + response.status_code.__str__())
        else:  # response ok
            print("CB response -> " + response.text)

if __name__ == "__main__":
    pass
