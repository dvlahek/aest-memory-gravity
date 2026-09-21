# GE19 Repair18 zero-coordinate constraint-projected momentum boundary lock

## Status

**DIAGNOSTIC IMPLEMENTATION LOCKED BEFORE REPAIR18 LOCAL RESULT**

Repair17 remains frozen with route

`FINITE_WINDOW_ZERO_BOUNDARY_INADMISSIBLE_SOURCE_COMPATIBLE`.

Repair18 is a boundary-certification diagnostic only. It performs no H3/Z20 time propagation.

## Parent Repair17 freeze

Commit:

`1ce72e3c3a732be59c1e390c8ef67859348b76c6`

File:

`docs/ge19_repair17_canonical_initial_manifold_result_freeze.md`

Blob:

`37c1f93e1fa52ce9963707fe2be3bd5d076005fa`

Frozen Repair17 JSON:

- SHA-256 `f81ad8ef52eb3a7ff4d4286670a62c830f17872459f43812b059447f85e14184`;
- bytes `4914970`.

## Repair18 preregistration

Commit:

`1e15c4f91827bdd068c3a0e19c55232345141e4d`

File:

`ge19/repair18_predata_zero_coordinate_constraint_projected_momentum_boundary.json`

Blob:

`884b26b4c65c3fc3c42defa9e7fdd37f9ca43850`

## Repair18 implementation

Commit:

`b8a8a0b8fe3bad5a4d23b653c335fd0297302fcc`

File:

`ge19/repair18_zero_coordinate_constraint_projected_momentum_boundary.py`

Blob:

`c7b3a5c689bd78a65a8150c26e1fbfae108cb580`

## Frozen boundary definition

At z=1.5:

`q0=(S20,u20,phi20,T20)=0`

exactly.

Only canonical momenta

`p0=(pS20,pu20,pphi20,pT20)`

are determined from the independent lapse and shift constraints after the same frozen algebraic reconstruction used in Repair17.

This preserves the original window-local zero-coordinate convention while removing the invalid zero-velocity/zero-momentum assumption.

## Frozen solver rule

For the complex 2x4 momentum system:

1. row-scale each constraint by
   `max(max(abs(A_row)), abs(b_row), tiny)`;
2. column-scale the row-scaled matrix by each momentum column's maximum absolute coefficient;
3. solve the doubly equilibrated system with
   `scipy.linalg.lstsq(..., lapack_driver="gelsd")`;
4. choose the minimum Euclidean norm in the doubly equilibrated momentum coordinates;
5. apply exactly **four** iterative-refinement correction sweeps;
6. each correction uses the same frozen row/column scales and the same GELSD pseudoinverse rule;
7. no case-dependent momentum-column selection and no post-result solver switch.

## Frozen gates

Material cases must satisfy:

- scaled lapse+shift relative residual <= `1e-8`;
- independent lapse backward error <= `1e-6`;
- independent shift backward error <= `1e-6`;
- eliminated p/density/anisotropy algebraic residual <= `1e-8`;
- rank exactly 2;
- all outputs finite.

No Stage-B propagation threshold is changed.

## Executable prelock audit

Workflow:

`.github/workflows/ge19-repair18-prelock-audit.yml`

Blob:

`9ec8bac242cd48fa2fb83cb768ee59b1d632dbf9`

Run:

`35612842980`

Job:

`106376026297`

Conclusion:

`success`

Terminal marker:

`GE19_REPAIR18_PRELOCK_AUDIT_PASS`.

Synthetic strongly anisotropic compatible 2x4 control:

- scaled residual `2.1683880231419792e-16`;
- rank `2`.

Synthetic incompatible control:

- scaled residual `0.19611613513818404`;
- coefficient rank `1`;
- augmented rank `2`.

The prelock statically verifies that Repair18 does not invoke:

- `solve_case_canonical`;
- `_radau2_integrate_canonical`;
- `solve_reduced_h1_case_canonical`.

## Frozen routing

Only:

- `ZERO_COORDINATE_CONSTRAINT_PROJECTED_MOMENTUM_BOUNDARY_CERTIFIED`;
- `ZERO_COORDINATE_BOUNDARY_NUMERICALLY_UNRESOLVED`;
- `IMPLEMENTATION_FAIL`.

## Stop rule

Repair18 performs no H3 propagation.

If the boundary is certified, a separately preregistered Repair19 may rerun H3/Z20 with this exact boundary and the original Stage-B propagation gates unchanged.

No q20 or H4/Z21 construction is licensed by Repair18 alone.

No threshold is relaxed.

## Claim boundary

Repair18 may certify one reproducible finite-window initial boundary rule. It does not certify Z20 propagation, nonlinear memory, or observables.
