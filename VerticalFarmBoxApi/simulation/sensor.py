from abc import abstractmethod
from datetime import datetime

from simulation.box import Box


class Sensor:
    type_id: str
    sensor_type: str
    instance_id: str

    def __init__(self, type_id, sensor_type, instance_id):
        self.type_id = type_id
        self.sensor_type = sensor_type
        self.instance_id = instance_id

    @abstractmethod
    def sense(self):
        pass

    @abstractmethod
    def get_value_message(self):
        pass

    def get_message(self):
        dt = datetime.now().strftime("%d-%m-%YT%H:%M:%S")
        message = {
            "type_id": self.type_id + "." + self.sensor_type,
            "sensor_type": self.sensor_type,
            "instance_id": self.instance_id,
            "timestamp": dt,
            "value": self.get_value_message()
        }
        return message

    def get_register_message(self, box: Box):
        return {
            "building": box.building
        }
