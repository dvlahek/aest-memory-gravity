# NL1C7B4 Repair18d1 — pre-data SVD-path reproduction harness repair

## Status

Pre-data / pre-run preregistration.

Repair18d is frozen as

`NL1C7B4_REPAIR18D_IMPLEMENTATION_FAIL`

at result-freeze commit

`1806635e031f269bfd9a9184fb148672941ad5c0`.

Frozen Repair18d result JSON:

- bytes: `20628`
- SHA-256:
  `adc1410d50118c8080c1f84e5733cb09e5ff7d8f51a4937f1e306a96fe416def`.

Repair18d result freeze:

- file:
  `docs/nl1c7b4_repair18d_result_freeze.md`
- blob:
  `c5cf4b1d228039937044e450f0619fff8fa77841`.

Repair18d1 is a harness/reproduction repair only.

## Exact defect

Repair18c used two SVD paths:

- values-only:
  `s_ref=np.linalg.svd(J,compute_uv=False)`
- full:
  `U,s,Vh=np.linalg.svd(J,full_matrices=True)`.

Repair18c froze:

- sigma_max
- sigma_min
- sigma_min/sigma_max
- rank tolerance
- numerical rank

from `s_ref`.

Repair18d incorrectly used the full-SVD singular values `s` for those frozen-scalar reproduction quantities.

The right-null basis used by the transversality audit was already taken from the full SVD and is unchanged.

## Licensed repair

Repair18d1 may change exactly:

`U,s,Vh=np.linalg.svd(J,full_matrices=True)`
`smax=s[0]`
`smin=s[-1]`
`rank=rank(s)`

to:

`s_ref=np.linalg.svd(J,compute_uv=False)`
`U,s,Vh=np.linalg.svd(J,full_matrices=True)`
`smax=s_ref[0]`
`smin=s_ref[-1]`
`rank=rank(s_ref)`.

The transversality basis remains:

`V0 = V[:, -2:]`

from the same full SVD as frozen Repair18d.

No other numerical or scientific change is permitted.

## Frozen transversality payload

Repair18d1 must recompute the same five candidate pairs in the same order:

1. `Y1+Qmean`
2. `Y4+Qmean`
3. `Y8+Qmean`
4. `Y16+Qmean`
5. `Y1+Q1`.

It must reproduce the frozen Repair18d payload to abs-or-rel `1e-12` for every scale/candidate:

- sigma_max(T)
- sigma_min(T)
- sigma_min/sigma_max
- condition number
- |det(T)|
- transverse Boolean.

It must also reproduce exactly:

- candidate ordering;
- globally-transverse Boolean;
- worst-scale sigma_min;
- max-scale sigma_min;
- max condition number;
- relative sigma_min spread;
- selected candidate;
- selected candidate order.

Repair18d itself remains IMPLEMENTATION_FAIL.

## Frozen science domain

Unchanged from Repair18d:

- eta=0
- Y=Simple
- beta=1
- lambda=1
- Nr=256
- scales=5,10,20 h^-1 Mpc
- solver coordinates `(y_L,q_Rt)`
- dense SciPy default 2-point Jacobian
- same five candidate condition pairs
- transversality threshold `sigma_min(T)>1e-6`
- same deterministic max-worst-scale selection rule
- tie threshold abs-or-rel `1e-12`.

## Gates

### R18D1_G1 — frozen provenance

Require exact hashes/classes for all frozen parent artifacts plus:

- Repair18d JSON SHA-256
  `adc1410d50118c8080c1f84e5733cb09e5ff7d8f51a4937f1e306a96fe416def`;
- Repair18d classification
  `NL1C7B4_REPAIR18D_IMPLEMENTATION_FAIL`;
- Repair18d gate pattern with only G2 false.

### R18D1_G2 — exact Repair18c reproduction

Using the exact Repair18c values-only SVD path, reproduce for all three scales to abs-or-rel `1e-12`:

- rank
- rank tolerance
- sigma_max
- sigma_min
- sigma_min/sigma_max.

### R18D1_G3 — exact Repair18d transversality payload reproduction

Require the complete frozen Repair18d candidate/transversality payload to reproduce as specified above.

### R18D1_G4 — deterministic selected pair

Require the recomputed selected pair to follow the frozen selection rule and to match the frozen Repair18d selected pair.

No candidate may be changed or added.

### R18D1_G5 — finite diagnostic

Require all Jacobians, SVD quantities, transversality matrices, and selection metrics finite.

### R18D1_G6 — claim boundary

Repair18d1 must not:

- relabel Repair18d;
- impose any candidate condition on a nonlinear solve;
- modify or solve the nonlinear state;
- change the projection pair;
- change the Jacobian rule;
- change the rank rule;
- change candidate definitions/order;
- change transversality/tie thresholds;
- change any source, coefficient, sign, branch, eta, point set, or historical threshold;
- write an NPZ;
- run nonlinear evolution;
- make an observational claim.

## Terminal classifications

If all six gates pass and the frozen deterministic selection is reproduced:

`NL1C7B4_REPAIR18D1_NULLSPACE_TRANSVERSALITY_AUDIT_PASS`.

Otherwise:

`NL1C7B4_REPAIR18D1_IMPLEMENTATION_FAIL`.

## Interpretation boundary

A PASS certifies only the transversality audit and the deterministic selected pair.

It does not yet impose `Y4+Qmean` as a nonlinear boundary/gauge fixing.

A subsequent separately preregistered nonlinear closure test may use the certified selected pair while retaining the historical exact-constraint threshold `1e-7`.
