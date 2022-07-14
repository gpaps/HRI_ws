import re
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
##colors
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
##colors

#insert new comment

pub2TaskExe = rospy.Publisher('Task2Execute', HRIDM2TaskExecution, queue_size=100)
fiware_iccs = 'iccs.Hbu.PoseEstimation.WorkerPose'

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
    pub2TaskExe.publish(task_exec)
    # print(task_exec, '\n', 'received')

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
    # print(task_exec, '\n', 'received')

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
    # print(task_exec, '\n', 'handOver_task')

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
    print("going to ....", location_name)
    xf=99999
    yf=99999
    dir=99999
    if re.findall('HumanLocation', location_name):
        ws=1
        hx, hy, ho = get_humanPose_ws(ws)
        rx, ry, ro = get_robotPose()
        pos_found, xf, yf = find_pos_Rel2Hum([rx, ry], [hx, hy], 1.1)
        if pos_found > 0:
            sol_l, a, b = linear_eq([xf, yf], [hx,hy])
            dir = np.arctan(a)
            print("direction=", dir)
            # q=get_quaternion_from_euler(0, 0, thetaDeg, "R")
        else:
            print("don't know where the robot should be sent ------------------")

    print('Location_Name__________', location_name)
    task_exec.navpos.x = xf
    task_exec.navpos.y = yf
    task_exec.navpos.theta = dir
    # synchronization
    task_exec.request_id = -1
    pub2TaskExe.publish(task_exec)
    # print(task_exec, '\n', 'navigate')

def get_humanPose_ws(ws):
    """ ws = WorkStation-number, ex.int: 1,2,3 """
    obj = requests.get('http://25.45.111.204:1026/v2/entities/iccs.hbu.PoseEstimation.WorkerPose:00' + str(ws))
    orn = obj.json()['orientation']['value']
    x = obj.json()['position']['value']['x']['value']
    y = obj.json()['position']['value']['y']['value']
    return x, y, orn

def get_robotPose():
    """ ws = WorkStation-number, ex.int: 1,2,3 """
    obj = requests.get('http://25.45.111.204:1026/v2/entities/FORTH.ScenePerception.WorkFlow')

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
        sender_module = obj['data'][0]['id']

        if re.findall('forth.hri.RobotAction', sender_module):
            # print(CYEL1, obj['data'][0]['type'], CEND)
            # print(obj)
            print(CYEL1, "navigate:",obj['data'][0]['a_navigate']['value']['state']['value'])
            print("grasp:",obj['data'][0]['a_grasp']['value']['state']['value'])
            print("handover:",obj['data'][0]['a_handover']['value']['state']['value'])
            print("release:",obj['data'][0]['a_releaseTool']['value']['state']['value'],
                  CEND)

        elif re.findall('AEGIS.Visualizations', sender_module):
            print(CRED1, obj['data'][0]['command']['value'], CEND)
            if obj['data'][0]['command']['value'] == "True":
                send_ROSmsg_release()

                print(CRED1, "release sent", CEND)

        elif re.findall('SystemHealth', sender_module):
            print(CGR1, obj['data'][0]['id'], CEND)

        elif re.findall('WorkflowCommand', sender_module):
            action_type = obj['data'][0]['actionType']['value']
            print('ACTION_TYPE', action_type)
            if action_type == 'release':
                print('send_ROSmsg_release')
                send_ROSmsg_release()

            elif action_type == 'pickup':
                print('send_ROSmsg_pickup')
                send_ROSmsg_pickup(obj)

            elif action_type == 'handover':
                print('send_ROSmsg_handover')
                send_ROSmsg_handover(obj)

            elif action_type == 'navigate':
                print('send_ROSmsg_navigate')
                send_ROSmsg_navigate(obj)

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
        # Log("INFO", "\nServing HTTP on", sa[0], "port", sa[1], "...")

        while not self.stopped:
            self.httpd.handle_request()
            print("in loop....")

    def close(self):  # Stop server method
        self.stopped = True


# CB_HEADER = {'Content-Type': 'application/json'}
# CB_BASE_URL = None
# selection_port = None
# selection_address = None

initLog()

# Input data acquisition
selection_port = '2620'
g_selection_address = '25.28.115.246'
#
m_selection_address = '172.21.229.83' #'25.28.181.178'

r_selection_address = '25.28.181.178'


# Broker
selection_port_CB = '1026'
selection_address_CB = '192.168.1.104' #'25.45.111.204'

######
# Test
# obj =  requests.get("")
# obj = requests.get("http://25.45.111.204:1026/v2/entities/" + str(fiware_iccs))
# action_type = obj.json()['actionType']['value']
# obj = json.loads(data)  # convert message to json
######

#########

try:
    user = sys.argv[1]
except IndexError:
    print(CYEL1, "------------------ No user Defined---------------")
    print("start with default user: g")
    print("---------------------     ---------------------", CEND)
    user = "g"
print ("user=", user)

Log("INFO", "Initialized")
rospy.init_node('fiware_ListenerFORTH', anonymous=True)
# Start server, receive message
try:
    if user == "g":
        server = MyReceiver(g_selection_address, int(selection_port))
    elif user == "m":
        server = MyReceiver(m_selection_address, int(selection_port))
    elif user == "r":
        print(CRED2, "------------------ the Robot IP is not Defined---------------")
        print("using michalis IP... ")
        print("---------------------     ---------------------", CEND)
        server = MyReceiver(r_selection_address, int(selection_port))
    else:
        print("Exit due to Unknown User")
        quit()
except Exception as ex:
    raise Exception("Unable to create a Receiver, check User-specification option")
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
