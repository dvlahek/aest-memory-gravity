# GE19 Repair06 canonical/Noether-regularized implementation lock

## Status

**IMPLEMENTATION LOCKED BEFORE REPAIR06 SCIENCE EXECUTION**

Historical Repair05 remains:

`GE19_REPAIR05_WINDOW_RETARDED_REDUCED_H3_Z20_PARTICULAR_FAIL`.

It is not relabeled.

## Frozen chain

Repair05 result freeze:

- commit `9a23f885cb96005a3a0199abe545f8283ba44027`
- `docs/ge19_repair05_reduced_h1_result_freeze.md`
- blob `51a8ade089fd3bc1521f72dd6415fd21aa179e45`

Repair06 preregistration:

- commit `0093500d8be6e7979544222157ce0dd268a8292d`
- `ge19/repair06_predata_canonical_momentum_time_march.json`
- blob `8f2764ef1b1ffc1517b35973f5badc50a43cd813`

Noether-regularized DAE amendment:

- commit `8c9e4fac8b3fe0dd9326ff0b17615f8a346c26c3`
- `ge19/repair06_predata_amendment01_noether_regularized_dae_partition.json`
- blob `458fd5958f2915e49dda36063ccaaa468d4b6e7c`

Full stable-Z polynomial-normalization amendment:

- commit `f0283e875258b68c071888062d9519a81d968f24`
- `ge19/repair06_predata_amendment02_full_stable_Z_polynomial_normalization.json`
- blob `cf4c2e03029ce7cfc493207592fc1122e33c4ecd`

Final audited Repair06 science implementation:

- implementation commit `bee22d28ec5dba8f19ad2da29096bc6bfea7d288`
- `ge19/repair06_window_retarded_reduced_h3_z20_particular.py`
- blob `98690421ed57f266745348bf56e2664d6fb9047a`

Executable prelock audit workflow:

- audit commit `37f0206de022a440f0f69a3fa57c9e58223008f1`
- `.github/workflows/ge19-repair06-prelock-audit.yml`
- blob `4d3dcc68ba03c4de8b5db18830ad542ca01db3f6`

The later exploratory symbolic-Jacobian diagnostic was reverted. Current pre-lock HEAD
`0e807a957e2f75db7bf8167e5c7e5529de292c2b`
has **zero file differences** relative to the successful audited tree
`37f0206de022a440f0f69a3fa57c9e58223008f1`.
Therefore the locked script/workflow blobs are exactly the already-audited blobs above.

## Successful executable audit

GitHub Actions run:

`35537171978`

Job:

`106148167499`

Conclusion:

`success`

Terminal marker:

`GE19_REPAIR06_PRELOCK_AUDIT_PASS`

Key frozen audit values:

- old algebraic-partition Noether null scaled L2 max:
  `5.2365940175405e-18`;
- augmented Noether-regularized algebraic scaled condition-2 max:
  `2.6187422468361112`;
- initial algebraic scaled residual:
  `4.108326725150325e-17`;
- local algebraic scaled residual max:
  `8.202271871932403e-21`;
- local old-partition Noether-null scaled L2:
  `9.495937976511657e-21`;
- canonical affine scaled relative error:
  `1.470362104949821e-17`;
- isotropic momentum identity error:
  `0.0`;
- Radau zero-state block scaled residual max:
  `0.0`;
- Radau scaled condition-2 max:
  `291.08556234271055`;
- local algebraic scaled condition-2 max:
  `2.6187422468361112`;
- stable GE06 benign c1 equivalence:
  `8.242856821646169e-16`;
- stable GE06 benign c2 equivalence:
  `7.939971560854226e-16`;
- stable GE06 physical c1/c2 probes: all finite.

## Structural repair

The old local algebraic row set

`(pS, pu, pphi, pT, lapse, dust_density)`

has an exact Noether/gauge null direction and is structurally rank-deficient.

Repair06 uses the preregistered regularized row set

`(pS, pu, pphi, pT, dust_density, anisotropy)`.

Lapse is not removed from the equations. It is evaluated independently after reconstruction and contributes to the unchanged Stage-A/Stage-B residual control. Shift remains an independent constraint monitor. Anisotropy is the gauge-closing algebraic row and is also independently reported.

The exact augmented determinant is nonzero on the frozen solved domain for k>0.

## Stable-Z normalization

The corrected physical coordinate remains

`Z_action=(Q_action-Q0)/Z0`.

Repair06 normalizes the complete c1/c2 stable-Z polynomial prefactors before numerical lambdification, while retaining the same exact symbolic functions and canonical `exp(Z^2)` branch.

This removes the float64 cancellation that had incorrectly driven the pphi principal row to zero.

No frozen action coefficient or physical parameter changes.

## Frozen integration realization

The global centered-collocation solve is replaced by the preregistered canonical-momentum initial-value realization.

Dynamic coordinates:

`(S,u,phi,T)`.

Canonical momenta:

`(pS,pu,pphi,pT)`.

Time stepping:

two-stage, order-3, L-stable Radau-IIA on the same Nt=64 primary and Nt=32 control output grids.

The second Radau stage uses the exact endpoint grid node `x[i+1]`, which is algebraically c2=1 and prevents floating-point interpolation-domain overshoot.

## Unchanged Stage-A science gates

- linear-system residual <= `1e-8`;
- shift constraint <= `1e-6`;
- anisotropy constraint <= `1e-6`;
- primary64/control32 state relative L2 <= `5e-3`;
- initial dynamic match abs-or-rel <= `1e-10`;
- all outputs finite.

If Stage A fails, H3/Z20 is not constructed.

## Unchanged Stage-B science gates

- Nx1024/Nx2048 source low-mode relative L2 <= `5e-4`;
- linear-system residual <= `1e-8`;
- shift constraint <= `1e-6`;
- anisotropy constraint <= `1e-6`;
- primary64/control32 state relative L2 <= `5e-3`;
- all beta0/C cases complete;
- all outputs finite.

## Frozen local parents

The runner consumes only:

- `results/ge15_R1_dense_accepted_step_trace.dat`
- `results/ge15_cancellation_free_s_state_precision_closure.json`
- `results/ge15_cancellation_free_s_state_precision_closure.npz`
- `results/ge18_repair01_on_shell_matched_dust_first_order_bridge.json`
- `results/ge18_repair01_on_shell_matched_dust_first_order_bridge.npz`

No CLASS build and no network access are permitted in the science runner.

## Claim boundary

A Repair06 PASS can certify only the frozen low-mode, window-retarded,
reduced-matter H3 directional particular coefficient in the formal epsilon->0 hierarchy.

It does not certify homogeneous/primordial Z20, full-species second order,
finite eta, finite physical-amplitude nonlinear evolution, collapse/halos,
lensing, or observational detection.

Terminal classifications:

- `GE19_REPAIR06_WINDOW_RETARDED_REDUCED_H3_Z20_PARTICULAR_PASS`
- `GE19_REPAIR06_WINDOW_RETARDED_REDUCED_H3_Z20_PARTICULAR_FAIL`
- `GE19_REPAIR06_WINDOW_RETARDED_REDUCED_H3_Z20_PARTICULAR_IMPLEMENTATION_FAIL`
