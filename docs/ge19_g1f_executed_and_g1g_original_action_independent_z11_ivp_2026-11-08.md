# GE19 G1F executed: scalar defect is primarily a momentum-reconstruction effect — G1G independent forced IVP

**Date:** 2026-11-08.  
**Branch:** `physics-first-gravitational-elasticity`.  
**G1F classification:** `GE19_G1F_Z11_CANONICAL_MOMENTUM_INTERPOLATION_PHYSICAL_EULER_COMPARISON_COMPLETED_G1_OPEN`.  
**Local executed evidence furnished by researcher:**
- `results/ge19_g1f_z11_Cstar_primary_20261108.json`, SHA256 `ba2a51ec761df38f4cffe392bf3bb05b4d1de08867a523056da1f8b5625469af`.
- `results/ge19_g1f_z11_Cstar_primary_20261108.log`, SHA256 `783a7f27eb6ce3f30b95b5beb457a17ad312783b61fec0b18c1e950797f28ede`.
- Source `ge19/h4f3d_g1f_z11_canonical_momentum_reconstruction_test.py` commit `84294a9`, original source and frozen NPZ parent hashes match.
- Actual scope: **C_star primary 128 nodes, six m=(3,5,8,10,15,20)**, 33 coarse intervals × 3 offclock samples/mode; original GE06+GE07+Lambda Cmat and frozen Repair32B original exact GE05 factor-two source.

## Actual controlled G1F outcome (all six modes)

Comparison of sampled maximum eight-row relative Euler backward error for the same frozen Z11 arrays:

| reconstruction | max over six modes, sampled |
|---|---:|
| A `pchip_saved` — original G1E | `2.4701626383408763e-4` |
| B `euler_hermite_saved` — Hermite p derivative from nodal Euler, frozen M1 source | `6.404014919655009e-7` |
| C `euler_hermite_actionB` — same Hermite p, action background × PCHIP B10 | `1.1199509573801788e-6` |

At each mode, the reported ratio `max_A/max_B` is about **385.721–385.740**, and all use exact same original frozen Z11 parent and action operator. The A-to-B improvement is a *strong physical-diagnostic indication* that G1E's large `~2.47e-4` sampled scalar Euler defect is dominated by an **offclock PCHIP canonical-momentum derivative surrogate**, not an intrinsic large failure of the Z11 physics. But the Hermite p endpoint slopes were **imposed by the Euler equation itself**, so this is a comparison of reconstructions, not an independent continuous original-action Z11 certification.

At m20:
- Absolute 8-row sampled Euler norm max: A `9.545377008155973e-9`, B `1.097613337589312e-11`, C `1.1041469960971199e-11`. These absolute maxima need not be co-located with relative maxima.
- Offclock constitutive `||p-Cmat w||_2` discrepancy: A `4.8891189081234445e-8`, B/C `4.22766546676e-8`. The momentum-field consistency problem is **NOT eliminated** by choosing Hermite p.
- Original M1 source at knots matches reconstructed factor-two `B10` **exactly** (relative L2=0), but the two declared offclock source reconstructions differ: relative `1.4453e-6` sampled. C's maximum relative error is about `1.12e-6`, *larger* than B's `6.40e-7`; this does not justify changing frozen GE05 source coefficients or interpolation.

## G1F definitive decision

The scientific conclusion is **not** `G1_PHYSICAL_CLOSED=true`. G1E/G1F tested a chosen Hermite/PCHIP representation on selected offclock samples; the genuine Repair32B output was produced by a canonical Radau IVP with frozen PCHIP source on coarse time nodes, and the original D17 exact-action background continuation can differ from frozen offclock PCHIP.

**Stop changing p interpolants or replaying G1E/G1F across modes.** Use one independent physical original-action forced Z11 IVP to see how the original equation's continuous dynamics behave. Only then design a validated interval method if the comparison is consistent.

## New G1G: actual independent integration, not another source audit

Source `ge19/h4f3d_g1g_independent_action_z11_ivp.py`, commit `dc4eb889b8c8ae3fa56fad5c1c05310a303260b7`, **not yet executed locally**. It:

1. SHA-locks original Repair13 `r13.npz` / Repair32B `Z11.npz` / GE15 background, source-locks original GE06/GE07/Λ canonical operator, D17 action background and Repair32B exact factor-two M1 forcing.
2. Chooses **one challenging original m=20, C_star, Nt128 cohort** in the pilot. Uses actual initial Z11 physical `(S,u,phi,T)` and `(Sdot,udot,phidot,Tdot)`, converted to the original canonical state `(q,p)` by original Repair07 `_initial_canonical_state`, including lapse/dust initial algebraic solution and actual GE05 source.
3. Integrates the **forced canonical original-action** equation `y_x=M(x)y+F(x)s_{M1}(x)` with the independent SciPy `DOP853` explicit Runge–Kutta integrator, `rtol=1e-11`, `atol=1e-13`, and `max_step<= min coarse x interval`. This is **not** the Repair32B two-stage implicit Radau method. `s_{M1}` is the *original Repair32B frozen PCHIP-interpolated six-row raw source*, not a newly tuned source.
4. Uses original D17 source-charge/Exp/`Λ` continuum (H,Q,Z) action callback, restores the original callback even if a run fails.
5. Reconstructs `(N,S,u,phi,T,drho)` and physical-time `qdot` from genuine source-derived canonical `WY,WR`, compares the full path on **128 original frozen times** against the original Repair32B Z11/Z11dot, and reports the independently re-integrated IVP drift and each original algebraic/shift/aniso residual at knots.
6. Records exact original source hash, source-row identity, RHS evaluation counts, and approximation limitations. Does not read original H4 integrated Ward or evaluate any H4 source cancellation.

**Meaning:** This is stronger than replacing one interpolant because it independently solves the actual 8D forced ODE using a different integrator and exactly the frozen initial data and source. However both solvers use the original action model and the original offclock background conventions *differ*: their discrepancy combines integration method and background continuation effects. An IVP with same PCHIP RHS is still an approximation of true continuous GE05 memory drive. It **does not** certify the exact solution, all-interval Euler residual, or full H4 Ward.

### Single WSL pilot (m20 only, no GitHub Actions)

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

python3 -m py_compile ge19/h4f3d_g1g_independent_action_z11_ivp.py &&
python3 -u -m ge19.h4f3d_g1g_independent_action_z11_ivp \
  --results-dir results \
  --tag C_star --grid primary --mode 20 \
  --json-out results/ge19_g1g_z11_Cstar_primary_m20_20261108.json \
  2>&1 | tee results/ge19_g1g_z11_Cstar_primary_m20_20261108.log
echo "EXIT=${PIPESTATUS[0]}"
```

### Science decision afterward

If independent DOP853 vs frozen Radau Cstar/m20 state and physical derivative errors are consistent with source/clock differences, **stop interpolation sweeps and move to an interval-validated source-driven 8D IVP and its actual algebraic/constraint enclosure**, with explicit GE05 B10 source uncertainty and action background coefficient intervals. If not, the independent discrepancy is a real physics/numerics investigation (stiffness, initial data, Noether algebraic choice, source mapping) and may require correcting the original Z11 physical reconstruction **without rewriting historical evidence**.

No criterion in this G1G pilot changes the preregistered strong original H4 active-shift `<=1e-6`, temporal order `>=2.5`, D9/D12R3 FD4/FD8+roundoff physical `B_total`, or the original source weights and historical FAILs.

**Unchanged:** `G1_PHYSICAL_CLOSED=false`, `G1_Z11_INTERVAL_EULER_CERTIFIED=false`, `GE05_FULL_COHORT_SOURCE_ERROR_CERTIFIED=false`, `G3_B_TOTAL_FROZEN=false`, `full_H4_Ward_certified=false`, `Z21_certified=false`, `lensing_licensed=false`. Missing historical R5g8 m20 file remains **MISSING**, not science FAIL.
