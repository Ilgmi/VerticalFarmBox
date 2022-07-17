from verticalfarm.box import MoistureLevel
from verticalfarm.gateway import Gateway


class ContextComponent:
    plant: str

    gateway: Gateway

    def __init__(self, gateway: Gateway):
        self.gateway = gateway
        self.gateway.subscribe_to("/+/+/+/roof/+/roof-opened")
        self.gateway.subscribe_to("/+/+/+/water-pump/+/start-pump")


    @staticmethod
    def map(sensor_type, value):
        actions = {
            "temperature": ContextComponent.map_temperature,
            "humidity": ContextComponent.map_humidity,
            "moisture": ContextComponent.map_moisture,
            "light": ContextComponent.map_light,
        }
        action = actions[sensor_type](value)
        if action is None:
            return value
        return action(value)

    @staticmethod
    def map_temperature(value) -> int:
        return value

    @staticmethod
    def map_humidity(value) -> int:
        return value

    @staticmethod
    def map_moisture(value) -> MoistureLevel:
        if value < 400:
            return MoistureLevel.dry
        if value >= 400 <= 700:
            return MoistureLevel.wet

        return MoistureLevel.very_wet

    @staticmethod
    def map_light(value) -> int:
        return value
