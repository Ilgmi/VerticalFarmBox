from abc import abstractmethod


class Actuator:
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
        print(f"Init actuator: type: '{type_id}' sensor_type:'{sensor_type}' instance: '{instance_id} ")

    def get_topic(self):
        return f"{self.building}/{self.room}/{self.name}/{self.sensor_type}/{self.instance_id}"

    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def run(self):
        pass
