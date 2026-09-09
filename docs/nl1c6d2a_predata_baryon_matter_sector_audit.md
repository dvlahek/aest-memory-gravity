# NL1C6D2A predata — baryon matter-sector audit

Status: **PREREGISTERED BEFORE NL1C6D2A MATTER-SECTOR RESULTS**.

Frozen label:

```text
NL1C6D2A_PREDATA_BARYON_MATTER_SECTOR_AUDIT
```

## Motivation and scope

NL1C6D1 is locked as

```text
NL1C6D1_DYNAMICAL_FORMULATION_AUDIT_PASS
```

for the repository's one-dimensional periodic longitudinal weak-field gravitational sector.

D1 does not yet permit nonlinear branch evolution with an arbitrarily prescribed time-dependent baryon density. The D1A fixed-source equation `dot(P_alpha)=0` is not the complete matter-coupled statement when `rho_b` evolves. Before D2 branch selection, the baryon density history must be accompanied by the velocity/momentum history required by stress-energy conservation.

NL1C6D2A is therefore a source/matter audit only. It does **not** evolve the nonlinear full-J AeST field, select a branch, evaluate memory `eta`, or use observational likelihoods.

## Frozen cosmological model and source identity

Use exactly the same theory-only CLASS model and Newtonian gauge as NL1C5B and the later response-map work:

```text
H0      = 67.3324639084866 km/s/Mpc
omega_b = 0.022377376877682164
K_B     = 0.0665
K2      = 9500
Q0      = 1e-4 Mpc^-1
memory  = off
eta     = 0
gauge   = newtonian
```

The CLASS implementation remains the frozen project build at commit

```text
e85808324f51fc694d12e3ed7439552a3c3f9540
```

and the frozen NL1C5B baryon-source artifact identity remains

```text
0ab60cbc32210ad3fb75c881f91a9db11148280e9223ea644680ed8cdfbaa590
```

for the source bundle already certified by NL1C5B.

The six requested wave numbers remain

```text
0.03, 0.05, 0.08, 0.10, 0.15, 0.20 h/Mpc.
```

The fresh CLASS run may add `vTk` to the requested output in order to expose baryon velocity transfer `t_b`. This is an output-only change. No physical model parameter may change.

## Matter variables and continuity equation

In CLASS `class` transfer format, the baryon density transfer is `d_b` and the baryon velocity-divergence transfer is `t_b`. In the Newtonian gauge used by the frozen project model, the CLASS baryon continuity equation is

```text
delta_b' = -theta_b + 3 phi'
```

where prime denotes conformal-time derivative and `theta_b` is the baryon velocity divergence. Equivalently,

```text
R_cont = delta_b' + theta_b - 3 phi' = 0.
```

D2A identifies the native `t_b` transfer history with the momentum/velocity information that was absent from the NL1C5B density-only freeze. No conversion of `theta_b` into a physical peculiar velocity field is required in D2A; that mapping will be frozen only in the later D2 nonlinear evolution preregistration if needed by the integrator.

## A. Native-grid density identity

Run CLASS with the same `k_output_values`, transfer conventions, `z_max_pk`, and model parameters used by NL1C5B, adding velocity transfers.

Require:

- `d_b` exists and is finite;
- `t_b` exists and is finite;
- `d_m` exists and is finite;
- fresh and frozen transfer array shapes are identical;
- maximum relative `k`-grid mismatch `<= 1e-12`;
- maximum absolute `z`-grid mismatch `<= 1e-12`;
- fresh `d_b` versus frozen NL1C5B `d_b` relative L2 `<= 1e-10`;
- fresh `d_m` versus frozen NL1C5B `d_m` relative L2 `<= 1e-10`;
- requested six `k` values match to relative error `<= 1e-12`.

A failure of density identity is a D2A FAIL; the velocity output may not silently define a different baseline cosmology.

## B. Dense-history continuity regression

Use CLASS `k_output_values` and `get_perturbations()` to obtain dense scalar perturbation histories for the same six requested modes. For every mode require finite arrays for

```text
tau [Mpc], a, delta_b, theta_b, phi
```

and use direct `phi_prime` when supplied by the frozen CLASS wrapper. If `phi_prime` is not present, its derivative is reconstructed from the same dense `phi(tau)` history with a cubic spline; this fallback is fixed before results.

The derivative `delta_b'` is reconstructed with a cubic spline in conformal time. Duplicate/non-increasing time samples, if any, are removed deterministically before spline construction.

Evaluate only samples with

```text
0.2 <= z <= 6.0
```

and discard the first and last two retained samples of each mode to avoid spline-edge differentiation. At least 20 interior samples per mode are required.

For each mode define

```text
R_cont = delta_b' + theta_b - 3 phi'
```

and the normalized L2 residual

```text
||R_cont||_2 /
max(||delta_b'||_2, ||theta_b||_2, ||3 phi'||_2, 1e-300).
```

Frozen gate:

```text
max continuity normalized L2 residual <= 2e-3.
```

This gate audits extraction/interpolation consistency; it is not a replacement for the internal CLASS ODE tolerance.

## C. Dense/native transfer identity

For each requested mode, interpolate the dense CLASS `delta_b` and `theta_b` histories to the native transfer redshifts over the common range `0.2 <= z <= 6.0`. Interpolation is performed deterministically with cubic splines after sorting by redshift and removing duplicate redshift samples.

Compare against the corresponding native transfer-grid `d_b` and `t_b` values. Frozen gates:

```text
max dense-vs-native d_b relative L2 <= 2e-4
max dense-vs-native t_b relative L2 <= 2e-4.
```

These controls establish that `t_b` and the dense `theta_b` history are the same baryon momentum variable in the frozen CLASS normalization and that the dense history is aligned with the already frozen density source.

## D. Output bundle

A PASS bundle must save at least

```text
k_native_h
z_native
d_b
t_b
d_m
```

and, when available from the native transfer output,

```text
phi
psi
```

plus JSON diagnostics containing the CLASS transfer keys, dense-history keys, identity metrics, continuity residuals, interpolation controls, git commit, and declared frozen input identity.

The bundle is a matter-history input for a later D2 preregistration. It is not itself a nonlinear AeST solution.

## Frozen D2A classifications

All density-identity, finite-momentum, continuity, and dense/native identity gates pass:

```text
NL1C6D2A_BARYON_MATTER_SECTOR_AUDIT_PASS
```

Otherwise:

```text
NL1C6D2A_BARYON_MATTER_SECTOR_AUDIT_FAIL
```

## Continuation rule

Only

```text
NL1C6D2A_BARYON_MATTER_SECTOR_AUDIT_PASS
```

permits preregistration of the nonlinear D2 branch-selection evolution.

A D2A PASS does not by itself establish a physical full-J trajectory. The later D2 preregistration must separately freeze the background/time variable, initialization, pressure/dust approximation if used, mapping of baryon momentum into the reduced AeST equations, time integrator, constraint handling, treatment of the sharp interpolation kink, resolution/time-step controls, and classifications for settling, persistent dynamics, branch switching, or numerical failure.

NL1C7 causal-memory physics remains blocked until D2 establishes a self-consistent nonlinear full-J trajectory.
