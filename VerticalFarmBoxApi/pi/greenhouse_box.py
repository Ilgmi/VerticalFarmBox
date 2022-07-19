import json, time, traceback
from threading import Thread

import requests

from actuators.actuator import Actuator
from actuators.display import Display
from actuators.roof import Roof
from actuators.water_pump import WaterPump
from mqtt_client import MQTTClient
from sensors.humidity import Humidity
from sensors.light import Light
from sensors.moisture import Moisture
from sensors.sensor import Sensor
from sensors.temperature import Temperature
from udp_client import UdpClient


class GreenhouseBox:
    building: str
    room: str
    name: str

    mqttClient: MQTTClient

    sensors = []
    actuators = []

    threads = []
    udpClient: UdpClient

    def __init__(self, building, room, name, ):
        print(f"Init GreenhouseBox with in Building '{building}' Room '{room}' Name '{name}'")
        self.building = building
        self.room = room
        self.name = name
        self.udpClient = UdpClient("192.168.2.120", "224.1.1.5", 10000)
        self.backend_ip = "192.168.2.110"

    def find_backend(self):
        self.udpClient.on_backend_send_connection_data = self.__on_backend_send_ip
        t = Thread(target=lambda: self.udpClient.wait_for_backend_answer())
        t.start()
        self.udpClient.find_backend()

    def __on_backend_send_ip(self, ip):
        self.backend_ip = ip

    def register_to_backend(self):
        ip = self.backend_ip
        print(f"Try to register to {ip}")
        self.mqttClient = MQTTClient(self.name, ip)
        self.mqttClient.connectToMQTT()

        print("Wait for connection ...")
        time.sleep(5)

        msg = json.dumps({
            "building": self.building,
            "room": self.room,
            "name": self.name
        })
        result = requests.post(f"http://{ip}:8000/api/boxes", msg)
        print(result.ok)

        type_id = "de.uni-stuttgart.iaas.sc"

        self.sensors.append(Temperature(self.mqttClient, self.building, self.room, self.name, type_id, "1"))
        self.sensors.append(Humidity(self.mqttClient, self.building, self.room, self.name, type_id, "1"))
        self.sensors.append(Moisture(self.mqttClient, self.building, self.room, self.name, type_id, "1"))
        self.sensors.append(Light(self.mqttClient, self.building, self.room, self.name, type_id, "1"))

        self.actuators.append(WaterPump(self.mqttClient, self.building, self.room, self.name, type_id))
        self.actuators.append(Display(self.mqttClient, self.building, self.room, self.name, type_id))
        self.actuators.append(Roof(self.mqttClient, self.building, self.room, self.name, type_id))


        return result.ok

    def run(self):
        # self.threads = [Thread(target=self.__sensor_collect_data, args=[sensor]) for sensor in self.sensors]
        # self.threads.extend([Thread(target=self.__actuators_run, args=[actuator]) for actuator in self.actuators])
        #
        #
        #
        # for thread in self.threads:
        #     thread.start()

        print("Actuators")
        for actuator in self.actuators:
            actuator.init()

        while True:
            print('new selection round')
            for sensor in self.sensors:
                sensor.collect_data()
            time.sleep(5)


    def __sensor_collect_data(self, sensor: Sensor):
        try:
            while True:
                sensor.collect_data()
        except:
            print("some error")
            traceback.print_exc()
        finally:
            return True

    def __actuators_run(self, actuator: Actuator):
        actuator.init()
        try:
            while True:
                actuator.run()

        except:
            print("some error")
            traceback.print_exc()
        finally:
            return True

