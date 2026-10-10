# D21R1 — unbound `proper` implementation repair

D21's actual M2 calculation ran over all 2048 bath nodes. The final source-Ward serialization referenced an undefined `proper` variable at old line 204. The failed run wrote **no JSON or NPZ**. This D21R1 is a versioned, fail-closed repair. It never edits the old D21 source, its preregistration, D17, D19R1, D20R1, original action or frozen Repair37.

The exact code change is: recompute `proper=physical_six_piece_ward(parts, x, a, H, kfund)` after replacing only the M2 scalar row, compare its `total_source_ward` to the archived D20R1 `oldward`, then save that recomputed Ward. Each source family retains its frozen FD8 or FD4 scheme. This is source-only Ward linearity, **not full H4 Noether**. Original D21's physical M2 calculation, sign, node count, gates and cutoffs are unchanged.

The completed earlier run logged the final `c2[pt]` current identity discrepancy 5.094e-12, below the original preregistered 1e-10 threshold. That is a preliminary pointwise algebra check, not a final D21R1 PASS.

From repo root in WSL, copy the ZIP there, then run:

```bash
cd ~/aest-memory-gravity
unzip -n ge19_h4f3d21r1_undefined_proper_repair_package.zip \
  'ge19/*' 'docs/*' D21R1_SOURCE_MANIFEST.json README_D21R1.md
source .venv/bin/activate
mkdir -p results
set -o pipefail
bash ge19/run_local_h4f3d21r1_undefined_proper_repair.sh \
  2>&1 | tee results/ge19_H4F3D21R1_LOCAL_runner.log
echo "EXIT=${PIPESTATUS[0]}"
```

Return runner log, `results/ge19_h4f3d21r1_actual_Cstar_GE05_phase_safe_M2_source.json`, NPZ, FULL.log. The runner emits progress after every 256 of 2048 nodes. It fails closed on original-action/source/parent SHA, scientific gates or output paths. No old result is overwritten. GE05 on-shell, q20/M1, Z11 under D17 drive, full H4 Ward, Z21 and lensing stay open.
