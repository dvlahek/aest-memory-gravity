# D20R1 — repair of canonical H1 reconstruction gate (original D20 immutable)

Original D20 failed after all parent/source hashes passed. Its `canonical_knots_to_h1` combined the six algebraic residuals into an unscaled L2 norm, then divided by a near-null pooled target. That metric is not the per-row cancellation-safe backward error used by the original frozen Repair07. D20R1 uses Repair07 `_constraint_backward_error` individually on each of the six original constraint rows. The old pooled relative norm is preserved as **report only**. Independent D17 direct canonical-state-to-X10 identity agrees with saved X10 at approximately 2.4e-18 on the original knots. A true X10 mismatch, canonical q-slot mismatch, or per-row backward error above 1e-9 still **fails closed** and prints all five diagnostic values.

D20R1 changes only the reconstruction *audit metric* and diagnostic reporting. No action, H1 state, GE05 integrator, H4 source equation, physics tolerances, observables, certified parent artifact or original D20 file is changed. This is a conditional source/GE05 Ward subset, not a full H4 Noether closure. Old H3G q20/M1 is a labeled **stale comparison**. Original FD4 M2 high-phase aliasing, nonbath Euler/boundary parents, full GE05 on-shell, Z21, lensing remain open.

Copy the ZIP into `~/aest-memory-gravity` and run:

```bash
cd ~/aest-memory-gravity
unzip -n ge19_h4f3d20r1_canonical_backward_repair_package.zip \
  'ge19/*' 'docs/*' D20R1_SOURCE_MANIFEST.json README_D20R1.md
source .venv/bin/activate
mkdir -p results
set -o pipefail
bash ge19/run_local_h4f3d20r1_canonical_backward_source_GE05_ward_subset.sh \
  2>&1 | tee results/ge19_H4F3D20R1_LOCAL_runner.log
echo "EXIT=${PIPESTATUS[0]}"
```

Return `results/ge19_H4F3D20R1_LOCAL_runner.log`, and, if produced, `results/ge19_h4f3d20r1_actual_Cstar_five_sources_GE05_ward_subset.json`, its NPZ and FULL.log. A D20R1 PASS establishes only the five-family dependency diagnostic, NOT H4 Ward, Z21 or lensing.
