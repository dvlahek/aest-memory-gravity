# Stable AeST observable projection R5 — pre-data declaration

Date: 2026-09-14

## Parent result

R5 is licensed only by the completed R4 classification

`STABLE_AEST_GROWTH_WEYL_MEMORY_R4_SINGLE_AMPLITUDE_MODE_CERTIFIED`.

R4 post-data lock: `c7c317be346371d0943e29b1b16016f9c36ef704`.

R5 does not alter or reinterpret R1–R4 historical outcomes.

## Scientific question

Does the certified stable-AeST single-amplitude scalar memory response survive projection into integrated linear observables, specifically total-matter sigma8(z), effective f sigma8(z), and the CMB lensing convergence spectrum derived from CLASS C_L^{phi phi}?

This is an observable-projection test, not an observational likelihood or detection claim.

## Frozen model/source

- CLASS/AeST parent head: `e85808324f51fc694d12e3ed7439552a3c3f9540`.
- Stable-chi residual patch required.
- The disposable R5 science source must contain exactly one physical memory multiplier `Bchi_aest *= pba->aest_eta;`, exactly one physical closure `E_rhs_aest -= 0.5*Q_aest*Bchi_aest;`, and no diagnostic `aest_tangent_external_force` injection in `perturbations_derivs`.
- `tau H0 = 10`.
- memory order = 20.
- no nonlinear/Halofit correction.

## Observable definitions

### Total-matter sigma8(z)

Use the CLASS Python wrapper directly:

`Class.sigma(8.0, z, h_units=True)`.

No transfer-function proxy is permitted.

### Effective f sigma8(z)

Use the CLASS Python wrapper directly:

`Class.effective_f_sigma8(z, z_step=0.1)`.

This quantity is the wrapper's direct finite-difference estimate of `d sigma8 / d ln a` around the requested redshift.

Frozen redshifts for both growth observables:

`z = [0.2, 0.5, 1.0, 1.5, 2.0]`.

### Linear CMB lensing convergence

Request CLASS lensing-potential spectra and use the raw harmonic output `pp = C_L^{phi phi}` with no nonlinear matter correction.

Convert to convergence through

`C_L^{kappa kappa} = [L(L+1)/2]^2 C_L^{phi phi}`.

Science multipoles:

`40 <= L <= 2000`.

The CLASS run must use `l_max_scalars >= 2000` and a sufficiently large linear matter-power support (`P_k_max_h/Mpc = 5`).

## Physical eta scan

The R4 response is extremely small. R5 therefore uses a response-amplified but still physical eta scan:

`eta = [0, 1, 10]`.

These are physical model runs, not signed diagnostic amplifiers. A tangent inferred from eta=10 is licensed as a first-order projection only if it agrees with eta=1 under the gates below.

For an observable vector X,

`T_X(eta) = [X(eta)-X(0)]/[eta X(0)]`.

## Precision control

Nominal perturbation tolerance: `3e-8`.

A tighter-control pair is frozen at `1e-8` for `eta=0` and `eta=10`. The tight pair is used only to assess numerical stability of the projected tangent; it does not replace the nominal result.

## Gates

### R5-G1 provenance/parent

PASS iff the R4 post-data lock is an ancestor, the parent R4 JSON has the exact certified classification, and frozen source provenance checks pass.

### R5-G2 source topology

PASS iff the disposable science source has the certified stable-chi marker, one physical eta multiplier, one physical memory closure, and zero diagnostic external-force injections in `perturbations_derivs`.

### R5-G3 finite observable runs

PASS iff all nominal eta runs and both tight-control runs complete with finite positive sigma8(z), finite effective f sigma8(z), and finite positive C_L^{kappa kappa} over all science multipoles.

### R5-G4 physical-eta tangent consistency

For each of sigma8, effective f sigma8, and C_L^{kappa kappa}, compare `T_X(1)` with `T_X(10)`.

Strict PASS for an observable: relative vector-L2 error <= 0.05 and cosine >= 0.999.

R5-G4 PASS iff all three observables pass strict consistency.

### R5-G5 precision stability

Construct the eta=10 tangent independently from the tight-control pair. Compare nominal and tight eta=10 tangents.

PASS for an observable: relative vector-L2 error <= 0.10 and cosine >= 0.995.

R5-G5 PASS iff all three observables pass.

### R5-G6 resolved observable response

PASS iff all three nominal eta=10 tangent vectors are finite and have nonzero L2 norm, and the tight-control comparison in G5 has passed. No sign is preregistered.

## Classification priority

1. `STABLE_AEST_OBSERVABLE_PROJECTION_R5_INCOMPLETE`
2. `STABLE_AEST_OBSERVABLE_PROJECTION_R5_SOURCE_TOPOLOGY_FAIL`
3. `STABLE_AEST_OBSERVABLE_PROJECTION_R5_RUN_FAIL`
4. `STABLE_AEST_OBSERVABLE_PROJECTION_R5_ETA_SCALING_FAIL`
5. `STABLE_AEST_OBSERVABLE_PROJECTION_R5_PRECISION_UNRESOLVED`
6. `STABLE_AEST_OBSERVABLE_PROJECTION_R5_RESPONSE_UNRESOLVED`
7. if G1–G6 pass: `STABLE_AEST_OBSERVABLE_PROJECTION_R5_CERTIFIED`.

## Claim discipline

A PASS licenses only the statement that the stable-AeST memory response projects reproducibly into these three linear integrated observables in the locked tau-H0=10 regime.

It does not license an ACT, DESI, RSD, CMB-lensing, or other observational detection, parameter bound, likelihood preference, or positive growth–Weyl separation claim. Those require a separate preregistered likelihood stage.
