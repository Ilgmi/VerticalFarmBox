import json
from abc import abstractmethod
from dataclasses import dataclass
from typing import List

from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.cursor import Cursor

from verticalfarm.box import Box, Plant, MoistureLevel, Condition, BoxEncoder
from verticalfarm.messages import SensorDataMessage, RegisterBoxMessage, RegisterSensorMessage

@dataclass
class BoxesResult:
    count: int
    boxes: []


class DBConnector:

    @abstractmethod
    def add_box(self, message: RegisterBoxMessage):
        pass

    @abstractmethod
    def has_box(self, key):
        pass

    @abstractmethod
    def get_box(self, key) -> Box:
        pass

    @abstractmethod
    def update_box(self, key, sensor_data: SensorDataMessage):
        pass

    @abstractmethod
    def add_sensor(self, message: RegisterSensorMessage):
        pass

    @abstractmethod
    def add_sensor_data(self, key, message: SensorDataMessage):
        pass

    def get_boxes(self, skip, take) -> BoxesResult:
        pass


class MongoDBConnector(DBConnector):

    def __init__(self):
        self.dbClient = MongoClient("mongodb://root:example@mongodb:27017/")
        self.vertical_farmDb = self.dbClient.vertical_farm
        self.boxes = self.vertical_farmDb.boxes
        self.sensor_data = self.vertical_farmDb.sensor_data

    def __ini(self):
        self.dbClient = MongoClient("mongodb://root:example@mongodb:27017/")
        self.vertical_farmDb = self.dbClient.vertical_farm
        self.boxes = self.vertical_farmDb.boxes

    def add_box(self, message: RegisterBoxMessage):
        if not self.has_box(message.get_key()):
            box = Box(0, 0, 0, 0, 0, Plant(MoistureLevel.dry), Condition(25, 30), Condition(50, 60))
            boxToAdd = {
                "key": message.get_key(),
                "building": message.building,
                "room": message.room,
                "name": message.name,
                "connection-state": "connected",
                "state": json.dumps(box, cls=BoxEncoder)
            }
            result = self.boxes.insert_one(boxToAdd)
            return result.inserted_id
        return None

    def has_box(self, key):
        vertical_farmDb = self.dbClient["vertical_farm"]
        boxes = vertical_farmDb["boxes"]
        t = boxes.find()
        boxes: Cursor = self.boxes.find({'key': key})

        return boxes.retrieved > 0

    def get_boxes(self, skip, take) -> BoxesResult:
        boxes: Cursor = self.boxes.find()
        result = BoxesResult(boxes.retrieved, [])
        for box in boxes:
            result.boxes.append(box)
        print(result)
        return result

    def get_box(self, key):
        box = self.boxes.find_one({'key': key})
        return box

    def update_box(self, key, sensor_data: SensorDataMessage):
        pass

    def add_sensor(self, message: RegisterSensorMessage):
        pass

    def add_sensor_data(self, key, message: SensorDataMessage):
        self.sensor_data.insert_one({
            "key": key,
            "type_id": message.type_id,
            "sensor_type": message.sensor_type,
            "instance_id": message.instance_id,
            "timestamp": message.timestamp,
            "value": message.value
        })


class InMemoryDBConnector(DBConnector):
    boxes = {}
    sensors = {}
    sensor_datas = []

    def add_box(self, message: RegisterBoxMessage):
        key = message.get_key()
        box = Box(0, 0, 0, 0, 0, Plant(MoistureLevel.dry), Condition(25, 30), Condition(50, 60))
        self.boxes[key] = {
            "building": message.building,
            "room": message.room,
            "name": message.name,
            "state": "connected",
            "box": box
        }
        print(self.boxes)

    def has_box(self, key):
        return self.boxes.get(key) is not None

    def get_box(self, key) -> Box:
        return self.boxes.get(key)["box"]

    def update_box(self, key, sensor_data: SensorDataMessage):
        pass

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

    def add_sensor_data(self, key, message: SensorDataMessage):
        print("Add data", message)
        self.sensor_datas.append(message)
