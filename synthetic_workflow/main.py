import argparse
import sys

from .lib.temperature import (
    make_annual_deviations,
    write_deviations_as_netcdf
)

from .lib.solver import gauss_newton_fd
from .lib.population import (
    load_deviations,
    generate_population_series,
    write_populations_as_netcdf
)
from .lib.cmip import retrieve_datasets

import matplotlib.pyplot as plt
import numpy as np


np.random.seed(0x20)


def parse_args(argv):
    parser = argparse.ArgumentParser(
        prog="synthetic-ca4eosc-workflow",
        description="A demonstration synthetic climate impact workflow",
        epilog="https://github.com/CA4EOSC/synthetic-impact-workflow"
    )

    parser.add_argument("--retrieve-data",
        action="store_true",
        default=False,
        help="Perform Stage 1 of the Workflow: Data Retrieval"
    )

    parser.add_argument("--make-deviations",
        action="store_true",
        default=False,
        help="Perform Stage 2 of the Workflow: Calculate Temperature Deviations"
    )

    parser.add_argument("--make-population",
        action="store_true",
        default=False,
        help="Perform Stage 3 of the Workflow: Generate Synthetic Population"
    )

    parser.add_argument("--fit-capacities",
        action="store_true",
        default=False,
        help="Perform Stage 4 of the Workflow: Fit Carrying Capacities"
    )

    parser.add_argument("--make-regression",
        action="store_true",
        default=False,
        help="Perform Stage 5 of the Workflow: Deviation/Capacity Regression"
    )

    parser.add_argument("--make-visualisation",
        action="store_true",
        default=False,
        help="Perform Stage 6 of the Workflow: Regression Visualisation"
    )

    parser.add_argument("--run-workflow",
        action="store_true",
        default=False,
        help="Run all Stages of the workflow in order"
    )

    if len(argv) == 1:
        parser.print_help()
        sys.exit(0)

    return parser.parse_args()


def handle_args(args):
    if args.run_workflow:
        run_workflow()

    if args.retrieve_data:
        retrieve_datasets()
        sys.exit(0)

    if args.make_deviations:
        annual_deviations = make_annual_deviations()
        write_deviations_as_netcdf(annual_deviations)
        sys.exit(0)

    if args.make_population:
        annual_deviations = load_deviations()
        pop = generate_population_series(annual_deviations)
        write_populations_as_netcdf(pop)
        sys.exit(0)


    if args.fit_capacities:
        params = np.array([1.0, 0.5])
        rx, ry = [], []

        for idx, dev in enumerate(annual_deviations):
            y = pop[idx][0:8]
            x = np.array([*range(8)])
            fit = gauss_newton_fd(x, y, params)
            rx.append(dev)
            ry.append(fit[0])

    if args.make_regression:
        b, m = np.polynomial.polynomial.polyfit(rx, ry, 1)

    if args.make_visualisation:
        plt.scatter(rx, ry)
        plt.axline((0, b), (1, b+m), color="red")
        plt.xlabel("Temperature Deviation °C")
        plt.ylabel("Annual Inferred Capacity")
        plt.show()


def run_workflow():
    params = np.array([1.0, 0.5])

    annual_deviations = make_annual_deviations()
    pop = generate_population_series(annual_deviations)

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


def main():
    args = parse_args(sys.argv)
    handle_args(args)


if __name__ == "__main__":
    main()
