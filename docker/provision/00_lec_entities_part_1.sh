curl --location 'http://localhost:1026/ngsi-ld/v1/entityOperations/upsert' \
--header 'Content-Type: application/json' \
--header 'Link: <http://context/ngsi-context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"' \
--header 'Accept: application/ld+json' \
--header 'fiware-service: openiot' \
--header 'fiware-servicepath: /' \
--data '[
    {
        "id": "urn:ngsi-ld:WarmWaterTank:001",
        "type": "WarmWaterTank",
        "name": "Smart Warm Water Tank 1",
        "description": "A smart warm water tank, that supports variable input power levels",
        "capacity": {
            "type": "Property",
            "value": 300.0,
            "unitCode": "LTR"
        },
        "NominalPower": {
            "type": "Property",
            "value": 3.6,
            "unitCode": "KWT"
        },
        "thermalLoss": {
            "type": "Property",
            "value": 50,
            "unitCode": "WTT"
        },
        "targetTemperature": {
            "type": "Property",
            "value": 60,
            "unitCode": "CEL"
        },
        "maxTemperatureDifference": {
            "type": "Property",
            "value": 5,
            "unitCode": "CEL"
        }
    },
    {
        "id": "urn:ngsi-ld:WarmWaterTank:002",
        "type": "WarmWaterTank",
        "name": "Smart Warm Water Tank 2",
        "description": "A smart warm water tank, that supports variable input power levels",
        "capacity": {
            "type": "Property",
            "value": 1200.0,
            "unitCode": "LTR"
        },
        "NominalPower": {
            "type": "Property",
            "value": 5.2,
            "unitCode": "KWT"
        },
        "thermalLoss": {
            "type": "Property",
            "value": 35,
            "unitCode": "WTT"
        },
        "targetTemperature": {
            "type": "Property",
            "value": 60,
            "unitCode": "CEL"
        },
        "maxTemperatureDifference": {
            "type": "Property",
            "value": 5,
            "unitCode": "CEL"
        }
    },
    {
        "id": "urn:ngsi-ld:WarmWaterTank:003",
        "type": "WarmWaterTank",
        "name": "Smart Warm Water Tank 3",
        "description": "A smart warm water tank, that supports variable input power levels",
        "capacity": {
            "type": "Property",
            "value": 1200.0,
            "unitCode": "LTR"
        },
        "NominalPower": {
            "type": "Property",
            "value": 5.2,
            "unitCode": "KWT"
        },
        "thermalLoss": {
            "type": "Property",
            "value": 35,
            "unitCode": "WTT"
        },
        "targetTemperature": {
            "type": "Property",
            "value": 60,
            "unitCode": "CEL"
        },
        "maxTemperatureDifference": {
            "type": "Property",
            "value": 5,
            "unitCode": "CEL"
        }
    },
    {
        "id": "urn:ngsi-ld:PhotovoltaicDevice:001",
        "type": "PhotovoltaicDevice",
        "name": "Solar Pannel",
        "description": "A residential solar panel",
        "MaximumSystemVoltage": {
            "type": "Property",
            "value": 400,
            "unitCode": "VLT"
        },
        "NominalPower": {
            "type": "Property",
            "value": 8000,
            "unitCode": "WTT"
        },
        "location": {
            "type": "Point",
            "coordinates": [
                16.470517,
                47.856821
            ]
        },
        "surfaceTilt": {
            "type": "Property",
            "value": 30,
            "unitCode": "DD"
        },
        "surfaceAzimuth": {
            "type": "Property",
            "value": 180,
            "unitCode": "DD"
        }
    },
    {
        "id": "urn:ngsi-ld:PhotovoltaicDevice:002",
        "type": "PhotovoltaicDevice",
        "name": "Solar Pannel",
        "description": "A residential solar panel",
        "MaximumSystemVoltage": {
            "type": "Property",
            "value": 400,
            "unitCode": "VLT"
        },
        "NominalPower": {
            "type": "Property",
            "value": 14,
            "unitCode": "KWT"
        },
        "location": {
            "type": "Point",
            "coordinates": [
                16.480517,
                47.846821
            ]
        },
        "surfaceTilt": {
            "type": "Property",
            "value": 44,
            "unitCode": "DD"
        },
        "surfaceAzimuth": {
            "type": "Property",
            "value": 180,
            "unitCode": "DD"
        }
    },
    {
        "id": "urn:ngsi-ld:PhotovoltaicMeasurement:001",
        "type": "PhotovoltaicMeasurement",
        "dateEnergyMeteringStarted": {
            "type": "Property",
            "value": ""
        },
        "TimeInstant": {
            "type": "Property",
            "value": ""
        },
        "dateObservedFrom": {
            "type": "Property",
            "value": ""
        },
        "dateObservedTo": {
            "type": "Property",
            "value": ""
        },
        "description": {
            "type": "Property",
            "value": "Photovoltaic data"
        },
        "name": {
            "type": "Property",
            "value": "Photovoltaic station (EMS)"
        },
        "refPhotovoltaicDevice": {
            "type": "Relationship",
            "object": "urn:ngsi-ld:PhotovoltaicDevice:001"
        },
        "temperature": {
            "type": "Property",
            "value": 23.4,
            "unitCode": "CEL"
        },
        "activePower": {
            "type": "Property",
            "value": 5,
            "unitCode": "KWT"
        }
    },
    {
        "id": "urn:ngsi-ld:PhotovoltaicMeasurement:002",
        "type": "PhotovoltaicMeasurement",
        "dateEnergyMeteringStarted": {
            "type": "Property",
            "value": ""
        },
        "TimeInstant": {
            "type": "Property",
            "value": ""
        },
        "dateObservedFrom": {
            "type": "Property",
            "value": ""
        },
        "dateObservedTo": {
            "type": "Property",
            "value": ""
        },
        "description": {
            "type": "Property",
            "value": "Photovoltaic data"
        },
        "name": {
            "type": "Property",
            "value": "Photovoltaic station (EMS)"
        },
        "refPhotovoltaicDevice": {
            "type": "Relationship",
            "object": "urn:ngsi-ld:PhotovoltaicDevice:002"
        },
        "temperature": {
            "type": "Property",
            "value": 23.4,
            "unitCode": "CEL"
        },
        "activePower": {
            "type": "Property",
            "value": 5,
            "unitCode": "KWT"
        }
    }
]'