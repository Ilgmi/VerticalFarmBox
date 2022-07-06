from verticalfarm.messages import SensorDataMessage, RegisterBoxMessage


class DBConnector:
    boxes = {}
    sensors = {}
    sensor_datas = []

    def add_box(self, message: RegisterBoxMessage):
        key = message.get_key()
        self.boxes[key] = {
            "building": message.building,
            "room": message.room,
            "name": message.name
        }
        print(self.boxes)

    def add_sensor(self, building, room, name, sensor_type, instance_id):
        key = building + "/" + room + "/" + name + "/" + instance_id
        self.sensors[key] = {
            instance_id: instance_id,
            name: name,
            building: building,
            room: room,
            sensor_type: sensor_type
        }

    def add_sensor_data(self, message: SensorDataMessage):
        self.sensor_datas.append(message)

