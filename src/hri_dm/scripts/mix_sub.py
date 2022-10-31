import sys
import requests

# Input data acquisition
CB_HEADER = {'Content-Type': 'application/json'}
selection_port = '2620'
selection_address = '53.54.56.159'  #'25.28.181.178'  # custom_hamachi IP
selection_port_CB = '1026'
selection_address_CB = '192.168.2.106' #'25.45.111.204', '192.168.1.106'

# subscription
msg_FORTH_HRI = "{" \
      "    \"description\": \"FORTH-U20a\",\n" \
      "    \"subject\": {\n" \
      "        \"entities\":\n" \
      "        [{\n" \
      "            \"idPattern\": \"forth.hri.*\",\n" \
      "            \"typePattern\": \".*\"\n" \
      "        }],\n" \
      "        \"conditions\": {\n" \
      "            \"attrs\": []\n" \
      "        }\n" \
      "    },\n" \
      "    \"notification\": {\n" \
      "        \"http\": {\n" \
      "            \"url\": \""+selection_address+":2620/\",\n" \
      "            \"method\": \"POST\",\n" \
      "            \"headers\": {\n" \
      "                \"Content-Type\": \"application/json\"\n" \
      "            }\n" \
      "        }\n" \
      "    }\n}"

# subscription
msg_FORTH_ScenePerception = "{" \
       "    \"description\": \"FORTH-U20b\",\n" \
       "    \"subject\": {\n" \
       "        \"entities\":\n" \
       "        [{\n" \
       "            \"idPattern\": \"FORTH.ScenePerception.*\",\n" \
       "            \"typePattern\": \".*\"\n" \
       "        }],\n" \
       "        \"conditions\": {\n" \
       "            \"attrs\": []\n" \
       "        }\n" \
       "    },\n" \
       "    \"notification\": {\n" \
       "        \"http\": {\n" \
       "         \"url\": \""+selection_address+":2620/\",\n" \
       "            \"method\": \"POST\",\n" \
       "            \"headers\": {\n" \
       "                \"Content-Type\": \"application/json\"\n" \
       "            }\n" \
       "        }\n" \
       "    }\n}"

# subscription
msg_FHOE = "{" \
       "    \"description\": \"FORTH-U20c\",\n" \
       "    \"subject\": {\n" \
       "        \"entities\":\n" \
       "        [{\n" \
       "            \"idPattern\": \"FHOOE.Orchestrator.*\",\n" \
       "            \"typePattern\": \".*\"\n" \
       "        }],\n" \
       "        \"conditions\": {\n" \
       "            \"attrs\": []\n" \
       "        }\n" \
       "    },\n" \
       "    \"notification\": {\n" \
       "        \"http\": {\n" \
       "         \"url\": \"" + selection_address + ":2620/\",\n" \
       "            \"method\": \"POST\",\n" \
       "            \"headers\": {\n" \
       "                \"Content-Type\": \"application/json\"\n" \
       "            }\n" \
       "        }\n" \
       "    }\n}"

CB_BASE_URL = "http://{}:{}/".format(selection_address_CB, selection_port_CB)  # url send notification

# subscription
msg_AEGIS_ButtonPress = "{" \
       "    \"description\": \"FORTH-U20c\",\n" \
       "    \"subject\": {\n" \
       "        \"entities\":\n" \
       "        [{\n" \
       "            \"idPattern\": \"AEGIS.Visualizations.*\",\n" \
       "            \"typePattern\": \".*\"\n" \
       "        }],\n" \
       "        \"conditions\": {\n" \
       "            \"attrs\": []\n" \
       "        }\n" \
       "    },\n" \
       "    \"notification\": {\n" \
       "        \"http\": {\n" \
       "            \"url\": \"http://25.28.115.246:2620/\",\n" \
       "            \"method\": \"POST\",\n" \
       "            \"headers\": {\n" \
       "                \"Content-Type\": \"application/json\"\n" \
       "            }\n" \
       "        }\n" \
       "    }\n}"

CB_BASE_URL = "http://{}:{}/v2/".format(selection_address_CB, selection_port_CB)  # url send notification

# subscription
msg_UNISA_SpeechGestureAnalysis_Speech = "{" \
       "    \"description\": \"FORTH-U20c\",\n" \
       "    \"subject\": {\n" \
       "        \"entities\":\n" \
       "        [{\n" \
       "            \"idPattern\": \"UNISA.SpeechGestureAnalysis.*\",\n" \
       "            \"typePattern\": \".*\"\n" \
       "        }],\n" \
       "        \"conditions\": {\n" \
       "            \"attrs\": []\n" \
       "        }\n" \
       "    },\n" \
       "    \"notification\": {\n" \
       "        \"http\": {\n" \
       "            \"url\": \"http://25.28.115.246:2620/\",\n" \
       "            \"method\": \"POST\",\n" \
       "            \"headers\": {\n" \
       "                \"Content-Type\": \"application/json\"\n" \
       "            }\n" \
       "        }\n" \
       "    }\n}"

CB_BASE_URL = "http://{}:{}/v2/".format(selection_address_CB, selection_port_CB)  # url send notification


# Log("INFO", "Send subcription")
# Log("INFO", msg)
# This is to subscribe. It is performed ONLY ONCE for each subscription.
#
'\n'
# FORTH HRI
response = requests.post(CB_BASE_URL + "subscriptions/", data=msg_FORTH_HRI, headers=CB_HEADER)  # send request to Context Broker
if response.ok:  # positive response, notification accepted
    print("CB response -> status " + response.status_code.__str__())
else:  # error response
    print("CB response -> " + response.text)

# Forth_ScenePerception
response1 = requests.post(CB_BASE_URL + "subscriptions/", data=msg_FORTH_ScenePerception, headers=CB_HEADER)
if response1.ok:  # positive response, notification accepted
    print("CB response1 -> status " + response1.status_code.__str__())
else:  # error response
    print("CB response1 -> " + response1.text)

# FHOE
response2 = requests.post(CB_BASE_URL + "subscriptions/", data=msg_FHOE, headers=CB_HEADER)
if response2.ok:  # positive response, notification accepted
    print("CB response1 -> status " + response2.status_code.__str__())
else:  # error response
    print("CB response1 -> " + response2.text)

# AEGIS_ButtonPress
response3 = requests.post(CB_BASE_URL + "subscriptions/", data=msg_AEGIS_ButtonPress, headers=CB_HEADER)
if response3.ok:  # positive response, notification accepted
    print("CB response AEGIS_ButtonPress -> status " + response3.status_code.__str__())
else:  # error response
    print("CB response AEGIS_ButtonPress -> " + response3.text)

# UNISA_ Speech Gesture Analysis(SGA) _Speech
response4 = requests.post(CB_BASE_URL + "subscriptions/", data=msg_UNISA_SpeechGestureAnalysis_Speech, headers=CB_HEADER)
if response4.ok:  # positive response, notification accepted
    print("CB response msg_UNISA_SGA_Speech -> status " + response4.status_code.__str__())
else:  # error response
    print("CB response msg_UNISA_SGA_Speech -> " + response4.text)
