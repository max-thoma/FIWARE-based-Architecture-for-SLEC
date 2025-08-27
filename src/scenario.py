# demo_1.py
import datetime
import mosaik
import mosaik.util
from enum import Enum
import os
from dotenv import load_dotenv

ROOT_DIR = os.path.realpath(os.path.dirname(__file__))
load_dotenv()

class Scenario(Enum):
    WITH_OPTI_NO_EM = 1
    NO_OPTI_NO_EM = 2
    WITH_OPTI_WITH_EM = 3
    NO_OPTI_WITH_EM = 4


scenario = Scenario.WITH_OPTI_WITH_EM

SIM_CONFIG = {
    "WarmWaterTankSim": {
        "python": "wwt_simulator:WarmWaterTankSimulator",
    },
    "Collector": {
        "python": "collector:Collector",
    },
    "Controller": {
        "python": "controller:Controller",
    },
    "SolarModel": {
        "python": "solar_model:Solar",
    },
    "CSV": {"python": "mosaik_csv:CSV"},
    "BridgeMQTT": {
        "python": "mosaik_to_mqtt:BridgeMosaikMQTT",
    },
    "BridgeMQTT2mosaik": {
        "python": "mqtt_to_mosaik:BridgeMQTT2mosaik",
    },
    "StatCollector": {
        "python": "stat_collector:Stat",
    },
    "ProgressReporter": {
        "python": "progress_reporter:Progress",
    },
}
START = "2022-09-01 00:00:00"
START_DATE = datetime.datetime(2022, 9, 15, 0, 0, 0, 0)
START_DATE_CSV = "15/09/2022 00:00"
# END = 1*24*60*60  # 24 h
END = 2 * 24 * 60 * 60  # 48 h

INITIAL_TEMP = 60
API_KEY_WWT = "4683c88be51128babac5be9701944d78"  # md5sum wwt
API_KEY_PV = "eeeeba8ac7ec84cd9eadc5be00ca2926"  # md5sum pv
API_KEY_EM = "5e0d38d5ad6216089df313e8d2870a4c"  # md5sum em

# Create World
world = mosaik.World(SIM_CONFIG)

match scenario:
    case Scenario.WITH_OPTI_NO_EM:
        collector = world.start(
            "Collector", sim_start=START_DATE, csv_folder="With-Opti-No-EM"
        )
    case Scenario.WITH_OPTI_WITH_EM:
        collector = world.start(
            "Collector", sim_start=START_DATE, csv_folder="With-Opti-With-EM"
        )
    case Scenario.NO_OPTI_NO_EM:
        collector = world.start(
            "Collector", sim_start=START_DATE, csv_folder="No-Opti-No-EM"
        )
    case Scenario.NO_OPTI_WITH_EM:
        collector = world.start(
            "Collector", sim_start=START_DATE, csv_folder="No-Opti-With-EM"
        )


# Start simulators
hwt_sim = world.start("WarmWaterTankSim", sim_start=START_DATE)
stat_collector = world.start("StatCollector", sim_start=START_DATE)
progress_reporter = world.start("ProgressReporter", sim_start=START_DATE, until=END)
controller = world.start("Controller", sim_start=START_DATE)
solar = world.start("SolarModel", sim_start=START_DATE, sim_duration=END)
# csv = world.start('CSV', sim_start=START,
#                   datafile='Data/WaterData.csv', date_format='YYYY-MM-DD HH:mm:ss')
csv_water_CHR16 = world.start(
    "CSV",
    sim_start=START_DATE_CSV,
    datafile=os.path.join(ROOT_DIR, "Data/HotWaterUsageCHR16.csv"),
    date_format="DD/MM/YYYY HH:mm",
)
csv_water_CHR27 = world.start(
    "CSV",
    sim_start=START_DATE_CSV,
    datafile=os.path.join(ROOT_DIR, "Data/HotWaterUsageCHR27.csv"),
    date_format="DD/MM/YYYY HH:mm",
)
csv_water_CHR45 = world.start(
    "CSV",
    sim_start=START_DATE_CSV,
    datafile=os.path.join(ROOT_DIR, "Data/HotWaterUsageCHR45.csv"),
    date_format="DD/MM/YYYY HH:mm",
)

bridge_mosaik_to_mqtt = world.start("BridgeMQTT", sim_start=START_DATE)

csv_electricity_CHR16 = world.start(
    "CSV",
    sim_start=START_DATE_CSV,
    datafile=os.path.join(ROOT_DIR, "Data/HouseElectricityCHR16.csv"),
    date_format="DD/MM/YYYY HH:mm",
)
csv_electricity_CHR27 = world.start(
    "CSV",
    sim_start=START_DATE_CSV,
    datafile=os.path.join(ROOT_DIR, "Data/HouseElectricityCHR27.csv"),
    date_format="DD/MM/YYYY HH:mm",
)
csv_electricity_CHR45 = world.start(
    "CSV",
    sim_start=START_DATE_CSV,
    datafile=os.path.join(ROOT_DIR, "Data/HouseElectricityCHR45.csv"),
    date_format="DD/MM/YYYY HH:mm",
)

# Get solar data
solar_parameter = solar.get_parameter()
wwt_parameter = hwt_sim.get_parameter()

agents = []
monitor = collector.Monitor()
stat = stat_collector.Stat()
progress = progress_reporter.Progress()

water_usage = []
water_usage.append(csv_water_CHR16.WaterUsage())
water_usage.append(csv_water_CHR27.WaterUsage())
water_usage.append(csv_water_CHR45.WaterUsage())

energy_meter = []
energy_meter.append(csv_electricity_CHR16.Electricity())
energy_meter.append(csv_electricity_CHR27.Electricity())
energy_meter.append(csv_electricity_CHR45.Electricity())


sub_attrs = {}
for i in range(1, len(wwt_parameter) + 1):
    sub_attrs[f"wwt00{i}"] = ["p"]


bridge_mqtt_to_mosaik = world.start(
    "BridgeMQTT2mosaik", sim_start=START_DATE, sub_attrs=sub_attrs, api_key=API_KEY_WWT
)
mqtt_to_mosaik = bridge_mqtt_to_mosaik.BridgeMQTT2mosaik()

idx = 1
solar_data = []
for sp in solar_parameter:
    new_solar = solar.SolarModel(params=sp)

    solar_data.append(new_solar)
    mosaik_to_mqtt_pv = bridge_mosaik_to_mqtt.BridgeMQTT(
        api_key=API_KEY_PV, device_id=f"ems00{idx}"
    )
    world.connect(new_solar, mosaik_to_mqtt_pv, ("p_out", "p"))
    idx += 1


warm_water_tanks = []
idx = 1
for wwt in wwt_parameter:
    new_tank = hwt_sim.WarmWaterTankModel(init_temp=INITIAL_TEMP, params=wwt)
    warm_water_tanks.append(new_tank)

    mosaik_to_mqtt_wwt = bridge_mosaik_to_mqtt.BridgeMQTT(
        api_key=API_KEY_WWT, device_id=f"wwt00{idx}"
    )
    mosaik_to_mqtt_em = bridge_mosaik_to_mqtt.BridgeMQTT(
        api_key=API_KEY_EM, device_id=f"em00{idx}"
    )

    new_agent = controller.Agent()
    agents.append(new_agent)
    world.connect(
        new_tank,
        new_agent,
        "temp",
        "water_level",
        "params",
        time_shifted=True,
        initial_data={
            "temp": INITIAL_TEMP,
            "water_level": wwt["capacity"],
            "params": {
                "capacity": wwt["capacity"],
                "p_max": wwt["NominalPower"],
                "target_temp": wwt["targetTemperature"],
                "max_temp_diff": wwt["maxTemperatureDifference"],
            },
        },
    )

    world.connect(new_agent, new_tank, ("p", "p_in"))
    world.connect(water_usage[idx - 1], new_tank, "water_out")
    world.connect(mqtt_to_mosaik, new_agent, (f"wwt00{idx}_p", "p_available"))

    world.connect(
        new_tank, mosaik_to_mqtt_wwt, ("temp", "temp"), ("p_in", "activePower")
    )
    world.connect(energy_meter[idx - 1], mosaik_to_mqtt_em, ("p_usage", "p"))

    world.connect(water_usage[idx - 1], monitor, "water_out")
    world.connect(new_tank, monitor, "water_level", "temp", "p_in", "water_in")
    world.connect(
        new_agent,
        monitor,
        "p_available",
        "p_cumulative",
        "p_available_cumultative",
        "p_imported",
    )
    world.connect(new_tank, monitor, "temp")
    world.connect(new_tank, monitor, "p_in")

    world.connect(new_agent, stat, ("p_kwh", "p_consumption"))

    if (scenario is Scenario.NO_OPTI_WITH_EM) or (
        scenario is Scenario.WITH_OPTI_WITH_EM
    ):
        world.connect(energy_meter[idx - 1], stat, ("p_usage", "p_consumption"))

    idx += 1

# world.connect(csv_water_usage, monitor, 'water_out')

# world.connect(stat, monitor, 'p_consumption_cumultative', 'p_import_cumultative', 'p_production_cumultative',
#                              'p_consumption', 'p_import', 'p_production' )
world.connect(
    stat,
    monitor,
    "p_consumption_cumultative",
    "p_import_cumultative",
    "p_consumption",
    "p_import",
)

mosaik.util.connect_many_to_one(
    world, solar_data, monitor, "p_out", "p_out_cumultative"
)
mosaik.util.connect_many_to_one(world, solar_data, stat, ("p_out_kwh", "p_production"))

if (scenario is Scenario.WITH_OPTI_WITH_EM) or (scenario is Scenario.WITH_OPTI_NO_EM):
    world.run(until=END, print_progress=False, rt_factor=1 / 1200)
else:
    world.run(until=END, print_progress=False)
