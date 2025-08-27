#! /bin/python

import requests
import json

# curl -G -X GET 'http://localhost:1026/ngsi-ld/v1/entities/' \
#                             -H 'Link: <http://context/ngsi-context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"' \
#                             -d 'idPattern=urn:*'

url = 'http://localhost:1026/ngsi-ld/v1/entities/'
headers = {
      'Content-Type': 'application/json',
      'Link': '<http://context/ngsi-context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"',
      'Accept': 'application/ld+json',
      'fiware-service': 'openiot',
      'fiware-servicepath': '/'
      }

params = {'idPattern': '.*'}

response = requests.request("GET", url, headers=headers, params=params)
entities = json.loads(response.text)

print("{:<3} {:<40} {:<25} {:<40} ".format("\033[1mNo.", "Name", "Desctiption", "URN\033[0m"))
count = 1
for entity in entities:
    name = ""
    description = ""
    try:
        name = str(entity["name"]["value"])
    except:
        name = "No Name"
    try:
        description = str(entity["description"]["value"])
    except:
        description = "No description" 
    # print(str(count) + ". " + name + 3*"\t" + description + 3*'\t' +  str(entity["id"]))
    print("{:<3} {:<40} {:<35} {:<40} ".format(str(count)+".",  name, "\x1B[3m" + description[0:20] + "\x1B[0m", entity["id"]))
    count = count + 1

for entity in entities:
    name = ""
    description = ""
    try:
        name = str(entity["name"]["value"])
    except:
        name = "No Name"
    try:
        description = str(entity["description"]["value"])
    except:
        description = "No description" 
    # print(str(count) + ". " + name + 3*"\t" + description + 3*'\t' +  str(entity["id"]))
    print('"' + entity["id"] + '",')
    count = count + 1
