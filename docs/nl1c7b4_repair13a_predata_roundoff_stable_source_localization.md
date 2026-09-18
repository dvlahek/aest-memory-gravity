# NL1C7B4 Repair13a — roundoff-stable Hamiltonian source-localization certification

## Status

Locked before implementation and before any Repair13a execution.

Repair13a is licensed only by the frozen Repair13 harness failure at commit `f3d25b37eddd322b4e1ed147c99af9b2dec0227f`.

Repair13a is a **harness-only numerical certification repair**. It may not modify or recompute the scientific definitions of any source, state variable, perturbation path, source-order label, slope, projection fraction, dominant-source rule, or historical B4 gate.

## Frozen Repair13 result

The exact local Repair13 JSON is frozen by SHA-256:

`ef6791edd595a2bd8b44e52a703915385a1e2c4d98345ff4cc509a5d22a61a9b`.

It must have terminal class

`NL1C7B4_REPAIR13_IMPLEMENTATION_FAIL`

with:

- G1 PASS;
- G2 PASS;
- G3 FAIL;
- G4 FAIL;
- G5 FAIL;
- G6 PASS;
- G7 PASS;
- G8 PASS.

The following Repair13 diagnostic values are frozen and must remain unchanged:

- 54 cases;
- `dominant_A_L2_source_counts = {"AeST_E2":54}`;
- `AeST_E2: first_order_like` in 54/54 cases;
- `AeST_EX: first_order_like` in 54/54 cases;
- `AeST_X2: second_order_like` in 54/54 cases;
- historical B4 class remains `NL1C7B4_REPAIR09_REPAIR08_RAW_CONSTRAINT_FAIL`.

Repair13a does not relabel the historical Repair13 run.

## Numerical diagnosis

Repair13 G3 compared

`fl(sum_i fl(C_i(lambda)-C_i(0)))`

with

`fl(fl(sum_i C_i(lambda))-fl(sum_i C_i(0)))`

using a fixed relative tolerance normalized by the small perturbative residual.

These expressions are algebraically identical but use different floating-point association. Because the B3 background source terms are much larger than the perturbative increment, the relative error with respect to the small increment is cancellation-conditioned.

The same association effect propagates into G4 and G5.

Repair13a replaces only those three numerical closure gates by explicit IEEE-754 binary64 forward-error bounds.

## Frozen arithmetic model

Use IEEE-754 binary64 unit roundoff

`u = 2^-53`.

Define

`gamma_n = n u / (1 - n u)`.

No empirical tolerance inferred from the failed Repair13 values is allowed.

### R13a_G3 — roundoff-aware source-sum closure

At every frozen case, positive lambda, and non-center radial point, define

`S = sum_i (|C_i(lambda)| + |C_i(0)|)`.

Let

`d3 = |sum_i [C_i(lambda)-C_i(0)] - ([sum_i C_i(lambda)]-[sum_i C_i(0)])|`

using the same float64 paths as Repair13.

Require pointwise

`d3 <= gamma_64 S`.

The operation budget 64 is a fixed conservative upper bound for the two 11-term summations, 11 pairwise subtractions, and final subtraction, including association differences.

The old Repair13 normalized closure error and its failed `1e-12` gate must still be reported.

### R13a_G4 — roundoff-aware first-order coefficient closure

For positive lambda, define the same frozen

`A_i = [C_i(lambda)-C_i(0)]/lambda`

and

`A_tot = ([sum_i C_i(lambda)]-[sum_i C_i(0)])/lambda`.

Let

`S_A = S/lambda`.

Require pointwise

`|sum_i A_i - A_tot| <= gamma_96 S_A`.

The operation budget 96 includes the G3 arithmetic plus the coefficient divisions and their association.

The old Repair13 normalized coefficient-closure error remains reported and historically failed.

### R13a_G5 — projection identity with coefficient-closure correction

Repair13 projection fractions remain exactly

`P_i = <A_i,A_tot>/||A_tot||^2`.

They are not redefined.

Let

`A_sum = sum_i A_i`,

`D = <A_tot,A_tot>`,

and define the algebraically correct expected projection sum for the actually represented floating-point coefficient profiles:

`P_expected = 1 + <A_sum-A_tot,A_tot>/D`.

Thus coefficient-closure roundoff is not falsely interpreted as a projection-definition failure.

Let

`P_sum` be the compensated scalar sum of the frozen `P_i` values.

For a radial vector of length `m`, define

`T = sum_i sum_j |A_i[j] A_tot[j]| + sum_j |A_tot[j]^2|`.

Require

`|P_sum-P_expected| <= gamma_(32 m + 128) T / D`.

The operation budget covers 11 source dot products, one denominator dot product, scalar accumulation, and multiplication/addition roundoff.

The old Repair13 `|sum_i P_i-1|` value and failed `1e-12` gate remain reported.

## Frozen inputs

Require the exact frozen hashes for Repair08, Repair10, Repair11, Repair12, and Repair13, together with the frozen dense trace and coverage.

No official state is written.

## Gates

### R13a_G1 — exact historical provenance

Require:

- exact Repair08/10/11/12 inputs;
- exact Repair13 JSON hash and class;
- Repair13 result-freeze ancestry;
- exact frozen imported-code blobs.

### R13a_G2 — historical Repair13 pass/fail pattern

Require historical Repair13 gates exactly:

`[PASS,PASS,FAIL,FAIL,FAIL,PASS,PASS,PASS]`

for G1-G8.

### R13a_G3 — roundoff-aware source-sum closure

Require all pointwise G3 inequalities above.

### R13a_G4 — roundoff-aware coefficient closure

Require all pointwise G4 inequalities above.

### R13a_G5 — roundoff-aware projection identity

Require all 54 smallest-lambda projection identities above.

### R13a_G6 — frozen localization payload unchanged

Require from the exact frozen Repair13 JSON:

- 54 cases;
- E2 dominant in 54/54;
- E2 first-order-like in 54/54;
- EX first-order-like in 54/54;
- X2 second-order-like in 54/54;
- all Repair12 total-H slope reproductions PASS.

No post-result source selection is allowed.

### R13a_G7 — claim boundary

Require no state write/projection, nonlinear correction, coefficient fit/rescale, source insertion/removal, sign change, K clipping, Q linearization, threshold change, point removal, Y/beta/scale selection, nonlinear evolution, finite eta, B4 relabel, or observational-detection claim.

## Terminal classifications

Allowed:

- `NL1C7B4_REPAIR13A_ROUNDOFF_STABLE_SOURCE_LOCALIZATION_PASS`;
- `NL1C7B4_REPAIR13A_IMPLEMENTATION_FAIL`.

A PASS certifies only that the already frozen Repair13 source-localization payload is numerically self-consistent once cancellation-conditioned closure identities are tested with preregistered IEEE-754 forward-error bounds.

It does **not** establish that `AeST_E2` is physically wrong. A separate analytic first-variation audit is required before any model/interface change.
