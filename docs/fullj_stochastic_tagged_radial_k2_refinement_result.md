# Full-J stochastic tagged radial K2 refinement — locked result

## Classification

`FULLJ_STOCHASTIC_TAGGED_RADIAL_K2_REFINEMENT_FAIL`

This is a formal FAIL of the preregistered K1->K2 scalar tagged-radial continuum milestone. The FAIL is preserved and is not reinterpreted as a PASS.

## Frozen setup

- Parent K1->K2 preregistration and implementation ancestry preserved.
- Frozen Gaussian seed: `20260912`.
- Frozen coefficient SHA256: `9c511b09899cb874d09c0513b89b82c796769886ecba5dd6347c71678b19d200`.
- Common geometry: `kF/h = 0.005`, `NX = 256`, `NSTEP = 4096`, box `1866.3167638478922 Mpc`.
- Locked K1 grid: 11 nodes.
- Added H2 interior nodes: `{0.035,0.045,0.055,0.070,0.085,0.095,0.110,0.135,0.160,0.185} h Mpc^-1`.
- Combined K2 grid: 21 nodes over `0.03 <= k/h <= 0.20 Mpc^-1`.
- Four common-random Gaussian backgrounds and symmetric `+/- epsilon` tagging with `epsilon=0.05`.
- 80 new nonlinear R2 integrations; all old K1 response values were reused from the locked K1 result.

## Numerical health

All 80/80 new runs completed and remained constraint-clean. Canonical residuals stayed at approximately `1e-14` or below, with metric constraints at machine precision. The maximum broadband saturation residual was

`4.685341037108981e-05`,

well inside the locked broadband saturated regime.

Background convergence remained extremely strong:

- global response B2->B4 relative difference: `8.365367254904334e-09`,
- maximum per-k response B2->B4 relative difference: `4.4084083713327985e-08`,
- global power B2->B4 relative difference: `6.395079131901006e-09`,
- maximum per-k power B2->B4 relative difference: `1.0639544074888503e-07`.

The tagged power identity residual was `9.331016323231795e-18`.

Therefore the FAIL is not caused by solver instability, Gaussian-background nonconvergence, loss of the broadband saturated constitutive regime, or tagged-power algebra.

## Radial refinement result

The K1->K2 refinement improved both transfer and power holdout error at **all 9 redshifts**. This is an important monotonic refinement result, but the locked absolute accuracy gates still fail at late time.

Direct K1->K2 holdout errors:

- at `z=6`: transfer L2 `0.00378796`, power L2 `0.00543186`,
- at `z=1`: transfer L2 `0.0317236`, power L2 `0.0221005`,
- at `z=0.5`: transfer L2 `0.143397`, power L2 `0.0820088`,
- at `z=0.2`: transfer L2 `0.330989`, power L2 `0.202117`.

Continuous K1->K2 refinement errors show the same pattern:

- median transfer L2: `0.00255631`,
- median power L2: `0.00241799`,
- maximum transfer L2: `0.195495`,
- maximum power L2: `0.0931768`,
- maximum power peak error: `0.0769497`.

The direct radial smoothness/spike veto also fails, with maximum interior-to-endpoint ratio `2.686695371706448`.

## Gates

PASS:

- `K2_G1_provenance_and_locked_K1_identity`
- `K2_G2_all_80_new_runs_finite_constraint_clean`
- `K2_G3_broadband_saturated_closure`
- `K2_G4_tagged_response_power_algebra`
- `K2_G5_new_node_background_convergence_B2_to_B4`
- `K2_G9_refinement_improves_every_redshift`

FAIL:

- `K2_G6_direct_K1_to_K2_holdout_accuracy`
- `K2_G7_continuous_K1_to_K2_radial_convergence`
- `K2_G8_direct_radial_smoothness_spike_veto`

## Interpretation lock

The stochastic broadband tagged construction itself remains numerically healthy and highly reproducible. K1->K2 refinement improves at every redshift, so the earlier K0->K1 failure was not random numerical noise. However, the late-time diagonal scalar tagged response develops real sign-changing and locally sharp radial structure that is not represented by a smooth scalar interpolation at the preregistered accuracy.

This result therefore triggers the preregistered conceptual pivot: do **not** continue K3/K4 scalar-grid densification merely to force a smooth transfer. The next bounded diagnostic must measure the full directional response kernel `K(k_out,k_in,z)` around the frozen broadband Gaussian backgrounds and quantify off-diagonal mode coupling. That diagnostic decides if the scalar diagonal response is an adequate reduced object or if a genuine mode-coupling kernel is required.

## Scope after this result

- `STOCHASTIC_TAGGED_RADIAL_CONTINUUM_LICENSED=False`
- `STOCHASTIC_TAGGED_BOUNDED_RESPONSE_TESTED=False`
- `THREE_D_BOUNDED_CONTINUOUS_WEYL_POWER_LICENSED=False`
- `THREE_D_CONTINUOUS_WEYL_POWER_LICENSED=False`
- `EVOLVING_WEYL_POWER_LICENSED=False`
- `ACT_LIKELIHOOD_LICENSED=False`
- `OBSERVATIONAL_CLAIM_LICENSED=False`
