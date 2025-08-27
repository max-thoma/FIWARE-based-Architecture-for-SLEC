#! /bin/python

import requests
import json

# curl -G -X GET 'http://localhost:1026/ngsi-ld/v1/entities/' \
#                             -H 'Link: <http://context/ngsi-context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"' \
#                             -d 'idPattern=urn:*'

url = 'http://localhost:1026/ngsi-ld/v1/entities/'
headers = {
  'Content-Type': 'application/ld+json',
  'Accept': 'application/ld+json',
  'NGSILD-Tenant': 'openiot'
}

params = {'idPattern': 'urn*', 'options': 'sysAttrs', 'limit': '100'}

response = requests.request("GET", url, headers=headers, params=params)
entities = json.loads(response.text)

count = 1
for entity in entities:
    try:
        name = str(entity["name"]["value"])
    except:
        name = "No Name"
    print("{:<3} {:<40} {:<40}".format(
        str(count) + ".", name,  str(entity["id"])))
    count = count + 1

try:
    sub_id = input("Enter the enitiy number: ")
    sub_index = int(sub_id) - 1
except:
    exit(1)

count = 1
for key in entities[sub_index].keys():
    print(str(count) + ". " + key)
    count = count + 1

try:
    key_id = input("Enter the key number of the watched attribute: ")
    key_index = int(key_id) - 1
except:
    exit(1)

# try:
#     time_id = input("Enter the key number of the time index: ")
#     time_index = int(time_id) - 1
# except:
#     exit(1)

keys = list(entities[sub_index].keys())
notification_list = list()

while True:
    try:
        notfication_id = input(
            "Enter the key number of the notfication attribute: ")
        notification_index = int(notfication_id) - 1
        notification_list.append(str(keys[notification_index]))
    except:
        break

print("Watched attributes: ")
print(str(keys[key_index]))
print("Notification attributes: ")
print(notification_list)
# print("Time intex: ")
# print(str(keys[time_index]))

url = 'http://localhost:1026/ngsi-ld/v1/subscriptions/'
data = {
    "description": "Notify Power Consumption",
    "type": "Subscription",
    "entities": [{"type": str(entities[sub_index]["type"])}],
    "watchedAttributes": [str(keys[key_index])],
    "notification": {
        "attributes": notification_list,
        "format": "normalized",
        "endpoint": {
            #"uri": "http://opti:57821/",
            #"uri": "http://quantumleap:8668/v2/notify",
            "uri": "http://sub-handler:57821/",
            "accept": "application/json",
        },
    }
}

print(json.dumps(data))

response = requests.request("POST", url, headers=headers, json=data)
print("Status Code " + str(response.status_code) + ": " + response.reason)
print(response.text)
print("")
print(json.dumps(data))