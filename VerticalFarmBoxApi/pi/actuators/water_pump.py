from pi.actuators.actuator import Actuator
from pi.mqtt_client import MQTTClient


class WaterPump(Actuator):
    mqtt_client: MQTTClient

    def __init__(self, mqtt_client, building, room, name, type_id):
        super().__init__(building, room, name, type_id, "water-pump", "1")
        self.mqtt_client = mqtt_client

    def __on_start_pump(self, message):
        print(message.topic)
        # implement to start pump
        self.mqtt_client.publish_data(self.get_topic() + "/pump-started", "")
        #
        self.mqtt_client.publish_data(self.get_topic() + "/pump-stopped", "")

    def run(self):
        self.mqtt_client.subscribe_to_topic(self.get_topic() + "/start-pump", self.__on_start_pump)
