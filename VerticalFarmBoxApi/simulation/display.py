from abc import ABC

from simulation.actuator import Actuator


class Display(Actuator, ABC):

    def __init__(self, instance_id):
        super().__init__("de.uni-stuttgart.iaas.sc", "display", instance_id)

    def toggle(self):
        print("Need new water")
