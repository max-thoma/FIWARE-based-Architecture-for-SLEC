# FIWARE-based Architecture for Smart Local Energy Communities

This repository holds the code for the work-in-progress Paper [FIWARE-based Architecture for Smart Local Energy Communities](https://ieeexplore.ieee.org/document/10228053) published at the ISIE 2023 conference.
Please notice that the implementation is considered as _work-in-progress_ and is not stable or ready for production.

## Project Overview

The `docker` directory holds all relevant files to build, run, and configure the containerized infrastructure. The implementation of the co-simulation scenarios can be found in the `src` folder.

## Getting started

To get started using running this project you need a couple of tools:

- [just](https://github.com/casey/just): a modern command runner
- [poetry](https://python-poetry.org): a modern Python package manager
- Docker
- curl

After installing both tools, run the following command to set up your Python environment:

```sh
just install
```

Then, select one of the four simulation scenario by changing the `src/scenario.py` file.
There are four possible scenarios:


1. `WITH_OPTI_NO_EM`: With the optimizer enabled and no Smart Meter data
2. `NO_OPTI_NO_EM`: With the optimizer disabled and with Smart Meter data
3. `WITH_OPTI_WITH_EM`: With the optimizer enabled and no Smart Meter data
4. `NO_OPTI_WITH_EM`: With the optimizer disabled and Smart Meter data

Finally to run the simulation run the following just command:

```sh
just sim
```

If the simulation was successful, the results are stored in `src/graphs`

## Simulator

There are three main simulator deployed:

1. Photovoltaic Simulator: this simulator us [pvlib](https://pvlib-python.readthedocs.io/en/stable/)
2. Warm Water Tank Simulator: this is a simplified model of a Warm Water Tank and very much work-in-progress
3. Usage Profiles: the warm water and electricity demands have been simulated with the [LoadProfileGenerator](https://www.loadprofilegenerator.de)

## Time Series Data and Grafana Dashboard 

As this project uses FIWARE as IoT Platform, it is straight forward to integrate a time series data base such as CrateDB.
The pluming to this is already implemented in this project.
The best way to start is by following the official FIWARE [Tutorial](https://ngsi-ld-tutorials.readthedocs.io/en/latest/time-series-data.html).
An example Grafana Dashboard can be found in `docker/grafana-dashboard.json`.
