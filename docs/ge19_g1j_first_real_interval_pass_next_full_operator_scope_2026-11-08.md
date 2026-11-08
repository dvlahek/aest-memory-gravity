# GE19 — G1J first real action-operator interval: verified Neumann criterion passes (scope j0 only)

**Date:** 2026-11-08  
**Branch:** `physics-first-gravitational-elasticity`  
**Executed classification:** `GE19_G1J_FIXED_INPUT_ACTION_OPERATOR_SUBDOMAIN_NEUMANN_PASS_FULL_G1_OPEN`  
**Uploaded local executed files**:
- `results/ge19_g1j_Cstar_primary_m20_j0_r1.json`: 3,743 bytes, SHA256 **`dcbf4163feb6cb645366bdd72949ddcda9fdd9ad92730d34acb863342b01327d`**
- `results/ge19_g1j_Cstar_primary_m20_j0_r1.log`: 123 bytes, SHA256 **`fc1e94cee1fb21bc912dd9159159a2423202df517bed7519f633910edf4aeda4`**

Frozen original GE15, Repair13, GE06, GE07, D15a, D17 and Repair07 input/source locks all match. Interval inverse selftests and interval symbolic hyperbolic lambdify test all PASS.

## Actual result and strict scope

One original interval `j=0`, `C_star`, primary `Nt=128`, Fourier `m=20`, `k=0.13466492781697323`, 60 decimal digit interval context:

```text
x0_exact_float64 = -0.916290731874155
x1_exact_float64 = -0.9105114470310038
q_neumann_upper = 0.03087000343601109  < 1
Az_continuous_invertible = true, j0 only
Az_inverse_norm_inf_upper = 129.72736718728913
Aq_norm_inf_upper = 0.09119875742066613
C_dynamic_rows_norm_inf_upper = 0.26443070547322606
WY_norm_inf_upper = 141.5583418782244
WR_norm_inf_upper = 129.72736718728913
M_norm_inf_upper = 267944.4184581657
F_norm_inf_upper = 245550.51647192347
H_lower_positive_conservative = 0.0005283123369122389
midpoint_Az_condition_2_report_only = 8.982775359881845e16
```

Under the stated exact-binary64-input GE06+GE07+Lambda analytic action interval model and assumptions of directed interval evaluations, the verified `||I - R Az([x0,x1])||inf < 1` provides mathematically a full-interval invertibility proof of `Az(x)` for all original `x` in j0, with `||Az^-1||inf <= ||R||inf/(1-q)`. Numeric midpoint `cond(Az)≈9e16` is NOT a proof of singularity nor by itself an error estimate. A numerically approximate midpoint `R` does not invalidate the interval proof because the fixed binary64 `R` itself is included as an exact input in the residual bound.

The `M`/`F` upper bounds are conservative operator norm bounds, **not observed solutions/errors**. They are too loose to immediately use a naive global `exp(Integral ||M|| dx)` estimate; aim for scaled local log norm or interval fundamental-matrix propagation with algebraic structure. Nothing here says Z11/GE05 true solution is accurate, or that H4 active shift is under `1e-6`.

## Next run: all 127 intervals, same Cstar m20 exact-input operator

The first interval passed. The natural next physics work is the **full contiguous interval run** of the same source-locked G1J script, `--start-interval 0 --interval-count 127`, distinct full-scope JSON output. It may find some intervals INCONCLUSIVE (q≥1) due to interval overestimation: these are not physical singularities, and should be addressed with mathematical subdivision/tighter enclosures, without modifying physical parameters, source weights, or earlier evidence. An all-interval output can only classify `Az` globally invertible once **all** original intervals are certified; a partial report must not be promoted.

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

python3 -u -m ge19.h4f3d_g1j_verified_action_operator_interval \
  --results-dir results --tag C_star --grid primary --mode 20 \
  --start-interval 0 --interval-count 127 --dps 60 \
  --json-out results/ge19_g1j_Cstar_primary_m20_all127_20261108.json \
  2>&1 | tee results/ge19_g1j_Cstar_primary_m20_all127_20261108.log
echo "EXIT=${PIPESTATUS[0]}"
```

The program is read-only for original input and only writes the result JSON at completion; stdout is emitted one interval at a time. If a terminal crashes mid-run, its log can show the last completed interval, but there will not yet be a final JSON. Do **not** assert a full-scope PASS based on a partial stdout log.

## Remaining strict physics gates

```text
G1I_EXACT_INPUT_GE05_PCHIP_SOURCE_POLYNOMIAL = PASS (six-mode, 127 intervals)
G1J_EXACT_INPUT_ACTION_AZ_J0 = PASS (one interval, one mode)
G1J_EXACT_INPUT_ACTION_AZ_ALL127 = OPEN
TRUE_GE05_SOURCE_ERROR_ENCLOSED = false
Z11_TRUE_CONTINUOUS_CANONICAL_IVP_ERROR_ENCLOSED = false
G1_PHYSICAL_CLOSED = false
G3_ORIGINAL_H4_FD4_FD8_AND_ROUNDOFF_B_TOTAL_FROZEN = false
FULL_H4_WARD_CERTIFIED = false
Z21_CERTIFIED = false
LENSING_LICENSED = false
```

Original 16/16 first-order source Ward, 14/14 H1 nodal identity, frozen H3F/H3G/Z11 artifact certificates and previous failures remain unchanged. No physical model tuning and no observation use.
