class Actuator:
    # Angolo massimo di sterzata delle ruote
    max_angle = 45.0
    max_speed = 2.0
    max_distance = 3
    target_distance = 0.2

    def __init__(self, sim):
        self.sim = sim

        # Ruote robot
        self.r_wheel = sim.getObject('/dr20/rightWheelJoint_')
        self.l_wheel = sim.getObject('/dr20/leftWheelJoint_')

    def move(self, wheel_speed):
        wheel_speed_left, wheel_speed_right = wheel_speed
        self.sim.setJointTargetVelocity(self.l_wheel, wheel_speed_left)
        self.sim.setJointTargetVelocity(self.r_wheel, wheel_speed_right)

    def stop(self):
        self.sim.setJointTargetVelocity(self.l_wheel, 0)
        self.sim.setJointTargetVelocity(self.r_wheel, 0)

    def back(self):
        self.sim.setJointTargetVelocity(self.l_wheel, -1)
        self.sim.setJointTargetVelocity(self.r_wheel, -1)
