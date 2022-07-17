from verticalfarm.gateway import Gateway


class Orchestrator:
    gateway: Gateway

    actor_commands = {
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
            'type': 'water-pump',
            'action': 'stop-pump'
        },
        'do_not_show_change_water_text': {
            'type': 'water-pump',
            'action': 'stop-pump'
        },

    }

    def __init__(self, gateway: Gateway):
        self.gateway = gateway

    def send(self, box_key, sensor, instance, action):
        self.gateway.send_action(box_key + "/" + sensor + "/" + instance + "/action", action)
