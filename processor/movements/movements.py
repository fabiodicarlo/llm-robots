from actuator import Actuator


def calculate_wheel_speed(sensors, angle, direction=False):
    normalized_angle = angle / Actuator.max_angle

    max_speed = Actuator.max_speed
    if direction:
        max_speed = 1

    wheel_speed_left = max_speed * (1 - normalized_angle)
    wheel_speed_right = max_speed * (1 + normalized_angle)

    result, distance, _, _, _ = sensors.get_ultrasonic_sensor()
    if distance > 0.0:
        if distance < Actuator.target_distance:
            speed_factor = 0.0
        else:
            speed_factor = 1 - (
                        (Actuator.max_distance - distance) / (Actuator.max_distance - Actuator.target_distance))
            speed_factor = max(speed_factor, 0.0)
    else:
        speed_factor = 1.0

    wheel_speed_left *= speed_factor
    wheel_speed_right *= speed_factor
    return wheel_speed_left, wheel_speed_right
