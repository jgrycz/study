from drivers.seven_segments_display import SevenSegmentsDisplay
from drivers.status_leds import StatusLeds
from drivers.button import Button
from drivers.buzzer import Buzzer

from threading import Thread
from time import sleep
import RPi.GPIO as GPIO

# GPIO.setmode(GPIO.BCM)

display = SevenSegmentsDisplay(a=19, b=26, c=22, d=27, e=17, f=13, g=6, dp=5, init_number=0)
status_leds = StatusLeds(red=16, yellow=20, green=21, init_state='warning')
buzzer = Buzzer(12)


def _increment(channel):
    print("Invoking increment method")
    if display.current_number == 9:
        status_leds.set_error_state()
        buzzer.beep(beep_time=0.4)
        return
    if display.current_number == 8:
        status_leds.set_warning_state()
    else:
        status_leds.set_good_state()
    display.increment()
    buzzer.beep()


def _decrement(channel):
    print("Invoking decrement method")
    if display.current_number == 0:
        status_leds.set_error_state()
        buzzer.beep(beep_time=0.4)
        return
    if display.current_number == 1:
        status_leds.set_warning_state()
    else:
        status_leds.set_good_state()
    display.decrement()
    buzzer.beep()

def _reset(channel):
    print("Invoking reset method")
    Thread(target=display.blink_number, kwargs={'times': 2}).start()
    thread = Thread(target=buzzer.beep, kwargs={'times': 2})
    thread.start()
    thread.join()
    display.display_number(0)
    status_leds.set_warning_state()


inc = Button(18, "increment", _increment)
dec = Button(23, "decrement", _decrement)
reset = Button(24, "reset", _reset)


if "__main__" == __name__:
    message = input("Press enter to quit\n\n")
    GPIO.cleanup()
