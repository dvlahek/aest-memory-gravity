# Stable AeST cosmic memory R8a2 — precision-qualified relaxation-time scan (pre-data)

Date: 2026-09-15
Branch: `fullj-evolving-weyl-bridge`

## Status before any R8a2 result

This document preregisters R8a2 before implementation or inspection of any R8a2 result.

Parents:

- certified R7a live lookback result: `STABLE_AEST_COSMIC_MEMORY_R7A_LIVE_LOOKBACK_DECOMPOSITION_CERTIFIED`, post-data lock `86c03e6ba2ee9fcbf33a9d319d12ae778a747881`;
- historical R8a result: `STABLE_AEST_COSMIC_MEMORY_R8A_RUN_FAIL`, post-data lock `9b138cf04d3a8c323bbf3a82e3e747deea0393dc`.

R8a is not reclassified.

## Motivation

R8a completed all 20 direct physical runs but failed its preregistered G3 because eta-zero observables at different tau values differed at the `~1e-9` level while the frozen cross-tau threshold was `1e-10`.

At eta=0 the physical memory feedback is absent, but the auxiliary bath remains in the numerical state vector and changing tau can alter the adaptive integration trajectory at numerical precision. Therefore R8a2 uses the same-tau eta-zero solution as the normalization for the same-tau central derivative and assesses baseline numerical precision by nominal-versus-tight integration tolerance. Cross-tau eta-zero differences remain recorded diagnostics but are not a pass/fail condition.

## Frozen model and observables

Reuse the certified R7a direct physical source construction:

- CLASS parent `e85808324f51fc694d12e3ed7439552a3c3f9540`,
- stable-chi residual,
- memory order 20,
- no nonlinear/Halofit,
- no R2d history trace,
- no external replay hook,
- direct physical memory feedback,
- diagnostic signed eta continuation only in the disposable source,
- epoch mode fixed to `full`.

Observables and domains remain exactly:

- `sigma8(z)`,
- effective `f sigma8(z)`,
- linear `C_L^{kappa kappa}` from CLASS raw `pp`,
- `z = [0.2,0.5,1.0,1.5,2.0]`,
- `L = 40,...,2000`,
- `P_k_max_h/Mpc = 5`.

## Frozen tau and eta grid

Tau grid is unchanged from R8a:

`tau H0 = [10.0, 5.0, 2.5, 1.25]`.

For every tau, nominal tolerance `3e-8` runs are

- `eta = 0`,
- `eta = +0.025`,
- `eta = -0.025`,
- `eta = +0.05`,
- `eta = -0.05`.

Additionally, for every tau run an eta-zero tight-precision control at tolerance `1e-8`.

Total frozen run count: 24.

## Derivative construction

For observable X and each tau define

`T_X(tau,eps) = [X(+eps;tau)-X(-eps;tau)] / [2 eps X(0;tau)]`,

using the nominal same-tau eta-zero baseline.

Primary derivative: `eps=0.025`.

Control derivative: `eps=0.05`.

## Metrics

For vectors A,B:

- `E = ||A-B|| / max(||A||,||B||)`,
- `C = A.B/(||A|| ||B||)`.

Record for every tau and observable:

- nominal-versus-tight eta-zero baseline metric,
- primary-versus-control derivative metric,
- primary tangent norm, min and max,
- amplitude ratio to tau10,
- cosine to tau10,
- cross-tau eta-zero differences to tau10 as non-gating diagnostics.

Amplitude ratios and shape changes are science outputs, not gates.

## Preregistered gates

### R8A2-G1 provenance and parent lock

PASS if this preregistration, the R7a post-data lock, and the R8a post-data lock are ancestors of the implementation head, R7a remains certified, and R8a remains historical `RUN_FAIL`.

### R8A2-G2 direct physical source topology

PASS if the disposable source has exactly one live physical memory closure, one R7a-style multiplier in `full` mode, zero external replay hooks, zero R2d history trace hooks, and the signed-eta diagnostic parser repair exactly once.

### R8A2-G3 finite runs and same-tau eta-zero precision

PASS if all 24 frozen runs are finite and domain-positive and, for every tau and observable, nominal versus tight eta-zero baseline satisfies

- `E <= 1e-7`,
- `C >= 0.99999999`.

Cross-tau eta-zero differences are reported but are explicitly non-gating.

### R8A2-G4 tau10 parent derivative bridge

PASS if the tau10 primary derivative reproduces frozen R7a tau10 full derivative for every observable with

- `E <= 0.02`,
- `C >= 0.999`.

### R8A2-G5 central derivative consistency across tau

PASS if for every tau and observable primary versus control derivatives satisfy

- `E <= 0.10`,
- `C >= 0.995`.

### R8A2-G6 resolved response across tau

PASS if every primary tangent norm is finite and strictly positive.

No monotonicity with tau is preregistered.

## Formal classifications

Priority order:

1. `STABLE_AEST_COSMIC_MEMORY_R8A2_INCOMPLETE`
2. `STABLE_AEST_COSMIC_MEMORY_R8A2_PARENT_PROVENANCE_FAIL`
3. `STABLE_AEST_COSMIC_MEMORY_R8A2_SOURCE_TOPOLOGY_FAIL`
4. `STABLE_AEST_COSMIC_MEMORY_R8A2_RUN_OR_PRECISION_FAIL`
5. `STABLE_AEST_COSMIC_MEMORY_R8A2_TAU10_BRIDGE_FAIL`
6. `STABLE_AEST_COSMIC_MEMORY_R8A2_CENTRAL_DERIVATIVE_FAIL`
7. `STABLE_AEST_COSMIC_MEMORY_R8A2_RESPONSE_UNRESOLVED`
8. `STABLE_AEST_COSMIC_MEMORY_R8A2_TAU_GENERALITY_CERTIFIED`

## Licensed interpretation of PASS

A PASS licenses reporting the measured local derivative amplitude and shape across the frozen tau grid in this stable-AeST setup.

It does not license monotonic extrapolation below tau H0=1.25, observational detection, a tau bound, or a universal law. A subsequent R8b may apply the certified R7a lookback decomposition to preselected tau values only after a separate preregistration.
