# Stable AeST DESI DR1 R9b2g bounded-source extraction post-result record

## Historical classification

R9b2g completed with

`STABLE_AEST_DESI_DR1_R9B2G_CENTRAL_DERIVATIVE_FAIL`

and `EXIT=1`.

This classification is retained permanently. It does not reclassify any earlier R9b/R9b2/R9b2a/R9b2b/R9b2c/R9b2d/R9b2e/R9b2f result.

No DESI data vector, covariance, likelihood, eta preference, or tau constraint was evaluated.

## Frozen artifacts

Local completed artifacts supplied after the run:

- JSON SHA-256: `2e2be7821088b8bbe2f152d8ee03cc950d3d4270d4725286dd0e976a522f4d34`
- science log SHA-256: `eb75011d498aeabe7e8282114b4d2eb3d10901e994363aa70b3116f7ff625cb3`
- full-runner log SHA-256: `c56662b54ce1bad1293ea53bb7ff120cf211df48a54dd4be13474cd64e7c21cc`.

R9b2g preregistration: `2ea44eb92319fc6c2a3273dc91254e14dc797e35`.
R9b2g implementation: `ca8b788a40bc5de1649f53ff4cfe7ace5aa1500b`.
R9b2g runner: `1d1affe23676d7c2ef5baa0e1562cae98258dd4a`.
Parent R9b2f postdata: `b569aebc41efc841755f5fcec63b91092c192ba3`.

## Gate result

- G1 provenance and construction: PASS
- G2 full-grid finite physical: PASS
- G3 independent bounded-integral agreement: PASS
- G4 eta=0 internal closure: PASS
- G5 eta=0 tau invariance: PASS
- G6 central derivative consistency: FAIL.

The bounded extraction itself is numerically well behaved:

- maximum bounded-cosmoprimo vs bounded-loglinear relative discrepancy:
  - `sigma8_dd = 8.689925958595555e-05`
  - `sigma8_tt = 2.377867695753983e-04`
  - `f = 1.5090062314196157e-04`
- maximum eta=0 source/internal discrepancy:
  - `sigma8 = 4.363621755422454e-03`
  - `f = 1.2627260454545774e-03`
- maximum eta=0 tau variation:
  - `sigma8_dd = 5.325194681550037e-10`
  - `sigma8_tt = 9.398982297121738e-10`
  - `f = 4.4035506990721125e-10`.

Thus the R9b2f high-k extrapolation repair remains successful at the value level over all 20 frozen `(tau,eta)` cases.

## Frozen G6 failure

Using bounded cosmoprimo interpolation, the preregistered primary/control central derivative comparison gave:

| tau_H0 | E | C |
|---:|---:|---:|
| 10 | 0.05935989800149155 | 0.9999999301009804 |
| 5 | 0.058329910203837966 | 0.9999999359610111 |
| 2.5 | 0.05635676262594108 | 0.9999999359742759 |
| 1.25 | 0.052691723089789776 | 0.999999942632074 |

The frozen gate was `E <= 0.05` and `C >= 0.995`, so G6 correctly fails for all four tau values. The threshold is not changed post-result.

The failure is almost purely an amplitude mismatch. The tangent directions are essentially identical (`C > 0.99999993`). It is also dominated by the first theory coordinate `z=0.295364...`: bounded-cosmoprimo gives first-component tangents of order `-2.2e-4` to `-2.5e-4`, while the remaining five components are mostly `~1e-6` or smaller.

## Post-result diagnostic from the already stored independent quadrature

R9b2g stored, for every one of the same 20 CLASS runs, both bounded-cosmoprimo and independent bounded log-linear sigma8 values. No new CLASS evaluation is needed to compare their finite-difference behavior.

Recomputing the same primary/control central derivative from the stored **bounded log-linear** `f` values gives:

| tau_H0 | E_loglinear | C_loglinear |
|---:|---:|---:|
| 10 | 0.02599485727739099 | 0.9999311345375457 |
| 5 | 0.025906329840608897 | 0.9999397466268711 |
| 2.5 | 0.024472498905480325 | 0.9999382643471886 |
| 1.25 | 0.023054305193538793 | 0.9999440833413786 |

All four satisfy the original `E <= 0.05`, `C >= 0.995` criterion. This is a **post-result diagnostic only** and does not convert R9b2g to PASS.

At `tau_H0=10`, for example, the first derivative component changes from approximately

- bounded cosmoprimo primary: `-2.3715435524929163e-04`
- bounded cosmoprimo control: `-2.521204635719254e-04`

to

- bounded log-linear primary: `+2.491788718917531e-06`
- bounded log-linear control: `+2.56610907611865e-06`.

Thus a value-level method difference of only about `1e-4` relative is large compared with the very small eta derivative being estimated and can dominate the finite-difference tangent. The R9b2g G6 failure therefore localizes a **derivative-level interpolation sensitivity**, not a failure of the AeST solver, transfer mapping, bounded-support construction, eta=0 closure, or tau invariance.

## Consequence

A corrected ShapeFit science projection is still **not licensed** by R9b2g. Before loading DESI data, the derivative must be validated with a separately preregistered bounded quadrature audit that:

1. avoids generic spectral extrapolation;
2. tests convergence with integration resolution;
3. compares at least two shape-preserving/direct bounded quadratures;
4. verifies the original `E <= 0.05`, `C >= 0.995` primary/control derivative gate for each method;
5. verifies cross-method tangent agreement; and
6. checks convergence when the actual CLASS support is extended to higher `P_k_max_h/Mpc`.

No observational likelihood should be evaluated until that derivative-level audit passes.
