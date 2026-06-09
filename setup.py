from setuptools import (
    find_packages,
    setup
)


dev_requires = [
    "flake8",
    "pdbpp"
]


setup(
    name = "synthetic-ca4eosc-workflow",
    version = "0.1.0",
    packages = find_packages(),
    install_requires = [
        "cdsapi",        # Copernicus Climate Data Store api
        "matplotlib",
        "numpy",
        "xarray"         # CMIP6 subset NetCDF4 files
    ],
    extras_require = {
        "dev": dev_requires
    },
    entry_points = {
        "console_scripts": ["synthetic-ca4eosc-workflow=synthetic_workflow.main:main"]
    }
)
