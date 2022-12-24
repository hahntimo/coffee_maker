import threading
import time
import os
import multiprocessing
import RPi.GPIO as GPIO


class PitcherSpinController(multiprocessing.Process):
    def __init__(self, task_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue

        self.revolution = 0  # revolutions per minute
        self.direction = 1  # 0 = CW | 1 = CCW
        self.running = False
        self.delay = 0
        self.spr = 6400  # steps per revolution
        self.DIR_PIN = 24
        self.STEP_PIN = 23
        self.MOTOR_PIN_1 = 14
        self.MOTOR_PIN_2 = 15
        self.MOTOR_PIN_3 = 18

    def run(self):
        self.start_thread()
        self.set_pins()

        while True:
            new_task, data = self.task_queue.get()
            print(new_task, data)
            if new_task == "change_parameters":
                self.change_parameters(new_revolution=data)
            elif new_task == "shutdown":
                GPIO.cleanup()
                print("CLEANUP SUCCESS")
                for _ in range(10):
                    print("sub kill attempt:", _)
                    os.exit()


    def set_pins(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.DIR_PIN, GPIO.OUT)
        GPIO.setup(self.STEP_PIN, GPIO.OUT)
        # GPIO.output(self.DIR_PIN, self.direction)

        GPIO.setup((self.MOTOR_PIN_1, self.MOTOR_PIN_2, self.MOTOR_PIN_3), GPIO.OUT)
        GPIO.output((self.MOTOR_PIN_1, self.MOTOR_PIN_2, self.MOTOR_PIN_3), (1, 0, 1))

    def start_thread(self):
        threading.Thread(target=self.handler).start()

    def change_parameters(self, new_revolution):
        self.revolution = abs(new_revolution)
        self.running = True if self.revolution != 0 else False
        self.direction = 0 if new_revolution > 0 else 1

        if new_revolution == 0:
            self.running = False

        elif new_revolution > 0:
            self.running = False
            self.direction = 0
            GPIO.output(self.DIR_PIN, self.direction)
            self.delay = 60 / (self.revolution * self.spr)
            self.running = True

        elif new_revolution < 0:
            self.running = False
            self.direction = 1
            GPIO.output(self.DIR_PIN, self.direction)
            self.delay = 60 / (self.revolution * self.spr)
            self.running = True

        print("DIRECTION:", self.direction)

    def handler(self):
        while True:
            if self.running:
                # print(f"subthread: {self.revolution} | {self.direction} | {step_counter}")
                GPIO.output(self.STEP_PIN, GPIO.HIGH)
                time.sleep(self.delay)
                GPIO.output(self.STEP_PIN, GPIO.LOW)
                time.sleep(self.delay)

    def cleanup(self):
        GPIO.cleanup()
        print("CLEANUP SUCCESS")