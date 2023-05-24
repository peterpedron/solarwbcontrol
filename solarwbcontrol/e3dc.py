import logging
import time
import json
import mqtt_connection
from time_range_average import TimeRangeAverage

TOPIC_E3DC_STATUS = "e3dc/status"
VALIDITY_TIMEOUT = 60.0  # timeout
VALUE_AVERAGE = 120.0


class E3DC:
    def __init__(self):
        self.mqtt_client = mqtt_connection.init(client_id="solarwb_control_e3dc")
        self.__battery_soc = TimeRangeAverage(VALUE_AVERAGE)
        self.__power_sun = TimeRangeAverage(VALUE_AVERAGE)
        self.__power_house = TimeRangeAverage(VALUE_AVERAGE)
        self.__last_timestamp = 0.0

        def mqtt_connection_callback(client, userdata, flags, rc):
            if rc == 0:
                logging.info("E3DC: MQTT Connection established!")
                self.mqtt_client.subscribe(TOPIC_E3DC_STATUS)
            else:
                logging.info("E3DC: MQTT connection failed! Return Code %d\n", rc)

        self.mqtt_client.on_connect = mqtt_connection_callback
        self.mqtt_client.on_message = self.on_status_update
        self.mqtt_client.loop_start()

    def is_valid(self):
        return (time.time() - self.__last_timestamp) < VALIDITY_TIMEOUT

    def __reset_values(self):
        self.__battery_soc.reset()
        self.__power_sun.reset()
        self.__power_house.reset()
        self.__last_timestamp = 0.0

    def __check_validity(self):
        if not self.is_valid():
            logging.warn("E3DC status is invalid!")
            self.__reset_values()

    def on_status_update(self, client, userdata, message):
        if message.topic == TOPIC_E3DC_STATUS:
            logging.debug("E3DC status update!")
            timestamp = time.time()
            e3dc_status = json.loads(message.payload.decode())
            self.__battery_soc.add_value(timestamp, e3dc_status["battery_soc"])
            self.__power_sun.add_value(timestamp, e3dc_status["energy_sun"])
            self.__power_house.add_value(timestamp, e3dc_status["energy_house"])
            logging.debug(f"PowerHouse: {e3dc_status['energy_house']}W")
            self.__last_timestamp = timestamp
            logging.info(
                f"E3DC values: Battery {self.__battery_soc.average()}%, PowerSun {self.__power_sun.average()}W, PowerHouse {self.__power_house.average()}W"
            )

    def battery_soc(self):
        self.__check_validity()
        return self.__battery_soc.average()

    def power_sun(self):
        self.__check_validity()
        return self.__power_sun.average()

    def power_house(self):
        self.__check_validity()
        return self.__power_house.average()
