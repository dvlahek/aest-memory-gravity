# NL1C7B4 Repair18 — local result freeze

## Status

Frozen local WSL feasibility result from the first locked Repair18 execution.

Terminal classification:

`NL1C7B4_REPAIR18_MINIMAL_NONLINEAR_PROJECTION_FEASIBILITY_FAIL`.

The execution used HEAD

`549f02637437c2b89aa54642d6ec2b6b6d807c19`.

This is a local WSL result, not an official GitHub Actions run.

## Frozen output hashes

- result JSON:
  - bytes: `62984`
  - SHA-256:
    `8f8b6ce1316bd5cad3442ebd0cba692e4d4c82060685da083517b990cac36922`
- evaluator log:
  - bytes: `63430`
  - SHA-256:
    `d9c8415fa17fba3cd210370975bdd01c3ba196be3f20b66f4de2e80b0e1b7da8`
- local runner log:
  - bytes: `67055`
  - SHA-256:
    `34df8e60c616f65fa33af543233a5daffd2a6e6c8a9a4ce5d58fc31a147c8e66`

## Gate result

PASS:
- R18_G1 frozen provenance
- R18_G2 unprojected lambda=1 reproduction
- R18_G4 second-order correction scaling
- R18_G5 two-grid correction-amplitude control
- R18_G6 field-freeze invariant
- R18_G7 claim boundary

FAIL:
- R18_G3 canonical nonlinear solve closure

All 24 locked least-squares solves returned solver success, but 0/24 satisfied both historical exact nonlinear constraints at the preregistered 1e-7 threshold.

## Correction scaling

The combined correction norm is extremely close to quadratic in amplitude on both grids and all scales.

Representative adjacent log2 slopes:

- scale 5, Nr=256:
  `2.01358, 2.00883, 2.00775`
- scale 5, Nr=512:
  `2.01394, 2.00748, 2.01604`
- scale 10, Nr=256:
  `2.04265, 2.02322, 2.02032`
- scale 10, Nr=512:
  `2.04627, 2.02469, 2.01808`
- scale 20, Nr=256:
  `2.03400, 2.02199, 2.01872`
- scale 20, Nr=512:
  `2.03360, 2.01952, 2.01459`

Thus R18_G4 passes cleanly.

## Two-grid correction control

At lambda=1:

- scale 5:
  `C256=8.483790265345302e-7`,
  `C512=8.427234533593616e-7`,
  ratio `1.0067110665457615`;
- scale 10:
  `C256=1.5679544673532012e-5`,
  `C512=1.56305499136285e-5`,
  ratio `1.0031345512585448`;
- scale 20:
  `C256=2.1649172984256557e-5`,
  `C512=2.138399002733248e-5`,
  ratio `1.0124010045171705`.

Thus R18_G5 passes with much tighter agreement than the frozen factor-2 limit.

## Solver behavior

No solve hit a bound.

The solver typically terminated by `xtol` while the reported first-order optimality remained extremely large.

Examples:

- scale 5, Nr=256, lambda=1:
  - solver success: true
  - nfev: 20
  - optimality: `5.845487058573309e7`
  - projected H epsilon: `1.7889472614822846e-6`
  - projected M epsilon: `1.1479802636366962e-4`
- scale 10, Nr=256, lambda=1:
  - nfev: 49
  - optimality: `4.6143271580627464e7`
  - projected H epsilon: `6.934714256628259e-5`
  - projected M epsilon: `2.2007770929911516e-4`
- scale 20, Nr=256, lambda=1:
  - projected H epsilon: `8.46294665422586e-5`
  - projected M epsilon: `6.650466337451489e-6`.

The exact Q reconstruction remains zero-error and all frozen non-projection fields remain bitwise unchanged.

## Numerical diagnosis licensed by the frozen result

Repair18 does not establish non-existence of an exact projection in the physical pair `(L,R_t)`.

The result instead shows:

1. the correction direction found by the locked solver scales as O(delta^2);
2. its amplitude is grid stable;
3. all bounds remain inactive;
4. solver termination occurs with very large optimality;
5. the `R_t` correction is much smaller than the `L` correction and is represented internally in physical units.

Because scipy finite-difference steps are taken in solver coordinates, the physical-unit `delta R_t` coordinate is numerically poorly scaled relative to the dimensionless `y_L` coordinate at the tiny corrections required here.

A separately preregistered implementation repair may therefore retain exactly the same physical projection, residual, thresholds, branches, amplitude path, and bounds, but reparameterize the second solver coordinate as

`q_Rt = delta R_t / (a H R_s)`.

Repair18 itself remains FAIL and is not relabelled.

## Claim boundary

No official NPZ was written.
No source, sign, coefficient, branch, threshold, eta value, or physics was changed.
No nonlinear evolution or observational claim was made.
