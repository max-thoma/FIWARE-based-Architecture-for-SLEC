# solar.py

from datetime import timedelta
import json
import mosaik_api
import pandas as pd
import requests
from pvlib import location, modelchain, pvsystem
from dotenv import load_dotenv
import os

META = {
    "type": "time-based",
    "models": {
        "Progress": {
            "public": True,
            "params": [],
            "attrs": [],
        },
    },
}


class Progress(mosaik_api.Simulator):

    def __init__(self):
        super().__init__(META)
        self.time = 0
        self.eid = None

    def post_progress(self, prg):
        try:
            requests.post(self.notif_url, data=prg)
        except:
            pass

    def init(self, sid, time_resolution, sim_start, until, step_size=5 * 60):
        self.step_size = step_size
        self.sim_start = sim_start
        self.until = until
        print(until)
        load_dotenv("../.env")
        self.notif_url = os.getenv("WEB_UI_URL")
        return self.meta

    def create(self, num, model):
        if num > 1 or self.eid is not None:
            raise RuntimeError("Can only create one instance of Progress Reporter.")

        self.eid = "Progress_Reporter"
        return [{"eid": self.eid, "type": model}]

    def step(self, time, inputs, max_advance):
        self.time = time
        # print(
        #     f"{self.sim_start} - {self.time} - {self.until} - {(self.time/self.until)*100:.2f}%")
        sim_step = self.sim_start + timedelta(seconds=self.time)
        stop_date = self.sim_start + timedelta(seconds=self.until)
        msg = f"Start Date: {self.sim_start}, Current Simulation Step: {sim_step}, Stop Date: {stop_date}"
        print(stop_date)
        msg = {
            "start": self.sim_start,
            "current": sim_step,
            "until": stop_date,
            "done": False,
        }
        msg = json.dumps(msg, default=str)
        self.post_progress(msg)

        return time + self.step_size

    def finalize(self):
        # print(f"{self.sim_start} - {self.time} - {self.until} - {100:.2f}%")
        sim_step = self.sim_start + timedelta(seconds=self.time)
        stop_date = self.sim_start + timedelta(seconds=self.until)
        msg = f"Simulation Done"
        msg = {
            "start": self.sim_start,
            "current": sim_step,
            "until": stop_date,
            "done": True,
        }
        msg = json.dumps(msg, default=str)
        self.post_progress(msg)

    def get_data(self, outputs):
        data = {}
        return data


def main():
    return mosaik_api.start_simulation(Progress())


if __name__ == "__main__":
    main()
