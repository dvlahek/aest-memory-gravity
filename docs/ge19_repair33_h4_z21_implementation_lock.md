# GE19 Repair33 window-local H4/Z21 — implementation lock

## Status

Repair33 implementation is frozen before any science result.

Target:

`GE19_REPAIR33_WINDOW_LOCAL_REDUCED_H4_Z21_PARTICULAR_PASS/FAIL`.

Repair33 constructs only the window-local particular reduced H4/Z21 state.
It does not choose a primordial homogeneous Z21 mode, introduce finite eta,
use observational data, or certify a full-species nonlinear cosmology.

## Frozen preregistration

File:

`ge19/repair33_predata_window_local_reduced_h4_z21_particular.json`.

Blob:

`f1c646e3011193b7df61014365e985b47ad8e0b4`.

Commit:

`b98af3f09a3adcca779f27fd19c9f8d78fa3b814`.

## Frozen implementation

File:

`ge19/repair33_window_local_reduced_h4_z21_particular.py`.

Blob:

`6863f6dd1f8d22acb9f891659ded34abbb747763`.

Commit:

`9534debc82d2d2a50c832f400754ea2feee866c0`.

Global static audit:

- run:
  `35766941122`;
- conclusion:
  `success`.

## Dedicated H4 prelock

Workflow:

`.github/workflows/ge19-repair33-prelock-audit.yml`.

Blob:

`4e022a0050a7be1b69895343915f6300fd019475`.

Workflow commit:

`2642bb65f47d90732b4c359d8a4004e2c278b60e`.

Run:

`35767062116`.

Job:

`106879161705`.

Conclusion:

`success`.

The prelock verifies the exact four-block H4 hierarchy, the GE05->GE06
dictionary factor, zero-homogeneous H4 boundary, direct-script invocation,
and the absence of finite-eta or observational input.

## Frozen H4 hierarchy

The common GE06 raw-residual equation is

`L_GE06 Z21 = -2 Q_total(Z10,Z11) - 2 DY2[Z10;Z11] - 2 M1_GE05[Z20,q20] - 2 M2_GE05[(Z10,q10),(Z10,q10)]`.

The GE05 memory blocks are mapped with the exact Repair32A factor:

`GE05_M1/M2 -> 2 * GE05_M1/M2`.

This is a convention conversion derived from the action, not a fitted
normalization.

## Frozen parents

Repair22:
- Z10;
- window-local particular Z20.

Repair27:
- q10 weighted projection;
- q20 weighted projection;
- deterministic normalized-bath reconstruction.

Repair32B/32C:
- exact reduced Z11 arrays;
- formal Z11 certification and H4 license.

GE04:
- high-resolution DY2 representation.

GE05:
- action-derived M1/M2 memory residuals.

GE06/GE07:
- memory-off AeST and pressureless-dust L/Q operator conventions.

## Source implementation

### Memory-off Q cross

The cross bilinear is formed by exact polarization:

`Q(Z10,Z11)=[Q2(Z10+Z11)-Q2(Z10-Z11)]/4`.

A lambda=1 versus lambda=0.5 polarization self-consistency audit is frozen.

### DY2

The nonanalytic Y-sector directional derivative is reconstructed from the
certified reduced X10 and X11 directions.

Only this nonanalytic block requires the high-resolution spatial pair
Nx1024/Nx2048.

### M1

After summing bath nodes, GE05 M1 depends only on the certified second-order
bath mismatch

`B20 = X20 - sum_j w_j z20_j`.

The implementation still reconstructs the exact Repair27 bath parent through
the frozen Repair24 core and checks the reconstructed weighted projections
against the frozen Repair27 NPZ.

### M2

GE05 M2 is evaluated from the reconstructed per-node q10 state and the
certified reduced Z10 state, then summed over bath nodes before the exact
GE05->GE06 factor-two map.

## Polynomial spatial grid

GE06/GE07 Q and GE05 M1/M2 are polynomial blocks generated from first-order
input modes with maximum mode 20, hence their generated support is bounded by
m<=40. They are evaluated on an exact band-limited polynomial grid.

The preregistered Nx1024/Nx2048 spatial science control is applied to the
nonanalytic DY2 block and therefore to the assembled low-mode H4 source.

## Frozen science gates

- parent hashes/classifications exact;
- Repair32C Z11 certified and H4 licensed;
- GE05->GE06 factor exactly 2 with no fit;
- Q polarization self-consistency <= 1e-12;
- DY2 Nx1024/Nx2048 <= 5e-4;
- total H4 source Nx1024/Nx2048 <= 5e-4;
- memory source Nq1024/Nq2048 <= 1e-2;
- total H4 source Nt64/Nt128 <= 5e-3;
- H4 linear-system residual <= 1e-8;
- H4 state Nt64/Nt128 global relative L2 <= 5e-3;
- global shift / operator scale <= 1e-6;
- global anisotropy / operator scale <= 1e-6;
- zero dynamic H4 boundary <= 1e-12;
- all source/state outputs finite.

No threshold may be changed after the first valid Repair33 science result.

## Stop rule

The first execution that emits a valid Repair33 JSON is frozen as PASS or
FAIL.

Implementation/execution failures before a valid science JSON may be repaired
without changing the frozen science contract.

A PASS certifies only the window-local particular Z21 state and licenses a
separately preregistered lensing-facing observable calculation.
