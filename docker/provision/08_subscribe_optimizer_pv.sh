curl --location 'http://localhost:1026/ngsi-ld/v1/subscriptions/' \
--header 'Content-Type: application/json' \
--header 'NGSILD-Tenant: openiot' \
--header 'fiware-servicepath: /' \
--header 'Link: <http://context/ngsi-context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"' \
--data '{
    "description": "Optimizer Subscription",
    "type": "Subscription",
    "entities": [
        {
            "type": "PhotovoltaicMeasurement"
        }
    ],
    "watchedAttributes": [
        "activePower"
    ],
    "notification": {
        "attributes": [
            "activePower"
        ],
        "format": "normalized",
        "endpoint": {
            "uri": "http://opti:57821/",
            "accept": "application/json"
        }
    }
}'