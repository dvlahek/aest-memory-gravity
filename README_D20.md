# D20 — D17/D19R1-dependent source and original GE05 Ward subset

This package uses the **actual** D19R1 C_star, Nt128, Nq2048 bath data, not the historical Repair26 R1 bath. It reconstructs the original GE06/GE07 canonical H1 from the D17 8D action-based state at the original 128 knots; compares X10 with the saved D17 source-action drive; recomputes original GE06, GE07 and Lambda Q(Z10,Z11) mixed source families, action-complete StageE DY2 (both u and phi rows), and original GE05 M2 from all D19R1 bath nodes. The original sign/factor -2, signed Fourier dictionary and quadrature weights are retained. It also evaluates original GE05 normalized bath Euler/Ward on original knots (FD4) and preserves the separate D19R1 sampled signed bath Ward. Results are original-source numerical **diagnostics** for a single cohort.

**Scientific boundary:** the unchanged H3F Z20, H3G q20/B20 and Z11 still belong to the original frozen H1/R1 parent hierarchy. They are not automatically consistent with the D17/D19R1 numerical replacement. M1 uses H3G B20 solely as a clearly labeled **stale comparison** in a mixed-provenance source ledger. The original GE05 M2 routine uses FD4 on 128 knots and may be aliased for high-phase bath nodes. A small D19 GE05 residual at its fixed interior samples does not prove that its original-knot FD4 current has converged. Full original nonbath Euler and boundary Ward parents, linear H4 operator on Z21, original-action all-interval GE05 on-shell and lensing are **not** certified. The original Repair37 SCIENCE_FAIL is immutable. No observational fitting or threshold changes.

**Local run**: copy ZIP to `~/aest-memory-gravity`, then:

```bash
cd ~/aest-memory-gravity
unzip -n ge19_h4f3d20_D17_D19R1_source_and_GE05_ward_subset_package.zip \
  'ge19/*' 'docs/*' D20_SOURCE_MANIFEST.json README_D20.md
source .venv/bin/activate
mkdir -p results
set -o pipefail
bash ge19/run_local_h4f3d20_five_sources_GE05_ward_subset.sh \
  2>&1 | tee results/ge19_H4F3D20_LOCAL_runner.log
echo "EXIT=${PIPESTATUS[0]}"
```

Preflight SHA checks fail closed if the actual D17/D19R1 parent files or original action sources have changed. It prints a progress line every 256 original bath quadrature nodes while evaluating GE05 M2, and does not overwrite previous or existing D20 results. The optional immutable H4F3b source NPZ, if present in `results/` under the original filename, is hash-checked and used only to quantify the difference between old and newly recomputed GE05 M2.

Expected new files in `results/`: `ge19_h4f3d20_actual_Cstar_five_sources_GE05_ward_subset.json`, corresponding `.npz` and `_FULL.log`, plus `ge19_H4F3D20_LOCAL_runner.log`.

A D20 structural diagnostic PASS means that the dependent source routines executed consistently and produced finite values; it does **not** mean that a physical six-source/parent H4 or Z21 solution passed.
