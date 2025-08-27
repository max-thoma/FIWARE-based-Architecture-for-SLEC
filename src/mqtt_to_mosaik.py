"""
A simple data collector that prints all data when the simulation finishes.

"""

import json
from os import PRIO_USER
import mosaik_api
import paho.mqtt.client as mqtt


META = {
    "type": "time-based",
    "models": {
        "BridgeMQTT2mosaik": {
            "public": True,
            "any_inputs": True,
            "params": [],
            "attrs": [],
        },
    },
}


def on_message(client, userdata, msg):
    msg_data = json.loads(msg.payload)

    id = msg.topic.split("/")[2]
    for key, val in msg_data.items():
        if userdata.get(f"{id}_{key}", 0) == 0:
            userdata[f"{id}_{key}"] = int(val)
        else:
            userdata[f"{id}_{key}"] += int(val)
        # userdata[f"{id}_{key}"] = int(val)


def on_connect(client, userdata, flags, rc):
    client.subscribe(userdata["topics"])


class BridgeMQTT2mosaik(mosaik_api.Simulator):
    def __init__(self):
        super().__init__(META)
        self.eid = None
        self.time = 0
        self.data = {}

    def init(
        self,
        sid,
        time_resolution,
        sim_start,
        api_key,
        sub_attrs,
        step_size=5 * 60,
        broker="localhost",
        port=1883,
    ):
        self.sim_start = sim_start
        self.step_size = step_size
        self.attrs = sub_attrs
        self.api_key = api_key

        topics = []
        for id, attrs in sub_attrs.items():
            for attr in attrs:
                new_attr = f"{id}_{attr}"
                topics.append((f"/{api_key}/{id}/cmd", 0))
                self.meta["models"]["BridgeMQTT2mosaik"]["attrs"].append(new_attr)

        self.data["topics"] = topics
        self.client = mqtt.Client()
        self.client.on_message = on_message
        self.client.on_connect = on_connect
        self.client.user_data_set(self.data)
        self.client.connect(broker, port)
        self.client.loop_start()

        self.client.subscribe

        return self.meta

    def create(self, num, model):
        if num > 1 or self.eid is not None:
            raise RuntimeError("Can only create one instance of BridgeMQTT2mosaik.")

        self.eid = "BridgeMQTT2mosaik"
        return [{"eid": self.eid, "type": model}]

    def step(self, time, inputs, max_advance):
        self.time = time
        return time + self.step_size

    def get_data(self, outputs):
        data = {}
        for eid, attrs in outputs.items():
            data["time"] = self.time
            data[eid] = {}
            for attr in attrs:
                # the default value is 0
                # data[eid][attr] = int(self.data.get(attr, 0))
                try:
                    data[eid][attr] = int(self.data[attr])
                    self.data[attr] = 0
                except:
                    # default value
                    data[eid][attr] = 0
                # print(f"attr: {attr}\tdata: {data[eid][attr]}")

        return data

    def finalize(self):
        self.client.loop_stop()


if __name__ == "__main__":
    mosaik_api.start_simulation(BridgeMQTT2mosaik())
