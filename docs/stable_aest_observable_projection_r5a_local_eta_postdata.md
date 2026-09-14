# Stable AeST observable projection R5a — local-eta tangent post-data

Date: 2026-09-14

## Historical status

R5a completed with the formal classification

`STABLE_AEST_OBSERVABLE_PROJECTION_R5A_LOCAL_ETA_SCALING_FAIL`.

This is a completed science outcome, not a technical/runtime failure. It does not reclassify R5 or any earlier result.

Parent R5 classification remains

`STABLE_AEST_OBSERVABLE_PROJECTION_R5_ETA_SCALING_FAIL`.

R5a pre-data lock: `d728b9629866da83182f5324988dea659eb61f0d`.
R5 post-data lock: `7e02d7789c7478f56c1c63b7fa94ca59192d4ac4`.

## Completed run validity

All six physical CLASS runs completed with finite outputs on the frozen domains:

- nominal eta = 0, 0.1, 0.25, 0.5 at tolerance 3e-8;
- tight eta = 0, 0.1 at tolerance 1e-8.

The disposable source passed the frozen single-channel topology audit: one physical eta multiplier, one physical memory closure, and zero diagnostic external-force injections in `perturbations_derivs`.

## Gate outcomes

- G1 provenance and parent lock: PASS.
- G2 single-channel source topology: PASS.
- G3 finite observable runs: PASS.
- G4 smallest-eta precision stability: PASS.
- G5 local eta-tangent consistency: FAIL.
- G6 resolved local response: formally FALSE because certification requires G4 and G5; the individual eta=0.1 response vectors themselves were finite and nonzero for all three observables.

## Observable metrics

### sigma8

Precision, nominal eta=0.1 versus tight eta=0.1:

- relative vector-L2 error = 1.7186975476221332e-05,
- cosine = 0.9999999999814404.

Local eta consistency:

- T(0.1) versus T(0.25): E = 0.023961463262074673, C = 0.9997168630911835;
- T(0.25) versus T(0.5): E = 0.009053056801357685, C = 0.9999975216052475.

Thus sigma8 passes the preregistered local-eta consistency gate.

### effective f sigma8

Precision, nominal eta=0.1 versus tight eta=0.1:

- E = 0.00010807273958466366,
- C = 0.9999999967137259.

Local eta consistency:

- T(0.1) versus T(0.25): E = 0.13491012706550373, C = 0.9910734348254062;
- T(0.25) versus T(0.5): E = 0.10992263976383485, C = 0.9939827692316474.

Thus effective f sigma8 fails the preregistered local-eta consistency gate.

### linear CMB lensing convergence

Precision, nominal eta=0.1 versus tight eta=0.1:

- E = 2.1315112661770028e-05,
- C = 0.9999999998026443.

Local eta consistency:

- T(0.1) versus T(0.25): E = 0.11424850507127694, C = 0.9942630840300234;
- T(0.25) versus T(0.5): E = 0.19724324743810706, C = 0.9808752216818967.

The eta=0.1 lensing tangent is sign-changing over the frozen multipole range, with minimum -3.14651566403766e-06 and maximum 2.7058519880439887e-06.

Thus linear CMB lensing convergence fails the preregistered local-eta consistency gate.

## Interpretation

The failure is not explained by the tested perturbation-integration tolerance: the nominal-versus-tight eta=0.1 tangents agree extremely well for sigma8, effective f sigma8, and lensing.

R5a therefore rejects the specific preregistered claim that eta = 0.1, 0.25, and 0.5 already define a common first-order observable tangent for all three integrated observables. Sigma8 is locally consistent over this range, while effective f sigma8 and CMB lensing are not.

This does not establish that the derivative at eta=0 does not exist. It motivates, but does not itself license, a separately preregistered smaller-eta convergence audit. The existing R5a result must remain historical and unchanged.

No observable projection, likelihood, observational detection, parameter bound, ACT/DESI/RSD preference, or positive growth-Weyl separation claim is licensed by R5a.
