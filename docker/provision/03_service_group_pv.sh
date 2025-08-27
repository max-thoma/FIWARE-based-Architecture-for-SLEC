curl --location 'http://localhost:4041/iot/services' \
--header 'fiware-service: openiot' \
--header 'fiware-servicepath: /' \
--header 'Content-Type: application/json' \
--data '{
    "services": [
        {
            "apikey": "eeeeba8ac7ec84cd9eadc5be00ca2926",
            "cbroker": "http://orion:1026",
            "entity_type": "PhotovoltaicMeasurement",
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
                },
                {
                    "object_id": "gps",
                    "name": "location",
                    "type": "geo:point"
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