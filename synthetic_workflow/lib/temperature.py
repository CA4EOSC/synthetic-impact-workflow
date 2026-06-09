import os

import xarray as xr


K0 = -273.15
data_dir = "data"
datasets = {
  "baseline":    "tas_Amon_HadGEM3-GC31-MM_historical_r1i1p1f3_gn_18500116-19141216.nc",
  "observation": "tas_Amon_HadGEM3-GC31-MM_historical_r1i1p1f3_gn_19500116-20141216.nc"
}


def make_annual_deviations():
    ds0 = xr.open_dataset(os.path.join(data_dir, datasets["baseline"]))
    ds1 = xr.open_dataset(os.path.join(data_dir, datasets["observation"]))
    series0 = ds0["tas"].isel(lat=32, lon=9).values + K0
    series1 = ds1["tas"].isel(lat=32, lon=9).values + K0
    historic_mean = series0.mean()
    return [series1[m:m+12].mean() - historic_mean for m in range(0, len(series1), 12)]
