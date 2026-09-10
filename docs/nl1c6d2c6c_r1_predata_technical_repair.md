# NL1C6D2C6C-R1 pre-data technical repair — tau1 memory-order parser compatibility

## Historical run

The first D2C6C implementation run is Actions run `34455671312` at commit `f1a72bea0a3826ae00e501bc815f85df3a3560b6`. It remains an immutable historical technical FAIL.

The run successfully built the corrected tau-H0=1 CLASS, applied the validated 39/47-node memory patch, and produced `D2C6C_LINEAR_ETA0_VARIATIONAL_REFERENCE_READY` with 23,864 unique forcing rows and 918 k groups. It then failed before `NL1C6D2C6C_ETA0_NONLINEAR_MEMORY_TANGENT_START`, before C2/C3, and before any of the 27 members.

The exact failure is the v0.19u parser guard

`v0.19u aest_memory_order must be 39 or 47`

when the inherited D2C6B `prepare_class_data()` supplies its historical memory-off input `aest_memory_order=16`. The memory flag in that base run is `aest_memory_enabled=no`; the integer has no physical effect there, but the tau1 parser validates it unconditionally.

## Frozen repair

R1 changes only this interface value for the inherited memory-off CLASS base/reference input:

`aest_memory_order: 16 -> 39`.

The value 39 is already the preregistered D2C6C primary bath order and is accepted by the validated v0.19u parser. `aest_memory_enabled` remains `no` and `aest_eta` remains exactly zero for the base CLASS trajectory, so this repair does not activate memory and does not alter the D2C6B base physics.

Implementation may be done by a local wrapper/monkeypatch of the inherited `build_params()` used by `prepare_class_data()`. The original D2C6B source is not modified.

## No changes permitted

R1 does not change the D2C6C physics, 27-member family, stable canonical equations, retarded prehistory, tau-H0=1 choice, 39/47 bath definitions, tangent forcing, CLASS reference construction, discretizations, C1-C8 gates, thresholds, diagnostics, or continuation rule.

The original D2C6C preregistration at `fe34cbfb651f4e27fd05479f48c5832dd23863c2` remains controlling. This document licenses only the parser/interface repair above.

A rerun after this repair is the first run eligible to produce a valid D2C6C C1-C8 physics/numerical classification.