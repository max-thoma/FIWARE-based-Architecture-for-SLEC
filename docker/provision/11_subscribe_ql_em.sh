curl --location 'http://localhost:1026/ngsi-ld/v1/subscriptions/' \
--header 'Content-Type: application/json' \
--header 'NGSILD-Tenant: openiot' \
--header 'fiware-servicepath: /' \
--header 'Link: <http://context/ngsi-context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"' \
--data '{
    "description": "Notify Power Consumption",
    "type": "Subscription",
    "entities": [
        {
            "type": "EnergyMeter"
        }
    ],
    "watchedAttributes": [
        "dateObservedFrom"
    ],
    "notification": {
        "attributes": [
            "energyConsumed",
            "dateObservedFrom",
            "dateObservedTo"
        ],
        "format": "normalized",
        "endpoint": {
            "uri": "http://quantumleap:8668/v2/notify",
            "accept": "application/json"
        }
    }
}'