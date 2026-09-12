# Full-J isotropic Weyl transfer nodes R1 phase audit — locked result

## Classification

`FULLJ_ISOTROPIC_WEYL_TRANSFER_NODES_R1_PHASE_AUDIT_PASS`

This result is a post-failure zero-safe phase audit of the already completed six-node isotropic transfer calculation. It does not replace or rewrite the historical original classification

`FULLJ_ISOTROPIC_WEYL_TRANSFER_NODES_FAIL`.

The historical failure remains preserved because its preregistered local phase ratio used `|Im T|/|T|`, which became ill-conditioned at a near-zero transfer cell.

## Locked ancestry

The completed audit reported all ancestry/provenance locks true, including the historical FAIL result, original predata/implementation/runner, and the separately preregistered R1 phase-audit declaration.

## Zero-safe phase result

The historical worst cell was

- mode `n=10`, `k/h=0.10 Mpc^-1`, `z=0.2`,
- `Re(T)=0.006174491143802195`,
- `Im(T)=-4.167138770915273e-10`,
- legacy local ratio `|Im T|/|T| = 6.748959021664703e-08`.

The zero-safe global quadrature diagnostics are instead

- six-mode `||Im T||_2 / ||T||_2 = 2.111968330037605e-09`,
- single-mode `||Im T||_2 / ||T||_2 = 9.307488239399517e-10`,
- max absolute six-mode imaginary component `3.6506339129726453e-09`,
- max absolute single-mode imaginary component `1.2628847863942706e-09`.

The original `1e-8` phase tolerance was not relaxed.

## Real-transfer projection

Replacing the complex numerical transfer by its physically reported real component changes the discrete Weyl power nodes by at most

`4.443528347476122e-15`

with median change exactly zero at reported precision.

Therefore the quadrature component is numerically irrelevant for the certified discrete power nodes.

## Retained independent validations

The R1 audit retained the independent validations from the completed original calculation:

- amplitude-homogeneity max: `2.6170804943117027e-06`,
- Gaussian-ratio reconstruction max: `1.7807695548234596e-08`,
- off-target leakage max: `7.451381233238023e-12`,
- power identity residual: `7.174174695641998e-18`,
- single-vs-multi separability max: `1.0487263309295026e-06`.

All five R1 gates passed:

- `R1_G1_provenance_historical_state_lock=True`,
- `R1_G2_global_zero_safe_phase_consistency=True`,
- `R1_G3_absolute_quadrature_leakage=True`,
- `R1_G4_real_projection_power_contamination=True`,
- `R1_G5_retained_independent_validations=True`.

## Licensed scope

This PASS licenses

- `REAL_TRANSFER_PROJECTION_LICENSED=True`,
- `THREE_D_ISOTROPIC_WEYL_TRANSFER_NODES_LICENSED=True`,
- `THREE_D_ISOTROPIC_WEYL_POWER_NODES_LICENSED=True`.

It does not license interpolation between the six nodes, extrapolation outside the tested radial interval, a continuous Weyl spectrum, line-of-sight lensing, ACT likelihood use, or observational claims. Therefore

- `THREE_D_CONTINUOUS_WEYL_POWER_LICENSED=False`,
- `EVOLVING_WEYL_POWER_LICENSED=False`,
- `ACT_LIKELIHOOD_LICENSED=False`,
- `OBSERVATIONAL_CLAIM_LICENSED=False`.

## Next milestone

The next milestone is a separately preregistered dense-radial-node extension on the already licensed interval `0.03 <= k/h <= 0.20 Mpc^-1`, with direct new R2 nodes and nested-grid interpolation/convergence tests. No line-of-sight lensing calculation is licensed before that test is complete.
