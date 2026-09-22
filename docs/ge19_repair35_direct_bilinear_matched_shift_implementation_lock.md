# GE19 Repair35 direct-bilinear matched-shift H4/Z21 — implementation lock

## Status

Repair35 is frozen before any science result.

Repair34 remains the historical valid H4/Z21 FAIL and is not relabelled.

Repair35 changes no H4 physics. It corrects only the two audit defects localized
from Repair34:

1. floating subtractive polarization of the GE06/GE07 quadratic cross;
2. use of an all-row propagated-shift relative metric instead of the already
   certified Repair21/Repair22 active/near-null rule.

## Frozen preregistration

File:

`ge19/repair35_predata_direct_bilinear_matched_shift_h4_z21.json`.

Blob:

`77779a3e1fefa2847c47a3afe8000d5434377ed1`.

Commit:

`17464d784fd35ef8bd6d67d4f0c6da660c20ff9a`.

## Frozen implementation

File:

`ge19/repair35_direct_bilinear_matched_shift_h4_z21.py`.

Blob:

`41e2907772dd53eb43d41e390bb616b270921cfa`.

Final implementation commit before lock:

`f02508170615c32be171fa4dc4121a6b4f6c9ce6`.

Global static audit:

- run `35781971797`;
- conclusion `success`.

## Frozen Repair34 localization parent

File:

`docs/ge19_repair34_h4_z21_valid_fail_localization_freeze.md`.

Blob:

`f985d45ebc983b56697eb0a3bb37c8b71333339b`.

Commit:

`8bab319dccd212ed6a92f4e0f448e46b84eed5c8`.

Frozen Repair34 artifacts:

- JSON SHA-256:
  `5d6fd3b90e4980e2397058f6785f15b156e4a3826b5b21b614f2fea3acee03d8`;
- NPZ SHA-256:
  `8e6f7f2b02b48ee5c956822a09a591fa32237cd0c5865a7dfb838996d08824ed`.

## Dedicated Repair35 prelock

Workflow:

`.github/workflows/ge19-repair35-prelock-audit.yml`.

Blob:

`e8c5aee4237ff2c2d77e60727539e30d31f26cb2`.

Workflow commit:

`758b2813fdc0a37d25c7eb19ba0a90ed30c3e26b`.

Run:

`35782081114`.

Job:

`106929790398`.

Conclusion:

`success`.

The prelock verifies:

- unchanged H4 equation and GE05->GE06 factor two;
- unchanged physical/source-resolution constants and thresholds;
- unchanged DY2, M1 and M2 source implementations;
- unchanged Repair18 projected boundary;
- unchanged Repair07 canonical Radau propagation;
- exact symbolic identity between the direct mixed GE06/GE07 bilinear
  coefficient and quadratic polarization;
- numerical bilinear swap symmetry at the frozen `1e-12` threshold;
- exact Repair21/Repair22 active/near-null shift definitions:
  `sqrt(eps) S_ref`, active `1e-6`, near-null `1000 eps`, and matched
  convergence order `>=2.5`.

## Frozen H4 equation

`L_GE06 Z21 = -2 Q_total(Z10,Z11) - 2 DY2[Z10;Z11] - 2 M1_GE05[Z20,q20] - 2 M2_GE05[(Z10,q10),(Z10,q10)]`.

No physical coefficient or source term changes relative to Repair34.

## Direct bilinear Q cross

For the frozen homogeneous quadratic source `Q2(d,d)`, Repair35 evaluates

`B(d,e) = (1/2) sum_i [partial Q2(d,d)/partial d_i] e_i`.

The prelock proves symbolically for every frozen GE06 and GE07 local partial:

`B(d,e) = [Q2(d+e,d+e)-Q2(d-e,d-e)]/4`.

Thus the source is algebraically identical to Repair34 but avoids floating
subtractive cancellation.

The old balanced polarization remains report-only.

## Propagated shift certification

Repair35 restores the already frozen Repair21/Repair22 rule:

- `S_ref` is the maximum Nt128 natural shift contribution scale;
- near-null rows satisfy
  `scale <= sqrt(eps) S_ref`;
- active Nt128 rows retain the original `1e-6` backward-error threshold;
- near-null rows use
  `max |residual| / S_ref <= 1000 eps`;
- Nt64 shift metrics are PCHIP-interpolated to the Nt128 physical grid;
- active Linf and RMS convergence orders must each be `>=2.5`.

The historical raw all-row shift maximum remains report-only.

## Stop rule

The first Repair35 execution that emits a valid Repair35 science JSON is
frozen as PASS or FAIL.

Implementation/execution failures before a valid science JSON may be repaired
without changing this contract.

A PASS certifies only the canonical window-local particular reduced Z21 state.
