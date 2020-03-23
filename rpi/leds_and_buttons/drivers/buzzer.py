from .base import BaseRPIObject

from time import sleep

import RPi.GPIO as GPIO


class Buzzer(BaseRPIObject):
    def __init__(self, gpio_num):
        super().__init__()
        self.gpio_num = gpio_num
        GPIO.setup(self.gpio_num, GPIO.OUT)

    def beep(self, beep_time=0.1, times=1):
        for _ in range(times):
            GPIO.output(self.gpio_num, True)
            sleep(beep_time/2)
            GPIO.output(self.gpio_num, False)
            sleep(beep_time/2)
