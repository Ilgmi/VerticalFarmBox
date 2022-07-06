from datetime import datetime
from enum import Enum


class SensorTypes(Enum):
    Temperature = "Temperature"
    PH = "PH"
    Water = "Water"
    Humidity = "Humidity"


class RegisterBoxMessage:
    building: str
    room: str
    name: str

    def __init__(self, building, room, name):
        self.building = building
        self.room = room
        self.name = name

    def get_key(self) -> str:
        return self.building + "/" + self.room + "/" + self.name


class RegisterSensorMessage:
    building: str
    room: str
    name: str
    type_id: str
    instance_id: str
    sensor_type: str

    def __init__(self, building, room, name, type_id, instance_id, sensor_type):
        self.building = building
        self.room = room
        self.name = name
        self.type_id = type_id
        self.instance_id = instance_id
        self.sensor_type = sensor_type

    def get_key(self) -> str:
        return self.building + "/" + self.room + "/" + self.name + "/" + self.instance_id


class SensorDataMessage:
    type_id: str
    sensor_type: str
    instance_id: str
    timestamp: datetime
    value: any

    def __init__(self, type_id, sensor_type, instance_id, timestamp: datetime, value: any):
        self.type_id = type_id
        self.sensor_type = sensor_type
        self.instance_id = instance_id
        self.timestamp = timestamp
        self.value = value
