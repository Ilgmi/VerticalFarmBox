import json

from pymongo import MongoClient

from ai.Planner import Planner
from verticalfarm.db_connector import DBConnector
from verticalfarm.gateway import Gateway
from verticalfarm.messages import RegisterBoxMessage, RegisterSensorMessage, SensorDataMessage


class VerticalFarm:
    gateway: Gateway
    dbClient: DBConnector
    vertical_farmDb: any
    planner: Planner

    def __init__(self):
        self.connectToMQTT()
        self.connectToDB()
        # self.gateway.on_box_register(self.on_box_register)
        self.gateway.on_sensor_receive_data(self.on_sensor_receive_data)
        self.planner = Planner()

        test = self.planner.solve()
        x = 1

    def connectToMQTT(self):
        self.gateway = Gateway()
        self.gateway.connectToMQTT()

    def connectToDB(self):
        self.dbClient = DBConnector()
        # self.dbClient = MongoClient("mongodb://root:example@mongodb:27017/")
        # self.vertical_farmDb = self.dbClient.vertical_farm

    def on_box_register(self, message: RegisterBoxMessage):
        print("Vertical Farm Register Box")
        print("TODO: Handle Register of Box. Is there already a box ?")
        print(message)
        self.dbClient.add_box(message)

    def get_boxes(self):
        boxes = list(self.dbClient.boxes.values())
        data = []
        for box in boxes:
            data.append({
                "building": box["building"],
                "room": box["room"],
                "box": box["box"],
                "state": box["state"],
            })
        return {
            "boxes": data
        }

    def on_sensor_register(self, message: RegisterSensorMessage):
        print("Vertical Farm Register Sensor")
        print("TODO: Handle Register of Box. Is there already a box ?")
        print(message)
        self.dbClient.add_sensor(message)

    def on_box_send_message(self, message: SensorDataMessage):
        print("Vertical Farm Register Box")
        print("TODO: Handle to save the message to the database")
        print(message)

    def get_sensors(self, box_name):
        box = self.dbClient.boxes.get()

    def get_box(self, box_key):
        if self.dbClient.has_box(box_key):
            return self.dbClient.get_box(box_key)

    def on_sensor_receive_data(self, topic, message):
        print(topic)

        keys = topic.split("/")
        box_key = '/'.join(keys[0:3])

        if self.dbClient.has_box(box_key):
            self.dbClient.add_sensor_data(message)
            box = self.dbClient.get_box(box_key)



