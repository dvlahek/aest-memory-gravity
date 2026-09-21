# GE19 Repair14 self-consistent reduced-H3 Z20 implementation lock

## Status

**IMPLEMENTATION LOCKED BEFORE REPAIR14 LOCAL SCIENCE EXECUTION**

Repair13 remains the frozen certified H1 parent.

Repair14 is the first H3/Z20 attempt licensed after the Repair13 self-consistent reduced-background PASS.

## Parent Repair13 result freeze

Commit:

`5461f89f77f91e931f14abb6a2e5014597e0cb6f`

File:

`docs/ge19_repair13_reduced_background_h1_result_freeze.md`

Blob:

`06530bf2df460c27c48e4fca4bd6e089dd839137`

Frozen Repair13 local outputs:

- JSON SHA-256 `ae3cc790ecffbd5498b5852273c72ae578d4615de29bbb616673c05cdb3e74b7`;
- NPZ SHA-256 `011c0ae54fd21d70c0e2c695ce62e7b74a3c5529a07c9023c882a447d5b40ca3`.

Repair13 classification:

`GE19_REPAIR13_SELF_CONSISTENT_REDUCED_BACKGROUND_H1_RECLOSURE_PASS`.

## Repair14 preregistration

Commit:

`83faed57a2f49a30a1a0010995e1966cc49aebb6`

File:

`ge19/repair14_predata_self_consistent_reduced_h3_z20_particular.json`

Blob:

`abf5b794ac4d53c2098bf596247f996cb07fa6c2`

## Repair14 implementation

Commit:

`5a969ff0dc00b8683fe239733ae25c935c2b8f70`

File:

`ge19/repair14_self_consistent_reduced_h3_z20_particular.py`

Blob:

`06c5ced952c2370cfa4aaadb6ef8f72d2d7221de`

The implementation:

- loads the frozen Repair13 Z10 primary/control arrays from the parent NPZ;
- does not call either reduced-H1 solver;
- reconstructs only the deterministic Repair13 homogeneous reduced background;
- verifies the reconstructed H(a) against the frozen Repair13 NPZ;
- installs the exact locked Repair11 first-directional Lambda operator;
- adds the exact Lambda second-directional metric source;
- computes Nx=1024/2048 H3 source convergence;
- solves the window-retarded Z20 particular state for m=1..40;
- repeats the solve on Nt=32 as the frozen time-grid control.

## Frozen H3 equation

`L_total Z20 = -Q_total(Z10,Z10) - 2 Y2[Z10]`.

The total quadratic analytic equation source is

`Q_total = Q_Einstein+AeST + Q_dust + Q_lambda`.

## Exact Lambda second-directional source

Frozen action:

`L_lambda = -6 rho_lambda N L R^2`.

Common gauge direction:

`N=1+eps N1`, `L=a+eps S1`, `R=a+eps S1`.

Exact second directional equation coefficients:

- lapse:
  `delta2 E_N^lambda = -36 rho_lambda a S1^2`;
- longitudinal scale:
  `delta2 E_L^lambda = -24 rho_lambda a N1 S1 -12 rho_lambda S1^2`;
- transverse scale:
  `delta2 E_R^lambda = -48 rho_lambda a N1 S1 -24 rho_lambda S1^2`;
- isotropic:
  `delta2(E_L+E_R)^lambda = -72 rho_lambda a N1 S1 -36 rho_lambda S1^2`;
- anisotropy:
  `0`;
- shift:
  `0`.

The H3 RHS uses the frozen sign

`-Q_lambda`.

No factor 1/2 is inserted because GE06/GE07 `f_c2` use the literal second common-direction derivative.

## Final executable prelock audit

Workflow:

`.github/workflows/ge19-repair14-prelock-audit.yml`

Final workflow commit:

`3ad4572442bf0a08d465ed63111b8d59cfcc133a`

Workflow blob:

`70ca950c5ead671be8e62f681bc43a0ddaae6cd6`

GitHub Actions run:

`35598797189`

Job:

`106329706444`

Conclusion:

`success`

Terminal marker:

`GE19_REPAIR14_PRELOCK_AUDIT_PASS`

Independent symbolic outputs:

- `LAMBDA_EN_C2 = -36*S1**2*a*rho`;
- `LAMBDA_EL_C2 = -24*N1*S1*a*rho - 12*S1**2*rho`;
- `LAMBDA_ER_C2 = -48*N1*S1*a*rho - 24*S1**2*rho`;
- `LAMBDA_ISO_C2 = -72*N1*S1*a*rho - 36*S1**2*rho`;
- `LAMBDA_ANISO_C2 = 0`;
- `LAMBDA_SHIFT_C2 = 0`.

The first prelock run `35598646781` failed only because its numerical self-audit compared algebraically identical floating-point expressions generated with different multiplication order under an unrealistically exact `rtol=0, atol=1e-30` check. The science implementation was not changed. The corrected prelock uses identical arithmetic ordering and bitwise equality.

## Frozen grids and cases

- C: `C_min,C_star,C_max`;
- beta0: `1.0,0.5,0.1`;
- H1 input modes: `3,5,8,10,15,20`;
- H3 solved modes: `m=1..40`;
- Nt primary/control: `64/32`;
- Nx primary/control: `1024/2048`;
- m=0: source report only.

## Frozen window-retarded convention

At z=1.5:

- `S20=u20=phi20=T20=0`;
- their cosmic-time derivatives are zero.

This selects one window-local particular solution. It does not select or certify the primordial/homogeneous second-order mode.

## Unchanged Stage-B gates

- Nx1024/Nx2048 low-mode source relative L2 <= `5e-4`;
- primary canonical/linear residual <= `1e-8`;
- shift constraint backward error <= `1e-6`;
- anisotropy constraint backward error <= `1e-6`;
- primary64/control32 state relative L2 <= `5e-3`;
- all three beta0 and all three C cases complete;
- all outputs finite.

No threshold is relaxed.

## Stop rule

If Repair14 fails any frozen Stage-B gate, Z20 is not certified and q20/H4/Z21 remain unlicensed.

If Repair14 passes all gates, the result must be frozen before any q20 or H4/Z21 construction.

## Claim boundary

A Repair14 PASS certifies only the low-mode window-retarded reduced-H3 particular directional state on the Repair13 self-consistent AeST+dust+Lambda background.

It does not certify the omitted homogeneous/primordial Z20 solution, full standard species, finite eta, finite physical-amplitude nonlinear evolution, collapse, lensing or observations.
