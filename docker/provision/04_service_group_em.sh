curl --location 'http://localhost:4041/iot/services' \
--header 'fiware-service: openiot' \
--header 'fiware-servicepath: /' \
--header 'Content-Type: application/json' \
--data '{
    "services": [
        {
            "apikey": "5e0d38d5ad6216089df313e8d2870a4c",
            "cbroker": "http://orion:1026",
            "entity_type": "EnergyMeter",
            "resource": "/iot/json",
            "attributes": [
                {
                    "object_id": "p",
                    "type": "Property",
                    "name": "energyConsumed",
                    "metadata": {
                        "unitCode": {
                            "type": "Text",
                            "value": "KWH"
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