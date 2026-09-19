# NL1C7B4 Repair19c1 — local result freeze

## Status

Frozen local WSL diagnostic result from the first locked Repair19c1 execution.

Terminal classification:

`NL1C7B4_REPAIR19C1_FIRST_STEP_DIRECTIONAL_JACOBIAN_FIDELITY_CHARACTERIZED`

with

`SCIENCE_RC=0`.

Execution HEAD:

`db76d7106017adf9a3e4de2055956d717c982618`.

This is a local WSL result, not an official GitHub Actions run.

## Frozen output hashes

- result JSON:
  - bytes: `151045`
  - SHA-256:
    `b4898fed6c6bbe7d4c91f8144ed35d03e6f318b298a2fc13c0daaef038c0e3cd`
- evaluator log:
  - bytes: `151491`
  - SHA-256:
    `0db205484be993b7c9732afa2cea96df281279a6956bc4b1ba5b8c831ff3f89b`
- local runner log:
  - bytes: `168832`
  - SHA-256:
    `63d6f55bfd067a770568669dcf5ff78d53b1c7428dfd6adce194282cade9ca6e`.

## Gate result

All eight preregistered gates PASS:

- G1 exact frozen provenance
- G2 exact orthonormal basis reproduction
- G3 exact parent reproduction
- G4 exact first-step reproduction
- G5 complete finite directional sweep
- G6 exact gauge and Q preservation
- G7 field-freeze invariant
- G8 claim boundary.

Repair19c remains frozen as nonlinear science FAIL and is not relabelled.

## Global summary

Across all six lambda=1 canonical cases:

- minimum exact/predicted alpha=1 residual ratio:
  `50334591.40411471`
- maximum exact/predicted alpha=1 residual ratio:
  `961747913.6033223`
- minimum directional-derivative mismatch observed:
  `0.00023723689066523836`
- largest per-case minimum directional mismatch:
  `0.04768010277751975`.

The exact first-step residual is therefore between about 5e7 and 9.6e8 times larger than the frozen linear prediction.

## Per-case directional characterization

### Scale 5, Nr=256

- exact/predicted alpha=1:
  `595750268.0927533`
- minimum directional mismatch:
  `2.3723689066523836e-4` at alpha `1/16`
- minimum exact residual ratio:
  `9.331671318094959e-4` at alpha `1`
- median remainder slope over largest three intervals:
  `1.0393254741599653`
- median directional-mismatch slope over largest three:
  `0.03932547415996939`.

### Scale 5, Nr=512

- exact/predicted alpha=1:
  `643369532.3683087`
- minimum directional mismatch:
  `9.313969790903207e-4` at alpha `1/2`
- minimum exact residual ratio:
  `1.1252311233495844e-3` at alpha `1`
- median remainder slope over largest three:
  `0.6435065574989479`
- median directional-mismatch slope over largest three:
  `-0.35649344250105186`.

### Scale 10, Nr=256

- exact/predicted alpha=1:
  `961747913.6033223`
- minimum directional mismatch:
  `0.04768010277751975` at alpha `1/32`
- minimum exact residual ratio:
  `0.0481225091564709` at alpha `1`
- median remainder slope over largest three:
  `0.9992309232742833`
- median directional-mismatch slope over largest three:
  `-0.0007690767257163153`.

### Scale 10, Nr=512

- exact/predicted alpha=1:
  `105634290.61095394`
- minimum directional mismatch:
  `0.014869933428773982` at alpha `1/16`
- minimum exact residual ratio:
  `0.014987074576209498` at alpha `1`
- median remainder slope over largest three:
  `0.9931683947946053`
- median directional-mismatch slope over largest three:
  `-0.0068316052053947465`.

### Scale 20, Nr=256

- exact/predicted alpha=1:
  `50334591.40411471`
- minimum directional mismatch:
  `0.002519863924596263` at alpha `1/1024`
- minimum exact residual ratio:
  `0.0027244485738727505` at alpha `1`
- median remainder slope over largest three:
  `1.001923750047911`
- median directional-mismatch slope over largest three:
  `0.0019237500479096707`.

### Scale 20, Nr=512

- exact/predicted alpha=1:
  `130741133.2023303`
- minimum directional mismatch:
  `0.0014956120720392427` at alpha `1/8`
- minimum exact residual ratio:
  `0.0015033946146374639` at alpha `1`
- median remainder slope over largest three:
  `1.0052406385742456`
- median directional-mismatch slope over largest three:
  `0.005240638574248234`.

## Main numerical interpretation

For a faithful Jacobian, along a fixed direction one expects

`F(alpha dx)=F0 + alpha J dx + O(alpha^2)`.

The observed Repair19c1 remainder is not predominantly quadratic.

Across the most informative large-amplitude part of the sweep, four cases show remainder slopes essentially equal to 1, and the remaining two are also far from a stable quadratic value of 2.

At the same time the directional-derivative mismatch is approximately amplitude independent over that regime.

Therefore the leading discrepancy has the form

`alpha * deltaD`

rather than an ordinary `O(alpha^2)` nonlinear remainder.

This identifies loss of local derivative fidelity in the frozen finite-difference Jacobian action along the Repair19c Newton direction.

At the smallest amplitudes the mismatch frequently worsens instead of converging, consistent with roundoff/cancellation entering the residual differences.

## Constraint-block localization

The alpha=1 discrepancy is momentum dominated.

For scale 5, Nr=256:

- linear predicted H block L2:
  `1.730125720882397e-11`
- exact H block L2:
  `2.2966597986918426e-11`
- linear predicted M block L2:
  `1.734476793775352e-11`
- exact M block L2:
  `0.01459496330366806`.

Thus the Hamiltonian directional prediction is locally accurate while the momentum directional prediction is not.

The same qualitative split occurs across the other canonical cases.

## Scientific conclusion

Repair19c1 does not show that the physical `(L,R_t)` projection ansatz is infeasible.

It shows that the specific frozen default finite-difference Jacobian used by Repair19c is not a sufficiently faithful local derivative for the cancellation-sensitive momentum residual.

The earlier sparse-versus-dense Jacobian agreement does not contradict this result because both constructions used the same default finite-difference scale and can therefore share the same derivative bias.

The next diagnostic should vary finite-difference scheme and absolute step size while keeping the physical problem and frozen first-step direction fixed.

## Licensed continuation

A separately preregistered Repair19c2 may:

- keep the same six lambda=1 parents and exact orthonormal gauge;
- reproduce the frozen Repair19c first direction;
- construct grouped finite-difference Jacobians with a preregistered set of absolute step sizes and 2-point/3-point schemes;
- compare their action on the frozen direction with symmetric exact directional secants;
- report rank and direct one-step residuals descriptively;
- preregister a deterministic scheme/step selection metric for a later solver repair.

It may not:

- run a nonlinear iteration;
- change the physical projection pair;
- add a field;
- alter Y4/Qmean, sources, coefficients, signs, eta, branch, threshold, radial points, or historical artifacts;
- write a corrected-state NPZ;
- run time evolution.
