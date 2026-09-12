# Full-J evolving FLRW Weyl bridge R2 result

## Classification

`FULLJ_EVOLVING_WEYL_BRIDGE_R2_PASS`

This result closes the R2 triangular evolving-FLRW Weyl bridge milestone on the locked D2C6 canonical trajectories.

Historical classifications are preserved:

- R0: `FULLJ_EVOLVING_WEYL_BRIDGE_FAIL`
- R1: `FULLJ_EVOLVING_WEYL_BRIDGE_R1_FAIL`
- R1A continuity audit: formal FAIL only because the preregistered ill-conditioned algebraic Theta-map identity gate did not meet 1e-12; the continuity equation itself passed strongly.
- R1B Euler audit: `FULLJ_WEYL_R1B_EULER_IDENTITY_PASS`.

The R2 run used git head:

`970b5fd1612e52aa3adff98d6d0b0a6084a40cf7`

## Locked scope

R2 is an eta=0 triangular evolving-FLRW Weyl bridge on locked D2C6 canonical trajectories. The canonical state `(alpha, chi, P_chi, S)` is unchanged. The effective-fluid pair `(delta_A, Theta_A)` is evolved directly with the action-derived continuity and Euler equations certified by R1A/R1B. The numerically ill-conditioned algebraic reconstruction `Theta_A ~ k^2/a (chi/Q-alpha)` is not used in the RHS.

Metric reconstruction uses the same corrected CLASS baseline and the locked D2C6G Hamiltonian/momentum/shear convention. The nonlinear completion adds no retained shear correction at this order, so the corrected CLASS evolving slip is preserved algebraically.

This is not a fully coupled nonlinear cosmological evolution: reconstructed nonlinear metric variables are not fed back into the locked canonical D2C6 trajectory.

## Gates

### G1 — source-equation provenance

PASS.

- `rho_plus_p_identity_rel_max = 1.4676848337955002e-16`
- R1A continuity equation certification retained.
- R1B Euler equation certification retained.
- `ill_conditioned_theta_reconstruction_used_in_RHS = false`
- nonlinear completion shear source maxabs = 0.

### G2 — linear corrected-CLASS regression

PASS with gate 5e-3.

- `Phi relative_L2 = 3.5663537228334447e-06`
- `Psi relative_L2 = 3.566353762253849e-06`
- `W relative_L2 = 3.566353742544462e-06`
- `delta_A relative_L2 = 1.0794106743933171e-05`
- `Theta_A relative_L2 = 1.1537477451593335e-05`

Metric-correction constraint residuals in the linear control:

- Hamiltonian = `1.0929277789329367e-16`
- momentum = `6.12446047960491e-17`
- shear = `0`

### G3 — static/fixed-a full-J regression

PASS with gate 1e-10.

- maximum error = `1.6558749359114465e-15`

Thus the bridge retains the locked static identity `Psi -> Phi` and `W -> 2 Phi` only in the static/fixed-a limit.

### G4 — evolving metric constraint closure

PASS with gate 1e-8.

Across all nonlinear members:

- Hamiltonian max = `1.792857169360222e-16`
- momentum max = `1.8242139578042917e-16`
- shear max = `0`

### G5 — finite evolving output

PASS.

- finite members = `27/27`

All 27 co-primary nonlinear trajectory members produced finite evolving `Phi`, `Psi`, `W`, `slip`, `delta_A`, and `Theta_A` outputs at the retained checkpoints.

### G6 — static-versus-evolving slip distinction

PASS.

- slip-to-CLASS-slip relative L2 max = `0`
- global slip maxabs = `7.580377501376599e-13`

The evolving slip is therefore not silently forced to zero.

### G7 — no ill-conditioned Theta reconstruction in RHS

PASS.

- `directly_evolved_Theta_A = true`

This is the numerical repair established by the R1A/R1B diagnostic sequence.

## Interpretation

R2 establishes a parameter-free evolving Weyl reconstruction on the locked nonlinear full-J trajectory grid that:

1. reproduces the corrected CLASS linear limit at approximately 3.6e-6 relative L2 in `Phi`, `Psi`, and `W`;
2. reproduces the static full-J limit at machine precision;
3. closes the projected Hamiltonian, momentum, and shear constraints at machine precision;
4. remains finite for all 27 nonlinear members;
5. preserves the evolving corrected-CLASS slip;
6. avoids the independently demonstrated catastrophic conditioning of the algebraic `Theta_A` reconstruction.

The R1 failure is therefore resolved as a numerical-state-choice problem rather than a failure of the effective-fluid equations: R1A certified the continuity identity, R1B certified the Euler identity, and R2 succeeds when `Theta_A` is evolved directly.

## Licensing after R2

- `EVOLVING_WEYL_COVARIANCE_DIAGNOSTIC_LICENSED=True`
- `EVOLVING_WEYL_POWER_LICENSED=False`
- `ACT_LIKELIHOOD_LICENSED=False`
- `OBSERVATIONAL_CLAIM_LICENSED=False`
- `CANONICAL_TRAJECTORY_METRIC_FEEDBACK_ENABLED=False`

The next allowed step is a separately preregistered evolving Weyl covariance diagnostic. A cosmological stochastic Weyl power spectrum, line-of-sight lensing prediction, ACT likelihood, and observational claim remain unlicensed.