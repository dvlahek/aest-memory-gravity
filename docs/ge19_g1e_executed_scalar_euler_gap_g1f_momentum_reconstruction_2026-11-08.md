# GE19 G1E executed — scalar Euler residual and G1F momentum reconstruction diagnostic

**Date:** 2026-11-08  
**Branch:** `physics-first-gravitational-elasticity`  
**Local executed classification:** `GE19_G1E_ORIGINAL_ACTION_Z11_EULER_AND_GE05_SOURCE_OFFCLOCK_SAMPLED_DIAGNOSTIC_COMPLETED_G1_OPEN`  
**Evidence supplied in this conversation:**
- `results/ge19_g1e_z11_Cstar_primary_20261108.json`, original bytes 11,175, SHA256 `58f1dc115c175c670d32b47141e668236c5779076c613678041198e31aa7afd8`.
- `results/ge19_g1e_z11_Cstar_primary_20261108.log`, original bytes 717, SHA256 `172635b94571dd5590aa748595b21b42fd66624dd2faccdea48f9c9086c3adff`.
- Original G1E source as executed `ge19/h4f3d_g1e_z11_original_action_euler_offclock.py` Git blob `017ddec6b52434920f394a728a994f017af62dd9`.

## What was actually tested

The sampled **original-action** `Cmat` GE06+GE07+Lambda first-order Euler rows and independent physical shift/aniso constraints were reconstructed on **C_star, Nt128**, with six modes `m=3,5,8,10,15,20`. For each mode, 33 original coarse time intervals (stride 4 plus last) × 3 fixed fractions (1/4,1/2,3/4) = **99 offclock points per mode**. Original scalar-charge/Lambda/Exp Repair13 background (not background PCHIP), original Repair32B Z11/Z11dot and raw six-row `M1_rhs` source, and original Repair32A/Repair32B factor-two GE05 normalization were source and SHA locked. No new solver, no H4 total Ward residual and no Z21.

The numerical field reconstruction was an *explicit surrogate*: dynamic `S,u,phi,T` cubic-Hermite in `x=ln(a)` from saved physical-time `Z11dot/H`; lapse and dust-density PCHIP; nodal canonical momenta `p=Cmat[0:4]w` PCHIP with `p_x` taken from that PCHIP; saved raw M1 RHS also PCHIP. These choices are NOT a claim that the original Radau dense output is PCHIP/Hermite.

## Quantitative findings

| mode | peak 8-row relative backward error (sampled) | peak absolute eight-row Euler L2 | peak absolute scalar row |
|---:|---:|---:|---:|
| 3 | 2.4701626383408763e-4 | 1.0581145654367644e-11 | 1.0580781747774223e-11 |
| 5 | 2.470160754580341e-4 | 1.0803327841146483e-10 | 1.0803191136773015e-10 |
| 8 | 2.4701606666413e-4 | 5.475343020182669e-10 | 5.475314533236844e-10 |
| 10 | 2.4701603495853544e-4 | 1.1984344645198956e-9 | 1.198430290002072e-9 |
| 15 | 2.4701603164287205e-4 | 5.4556828111475185e-9 | 5.455673072422955e-9 |
| 20 | 2.470162465314743e-4 | 9.545377008155973e-9 | 9.545365642741486e-9 |

**All six peak relative errors occurred at time interval 0, fraction 0.5**, a strong reproducible indication of a common reconstruction/time-discretization mechanism, but not by itself a physical proof. The scalar Euler row dominates; at m20 the remaining maximum aether row is only `1.1800908456872003e-11`, lapse `9.068379866488436e-12`. The maximum absolute shift over all modes is `1.7738357267513535e-22` (m5), and anisotropy `4.1095245505242337e-22` (m20). Do not compare these to the **original H4 active-shift <=1e-6 gate**: different perturbation order, quantity and normalization.

The frozen nodal Repair32B M1 RHS is exactly reconstructed from frozen `B10` (`recomputed_frozen_source_relative_L2=0`). After **offclock** PCHIP interpolation, saved RHS versus `(a^3 Q B10,-ik a^2 B10)` differ by at most relative `1.4452840286564495e-6` across six modes (native source L2 metric). For m20 the maximum **absolute** source difference is `1.7772337933842358e-12`, while the observed peak scalar Euler residual is `9.545365642741486e-9`, **over 5,000× larger**. Even allowing the maxima to occur at different samples, because source error is bounded by the reported sampled maximum, source-PCHIP mismatch alone cannot explain the peak residual in the same offclock sample. That is a conclusion about these samples only, not a continuous envelope.

The G1E JSON field `max_nodal_momentum_relation_discrepancy_sampled` is **misleadingly named**: the code computes `p_PCHIP(x)-Cmat(x) w_surrogate(x)` **at offclock sampled points**, not a nodal momentum mismatch. Peak (m20) `4.8891189081234445e-8`; it is bigger than the Euler dynamic residual but these two norms involve different units and may peak at different times, so one cannot assign causality without a controlled comparison. Every reported original source Cmat zero-offset was exactly zero.

## Next physically targeted computational decision: G1F

New read-only `ge19/h4f3d_g1f_z11_canonical_momentum_reconstruction_test.py` committed `84294a9eef8c739c8cba84d5d58edf9f6e88d37a` implements **one** three-way test on the same frozen Z11 and background, on the same C_star primary six modes and offclock sample pattern:

A. `pchip_saved`: exactly the original G1E PCHIP(momentum) + saved PCHIP(M1 RHS).
B. `euler_hermite_saved`: cubic-Hermite momentum `p(x)`, anchored to original frozen node values `p_j=Cmat(x_j)[0:4]w_j` and original action nodal dynamic Euler derivatives

```text
(p_x)_j = [Cmat(x_j)[6:10] w_j - M1_rhs(x_j)[1:5]] / H(x_j).
```

Use the original saved PCHIP(M1 RHS). **The nodal momentum derivative is imposed using the Euler equation**, so residual cancellation exactly at those nodes is **built in** and is NOT independent proof.
C. `euler_hermite_actionB`: same B momentum, but offclock GE05 RHS recomputed from original action `a(x),Q(x)` and PCHIP(B10), to separately measure the effect of forcing representation.

Compare sampled absolute and relative full eight-row Euler residuals, scalar row, constitutive momentum mismatch, peak positions and the first-interval midpoint, with frozen source pins and immutable physical inputs. No source tuning or new integration.

### One local WSL execution

```bash
cd ~/aest-memory-gravity
git pull --ff-only
source .venv/bin/activate
export PYTHONPATH="$PWD"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
mkdir -p results
set -o pipefail
python3 -m py_compile ge19/h4f3d_g1f_z11_canonical_momentum_reconstruction_test.py &&
python3 -u -m ge19.h4f3d_g1f_z11_canonical_momentum_reconstruction_test \
  --results-dir results \
  --tag C_star --grid primary --interval-stride 4 \
  --json-out results/ge19_g1f_z11_Cstar_primary_20261108.json \
  2>&1 | tee results/ge19_g1f_z11_Cstar_primary_20261108.log
echo "EXIT=${PIPESTATUS[0]}"
```

**Scientific go/no-go:** If B dramatically improves sampled scalar Euler residual relative to A while C≈B, the specific *PCHIP-momentum interpolation* is the dominant numerical representation error in the original G1E diagnostic. If B≈A or is worse, need a physically consistent coupled field/momentum/reduced canonical interval method rather than playing with individual interpolants. Either outcome remains a **sampled reconstruction diagnostic only**, with no rigorous true-action Euler interval error enclosure, no G1 certification and no G3 or full H4 license.

## Unchanged science flags

```text
G1_PHYSICAL_CLOSED = false
G1_Z11_CONTINUOUS_ACTION_EULER_SUPREMUM_CERTIFIED = false
G1_GE05_TRUE_B10_ERROR_ENCLOSED = false
G3_ORIGINAL_D9_B_TOTAL_FROZEN = false
FULL_H4_WARD_CERTIFIED = false
Z21_CERTIFIED = false
LENSING_LICENSED = false
```

Original GE19 16/16 source-bound **continuum linear Ward PASS**, G1B 14/14 nodal PASS, G1C2 physical nodal diagnostic PASS, old D47 m20 missing local report and predeclared original H4 science gates/old failures are all preserved.
