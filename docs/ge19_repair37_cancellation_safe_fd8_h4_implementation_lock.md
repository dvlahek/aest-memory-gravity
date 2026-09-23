# GE19 Repair37 cancellation-safe FD8 H4/Z21 reclosure — implementation lock

## Status

Repair37 is frozen before its first science execution.

Repair36 remains the historical valid FAIL and is not relabelled.

Repair37 changes only two localized numerical aspects:

1. the cancellation-dominated floating Lambda polarization audit is replaced
   by a cancellation-safe direct-vs-expanded exact bilinear audit;
2. the GE06/GE07 nonlinear Euler-Lagrange time derivative in
   `Dt @ partial` uses a 9-point degree-8 exact first-derivative operator on
   the same Nt128/Nt64 grids instead of the frozen Repair36 fourth-order
   `fd4_matrix`.

The physical H4 equation, source formulas, parents, Lambda sector, memory
normalization, Repair18 boundary, Repair07 Radau propagator, grids and science
thresholds are unchanged.

## Frozen Repair36 valid FAIL

Localization freeze:

`docs/ge19_repair36_valid_fail_numerical_localization_freeze.md`.

Blob:

`4ff3b601e96936963e8f2d36e2a22ba5c5f059ed`.

Commit:

`fa82cf21c3bfd0b1bdb9f6c451670e83b1e115c0`.

Frozen Repair36 science artifacts:

- JSON SHA-256:
  `5ba2dacf586ccbbdd5eb41c4ea7cf5c839f5aa2829c294702b4fc37d84ef113f`;
- NPZ SHA-256:
  `e19962ca71ea002c61b3251365496ee46ac1467054fff81625fb2bce5b5c652a`;
- FULL SHA-256:
  `5ba2dacf586ccbbdd5eb41c4ea7cf5c839f5aa2829c294702b4fc37d84ef113f`;
- outer runner SHA-256:
  `200ac7f4011420ca604b9518a52d791ef783e24de3f18d3b0ebc7bed6ea8e2d2`.

## Frozen preregistration

File:

`ge19/repair37_predata_cancellation_safe_fd8_h4_z21_reclosure.json`.

Blob:

`cd60e8bc725588cdc13f22255fcba16ba27393d1`.

Commit:

`1ef3d95bbd9977d89c3f12beef8eada82995c1a9`.

## Frozen implementation

File:

`ge19/repair37_cancellation_safe_fd8_h4_z21_reclosure.py`.

Blob:

`45d203a092f9ac71cc612b15df5f0c0c630f5898`.

Final implementation commit:

`110f066a9d1bbb2b8ca28cff6b4c08404c457a67`.

Static audit:

- run `35826607062`;
- conclusion `success`.

## Dedicated Repair37 prelock

Workflow:

`.github/workflows/ge19-repair37-prelock-audit.yml`.

Blob:

`4b12ac770b76cf705b6d5c04cb459ae13888f8bd`.

Workflow commit:

`65a5edc61da155f59ec9c57429eb52d1a03893e7`.

Run:

`35826658894`.

Conclusion:

`success`.

The prelock verifies:

- Repair36 valid FAIL is retained and not relabelled;
- the frozen H4 shift threshold remains exactly `1e-6`;
- all other frozen Repair36 thresholds remain unchanged;
- all unchanged physical/numerical helper functions remain source-identical;
- `q_cross_direct` differs from Repair36 only by
  `r7.fd4_matrix -> fd8_matrix`;
- the FD8 stencil is degree-8 exact to floating roundoff;
- the exact Lambda direct-vs-expanded bilinear identity is symbolic exact;
- Lambda direct swap symmetry is exact;
- the historical subtractive Lambda polarization is report-only.

## Frozen FD8 operator

The derivative uses 9 grid points.

Interior rows use the centered degree-8 exact stencil

`[1/280,-4/105,1/5,-4/5,0,4/5,-1/5,4/105,-1/280]/h`.

The first/last four rows use the corresponding one-sided 9-point degree-8
exact stencils.

The operator is used only in the nonlinear GE06/GE07 Euler-Lagrange source
assembly terms that previously used Repair36 `fd4_matrix`.

It does not modify the Repair07 canonical Radau propagator.

## Frozen Lambda audit repair

The physical mixed Lambda source is unchanged.

The certification gate compares the direct source to the independently
expanded exact bilinear expression.

The old subtractive

`[Q(d+e)-Q(d-e)]/4`

floating evaluation is retained only as a report-only cancellation
diagnostic.

## Stop rule

The first Repair37 execution that emits a valid Repair37 science JSON is
frozen as PASS or FAIL.

Implementation/execution failures before a valid science JSON may be repaired
without changing this contract.

A Repair37 PASS certifies only the canonical window-local particular reduced
Z21 state. It does not certify a primordial homogeneous Z21 mode, a
full-species nonlinear cosmology, finite eta, or an observational signal.
