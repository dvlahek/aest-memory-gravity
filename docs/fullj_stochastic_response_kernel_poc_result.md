# Full-J stochastic response-kernel POC — locked result

Classification:

`FULLJ_STOCHASTIC_RESPONSE_KERNEL_POC_PASS`

This document locks the completed stochastic full-response-kernel POC without expanding any downstream Weyl-power, lensing, ACT, or observational license.

## Frozen setup

- ancestry/provenance locks: all PASS
- Gaussian seed: `20260912`
- coefficient SHA256: `9c511b09899cb874d09c0513b89b82c796769886ecba5dd6347c71678b19d200`
- input modes: `k_in/h = {0.095, 0.110, 0.135, 0.160, 0.185} Mpc^-1`
- common geometry: `kF/h = 0.005 Mpc^-1`, `NX=256`, box `1866.3167638478922 Mpc`
- resolution control: `NX_high=512`
- primary tag amplitude: `epsilon=0.05`
- tangent control: `epsilon_half=0.025`
- four common-random Gaussian backgrounds
- total runs: 44

## Numerical result

All preregistered gates passed:

- `RK_G1_provenance_and_frozen_identity=True`
- `RK_G2_all_44_runs_finite_constraint_clean=True`
- `RK_G3_broadband_saturated_closure=True`
- `RK_G4_full_kernel_fourier_sanity=True`
- `RK_G5_diagonal_regression_to_locked_K2=True`
- `RK_G6_epsilon_tangent_control=True`
- `RK_G7_resolution_aliasing_control=True`

Summary diagnostics:

- `runs_finite = 44 / 44`
- `broadband_saturation_max = 5.5238424290437937e-05`
- `fourier_conjugacy_max = 3.769753085622259e-16`
- `diagonal_regression_median = 0.0`
- `diagonal_regression_max = 0.0`
- `epsilon_control_global = 8.733718515039043e-08`
- `epsilon_control_per_z_max = 3.916889802689913e-07`
- `resolution_control_global = 6.568005311156747e-08`
- `resolution_control_per_z_max = 2.945743728175932e-07`
- `bounded_kernel_B2_to_B4_global = 4.08544238306091e-08`
- `bounded_kernel_B2_to_B4_per_input_max = 6.261265961317079e-08`
- `max_bounded_offdiag_energy_fraction = 1.7917824294299406e-12`
- `max_out_of_band_leakage_fraction = 7.865977813732887e-15`
- `max_total_offdiag_energy_fraction = 1.7989942441170814e-12`

## Physical interpretation

The full positive-frequency Fourier response kernel is numerically diagonal to extremely high precision over the five deliberately difficult late-time input modes. The maximum total off-diagonal energy fraction is below `1.8e-12`, while the extracted diagonal element reproduces the locked K2 scalar tagged response exactly to stored precision.

Therefore the K0->K1 and K1->K2 radial failures are not caused by hidden off-diagonal mode mixing in the tagged linearized response. In this tested broadband saturated regime, the scalar diagonal tagged response is the correct reduced response object. The late-time radial sign changes/spikes are genuine diagonal radial structure within the frozen model and geometry, not a projection artifact from a broad response kernel.

The epsilon-halving and NX=512 controls independently show that the result is not explained by finite tag amplitude or the tested spatial-resolution/aliasing control.

## Locked scope

Set:

- `STOCHASTIC_RESPONSE_KERNEL_POC_TESTED=True`
- `STOCHASTIC_SCALAR_DIAGONAL_REDUCTION_SUPPORTED=True`
- `STOCHASTIC_MODE_COUPLING_KERNEL_REQUIRED=False`

Keep false:

- `STOCHASTIC_TAGGED_RADIAL_CONTINUUM_LICENSED=False`
- `THREE_D_BOUNDED_CONTINUOUS_WEYL_POWER_LICENSED=False`
- `THREE_D_CONTINUOUS_WEYL_POWER_LICENSED=False`
- `EVOLVING_WEYL_POWER_LICENSED=False`
- `ACT_LIKELIHOOD_LICENSED=False`
- `OBSERVATIONAL_CLAIM_LICENSED=False`

## Consequence for next milestone

Do not pursue a full off-diagonal kernel construction and do not reinterpret either tagged radial FAIL as a kernel effect. The next bounded question is radial sampling itself. Because the response is diagonal but sharply structured at late time, test the scalar tagged response on the complete `kF/h=0.005` lattice across the bounded interval, then use a preregistered `kF/h=0.0025`, `NX=512` half-lattice control at selected late-time high-curvature intervals to determine if the `0.005` radial lattice resolves the physical response sufficiently for interpolation.
