# GE19 D16R1 — Repair26 bracket initialization (implementation-only)

The original D16 run failed before physical propagation. The original Repair24
`full_history_boundary` still held historical v0.77 `a=0.4` bracket constants
when D16 called it. The original Repair37 `build_context` installs the frozen
Repair26 bracket 0.39953919419256334 ... 0.4000388311146992, but the D16
caller invoked `full_history_boundary` *before* `build_context`. D13 and D15a
already used the correct order. The original Repair26 trace SHA passed.

D16R1 is a new, separately named implementation: the original D16 source,
preregistration, static tests, Repair24, Repair26 trace and parent files must
remain unmodified. The revised driver moves `full_history_boundary` after
`build_context` and asserts the source-frozen Repair27 Repair26 bracket.
It changes no theory or numerical physics. The revised runner retains old
source checks and separately locks the D16R1 source/prereg. It uses distinct
`ge19_h4f3d16r1_*` results and never overwrites the failed original D16 FULL.log.

From repository root: `unzip -n ge19_h4f3d16r1_repair26_bracket_package.zip`,
then `bash ge19/run_local_h4f3d16r1_repair26_bracket_H1dot_Hermite_physical_bath.sh
  2>&1 | tee results/ge19_H4F3D16R1_LOCAL_runner.log`
with `set -o pipefail`; inspect `${PIPESTATUS[0]}`.

Synthetic STATIC PASS is not an actual physical run. Even a physical D16R1 PASS
only licenses an empirical H1dot-Hermite surrogate diagnostic. True continuous
H1/X10 enclosure, genuine first-order GE05 on-shell, full H4 Ward, Z21 and
lensing remain OPEN. No observational tuning.
