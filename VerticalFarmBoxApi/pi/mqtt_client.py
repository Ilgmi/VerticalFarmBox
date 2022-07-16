import json

import paho.mqtt.client as mqtt


class MQTTClient:
    mqtt_client: mqtt.Client

    on_sensor_receive_data_call_back = {}

    def __init__(self, name: str):
        self.mqtt_client = mqtt.Client("VerticalFarmBackend")

        self.mqtt_client.on_connect = self.__on_connect
        self.mqtt_client.on_message = self.__on_message

        self.mqtt_client.username_pw_set("admin", "password")
        self.mqtt_client.connect("mosquitto", 1883, 70)

    def connectToMQTT(self):

        self.mqtt_client.loop_start()

    def __del__(self):
        self.mqtt_client.loop_stop()

    def __on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("connected OK Returned code=", rc)
        else:
            print("Bad connection Returned code=", rc)

    def __on_message(self, client, userdata, message):
        print('Message topic {}'.format(message.topic))
        print('Message payload:')
        print(json.loads(message.payload.decode()))

        funcs = self.on_sensor_receive_data_call_back.get(message.topic)
        if funcs is not None:
            for func in funcs:
                func(message)

    def subscribe_to_topic(self, name, func):
        funcs = self.on_sensor_receive_data_call_back.get(name)
        if funcs is None:
            self.on_sensor_receive_data_call_back.setdefault(name, [func])
        else:
            funcs.append(func)
            self.on_sensor_receive_data_call_back.setdefault(name, funcs)

    def publish_data(self, topic, data):

        self.mqtt_client.publish(topic, json.dumps(data), qos=0, retain=False)
