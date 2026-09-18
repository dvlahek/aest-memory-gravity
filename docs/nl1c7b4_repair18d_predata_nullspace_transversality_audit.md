# NL1C7B4 Repair18d — pre-data null-space transversality audit

## Status

Pre-data / pre-run diagnostic preregistration.

Repair18c is frozen as

`NL1C7B4_REPAIR18C_TWO_MODE_NULLSPACE_CHARACTERIZED`

at result-freeze commit

`c29ce80b65435b60882bd5140a9cfe648b4f3a5b`.

Frozen Repair18c result JSON:

- SHA-256:
  `d49600f8b27536aeb0dca28d1d777d09439a376241c7f8f93b74e754c502e24b`.

Repair18d does not solve or modify the nonlinear state. It audits fixed candidate pairs of simple linear regularity/gauge functionals against the certified two-dimensional right-null subspace.

## Frozen domain

Unchanged from Repair18c:

- eta = 0
- Y = Simple
- beta = 1
- lambda = 1
- Nr = 256
- scales = 5,10,20 h^-1 Mpc
- solver coordinates = `(y_L,q_Rt)`
- dense SciPy default 2-point Jacobian at x=0
- frozen Repair18c rank rule.

## Candidate functionals

Let `m=Nr-1=255` and let the solver coordinate be

`x=[y_L(1..m),q_Rt(1..m)]`.

Each functional row is Euclidean-normalized before the audit.

Define:

- `Y1`: first noncenter y_L coordinate;
- `Y4`: uniform mean over the first 4 noncenter y_L coordinates;
- `Y8`: uniform mean over the first 8 noncenter y_L coordinates;
- `Y16`: uniform mean over the first 16 noncenter y_L coordinates;
- `Qmean`: uniform mean over all q_Rt coordinates;
- `Q1`: first noncenter q_Rt coordinate.

The five preregistered candidate pairs are, in this exact order:

1. `Y1 + Qmean`
2. `Y4 + Qmean`
3. `Y8 + Qmean`
4. `Y16 + Qmean`
5. `Y1 + Q1`

No other pair may be added after the first execution.

## Transversality matrix

For each scale reconstruct the frozen Repair18c right-null basis

`V0 in R^(510x2)`.

For each candidate pair form the normalized 2x510 functional matrix `G` and the 2x2 null-space intersection matrix

`T = G V0`.

Because individual V0 vectors may rotate/sign-flip, all classification metrics use singular values of T.

Report:

- `sigma_max(T)`
- `sigma_min(T)`
- `sigma_min/sigma_max`
- condition number `sigma_max/sigma_min`
- determinant magnitude `|det(T)|`.

A pair is numerically transverse at one scale if

`sigma_min(T) > 1e-6`.

A pair is globally transverse if this holds at all three scales.

This 1e-6 threshold is a numerical-identifiability threshold only. It does not alter any historical physics gate.

## Frozen selection rule

For each candidate define the worst-scale score

`S = min_scale sigma_min(T)`.

Among globally transverse candidates, select the candidate with the largest S.

If two scores are equal within `1e-12` absolute-or-relative, select the earlier candidate in the preregistered order above.

The selected pair is diagnostic output only. Repair18d does not impose it on a nonlinear solve.

## Cross-scale stability of the selected pair

For the selected pair report:

- all three 2x2 singular-value pairs;
- worst-scale sigma_min;
- maximum condition number;
- relative spread of sigma_min across scales:
  `(max-min)/max`.

No spread/condition threshold is imposed beyond the global transversality requirement.

## Frozen gates

### R18D_G1 — exact frozen provenance

Require exact Repair18c JSON hash/classification/gates and all frozen parent hashes.

### R18D_G2 — exact Repair18c null-space reproduction

For each scale reproduce to abs-or-rel `1e-12`:

- rank;
- rank tolerance;
- sigma_max;
- sigma_min;
- sigma_min/sigma_max.

### R18D_G3 — exact candidate set

Require exactly the five preregistered candidate pairs and normalized functional rows.

### R18D_G4 — complete finite transversality audit

Require finite 2x2 matrices and singular metrics for all 15 candidate/scale combinations.

### R18D_G5 — at least one globally transverse pair

Require at least one candidate with

`sigma_min(T)>1e-6`

at all three scales.

### R18D_G6 — deterministic selection rule

Require the reported selected pair to equal the preregistered max-worst-scale rule with frozen tie-breaking.

### R18D_G7 — claim boundary

Repair18d must not:

- modify or solve the nonlinear state;
- impose any candidate condition;
- change the projection pair;
- change the Jacobian rule;
- change the rank rule;
- change any source, coefficient, sign, branch, eta, radial point set, or historical threshold;
- write an NPZ;
- run nonlinear evolution;
- make an observational claim;
- relabel any earlier Repair18 result.

## Terminal classifications

PASS:

`NL1C7B4_REPAIR18D_NULLSPACE_TRANSVERSALITY_AUDIT_PASS`

FAIL:

`NL1C7B4_REPAIR18D_IMPLEMENTATION_FAIL`.

## Interpretation boundary

A PASS identifies a fixed pair of linear conditions that independently intersects the two-dimensional certified null space across all three scales.

It does not establish that the pair is a unique physical gauge choice.

The selected pair may be used only by a separately preregistered nonlinear closure test that preserves the historical `1e-7` exact-constraint threshold.
