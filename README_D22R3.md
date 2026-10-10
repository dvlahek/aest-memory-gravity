# D22R3 — one direct R2-boundary decision, no new H4 claims

D22A-R2 localized a failure of the shift constraint, but D22A's code used `refdot=olddot`, where `olddot` is the previously *solved* Z11 jet, not an independently rebuilt Repair28 R2 eta-tangent jet. D22R3 reads the original, SHA-locked Repair28 R2 NPZ and regenerates the complete physical initial R2 reference (`make_reference` and `integrate_dust_tangent`). It tests the fresh physical jet in both frozen and original-action constraint matrices, and **re-solves only the six Z11 modes if that input genuinely changes**. If fresh and old inputs are equivalent, it stops rather than repeating expensive, scientifically identical calculations.

The old D22A `FAIL` remains immutable. D22R3 does not solve Z20 again, change any failed tolerance, certify H2/H3, compute q20/B20 or H4/Z21/lensing, or use observations for tuning. The D22AR2 diagnostic and D22A candidate are provenance, not certified parents.

Put the ZIP in `~/aest-memory-gravity`, unzip without overwriting, activate `.venv`, and run the runner. R28 is searched in `results/*repair28*.npz` and the frozen Repair26/27 folder by its frozen SHA. If stored elsewhere, set `GE19_REPAIR28_R2_NPZ=/absolute/path/to/your/Repair28.npz` before running. For the Repair26 trace, the same `GE19_REPAIR26_R1_TRACE` fallback as D22A is used.

```bash
cd ~/aest-memory-gravity
unzip -n ge19_h4f3d22r3_direct_R2_boundary_decision_package.zip 'ge19/*' README_D22R3.md D22R3_SOURCE_MANIFEST.json
source .venv/bin/activate
mkdir -p results
set -o pipefail
bash ge19/run_local_h4f3d22r3_direct_R2_boundary.sh 2>&1 | tee results/ge19_H4F3D22R3_LOCAL_runner.log
echo "EXIT=${PIPESTATUS[0]}"
```

Outputs: `results/ge19_h4f3d22r3_fresh_R2_boundary_decision.json`, `.npz`, `_FULL.log` and the outer runner log. The JSON is the one-result decision. If the recomputed R2 jet is effectively identical to old Z11's solved jet, stop and address the original-action constraint/source compatibility rather than rerunning Z11 or Z20 and relaxing gates.
