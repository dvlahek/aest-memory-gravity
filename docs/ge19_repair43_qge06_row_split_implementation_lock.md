# GE19 Repair43 GE06 main-versus-constraint stage-source split — implementation lock

## Status and claim boundary

Repair43 is frozen before its first local diagnostic execution.
It is diagnostic-only: no H4 physics/source builder, projected boundary,
canonical operator, time grid, Radau tableau, active mask, science threshold,
finite physical eta or observational input changes.

Repair37 remains immutable science FAIL; Repair38--Repair42 remain immutable
diagnostic results. Repair43 cannot certify Z21 or license lensing.

## Frozen valid Repair42 parent

Freeze file:
`docs/ge19_repair42_valid_direct_target_above_threshold_constraint_localization_freeze.md`.

Freeze commit:
`9a7fd6262832a44ca7d0d2cb73c322b856dcf514`.

Freeze blob:
`e3b89cc656ca5dade9a555aa21ae0ba65817af46`.

Frozen classification:
`GE19_REPAIR42_DIRECT_TARGET_H4_PROPAGATION_DIAGNOSTIC_COMPLETE`.

Frozen route:
`DIRECT_TARGET_CORRECTION_ABOVE_SCIENCE_TARGET`.

Frozen artifacts:
- JSON/FULL SHA-256:
  `4a211581a77c1ad00e14cc398ca7a19b12642f3f3e35b416314d6721f5f81e25`;
- NPZ SHA-256:
  `a60515f3d92bbd388fd2fadae6cf2dd07f3ee68e8690b07632bbe5091e9013c5`;
- outer runner SHA-256:
  `855067c5f733374d98a97e5013c0f23ea1cfbcb1f62494a596beab9768cbcf9c`.

## Frozen Repair43 preregistration

File:
`ge19/repair43_predata_qge06_main_constraint_stage_split.json`.

Commit:
`9aa0bfcb9e2e21979ad665037e1bd7b18213934a`.

Blob:
`b2161c074012c096fba8790fa377c69fd548a234`.

## Frozen implementation

File:
`ge19/repair43_qge06_main_constraint_stage_split.py`.

Commit:
`6257c3ba57e26035aaa2602440bedf0c368854f6`.

Blob:
`50769723c1ff5abce1548a15d41353fb295e932c`.

The script imports the frozen Repair42 loader, source-binding utilities,
stage locator and exact Repair41 direct target arrays. It does not
reconstruct or interpolate any direct target source.

The seven variants are:

- frozen Repair37 PCHIP baseline;
- direct382 Q_GE06 main only;
- direct382 Q_GE06 constraint only;
- direct382 Q_GE06 both;
- direct763 Q_GE06 main only;
- direct763 Q_GE06 constraint only;
- direct763 Q_GE06 both.

For BOTH, both corrected source-row families must reproduce the exact
frozen Repair42 Q_GE06-only states and shift metrics before interpretation.

At each node the script retains the actual per-sample shift metric, absolute
shift residual and its backward-error denominator; it reports the full
active fields and the separately preregistered C_max/beta0=1/m8/it3
early-window hotspot. The frozen active count remains 23850 and the
unchanged target is 1e-6, report-only in Repair43.

## Routing rule

For each direct resolution, calculate the RMS difference on the exact frozen
active mask between the main-only shift field and the full frozen
Repair42 Q_GE06-only shift field; repeat for constraint-only.

- if constraint-only is strictly closer for both resolutions:
  `QGE06_CONSTRAINT_ROW_FIELD_CLOSER_TO_FULL`;
- if main-only is strictly closer for both:
  `QGE06_MAIN_ROW_FIELD_CLOSER_TO_FULL`;
- otherwise:
  `QGE06_MIXED_ROW_SENSITIVITY`.

No new improvement percentage or science gate is introduced. A failed
reproduction/finiteness/parent gate is `IMPLEMENTATION_FAIL`, not a
scientific conclusion.

## Audits

Static implementation audit:
- run: `35962062683`;
- conclusion: `success`.

Dedicated Repair43 prelock:
- workflow file:
  `.github/workflows/ge19-repair43-prelock-audit.yml`;
- workflow commit:
  `c2c25dfc3f139fc616a672c3101fa5d4ed43356c`;
- workflow blob:
  `678a2f4d81d8ebce3c53246b86c6f89df1d7ad9b`;
- run: `35962103386`;
- job: `107512678243`;
- conclusion: `success`.

These audits do not substitute for a valid local diagnostic execution.
