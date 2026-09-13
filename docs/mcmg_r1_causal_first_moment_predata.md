# MCMG-R1 pre-data declaration: causal first-moment universality

Date: 2026-09-13
Branch: `minimal-causal-memory-gravity`
Program lock parent: `ab20c3f3ec9f04d29b312cc6066825709afbcdf8`

This declaration is fixed before executing MCMG-R1.

## Question

For a prescribed GR cosmological potential source, does a normalized causal memory kernel produce the universal small-delay response

    M - S = -tau_bar dS/dt + O(tau_bar^2)

independently of kernel shape, while preserving exact static, zero-memory, and causal limits?

This is a host-independent test. No AeST quantities enter R1.

## Background and source

Use a flat matter + Lambda background with

    Omega_m0 = 0.315
    Omega_Lambda0 = 0.685

and dimensionless cosmic time x = H0 t.

Linear GR growth D(a) is obtained from

    D'' + [2 + d ln H / d ln a] D' - (3/2) Omega_m(a) D = 0,

where primes denote d/d ln a.

Integrate from

    a_ini = 1e-3

to a=1 with growing-mode initial conditions

    D(a_ini) = a_ini,
    D'(a_ini) = a_ini,

then normalize D(1)=1.

The frozen gravitational source is

    S(a) = D(a)/a.

No memory backreaction on D is allowed in R1.

## Time coordinate

For the matter + Lambda background use

    x(a) = 2/[3 sqrt(Omega_Lambda0)] asinh[sqrt(Omega_Lambda0/Omega_m0) a^(3/2)].

All kernels are functions of positive lag s in x=H0 t.

For times prior to a_ini, freeze the source at S(a_ini). This removes an arbitrary initial-memory transient.

## Causal kernels

All kernels are non-negative, normalized on s>=0, and have the same first moment u = H0 tau_bar.

K1 exponential:

    K1(s;u) = exp(-s/u)/u.

K2 Gamma/Erlang shape 2:

    K2(s;u) = 4 s exp(-2s/u)/u^2.

K3 Gamma shape 4 with scale u/4:

    K3(s;u) = (4/u)^4 s^3 exp(-4s/u) / 3!.

K4 top-hat:

    K4(s;u) = 1/(2u),  0 <= s <= 2u,
             = 0 otherwise.

The tested mean delays are

    u in {0.005, 0.01, 0.02, 0.04}.

A numerical zero-memory probe uses u=1e-5 with K1.

## Memory observable

For each kernel,

    M(x) = integral_0^infinity K(s) S(x-s) ds,

with frozen prehistory S(x<x_ini)=S(x_ini).

Define

    Delta(x) = M(x) - S(x),

and the first-moment prediction

    Delta_1(x;u) = -u dS/dx.

The principal evaluation window is

    0 <= z <= 2.

The implementation may use a denser internal time grid, but this science window, source, kernels, and u values are frozen.

## Numerical controls

### R1-G1 GR source and finite control

- D, S, M, and derivatives are finite over the full domain.
- D is positive.
- The numerical growth solution reproduces the Einstein-de Sitter growing-mode behavior at the early boundary to relative tolerance 1e-5 in D'/D.

### R1-G2 exact static-source limit

Repeat the convolution with S=constant. Require

    max |M-S| / max |S| <= 1e-10

for every kernel at u=0.04.

### R1-G3 zero-memory limit

For exponential u=1e-5 require over 0<=z<=2

    max |M-S| / max |S| <= 2e-5.

### R1-G4 explicit causality

Construct S_future by changing S only after z=0.5 (later cosmic time). Recompute M with the same causal convolution. For all times at z>=0.5 require

    max |M_future-M| / max |M| <= 1e-12.

No advanced/future dependence is permitted.

### R1-G5 first-moment convergence

For each kernel define over 0<=z<=2

    E_K(u) = ||Delta/u + dS/dx||_2 / ||dS/dx||_2.

Require:

1. E_K(0.005) < 0.15 for all four kernels.
2. E_K(0.005) < E_K(0.02) for all four kernels.
3. At least three of four kernels satisfy

       E_K(0.005) < E_K(0.01) < E_K(0.02).

The u=0.04 point is diagnostic and not part of the asymptotic monotonicity gate.

### R1-G6 kernel-shape collapse at fixed first moment

Define Q_K(u)=Delta_K(u)/u. For every pair of kernels compute relative L2 disagreement over 0<=z<=2 using the symmetric denominator max(||Qa||,||Qb||).

Require

    C(0.005) = max_pair relL2[Q_K(0.005)] < 0.10,

and

    C(0.005) < C(0.02).

### R1-G7 lag-sign consistency

For the frozen LambdaCDM source S=D/a, define points in 0<=z<=2 where |dS/dx| exceeds 1e-6 times its maximum in that window. At u=0.01 require, for every kernel, Delta and -dS/dx to have the same sign on at least 99% of those points.

## Classification

If G1-G7 all pass:

    MCMG_CAUSAL_FIRST_MOMENT_UNIVERSALITY_PASS

If numerical/source controls G1-G4 fail:

    MCMG_CAUSAL_FIRST_MOMENT_NUMERICAL_CONTROL_FAIL

If G1-G4 pass but G5 fails:

    MCMG_CAUSAL_FIRST_MOMENT_ASYMPTOTIC_FAIL

If G1-G5 pass but G6 fails:

    MCMG_CAUSAL_FIRST_MOMENT_KERNEL_UNIVERSALITY_FAIL

If G1-G6 pass but G7 fails:

    MCMG_CAUSAL_FIRST_MOMENT_SIGN_FAIL

## Interpretation lock

A PASS establishes only a host-independent causal first-moment response for the prescribed GR source. It licenses MCMG-R2, the self-consistent coupled growth + memory system.

A PASS does not license:

- a detection of gravitational memory,
- a claim that GR is incomplete,
- a Nature-level claim,
- an AeST reclassification,
- or an observational preference for nonzero memory.

The scientific purpose of R1 is to establish the universal object that later growth+lensing and host-realization tests must reproduce.