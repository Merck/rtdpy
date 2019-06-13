---
title: 'rtdpy: A python package for residence time distributions'
tags:
  - Python
  - residence time distribution
authors:
  - name: Matthew H. Flamm
    orcid: 0000-0002-2040-5481
    affiliation: "1"
affiliations:
 - name: US Data Science and Applied Mathematics, Merck & Co., Inc., Kenilworth, NJ, USA
   index: 1
date: 12 June 2019
bibliography: paper.bib
---

# Summary

Residence time distributions (RTDs) are used to understand nonideality in chemical
reactors and other continuous flow through steps[@levenspiel_1999]. Applications
include chemical reaction conversion[@danckwerts_1953], pipeline mixing
[@levenspiel_1958], and material traceability[@engisch_muzzio_2016]. RTDs also
characterize flow patterns in stream flows [@haggerty_wondzell_johnson_2002] with
applications in transport of pollutants [@kirchner_feng_neal_2000].

A residence time distribution, also known as the exit-age function, is the
distribution of time material takes to exit a volume once it enters. While
some RTD models are nearly trivial to implement, some require numerical
solutions to PDE advection-diffusion equations. In many analyses, there is a
need to combine multiple RTD models together, particularly for processes with
mutliple unit operations. Common RTD analyses are output prediction given an
input signal, frequency-space signal damping, and disturbance mapping.

``rtdpy`` is a Python package that enables quick and easy computation and usage
of RTD models.  Current model functionality is focused on continuous process
unit operations.   RTD models include:

* N-continually stirred tank reactors (NCSTR), AKA tanks-in-series
* Tube flow with Axial Dispersion
  * Large Peclet number assumption
  * Open-open boundary conditions
  * Closed-closed boundary conditions
* Plug flow reactor (PFR)
* Pure convection model
* Zusatz model
* Any arbitrary combinations of the above

Built-in functionalities for all RTD models include:

* The RTD itself
* Mean residence time
* Variance
* Frequency response
* Disturbance funnelplot
* Input signal convolution
* Step response

![Figure 1.](../images/ncstr.png?raw=true "N-Cstr RTDs")

``rtdpy`` is enabled by ``numpy`` and ``scipy`` packages. Documentation on all
major funcitonality and all RTD models is included in the repository.  Several
examples of common workflows are also provided. The base RTD class is available
for adding additional functionality. The RTD class can also be extended for
future or user-defined RTD models.

# References
