"""
A simple data collector that prints all data when the simulation finishes.

"""

import collections
from math import ceil
import datetime

import mosaik_api

import matplotlib.pyplot as plt

META = {
    "type": "time-based",
    "models": {
        "Stat": {
            "public": True,
            "any_inputs": True,
            "params": [],
            "attrs": [
                "p_consumption_cumultative",
                "p_consumption",
                "p_import",
                "p_import_cumultative",
                "p_production",
                "p_production_cumultative",
            ],
        },
    },
}


class Stat(mosaik_api.Simulator):
    def __init__(self):
        super().__init__(META)
        self.p_consumption_cumultative = 0
        self.p_consumption = 0
        self.p_production_cumultative = 0
        self.p_import = 0
        self.p_import_cumultative = 0
        self.eid = None
        self.time = 0
        self.data = collections.defaultdict(lambda: collections.defaultdict(dict))

    def init(self, sid, time_resolution, sim_start, step_size=5 * 60):
        self.step_size = step_size
        self.sim_start = sim_start

        return self.meta

    def create(self, num, model):
        if num > 1 or self.eid is not None:
            raise RuntimeError("Can only create one instance of Statistics.")

        self.eid = "Stat"
        return [{"eid": self.eid, "type": model}]

    def step(self, time, inputs, max_advance):
        self.time = time
        data = inputs.get(self.eid, {})
        current_consumption = 0
        current_production = 0
        for attr, values in data.items():
            if attr == "p_consumption":
                current_consumption = sum(values.values())
                self.p_consumption_cumultative += current_consumption
                self.p_consumption = current_consumption
            if attr == "p_production":
                current_production = sum(values.values())
                self.p_production_cumultative += current_production
                self.p_production = current_production
                # for src, value in values.items():
                #     self.data[src][attr][time] = value
        current_import = current_consumption - current_production
        if (current_import) > 0:
            self.p_import_cumultative += current_import
            self.p_import = current_import
        else:
            self.p_import = 0

        return time + self.step_size

    def get_data(self, outputs):
        data = {}
        for eid, attrs in outputs.items():
            data["time"] = self.time
            data[eid] = {}
            for attr in attrs:
                data[eid][attr] = getattr(self, attr, {})
        return data

    def finalize(self):
        print(f"consumption {self.p_consumption_cumultative} [kWh]")
        print(f"production {self.p_production_cumultative} [kWh]")
        print(f"import {self.p_import_cumultative} [kWh]")


if __name__ == "__main__":
    mosaik_api.start_simulation(Stat())
