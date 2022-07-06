from simulation.sensor import Sensor


class Box:
    building: str
    room: str
    name: str

    sensors = []

    def __init__(self, building, room, name):
        self.building = building
        self.room = room
        self.name = name

    def add_sensor(self, sensor: Sensor):
        self.sensors.append(sensor)

    def get_key(self):
        return self.building + "/" + self.room + "/" + self.name + "/"

    def get_register_message(self):
        return {
            "building": self.building,
            "room": self.room,
            "name": self.name
        }
