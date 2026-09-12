# Result lock: stochastic tagged power-lattice adequacy

Classification:

`FULLJ_STOCHASTIC_TAGGED_POWER_LATTICE_FAIL`

This result preserves the preregistered classification. The complete 0.005 lattice and all selected half-lattice controls were executed without relaxing any threshold.

## Frozen setup

- full lattice: `k/h = 0.030,0.035,...,0.200 Mpc^-1` (35 nodes)
- Stage A geometry: `kF/h=0.005 Mpc^-1`, `NX=256`
- Stage B half-lattice geometry: `kF/h=0.0025 Mpc^-1`, `NX=512`
- Gaussian coefficient SHA256: `9c511b09899cb874d09c0513b89b82c796769886ecba5dd6347c71678b19d200`
- Stage A backgrounds: `B4={0,1,2,3}`
- Stage B backgrounds: `B2={0,1}`
- symmetric tag amplitude: `epsilon=0.05`
- 176/176 new integrations finite

## Gate outcome

Passed:

- `PL_G1_provenance_and_frozen_identity`
- `PL_G2_stageA_solver_constraint_health`
- `PL_G3_stageA_broadband_saturated_closure`
- `PL_G4_complete_lattice_algebra_background_sanity`
- `PL_G5_stageB_solver_constraint_saturation_health`

Failed:

- `PL_G6_power_half_lattice_interpolation_accuracy`
- `PL_G7_no_unresolved_selected_interval_power_spike`

## Solver and stochastic health

The failure is not a solver, constraint, saturation, or background-sampling failure.

- Stage-A saturation maximum: `4.686860739225767e-05`
- Stage-B saturation maximum: `4.305454091526383e-05`
- tagged power algebra residual: `8.402032262086121e-18`
- new-node B2->B4 response global relative L2: `1.4972561232033347e-08`
- new-node B2->B4 response per-k maximum: `4.500162052456869e-08`
- new-node B2->B4 power global relative L2: `1.2008620017571966e-08`
- new-node B2->B4 power per-k maximum: `8.798466353011845e-08`

## Half-lattice interpolation result

The high-redshift power interpolant is accurate, but the error grows strongly at late time:

| z | power L2 | power peak |
|---:|---:|---:|
| 6.0 | 6.6744e-4 | 7.2244e-4 |
| 5.0 | 6.7635e-4 | 7.3020e-4 |
| 4.0 | 7.0944e-4 | 7.5096e-4 |
| 3.0 | 9.5091e-4 | 8.3427e-4 |
| 2.0 | 3.3287e-3 | 1.8036e-3 |
| 1.5 | 9.2479e-3 | 5.3038e-3 |
| 1.0 | 3.0061e-2 | 1.7516e-2 |
| 0.5 | 9.6605e-2 | 5.5873e-2 |
| 0.2 | 3.0864e-1 | 1.8662e-1 |

The frozen maxima are therefore:

- `power_half_L2_max = 0.3086377990034805`
- `power_half_L2_median = 0.003328742986623499`
- `power_half_peak_max = 0.18662232403879295`
- power interpolant finite and nonnegative: `true`

The median criterion passes, but the frozen maximum-L2 and peak criteria fail at late time.

## Direct unresolved half-lattice structure

The power spike veto fails with

`power_midpoint_spike_max_ratio = 11.436423060133826`.

The strongest direct example is at `z=0.2`, `k/h=0.0975`:

- direct midpoint power: about `8.512e-3`
- neighboring full-lattice powers: about `7.44e-4` and `3.8e-5`
- direct midpoint / max(endpoint) ratio: about `11.436`
- PCHIP prediction from the 0.005 lattice: about `2.18e-4`

Further preregistered spike-veto violations occur at approximately:

- `z=0.2`, `k/h=0.1225`, ratio `2.510`
- `z=1.0`, `k/h=0.1975`, ratio `2.200`

The largest peak-normalized interpolation discrepancies at `z=0.2` are concentrated around `k/h=0.1575-0.1975`, with additional sharp structure around `0.0875-0.1225`.

## Interpretation lock

This result does not invalidate the stochastic tagged construction. The solver, constraints, broadband saturation, power algebra, and B2->B4 stochastic convergence remain strongly validated. The preceding response-kernel POC also established that the response is diagonal to very high precision, so the present late-time structure is not explained by hidden off-diagonal mode coupling.

However, the current experiment compares two different periodic embeddings: Stage A uses `kF/h=0.005, NX=256`, while Stage B uses a doubled box with `kF/h=0.0025, NX=512` at the same physical grid spacing. The power-lattice preregistration did not include a same-k box-doubling regression. Therefore the next bounded step is not to loosen thresholds or immediately declare a physical sub-0.005 radial spectrum. First perform a common-node box-doubling audit on identical k values under both geometries. If that audit passes, the half-lattice failures can be attributed to under-resolution of genuine radial structure and a finer/adaptive power lattice is justified. If it fails, the periodic embedding dependence must be resolved before any continuum claim.

## Scope after this FAIL

Remain true/tested:

- stochastic broadband tagged response POC
- broadband low-k saturation
- scalar diagonal reduction supported by the full response-kernel POC
- complete 0.005 lattice numerically computed and finite
- B2->B4 background convergence on new 0.005 nodes

Remain false/unlicensed:

- `STOCHASTIC_TAGGED_FULL_005_LATTICE_TESTED=False`
- `STOCHASTIC_TAGGED_BOUNDED_POWER_INTERPOLANT_TESTED=False`
- `THREE_D_BOUNDED_CONTINUOUS_WEYL_POWER_LICENSED=False`
- `THREE_D_CONTINUOUS_WEYL_POWER_LICENSED=False`
- `EVOLVING_WEYL_POWER_LICENSED=False`
- `ACT_LIKELIHOOD_LICENSED=False`
- `OBSERVATIONAL_CLAIM_LICENSED=False`
