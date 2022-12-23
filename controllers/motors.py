import threading
try:
    import RPi.GPIO as GPIO
except:
    pass


class PitcherSpinnerController:
    def __init__(self):
        self.revolution = 0  # revolutions per minute
        self.direction = 0  # 0 = CW | 1 = CCW
        self.running = False
        self.DIR_PIN = 20
        self.STEP_PIN = 16

        self.setup_pins()

    def setup_pins(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.DIR_PIN, GPIO.OUT)
        GPIO.setup(self.STEP_PIN, GPIO.OUT)

    def start_thread(self):
        threading.Thread(target=self.handler).start()

    def change_parameters(self, new_revolution):
        self.revolution = abs(new_revolution)
        self.running = True if self.revolution != 0 else False
        self.direction = 0 if new_revolution > 0 else 1

    def handler(self):
        while True:
            while self.running:
                print(f"subthread: {self.revolution} | {self.direction}")

