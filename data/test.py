import xarray as xr

ds = xr.open_dataset("hycom_data.nc")

print(ds)