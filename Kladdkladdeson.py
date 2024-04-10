import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Define your system matrices and vectors (A_cl87, B87, K87, CY2, l87) here. 
# Example: A_cl87 = np.array([[...], [...], [...]])
A_cl87 = np.array([[0, 1], 
              [0, -7.6336]])
B87 = np.array([[0],  
              [15267]])
CY2 = np.array([[0, 1]])
D_cl87 = np.array([[0]])

K = np.array([[120.02, 2.396]])
L = np.array([[1547700], [4320]]) 
# Observer dynamics
A_obs = A_cl87 - l87.dot(CY2)
B_obs = np.hstack([B87, l87])  # Incorporate both control input and measurement input
C_obs = np.eye(A_cl87.shape[0])  # Observer outputs all estimated states
D_obs = 0

# Full-state feedback control using observer
r = 45  # constant command signal

# Define initial conditions
# Define initial conditions
x0_system = np.array([[0], [0], [0]])  # Initial condition of the system
x0_observer = np.array([[0], [0], [0]])  # Initial condition of the observer


# Simulation setup
t_span = (0, 5)
t_eval = np.arange(0, 5, 0.01)  # Simulation time

def dynamics(t, x, A_cl87, B87, K87, A_obs, B_obs, CY2):
    # Example state extraction (this part will vary based on your specific problem)
    x_system = x[:3]  # Assuming first 3 states are system states
    x_observer = x[3:]  # Next states are observer states

    # Observer-based control law
    control_input = -K87 @ x_observer  # Using estimated states from observer
    
    # Simplified dynamics calculations (replace with your actual dynamics)
    dxdt_system = A_cl87 @ x_system + B87 * control_input
    dxdt_observer = A_obs @ x_observer + B_obs @ np.array([control_input, -CY2 @ x_observer])
    
    return np.concatenate([dxdt_system, dxdt_observer])

# Solve the differential equation
sol = solve_ivp(lambda t, x: dynamics(t, x, A_cl87, B87, K87, A_obs, B_obs, CY2), t_span, np.concatenate([x0_system.flatten(), x0_observer.flatten()]), t_eval=t_eval)



# Extract actual and estimated states
x_actual = sol.y[:3, :].T  # First three states are the actual system states
x_estimated = sol.y[3:, :].T  # Next states are the estimated states

# Plot results for actual states
plt.figure()
plt.plot(sol.t, x_actual[:, 0], 'b', label='Actual State 1: Integrated Angle Error')
plt.plot(sol.t, x_actual[:, 1], 'g', label='Actual State 2: Angle Error')
plt.plot(sol.t, x_actual[:, 2], 'r', label='Actual State 3: Angular Velocity')
plt.legend()
plt.title('Actual States over Time')
plt.xlabel('Time (s)')
plt.ylabel('Actual States')

# Plot results for estimated states
plt.figure()
plt.plot(sol.t, x_estimated[:, 0], '--b', label='Estimated State 1: Integrated Angle Error')
plt.plot(sol.t, x_estimated[:, 1], '--g', label='Estimated State 2: Angle Error')
plt.plot(sol.t, x_estimated[:, 2], '--r', label='Estimated State 3: Angular Velocity')
plt.legend()
plt.title('Estimated States over Time')
plt.xlabel('Time (s)')
plt.ylabel('Estimated States')

plt.show()