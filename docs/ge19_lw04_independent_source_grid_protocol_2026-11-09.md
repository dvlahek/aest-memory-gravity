# GE19 LW04 — one fixed-physics source-time sampling refinement

**Date:** 2026-11-09. **Status:** FROZEN PREEXECUTION, NOT SCIENTIFIC PASS. **Scientific reason:** LW03 source/Fourier native-grid equality was machine accurate, but its lensing quadrature failed at every eligible multipole.

Pre-data was frozen *before any new LW04 CLASS calculation* in commit **afd9aae00700a8cabb1db0b2493f820720296a4c**:
[ge19/lw04_source_grid_refinement_predata_20261109.json](../ge19/lw04_source_grid_refinement_predata_20261109.json). Executable:
[ge19/lw04_source_grid_refinement_20261109.py](../ge19/lw04_source_grid_refinement_20261109.py). No GitHub Actions.

## Why this resolution change is independent of LW03 quadrature

CLASS **pinned upstream code** at commit \`e85808324f51fc694d12e3ed7439552a3c3f9540\` explicitly sets \`perturbations_sampling_stepsize\` default **0.1** in \`include/precisions.h\`. In \`source/perturbations.c\`, this multiplies the source timescale when CLASS creates \`tau_sampling\`. Thus modifying it to **0.025** recomputes actual saved source histories with a different temporal source discretization. This is not equivalent to integrating an unchanged smooth interpolation at more radial points. The **CLASS integrator tolerance is not modified**, so the experiment probes source-time sampling, not independent ODE tolerance or physical action completeness.

Only **three** new CLASS linear computations on the unchanged positive-Drude forcing: baseline, lambda +2.5, lambda -2.5. The prior three-run LW03 \`W\` and signed \`dW/deta\` are loaded from the immutable archived local NPZ, rather than rerun. The program also verifies original k-prefix exactly, SHA-pins LW01/LW03 JSON and NPZ and the original force, pins the patched official CLASS HEAD, and compares the same previously saved four 65-point \`chi\` paths. Thus source-time discretization is the **only intended new numerical axis**.

## Frozen decision gates (not to be changed after looking at results)

- Refined native Fourier source-time node count ≥ twice the original 24 nodes; otherwise source resolution was not truly increased enough.
- Exact k-prefix relative error ≤1e-10, geometry discrepancy ≤1e-8, and all transfer samples finite.
- For each original ell=100,150,200,300: additive whole-window relative L2 \`W\` change ≤1%; additive signed \`TW\` change ≤1%. There are no local \`TW/W\` ratios near zero crossings.
- For each ell, \`abs(dC_fine-dC_LW03)/∫abs(dC_LW03(chi)) dchi ≤0.05\`, where signed integrals refer to the **same original 65 chi points and same source-plane**; normalizing by absolute integrand prevents unstable division by a near-cancelled integrated derivative.
- No posthoc multipole masking or threshold changes; all four eligible multipoles must pass the same numerical stability gate.
- ell500 remains outside original ≥4 native-z support and is excluded **because its exclusion preceded any LW04 result**, not for favorable-sign selection.

**Possible PASS:** finer CLASS source-time grid reproduces the original 65-point source Weyl/lensing intermediate within specified limits. **Even this is not a fully converged radial integral**, and LW03 stays a valid FAILED gate.

**Possible FAIL:** original offnative Weyl interpolation changes significantly after genuine source-time grid refinement, or a strict numerical gate fails. Then the physical lensing sign is clearly unresolved, and no DES/ACT interpretation is allowed. In either case, only one frozen local campaign is authorized here, not repeat-until-pass tuning.

## Full observable not yet available

Even if this limited time-grid test passes, the following remain missing for a Nature-level detection or constraint: independently validated radial integration (previous LW03 FAIL), complete \(k,z\) support for a survey source distribution, physical coupling normalization, baryonic/galaxy-bias/systematics model, covariance-aware likelihood, negative controls against instantaneous modified gravity, and external replication. The high-level scientific plan is [GE19 observational pivot](ge19_nature_target_observational_pivot_2026-11-09.md).

## One copyable local WSL execution

\`\`\`bash
cd ~/aest-memory-gravity
git pull --ff-only
source .venv/bin/activate
export OPENBLAS_NUM_THREADS=1
export OMP_NUM_THREADS=1

python3 -m py_compile ge19/lw04_source_grid_refinement_20261109.py
python3 -u -m ge19.lw04_source_grid_refinement_20261109 --self-test

set -o pipefail
python3 -u -m ge19.lw04_source_grid_refinement_20261109 \
  --class-root "$PWD/class_v077" \
  2>&1 | tee results/ge19_lw04_source_grid_refinement_20261109.log
echo "EXIT=\${PIPESTATUS[0]}"
\`\`\`

Expected results \`results/ge19_lw04_source_grid_refinement_20261109.{json,npz,log}\`, all under the existing local WSL checkout. For a code/compatibility failure, preserve the failed log; only change implementation if a discrete bug is demonstrated. No CLASS source modification or forcing rerun is permitted.
