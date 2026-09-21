# GE19 Repair17 full canonical initial-manifold audit lock

## Status

**DIAGNOSTIC IMPLEMENTATION LOCKED BEFORE REPAIR17 LOCAL RESULT**

Repair16 remains frozen with route

`QUADRATIC_SOURCE_NOETHER_INCOMPATIBILITY_REMAINS`.

That route records failure of canonical y0=0. It is not yet interpreted as proof of a source-level identity failure.

Repair17 is diagnostic only.

## Parent Repair16 freeze

Commit:

`d5a619495f0f8fb2da53528b46476a15c1a32922`

File:

`docs/ge19_repair16_canonical_zero_initial_result_freeze.md`

Blob:

`f5f793e41d81e450daa849786b7da7db4a2def5e`

Frozen Repair16 JSON:

- SHA-256 `768d5a2de7cd62059e7149a4765ab5a9663eef708fc29989c05192f607c5bf68`;
- bytes `1366591`.

## Repair17 preregistration

Commit:

`7d5664743b2bda32fcd1a444ece37cdc14a3d96d`

File:

`ge19/repair17_predata_full_canonical_initial_manifold_audit.json`

Blob:

`793ae9eebb100f71b425403f14d743ff2cbde5d5`

## Repair17 implementation

Commit:

`753015f7a377ca8bfe541cace99fb239b49a7654`

File:

`ge19/repair17_full_canonical_initial_manifold_audit.py`

Blob:

`531939bc5859a66c80b9f59755d6f10a0dae4ca7`

## Frozen question

At z=1.5, using the exact same frozen Repair14 source and Repair13 reduced background, define the canonical state

`y=(S,u,phi,T,pS,pu,pphi,pT)`.

The frozen algebraic reconstruction is

`w(y)=WY y + WR source`.

After this reconstruction, Repair17 forms the two independent affine constraints:

- lapse;
- shift.

It tests three subspaces:

1. full canonical y, 2x8;
2. q-only, 2x4 with p=0;
3. p-only, 2x4 with q=0.

For every candidate it independently reconstructs:

- eliminated p/density/anisotropy equations;
- lapse backward error;
- shift backward error.

## Frozen thresholds

- full-y row-scaled constraint relative residual <= `1e-8`;
- independent lapse/shift backward error <= `1e-6`;
- eliminated algebraic relative residual <= `1e-8`;
- finite outputs.

Material-source floor remains `1e-12` relative to the global initial-source norm maximum.

## Frozen routing

Only:

- `FINITE_WINDOW_ZERO_BOUNDARY_INADMISSIBLE_SOURCE_COMPATIBLE`;
- `QUADRATIC_SOURCE_INITIAL_NOETHER_INCOMPATIBILITY_CONFIRMED`;
- `IMPLEMENTATION_FAIL`.

If full-y is compatible, Repair15/16 are interpreted as failures of the imposed zero boundary, not proof that the quadratic source is inconsistent.

If full-y is incompatible, no canonical initial state can satisfy the independent constraints and a sector-by-sector source identity audit is licensed.

## Executable prelock audit

Workflow:

`.github/workflows/ge19-repair17-prelock-audit.yml`

Blob:

`b260d33d803d5359ca26044c21f3dad7e6930b6e`

Run:

`35609640571`

Job:

`106365242539`

Conclusion:

`success`

Terminal marker:

`GE19_REPAIR17_PRELOCK_AUDIT_PASS`.

Synthetic controls:

- compatible full-y residual: `2.220446049250313e-16`;
- intentionally incompatible residual: `0.7071067811865475`.

The prelock statically verifies that Repair17 does not invoke:

- `solve_case_canonical`;
- `_radau2_integrate_canonical`;
- `solve_reduced_h1_case_canonical`.

## Stop rule

Repair17 performs no propagation.

No Repair14 rerun, q20, H4 or Z21 is licensed by Repair17 alone.

Any propagation test after Repair17 requires a new preregistration.

No threshold is relaxed.

## Claim boundary

Repair17 distinguishes source incompatibility at the initial surface from an inadmissible finite-window zero-state boundary. It does not certify Z20 or nonlinear memory propagation.
