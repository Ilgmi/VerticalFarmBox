from pi.actuators.actuator import Actuator
from pi.mqtt_client import MQTTClient


class RoofActuators(Actuator):
    mqtt_client: MQTTClient

    def __init__(self, mqtt_client, building, room, name, type_id):
        super().__init__(building, room, name, type_id, "roof", "1")
        self.mqtt_client = mqtt_client

    def __on_open_roof(self, message):
        print(message.topic)
        # implement to open the roof
        self.mqtt_client.publish_data(self.get_topic() + "/roof-opened", "")

    def __on_close_roof(self, message):
        print(message.topic)
        # implement to close the roof
        self.mqtt_client.publish_data(self.get_topic() + "/roof-opened", "")

    def run(self):
        self.mqtt_client.subscribe_to_topic(self.get_topic() + "/open-roof", self.__on_open_roof)
        self.mqtt_client.subscribe_to_topic(self.get_topic() + "/close-roof", self.__on_close_roof)
