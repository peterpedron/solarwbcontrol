from paho.mqtt import client as mqtt_client
import json
import logging


'''
'''
def init(config_file="mqtt.conf", client_id="paho-client"):

    client = mqtt_client.Client(client_id)

    with open(config_file) as config_json:
        mqtt_config = json.load(config_json)

    # Mandatory connection info
    if ("host" not in mqtt_config.keys()):
        logging.error("No MQTT host found in mqtt config file: " + config_file)
        return None

    if ("port" not in mqtt_config.keys()):
        logging.error("No MQTT port found in mqtt config file: " + config_file)
        return None

    # Optional credential info
    if (("user" in mqtt_config) and ("password" in mqtt_config)):
        logging.info("Using MQTT credentials from mqtt config file: " + config_file)
        client.username_pw_set(mqtt_config["user"], mqtt_config["password"])
    else:
        logging.info("No MQTT credentials found in config file: " + config_file + ". Proceeding without authentication")

    # connect
    try:
        def mqtt_connection_callback(client, userdata, flags, rc):
            if rc == 0:
                logging.info("MQTT Connection established!")
            else:
                logging.info("MQTT connection failed! Return Code %d\n", rc)

        client.on_connect = mqtt_connection_callback

        client.connect(mqtt_config["host"], mqtt_config["port"])
        return client
    except:
        logging.error("MQTT connection could not be established. Check configuration in " + config_file)
    return

