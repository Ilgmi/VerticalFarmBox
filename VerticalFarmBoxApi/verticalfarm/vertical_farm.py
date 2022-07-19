import json
import threading

from ai.planner import Planner
from pi.udp_client import UdpClient
from verticalfarm.context_component import ContextComponent
from verticalfarm.db_connector import DBConnector, MongoDBConnector
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

        self.gateway.subscribe_to("+/+/+/+/+", self.__save_to_db)
        self.orchestrator = Orchestrator(self.gateway)
        self.planner = Planner(self.orchestrator)
        self.context = ContextComponent(self.gateway, self.dbClient, self.planner)
        self.context.init()
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

    def listen_to_box_connections(self):
        udpClient = UdpClient("192.168.2.110", "224.1.1.5", 10000)
        t = threading.Thread(name="provide-multicast-request", target=lambda: udpClient.wait_for_backend_requests())
        t.start()

    def on_box_register(self, message: RegisterBoxMessage):
        print("Vertical Farm Register Box")
        print("TODO: Handle Register of Box. Is there already a box ?")
        if not self.dbClient.has_box(message.get_key()):
            self.dbClient.add_box(message)
        return True

    def get_boxes(self, skip: 0, take: 10):
        result = self.dbClient.get_boxes(skip, take)
        return result

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

    def __save_to_db(self, mosq, obj, msg):
        print("Receive data from sensor", msg.topic)
        keys = msg.topic.split("/")
        box_key = '/'.join(keys[0:3])
        if self.dbClient.has_box(box_key):
            self.dbClient.add_sensor_data(msg.topic, json.loads(msg.payload.decode()))

    def on_sensor_receive_data(self, topic, message):
        print(topic)

        keys = topic.split("/")
        box_key = '/'.join(keys[0:3])

    def get_box_sensors_data(self, box_key):
        return self.dbClient.get_sensors_data(box_key)

    def toggle_roof(self, box_id):
        if not self.dbClient.has_box(box_id):
            return False
        box = self.dbClient.get_box(box_id)
        if box["roof"] == 0:
            self.orchestrator.send(box_id, 'roof', "open-roof")
        elif box["roof"] == 1:
            self.orchestrator.send(box_id, 'roof', "close-roof")

    def water_plant(self, box_id):
        if not self.dbClient.has_box(box_id):
            return False
        box = self.dbClient.get_box(box_id)
        if box["water_pump"] == 0:
            self.orchestrator.send(box_id, 'water-pump', "start-pump")

    def move_roof(self, box_id, move_roof):
        if not self.dbClient.has_box(box_id):
            return False
        self.dbClient.update_box(box_id, {"roof": 0})
        self.orchestrator.send(box_id, 'roof', "init", {
            "direction": move_roof.direction,
            "steps": move_roof.steps
        })

    def update_conditions(self, box_id, conditions):
        if not self.dbClient.has_box(box_id):
            return False

        update_string = {"temperature_condition.min_val": conditions.temperature_condition.min_val,
                         "temperature_condition.max_val": conditions.temperature_condition.max_val,
                         "humidity_condition.min_val": conditions.humidity_condition.min_val,
                         "humidity_condition.max_val": conditions.humidity_condition.max_val,
                         }
        self.dbClient.update_box(box_id, update_string)

    def water_changed(self, box_id):
        if not self.dbClient.has_box(box_id):
            return False
        self.dbClient.update_box(box_id, {"watering_plants": 0})
