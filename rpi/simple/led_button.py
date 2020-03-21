from time import sleep
import RPi.GPIO as GPIO

LED_PIN = 16
BUTTON_PIN = 20

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        GPIO.output(LED_PIN, GPIO.input(BUTTON_PIN))
        sleep(0.1)
finally:
    GPIO.output(LED_PIN, False)
    GPIO.cleanup()
