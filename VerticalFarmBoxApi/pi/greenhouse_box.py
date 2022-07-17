import json
from threading import Thread

import requests

from actuators.actuator import Actuator
from actuators.display import Display
from actuators.water_pump import WaterPump
from mqtt_client import MQTTClient
from sensors.humidity import Humidity
from sensors.light import Light
from sensors.moisture import Moisture
from sensors.sensor import Sensor
from sensors.temperature import Temperature


class GreenhouseBox:
    building: str
    room: str
    name: str

    mqttClient: MQTTClient

    sensors = []
    actuators = []

    threads = []

    def __init__(self, building, room, name, ):
        print(f"Init GreenhouseBox with in Building '{building}' Room '{room}' Name '{name}'")
        self.building = building
        self.room = room
        self.name = name

    def find_backend(self):
        pass

    def register_to_backend(self):
        ip = "192.168.2.110"
        print(f"Try to register to {ip}")
        self.mqttClient = MQTTClient(self.name, ip)
        self.mqttClient.connectToMQTT()
        msg = json.dumps({
            "building": self.building,
            "room": self.room,
            "name": self.name
        })
        result = requests.post(f"http://{ip}:8000/api/boxes", msg)
        print(result.ok)

        type_id = "de.uni-stuttgart.iaas.sc"

        # self.sensors.append(Temperature(self.mqttClient, self.building, self.room, self.name, type_id, "1"))
        # self.sensors.append(Humidity(self.mqttClient, self.building, self.room, self.name, type_id, "1"))
        # self.sensors.append(Moisture(self.mqttClient, self.building, self.room, self.name, type_id, "1"))
        # self.sensors.append(Light(self.mqttClient, self.building, self.room, self.name, type_id, "1"))

        # self.actuators.append(WaterPump(self.mqttClient, self.building, self.room, self.name, type_id))
        self.actuators.append(Display(self.mqttClient, self.building, self.room, self.name, type_id))

        return result.ok

    def run(self):
        self.threads = [Thread(target=self.__sensor_collect_data, args=[sensor]) for sensor in self.sensors]
        self.threads.extend([Thread(target=self.__actuators_run, args=[actuator]) for actuator in self.actuators])

        for thread in self.threads:
            thread.start()

        [thread.join() for thread in self.threads]

    def __sensor_collect_data(self, sensor: Sensor):
        try:
            while True:
                sensor.collect_data()
        except:
            print("some error")
        finally:
            return True

    def __actuators_run(self, actuator: Actuator):
        actuator.init()
        try:
            while True:
                actuator.run()

        except:
            print("some error")
        finally:
            return True

