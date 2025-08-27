curl --location 'http://localhost:4041/iot/services' \
--header 'fiware-service: openiot' \
--header 'fiware-servicepath: /' \
--header 'Content-Type: application/json' \
--data '{
    "services": [
        {
            "apikey": "4683c88be51128babac5be9701944d78",
            "cbroker": "http://orion:1026",
            "entity_type": "WarmWaterTankMeasurement",
            "resource": "/iot/json",
            "attributes": [
                {
                    "object_id": "p",
                    "type": "Property",
                    "name": "activePower",
                    "metadata": {
                        "unitCode": {
                            "type": "Text",
                            "value": "WTT"
                        }
                    }
                },
                {
                    "object_id": "temp",
                    "type": "Property",
                    "name": "temperature",
                    "metadata": {
                        "unitCode": {
                            "type": "Text",
                            "value": "CEL"
                        }
                    }
                }
            ],
            "static_attributes": [
                {
                    "name": "supportedProtocol",
                    "type": "Property",
                    "value": "ul20"
                }
            ]
        }
    ]
}'