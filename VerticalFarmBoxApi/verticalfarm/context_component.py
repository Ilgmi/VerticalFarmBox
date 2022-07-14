from verticalfarm.box import MoistureLevel


class ContextComponent:
    plant: str

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
