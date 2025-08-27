"""
A simple data collector that prints all data when the simulation finishes.

"""

import collections
from math import ceil
import datetime
import csv
import os
import mosaik_api

import matplotlib.pyplot as plt

ROOT_DIR = os.path.realpath(os.path.dirname(__file__))

META = {
    "type": "event-based",
    "models": {
        "Monitor": {
            "public": True,
            "any_inputs": True,
            "params": [],
            "attrs": [],
        },
    },
}


def beautify_string(s: str):
    replacements = {
        "temp": "Temperature",
        "p_in": "Power Input",
        "p_out_cumultative": "Power Production Cumultative",
        "p_out": "Power Output",
        "water_out": "Warm Water Usage",
        "water_in": "Water Output",
        "water_level": "Water Level",
        "p_consumption_cumultative": "Power Consumed Cumultative",
        "p_import_cumultative": "Power Import Cumultative",
        "p_production_cumultative": "Power Production Cumultative",
        "p_consumption": "Power Consumption",
        "p_import": "Power Import",
        "p_production": "Power Production",
        "p_available_cumultative": "Power Available Cumultative",
        "p_available": "Surplus Power Available",
        "p_cumulative": "Power Consumed Cumultative",
        "p_imported": "Power Import",
        # "-": " ", ".": ", ", "_": " "
        " ": "-",
        ".": "-",
        "_": "-",
    }

    for key, val in replacements.items():
        s = s.replace(key, val)
    return s


class Collector(mosaik_api.Simulator):
    def __init__(self):
        super().__init__(META)
        self.eid = None
        self.data = collections.defaultdict(lambda: collections.defaultdict(dict))

    def init(self, sid, time_resolution, sim_start, csv_folder):
        self.sim_start = sim_start
        self.csv_folder = csv_folder
        return self.meta

    def create(self, num, model):
        if num > 1 or self.eid is not None:
            raise RuntimeError("Can only create one instance of Monitor.")

        self.eid = "Monitor"
        return [{"eid": self.eid, "type": model}]

    def step(self, time, inputs, max_advance):
        data = inputs.get(self.eid, {})
        for attr, values in data.items():
            for src, value in values.items():
                self.data[src][attr][time] = value

        return None

    def finalize(self):
        color_palet = ["r", "g", "b", "m", "c", "y", "k"]
        dt = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

        print("Collected data:")
        for sim, sim_data in sorted(self.data.items()):
            print("\t- %s" % sim)

            # ####
            # if (sim == "CSV-1.Electricity_0"):
            #     data = list(sim_data.values())
            #     y = list(data[0].values())
            #     print(f"sum: {sum(y)}")

            # if (sim == "CSV-0.WaterUsage_0"):
            #     data = list(sim_data.values())
            #     y = list(data[0].values())
            #     print(f"sum: {sum(y)}")

            # if (sim == "WarmWaterTankSim-0.Model_0"):
            #     data = list(sim_data.values())
            #     y = list(data[0].values())
            #     print(f"sum: {sum(y)/(12*1000)}")

            # if (sim == "WarmWaterTankSim-0.Model_1"):
            #     data = list(sim_data.values())
            #     y = list(data[0].values())
            #     print(f"sum: {sum(y)/(12*1000)}")

            # if (sim == "WarmWaterTankSim-0.Model_2"):
            #     data = list(sim_data.values())
            #     y = list(data[0].values())
            #     print(f"sum: {sum(y)/(12*1000)}")

            # ####

            num = len(sim_data.keys())
            data = list(sim_data.values())
            legend = list(sim_data.keys())

            if num > 1:
                # fig = plt.figure(figsize=(30, 12), dpi=300)
                fig = plt.figure(figsize=(30, 12), dpi=80)
                plt.rcParams.update({"font.size": 22})
            else:
                # fig = plt.figure(figsize=(15, 6), dpi=300)
                fig = plt.figure(figsize=(15, 6), dpi=80)
                plt.rcParams.update({"font.size": 18})

            for i in range(0, num):
                x = list(data[i].keys())
                y = list(data[i].values())

                d_base = self.sim_start
                nx = []
                [nx.append(d_base + datetime.timedelta(seconds=i)) for i in x]

                if num > 1:
                    fig.add_subplot(2, int(ceil(num / 2)), i + 1)

                s = beautify_string(s=f"{legend[i]}")
                plt.title(s)

                if s.__contains__("Water"):
                    plt.ylabel("[L]")
                elif (
                    s.__contains__("Cumultative")
                    or s.__contains__("Import")
                    or s.__contains__("Consumption")
                ):
                    plt.ylabel("[kWh]")
                elif s.__contains__("Power"):
                    plt.ylabel("[W]")
                elif s.__contains__("Temperature"):
                    plt.ylabel("[°C]")
                else:
                    plt.ylabel("")

                plt.xlabel("Time")
                plt.plot(nx, y, color_palet[i % len(color_palet)] + ".")
                plt.tight_layout()
                # with open(f"../../graphics/diagramme/mosaik/csv/{self.csv_folder}/{sim}-{s}.csv", 'w') as csvfile:
                #     filewriter = csv.writer(csvfile, delimiter=',')
                #     csv_data = []
                #     for z in zip(nx, y):
                #         csv_data.append([z[0],z[1]])
                #     filewriter.writerow(["time", "value"])
                #     filewriter.writerows(csv_data)

            # plt.show()
            plt.savefig(os.path.join(ROOT_DIR, f"graphs/{sim}.png"))


if __name__ == "__main__":
    mosaik_api.start_simulation(Collector())
