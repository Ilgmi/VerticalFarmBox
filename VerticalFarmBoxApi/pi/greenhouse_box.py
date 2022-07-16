from pi.actuators.actuator import Actuator
from pi.mqtt_client import MQTTClient
from pi.sensors.sensor import Sensor
from pi.sensors.temperature import Temperature


class GreenhouseBox:
    building: str
    room: str
    name: str

    mqttClient: MQTTClient

    sensors = []
    actuators = []

    def __init__(self, building, room, name, ):
        self.building = building
        self.room = room
        self.name = name
        self.mqttClient = MQTTClient(name)

        typeId = "de.uni-stuttgart.iaas.sc"

        self.sensors.append(Temperature(self.mqttClient, self.building, self.room, self.name, typeId, "1"))

    def __sensor_collect_data(self, sensor: Sensor):
        sensor.collect_data()

    def __actuators_listen(self, actuator: Actuator):
        actuator.run()
