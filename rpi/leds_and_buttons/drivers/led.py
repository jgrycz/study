from .base import BaseRPIObject

from time import sleep

import RPi.GPIO as GPIO


class Led(BaseRPIObject):
    def __init__(self, gpio_num, name):
        super().__init__()
        self.gpio_num = gpio_num
        self.name = name
        self.state = False
        print("Setuping ({}) led on GPIO: {}".format(self.name, self.gpio_num))
        GPIO.setup(self.gpio_num, GPIO.OUT)

    def on(self):
        print("Turning {} on".format(self.name))
        GPIO.output(self.gpio_num, True)

    def off(self):
        print("Turning {} off".format(self.name))
        GPIO.output(self.gpio_num, False)

    def is_on(self):
        return self.state

    def blink(self, sleep_time=0.1, times=1):
        print("Blinking {}".format(self.name))
        state = self.state
        for _ in range(times):
            state = not state
            GPIO.output(self.gpio_num, state)
            sleep(sleep_time)

        GPIO.output(self.gpio_num, self.state)
