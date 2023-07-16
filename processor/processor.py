from .movements import calculate_wheel_speed
from actuator import Actuator
from sensor import Sensors
from .movements import object_detector
import threading
import cv2


class Processor:
    def __init__(self, sim):
        self.sim = sim
        self.sensors = Sensors(self.sim)
        self.actuator = Actuator(self.sim)
        self.object_detector = object_detector.ObjectDetector(self.sim, self.actuator, self.sensors)
        self.actuator.stop()

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

    def brain(self, command=None):
        if command is not None:
            return self.execute_cmd(command)

        return None
