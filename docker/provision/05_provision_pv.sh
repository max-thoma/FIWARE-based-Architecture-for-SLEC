curl --location 'http://localhost:4041/iot/devices' \
--header 'fiware-service: openiot' \
--header 'fiware-servicepath: /' \
--header 'Content-Type: application/json' \
--data '{
    "devices": [
        {
            "device_id": "ems001",
            "entity_name": "urn:ngsi-ld:PhotovoltaicMeasurement:001",
            "entity_type": "PhotovoltaicMeasurement",
            "timezone": "Europe/Berlin",
            "static_attributes": [
                {
                    "name": "refPhotovoltaicDevice",
                    "type": "Relationship",
                    "value": "urn:ngsi-ld:PhotovoltaicDevice:001"
                },
                {
                    "name": "name",
                    "type": "Property",
                    "value": "Photovoltaic station (EMS)"
                },
                {
                    "name": "description",
                    "type": "Property",
                    "value": "Photovoltaic data"
                }
            ]
        },
        {
            "device_id": "ems002",
            "entity_name": "urn:ngsi-ld:PhotovoltaicMeasurement:002",
            "entity_type": "PhotovoltaicMeasurement",
            "timezone": "Europe/Berlin",
            "static_attributes": [
                {
                    "name": "refPhotovoltaicDevice",
                    "type": "Relationship",
                    "value": "urn:ngsi-ld:PhotovoltaicDevice:001"
                },
                {
                    "name": "name",
                    "type": "Property",
                    "value": "Photovoltaic station (EMS)"
                },
                {
                    "name": "description",
                    "type": "Property",
                    "value": "Photovoltaic data"
                }
            ]
        }
    ]
}'