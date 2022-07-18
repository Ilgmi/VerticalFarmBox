import datetime
import json
import re
from abc import abstractmethod
from dataclasses import dataclass
from typing import List

from pymongo import MongoClient
from pymongo.collection import Collection

from verticalfarm.domain.greenhouse_box import GreenhouseBox, BoxEncoder
from verticalfarm.messages import SensorDataMessage, RegisterBoxMessage
from dateutil.parser import parse

@dataclass
class BoxesResult:
    count: int
    boxes: List[GreenhouseBox]


class DBConnector:

    @abstractmethod
    def add_box(self, message: RegisterBoxMessage):
        pass

    @abstractmethod
    def has_box(self, key) -> bool:
        pass

    @abstractmethod
    def get_box(self, key):
        pass

    @abstractmethod
    def update_box(self, key, box):
        pass

    @abstractmethod
    def add_sensor_data(self, key, message: SensorDataMessage):
        pass

    @abstractmethod
    def get_boxes(self, skip, take) -> BoxesResult:
        pass

    @abstractmethod
    def get_sensors_data(self, box_key):
        pass


class MongoDBConnector(DBConnector):

    def __init__(self):
        self.dbClient = MongoClient("mongodb://root:example@mongodb:27017/")
        self.vertical_farmDb = self.dbClient.VerticalFarm
        self.box: Collection = self.vertical_farmDb.Box
        self.sensor_data: Collection = self.vertical_farmDb.SensorData

    def add_box(self, message: RegisterBoxMessage):
        if not self.has_box(message.get_key()):
            box = GreenhouseBox.create_box(message.get_key(), message.building, message.room, message.name)
            j = json.loads(json.dumps(box, cls=BoxEncoder))
            result = self.box.insert_one(j)
            return result.inserted_id
        return None

    def has_box(self, key) -> bool:
        box = self.box.find_one({'_id': key})
        return box is not None

    def get_box(self, key):
        data = self.box.find_one({'_id': key})
        return data

    def get_boxes(self, skip, take) -> BoxesResult:
        data = self.box.find()
        boxes: List[GreenhouseBox] = []
        for b in data:
            boxes.append(b)

        result = BoxesResult(data.retrieved, boxes)

        return result

    def update_box(self, key, to_update):

        to_update["updated"] = datetime.datetime.now().strftime("%d-%m-%YT%H:%M:%S")
        new_values = {"$set": to_update}
        result = self.box.update_one({'_id': key}, new_values)

    def add_sensor_data(self, key, message):
        self.sensor_data.insert_one({
            "key": key,
            "type_id": message["type_id"],
            "sensor_type": message["sensor_type"],
            "instance_id": message["instance_id"],
            "timestamp": message["timestamp"],
            "value": message["value"]
        })

    def get_sensors_data(self, box_key: str):



        values = self.sensor_data.find({"key": { "$regex": f'{re.escape(box_key)}.*' }},
                                       {"instance_id": 1, "sensor_type": 1, "timestamp": 1, "value": 1}).sort(
            "sensor_type")

        data = {}
        for value in values:
            sensor_type = value.get("sensor_type")
            if sensor_type not in data.keys():
                data.setdefault(sensor_type, [])
            sensor_values: List = data[sensor_type]
            sensor_value = value.get("value")["value"]
            timestamp = value.get("timestamp")
            sensor_values.append({"name": parse(timestamp), "value": sensor_value})

        result = []
        for sensor_type in data:
            result.append({
                "name": sensor_type,
                "series": data[sensor_type]
            })
        return result


class InMemoryDBConnector(DBConnector):
    boxes = {}
    sensors = {}
    sensor_datas = []

    def add_box(self, message: RegisterBoxMessage):
        pass

    def has_box(self, key) -> bool:
        pass

    def get_box(self, key) -> GreenhouseBox:
        pass

    def get_boxes(self, skip, take) -> BoxesResult:
        pass

    def update_box(self, key, box: GreenhouseBox):
        pass

    def add_sensor_data(self, key, message: SensorDataMessage):
        print("Add data", message)
        self.sensor_datas.append(message)
