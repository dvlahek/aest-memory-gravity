# GE19 Repair32C Repair01 — direct-script import repair lock

## Status

Repair32C Repair01 is an implementation-only repair after the first local
Repair32C invocation failed before producing any valid science JSON.

The Repair32C certification contract, artifacts, thresholds, diagnostics and
routing are unchanged.

## Frozen failure parent

Failure freeze:

- file:
  `docs/ge19_repair32c_initial_execution_import_fail_freeze.md`;
- blob:
  `f57129227ad6a06604a195238c10eaeb8119f3aa`;
- commit:
  `5f7cc60c0ff45badadd2b01d7d549512040f3b5d`.

Failure:

`ModuleNotFoundError: No module named 'ge19'`.

The failed invocation produced no Repair32C science JSON.

## Repair01 implementation

Repaired file:

`ge19/repair32c_artifact_only_reduced_z11_certification.py`.

Blob:

`b2e89fe8e3dc66a430ee47e4d0ba085b82e9ad57`.

Commit:

`743c9eb6505ca3f318257c22601e80b35ed0a028`.

The only code change is direct-script package plumbing:

- add `import sys`;
- after computing repository `ROOT`, add
  `sys.path.insert(0,str(ROOT))`.

No certification calculation or science threshold changes.

## Dedicated Repair01 prelock

Workflow:

`.github/workflows/ge19-repair32c-repair01-prelock-audit.yml`.

Blob:

`59b44fa84d265836ed77d8db31be0a713aae4869`.

Workflow commit:

`87036cc935ba18b109fc02130ac1b59e450094f7`.

Run:

`35762167388`.

Job:

`106862627978`.

Conclusion:

`success`.

Critically, this prelock executes the same direct-script entry mode used by
the local runner:

`python3 ge19/repair32c_artifact_only_reduced_z11_certification.py --help`.

Therefore the repaired import path is tested in the invocation mode that
failed locally.

## Historical original prelock

The original Repair32C prelock remains tied to the original implementation
blob. It fails on the repaired blob by design and is not relabelled.

## Scientific status

No valid Repair32C PASS/FAIL result exists yet.

Reduced Z11 remains NOT CERTIFIED.

H4/Z21 remains BLOCKED until a valid Repair32C result.
