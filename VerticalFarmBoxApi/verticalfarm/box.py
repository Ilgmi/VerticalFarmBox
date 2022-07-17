import json
from enum import Enum
from json import JSONEncoder


class MoistureLevel(int, Enum):
    dry = 0
    wet = 1
    very_wet = 2


class Plant:
    moisture_level: MoistureLevel = MoistureLevel.dry

    def __init__(self, moisture_level):
        self.moisture_level = moisture_level


class Condition:
    min_val: int
    max_val: int

    def __init__(self, min_val, max_val):
        self.min_val = min_val
        self.max_val = max_val


class Box:
    roof = 0
    watering_plants = 0
    temperature = 0
    humidity = 0
    light = 0
    plant: Plant

    temperature_condition: Condition
    humidity_condition: Condition

    def __init__(self, roof, watering_plants, temperature, humidity, light, plant, temperature_condition,
                 humidity_condition):
        self.roof = roof
        self.watering_plants = watering_plants
        self.temperature = temperature
        self.humidity = humidity
        self.light = light
        self.plant = plant
        self.temperature_condition = temperature_condition
        self.humidity_condition = humidity_condition


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
        if isinstance(object, Box):
            return object.__dict__
        elif isinstance(object, Plant) or isinstance(object, Condition):
            return DefaultEncoder().default(object)
        else:
            # call base class implementation which takes care of
            # raising exceptions for unsupported types
            return json.JSONEncoder.default(self, object)
