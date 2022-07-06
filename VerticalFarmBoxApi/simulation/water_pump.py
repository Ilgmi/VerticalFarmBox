from simulation.actuator import Actuator


class WaterPump(Actuator):
    state = False

    def __init__(self, instance_id):
        super().__init__("de.uni-stuttgart.iaas.sc", "water_pump", instance_id)

    def toggle(self):
        self.state = not self.state
        if self.state:
            print("Pump is on")
        else:
            print("Pump is off")
