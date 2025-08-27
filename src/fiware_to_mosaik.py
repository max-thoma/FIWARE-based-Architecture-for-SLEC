"""
A simple data collector that prints all data when the simulation finishes.

"""

import collections
import json
import requests
import mosaik_api

META = {
    "type": "time-based",
    "models": {
        "Bridge": {
            "public": True,
            "any_inputs": True,
            "params": [],
            "attrs": [],
        },
    },
}


class Bridge(mosaik_api.Simulator):
    def __init__(self):
        super().__init__(META)
        self.eid = None
        self.data = collections.defaultdict(lambda: collections.defaultdict(dict))
        self.time = 0

    def init(self, sid, time_resolution, sim_start, urns, step_size=5 * 60):
        self.sim_start = sim_start
        self.step_size = step_size
        self.urns = urns

        for dicts in urns:
            for urn, attrs in dicts.items():
                for attr in attrs:
                    new_attr = f"{urn}_{attr}"
                    self.meta["models"]["Bridge"]["attrs"].append(new_attr)
        return self.meta

    def create(self, num, model):
        if num > 1 or self.eid is not None:
            raise RuntimeError("Can only create one instance of Bridge.")

        self.eid = "Bridge"
        return [{"eid": self.eid, "type": model}]

    def step(self, time, inputs, max_advance):
        self.time = time

        for dicts in self.urns:
            for urn, attrs in dicts.items():
                for attr in attrs:
                    idx = f"{urn}_{attr}"
                    self.data[self.eid][idx] = get_fiware_attr(urn, attr)

        return time + self.step_size

    def get_data(self, outputs):
        data = {}
        get_fiware_attr
        for eid, attrs in outputs.items():
            data["time"] = self.time
            data[eid] = {}
            for attr in attrs:
                data[eid][attr] = self.data[eid][attr]

        return data


def get_fiware_attr(urn, attr):
    url = f"http://localhost:1026/ngsi-ld/v1/entities/{urn}/"

    headers = {
        "Content-Type": "application/json",
        "Link": '<http://context/ngsi-context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"',
        "Accept": "application/json",
    }

    params = {"options": "keyValues", "attrs": attr}

    response = requests.request("GET", url, headers=headers, params=params)
    data = json.loads(response.text)
    return data[attr]


if __name__ == "__main__":
    mosaik_api.start_simulation(Bridge())
