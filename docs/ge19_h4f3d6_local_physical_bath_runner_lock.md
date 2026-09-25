# GE19 H4F3d6 — locked local physical bath-parent Ward subset

## Status

**READY FOR FIRST EXACT LOCAL PHYSICAL SUBSET RUN; NOT YET EXECUTED.**

The newly versioned H4F3d6 code reconstructs the original certified
Repair26 R1 per-node `z10,v10` first-order bath on the actual
H3F/H3G/Z11/R13 corrected-parent `x=ln(a)` grid. It calculates
the physical normalized GE05 Euler residual and its signed
`+4 sum_j E_qj10 q_j10,x` mixed Ward term using an independent
Fourier convolution over both positive and conjugate-negative
original modes.

This is only the **bath-parent subset**. It records the actual
frozen H4F3b source Ward and `W_source+W_bath`, but neither
sum is required to vanish without all nonbath parents,
action boundary and canonical linear-operator Ward.

The original physical H4F3b six-piece source files
and certified historical Repair32B Z11 NPZ exist in the
user's prior local scientific execution, but are not
present in the GitHub Actions checkout. No fabricated
replacement has been used. No H4/Z21 solver was run.

## Frozen artifact and CI

Predata:
`ge19/h4f3d6_predata_actual_normalized_bath_parent_ward.json`,
blob `d283086a6ae95efd184db570d6c2f9a8aa32ac7c`.

Code:
`ge19/h4f3d6_actual_normalized_bath_parent_ward.py`,
blob `0419145499f5f44e06ba0c96f779c2a604e84ce7`.

Valid manufactured compiler freeze:
`docs/ge19_h4f3d6_bath_convolution_compiler_valid_freeze.md`,
blob `5695cc61be84098787af2cec8585f7daea6ced38`.
The compiler's own GitHub run `36127944207` passed,
JSON SHA-256
`db6eb2effc711c2c83ebeff6bbeae5e64c295e160505174d657ec676e2f8ad9f`.

Frozen physical local runner:
`ge19/run_local_h4f3d6_actual_normalized_bath_parent_ward.sh`,
blob `3690147a766f276309d628fba9f436df3941deae`.

Dedicated runner static audit:
- workflow:
  `.github/workflows/ge19-h4f3d6-local-runner-static.yml`,
  blob `19a84a54be88bd0e95e24434b9f7c5d315fa72dc`;
- run `36128447037`;
- job `108049891704`;
- conclusion `success`;
- terminal marker `GE19_H4F3D6_PHYSICAL_LOCAL_RUNNER_STATIC_PASS`.

**Neither CI job evaluates the actual physical H4F3d6 bath parent.**

## First exact physical run

```bash
cd ~/aest-memory-gravity
git pull --ff-only
source .venv/bin/activate
mkdir -p results
set -o pipefail
bash ge19/run_local_h4f3d6_actual_normalized_bath_parent_ward.sh \
  2>&1 | tee results/ge19_H4F3D6_LOCAL_runner.log
echo "EXIT=${PIPESTATUS[0]}"
```

The runner checks all tracked code blobs and local modifications,
then the original H4F3b source JSON and NPZ hashes, exact
H3F/H3G/Z11/R13 certified parents and Repair26 R1 trace
before launching any physical calculation.

It runs in a temporary CWD to isolate the historical
generator side effects and writes only new files:

- `results/ge19_h4f3d6_actual_normalized_bath_parent_ward.json`;
- `results/ge19_h4f3d6_actual_normalized_bath_parent_ward.npz`;
- `results/ge19_h4f3d6_actual_normalized_bath_parent_ward_FULL.log`;
- `results/ge19_H4F3D6_LOCAL_runner.log` from the outer tee.

Success marker:
`GE19_H4F3D6_ACTUAL_BATH_SUBSET_PASS_FULL_NOETHER_OPEN`.

All derived physical bath Euler residual magnitudes,
source+bath complex arrays and their natural scales are
**report-only**. The first local physical result must be
frozen as distinct PASS, subset FAIL, input/implementation
FAIL or unresolved; no new zero threshold may be chosen
after inspecting the arrays.

## Next scientific work

Instantiate and independently evaluate the remaining
nonbath Euler lower-parent and action-boundary terms
alongside the frozen original canonical Cmat operator
Ward on the exact same corrected physical grids.
Preregister and justify the full structural FD4/FD8
truncation tolerance from the signed identity **before**
testing the integrated physical result.

Only a complete independently validated all-sector
H4 Ward structural PASS would license a separately
preregistered Z21 science run. It would not itself
certify Z21.

Original Repair37 H4 FAIL, Repair38--44 diagnostics
and original active-shift 1e-6 and matched temporal
order >=2.5 remain unchanged.

**Full all-sector H4 Noether NOT CERTIFIED;
Z21 NOT CERTIFIED; lensing blocked.**
