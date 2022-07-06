from random import random

from simulation.sensor import Sensor


class TemperatureSensor(Sensor):
    unit = "celsius"

    def __init__(self, averageTemperature, temperatureVariation, minTemperature, maxTemperature, instance_id):
        super().__init__("de.uni-stuttgart.iaas.sc", "temperature", instance_id)
        self.averageTemperature = averageTemperature
        self.temperatureVariation = temperatureVariation
        self.minTemperature = minTemperature
        self.maxTemperature = maxTemperature
        self.value = 0.0

    def sense(self):
        # self.value = self.value + self.simpleRandom()
        self.value = self.complexRandom()
        return self.value

    def get_value_message(self):
        return {
            self.unit: self.sense()
        }
        pass

    def simpleRandom(self):
        value = self.minTemperature + (random() * ((self.maxTemperature - self.minTemperature)))
        return value

    def complexRandom(self):
        value = self.averageTemperature * (1 + ((self.temperatureVariation / 100) * (3 * random() - 1)))
        value = max(value, self.minTemperature)
        value = min(value, self.maxTemperature)
        return value
