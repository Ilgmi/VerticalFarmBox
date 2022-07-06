from simulation.sensor import Sensor


class WaterLevelSensor(Sensor):

    def __init__(self, instance_id):
        super().__init__("de.uni-stuttgart.iaas.sc", "water_level", instance_id)
        self.value = 700

    def sense(self):
        val = self.value - 100
        if val < 0:
            val = 0
        self.value = val
        return self.value

    def get_value_message(self):
        return {
            "value": self.sense()
        }
