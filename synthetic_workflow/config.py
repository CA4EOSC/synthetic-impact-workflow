import os


data_dir = "data"

deviations_file = os.path.join(data_dir, "deviations.nc")
population_file = os.path.join(data_dir, "populations.nc")
capacity_fits_file = os.path.join(data_dir, "capacity_fits.nc")
linear_reg_coeffs_file = os.path.join(data_dir, "linear_reg_coeffs.txt")

cmip6_datasets = {
  "baseline":    "tas_Amon_HadGEM3-GC31-MM_historical_r1i1p1f3_gn_18500116-19141216.nc",
  "observation": "tas_Amon_HadGEM3-GC31-MM_historical_r1i1p1f3_gn_19500116-20141216.nc"
}
