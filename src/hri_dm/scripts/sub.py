import sys
import requests

# Input data acquisition
CB_HEADER = {'Content-Type': 'application/json'}
selection_port = '2620'
selection_address = '25.28.115.246'  # custom_hamachi IP
selection_port_CB = '1026'
selection_address_CB = '25.45.111.204'

# subscription
msg = "{" \
      "    \"description\": \"FORTH-RoboTest\",\n" \
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

#
#
# This is to subscribe. It is performed ONLY ONCE for each subscription.
#
#

response = requests.post(CB_BASE_URL + "subscriptions/", data=msg, headers=CB_HEADER)  # send request to Context Broker
if response.ok:  # positive response, notification accepted
    print("CB response -> status " + response.status_code.__str__())
else:  # error response
    print("CB response -> " + response.text)
