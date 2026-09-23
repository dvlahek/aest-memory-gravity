# GE19 Repair41 valid diagnostic — direct fine-grid target reference freeze

## Status

Repair41 completed successfully and is frozen as a valid diagnostic result.

Classification:

`GE19_REPAIR41_DIRECT_FINE_GRID_TARGET_SOURCE_RECONSTRUCTION_COMPLETE`.

Route:

`DIRECT_TARGET_REFERENCE_RESOLVED`.

Repair41 is diagnostic-only. It does not solve or certify Z21 and does not
license lensing.

## Frozen artifacts

JSON:

- bytes: `6799`;
- SHA-256:
  `1b18fede26b021e077ffe5c8b6b7ff0dc727b4defaab48e63491c86d868d1320`.

NPZ:

- bytes: `40744209`;
- SHA-256:
  `6bfb87ea21d55e2a1d2b16aee9bc8d7246111f91a064a78b74d2ed946ec2ba45`.

FULL log:

- bytes: `6799`;
- SHA-256:
  `1b18fede26b021e077ffe5c8b6b7ff0dc727b4defaab48e63491c86d868d1320`.

Outer runner log:

- bytes: `9930`;
- SHA-256:
  `8d9360c8bad9f7f7ed985957cf2230e0713715dd7057347feb10f31f5bee4375`.

Terminal marker:

`GE19_REPAIR41_DIAGNOSTIC_COMPLETE`.

## Integrity and direct-grid resolution

All implementation gates pass.

The Nt128 formula adapters reproduce both frozen Repair37 target pieces exactly:

- `2M1_GE05_mapped` relative L2 = `0.0`;
- `2Q_GE06_cross` relative L2 = `0.0`.

The original Nt128 factor-1 Radau stage coordinates are represented on both
fine grids with maximum absolute coordinate mismatch

`1.1102230246251565e-16`.

All direct Nt382 versus Nt763 inherited resolution gates pass:

- Z10 stage relative L2:
  `6.827917360174027e-08`;
- Z20 stage relative L2:
  `6.689744508124505e-08`;
- weighted z20 stage relative L2:
  `5.644520359737512e-07`;
- Z11 stage relative L2:
  `1.649473952142779e-05`;
- 2M1 stage-source relative L2:
  `6.169210815952087e-08`;
- 2Q_GE06 stage-source relative L2:
  `1.0122348516611055e-05`.

All are far below the inherited `5e-3` ceiling.

## Direct763 versus frozen Nt128 stage representations

### 2M1_GE05_mapped

- PCHIP versus direct763 relative L2:
  `2.104807968459713e-06`;
- Akima versus direct763 relative L2:
  `2.0255490463534962e-06`;
- closer frozen representation:
  `AKIMA`;
- PCHIP-to-Akima delta alignment with PCHIP-to-direct delta:
  `0.5236070119337672`;
- PCHIP-to-direct delta L2:
  `270.7435568006532`;
- PCHIP-to-Akima delta L2:
  `20.60131541747064`;
- direct763 L2:
  `128631001.4299223`.

Akima is only marginally closer in relative error. The frozen
PCHIP-to-Akima displacement is much smaller than the actual PCHIP-to-direct
displacement and is not a quantitatively faithful direct correction.

### 2Q_GE06_cross

- PCHIP versus direct763 relative L2:
  `1.1217479471594003e-05`;
- Akima versus direct763 relative L2:
  `1.1561946756579428e-05`;
- closer frozen representation:
  `PCHIP`;
- PCHIP-to-Akima delta alignment with PCHIP-to-direct delta:
  `-0.34747480302850875`;
- PCHIP-to-direct delta L2:
  `120134.18108398105`;
- PCHIP-to-Akima delta L2:
  `9661.904038081542`;
- direct763 L2:
  `10709452386.694689`.

For the shift-critical GE06 cross term, PCHIP is slightly closer to the
direct reference and the Akima displacement is anti-aligned with the true
PCHIP-to-direct correction. Therefore the Repair39 Akima response must not
be used as a proxy for the direct fine-grid correction.

## Interpretation

Repair41 resolves the direct target reference and removes the interpolation
ambiguity for the two mandatory Repair40 targets.

The next valid question is no longer which interpolant is preferable.

The next question is what happens to the H4 propagation when the frozen
PCHIP stage source is corrected by the directly reconstructed target values.

The direct target references are independently resolved on Nt382 and Nt763,
so both should be propagated in the next diagnostic to test threshold-side
stability without introducing a new arbitrary tolerance.

## Next licensed step

A separately preregistered Repair42 direct-target H4 propagation diagnostic:

- frozen Repair37 total source remains the baseline;
- factor-1 Repair07/Radau propagation is retained because Repair41 direct
  values are defined exactly at those stage coordinates;
- apply direct382 and direct763 corrections for:
  - 2M1_GE05_mapped only;
  - 2Q_GE06_cross only;
  - both targets together;
- preserve the frozen Repair37 projected p0 and active mask;
- require exact Repair37 baseline reproduction before interpretation;
- classify only by the existing 1e-6 science target:
  - both direct382 and direct763 combined corrections below target;
  - both above target;
  - or threshold-side disagreement.

Repair42 remains diagnostic-only and cannot certify Z21.

## Claim boundary

Repair41 does not certify Z21, finite eta, full-species nonlinear cosmology,
lensing or any observational signal.
