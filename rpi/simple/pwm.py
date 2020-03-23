from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)
red_led = GPIO.PWM(16, 50)
red_duty_cycle = 0
red_led.start(red_duty_cycle)

GPIO.setup(20, GPIO.OUT)
yellow_led = GPIO.PWM(20, 50)
yellow_duty_cycle = 100
yellow_led.start(yellow_duty_cycle)


try:
    while True:
        red_duty_cycle += 5
        print("+5, {}".format(red_duty_cycle))
        if red_duty_cycle > 100:
            red_duty_cycle = 0
            print("reset")

        yellow_duty_cycle -= 5
        print("+5, {}".format(yellow_duty_cycle))
        if yellow_duty_cycle < 0:
            yellow_duty_cycle = 100
            print("reset")


        sleep(0.2)
        red_led.ChangeDutyCycle(red_duty_cycle)
        yellow_led.ChangeDutyCycle(yellow_duty_cycle)
except KeyboardInterrupt:
    print("THE END!")

red_led.stop()
GPIO.cleanup()
