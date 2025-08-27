"""
A simple data collector that prints all data when the simulation finishes.

"""

import collections
import mosaik_api
import datetime
import paho.mqtt.client as paho
import json


META = {
    "type": "event-based",
    "models": {
        "BridgeMQTT": {
            "public": True,
            "any_inputs": True,
            "params": ["device_id", "api_key"],
            "attrs": [],
        },
    },
}


class BridgeMosaikMQTT(mosaik_api.Simulator):
    def __init__(self):
        super().__init__(META)
        self.eid = None
        self.data = collections.defaultdict(lambda: collections.defaultdict(dict))
        self.time = 0
        self.entities = []

    def init(
        self,
        sid,
        time_resolution,
        sim_start,
        step_size=5 * 60,
        broker="localhost",
        port=1883,
    ):
        self.sim_start = sim_start
        self.step_size = step_size
        self.mqtt = paho.Client("MosaikMQTTControler")
        self.mqtt.connect(broker, port)

        return self.meta

    def create(self, num, model, device_id, api_key):

        bridges = []
        n_models = len(self.entities)
        for i in range(n_models, n_models + num):
            eid = "MQTT_%d" % i
            self.data[eid]["device_id"] = device_id
            self.data[eid]["api"] = api_key
            bridges.append({"eid": eid, "type": model})
            self.entities.append({"eid": eid, "type": model})

        return bridges

    def step(self, time, inputs, max_advance):
        self.time = time
        for eid in self.data:
            if eid in inputs:
                attrs = inputs[eid]
                pl = gen_payload(self.sim_start, time, self.step_size, attrs)
                update_measurement(
                    self.mqtt, pl, self.data[eid]["device_id"], self.data[eid]["api"]
                )

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
    payload["gps"] = "16.480517, 47.846821"
    return payload


def update_measurement(client, payload, id, api_key):
    topic = f"json/{api_key}/{id}/attrs/"
    client.publish(topic, payload=json.dumps(payload))


if __name__ == "__main__":
    mosaik_api.start_simulation(BridgeMosaikMQTT())
