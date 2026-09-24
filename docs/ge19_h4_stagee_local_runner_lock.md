# GE19 H4 Stage E — local source-only runner lock

## Status

The Stage E lightweight deterministic Y source-row audit
has a frozen local runner. It does not execute an H3/H4
state solve, change any old source file or use observations.

Runner:
`ge19/run_local_h4_stagee_y_source_rows.sh`.

Runner commit:
`6f8ac6a3e73c2a69db7457e6ef193b921dac26c5`.

Runner blob:
`3d455fb2dd5b9bf7d4f8dc51e06bfd03962b99a1`.

Dedicated static audit:
- workflow:
  `.github/workflows/ge19-h4-stagee-local-runner-static.yml`;
- commit: `e0be317653a9c71b81d195d92e9047666035e181`;
- blob: `898f7a78d4aa94663ad8a878c19f61cd87f3c892`;
- run: `35995568675`;
- job: `107619545890`;
- conclusion: `success`;
- marker: `GE19_H4_STAGEE_LOCAL_RUNNER_STATIC_PASS`.

Valid Stage E CI parent:
`docs/ge19_h4_stagee_versioned_y_rows_valid_freeze.md`,
blob `ddec5651400a843994779114d61203e4187cef04`.

CI result:
`GE19_H4_STAGEE_Y_SOURCE_ROW_DICTIONARY_IMPLEMENTATION_PASS`;
run `35995241998`;
JSON SHA-256:
`c3ff4cc18dc8c7a69ba661a68ea3de987818f1b9c1db3275b08f2976c385896e`.

## Local command

```bash
cd ~/aest-memory-gravity
git pull --ff-only
source .venv/bin/activate
mkdir -p results

set -o pipefail
bash ge19/run_local_h4_stagee_y_source_rows.sh \
  2>&1 | tee results/ge19_H4_STAGEE_LOCAL_runner.log
echo "EXIT=${PIPESTATUS[0]}"
```

Expected local markers:

`GE19_H4_STAGEE_LOCAL_LOCK_PASS`,
`GE19_H4_STAGEE_LOCAL_PREEXECUTION_PASS`,
`GE19_H4_STAGEE_LOCAL_SOURCE_ROWS_PASS`.

The runner creates only:

- `results/ge19_h4_stagee_y_source_rows_LOCAL.json`;
- `results/ge19_h4_stagee_y_source_rows_LOCAL_FULL.log`;
- `results/ge19_H4_STAGEE_LOCAL_runner.log`.

All original parent and source blobs must match the preregistered
versions with no uncommitted changes. The exact original beta
cohorts are tested without outcome-based selection.

A valid local PASS certifies **only** the standalone Y-only
source-row implementation, not a corrected parent H3,
new q20, H4/Z21 or lensing.
