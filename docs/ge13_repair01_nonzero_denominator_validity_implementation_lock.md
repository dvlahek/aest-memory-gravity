# GE13 Repair01 nonzero-denominator validity — implementation lock

## Status

Implementation locked before the first Repair01 execution.

Historical parent outcome remains:

`GE13_PRE_SCIENCE_DYNAMIC_RANGE_IMPLEMENTATION_FAIL`.

No GE13 science classification exists yet.

## Repair01 preregistration

Commit:

`d1967f5f3bb89eee3739c5b069f020c2ea6b250b`.

File:

`docs/ge13_repair01_predata_nonzero_denominator_validity.md`.

Frozen blob:

`711b2f65b77ef647cc6a95f78c1922c2587bbf64`.

## Repair01 implementation

Commit:

`28606dc93925c2ec02e78c5a6dee09ed6237b152`.

File:

`ge13/aest_mode_amplitude_onset_localization.py`.

Frozen blob:

`0f5498d401502869d9613a52a9dee03456e67e13`.

## Exact source change

The only GE13 science-code change relative to the historical locked implementation is:

from

`floor=max(max|alpha_R1|*1e-15,1e-300); valid=|alpha_R1|>floor`

to

`valid=isfinite(alpha_R1) & isfinite(alpha_R2) & (|alpha_R1|>1e-300)`.

No other source line changed.

## Frozen parent artifacts

Unchanged:

- GE11 Repair01 artifact ID `10600652596`;
- GE11 digest
  `sha256:b35a3a0c8bbd22483bd04c006b20ceb97d3c7f263e178382026cba2983628ecc`;
- GE12 artifact ID `10602610942`;
- GE12 digest
  `sha256:2b44a0c38d1a3aadcb05f1ed743560a68817e720dcb4d2cc41fe040d0b409fd9`.

## Frozen science contract

Unchanged:

- six k modes;
- channels `alpha_aest,E_aest,chi,ut_kernel`;
- 4096 common ln(a) history samples per k;
- onset thresholds `{1e-3,1e-2,0.05,0.10}`;
- 16 equal-ln(a) bins;
- GE12 late-scale reproduction to `1e-12`;
- exact retained IC source identities;
- all provenance/reconstruction gates;
- claim boundary.

## Terminal classifications

The first lock-aware Repair01 execution may classify only as:

- `GE13_AEST_MODE_AMPLITUDE_ONSET_LOCALIZED`;
- `GE13_AEST_MODE_AMPLITUDE_ONSET_DIAGNOSTIC_FAIL`.

## Project boundary

Repair01 cannot:

- relabel GE11/GE12;
- select R1/R2;
- add R3;
- alter ICs or precision;
- change onset thresholds;
- claim a physical instability;
- license Z20.
