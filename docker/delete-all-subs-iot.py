#! /bin/python

import json
import requests

headers = {
    'NGSILD-Tenant': 'openiot',
    'Content-Type': 'application/json',
    'Link': '<http://context/ngsi-context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"',
    'Accept': 'application/ld+json'
}

response = requests.get('http://localhost:1026/ngsi-ld/v1/subscriptions/', headers=headers)
subs = json.loads(response.text)

if (len(subs) == 0):
    print("There are no subscriptions")
    exit(0)

print("__________")
for sub in subs:
     print(sub)
print("__________")

for sub in subs:
	print(sub["id"])

try:
    choice = input("Delete all? [y/N]")
    if (choice.lower() == "y"):
        for sub in subs:
            response = requests.delete('http://localhost:1026/ngsi-ld/v1/subscriptions/'+ str(sub["id"]), headers=headers)
            print("Status Code " + str(response.status_code) + ": " + response.reason)
    else:
        print("Not deleted")
except:
    exit(1)
    

