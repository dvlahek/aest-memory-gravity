# GE19 H4F3b synthetic production-wiring audit — valid Actions freeze

## Classification and exact epistemic boundary

`GE19_H4F3B_SYNTHETIC_PRODUCTION_WIRING_PASS`.

The actual separately frozen H4F3b **source wrapper** was exercised
through the unchanged GE19 reduced Fourier reconstruction,
actual H4F2g six-piece assembler, Stage E u+phi Y source,
frozen M1(B20) source and physical H*FD8/H*FD4 H4F2h
source-Ward adapter. Three externally expensive frozen
source evaluators were intentionally replaced by
explicit manufactured shape-correct fixtures:

- `q_cross_direct` (GE06+GE07 nonlinear mixed Q, twice
  per call to include the swap-symmetry control);
- `lambda_cross_direct`;
- `reconstruct_m2_source` (GE05 M2/R1 bath source).

These fake evaluator values are **not** physical corrected-parent
source data. The unmodified H4F3b source module was not edited.
The test did not access the actual H3F/H3G parent files,
the original certified Repair32B Z11 NPZ or original
Repair26 R1 bath trace.

A PASS verifies only production code integration, not
the six action-derived source values on certified data,
operator/parent Euler Ward identity, H4/Z21 solve or lensing.

## Immutable input/code versions

Preregistration:
`ge19/h4f3b_predata_synthetic_production_wiring.json`,
blob `7121c2fa7ca2502dbf66923a2522fb2340003ee3`.

Valid deterministic selftest:
`ge19/h4f3b_synthetic_production_wiring_selftest.py`,
blob `2daf44fa2377495eed69a7272727478426a585ad`.

Unmodified actual source wrapper:
`ge19/h4f3b_actual_corrected_six_piece_source.py`,
blob `0423cbc64f6cda3b2a9aeb67c734935ef3ae7f9c`.

Dedicated workflow:
`.github/workflows/ge19-h4f3b-synthetic-production-wiring.yml`,
blob `1940fdbb6c66f146c6da0690f6ecc0f42fc2c696`.

## Successful GitHub Actions run

- run: `36060197350`;
- job: `107837030623`;
- execution commit:
  `6799208157fcdb753fdf05620155bbdeac0aaa22`;
- conclusion: `success`;
- marker: `GE19_H4F3B_SYNTHETIC_PRODUCTION_WIRING_PASS`;
- artifact ID: `10833717959`;
- JSON:
  `results/ge19_h4f3b_synthetic_production_wiring.json`;
- JSON bytes: `4703`;
- JSON SHA-256:
  `4c015f242cbbd97628c4775b4e1978b80c9d95a1e650830485aceb3c608ffd49`.

All source-code Git blob checks and all three beta
`{1.0,0.5,0.1}` fixture gates passed.
The exact six-piece source and physical-Ward
summation defects are 0.0 for each beta.
The actual Stage E Y source has nonzero
u and phi rows and exactly zero Y
metric/constraint rows.
Frozen M1(B20) is reproduced exactly.
The source-only Ward itself is intentionally
nonzero; **its smallness is not a gate**.
The negative tests detect a wrong q10 weighted
projection and an inconsistent physical time grid.
No Z21 source or solver is certified.

## Preserved first-attempt audit failures

The first two CI executions
`36059920276` and `36060036842`
produced complete source-wiring reports with all
three beta-case gate dictionaries true.
The aggregate test incorrectly required only
two `q_cross_direct` calls, but the unchanged
actual H4F3b implementation correctly makes
**four** calls: direct and swapped directions,
in both nominal and deliberate wrong-q10 controls.
This is a synthetic test call-count expectation
error, not a source-science failure.

The fixture count was corrected without changing
any historical H3/H4 physics module.
Run `36060168735` then stopped at the workflow's
stale selftest Git blob preexecution lock and
never ran the corrected fixture. Updating only
that workflow blob pin produced the valid
successful run `36060197350`.

None of these CI failures is a physical
H4/Z21 science result or a change to the
original Repair37 science FAIL.

## Actual-data dependency remains open

The true H4F3b local source runner remains

`ge19/run_local_h4f3b_actual_corrected_six_piece_source.sh`.

It fails closed without the original exact
Repair32B Z11 NPZ, SHA-256

`5d4a0a72c08d09d096a8de0b428b3c8443fc33e8ad442ed6d997d6bf2bc6e327`.

The historical Repair32B Actions runs inspected
for possible recovery
(`35758781356`, `35758540985`)
have **no downloadable numerical artifacts**:
they were static code/prelock audits.
The named Z11 binary was not found among
the currently available conversation/Library files
or mounted working files. Actual H3F/H3G
binaries are available in the conversation,
but this does not put them or missing Z11
inside the GitHub Actions runner.

NEXT: run the **actual** H4F3b source evaluation
only with the exact certified missing Z11,
original H3F/H3G/R13, original frozen R1 trace
and common physical background. Freeze its
real source PASS/FAIL separately. Even a
real source PASS still requires independent
operator-plus-all-parent Euler Ward and boundary
compatibility before one separately preregistered
H4/Z21 solve.

The original active shift threshold `1e-6`
is unchanged. Full H4 Noether NOT CERTIFIED.
Z21 NOT CERTIFIED. Lensing blocked.
