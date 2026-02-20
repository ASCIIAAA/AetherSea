import matplotlib.pyplot as plt
import random
import math


class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy




def simulate_drift(particle, wind_velocity, current_velocity, hours):

    x_positions = []
    y_positions = []

    for _ in range(hours):

        # Random wind fluctuation
        wind_x = wind_velocity[0] + random.uniform(-0.1, 0.1)
        wind_y = wind_velocity[1] + random.uniform(-0.1, 0.1)

        # Ocean rotation (eddy effect)
        rotation_strength = 0.15
        rotation_x = -rotation_strength * particle.y
        rotation_y = rotation_strength * particle.x

        # Total velocity
        total_x = wind_x + current_velocity[0] + rotation_x
        total_y = wind_y + current_velocity[1] + rotation_y

        particle.move(total_x, total_y)

        x_positions.append(particle.x)
        y_positions.append(particle.y)

    return x_positions, y_positions



def calculate_spread(x_positions, y_positions):
    """
    Calculate average distance of particles
    from their center of mass
    """

    final_x = [x[-1] for x in x_positions]
    final_y = [y[-1] for y in y_positions]

    center_x = sum(final_x) / len(final_x)
    center_y = sum(final_y) / len(final_y)

    distances = []
    for x, y in zip(final_x, final_y):
        distance = math.sqrt((x - center_x)**2 + (y - center_y)**2)
        distances.append(distance)

    average_spread = sum(distances) / len(distances)

    return average_spread

import numpy as np

def plot_density_heatmap(all_x, all_y):

    # Get final positions
    final_x = [x[-1] for x in all_x]
    final_y = [y[-1] for y in all_y]

    plt.figure()

    # Create 2D histogram (density grid)
    heatmap, xedges, yedges = np.histogram2d(final_x, final_y, bins=20)

    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

    plt.imshow(heatmap.T, extent=extent, origin='lower')
    plt.colorbar(label="Particle Density")

    plt.title("Plastic Density Heatmap")
    plt.xlabel("X Position (km)")
    plt.ylabel("Y Position (km)")
    plt.show()

from matplotlib.animation import FuncAnimation

from matplotlib.animation import FuncAnimation

def animate_particles(all_x, all_y, hours):

    fig, ax = plt.subplots()
    ax.set_title("AetherSea Drift Animation")
    ax.set_xlabel("X Position (km)")
    ax.set_ylabel("Y Position (km)")

    # Set proper limits based on simulation range
    all_final_x = [x[-1] for x in all_x]
    all_final_y = [y[-1] for y in all_y]

    ax.set_xlim(min(all_final_x) - 2, max(all_final_x) + 2)
    ax.set_ylim(min(all_final_y) - 2, max(all_final_y) + 2)

    scat = ax.scatter([], [])

    def update(frame):
        x_frame = [x[frame] for x in all_x]
        y_frame = [y[frame] for y in all_y]

        scat.set_offsets(list(zip(x_frame, y_frame)))
        return scat,

    ani = FuncAnimation(fig, update, frames=hours, interval=300, repeat=False)
    plt.show()

def predict_patch_movement(all_x, all_y):

    # Compute center at each time step
    hours = len(all_x[0])
    center_x = []
    center_y = []

    for t in range(hours):
        x_t = [x[t] for x in all_x]
        y_t = [y[t] for y in all_y]

        center_x.append(sum(x_t) / len(x_t))
        center_y.append(sum(y_t) / len(y_t))

    # Estimate velocity from last two steps
    vx = center_x[-1] - center_x[-2]
    vy = center_y[-1] - center_y[-2]

    # Predict next 10 future steps
    future_x = []
    future_y = []

    last_x = center_x[-1]
    last_y = center_y[-1]

    for _ in range(10):
        last_x += vx
        last_y += vy
        future_x.append(last_x)
        future_y.append(last_y)

    return center_x, center_y, future_x, future_y

def plot_prediction(center_x, center_y, future_x, future_y):

    plt.figure()
    plt.plot(center_x, center_y, label="Actual Patch Movement")
    plt.plot(future_x, future_y, '--', label="Predicted Movement")

    plt.scatter(center_x[-1], center_y[-1], marker='o', s=100, label="Current Position")

    plt.title("Garbage Patch Movement Prediction")
    plt.xlabel("X Position (km)")
    plt.ylabel("Y Position (km)")
    plt.legend()
    plt.grid(True)
    plt.show()

def plan_cleanup_route(future_x, future_y, port_location=(0, 0)):

    # Choose predicted position 5 steps ahead
    target_x = future_x[4]
    target_y = future_y[4]

    port_x, port_y = port_location

    return port_x, port_y, target_x, target_y

def plot_cleanup_route(port_x, port_y, target_x, target_y):

    plt.figure()

    plt.scatter(port_x, port_y, s=150, marker='s', label="Cleanup Vessel Start")
    plt.scatter(target_x, target_y, s=150, marker='o', label="Interception Point")

    plt.plot([port_x, target_x], [port_y, target_y], '--', label="Optimal Route")

    plt.title("Cleanup Vessel Route Planning")
    plt.xlabel("X Position (km)")
    plt.ylabel("Y Position (km)")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":

    import random

    wind = (0.5, 0.2)
    current = (0.3, 0.4)
    hours = 24

    num_particles = 30
    all_x = []
    all_y = []

    for _ in range(num_particles):
        # Start particles near (0,0) with small random spread
        start_x = random.uniform(-1, 1)
        start_y = random.uniform(-1, 1)

        particle = Particle(start_x, start_y)

        x_pos, y_pos = simulate_drift(particle, wind, current, hours)

        all_x.append(x_pos)
        all_y.append(y_pos)

    # Plot all particles
    plt.figure()

    for i in range(num_particles):
        plt.plot(all_x[i], all_y[i])

    plt.title("AetherSea Drift Simulation - Plastic Patch")
    plt.xlabel("X Position (km)")
    plt.ylabel("Y Position (km)")
    plt.grid(True)
    plt.show()

    spread = calculate_spread(all_x, all_y)
    print(f"Average particle spread: {spread:.2f} km")

    if spread < 3:
        print("⚠️ Accumulation zone forming (Garbage Patch Detected)")
    else:
        print("Particles are dispersing")

    # Always show heatmap and animation
    plot_density_heatmap(all_x, all_y)
    animate_particles(all_x, all_y, hours)
    center_x, center_y, future_x, future_y = predict_patch_movement(all_x, all_y)
    plot_prediction(center_x, center_y, future_x, future_y)
    port_x, port_y, target_x, target_y = plan_cleanup_route(future_x, future_y)
    plot_cleanup_route(port_x, port_y, target_x, target_y)

 