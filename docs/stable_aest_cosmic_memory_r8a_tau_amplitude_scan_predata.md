# Stable AeST cosmic memory R8a — relaxation-time amplitude scan (pre-data)

Date: 2026-09-15
Branch: `fullj-evolving-weyl-bridge`

## Status before any R8a result

This document preregisters R8a before implementation or inspection of any R8a tau-scan result.

The immediate physics parent is the certified live physical lookback result

`STABLE_AEST_COSMIC_MEMORY_R7A_LIVE_LOOKBACK_DECOMPOSITION_CERTIFIED`

with post-data checkpoint

`86c03e6ba2ee9fcbf33a9d319d12ae778a747881`.

Historical R7 remains `STABLE_AEST_COSMIC_MEMORY_R7_PHYSICAL_BRIDGE_FAIL` and is not reclassified.

## Question

R7a certified the lookback decomposition at `tau H0 = 10`. R8a asks if the direct physical observable derivative remains numerically reproducible as the relaxation time is shortened, and how its amplitude and shape change with `tau H0`.

This is an amplitude/generality scan only. It does not perform epoch decomposition at every tau and it does not use observational likelihood data.

## Frozen model and observable setup

Reuse the certified R7a direct physical source construction:

- frozen CLASS parent `e85808324f51fc694d12e3ed7439552a3c3f9540`,
- certified stable-chi residual,
- memory order 20,
- tolerance `3e-8`,
- no nonlinear/Halofit,
- no R2d history trace,
- no external replay hook,
- live physical memory feedback only,
- signed eta allowed only in the disposable diagnostic source for central differentiation,
- epoch mode fixed to `full` for all R8a runs.

Observables are exactly the R5b/R7a set:

- `sigma8(z)`,
- effective `f sigma8(z)`,
- linear CMB lensing convergence `C_L^{kappa kappa}` obtained from CLASS raw `pp`.

Frozen domains:

- `z = [0.2, 0.5, 1.0, 1.5, 2.0]`,
- `L = 40,...,2000`,
- `P_k_max_h/Mpc = 5`,
- same canonical initialization anchor used by R5b/R7a.

## Frozen relaxation-time grid

The R8a scan is

`tau H0 = [10.0, 5.0, 2.5, 1.25]`.

The grid is geometric and was selected before R8a results. It approaches the previously difficult order-unity relaxation regime without adding `tau H0 = 1` to this first generality scan.

No tau point may be removed, added, or moved after data are inspected.

## Frozen derivative construction

For every tau value run

- `eta = 0`,
- `eta = +0.025`,
- `eta = -0.025`,
- `eta = +0.05`,
- `eta = -0.05`.

For observable X define the central derivative

`T_X(tau,eps) = [X(+eps;tau)-X(-eps;tau)] / [2 eps X(0;tau)]`.

Primary derivative: `eps = 0.025`.

Control derivative: `eps = 0.05`.

Signed eta is a diagnostic continuation used only to evaluate the local derivative at eta=0. It does not enlarge the physical parameter domain used in previous observational claims.

## Metrics

For vectors A and B use

- relative vector error `E = ||A-B|| / max(||A||,||B||)`,
- cosine `C = A.B/(||A|| ||B||)`.

For each observable and each tau record:

- `||T(tau,0.025)||`,
- min/max tangent,
- `E` and `C` between `T(tau,0.025)` and `T(tau,0.05)`,
- amplitude ratio relative to tau10,
- cosine relative to the tau10 tangent.

Amplitude ratios and shape changes across tau are science outputs, not pass/fail conditions.

## Preregistered gates

### R8A-G1 provenance and parent lock

PASS if the preregistration lock and R7a post-data checkpoint are ancestors of the implementation head and the frozen R7a result is certified.

### R8A-G2 direct physical source topology

PASS if the disposable CLASS source contains exactly one live physical memory closure, exactly one R7a-style windowed eta multiplier with mode `full`, zero external tangent replay hooks, and zero R2d history trace hooks.

### R8A-G3 finite tau-grid runs and eta-zero identity

PASS if all 20 frozen runs are finite and domain-positive, and the eta-zero observables at all four tau values agree with the tau10 eta-zero baseline to `E <= 1e-10` and `C >= 0.9999999999` for each observable.

### R8A-G4 tau10 parent derivative bridge

PASS if the tau10 primary central derivative reproduces the frozen R7a tau10 full derivative for each observable with

- `E <= 0.02`,
- `C >= 0.999`.

### R8A-G5 central-derivative consistency across tau

PASS if, for every tau and every observable, primary versus control derivatives satisfy

- `E <= 0.10`,
- `C >= 0.995`.

No monotonicity in tau is preregistered.

### R8A-G6 resolved response across tau

PASS if every primary tangent norm is finite and strictly positive.

## Formal classifications

In priority order:

1. `STABLE_AEST_COSMIC_MEMORY_R8A_INCOMPLETE`
2. `STABLE_AEST_COSMIC_MEMORY_R8A_PARENT_PROVENANCE_FAIL`
3. `STABLE_AEST_COSMIC_MEMORY_R8A_SOURCE_TOPOLOGY_FAIL`
4. `STABLE_AEST_COSMIC_MEMORY_R8A_RUN_FAIL`
5. `STABLE_AEST_COSMIC_MEMORY_R8A_TAU10_BRIDGE_FAIL`
6. `STABLE_AEST_COSMIC_MEMORY_R8A_CENTRAL_DERIVATIVE_FAIL`
7. `STABLE_AEST_COSMIC_MEMORY_R8A_RESPONSE_UNRESOLVED`
8. `STABLE_AEST_COSMIC_MEMORY_R8A_TAU_GENERALITY_CERTIFIED`

## Licensed interpretation of a PASS

A PASS licenses only the statement that, in the locked stable-AeST setup and tested tau grid, the local observable memory derivative is numerically reproducible across the scanned relaxation times. It also licenses reporting the measured tau dependence of the tangent amplitude and shape.

A PASS does not license monotonic scaling beyond the sampled points, tau values below 1.25, observational detection, a bound on tau, a universal law of gravitational memory, or a claim that shorter tau necessarily makes the signal observable.

## Next step

If at least one shorter tau point is certified and scientifically informative, a separate preregistered R8b will apply the R7a live epoch decomposition to selected predeclared tau point(s). R8b selection rules must be frozen before those epoch-decomposition results are computed.