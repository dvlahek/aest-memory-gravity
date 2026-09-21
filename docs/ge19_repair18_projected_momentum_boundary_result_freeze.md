# GE19 Repair18 zero-coordinate constraint-projected momentum boundary result freeze

## Status

Frozen first locked Repair18 local diagnostic execution.

Terminal classification:

`GE19_REPAIR18_ZERO_COORDINATE_CONSTRAINT_PROJECTED_MOMENTUM_BOUNDARY_AUDIT_COMPLETE`.

Frozen routing:

`ZERO_COORDINATE_CONSTRAINT_PROJECTED_MOMENTUM_BOUNDARY_CERTIFIED`.

Repair18 certifies a reproducible finite-window H3 initial boundary. It does not itself propagate or certify Z20.

## Frozen local outputs

Science JSON:

- bytes: `3265739`;
- SHA-256: `d5603138c2f488413686323d1241613f6ef707b586116aa7fe865ae25ceb0edc`.

Inner FULL log:

- bytes: `3265739`;
- SHA-256: `d5603138c2f488413686323d1241613f6ef707b586116aa7fe865ae25ceb0edc`.

Outer local runner log:

- bytes: `3272825`;
- SHA-256: `f50fe69000c31ddbb57228ae5dc15c2fc6c641e4adb08e30fda6ad3e0677f2c5`.

Terminal marker:

`GE19_REPAIR18_DIAGNOSTIC_COMPLETE`.

## Provenance

Frozen parent hashes reproduce exactly:

- Repair13 JSON:
  `ae3cc790ecffbd5498b5852273c72ae578d4615de29bbb616673c05cdb3e74b7`;
- Repair13 NPZ:
  `011c0ae54fd21d70c0e2c695ce62e7b74a3c5529a07c9023c882a447d5b40ca3`;
- Repair14 JSON:
  `741da95a0aaffa31e27f2b05d42b8a7f011574013de8639812e453d7b130fe57`;
- Repair15 JSON:
  `a8c86b6056a3d6ab2f6f443850bef34881452b4a11b32bb6a66e2ac7920f1e50`;
- Repair16 JSON:
  `768d5a2de7cd62059e7149a4765ab5a9663eef708fc29989c05192f607c5bf68`;
- Repair17 JSON:
  `f81ad8ef52eb3a7ff4d4286670a62c830f17872459f43812b059447f85e14184`.

No H1 recomputation, no Z20 trajectory recomputation and no time integration were performed.

## Frozen boundary rule

At z=1.5:

`q0=(S20,u20,phi20,T20)=0`

exactly.

Only canonical momenta

`p0=(pS20,pu20,pphi20,pT20)`

are determined from the independent lapse and shift constraints after the same frozen algebraic reconstruction used in Repair17.

Numerical rule:

- row equilibration;
- column equilibration;
- `scipy.linalg.lstsq(..., lapack_driver="gelsd")`;
- minimum Euclidean norm in doubly equilibrated momentum coordinates;
- exactly four iterative-refinement sweeps;
- no case-dependent variable selection or post-result solver switch.

## Frozen gates and result

Thresholds:

- scaled constraint residual <= `1e-8`;
- lapse backward error <= `1e-6`;
- shift backward error <= `1e-6`;
- eliminated algebraic residual <= `1e-8`;
- rank exactly 2;
- finite outputs.

Material cases:

`714 / 714 PASS`.

Global maxima:

- scaled constraint residual:
  `2.482534153108436e-16`;
- lapse backward error:
  `2.639993079262776e-16`;
- shift backward error:
  `3.2234628832120975e-16`;
- eliminated algebraic residual:
  `2.457039030496151e-16`;
- anisotropy backward error:
  `6.394777335818628e-16`;
- rank min/max:
  `2 / 2`;
- augmented rank max:
  `2`;
- all material outputs finite:
  true.

The scaled solution norm max is

`0.577350276667655`.

Raw coordinate norms are strongly scale-sensitive:

- momentum L2 max:
  `6382956895.805921`;
- determined qdot L2 max:
  `890954381.6463909`.

These large raw norms are therefore monitored descriptively and are not reinterpreted as a physical-amplitude statement.

## Primary/control reproducibility

Although not printed in the runner summary, the preregistered primary/control reproducibility requirement was checked directly from the frozen JSON.

Across all 360 matched (C,beta,m) primary/control pairs:

- projected p0 relative L2 difference max:
  `0.0`;
- determined qdot0 relative L2 difference max:
  `6.468697709110601e-15`.

Thus the certified boundary is time-grid reproducible at the initial surface.

## Interpretation

Repair18 converts the Repair17 existence result into one unique reproducible finite-window boundary prescription.

It preserves zero second-order coordinates at the window entrance while using the constraints to supply the canonical momentum content required by the already nonzero quadratic forcing source.

This is a window-local particular-solution convention. It is not a primordial second-order initial condition and does not claim that omitted homogeneous prehistory vanishes physically.

## Next licensed step

A separately preregistered Repair19 may rerun the H3/Z20 propagation using this exact Repair18 boundary.

Repair19 must keep unchanged:

- Repair13 background and Z10 parent;
- Repair14 quadratic source construction;
- Lambda c2;
- C envelope;
- beta0 values;
- m=1..40;
- Nx=1024/2048 source convergence control;
- Nt=64/32 propagation control;
- original Stage-B residual, shift, anisotropy and finite-output gates.

Repair19 must add an initial-boundary reproduction gate against this frozen Repair18 prescription.

## Stop rule

No q20 and no H4/Z21 until a Repair19 H3/Z20 propagation passes all frozen Stage-B gates.

No threshold relaxation.

## Claim boundary

Repair18 certifies the finite-window boundary prescription only. It does not certify propagated Z20, nonlinear memory, observables or data.
