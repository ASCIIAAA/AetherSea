import xarray as xr
import numpy as np

class MonitoringAgent:

    def observe(self):

        # Load HYCOM dataset
        ds = xr.open_dataset("data/hycom_data.nc")

        # Extract useful variables
        temperature = ds['water_temp'].values
        salinity = ds['salinity'].values
        currents_u = ds['water_u'].values
        currents_v = ds['water_v'].values

        # Example synthetic plastic concentration
        plastic_concentration = np.random.rand(*temperature.shape) * 0.5

        data = {
            "temperature": temperature,
            "salinity": salinity,
            "currents_u": currents_u,
            "currents_v": currents_v,
            "plastic": plastic_concentration
        }

        return data