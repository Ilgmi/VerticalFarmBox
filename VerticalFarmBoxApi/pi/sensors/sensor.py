from abc import abstractmethod
from datetime import datetime


class Sensor:
    building: str
    room: str
    name: str

    type_id: str
    sensor_type: str
    instance_id: str

    def __init__(self, building, room, name, type_id, sensor_type, instance_id):
        self.building = building
        self.room = room
        self.name = name
        self.type_id = type_id
        self.sensor_type = sensor_type
        self.instance_id = instance_id
        print(f"Init Sensor: type: '{type_id}' sensor_type:'{sensor_type}' instance: '{instance_id} ")

    def get_topic(self):
        return f"{self.building}/{self.room}/{self.name}/{self.sensor_type}/{self.instance_id}"

    def get_message(self, data):
        dt = datetime.now().strftime("%d-%m-%YT%H:%M:%S")
        message = {
            "type_id": self.type_id + "." + self.sensor_type,
            "sensor_type": self.sensor_type,
            "instance_id": self.instance_id,
            "timestamp": dt,
            "value": data
        }
        return message

    @abstractmethod
    def collect_data(self):
        pass
