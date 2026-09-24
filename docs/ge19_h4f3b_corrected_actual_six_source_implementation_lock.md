# GE19 H4F3b — corrected-parent actual six-piece source implementation and first-run lock

## Status

**Ready for first local actual-source evaluation; not yet numerically executed.**

The separately preregistered H4F3b adapter binds the exact
certified corrected-Y H3F Z20 and H3G q20, the original
Repair32B/32C certified Z11, the frozen on-shell H1,
the Repair26 R1 full-history first-order bath and the
original Repair13/GE15 physical H(x). It assembles the
genuine six source families into the original GE19
eight-row, FFT/nx convention and computes their
source-only physical Ward projection.

This does **not** evaluate the independent H4 linear-operator
Ward contribution, signed parent Euler residuals or boundary
terms, propagate Z21, certify full Noether or license lensing.
In particular, no smallness of the standalone source-Ward
sum is required or interpreted as a full identity.

## Preregistered inputs and frozen code

- preregistration:
  `ge19/h4f3b_predata_actual_corrected_six_piece_source.json`,
  blob `c3362f5360c2a9951d77060027c82830c031c145`;
- new source-only evaluator:
  `ge19/h4f3b_actual_corrected_six_piece_source.py`,
  blob `0423cbc64f6cda3b2a9aeb67c734935ef3ae7f9c`;
- local runner:
  `ge19/run_local_h4f3b_actual_corrected_six_piece_source.sh`,
  blob `ef0fd6656add30cec667dda0d7bc9a435c3a2562`.

The historical frozen Repair37 implementation is imported only
for its actual independent GE06/GE07/Lambda mixed generators,
R1 M2 source generator, M1 mapping and background builder.
It is never executed through its historical source-assembly
function or H4/Z21 state solver. Its original parent
NPZs and scalar-only DY2 are never accepted as the corrected
H4 source result.

The new code assembles the frozen action-completed Stage E
u+phi Y rows via the H4F2g six-piece source ledger.
M1 uses the exact certified H3G
`B20=X20-weighted_z20`.
The frozen first-order Repair26 R1 bath nodes are
reconstructed independently for GE05 M2, and their
weighted q10 projection is compared with the original
H3G first-order q10 output. The H3G time-control artifact
contains weighted q20 but not a stored B20 control:
the code reconstructs its X20 from H3F Nt64 Z20 and
subtracts the exact stored Nt64 weighted q20.

The same frozen physical time `x=ln(a)`, `H(x)` is
required in all parent arrays. The actual source-Ward
projection is computed through H4F2h with
`H*FD8_x` for GE06/GE07/Lambda and
`H*FD4_x` for GE05 M1/M2. Complete Y has
exactly zero independent shift/isotropic/anisotropy
source rows. No generic `np.gradient` surrogate
is reused as the physical Ward derivative.

## Static Actions evidence, and its strict limit

Dedicated implementation preexecution:
- workflow:
  `.github/workflows/ge19-h4f3b-actual-six-source-preexecution.yml`;
- blob `125d37a65f710507a7fdf35eaf712f2da76b6677`;
- run `36057797491`, job `107829030982`;
- conclusion `success`, marker
  `GE19_H4F3B_ACTUAL_CORRECTED_SIX_SOURCE_PREEXECUTION_PASS`.

Dedicated local-runner static validation:
- workflow:
  `.github/workflows/ge19-h4f3b-local-runner-static.yml`;
- blob `a4d6aa2a3a61ca6a4ad42334ba85f76792e385a3`;
- run `36058048497`, job `107829870394`;
- conclusion `success`, marker
  `GE19_H4F3B_LOCAL_RUNNER_STATIC_PASS`.

Both workflows compile and inspect the exact
versioned source/runner, original parent SHA contracts,
source adapter and no-Z21 boundaries. **Neither had
access to the current user's corrected H3F/H3G binary
parents nor executed the physical source evaluator.**
Do not promote either static PASS to a physical-source
or Noether result.

## Required local frozen inputs

Under `results/` the runner requires exact hash-matched
original Repair13 NPZ, H3F JSON+NPZ, H3G JSON+NPZ,
Repair32B Z11 NPZ, Repair32C Z11 certification JSON,
GE15 R1 dense trace and original GE15 Lambda CLI
background. It uses exact Repair26 R1 full-history
bath trace (SHA-256
`608ee0b4c868a701db6976f756b9a551cd2361405a6f8`,
26643162 bytes), reusing the
`frozen_repair26_repair27` cache or downloading
the already frozen GitHub Actions artifact from
run `35721220889`.

The exact Repair32B Z11 NPZ SHA-256 is
`5d4a0a72c08d09d096a8de0b428b3c8443fc33e8ad442ed6d997d6bf2bc6e327`.
It was not in the currently mounted conversation
files during this implementation; this does
not invalidate the earlier local Repair32B/32C
certification. An actual H4F3b source computation
must fail closed until that exact file is supplied.

## First-run command

```bash
cd ~/aest-memory-gravity
git pull --ff-only
source .venv/bin/activate
mkdir -p results
set -o pipefail
bash ge19/run_local_h4f3b_actual_corrected_six_piece_source.sh \
  2>&1 | tee results/ge19_H4F3B_LOCAL_runner.log
echo "EXIT=${PIPESTATUS[0]}"
```

This runner checks frozen blobs and all exact parent hashes
before starting source calculations. It runs imported
source generators in an isolated disposable working
directory to protect historical `results/` files.
Its only persistent new outputs are:

- `results/ge19_h4f3b_actual_corrected_six_piece_source.json`;
- `results/ge19_h4f3b_actual_corrected_six_piece_source.npz`;
- `results/ge19_h4f3b_actual_corrected_six_piece_source_FULL.log`;
- `results/ge19_H4F3B_LOCAL_runner.log`.

The final marker distinguishes
`GE19_H4F3B_ACTUAL_SIX_SOURCE_PASS_FULL_WARD_OPEN`,
`GE19_H4F3B_ACTUAL_SIX_SOURCE_SCIENCE_FAIL` and
`GE19_H4F3B_IMPLEMENTATION_OR_EXECUTION_FAIL`.
A valid science FAIL must be frozen without fitting
a source coefficient, changing a parent or
relaxing the original shift threshold.

Even a future H4F3b actual-source PASS leaves
the complete operator-plus-parent Ward identity
unproved; H4/Z21 and lensing remain blocked.
