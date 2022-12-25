import threading
import time
import os
import json
import multiprocessing
import RPi.GPIO as GPIO
import datetime


class PitcherSpinController(multiprocessing.Process):
    def __init__(self, task_queue):
        multiprocessing.Process.__init__(self)
        self.config_json_path = f"{os.path.dirname(os.path.abspath('__main__'))}/configs/calibration.json"
        self.task_queue = task_queue

        self.revolution = 0
        self.direction = 1
        self.running = False
        self.theoretical_delay = 0  # theoretical pause between steps
        self.runtime_delay = 0      # delay occurring through runtime delay
        self.actual_delay = 0       # self.theoretical_delay - self.runtime_delay
        self.spr = 12800  # 6400  # steps per revolution
        self.DIR_PIN = 19
        self.STEP_PIN = 26
        self.MOTOR_PIN_1 = 16
        self.MOTOR_PIN_2 = 20
        self.MOTOR_PIN_3 = 21

    def run(self):
        with open(self.config_json_path, "r") as json_file:
            config_json = json.load(json_file)
        self.runtime_delay = config_json["spin_motor_delay"]
        print("RUNTIME_DELAY SPINNER:", self.runtime_delay)
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
                    try:
                        os._exit(_)
                    except:
                        print("sub kill fail", _)
            elif new_task == "calibrate":
                self.calibrate()

    def set_pins(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.DIR_PIN, GPIO.OUT)
        GPIO.setup(self.STEP_PIN, GPIO.OUT)
        # GPIO.output(self.DIR_PIN, self.direction)

        GPIO.setup((self.MOTOR_PIN_1, self.MOTOR_PIN_2, self.MOTOR_PIN_3), GPIO.OUT)
        GPIO.output((self.MOTOR_PIN_1, self.MOTOR_PIN_2, self.MOTOR_PIN_3), (1, 0, 1))

    def start_thread(self):
        threading.Thread(target=self.handler).start()

    def calibrate(self):
        self.running = False
        test_steps = 10000
        print("START CALIBRATION")
        start_time = time.time()
        for step in range(test_steps):
            GPIO.output(self.STEP_PIN, GPIO.HIGH)
            GPIO.output(self.STEP_PIN, GPIO.LOW)
        end_time = time.time()
        diff = end_time - start_time
        delay_per_substep = diff/(test_steps*2)
        print("CALIBRATE RESULT:", delay_per_substep)
        self.runtime_delay = delay_per_substep

        with open(self.config_json_path, "r") as json_file:
            config_json = json.load(json_file)
        config_json["spin_motor_delay"] = self.runtime_delay
        with open(self.config_json_path, "w") as json_file:
            json.dump(config_json, json_file)

        print("CALIBRATION DONE")

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
            self.actual_delay = (60 / (self.revolution * self.spr)) - self.runtime_delay
            if self.actual_delay < 0:
                self.actual_delay = 0
            self.running = True

        elif new_revolution < 0:
            self.running = False
            self.direction = 1
            GPIO.output(self.DIR_PIN, self.direction)
            self.actual_delay = (60 / (self.revolution * self.spr)) - self.runtime_delay
            if self.actual_delay < 0:
                self.actual_delay = 0
            self.running = True

        print("DIRECTION:", self.direction, "DELAY:", self.actual_delay)

    def handler(self):
        while True:
            if self.running:
                GPIO.output(self.STEP_PIN, GPIO.HIGH)
                time.sleep(self.actual_delay)
                GPIO.output(self.STEP_PIN, GPIO.LOW)
                time.sleep(self.actual_delay)

    def cleanup(self):
        GPIO.cleanup()
        print("CLEANUP SUCCESS")


class PumpController(multiprocessing.Process):
    def __init__(self, task_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
