# GE19 — G1K actual complete first-interval defect result and fused G1L controlled proof

Date: 2026-11-08. Repo `dvlahek/aest-memory-gravity`, branch `physics-first-gravitational-elasticity`.

## Executed G1K evidence, original frozen parent

Researcher-uploaded real WSL results:

- `results/ge19_g1k_Cstar_primary_m20_j0_s4_20261108.json` — 6,182 bytes, SHA256 `9f26b231d9343507dad91390fcdda01949efa9170b1f51ddac3e47a689691500`.
- `results/ge19_g1k_Cstar_primary_m20_j0_s4_20261108.log` — 341 bytes, SHA256 `c16257df6634a24d54085eaa8508fb143a4f6afb22f3c0ba77526a7390f41c8c`.
- Classification `GE19_G1K_EXACT_INPUT_FULL_SUBINTERVAL_CANONICAL_Z11_POLYNOMIAL_DEFECT_ENCLOSED_TRUE_Z11_ERROR_OPEN`.
- Provenance: original frozen dense GE15 `7f57ab676f2a31cf0abf93ff0f8b0f1f2f80bb9a58d7cf1e47e10a158c57c69f`; Repair13 `011c0ae54fd21d70c0e2c695ce62e7b74a3c5529a07c9023c882a447d5b40ca3`; Repair32B Z11 `5d4a0a72c08d09d096a8de0b428b3c8443fc33e8ad442ed6d997d6bf2bc6e327`. Original GE06, GE07, D15a, D17, Repair07 and G1I/J code SHA pins match. New exact rational Bernstein/de Casteljau and outward hull selftests passed.
- `C_star`, original primary Nt128, m20, exactly original coarse interval **j0**, x from `-0.916290731874155` to `-0.9105114470310038`; **four** exact-rational normalized subsegments with all-subsegment G1K Neumann contractions <1. This does **not** certify other 126 coarse intervals or other modes/cohorts.

## Computed all-subsegment exact-input polynomial defect upper bounds

The explicitly constructed cubic Hermite polynomial `y_h=(S,u,phi,T,pS,pu,pphi,pT)` uses the original frozen Repair32B field values and Euler-imposed nodal slopes. The frozen GE05 six-row source polynomial `s_h` is original Repair32B separate real/imag PCHIP, extended to eight forcing rows with zero shift and anisotropy. The original exact-input action GE06+GE07+Λ Cmat and 6×6 Noether Az are interval enclosed, and G1K reconstructs **separately** interval 8×8 `M,F`. The entire physical time subinterval (not selected points) is enclosed in `r(x)=y_h'(x)-M(x)y_h(x)-F(x)s_h(x)`.

| u subinterval | Neumann q upper | sup ||r||inf upper | maximum Az matrix-column correction |
|---|---:|---:|---:|
| [0,1/4] | 0.007705803770790303 | 7.355363490488548e-4 | 0.2563083637573321 |
| [1/4,1/2] | 0.007705168221860092 | 7.440725418670727e-4 | 0.25519964525592165 |
| [1/2,3/4] | 0.007704533546435668 | 7.526328362810803e-4 | 0.25409572298532423 |
| [3/4,1] | 0.007703899736874935 | 7.612339727225005e-4 | 0.2529965761944964 |

**Maximum continuous original Z11 surrogate canonical defect envelope:** `7.612339727225005e-4` absolute `||·||∞`; **full coarse j0 integrated absolute defect upper:** `4.3250371852215285e-6` in `x=ln(a)`.

Maximum per-canonical-row upper for rows [S',u',phi',T',pS',pu',pphi',pT']:

```text
2.4441805876343546e-4
7.6123397272250050e-4  <-- u' (aether)
2.4441805876344810e-4
2.4441805876548950e-4
1.9872800647011552e-5
3.7261121701319210e-8
1.0071427196912466e-4
8.7474330820066170e-22
```

**This is a proved upper bound in the exact-input polynomial/operator interval model, not an observed Euler violation, not the error in physical u, not a true-source uncertainty and not the order-H4 active shift.** The upper bound being `~7.6e-4` does **not** mean the physical Z11 or gravitomagnetic theory fails a `1e-6` gate. The narrow Neumann q and large `0.2563` correction of individual algebraic inverse columns show **interval dependency/cancellation loss** is a plausible major bound-width mechanism, not evidence of an actual singularity or physical large residual.

## Science decision: G1L, not 127 × old G1K, no parameter tuning

**Prepared successor:** `ge19/h4f3d_g1l_fused_z11_interval_canonical_defect.py`, create commit `ac61ea4`, corrected run labels commit `89a27c2`, **not yet executed**.

G1L uses the exact same original frozen Repair13/Repair32B input and original GE06+GE07+Λ Noether-regularized canonical system, identical physical Z11 Hermite polynomial and original frozen numerical GE05 source. It does **not** rerun an ODE or modify any original result or source weight. It changes only how the *interval proof enclosure* preserves algebraic correlations:

Instead of separately enclosing all 16 columns of the two linear maps `ZY` and `ZR` and subsequently widening the products `M(I) y_h(I)` and `F(I) s_h(I)`, form one **joined canonical algebraic RHS**

```text
b_j(x) = Ry(x)y_h(x)+Rr s_h(x)
Az(x) z_j(x) = b_j(x)
```

in a single interval matrix-vector solve. Select any midpoint approximate fixed complex numerical `z0` and preconditioner `R` (neither is a certificate), then use directed intervals for the complete subinterval:

```text
q = sup ||I-R Az(x)||inf < 1
rho >= sup ||R(b_j(x)-Az(x) z0)||inf /(1-q)
forall x: ||z_j(x)-z0||inf <= rho.
```

Recover `w=(N,dr,S,u,phi,T,Sdot,udot,phidot,Tdot)` and the source-driven original eight-dimensional physical derivative **directly**:

```text
f[0:4] = w[6:10]/H
f[4:8] = (Cmat[6:10] w - s_h[1:5])/H
r(x)=y_h'(x)-f(x).
```

All input `y_h,y'_h,s_h` use exact-rational Bernstein/de Casteljau hulls on each normalized subsegment, original `Cmat,H` remain G1J outward interval enclosures. G1L's selftest separately exercises nonpoint RHS interval Neumann solve on identity Az with `b0∈[1,2]` and requires the computed result to enclose the entire RHS interval. This is a **mathematically equivalent stricter enclosure** of the same frozen surrogate residual. It is allowed to be tighter, the true mathematical defect cannot be inferred from a difference between two valid upper bounds.

**Meaningful comparison after one WSL run:** compare G1L **same j0, same four subsegments** to G1K on the **same exact-input norm and source representation**. Record whether the full-subinterval and integrated upper bounds shrink materially, and by what factor. If G1L remains broad, do not force an artificial PASS by changing the physics: use narrower validated segment enclosures, correlation-preserving Taylor model or a rigorous weighted-local fundamental matrix, then ultimately bound *true* GE05 forcing error and initial-data error.

### Actual WSL local pilot

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

python3 -m py_compile ge19/h4f3d_g1l_fused_z11_interval_canonical_defect.py &&
python3 -u -m ge19.h4f3d_g1l_fused_z11_interval_canonical_defect --self-test &&
python3 -u -m ge19.h4f3d_g1l_fused_z11_interval_canonical_defect \
  --results-dir results --tag C_star --grid primary --mode 20 \
  --interval 0 --subdivisions 4 --dps 60 \
  --json-out results/ge19_g1l_Cstar_primary_m20_j0_s4_20261108.json \
  2>&1 | tee results/ge19_g1l_Cstar_primary_m20_j0_s4_20261108.log
echo "EXIT=${PIPESTATUS[0]}"
```

Preserve and send **both JSON and log**; do not rewrite original G1K output. On a source-lock mismatch, fail closed and do not use new physics constants. On an interval q>=1, classify INCONCLUSIVE, not physical singularity.

## Hard original science boundaries unchanged

```text
G1I_FROZEN_PCHIP_GE05_SOURCE_POLYNOMIAL_CONTINUOUS = PASS (six modes, Cstar primary)
G1J_ORIGINAL_ACTION_AZ_ALL_127 = PASS (one m20 Cstar primary cohort)
G1K_ORIGINAL_J0_HERMITE_CANONICAL_DEFECT = PASS (wide verified upper bound, one j)
G1L_FUSED_SAME_J0_CANONICAL_DEFECT = PREPARED, NOT EXECUTED
TRUE_PHYSICAL_GE05_SOURCE_ERROR_CERTIFIED = false
TRUE_Z11_IVP_ERROR_CERTIFIED = false
FULL_G1_PHYSICAL_CLOSED = false
ORIGINAL_D9_D12R3_G3_B_TOTAL_FROZEN = false
FULL_H4_WARD_CERTIFIED = false
Z21_CERTIFIED = false
LENSING_LICENSED = false
```

No model/forcing tuning and no observational input. Do not equate GE05 source amplitude, canonical absolute residual or the original order-H4 active-shift threshold.
