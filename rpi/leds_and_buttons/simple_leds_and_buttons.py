from functools import wraps
from time import sleep
import RPi.GPIO as GPIO
import signal

RED_BUTTON = 18
YELLOW_BUTTON = 23
GREEN_BUTTON = 24

RED_LED = 16
YELLOW_LED = 20
GREEN_LED = 21

layout = {RED_BUTTON: (RED_LED, "RED"),
          YELLOW_BUTTON: (YELLOW_LED, "YELLOW"),
          GREEN_BUTTON: (GREEN_LED, "GREEN")}

GPIO.setmode(GPIO.BCM)


def memoize(func):
    cache = func.cache = {}
    @wraps(func)
    def memoized_func(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    return memoized_func


def setup():
    for button, (led, color) in layout.items():
        print("Setuping button: {}, and led: {}, color: {}".format(button, led, color))
        GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(led, GPIO.OUT)


@memoize
def cleanup(signum=None, frame=None):
    for _, (led, color) in layout.items():
        print("Cleanning led up: {}, color: {}".format(led, color))
        GPIO.output(led, False)
    GPIO.cleanup()


def work():
    try:
        while True:
            for button, (led, color) in layout.items():
                if not GPIO.input(button):
                    print("Noticed event button: {}".format(color))
                GPIO.output(led, not GPIO.input(button))
            sleep(0.1)
    finally:
        cleanup()


if "__main__" == __name__:
    signal.signal(signal.SIGTERM, cleanup)
    setup()
    work()
