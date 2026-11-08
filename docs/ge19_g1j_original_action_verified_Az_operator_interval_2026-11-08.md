# GE19 G1J — continuous original-action canonical operator interval proof (prepared, unexecuted)

**Date:** 2026-11-08. Branch: `physics-first-gravitational-elasticity`.  
**Executable:** `ge19/h4f3d_g1j_verified_action_operator_interval.py`, committed as `36646b925ab3875a1bb673249c6bff961ca2f165`.  
**Status:** PREPARED, **NOT EXECUTED on the frozen researcher NPZ**. No numerical result is claimed here.

## Why G1J is the next actual physics gate

The researcher-executed **G1I** certified on all 127 original `C_star` Nt128 intervals for all six m the continuous-in-x upper bounds of the exact-input **frozen GE05 PCHIP forcing polynomial** (`S_h`, `S'_h` and `Integral ||S_h|| dx`), including for m20 `sup||S_h||_2<=3.7629093376111272140543802e-5`, `sup||S'_h||_2<=1.3106476159841288980738455e-4`, `Integral||S_h||_2dx<=8.191052483872821567231423e-6`. The source/coefficients/true physical GE05 error are not independently certified. G1H matched-solver backgrounds showed original frozen Repair32B-vs-new DOP853 `~4.148e-6` relative Z11 field discrepancy persists even on the same historical PCHIP background; this is a cross-numerical-solution difference, NOT a true-solution error bound. **Do not repeat G1E/G1F/G1G/G1H interpolation/background tests.**

The next missing component is a **verified continuous coefficient oracle** for the unmodified original GE06+GE07+Lambda action:

```text
y_x = M_action(x) y + F_action(x) S_h(x)
y=(S,u,phi,T,pS,pu,pphi,pT).
```

G1J targets the source-derived **16×10 local action matrix** `Cmat` and the original **Noether-regularized 6×6 algebraic block**. The old non-Noether partition (the six p/lapse/density rows) has a known structural null vector and is not invertible; the repaired original uses four momenta, density and **anisotropy**:

```text
Calg = vstack(Cmat[0:4], Cmat[5], Cmat[12]+Cmat[13])
ZIDX = (0,1,6,7,8,9)
QIDX = (2,3,4,5)
Az = Calg[:,ZIDX],  Aq=Calg[:,QIDX].
```

## The actual all-interval proof method

1. **Source-frozen exact-input analytic background.** For each full `I_j=[x_j,x_{j+1}]`, with stored float64 endpoints treated as exact real input, construct a high-precision outward-rounded interval using `mpmath.iv`. The original D15a/Repair13 action is

```text
a(x)=exp(x)
KQ(x)=I0 exp(-3x)
KQ=4 K2 Z0 Z exp(Z^2)  (Z>0, monotone)
Q=Q0+Z0 Z
K=2 K2 Z0^2(exp(Z^2)-1)
H^2=(Q KQ-K)/3+C exp(-3x)+rho_lambda .
```

Here **`I0` and `rho_lambda` are original frozen binary64 medians** (exact-input numerical parameters, not independently uncertain physical constants). For every x interval, lower/upper (Z) root brackets are established by 68 rational-dyadic bisections checked with outward mpmath intervals against lower and upper `KQ` bounds. This is an algebraic range proof of the positive Exp branch, not a sampling of `exp_Z_from_KQ`.

2. **Source-derived full Cmat interval.** Load the exact frozen GE06 action symbolic first-order `c1` expressions (the same stable-Z normalized expressions used by the original Repair07 generator) and frozen GE07 pressureless dust first-order expressions, lambdify them to **directed interval arithmetic** (all rational constants through `iv.mpf`, all exponentials through `iv.exp`). Inject the 10 original unit physical directions `w=(N,dr,S,u,phi,T,Sdot,udot,phidot,Tdot)` exactly as in `r7._raw_local_outputs`. Thus `Cmat(I_j)` encloses all exact original-action coefficients across the whole original temporal interval. No finite-point Cmat sampling is used to bound time variation.

3. **Provable algebraic invertibility.** Choose a numerical approximate preconditioner `R` by inverting the original `Az` at the interval midpoint. `R` is then treated **only as a fixed exact-input complex binary64 matrix**. Calculate using interval arithmetic

```text
q_j >= sup_{x in I_j} ||I - R Az(x)||_infty
```

and certify **only** when `q_j<1`. The Banach/Neumann lemma gives

```text
forall x in I_j:  Az(x) is invertible
sup_{x in I_j} ||Az(x)^(-1)||_infty
    <= ||R||_infty / (1-q_j).
```

No certification may be inferred from `cond(Az(midpoint))` by itself or from numerical matrix inversion quality. The preconditioner is allowed to be imperfect: its exact printed binary64 matrix enters the interval residual test.

4. **Certified full canonical norm upper bounds.** The original 8D canonical block is generated using `ZY=Az^-1 Ry`, `ZR=Az^-1 Rr`, `WY` and `WR` with original column placement and `M,F` from source-locked `_canonical_operator_matrices`. Since `||Ry||inf<=1+||Aq||inf` and `||Rr||inf=1`, the program conservatively bounds

```text
||ZY||inf <= ||Az^-1||inf * (1+||Aq||inf)
||ZR||inf <= ||Az^-1||inf
||WY||inf <= max(1,||ZY||inf)
||WR||inf <= ||ZR||inf
||M||inf <= max(||ZY||inf, ||Cmat[6:10]||inf ||WY||inf) / H_min
||F||inf <= max(||ZR||inf, 1+||Cmat[6:10]||inf ||WR||inf) / H_min .
```

These are rigorous **induced infinity-norm** bounds, hence they also bound the absolute values of every coefficient entry. They are not yet narrow complex interval coefficient boxes, a logarithmic-norm bound, an IVP defect/error certificate or a physical Ward residual. The original scalar (H_{min}) must have its strictly positive lower interval endpoint proved. A conservative interval `q>=1` means **INCONCLUSIVE**, not that Az is singular.

5. **Explicit local scope and source hash verification.** Before physics numbers, run two synthetic Neumann tests: a nonsingular interval matrix passes, and a singular interval matrix is rejected. Strictly verify source blobs for Repair07, D17, D15a clock, original GE06 and GE07, frozen Repair13 NPZ and GE15 dense. Source/parent changes are a provenance failure, not physical evidence. No source or original data is overwritten.

### One safely scoped WSL pilot — only m20, one original interval

Do not immediately run all 127 original intervals, since symbolic interval evaluation can be more expensive than sampled original Cmat. Start with `j=0` to test the real source functions, positive action background and nonsingular original Noether block:

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

python3 -m py_compile ge19/h4f3d_g1j_verified_action_operator_interval.py &&
python3 -u -m ge19.h4f3d_g1j_verified_action_operator_interval --self-test &&
python3 -u -m ge19.h4f3d_g1j_verified_action_operator_interval \
  --results-dir results \
  --tag C_star --grid primary --mode 20 \
  --start-interval 0 --interval-count 1 --dps 60 \
  --json-out results/ge19_g1j_Cstar_primary_m20_j0_20261108.json \
  2>&1 | tee results/ge19_g1j_Cstar_primary_m20_j0_20261108.log
echo "EXIT=${PIPESTATUS[0]}"
```

**Send the original JSON and log.** If the pilot is genuinely interval certified, the next run should cover `--start-interval 0 --interval-count 127` with a new JSON filename, not simply assume all intervals work. If `q>=1`, the correct next method is interval subdivision / stronger preconditioning, never a sampled `cond` proof. If symbolic/interval code fails, classify as **G1J implementation failure** and correct the new G1J script without modifying original GE06/GE07 or parents.

### Non-negotiable scientific limitations

Even complete G1J success would establish continuous **source-frozen exact-input original-action operator** invertibility and conservative `M,F` norm bounds, not a true error bound of the original frozen `Z11`, and not true GE05 bath forcing. A full G1 proof still requires verified all-interval numerical trajectory residual for the actual forced 8D IVP, stability propagation, original action and bath source errors, independent algebraic Euler/shift/anisotropy constraints, H1 and parent boundary, all original `C_min/C_star/C_max`/Nt128/Nt64/modes. The preregistered original G3 D9/D12R3 FD4/FD8+roundoff physical `B_total`, original H4 active-shift `<=1e-6`, temporal order `>=2.5`, full mixed H4 Ward, Z21 and lensing remain unaffected.

```text
G1I_FROZEN_PCHIP_GE05_CONTINUOUS_POLYNOMIAL = PASS_SCOPE_LOCKED
G1J_ORIGINAL_ACTION_AZ_INTERVAL_CERTIFICATE = PREPARED_NOT_EXECUTED
G1_PHYSICAL_CLOSED = false
G3_ORIGINAL_PHYSICAL_B_TOTAL_FROZEN = false
FULL_H4_WARD_CERTIFIED = false
Z21_CERTIFIED = false
LENSING_LICENSED = false
```
