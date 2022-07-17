import os

import requests

from verticalfarm.box import Box


class Planner:

    def solve(self, box: Box):
        print("request function help ")
        dir_name = os.path.dirname(os.getcwd())
        print(dir_name)
        with open(dir_name + "/VerticalFarmBoxApi/ai/domain.pddl", 'r') as domain_file, open(
                dir_name + "/VerticalFarmBoxApi/ai/problem.pddl",
                'r') as problem_file:
            print("files opened")
            domain_string = domain_file.read()
            problem_string = problem_file.read()

            problem_string.replace("$$actual_temp$$", str(box.temperature))
            problem_string.replace("$$actual_hum$$", str(box.humidity))

            problem_string.replace("$$min_temperature$$", str(box.temperature_condition.min_val))
            problem_string.replace("$$max_temperature$$", str(box.temperature_condition.max_val))

            problem_string.replace("$$min_humidity$$", str(box.humidity_condition.min_val))
            problem_string.replace("$$max_humidity$$", str(box.humidity_condition.max_val))

            problem_string.replace("$$watering_count$$", str(box.watering_plants))
            problem_string.replace("$$max_watering_count$$", str(20))

            print("files read")

            json = {
                'domain': domain_string,
                'problem': problem_string
            }

            response = requests.post("http://solver.planning.domains/solve", json=json).json()
            print("made request")
            return response
