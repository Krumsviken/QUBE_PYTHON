import sys
import numpy as np
from time import time


class Observer:

    def __init__(self):
        self.x1_est = 0
        self.x2_est = 0
        self.k1 = 0
        self.k2 = 0
        self.k3 = 0
        self.lastIntegral = 0

    def regulate(self, x1, value, x2):
        A = np.array([[0, 1], 
              [-4580, -80]])
        B = np.array([[0],  
              [15267]])
        C = np.array([[1, 0]])
        D = np.array([[0]])
        l1 = 600
        l2 = 60000
        #l3 = 1.5477e+6
        self.last_time = time()

        current_time = time()
        delta_time = current_time - self.last_time
        self.last_time = current_time
        

        dx1_est = self.x1_est + delta_time * (A[0, 0] * self.x1_est + A[0, 1] * self.x2_est + B[0, 0] * value - l1 * (C[0, 0] * self.x1_est - x1))
        dx2_est = self.x2_est + delta_time * (A[1, 0] * self.x1_est + A[1, 1] * self.x2_est + B[1, 0] * value - l2 * (C[0, 0] * self.x1_est - x2))

        x1_est = self.x1_est + delta_time *dx1_est
        x2_est = self.x2_est + delta_time *dx2_est

        error = x1 - value
        self.lastIntegral += error * delta_time

        u = -((self.k1 * error - self.k2 * x2 - self.k3 * self.lastIntegral)) 

        self.x1_est = x2_est
        self.x2_est = x2_est

        return u