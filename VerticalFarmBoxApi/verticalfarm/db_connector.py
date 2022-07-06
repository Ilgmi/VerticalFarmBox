from verticalfarm.messages import SensorDataMessage, RegisterBoxMessage, RegisterSensorMessage


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

    def add_sensor(self, message: RegisterSensorMessage):
        key = message.get_key()
        self.sensors[key] = {
            "room": message.room,
            "building": message.building,
            "name": message.name,
            "type_id": message.type_id,
            "instance_id": message.instance_id,
            "sensor_type": message.sensor_type
        }

    def add_sensor_data(self, message: SensorDataMessage):
        print("Add data", message)
        self.sensor_datas.append(message)

