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

## Remaining D9 obligations after D12R12A

1. Rigorous continuum source-shift derivative envelopes:
   - GE06 M9
   - GE07 M9
   - GE05 M2 M5
2. Non-Y operator M5 envelopes for the exact D1 products.
3. Non-Y parent/lower-boundary discretization budget using the certified continuous parents, including D12R11G1 for Z11.
4. Operation-level roundoff propagation.
5. Freeze `B_total` independently of the observed full-Ward residual.
6. Execute the integrated physical H4 Ward test.
7. If the Ward certificate passes, solve final window-local particular Z21 and apply the unchanged `1e-6` science gate.
8. Lensing remains blocked until Z21 is certified.

## Next route

`D12R12B_GE06_GE07_M9_AND_GE05_M2_M5_CONTINUUM_SOURCE_SHIFT_BOUNDS`
