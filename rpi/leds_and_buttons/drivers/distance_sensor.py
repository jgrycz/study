from .base import BaseRPIObject

import RPi.GPIO as GPIO
import time


class DistanceSensor(BaseRPIObject):
    def __init__(self, trig, echo):
        super().__init__()
        self.trig = trig
        self.echo = echo

        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)

    def measure(self):
        GPIO.output(TRIG, False)
        time.sleep(1)

        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        while GPIO.input(self.echo) == 0:
            pulse_start = time.time()

        while GPIO.input(self.echo) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = round(pulse_duration * 17150, 2)
        return distance


if __name__ == "__main__":
    TRIG = 25
    ECHO = 4
    ds = DistanceSensor(trig=25, echo=4)
    print("Reading distance")
    distance = ds.measure()
    print("Distance: {}cm".format(distance))


