# GE19 Repair16 canonical-zero initial-state audit lock

## Status

**DIAGNOSTIC IMPLEMENTATION LOCKED BEFORE REPAIR16 LOCAL RESULT**

Repair15 remains frozen with route

`INITIAL_SOURCE_INCOMPATIBILITY`.

Repair14 remains a historical H3/Z20 FAIL.

Repair16 is diagnostic only.

## Parent Repair15 freeze

Commit:

`e2d642eb528fab10aa4d3ba0a2afc94b2dcacbaf`

File:

`docs/ge19_repair15_initial_shift_compatibility_result_freeze.md`

Blob:

`fb79a6fcb2e8cc172edcf3b1f4cdc25e643da8ca`

Frozen Repair15 JSON:

- SHA-256 `a8c86b6056a3d6ab2f6f443850bef34881452b4a11b32bb6a66e2ac7920f1e50`;
- bytes `3507539`.

## Repair16 preregistration

Commit:

`eceadb445335212621aa6563118882f6b6a8d8ab`

File:

`ge19/repair16_predata_canonical_zero_initial_state_audit.json`

Blob:

`46dfc2004cfd4f8d3ba22f67c48518dc2af95269`

## Repair16 implementation

Commit:

`d86abd3452827a491a1acc627873ff4b62752693`

File:

`ge19/repair16_canonical_zero_initial_state_audit.py`

Blob:

`232bae522de42225db0e95ce7ad685c6a5251e3d`

## Canonical-zero definition

The frozen canonical state is

`y=(S,u,phi,T,pS,pu,pphi,pT)`.

Repair16 sets

`y0=0`

at z=1.5.

It does **not** separately set qdot=0.

Instead the frozen Noether-regularized algebraic map determines

- N20;
- delta_varrho20;
- S20dot;
- u20dot;
- phi20dot;
- T20dot

from the same frozen Repair14 quadratic source.

By construction the eliminated rows are

- pS;
- pu;
- pphi;
- pT;
- dust density;
- anisotropy.

Independent monitors are

- lapse;
- shift.

## Frozen diagnostic thresholds

- algebraic relative residual <= `1e-8`;
- independent lapse backward error <= `1e-6`;
- independent shift backward error <= `1e-6`;
- all outputs finite.

Material-source floor:

`1e-12`

relative to the global initial-source norm maximum.

## Frozen routing

Repair16 may return only:

- `CANONICAL_ZERO_INITIAL_STATE_CLOSES_CONSTRAINTS`;
- `QUADRATIC_SOURCE_NOETHER_INCOMPATIBILITY_REMAINS`;
- `IMPLEMENTATION_FAIL`.

## Executable prelock audit

Workflow:

`.github/workflows/ge19-repair16-prelock-audit.yml`

Blob:

`af7235396e3a6c82373497fd449ab0e1610551a8`

GitHub Actions run:

`35607215229`

Job:

`106357145652`

Conclusion:

`success`

Terminal marker:

`GE19_REPAIR16_PRELOCK_AUDIT_PASS`.

Synthetic backward-error controls:

- compatible case: `0.0`;
- intentionally incompatible case: `0.2`.

The audit statically verifies that Repair16 does not invoke:

- `solve_case_canonical`;
- `_radau2_integrate_canonical`;
- `solve_reduced_h1_case_canonical`.

## Stop rule

Repair16 does not modify or rerun Repair14 Z20.

If canonical-zero closes lapse and shift, a separately preregistered Repair17 may rerun H3 with canonical y0=0.

If canonical-zero still fails, the next step is a direct quadratic Noether/source identity audit before any new H3 solve.

No threshold is relaxed.

## Claim boundary

Repair16 can distinguish an initial-variable convention error from a genuine quadratic-source/Noether incompatibility.

It does not certify Z20 or nonlinear memory propagation.
