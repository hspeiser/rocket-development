import numpy as np
import matplotlib.pyplot as plt

# Constants
g = 9.81  # Acceleration due to gravity
A = 4.67e-4  # Cross-sectional area
"""
launch_mass_before_burn = 0.0518 # kg
launch_mass_after_burn = launch_mass_before_burn - 0.006  # kg
launch_mass_during_burn = (launch_mass_before_burn + launch_mass_after_burn) / 2 # kg
average_burning_time = 0.952     # seconds
average_thrust = 4.45            # Newton
Cd = 0.749                  # Drag coefficient


"""
#Henry Numbers
launch_mass_before_burn = 0.273 + 0.06  # kg
launch_mass_after_burn = launch_mass_before_burn - 0.076  # kg
launch_mass_during_burn = (launch_mass_before_burn +
                           launch_mass_after_burn) / 2  # kg
average_burning_time = 1.68  # seconds
average_thrust = 89.88  # Newton
Cd = 0.7  # Drag coefficient\

# Lists to store results
t_values = []
h_values = []
v_values = []
a_values = []

# Time step
dt = 0.05

# Initial conditions
t = 0.0
h = 0.0
v = 0.0
a = 0.0

t_values.append(t)
h_values.append(h)
v_values.append(v)
a_values.append(a)

# Perform calculations
while t <= 6.0:  # up to 6 seconds
    if t <= average_burning_time:  # During the burn
        current_mass = np.interp(
            t, [0, average_burning_time],
            [launch_mass_before_burn, launch_mass_after_burn])
        Ft = average_thrust
    else:  # After the burn
        current_mass = launch_mass_after_burn
        Ft = 0

    # Calculate the forces
    Fd = Cd * A * v**2
    Fg = current_mass * g
    F_total = Ft - Fd - Fg

    # Acceleration, velocity, height
    a = F_total / current_mass
    v = v + a * dt
    h = h + v * dt

    # Store results
    t_values.append(t)
    h_values.append(h)
    v_values.append(v)
    a_values.append(a)

    # Increase time
    t += dt
# Find the maximum height
#max_height_index = v_values.index(next(
#    x for x in v_values
#    if x < 0))  # find the index where velocity changes sign

# If the rocket is still ascending when the ejection charge fires
#if t_values[max_height_index] < average_burning_time + 4:
#    max_height = h_values[max_height_index] + 2
#else:  # if the rocket is coming down when the ejection charge fires
#    max_height = max(h_values)

# Find the maximum velocity and acceleration
#max_velocity = max(v_values)
#max_acceleration = max(a_values)

#print(f"Maximum height is {max_height:.2f} m")
#print(f"Maximum velocity is {max_velocity:.2f} m/s")
#print(f"Maximum acceleration is {max_acceleration:.2f} m/s^2")

# Plotting
plt.figure(figsize=(10, 8))

plt.subplot(3, 1, 1)
plt.plot(t_values, h_values, label='Height (m)')
plt.title('Height over time')
plt.xlabel('Time (s)')
plt.ylabel('Height (m)')
plt.grid(True)

plt.subplot(3, 1, 2)
plt.plot(t_values, v_values, label='Velocity (m/s)')
plt.title('Velocity over time')
plt.xlabel('Time (s)')
plt.ylabel('Velocity (m/s)')
plt.grid(True)

plt.subplot(3, 1, 3)
plt.plot(t_values, a_values, label='Acceleration (m/s^2)')
plt.title('Acceleration over time')
plt.xlabel('Time (s)')
plt.ylabel('Acceleration (m/s^2)')
plt.grid(True)

plt.tight_layout()

plt.show()

