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

Frozen source-code blobs:

```text
Repair37 = 45d203a092f9ac71cc612b15df5f0c0c630f5898
h4f2g    = d9778da0bb6cc52a15015238810c79978527ffc5
h4f2h    = 65ce1e68a2f77e063c4bb8848d770abb4baeeebf
```

The physical source Ward differentiates only source row 6, the shift row.

Actual saved H4F3B source arrays were checked in all 18 C/beta/Nt cohorts. The following temporal derivative truncation obligations close exactly because their shift row is structurally and bitwise zero:

```text
2Q_Lambda_cross                     FD8 temporal truncation = exactly zero
2DY2_action_complete_Y_u_and_phi    FD8 temporal truncation = exactly zero
2M1_GE05_mapped                     FD4 temporal truncation = exactly zero
```

Observed actual shift-row maxima:

```text
Lambda = 0
Y      = 0
M1     = 0
```

The only remaining source temporal-derivative budgets are:

```text
2Q_GE06_cross   -> FD8 -> require rigorous continuum M9 shift envelope
2Q_GE07_cross   -> FD8 -> require rigorous continuum M9 shift envelope
2M2_GE05_mapped -> FD4 -> require rigorous continuum M5 shift envelope
```

Actual saved shift-row maxima, report-only and not used as derivative bounds:

```text
GE06 = 1.9117449658448746e-04
GE07 = 2.4812747894409690e-13
M2   = 2.0057880026144538e-07
```

These sampled maxima are not M9/M5 certificates and must not be promoted into the D9 tolerance.

### Claim boundary

D12R12A closes only temporal finite-difference truncation obligations whose frozen H4 source shift row is structurally and actually zero. It does not bound GE06, GE07 or GE05-M2 temporal derivative error, operator M5, parent/boundary error, roundoff, the full H4 Ward identity, or Z21.

No science threshold changed. No observational tuning was used.

## D12R12B0 — high-derivative source jet contract

**CLOSED / dependency-contract certificate**

Classification:

`GE19_D12R12B0_HIGH_DERIVATIVE_SOURCE_JET_CONTRACT_PASS_VALIDATED_JET_ENGINE_REQUIRED`

Uploaded result JSON SHA256:

`4bbbdc925115e8aa10e89928ad1dae7037927444d0917465b9e4836cc903710c`

Uploaded result confirms the D12R12A remaining family set exactly and freezes the high-order parent dependencies without reading the full Ward residual or promoting sampled Nt64/Nt128 values into derivative bounds.

Key consequences:

```text
2Q_GE06_cross:
  FD8 source derivative order = 9
  required H1 temporal jet order = 10
  required Z11 temporal jet order = 10

2Q_GE07_cross:
  FD8 source derivative order = 9
  required H1 temporal jet order = 10
  required Z11 temporal jet order = 10

2M2_GE05_mapped:
  FD4 source derivative order = 5
  required H1 temporal jet order = 6
  required bath temporal jet order = 6
```

For Z11, the first-order H2 system implies that a state jet through order 10 requires the H2 forcing jet through order 9. Since the forcing is built from

```text
B10 = X10 - weighted_z10
```

the weighted bath state also requires validated high-order jets.

D12R12B0 explicitly records:

```text
existing order-6/order-10 validated parent jet certificate = false
M5/M9 certified = false
B_total defined = false
full H4 Ward execution licensed = false
Z21 certified = false
```

It also explicitly forbids two invalid shortcuts:

```text
sampled source magnitudes used as M5/M9 bound = false
Nt128/Nt64 difference used as M5/M9 bound = false
```

### Claim boundary

D12R12B0 is not an M5/M9 proof. It freezes the exact high-derivative dependency graph for the three remaining source temporal truncation terms. The next mathematical requirement is a validated continuous parent/bath jet engine through order 10.

No science threshold changed. No observational tuning was used.

## Remaining D9 obligations after D12R12B0

1. Build and validate the continuous order-10 parent/bath jet engine.
2. Use it to certify:
   - GE06 M9
   - GE07 M9
   - GE05 M2 M5
3. Non-Y operator M5 envelopes for the exact D1 products.
4. Non-Y parent/lower-boundary discretization budget using the certified continuous parents, including D12R11G1 for Z11.
5. Operation-level roundoff propagation.
6. Freeze `B_total` independently of the observed full-Ward residual.
7. Execute the integrated physical H4 Ward test.
8. If the Ward certificate passes, solve final window-local particular Z21 and apply the unchanged `1e-6` science gate.
9. Lensing remains blocked until Z21 is certified.

## Next route

`D12R12B1_VALIDATED_CONTINUOUS_PARENT_BATH_JET_ENGINE_ORDER10`
