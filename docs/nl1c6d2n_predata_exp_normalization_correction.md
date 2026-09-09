# NL1C6D2N predata — corrected Exp K2 normalization model revision

Status: **PREREGISTERED BEFORE ANY CORRECTED-MODEL CLASS BACKGROUND, SOURCE, PERTURBATION, D2, MEMORY, OR LIKELIHOOD RESULT**.

Frozen label:

```text
NL1C6D2N_PREDATA_EXP_NORMALIZATION_CORRECTION
```

## 1. Historical boundary

This phase starts from the locked historical chain ending in

```text
NL1C6D2C_COVARIANT_MIXED_SECTOR_COMPLETION_FAIL
```

on branch `v053-model-freeze-planck`.

That historical classification is immutable. The corrected model is developed only on the new branch

```text
v053-exp-normalization-corrected
```

created from commit

```text
dc7510d973950a13b0be2b54301dbb2afef2627e
```

No historical v053 PASS/FAIL result is reclassified by this revision.

## 2. Motivation

The frozen D1A/R3 weak-field normalization and the dedicated AeST Minkowski expansion use

\[
K(Q)=K_2(Q-Q_0)^2+O[(Q-Q_0)^3],
\]

which implies

\[
K_{QQ}(Q_0)=2K_2,
\qquad
F_{QQ}(0,Q_0)=-4K_2,
\]

and yields the already frozen weak-field relations

\[
P_\chi=4K_2 U,
\qquad
\mu^2=\frac{2K_2Q_0^2}{2-K_B}.
\]

The historical CLASS Exp implementation instead used

\[
K_{\rm Exp}^{\rm old}=2K_2Z_0^2(e^{Z^2}-1),
\qquad
Z=(Q-Q_0)/Z_0,
\]

which has twice the required quadratic curvature at `Q=Q0`.

D2N adopts the corrected Exp convention

\[
\boxed{K_{\rm Exp}^{\rm corr}=K_2Z_0^2(e^{Z^2}-1)}
\]

while retaining the numerical parameter

```text
K2 = 9500
```

and all other already frozen physical parameters unless a later separately preregistered model-refit phase explicitly changes them.

## 3. Exact source-code correction

Only the Exp branch of the AeST homogeneous `K(Q)` evaluator is corrected in the first implementation commit.

For

\[
K=K_2 Z_0^2(e^{Z^2}-1),
\]

the implementation must use

\[
K_Q=2K_2Z_0 Z e^{Z^2},
\]

\[
K_{QQ}=2K_2 e^{Z^2}(1+2Z^2).
\]

The inverse background evaluation must therefore solve

\[
Z e^{Z^2}=\frac{K_Q}{2K_2Z_0},
\]

not the historical denominator `4 K2 Z0`.

The Cosh implementation is not changed in this phase.

No change is allowed to `K_B`, `Q0`, `K2`, `Z0`, baryon/cosmological parameters, memory parameters, full-J interpolation functions, or observational likelihood settings in this correction commit.

## 4. D2N-A normalization regression

Before any corrected CLASS cosmological trajectory is interpreted, run an implementation-level audit with the following frozen checks.

### N1 — exact local curvature

At `Z=0`, require

```text
K = 0
KQ = 0
KQQ / (2 K2) = 1
```

with normalized discrepancy `<= 1e-14`.

Also require the weak-field mass reconstructed from the corrected curvature to equal

\[
\mu^2=\frac{2K_2Q_0^2}{2-K_B}
\]

with relative discrepancy `<=1e-14`.

### N2 — quadratic small-Z limit

On the fixed ladder

```text
|Z| in {1e-1, 3e-2, 1e-2, 3e-3, 1e-3}
```

verify

\[
R_K(Z)=\frac{K(Z)}{K_2(Q-Q_0)^2}-1
\]

tends monotonically to zero as `|Z|` decreases. Require

```text
|R_K(1e-3)| <= 1e-6.
```

The same test is performed for positive and negative `Z`.

### N3 — derivative consistency

On

```text
Z in {-4,-2,-1,-0.1,0.1,1,2,4}
```

compare analytic `KQ` and `KQQ` against centered finite differences of the corrected `K(Q)`.

Required maximum normalized discrepancies:

```text
KQ  <= 2e-7
KQQ <= 2e-5.
```

### N4 — forward/inverse Exp consistency

For the same nonzero `Z` grid, construct `KQ` analytically, invert it through the exact corrected `KQ -> Z` routine, and require

```text
max |Z_recovered-Z| / max(1,|Z|) <= 1e-12.
```

### N5 — background charge law

Using the existing background calibration/evaluation logic, verify at

```text
a in {1.0,0.8,0.5,0.3,0.2,1/7}
```

that the returned `KQ(a)` obeys exactly the frozen shift-charge law

\[
K_Q(a)=I_0/a^3
\]

with maximum normalized discrepancy `<=1e-12`.

At `a=1`, the calibrated effective dark density must reproduce the requested target density with relative discrepancy `<=1e-12`.

### N6 — Cosh non-regression

The Cosh formulas and their numerical outputs on the same fixed `Z` ladder must be byte/source-identical or numerically identical at `<=1e-15` to the parent commit. D2N is an Exp-only normalization correction.

## 5. D2N-A classifications

All N1-N6 pass:

```text
NL1C6D2N_EXP_NORMALIZATION_AUDIT_PASS
```

Any exact identity or frozen gate fails:

```text
NL1C6D2N_EXP_NORMALIZATION_AUDIT_FAIL
```

No gate may be relaxed after inspecting output.

## 6. What D2N-A PASS does not establish

A normalization-audit PASS does **not** establish that the corrected cosmology is observationally acceptable and does not recover any historical v053 result automatically.

In particular it does not authorize:

- reusing historical D2A source arrays as corrected-model sources;
- reusing historical CLASS perturbation traces as corrected-model traces;
- nonlinear branch selection;
- NL1C7 memory science;
- Planck/ACT/SPT likelihood interpretation.

## 7. Continuation after D2N-A PASS

Only after `NL1C6D2N_EXP_NORMALIZATION_AUDIT_PASS`:

1. build a clean pinned CLASS tree with the corrected Exp patch;
2. recompute the corrected homogeneous background and linear perturbation trajectory with the unchanged numerical parameter set;
3. quantify the difference from the historical v053 baseline without retuning cosmological parameters;
4. preregister any required corrected-model cosmological refit before performing it;
5. regenerate D2A matter/source products from the corrected model;
6. rerun the D1/D2 consistency chain required before nonlinear FLRW branch evolution.

The first corrected-model CLASS trajectory is a diagnostic/regression result, not an observational fit.

## 8. Anti-tuning rule

The normalization correction is motivated only by the action-level factor-of-two inconsistency identified before any corrected-model cosmological output was inspected.

No later corrected-model result may motivate changing the factor, redefining `K2`, or selecting a different Exp normalization within this D2N phase.
