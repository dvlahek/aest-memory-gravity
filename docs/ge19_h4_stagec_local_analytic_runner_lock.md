# GE19 H4 Stage C — local analytic reproduction runner lock

## Scope

Run the already verified small **symbolic action-to-GE19
convention audit locally**, without an H3/H4 state solve,
numerical fitting or changes to parent results.

Frozen runner:

`ge19/run_local_h4_stagec_y_raw_ge19_convention_audit.sh`.

Runner commit:
`f27fff9d89eeda595b2e330543dfc88892e5b343`.

Runner blob:
`775499da90e28bb427fe9ce403b8a08cb8695552`.

Dedicated static audit:

- workflow: `.github/workflows/ge19-h4-stagec-local-runner-static.yml`;
- workflow commit: `bf7979a8f98143b1481680279f172d86243ce15b`;
- run: `35982909486`;
- job: `107578798063`;
- conclusion: `success`;
- marker: `GE19_H4_STAGEC_LOCAL_RUNNER_STATIC_PASS`.

Frozen analytic parent:

- result: `docs/ge19_h4_stagec_y_raw_ge19_conventions_valid_freeze.md`;
- result blob: `a22a762148cb30f4d52c494f9df377c4613941d1`;
- symbolic script blob:
  `80e79006613f6067926adf39995fa08bffe51534`;
- predata blob:
  `cc43754e92eef83d025475a9c5f893aa6dd81ce4`;
- successful CI result run:
  `35982602472`;
- CI JSON SHA-256:
  `76f6af0ec5f765c2cf6cf9f33a6cb35d3bd0b8dbfbdec18832955cd8cf5ccb55`.

## How to run

```bash
cd ~/aest-memory-gravity
git pull --ff-only
source .venv/bin/activate
set -o pipefail
bash ge19/run_local_h4_stagec_y_raw_ge19_convention_audit.sh \
  2>&1 | tee results/ge19_H4_STAGEC_LOCAL_runner.log
echo "EXIT=${PIPESTATUS[0]}"
```

Expected terminal markers:

`GE19_H4_STAGEC_LOCAL_LOCK_PASS`,
`GE19_H4_STAGEC_LOCAL_PREEXECUTION_PASS`,
`GE19_H4_STAGEC_LOCAL_ANALYTIC_PASS`.

Local output paths deliberately do not overwrite the frozen CI
artifact or previous GE19 outputs:

- `results/ge19_h4_stagec_y_raw_ge19_convention_audit_LOCAL.json`;
- `results/ge19_h4_stagec_y_raw_ge19_convention_audit_LOCAL_FULL.log`;
- `results/ge19_H4_STAGEC_LOCAL_runner.log`.

The runner checks the committed artifact/source blobs, any
uncommitted source changes, virtual environment, and the full
symbolic and claim-boundary gate suite. A local PASS reproduces
only the *restricted analytic* Stage C result; it cannot certify
the global NL0C-to-GE06 action prefactor, H3/H4 or Z21.

A full local numerical campaign remains blocked until a
separately versioned complete action-derived Y scalar+aether
source dictionary is independently proven and its parent
reclosure is specified.
