# GE19 Repair05 equilibrated-linear-solve implementation lock

## Status

**IMPLEMENTATION LOCKED BEFORE REPAIR05 SCIENCE EXECUTION**

Historical Repair04 remains frozen as

`GE19_REPAIR04_WINDOW_RETARDED_REDUCED_H3_Z20_PARTICULAR_FAIL`.

It is not relabeled.

## Repair04 result freeze

Freeze commit:

`8b12628c5c80c1f92e3315c0e2dfbecbc58b419b`

File:

`docs/ge19_repair04_reduced_h1_result_freeze.md`

Frozen blob:

`d7057f104dbc95ac5cf5215ee0e7fe28b6ad462f`

The frozen Repair04 local JSON / inner FULL-log SHA256 is

`dd03f40b392f8b5b31332de8526bfcf590a44aea8f3f356254e5d2ee86d845b7`.

The frozen outer runner-log SHA256 is

`1309b263507aa5fd4a9df2d887e664b4a6cb3729eaa785461af8ba64a5ce2c1f`.

## Repair05 preregistration

Commit:

`d488d1d406e523166777dfa46cf62bf98321fb9f`

File:

`ge19/repair05_predata_equilibrated_linear_solve.json`

Frozen blob:

`4ce7086dcf61e4ec704ec4a5f9fbbffa60fe9893`

Permitted change is numerical only: deterministic positive diagonal row/column equilibration of the same frozen `A x = B`, back-transform to the original variables, and at most four residual-based iterative-refinement corrections.

No physics or science threshold is changed.

## Repair05 implementation

Final implementation commit before the prelock workflow:

`01def6f57c37f5bd0e5e3d68c27ac5375aed4b83`

File:

`ge19/repair05_window_retarded_reduced_h3_z20_particular.py`

Frozen blob:

`61a34c2253f5d7c6f66efb7ee50444d2a24ce03d`

The implementation keeps the following Repair04 functions source-identical:

- `reference_reduced_mode_state`;
- `source_real_reduced`;
- `linear_operator_batch`;
- `build_matrix`;
- `apply_bc_rhs`;
- `reduced_h1_time_control`.

The frozen physical constants, grids, modes, beta/C values, gates and GE15/GE18 bindings are unchanged.

## Static audit

Existing GE19 static prelock audit on the final Repair05 implementation:

- run: `35534446846`;
- audited HEAD: `01def6f57c37f5bd0e5e3d68c27ac5375aed4b83`;
- conclusion: `success`.

## Repair05 executable prelock audit

Workflow final commit:

`0e4179f11cbe6cab15c1ea0611440ab4223fa590`

Workflow:

`.github/workflows/ge19-repair05-prelock-audit.yml`

Frozen blob:

`4bbc1b8504e735b985f00ee5122dcdbeb3d9aee3`

GitHub Actions run:

`35534506197`

Job:

`106140985549`

Audited HEAD:

`0e4179f11cbe6cab15c1ea0611440ab4223fa590`

Conclusion:

`success`

Terminal marker:

`GE19_REPAIR05_PRELOCK_AUDIT_PASS`

### Frozen executable audit numbers

Deterministic ill-scaled two-RHS test:

- row-max dynamic range: `1.0000000000000001e8`;
- scaled matrix max absolute entry: `1.0`;
- initial original-system residual max: `2.739403977959393e-16`;
- final original-system residual max: `4.5798926346267995e-17`;
- accepted refinement steps: `1`;
- known-solution relative L2 max: `1.0936484695602904e-16`;
- all solution values finite.

Single-RHS original-system residual:

`4.5798926346267995e-17`.

Stable GE06 benign equivalence under the audit environment:

- c1: `1.0224728415507297e-15`;
- c2: `1.3286965479102186e-15`;
- all stable outputs finite.

Physical-parameter probes:

- c1 all partials finite, finite max abs `134217727.98421885`;
- c2 all partials finite, finite max abs `4.056481920730334e31`.

## Frozen ancestry

Verified chain:

- Repair04 result freeze -> Repair05 prereg: one commit ahead, common merge base = Repair04 freeze.
- Repair05 prereg -> final Repair05 implementation: two commits ahead, common merge base = prereg.
- final Repair05 implementation -> final prelock workflow HEAD: two commits ahead, common merge base = final implementation.

No science result existed before this lock.

## Exact numerical transformation

For the unchanged matrix equation

`A x = B`,

Repair05 computes positive diagonal scalings

`Dr_ii = 1/max_j |A_ij|`

and, after row scaling,

`Dc_jj = 1/max_i |(Dr A)_ij|`.

It solves

`(Dr A Dc) y = Dr B`

and maps back with

`x = Dc y`.

Any iterative-refinement correction uses the same fixed scaled factorization but accepts a correction only if the residual measured on the original, unscaled system decreases.

This is algebraically the same linear system. It does not modify `A`, `B`, the field equations, boundary rows or boundary values.

## Unchanged Stage-A gates

- linear-system relative L2 residual <= `1e-8`;
- shift constraint relative L2 <= `1e-6`;
- anisotropy constraint relative L2 <= `1e-6`;
- primary64/control32 state relative L2 <= `5e-3`;
- initial dynamic match abs-or-rel <= `1e-10`;
- all outputs finite.

If Stage A fails, H3/Z20 is not constructed.

## Unchanged Stage-B gates

- Nx1024/Nx2048 source low-mode relative L2 <= `5e-4`;
- primary linear-system relative L2 <= `1e-8`;
- shift constraint relative L2 <= `1e-6`;
- anisotropy constraint relative L2 <= `1e-6`;
- primary64/control32 state relative L2 <= `5e-3`;
- all beta0/C cases complete;
- all outputs finite.

## Claim boundary

Even a Repair05 PASS certifies only one frozen low-mode window-retarded reduced-matter H3 directional particular coefficient in the formal epsilon->0 hierarchy.

It does not certify:

- homogeneous/primordial Z20;
- full-species second order;
- finite eta;
- finite physical-amplitude nonlinear evolution;
- collapse/halos;
- lensing;
- observational detection.

Terminal classifications remain:

- `GE19_REPAIR05_WINDOW_RETARDED_REDUCED_H3_Z20_PARTICULAR_PASS`
- `GE19_REPAIR05_WINDOW_RETARDED_REDUCED_H3_Z20_PARTICULAR_FAIL`
- `GE19_REPAIR05_WINDOW_RETARDED_REDUCED_H3_Z20_PARTICULAR_IMPLEMENTATION_FAIL`

## Local execution policy

A local WSL run is diagnostic and must use the locked runner created after this document.

The runner must:

- verify exact frozen blobs and ancestry;
- use the existing frozen GE15/GE18 local results;
- use the already activated/local Python environment;
- perform no `pip install`, network access or CLASS build;
- run the same local equilibration self-audit before science execution;
- preserve every frozen science gate.
