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
        return actions[sensor_type](value)

    @staticmethod
    def map_temperature(value) -> int:
        return value

    @staticmethod
    def map_humidity(value) -> int:
        return value

    @staticmethod
    def map_moisture(value) -> int:
        return value

    @staticmethod
    def map_light(value) -> int:
        return value
