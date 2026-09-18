# NL1C7B4 Repair18a — local result freeze

## Status

Frozen local WSL result from the first locked Repair18a execution.

Terminal classification:

`NL1C7B4_REPAIR18A_DIMENSIONLESS_RT_COORDINATE_FEASIBILITY_FAIL`.

Execution HEAD:

`f0434b8fbf76de11427a62d5563272afd915ce55`.

This is a local WSL result, not an official GitHub Actions run.

## Frozen output hashes

- result JSON:
  - bytes: `63534`
  - SHA-256:
    `29a81013b42ebe22989ca1a00b48bb2bb33447677bb77db6aefee298c7159782`
- evaluator log:
  - bytes: `63980`
  - SHA-256:
    `57ce0587d12cd276c9bb12e302fb8bebeb28aaa73126a51eb52107af956142e8`
- local runner log:
  - bytes: `67802`
  - SHA-256:
    `9df0ac939a8edc678475fc3e2d25856d944e0fc33d49afe5e7102aab6c79b765`.

## Gate result

PASS:
- R18A_G1 frozen provenance
- R18A_G2 unprojected lambda=1 reproduction
- R18A_G4 second-order correction scaling
- R18A_G5 two-grid correction-amplitude control
- R18A_G6 field-freeze invariant
- R18A_G7 coordinate-equivalence and claim boundary

FAIL:
- R18A_G3 canonical nonlinear solve closure

All 24 locked solves returned solver success but 0/24 satisfied both exact nonlinear constraints at the historical `1e-7` threshold.

## Coordinate-repair comparison with Repair18

Repair18a changed only the solver coordinate from physical `delta R_t` to

`q_Rt = delta R_t/(a H R_s)`.

The physical correction norm remained almost unchanged from Repair18.

At lambda=1:

- scale 5, Nr=256:
  - Repair18 correction norm: `8.483790265345302e-7`
  - Repair18a correction norm: `8.483791371805613e-7`
- scale 10, Nr=256:
  - Repair18: `1.5679544673532012e-5`
  - Repair18a: `1.5681166125114954e-5`
- scale 20, Nr=256:
  - Repair18: `2.1649172984256557e-5`
  - Repair18a: `2.164911461158314e-5`.

Hamiltonian closure is essentially unchanged.

Momentum closure improves in several lambda=1 cases but remains far above the historical threshold:

- scale 5, Nr=256:
  - Repair18 M: `1.1479802636366962e-4`
  - Repair18a M: `1.1006869013274092e-4`
- scale 5, Nr=512:
  - Repair18 M: `3.6038225967086957e-4`
  - Repair18a M: `2.6837585173549133e-4`
- scale 10, Nr=256:
  - Repair18 M: `2.2007770929911516e-4`
  - Repair18a M: `1.7160210901977888e-4`
- scale 10, Nr=512:
  - Repair18 M: `5.715993862656362e-4`
  - Repair18a M: `3.3534705483588643e-4`.

The change therefore does not rescue exact closure and does not support the hypothesis that physical-unit `delta R_t` scaling was the sole failure mechanism.

## Correction scaling

All six scale/grid paths remain cleanly quadratic.

Representative adjacent log2 slopes:

- scale 5, Nr=256:
  `2.01357, 2.00887, 2.00727`
- scale 5, Nr=512:
  `2.01334, 2.00811, 2.00646`
- scale 10, Nr=256:
  `2.04250, 2.02454, 2.01636`
- scale 10, Nr=512:
  `2.04677, 2.02568, 2.01685`
- scale 20, Nr=256:
  `2.03401, 2.02193, 2.01896`
- scale 20, Nr=512:
  `2.03359, 2.01951, 2.01427`.

## Two-grid correction control

At lambda=1:

- scale 5 ratio:
  `1.006700522865515`
- scale 10 ratio:
  `1.0028476535935`
- scale 20 ratio:
  `1.0123990431992982`.

All pass the frozen factor-2 gate by a large margin.

## Solver behavior

Every lambda=1 solve has inactive bounds and terminates by `xtol`.

Representative lambda=1 rows:

- scale 5, Nr=256:
  - H: `1.7889413434231663e-6`
  - M: `1.1006869013274092e-4`
  - optimality: `3.6766043954700336e7`
- scale 10, Nr=256:
  - H: `6.935250462804677e-5`
  - M: `1.7160210901977888e-4`
  - optimality: `2.171041496061589e7`
- scale 20, Nr=256:
  - H: `8.462938110491739e-5`
  - M: `6.505439993722767e-6`
  - optimality: `7.342287920892342e4`.

Thus the numerical termination still occurs well before the frozen exact-constraint target.

## Interpretation

Repair18a is a clean negative result for the single-coordinate-rescaling hypothesis.

It does not establish that the physical pair `(L,R_t)` is infeasible, because the frozen solver still uses the same sparse finite-difference Jacobian approximation and termination machinery as Repair18.

The next admissible diagnostic is therefore to audit Jacobian fidelity without changing the physical projection pair or classification threshold.

## Claim boundary

Repair18 remains FAIL.
Repair18a remains FAIL.
No official NPZ was written.
No source, sign, coefficient, branch, threshold, eta value, point set, or physics was changed.
No nonlinear evolution or observational claim was made.
