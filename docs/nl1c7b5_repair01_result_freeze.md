# NL1C7B5 Repair01 — result freeze

## Status

Frozen first locked Repair01 execution after analytic regular-center source completion.

Terminal classification:

`NL1C7B5_CONSERVATIVE_DIFFERENTIAL_CERTIFICATION_FAIL`.

Science return code:

`SCIENCE_RC=2`.

Execution HEAD:

`07d767a918d13ce92f07c0718b47fd7333ba89f5`.

The run began with:

`NL1C7B5_REPAIR01_REGULAR_CENTER_LOCK_PASS`.

This is a complete B5 science result, not an implementation failure.

## Frozen output hashes

Result JSON:

- bytes: `23396`
- SHA-256:
  `bfeae8019b69f23e0fa659c6c3e0134353b85e0dcd67f0337c14d6f50b887c8d`.

Evaluator log:

- bytes: `23842`
- SHA-256:
  `af3096b43a25bb40916262e36ea1346721e195cf0bab26d7ff6276cce1ab9df5`.

Full runner log:

- bytes: `31604`
- SHA-256:
  `120320347eb706f4581629ac69e857c6b3fb76b3dc7d80d96215db8237fd6ae8`.

No corrected-state NPZ was written.

## Parent implementation failure

The original first B5 execution remains frozen separately as

`NL1C7B5_CONSERVATIVE_INITIAL_DATA_IMPLEMENTATION_FAIL`

with result JSON SHA-256

`6f59e45621d4895ee8fbb4ce125943fcd2939a534a7266fbebae4759190f79bc`.

Repair01 does not relabel that historical result.

Repair01 only replaces the undefined raw center source representation by the analytic regular-center limits

`S_H(0)=0`

and

`S_M(0)=0`.

## Gate result

PASS:

- B5_G1 frozen provenance;
- B5_G2 conservative decomposition identity;
- B5_G3 orthonormal gauge representation;
- B5_G4 complete conservative construction;
- B5_G5 safety, exact-Q, gauge and field freeze;
- B5_G7 two-grid correction control;
- B5_G8 output integrity;
- B5_G9 claim boundary.

FAIL:

- B5_G6 original differential exact constraints.

Thus the implementation repair succeeded and exposed the intended B5 science test.

## Regular-center repair verification

All six cases report finite conservative residuals at the frozen start `z=0`.

The center implementation bug from the original B5 run is therefore removed.

The raw lambdified expressions still emit harmless floating-point warnings before the analytic center assignment, but the conservative residual passed to the nonlinear solver is finite in all six cases.

No noncenter physical source, quadrature rule, solver setting, threshold or field definition changed.

## Complete conservative construction

Exactly six preregistered cases were attempted:

- scale 5 h^-1 Mpc, Nr=256;
- scale 5 h^-1 Mpc, Nr=512;
- scale 10 h^-1 Mpc, Nr=256;
- scale 10 h^-1 Mpc, Nr=512;
- scale 20 h^-1 Mpc, Nr=256;
- scale 20 h^-1 Mpc, Nr=512.

All six returned finite safe states.

For all six:

- exact-Q normalized error is zero at reported precision;
- Y4 and Qmean remain at floating-point zero;
- all nonprojection fields remain bitwise frozen;
- source/flux decomposition remains consistent with the original B4 differential numerator.

The returned corrections stay inside the frozen safety bounds.

## Nonlinear driver behavior

All six TRF solves reach the frozen `max_nfev=200` limit with solver status 0.

Solver success is false in every case.

This does not convert the run into an implementation failure because the preregistration explicitly states that solver success/status is recorded but is not by itself the science criterion.

No additional evaluations, restart, alternate solver, tolerance change or continuation are licensed.

## Conservative residual behavior

The conservative objective decreases only modestly.

For Nr=256, representative full conservative L2 values are approximately:

- scale 5:
  `0.0381012493 -> 0.0339851780`;
- scale 10:
  `0.0381013206 -> 0.0339852676`;
- scale 20:
  `0.0381014456 -> 0.0339853586`.

For Nr=512:

- scale 5:
  `0.0381012446 -> 0.0339838794`;
- scale 10:
  `0.0381012627 -> 0.0339839019`;
- scale 20:
  `0.0381012947 -> 0.0339839243`.

The Hamiltonian conservative maximum remains approximately

`3.07e-2`

after construction.

The momentum conservative residual, which is initially much smaller, increases during the solve to approximately

`7.4e-6--2.5e-5`

in maximum normalized cell residual.

This indicates that the frozen conservative objective itself is not approaching zero under the preregistered two-field construction.

## Original differential certification

The decisive original B4 differential gate fails in all six cases.

Maximum exact differential residuals after construction are:

- scale 5, Nr=256:
  - H: `0.04245571532982025`
  - M: `0.9999999999999825`;
- scale 5, Nr=512:
  - H: `0.042382180710090915`
  - M: `0.999999999999982`;
- scale 10, Nr=256:
  - H: `0.042454046851644375`
  - M: `0.9999999999999893`;
- scale 10, Nr=512:
  - H: `0.04238175363839366`
  - M: `0.9999999999999891`;
- scale 20, Nr=256:
  - H: `0.042447140347855655`
  - M: `0.99999999999999`;
- scale 20, Nr=512:
  - H: `0.04237992699942037`
  - M: `0.9999999999999901`.

The historical exact certification threshold remains

`1e-7`.

Therefore every case fails by many orders of magnitude.

The failure is systematic across scale and grid resolution, not a single-case outlier.

## Two-grid control

The correction-amplitude two-grid control passes for all scales.

Symmetric Nr256/Nr512 correction ratios are:

- scale 5:
  `1.7236598674876025`;
- scale 10:
  `1.7218237728581751`;
- scale 20:
  `1.7225161300364087`.

All remain below the frozen limit 2.0.

Thus the failure of the differential certification is not caused by a failure of the preregistered two-grid correction-amplitude control.

## Scientific interpretation

Repair01 establishes that the B5 conservative constructor can be executed consistently after analytic regular-center completion, but it does not produce an initial state that satisfies the original exact B4 differential constraints.

The failure is substantially larger than the historical `1e-7` gate:

- H remains at approximately `4.24e-2`;
- M remains effectively unity.

The nearly scale-independent and grid-paired values show that this outcome is reproducible across the frozen benchmark family.

This result does not prove that an exact physical `(L,R_t)` solution does not exist.

It does establish that two distinct frozen construction strategies have now failed to produce a certified state in the same double-precision two-field framework:

1. the pointwise differential Gauss-Newton track through Repair19c4;
2. the preregistered conservative cell-integrated B5 constructor.

## Project decision boundary

The frozen B5 boundary now applies.

Therefore:

- no B5a/B5b solver-parameter repair is licensed;
- increasing `max_nfev` is not licensed;
- changing TRF settings is not licensed;
- trying another finite-difference step is not licensed;
- multistart, continuation, damping or alternate nonlinear solvers are not licensed inside B5;
- the exact `1e-7` differential threshold remains unchanged;
- no B5 state NPZ is licensed;
- eta=0 short-time evolution is not licensed from B5;
- finite eta is not certified;
- no observational AeST result is licensed from this initial-data track;
- no physical nonexistence claim for `(L,R_t)` is justified.

Any further initial-data work must be a genuinely different project-level representation, for example analytically reduced constraints or higher-precision arithmetic, and must be separately preregistered before implementation.

Alternatively the project may stop the nonlinear spherical initial-data program and continue only the already separated observational/tangent infrastructure without presenting it as a tested finite-eta nonlinear AeST prediction.
