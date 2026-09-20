# GE16 late-time standard-matter residual diagnostic — implementation lock

## Status

Implementation locked before first GE16 execution.

GE16 is diagnostic only. It does not run CLASS and does not accept any approximation.

## Parent provenance

Frozen parent:

`GE08_REPAIR01_FULL_FIRST_ORDER_STATE_BRIDGE_PASS_MATTER_INCOMPLETE`.

Artifact:

- ID `10598944561`;
- digest
  `sha256:d237aaf4b8f7314992de8dc1a0b432b4fb81eb80fe08352ac3f9d95cfc54982d`.

Frozen parent global diagnostics:

- pressure / density:
  `4.0296809261404915e-7`;
- shear / density:
  `5.717716788656946e-10`;
- standard density versus baryon-only relative L2:
  `1.3238516018121685e-3`.

## Preregistration

Commit:

`bde1aa3a2ce9f7c066d7f03afa9ed2bfe130c511`.

File:

`ge16/predata_late_time_standard_matter_residual_diagnostic.json`.

Frozen blob:

`334af2c5fd8b2e48bb6ef939c09bb1100bdda9d7`.

## Implementation

Commit:

`ecce5c7c025ccb3933e9b5916ed643fd55fb8404`.

File:

`ge16/late_time_standard_matter_residual_diagnostic.py`.

Frozen blob:

`b1bd494e0d01ea1b3f6354ecef8cd2452fe1f561`.

## Frozen definitions

Standard sector:

`CLASS total scalar stress - AeST effective-dark scalar stress`.

Matched effective dust:

- retain exact standard-sector `delta rho`;
- retain exact standard-sector momentum;
- set standard pressure to zero;
- set standard scalar shear to zero.

Baryon-only approximation:

- retain baryon density only;
- retain baryon momentum `rho_b theta_b`.

GE16 distinguishes these two approximations explicitly.

## Frozen outputs

Global, per-k and per-native-redshift diagnostics include:

- pressure / standard density;
- shear / standard density;
- pointwise pressure / density;
- pointwise shear / density;
- baryon-only density mismatch;
- baryon-only momentum mismatch;
- non-baryon residual density fraction;
- non-baryon residual momentum fraction;
- pressure / non-baryon residual density;
- shear / non-baryon residual density.

## Frozen gates

Require:

- exact artifact metadata/digest;
- exact parent classification;
- 48 selected rows;
- six k modes;
- eight native times;
- reproduction of the frozen GE08 global pressure ratio to absolute error <= `1e-15`;
- reproduction of the frozen GE08 global shear ratio to absolute error <= `1e-15`;
- reproduction of the frozen GE08 baryon-density mismatch to absolute error <= `1e-15`;
- all values finite.

## No approximation acceptance gate

GE16 contains no criterion saying the matched effective-dust approximation is acceptable.

Its result may inform a later separately locked model choice, but GE16 itself cannot license that choice.

## Terminal classes

Pass:

`GE16_LATE_TIME_STANDARD_MATTER_RESIDUAL_DIAGNOSTIC_PASS`.

Fail:

`GE16_LATE_TIME_STANDARD_MATTER_RESIDUAL_DIAGNOSTIC_FAIL`.

## Claim boundary

Even PASS does not:

- accept a dust truncation;
- change GE08;
- license `Z20`;
- introduce finite eta;
- make a nonlinear-collapse or observational claim.
