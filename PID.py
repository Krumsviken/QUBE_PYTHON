import sys
import numpy as np

class PID:
    def __init__(self, Ts, kp, ki, kd, umax, umin, tau):
        self.Ts = Ts     # Sample period
        self.kp = kp     # Proportional gain
        self.ki = ki     # Integral gain
        self.kd = kd     # Derivative gain
        self.umax = umax # Upper output saturation limit
        self.umin = umin # Lower output saturation limit
        self.tau = tau      # Derivative tilter time constant
        self.windup = 0
        self.lastIntegral = 0
        self.lastError = 0
        self.useWindup = False

        self.preverror = [0, 0] # Previous error e[n-1], e[n-2]
        self.prevc = 0          # Previous controller output u[n-1]
        self.prev_dfilter = 0   # Previous derivative term filtered value

    def regulate(self):
        # Implement controller using this function
        return 0
    
    def copy(self, pid):
        self.kp = pid.kp
        self.ki = pid.ki
        self.kd = pid.kd
        self.windup = pid.windup
        self.useWindup = pid.useWindup
