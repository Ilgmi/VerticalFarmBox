from verticalfarm.gateway import Gateway


class Orchestrator:
    gateway: Gateway

    actor_actions = {
        'pump_on': {
            'type': 'water-pump',
            'action': 'start-pump'
        },
        'pump_off': {
            'type': 'water-pump',
            'action': 'stop-pump'
        },
        'open_roof': {
            'type': 'roof',
            'action': 'open-roof'
        },
        'close_roof': {
            'type': 'roof',
            'action': 'close-roof'
        },

        'show_change_water_text': {
            'type': 'display',
            'action': 'show-text',
            'data': 'Please change the water'
        },
        'do_not_show_change_water_text': {
            'type': 'display',
            'action': 'clear',
        },

    }

    def __init__(self, gateway: Gateway):
        self.gateway = gateway

    def handle_new_plan(self, box_key, plan):
        pass
        actions = self.actor_actions.keys()
        for act in plan:
            for action in actions:
                if act.find(action.lower()) != -1:
                    print(self.actor_actions[action])
                    self.send(box_key, self.actor_actions[action]["type"], self.actor_actions[action]["type"])

    def send(self, box_key, actuator, action, data=None):
        if data is None:
            data = {}
        self.gateway.send_action(box_key + "/" + actuator + "/" + action, data)
