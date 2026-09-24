# GE19 H3F — first local corrected-Y Z20 science runner lock

## Status

The first local H3F science execution path is frozen
**before** running the corrected-Y Z20 numerical solver.

Runner:
`ge19/run_local_h3f_corrected_y_z20_science_reclosure.sh`.

Runner commit:
`3a83ba2e4957278c30b19a94ee217bf4d4ea4412`.

Runner blob:
`8633cf4167ee17ef41b277e3a4ba2cbd56cf05a6`.

Dedicated static audit:
- workflow: `.github/workflows/ge19-h3f-local-runner-static.yml`;
- workflow commit: `3c18136de42b7376b568a98e9e70b5d552862d34`;
- workflow blob: `226683f46e6bf839210d4494fc4f71144dd650a2`;
- run: `35998084151`;
- conclusion: `success`.

Parent H3F preexecution audit `35997860156`
and source-adapter CI audit `35997209177`
also passed.

Implementation lock:
`docs/ge19_h3f_corrected_y_implementation_lock.md`.

Preregistration:
`ge19/h3f_predata_action_completed_y_z20_parent_reclosure.json`.

## Required inputs and frozen outputs

The runner checks the tracked source/preregistration
blobs, absence of local modifications and all pinned
GE15/GE18/Repair13/18/19/20/21/22 and local Stage E
source-result hashes. The GE15 Lambda background
file must also exist and be nonempty.

The exact Stage E local prerequisite is

`results/ge19_h4_stagee_y_source_rows_LOCAL.json`

with SHA-256
`c3ff4cc18dc8c7a69ba661a68ea3de987818f1b9c1db3275b08f2976c385896e`.

First local H3F outputs are new filenames, never
overwriting historical science artifacts:

- `results/ge19_h3f_corrected_y_z20_science_reclosure.json`;
- `results/ge19_h3f_corrected_y_z20_science_reclosure.npz`;
- `results/ge19_h3f_corrected_y_z20_science_reclosure_FULL.log`;
- `results/ge19_H3F_LOCAL_runner.log`.

## Command

```bash
cd ~/aest-memory-gravity
git pull --ff-only
source .venv/bin/activate
mkdir -p results
set -o pipefail
bash ge19/run_local_h3f_corrected_y_z20_science_reclosure.sh \
  2>&1 | tee results/ge19_H3F_LOCAL_runner.log
echo "EXIT=${PIPESTATUS[0]}"
```

Expected preexecution markers:

`GE19_H3F_LOCK_PASS`;

`GE19_H3F_LOCAL_PREEXECUTION_AUDIT_PASS`;

`GE19_H3F_FROZEN_PARENTS_PASS`.

One of the final classifications must be preserved:

- `GE19_H3F_NEW_Z20_SCIENCE_PASS` if exit 0 and
  all new source and science gates pass;
- `GE19_H3F_NEW_Z20_SCIENCE_FAIL` if exit 2
  after successful implementation and one or
  more unchanged science gates fail;
- `GE19_H3F_IMPLEMENTATION_OR_EXECUTION_FAIL`
  for missing/rejected inputs, failed legacy
  replay or numerical implementation errors.

No old result can be relabelled by this runner.
Do not interpret a science FAIL as a solver setup
error or an implementation failure as a physical
result.

Even if H3F Z20 passes, new dependent q20 and
all-sector H4 source/Noether compatibility are
still open. Z21 is NOT CERTIFIED and lensing
remains blocked.
