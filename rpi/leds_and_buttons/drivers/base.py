import RPi.GPIO as GPIO


class BaseRPIObject:
    def __init__(self):
        print("seting GPIO.BCM mode")
        GPIO.setmode(GPIO.BCM)

    def __del__(self):
        print("cleaning")
        GPIO.cleanup()
