curl --location 'http://localhost:4041/iot/devices' \
--header 'fiware-service: openiot' \
--header 'fiware-servicepath: /' \
--header 'Content-Type: application/json' \
--data '{
    "devices": [
        {
            "device_id": "em001",
            "entity_name": "urn:ngsi-ld:EnergyMeter:001",
            "entity_type": "EnergyMeter",
            "timezone": "Europe/Berlin",
            "static_attributes": [
                {
                    "name": "name",
                    "type": "Property",
                    "value": "(S)MS 1"
                },
                {
                    "name": "description",
                    "type": "Property",
                    "value": "Smart Energy Meter data"
                }
            ]
        },
        {
            "device_id": "em002",
            "entity_name": "urn:ngsi-ld:EnergyMeter:002",
            "entity_type": "EnergyMeter",
            "timezone": "Europe/Berlin",
            "static_attributes": [
                {
                    "name": "name",
                    "type": "Property",
                    "value": "(S)MS 2"
                },
                {
                    "name": "description",
                    "type": "Property",
                    "value": "Smart Energy Meter data"
                }
            ]
        },
        {
            "device_id": "em003",
            "entity_name": "urn:ngsi-ld:EnergyMeter:003",
            "entity_type": "EnergyMeter",
            "timezone": "Europe/Berlin",
            "static_attributes": [
                {
                    "name": "name",
                    "type": "Property",
                    "value": "(S)MS 3"
                },
                {
                    "name": "description",
                    "type": "Property",
                    "value": "Smart Energy Meter data"
                }
            ]
        }
    ]
}'