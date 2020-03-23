from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

buzzer = 12
GPIO.setup(buzzer, GPIO.OUT)

status = True

def beep(beep_time=0.1):
    GPIO.output(buzzer, True)
    sleep(beep_time)
    GPIO.output(buzzer, False)

for _ in range(3):
    beep()
    sleep(3)
