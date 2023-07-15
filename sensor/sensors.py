class Sensors:
    def __init__(self, sim):
        self.sim = sim

        # Sensori robot
        self.infrared_sensor_RT = sim.getObject('/dr20/infraredSensor1_')
        self.infrared_sensor_RB = sim.getObject('/dr20/infraredSensor2_')
        self.infrared_sensor_LB = sim.getObject('/dr20/infraredSensor5_')
        self.infrared_sensor_LT = sim.getObject('/dr20/infraredSensor6_')
        self.ultrasonic_sensor = sim.getObject('/dr20/ultrasonicSensorJoint_/ultrasonicSensor_')

        # Telecamera sulla testa del robot
        self.vision_sensor_handle = sim.getObject('/dr20/sensor[1]')

    def get_ultrasonic_sensor(self):
        return self.sim.readProximitySensor(self.ultrasonic_sensor)
