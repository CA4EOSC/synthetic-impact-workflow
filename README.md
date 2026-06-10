# Synthetic Climate Impact Workflow RO-Crate

## Workflow Overview

This repository provides the components of a workflow which implements
a synthetic climate impact model that relates deviations in near-surface
temperature to variations in the inferred environmental carrying-capacity
of a representative species, as derived from seasonal observations of its
population.

The workflow consists of the following conceptual stages:

1. The Copernicus CMIP6 projections are queried via the Climate Data Store api
to produce a subset of the HadGEM3 historical dataset. This provides the
monthly near-surface `tas` variable for the period 1950-2014 for the European
region. This variable is compared to the 1850-1914 mean for the same region
to derive a series of temperature deviations representing differences from this
mean.

2. A synthetic series of monthly "population observations" are generated for a
representative species over the same period. This consists of a logistic
(Verhulst) model which describes the annual seasonal cycle of the population
from a minimum in the northern hemisphere winter, growing at rate *r* to a
capacity *K* reached during summer. A normally-distributed error component
is introduced in order to represent experimental error and natural variation
around the strict logistic value. The *K* and *r* values used in generation
of the population data are discarded and only the "observations" participate
in the workflow, allowing this synthetic stage to be replaced by genuine
experimental observations.

3. This stage attempts to numerically retrieve the environmental capacity *K*
values used in stage (2) above by fitting a logistic model to the "population
observation" data using a non-linear least squares method. This allows a series
of annual inferred values for the environmental carrying capacity in a particular
year to be derived from the raw population observations. (For the case of the
synthetic data described in (2), these values should agree with the original *K*
values used to generate the population data.)

4. A linear least-squares regression is used to identify any relationship between
(i) the series of temperature deviations and (ii) the series of annual carrying
capacities. This attempts to quantify the association between variations in mean
temperature and changes in environmental carrying capacity for te species in question.

5. Visualisations and a statistical analysis of the above result may be produced.

This workflow can be considered in terms of its `Primary Datasets` and the `Processes`
which operate upon them to generate `Derived Datasets`, as represented in the following
figure.

![overview](https://github.com/CA4EOSC/synthetic-impact-workflow/blob/master/assets/climate-impact-workflow.png?raw=true)

## Outputs

The process described in Stage 4 of the [Overview](#Workflow-Overview) above results
in a linear and inversely-correlated relationship between temperature deviations and
inferred carrying capacities.

![output](https://github.com/CA4EOSC/synthetic-impact-workflow/blob/master/assets/capacity-regression.png?raw=true)
