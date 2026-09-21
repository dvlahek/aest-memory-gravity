# GE19 Repair09 dual-constraint partition audit lock

## Status

**DIAGNOSTIC IMPLEMENTATION LOCKED BEFORE REPAIR09 LOCAL RESULT**

Repair08 remains diagnostic-only and frozen.

## Parent freeze

Commit:

`f08f3d076e58240766afa21df5df6b927146d67c`

File:

`docs/ge19_repair08_shift_localization_result_freeze.md`

Blob:

`9f2661fee8eb6a0efad805644ecdf370b0fb60ba`

Frozen Repair08 result JSON SHA-256:

`8402a9f3ede227ca4c0c762976c8de247dd07161b41f504c438c6f248361d7d0`.

## Preregistration

Commit:

`d4d280748ff5f6140833ed876c484f7a6497d550`

File:

`ge19/repair09_predata_dual_constraint_partition_audit.json`

Blob:

`9716f45898959bfec49128195035a2c61327b041`

## Implementation

Commit:

`d5312a74be737646739a0220c0414c44551f3577`

File:

`ge19/repair09_dual_constraint_partition_audit.py`

Blob:

`b07572411b14266f40cdc849174bd01e31771f0e`

Repair09 changes only the diagnostic algebraic partition:

Repair07 enforced

`(pS, pu, pphi, pT, dust_density, anisotropy)`

and monitored shift.

Repair09 diagnostically enforces

`(pS, pu, pphi, pT, dust_density, shift)`

and monitors anisotropy.

No continuum equation, sign, background, threshold, initial state, Radau coefficient, C value or mode is changed.

## Prelock workflow

Commit:

`fa4c2576730e0fcb3e82c1407deaf2764f556e19`

Workflow:

`.github/workflows/ge19-repair09-prelock-audit.yml`

Blob:

`b69a21546a87671d119b9f0910635ca253993255`

GitHub Actions run:

`35566207899`

Job:

`106228412963`

Conclusion:

`success`

Terminal marker:

`GE19_REPAIR09_PRELOCK_AUDIT_PASS`

Static GE19 prelock audits also passed for preregistration and implementation commits.

## Important prelock diagnostic

On the synthetic physical-scale probe, the shift-enforced algebraic reconstruction satisfies shift to

`1.2049579996938079e-23`.

However the same probe has

`algebraic_scaled_condition_2 = 1.5521269268870098e16`

and an unconstrained anisotropy probe magnitude

`2.209585978220593e14`.

These numbers do **not** classify the physical Repair09 result; they only prove that the alternative partition is structurally dangerous and must be tested on the frozen real system with the preregistered numerical and 64/32 gates.

## Frozen routing

Repair09 may return only one of the preregistered routes:

- `DAE_PARTITION_DEFECT_LOCALIZED`;
- `REDUCED_BACKGROUND_CONSTRAINT_INCOMPATIBILITY_CONFIRMED`;
- `ALTERNATE_PARTITION_NUMERICAL_FAIL`;
- `DUAL_PARTITION_RESULT_AMBIGUOUS`.

No H3/Z20 construction is permitted.

## Frozen thresholds

- canonical/linear residual <= `1e-8`;
- shift backward error <= `1e-6`;
- anisotropy backward error <= `1e-6`;
- Nt64/Nt32 state convergence <= `5e-3`;
- initial dynamic match <= `1e-10`;
- finite outputs required.

No threshold may be relaxed after the result.

## Claim boundary

Repair09 is a reduced-H1 diagnostic only. It cannot establish H3/Z20, finite eta, finite physical-amplitude nonlinear evolution, collapse, lensing or observational detection.
