from paho.mqtt import client as mqtt_client
import logging
import mqtt_connection
import e3dc

TOPIC_SUN_CHARGE = "solarwbcontrol/suncharge"


class SolarWbController:
    def __init__(self):
        self.mqtt_client = mqtt_connection.init(client_id="solarwbcontroller")

        self.__sun_charge_mode = True
        self.__e3dc = e3dc.E3DC()

        def mqtt_connection_callback(client, userdata, flags, rc):
            if rc == 0:
                logging.info("solarwbcontroller: MQTT Connection established!")
                self.mqtt_client.subscribe(TOPIC_SUN_CHARGE)
            else:
                logging.info(
                    "solarwbcontroller: MQTT connection failed! Return Code %d\n", rc
                )

        self.mqtt_client.on_connect = mqtt_connection_callback
        self.mqtt_client.on_message = self.on_topic_update
        self.mqtt_client.loop_start()

    def enable_sun_charge(self):
        if self.__sun_charge_mode == False:
            logging.info("Enabling SunCharge")
            self.__sun_charge_mode = True

    def disable_sun_charge(self):
        if self.__sun_charge_mode == True:
            logging.info("Disabling SunCharge")
            self.__sun_charge_mode = False

    def sun_charge_mode(self):
        return self.__sun_charge_mode

    def on_topic_update(self, client, userdata, message):
        if message.topic == TOPIC_SUN_CHARGE:
            logging.debug("SunCharge update received")
            value = int(message.payload.decode())
            if value == 0:
                self.disable_sun_charge()
            elif value == 1:
                self.enable_sun_charge()
            else:
                logging.warn(
                    f"Ignoring unsupported value '{value}' for topic {TOPIC_SUN_CHARGE}"
                )

    def step(self):
        logging.debug("Publish SunCharge: " + str(self.__sun_charge_mode))
        self.mqtt_client.publish(TOPIC_SUN_CHARGE, 1 if self.sun_charge_mode() else 0)
