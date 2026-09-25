# GE19 H4F3d10 original physical archive failure and H4F3d10r1 lossless repair freeze

## Scientific classification

Original H4F3d10 original-parent six-case execution:
`GE19_H4F3D10_ACTUAL_PARENT_INTERFACE_UNRESOLVED`.
All original code/input/parent hashes were true, all six
`C_min,C_star,C_max x Nt128,Nt64` cohorts completed and
their NPZ stored 530 finite arrays. All six original
archive-only case PASS flags are **false**.
This original result and original fixed
`1e-12` archive check remain immutable.

Independent uploaded-artifact audit established:
- JSON SHA256
  `df4240b40aa7f3b787e36dd0fd87212c6dcb746b35278f6cb36fc1083aa4ea21`
  (25580 bytes).
- Original NPZ SHA256
  `1b9ff8e421f2b9241cd0ffbc65967ecc4f5efc8afc43d5747ae1216f5d944fab`
  (23566797 bytes).
- FULL log byte-identical to JSON, same SHA256.
- User-local runner-log SHA256
  `14410be4b9c2139a8561a9e116ff23a64d8e76c4472a4204d8fc7ad814946648`
  (2390 bytes).
- Runner's recorded JSON/NPZ/FULL digests match actual uploads.
- All reported original low-mode parent sums, known signed
  lower-boundary combinations and spectral
  `partial_chi` algebraic identities have maximum
  relative discrepancy `2.6490057104221805e-16`.
  Independent low-mode reconstruction of all six
  original `P_known,B_known,W_known` L2 norms under
  both FD4 and FD8 differs by at most
  `1.3030086426085057e-15` relative.

**Localized implementation/interface error:** original
`h4f3d10_known_parent_boundary_assembly.py` stores
only `m0..40` Fourier coefficients even for
unprojected real `Nx128` Euler fields, then requires
relative `1e-12` recovery of each full original real
field from those deliberately truncated coefficients.
Near-zero original `E_rho10` and `E_T11` can have
a large *fraction* of their tiny norm in unsaved
`m41..64` components. In the original primary
`C_min,FD4,E_rho10` output, the full L2 is
`9.092607269317478e-21`, with inferred unarchived
high-band L2 `4.039493810461776e-21` (44.4%).
The largest reconstructed case fraction was 46.5%,
`C_star,Nt64,E_rho10`, with inferred omitted L2
`5.0972444265964545e-21`.
These high-band values are inferred by Parseval
from original saved field norm and retained coefficients;
original full high-band coefficients were NOT uploaded
and their detailed origin is not established here.
Do not equate a large near-zero-field relative
archive projection ratio with the full physical H4 Ward.

Machine-readable immutable original-forensic manifest:
`ge19/h4f3d10_original_physical_archive_projection_failure_independent_audit.json`,
Git blob `b4bce81d944201e663717e5f2d0dace546abd535`.

## Versioned H4F3d10r1 exact archive correction

Preregistered before any r1 physical execution:
`ge19/h4f3d10r1_predata_lossless_fourier_archive_repair.json`,
blob `418859847f108b31cf66ac71c998cc604ca35c31`.

Separate lossless signed assembler:
`ge19/h4f3d10r1_lossless_known_parent_boundary_assembly.py`,
blob `d4f67adc2c9267cd3e4fd0e6dd1358c2c97a8545`.
Separate physical driver:
`ge19/h4f3d10r1_lossless_fourier_physical_main.py`,
blob `659ba72aafedc6f62d519f5fe09e47736074e90a`.
Separate hash-locked no-overwrite local runner:
`ge19/run_local_h4f3d10r1_lossless_fourier_archive_repair.sh`,
blob `4bc186f7f6185198fc53cc6e072a221214ed81ad`.

Only the archive representation and archive-only inverse
transform check are corrected:
every original `m0..40` complex array is preserved
**bitwise** and every original full real `Nx128` field
also saves `m41..64` under a separate
`_hi41_64` NPZ key. All 65 nonnegative Fourier
coefficients are used for inverse real FFT, including
the exact real Nyquist mode. High-band norms and
fractions are recorded as report-only diagnostics.
Original full-resolution GE06/GE07/Lambda Euler,
physical H1/Z11, signed eight-field parent,
L/shift action boundary, time schemes, all original
bath nodes, thresholds and physics remain unchanged.

The versioned driver refuses to proceed unless both
immutable original H4F3d10 physical JSON and NPZ
match the exact SHA256 above, the original result
still classifies as UNRESOLVED and its archive gate
still failed. It independently requires the
complete original NPZ low-mode key set and EVERY
original archived low-mode array to be reproduced
bitwise by r1. This is a provenance gate, not a
new physics acceptance threshold.

Dedicated [GitHub Actions 36169632733](https://github.com/dvlahek/aest-memory-gravity/actions/runs/36169632733),
job `108185729313`, **SUCCESS**, marker
`GE19_H4F3D10R1_FULL_NYQUIST_ARCHIVE_STATIC_PASS_ACTUAL_PHYSICAL_OPEN`.
It uses source-pinned synthetic nonzero high-frequency
near-null Euler rows to reproduce the original
lossy-archive FAIL and verify the r1 full-Nyquist
archive PASS and byte-identical original low spectra.
This CI does **not** run the physical certified parents.

## Required original local physical execution

```bash
cd ~/aest-memory-gravity
git checkout physics-first-gravitational-elasticity
git pull --ff-only
source .venv/bin/activate
set -o pipefail
bash ge19/run_local_h4f3d10r1_lossless_fourier_archive_repair.sh \
  2>&1 | tee results/ge19_H4F3D10R1_LOCAL_runner.log
echo "EXIT=${PIPESTATUS[0]}"
```

The distinct outputs, if local physical execution
completes, are
`results/ge19_h4f3d10r1_lossless_fourier_known_boundary.json`,
matching `.npz`, and `_FULL.log`; retain the
separate LOCAL runner log. Independently audit
all original low-mode bitwise gates and new
full high-band arrays before any r1 physical freeze.

Original H4F3d10 is NOT relabeled a physical PASS.
No actual full H4 Noether has been evaluated.
Unknown `sum_i E_i00 F_i21,chi` and
`L21 E_L00-b21 E_b00` still require independent
action-background and Z21-dependent evaluation.
No new GE05 bath-on-shell claim, no original
Repair37 SCIENCE_FAIL relabel, no Z21
certification, no lensing. Original shift
`1e-6` and matched time order `>=2.5` unchanged.
