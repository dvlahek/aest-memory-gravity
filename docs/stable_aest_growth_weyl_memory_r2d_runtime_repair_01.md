# Stable AeST growth–Weyl memory R2d — runtime repair 01

Date: 2026-09-14
Branch: `fullj-evolving-weyl-bridge`

## Status before repair

The first R2d attempt passed source construction and reached the first target anchor. The direct full-history RHS trace was generated and its overlap with the completed R2c dense source-grid forcing passed at `k_h=0.09875`:

- `E_force = 9.635481681272698e-06`
- `C_force = 0.9999999999622112`
- overlap points = 489.

The run then failed before any signed variational cell was completed. The historical external-force helper queried another CLASS transfer-grid mode (`k=0.2021851436888257 1/Mpc`) while the R2d force table contained only the target physical mode (`k≈0.0664908081096305 1/Mpc`). The helper correctly stopped with `AEST_TANGENT_FORCE_K_MISS`.

Therefore this attempt produced no R2d science classification. In particular, it is not a failure of the R2d normalization, common-mode, or separation gates.

## Cause

R2d initially used the preregistration allowance that the diagnostic full-history hook *may* be restricted to the target k. This is sufficient for target-k trace/overlap diagnostics but insufficient for the existing signed external-force mechanism when CLASS is run with `mTk,vTk`: CLASS evolves a full transfer-k grid and the external forcing is queried at every evolved k.

Using `AEST_TANGENT_ALLOW_K_MISS` or setting non-target modes to zero would change the response used for transfer interpolation and is therefore not an acceptable repair.

## Locked repair

The repair changes only diagnostic force transport:

1. Trace the exact in-block full-history forcing
   `F_eta=-a Q B_chi,raw/(2 K_B)`
   for the full CLASS perturbation k grid during the eta=0 trace run.
2. Store the full `(k,tau,F_eta)` table and use it unchanged with the existing external-force helper for the signed lambda probes.
3. Continue to evaluate the preregistered full-history coverage and R2c-overlap metrics only on the locked target-k block for each anchor.
4. Keep the physical memory closure, stable `chi=Q*s`, finite-memory parameters, lambda values, finite-eta reference, all thresholds, and classification priority unchanged.

The R2d preregistration explicitly states that the trace hook *may* be restricted to the target k; target restriction is therefore optional, not a frozen requirement. Expanding diagnostic trace coverage to the full CLASS k grid is a runtime compatibility repair required by the already frozen signed-probe definition.

No previous R1/R1b/R2/R2a/R2b/R2c classification is changed.