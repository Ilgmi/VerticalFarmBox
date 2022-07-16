import time

import grovepi

from pi.mqtt_client import MQTTClient
from pi.sensors.sensor import Sensor


class Light(Sensor):
    mqtt_Client: MQTTClient

    def __init__(self, mqtt_client, building, room, name, type_id, instance_id):
        super().__init__(building, room, name, type_id, "light", instance_id)
        self.mqtt_Client = mqtt_client
        self.port = 0

    # Collect data from temp
    def collect_data(self):
        light = grovepi.analogRead(self.port)
        data = {
            "value": light
        }
        self.mqtt_Client.publish_data(self.get_topic(), self.get_message(data))

        time.sleep(5)
