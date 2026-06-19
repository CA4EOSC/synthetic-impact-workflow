import netCDF4 as nc
import numpy as np

from synthetic_workflow import config


def logistic_fit(t, K, r):
    """
      The Logistic equation with t=time,
      K=capacity and r=rate
      Note that this differs from the Logistic
      equation used for population generation
      in that it lacks an initial condition.
    """
    return K/(1 + np.exp(-r*t))


def residuals(params, t, y):
    return y - logistic_fit(t, *params)


def jacobian_fd(params, t, y, delta=1e-5):
    """
      A centred finite-difference approximation
      of the Jacobian.
    """
    J = np.zeros((len(t), len(params)))
    for j in range(len(params)):
        param_plus = params.copy()
        param_minus = params.copy()

        param_plus[j] += delta
        param_minus[j] -= delta

        r_plus = residuals(param_plus, t, y)
        r_minus = residuals(param_minus, t, y)

        J[:, j] = (r_plus - r_minus)/(2*delta)

    return J


def gauss_newton_fd(t, y, params, max_iter=200, tol=1e-6, delta=1e-5):
    """
      Gauss-Newton non-linear least squares solution
      of t=times vs. y=observation.
      Solves [J][pdiff] = [res] by left-multiplying
      by the transpose of the Jacobian.
    """
    for _ in range(max_iter):
        res = residuals(params, t, y)

        J = jacobian_fd(params, t, y, delta)

        # Left-multiply by Jacobian transpose
        JT = J.T
        H = JT @ J
        gradient = JT @ res

        pdiff = np.linalg.solve(H, gradient)
        params = params - pdiff

        if np.linalg.norm(pdiff) < tol:
            break

    return params


def write_capacity_fits(rx, ry, filename=config.capacity_fits_file):
    ds = nc.Dataset(filename, 'w', diskless=True, persist=True)
    dev_dim_name = "Temperature"
    dev_var_name = "Degrees Deviation"
    cap_dim_name = "Population"
    cap_var_name = "Normalised Capacity"

    ds.createDimension(dev_dim_name, None)
    ds.createVariable(dev_var_name, np.float64, dev_dim_name)
    ds.variables[dev_var_name][:] = rx

    ds.createDimension(cap_dim_name, None)
    ds.createVariable(cap_var_name, np.float64, cap_dim_name)
    ds.variables[cap_var_name][:] = ry

    ds.close()  # Persists dataset on close


def load_capacity_fits(filename=config.capacity_fits_file):
    ds = nc.Dataset(filename, 'r')
    rx = ds["Degrees Deviation"][:]
    ry = ds["Normalised Capacity"][:]

    ds.close()
    return rx, ry


