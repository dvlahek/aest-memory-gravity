# D21 — GE05 phase-safe scalar M2 time-derivative repair

D20R1 passed its five-dependent-source diagnostic but reused original-knot FD4 for the GE05 M2 scalar-phi temporal current. That derivative is not resolved for the highest-frequency bath nodes. D21 evaluates the **unchanged original GE05 quadratic current** and its exact physical-time chain derivative from D17 H1 and the stored D19R1 full 2048-node bath. It changes only M2 source row 3 and makes no Z21/lensing claims.

Place this ZIP in `~/aest-memory-gravity`. Run in WSL:

```bash
cd ~/aest-memory-gravity
unzip -n ge19_h4f3d21_GE05_phase_safe_M2_source_package.zip \
  'ge19/*' 'docs/*' D21_SOURCE_MANIFEST.json README_D21.md
source .venv/bin/activate
mkdir -p results
set -o pipefail
bash ge19/run_local_h4f3d21_GE05_phase_safe_M2_source.sh \
  2>&1 | tee results/ge19_H4F3D21_LOCAL_runner.log
echo "EXIT=${PIPESTATUS[0]}"
```

Return `results/ge19_H4F3D21_LOCAL_runner.log`, `results/ge19_h4f3d21_actual_Cstar_GE05_phase_safe_M2_source.json`, its NPZ and FULL.log. The runner streams a progress line every 256 of 2048 original bath nodes. Results are never overwritten. Run uses your exact original Git source blobs and SHA-256 frozen D17/D19R1/D20R1 results. The `D21 PASS` is restricted to original GE05 c2[pt] identity, analytic scalar time derivative and labeled source delta; it is **not** GE05 on-shell, q20/M1, H4 Ward, Z21 or lensing certification.
