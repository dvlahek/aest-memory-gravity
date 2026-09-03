# v0.19 — AeST eta=0 CLASS physics bridge

This is the first gate that **actively changes CLASS cosmological physics**.

It reinterprets the standard CDM background/perturbation slot as the published AeST effective dark component when `aest_enabled = yes`, adds the scalar closure states `alpha_aest` and `E_aest`, and keeps memory strictly disabled (`eta=0`). Standard CLASS remains unchanged when `aest_enabled = no`.

Two published AeST background benchmarks are included: Cosh and Exp. The scalar initial condition used here is the regular proxy `chi_i=0, E_i=0`. It is deliberately not presented as the exact radiation-era adiabatic initial condition used by the original AeST Boltzmann calculation, because that derivation was not given in the 2021 primary paper.

The GitHub Action performs the v0.18 off-regression again, compiles the active patch, runs CDM/Cosh/Exp in Newtonian gauge, and reports background and CMB-spectrum diagnostics.
