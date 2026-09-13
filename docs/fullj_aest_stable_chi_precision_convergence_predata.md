# AeST stable-chi precision convergence audit — pre-data declaration

Date: 2026-09-13
Branch: `fullj-evolving-weyl-bridge`
Parent formal result: `FULLJ_AEST_STABLE_CHI_REFERENCE_MISMATCH`
Stable-residual predata: `63d673b0e7f6349a2a10c762aac970f301646abd`

This declaration is fixed before any tolerance-convergence result is inspected.

## Motivation

The preregistered stable-residual intervention removed adjacent-binary64 sensitivity at all four pathological anchors and all four held-out anchors, with residual-state identity errors around 1e-12--1e-11. However it failed the frozen reference/regression gates because the unmodified reference reproduction exceeded the locked 2e-5 bound at two endpoints and, more importantly, the stable formulation changed the three nominally calm late-time Weyl histories by about 0.32--0.39 in relative L2.

The exact residual identity

    s = a theta/k^2 + alpha

and its derived evolution equation

    s' = 3 c_a^2 Hc (s-alpha) + a[Pi/(1+w)+E]

remain algebraically valid. The present audit asks which numerical representation is convergence-stable under a frozen one-factor tightening of the CLASS perturbation integration tolerance.

No memory term is active:

    aest_memory_enabled = no
    aest_eta = 0.

No historical result is reclassified by this audit.

## Frozen implementations

Compare exactly two implementations built from the same corrected CLASS/AeST runtime:

1. **OLD** — the unmodified subtraction-defined representation

       chi = Q (a theta/k^2 + alpha)

2. **STABLE** — the already locked redundant residual-state representation

       chi = Q s_aest

   with

       s_aest' = 3 c_a^2 Hc (s_aest-alpha) + a[Pi/(1+w)+E].

No equation, physical parameter, requested k value, background setting, approximation threshold, output extractor, or memory setting may differ between OLD and STABLE except the residual-state coordinate already locked in the parent intervention.

## One-factor precision scan

Vary only

    tol_perturbations_integration

using the frozen grid

    eps in {1e-5, 3e-6, 1e-6, 3e-7}.

The CLASS v3.3.4 default is 1e-5. No other precision parameter may be changed.

Use a single thread and the same build/compiler environment for every run.

## Frozen anchors

Use the exact direct/R3 serialized token at the following anchors:

### Calm anchors

    k_h in {0.09875, 0.10250, 0.10375}

These are the same calm controls from the parent intervention.

### Pathology anchors

Use endpoint A of the four previously certified pathological pairs:

    k_h in {0.10125, 0.10250, 0.16500, 0.19750}.

The duplicated 0.10250 serves both roles but is run only once per implementation/tolerance.

### Held-out anchors

Use endpoint A at

    k_h in {0.10000, 0.16125, 0.19500, 0.19875}.

Thus the unique anchor set is fixed before results.

## Observable grid

For every run extract

    W = phi + psi

on the locked redshifts

    z = [6,5,4,3,2,1.5,1,0.5,0.2].

For STABLE also retain `alpha_aest`, `E_aest`, and `s_aest` dense histories for residual-identity verification.

## Metrics

For implementation X in {OLD, STABLE}, anchor k, and tolerance eps define

    C_X(eps;k) = relL2[ W_X(eps;k), W_X(3e-7;k) ]

on the nine-redshift vector.

Define the tightest old/stable discrepancy

    D_OS(k) = relL2[ W_OLD(3e-7;k), W_STABLE(3e-7;k) ].

Define monotone-convergence count for an anchor if

    C_X(1e-5;k) >= C_X(3e-6;k) >= C_X(1e-6;k)

allowing only numerical ties within 2% relative or 1e-12 absolute.

For STABLE retain the residual identity on non-cancellation-dominated dense points:

    s_aest versus a theta/k^2 + alpha.

## Gates

### PC-G1 provenance and parent lock

Require the frozen CLASS/AeST provenance, the parent classification `FULLJ_AEST_STABLE_CHI_REFERENCE_MISMATCH`, the stable-residual predata ancestor, exact tolerance grid, exact anchors, and memory-off settings.

### PC-G2 stable tight-tolerance convergence

At least 8/10 unique anchors must satisfy

    C_STABLE(1e-6;k) <= 2e-3

and all anchors must satisfy

    C_STABLE(1e-6;k) <= 1e-2.

The median C_STABLE(1e-6) must be <=5e-4.

### PC-G3 stable convergence trend

At least 8/10 unique anchors must satisfy the frozen monotone-convergence criterion for STABLE.

### PC-G4 old-coordinate diagnostic

This is descriptive, not required for stable certification. Report for all anchors:

- C_OLD at all scanned tolerances;
- old monotone-convergence count;
- D_OS at the tightest tolerance;
- whether OLD moves toward STABLE as eps is tightened.

### PC-G5 stable adjacent-ULP preservation

At the tightest tolerance 3e-7 rerun the four held-out adjacent-ULP pairs from the parent intervention. Require all four W relL2 <=1e-3 and at least 3/4 <=1e-4.

### PC-G6 stable residual identity

At the tightest tolerance require the parent non-cancellation residual-state identity control to remain <=1e-4 on at least 3/4 pathological endpoint-A runs.

## Classification

1. G1 fail:
   `FULLJ_AEST_STABLE_CHI_PRECISION_AUDIT_INCOMPLETE`
2. G2 or G3 fail:
   `FULLJ_AEST_STABLE_CHI_NOT_PRECISION_CONVERGED`
3. G1-G3 pass, G5 fail:
   `FULLJ_AEST_STABLE_CHI_ULP_RECOVERY_NOT_ROBUST`
4. G1-G3 and G5 pass, G6 fail:
   `FULLJ_AEST_STABLE_CHI_IDENTITY_NOT_ROBUST`
5. G1-G3, G5, G6 pass and OLD does not converge to the same tight-tolerance solution (median D_OS >1e-2):
   `FULLJ_AEST_STABLE_CHI_NUMERICALLY_RESOLVED_COORDINATE`
6. G1-G3, G5, G6 pass and OLD converges to the same tight-tolerance solution (median D_OS <=1e-2):
   `FULLJ_AEST_STABLE_CHI_EQUIVALENT_CONVERGED_SOLUTION`

## Interpretation lock

A `NUMERICALLY_RESOLVED_COORDINATE` outcome means the exact residual-state formulation is internally converged and ULP-robust while the historical subtraction coordinate does not approach the same numerical solution over the frozen precision scan. This supports, but does not by itself prove in arbitrary precision, that the historical late-time solution was contaminated by coordinate conditioning.

An `EQUIVALENT_CONVERGED_SOLUTION` outcome is stronger: both formulations approach the same solution as the integrator tolerance is tightened.

Neither outcome reclassifies historical R3, licenses a new-physics claim, or establishes physical instability. Only a precision-converged stable host can be used for renewed memory-on AeST tests.