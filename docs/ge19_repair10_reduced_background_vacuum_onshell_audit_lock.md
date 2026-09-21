# GE19 Repair10 reduced-background vacuum on-shell audit lock

## Status

**DIAGNOSTIC IMPLEMENTATION LOCKED BEFORE REPAIR10 RESULT**

Repair08 and Repair09 remain frozen.

No Lambda term has yet been added to the GE19 H1/H3 operator.

## Parent results

Repair08 result freeze:

- commit `f08f3d076e58240766afa21df5df6b927146d67c`;
- blob `9f2661fee8eb6a0efad805644ecdf370b0fb60ba`.

Repair09 structural result freeze:

- commit `c0d0fe65e63eeaabcbe0ddd2a49e336089fe2097`;
- blob `b8fc626881cdd57624b8afff01b3d88338e61715`.

## Repair10 preregistration

Commit:

`2b87fcfe87a7b40455ca64b0f824c66fb4fc63fa`

File:

`ge19/repair10_predata_reduced_background_vacuum_onshell_audit.json`

Blob:

`fc7759463c5c84667872971e763b91824298fbc3`

## Diagnostic implementation

Commit:

`9be665966061f0673e6f4a8e1761d1d14b4f2857`

File:

`ge19/repair10_reduced_background_vacuum_onshell_audit.py`

Blob:

`2487b809a55bc8a3d87c5add89fe4eb6372f88c6`

## Executable prelock audit

Workflow commit:

`371e30a88d62b6d799197695be99c3e8d1eed581`

Workflow:

`.github/workflows/ge19-repair10-prelock-audit.yml`

Blob:

`15b08d663dd75537c416ada8bd9d131a8d90f269`

Run:

`35566975098`

Job:

`106230653908`

Conclusion:

`success`

Markers:

- `GE19_REPAIR10_PREREG_AUDIT_PASS`
- `GE19_REPAIR10_ACTION_AUDIT_PASS`
- `GE19_REPAIR10_IMPORT_PASS`

## Exact homogeneous action identities

The prelock derives directly from the frozen GE06 action:

`GE06_HOMOGENEOUS_LAPSE = 2*a*(K*a**2 - KQ*Q*a**2 + 3*adot**2)`

and

`GE06_HOMOGENEOUS_SCALE = 2*K*a**2 + 4*a*addot + 2*adot**2`.

Thus

`E_N/(2 a^3) = 3 H^2 - (Q KQ - K)`

and the CLASS-normalized non-AeST density required by the GE06 background equation is

`rho_req = [3 H^2 - (Q KQ-K)]/3`.

The non-AeST pressure required by the longitudinal metric equation is

`p_req = -E_L/(6 a^2)`.

## Exact Lambda normalization

In the frozen GE06 normalization,

`L_lambda = -6 rho_lambda N L R^2`.

Its homogeneous Euler contributions are exactly

- lapse: `-6 a^3 rho_lambda`;
- longitudinal scale: `-6 a^2 rho_lambda`;
- transverse scale: `-12 a^2 rho_lambda`;
- shift: `0`.

This is fixed before the Repair10 numerical result.

## Frozen comparisons

Repair10 compares the same required non-AeST background against:

1. current reduced matter:
   `rho=C/a^3, p=0`;
2. current reduced matter plus frozen CLASS Lambda:
   `rho=C/a^3+rho_lambda, p=-rho_lambda`;
3. complete known non-AeST CLASS background:
   `rho=rho_std+rho_lambda, p=p_std-rho_lambda`.

Here

`rho_std=rho_b+rho_g+rho_ur+rho_ncdm[0]`

and

`p_std=rho_g/3+rho_ur/3+p_ncdm[0]`.

## Predeclared controls

- stable AeST native reconstruction: unchanged Repair07 gates;
- full-known density closure relative L2 <= `5e-5`;
- full-known pressure closure relative L2 <= `5e-3`;
- Lambda dominance reference improvement factor: `10`;
- all outputs finite.

No threshold may be changed after the result.

## Claim boundary

Repair10 is background/action diagnosis only.

It does not add Lambda to the linear operator, reclose H1, construct H3/Z20, introduce finite eta, or make nonlinear/observational claims.
