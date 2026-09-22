# GE19 Repair34 canonical H4/Z21 — implementation lock

## Status

Repair34 is frozen before any science result.

Repair33 remains the historical first valid H4/Z21 FAIL and is not relabelled.

Repair34 changes no H4 physics. It corrects only two implementation-level
mismatches localized from Repair33:

1. subtractive floating-point cancellation in the Q-cross polarization audit;
2. use of the historical all-time sparse BVP path instead of the certified
   H3 canonical particular-state boundary/propagator.

## Frozen preregistration

File:

`ge19/repair34_predata_canonical_window_local_reduced_h4_z21_particular.json`.

Blob:

`5653c99b4fc20fd4ccc286ac0aed6c54a8411185`.

Commit:

`701dce93ad30303b368de840955368027edd1271`.

## Frozen implementation

File:

`ge19/repair34_canonical_window_local_reduced_h4_z21_particular.py`.

Blob:

`f2171a630c2e41055dd966e6dd3ab39cb7839e3b`.

Commit:

`7740a1479e7499ff25e8d8dc006279cd061e76f9`.

Global static audit:

- run:
  `35778827363`;
- conclusion:
  `success`.

## Repair33 localization parent

File:

`docs/ge19_repair33_h4_z21_fail_localization_freeze.md`.

Blob:

`434309199eb58901aa1c0ad6e3f96a6656d72389`.

Commit:

`34c7747f12e06b49aa660c4251409d593702f339`.

Frozen Repair33 science result:

- JSON SHA-256:
  `62da23947b59ae0ee20b858ee2dcbf394e6dcb91b85b0faae07fa5bf91366f07`;
- NPZ SHA-256:
  `80fbd027b8392bed25beb6ebd7111507be36c24d5f21a1ba218c9e3594bec407`.

## Dedicated Repair34 prelock

Workflow:

`.github/workflows/ge19-repair34-prelock-audit.yml`.

Blob:

`c47f9b9799f6c70f3ffc22735da7558da87f72da`.

Workflow commit:

`dd7e82105d9b3b393a62a576b3c87694c2912455`.

Run:

`35778912256`.

Job:

`106919065341`.

Conclusion:

`success`.

The prelock verifies:

- unchanged H4 equation;
- unchanged GE05->GE06 factor two;
- unchanged source-construction functions;
- unchanged grids and source thresholds;
- absence of observational/finite-eta input;
- exact use of Repair18 projected momentum boundary;
- exact use of Repair07 canonical Radau IIA march and canonical reconstruction;
- absence of the historical `r7.solve_case(...)` BVP path;
- deterministic norm-balanced Q polarization;
- mu=1 versus mu=0.5 consistency on a deliberately scale-separated toy
  quadratic direction.

## Frozen H4 equation

`L_GE06 Z21 = -2 Q_total(Z10,Z11) - 2 DY2[Z10;Z11] - 2 M1_GE05[Z20,q20] - 2 M2_GE05[(Z10,q10),(Z10,q10)]`.

No source formula or physical coefficient changes relative to Repair33.

## Balanced Q polarization

For each frozen (Nt,C) parent pair:

- `n10=sqrt(||Z10||^2+||Z10dot||^2)`;
- `n11=sqrt(||Z11||^2+||Z11dot||^2)`;
- `A=Z10/n10`;
- `B=Z11/n11`.

Then

`Qcross = n10*n11 * [Q2(A+mu B)-Q2(A-mu B)]/(4 mu)`.

Primary `mu=1`; control `mu=0.5`.

This is algebraically identical to the quadratic polarization used in
Repair33. It only balances floating-point magnitudes before subtraction.

## Canonical particular-state boundary

Repair34 restores the exact convention inherited by the Repair22-certified
H3/Z20 state:

- canonical coordinates:
  `q0=(S,u,phi,T)=0`;
- canonical momenta:
  Repair18 doubly equilibrated minimum-norm lapse+shift projection;
- propagation:
  Repair07 two-stage Radau IIA canonical march;
- reconstruction:
  Repair07 canonical algebraic reconstruction.

The boundary audit therefore checks q0, projected-momentum residual,
lapse/shift backward errors and algebraic closure. It does not require the
source-forced canonical momenta/time derivatives to vanish.

## Frozen gates

- balanced Q polarization <= 1e-12;
- DY2 Nx1024/Nx2048 <= 5e-4;
- total H4 source Nx1024/Nx2048 <= 5e-4;
- memory source Nq1024/Nq2048 <= 1e-2;
- total H4 source Nt64/Nt128 <= 5e-3;
- canonical Radau/algebraic/lapse residual <= 1e-8;
- H4 state Nt128/Nt64 <= 5e-3;
- shift backward error <= 1e-6;
- anisotropy backward error <= 1e-6;
- boundary q0 <= 1e-12;
- boundary projected-momentum residual <= 1e-8;
- boundary lapse backward error <= 1e-6;
- boundary shift backward error <= 1e-6;
- boundary algebraic residual <= 1e-8;
- all source/state outputs finite.

## Stop rule

The first Repair34 execution that emits a valid Repair34 science JSON is
frozen as PASS or FAIL.

Implementation/execution failures before a valid science JSON may be repaired
without changing this contract.

A PASS certifies only the canonical window-local particular reduced Z21 state.
