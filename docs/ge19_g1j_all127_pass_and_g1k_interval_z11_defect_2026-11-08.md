# GE19 — all 127 original-action G1J intervals PASS; G1K verified continuous Z11 canonical defect pilot prepared

**Date:** 2026-11-08  
**Repository/branch:** `dvlahek/aest-memory-gravity` / `physics-first-gravitational-elasticity`  
**Executed G1J classification:** `GE19_G1J_FIXED_INPUT_ACTION_OPERATOR_FULL_INTERVAL_AZ_NEUMANN_ENCLOSURE_PASS_Z11_OPEN`  
**New G1K status:** SOURCE IMPLEMENTED, **NOT YET EXECUTED** with frozen original project inputs.

## Frozen user-executed evidence

- `results/ge19_g1j_Cstar_primary_m20_all127_20261108.json` — **105087 bytes**, SHA256 **`e662289a96c58e2ba1c2c4316cc859dc4873e5c1dedf356f8215dfbe980489bf`**.
- `results/ge19_g1j_Cstar_primary_m20_all127_20261108.log` — **6572 bytes**, SHA256 **`d003ada76a28f9319fad93485a8cb194fc300acdcc0dd5b028d1c557609de416`**.
- All original pinned GE15, Repair13, GE06, GE07, D15a, D17, Repair07 source/NPZ SHA match; G1J interval inverse and hyperbolic symbolic lambdify selftests PASS. 60 decimal interval digits.
- **Scope:** original `C_star`, primary `Nt=128`, original `m=20` / `k=0.13466492781697323`; exactly **127 contiguous, non-overlapping original time intervals** `j=0..126`, x from **-0.916290731874155** to **-0.1823215567939546**. All 127 report `Az_continuous_invertible=true` with reported Neumann q upper strictly below 1; no missing interval or numerical fallback.

## Recomputed independent report-audit descriptive statistics

| Reported exact-input interval property | max across 127 | interval at max | min across 127 | interval at min |
|---|---:|---:|---:|---:|
| Neumann `q=||I-R Az(I)||∞` upper | `0.03087000343601109` | 0 | `0.029952983902998272` | 126 |
| `||Az^-1||∞` upper | `129.72736718728913` | 0 | `29.32132200428836` | 126 |
| `||M||∞` upper | `267944.4184581657` | 0 | `128888.76325837398` | 92 |
| `||F||∞` upper | `245550.51647192347` | 0 | `103587.48936437634` | 92 |
| `||WY||∞` upper | `141.5583418782244` | 0 | `37.38792842689827` | 92 |
| `||WR||∞` upper | `129.72736718728913` | 0 | `29.32132200428836` | 126 |
| positive lower `H` | `0.0005283123369122389` | 0 | `0.00024908420040328967` | 126 |

The midpoint **unscaled** `cond_2(Az)` ranges `2.8756793418490396e16` to `8.982775359881845e16` as an **unverified diagnostic** only, not a proof of singularity. The mathematical invertibility evidence is the interval directed Neumann bound `q<1` over each entire original interval, not the midpoint condition number. With declared binary64 original parameter inputs and correct symbolic mapping/directed interval evaluation, the 127 results collectively verify that the original reduced six-dimensional algebraic elimination is valid for every x in the declared Cstar m20 primary interval. This is a **defined exact-input continuous coefficient proof**, not an independent full-model proof including uncertainty in source generation/physical parameters.

**Important mathematical caveat:** the original G1J certificate depends on the SymPy → `mpmath.iv` expression translation consistently using directed interval arithmetic throughout, including symbolic numeric constants. Before upgrading to publication-grade proof, independently audit the generated functions for any unprotected Python-float constants or noninterval fallback and independently cross-check physical Cmat rows. The JSON PASS and internally consistent data are strong numerical evidence but a claim of *formally verified software* is not licensed.

## Exact existing frozen parent status

- G1I GE05 frozen `PCHIP` numerical source-polynomial continuum Bernstein envelope: executed PASS in declared six-mode Cstar primary 127-interval scope, **not** true GE05 source uncertainty.
- G1J exact-input original GE06+GE07+Lambda analytic action coefficient `Az` invertibility and conservative `M,F,WY,WR` bounds: 127/127 **PASS in Cstar Nt128 m20**.
- G1E/F polynomial surrogate Euler diagnostics and G1G/H independent canonical integration: numerical diagnostic scopes only; independent DOP853 same-background vs frozen Repair32B Radau `4.148055458321041e-6` relative Z11 field L2 is **not** certified error against exact IVP.
- `G1_PHYSICAL_CLOSED=false`; no rigorous error for true 8D Z11, true GE05 bath source, original H4 Ward, Z21 or lensing; original D9/D12R3 M5/M9 physical FD4/FD8 + roundoff `B_total` OPEN. Original H4 active-shift 1e-6 and temporal-order >=2.5 thresholds unmodified.

## Next actual physics computation: G1K continuous forced canonical polynomial defect, one-interval pilot

**Prepared code:** `ge19/h4f3d_g1k_interval_z11_canonical_trajectory_defect.py`, initial commit `cbbe6e0`, corrected rational subinterval endpoints / interval-integral accumulation commit `24df03a`, **NOT EXECUTED on researcher data**.

For the first original Cstar/primary/m20 interval, the script:
1. Loads hash-locked original Repair13 and Repair32B data, verifies exact original M1 source `source_from_B(B10)` on nodes. Construct original 8D canonical nodal `y=(S,u,phi,T,pS,pu,pphi,pT)` from Z11/Z11dot and GE06+GE07+Lambda momentum `p=Cmat[0:4]w`. Compute endpoint slopes `y_x=M(x)y+F(x)s_h(x)` using the original source and action callback. This endpoint relation is imposed, **not independently tested**.
2. Define an exact-in-input cubic Hermite polynomial `y_h(x)`, with its coefficients represented as **exact rational complex pairs from stored float64 endpoint states/derivatives**. Reconstruct the exact-in-input original Repair32B source cubic PCHIP `s_h(x)` using the same G1I Bernstein construction.
3. Split original interval into **four** disjoint rational normalized subintervals. Use exact rational de Casteljau subdivision and Bernstein convex hulls to bound `y_h(x), y_h'(x), s_h(x)` everywhere on each subinterval. Original x-boundaries are converted to covering float64 x boxes with **exact rational outward comparisons**, not guessed ulps.
4. Independently recompute original action `Cmat(I)` with G1J's source-derived interval GE06/GE07. Verify `Az(I)` invertible by a local directed Neumann bound. For every column of `ZY, ZR`, use a numerical midpoint guess `z0` only as a center and prove using `||R(b-Az0)||/(1-q)` that the true original-action algebraic column belongs in an explicit complex interval enclosure. Reconstruct **entrywise interval** matrices `M(I),F(I)` with the same original R07 canonical block equations, rather than only using coarse `||M||∞` norm maxima.
5. Compute directed interval (r(I)=y_h'(I)-M(I)y_h(I)-F(I)s_h(I)) and print `sup_{x in subinterval} ||r(x)||∞` upper for **every x**, plus an outward-rounded bound on `Integral ||r||∞ dx`. The latter is only a local verified **defect for the declared polynomial and declared frozen numerical source**. It may be too conservative for physical true solution accuracy; this must be assessed from the output instead of tuning physics/source.

G1K intentionally does **not** integrate a new Z11 IVP, adjust old source weights, or claim true Z11 physical error. A full validated a posteriori error still needs initial-condition and source uncertainty envelopes plus a usable interval stability propagator/log norm. An overly conservative local defect/integral is a mathematically useful blocker report, not physical failure.

### WSL pilot (four complete subintervals of j0 only)

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

python3 -m py_compile ge19/h4f3d_g1k_interval_z11_canonical_trajectory_defect.py &&
python3 -u -m ge19.h4f3d_g1k_interval_z11_canonical_trajectory_defect --self-test &&
python3 -u -m ge19.h4f3d_g1k_interval_z11_canonical_trajectory_defect \
   --results-dir results --tag C_star --grid primary --mode 20 \
   --interval 0 --subdivisions 4 --dps 60 \
   --json-out results/ge19_g1k_Cstar_primary_m20_j0_s4_20261108.json \
   2>&1 | tee results/ge19_g1k_Cstar_primary_m20_j0_s4_20261108.log
echo "EXIT=${PIPESTATUS[0]}"
```

**Interpretation decision:** If source locks or new G1K exact arithmetic fail, treat as G1K implementation failure without modifying original action. If interval Neumann q>=1 on a subsegment, mark as INCONCLUSIVE, not physical singularity. If G1K produces valid but large residuals, consider tighter interval **correlation-preserving** residual evaluation or properly scaled local fundamental matrix rather than using massive global \(\exp(\int ||M||)\) bounds. Only after local pilot is correct should one consider all127 intervals and original cohort expansion.
