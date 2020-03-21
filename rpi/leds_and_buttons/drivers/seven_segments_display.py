from itertools import cycle
from time import sleep

import RPi.GPIO as GPIO


class SevenSegmentsDisplay:
    NUMBERS = {
        0: ['a', 'b', 'c', 'd', 'e', 'f'],
        1: ['b', 'c'],
        2: ['a', 'b', 'g', 'e', 'd'],
        3: ['a', 'b', 'c', 'd', 'g'],
        4: ['b', 'c', 'f', 'g'],
        5: ['a', 'c', 'd', 'f', 'g'],
        6: ['a', 'c', 'd', 'e', 'f', 'g'],
        7: ['a', 'b', 'c'],
        8: ['a', 'b', 'c', 'd', 'e', 'f', 'g'],
        9: ['a', 'b', 'c', 'd', 'f', 'g'],
        }

    def __init__(self, a, b, c, d, e, f, g, dp, init_number=None):
        self.current_number = None
        self.dp_state = False
        self.segments = {'a': a, 'b': b, 'c': c, 'd': d,
                         'e': e, 'f': f, "g": g}
        self.dp = dp

        for segment, num in self.segments.items():
            print('Seting up segment {}: {}'.format(segment, num))
            GPIO.setup(num, GPIO.OUT)


        if init_number is not None:
            self.display_number(init_number)

        print('Seting up dot: {}'.format(self.dp))
        GPIO.setup(self.dp, GPIO.OUT)

    def enable_all(self):
        GPIO.output(self.dp, True)
        for segment, num in self.segments.items():
            GPIO.output(num, True)

    def disable_all(self):
        GPIO.output(self.dp, False)
        for segment, num in self.segments.items():
            GPIO.output(num, False)

    def increment(self):
        if not self.current_number and self.current_number != 0:
            raise RuntimeError("Display doesn't display any number")
        elif self.current_number == 9:
            raise RuntimeError("Can not exceed 9")
        self.display_number(self.current_number + 1)

    def decrement(self):
        if self.current_number == 0:
            raise RuntimeError("Can not exceed 0")
        elif not self.current_number:
            raise RuntimeError("Display doesn't display any number")
        self.display_number(self.current_number - 1)

    def enable_dp(self):
        GPIO.output(self.dp, True)
        self.dp_state = True

    def disable_dp(self):
        GPIO.output(self.dp, False)
        self.dp_state = False

    def debug(self):
        for segment, num in self.segments.items():
            GPIO.output(num, False)

        for segment in 'abcdefg':
            num = self.segments[segment]
            print('Displaying segment {}: {}'.format(segment, num))
            GPIO.output(num, True)
            sleep(5)
            GPIO.output(num, False)

    def display_number(self, number):
        if 0 > number > 9:
            raise RuntimeError("Number {}, is out of range {0..9}".format(number))

        segments_to_display = self.NUMBERS[number]
        for segment, num in self.segments.items():
            state = True if segment in segments_to_display else False
            GPIO.output(num, state)

        self.current_number = number

    def count(self, num_range=range(10)):
        for num in num_range:
            self.display_number(num)
            sleep(1)

    def count_in_loop(self, num_range=range(10)):
        for num in cycle(num_range):
            self.display_number(num)
            sleep(1)

    def blink_dp(self, sleep_time=0.3, times=1):
        state = self.dp_state
        for _ in range(times):
            state = not state
            GPIO.output(self.dp, state)
            sleep(sleep_time)

        GPIO.output(self.dp, self.dp_state)

    def blink_number(self, sleep_time=0.1, times=1):
        for _ in range(times):
            self.disable_all()
            sleep(sleep_time)
            self.display_number(self.current_number)
            sleep(sleep_time)
