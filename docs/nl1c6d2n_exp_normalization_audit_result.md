# NL1C6D2N result — corrected Exp normalization audit

Status: **LOCKED RESULT**.

Classification:

```text
NL1C6D2N_EXP_NORMALIZATION_AUDIT_PASS
```

Result-producing branch and head:

```text
v053-exp-normalization-corrected
e13633549ac7a20b51389d21c4e23791ec1c0772
```

The corrected Exp homogeneous sector is

\[
K=K_2 Z_0^2(e^{Z^2}-1),\qquad
K_Q=2K_2Z_0Ze^{Z^2},\qquad
K_{QQ}=2K_2e^{Z^2}(1+2Z^2).
\]

The inverse background variable uses

\[
Z e^{Z^2}=K_Q/(2K_2Z_0).
\]

All preregistered N1-N6 gates passed.

## N1 — exact local curvature

At `Z=0`:

```text
K = 0
KQ = 0
KQQ = 19000 = 2*K2
KQQ/(2*K2) = 1
```

and

```text
mu2_reference = 9.826739074217741e-05 Mpc^-2
mu2_from_curvature = 9.826739074217741e-05 Mpc^-2
relative error = 0
```

This restores exact consistency with the frozen D1A/R3 weak-field mass normalization while retaining `K2=9500`.

## N2 — quadratic small-Z limit

The relative deviation from `K2 (Q-Q0)^2` decreases monotonically for both signs of `Z`. At `|Z|=1e-3`:

```text
relative error = 5.000001668253873e-07
frozen gate    = 1e-6
```

PASS.

## N3 — derivative and parity consistency

```text
max KQ relative error   = 1.4226805987449831e-12
max KQQ relative error  = 7.954855576201724e-09
max parity error        = 0
```

against gates `2e-7`, `2e-5`, and `1e-14`, respectively.

PASS.

## N4 — positive-branch forward/inverse consistency

For the preregistered positive cosmological charge branch `Z={0.1,1,2,4}`:

```text
max normalized recovery error = 0
```

against gate `1e-12`.

PASS.

## N5 — background charge law and a=1 calibration

The calibrated present-day value is

```text
Z(a=1) = 4.469057123516087
I0     = 0.00040077784067420186
```

The maximum shift-charge mismatch over `a={1,0.8,0.5,0.3,0.2,1/7}` is

```text
4.432273092773803e-15
```

and the present-day target density relative error is

```text
9.741787332055634e-15
```

against gate `1e-12`.

PASS.

## N6 — Cosh non-regression

The required corrected Exp source snippets are present and the untouched Cosh branch agrees identically on the fixed `Z` ladder:

```text
max Cosh numerical error = 0
```

against gate `1e-15`.

PASS.

## Interpretation and continuation boundary

This PASS validates the implementation-level correction of the Exp `K(Q)` normalization and its local matching to the D1A/R3 value of `K2` and `mu^2`.

It does not establish a corrected cosmological trajectory. In particular:

```text
historical_v053_results_unchanged = true
corrected_CLASS_cosmological_trajectory_evaluated = false
nonlinear_branch_selection_performed = false
NL1C7_authorized = false
```

No historical result is reclassified. The next permitted stage is a separately preregistered, no-refit corrected CLASS background/linear-baseline run using the same numerical cosmological parameters and pinned CLASS source commit.