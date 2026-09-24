# GE19 H3G — corrected-Y q20 first local science runner lock

## Scope and status

This runner is frozen before the first H3G
corrected-Y q20 science execution. The valid
H3F Z20 parent is already certified and frozen;
H3G itself has **not** been numerically executed
or certified.

The new local runner reconstructs only the
window-local particular normalized-bath weighted
q20 response from the certified H3F corrected-Y
Z20, keeping the independently certified
Repair26 R1 full-history first-order bath
and every inherited Repair27 q20 science gate.

The historical Repair27 numerical q20 result
is never reused as the new parent and no
historical result files are overwritten.

## Immutable files

- preregistration:
  `ge19/h3g_predata_corrected_y_q20_reconstruction.json`,
  blob `09fc1bd7fc06459d90fc6f6ba37a84adba757d37`;
- source-corrected q20 core:
  `ge19/h3g_corrected_y_q20_core.py`,
  blob `688920e840a0a13bc85a6f416c2573cf0472eaa3`;
- science wrapper:
  `ge19/h3g_corrected_y_q20_reconstruction.py`,
  blob `de929ae025e3ce58e60e6d229682cf885e7b1007`;
- implementation freeze:
  `docs/ge19_h3g_corrected_y_q20_implementation_lock.md`,
  blob `beae8d8a49eaedab58e3bc1e67a45fe7f7174bf6`;
- final locked runner:
  `ge19/run_local_h3g_corrected_y_q20_reconstruction.sh`,
  commit `b31cadff842dcfcea1cd2495d008dab4db905fd9`,
  blob `bc46078cbbbce46f5955faa7d0e8037e19905a4b`.

An initial draft of the unexecuted runner had
an incorrect implementation-document blob.
This was corrected before the runner static
audit and before any H3G science execution.
The frozen, audited version above has the
correct observed hash. This was a preexecution
lock-data correction, not a changed science
equation or threshold.

## Static CI

H3G science-preexecution CI:
`36013702448`, job `107680654924`,
`GE19_H3G_CORRECTED_Y_Q20_PREEXECUTION_AUDIT_PASS`.

Dedicated runner static CI:
- workflow:
  `.github/workflows/ge19-h3g-local-runner-static.yml`;
- blob `242593e97ee95ea01e6de5699a6801bf990a6f6a`;
- commit `b5fdd9dbde3f44ed25d64d4a0d1e4aa7fcf15ad9`;
- run `36014109845`;
- job `107682063427`;
- conclusion `success`;
- marker `GE19_H3G_LOCAL_RUNNER_STATIC_PASS`.

Neither CI run solves H3G q20.

## Exact frozen science inputs

The runner verifies the exact user-provided
H3F Z20 JSON/NPZ hashes:

`0616188d2bb7a6c09b2b56433a1f8a1860f360b2e54d2cb84e1ae214a407866b`
and
`90840755fa9febb1d8cb84609d9e58f67dec2a0a01cd6bf8e47685b45caa4542`.

The frozen Repair26 R1 trace has SHA-256
`608ee0b4c868a701db6976f756b9a551cd9ddffe1e8e4ab37c5cd2361405a6f8`
and 26643162 bytes. The runner first reuses
the local `frozen_repair26_repair27`
artifact directory and, only if absent,
uses GitHub CLI to download the frozen
run `35721220889` artifact.

Repair13, GE15 dense and Lambda background
inputs remain original and verified.
The unchanged q20 helper AST and science
constants are checked before q20 is started.

## Exact first-run command

```bash
cd ~/aest-memory-gravity
git pull --ff-only
source .venv/bin/activate
mkdir -p results
set -o pipefail
bash ge19/run_local_h3g_corrected_y_q20_reconstruction.sh \
  2>&1 | tee results/ge19_H3G_LOCAL_runner.log
echo "EXIT=${PIPESTATUS[0]}"
```

Expected preexecution markers:

`GE19_H3G_LOCK_PASS`,
`GE19_H3G_LOCAL_PREEXECUTION_AUDIT_PASS`,
`GE19_H3G_H3F_FROZEN_PARENT_PASS`,
`GE19_H3G_REPAIR26_R1_PARENT_PASS`.

New result paths (do NOT overwrite Repair27):

`results/ge19_h3g_corrected_y_q20_reconstruction.json`;

`results/ge19_h3g_corrected_y_q20_reconstruction.npz`;

`results/ge19_h3g_corrected_y_q20_reconstruction_FULL.log`;

`results/ge19_H3G_LOCAL_runner.log`.

The final marker must distinguish
`GE19_H3G_CORRECTED_Y_Q20_SCIENCE_PASS`
from `GE19_H3G_CORRECTED_Y_Q20_SCIENCE_FAIL`
and `GE19_H3G_IMPLEMENTATION_OR_EXECUTION_FAIL`.
A valid science FAIL is frozen and must
not be hidden by parameter fitting or
threshold relaxation.

The old Repair27 weighted projection is
only an optional exact-hash-verified,
report-only numerical comparator. The
normalized bath equations, first-order
R1 parent and all inherited science
thresholds remain fixed.

Even a valid H3G q20 PASS does not
establish complete all-sector H4
Noether compatibility, certify Z21,
license lensing or produce observations.
