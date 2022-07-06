import json
import time

import paho.mqtt.client as mqtt
import requests

from simulation.box import Box
from simulation.temperatur_sensor import TemperatureSensor


class BoxSimulator:
    interval: int
    box: Box
    mqtt_client: mqtt.Client

    def __init__(self, interval):
        self.interval = interval

    def init(self):
        self.box = Box("u38", "38.3", "Box123")
        self.box.add_sensor(TemperatureSensor(20, 10, 16, 35, "32kd403ks"))

        self.mqtt_client = mqtt.Client('Temperature publisher')

        self.mqtt_client.username_pw_set("admin", "password")
        self.mqtt_client.connect("mosquitto", 1883, 70)

    def __on_message(self, client, userdata, message):
        print('Message topic {}'.format(message.topic))
        print('Message payload:')
        print(json.loads(message.payload.decode()))

    def start(self):
        self.mqtt_client.loop_start()

        requests.post("http://localhost:8000/api/boxes", self.box.get_register_message())

        jmsg = json.dumps(self.box.get_register_message())
        self.mqtt_client.publish("register/"+self.box.get_key(), jmsg)

        while True:
            for sensor in self.box.sensors:
                message = sensor.get_message()
                jmsg = json.dumps(message)
                key = self.box.get_key() + sensor.sensor_type + "/" + sensor.instance_id
                self.mqtt_client.publish(key, jmsg, 2)
                print("Send Message: ", jmsg)
            time.sleep(self.interval)


print("Start Simulation")
box = BoxSimulator(10)
box.init()
box.start()
