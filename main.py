# ------------------------------------- AVAILABLE FUNCTIONS --------------------------------#
# qube.setRGB(r, g, b) - Sets the LED color of the QUBE. Color values range from [0, 999].
# qube.setMotorSpeed(speed) - Sets the motor speed. Speed ranges from [-999, 999].
# qube.setMotorVoltage(volts) - Applies the given voltage to the motor. Volts range from (-24, 24).
# qube.resetMotorEncoder() - Resets the motor encoder in the current position.
# qube.resetPendulumEncoder() - Resets the pendulum encoder in the current position.

# qube.getMotorPosition() - Returns the cumulative angular positon of the motor.
# qube.getPendulumPosition() - Returns the cumulative angular position of the pendulum.
# qube.getMotorRPM() - Returns the newest rpm reading of the motor.
# qube.getMotorCurrent() - Returns the newest reading of the motor's current.
# ------------------------------------- AVAILABLE FUNCTIONS --------------------------------#

# main.py

from QUBE import *
from logger import *
from com import *
from liveplot import *
from time import time
import threading
import numpy as np
from Observer import Observer  # Importing the variables from observer.py
from PID import *

# Replace with the Arduino port. Can be found in the Arduino IDE (Tools -> Port:)
port = "COM8"
baudrate = 115200
qube = QUBE(port, baudrate)

# Resets the encoders in their current position.
qube.resetMotorEncoder()
qube.resetPendulumEncoder()

# Enables logging - comment out to remove
enableLogging()

t_last = time()

# Define the goal angle and voltage threshold
m_target = 250
p_target = 0
k1 = 120.02
k2 = 2.396
observer = Observer()

pid = PID(kp, ki, kd)

def control(data, lock):
    global m_target, p_target, observer, pid  # Ensure we're using the global observer object
    angle_ref = 250

    while True:
        # Updates the qube - Sends and receives data
        qube.update()

        # Gets the logdata and writes it to the log file
        logdata = qube.getLogData(m_target, p_target)
        save_data(logdata)

        # Multithreading stuff that must happen. Don't mind it.
        with lock:
            doMTStuff(data)

        # Get deltatime
        dt = getDT()

        # PID
        #angle = qube.getMotorAngle()
        #u = pid.regulate(1000, angle)

        # Observator

        x1 = qube.getMotorAngle()
        x2 = qube.getMotorRPM()
        est_angle = observer.x1_est
        est_rpm = observer.x2_est
        error = angle_ref - x1

        u = -k1 * error - k2 * x2
        #u = observer.regulate(500, x1)
        u = max(min(u, 24), -24)

        speed = observer.regulate(x1, u, x2)

        qube.setMotorVoltage(u)
        print("Reference Angle:", angle_ref)
        print("Measured Speed:", x2)
        print("Control Input:", u)
        print("Estimated Speed:", speed)
        print("Estimated Angle:", est_angle)



def getDT():
    global t_last
    t_now = time()
    dt = t_now - t_last
    t_last += dt
    return dt


def doMTStuff(data):
    packet = data[7]
    #observer = observer(other)
    if packet.resetEncoders:
        qube.resetMotorEncoder()
        qube.resetPendulumEncoder()
        packet.resetEncoders = False

    new_data = qube.getPlotData(m_target, p_target)
    for i, item in enumerate(new_data):
        data[i].append(item)


if __name__ == "__main__":
    _data = [[], [], [], [], [], [], [], Packet()]
    lock = threading.Lock()
    thread1 = threading.Thread(target=startPlot, args=(_data, lock))
    thread2 = threading.Thread(target=control, args=(_data, lock))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
