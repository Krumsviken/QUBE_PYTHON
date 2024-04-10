import sys
from time import time


kp = 0.04
ki = 0.02
kd = 0.0025

class PID:
    def __init__(self, P, I, D):
        self.kp = P
        self.ki = I
        self.kd = D
        self.windup = 5
        self.lastIntegral = 0
        self.lastError = 0
        self.useWindup = False
        self.last_time = 0
        self.prev_error = 0
        self.last_time = time()

    def regulate(self, setpoint, pos):
        # Implement controller using this function
        current_time = time()
        delta_time = current_time - self.last_time

        error = setpoint - pos
        self.lastIntegral += error * delta_time
        derivative = (error - self.prev_error) / delta_time
        self.prev_error = error
        
        if (self.lastIntegral > self.windup):
            self.lastIntegral = -self.windup
        if (self.lastIntegral < -self.windup):
            self.lastIntegral = self.windup

        self.last_time = current_time


        return self.kp*error + self.ki*self.lastIntegral + self.kd*derivative

    def copy(self, pid):
        self.kp = pid.kp
        self.ki = pid.ki
        self.kd = pid.kd
        self.windup = pid.windup
        self.useWindup = pid.useWindup
