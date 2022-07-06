import sys
import json

import reportlab.pdfbase.pdfmetrics

import rospy
import signal
import requests
from reader_wfc import *
from logger import Log, initLog
from http.server import HTTPServer  # this is for use with python3
from http.server import BaseHTTPRequestHandler  # this is for use with python3
from hri_dm.msg import HRIDM2TaskExecution, TaskExecution2HRIDM
from handover_pos import *
# from reader_wfc import * # omitted for now
from _eq import *

pub2TaskExe = rospy.Publisher('Task2Execute', HRIDM2TaskExecution, queue_size=100)

fiware_iccs = 'iccs.Hbu.PoseEstimation.WorkerPose'
link_pickup = 'FHOOE.Orchestrator.Runtime.WorkflowCommand:8a81ceca-06ef-425d-8f86-9309c39103ea'
link_navigate = 'FHOOE.Orchestrator.Runtime.WorkflowCommand:c25785b9-614f-48b2-88f3-45e1e2371507'
link_release = 'FHOOE.Orchestrator.Runtime.WorkflowCommand:4d0f5c32-8db6-49cb-b5ef-2af7d492ca12'
link_handover = 'FHOOE.Orchestrator.Runtime.WorkflowCommand:d8076bf9-bc2e-4bb3-89cd-052c79f2c3b5'


def get_adaptId(wfc):
    r = requests.get("http://25.45.111.204:1026/v2/entities/" + str(wfc))
    print(r.status_code, 'first_query')
    action_link = r.json()['refAction']['value']
    action_r = requests.get("http://25.45.111.204:1026/v2/entities/" + str(action_link))
    print(action_r.status_code, 'second_query')
    action_name = action_r.json()['adaptType']['value']
    # params = r.json()['parameters']['value']['location']
    return r, action_name

def send_ROSmsg_release():
    global pub2TaskExe
    task_exec = HRIDM2TaskExecution()
    task_exec.action = 'release'  # action
    task_exec.tool_id = -1
    # location/vector3 geom_msgs location
    task_exec.location.x = 99999
    task_exec.location.y = 99999
    task_exec.location.z = 99999
    # location/nav Pose2D
    task_exec.navpos.x = 0
    task_exec.navpos.y = 0
    task_exec.navpos.theta = 0.0
    # synchronization
    task_exec.request_id = -1
    print(task_exec, '\n', 'received')

def send_ROSmsg_pickup(obj):
    global pub2TaskExe
    task_exec = HRIDM2TaskExecution()
    task_exec.action = 'pickup'  # action

    task_exec.tool_id = int(obj['data'][0]['parameters']['value']['tool']['toolId']) # TODO to receive and publish
    # print('TOOL_____ID', task_exec.tool_id)
    # location/vector3 geom_msgs location
    task_exec.location.x = 99999
    task_exec.location.y = 99999
    task_exec.location.z = 99999
    # location/nav Pose2D
    task_exec.navpos.x = 99999
    task_exec.navpos.y = 99999
    task_exec.navpos.theta = 99999
    # synchronization
    task_exec.request_id = 99
    pub2TaskExe.publish(task_exec)
    print(task_exec, '\n', 'received')

def send_ROSmsg_handover(obj):
    global pub2TaskExe
    ws = 1  # refers to workStation
    workerx, workery, workertheta = get_humanPose_ws(ws)  # get worker position and theta in the global coordinate system

    # pb_x = find_HO_pos(x, y)   # pyBullet # locX, locY, locZ = x[0][0], x[0][1], x[0][2]
    # use the old version without translation in pybullet
    p3d_x, p3d_y, p3d_z = find_HandOver_pos()  # pyBullet, this is the handover location in the human coordinate system
    rlocalx, rlocaly = rotate(p3d_x, p3d_y, workertheta)  # rotate handover location by the human-theta

    task_exec = HRIDM2TaskExecution()
    task_exec.action = 'handover'  # action
    task_exec.tool_id = int(obj['data'][0]['parameters']['value']['tool']['toolId'])
    # print('TOOL_ID_________Handover ',task_exec.tool_id)
    # location/vector3 geom_msgs location
    task_exec.location.x = workerx + rlocalx  # this is the handover location in the global coordinate system
    task_exec.location.y = workery + rlocaly  # this is the handover location in the global coordinate system
    task_exec.location.z = p3d_z  # the z is not affected by the rotation of the human
    # location/nav Pose2D
    # task_exec.navpos.x = x
    # task_exec.navpos.y = y
    # task_exec.navpos.theta = theta  # counterclockwise
    # synchronization
    task_exec.request_id = -1
    pub2TaskExe.publish(task_exec)
    print(task_exec, '\n', 'handOver_task')

def send_ROSmsg_navigate(obj):
    global pub2TaskExe
    task_exec = HRIDM2TaskExecution()
    task_exec.action = 'navigate'  # action
    # task_exec.tool_id = int(obj['data'][0]['parameters']['value']['tool']['toolId']) # not usable for nav.
    # location/vector3 geom_msgs location
    task_exec.location.x = 9999
    task_exec.location.y = 9999
    task_exec.location.z = 9999
    # location/nav Pose2D
    location_name = obj['data'][0]['parameters']['value']['location']['namedLocation']
    print('Location_Name__________', location_name)
    task_exec.navpos.x = 9999
    task_exec.navpos.y = 9999
    task_exec.navpos.theta = 9999
    # synchronization
    task_exec.request_id = -1
    pub2TaskExe.publish(task_exec)
    print(task_exec, '\n', 'navigate')

def get_humanPose_ws(ws):
    """ ws = WorkStation-number, ex.int: 1,2,3 """
    obj = requests.get('http://25.45.111.204:1026/v2/entities/iccs.hbu.PoseEstimation.WorkerPose:00' + str(ws))
    orn = obj.json()['orientation']['value']
    x = obj.json()['position']['value']['x']['value']
    y = obj.json()['position']['value']['y']['value']
    return x, y, orn

def rotate(x, y, theta):
    xn = x * math.cos(theta) + y * math.sin(theta)
    yn = -x * math.sin(theta) + y * math.cos(theta)
    return xn, yn


# Intercepts incoming messages
class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        datalen = int(self.headers['Content-Length'])  # size receive message
        data = self.rfile.read(datalen)  # read receive messages
        obj = json.loads(data)  # convert message to json
        # obj = requests.get("http://25.45.111.204:1026/v2/entities/" )#+ str(link_handover))
        print(obj)
        sender_module = obj['data'][0]['id']
        print(sender_module, '_______')
        if re.findall('WorkerPose', sender_module):
            pass
            print('KOSTAS IS HERE !!!!', )

        elif re.findall('SystemHealth', sender_module):
            pass

        elif re.findall('WorkflowCommand', sender_module):
            print('WORKFLOW COMMAND IS HERE!!!')

            action_type = obj['data'][0]['actionType']['value']
            print('ACTION_TYPE', action_type)

            if action_type == 'release':
                send_ROSmsg_release()

            elif action_type == 'pickup':
                send_ROSmsg_pickup(obj)

            elif action_type == 'handover':
                send_ROSmsg_handover(obj)

            elif action_type == 'navigate':
                send_ROSmsg_navigate(obj)

        # else:
        #     action_type = obj.json()['actionType']['value']
        #     if action_type == 'release':
        #         send_msg_release()
        #     elif action_type == 'pickup':
        #         send_msg_pickup(obj)
        #     elif action_type == 'handover':
        #         send_msg_handover()
        #     elif action_type == 'navigate':
        #         send_msg_navigate()

        print('___________________')
        # this is to place the code

        # Here add thr code for processing.
        print(" Received Fiware Msg ")

        # Log("INFO", json.dumps(obj, indent=4, sort_keys=True))  # print receive messages
        self.send_response(200)
        self.end_headers()


class MyReceiver:
    def __init__(self, address="0.0.0.0", port=8080):
        self.address = address
        self.port = port
        self.stopped = False
        Protocol = "HTTP/1.0"

        # set ip and port my server
        server_address = (self.address, self.port)

        # initialize RequestHandler
        RequestHandler.protocol_version = Protocol
        self.httpd = HTTPServer(server_address, RequestHandler)

    def start(self):  # Start server method
        sa = self.httpd.socket.getsockname()
        Log("INFO", "\nServing HTTP on", sa[0], "port", sa[1], "...")

        while not self.stopped:
            print("inloop")
            self.httpd.handle_request()
            print("inloop....2")

    def close(self):  # Stop server method
        self.stopped = True


# CB_HEADER = {'Content-Type': 'application/json'}
# CB_BASE_URL = None
# selection_port = None
# selection_address = None

initLog()

# Input data acquisition
selection_port = '2620'
selection_address = '25.28.115.246'
selection_port_CB = '1026'
selection_address_CB = '25.45.111.204'

######
# Test
# obj =  requests.get("")
# obj = requests.get("http://25.45.111.204:1026/v2/entities/" + str(fiware_iccs))
# action_type = obj.json()['actionType']['value']
# obj = json.loads(data)  # convert message to json
######

#########
Log("INFO", "Initialized")
rospy.init_node('fiware_ListenerFORTH', anonymous=True)
# Start server, receive message
try:
    # send_msg_release()
    server = MyReceiver(selection_address, int(selection_port))
except Exception as ex:
    raise Exception("Unable to create a Receiver")
else:  # close application and server
    def signal_handler(signal, frame):
        Log("INFO", '\nExiting from the application')
        server.close()
        Log("INFO", '\nExit')
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

Log("INFO", "\nStarting...")
Log("INFO", "---------------------------------\n")
server.start()
