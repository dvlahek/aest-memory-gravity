# Stable AeST finite-memory R1 — post-data diagnosis

Date: 2026-09-14
Branch: `fullj-evolving-weyl-bridge`
Parent pre-data lock: `a7b10d1a9195ad41ea1ce456c259bd88351a951a`

## Formal result

The preregistered R1 classification remains

    STABLE_AEST_FINITE_MEMORY_R1_ETA_SMOOTHNESS_FAIL

with gates

- FM-G1 provenance and stable-host lock: PASS
- FM-G2 zero-coupling memory regression: PASS
- FM-G3 finite-memory numerical regularity: PASS
- FM-G4 small-eta smoothness: FAIL
- FM-G5 material memory response: FAIL
- FM-G6 relaxation-time dependence: PASS

This result is not reclassified by the analysis below.

## Key diagnostic observation

R1 defined the finite-memory response relative to the memory-off host baseline,

    Delta_X(eta,tau) = X(memory enabled,eta,tau) - X(memory off).

However, the zero-coupling control showed that merely integrating the enlarged memory-enabled ODE system with `eta=0` introduces a small numerical infrastructure offset in W of order 1e-9 relative L2. This is the same order as the preregistered finite-memory amplitudes used by FM-G4 and FM-G5.

Therefore the preregistered Delta_X contains two contributions,

    Delta_X = [X(eta,tau)-X(0,tau)] + [X(0,tau)-X(memory off)],

where the second term is independent of the coupling eta but can dominate the first. Such a constant offset prevents the raw Delta_X from scaling linearly with eta even if the coupling-dependent increment itself is linear.

## Post-hoc matched-baseline calculation for tau H0 = 10

The existing R1 output contains a memory-enabled `eta=0, tau H0=10` run. Define post hoc

    delta_X_matched(eta,10) = X(eta,10) - X(0,10),

with both trajectories integrating the same memory-enabled ODE state dimension and using the same bath relaxation time.

Using the frozen nine-redshift vectors from the R1 NPZ, the Weyl matched-baseline amplitudes relative to the original stable memory-off W norm are:

| k_h | eta=0.0025 | eta=0.005 | eta=0.01 |
|---:|---:|---:|---:|
| 0.10000 | 1.3976e-12 | 2.7970e-12 | 5.5925e-12 |
| 0.16500 | 1.5964e-11 | 3.1926e-11 | 6.3847e-11 |
| 0.19750 | 3.6650e-11 | 7.3300e-11 | 1.4659e-10 |

The successive amplitude ratios are approximately

- k_h=0.10000: 2.00132 and 1.99943
- k_h=0.16500: 1.99991 and 1.99985
- k_h=0.19750: 1.99999 and 1.99992

Using the same preregistered smoothness functional but with the matched baseline gives

| k_h | L1 matched | L2 matched |
|---:|---:|---:|
| 0.10000 | 1.4791e-3 | 4.1501e-4 |
| 0.16500 | 5.2803e-5 | 7.7230e-5 |
| 0.19750 | 6.2808e-5 | 6.1333e-5 |

The delta_cdm matched-baseline increments show the same near-doubling with eta.

## Interpretation

This post-hoc calculation does not convert R1 into a PASS. It identifies a likely measurement-definition issue: the preregistered smoothness statistic was dominated by a coupling-independent numerical offset associated with changing the ODE state dimension from memory-off to memory-enabled.

The matched-baseline result is strongly consistent with a smooth first-order coupling response at tau H0=10, but its absolute observable amplitude is very small. A dedicated confirmatory test is required to establish that this differential response is stable under integration-tolerance changes and to measure relaxation-time dependence using an eta=0 baseline matched separately at each tau.

In particular, the preregistered FM-G6 PASS must not yet be interpreted as physical relaxation-time dependence because R1 did not include an eta=0 matched baseline at tau H0=1. Different bath stiffness can alter the numerical infrastructure offset even at zero coupling.

## Licensed next test

A follow-up may test a matched-bath response

    delta_X^M(eta,tau) = X(memory enabled,eta,tau) - X(memory enabled,eta=0,tau)

for each tau separately, with paired tolerance convergence and a direct test of the tangent response delta_X^M / eta.

No observational claim, new-physics claim, or permanent-elasticity-loss claim is licensed by R1 or by this post-hoc analysis.
