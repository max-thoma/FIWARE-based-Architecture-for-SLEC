curl --location 'http://localhost:1026/ngsi-ld/v1/entityOperations/upsert' \
--header 'Content-Type: application/json' \
--header 'Link: <http://context/ngsi-context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"' \
--header 'Accept: application/ld+json' \
--header 'fiware-service: openiot' \
--header 'fiware-servicepath: /' \
--data '[
    {
        "id": "urn:ngsi-ld:Person:001",
        "type": "Person",
        "name": "Ernst Hauptmann"
    },
    {
        "id": "urn:ngsi-ld:Person:002",
        "type": "Person",
        "name": "Maria Schwert"
    },
    {
        "id": "urn:ngsi-ld:Person:003",
        "type": "Person",
        "name": "Klaus Stark"
    },
    {
        "id": "urn:ngsi-ld:Building:house001",
        "type": "Building",
        "category": {
            "type": "Property",
            "value": [
                "house"
            ]
        },
        "location": {
            "type": "GeoProperty",
            "value": {
                "type": "Point",
                "coordinates": [
                    16.3046577,
                    47.7794091
                ]
            }
        },
        "name": {
            "type": "Property",
            "value": "House 1"
        },
        "owner": {
            "type": "Relationship",
            "object": "urn:ngsi-ld:Person:person001"
        }
    },
    {
        "id": "urn:ngsi-ld:Building:house002",
        "type": "Building",
        "category": {
            "type": "Property",
            "value": [
                "house"
            ]
        },
        "location": {
            "type": "GeoProperty",
            "value": {
                "type": "Point",
                "coordinates": [
                    16.3046577,
                    47.7794091
                ]
            }
        },
        "name": {
            "type": "Property",
            "value": "House 2"
        },
        "owner": {
            "type": "Relationship",
            "object": "urn:ngsi-ld:Person:person002"
        }
    },
    {
        "id": "urn:ngsi-ld:Building:house003",
        "type": "Building",
        "category": {
            "type": "Property",
            "value": [
                "house"
            ]
        },
        "location": {
            "type": "GeoProperty",
            "value": {
                "type": "Point",
                "coordinates": [
                    16.3046577,
                    47.7794091
                ]
            }
        },
        "name": {
            "type": "Property",
            "value": "House 3"
        },
        "owner": {
            "type": "Relationship",
            "object": "urn:ngsi-ld:Person:person003"
        }
    },
    {
        "id": "urn:ngsi-ld:EnergyMeter:001",
        "type": "EnergyMeter",
        "name": "Energy Meter 1",
        "description": "Smart Energy Meter measures power consumption.",
        "energyConsumed": {
            "type": "Property",
            "value": "0",
            "unitCode": "KWH"
        },
        "dateObservedFrom": {
            "type": "Property",
            "value": ""
        },
        "dateObservedTo": {
            "type": "Property",
            "value": ""
        },
        "owner": {
            "type": "Property",
            "value": [
                "urn:ngsi-ld:Person:001"
            ]
        }
    },
    {
        "id": "urn:ngsi-ld:EnergyMeter:002",
        "type": "EnergyMeter",
        "name": "Energy Meter 2",
        "description": "Smart Energy Meter measures power consumption.",
        "energyConsumed": {
            "type": "Property",
            "value": "0",
            "unitCode": "KWH"
        },
        "dateObservedFrom": {
            "type": "Property",
            "value": ""
        },
        "dateObservedTo": {
            "type": "Property",
            "value": ""
        },
        "owner": {
            "type": "Property",
            "value": [
                "urn:ngsi-ld:Person:002"
            ]
        }
    },
    {
        "id": "urn:ngsi-ld:EnergyMeter:003",
        "type": "EnergyMeter",
        "name": "Energy Meter 2",
        "description": "Smart Energy Meter measures power consumption.",
        "energyConsumed": {
            "type": "Property",
            "value": "0",
            "unitCode": "KWH"
        },
        "dateObservedFrom": {
            "type": "Property",
            "value": ""
        },
        "dateObservedTo": {
            "type": "Property",
            "value": ""
        },
        "owner": {
            "type": "Property",
            "value": [
                "urn:ngsi-ld:Person:003"
            ]
        }
    }
]'