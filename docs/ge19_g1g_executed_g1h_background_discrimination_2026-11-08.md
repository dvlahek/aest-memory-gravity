# GE19 — executed G1G independent Z11 IVP and G1H matched-background separation

Date: 2026-11-08. Branch: `physics-first-gravitational-elasticity`.  
**Executed G1G classification:** `GE19_G1G_DOP853_ORIGINAL_ACTION_FORCED_Z11_INDEPENDENT_IVP_COMPLETED_CONTINUOUS_G1_OPEN`.  
**G1H classification:** `GE19_G1H_MATCHED_DOP853_Z11_BACKGROUND_DISCRIMINATION_PREPARED_NOT_EXECUTED`.

## Immutable G1G results uploaded by researcher

- `results/ge19_g1g_z11_Cstar_primary_m20_20261108.json` (4,477 bytes) SHA256 **`2953fa13a35fb2bc60c8cd5315f61529f51915f2b8d851588df217a1ffeabd7e`**.
- `results/ge19_g1g_z11_Cstar_primary_m20_20261108.log` (166 bytes) SHA256 **`ff21e49587cb54e02562610a12a6dace26dcc9cf74a61b2c3075dda2e77407b2`**.
- Frozen input hashes match: GE15 dense `7f57ab67...fd4373c69f`, Repair13 NPZ `011c0ae5...bd5b40ca3`, Repair32B Z11 NPZ `5d4a0a72...2bc6e327`. Source Git locks matched. Original frozen M1 GE05 raw forcing derived from B10 matched all original nodes *exactly*.
- Original `C_star`, Nt128, m20, physical wavenumber `k=0.13466492781697323`, independent SciPy DOP853, `rtol=1e-11`, `atol=1e-13`, `max_step=0.005779284843151045`. `nfev=1922`, integrator `success=true`.
- Relative full state L2 error vs historical frozen Repair32B `4.14818771056538e-6`, maximum absolute difference `8.39596022830895e-7` (at final time). Dynamic fields share the same max, and the lapse/dust pair differs in relative L2 by `1.5234899616689962e-10`.
- Relative L2 time-derivative difference `7.034317228358821e-7`; maximum absolute derivative difference `1.2442188325931177e-10`.
- At actual original nodes, independent canonical reconstruction yields constitutive `max |Cmat[0:4]w-p|=2.0888837078800488e-17` and max absolute 8-row Euler/constraint `1.4032603509381149e-14`. **These nodal relations are enforced algebraically by the canonical reconstruction and the evaluated RHS; they are not independent error-vs-true-solution certificates**. The source-action background's maximum algebraic matrix condition estimate `2.74966` is diagnostic only.
- Offclock relative difference between original frozen PCHIP M1 source and action-background times PCHIP(B10) `1.466161081891597e-6` is a *representation difference*, not a certified true GE05 source error. The G1G solver uses only the **unchanged original frozen PCHIP M1 source**.

## What the independent integration proves, and its limit

G1G is the first new **independent canonical IVP integration** of the original-action GE06+GE07+Lambda forced Z11 system, rather than merely comparing Hermite/PCHIP interpolations. A different (DOP853, not implicit Radau) integrator solves it successfully without obvious physical algebraic inconsistency. However, relative `4.15e-6` deviation vs historical Repair32B cannot yet be labeled `Radau error`: historical Repair32B solves under original `r7._bg_point`, which is **offclock PCHIP** for `H,Q,Z`, whereas the new G1G uses the source-identical D17 action charge/Exp + Lambda background offclock. These are two different coefficient functions between frozen nodes even though they share the exact source-derived knot values. That difference must be separated before choosing an interval validation method. The original H4 `1e-6` active-shift gate is a *different physical object*, not applicable to these Z11 full-field comparisons.

Neither DOP853 local tolerance nor pointwise algebraic identity provides a rigorous true-solution continuum error, GE05 source-error envelope, all C modes/Nt intervals, lower-boundary Euler or prelocked original D9/D12R3 M5/M9 physical FD4/FD8 budget. **`G1_PHYSICAL_CLOSED=false`, `full_H4_Ward_certified=false`, `Z21_certified=false`, `lensing_licensed=false`**.

## Next physics-focused, one-shot matched original equation G1H

New `ge19/h4f3d_g1h_z11_background_vs_integrator_discrimination.py`, commit `2a1b5db61b751b0ecdcba9d5ace234a91ec3b66f`, is an original-data **read-only, two-integration matched experiment** on the same original `C_star` Nt128 m20 case:

1. **DOP853 + original Repair32B offclock PCHIP background** `r7._bg_point`; original frozen GE05 M1 PCHIP source; original physical initial data mapped through original canonical constraints.
2. **DOP853 + original action continuum background** D17 `ActionBackground` with exact scalar charge/Exp and Lambda H; ***same*** original frozen GE05 M1 PCHIP source, physical initial data, clock and solver settings.

Both use original GE06+GE07+Lambda 8D canonical `M,F` from frozen Repair07. The script restores original background callbacks and Cmat caches even on failure. It reports initial canonical state agreement, both full 128-node Z11 field/dot differences against frozen historical Repair32B, **action vs PCHIP under the same DOP853 solver** for both Z11 fields and derivatives, and directly samples offclock changes in original canonical `M` and force map `F`. It does **not** re-integrate other cohorts or scan old historical missing D47 m20.

### Decision logic, without fitted thresholds

Let `Z_R` be frozen Repair32B Radau state, `Z_P` new DOP853 with historical PCHIP background, `Z_A` new DOP853 with original-action background. Decompose using the triangle inequality in the **same norm**:

```text
Z_A - Z_R = (Z_A - Z_P) + (Z_P - Z_R).
||Z_A-Z_R|| <= ||Z_A-Z_P|| + ||Z_P-Z_R||.
```

Numerically **attribute by comparing actual state vectors**, not by subtracting relative scalar percentages: `Z_A-Z_P` is matched-solver background-continuation sensitivity; `Z_P-Z_R` is the remaining matched-background cross-integrator/sampling difference. They need not point in the same direction or have nonnegative signed contributions. The original Repair32B uses coarse Radau and separate reconstruction, so residual `Z_P-Z_R` also includes possible reconstruction differences; don't assert pure integrator truncation error without independent identity checks.

The G1H script does not include validated interval arithmetic, and any observed split is a **controlled numerical diagnostic only**, not a certified bound on the physical Z11 true solution or original H4 Ward. If background sensitivity dominates, prioritize original physical background interval enclosures; if same-background DOP853–Radau dominates, prioritize validated forced canonical IVP integration with original frozen physical source and full algebraic/constraint row errors. In either case, the true GE05 B10 source bound remains an independent requirement.

## One local WSL run (original m20 only)

```bash
cd ~/aest-memory-gravity
git pull --ff-only
source .venv/bin/activate

export PYTHONPATH="$PWD"
export OPENBLAS_NUM_THREADS=1
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1

mkdir -p results
set -o pipefail

if python3 -m py_compile ge19/h4f3d_g1h_z11_background_vs_integrator_discrimination.py; then
  python3 -u -m ge19.h4f3d_g1h_z11_background_vs_integrator_discrimination \
    --results-dir results \
    --tag C_star --grid primary --mode 20 \
    --json-out results/ge19_g1h_z11_Cstar_primary_m20_20261108.json \
    2>&1 | tee results/ge19_g1h_z11_Cstar_primary_m20_20261108.log
  echo "EXIT=${PIPESTATUS[0]}"
fi
```

**No original frozen artifacts overwritten**, no GitHub Actions, no new H4 Ward cancellation or Z21, no adjustment of original action/GE05 source. If a source/file SHA check fails, stop as an implementation/provenance issue rather than replacing scientific inputs.

G1H is the last necessary *discrimination* before allocating resources to a physically validated continuum parent-error method; stop repeating broad diagnostics after it.
