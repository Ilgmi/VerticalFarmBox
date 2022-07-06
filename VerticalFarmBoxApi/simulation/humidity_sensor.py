from random import random

from simulation.sensor import Sensor


class HumiditySensor(Sensor):

    def __init__(self, instance_id):
        super().__init__("de.uni-stuttgart.iaas.sc", "humidity", instance_id)
        self.value = 50
        self.average = 50
        self.min = 0
        self.max = 100
        self.temperatureVariation = 1

    def sense(self):
        self.value = self.complexRandom()
        return self.value

    def get_value_message(self):
        return {
            "value": self.sense()
        }

    def complexRandom(self):
        value = self.average * (1 + ((self.temperatureVariation / 100) * (3 * random() - 1)))
        value = max(value, self.min)
        value = min(value, self.max)
        return value
