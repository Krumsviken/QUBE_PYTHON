import sys
import numpy as np


class Observer:
        # Continuous system matrices
    A = np.array([[0, 1, 0], 
                [0, 0, 1], 
                [-15391, -1511, -98]])
    B = np.array([[0], 
                [0], 
                [29024]])
    C = np.array([[0, 1, 0]])
    D = np.array([[0]])

    # Sampling Time
    Ts = 0.1

    Ad = np.eye(3) + Ts * A
    Bd = Ts * B
    K = np.array([[63.131, 1.2603, 0.016258]]) 
    L = np.array([[1547700], [4320], [-998.48]]) 
    # Initial condition
    u = 8.7

    def __init__(self):
        self.x_est = np.zeros((self.Ad.shape[0], 1))  # Initial state estimate


    def regulate(self, y, u):
        # State estimation update
        y_est = self.C.dot(self.x_est)
        self.x_est = self.Ad.dot(self.x_est) + self.Bd.dot(u) + self.L.dot(y - y_est)

        # Compute control input using state feedback
        u_new = -self.K.dot(self.x_est)

        return u_new.flatten(), self.x_est  # Ensure u_new is a 1D array for compatibility
    
    def reset (self):
        self.x_est = np.zeros_like(self.x_est)

    def copy(self, other):
        self.x_est = np.copy(other.x_est)
