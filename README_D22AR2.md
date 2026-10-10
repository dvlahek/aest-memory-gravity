# D22A-R2 — JSON serialization-only repair of archived shift localization

D22A-R1 finished all six Z11 and 40 Z20 mode evaluations but failed at JSON
serialization because the worst-mode index was a `numpy.int64`. It wrote no
completed forensic JSON/NPZ. R2 uses the same archived D22A SCIENCE_FAIL inputs,
original-action operator, physics equations, time derivatives, gates and norms.

The exact change to the calculation is **none**. The implementation converts
the Z20 worst-mode index to a native Python `int` and supplies a strict JSON
encoder for NumPy scalar diagnostics (`integer`, `floating`, `bool_`). Complex
numbers, NumPy arrays, unexpected objects and nonfinite numbers remain
rejected. The immutable original R1 script must match its pinned SHA-256.

R2 produces NEW forensic files, does not overwrite R1 or D22A outputs, does
not solve any equations, and does not certify Z11/Z20/q20/H4/Z21/lensing.
Its own negative control checks the serialization path before running.

Copy the ZIP into `~/aest-memory-gravity` and run in WSL:

```bash
cd ~/aest-memory-gravity
unzip -n ge19_h4f3d22a_r2_shift_serialization_repair_package.zip \
  'ge19/*' README_D22AR2.md D22AR2_SOURCE_MANIFEST.json
source .venv/bin/activate
mkdir -p results
set -o pipefail
bash ge19/run_local_h4f3d22a_r2_shift_constraint_serialization_repair.sh \
  2>&1 | tee results/ge19_H4F3D22AR2_LOCAL_runner.log
echo "EXIT=${PIPESTATUS[0]}"
```

Upload the runner log and
`results/ge19_h4f3d22a_r2_shift_forensic.json` and `.npz`. The output
will localize the actual stored D22A shift residuals; a failure of its
reproduction check remains a real forensic finding and must not be
reclassified as a D22A PASS.
