# MCMG-R2 protocol lock: self-consistent growth + Weyl memory

Date: 2026-09-13
Branch: `minimal-causal-memory-gravity`
Parent R1 result: `MCMG_CAUSAL_FIRST_MOMENT_UNIVERSALITY_PASS`

This is a protocol lock before the official R2 production run. A brief implementation sanity check was performed during design, so this is not described as a blind preregistration. No thresholds below may be changed after the production run begins.

## Purpose

R1 established that a causal memory state obeys the universal first-moment response for a prescribed GR source. R2 tests the nontrivial case in which the memory state feeds back into structure growth and simultaneously controls the Weyl/lensing source.

The central object is a self-consistent pure-memory deformation with no-slip baseline.

## Background

Use the same flat LambdaCDM background as R1:

- Omega_m0 = 0.315
- Omega_Lambda0 = 0.685
- a_ini = 1e-3

The background expansion is fixed. Memory modifies perturbation growth, not H(a), in R2.

## Dynamical system

Let N = ln a, u = H0 tau_mem, E(a)=H/H0, and M be the exponential-kernel memory state.

The system is

    D' = V,

    V' = -[2 + H'/H] V
         + (3/2) Omega_m(a) [(1-eta) D + eta a M],

    M' = [D/a - M] / [u E(a)].

The effective Weyl/potential source is

    P_eff = (1-eta) D/a + eta M.

The GR reference is P_GR = D_GR/a.

Initial conditions are the same normalized growing-mode GR initial conditions used in R1, with

    M(a_ini) = D(a_ini)/a_ini.

No independent slip or lensing parameter is introduced.

## Frozen parameter grid

Memory times:

    u in {0.005, 0.01, 0.02, 0.04}.

Finite amplitudes:

    eta in {-0.50, -0.25, 0, +0.25, +0.50}.

Tangent amplitudes:

    eta_tan = +/-0.01.

Zero-memory control:

    u_zero = 1e-5

at eta = +/-0.50.

Primary science window:

    0 <= z <= 2.

## Response observables

Define

    g_eta(a) = D_eta/D_GR - 1,

    w_eta(a) = P_eff,eta/P_GR - 1.

The growth-Weyl separation is

    h_eta(a) = w_eta(a) - g_eta(a).

At first order in eta,

    d h / d eta |_(eta=0) = [M_GR - P_GR] / P_GR.

For small u, R1 implies

    [M_GR - P_GR] / P_GR
      = -u d ln(P_GR)/d(H0 t) + O(u^2).

This cancellation of the self-consistent growth response in `w-g` is the key R2 consistency relation.

## Numerical controls and gates

### R2-G1 finite self-consistent evolution

For every frozen (u, eta) run require D, V, M, and P_eff finite over the full domain and D>0.

### R2-G2 exact nested-GR amplitude limit

For eta=0 at every u, require over 0<=z<=2

    relL2[D_eta0, D_GR] <= 1e-8

and

    relL2[P_eff,eta0, P_GR] <= 1e-8.

### R2-G3 zero-memory GR limit

For u=1e-5 and eta=+/-0.50 require over 0<=z<=2

    relL2[D, D_GR] <= 2e-5

and

    relL2[P_eff, P_GR] <= 2e-5.

### R2-G4 tangent odd-symmetry control

For eta=+/-0.01 and each frozen u, define the even-to-odd ratios

    E_g = ||g_+ + g_-|| / ||g_+ - g_-||,
    E_w = ||w_+ + w_-|| / ||w_+ - w_-||.

Require

    max(E_g, E_w) <= 0.02

for every u.

### R2-G5 exact growth-Weyl tangent consistency

For eta_tan=0.01 define

    C_u(a) = { [w_+ - g_+] - [w_- - g_-] } / (2 eta_tan).

Independently obtain the passive eta=0 memory lag

    L_u(a) = [M_GR,u - P_GR] / P_GR.

Require for every u over 0<=z<=2

    relL2[C_u, L_u] <= 0.005.

### R2-G6 first-moment causal consistency

Define

    T(a) = - d ln(P_GR)/d(H0 t).

Require

    relL2[C_0.005 / 0.005, T] <= 0.02,

    relL2[C_0.01 / 0.01, T] <= 0.03,

and the error at u=0.005 must be smaller than the error at u=0.02.

### R2-G7 finite-amplitude sign/stability control

For eta = +/-0.25 and +/-0.50:

1. all runs satisfy G1;
2. at z=0, sign(g_eta) = sign(eta);
3. at z=0, sign(w_eta) = sign(eta);
4. max absolute |g_eta| over 0<=z<=2 is < 0.05;
5. max absolute |w_eta| over 0<=z<=2 is < 0.05.

The magnitude bounds are stability/perturbativity controls, not phenomenological priors.

## Classification

If G1-G7 pass:

    MCMG_SELF_CONSISTENT_GROWTH_WEYL_MEMORY_PASS

If G1-G3 fail:

    MCMG_SELF_CONSISTENT_NUMERICAL_CONTROL_FAIL

If G1-G3 pass but G4 fails:

    MCMG_SELF_CONSISTENT_TANGENT_CONTROL_FAIL

If G1-G4 pass but G5 fails:

    MCMG_GROWTH_WEYL_CONSISTENCY_FAIL

If G1-G5 pass but G6 fails:

    MCMG_FIRST_MOMENT_SELF_CONSISTENCY_FAIL

If G1-G6 pass but G7 fails:

    MCMG_FINITE_AMPLITUDE_STABILITY_FAIL

## Interpretation lock

A PASS establishes that the same causal memory state can self-consistently modify matter growth and the Weyl/lensing source while preserving the nested GR and zero-memory limits. It also establishes the tangent growth-Weyl consistency relation within the minimal exponential-kernel realization.

A PASS licenses R3: a held-out, blind kernel/background generality test of the growth-Weyl memory consistency relation.

A PASS does not license an observational detection, a preference for nonzero memory, or a Nature-level claim.