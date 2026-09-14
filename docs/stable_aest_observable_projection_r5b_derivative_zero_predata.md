# Stable AeST observable projection R5b — derivative-at-zero pre-data declaration

Date: 2026-09-14

## Parent result

R5b is a post-R5a follow-up. The historical parent classification remains exactly

`STABLE_AEST_OBSERVABLE_PROJECTION_R5A_LOCAL_ETA_SCALING_FAIL`.

R5a post-data lock: `118c680c3c05e7ca95bbc16700bd846e200a7ab6`.

R5b does not reclassify R5a, R5, or any earlier result.

## Scientific question

Does a reproducible derivative-at-zero observable tangent emerge on a smaller physical eta interval, even though R5a showed that eta = 0.1, 0.25, and 0.5 do not define a common tangent for effective f sigma8 and linear CMB lensing?

The same three linear integrated observables are retained:

- total-matter sigma8(z),
- effective f sigma8(z),
- linear CMB lensing convergence C_L^{kappa kappa} derived from raw CLASS C_L^{phi phi}.

This is still an observable-projection convergence audit, not a likelihood or detection claim.

## Frozen source/model

Identical physical model and observable definitions to R5/R5a:

- CLASS/AeST parent head `e85808324f51fc694d12e3ed7439552a3c3f9540`,
- stable-chi residual patch,
- exactly one physical memory multiplier `Bchi_aest *= pba->aest_eta;`,
- exactly one physical closure `E_rhs_aest -= 0.5*Q_aest*Bchi_aest;`,
- zero diagnostic `aest_tangent_external_force` injections in `perturbations_derivs`,
- tau H0 = 10,
- memory order = 20,
- no nonlinear/Halofit correction,
- growth redshifts z = [0.2, 0.5, 1.0, 1.5, 2.0],
- lensing multipoles 40 <= L <= 2000,
- P_k_max_h/Mpc = 5,
- l_max_scalars >= 2000.

The observable definitions remain exactly:

- `Class.sigma(8.0, z, h_units=True)`,
- `Class.effective_f_sigma8(z, z_step=0.1)`,
- `C_L^{kappa kappa} = [L(L+1)/2]^2 C_L^{phi phi}` from raw CLASS `pp`.

## Small-eta physical scan

Nominal perturbation tolerance: `3e-8`.

Certification eta values:

`eta = [0, 0.01, 0.025, 0.05]`.

A bridge run at `eta = 0.1` is also frozen, but it is diagnostic only and does not enter the certification gates. It connects R5b continuously to the completed R5a domain.

No signed or external variational amplifier is permitted.

For each observable vector X,

`T_X(eta) = [X(eta)-X(0)]/[eta X(0)]`.

The derivative-at-zero consistency test uses only:

- T(0.01) versus T(0.025),
- T(0.025) versus T(0.05).

T(0.05) versus T(0.1) is reported only as a bridge diagnostic.

## Precision control

A separate tighter pair at tolerance `1e-8` is frozen for eta = 0 and eta = 0.01.

This directly tests the smallest physical tangent used for certification.

## Gates

### R5b-G1 provenance/parent

PASS iff the R5a post-data lock is an ancestor and the parent R5a JSON has the exact classification `STABLE_AEST_OBSERVABLE_PROJECTION_R5A_LOCAL_ETA_SCALING_FAIL` with diagnostic_complete = true.

### R5b-G2 source topology

PASS iff the disposable science source has the stable-chi marker, exactly one physical eta multiplier, exactly one physical memory closure, and zero diagnostic external-force injections in `perturbations_derivs`.

### R5b-G3 finite observable runs

PASS iff all five nominal runs eta = 0, 0.01, 0.025, 0.05, 0.1 and both tight-control runs eta = 0, 0.01 complete with finite sigma8(z), finite effective f sigma8(z), and finite C_L^{kappa kappa} over the frozen domains; sigma8 and C_L^{kappa kappa} must remain positive.

### R5b-G4 smallest-eta precision stability

For each observable compare nominal T_X(0.01) with tight-control T_X(0.01).

PASS per observable iff relative vector-L2 error <= 0.10 and cosine >= 0.995.

G4 PASS iff all three observables pass.

### R5b-G5 derivative-at-zero eta consistency

For each observable require both certification comparisons:

- T_X(0.01) versus T_X(0.025): relative vector-L2 error <= 0.10 and cosine >= 0.995,
- T_X(0.025) versus T_X(0.05): relative vector-L2 error <= 0.10 and cosine >= 0.995.

G5 PASS iff all three observables pass both comparisons.

The T_X(0.05) versus T_X(0.1) comparison is recorded but is not a gate.

### R5b-G6 resolved derivative-at-zero response

PASS iff G4 and G5 pass and all nominal T_X(0.01) vectors are finite with nonzero L2 norm.

No sign is preregistered.

## Classification priority

1. `STABLE_AEST_OBSERVABLE_PROJECTION_R5B_INCOMPLETE`
2. `STABLE_AEST_OBSERVABLE_PROJECTION_R5B_SOURCE_TOPOLOGY_FAIL`
3. `STABLE_AEST_OBSERVABLE_PROJECTION_R5B_RUN_FAIL`
4. `STABLE_AEST_OBSERVABLE_PROJECTION_R5B_PRECISION_UNRESOLVED`
5. `STABLE_AEST_OBSERVABLE_PROJECTION_R5B_DERIVATIVE_SCALING_FAIL`
6. `STABLE_AEST_OBSERVABLE_PROJECTION_R5B_RESPONSE_UNRESOLVED`
7. if G1–G6 pass: `STABLE_AEST_OBSERVABLE_PROJECTION_R5B_DERIVATIVE_ZERO_CERTIFIED`.

## Claim discipline

A PASS licenses only a reproducible local derivative-at-zero projection of the stable-AeST memory response into sigma8, effective f sigma8, and linear CMB lensing convergence in the locked tau-H0=10 setup.

It does not license any observational likelihood, detection, parameter bound, ACT/DESI/RSD preference, or positive growth-Weyl separation claim.

A FAIL must remain historical. In particular, no post-data threshold relaxation or retroactive substitution of the diagnostic eta=0.1 bridge into the certification interval is permitted.