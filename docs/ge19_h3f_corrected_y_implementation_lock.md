# GE19 H3F — corrected-Y Z20 numerical implementation lock

## Status: READY FOR FIRST LOCAL SCIENCE EXECUTION, NOT YET EXECUTED

A separately versioned H3F corrected-Y H3/Z20 science pipeline is
implemented and statically audited. Its first local science result is
**not yet available**, and no certification can be claimed from the
static audit alone.

The exact preregistered test is
`ge19/h3f_predata_action_completed_y_z20_parent_reclosure.json`,
blob `6ae1dd8c27ee1f94d85831cd5ae7b5ec21e3794e`.

Frozen source-adapter result:
`docs/ge19_h3f_complete_y_source_adapter_valid_freeze.md`,
blob `01aa03757568a4f42223407a3bf10805d6f012e0`.

## Immutable new implementation

- source:
  `ge19/h3f_corrected_y_source_adapter.py`,
  blob `395294868191111b9b01201315cd2e6a30e47578`;
- on-shell H1/H3 core:
  `ge19/h3f_corrected_y_parent_core.py`,
  commit `34c9d081c63bafce33cafaec3214bd7969bcc75d`,
  blob `7e1da10ae8d79b6269b306f5483783de0fd3fd30`;
- complete H3F science certification:
  `ge19/h3f_corrected_y_z20_science_reclosure.py`,
  commit `c4cf9749c5e322f3b90fe6a410a498efe88e6c6a`,
  blob `31e36aaf16c8d68f0ad1ffaff97459d67a23a8b0`.

The implementation preserves the frozen Repair07 linear
operator, Repair13/Repair21 on-shell H1 parent,
GE06/GE07/Lambda non-Y source and Repair18
constraint-projected momentum algorithm.

The H3F source is exactly the old complete non-Y
source plus the independently verified Stage E
aether+scalar raw Y RHS. The complete old scalar-only
Y piece is removed. Frozen non-Y decomposition is
checked against the independent analytic pieces before
propagation.

The initial projected p0 is **recomputed** from the
new source using the unchanged Repair18 algorithm.
The old numerical Repair18 p0 is report-only; it is
not an H3F certification gate.

## Mandatory Y-disabled legacy replay

The H3F science script additionally runs the
same newly versioned core with its legacy-Y-control
flag. Its states and projected p0 for the original
Nt128/Nt64, C and beta/m cohorts must reproduce
the frozen historical Repair22 Z20 and p0 arrays
at relative L2 <= 1e-11. A failed legacy replay is
an implementation failure, never a new physical
discovery or relaxation of this gate.

## Unchanged science criteria

- exact original beta={1,0.5,0.1}, C_min/C_star/C_max,
  m=1..40, Nt128/Nt64 and Nx1024/Nx2048;
- original H1/source-spatial, boundary, linear,
  anisotropy and time-grid controls;
- original active shift threshold 1e-6;
- original near-null and matched-order >=2.5
  controls;
- original 2-stage Radau propagation and full
  source-convention/finite-value checks.

A successful first local run must still pass **all**
science gates before the new corrected-Y Z20 can be
certified. The old Repair22 certification stays
valid solely for its original equations.

## Dedicated static results

H3F preexecution:
- workflow: `.github/workflows/ge19-h3f-corrected-y-preexecution.yml`;
- blob `fc32bf577d3d50df21f67324f3bc7590f9dc4aa8`;
- run `35997860156`;
- job `107627003995`;
- conclusion `success`;
- marker `GE19_H3F_CORRECTED_Y_PREEXECUTION_AUDIT_PASS`.

These controls compile and import both newly
versioned H3F executables and verify preserved
science thresholds, new source routing, legacy
replay, source-aware boundary and claim boundaries.
They do **not** execute the H3F numerical state
solver.

## Next execution and scientific boundary

Run the separately frozen local runner; preserve
PASS, SCIENCE_FAIL and IMPLEMENTATION_FAIL as
different immutable outcomes. In a genuine PASS,
recompute new dependent q20 on the existing
cancellation-free full-history parent. Do not reuse
the historical Repair27 q20 with a changed Z20.

Complete H4 source/Noether compatibility is still
required before any new H4/Z21 reclosure.
The old Repair37 science FAIL and Repair38--44
diagnostics remain unchanged. Z21 remains NOT
CERTIFIED and lensing blocked.
