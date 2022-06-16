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

'25.28.118.246'

address = '25.45.111.204'
port = 1026


class HRI_Health:

    def __init__(self):
        pass


class HRI_HealthStatePost(HRI_Health):

    def __init__(self, address, port, json_fname=[]):

        self.address = address
        self.port = port
        self.CB_BASE_URL = "http://{}:{}/v2/".format(self.address, self.port)
        self.uuid = []

        self.json_action_message = []
        self.json_message = []

        f = open(json_fname, 'r')  # encoding="cp866")
        self.json_message = json.load(f)
        self.json_message['id'] = 'forth.hri_testTranslate.SystemHealth:001'
        self.json_message['type'] = 'SystemHealth'

    def updateStateMsg(self, status_str, time_str):

        self.json_message['status']['value'] = status_str
        self.json_message['timestamp']['value'] = time_str

        print(status_str, time_str)

        self.json_action_message = {"actionType": "append", "entities": [self.json_message]}
        # self.json_action_message = {"actionType": "update", "entities": [self.json_message]}
        msg = json.dumps(self.json_action_message)
        print(msg)
        response = requests.post(self.CB_BASE_URL + "op/update", data=msg, headers=CB_HEADER)

        if response.ok:  # response successful
            print("CB response -> status " + response.status_code.__str__())
        else:  # response ok
            print("CB response -> " + response.text)


if __name__ == "__main__":

    robotAction_jsonFName = 'health.json'
    hriStateTest = HRI_HealthStatePost(address, port, robotAction_jsonFName)
    sleepSecs = 4  # seconds to sleep before sending another message
    position = [0.0, 0.0]
    while True:
        time.sleep(sleepSecs)
        # my_date = datetime.now() # this is for local time
        my_date = datetime.utcnow()  # utc time, this is used in FELICE
        print(my_date.isoformat())

        hriStateTest.updateStateMsg("OK", str(my_date.isoformat()))