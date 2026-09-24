# GE19 H4F2e — isolated local shift-action runner lock

## Purpose and result boundary

The independently audited H4F2e shift-action
subset has classification
`GE19_H4F2E_SHIFT_ACTION_SUBIDENTITY_PASS`,
CI run `36027647449`, JSON SHA-256
`32b0fbc9cddd55d51b6380e6ad36c1da39229c8820974a00eb2837ca7bcf6dd2`.

This locked local runner independently replays
**only** that exact source-action analytic/
deterministic audit. It does not reconstruct
H3F/H3G parents, execute the full six-piece
H4 Ward audit, reclose H4/Z21 or license lensing.

## Frozen runner and successful static audit

Runner:
`ge19/run_local_h4f2e_dust_m2_lambda_shift_action.sh`,
commit `6a8a93e212d9c5fea3c7105d2f97f5ae42cc6bee`,
blob `951a51bcaacb082b581323d8190220a1b7fa7599`.

Static workflow:
`.github/workflows/ge19-h4f2e-local-runner-static.yml`,
commit `5ae4e1ad8de437e75dc9bff2008e743c6da9b8c8`,
blob `e397c17d3651483bc69e69a44b39c3522e1ec504`.

GitHub run `36028343263`, job
`107730493210`, conclusion `success`,
marker
`GE19_H4F2E_LOCAL_RUNNER_STATIC_PASS`.

The runner requires the exact preregistered
source and all frozen generator blobs,
rejects locally modified pinned sources,
and requires the activated repository
virtual environment.

**Important isolation:** both frozen GE05
and GE07 generators execute numerical
diagnostics and write their own standard
relative-path `results/` outputs when
imported. To avoid overwriting historical
project results, this runner creates a
temporary directory, changes its working
directory to that directory and makes
the repository importable through
`PYTHONPATH`. Those generator side effects
therefore remain in the temporary folder
and are cleaned up after execution.
Only the explicitly requested new
`_LOCAL` H4F2e outputs are written
to the real project `results/` directory.

## Exact local command

```bash
cd ~/aest-memory-gravity
git pull --ff-only
source .venv/bin/activate
mkdir -p results
set -o pipefail
bash ge19/run_local_h4f2e_dust_m2_lambda_shift_action.sh \
  2>&1 | tee results/ge19_H4F2E_LOCAL_runner.log
echo "EXIT=${PIPESTATUS[0]}"
```

Expected markers:

`GE19_H4F2E_LOCAL_LOCK_PASS`;

`GE19_H4F2E_LOCAL_PREEXECUTION_PASS`;

`GE19_H4F2E_GENERATOR_OUTPUT_ISOLATED_PASS`;

`GE19_H4F2E_LOCAL_ACTION_SUBIDENTITY_PASS`.

Outputs:

`results/ge19_h4f2e_dust_m2_lambda_shift_action_LOCAL.json`;

`results/ge19_h4f2e_dust_m2_lambda_shift_action_LOCAL_FULL.log`;

`results/ge19_H4F2E_LOCAL_runner.log`.

The local FULL log includes generator output
before the final H4F2e JSON, so do not
mistake its SHA for the JSON SHA. The
local result may differ bytewise across
NumPy/SymPy versions, but every exact gate
must pass. Never relax a preregistered
source or science threshold to obtain PASS.

A source/implementation failure must be
preserved as a separate result. It is not
an H4 physics science FAIL.

## Next structural obligation

The complete H4F2 mixed six-piece
source/parent identity is still open.
The remaining GE06 independent
shift/anisotropy source and complete
GE07/Lambda/M2 all-row parent residual
terms must be instantiated on one
corrected H3F/H3G/Z11 representation
before a separate H4/Z21 numerical
science preregistration.

Original active-shift target `1e-6`
and historical Repair37 FAIL remain
unchanged.

**Z21 NOT CERTIFIED. Lensing blocked.**
