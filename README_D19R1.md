# GE19 D19R1 — original-action GE05 bath numerical reclosure

This version fixes the **independent offline test's missing exponential factors in the overdamped frozen bath step**. It does not modify original Repair24, D13–D18, the Repair26 trace, observational parameters, or the previous D19 preregistration. Corrected full D16R1 parent replay gave exactly zero relative error in both z and v; initial weighted errors were approximately 5e-16. The old independent discrepancy was an implementation error, not evidence of an original GE05 failure.

The verified, source-frozen D19R1 driver takes the original D17 action-derived H1 X/X_x fine grid, continuous D15a original action H(x), the exact frozen Repair24 step, and archived D16R1 original Repair26 bath initial data. It replays all frozen D16R1 node states before starting. It then computes 64, 128 and 256 physical-clock steps per original H3F interval, retaining all 2048 quadrature nodes and all six positive Fourier modes, with the signed +/- GE05 source and the original phase mask.

Original D19 numerical thresholds are preserved, especially sampled GE05 relative residual <= 0.001 and sub128-vs-sub256 full node v <= 0.0005. No threshold changes are permitted after seeing results. Source-action original H1 is still a numerical reconstruction rather than a certified continuum bound. Sampled GE05 residual does NOT prove all-interval GE05 on-shell, full H4 Ward, q20/Z11 reclosure, Z21 or lensing.

The independent accelerated pilot saw GE05 sampled residuals 0.003156, 0.000525 and 0.000196 for 64, 128 and 256 steps. Its source-step outputs agreed with frozen Repair24 on a separate 8-original-interval spot test at < 1e-12. The actual locked D19R1 runner has not been executed on the user's local parent data; its result must be judged solely by its own JSON.

## WSL command

Copy the ZIP to your repository root `~/aest-memory-gravity`. Run:

```bash
cd ~/aest-memory-gravity
unzip -n ge19_h4f3d19r1_original_action_GE05_bath_extended_package.zip 'ge19/*' 'docs/*' D19R1_SOURCE_MANIFEST.json README_D19R1.md
source .venv/bin/activate
set -o pipefail
bash ge19/run_local_h4f3d19r1_source_action_physical_bath_numerical_reclosure.sh 2>&1 | tee results/ge19_H4F3D19R1_LOCAL_runner.log
echo "EXIT=${PIPESTATUS[0]}"
```

The runner uses an unbuffered Python process and prints progress every 16 original intervals, so output is visible in WSL during the three real bath propagations. No prior files are overwritten.

Output: `results/ge19_h4f3d19r1_actual_Cstar_Nt128_Nq2048_numerical_reclosure.json`, `.npz`, `_FULL.log` and the runner log. If any gate fails, the JSON records `numerical_tol_pass=false`, even when the process completed successfully.
