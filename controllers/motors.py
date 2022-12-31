import threading
import time
import os
import json
import multiprocessing
import RPi.GPIO as GPIO
from w1thermsensor import W1ThermSensor


calibration_json_path = f"{os.path.dirname(os.path.abspath('__main__'))}/configs/calibration.json"
spinner_calibration_diff = None


class PitcherSpinController(multiprocessing.Process):
    def __init__(self, task_queue, output_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.output_queue = output_queue

        self.revolution = 0
        self.direction = 1
        self.running = False
        self.theoretical_delay = 0  # theoretical pause between steps
        self.runtime_delay = 0      # delay occurring through runtime delay
        self.actual_delay = 0       # self.theoretical_delay - self.runtime_delay
        self.spr = 6400*2           # steps per revolution
        self.DIR_PIN = 19
        self.STEP_PIN = 26
        self.MOTOR_PIN_1 = 16
        self.MOTOR_PIN_2 = 20
        self.MOTOR_PIN_3 = 21

    def run(self):
        with open(calibration_json_path, "r") as json_file:
            config_json = json.load(json_file)
        self.runtime_delay = config_json["spin_motor_delay"]

        self.set_pins()
        threading.Thread(target=self.handler).start()

        while True:
            new_task, data = self.task_queue.get()

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

        GPIO.setup((self.MOTOR_PIN_1, self.MOTOR_PIN_2, self.MOTOR_PIN_3), GPIO.OUT)
        GPIO.output((self.MOTOR_PIN_1, self.MOTOR_PIN_2, self.MOTOR_PIN_3), (1, 0, 1))

    def calibrate(self):
        global spinner_calibration_diff

        def test_run():
            global spinner_calibration_diff
            start_time = time.time()
            for step in range(test_steps):
                GPIO.output(self.STEP_PIN, GPIO.HIGH)
                GPIO.output(self.STEP_PIN, GPIO.LOW)
            end_time = time.time()
            spinner_calibration_diff = end_time - start_time

        test_steps = 1000

        self.running = False

        test_thread = threading.Thread(target=test_run)
        test_thread.start()
        test_thread.join()

        while spinner_calibration_diff is None:
            time.sleep(0.1)

        print("DIFF FROM THREAD:", spinner_calibration_diff)
        delay_per_substep = spinner_calibration_diff/(test_steps*2)

        self.runtime_delay = delay_per_substep

        with open(calibration_json_path, "r") as json_file:
            config_json = json.load(json_file)
        config_json["spin_motor_delay"] = self.runtime_delay
        with open(calibration_json_path, "w") as json_file:
            json.dump(config_json, json_file)

        spinner_calibration_diff = None
        self.output_queue.put(("calibration_done", self.runtime_delay))

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
    def __init__(self, task_queue, output_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.output_queue = output_queue

        self.revolution = 0
        self.direction = 1

        self.theoretical_delay = 0  # theoretical pause between steps
        self.runtime_delay = 0  # delay occurring through runtime delay
        self.actual_delay = 0  # self.theoretical_delay - self.runtime_delay
        self.spr = 4000 * 2  # steps per revolution
        self.ml_per_revolution = 5
        self.task_target_steps = 0

        self.DIR_PIN = 24
        self.STEP_PIN = 23
        self.MOTOR_PIN_1 = 14
        self.MOTOR_PIN_2 = 15
        self.MOTOR_PIN_3 = 18

    def run(self):
        self.set_pins()
        threading.Thread(target=self.handler).start()

        while True:
            new_task, volume_in_ml, time_in_seconds = self.task_queue.get()
            if new_task == "pump_task":
                self.actual_delay = 1 / self.spr
                self.task_target_steps = int((volume_in_ml / self.ml_per_revolution) * (self.spr / 2))
                self.actual_delay = time_in_seconds/(self.task_target_steps * 2)

                print("TASK_TARGET_STEPS:", self.task_target_steps, "---", "ACTUAL_DELAY", self.actual_delay)

            elif new_task == "stop":
                self.task_target_steps = 0

    def set_pins(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.DIR_PIN, GPIO.OUT)
        GPIO.setup(self.STEP_PIN, GPIO.OUT)

        GPIO.setup((self.MOTOR_PIN_1, self.MOTOR_PIN_2, self.MOTOR_PIN_3), GPIO.OUT)
        GPIO.output((self.MOTOR_PIN_1, self.MOTOR_PIN_2, self.MOTOR_PIN_3), (1, 0, 1))

    def handler(self):
        while True:
            if self.task_target_steps != 0:
                self.task_target_steps -= 1

                GPIO.output(self.STEP_PIN, GPIO.HIGH)
                time.sleep(self.actual_delay)
                GPIO.output(self.STEP_PIN, GPIO.LOW)
                time.sleep(self.actual_delay)


class Heater(multiprocessing.Process):
    def __init__(self, task_queue, output_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.output_queue = output_queue

        self.sensor = W1ThermSensor()

        self.handling_task = False
        self.target_temperature = 0

    def run(self):
        threading.Thread(target=self.handler).start()

        while True:
            new_task, data = self.task_queue.get()
            print("NEW TASK:", new_task, data)
            if new_task == "set_temperature":
                self.target_temperature = data
                self.handling_task = True

            if new_task == "stop":
                self.handling_task = False

    def handler(self):
        while True:
            if self.handling_task:
                current_temp = self.sensor.get_temperature()
                print("Current temp:", current_temp)
                time.sleep(0.5)
                self.output_queue.put(("current_temp", current_temp))

