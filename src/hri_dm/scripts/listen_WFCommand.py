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
from hri_dm.msg import HRIDM2TaskExecution, Pose2D
from handover_pos import *
# from reader_wfc import * # omitted for now
from _eq import *
request_number = 0
# from listen_TaskExec import test_goRobo2Human  # import from ROS-Module

robotAtWs = 10  # possible values -1: lost, 0: on navigation, WS10:10, WS20:20, WS30:30

# this is a new line

pub2TaskExe = rospy.Publisher('Task2Execute', HRIDM2TaskExecution, queue_size=100)
fiware_iccs = 'iccs.Hbu.PoseEstimation.WorkerPose'


# TODO evaluate if we need this Function(get_linkInfo) anymore.. ?
def get_linkInfo(wfc):
    """ query links for /v2/entities/ or parse whatever link we want,
     : mallon den tha usaroume"""
    r = requests.get("http://25.45.111.204:1026/v2/entities/" + str(wfc))
    print(r.status_code, 'first_query')
    action_link = r.json()['refAction']['value']
    action_r = requests.get("http://25.45.111.204:1026/v2/entities/" + str(action_link))
    print(action_r.status_code, 'second_query')
    action_name = action_r.json()['adaptType']['value']
    # params = r.json()['parameters']['value']['location']
    return r, action_name


def get_humanPose_ws(ws):
    """
     ws = Workstation number, ex.int: 1,2,3
    query ICCS for human pose,
    return x_hpose, y_hpose, orn_pose
    """

    obj = requests.get('http://25.45.111.204:1026/v2/entities/iccs.hbu.PoseEstimation.WorkerPose:00' + str(ws))
    x_hpose = obj.json()['position']['value']['x']['value']
    y_hpose = obj.json()['position']['value']['y']['value']
    orn_pose = obj.json()['orientation']['value']
    return x_hpose, y_hpose, orn_pose


def rob_goto_human(ws):
    """
    finds the direct/cross line between human and robot
    starts Pybullet for HRI, triggered by ICCS,
    found: is the status if link is dead or not.
    :param ws: workstation human is currently in
    :return: found, xf, yf, dir
    """

    # TODO  I assume this is for 2DPose, we query for this from ICCS or AEGIS?
    xf, yf, dir = 99999, 99999, 99999

    found = 0

    hx, hy, ho = get_humanPose_ws(ws)   # ICCS query
    rx, ry, ro = get_robotPose()
    pos_found, xf, yf = find_pos_Rel2Hum([rx, ry], [hx, hy], 1.1)
    if pos_found > 0:
        found = 1
        sol_l, a, b = linear_eq([xf, yf], [hx, hy])
        dir = np.arctan(a)
        print("direction=", dir)
        return found, xf, yf, dir
        # q=get_quaternion_from_euler(0, 0, thetaDeg, "R")
    else:
        print("don't know where the robot should be sent ------------------")
        return found, xf, yf, dir


def get_robotPose():
    """
    Robot Pose, query from ICS a 2D-position and orn.
    found: is the status if link is dead or not.
    :return: found, x_rpose, y_rpose, orn_rpose
    """
    obj = requests.get('http://25.45.111.204:1026/v2/entities/FORTH.ScenePerception.WorkFlow')
    found = 0
    if obj.status_code == 204:
        found = 1
        x_rpose = obj.json()['position']['value']['x']['value']
        y_rpose = obj.json()['position']['value']['y']['value']
        orn_rpose = obj.json()['orientation']['value']

    return found, x_rpose, y_rpose, orn_rpose


def get_xyo(obj):  # 4nameDLocation

    """ Activate when namedLocation from fiware,
     grabs - json, outputs x,y,orn, workspace """
    x_ws = obj.json()[0]['x']
    y_ws = obj.json()[0]['y']
    orn_ws = obj.json()[0]['orientation']
    return x_ws, y_ws, orn_ws

def get_robotWS():
    """
    Activates when "Navigate",
    appears from fiware, then query for Cobot_Current_WS,
     """
    obj = requests.get('http://25.17.36.113:2620/cobotloc')
    ws = obj.json()[0]['???ws??']  # TODO verify with (vaggelhs) AEGIS about json format
    # x, y, orn = get_xyo(obj) # palio apo allo function 8a to dle later
    return ws


def decode_named_location(obj):
    """
    Activates when "NamedLocation",
    appears from fiware, then query for pos/orn to,
    (a)HumanLocation
    (b)RobotArrival
    (c)ToolcaseLocation
     """

    # Adaptive Workstation AEGIS
    named_loc = obj['data'][0]['parameters']['value']['location']['namedLocation']
    print('object WORKSTATION ADAPTIVE', '\n', named_loc)
    if re.findall('AdapticeWS_Location', named_loc):
        cords_obj = requests.get('http://25.17.36.113:2620/awsloc')
        x, y, orn = get_xyo(cords_obj)

    elif re.findall('Human_Location_WS10', named_loc):
        cords_obj = requests.get('http://25.17.36.113:2620/humanlocws10')
        x, y, orn = get_xyo(cords_obj)

    elif re.findall('Human_Location_WS20', named_loc):
        cords_obj = requests.get('http://25.17.36.113:2620/humanlocws20')
        x, y, orn = get_xyo(cords_obj)

    elif re.findall('Human_Location_WS30', named_loc):
        cords_obj = requests.get('http://25.17.36.113:2620/humanlocws30')
        x, y, orn = get_xyo(cords_obj)

    # AEGIS
    if re.findall('Robot_Arrival_Location_WS10', named_loc):
        cords_obj = requests.get('http://25.17.36.113:2620/robot_arrival_ws10_loc')
        x, y, orn = get_xyo(cords_obj)
    elif re.findall('Robot_Arrival_Location_WS20', named_loc):
        cords_obj = requests.get('http://25.17.36.113:2620/robot_arrival_ws20_loc')
        x, y, orn = get_xyo(cords_obj)

    elif re.findall('Robot_Arrival_Location_WS30', named_loc):
        cords_obj = requests.get('http://25.17.36.113:2620/robot_arrival_ws30_loc')
        x, y, orn = get_xyo(cords_obj)

    elif re.findall('Toolcase_Location_WS10', named_loc):
        cords_obj = requests.get('http://25.17.36.113:2620/toolcaselocws10')
        x, y, orn = get_xyo(cords_obj)

    elif re.findall('Toolcase_Location_WS20', named_loc):
        cords_obj = requests.get('http://25.17.36.113:2620/toolcaselocws20')
        x, y, orn = get_xyo(cords_obj)

    elif re.findall('Toolcase_Location_WS30', named_loc):
        cords_obj = requests.get('http://25.17.36.113:2620/toolcaselocws30')
        x, y, orn = get_xyo(cords_obj)

    # omited for now one robot currently we have.
    # elif re.findall('Cobot_Current_WS', named_loc):
    #     obj = requests.get('http://25.17.36.113:2620/cobotloc')
    #     x, y, orn = get_xyo(obj)

    return x, y, orn

### ROS-Message and Routines, (release, pickup, handover, navigate)

def send_ROSmsg_release():
    global pub2TaskExe, request_number
    task_exec = HRIDM2TaskExecution()
    task_exec.action = 'release'  # action
    task_exec.tool_id = -1
    # location/vector3 geom_msgs location
    # task_exec.location.x = 99999 # not used by us in release
    # task_exec.location.y = 99999 # not used by us in release
    # task_exec.location.z = 99999 # not used by us in release
    # location/nav Pose2D
    task_exec.navpos.x = 0
    task_exec.navpos.y = 0
    task_exec.navpos.theta = 0.0
    # synchronization
    request_number = request_number+1
    task_exec.request_id = request_number
    pub2TaskExe.publish(task_exec)
    # print(task_exec, '\n', 'received')


def send_ROSmsg_pickup(obj):
    global pub2TaskExe, request_number
    task_exec = HRIDM2TaskExecution()
    task_exec.action = 'pickup'  # action
    task_exec.tool_id = int(obj['data'][0]['parameters']['value']['tool']['toolId'])
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
    request_number = request_number+1
    task_exec.request_id = request_number
    pub2TaskExe.publish(task_exec)
    # print(task_exec, '\n', 'received')


def send_ROSmsg_handover(obj):
    global pub2TaskExe, request_number
    ws = 1  # refers to workStation
    workerx, workery, workertheta = get_humanPose_ws(
        ws)  # get worker position and theta in the global coordinate system

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
    request_number = request_number+1
    task_exec.request_id = request_number
    pub2TaskExe.publish(task_exec)
    # print(task_exec, '\n', 'handOver_task')


def send_ROSmsg_navigate(obj):
    global pub2TaskExe, request_number
    task_exec = HRIDM2TaskExecution()
    task_exec.action = 'navigate'  # action
    # task_exec.tool_id = int(obj['data'][0]['parameters']['value']['tool']['toolId']) # not usable for nav.
    # location/vector3 geom_msgs location
    # task_exec.location.x = 9999
    # task_exec.location.y = 9999
    # task_exec.location.z = 9999

    # location/nav Pose2D # navigation for ICS and Aegis colab
    location_name = obj['data'][0]['parameters']['value']['location']['namedLocation']
    print("  Navigation Module : going to .... location_name:", location_name)
    pass
    # bear in mind [timestamp] for future debugs, network latency might or not.
    xf, yf, dir = decode_named_location(obj)
    if re.findall('Human_Location', location_name):
        ws = get_robotWS()
        found, xf, yf, dir = rob_goto_human(ws)
        if found < 1:
            print("ERROR  !!!!!!! please check")

    task_exec.navpos.x = xf
    task_exec.navpos.y = yf
    task_exec.navpos.theta = dir
    # synchronization
    request_number = request_number + 1
    task_exec.request_id = request_number
    pub2TaskExe.publish(task_exec)


# Intercepts incoming messages
class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        datalen = int(self.headers['Content-Length'])  # size receive message
        data = self.rfile.read(datalen)  # read receive messages
        obj = json.loads(data)  # convert message to json
        sender_module = obj['data'][0]['id']
        # print(obj['data'][0])

        if re.findall('forth.hri.RobotAction', sender_module):
            # print(CYEL1, obj['data'][0]['type'], CEND)
            # print(obj)
            print(CYEL1, "navigate:", obj['data'][0]['a_navigate']['value']['state']['value'])
            print(" pickup :", obj['data'][0]['a_grasp']['value']['state']['value'])
            print(" handover :", obj['data'][0]['a_handover']['value']['state']['value'])
            print(" release :", obj['data'][0]['a_releaseTool']['value']['state']['value'],
                  CEND)

        elif re.findall('UNISA.SpeechGestureAnalysis.Speech', sender_module):
            print(CBLUE2, obj['data'][0]['command']['value'], CEND)
            if obj['data'][0]['command']['value'] == 3:
                print('send_ROSmsg_release')
                send_ROSmsg_release()
                print(CBLUE2, "SGA.Speech received", CEND)

        elif re.findall('AEGIS.Visualizations', sender_module):
            print(CBLUE2, obj['data'][0]['command']['value'], CEND)
            if obj['data'][0]['command']['value'] == "True":
                send_ROSmsg_release()
                print(CBlUE1, "release sent", CEND)

        elif re.findall('SystemHealth', sender_module):
            print(CGR1, obj['data'][0]['id'], CEND)

        elif re.findall('WorkflowCommand', sender_module):
            action_type = obj['data'][0]['actionType']['value']
            print('ACTION_TYPE', action_type)
            if action_type == 'release':
                print(CBlUE1, 'send_ROSmsg_release', CEND)
                send_ROSmsg_release()

            elif action_type == 'pickup':
                print(CBlUE1, 'send_ROSmsg_pickup', CEND)
                send_ROSmsg_pickup(obj)

            elif action_type == 'handover':
                print(CBlUE1, 'send_ROSmsg_handover', CEND)
                send_ROSmsg_handover(obj)

            elif action_type == 'navigate':
                print(CBlUE1, 'send_ROSmsg_navigate', CEND)
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
m_selection_address = '172.21.229.83'  # '25.28.181.178'

r_selection_address = '25.28.181.178'

# Broker
selection_port_CB = '1026'
selection_address_CB = '192.168.1.104'  # '25.45.111.204'

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
print("user=", user)

Log("INFO", "Initialized")
# ROS INIT NODE
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
