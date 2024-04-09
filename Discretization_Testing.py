import numpy as np
import matplotlib.pyplot as plt

# Model parameters
K = 3
T = 4

a = -1/T
b = K/T

# Simulation Parameters
Ts = 0.1
Tstop = 30
uk = 1
yk = 0
N = int(Tstop/Ts)

data = []
data.append(yk)

# Simulation
for k in range (N):
    yk1 = (1 + a*Ts) * yk + Ts * b * uk
    yk = yk1
    data.append(yk1)

# Plot the Simulation results
t = np.arange(0, Tstop+Ts, Ts)

plt.plot(t, data)
plt.title ('1.order Dynamic System')
plt.xlabel('t [s]')
plt.ylabel('y(t)')
plt.grid()
plt.show()
