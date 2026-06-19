import os

import xarray as xr
import netCDF4 as nc
import numpy as np

from synthetic_workflow import config


K0 = -273.15  # Absolute zero, for K to C conversion


def make_annual_deviations():
    ds0 = xr.open_dataset(os.path.join(config.data_dir, config.cmip6_datasets["baseline"]))
    ds1 = xr.open_dataset(os.path.join(config.data_dir, config.cmip6_datasets["observation"]))
    series0 = ds0["tas"].isel(lat=32, lon=9).values + K0
    series1 = ds1["tas"].isel(lat=32, lon=9).values + K0
    historic_mean = series0.mean()
    return [series1[m:m+12].mean() - historic_mean for m in range(0, len(series1), 12)]


def write_deviations_as_netcdf(devs, filename=config.deviations_file):
    ds = nc.Dataset(filename, 'w', diskless=True, persist=True)
    dim_name = "Temperature"
    var_name = "Degrees Deviation"
    ds.createDimension(dim_name, None)
    ds.createVariable(var_name, np.float64, dim_name)
    ds.variables[var_name][:] = devs

    ds.close()  # Persists dataset on close


def load_deviations(filename=config.deviations_file):
    ds = nc.Dataset(filename, 'r')
    return ds["Degrees Deviation"][:]


if __name__ == "__main__":
    devs = make_annual_deviations()
    write_deviations_as_netcdf(devs)
