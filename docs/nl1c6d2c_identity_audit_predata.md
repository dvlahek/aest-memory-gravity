# NL1C6D2C identity audit — implementation predata

Status: **PREREGISTERED BEFORE FIRST NL1C6D2C COMPLETION-IDENTITY OUTPUT**.

This file refines only the deterministic coefficient/asymptotic audit already required by `docs/nl1c6d2c_predata_covariant_mixed_sector_completion.md`. It does not change the D2C completion family or any historical result.

Frozen subtest label:

```text
NL1C6D2C_COMPLETION_IDENTITY_AUDIT
```

This subtest cannot classify full D2C PASS. It only tests C1, the coefficient-level part of C2, C3, C4, and C5 before the action-level FLRW reduction is attempted.

## Frozen constants

Use exactly

```text
K_B = 0.0665
K2 = 9500
Q0 = 1e-4 Mpc^-1
Z0 = 1e-17 Mpc^-1
a0 = 1.2e-10 m s^-2
c = 299792458 m s^-1
Mpc = 3.085677581491367e22 m
epsilon_mix = 0.25
sigma = {-1,0,+1}
beta0 = {1.0,0.5,0.1}
kind = {simple,exponential,sharp}
```

Convert the MOND acceleration once to the geometric gradient scale

\[
a_{0,\rm geo}=a_0\,{\rm Mpc}/c^2
\]

in `Mpc^-1`.

## Frozen grids

For homogeneous-`Q` checks use

```text
Z_GRID = {-8,-4,-2,-1,0,+1,+2,+4,+8}
```

with

\[
Q=Q_0+Z_0 Z.
\]

For exact tracking/full-`J` checks use

```text
X_TRACK = {0,1e-8,1e-6,1e-4,1e-2,1,1e2,1e6,1e10}
```

with `Y = a0_geo^2 x^2` and `Z=0`.

For the small-gradient mixed-derivative and deep-MOND asymptotic checks use the decreasing ladder

```text
X_DEEP = {1e-2,3e-3,1e-3,3e-4,1e-4}
```

and evaluate the worst case over `Z_GRID`, `sigma=±1`, all three interpolation functions, and all three `beta0` values.

For the high-gradient bound use

```text
X_HIGH = 1e10
```

and all `Z_GRID` values.

## A1 — homogeneous identity C1

For all 27 completion/function/beta combinations and all `Z_GRID`, evaluate

\[
r_{\rm bg}=F_\sigma(0,Q)+2K_{\rm Exp}(Q).
\]

Normalize by

\[
S_{\rm bg}=(2-K_B)a_{0,\rm geo}^2+2|K_{\rm Exp}(Q)|.
\]

Gate:

```text
max |r_bg|/S_bg <= 1e-14
```

## A2 — mixed linear-invisibility coefficient

For the mixed term

\[
\Delta F_\sigma=\sigma\epsilon_{\rm mix}(2-K_B)\lambda_s
Y\tanh Z\frac{x^2}{1+x^2},
\]

define

\[
R_Y(x,Z)=
\frac{|\partial_Y\Delta F_\sigma|}
{(2-K_B)\lambda_s}.
\]

This quantity must tend to zero as `x -> 0` because the mixed term begins at `O(Y^2)`.

Requirements over `X_DEEP`:

```text
R_Y must decrease monotonically as x decreases
max R_Y at x=1e-4 <= 6e-9
```

This is only the coefficient-level C2 audit. The full frozen CLASS equation regression remains part of D2C-B and is not replaced by A2.

## A3 — exact tracking identity C3

At `Z=0`, for all `X_TRACK`, require

\[
r_{\rm track}=F_\sigma(Y,Q_0)-(2-K_B)J(Y).
\]

Normalize by

\[
S_{\rm track}=(2-K_B)\left[a_{0,\rm geo}^2+|J(Y)|\right].
\]

Gate:

```text
max |r_track|/S_track <= 1e-14
```

## A4 — deep-MOND subleading mixed term C4

For every nonzero `sigma`, define

\[
R_{\rm deep}=
\frac{|\Delta F_\sigma|}
{(2-K_B)|J(Y)|}.
\]

Use the worst case over `Z_GRID` and all co-primary `J/beta0` combinations.

Requirements:

```text
worst-case R_deep decreases monotonically as x decreases
worst-case R_deep at x=1e-4 <= 5e-4
```

No result may be used to move the deep ladder or relax the threshold.

## A5 — high-gradient sign/bound control C5

At `X_HIGH=1e10`, define the multiplicative control factor

\[
B_\sigma=1+\sigma\epsilon_{\rm mix}\tanh Z\frac{x^2}{1+x^2}.
\]

For every `Z_GRID` and `sigma`, require

```text
0.75 - 1e-12 <= B_sigma <= 1.25 + 1e-12
B_sigma > 0
```

The exact finite-grid extrema are reported.

## Subtest classification

All A1-A5 pass for all frozen combinations:

```text
NL1C6D2C_COMPLETION_IDENTITY_AUDIT_PASS
```

Otherwise:

```text
NL1C6D2C_COMPLETION_IDENTITY_AUDIT_FAIL
```

A subtest PASS only certifies the preregistered completion identities and asymptotics. It does not establish the action-derived nonlinear FLRW equations and does not authorize nonlinear branch evolution or NL1C7.
