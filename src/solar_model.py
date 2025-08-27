# solar.py

import datetime
import json
import mosaik_api
import pandas as pd
import requests
from pvlib import location, modelchain, pvsystem
import os

META = {
    "type": "time-based",
    "models": {
        "SolarModel": {
            "public": True,
            "params": ["params"],
            "attrs": ["p_out", "p_out_kwh", "p_out_cumultative"],
        },
    },
    "extra_methods": ["get_parameter"],
}


class Solar(mosaik_api.Simulator):

    def __init__(self):
        super().__init__(META)
        self.solar_results = {}
        self.urn = {}
        self.time = 0

    def init(self, sid, time_resolution, sim_start, sim_duration, step_size=5 * 60):
        self.step_size = step_size
        self.cb_hostname = os.getenv("CB_HOSTNAME")
        self.sim_start = sim_start
        self.sim_duration = sim_duration

        return self.meta

    def create(self, num, model, params):
        self.p_out = {}
        self.p_out_kwh = {}
        self.p_out_c = {}
        solar_results = solar_model(
            start_date=self.sim_start, duration=self.sim_duration, params=params
        )

        n_models = len(self.solar_results)
        entities = []
        for i in range(n_models, n_models + num):
            eid = "Solar_%d" % i
            self.solar_results[eid] = solar_results
            self.urn[eid] = params["urn"]
            entities.append({"eid": eid, "type": model})

        return entities

    def step(self, time, inputs, max_advance):
        self.time = time

        for eid in self.solar_results.keys():
            idx = int(time / self.step_size)
            # cell_temp = (self.solar_results[eid].cell_temperature[idx])
            cell_p = self.solar_results[eid].dc[idx]
            self.p_out[eid] = cell_p
            self.p_out_kwh[eid] = cell_p / (12 * 1000)
            self.p_out_c[eid] = self.p_out_c.get(eid, 0) + cell_p / (12 * 1000)  # kWh

        return time + self.step_size

    def get_data(self, outputs):
        data = {}
        for eid, attrs in outputs.items():
            data["time"] = self.time
            data[eid] = {
                "p_out": self.p_out[eid],
                "p_out_kwh": self.p_out_kwh[eid],
                "p_out_cumultative": self.p_out_c[eid],
            }
        return data

    def get_parameter(self):
        url = f"http://{self.cb_hostname}:1026/ngsi-ld/v1/entities/"

        headers = {
            "Content-Type": "application/json",
            "Link": '<http://context/ngsi-context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"',
            "Accept": "application/json",
            "NGSILD-Tenant": "openiot",
        }
        params = {"type": "PhotovoltaicDevice"}
        try:
            response = requests.request("GET", url, headers=headers, params=params)
        except:
            raise Exception("The context broker could not be reached")
        pv_devices = json.loads(response.text)

        params = []

        for entity in pv_devices:
            p = {}

            p["urn"] = entity["id"]
            p["longitude"] = entity["location"]["value"]["coordinates"][0]
            p["latitude"] = entity["location"]["value"]["coordinates"][1]

            pwr = 0
            if entity["NominalPower"]["unitCode"] == "WTT":
                pwr = entity["NominalPower"]["value"]
            elif entity["NominalPower"]["unitCode"] == "KWT":
                pwr = entity["NominalPower"]["value"] * 1000
            else:
                print(
                    "Error: Unkown measurement unit: '%s'"
                    % str(entity["NominalPower"]["unitCode"])
                )
                exit(1)
            p["pwr"] = pwr

            p["surface_tilt"] = entity["surfaceTilt"]["value"]
            if entity["surfaceTilt"]["unitCode"] != "DD":
                print(
                    "Error: Unkown measurement unit: '%s'"
                    % str(entity["surfaceTilt"]["unitCode"])
                )
                exit(1)

            p["surface_azimuth"] = entity["surfaceAzimuth"]["value"]
            if entity["surfaceAzimuth"]["unitCode"] != "DD":
                print(
                    "Error: Unkown measurement unit: '%s'"
                    % str(entity["surfaceAzimuth"]["unitCode"])
                )
                exit(1)
            params.append(p)
        return params


def solar_model(start_date, duration, params):
    pdc = params["pwr"]
    surface_tilt = params["surface_tilt"]
    surface_azimuth = params["surface_azimuth"]
    latitude = params["latitude"]
    longitude = params["longitude"]

    array_kwargs = dict(
        module_parameters=dict(pdc0=pdc, gamma_pdc=-0.004),
        temperature_model_parameters=dict(a=-3.56, b=-0.075, deltaT=3),
    )

    arrays = [
        pvsystem.Array(
            pvsystem.FixedMount(surface_tilt, surface_azimuth),
            name="Solar Array",
            **array_kwargs,
        ),
    ]

    loc = location.Location(latitude, longitude)
    system = pvsystem.PVSystem(arrays=arrays, inverter_parameters=dict(pdc0=pdc))
    mc = modelchain.ModelChain(
        system, loc, aoi_model="physical", spectral_model="no_loss"
    )

    times = pd.date_range(
        start_date, start_date + datetime.timedelta(seconds=duration), freq="5min"
    )
    weather = loc.get_clearsky(times)
    mc.run_model(weather)

    return mc.results


def main():
    return mosaik_api.start_simulation(Solar())


if __name__ == "__main__":
    main()
