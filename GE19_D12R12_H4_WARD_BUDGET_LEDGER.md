# GE19 D12R12 H4 Ward numerical-budget ledger

Status date: 2026-10-14

Frozen science branch: `physics-first-gravitational-elasticity`

Frozen science HEAD:

`6282ed54e35d4db6b58fcd13d1c7403419f8afb7`

This ledger is maintained on the documentation branch. Documentation commits do not advance the frozen science HEAD.

## Project frontier

D12R11 continuous physical Z11 is CLOSED. Preferred H4 parent:

`GE19_D12R11G1_TIGHT_CONTINUOUS_COMPONENTWISE_Z11_ENCLOSURE_PASS_H4_PARENT_READY`

The actual frontier is now the remaining non-Y D9 numerical budget before the integrated physical H4 Ward test and final Z21 solve.

Frozen science gate remains unchanged:

```text
H4_active_shift_Nt128_Linf <= 1e-6
```

Historical Repair37 remains FAIL and is never relabeled:

```text
1.1749387207106255e-06
```

No observational or lensing tuning is allowed.

## D12R12A — source temporal-derivative obligation reduction

**CLOSED / structural exact-zero certificate**

Classification:

`GE19_D12R12A_SOURCE_TEMPORAL_DERIVATIVE_OBLIGATION_REDUCTION_PASS`

Uploaded result JSON SHA256:

`f792c1cf85ba12e980051295e374433b690b2414bcea9eee7e12e87293ca735c`

Frozen H4F3B parent hashes:

```text
JSON = 1ec88fd3fd6b81bf30614b0cb78d722a02dd4f745e1f22cb9b8f956a44bac6c1
NPZ  = 787d5d177838b05078057aa932f379dd529449ce203f5664c36cf723acb0116b
```

The physical source Ward differentiates only source row 6, the shift row. Lambda, Y and GE05-M1 have structurally and actually zero shift rows in all 18 frozen H4F3B cohorts, so their temporal FD truncation contributions close exactly.

The only remaining source temporal-derivative budgets are:

```text
2Q_GE06_cross   -> FD8 -> rigorous continuum M9 shift envelope
2Q_GE07_cross   -> FD8 -> rigorous continuum M9 shift envelope
2M2_GE05_mapped -> FD4 -> rigorous continuum M5 shift envelope
```

Sampled source magnitudes are report-only and are never promoted into M9/M5 certificates.

## D12R12B0 — high-derivative source jet contract

**CLOSED / dependency-contract certificate**

Classification:

`GE19_D12R12B0_HIGH_DERIVATIVE_SOURCE_JET_CONTRACT_PASS_VALIDATED_JET_ENGINE_REQUIRED`

Uploaded result JSON SHA256:

`4bbbdc925115e8aa10e89928ad1dae7037927444d0917465b9e4836cc903710c`

Frozen dependency consequences:

```text
GE06: source derivative order 9 -> H1 and Z11 temporal jets through order 10
GE07: source derivative order 9 -> H1 and Z11 temporal jets through order 10
M2:   source derivative order 5 -> H1 and bath temporal jets through order 6
```

For Z11, the forcing is built from `B10 = X10 - weighted_z10`, so high-order bath jets are part of the proof chain. B0 does not certify M5/M9 and explicitly forbids sampled-grid or Nt64/Nt128 differences as derivative suprema.

## D12R12B1A — order-9 operator/source-map Taylor jet engine

### Smoke

**CLOSED / smoke validation**

Classification:

`GE19_D12R12B1A_ORDER9_OPERATOR_SOURCE_MAP_JET_ENGINE_SMOKE_PASS_ALL_TRAJECTORIES_OPEN`

Uploaded smoke JSON SHA256:

`9e9299e0c84422faab3321327a54ad8b32e9ba18ff04936366447d085c49d421`

Smoke trajectory `Nt64 / C_min / m20` used 252 sub4 child intervals. All 16128 midpoint M0 reference checks were contained, verified-solve `q_inf <= 8.867822383763307e-03`, and all order-0..9 derivative bounds were finite.

### All 36 trajectories

**CLOSED / validated operator-source-map jet engine**

Classification:

`GE19_D12R12B1A_ORDER9_OPERATOR_SOURCE_MAP_JET_ENGINE_ALL_TRAJECTORIES_PASS_H1_Z11_STATE_JETS_OPEN`

Uploaded all-trajectories JSON SHA256:

`9ee27cc613b0173d20648a63e997657586a83f00ed379e568f619b0d06a65dbf`

Coverage:

```text
trajectory count = 36
child interval count = 13680
midpoint M0 reference checks = 875520 / 875520 contained
all verified-solve q_inf < 1 = true
all operator/map derivative bounds finite = true
```

The global worst verified-solve contraction and order-9 operator/map bounds occur on `Nt64 / C_min / m3`:

```text
q_inf max            = 8.867822383763307e-03
max |M^(9)| upper    = 7.301968054456321e+15
max |F^(9)| upper    = 1.777692843756749e+17
```

These are rigorous derivative envelopes for the exact original-action canonical operator/source map. They are not GE06/GE07 source M9 certificates. B1A still leaves H1 state jets, Z11 state jets and bath jets open.

B1A reuses the frozen D12R10 exact symbolic C matrix, verified interval Az solve and exact original-action background identities. No H1/Z11/bath solve is performed, no science threshold changes, and no observational tuning is used.

## Remaining D9 obligations after D12R12B1A

1. D12R12B1B: certify continuous H1 state jets through order 10 from the D17 continuous approximant, D12R10 componentwise H1 error enclosure and the B1A operator jets.
2. Propagate bath and Z11 forcing/state jets through the required orders.
3. Use those jets to certify GE06 M9, GE07 M9 and GE05-M2 M5.
4. Non-Y operator M5 envelopes for the exact D1 products.
5. Non-Y parent/lower-boundary discretization budget using the certified continuous parents, including D12R11G1 for Z11.
6. Operation-level roundoff propagation.
7. Freeze `B_total` independently of the observed full-Ward residual.
8. Execute the integrated physical H4 Ward test.
9. If the Ward certificate passes, solve final window-local particular Z21 and apply the unchanged `1e-6` science gate.
10. Lensing remains blocked until Z21 is certified.

## Next route

`D12R12B1B_H1_STATE_JETS_ORDER10`
