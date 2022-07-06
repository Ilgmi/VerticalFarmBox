from simulation.display import Display
from simulation.humidity_sensor import HumiditySensor
from simulation.moisture_sensor import MoistureSensor
from simulation.ph_sensor import PHSensor
from simulation.temperatur_sensor import TemperatureSensor
from simulation.water_level_sensor import WaterLevelSensor
from simulation.water_pump import WaterPump


class Box:
    building: str
    room: str
    name: str

    sensors = []

    moisture: MoistureSensor
    ph: PHSensor
    humidity: HumiditySensor
    water_level: WaterLevelSensor
    temperature: TemperatureSensor

    display: Display
    water_pump: WaterPump

    def __init__(self, building, room, name):
        self.building = building
        self.room = room
        self.name = name
        self.moisture = MoistureSensor(1)
        self.ph = PHSensor(1)
        self.humidity = HumiditySensor(1)
        self.water_level = WaterLevelSensor(1)
        self.temperature = TemperatureSensor(20, 10, 16, 35, 1)
        self.display = Display(1)
        self.water_pump = WaterPump(1)

    def get_key(self):
        return self.building + "/" + self.room + "/" + self.name + "/"

    def get_register_message(self):
        return {
            "building": self.building,
            "room": self.room,
            "name": self.name
        }



