import sys
import numpy as np
from time import time


class Observer:

    def __init__(self):
        self.x1_est = 0
        self.x2_est = 0
        self.k1 = 0
        self.k2 = 0
        self.last_time = time()

    def regulate(self, x1, value, x2):
        A = np.array([[0, 1], 
              [0, -7.6336]])
        B = np.array([[0],  
              [15267]])
        C = np.array([[1, 0]])
        D = np.array([[0]])
        l1 = 5.6393
        l2 = 0.0824
        self.last_time = time()

        current_time = time()
        delta_time = current_time - self.last_time
        self.last_time = current_time

        x1_est = self.x1_est + delta_time * (A[0, 0] * self.x1_est + A[0, 1] * self.x2_est + B[0, 0] * value - l1 * (C[0, 0] * self.x1_est - x1))
        x2_est = self.x2_est + delta_time * (A[1, 0] * self.x1_est + A[1, 1] * self.x2_est + B[1, 0] * value - l2 * (C[0, 0] * self.x1_est - x2))

        error = x1 - value

        u = -((self.k1 * error - self.k2 * x2)) 

        self.x1_est = x2_est
        self.x2_est = x2_est

        return u