from abc import abstractmethod


class Actuator:
    building: str
    room: str
    name: str

    type_id: str
    actuator_type: str

    def __init__(self, building, room, name, type_id, actuator_type):
        self.building = building
        self.room = room
        self.name = name
        self.type_id = type_id
        self.actuator_type = actuator_type
        print(f"Init actuator: type: '{type_id}' sensor_type:'{actuator_type}' ")

    def get_topic(self):
        return f"{self.building}/{self.room}/{self.name}/{self.actuator_type}"

    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def run(self):
        pass
