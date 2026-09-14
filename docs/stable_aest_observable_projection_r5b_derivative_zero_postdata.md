# Stable AeST observable projection R5b — derivative-at-zero post-data

Date: 2026-09-14

## Formal outcome

R5b completed with

`STABLE_AEST_OBSERVABLE_PROJECTION_R5B_DERIVATIVE_ZERO_CERTIFIED`.

This is a completed science PASS. It does not reclassify R5 or R5a. Historical outcomes remain:

- `STABLE_AEST_OBSERVABLE_PROJECTION_R5_ETA_SCALING_FAIL`;
- `STABLE_AEST_OBSERVABLE_PROJECTION_R5A_LOCAL_ETA_SCALING_FAIL`.

R5b pre-data lock: `f6886b2b934330036e9239e3fb2d3678dee3c72f`.
R5a post-data lock: `118c680c3c05e7ca95bbc16700bd846e200a7ab6`.

## Completed run validity

All seven direct physical CLASS runs completed with finite outputs on the frozen domains:

- nominal eta = 0, 0.01, 0.025, 0.05;
- non-gating bridge eta = 0.1;
- tight eta = 0, 0.01.

The disposable source passed the single-channel topology audit: one physical eta multiplier, one physical memory closure, and zero diagnostic external-force injections in `perturbations_derivs`.

## Gate outcomes

All preregistered gates passed:

- G1 provenance and parent lock: PASS;
- G2 single-channel source topology: PASS;
- G3 finite observable runs: PASS;
- G4 smallest-eta precision stability: PASS;
- G5 derivative-at-zero eta consistency: PASS;
- G6 resolved derivative-at-zero response: PASS.

## Derivative-at-zero consistency

### sigma8

Precision, nominal eta=0.01 versus tight eta=0.01:

- E = 7.24986766557888e-05;
- C = 0.9999999988268804.

Derivative convergence:

- T(0.01) versus T(0.025): E = 0.0012324380073038376, C = 0.9999992493630907;
- T(0.025) versus T(0.05): E = 0.002251729101888944, C = 0.9999975659703252.

The eta=0.01 fractional tangent is positive on all frozen redshifts z=[0.2,0.5,1.0,1.5,2.0], with values approximately

- 1.1137522841e-06,
- 3.2253844452e-07,
- 5.0351484640e-08,
- 7.4969968068e-09,
- 1.5213433379e-09.

### effective f sigma8

Precision:

- E = 0.0008277584322778172;
- C = 0.9999998016672529.

Derivative convergence:

- T(0.01) versus T(0.025): E = 0.005270802905218184, C = 0.9999869028140602;
- T(0.025) versus T(0.05): E = 0.01035593852712982, C = 0.9999504397809247.

The eta=0.01 fractional tangent is positive on all frozen redshifts, approximately

- 3.8998907395e-06,
- 4.2653948717e-06,
- 4.6173385394e-07,
- 8.1614328048e-08,
- 1.5924806715e-08.

### linear CMB lensing convergence

Precision:

- E = 0.0002860292294686824;
- C = 0.9999999639661072.

Derivative convergence:

- T(0.01) versus T(0.025): E = 0.0111118118817769, C = 0.9999533492490863;
- T(0.025) versus T(0.05): E = 0.018518254074765234, C = 0.9998677814410751.

The eta=0.01 lensing tangent is resolved and sign-changing across 40<=L<=2000. Its minimum is approximately -3.2414192957e-06 at L=1138 and its maximum is approximately 2.4765268065e-06 at L=2000. The tangent changes sign near L=596 and again near L=1817.

Representative eta=0.01 fractional lensing tangents are approximately:

- L=40: 1.57e-08;
- L=100: 5.69e-08;
- L=200: 1.78e-07;
- L=400: 3.77e-07;
- L=600: -1.69e-08;
- L=800: -1.22e-06;
- L=1000: -2.70e-06;
- L=1500: -1.87e-06;
- L=2000: 2.48e-06.

## Non-gating eta=0.1 bridge

The eta=0.05 versus eta=0.1 bridge was not part of certification. It remained reasonably close but showed increasing nonlinearity:

- sigma8: E = 0.004954967241110721, C = 0.9999879614462938;
- effective f sigma8: E = 0.024836567645797582, C = 0.9997123999717742;
- C_L^{kappa kappa}: E = 0.03761746734612704, C = 0.9994362757631929.

This is consistent with R5/R5a: the local derivative exists near eta=0, while larger eta values increasingly leave the first-order regime, especially for integrated lensing.

## Interpretation

R5b licenses a reproducible derivative-at-zero observable tangent for total-matter sigma8(z), effective f sigma8(z), and linear CMB lensing convergence C_L^{kappa kappa} in the locked tau-H0=10 stable-AeST setup.

The result connects the previously certified single-amplitude scalar memory response to integrated linear observables. Growth observables respond with a positive late-time tangent on the frozen redshift grid. Lensing exhibits a reproducible scale-dependent sign-changing tangent, so projection through the line-of-sight kernel is not equivalent to a uniform rescaling of C_L^{kappa kappa} even though the underlying phi, psi, and matter transfer responses are nearly common-amplitude.

No likelihood preference, observational detection, parameter bound, ACT/DESI/RSD claim, or positive growth-Weyl separation is licensed by R5b. Those require a separate preregistered likelihood stage.
