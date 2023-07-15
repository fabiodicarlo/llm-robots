import cv2
import numpy as np
from .movements import calculate_wheel_speed

class ObjectDetector:

    def __init__(self, sim, actuator, sensors):
        self.sim = sim
        self.actuator = actuator
        self.sensors = sensors

    def inside(self, r, q):
        rx, ry, rw, rh = r
        qx, qy, qw, qh = q
        return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh

    def draw_detections(self, img, rects, thickness=1):
        for x, y, w, h in rects:
            pad_w, pad_h = int(0.15 * w), int(0.05 * h)
            cv2.rectangle(img, (x + pad_w, y + pad_h), (x + w - pad_w, y + h - pad_h), (0, 255, 0), thickness)
            return self.angle_obj((x, y, w, h), img)

    def angle_obj(self, rect, frame):
        center_x = rect[0] + rect[2] // 2
        center_y = rect[1] + rect[3] // 2

        image_center_x = frame.shape[1] // 2
        image_center_y = frame.shape[0] // 2
        return np.arctan2(center_x - image_center_x, image_center_y - center_y) * 180 / np.pi

    def start_detector(self, vision_sensor_handle):
        vision_sensor, resX, resY = self.sim.getVisionSensorCharImage(vision_sensor_handle)
        vision_sensor = np.frombuffer(vision_sensor, dtype=np.uint8).reshape(resY, resX, 3)
        vision_sensor = cv2.flip(cv2.cvtColor(vision_sensor, cv2.COLOR_BGR2RGB), 0)

        hog = cv2.HOGDescriptor()
        hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

        rects, weights = hog.detectMultiScale(vision_sensor, winStride=(8, 8), padding=(32, 32), scale=1.05)

        found_filtered = []
        for ri, r in enumerate(rects):
            for qi, q in enumerate(rects):
                if ri != qi and self.inside(r, q):
                    break
                else:
                    found_filtered.append(r)
                    angle1 = self.draw_detections(vision_sensor, rects)
                    angle2 = self.draw_detections(vision_sensor, found_filtered, 3)
                    self.actuator.move(calculate_wheel_speed(self.sensors, -max(angle1, angle2), True))

        if vision_sensor is not None:
            cv2.imshow('object_detector', vision_sensor)
            cv2.waitKey(1)
