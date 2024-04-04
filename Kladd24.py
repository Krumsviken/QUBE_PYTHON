import numpy as np
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

# Sampling time (choose based on the dynamics of your system)
dt = 0.0001

# Discretize system matrices using Forward Euler
Ad = np.eye(3) + dt * A
Bd = dt * B

# Controller gain (K) and observer gain (L) need to be designed based on the system dynamics and requirements
# For demonstration, we initialize them with arbitrary values; tune these for your specific system
K = np.array([[0.5303, 0.0521, 0.0031]]) 
L = np.array([[-998], [878], [63937]]) 

# Initial conditions
x_est = np.zeros((3, 1))  # Initial state estimate
x_real = np.array([[0], [1], [0]])  # Initial real state, assuming starting in a non-zero state for demonstration
u = 0  # Initial control input

# Simulation parameters
max_iterations = 150
tolerance = 1e-4
iteration = 0

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
    
    # Convergence check (optional, based on your system's requirements)
    if np.linalg.norm(x_real - x_est) < tolerance:
        print("Convergence reached at iteration:", iteration)
        break

    # For demonstration, print every 100 steps
    if iteration % 2 == 0:
        print(f"Iteration: {iteration}, Estimated state: {x_est.flatten()}, Control input: {u}")

# Note: K and L should be carefully designed based on system requirements
