import json

from ai.planner import Planner
from verticalfarm.db_connector import DBConnector
from verticalfarm.domain.plant import MoistureLevel
from verticalfarm.gateway import Gateway


class ContextComponent:
    gateway: Gateway
    database: DBConnector
    planner: Planner

    def __init__(self, gateway: Gateway, database: DBConnector, planner: Planner):
        self.gateway = gateway
        self.database = database
        self.planner = planner

    def init(self):
        print("sub to roof-opened")
        self.gateway.subscribe_to("+/+/+/roof/+/roof-opened", self.__on_roof_opened)
        self.gateway.subscribe_to("+/+/+/roof/+/roof-closed", self.__on_roof_closed)

        self.gateway.subscribe_to("+/+/+/display/+/text-is-set", self.__on_text_is_set)
        self.gateway.subscribe_to("+/+/+/display/+/display-cleared", self.__on_display_is_cleared)

        self.gateway.subscribe_to("+/+/+/water-pump/+/pump-started", self.__on_water_pump_started)
        self.gateway.subscribe_to("+/+/+/water-pump/+/pump-stopped", self.__on_water_pump_stopped)

        self.gateway.subscribe_to("+/+/+/humidity/+", self.__on_receive_humidity_data)
        self.gateway.subscribe_to("+/+/+/light/+", self.__on_receive_light_data)
        self.gateway.subscribe_to("+/+/+/moisture/+", self.__on_receive_moisture_data)
        self.gateway.subscribe_to("+/+/+/temperature/+", self.__on_receive_temperature_data)

    def state_changed(self, box_key):
        box = self.database.get_box(box_key)
        self.planner.solve(box_key, box)

    def get_box_key(self, msg):
        topic = msg.topic
        keys = topic.split("/")
        return "/".join(keys[0:3])

    def __on_roof_opened(self, mosq, obj, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        box_key = self.get_box_key(msg)
        if self.database.has_box(box_key):
            self.database.update_box(box_key, {"roof": 1})

    def __on_roof_closed(self, mosq, obj, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        box_key = self.get_box_key(msg)
        if self.database.has_box(box_key):
            self.database.update_box(box_key, {"roof": 0})

    def __on_text_is_set(self, mosq, obj, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        box_key = self.get_box_key(msg)
        if self.database.has_box(box_key):
            self.database.update_box(box_key, {"show_text": 1})

    def __on_display_is_cleared(self, mosq, obj, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        box_key = self.get_box_key(msg)
        if self.database.has_box(box_key):
            self.database.update_box(box_key, {"show_text": 0})

    def __on_water_pump_started(self, mosq, obj, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        box_key = self.get_box_key(msg)
        if self.database.has_box(box_key):
            box = self.database.get_box(box_key)
            watering_plant = int(box["watering_plant"])
            self.database.update_box(box_key, {"water_pump": 1, "watering_plant": watering_plant + 1})

    def __on_water_pump_stopped(self, mosq, obj, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        box_key = self.get_box_key(msg)
        if self.database.has_box(box_key):
            self.database.update_box(box_key, {"water_pump": 0})

    def __on_receive_humidity_data(self, mosq, obj, msg):
        print("Context receive humidity data")
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        box_key = self.get_box_key(msg)
        if self.database.has_box(box_key):
            data = json.loads(msg.payload.decode())
            box = self.database.get_box(box_key)
            new_value = data["value"]["value"]
            old_value = box["humidity"]
            self.database.update_box(box_key, {"humidity": new_value})
            if abs(new_value - old_value) > 5:
                self.state_changed(box_key)

    def __on_receive_light_data(self, mosq, obj, msg):
        print("Context receive light data")
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        box_key = self.get_box_key(msg)
        if self.database.has_box(box_key):
            data = json.loads(msg.payload.decode())
            box = self.database.get_box(box_key)
            new_value = data["value"]["value"]
            old_value = box["light"]
            self.database.update_box(box_key, {"light": new_value})

    def __on_receive_moisture_data(self, mosq, obj, msg):
        print("Context receive moisture data")
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        box_key = self.get_box_key(msg)
        if self.database.has_box(box_key):
            data = json.loads(msg.payload.decode())
            box = self.database.get_box(box_key)
            new_value = data["value"]["value"]
            moisture_level = self.map_moisture(new_value)
            old_value = box["plant"]["moisture_level"]
            self.database.update_box(box_key, {"plant.moisture_level": moisture_level})
            if moisture_level != old_value:
                self.state_changed(box_key)

    def __on_receive_temperature_data(self, mosq, obj, msg):
        print("Context receive temperature data")
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        box_key = self.get_box_key(msg)
        print(box_key)
        if self.database.has_box(box_key):
            data = json.loads(msg.payload.decode())
            box = self.database.get_box(box_key)
            new_value = data["value"]["value"]
            old_value = box["temperature"]
            self.database.update_box(box_key, {"temperature": new_value})
            if abs(old_value - new_value) > 5:
                self.state_changed(box_key)

    @staticmethod
    def map(sensor_type, value):
        actions = {
            "temperature": ContextComponent.map_temperature,
            "humidity": ContextComponent.map_humidity,
            "moisture": ContextComponent.map_moisture,
            "light": ContextComponent.map_light,
        }
        action = actions[sensor_type](value)
        if action is None:
            return value
        return action(value)

    @staticmethod
    def map_temperature(value) -> int:
        return value

    @staticmethod
    def map_humidity(value) -> int:
        return value

    @staticmethod
    def map_moisture(value) -> MoistureLevel:
        if value < 400:
            return MoistureLevel.dry
        if value >= 400 <= 700:
            return MoistureLevel.wet

        return MoistureLevel.very_wet

    @staticmethod
    def map_light(value) -> int:
        return value
