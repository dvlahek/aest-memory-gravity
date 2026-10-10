# GE19 H4F3D12R2 exact background on-shell elimination — result freeze

Date: 2026-10-10

Branch: `physics-first-gravitational-elasticity`

Preregistered source commit:

`9573f0316b0bdce5cb8b3e824602d05ca7b3dcdd`

Classification:

`GE19_H4F3D12R2_EXACT_BACKGROUND_ONSHELL_ELIMINATION_PASS_F21_INDEPENDENT`

## Frozen result

D12R2 proves the exact continuum homogeneous-background elimination required before the integrated H4 Ward test.

Under the frozen Repair13 Friedmann, scalar-charge, dust and Lambda background equations, with homogeneous Y background `X0=0` and the regular GE05 bath background, the relevant background Euler factors vanish exactly.

Therefore the mixed-H4 unknown-state factors

`E00 * dchi(F21)`

and

`L21 * E_L00 - b21 * E_b00`

vanish for arbitrary unknown `F21`, `L21` and `b21` because their multiplying background Euler factors vanish. The stage does not assign, solve or set the unknown mixed-H4 states to zero.

All explicit D12R2 gates passed:

- parent lock: PASS;
- exact nonbath background: PASS;
- dust background: PASS;
- GE05 background: PASS;
- arbitrary `F21/L21/b21` elimination: PASS;
- negative controls: PASS.

The process exited with status `0`.

## Result hashes

Frozen local result JSON SHA-256:

`8a76edf7a9e8c21f1de49eb49f85332876cc230cf5e7c2d8ef136ca5e368b650`

Frozen full log SHA-256:

`ad1b12a0aac883b7d0d93302dcd4d2c1bd47e138bd1fae85e80aaae88e65ed99`

## Claim boundary

This is an exact continuum homogeneous-background on-shell elimination result only.

It does **not** certify:

- the remaining H1/Z11/Z20/q20/bath/operator/source Ward residual;
- the full original H4 Ward identity;
- `Z21`;
- lensing.

Historical D11 FD4/FD8 background residual arrays remain immutable numerical diagnostics and are not promoted to exact discrete zeros. Historical H4 FAIL results remain unchanged.

No source coefficient, action normalization, threshold or observation-based tuning was changed.

## Next route

The next and only remaining structural gate before the final Z21 science solve is:

`ONE_ACTUAL_COMMON_GRID_OPERATOR_SIX_SOURCE_ALL_PARENT_WARD_TEST`

If that integrated full H4 Ward test PASSes, one final action-completed Z21 solve is licensed using the unchanged original gate

`H4_active_shift_Nt128_Linf <= 1e-6`.

Lensing remains blocked until that Z21 solve passes.
