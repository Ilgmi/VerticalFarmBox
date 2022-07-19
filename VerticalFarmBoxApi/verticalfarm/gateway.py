import json

import paho.mqtt.client as mqtt


class Gateway:
    mqtt_client: mqtt.Client

    on_sensor_receive_data_call_back = []

    def connectToMQTT(self):

        self.mqtt_client = mqtt.Client("VerticalFarmBackend")

        self.mqtt_client.on_connect = self.__on_connect
        self.mqtt_client.on_message = self.__on_message

        self.mqtt_client.username_pw_set("admin", "password")
        self.mqtt_client.connect("mosquitto", 1883, 70)

        self.mqtt_client.loop_start()
        self.mqtt_client.subscribe("+/+/+/+/+", qos=2)

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

        self.__on_sensor_receive_data(message)

    def __on_sensor_receive_data(self, message):
        data = json.loads(message.payload.decode())
        for func in self.on_sensor_receive_data_call_back:
            func(message.topic, data)

    def on_sensor_receive_data(self, func):
        self.on_sensor_receive_data_call_back.append(func)

    def send_action(self, topic, action):
        print("Send Action to", topic, "with data", action)
        self.mqtt_client.publish(topic, json.dumps(action))

    def subscribe_to(self, topic, fuc):
        print("Subscribe to", topic)
        self.mqtt_client.subscribe(topic, 2)
        self.mqtt_client.message_callback_add(topic, fuc)
