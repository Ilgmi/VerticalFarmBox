import os

import requests

from verticalfarm.domain.greenhouse_box import GreenhouseBox


class Planner:

    solve_map = {}

    def solve(self, box):
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

            problem_string = problem_string.replace("$$actual_temp$$", str(box["temperature"]))
            problem_string = problem_string.replace("$$actual_hum$$", str(box["humidity"]))

            problem_string = problem_string.replace("$$min_temperature$$", str(box["temperature_condition"]["min_val"]))
            problem_string = problem_string.replace("$$max_temperature$$", str(box["temperature_condition"]["max_val"]))

            problem_string = problem_string.replace("$$min_humidity$$", str(box["humidity_condition"]["min_val"]))
            problem_string = problem_string.replace("$$max_humidity$$", str(box["humidity_condition"]["max_val"]))

            problem_string = problem_string.replace("$$watering_count$$", str(box["watering_plants"]))
            problem_string = problem_string.replace("$$max_watering_count$$", str(20))

            print("files read")

            json = {
                'domain': domain_string,
                'problem': problem_string
            }


            response = requests.post("http://solver.planning.domains/solve", json=json).json()
            print("made request")
            return response
