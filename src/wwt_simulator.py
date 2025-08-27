import mosaik_api
import wwt_model
import requests
import json
import datetime
from dotenv import load_dotenv
import os


META = {
    "type": "time-based",
    "models": {
        "WarmWaterTankModel": {
            "public": True,
            "params": ["params", "init_temp"],
            "attrs": [
                "temp",
                "p_in",
                "water_out",
                "water_in",
                "water_in_temp",
                "water_level",
                "p_consumption",
                "params",
            ],
        },
    },
    "extra_methods": ["get_parameter"],
}


class WarmWaterTankSimulator(mosaik_api.Simulator):
    def __init__(self):
        super().__init__(META)
        self.eid_prefix = "Model_"
        self.entities = {}  # Maps EIDs to model instances/entities
        self.urn = {}
        self.time = 0

    def init(self, sid, time_resolution, sim_start, eid_prefix=None, step_size=5 * 60):
        self.cb_hostname = os.getenv("CB_HOSTNAME")
        if float(time_resolution) != 1.0:
            raise ValueError(
                f"Simulator only supports time_resolution=1., but {time_resolution} was set."
            )
        if eid_prefix is not None:
            self.eid_prefix = eid_prefix
        self.step_size = step_size
        self.sid = sid
        if isinstance(sim_start, datetime.date):
            self.sim_start = sim_start
        else:
            raise ("Invalid Start date")
        return self.meta

    def create(self, num, model, init_temp, params):
        next_eid = len(self.entities)
        entities = []
        capacity = params["capacity"]
        thermalLoss = params["thermalLoss"]
        target_temp = params["targetTemperature"]
        p_max = params["NominalPower"]
        max_temp_diff = params["maxTemperatureDifference"]
        urn = params["urn"]

        for i in range(next_eid, next_eid + num):
            model_instance = wwt_model.WarmWaterTankModel(
                init_temp, capacity, thermalLoss, p_max, target_temp, max_temp_diff
            )
            eid = "%s%d" % (self.eid_prefix, i)
            self.entities[eid] = model_instance
            self.urn[eid] = urn
            entities.append({"eid": eid, "type": model})

        return entities

    def step(self, time, inputs, max_advance):
        self.time = time
        for eid, model_instance in self.entities.items():
            if eid in inputs:
                attrs = inputs[eid]
                for attr, values in attrs.items():
                    val = sum(values.values())
                    setattr(model_instance, attr, val)

            model_instance.step()

        return time + self.step_size  # Step size is 5 minutes

    def get_data(self, outputs):
        data = {}
        for eid, attrs in outputs.items():
            model = self.entities[eid]
            data["time"] = self.time
            data[eid] = {}
            for attr in attrs:
                if attr not in self.meta["models"]["WarmWaterTankModel"]["attrs"]:
                    raise ValueError("Unknown output attribute: %s" % attr)
                data[eid][attr] = getattr(model, attr)

        return data

    def get_parameter(self):
        url = f"http://{self.cb_hostname}:1026/ngsi-ld/v1/entities/"

        headers = {
            "Content-Type": "application/json",
            "Link": '<http://context/ngsi-context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"',
            "Accept": "application/json",
            "NGSILD-Tenant": "openiot",
        }
        req_params = {"type": "WarmWaterTank"}
        try:
            response = requests.request("GET", url, headers=headers, params=req_params)
        except:
            raise Exception("The context broker could not be reached")

        wwt_entities = json.loads(response.text)

        params = []

        for entity in wwt_entities:
            param = {}
            if entity["capacity"]["unitCode"] != "LTR":
                print(
                    "Error: Unkown measurement unit: '%s'"
                    % str(entity["capacity"]["unitCode"])
                )
                exit(1)
            param["capacity"] = entity["capacity"]["value"]

            pwr = 0
            if entity["NominalPower"]["unitCode"] == "WTT":
                pwr = entity["NominalPower"]["value"]
            elif entity["NominalPower"]["unitCode"] == "KWT":
                pwr = 1000 * entity["NominalPower"]["value"]
            else:
                print(
                    "Error: Unkown measurement unit: '%s'"
                    % str(entity["NominalPower"]["unitCode"])
                )
                exit(1)
            param["NominalPower"] = pwr

            tl = 0
            if entity["thermalLoss"]["unitCode"] == "WTT":
                tl = entity["thermalLoss"]["value"]
            elif entity["thermalLoss"]["unitCode"] == "KWT":
                tl = 1000 * entity["thermalLoss"]["value"]
            else:
                print(
                    "Error: Unkown measurement unit: '%s'"
                    % str(entity["thermalLoss"]["unitCode"])
                )
                exit(1)
            param["thermalLoss"] = tl

            t_temp = 0
            if entity["targetTemperature"]["unitCode"] == "CEL":
                t_temp = entity["targetTemperature"]["value"]
            else:
                print(
                    "Error: Unkown measurement unit: '%s'"
                    % str(entity["targetTemperature"]["unitCode"])
                )
                exit(1)
            param["targetTemperature"] = t_temp

            t_diff = 0
            if entity["maxTemperatureDifference"]["unitCode"] == "CEL":
                t_diff = entity["maxTemperatureDifference"]["value"]
            else:
                print(
                    "Error: Unkown measurement unit: '%s'"
                    % str(entity["maxTemperatureDifference"]["unitCode"])
                )
                exit(1)
            param["maxTemperatureDifference"] = t_diff

            urn = entity["id"]
            req_params = {
                "q": f'refWarmWaterTank=="{urn}"',
                "attrs": "refWarmWaterTank",
                "options": "keyValues",
            }
            response = requests.request("GET", url, headers=headers, params=req_params)
            measurement_data = json.loads(response.text)
            print("===========================")
            print(json.dumps(measurement_data, indent=2))
            print("===========================")

            param["urn"] = measurement_data[0]["id"]

            params.append(param)
        return params


def main():
    return mosaik_api.start_simulation(WarmWaterTankSimulator())


if __name__ == "__main__":
    main()
