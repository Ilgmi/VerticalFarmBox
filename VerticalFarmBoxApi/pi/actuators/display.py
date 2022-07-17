from actuators.actuator import Actuator
from mqtt_client import MQTTClient
import time,sys, json




class Display(Actuator):
    mqtt_client: MQTTClient

    DISPLAY_RGB_ADDR = 0x62
    DISPLAY_TEXT_ADDR = 0x3e

    def __init__(self, mqtt_client, building, room, name, type_id):
        super().__init__(building, room, name, type_id, "display", "1")
        self.bus = None
        self.mqtt_client = mqtt_client

        if sys.platform == 'uwp':
            import winrt_smbus as smbus
            self.bus = smbus.SMBus(1)
        else:
            import smbus
            import RPi.GPIO as GPIO
            rev = GPIO.RPI_REVISION
            if rev == 2 or rev == 3:
                self.bus = smbus.SMBus(1)
            else:
                self.bus = smbus.SMBus(0)

    def __on_show_text(self, message):
        try:
            print(f"Show Text from Topic: '{message.topic}'")
            # implement to open the roof

            data = json.loads(message.payload.decode())
            message = data["message"]
            print(message)
            if message is not None:
                self.__set_text(message)

            self.mqtt_client.publish_data(self.get_topic() + "/text-is-set", "")
        except:
            print("Some Error on Parsing")


    def __on_clear(self, message):
        print(f"clear text")
        # implement to close the roof
        self.__text_command(0x01)  # clear display
        self.mqtt_client.publish_data(self.get_topic() + "/display-cleared", "")

    def init(self):
        self.mqtt_client.subscribe_to_topic(self.get_topic() + "show-text", self.__on_show_text)
        self.mqtt_client.subscribe_to_topic(self.get_topic() + "clear", self.__on_clear)

    def run(self):
        pass

    def __set_rgb(self, r, g, b):
        self.bus.write_byte_data(self.DISPLAY_RGB_ADDR, 0, 0)
        self.bus.write_byte_data(self.DISPLAY_RGB_ADDR, 1, 0)
        self.bus.write_byte_data(self.DISPLAY_RGB_ADDR, 0x08, 0xaa)
        self.bus.write_byte_data(self.DISPLAY_RGB_ADDR, 4, r)
        self.bus.write_byte_data(self.DISPLAY_RGB_ADDR, 3, g)
        self.bus.write_byte_data(self.DISPLAY_RGB_ADDR, 2, b)

    def __text_command(self, cmd):
        self.bus.write_byte_data(self.DISPLAY_TEXT_ADDR, 0x80, cmd)

    def __set_text(self, text):

        self.__text_command(0x01)  # clear display
        time.sleep(.05)
        self.__text_command(0x08 | 0x04)  # display on, no cursor
        self.__text_command(0x28)  # 2 lines
        time.sleep(.05)
        count = 0
        row = 0
        for c in text:
            if c == '\n' or count == 16:
                count = 0
                row += 1
                if row == 2:
                    break
                self.__text_command(0xc0)
                if c == '\n':
                    continue
            count += 1
            self.bus.write_byte_data(self.DISPLAY_TEXT_ADDR, 0x40, ord(c))

    def set_text_norefresh(self, text):
        self.__text_command(0x02) # return home
        time.sleep(.05)
        self.__text_command(0x08 | 0x04) # display on, no cursor
        self.__text_command(0x28) # 2 lines
        time.sleep(.05)
        count = 0
        row = 0
        while len(text) < 32: #clears the rest of the screen
            text += ' '
        for c in text:
            if c == '\n' or count == 16:
                count = 0
                row += 1
                if row == 2:
                    break
                self.__text_command(0xc0)
                if c == '\n':
                    continue
            count += 1
            self.bus.write_byte_data(self.DISPLAY_TEXT_ADDR,0x40,ord(c))