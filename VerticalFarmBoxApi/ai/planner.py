import os

import requests


class Planner:

    def solve(self):
        print("request function help ")
        dir_name = os.path.dirname(os.getcwd())
        print(dir_name)
        with open(dir_name + "/VerticalFarmBoxApi/ai/domain.pddl", 'r') as domain_file, open(
                dir_name + "/VerticalFarmBoxApi/ai/problem.pddl",
                'r') as problem_file:
            print("files opened")
            domain_string = domain_file.read()
            problem_string = problem_file.read()
            print("files read")

            json = {
                'domain': domain_string,
                'problem': problem_string
            }

            response = requests.post("http://solver.planning.domains/solve", json=json).json()
            print("made request")
            return response
