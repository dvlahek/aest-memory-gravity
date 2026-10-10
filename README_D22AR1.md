# GE19 D22A-R1 — localization of the failed shift constraint

D22A computed numerically finite B10/Z11/Z20 candidates but FAILED its independently
preregistered shift constraint gate (Z11 ~0.940; Z20 ~1.927). Never reclassify
D22A as PASS. This package does **not** rerun a differential equation or loosen
any numerical tolerance. It independently evaluates the exact frozen canonical
shift row Cmat[10]+Cmat[11] using the *saved* complex states and physical
time jets, the original-action background, and the saved source rows at **all**
128 time knots, six H2 modes and three beta times forty H3 modes.

It records absolute residual, backward scale, lhs, rhs, per-entry relative error
and globally aggregated diagnostics. It evaluates the historical frozen Z11
on the same action background and checks the same stored states at the
original legacy background only at the three worst offending points.
This separates solver drift, source inconsistency, local cancellation and
background interpolation as numerical hypotheses; no conclusion is
hardcoded. It must reproduce the archived D22A worst shift metrics.

It cryptographically pins the exact failed D22A JSON/NPZ and all original
source parents checked by D22A. Its output is only a forensic diagnosis;
q20/M1, full GE05 on shell, full H4 Ward, Z21 and lensing remain open.
Original Repair37 SCIENCE_FAIL and failed D22A results stay immutable.

Run from `~/aest-memory-gravity` after copying this ZIP to the repo root:

```bash
unzip -n ge19_h4f3d22a_r1_shift_constraint_localization_package.zip \
  'ge19/*' README_D22AR1.md D22AR1_SOURCE_MANIFEST.json
source .venv/bin/activate
mkdir -p results
set -o pipefail
bash ge19/run_local_h4f3d22a_r1_shift_constraint_localization.sh \
  2>&1 | tee results/ge19_H4F3D22AR1_LOCAL_runner.log
echo "EXIT=${PIPESTATUS[0]}"
```

The script prints progress at each of the six H2 modes and every five H3 modes.
It does not overwrite outputs. It needs only the exact same frozen repo,
results and Repair26 trace available during D22A. If the Repair26 trace is
stored elsewhere, use `export GE19_REPAIR26_R1_TRACE=/absolute/path/to/trace.dat`.

Upload `results/ge19_H4F3D22AR1_LOCAL_runner.log`,
`results/ge19_h4f3d22a_r1_shift_forensic.json` and `.npz`. The diagnostic
JSON stores three worst positions and checks the reproduced D22A max.
