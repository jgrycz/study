from .base import BaseRPIObject

from .led import Led


class StatusLeds(BaseRPIObject):
    def __init__(self, red, yellow, green, init_state=None):
        super().__init__()
        self.state = None
        self.red = Led(red, 'red')
        self.yellow = Led(yellow, 'yellow')
        self.green = Led(green, 'green')
        if init_state == 'good':
            self.set_good_state()
        elif init_state == 'warning':
            self.set_warning_state()
        elif init_state == 'error':
            self.set_error_state()

    def set_good_state(self):
        if self.state == 'good':
            return

        print("Seting good status")
        self.green.on()
        self.yellow.off()
        self.red.off()
        self.state = 'good'

    def set_warning_state(self):
        if self.state == 'warning':
            return

        print("Seting warning status")
        self.green.off()
        self.yellow.on()
        self.red.off()
        self.state = 'warning'

    def set_error_state(self):
        if self.state == 'error':
            return

        print("Seting error status")
        self.green.off()
        self.yellow.off()
        self.red.on()
        self.state = 'error'
