import time
import logging
import sys
import solarwbcontroller

# import systemd

cycle_time = 5

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    # Tell systemd that our service is ready
    # systemd.daemon.notify('READY=1')

    controller = solarwbcontroller.SolarWbController()

    while True:
        controller.step()
        time.sleep(cycle_time)
