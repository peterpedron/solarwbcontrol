from paho.mqtt import client as mqtt_client
import logging

class SolarWbController:
    def __init__(self,  client : mqtt_client.Client):
        self.mqtt_client = client
        self.topic_sun_charge ="solarwbcontrol/suncharge"

        self.enable_sun_charge()

        self.mqtt_client.on_message = self.on_topic_update
        self.mqtt_client.subscribe(self.topic_sun_charge)

    def enable_sun_charge(self):
        self.__sun_charge_mode = True

    def disable_sun_charge(self):
        self.__sun_charge_mode = False

    def sun_charge_mode(self):
        return self.__sun_charge_mode

    def on_topic_update(self, client, userdata, message):
         if message.topic == self.topic_sun_charge:
             logging.info("SunCharge update received")
             value = int(message.payload.decode())
             if value == 0:
                 self.disable_sun_charge()
             elif value == 1:
                 self.enable_sun_charge()
             else:
                 logging.warn(f"Ignoring unsupported value '{value}' for topic {self.topic_sun_charge}")

    def step(self):
        logging.info("Publish SunCharge: " +  str(self.__sun_charge_mode))
        self.mqtt_client.publish(self.topic_sun_charge, 1 if self.sun_charge_mode() else 0)
