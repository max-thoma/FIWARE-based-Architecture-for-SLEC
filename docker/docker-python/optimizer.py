import json
from time import sleep
import requests


class Optimizer():
    def __init__(self):
        self.params = self.get_parameter_wwt()
        self.data = {}

    def calc(self):
        # print(self.data)
        # print(self.data['data'][0]['id'])
        try:
            p_available = self.data['data'][0]['activePower']['value']
        except:
            p_available = 0
        # print(p_available)
        wwt_state = self.get_wwt_state()

        house_hold_p = (12*1000)*self.get_em()
        p_available -= house_hold_p

        for wwt in wwt_state:
            p_available -= wwt['activePower']

        if p_available > 0:
            temp_diffs = {}
            sum_temp_diff = 0
            for wwt in wwt_state:
                id = wwt['id']
                temp = wwt['temperature']
                target_temp = self.params[id]['targetTemperature']
                max_temp_diff = self.params[id]['maxTemperatureDifference']
                temp_diff = (target_temp + max_temp_diff) - temp
                if temp_diff > 0:
                    temp_diffs[id] = temp_diff
                    sum_temp_diff += temp_diffs[id]

            temp_diffs_ratio = {}
            for id, diff in temp_diffs.items():
                temp_diffs_ratio[id] = diff/sum_temp_diff

            for id, ratio in temp_diffs_ratio.items():
                p_val = int(p_available*ratio)
                assert (
                    p_val >= 0), f"number greater than 0 expected, got: {p_val}"
                if p_val > 0:
                    self.send_cmd(id, 'p', p_val)
                #print(f"p_val: {p_val}")
        else:
            # Slow down
            for wwt in wwt_state:
                if wwt['activePower'] != 0:
                    #self.send_cmd(wwt['id'], 'p', int(-wwt['activePower']/8))
                    pass

    def send_cmd(self, urn, cmd, val):
        url = f"http://orion:1026/ngsi-ld/v1/entities/{urn}/attrs/{cmd}"
        # url = f"http://localhost:1026/ngsi-ld/v1/entities/{urn}/attrs/{cmd}"

        payload = json.dumps({
            "type": "Property",
            "value": f"{val}"
        })
        headers = {
            'NGSILD-Tenant': 'openiot',
            'Content-Type': 'application/json',
            'Link': '<http://context/ngsi-context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
        }

        requests.request(
            "PATCH", url, headers=headers, data=payload)

    def get_parameter_wwt(self):
        url = 'http://orion:1026/ngsi-ld/v1/entities/'
        # url = f"http://localhost:1026/ngsi-ld/v1/entities/"

        headers = {
            'Content-Type': 'application/json',
            'Link': '<http://context/ngsi-context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"',
            'Accept': 'application/json',
            'NGSILD-Tenant': 'openiot'
        }
        req_params = {'type': 'WarmWaterTank'}
        try:
            response = requests.request(
                "GET", url, headers=headers, params=req_params)
        except:
            raise Exception("The context broker could not be reached")

        wwt_entities = json.loads(response.text)

        params = {}

        for entity in wwt_entities:
            param = {}
            if entity['capacity']['unitCode'] != "LTR":
                print("Error: Unkown measurement unit: '%s'" %
                      str(entity['capacity']['unitCode']))
                exit(1)
            param['capacity'] = entity['capacity']['value']

            pwr = 0
            if entity['NominalPower']['unitCode'] == "WTT":
                pwr = entity['NominalPower']['value']
            elif entity['NominalPower']['unitCode'] == "KWT":
                pwr = 1000 * entity['NominalPower']['value']
            else:
                print("Error: Unkown measurement unit: '%s'" %
                      str(entity['NominalPower']['unitCode']))
                exit(1)
            param['NominalPower'] = pwr

            tl = 0
            if entity['thermalLoss']['unitCode'] == "WTT":
                tl = entity['thermalLoss']['value']
            elif entity['thermalLoss']['unitCode'] == "KWT":
                tl = 1000 * entity['thermalLoss']['value']
            else:
                print("Error: Unkown measurement unit: '%s'" %
                      str(entity['thermalLoss']['unitCode']))
                exit(1)
            param['thermalLoss'] = tl

            maxTempDiff = 0
            if entity['targetTemperature']['unitCode'] == "CEL":
                maxTempDiff = entity['targetTemperature']['value']
            else:
                print("Error: Unkown measurement unit: '%s'" %
                      str(entity['targetTemperature']['unitCode']))
                exit(1)
            param['targetTemperature'] = maxTempDiff

            maxTempDiff = 0
            if entity['maxTemperatureDifference']['unitCode'] == "CEL":
                maxTempDiff = entity['maxTemperatureDifference']['value']
            else:
                print("Error: Unkown measurement unit: '%s'" %
                      str(entity['maxTemperatureDifference']['unitCode']))
                exit(1)
            param['maxTemperatureDifference'] = maxTempDiff

            urn = entity['id']
            req_params = {'q': f'refWarmWaterTank=="{urn}"',
                          'attrs': 'refWarmWaterTank',
                          'options': 'keyValues'}
            response = requests.request(
                "GET", url, headers=headers, params=req_params)
            measurement_data = json.loads(response.text)
            id = measurement_data[0]['id']
            param['urn'] = id
            params[id] = param
        return params

    def get_solar_energy(self):
        url = "http://orion:1026/ngsi-ld/v1/entities/"
        # url = "http://localhost:1026/ngsi-ld/v1/entities/"

        payload = {}
        headers = {
            'Link': '<http://context/ngsi-context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"',
            'NGSILD-Tenant': 'openiot'
        }
        params = {
            'attrs': 'activePower',
            'options': 'keyValues',
            'idPattern': '.*PhotovoltaicMeasurement*'
        }

        response = requests.request(
            "GET", url, headers=headers, data=payload, params=params)
        try:
            data_set = json.loads(response.text)
            p = 0
            for data in data_set:
                p += float(data['activePower'])
            return p
        except:
            return 0

    def get_wwt_state(self):
        url = "http://orion:1026/ngsi-ld/v1/entities/"
        # url = "http://localhost:1026/ngsi-ld/v1/entities/"

        payload = {}
        headers = {
            'Link': '<http://context/ngsi-context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"',
            'NGSILD-Tenant': 'openiot',
        }
        params = {
            'attrs': 'activePower,temperature',
            'type': 'WarmWaterTankMeasurement'
        }

        response = requests.request(
            "GET", url, headers=headers, data=payload, params=params)
        wwt_data = []

        data_set = json.loads(response.text)
        for wwt in data_set:
            wwt_state = {}
            wwt_state['temperature'] = wwt['temperature']['value']
            wwt_state['activePower'] = wwt['activePower']['value']
            wwt_state['id'] = wwt['id']
            wwt_data.append(wwt_state)
        return wwt_data

    def get_em(self):
        url = "http://orion:1026/ngsi-ld/v1/entities/"

        payload = {}
        headers = {
            'Link': '<http://context/ngsi-context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"',
            'NGSILD-Tenant': 'openiot',
        }
        params = {
            'attrs': 'energyConsumed',
            'type': 'EnergyMeter'
        }

        response = requests.request(
            "GET", url, headers=headers, data=payload, params=params)

        em_val = 0

        data_set = json.loads(response.text)
        for em in data_set:
            try:
                em_val += em['energyConsumed']['value']
            except:
                pass
        # print(em_val)
        return em_val
