import json

from pymongo import MongoClient

from ai.planner import Planner
from verticalfarm.box import MoistureLevel
from verticalfarm.context_component import ContextComponent
from verticalfarm.db_connector import DBConnector, InMemoryDBConnector, MongoDBConnector
from verticalfarm.gateway import Gateway
from verticalfarm.messages import RegisterBoxMessage, RegisterSensorMessage, SensorDataMessage
from verticalfarm.orchestrator import Orchestrator


class VerticalFarm:
    gateway: Gateway
    dbClient: DBConnector
    vertical_farmDb: any
    planner: Planner
    orchestrator: Orchestrator
    context: ContextComponent

    def __init__(self):
        self.connectToMQTT()
        self.connectToDB()
        # self.gateway.on_box_register(self.on_box_register)
        self.gateway.on_sensor_receive_data(self.on_sensor_receive_data)
        self.planner = Planner()
        self.orchestrator = Orchestrator(self.gateway)
        self.context = ContextComponent(self.gateway)
        # test = self.planner.solve()
        x = 1

    def connectToMQTT(self):
        self.gateway = Gateway()
        self.gateway.connectToMQTT()

    def connectToDB(self):
        self.dbClient = MongoDBConnector()
        # self.dbClient = InMemoryDBConnector()
        # self.dbClient = MongoClient("mongodb://root:example@mongodb:27017/")
        # self.vertical_farmDb = self.dbClient.vertical_farm

    def on_box_register(self, message: RegisterBoxMessage):
        print("Vertical Farm Register Box")
        print("TODO: Handle Register of Box. Is there already a box ?")
        if not self.dbClient.has_box(message.get_key()):
            self.dbClient.add_box(message)
        return True

    def get_boxes(self, skip: 0, take: 10):
        result = self.dbClient.get_boxes(skip, take)
        data = []
        for box in result.boxes:
            data.append({
                "building": box["building"],
                "room": box["room"],
                "name": box["name"],
                "state": json.loads(box["state"]),
            })
        return {
            "count": result.count,
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
        # box = self.dbClient.get_sensors()
        return []

    def get_box(self, box_key):
        if self.dbClient.has_box(box_key):
            return self.dbClient.get_box(box_key)

    def on_sensor_receive_data(self, topic, message):
        print(topic)

        keys = topic.split("/")
        box_key = '/'.join(keys[0:3])

        if self.dbClient.has_box(box_key):
            self.dbClient.add_sensor_data(topic, message)
            box = self.dbClient.get_box(box_key)

            # TODO: use context to create values
            new_value = ContextComponent.map(keys[3], message["value"]["value"])
            # TODO: update current box values

            possible_state_change = False

            if keys[3] == "temperature":
                possible_state_change = abs(box.temperature - new_value > 2)
                box.temperature = new_value
            elif keys[3] == "humidity":
                possible_state_change = abs(box.humidity - new_value) > 10
                box.humidity = new_value
            elif keys[3] == "moisture":
                possible_state_change = new_value == MoistureLevel.dry
                box.plant.moisture_level = new_value
            elif keys[3] == "light":
                possible_state_change = abs(box.light - new_value) > 10
                box.light = new_value
            elif keys[3] == "roof":
                box.roof = new_value

            # TODO: if state change calc solution for problem
            if possible_state_change:
                test = 1
            # TODO: send action to sensors
            if possible_state_change:
                test = 2
