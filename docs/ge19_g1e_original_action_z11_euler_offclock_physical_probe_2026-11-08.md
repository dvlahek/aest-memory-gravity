# GE19 G1E — original-action Z11 Euler residual on actual frozen H4 parents

Date: 2026-11-08  
Branch: `physics-first-gravitational-elasticity`  
Classification: `GE19_G1E_SOURCE_ACTION_Z11_EULER_PROBE_PREPARED_NOT_EXECUTED_INTERVAL_G1_OPEN`  
New script: `ge19/h4f3d_g1e_z11_original_action_euler_offclock.py`, commit `fb3a8e67c3b2ed42e9165f4660e4b166b8f0a7fe`.

## Why this computation, and no more lineage tests

- Original GE06+GE07+Lambda `Cmat` continuum first-order Ward syzygy 16/16 is PASS.
- H3F/Repair22 H1 nodal identity 14/14 PASS.
- G1C2 correct physical D17–H3F nodal field/drive comparison PASS, and exact-rational Bernstein bound of the two defined X10 Hermite surrogates PASS. This proves no true original-action off-clock Euler bound or H4 source interpolation.
- Original D47 R5g8 `m=20` certificate was not found anywhere in the user's searched `results` tree. Existing modes `3,5,8,10,15` remain valid in declared `C_star` primary scope only. No expensive D47 m20 reconstruction now.
- Original Repair32C Z11 `Z11_certified=true` PASS is an **artifact-only nodal/reduced-operator certificate**, NOT a continuous action-Euler residual enclosure. The actual H4 source `ge19/h4f3b_actual_corrected_six_piece_source.py` reads `{tag}_Z11_{primary/control}` and `{tag}_Z11dot_{primary/control}` from frozen Repair32B NPZ.
- GE05 first-order D55 continuous/bath certificate passes in its own frozen scope; transfer to every actual H4 cohort and off-clock original Z11 forcing remains OPEN.

## Exact action-derived operator vs numerical reconstruction

Original Repair32B solves `L_total Z11=-2 M1_GE05[H1,q10]` with frozen source factor two, in raw six main-source order:

```text
(lapse,isotropic,aether,scalar,dust_potential,dust_density).
s11 = (0,0,a^3 Q B10,-ik a^2 B10,0,0).
```

The source arrays `{tag}_M1_rhs_{label}` were saved and later used by `Repair32B.source_interp`, which applies componentwise PCHIP **in x=ln a** off knot. We must not silently replace that by the mathematically distinct `a(x)^3 Q(x)*PCHIP(B10)(x)`. The new test independently computes and compares both, with the **original action** background `a,H,Q,Z` derived from the D15a scalar charge / Lambda Exp branch, not original off-knot background PCHIP.

Canonical 8D momentum `p` is NOT `(Sdot,udot,phidot,Tdot)`:

```text
w = (N,dr,S,u,phi,T,Sdot,udot,phidot,Tdot)
p = Cmat[0:4] w
x=ln a,  d/dt = H d/dx.
```

For the explicitly declared numerical surrogate, from real frozen Z11 nodal arrays:
- construct `S,u,phi,T` **piecewise-cubic Hermite** using original saved physical time `Z11dot/H_action` at each endpoint;
- reconstruct `N,dr` by componentwise PCHIP from saved Z11 arrays;
- reconstruct nodal `p_i=Cmat(t_i)[0:4] w_i` from **original-action** `Cmat`, then define off-clock `p` as a componentwise PCHIP and its **exact PCHIP x-derivative**;
- reconstruct GE05 `B10` via componentwise PCHIP and separately the saved six-row `M1_rhs` by the original Repair32B PCHIP rule.

The continuous **surrogate physical Euler defect** at a selected offclock instant is now evaluated with original action operators, without invoking a solver:

```text
E_lapse = Cmat[4] w - s_lapse
E_dust_density = Cmat[5] w - s_dust_density
E_(iso,u,phi,T) = Cmat[6:10] w - H * d_x p_PCHIP - s_(iso,u,phi,T)
E_shift = (Cmat[10]+Cmat[11]) w
E_aniso = (Cmat[12]+Cmat[13]) w .
```

This is **six actual signed Euler main rows + two actual independent constraints**. All source row signs, the GE05 factor two, the original canonical velocity/momentum dictionary, and background callback remain frozen. The test separately reports `p_PCHIP - Cmat(x)w`, because the interpolated canonical momentum need not equal the momentum reconstructed algebraically from the chosen field surrogates at arbitrary offclock points. This mismatch is itself meaningful evidence of a physical reconstruction gap.

The program chooses the primary `C_star` case by default, all six original modes, 3 fixed fractions `1/4,1/2,3/4` of every fourth of the 127 intervals **plus final interval 126**, and recomputes all original 128 nodal Cmat momenta per mode. It keeps only one mode's local Cmat cache in memory (important for previous 9.7 GiB WSL crashes). `--interval-stride 1` and alternate `--tag C_min/C_max --grid control` are available if the pilot reveals a worthwhile certified path; **no extrapolation** from Cstar to all H4 cohorts occurs.

### Why this is not a rigorous G1 interval certificate

This test observes finite offclock samples of a **chosen** Hermite/PCHIP reconstructed frozen Z11 field. It is NOT a proven continuous-time representation of the original Repair32B Radau integrator, nor is it a rigorous **supremum bound** of the action Euler residual between sample points. It also does NOT bound the exact true GE05 `B10` error or original action background floating evaluation.

Even if all measured values are tiny, `G1_PHYSICAL_CLOSED=false`, `G3_B_total_frozen=false`, `full_H4_Ward_certified=false`, `Z21_certified=false`, `lensing_licensed=false` remain. The original D9/D12R3 physical FD4/FD8 and roundoff `B_total`, original H4 active-shift `<=1e-6`, temporal order `>=2.5`, and historical FAILs remain unchanged.

**What a PASS would still require:** explicit interval enclosure of action `Cmat`, its time derivatives, the numerical source representation and true GE05 source error, the exact off-clock Z11 numerical reconstruction, *all* first-order Euler rows and lower-parent boundary amplitudes on each original H4 cohort. Pointwise source Ward cancellation or an observed tiny sampled residual is not a substitute.

## WSL (one bounded physical probe, not a new integration)

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

python3 -m py_compile ge19/h4f3d_g1e_z11_original_action_euler_offclock.py &&
python3 -u -m ge19.h4f3d_g1e_z11_original_action_euler_offclock \
  --results-dir results \
  --tag C_star \
  --grid primary \
  --interval-stride 4 \
  --json-out results/ge19_g1e_z11_Cstar_primary_20261108.json \
  2>&1 | tee results/ge19_g1e_z11_Cstar_primary_20261108.log
echo "EXIT=${PIPESTATUS[0]}"
```

The frozen input NPZs are SHA-locked. Do not overwrite or substitute them. If source/network provenance or float handling fails, classify as implementation failure, not a physics FAIL.

## Decision gate after exactly this one probe

Inspect which of the **original physical Euler rows** dominate, and whether the difference between source `M1_rhs` PCHIP and `a^3 Q B10` action-derived offclock forcing explains part of the residual. Distinguish the magnitude of dynamic Euler defect from algebraic/shift/aniso defect and from the constitutive p mismatch. This determines the actual next analytical/interval work and avoids a blind brute-force m20 D47 rerun.

This is a physics-first ***diagnostic with no arbitrary acceptance tolerance***. An interval theorem or verified interval computation is still mandatory before integrating the true full H4 Ward.
