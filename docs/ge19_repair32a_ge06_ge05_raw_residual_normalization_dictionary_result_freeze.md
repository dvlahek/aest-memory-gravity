# GE19 Repair32A GE06/GE05 raw-residual normalization dictionary — result freeze

## Status

Classification:

`GE19_REPAIR32A_GE06_GE05_RAW_RESIDUAL_NORMALIZATION_DICTIONARY_PASS`.

Repair30 and Repair31 remain historical results and are not relabelled.

No H2 reintegration and no H4/Z21 solve were performed.

## Local output provenance

JSON:

- SHA-256: `adef8fad50233c7fa5df3d57e7f21df80ed99228402831b2861ad06256519725`
- bytes: `2121`

FULL log:

- SHA-256: `adef8fad50233c7fa5df3d57e7f21df80ed99228402831b2861ad06256519725`
- bytes: `2121`

Runner log:

- SHA-256: `dd4fc750df7e03e3fe93bf4d3df97e66a467160cc8f022079b97303ce74742e0`
- bytes: `4038`

The JSON and FULL log are byte-identical.

## Exact dictionary result

The isolated GE06 aether term is

`L_GE06 = a^3 K_B E^2`.

Therefore

`dL_GE06/dE = 2 a^3 K_B E`.

The frozen physical CLASS memory tangent is

`dE/dt|_mem = -Q B/(2 K_B)`.

Mapped into the GE06 raw Euler-Lagrange residual convention, this gives the
RHS magnitude

`a^3 Q B`.

The separately generated GE05 raw first-directional memory residual is

`M1_r = -a^3 Q B/2`.

Therefore the exact conversion is

`GE05_M1_to_GE06_raw_residual_scale = 2`.

This is symbolic and exact. It is not a fitted normalization.

## Independent implementation convention checks

All frozen convention checks pass:

- GE06 contains the `a^3 K_B E^2` normalization;
- GE05 contains the completed-square `1/4` action normalization;
- v0.39 force builder uses the physical `-1/2` memory forcing;
- v0.19w runtime tangent patch uses `dE'/deta|0=-aQB/(2K_B)`;
- NL0B result freeze explicitly fixes the physical factor `1/2`.

## Repair31 empirical consistency

The exact dictionary factor is independently supported by the frozen
Repair31 operator audit:

- Repair30 solution aether LHS/RHS:
  `0.9999961596269547`;
- Repair30 solution scalar LHS/RHS:
  `1.0000041795942898`;
- R2 parent aether LHS / Repair30 RHS:
  `2.0002926513914643`;
- R2 parent scalar LHS / Repair30 RHS:
  `2.0004430883773`.

Both R2 ratios lie within `1e-3` of the exact symbolic factor two.

## Consequence for Repair30

Repair30 used the GE05 raw M1 residual directly inside the GE06 raw
operator convention:

`L_GE06 Z11 = -M1_GE05`.

The exact dictionary shows that the compatible equation is instead

`L_GE06 Z11 = -2 M1_GE05`.

Thus Repair30 is retained as historical science FAIL under its frozen
contract, but its H2 source normalization is now proven incompatible with
the GE06 raw residual convention.

## Next licensed step

Repair32B may change exactly one physics/dictionary item relative to the
Repair30 H2 construction:

`M1_GE05_to_GE06_raw_residual_scale: 1 -> 2`.

No fitted normalization is permitted.

Repair32B must not silently repair or relax the two Repair30 monitor
pathologies identified by Repair31. Those monitors may be reported, but any
new certification rule requires a separately preregistered follow-up.

## Canonical status

**Repair32A = PASS. Exact GE05 -> GE06 raw-residual dictionary factor is 2.
Repair30 remains historical FAIL. Reduced Z11 remains NOT CERTIFIED.
H4/Z21 remains BLOCKED. Repair32B factor-two corrected H2 reconstruction is
the next licensed science run.**
