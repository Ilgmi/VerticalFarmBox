from abc import abstractmethod


class Actuator:
    type_id: str
    sensor_type: str
    instance_id: str

    def __init__(self, type_id, sensor_type, instance_id):
        self.type_id = type_id
        self.sensor_type = sensor_type
        self.instance_id = instance_id

    @abstractmethod
    def toggle(self):
        pass