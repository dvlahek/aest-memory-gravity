# GE19 H4F3B — valid local actual corrected six-piece H4 source freeze

## Frozen result and exact claim boundary

Classification:
`GE19_H4F3B_ACTUAL_CORRECTED_SIX_SOURCE_PASS_FULL_WARD_OPEN`.

The user provided all four local output files. An independent file-level
audit verified their exact bytes and SHA-256, inspected the NPZ without
pickle, and checked all 18 source cohorts directly from stored arrays.

This is a **valid actual six-source source-only result** on the
certified corrected-Y H3F/H3G parents and the exact historical
certified Repair32B/32C Z11 used by the local runner. It is **not**
a complete linear-operator-plus-parent Euler Ward/Noether identity,
an H4/Z21 solve, a science Z21 certification or a lensing result.
All historical Repair37–44 results and frozen science thresholds
remain unchanged.

## Verified local file provenance

| Original runner file | Bytes | Independently computed SHA-256 |
|---|---:|---|
| `results/ge19_h4f3b_actual_corrected_six_piece_source.json` | 17898 | `1ec88fd3fd6b81bf30614b0cb78d722a02dd4f745e1f22cb9b8f956a44bac6c1` |
| `results/ge19_h4f3b_actual_corrected_six_piece_source_FULL.log` | 17898 | `1ec88fd3fd6b81bf30614b0cb78d722a02dd4f745e1f22cb9b8f956a44bac6c1` |
| `results/ge19_h4f3b_actual_corrected_six_piece_source.npz` | 30913364 | `787d5d177838b05078057aa932f379dd529449ce203f5664c36cf723acb0116b` |
| `results/ge19_H4F3B_LOCAL_runner.log` | 3180 | `411c72f0c54557c69883718082e030b1158cdb6fdfb6e1702abf45510e222179` |

The first two files are byte-identical. The outer runner reported the
same three inner-file hashes and the terminal marker
`GE19_H4F3B_ACTUAL_SIX_SOURCE_PASS_FULL_WARD_OPEN`.

All exact input-parent and source-code blob gates in the JSON were true.
The expected frozen Repair26 R1 bath trace SHA-256 was
`608ee0b4c868a701db6976f756b9a551cd9ddffe1e8e4ab37c5cd2361405a6f8`
at 26643162 bytes. Actual H3F/H3G/Z11/R13 input hashes in the JSON
equaled the preregistered hashes. This audit did not independently
rerun the source-generator calculation: it independently inspected
the exact user-provided local outputs.

## Independent stored-array and science-gate audit

- NPZ contains **146 fields**: 144 per-case source and Ward fields
  plus `x_primary` and `x_control`.
- All stored numeric arrays finite; numeric dtypes are float64 and complex128.
- All 18 C/beta/Nt cases have the expected
  8 GE19 source rows, modes 0..40 and Nt128/Nt64 temporal shapes.
- All six actual per-case source contributions exist:
  `2Q_GE06_cross`,
  `2Q_GE07_cross`,
  `2Q_Lambda_cross`,
  `2DY2_action_complete_Y_u_and_phi`,
  `2M1_GE05_mapped`,
  `2M2_GE05_mapped`.
- Direct independently computed maximum absolute discrepancy between
  saved total source and sum of its six saved pieces is **0.0**
  over all 18 cases.
- The nine stored controls at Nt128 and nine at Nt64
  meet all eight frozen science/source gates, with zero failed gates.
- Actual Stage E complete Y includes both u and phi raw RHS
  rows. Historical scalar-only Y was not consumed.
  Historical Repair27 q20 was not consumed.
- The exact certified Repair26 R1 first-order weighted q10 and
  H3G weighted z10 matched with reported relative L2 difference 0.0.
- GE06/GE07 mixed direct-swapped relative L2 max
  `2.0770354057402384e-14` (Nt128) and
  `1.500914820437318e-14` (Nt64).
- Lambda direct-vs-exact relative L2 max
  `1.9148071003126113e-16` (Nt128).
- Maximum saved **source-only** physical Ward absolute value:
  `3.610734858956584e-12` (Nt64);
  Nt128 maximum `4.3455270301029366e-13`.

**Critically, smallness of the source-only Ward expression was not
a pass gate**, and its being nonzero is not a Noether violation.
This test has not evaluated the linear-operator Ward term or the
complete signed background/H1/Z11/corrected Z20/q20/dust/bath
parent Euler residuals and boundaries.

## Exact implementation provenance and result boundary

- preregistration:
  `ge19/h4f3b_predata_actual_corrected_six_piece_source.json`,
  blob `c3362f5360c2a9951d77060027c82830c031c145`;
- unmodified actual local source module:
  `ge19/h4f3b_actual_corrected_six_piece_source.py`,
  blob `0423cbc64f6cda3b2a9aeb67c734935ef3ae7f9c`;
- original locked local runner:
  `ge19/run_local_h4f3b_actual_corrected_six_piece_source.sh`,
  blob `ef0fd6656add30cec667dda0d7bc9a435c3a2562`;
- physical source-Ward H*FD8/H*FD4 bridge:
  `ge19/h4f2h_physical_time_source_ward_bridge.py`,
  blob `65ce1e68a2f77e063c4bb8848d770abb4baeeebf`.

This result closes the previously documented absence of the original
Repair32B Z11 NPZ from the **conversation runtime**: the user's
separate local scientific environment supplied the exact hash-locked
certified Z11 parent and the actual H4F3B run passed its input locks.
The original certified Z11 binary is not automatically available in
GitHub Actions or attached to this conversation; do not conflate
that with the now valid H4F3B local output.

## Next licensed structural step

Use these immutable actual source rows and their exact physical
time grids as input to a new, separately preregistered **complete
linear-operator plus all-parent Euler/boundary H4 Ward evaluation**.
Retain the original canonical GE19 linear operator, exact
physical H*FD8/H*FD4 differentiation and existing C/beta/m/time
cohorts. The signed source term must be balanced against the
independent operator, all parent residuals and boundary contributions,
**not tested against zero in isolation**.

Before calling full H4F3 PASS, require the actual certified
H1/Z11/H3F Z20/H3G q20, dust/per-node bath residuals and
boundary data on the same representation. A full structural Ward
PASS may then license a separately preregistered Z21 science run;
it is not itself a Z21 PASS.

**Full H4 Noether not yet certified. Z21 NOT CERTIFIED.
Lensing blocked.**
