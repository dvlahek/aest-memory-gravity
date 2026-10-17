# Failure-Aware Numerical Certification for Stiff Memory Models

This branch isolates a numerical-methods project that emerged from the AeST memory-gravity certification campaign. The physics branch remains frozen and unchanged.

## Core problem

For stiff continuum-memory systems, a formally valid high-order truncation estimate can become useless because the derivative majorant explodes with the stiff spectral parameter. In the AeST case, a standard FD8 Taylor route required ninth derivatives of a bath-dependent source. The resulting absolute majorants reached approximately 1e28-1e39 even though the finite production trajectory remained well behaved.

The numerical question is therefore not only how to solve the stiff system, but how to certify the discretization error without introducing an artificial proof-width explosion.

## Proposed methodological contribution

The project studies a failure-aware certification workflow:

1. Run a conventional high-order derivative certificate.
2. Distinguish solver failure from certificate-width failure.
3. Diagnose whether the width comes from cancellation loss, UV stiffness, or the chosen representation.
4. Regularize the state before taking absolute values.
5. Replace generic derivative-supremum bounds with direct stencil-defect enclosures whenever possible.

For a first-derivative stencil D_h, the target object is

    E_h(f) = D_h[f] - f'.

Instead of bounding E_h through a global ninth- or fifth-derivative supremum, the direct route encloses the source values at the stencil nodes together with the exact first derivative at the target point.

## Gravity-independent theorem core

The methods branch now contains two benchmarks that establish the core mechanism before any gravity case study is used.

- `b0_analytic_separation.py` studies `f_kappa(x)=kappa^(-beta) sin(kappa x)` for `1 < beta < 9`. The standard FD8 high-jet certificate grows like `kappa^(9-beta)`, while an elementary direct certificate tends to zero.
- `b1_continuum_symbol_defect.py` studies `F_R(x)=int_1^R sin(r x)/[r^2(1+r^2)] dr`. The standard ninth-derivative certificate grows like `R^6`, while an explicit direct continuum-defect certificate is uniform in the spectral cutoff `R`.
- `THEOREM_CORE.md` records the separation theorem, the direct continuum defect identity, the parameter-uniform corollary, the explicit FD8 symbol bound, the failure-aware route-selection rule, and the stability-lift requirement.

For the default B1 setting `h=1e-2`, the explicit direct certificate has a finite `R -> infinity` limit of approximately `1.1960211073e-4`.

The nonrigorous high-accuracy quadrature values printed by B1 are diagnostics only. The rigorous benchmark claim is based on the closed-form direct envelope, not on QUADPACK error estimates.

## Observed failure ladder from AeST

The current numerical evidence is intentionally retained as a case-study seed, not as a completed proof.

- Naive absolute bath high-jet route: B10^(10) majorant about 1.30e39.
- Signed finite-production route: weighted z order 9 about 1.90e28.
- Compact/UV split: order-9 compact core about 8.8e1, while the UV sector carries essentially the entire 1.90e28 value.
- Direct-defect reformulation reduces the required parent derivative order from 10 to 2 and the bath derivative order from 10 to 1.
- Regularized variables u=z-X and q=(v-X_s)/r^2 show q approximately r^-1.95 and u_s=v-X_s approximately r^0.048 on the finite frozen UV diagnostic.
- The finite-quadrature absolute UV proxy for B10_x in that diagnostic is about 6.05e-8.

These numbers motivate the method. They are not yet promoted to a general theorem or a continuum certificate.

## Candidate paper framing

Working title:

**When High-Order Error Bounds Fail: Direct Defect Certification for Stiff Continuum-Memory Models**

Alternative OR-oriented title:

**Failure-Aware Numerical Certification for Stiff Memory Models: Choosing Between High-Derivative and Direct-Defect Bounds**

The intended novelty is not a new finite-difference stencil. The novelty target is a decision-oriented certification framework that detects proof-width failure and changes the certified object before increasing derivative order or precision.

## Planned benchmark suite

The paper should not rely on the gravity example alone. The clean benchmark plan is:

1. B0 analytical separation witness.
2. B1 continuum spectral benchmark.
3. A generalized Maxwell/viscoelastic memory model.
4. A manufactured Volterra memory equation.
5. The AeST memory-gravity case as the hard scientific stress test.

For each numerical benchmark, sweep stiffness, grid spacing, quadrature resolution where applicable, and stencil order. Compare:

- actual defect from a trusted reference,
- conventional Taylor derivative bound,
- direct stencil-defect enclosure,
- certificate-width / actual-error ratio,
- high-jet / direct-certificate ratio,
- runtime and enclosure width.

The actual defect is a diagnostic metric. Route selection must use only certified quantities and the requested certification tolerance.

## Branch boundary

Base frozen science commit:

    6282ed54e35d4db6b58fcd13d1c7403419f8afb7

Numerics branch:

    numerics/failure-aware-defect-certification

Do not merge experimental numerics changes back into the frozen physics branch unless they are separately reviewed as science changes. The AeST scripts in this directory are case-study diagnostics only.
