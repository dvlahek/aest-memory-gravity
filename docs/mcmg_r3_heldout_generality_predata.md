# MCMG-R3 pre-data declaration: held-out kernel/background generality

Date: 2026-09-13
Branch: `minimal-causal-memory-gravity`
Parent R2 production classification: `MCMG_SELF_CONSISTENT_GROWTH_WEYL_MEMORY_PASS`
Parent R2 code HEAD: `362a81b3673ffce99f92ac966d740b03e8ab79ca`

This declaration is fixed before any R3 production calculation. No R3 kernel/background result has been inspected before this lock.

## Question

Does the self-consistent growth–Weyl memory relation found in R2 survive simultaneous changes of the causal kernel and the background expansion history?

The target relation is

    h_eta(a) = w_eta(a) - g_eta(a),

with

    g_eta = D_eta/D_GR - 1,
    w_eta = P_eff,eta/P_GR - 1.

At tangent order,

    d h / d eta |_(eta=0) = [M_GR - P_GR]/P_GR.

For any normalized causal kernel with first moment u=H0 tau_bar,

    [M_GR-P_GR]/P_GR
      = -u d ln(P_GR)/d(H0 t) + O(u^2).

R3 tests if this is structural rather than specific to the exponential kernel and the fiducial LambdaCDM background.

## Background family

Use smooth constant-w dark energy with

    E(a)^2 = Omega_m0 a^-3 + (1-Omega_m0) a^[-3(1+w)].

Dark-energy perturbations are not included. The linear GR reference growth obeys

    D'' + [2 + d ln H/d ln a] D' - (3/2) Omega_m(a) D = 0.

Frozen background set:

    B0: Omega_m0=0.315, w=-1.0
    B1: Omega_m0=0.270, w=-1.0
    B2: Omega_m0=0.360, w=-1.0
    B3: Omega_m0=0.315, w=-0.9
    B4: Omega_m0=0.315, w=-1.1

All use a_ini=1e-3 and growing-mode initial conditions D(a_ini)=D'(a_ini)=a_ini, normalized to D(1)=1 for the GR reference.

## Causal kernel realizations

All kernels are positive, normalized, causal, and have the same first moment u.

K1 exponential:

    one relaxation state with time constant u.

K2 Erlang-2:

    two cascaded relaxation states, each with time constant u/2.

K3 Erlang-4:

    four cascaded relaxation states, each with time constant u/4.

K4 bi-exponential (new held-out shape):

    K = 0.5 Exp(tau=u/2) + 0.5 Exp(tau=3u/2).

Its mean delay is exactly u.

For each realization the memory output M is inserted into the same pure-memory deformation

    P_eff = (1-eta) D/a + eta M,

and the growth equation uses the corresponding drive

    (1-eta)D + eta a M.

## Frozen grid

Memory times:

    u in {0.005, 0.01, 0.02}.

Tangent amplitudes:

    eta_tan = +/-0.01.

Nested-GR run:

    eta = 0.

Finite-amplitude held-out control:

    eta = +/-0.50 at u=0.02.

Primary science window:

    0 <= z <= 2.

## R3 observables

For every background b, kernel k, and memory time u define

    C_bku(a) = {h_(+eta_tan)-h_(-eta_tan)}/(2 eta_tan),

and independently from the eta=0 run

    L_bku(a) = [M_GR,bku-P_GR,b]/P_GR,b.

The first-moment target for each background is

    T_b(a) = -d ln(P_GR,b)/d(H0 t).

## Gates

### R3-G1 finite positive evolution

All tangent, eta=0, and finite-amplitude runs must remain finite over the full domain, with D>0.

### R3-G2 nested GR for every kernel/background

For eta=0 require over 0<=z<=2

    relL2[D,D_GR] <= 1e-8,
    relL2[P_eff,P_GR] <= 1e-8

for every background, kernel, and u.

### R3-G3 tangent odd symmetry

For every background, kernel, and u require

    ||g_+ + g_-|| / ||g_+ - g_-|| <= 0.02,
    ||w_+ + w_-|| / ||w_+ - w_-|| <= 0.02.

### R3-G4 exact growth–Weyl memory consistency

For every background, kernel, and u require

    relL2[C_bku, L_bku] <= 0.005.

### R3-G5 first-moment universality across backgrounds and kernels

For every background and every kernel require

    relL2[C_(u=0.005)/0.005, T_b] <= 0.03,

and

    error(u=0.005) < error(u=0.02).

### R3-G6 kernel-shape collapse at fixed mean delay

For each background, compare C/u among all kernel pairs at u=0.005. Require

    max_pair relL2[(C_k/u),(C_j/u)] <= 0.02

for every background.

### R3-G7 finite-amplitude relation and stability

At u=0.02 and eta=+/-0.50, for every background and kernel require:

1. D>0 and all states finite;
2. sign[g(z=0)] = sign(eta);
3. sign[w(z=0)] = sign(eta);
4. max |g| < 0.05 over 0<=z<=2;
5. max |w| < 0.05 over 0<=z<=2;
6. relL2[(w-g)/eta, L_(eta=0)] <= 0.01.

The last condition tests if the R2 cancellation remains useful beyond tangent order.

## Classification

If G1-G7 all pass:

    MCMG_GROWTH_WEYL_MEMORY_GENERALITY_PASS

If G1-G2 fail:

    MCMG_R3_NUMERICAL_CONTROL_FAIL

If G1-G2 pass but G3 fails:

    MCMG_R3_TANGENT_CONTROL_FAIL

If G1-G3 pass but G4 fails:

    MCMG_R3_GROWTH_WEYL_CONSISTENCY_FAIL

If G1-G4 pass but G5 fails:

    MCMG_R3_FIRST_MOMENT_GENERALITY_FAIL

If G1-G5 pass but G6 fails:

    MCMG_R3_KERNEL_COLLAPSE_FAIL

If G1-G6 pass but G7 fails:

    MCMG_R3_FINITE_AMPLITUDE_GENERALITY_FAIL

## Interpretation lock

A PASS establishes a host-independent growth–Weyl causal-memory relation across the frozen kernel and background families. It licenses a next-stage derivation/observable projection of a low-dimensional memory consistency relation.

A PASS does not by itself license:

- an observational detection,
- a preference for nonzero memory,
- a claim that GR is incomplete,
- an AeST reclassification,
- or a Nature-level claim.

No threshold or frozen model choice above may be changed after R3 production begins.