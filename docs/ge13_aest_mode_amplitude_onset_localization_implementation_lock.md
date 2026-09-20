# GE13 AeST mode-amplitude onset localization — implementation lock

## Status

Implementation locked before the first GE13 execution.

GE13 is diagnostic only and executes no CLASS run.

## Frozen parents

GE11 Repair01:

- classification:
  `GE11_REPAIR01_DENSE_LOCAL_JET_FIXED_REFINEMENT_FAIL`;
- workflow run:
  `35497478790`;
- artifact ID:
  `10600652596`;
- artifact digest:
  `sha256:b35a3a0c8bbd22483bd04c006b20ceb97d3c7f263e178382026cba2983628ecc`.

GE12:

- classification:
  `GE12_GE11_R1_R2_STATE_DIVERGENCE_LOCALIZED`;
- workflow run:
  `35500848748`;
- artifact ID:
  `10602610942`;
- artifact digest:
  `sha256:2b44a0c38d1a3aadcb05f1ed743560a68817e720dcb4d2cc41fe040d0b409fd9`.

## Preregistration

Commit:

`656457deeede91d08aced160e452d7577711de50`.

File:

`ge13/predata_aest_mode_amplitude_onset_localization.json`.

Frozen blob:

`43f656b077d517acf3fe01b37c303db5dec00de5`.

## Implementation

Commit:

`1f619e0b2a7a00764bd8d0ba0c9260fc327cf23f`.

File:

`ge13/aest_mode_amplitude_onset_localization.py`.

Frozen blob:

`f1fdc8c71452f49ed06e1e329a6ab1d2b7d1d874`.

## Frozen late-window diagnostic

Use the GE12 NPZ directly for

- `alpha_aest`;
- `E_aest`;
- `chi`;
- `ut_kernel`.

For each k report:

- least-squares R2/R1 scale;
- post-rescaling relative L2;
- cosine.

The implementation also reproduces the frozen GE12 global scale fits and requires agreement within `1e-12`.

## Frozen full-history diagnostic

For each frozen k mode:

- read the complete R1/R2 accepted-step trace;
- build the same derivative-aware CubicHermite alpha interpolation;
- build the same PCHIP background H interpolation;
- evaluate on 4096 uniform ln(a) samples from the later first accepted endpoint to
  `a=1/(1+0.2)`.

Report the first point where

`|alpha_R2/alpha_R1 - 1|`

exceeds exactly

- `1e-3`;
- `1e-2`;
- `0.05`;
- `0.10`.

At each crossing report

- a;
- z;
- R2/R1 alpha ratio;
- `k/(aH)`.

Also report 16 equal-ln(a) bin scale fits.

## Frozen IC provenance audit

Require the historical v0.19i source to contain exactly the intended leading adiabatic identities:

- `alpha_i=-a theta_i/k^2`;
- `E_i=0`;
- `delta_A=(1+w_A)delta_c`.

This is provenance only.

It does not certify omitted finite-gradient terms.

## Frozen gates

Require:

- exact GE11 artifact metadata;
- exact GE12 artifact metadata;
- exact parent classifications;
- exact dense trace hashes;
- GE12 global scale reproduction within `1e-12`;
- finite common-history interpolation;
- exact frozen IC source identities present;
- all outputs finite.

No onset time, per-k amplitude factor, residual or `k/(aH)` value is a PASS gate.

## Terminal classifications

Pass:

`GE13_AEST_MODE_AMPLITUDE_ONSET_LOCALIZED`.

Fail:

`GE13_AEST_MODE_AMPLITUDE_ONSET_DIAGNOSTIC_FAIL`.

## Claim boundary

GE13 cannot:

- relabel GE11;
- select R1 or R2;
- add R3;
- alter precision values;
- modify initial conditions;
- claim a physical instability;
- license `Z20`.
