# Full-J metric projection physical-k mask repair result

Date: 2026-09-12

## Classification

`FULLJ_METRIC_PROJECTION_PHYSICAL_KMASK_REPAIR_PASS`

The preregistered physical-k repair audit completed successfully. The historical box-doubling failure is preserved as a historical FAIL and is not rewritten. The repair validates that the failure was caused by the inherited Fourier-index cutoff `n<=32` changing its physical meaning when the periodic box changed.

## Repair definition

The historical R2 metric projection used `NMAX=32` in the original geometry with `kF/h=0.01`, which is physically equivalent to

`0 < |k|/h <= 0.32`.

The repaired projection preserves this physical cutoff independently of box size. In the original R2 geometry the repaired mask is exactly identical to the historical mask:

- `metric_kmax_h = 0.32`
- `original_kF_h = 0.01`
- `nx = 128`
- `mismatch_count = 0`
- `identical = true`

Therefore the repair does not alter the original R2 result.

## Audit setup

Four physical tagged modes were tested:

`k/h = {0.06, 0.095, 0.16, 0.195}`.

For each mode the audit used two frozen Gaussian backgrounds, both tag signs, and two geometries:

- geometry A: `kF/h=0.005`, `NX=256`, `box=1866.3167638478922 Mpc`
- geometry B: `kF/h=0.0025`, `NX=512`, `box=3732.6335276957843 Mpc`

The total was 32 repaired runs.

## Result

All 32/32 runs were finite and all eight preregistered gates passed.

Numerical summary:

- `canonical_max = 1.8097824858362603e-14`
- `broadband_saturation_max = 4.288739111533391e-05`
- metric Hamiltonian residual max `= 1.8533251051449448e-16`
- metric momentum residual max `= 1.5283987431465636e-16`
- metric shear residual max `= 0`
- doubled-box repeat field max `= 8.079165690921655e-12`
- direct A/B field relative-L2 max `= 2.0111915213430488e-12`
- tagged-response global relative-L2 `= 6.6732360256820115e-15`
- tagged-response per-k max `= 1.6056515287574077e-14`
- tagged-response per-z max `= 1.3267708312139603e-14`
- tagged-power global relative-L2 `= 6.2923105961568036e-15`
- tagged-power per-k max `= 2.939406053885455e-14`
- tagged-power per-z max `= 1.4505558403050873e-14`

The A/B box differences collapse to numerical precision once the metric projection cutoff is defined in physical k rather than Fourier index.

## Interpretation

The prior box-doubling FAIL was an implementation artifact caused by a box-dependent metric-projection mask. It was not evidence for box dependence of the retained nonlinear dynamics, tagged response, or tagged power.

The repaired calculation establishes:

- `METRIC_PROJECTION_PHYSICAL_KMASK_REPAIR_VALIDATED=True`
- `STOCHASTIC_TAGGED_BOX_DOUBLING_INVARIANCE_REPAIRED=True`

The repair also confirms that the original R2 calculation is unchanged because the repaired physical-k mask is exactly identical to the historical mask in the original R2 geometry.

## Scope

This PASS is deliberately narrow. It does not by itself license a bounded continuous Weyl-power interpolant, continuous 3D Weyl power, evolving cosmological Weyl power, line-of-sight lensing, ACT likelihood use, or observational claims.

The following remain false after this result:

- `STOCHASTIC_TAGGED_BOUNDED_POWER_INTERPOLANT_TESTED=False`
- `THREE_D_BOUNDED_CONTINUOUS_WEYL_POWER_LICENSED=False`
- `THREE_D_CONTINUOUS_WEYL_POWER_LICENSED=False`
- `EVOLVING_WEYL_POWER_LICENSED=False`
- `ACT_LIKELIHOOD_LICENSED=False`
- `OBSERVATIONAL_CLAIM_LICENSED=False`

The next bounded milestone is a repaired tagged-power regression/power-lattice rerun using the physical-k metric projection consistently in both geometries before any 3D/isotropic lift or line-of-sight construction.
