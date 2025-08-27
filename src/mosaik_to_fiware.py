"""
A simple data collector that prints all data when the simulation finishes.

"""

import collections
import requests
import mosaik_api
import datetime

META = {
    "type": "event-based",
    "models": {
        "BridgeM2F": {
            "public": True,
            "any_inputs": True,
            "params": ["urn"],
            "attrs": [],
        },
    },
}


class BridgeMosaikFiware(mosaik_api.Simulator):
    def __init__(self):
        super().__init__(META)
        self.eid = None
        self.data = collections.defaultdict(lambda: collections.defaultdict(dict))
        self.time = 0
        self.entities = []

    def init(self, sid, time_resolution, sim_start, step_size=5 * 60):
        self.sim_start = sim_start
        self.step_size = step_size

        return self.meta

    def create(self, num, model, urn):

        bridges = []
        n_models = len(self.entities)
        for i in range(n_models, n_models + num):
            eid = "M2F_%d" % i
            self.data[eid]["urn"] = urn
            bridges.append({"eid": eid, "type": model})
            self.entities.append({"eid": eid, "type": model})

        return bridges

    def step(self, time, inputs, max_advance):
        self.time = time
        for eid in self.data:
            if eid in inputs:
                attrs = inputs[eid]
                pl = gen_payload(self.sim_start, time, self.step_size, attrs)
                update_measurement(pl, self.data[eid]["urn"])

        return time + self.step_size


def gen_payload(d_base, t, t_step, attrs):
    d_from = d_base + datetime.timedelta(seconds=t)
    d_to = d_base + datetime.timedelta(seconds=t + t_step)

    payload = {}
    for attr, values in attrs.items():
        payload[attr] = sum(values.values())

    payload["TimeInstant"] = d_from.isoformat()
    payload["dateObservedFrom"] = d_from.isoformat()
    payload["dateObservedTo"] = d_to.isoformat()
    return payload


def update_measurement(payload, urn):
    url = f"http://localhost:1026/ngsi-ld/v1/entities/{urn}/attrs"

    headers = {
        "Content-Type": "application/json",
        "Link": '<http://context/ngsi-context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"',
        "Accept": "application/ld+json",
    }
    response = requests.request("PATCH", url, headers=headers, json=payload)
    return response


if __name__ == "__main__":
    mosaik_api.start_simulation(BridgeMosaikFiware())
