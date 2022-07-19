import os
import traceback

import requests

from verticalfarm.domain.plant import MoistureLevel
from verticalfarm.orchestrator import Orchestrator


class Planner:
    orchestrator: Orchestrator

    def __init__(self, orchestrator: Orchestrator):
        self.orchestrator = orchestrator

    def solve(self, box_key, box):
        print("request function help ")
        dir_name = os.path.dirname(os.getcwd())
        print(dir_name)
        with open(dir_name + "/VerticalFarmBoxApi/ai/domain.pddl", 'r') as domain_file, open(
                dir_name + "/VerticalFarmBoxApi/ai/problem.pddl",
                'r') as problem_file:
            print("files opened")
            domain_string = domain_file.read()
            problem_string = problem_file.read()

            if box["water_pump"] == 0:
                problem_string = problem_string.replace("$$pump_state$$", "is_pump_off")
                problem_string = problem_string.replace("$$pump_state_goal$$", "is_pump_on")

            if box["water_pump"] == 1:
                problem_string = problem_string.replace("$$pump_state$$", "is_pump_on")
                problem_string = problem_string.replace("$$pump_state_goal$$", "is_pump_off")

            if box["roof"] == 0:
                problem_string = problem_string.replace("$$roof_state$$", "is_roof_close")
                problem_string = problem_string.replace("$$roof_state_goal$$", "is_roof_open")

            if box["roof"] == 1:
                problem_string = problem_string.replace("$$roof_state$$", "is_roof_open")
                problem_string = problem_string.replace("$$roof_state_goal$$", "is_roof_close")

            if box["show_text"] == 0:
                problem_string = problem_string.replace("$$show_text_state$$", "is_change_water_text_not_shown")
                problem_string = problem_string.replace("$$show_text_state_goal$$", "is_change_water_text_shown")

            if box["show_text"] == 1:
                problem_string = problem_string.replace("$$show_text_state$$", "is_change_water_text_shown")
                problem_string = problem_string.replace("$$show_text_state_goal$$", "is_change_water_text_not_shown")

            if box["plant"]["moisture_level"] == MoistureLevel.dry:
                problem_string = problem_string.replace("$$soil_state$$", "is_soil_dry")

            if box["plant"]["moisture_level"] == MoistureLevel.wet or box["plant"][
                "moisture_level"] == MoistureLevel.very_wet:
                problem_string = problem_string.replace("$$soil_state$$", "is_soil_wet")

            problem_string = problem_string.replace("$$actual_temp$$", str(box["temperature"]))
            problem_string = problem_string.replace("$$actual_hum$$", str(box["humidity"]))

            problem_string = problem_string.replace("$$min_temperature$$", str(box["temperature_condition"]["min_val"]))
            problem_string = problem_string.replace("$$max_temperature$$", str(box["temperature_condition"]["max_val"]))

            problem_string = problem_string.replace("$$min_humidity$$", str(box["humidity_condition"]["min_val"]))
            problem_string = problem_string.replace("$$max_humidity$$", str(box["humidity_condition"]["max_val"]))

            problem_string = problem_string.replace("$$watering_count$$", str(box["watering_plants"]))
            problem_string = problem_string.replace("$$max_watering_count$$", str(5))

            print("files read")

            json = {
                'domain': domain_string,
                'problem': problem_string
            }

            try:

                response = requests.post("http://solver.planning.domains/solve", verify=False, json=json).json()

                if response["status"] == "ok":
                    plan = response["result"]["plan"]
                    self.orchestrator.handle_new_plan(box_key, plan)
            except:
                print('error')
