# Full-J evolving Weyl covariance diagnostic — locked result

## Classification

The preregistered algebraic covariance diagnostic completed with

`FULLJ_EVOLVING_WEYL_COVARIANCE_DIAGNOSTIC_PASS`.

All six frozen gates passed.

## Locked numerical result

Primary matrices: 81, each 33 x 33.

Secondary theory-grid matrices: 9.

Algebraic health:

- max primary Hermiticity relative residual = `9.787708156291717e-22`
- min primary eigenvalue / max |eigenvalue| = `-7.364404041103933e-16`
- max primary trace-identity relative residual = `4.3326031713051555e-16`
- max secondary Hermiticity relative residual = `1.7519356253345916e-21`
- min secondary eigenvalue / max |eigenvalue| = `-5.148905681562549e-16`
- primary numerical rank: min 1, median 1, max 2
- primary off-diagonal Frobenius fraction: min `1.4158717369143633e-14`, median `0.7975407532713593`, max `0.7975476941285173`
- primary covariance trace: min `1.6815581571897805e-44`, median `3.3742304351929857e-20`, max `1.8706259438478836e-13`

The small negative eigenvalue ratios are at floating-point roundoff level and satisfy the frozen positive-semidefinite consistency gate.

## Gate result

- G1 locked R2 provenance: PASS
- G2 finite covariance construction: PASS
- G3 Hermiticity: PASS
- G4 positive-semidefinite consistency: PASS
- G5 sample covariance trace identity: PASS
- G6 structural three-sample rank bound: PASS

## Post-data terminology correction

The preregistration and first implementation called the three-member primary object "phase-conditioned" because it grouped the `sigma=-1,0,+1` members. Inspection of the already locked D2C6B source shows that this wording is incorrect.

In `nl1c6d2c6b/all27_physical_nonlinear_trajectories.py`, `sigma` enters

`mix = 1 + sigma * EPS_MIX * sx * tanh(Z)^2`

inside the nonlinear constitutive factor `j_eff`. Therefore `sigma` is a deterministic nonlinear-completion deformation coordinate. It is not a random Fourier phase.

This terminology correction does not change any matrix, gate, threshold, or PASS/FAIL result. The 81 primary matrices are correctly interpreted as centered covariance/sensitivity matrices across the three locked `sigma` completion branches at fixed `(kind,beta0,z)`. They are not stochastic cosmological covariance matrices.

The 9 secondary matrices remain centered sensitivity covariances over the full 27-member deterministic theory grid and are also non-stochastic.

Accordingly, the numerical PASS is retained as an algebraic/theory-grid covariance diagnostic, while no stochastic or observational license is added.

## Interpretation lock

The result establishes that the evolving R2 Weyl outputs admit finite, Hermitian, positive-semidefinite, internally consistent covariance-like sensitivity objects over the locked nonlinear-completion grid.

The relatively large median off-diagonal Frobenius fraction (~0.798) shows substantial cross-mode covariance in this deterministic completion sensitivity object. It must not be interpreted as the off-diagonal covariance of a cosmological random field.

The wide trace range also must not be interpreted as a cosmological Weyl power amplitude because the sampling directions are deterministic theory choices.

Therefore:

- `EVOLVING_WEYL_COVARIANCE_DIAGNOSTIC_TESTED=True`
- `THEORY_GRID_IS_COSMOLOGICAL_ENSEMBLE=False`
- `EVOLVING_WEYL_POWER_LICENSED=False`
- `ACT_LIKELIHOOD_LICENSED=False`
- `OBSERVATIONAL_CLAIM_LICENSED=False`

Historical R0/R1 failures and the R2 PASS remain unchanged.

## Next milestone

The next scientifically distinct milestone is a separately preregistered stochastic realization test. It must randomize the actual Fourier realization coefficients, not `sigma`. Because the current nonlinear evolution is performed on a one-dimensional periodic embedding, the first stochastic milestone should be labeled a 1D Gaussian-realization Weyl-spectrum/convergence diagnostic. A PASS there still does not by itself establish an isotropic 3D cosmological `P_W(k,z)` for lensing. A separate 3D/isotropic power bridge is required before line-of-sight lensing or ACT can be licensed.
