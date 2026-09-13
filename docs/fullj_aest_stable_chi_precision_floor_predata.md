# AeST stable-chi precision-floor adjudication — pre-data declaration

Date: 2026-09-13
Branch: `fullj-evolving-weyl-bridge`
Parent precision-audit classification: `FULLJ_AEST_STABLE_CHI_NOT_PRECISION_CONVERGED`
Parent precision-audit predata: `167a556247e334a4a3652d61b365a4d8af3b523f`

This declaration is fixed before inspecting any result at perturbation tolerances tighter than `3e-7`.

## Motivation

The parent precision audit passed its absolute tight-tolerance convergence gate, adjacent-ULP preservation gate, and residual-identity gate. It failed only the preregistered monotonic-trend gate because the stable formulation was monotone on 7/10 anchors rather than the required 8/10. The three non-monotone anchors were

- `k_h = 0.09875`,
- `k_h = 0.10000`,
- `k_h = 0.10125`.

At those anchors the stable-coordinate changes were already of order `1e-7` or below, so the failure may represent numerical-floor jitter rather than non-convergence. This follow-up adjudicates only that question. It does not reclassify the parent result.

## Frozen system

Use the same stable-residual AeST implementation as the parent audit:

    s = a theta/k^2 + alpha,
    chi = Q s,

with

    s' = 3 c_a^2 Hc (s-alpha) + a [Pi/(1+w) + E].

No memory term is active:

    aest_memory_enabled = no
    aest_eta = 0.

No physical parameter, background equation, initial condition, requested-k serialization, observable extractor, or source equation may change.

## Frozen anchors

Primary adjudication anchors are exactly the three non-monotone parent cases:

    k_h in {0.09875, 0.10000, 0.10125}.

Add one monotone control anchor:

    k_h = 0.19750.

For each anchor use exactly the direct/parent binary64 token used in the parent precision audit.

## New tolerances

Run the stable formulation only at

    tol_perturbations_integration in {1e-7, 3e-8}.

The parent stable result at `3e-7` is reused from the locked parent bundle and is not recomputed for the primary plateau comparisons.

## Primary observable

Use the same nine-redshift Weyl vector

    W = phi + psi,
    z = [6,5,4,3,2,1.5,1,0.5,0.2].

For vectors X and Y use the same relative L2 metric as the parent audit.

Define for each anchor

    C_37 = relL2(W_3e-7, W_3e-8),
    C_17 = relL2(W_1e-7, W_3e-8).

These are Cauchy-plateau diagnostics. Strict step-by-step monotonicity is not required once all compared solutions lie inside the frozen plateau threshold.

## Adjacent-ULP control

At the tightest new tolerance `3e-8`, also run the immediately next larger positive binary64 k token for each of the four anchors. Define

    U = relL2(W_direct, W_nextULP).

This confirms that tighter integration does not reintroduce the certified historical k-ULP pathology.

## Residual-identity control

At the direct token and `3e-8`, retain dense histories and compare the evolved residual `s_aest` against

    a theta/k^2 + alpha

only on points satisfying the same non-cancellation mask used by the parent audits:

    |s_aest| >= 1e-8 (|a theta/k^2| + |alpha|).

Require at least 8 valid points per anchor.

## Gates

### PF-G1 provenance and parent lock

Require:

- this predata commit is an ancestor of HEAD;
- parent classification is exactly `FULLJ_AEST_STABLE_CHI_NOT_PRECISION_CONVERGED`;
- parent stable NPZ/JSON are present;
- stable CLASS source contains `FULLJ_AEST_STABLE_CHI_RESIDUAL_V1` and the locked residual equation;
- frozen CLASS head and `aest_memory.c` provenance remain unchanged.

### PF-G2 primary Cauchy plateau

For all four anchors require

    C_17 <= 1e-6

and

    C_37 <= 1e-6.

This is the decisive numerical-floor criterion.

### PF-G3 targeted non-monotone-anchor closure

For all three primary adjudication anchors require both `C_17 <= 1e-6` and `C_37 <= 1e-6`.

The control anchor is reported separately so a control failure cannot be hidden by the three targeted cases.

### PF-G4 tight adjacent-ULP continuity

At `3e-8`, require all four anchors to satisfy

    U <= 1e-6.

### PF-G5 residual-state identity

For all four direct-token runs at `3e-8`, require

    relL2(s_aest, a theta/k^2 + alpha) <= 1e-6

on the non-cancellation subset, with at least 8 valid points.

## Classification priority

1. PF-G1 fail:
   `FULLJ_AEST_STABLE_CHI_PRECISION_FLOOR_INCOMPLETE`
2. PF-G2 or PF-G3 fail:
   `FULLJ_AEST_STABLE_CHI_PRECISION_FLOOR_NOT_REACHED`
3. PF-G4 fail:
   `FULLJ_AEST_STABLE_CHI_PRECISION_FLOOR_ULP_FAIL`
4. PF-G5 fail:
   `FULLJ_AEST_STABLE_CHI_PRECISION_FLOOR_IDENTITY_FAIL`
5. PF-G1--PF-G5 pass:
   `FULLJ_AEST_STABLE_CHI_PRECISION_FLOOR_CERTIFIED`

## Interpretation lock

A PASS establishes that the three parent non-monotone stable anchors lie on a Cauchy plateau at tighter perturbation tolerances, while adjacent-ULP continuity and the exact residual identity remain intact.

A PASS does not retroactively change the parent classification `FULLJ_AEST_STABLE_CHI_NOT_PRECISION_CONVERGED`. It resolves the specific reason that parent audit failed and licenses the stable-residual AeST implementation for the next host-level follow-up.

A PASS does not license a new-physics claim, a physical-instability claim, or any reclassification of historical R3.
