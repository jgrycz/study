from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)

status = True

while True:
    GPIO.output(16, status)
    sleep(1)
    status = not status

