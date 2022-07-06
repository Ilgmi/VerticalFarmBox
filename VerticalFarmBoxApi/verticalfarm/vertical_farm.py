import json

from pymongo import MongoClient

from verticalfarm.db_connector import DBConnector
from verticalfarm.gateway import Gateway
from verticalfarm.messages import RegisterBoxMessage, RegisterSensorMessage, SensorDataMessage


class VerticalFarm:
    gateway: Gateway
    dbClient: DBConnector
    vertical_farmDb: any

    def __init__(self):
        self.connectToMQTT()
        self.connectToDB()
        # self.gateway.on_box_register(self.on_box_register)
        self.gateway.on_sensor_receive_data(self.on_sensor_receive_data)

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
        return {
            "boxes": boxes
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

    def on_sensor_receive_data(self, message):
        self.dbClient.add_sensor_data(message)
