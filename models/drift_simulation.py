import xarray as xr
import numpy as np
import os

def run_simulation():

    # Find project root
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_path = os.path.join(base_dir, "data", "hycom_data.nc")

    # Load ocean current dataset
    ds = xr.open_dataset(data_path)

    print(ds)   # ADD THIS

    u = ds["u"].isel(time=0, depth=0).values
    v = ds["v"].isel(time=0, depth=0).values

    latitudes = ds["latitude"].values
    longitudes = ds["longitude"].values

    # Number of plastic particles
    num_particles = 3000

    # Random starting positions
    particle_i = np.random.randint(0, u.shape[0], num_particles)
    particle_j = np.random.randint(0, u.shape[1], num_particles)

    dt = 0.1
    steps = 150

    # Drift simulation
    for step in range(steps):
        for p in range(num_particles):

            i = particle_i[p]
            j = particle_j[p]

            noise_lat = np.random.normal(0, 0.02)
            noise_lon = np.random.normal(0, 0.02)

            new_lat = latitudes[i] + v[i, j] * dt + noise_lat
            new_lon = longitudes[j] + u[i, j] * dt + noise_lon

            i = np.argmin(np.abs(latitudes - new_lat))
            j = np.argmin(np.abs(longitudes - new_lon))

            particle_i[p] = i
            particle_j[p] = j

    # Density map (plastic accumulation)
    density = np.zeros_like(u)

    for i, j in zip(particle_i, particle_j):
        density[i, j] += 1

    return density, latitudes, longitudes


# Run standalone test
if __name__ == "__main__":

    density, latitudes, longitudes = run_simulation()

    max_index = np.argmax(density)
    lat_idx, lon_idx = np.unravel_index(max_index, density.shape)

    print("Drift simulation complete.")
    print("Highest accumulation at:")
    print("Latitude:", latitudes[lat_idx])
    print("Longitude:", longitudes[lon_idx])