import time
import logging
import sys
import mqtt_connection
import solarwbcontroller
#import systemd

cycle_time = 5

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    # Tell systemd that our service is ready
    #systemd.daemon.notify('READY=1')

    mqtt_client = mqtt_connection.init(client_id ="solarwbcontrol")
    controller = solarwbcontroller.SolarWbController(mqtt_client)

    mqtt_client.loop_start()
    while True:
        logging.debug("MQTT client connection: "+ str(mqtt_client.is_connected()))
        controller.step()
        time.sleep(cycle_time)
