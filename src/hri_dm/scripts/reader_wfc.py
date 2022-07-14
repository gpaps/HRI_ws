import re
import requests
import time
import json
link = 'FHOOE.Orchestrator.Runtime.WorkflowCommand:c25785b9-614f-48b2-88f3-45e1e2371507'


# from scripts.listen_fiwareFORTH import send_msg

def get_hash():
    cc = time.time()
    return hash(cc) % 9999999999


def get_linkInfo(wf):
    r = requests.get('http://25.45.111.204:1026/v2/entities/' + str(wf))
    r_action = r.json()['actionType']['value']
    print(r_action, )
    return r, r_action

# def obj_checker(obj):
#     return obj.json()['actionType']['value']


def entity_checker(r, link, r_act):
    if re.findall('WorkflowCommand', link):
        return dm_action(r_act, r)


def _locationParams(r):
    return print(r.json()['parameters']['value']['location']['namedLocation'])


def dm_action(r_action, r):
    if r_action == 'release':
        print('release received.')

        # send_msg()
    elif r_action == 'pickup':
        print('release pickup.')
        # action
        # tool_id="tool123"
        # location
        # navpos
        # request_id

    elif r_action == 'navigate':
        # action
        # tool_id=""
        # location
        # navpos
        # request_id

        print('navigate received.')
        _locationParams(r)
        # r.json()['parameters']['value']['location']['namedLocation']


    elif r_action == 'grasp':
        print('grasp received.')

    return r_action,


if __name__ == '__main__':
    r, r_act = get_linkInfo(link)
    entity_checker(r, link, r_act)
