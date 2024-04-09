import numpy as np
import matplotlib.pyplot as plt
import control as ctrl

# Continuous system matrices
A = np.array([[0, 1, 0], 
              [0, 0, 1], 
              [-15391, -1511, -98]])
B = np.array([[0], 
              [0], 
              [29024]])
C = np.array([[0, 1, 0]])
D = np.array([[0]])

# Sampling time
dt = 0.1

# Discretize system matrices using Forward Euler
Ad = np.eye(3) + dt * A
Bd = dt * B

# Controller gain (K) and observer gain (L)
K = np.array([[63.131, 1.2603, 0.016258]]) 
L = np.array([[-998.48], [4320], [1547700]]) 

# Initial conditions
x_est = np.zeros((3, 1))  # Initial state estimate
x_real = np.array([[0], [1], [0]])  # Initial real state
u = 0  # Initial control input

# Simulation parameters
max_iterations = 150
tolerance = 1e-4
iteration = 0

# Lists to store simulation data
x_est_history = []
x_real_history = []
u_history = []

# Simulation loop with a while condition
while iteration < max_iterations:
    iteration += 1
    
    # System simulation
    x_real = Ad.dot(x_real) + Bd * u
    
    # Output measurement
    y = C.dot(x_real) + D * u
    
    # State estimation using observer
    x_est = Ad.dot(x_est) + Bd * u + L.dot(y - C.dot(x_est))
    
    # Control law (state feedback)
    u = -K.dot(x_est)
    
    # Store data for plotting
    x_est_history.append(x_est.flatten())
    x_real_history.append(x_real.flatten())
    u_history.append(u.flatten())
    
    # Convergence check
    if np.linalg.norm(x_real - x_est) < tolerance:
        print("Convergence reached at iteration:", iteration)
        break


    if iteration % 2 == 0:
        print(f"Iteration: {iteration}, Estimated state: {x_est.flatten()}, Control input: {u}")

# Convert lists to numpy arrays for easier plotting
x_est_history = np.array(x_est_history)
x_real_history = np.array(x_real_history)
u_history = np.array(u_history)

# Plotting
fig, axs = plt.subplots(3, 1, figsize=(10, 8))

# Plot estimated states
for i in range(x_est_history.shape[1]):
    axs[0].plot(x_real_history[:, i], label=f'x_real_{i+1}', linestyle='--')
    axs[1].plot(x_est_history[:, i], label=f'x_est_{i+1}')
axs[0].set_title('Real State Variables over Iterations')
axs[1].set_title('Estimated State Variables over Iterations')
axs[0].set_ylabel('Real State')
axs[1].set_ylabel('Estimated State')
axs[0].legend()
axs[1].legend()
axs[0].grid()
axs[1].grid()

# Plot control input
axs[2].plot(u_history, label='Control Input u', color='red')
axs[2].set_title('Control Input over Iterations')
axs[2].set_xlabel('Iteration')
axs[2].set_ylabel('Control Input')
axs[2].legend()
axs[2].grid()

plt.tight_layout()
plt.show()