from actuators.actuator import Actuator
from mqtt_client import MQTTClient

import grovepi

class WaterPump(Actuator):
    mqtt_client: MQTTClient

    relay = 3

    def __init__(self, mqtt_client, building, room, name, type_id):
        super().__init__(building, room, name, type_id, "water-pump")
        self.mqtt_client = mqtt_client
        grovepi.pinMode(self.relay, "OUTPUT")
        grovepi.digitalWrite(self.relay, 0)

    def __on_start_pump(self, message):
        print(f"Start Pump from Topic: '{message.topic}'")
        # implement to start pump

        grovepi.digitalWrite(self.relay, 1)

        self.mqtt_client.publish_data(self.get_topic() + "/pump-started", "")


    def __on_stop_pump(self, message):
        print(f"Start Pump from Topic: '{message.topic}'")
        # implement to stop pump

        grovepi.digitalWrite(self.relay, 0)

        self.mqtt_client.publish_data(self.get_topic() + "/pump-stopped", "")

    def init(self):
        self.mqtt_client.subscribe_to_topic(self.get_topic() + "/start-pump", self.__on_start_pump)
        self.mqtt_client.subscribe_to_topic(self.get_topic() + "/stop-pump", self.__on_stop_pump)
        self.mqtt_client.publish_data(self.get_topic() + "/pump-stopped", "")

    def run(self):
        pass



