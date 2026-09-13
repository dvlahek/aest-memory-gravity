# Full-J direct-CLASS spectral-fringe k-list serialization repair

Date: 2026-09-13

## Historical incomplete attempt

The R2 transfer-input repair passed all ancestry, provenance and transfer-only input checks and reached the first direct science calculation

`FULLJ_DIRECT_CLASS_FRINGE_RUN aest_dense_51`.

CLASS completed far enough for `get_perturbations()` to return scalar histories, but the wrapper returned 49 histories although the frozen dense grid contains 51 requested k values. The run stopped immediately at the explicit cardinality assertion and therefore produced no complete AeST-dense array, no AeST-sparse array, no GR-dense array, and no DG-G2 through DG-G6 science statistics.

The historical classification remains

`FULLJ_CORRECTED_CLASS_SPECTRAL_FRINGE_INCOMPLETE`.

## Diagnosis

The dense requested-k string was serialized with 17 significant digits:

`", ".join(f"{x*h:.17g}" for x in K_DENSE)`.

For the frozen 51-point grid this produces a 1080-character value string. Frozen CLASS v3.3.4 defines

`_ARGUMENT_LENGTH_MAX_ = 1024`

for each parser argument. The first 1023 characters of the 17-digit dense string contain exactly 49 comma-separated fields. This reproduces the observed history count `49` and identifies the failure as an input-value serialization-length defect.

The underlying frozen physical grid itself remains 51 unique values. No evidence from this incomplete launch is interpreted as requested-k-list dependence, a CLASS perturbation-history physics effect, or a failure of DG-G3.

## Frozen technical repair

Before any new direct fine-grid AeST/GR spectrum is inspected, the repair is fixed as follows:

1. Preserve the original direct-CLASS preregistration unchanged, including the 51-point dense grid, 15 anchors, three windows, all redshifts, all thresholds, DG-G1 through DG-G6, and all classifications.
2. Preserve the historical provenance-INCOMPLETE, transfer-input-INCOMPLETE, and present serialization-INCOMPLETE launches unchanged.
3. Preserve the validated transfer-only repair: `output = mTk,vTk` and removal of inherited `l_max_scalars`.
4. Serialize only the CLASS `k_output_values` text representation with 15 significant digits instead of 17.
5. Require the complete 51-point serialized string length to be strictly below 1024 characters before calling `Class.set()`.
6. Require the serialized dense string to contain exactly 51 comma-separated values and the serialized sparse string exactly 15.
7. Parse the serialized values back to floating point before the CLASS call and require the maximum absolute displacement in physical `k/h` from the frozen grid to be <= `1e-12 h/Mpc`.
8. Keep the actual frozen Python arrays `K_DENSE`, `K_ANCHOR`, the window spacing `Delta k/h=0.000625`, all redshifts, and all science calculations unchanged.

For the frozen dense grid the 15-significant-digit serialization has length 982 characters and a maximum physical `k/h` displacement of about `7.3e-16 h/Mpc`, far below the frozen tolerance and many orders below the grid spacing.

No CLASS equation, CLASS source patch, cosmological parameter, AeST parameter, memory setting, physical requested-k grid, redshift, interpolation rule, observable definition, science threshold, gate, or classification rule is changed.

## Interpretation rule

Only after the repaired serialization returns all 51 AeST-dense histories, all 15 AeST-sparse histories and all 51 GR-dense histories may the original DG-G1 through DG-G6 statistics be evaluated. A failure before those three calculations complete remains `FULLJ_CORRECTED_CLASS_SPECTRAL_FRINGE_INCOMPLETE` unless an original preregistered science rule explicitly applies.
