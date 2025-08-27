curl --location 'http://localhost:4041/iot/devices' \
--header 'fiware-service: openiot' \
--header 'fiware-servicepath: /' \
--header 'Content-Type: application/json' \
--data '{
    "devices": [
        {
            "device_id": "wwt001",
            "entity_name": "urn:ngsi-ld:WarmWaterTankMeasurement:001",
            "entity_type": "WarmWaterTankMeasurement",
            "protocol": "PDI-IoTA-MQTT-UltraLight",
            "transport": "MQTT",
            "commands": [
                {
                    "name": "p",
                    "type": "command"
                }
            ],
            "static_attributes": [
                {
                    "name": "refWarmWaterTank",
                    "type": "Relationship",
                    "value": "urn:ngsi-ld:WarmWaterTank:001"
                },
                {
                    "name": "name",
                    "type": "Property",
                    "value": "WWT Measurement"
                },
                {
                    "name": "description",
                    "type": "Property",
                    "value": "Measurement data from the Warm Water Tank"
                }
            ]
        },
        {
            "device_id": "wwt002",
            "entity_name": "urn:ngsi-ld:WarmWaterTankMeasurement:002",
            "entity_type": "WarmWaterTankMeasurement",
            "protocol": "PDI-IoTA-MQTT-UltraLight",
            "transport": "MQTT",
            "commands": [
                {
                    "name": "p",
                    "type": "command"
                }
            ],
            "static_attributes": [
                {
                    "name": "refWarmWaterTank",
                    "type": "Relationship",
                    "value": "urn:ngsi-ld:WarmWaterTank:002"
                },
                {
                    "name": "name",
                    "type": "Property",
                    "value": "WWT Measurement"
                },
                {
                    "name": "description",
                    "type": "Property",
                    "value": "Measurement data from the Warm Water Tank"
                }
            ]
        },
        {
            "device_id": "wwt003",
            "entity_name": "urn:ngsi-ld:WarmWaterTankMeasurement:003",
            "entity_type": "WarmWaterTankMeasurement",
            "protocol": "PDI-IoTA-MQTT-UltraLight",
            "transport": "MQTT",
            "commands": [
                {
                    "name": "p",
                    "type": "command"
                }
            ],
            "static_attributes": [
                {
                    "name": "refWarmWaterTank",
                    "type": "Relationship",
                    "value": "urn:ngsi-ld:WarmWaterTank:003"
                },
                {
                    "name": "name",
                    "type": "Property",
                    "value": "WWT Measurement"
                },
                {
                    "name": "description",
                    "type": "Property",
                    "value": "Measurement data from the Warm Water Tank"
                }
            ]
        }
    ]
}'