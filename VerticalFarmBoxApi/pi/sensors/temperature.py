import math
import time

import grovepi

from mqtt_client import MQTTClient
from sensors.sensor import Sensor


class Temperature(Sensor):
    mqtt_Client: MQTTClient

    def __init__(self, mqtt_client, building, room, name, type_id, instance_id):
        super().__init__(building, room, name, type_id, "temperature", instance_id)
        self.mqtt_Client = mqtt_client
        self.sensor = 4
        self.blue = 0
        self.white = 1

    # Collect data from temp
    def collect_data(self):
        [temp, humidity] = grovepi.dht(self.sensor, self.blue)
        print(f"Try to collect temp {temp}")
        if not math.isnan(temp) and temp > 0:
            data = {
                "unit": "celsius",
                "value": temp
            }
            self.mqtt_Client.publish_data(self.get_topic(), self.get_message(data))
        time.sleep(5)
