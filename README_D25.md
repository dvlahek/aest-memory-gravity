# GE19 D25 — H3 first-interval shift transport (three-case decomposition)

**Purpose.** D24 showed that rebuilding the H3F source on nine dense first-interval D17 nodes did not remove the H3 shift violation: for m=14, beta=0.1, the first-step metric changed from 1.927 to 1.875. D25 does not repeat that source rebuild or solve all 40 modes. It decomposes the **frozen D22A coarse-source first-interval shift derivative** at the already source-aware projected initial boundary in three preselected cases: (m,beta)=(14,0.1),(1,1.0),(40,0.1).

In the frozen original-action canonical notation, with `s = (six main RHS, shift RHS, anisotropy RHS)` and `w=W_Y y+W_R s`, the shift defect is `g=(C_10+C_11)w-s_shift`. Define `K_y=(C_10+C_11)W_Y` and `K_s=(C_10+C_11)W_R-e_shift`. D25 evaluates

`g'_0 = K'_y y_0 + K_y (M y_0+F s_0) + K'_s s_0 + K_s s'_0`,

and preserves all four complex contributions separately. Here `s'_0` is the derivative of the **frozen original D22A PCHIP source**, not a newly asserted continuum H3F source derivative. The explicit coefficient derivatives are forward three-point probes at `h/16` and `h/32`; halving is a diagnostic only. The calculation replays the archived D23 first-step shift and records the separate D24 dense-step metric, without claiming that the D22A coarse calculation diagnoses the dense source exactly.

**Scope.** Read-only diagnostic on existing D17, D22A, D23, D24, Repair13 and frozen action generators. No H2/H3 re-integration, boundary change, new source term, tolerance change, q20/B20 reclosure, H4, Z21, lensing, or observational tuning. D22A FAIL, D23 diagnostic, D24 diagnostic, and Repair37 SCIENCE_FAIL remain immutable. The distinction between a large pointwise relative defect and a small absolute residual is preserved.

### Run (WSL)

Put `ge19_h4f3d25_H3_shift_transport_decomposition_package.zip` in `~/aest-memory-gravity`, then run:

```bash
cd ~/aest-memory-gravity
unzip -n ge19_h4f3d25_H3_shift_transport_decomposition_package.zip \
  'ge19/*' 'docs/*' README_D25.md D25_SOURCE_MANIFEST.json
source .venv/bin/activate
mkdir -p results
set -o pipefail
bash ge19/run_local_h4f3d25_H3_shift_transport_decomposition.sh \
  2>&1 | tee results/ge19_H4F3D25_LOCAL_runner.log
echo "EXIT=${PIPESTATUS[0]}"
```

Outputs: `results/ge19_h4f3d25_H3_first_step_shift_transport_decomposition.json`, corresponding `.npz`, and `_FULL.log`. Send the JSON and runner log. The NPZ is supplemental. A diagnostic COMPLETE does **not** promote any H2/H3 parent.
