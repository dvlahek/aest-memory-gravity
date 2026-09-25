# GE19 H4F3d4 — complete formal mixed Ward ledger with physical eta bath

## Exact result and its boundary

Classification:
`GE19_H4F3D4_FULL_FORMAL_ETA_WARD_LEDGER_PASS_ACTUAL_GRID_OPEN`.

The single analytic/compiler execution proves the **complete formal
off-shell** mixed physical `d_eta d_epsilon^2` longitudinal
spatial Ward decomposition with every nonbath Euler parent,
the newly derived physical eta-regularized GE05 bath parent,
the original GE19 full L/shift row projection, and exactly
six signed H4 RHS families. This is an algebraic identity
and source/implementation binding, **not** a physical
actual-grid all-parent H4F3d structural PASS and not a
Z21 science reclosure.

## Frozen predata and successful execution

- preregistration:
  `ge19/h4f3d4_predata_complete_eta_regularized_mixed_ward_ledger.json`,
  blob `cc921c4086d914274738a29f2b7b5c6961ab56b0`;
- analytic implementation:
  `ge19/h4f3d4_complete_eta_regularized_mixed_ward_ledger.py`,
  blob `87d8be9ec44ecb099feecbaf59a904bd989da2fb`;
- workflow:
  `.github/workflows/ge19-h4f3d4-full-formal-ward.yml`;
- successful run `36106532215`, job `107980223264`;
- terminal marker `GE19_H4F3D4_FULL_FORMAL_ETA_WARD_LEDGER_PASS`;
- JSON SHA-256
  `d6fd4f79910b552238756eb9015e6a7956a8fa0892cb2a46a9bd9e2e7c8d5694`;
- artifact ID `10850904820`.

All pinned-source, original action, canonical operator,
six-source implementation bindings and exact symbolic
sign/factor and negative-control gates passed.

## Full formal signed identity

For all nonbath fields
`i=(N,L,R,b,u,phi,T,rho)` and the physically regularized
NL0B per-node bath `U_j=sqrt(eta)q_j`, the exact mixed
spatial Ward coefficient reads

`W21= sum_{i != q}[
 E_i00 F_i21,x + 2 E_i10 F_i11,x + 2 E_i11 F_i10,x
] +4 sum_j E_qj10,GE05 q_j10,x
 -partial_x B21 -partial_t E_b21 = 0`.

The boundary combination is

`B21=a E_L21 + L21 E_L00 +2 L10 E_L11
 +2 L11 E_L10 -b21 E_b00
 -2 b10 E_b11 -2 b11 E_b10`.

The exact GE19 Euler row projection is
`E_L21=(E_iso21+2 E_aniso21)/3`.
With the unchanged source convention
`E21=L21-S21`, exact algebra splits this
identity into

`W_operator + W_six_source + W_all_parent = 0`.

`W_operator` uses the original Cmat 16x10 full
L momentum and independent shift rows.
`W_six_source` is the sum of the six signed
physical-clock source-Ward projections, with the
separate frozen H*FD8 and H*FD4 family derivatives.
`W_all_parent` retains the explicitly displayed
background/H1/Z11 Euler products, the bath
`+4 E_qj10 q_j10,x` term, and lower-order
action boundary products.

Crucially, this is an **off-shell formal identity**:
the actual Euler residuals and action-boundary
terms may not be set to zero until the exact
certified parents' equations and regularity
are checked. A small source-only Ward magnitude
is not evidence that either the full identity
or the independent H4 shift constraint passes.

## Next decisive test

The original H4F3d physical preregistration
`ge19/h4f3d_predata_actual_operator_all_parent_ward_closure.json`
still governs the required **independent**
one-common-grid, all-18-cohort test on the
actual H4F3b source NPZ and the exact corrected
H3F/H3G/Z11, R13 and Repair26 R1 parents.
Its own FD4/FD8 truncation tolerance must be
derived and frozen before comparing the full
physical structural defect. The formal PASS
does not substitute for these actual parent
Euler residual and boundary arrays.

The actual H4F3b and original certified
Repair32B Z11 NPZ were supplied in the
user's prior local environment but are not
available as raw bytes on GitHub Actions.
No manufactured input may be used to
report a physical Noether PASS.

The original Repair37 Z21 science FAIL and
Repair38–44 diagnostic classifications
remain immutable. The original active-shift
`1e-6` and matched-order `>=2.5` gates
are unchanged. **Z21 NOT CERTIFIED;
lensing blocked.**
