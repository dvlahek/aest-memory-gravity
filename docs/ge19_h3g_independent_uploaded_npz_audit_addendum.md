# GE19 H3G — independent uploaded NPZ audit addendum

## Scope and relation to original result freeze

This append-only addendum closes the explicit **NPZ-not-uploaded
limitation** recorded in the immutable original freeze
`docs/ge19_h3g_corrected_y_q20_valid_local_science_result_freeze.md`
(blob `e5b273a16a131be324162d3e66cf799e4ac543c3`).

The user subsequently uploaded the exact H3G NPZ, and it was read
directly from the mounted conversation file. This addendum does
not rewrite the original result chronology, alter the first
science outcome or imply an independent rerun of the q20 solver.

## Byte-level result provenance

Uploaded file:

`ge19_h3g_corrected_y_q20_reconstruction.npz`.

Observed byte count: `3550825`.

Independently calculated SHA-256:

`9e1bf36e1d81122225ff8c03f663501de7601a8fc9376fd86312e0ae1d809452`.

These equal the original frozen local runner's NPZ
byte count and SHA-256, as recorded in the first
H3G local science result. The NPZ was opened
with `allow_pickle=False`.

## Independent array audit

- 30 stored arrays, all of numeric dtype;
- all numeric entries in all 30 arrays finite;
- exact coordinate grids: `x_primary` (128),
  `x_control` (64), `r_primary,w_primary` (2048),
  `r_control,w_control` (1024);
- for each `C_min,C_star,C_max`,
  the stored primary weighted Z20 projection has
  shape `(3,40,128)` and its Nt64 time control
  has shape `(3,40,64)`;
- the stored `weighted_z20_primary[:,:,0]`
  is **exactly zero** in all three C cohorts,
  consistent with the frozen particular
  initial condition;
- all 27 representative scalar norms
  (`weighted_z20_primary_L2`,
  `X20_primary_L2`,
  `B20_linear_primary_L2`)
  in the nine (C,beta0) cases agree **exactly**
  with the already-uploaded H3G JSON:
  max relative report-to-array discrepancy `0.0`.

The independently recalculated q20
Nx/Nq control differences are in the
expected `8.23e-5` range, below the
unchanged preregistered `1e-2`
quadrature threshold; those individual
per-C recalculations use a local
per-array norm and are not asserted to
be exactly identical to the JSON's
cohort-aggregated control value.

The uploaded JSON's 13 science gates remain
true. This addendum specifically supplies the
previously missing independent **stored-array**
and **byte-hash** verification, not a new
model fit or science threshold.

## Final H3G boundary

The previously frozen classification remains:

`GE19_H3G_CORRECTED_Y_Q20_RECONSTRUCTION_PASS`.

The corrected-H3F/H3G Z20/q20 parent pair
is now independently array-audited for
its stored H3G result. The original H3F
certification and historical Repair22/27
results are unchanged.

The full all-sector H4 Ward/Noether
source identity and common-parent source
compatibility remain unproved.
No H4/Z21 science certification or
lensing prediction is licensed.
