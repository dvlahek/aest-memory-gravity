# GE19 Repair17 full canonical initial-manifold audit result freeze

## Status

Frozen first locked Repair17 local diagnostic execution.

Terminal classification:

`GE19_REPAIR17_FULL_CANONICAL_INITIAL_MANIFOLD_AUDIT_COMPLETE`.

Frozen routing:

`FINITE_WINDOW_ZERO_BOUNDARY_INADMISSIBLE_SOURCE_COMPATIBLE`.

This is a diagnostic PASS for existence of a constraint-compatible full canonical initial state. It does not certify a propagated Z20 trajectory.

## Frozen local outputs

Science JSON:

- bytes: `4914970`;
- SHA-256: `f81ad8ef52eb3a7ff4d4286670a62c830f17872459f43812b059447f85e14184`.

Inner FULL log:

- bytes: `4914970`;
- SHA-256: `f81ad8ef52eb3a7ff4d4286670a62c830f17872459f43812b059447f85e14184`.

Outer local runner log:

- bytes: `4922935`;
- SHA-256: `8cb82e530f104895bd2d22cd6ae1bb86c36d64dd80eb9418b3c6a6bbe7a5c1e0`.

The science JSON and inner FULL log are byte-identical.

Terminal marker:

`GE19_REPAIR17_DIAGNOSTIC_COMPLETE`.

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
  `768d5a2de7cd62059e7149a4765ab5a9663eef708fc29989c05192f607c5bf68`.

No H1 recomputation, no Z20 trajectory recomputation and no time integration were performed.

## Frozen thresholds

- full-y constraint relative residual <= `1e-8`;
- reconstructed independent lapse/shift backward error <= `1e-6`;
- eliminated algebraic residual <= `1e-8`;
- finite outputs.

## Global full-canonical result

Material cases:

`714 / 720`.

For the full canonical 2x8 constraint manifold:

- constraint relative residual max:
  `8.892022036425179e-13`;
- lapse backward error max:
  `2.6457320679749983e-16`;
- shift backward error max:
  `1.8699495216551784e-10`;
- eliminated algebraic residual max:
  `2.388467729664837e-16`;
- coefficient rank:
  `2` in every material case;
- augmented rank max:
  `2`;
- all outputs finite:
  true;
- pass count:
  `714 / 714`.

The local algebraic scaled condition number remains bounded:

`<= 3.1343173893632996`.

Therefore the frozen Repair14 quadratic source **does intersect the full canonical initial constraint manifold** in every material case.

## Restricted subspaces

### q-only, p=0

- constraint residual max:
  `1.7732165648834e-7`;
- eliminated algebraic residual max:
  `0.22760496547962522`;
- pass count:
  `0 / 714`.

Thus a coordinate-only correction is not an admissible replacement for the full canonical state.

### p-only, q=0

- constraint residual max:
  `1.9160597062254987e-10`;
- lapse backward error max:
  `1.2302409062294412e-13`;
- shift backward error max:
  `1.0092587566692186e-5`;
- eliminated algebraic residual max:
  `1.6529397640806795e-16`;
- pass count:
  `396 / 714`.

The p-only subspace is much closer to the full manifold than q-only, but it does not satisfy the frozen shift gate in all cases under the current minimum-norm numerical realization.

## Important interpretation

Repair17 resolves the ambiguity left by Repairs 15 and 16.

The frozen quadratic source is **not** shown to be intrinsically Noether-incompatible.

Instead, the imposed finite-window zero boundaries

- q=0, qdot=0;
- canonical y=(q,p)=0

are inadmissible for a nonzero forced source at z=1.5.

A constraint-compatible full canonical initial state exists in every material case.

Therefore the Repair14 shift failure must not be interpreted as a source-identity failure.

## Boundary-selection issue that remains

The full 2x8 system has rank 2, hence a six-dimensional canonical null freedom remains.

Repair17 uses a row-scaled minimum-norm full-y representative only as an existence witness.

Its Euclidean norm is not a frozen physical boundary prescription.

The full-y solution L2 norm reaches

`1908119.6665826605`

in the strongest material case, while q-only and p-only subspace behavior shows strong coordinate-scaling sensitivity.

Therefore a new H3 propagation must **not** simply inject the Repair17 Euclidean minimum-norm full-y state as a physical initial condition without a separately preregistered boundary-selection rule.

## Next licensed question

Construct and certify a physically and numerically well-defined constraint-compatible finite-window boundary.

The preferred next diagnostic should preserve zero field coordinates q=0 if possible and solve for the minimal canonical momentum correction with a frozen scaling/metric, because Repair17 shows that the p-only manifold is already algebraically exact and close to the shift gate.

Alternative boundary rules must be justified before execution and cannot be selected using a later H3 propagation outcome.

Only after a boundary rule is frozen and independently closes all initial constraints may a new H3/Z20 propagation be preregistered.

## Stop rule

No Repair14 relabeling.

No immediate H3 rerun from the unconstrained Euclidean full-y minimum-norm witness.

No q20 and no H4/Z21 yet.

No threshold relaxation.

## Claim boundary

Repair17 certifies existence of a full canonical initial constraint manifold for the frozen H3 source. It does not certify a unique physical initial state, a propagated Z20 solution, nonlinear memory propagation, or any observable/data claim.
