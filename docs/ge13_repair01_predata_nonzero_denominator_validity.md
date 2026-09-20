# GE13 Repair01 predata — nonzero-denominator validity repair

## Status

Implementation-only repair preregistration after the frozen classification

`GE13_PRE_SCIENCE_DYNAMIC_RANGE_IMPLEMENTATION_FAIL`.

No GE13 science classification exists yet.

## Frozen cause

The locked GE13 implementation defined a valid alpha-ratio sample using a
global amplitude-relative floor,

`|alpha_R1| > max(max|alpha_R1|*1e-15,1e-300)`.

Because alpha spans many orders of magnitude over the frozen history, this
excluded finite nonzero early-time samples and made one preregistered history
bin empty before science evaluation.

## Licensed change

Change only the validity rule to

`isfinite(alpha_R1) & isfinite(alpha_R2) & (abs(alpha_R1)>1e-300)`.

No ratio definition changes.

No threshold changes.

No history-grid changes.

No bin changes.

No parent artifact changes.

No CLASS run is added.

## Frozen science contract

Unchanged:

- GE11 Repair01 parent artifact and dense-trace hashes;
- GE12 parent artifact and classification;
- frozen k set;
- channels
  `alpha_aest,E_aest,chi,ut_kernel`;
- 4096 common ln(a) history samples per k;
- departure thresholds
  `{1e-3,1e-2,0.05,0.10}`;
- 16 equal-ln(a) history bins;
- GE12 late-scale reproduction to `1e-12`;
- frozen IC source identities;
- all diagnostic gates and claim boundaries.

## Terminal classifications

The first locked Repair01 execution may classify only as:

- `GE13_AEST_MODE_AMPLITUDE_ONSET_LOCALIZED`;
- `GE13_AEST_MODE_AMPLITUDE_ONSET_DIAGNOSTIC_FAIL`.

## Boundary

Repair01 cannot:

- relabel GE11 or GE12;
- select R1 or R2;
- add R3;
- alter ICs;
- change any onset threshold;
- claim a physical instability;
- license Z20.
