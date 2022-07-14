from verticalfarm.gateway import Gateway


class Orchestrator:
    gateway: Gateway

    def __init__(self, gateway: Gateway):
        self.gateway = gateway

    def send(self, box_key, sensor, instance, action):
        self.gateway.send_action(box_key + "/" + sensor + "/" + instance + "/action", action)
