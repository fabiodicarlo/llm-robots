from .movements import calculate_wheel_speed
from actuator import Actuator
from sensor import Sensors
from .movements import object_detector
from .llm.api import LlmApi
import threading
import cv2
from time import sleep


class Processor:
    def __init__(self, sim):
        self.sim = sim
        self.sensors = Sensors(self.sim)
        self.actuator = Actuator(self.sim)
        self.llm = LlmApi()
        self.object_detector = object_detector.ObjectDetector(self.sim, self.actuator, self.sensors)
        self.actuator.stop()
        self.last_command = None

    def execute_cmd(self, command):

        if command == 'follow':
            self.object_detector.start_detector(self.sensors.vision_sensor_handle)
            return 'follow'
        elif command == 'go on':
            cv2.destroyAllWindows()
            self.actuator.move(calculate_wheel_speed(self.sensors, 0))
            return None
        elif command == 'left':
            cv2.destroyAllWindows()
            self.actuator.move(calculate_wheel_speed(self.sensors, 45, True))
            return None
        elif command == 'right':
            cv2.destroyAllWindows()
            self.actuator.move(calculate_wheel_speed(self.sensors, -45, True))
            return None
        elif command == 'stop':
            cv2.destroyAllWindows()
            self.actuator.stop()
            return None
        elif command == 'back':
            cv2.destroyAllWindows()
            self.actuator.back()
            return None
        return None

    def background_task_command(self, command):
        self.llm.set_data(command)
        while not self.llm.check_status():
            sleep(2)
        answer = self.llm.get_processed_data()
        self.execute_cmd(command)

        print(answer)

    def brain(self, command=None):
        if command is not None:
            thread = threading.Thread(target=self.background_task_command, args=(command,))
            thread.start()
            self.last_command = command

        if self.last_command is not None:
            self.execute_cmd(self.last_command)

        return None
