import json
from datetime import datetime
from json import JSONEncoder

from verticalfarm.domain.condition import Condition
from verticalfarm.domain.plant import Plant, MoistureLevel


class GreenhouseBox:
    key: str
    building: str
    room: str
    name: str
    connection_state: bool
    created: str
    updated: str

    roof = 0
    water_pump = 0
    show_text = 0
    watering_plants = 0
    temperature = 0
    humidity = 0
    light = 0
    plant: Plant

    temperature_condition: Condition
    humidity_condition: Condition

    @staticmethod
    def create_box(key, building, room, name):
        return GreenhouseBox(None, key, building, room, name, True, datetime.now().strftime("%d-%m-%YT%H:%M:%S"), None,
                             0, 0, 0, 0, 0, 0, 0,
                             Plant(MoistureLevel.dry), Condition(24, 30), Condition(30, 50))

    def __init__(self, _id, key, building, room, name, connection_state, created, updated, roof, water_pump, show_text,
                 watering_plants,
                 temperature, humidity, light, plant, temperature_condition,
                 humidity_condition):
        self._id = key
        self.key = key
        self.building = building
        self.room = room
        self.name = name
        self.connection_state = connection_state
        self.created = created
        self.updated = updated

        self.roof = roof
        self.water_pump = water_pump
        self.show_text = show_text
        self.watering_plants = watering_plants
        self.temperature = temperature
        self.humidity = humidity
        self.light = light
        self.plant = plant
        self.temperature_condition = temperature_condition
        self.humidity_condition = humidity_condition

    @staticmethod
    def map(data):
        pass


class DefaultEncoder(JSONEncoder):

    def default(self, object):
        if isinstance(object, Plant) or isinstance(object, Condition) or isinstance(object, MoistureLevel):
            return object.__dict__
        else:
            # call base class implementation which takes care of
            # raising exceptions for unsupported types
            return json.JSONEncoder.default(self, object)


class BoxEncoder(JSONEncoder):
    def default(self, object):
        if isinstance(object, GreenhouseBox):
            return object.__dict__
        elif isinstance(object, Plant) or isinstance(object, Condition):
            return DefaultEncoder().default(object)
        elif isinstance(object, datetime):
            return (str(object))
        else:
            # call base class implementation which takes care of
            # raising exceptions for unsupported types
            return json.JSONEncoder.default(self, object)
