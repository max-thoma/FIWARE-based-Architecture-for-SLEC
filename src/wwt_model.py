class WarmWaterTankModel:

    def __init__(
        self, init_temp, capacity, thermalLoss, p_max, target_temp, max_temp_diff
    ):
        self.temp = init_temp
        self.capacity = capacity
        self.water_level = capacity
        self.thermalLoss = thermalLoss
        self.p_in = 0
        self.water_in_temp = 10
        self.water_in = 0
        self.water_out = 0
        self.p_consumption = 0
        self.params = {
            "capacity": capacity,
            "p_max": p_max,
            "target_temp": target_temp,
            "max_temp_diff": max_temp_diff,
        }

    def step(self):
        self.p_consumption += self.p_in / 12

        self.water_level -= self.water_out
        self.water_in = self.capacity - self.water_level
        self.water_level += self.water_in

        warm_water_factor = (self.water_level - self.water_in) / self.water_level
        cold_water_factor = self.water_in / self.water_level

        self.temp = (
            warm_water_factor * self.temp + cold_water_factor * self.water_in_temp
        )

        # print(warm_water_factor, cold_water_factor)

        pWh = (5.0 / 60.0) * self.p_in
        tlossWh = (5.0 / 60.0) * self.thermalLoss
        degWh = 1.16 * self.capacity

        self.temp = self.temp + pWh / degWh - tlossWh / degWh
        if self.temp < 0:
            self.temp = 0
