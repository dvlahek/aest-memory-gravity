# Full-J dense radial cardinality audit — locked result

## Classification

`FULLJ_DENSE_RADIAL_CARDINALITY_AUDIT_PASS`

This result closes the specific question of whether the completed dense-radial failures were caused by changing the corrected-CLASS history cardinality from 21 to 41 modes.

## Frozen rerun set

The six preregistered K2 nodes were rerun inside the same 41-mode `dense-k64` corrected-CLASS environment used by the completed residual-R2 milestone:

`k/h = [0.035, 0.040, 0.100, 0.150, 0.1625, 0.175] Mpc^-1`.

The reruns retained the same central theory branch, `n_embed=10`, `NX=128`, `NSTEP=4096`, probe-amplitude rule and probe-phase rule as the completed dense construction.

## Numerical result

All seven preregistered gates pass:

- `C_G1_provenance_setup=True`
- `C_G2_41mode_CLASS_reference_consistency=True`
- `C_G3_rerun_solver_metric_health=True`
- `C_G4_rerun_phase_health=True`
- `C_G5_transfer_cardinality_invariance=True`
- `C_G6_power_cardinality_invariance=True`
- `C_G7_saturation_cardinality_invariance=True`

The 21-history and 41-history calculations agree exactly to the stored numerical precision:

- CLASS median relative difference: `0.0`
- CLASS maximum relative difference: `0.0`
- transfer global relative L2 difference: `0.0`
- maximum per-k transfer relative L2 difference: `0.0`
- power global relative L2 difference: `0.0`
- maximum per-k power relative L2 difference: `0.0`
- saturation global relative L2 difference: `0.0`
- maximum absolute saturation difference: `0.0`

The rerun phase diagnostics remain clean:

- global quadrature relative L2: `7.138133556494455e-10`
- maximum absolute imaginary component: `9.58720098407621e-10`
- maximum real-projection power change: `2.2247196239048402e-15`

The largest saturation residual among the six rerun nodes is

`7.777766761843295e-04`,

at `k/h=0.040 Mpc^-1`, well below the historical 2% saturated-closure gate.

## Scientific interpretation

The audit rules out corrected-CLASS history cardinality and associated 21-mode/41-mode state plumbing as the origin of the completed dense-radial structure.

In particular:

1. The low-k desaturation observed at the new H3 nodes `k/h=0.0325` and `0.0375 Mpc^-1` is not produced by the switch from 21 to 41 CLASS histories.
2. The non-smooth radial structure in the isolated finite-amplitude single-mode correction `DeltaT_W(k,z)` is likewise not a cardinality artifact.
3. The completed historical classifications remain unchanged:
   - `FULLJ_DENSE_RADIAL_WEYL_EXTENSION_FAIL`
   - `FULLJ_DENSE_RADIAL_CLASS_RESIDUAL_R2_FAIL`
4. This PASS validates cardinality invariance only. It does not license a bounded continuous Weyl-power representation, unrestricted evolving Weyl power, lensing, ACT, or an observational claim.

## Scope lock

- `DENSE_RADIAL_CARDINALITY_INVARIANCE_TESTED=True`
- `DENSE_RADIAL_CARDINALITY_ARTIFACT_EXCLUDED=True`
- `THREE_D_BOUNDED_CONTINUOUS_WEYL_POWER_LICENSED=False`
- `THREE_D_CONTINUOUS_WEYL_POWER_LICENSED=False`
- `EVOLVING_WEYL_POWER_LICENSED=False`
- `ACT_LIKELIHOOD_LICENSED=False`
- `OBSERVATIONAL_CLAIM_LICENSED=False`

## Consequence for the next milestone

The next continuum construction should not attempt to rescue the failed isolated finite-amplitude signed-transfer PCHIP representation by simple radial grid refinement. A better-defined target is a stochastic/power-level response in which the nonlinear constitutive state is set by a broadband Gaussian field and the response of a tagged radial mode is measured about that background. Any such construction requires a separate pre-data declaration and independent validation.
