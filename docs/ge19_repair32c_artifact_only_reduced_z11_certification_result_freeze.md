# GE19 Repair32C artifact-only reduced Z11 certification — result freeze

## Status

Classification:

`GE19_REPAIR32C_ARTIFACT_ONLY_REDUCED_Z11_CERTIFICATION_PASS`.

Canonical consequences:

- `Z11_certified = true`;
- `H4_Z21_licensed = true`;
- next route:
  `REDUCED_Z11_CERTIFIED_PREREGISTER_H4_Z21`.

Repair32C performed no H2 reintegration, no source change, no threshold fit,
no H4/Z21 solve, no finite physical eta evolution and no observational fit.

## Local output provenance

Science JSON:

- SHA-256:
  `037314effa33c5bfaf51f6f3c72459de43cb486c6ef5e9a94f5b1984a68611b9`;
- bytes:
  `18893`.

FULL log:

- SHA-256:
  `037314effa33c5bfaf51f6f3c72459de43cb486c6ef5e9a94f5b1984a68611b9`;
- bytes:
  `18893`.

Runner log:

- SHA-256:
  `c6958d2e7778c4ae4cc7cac825e7fcfec9930e7963749d3bfa64ff27d9f6edb3`;
- bytes:
  `20728`.

The science JSON and FULL log are byte-identical.

## Frozen Repair32B parent

Repair32C certifies the exact frozen Repair32B corrected H2 reconstruction:

- Repair32B JSON SHA-256:
  `226dd2a2a0e86ddccc39a62d833960bdf9d5a9af038ad3bf225bbbf69d0b95cf`;
- Repair32B JSON bytes:
  `68434`;
- Repair32B NPZ SHA-256:
  `5d4a0a72c08d09d096a8de0b428b3c8443fc33e8ad442ed6d997d6bf2bc6e327`;
- Repair32B NPZ bytes:
  `1082578`;
- exact GE05 -> GE06 raw-residual dictionary scale:
  `2.0`;
- fitted normalization:
  `false`.

## State precision

Maximum full six-field global Nt128/Nt64 relative L2:

`2.556265819451129e-04`.

Maximum dynamic S,u,varphi,T Nt128/Nt64 relative L2:

`2.5562658185082605e-04`.

Both are well below the frozen `5e-3` threshold.

The large historical per-field `delta_varrho` ratios remain a near-zero
algebraic-coordinate normalization artifact and are not used as the global
state certificate.

## chi11 parent closure

Maximum reduced chi11 versus the independently certified Repair29B R2 parent:

`3.552163301878936e-04`.

Minimum temporal-shape cosine:

`0.9999999998559488`.

Maximum post-fit relative L2:

`1.6973582555861977e-05`.

Inherited initial-boundary abs-or-rel mismatch:

`2.134061856895356e-22`.

C-envelope relative L2 max:

`2.5827438644493813e-04`.

## Reduced-operator closure

Driven rows:

- aether global relative L2:
  `1.843818206810418e-05`;
- scalar global relative L2:
  `1.9965677339471006e-05`.

Maximum driven-row residual:

`1.9965677339471006e-05`

against the frozen `1e-4` artifact-only threshold.

Source-free rows are normalized by one global main-operator scale to avoid
the zero-RHS relative-residual pathology.

Maximum source-free absolute residual / global main-operator scale:

`6.80302904374535e-07`

against the frozen `1e-4` threshold.

## Constraint closure

Global shift relative to main-operator scale:

`1.1902506494394523e-17`.

Global anisotropy relative to main-operator scale:

`1.9874831190320898e-27`.

Both are far below the frozen `1e-6` threshold.

## Gates

All Repair32C gates PASS:

- Repair32B hashes exact;
- Repair32B reconstruction PASS;
- exact dictionary factor 2 with no fitted normalization;
- all Repair32B reconstruction gates PASS;
- global state precision PASS;
- dynamic state precision PASS;
- chi11 parent closure PASS;
- inherited boundary PASS;
- driven operator rows PASS;
- source-free operator rows PASS;
- shift PASS;
- anisotropy PASS;
- C-envelope PASS;
- all diagnostics finite.

## Scientific consequence

The complete reduced first-order eta tangent `Z11` is now certified on the
frozen late-time AeST + pressureless-dust reduction.

This closes the final missing parent required by H4.

The next licensed equation is

`L Z21 = -2 Q(Z10,Z11) - 2 DY2[Z10;Z11] - M1[Z20,q20] - M2[(Z10,q10),(Z10,q10)]`

with all terms mapped into one common GE06 raw-residual convention.

Because Repair32A proved that the entire GE05 raw memory residual convention
differs from the GE06 raw convention by an overall factor two, the GE05
memory contributions in H4 must be converted with that exact dictionary
before assembly. This is a convention conversion, not a fitted factor.

## Canonical status

**Repair32C = PASS. Reduced Z11 is CERTIFIED. H4/Z21 is LICENSED. The next
step is a separately preregistered H4/Z21 source assembly and solve.**
