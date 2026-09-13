# AeST adjacent-ULP seed: post-hoc localization to the chi residual

Date: 2026-09-13
Branch: `fullj-evolving-weyl-bridge`
Formal parent classification: `FULLJ_AEST_ULP_E_RHS_COMPONENT_DISCONTINUITY`
Formal parent pre-data lock: `0c8dce2022626e194fa90aafe45242f2ed1fc8a7`

This note is explicitly **post-hoc**. It does not replace, retune, or reclassify the preregistered E-RHS audit.

## Formal parent result

The preregistered E-RHS decomposition audit found:

- exact instrumentation neutrality for all four adjacent-ULP pairs;
- exact/near-machine initial-state continuity for all four pairs;
- material early E-RHS seeding for all four pairs;
- no cancellation among the four outer E-RHS terms, with `kappa_E` approximately 1 and `kappa_dy` approximately 1;
- component continuity failure because T1 and T3 acquire the same material relative difference while T2 and T4 remain continuous.

The locked formal classification is therefore

    FULLJ_AEST_ULP_E_RHS_COMPONENT_DISCONTINUITY

and remains unchanged.

## Source identity behind the component result

In the frozen AeST implementation,

    theta_potential = a theta / k^2
    chi = Q (theta_potential + alpha)

and

    T1 = K_Q chi
    T3 = -(2-K_B)(H+Q) chi.

Thus T1 and T3 share the same factor `chi`. Their matched discontinuity does not by itself imply two independent source discontinuities.

The frozen leading adiabatic initial condition is

    alpha = -a theta/k^2
    E = 0,

so that `chi=0` at leading order. Therefore the source representation constructs a very small physical residual by subtracting two much larger floating-point state contributions.

## Post-hoc conditioning diagnostic

Using the raw preregistered trace files at the already locked E-RHS onset points, define

    kappa_chi = |Q| ( |a theta/k^2| + |alpha| ) / |chi|.

This is the conditioning of the *inner* subtraction that forms chi. It was not the preregistered `kappa_E`, which measured only cancellation among T1--T4 after chi had already been formed.

At the four locked onset points the reconstructed values are approximately:

| k_h | kappa_chi endpoint A | kappa_chi endpoint B |
|---:|---:|---:|
| 0.10125 | 1.54e12 | 1.54e12 |
| 0.10250 | 2.35e12 | 2.36e12 |
| 0.16500 | 1.28e12 | 1.28e12 |
| 0.19750 | 1.88e12 | 1.68e12 |

At the same onset points, `alpha`, `theta`, and background quantities differ only at roughly 1e-9 or below, while the relative chi/T1/T3 difference ranges from approximately 1e-3 to 1e-1.

Hence the current best mechanistic interpretation is:

    well-matched state variables
        -> subtraction-conditioned chi residual
        -> material T1/T3 difference
        -> E-RHS seed
        -> later alpha/E multiplicative separation
        -> later Weyl difference.

## Important interpretation boundary

This post-hoc analysis does **not** certify that the historical fringe is physical and does not establish an AeST instability. It instead identifies a candidate numerical-coordinate conditioning mechanism one level upstream of the preregistered E-RHS cancellation metric.

Because this mechanism was recognized after inspecting the parent result, it must be tested interventionally before being treated as established. The appropriate next test is an algebraically equivalent stable-residual reformulation that evolves

    s = a theta/k^2 + alpha

as a state variable and forms `chi=Q s` directly.
