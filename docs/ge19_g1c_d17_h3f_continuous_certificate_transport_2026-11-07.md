# GE19 G1C — D17-to-H3F bridge for the existing D47 continuous H1 certificate

Date: 2026-11-07  
Branch: `physics-first-gravitational-elasticity`  
Classification: `GE19_G1C_SOURCE_LINEAGE_DERIVED_D17_H3F_NODAL_BRIDGE_PREPARED_CONTINUOUS_TRANSFER_OPEN`  
No new H4/Z21 solve, no source tuning, no new observations and no replacement of immutable failure results.

## The newly verified fact from actual code (rather than filename inference)

`ge19/h4f3d17_actual_original_action_dense_canonical_H1.py` (Git blob `813c350d1d1860515997ce43f223b9b6bc2091e9`) uses **the H3F immutable arrays as initial data** for a separately integrated, original-action Radau canonical H1 trajectory:

```python
h1 = h3f[f'{tag}_H1_{label}']
h1dot = h3f[f'{tag}_H1dot_{label}']
q0 = h1[im,[1,2,3,4],0]
v0 = h1dot[im,:,0]
y0,w0,idg = r7._initial_canonical_state(...,q0,v0,np.zeros(6,complex))
# integrate with the source-action continuous background, not PCHIP
```

Here canonical `y=(S,u,phi,T,pS,pu,pphi,pT)`; stored `H1=(N,S,u,phi,T,drho)`, and H1dot consists of the four physical-time dynamical momenta. D17 evaluates `r7._canonical_operator_matrices` with original GE06/GE07 and source-action scalar charge / Exp-branch / Friedmann background, rather than relying on original off-grid PCHIP as if it were action truth. It preserves the original 128 H3F clock knots as indices `0,4,8,...,508` in the D17 509-column `sub4` dense grid.

`ge19/h4f3b_actual_corrected_six_piece_source.py` consumes that *same frozen H3F array* as its actual H4 H1 parent. The locally executed G1B comparison has already proven H3F H1/H1dot equal Repair22 H1/H1dot exactly across all 14 stored original-node arrays, for Nt128/Nt64 and three C tags.

This closes the potential **initial-parent ancestry mismatch**, but does NOT say D17 Radau state and H3F original sampled state coincide at later knots. It is essential to keep that difference: D17 is an independently reconstructed original-action numerical trajectory, while H3F stores the earlier H1 pipeline's nodal result.

## D47 R5g8 physical certificate: existing scope

Historical D47 R5g8 local certificates were previously declared `GE19_D47_R5G8_PRIMARY_CSTAR_M*_N256_CONTINUOUS_H1_ARB_PASS` for **the six positive modes** `m={3,5,8,10,15,20}`, original primary/`C_star` case, 508 D17 fine Radau steps, 256 subsegments per step and original-action interval enclosure. Their previously reported conservative relative upper bounds were roughly 0.050–0.058 (worst about 5.81%) under their **own frozen denominator/normalization**, not equivalent to the original `1e-6` H4 shift threshold. These historical values are *context*, not newly rechecked contents of the six exact local JSON files.

No D47 R5g8 certificate for `C_min` or `C_max`, other Fourier modes or Nt64 is asserted here. Individual R5g7 endpoint enclosures are NOT interchangeable with R5g8 all-interval enclosures.

## Precise mathematical transport lemma

Let `y_true(x)` be the unique exact original-action first-order solution on interval `I=[x0,x1]`, with the **same canonical initial state** and background ODE; `y_D17(x)` be the D17 dense nominal/reconstruction to which a D47 continuous error certificate applies, and `y_H3F(x)` the *specific* continuous interpolant/reconstruction used to create the actual H4 source values.

At each x in I:

```text
  ||y_true(x) - y_H3F(x)||
    <= ||y_true(x) - y_D17(x)||
     + ||y_D17(x) - y_H3F(x)||.
```

If D47 provides a rigorously known absolute error function `epsilon_D47(x)` in a fixed norm, and a separately proved representation-difference bound `delta_bridge(x)`, then

```text
  sup_I ||y_true-y_H3F||
     <= sup_I epsilon_D47 + sup_I delta_bridge .
```

This requires: (a) correct D47 nominal reference and original action; (b) same initial canonical eight-vector, including separately solved N/drho algebraic rows and boundary constraints; (c) matched clock, Fourier convention and normalization; (d) existence/uniqueness on the declared interval; (e) a **rigorous full-interval bridge** to the actual H3F source-interpolation representation. A numerical *nodal difference* is NOT an upper bound on `sup_I delta_bridge`.

If D47 instead publishes a relative error `epsilon_rel = ||y_true-y_D17||/M_D47`, first recover a certified scale `M_D47` in the exact same norm and units before summing errors. It is invalid to add the historic 5–6% relative error directly to a 1e-6 shift residual or a relative H3F knot discrepancy with a different denominator.

## The immediate one-shot local test — only frozen data

Read-only program `ge19/h4f3d_g1c_d17_h3f_certificate_transport_bridge.py`:
- Locks original Git source blobs for D17, H3F, H4F3B and Repair07; refuses any unexpected code alteration.
- SHA-locks exact H3F NPZ `90840755...a4542` and D17 NPZ `cd3bcf8cf5ac9ab14385baa4d90bd53400daae9f2bb89d4d22bfa2a581846359`.
- Compares original primary/`C_star` 128 time nodes and all six 8D canonical modes, including original H3F H1dot, against D17's `primary_C_star_H1_canonical_y_dense_sub4[:,:,::4]`. Exact grids and shape are enforced, but no match tolerance is fitted. Reports initial and full-clock difference and per-component absolute maxima.
- Reads existing `results/d47_offclock_first_interval/d47_r5g8_primary_cstar_m{m}_n256_continuous_h1_final.json` reports for all six m, recording SHA, exact classification and genuine declared `case_mode_continuous_H1_error_enclosed` flags; it does not run or overwrite D47.
- Makes NO assertion that a small nodal difference proves all-interval H3F interpolation equivalence, that D47's relative error is the original H4 Ward error budget, or that any new G1/H4 science gate is closed.

Run locally with:

```bash
cd ~/aest-memory-gravity
git pull --ff-only
source .venv/bin/activate
export PYTHONPATH="$PWD"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
set -o pipefail
mkdir -p results

python3 -u -m ge19.h4f3d_g1c_d17_h3f_certificate_transport_bridge \
  --results-dir results \
  --d47-dir results/d47_offclock_first_interval \
  --json-out results/ge19_g1c_d17_h3f_bridge_20261107.json \
  2>&1 | tee results/ge19_g1c_d17_h3f_bridge_20261107.log
echo "EXIT=${PIPESTATUS[0]}"
```

No new numerical integration is performed, and original H3F, D17, D47, D55, H4 sources and scientific thresholds are untouched. Missing original files/changed SHA are grounds to **stop**, not to regenerate a substitute and silently inherit certification.

## Scientifically meaningful next step after this bridge

If local D17 and H3F knot discrepancies are quantified and all six D47 R5g8 certificates are traceable to the same D17 nominal/physical-clock initial-value problem, use an *independently controlled* continuous H3F-reconstruction difference `delta_bridge` and the D47 error envelope to obtain a **true interval source-parent error bound** in the exact original physical norm. Then propagate that to the H4 bilinear/M1/M2 and Y source by analytic source Lipschitz/envelope estimates, keeping the separately certified Z11 and GE05 bath hypotheses explicit.

For `C_min`, `C_max` and 40 H4 source modes obtained by nonlinear pair convolution, the six-mode `C_star` D47 certification does not automatically extend to all C tags; source-support and modal coupling must be audited. Avoid extrapolation.

If the D47 bound is too conservative to support the required eventual H4 tolerance, report that as a quantitative limitation and select a genuinely tighter independent physical method. Do not tune RHS weights, change the original 1e-6 H4 active-shift threshold or relabel historical FAILs.

## Frozen statuses

```text
G1B_H3F_REPAIR22_NODAL_IDENTICAL = true
G1C_D17_H3F_INITIAL_DATA_SOURCE_CONNECTED = true
G1C_D17_H3F_NODAL_DIFFERENCE_MEASURED = false  # local new test not run
G1C_D47_TO_H3F_ALL_INTERVAL_TRANSFER_CERTIFIED = false
G1_Z11_CONTINUOUS_EULER_CERTIFIED = false
G3_FD4_FD8_PHYSICAL_B_TOTAL_FROZEN = false
FULL_H4_WARD_CERTIFIED = false
Z21_CERTIFIED = false
LENSING_LICENSED = false
```
