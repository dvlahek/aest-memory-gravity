# NL1C7B4 Repair19c — local result freeze

## Status

Frozen local WSL science result from the first locked Repair19c execution.

Terminal classification:

`NL1C7B4_REPAIR19C_ORTHONORMAL_DIRECT_GN_NONLINEAR_CLOSURE_FAIL`

with

`SCIENCE_RC=2`.

Execution HEAD:

`2d59ebeef39bc2c4936eb3d6a465da25cc9613cf`.

This is a local WSL result, not an official GitHub Actions run.

## Frozen output hashes

- result JSON:
  - bytes: `293215`
  - SHA-256:
    `5ad02254c512f90d0f82a42d0f5aa00f15c1dae6248bdbe7ad69addb183b600a`
- evaluator log:
  - bytes: `293661`
  - SHA-256:
    `69c1c31de071087fd2cb06f291037903ee71da2524351780b5add081a8b76b6e`
- local runner log:
  - bytes: `302118`
  - SHA-256:
    `6f686fe7dca26eb5aca65c536b9fc1f4ffc7b490f35ca3df31ea4cbcb6dfeabb`.

No Repair19c state NPZ was written.

## Gate result

PASS:

- R19C_G1 exact frozen provenance
- R19C_G2 orthonormal constrained basis
- R19C_G3 exact parent reproduction
- R19C_G4 certified first-step reproduction
- R19C_G7 two-grid correction amplitude
- R19C_G9 field-freeze invariant
- R19C_G10 output integrity
- R19C_G11 claim boundary.

FAIL:

- R19C_G5 exact canonical nonlinear closure
- R19C_G6 second-order correction scaling
- R19C_G8 all-branch lambda=1 exact closure.

This is a science FAIL, not an implementation failure.

## Canonical result

All 24 canonical nonlinear solves fail the historical exact closure criterion.

Summary:

- canonical PASS: `0/24`
- lambda=1 PASS: `0/6`
- maximum accepted iterations: `9`
- maximum exact epsilon_H:
  `1.0992239196813544e-06`
- maximum exact epsilon_M:
  `0.030366968591611428`.

Every failed solve terminates through

`backtracking_failed`.

No case reaches the exact nonlinear stopping criterion.

## Gauge and state invariants

Across all 24 canonical solves:

- exact-Q reconstruction error remains zero;
- maximum observed |Y4| is approximately `5.3e-23`;
- maximum observed |Qmean| is approximately `4.4e-20`;
- every nonprojection field passes the bitwise freeze invariant.

Thus the failure is not caused by loss of the certified gauge conditions or accidental modification of frozen fields.

## Certified first-step reproduction

All six lambda=1 first GELSY steps reproduce the frozen Repair19b1 direct linear payload exactly under the preregistered tolerance.

Therefore the nonlinear run begins from the previously certified linear correction direction.

## Linear prediction versus exact nonlinear first step

The dominant new finding is a very large mismatch between the direct linear prediction and the exact nonlinear residual after the first accepted full step.

Representative lambda=1 cases:

### Scale 5, Nr=256

- predicted linear residual L2:
  `2.449845864172695e-11`
- exact nonlinear residual L2 after alpha=1:
  `1.459496330366806e-02`
- exact/predicted ratio:
  approximately `5.96e8`.

### Scale 5, Nr=512

- predicted:
  `3.871035489230522e-11`
- exact:
  `2.490506292487368e-02`
- ratio:
  approximately `6.43e8`.

### Scale 10, Nr=256

- predicted:
  `7.443387552956206e-10`
- exact:
  `7.158662449196569e-01`
- ratio:
  approximately `9.62e8`.

### Scale 10, Nr=512

- predicted:
  `2.9865897161852466e-09`
- exact:
  `3.154862860151988e-01`
- ratio:
  approximately `1.06e8`.

### Scale 20, Nr=256

- predicted:
  `7.040071257739262e-10`
- exact:
  `3.5435911021415765e-02`
- ratio:
  approximately `5.03e7`.

### Scale 20, Nr=512

- predicted:
  `2.1163971075393202e-10`
- exact:
  `2.7670015614582485e-02`
- ratio:
  approximately `1.31e8`.

The direct linear system can therefore predict near-annihilation while the exact nonlinear state remains many orders of magnitude away from that prediction.

This is the central Repair19c diagnostic fact.

## Constraint split

The final lambda=1 Hamiltonian residual is generally extremely small, while momentum remains above the historical threshold.

Lambda=1 exact values:

- scale 5, Nr=256:
  - H `1.4238605885848604e-12`
  - M `1.0025853680751008e-4`
- scale 5, Nr=512:
  - H `4.1640970462480227e-13`
  - M `3.097673966566966e-4`
- scale 10, Nr=256:
  - H `3.9190614713140965e-11`
  - M `2.093034986286432e-4`
- scale 10, Nr=512:
  - H `4.7738367109032445e-12`
  - M `2.459062462075578e-4`
- scale 20, Nr=256:
  - H `7.744070775025436e-11`
  - M `5.730951320826147e-6`
- scale 20, Nr=512:
  - H `9.492614483322324e-12`
  - M `1.7052044432331304e-5`.

Thus the residual after the nonlinear projection is momentum dominated.

## Correction scaling

Five of the six scale/grid paths pass the preregistered small-lambda O(lambda^2) slope gate.

The only failure is:

- scale 10, Nr=512
- final gated slope:
  `2.2059300525270347`

against the frozen interval `[1.8,2.2]`.

The excess above the upper bound is approximately `0.00593`.

Because exact canonical closure already fails, this marginal scaling failure is secondary and is preserved without threshold adjustment.

## Two-grid control

The lambda=1 correction amplitudes agree extremely well between Nr=256 and Nr=512:

- scale 5 ratio:
  `1.0034811583557677`
- scale 10:
  `1.0028899322177636`
- scale 20:
  `1.0034806074679696`.

All are far below the frozen limit of 2.

Thus there is no evidence here for a radial-grid-amplitude instability.

## Branch retests

The all-branch gate is false because no lambda=1 canonical solved state passed exact closure.

All 54 branch rows were therefore skipped by the preregistered rule.

The reported `0/54` is not 54 independently evaluated branch failures and must not be interpreted that way.

## Interpretation

Repair19c establishes:

1. the certified orthonormal gauge and first direct linear step are reproduced correctly;
2. the physical correction remains small and approximately second order;
3. grid-amplitude control is excellent;
4. the Hamiltonian constraint can become extremely small;
5. the momentum constraint remains above the historical threshold;
6. direct local Jacobian predictions can differ from the exact nonlinear residual by approximately 1e7-1e9 at the first full step;
7. subsequent direct Gauss-Newton steps eventually become extremely small while the exact residual remains finite, and backtracking then fails.

Therefore Repair19c does not justify adding a new physical field or changing the frozen physics.

The next diagnostic must test the fidelity of the frozen finite-difference Jacobian as a directional linearization of the exact residual over the physical step scale.

## Licensed continuation

A separately preregistered diagnostic may:

- keep the exact same parent states, residual, physical variables, orthonormal basis, source dictionary, eta=0 and grids;
- reproduce the frozen Repair19c first GELSY direction;
- evaluate exact residuals along deterministic amplitudes of that direction;
- compare exact secants with the frozen Jacobian prediction;
- measure first-order directional consistency and nonlinear-remainder scaling;
- inspect Hamiltonian and momentum blocks separately;
- record numerical-rank and finite-difference-scale sensitivity descriptively.

It may not:

- run a new nonlinear solver;
- change the physical projection pair;
- add a field;
- change Y4/Qmean;
- alter any source, coefficient, sign, eta, branch, threshold, radial point set, or historical artifact;
- write a corrected-state NPZ;
- run time evolution.
