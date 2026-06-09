from .lib.temperature import make_annual_deviations
from .lib.solver import gauss_newton_fd
from .lib.population import generate_population_series

import matplotlib.pyplot as plt
import numpy as np


np.random.seed(0x20)


def main():
    params = np.array([1.0, 0.5])

    annual_deviations = make_annual_deviations()
    pop = generate_population_series(annual_deviations)

    #plt.plot(np.ravel(pop))
    #plt.show()

    rx = []
    ry = []

    for idx, dev in enumerate(annual_deviations):
        y = pop[idx][0:8]
        x = np.array([*range(8)])
        fit = gauss_newton_fd(x, y, params)
        rx.append(dev)
        ry.append(fit[0])

    b, m = np.polynomial.polynomial.polyfit(rx, ry, 1)

    plt.scatter(rx, ry)
    plt.axline((0, b), (1, b+m), color="red")
    plt.xlabel("Temperature Deviation °C")
    plt.ylabel("Annual Inferred Capacity")
    plt.show()


if __name__ == "__main__":
    main()
