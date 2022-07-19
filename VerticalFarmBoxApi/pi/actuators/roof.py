import time,json

import RPi.GPIO as GPIO

from actuators.actuator import Actuator
from mqtt_client import MQTTClient


class Roof(Actuator):
    mqtt_client: MQTTClient

    A = 18
    B = 23
    C = 24
    D = 25
    step_sleep = 0.002

    rotate_steps = 50

    def __init__(self, mqtt_client, building, room, name, type_id):
        super().__init__(building, room, name, type_id, "roof")
        self.mqtt_client = mqtt_client

    def __on_open_roof(self, message):
        print(f"Open Roof from Topic: '{message.topic}'")
        # implement to open the roof

        self.init_stepper()

        self.left(self.rotate_steps)
        self.cleanup()

        self.mqtt_client.publish_data(self.get_topic() + "/roof-opened", "")



    def __on_close_roof(self, message):
        print(f"close Roof from Topic: '{message.topic}'")
        # implement to close the roof

        self.init_stepper()

        self.right(self.rotate_steps)
        self.cleanup()

        self.mqtt_client.publish_data(self.get_topic() + "/roof-closed", "")

    def __on_init_roof(self, message):
        print(f"close Roof from Topic: '{message.topic}'")
        # implement to close the roof
        try:

            data = json.loads(message.payload.decode())
            print(data)
            direction = True
            steps = int(data["steps"])
            direction = bool(data["direction"])
            if steps >= 0 or steps <= 512:
                self.init_stepper()
                if direction:
                    self.left(steps)
                else:
                    self.right(steps)
                self.cleanup()
        except:
            print("Some Error on parsing")

    def init(self):
        self.mqtt_client.subscribe_to_topic(self.get_topic() + "/open-roof", self.__on_open_roof)
        self.mqtt_client.subscribe_to_topic(self.get_topic() + "/close-roof", self.__on_close_roof)
        self.mqtt_client.subscribe_to_topic(self.get_topic() + "/init", self.__on_init_roof)
        self.mqtt_client.publish_data(self.get_topic() + "/roof-closed", "")

    def run(self):
        pass

    def init_stepper(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.A, GPIO.OUT)
        GPIO.setup(self.B, GPIO.OUT)
        GPIO.setup(self.C, GPIO.OUT)
        GPIO.setup(self.D, GPIO.OUT)
        GPIO.output(self.A, False)
        GPIO.output(self.B, False)
        GPIO.output(self.C, False)
        GPIO.output(self.D, False)

    def cleanup(self):
        GPIO.output(self.A, False)
        GPIO.output(self.B, False)
        GPIO.output(self.C, False)
        GPIO.output(self.D, False)
        GPIO.cleanup()

    def left(self, step):
        for i in range(step):
            self.Step1()
            self.Step2()
            self.Step3()
            self.Step4()
            self.Step5()
            self.Step6()
            self.Step7()
            self.Step8()

    def right(self, step):
        for i in range(step):
            self.Step8()
            self.Step7()
            self.Step6()
            self.Step5()
            self.Step4()
            self.Step3()
            self.Step2()
            self.Step1()

    def Step1(self):
        GPIO.output(self.D, True)
        time.sleep(self.step_sleep)
        GPIO.output(self.D, False)

    def Step2(self):
        GPIO.output(self.D, True)
        GPIO.output(self.C, True)
        time.sleep(self.step_sleep)
        GPIO.output(self.D, False)
        GPIO.output(self.C, False)

    def Step3(self):
        GPIO.output(self.C, True)
        time.sleep(self.step_sleep)
        GPIO.output(self.C, False)

    def Step4(self):
        GPIO.output(self.B, True)
        GPIO.output(self.C, True)
        time.sleep(self.step_sleep)
        GPIO.output(self.B, False)
        GPIO.output(self.C, False)

    def Step5(self):
        GPIO.output(self.B, True)
        time.sleep(self.step_sleep)
        GPIO.output(self.B, False)

    def Step6(self):
        GPIO.output(self.A, True)
        GPIO.output(self.B, True)
        time.sleep(self.step_sleep)
        GPIO.output(self.A, False)
        GPIO.output(self.B, False)

    def Step7(self):
        GPIO.output(self.A, True)
        time.sleep(self.step_sleep)
        GPIO.output(self.A, False)

    def Step8(self):
        GPIO.output(self.D, True)
        GPIO.output(self.A, True)
        time.sleep(self.step_sleep)
        GPIO.output(self.D, False)
        GPIO.output(self.A, False)
