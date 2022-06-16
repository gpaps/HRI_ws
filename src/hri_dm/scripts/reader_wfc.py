import requests
link = 'FHOOE.Orchestrator.Runtime.WorkflowCommand:c25785b9-614f-48b2-88f3-45e1e2371507'
# from scripts.listen_fiwareFORTH import send_msg

def get_linkInfo(wf):
    r = requests.get('http://25.45.111.204:1026/v2/entities/' + str(wf))
    r_action = r.json()['actionType']['value']
    return r, r_action


def dm_action(r_action):

    if r_action == 'release':
        print('release received.')
        # send_msg()
    elif r_action == 'pickup':
        print('release pickup')

    elif r_action == 'navigate':
        print('navigate received')

    elif r_action == 'grasp':
        print('grasp received')

    return r_action
if __name__ == '__main__':
    r, r_act = get_linkInfo(link)

    action_received = dm_action(r_act)
    print('here')