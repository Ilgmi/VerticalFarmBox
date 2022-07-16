import time

import grovepi

from pi.mqtt_client import MQTTClient
from pi.sensors.sensor import Sensor


class Light(Sensor):
    mqtt_Client: MQTTClient

    def __init__(self, mqtt_client, building, room, name, type_id, instance_id):
        super().__init__(building, room, name, type_id, "moisture", instance_id)
        self.mqtt_Client = mqtt_client
        self.port = 1

    # Collect data from temp
    def collect_data(self):
        moisture = grovepi.analogRead(self.port)
        data = {
            "value": moisture
        }
        self.mqtt_Client.publish_data(self.get_topic(), self.get_message(data))

        time.sleep(5)
