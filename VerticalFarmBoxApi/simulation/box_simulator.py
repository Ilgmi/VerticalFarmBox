import json
import time

import paho.mqtt.client as mqtt
import requests

from simulation.box import Box
from simulation.sensor import Sensor
from simulation.temperatur_sensor import TemperatureSensor


class BoxSimulator:
    interval: int
    box: Box
    mqtt_client: mqtt.Client

    def __init__(self, interval):
        self.interval = interval

    def init(self):
        self.box = Box("u38", "38.3", "Box123")

        self.mqtt_client = mqtt.Client('Temperature publisher')

        self.mqtt_client.username_pw_set("admin", "password")
        self.mqtt_client.connect("mosquitto", 1883, 70)

    def __on_message(self, client, userdata, message):
        print('Message topic {}'.format(message.topic))
        print('Message payload:')
        print(json.loads(message.payload.decode()))

    def send_sensordata(self, sensor: Sensor):
        message = sensor.get_message()
        jmsg = json.dumps(message)
        key = self.box.get_key() + sensor.sensor_type + "/" + sensor.instance_id
        self.mqtt_client.publish(key, jmsg, 2)
        print("Send Message: ", jmsg)

    def start(self):
        self.mqtt_client.loop_start()
        jmsg = json.dumps(self.box.get_register_message())
        requests.post("http://localhost:8000/api/boxes", jmsg)

        min_tick = 0
        h_tick = 0
        while True:

            if min_tick % 60 == 0:
                h_tick = h_tick + 1
                self.send_sensordata(self.box.moisture)
                self.send_sensordata(self.box.temperature)
                self.send_sensordata(self.box.humidity)

            if h_tick % 24 == 0:
                self.send_sensordata(self.box.water_level)

            min_tick = min_tick + 10
            time.sleep(self.interval)


print("Start Simulation")
box = BoxSimulator(10)
box.init()
box.start()
