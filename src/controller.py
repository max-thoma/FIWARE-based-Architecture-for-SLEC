# controller.py
"""
A simple Warm Water Tank controller.

"""
import mosaik_api


META = {
    "type": "time-based",
    "models": {
        "Agent": {
            "public": True,
            "any_inputs": True,
            "params": ["water_in_temp"],
            "attrs": [
                "temp",
                "water_level",
                "p",
                "p_kwh",
                "p_available",
                "p_cumulative",
                "p_imported",
                "p_available_cumultative",
            ],
        },
    },
}


class Controller(mosaik_api.Simulator):

    def __init__(self):
        super().__init__(META)
        self.agents = []
        self.data = {}
        self.time = 0
        self.count = 0

    def init(self, sid, time_resolution, sim_start, eid_prefix=None, step_size=5 * 60):
        self.step_size = step_size
        self.p_cumulative = 0
        self.p_imported = 0
        self.p_available_cumultative = 0
        self.sim_start = sim_start
        return self.meta

    def create(self, num, model, water_in_temp=10):

        self.water_in_temp = water_in_temp
        n_agents = len(self.agents)
        entities = []
        for i in range(n_agents, n_agents + num):
            eid = "Agent_%d" % i
            self.data[eid] = {}
            self.data[eid]["p"] = 0
            self.agents.append(eid)
            entities.append({"eid": eid, "type": model})

        return entities

    def step(self, time, inputs, max_advance):
        self.time = time
        p_max = {}
        max_temp_diff = {}
        capacity = {}
        target_temp = {}
        p_all_ctrl = 0
        p_available_stat = 0
        p_available_used = 0

        for agent_eid, attrs in inputs.items():

            data = {}
            params = attrs.get("params", {})
            for src_eid, src_param in params.items():
                p_available_dict = attrs.get("p_available", {})
                data["p_available"] = sum(p_available_dict.values())
                # Add up all load balancing comands
                p_available_stat += data["p_available"]
                data["water_level"] = attrs["water_level"][src_eid]
                data["temp"] = attrs["temp"][src_eid]

                p_max[agent_eid] = src_param["p_max"]
                max_temp_diff[agent_eid] = src_param["max_temp_diff"]
                capacity[agent_eid] = src_param["capacity"]
                target_temp[agent_eid] = src_param["target_temp"]

                temp_diff = target_temp[agent_eid] - data["temp"]

                data["p"] = self.data[agent_eid]["p"]
                if temp_diff > 8:
                    data["p"] = p_max[agent_eid]
                elif temp_diff > max_temp_diff[agent_eid]:
                    data["p"] = p_max[agent_eid] / 2
                elif temp_diff <= 0:
                    data["p"] = 0

                if data["temp"] <= (target_temp[agent_eid] + max_temp_diff[agent_eid]):
                    p_current = data["p"]
                    p_load_balanced = min(
                        p_current + data["p_available"], p_max[agent_eid]
                    )
                    p_available_used += max(p_load_balanced - p_current, 0)
                    data["p"] = p_load_balanced

                p_all_ctrl += data["p"]
                data["p_kwh"] = data["p"] / (12 * 1000)

            self.data[agent_eid] = data

        # statistics
        self.p_cumulative += p_all_ctrl / (12 * 1000)
        self.p_available_cumultative += p_available_stat / (12 * 1000)
        # self.p_available = p_available_stat/(12*1000)
        self.p_available = p_available_stat
        imported_p = p_all_ctrl - p_available_used
        if imported_p > 0:
            self.p_imported += imported_p / (12 * 1000)  # kWh

        return time + self.step_size

    def get_data(self, outputs):
        data = {}
        for eid, attrs in outputs.items():
            data["time"] = self.time
            data[eid] = {}
            for attr in attrs:
                r_data = {}
                r_data = getattr(self, attr, {})
                if r_data == {}:
                    r_data = self.data[eid][attr]

                data[eid][attr] = r_data
        return data


def main():
    return mosaik_api.start_simulation(Controller())


if __name__ == "__main__":
    main()
