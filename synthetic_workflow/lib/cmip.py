import os
import sys
import zipfile

import cdsapi


area = [66, -10, 35, 40]  # Boundary lats/longs of European region
base_start = 1850
base_end = 1914
sample_start = 1950
sample_end = 2104

data_dir = "data"

baseline = {
   "filename": "cmip6_baseline.zip",
   "ncfile": "tas_Amon_HadGEM3-GC31-MM_historical_r1i1p1f3_gn_18500116-19141216.nc",
   "dataset": "projections-cmip6",
   "request": {
        "temporal_resolution": "monthly",
        "experiment": "historical",
        "variable": "near_surface_air_temperature",
        "model": "hadgem3_gc31_mm",
        "year": [f"{y}" for y in range(base_start, base_end+1)],
        "month": [f"{m:02}" for m in range(1, 13)],
        "area": area
    }
}

sample = {
    "filename": "cmip6_sample.zip",
    "ncfile": "tas_Amon_HadGEM3-GC31-MM_historical_r1i1p1f3_gn_19500116-20141216.nc",
    "dataset": "projections-cmip6",
    "request": {
        "temporal_resolution": "monthly",
        "experiment": "historical",
        "variable": "near_surface_air_temperature",
        "model": "hadgem3_gc31_mm",
        "year": [f"{y}" for y in range(sample_start, sample_end+1)],
        "month": [f"{m:02}" for m in range(1, 13)],
        "area": area
    }
}


def retrieve_datasets():
    if has_local_datasets():
        print("Datasets present")
        sys.exit(0)

    client = cdsapi.Client()

    for subset in (baseline, sample):
        client.retrieve(subset["dataset"], subset["request"]).download(os.path.join(data_dir, subset["filename"]))
        unzip_dataset(os.path.join(data_dir, subset["filename"]))


def has_local_datasets():
    for subset in (baseline, sample):
        if not (os.path.exists(subset["filename"]) or os.path.exists(subset["ncfile"])):
            return False
    return True


def unzip_dataset(zfname, path=data_dir):
    # NB This will overwrite provenance.json and provenance.png
    with zipfile.ZipFile(zfname, 'r') as zf:
        zf.extractall(path=path)


if __name__ == "__main__":
    retrieve_datasets()
