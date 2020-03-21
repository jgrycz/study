import RPi.GPIO as GPIO

class Button:
    def __init__(self, gpio_num, name, callback=None):
        self.gpio_num = gpio_num
        self.name = name
        print("Setuping on ({}) button as input gpio: {}".format(self.name, self.gpio_num))
        GPIO.setup(self.gpio_num, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        if callback:
            GPIO.add_event_detect(self.gpio_num, GPIO.BOTH, callback=callback, bouncetime=500)

    def is_pushed(self):
        return not GPIO.input(self.gpio_num)
