from enum import Enum


class MoistureLevel(int, Enum):
    dry = 0
    wet = 1
    very_wet = 2

class Plant:
    moisture_level: MoistureLevel = MoistureLevel.dry

    def __init__(self, moisture_level):
        self.moisture_level = moisture_level
