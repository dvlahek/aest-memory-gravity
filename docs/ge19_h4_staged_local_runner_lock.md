# GE19 H4 Stage D local analytic runner — implementation lock

## Status

The lightweight local reproduction path for the valid Stage D
common GR-anchored Y-action normalization and Y-only source-row
derivation is frozen before local execution.

Runner:
`ge19/run_local_h4_staged_common_y_action_rows.sh`.

Runner commit:
`8fa5a59f705792cfc2c4c9edd4fd5e4043c4038e`.

Runner blob:
`cdf98460d84ee45f0f55b546c93230ee8066d46b`.

Dedicated static audit:
- workflow: `.github/workflows/ge19-h4-staged-local-runner-static.yml`;
- commit: `182df0ad4dc9d28d6e7566277691ad3a96c31187`;
- run: `35984559448`;
- job: `107584092558`;
- conclusion: `success`.

Frozen Stage D parent:
- valid freeze:
  `docs/ge19_h4_staged_common_y_action_rows_valid_freeze.md`;
- blob:
  `7d140a608d91a39106c34565cd50e4aa729ec30b`;
- preregistration:
  `ge19/h4_structural_stage_d_predata_global_y_normalization.json`;
- preregistration blob:
  `764d064c76d44bc597ab6c4f96044ba2a90433a5`;
- implementation:
  `ge19/h4_structural_stage_d_common_action_y_rows.py`;
- implementation blob:
  `162357ce845a93982b46aef7d839a7171964b47e`;
- successful original analytic CI run:
  `35984187949`;
- CI JSON SHA-256:
  `2d900249d1e030a9b11b2b3d3e4b65ada8cbfb39a119b40ac0aba3ce10380d11`.

## Local execution

```bash
cd ~/aest-memory-gravity
git pull --ff-only
source .venv/bin/activate
mkdir -p results

set -o pipefail
bash ge19/run_local_h4_staged_common_y_action_rows.sh \
  2>&1 | tee results/ge19_H4_STAGED_LOCAL_runner.log
echo "EXIT=${PIPESTATUS[0]}"
```

Expected markers:

`GE19_H4_STAGED_LOCAL_LOCK_PASS`,
`GE19_H4_STAGED_LOCAL_PREEXECUTION_PASS`,
`GE19_H4_STAGED_LOCAL_ANALYTIC_PASS`.

Outputs use separate local names:

- `results/ge19_h4_staged_common_y_action_rows_LOCAL.json`;
- `results/ge19_h4_staged_common_y_action_rows_LOCAL_FULL.log`;
- `results/ge19_H4_STAGED_LOCAL_runner.log`.

The runner rejects wrong committed source blobs, locally modified
pinned source files, missing virtual environment, nonfinite
or failed symbolic gates, incorrect action ratio, or any
unexpected science claim.

No H3/H4/Z21 numerical solver is launched by this runner.
A local PASS verifies only the GR-anchored common Y-action
normalization and the Y-only scalar/aether row formulas.

The complete all-sector H4 Noether certificate and
appropriately versioned H3/q20 parent reclosures remain open.
Historical results are not relabelled; Z21 and lensing
remain blocked.
