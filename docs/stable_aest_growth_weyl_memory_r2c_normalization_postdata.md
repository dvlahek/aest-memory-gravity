# Stable AeST growth–Weyl memory R2c — post-data checkpoint

Date: 2026-09-14
Branch: `fullj-evolving-weyl-bridge`

## Frozen parent

R2c was preregistered in commit

`6459fa6ceab26dfd56c4ba558613f3d1a4bd43c9`

after the completed R2b post-data checkpoint

`35913eb794d7427431e5f5050f05a71ecfbccbbe`.

R2b remains formally

`STABLE_AEST_GROWTH_WEYL_MEMORY_R2B_COMMON_MODE_BOUND_CERTIFIED`

and is not reclassified by R2c.

## Technical pre-result repair

The first R2c attempt stopped before any worker completed because the driver used the nonexistent CLASS parameter name `perturb_sampling_stepsize`. The correct CLASS name is `perturbations_sampling_stepsize`. This was repaired without changing the preregistered sampling values 0.02 and 0.005, physical model, gates, or thresholds. The completed run therefore evaluates the original R2c design.

## Formal R2c result

The completed run returned

`STABLE_AEST_GROWTH_WEYL_MEMORY_R2C_GLOBAL_NORMALIZATION_MISMATCH_CERTIFIED`

with exit code 0.

Gates:

- G1 provenance and parent lock: PASS
- G2 source-grid densification: PASS
- G3 patch neutrality: PASS
- G4 dense amplifier consistency: PASS
- G5 source-grid convergence: PASS
- G6 absolute normalization: FAIL
- G7 coherent normalization mismatch: PASS

The source-grid target-k sample count increased from 123 at sampling 0.02 to 489 at sampling 0.005 for all three anchors. Dense-grid convergence was strict at all three anchors.

Primary dense-grid normalization factors were:

- k_h=0.09875: A_G=0.50267199, A_L=0.50337030
- k_h=0.16125: A_G=0.50372528, A_L=0.50378900
- k_h=0.19500: A_G=0.50637210, A_L=0.50157345

Thus all six amplitude factors lie in [0.50157345,0.50637210]. The dense variational vectors retain essentially the same redshift shape as the frozen finite-eta R2 reference, but remain approximately a factor 1.98--1.99 larger in norm.

Patch-neutrality relL2 values remain at approximately 1.52e-7 for CLASS d_m and 2.15e-7 for phi+psi, far below the preregistered 2e-5 bound.

## Source-grid densification interpretation

R2c rules out sparse source-grid density as the explanation of the global factor-two normalization mismatch. The 0.02 and 0.005 source-grid variational tangents agree at the 1e-3 level or better in norm/shape while the absolute factor remains near 0.5.

However, densification did not extend the temporal coverage of the forcing table. Both source-grid traces cover the same interval, approximately

`tau = 5174.717262978337 ... 14151.626616283856`.

Only the number of samples inside this interval changed: 123 -> 489.

The R2b/R2c trace hook is located in `perturbations_sources()`. The physical finite-eta memory closure is evaluated inside `perturbations_derivs()` over the perturbation integration history. Therefore R2c certifies a global normalization mismatch for the source-grid frozen-forcing construction, but does not yet prove an incorrect analytic factor in the physical closure.

A leading post-data hypothesis is missing early-history forcing before the first source-grid time. Such an omitted contribution can preserve the late-time redshift shape while changing the absolute normalization if the earlier response partially cancels the later response. This hypothesis is not an R2c result and must be tested prospectively.

## Licensed interpretation

R2c licenses the statement that source-grid densification does not remove the coherent normalization mismatch. It does not license use of the source-grid variational G/L vectors as absolutely normalized partial_eta tangents.

R2c does not reclassify R2b, does not certify a positive growth–Weyl separation, and does not license observational or fundamental-new-physics claims.

Because temporal coverage remains incomplete by construction, the R2b one-percent common-mode result should be retained as its formal preregistered result, but its interpretation as the full-history physical eta tangent should not be strengthened until a full-history RHS variational audit is completed.

## Next step

Run a separately preregistered R2d full-history RHS forcing audit. Record the raw eta derivative forcing directly inside the physical memory block in `perturbations_derivs()` at eta=0, covering the complete perturbation integration history rather than the CLASS source grid. Re-run signed variational probes from that full-history forcing table and compare their absolute G/L normalization and common-mode residual with the frozen finite-eta R2 reference.
