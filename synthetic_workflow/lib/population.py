import math

import numpy as np


seasonal_min_prop = 0.3
rate = 0.5

np.random.seed(0x20)


def logistic_initial(K, r, t, P0=seasonal_min_prop):
    n = K*P0*np.exp(r*t)
    d = K + P0*(np.exp(r*t) - 1)
    return n/d


def make_logistic_seasonal_cycle(prev_seasonal_min, t1_dT):
    """
      An annualised pattern of growth and decline in a bee population, via:
      https://www.honeybeesuite.com/the-cyclic-nature-of-honey-bee-populations

      This models a logistic function which grows towards a capacity of K_max
      from February to June and then declines to a threshold of K_min from
      November to February.
    """
    stress_coeff = -0.03
    max_cap = 1.0
    rate = 0.5

    curr_year_stress = 1 + stress_coeff*t1_dT

    feb_jun = logistic_initial(max_cap*curr_year_stress, rate, np.linspace(0, 15, 5), P0=prev_seasonal_min)
    jul_oct = np.repeat(feb_jun[-1], 4)
    nov_jan = logistic_initial(seasonal_min_prop*curr_year_stress, rate, np.linspace(1, 3, 3), P0=jul_oct[-1])

    cycle = np.concatenate([feb_jun, jul_oct, nov_jan])
    return cycle + np.random.normal(0, -stress_coeff/2, size=cycle.shape)


def make_sinusoidal_seasonal_cycle():
    """
      N.B. Unused
      An annualised pattern of growth and decline in a bee population, via:
      https://www.honeybeesuite.com/the-cyclic-nature-of-honey-bee-populations

      This assumes a sinusoidal pattern of growth between the annual minimum
      in February and peak in June, then a period of decline from November to
      February.
    """
    season_angle = np.concatenate([
        np.linspace(0, math.pi/2, 5),
        np.repeat(math.pi/2, 3),
        np.linspace(math.pi/2, math.pi/8, 4)
    ])
    shift_sa = np.roll(season_angle, 1)
    return seasonal_min_prop + np.sin(shift_sa)*(1 - seasonal_min_prop)


def generate_population_series(annual_deviations):
    pop = []
    prev_seasonal_min = 0.3

    for dev in annual_deviations:
        p = make_logistic_seasonal_cycle(prev_seasonal_min, dev)
        pop.append(p)
        prev_seasonal_min = p[-1]

    return pop
