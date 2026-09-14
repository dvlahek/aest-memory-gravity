# Stable AeST finite-memory R1 — pre-data declaration

Date: 2026-09-14
Branch: `fullj-evolving-weyl-bridge`

This declaration is fixed before any stable-AeST memory-on result is inspected.

## Parent numerical milestone

The parent host is the stable residual-coordinate AeST implementation with

    s = a theta/k^2 + alpha,
    chi = Q s,

and the exact redundant-state equation

    s' = 3 c_a^2 Hc (s-alpha) + a[Pi/(1+w) + E].

The required local parent result is

    FULLJ_AEST_STABLE_CHI_PRECISION_FLOOR_CERTIFIED

with `stable_AeST_host_followup_licensed=true`.

All historical AeST classifications remain unchanged. In particular, this R1 cannot retroactively reclassify historical R3, the ULP forensic runs, `FULLJ_AEST_STABLE_CHI_REFERENCE_MISMATCH`, or `FULLJ_AEST_STABLE_CHI_NOT_PRECISION_CONVERGED`.

## Question

Does the already-implemented positive finite-bath memory sector produce a finite, smooth, reproducible relaxation response when coupled to the numerically certified stable-AeST host?

R1 is deliberately a host-level physics test. It contains no ACT/SPT likelihood, no parameter fit, and no observational claim.

It also does not test the MCMG consistency relation yet. That is reserved for a later growth–Weyl comparison if R1 passes.

## Frozen host and memory equations

No new physical source term may be introduced for R1.

Use the existing finite positive Drude-bath implementation with inputs

    aest_memory_enabled,
    aest_eta,
    aest_tau_H0,
    aest_memory_order.

The existing memory closure is

    E_rhs -> E_rhs - Q B_chi/2,

with

    B_chi = eta * sum_j [ w_j chi - sqrt(w_j) (a omega_j/k) q_j ],

and regular leading adiabatic bath initial conditions

    q_j = p_j = 0.

The memory sector must use the stable host variable

    chi = Q s,

not the historical subtraction reconstruction `Q(a theta/k^2+alpha)`.

## Numerical settings

Use the frozen corrected CLASS/AeST runtime and stable-chi source already certified by the parent chain.

Fix

    tol_perturbations_integration = 1e-7,
    aest_memory_order = 16

for all primary R1 runs.

No solver, background, cosmological parameter, requested-k serialization, initial-condition, or observable-extractor setting may otherwise be changed.

## Anchors

Use exactly three direct-token anchors spanning the previously audited k range:

    k_h in {0.10000, 0.16500, 0.19750}.

Use the existing direct/R3 serialized token at each anchor. No adjacent-ULP search is part of R1 because ULP stability is already a parent-certified property of the stable host.

## Redshift grid

Use

    z = [6,5,4,3,2,1.5,1,0.5,0.2].

Retain dense raw histories for diagnostics.

## Runs

### A. Stable memory-off baseline

For each anchor run

    aest_memory_enabled = no,
    aest_eta = 0.

### B. Zero-coupling memory regression

For each anchor run

    aest_memory_enabled = yes,
    aest_eta = 0,
    aest_tau_H0 = 10,
    aest_memory_order = 16.

The bath may be dynamically present, but it must not feed back at eta=0.

### C. Finite-memory scan

For each anchor use

    aest_eta in {0.0025, 0.005, 0.01},
    aest_tau_H0 in {1, 10},
    aest_memory_order = 16.

This is a small-positive-coupling scan only. Negative eta is not permitted by the frozen positive-bath implementation.

## Observables

At the locked redshift grid retain

- `delta_cdm` (AeST effective dark-component perturbation; an internal host growth proxy, not yet the final total-matter growth observable),
- `alpha_aest`,
- `E_aest`,
- `s_aest`,
- `phi`,
- `psi`,
- `W = phi + psi`.

For an observable X define the finite-memory response relative to the memory-off stable baseline

    Delta_X(eta,tau) = X(eta,tau) - X_0.

Define its normalized amplitude

    A_X(eta,tau) = ||Delta_X||_2 / max(||X_0||_2, tiny).

For eta-linearity define

    L1 = ||Delta_W(0.005)-2 Delta_W(0.0025)||
         / max(||Delta_W(0.005)||, 2||Delta_W(0.0025)||, tiny),

    L2 = ||Delta_W(0.01)-2 Delta_W(0.005)||
         / max(||Delta_W(0.01)||, 2||Delta_W(0.005)||, tiny).

For relaxation-time dependence at eta=0.01 define

    T_tau = ||Delta_W(0.01,10)-Delta_W(0.01,1)||
            / max(||Delta_W(0.01,10)||, ||Delta_W(0.01,1)||, tiny).

## Gates

### FM-G1 provenance and stable-host lock

Require:

- this pre-data commit is an ancestor of HEAD;
- local parent classification is `FULLJ_AEST_STABLE_CHI_PRECISION_FLOOR_CERTIFIED`;
- parent has `stable_AeST_host_followup_licensed=true`;
- stable source contains the residual-state marker and `chi=Q*s` at both construction sites;
- existing finite-bath source contains the frozen memory inputs and the `E_rhs -= 0.5*Q*Bchi` closure;
- no new physical source patch is used by R1.

### FM-G2 zero-coupling memory regression

For all three anchors compare memory-enabled eta=0 with the stable memory-off baseline.

Require

    W relL2 <= 1e-5,
    delta_cdm relL2 <= 1e-5,
    alpha relL2 <= 5e-5,
    E relL2 <= 5e-5,
    s relL2 <= 5e-5

for every anchor.

### FM-G3 finite-memory numerical regularity

All finite-memory runs must complete with finite retained observables.

For eta <= 0.01 require at every anchor/tau cell

    A_W <= 0.25,
    A_delta <= 0.25.

This is a gross perturbative-regime guard, not a physical bound.

### FM-G4 small-eta smoothness

For each of the six anchor/tau cells compute L1 and L2.

Require at least 5/6 cells to satisfy

    max(L1,L2) <= 0.10

and all six to satisfy

    max(L1,L2) <= 0.25.

This tests a smooth first-order response without assuming an exact tangent coefficient.

### FM-G5 material memory response

At

    eta = 0.01,
    tau H0 = 10

require

    A_W >= 1e-8

for at least 2/3 anchors.

This prevents a formal PASS in which the memory sector is numerically invisible.

### FM-G6 relaxation-time dependence

At eta=0.01 require

    T_tau >= 0.01

for at least 2/3 anchors.

This is the primary finite-relaxation gate: changing the bath relaxation time must change the Weyl response materially.

## Classification priority

1. FM-G1 fail:
   `STABLE_AEST_FINITE_MEMORY_R1_INCOMPLETE`
2. FM-G2 fail:
   `STABLE_AEST_FINITE_MEMORY_R1_ZERO_REGRESSION_FAIL`
3. FM-G3 fail:
   `STABLE_AEST_FINITE_MEMORY_R1_NUMERICAL_REGULARITY_FAIL`
4. FM-G4 fail:
   `STABLE_AEST_FINITE_MEMORY_R1_ETA_SMOOTHNESS_FAIL`
5. FM-G5 fail:
   `STABLE_AEST_FINITE_MEMORY_R1_RESPONSE_TOO_SMALL`
6. FM-G6 fail:
   `STABLE_AEST_FINITE_MEMORY_R1_RELAXATION_TIME_FAIL`
7. all gates pass:
   `STABLE_AEST_FINITE_MEMORY_R1_PASS`

## Interpretation lock

A PASS establishes only that the existing causal finite-bath memory sector, when placed on the numerically certified stable-AeST host, produces a finite, smooth, nonzero response that depends on the relaxation time.

A PASS licenses a later stable-AeST growth–Weyl memory test and comparison with the host-independent MCMG first-moment relation.

A PASS does not establish observational detection, does not license an ACT/SPT claim, does not prove permanent loss of gravitational elasticity, and does not license a new-physics claim.

A FAIL remains informative and must not be reclassified after inspection.
