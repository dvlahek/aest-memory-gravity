# NL1C7B4 Repair18d1 — implementation lock

## Status

Locked after implementation and before any Repair18d1 execution.

## Frozen Repair18d parent

- result-freeze commit:
  `1806635e031f269bfd9a9184fb148672941ad5c0`
- result-freeze blob:
  `c5cf4b1d228039937044e450f0619fff8fa77841`
- Repair18d JSON SHA-256:
  `adc1410d50118c8080c1f84e5733cb09e5ff7d8f51a4937f1e306a96fe416def`
- frozen classification:
  `NL1C7B4_REPAIR18D_IMPLEMENTATION_FAIL`.

## Preregistration

- commit:
  `72da0a2347e412b3f596afaa6a341532a9c5a2f1`
- file:
  `docs/nl1c7b4_repair18d1_predata_svd_path_reproduction_harness_repair.md`
- blob:
  `b3ed9f63654771a1ac44787ecebdba88a5f6a554`.

## Implementation

- commit:
  `0b6751a3e4ed448dde18fa906b4002e63920e699`
- file:
  `nl1c7b/initial_constraint_certification_repair18d1.py`
- blob:
  `e2092bf3ceaa1ad6ffab8b951f5002c3ad100e0d`.

## Sole SVD-path repair

Repair18d used the full-SVD singular values for frozen Repair18c scalar reproduction.

Repair18d1 uses:

`s_ref=np.linalg.svd(J,compute_uv=False)`

for:

- sigma_max
- sigma_min
- rank tolerance
- numerical rank

while retaining:

`U,s,Vh=np.linalg.svd(J,full_matrices=True)`

and

`V0=V[:,-2:]`

for the transversality subspace exactly as in Repair18d.

No candidate or transversality calculation is changed.

## Frozen payload reproduction

Repair18d1 must reproduce the frozen Repair18d candidate payload to abs-or-rel `1e-12`, including:

- all 15 scale/candidate sigma_max(T)
- sigma_min(T)
- sigma_min/sigma_max
- condition number
- determinant magnitude
- transverse flags
- candidate scores
- deterministic selected candidate and order.

The frozen Repair18d selected candidate is diagnostic input only until Repair18d1 passes.

## Frozen imported blobs

- Repair18d evaluator:
  `c7e5ab27e53798b9b907d0d3689f18cd97e36a79`
- Repair18b1 evaluator:
  `1a312dea619c46aa300cbd4c30f141d7d4b2e624`
- Repair18a evaluator:
  `767199e8ab620f5d6dabd50d0efde9828f22048b`
- Repair16 evaluator:
  `fbd7d24f748fc398638d4eea4b7707801161e52a`
- Repair01 source dictionary:
  `253a0ae2a19a597f06358704ea276c9005973af3`
- Repair09 exact helpers:
  `0cd67cecfbd590cb8819ad37314dc5b49047bc93`
- base B4:
  `8559120dc273be3174eca130ca313ed6ff5acb25`
- Repair08:
  `94fb3f42a7c819b0525860f7344d5dbaff93da19`
- C7A reconstruction:
  `ff383c1ddc2cb2a684e2b5dd11fde0ae811e4fac`.

## Frozen candidate order

1. `Y1+Qmean`
2. `Y4+Qmean`
3. `Y8+Qmean`
4. `Y16+Qmean`
5. `Y1+Q1`.

## Frozen thresholds

- Repair18c scalar reproduction: abs-or-rel <= `1e-12`
- Repair18d payload reproduction: abs-or-rel <= `1e-12`
- transversality: `sigma_min(T)>1e-6`
- selection tie threshold: abs-or-rel `1e-12`.

## Terminal classes

- `NL1C7B4_REPAIR18D1_NULLSPACE_TRANSVERSALITY_AUDIT_PASS`
- `NL1C7B4_REPAIR18D1_IMPLEMENTATION_FAIL`.

No nonlinear solve, state change, candidate modification, threshold change, physics change, or historical relabelling may occur after the first Repair18d1 execution.
