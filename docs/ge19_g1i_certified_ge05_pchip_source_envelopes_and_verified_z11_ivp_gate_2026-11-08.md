# GE19 G1I — rigorous continuous envelope of the frozen GE05 PCHIP forcing, first block of validated Z11 IVP

**Date:** 2026-11-08.  
**Branch:** `physics-first-gravitational-elasticity`.  
**New committed code:** `ge19/h4f3d_g1i_exact_pchip_ge05_forcing_interval_bound.py`, commit `d6dca436d3b7b7598c889c988c8dc65b008fac93`, Git blob `d33f70509f8e710157cd57423350d2dd84ff1a25`.  
**State:** **PREPARED; not yet run on researcher’s original frozen NPZ.** The polynomial and derivative Bernstein identities were independently reproduced in an exact-rational synthetic test in this session.

## Why this is physics work rather than another sampled interpolation sweep

The executed G1G/G1H results for original `C_star`, primary Nt128, m20 show the same-background independent DOP853-vs-Repair32B field discrepancy `4.148055458321041e-6` relative global L2 and `8.396240717426165e-7` max absolute, while changing the offclock action vs PCHIP background at the fixed DOP853 integrator gives only `1.4652177912210892e-10` relative L2 and `2.933135925746686e-11` max absolute. Background continuation cannot explain the solver-path discrepancy. Neither difference is a verified bound on true original-action Z11; none may be compared to the order-H4 active shift `1e-6` gate.

A full verified 8D Z11 error proof will need interval bounds on **both** `M(x),F(x)` and the **forcing `s_h(x)`**, plus a certified continuous numerical trajectory defect and stability enclosure, and then the true GE05 source uncertainty. The new G1I completes **one genuine all-interval mathematical obligation** exactly for the frozen numerical source, without inventing unknown coefficient bounds.

Original Repair32B `source_interp` defines `s_h(x)` as **real and imaginary SciPy PCHIP** of six rows saved in `{tag}_M1_rhs_{primary/control}`; no arbitrary source retuning. The original GE05 source only drives raw Euler rows `aether=2` and `scalar=3`; the other four main source rows vanish. Original exact Repair32A factor-two normalization remains frozen; source `ge19/repair32b_factor2_corrected_reduced_h2_z11_reconstruction.py` Git blob `6ece578e8a30f48faaded8808687a9bd5c114608`. Original Repair32B NPZ must match SHA-256 `5d4a0a72c08d09d096a8de0b428b3c8443fc33e8ad442ed6d997d6bf2bc6e327`.

## True continuous enclosure of a **specified polynomial**, not sampling

For every time segment `I_j=[x_j,x_{j+1}]`, with the represented binary64 time endpoints treated as exact rationals, define `h_j=x_{j+1}-x_j>0` and `u=(x-x_j)/h_j∈[0,1]`. In each component of the **actually generated PCHIP polynomial**, with floating-point coefficients treated as exact rational values, write

```text
p_j(x) = c3 (x-x_j)^3 + c2 (x-x_j)^2 + c1 (x-x_j) + c0 .
```

Its degree-three Bernstein controls are **exactly**:

```text
b0 = c0
b1 = c0 + h*c1/3
b2 = c0 + 2*h*c1/3 + h^2*c2/3
b3 = c0 + h*c1 + h^2*c2 + h^3*c3 .
```

The derivative `p_j'(x)` is degree two with **exact** Bernstein controls:

```text
d0 = c1
d1 = c1 + h*c2
d2 = c1 + 2*h*c2 + 3*h^2*c3 .
```

Since the (nonnegative) Bernstein basis functions sum to one, for the six-component complex saved GE05 forcing vector `S_j(x)` and controls `B_{j0},…,B_{j3}` and derivative controls `D_{j0},D_{j1},D_{j2}`:

```text
sup_{x∈I_j} ||S_j(x)||_2 <= max_{k=0..3} ||B_jk||_2
sup_{x∈I_j} ||S'_j(x)||_2 <= max_{k=0..2} ||D_jk||_2

Integral_{I_j} ||S_j(x)||_2 dx
    <= (h_j/4) sum_{k=0..3} ||B_jk||_2 .
```

The last inequality follows from norm convexity and `Integral_0^1 Bernstein_{3,k}(u)du = 1/4`. **There is no time-grid sampling** in any of the three inequalities. The script interprets stored binary64 PCHIP coefficients as exact `fractions.Fraction` complex pairs, computes `sum(Re^2+Im^2)` exactly, and uses integer `isqrt` followed by an **outward** ceiling of `sqrt(sum)` to the first multiple of `1e-30` above the exact value. All interval lengths and sums are rational, and displayed 30-digit decimals are rounded UP again.

The result is a **rigorous all-time-interval algebraic certificate for the explicitly defined frozen-data SciPy PCHIP interpolant** `s_h(x)`, not a validated proof that SciPy's floating coefficient-generation arithmetic itself encloses an ideal exact mathematical interpolation algorithm, and not a true source bath uncertainty bound. The SciPy version and original SHA-256 are recorded. If implementation details of SciPy PCHIP changed across environments, the polynomial calculated **now** is explicitly the object being bounded; comparing coefficient-generation across different SciPy versions remains a separate reproducibility issue.

## How this enters the actual Z11 eight-dimensional IVP

The original reduced canonical linear Z11 system is

```text
y_x = M_action(x) y + F_action(x) S_GE05(x) ,
y=(S,u,phi,T,pS,pu,pphi,pT).
```

For the **frozen numerical forcing polynomial** `S_h`, G1I produces exact-input `Linf`, time-derivative `Linf`, and `L1` bounds over the entire interval. In a proper validated IVP proof, if a rigorously enclosed bound `||F_action(x)|| <= G_j` is independently available on an interval, then

```text
||F_action(x) S_h(x)|| <= G_j * (G1I_Linf_source_bound_j).
```

And `Integral_I ||F_action S_h|| <= G_j * (G1I_L1_source_bound_j)`. Both formulas are **conditional on a truly validated coefficient bound** `G_j`; computing `G_j` by samples would invalidate the certification.

For any explicit continuous numerical trajectory `y_h`, a posteriori residual `r=y_h'-M_action y_h-F_action S_h`, source error `S_true-S_h` and certified logarithmic-norm upper function `mu`, the correct time-dependent a posteriori inequality is

```text
||y_true(x)-y_h(x)||
  <= e^{Integral_{x0}^x mu(t)dt} ||y_true(x0)-y_h(x0)||
   + Integral_{x0}^x e^{Integral_s^x mu(t)dt}
       [ ||r(s)|| + ||F_action(s)|| ||S_true(s)-S_h(s)|| ] ds .
```

This is a theorem conditional on **verified** bounds `mu`, `||r||`, true GE05 source error and initial condition. G1I supplies the exact numerical source polynomial size and smoothness, **not** the other missing terms. In particular, no `G1_PHYSICAL_CLOSED` or `Z11_true_interval_error_enclosed` is inferred from its numerical source envelope.

## One controlled local WSL execution

This routine is read-only, consumes the original hash-locked Repair32B Z11 NPZ, and does not integrate any ODE, reproduce G1G/H or load all GE15 parents. One source-only certificate for **all six Fourier modes** of original `C_star` Nt128 can be computed together:

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
python3 -m py_compile ge19/h4f3d_g1i_exact_pchip_ge05_forcing_interval_bound.py &&
python3 -u -m ge19.h4f3d_g1i_exact_pchip_ge05_forcing_interval_bound --self-test &&
python3 -u -m ge19.h4f3d_g1i_exact_pchip_ge05_forcing_interval_bound \
  --results-dir results \
  --tag C_star --grid primary \
  --modes 3,5,8,10,15,20 \
  --json-out results/ge19_g1i_Cstar_primary_all6_20261108.json \
  2>&1 | tee results/ge19_g1i_Cstar_primary_all6_20261108.log
echo "EXIT=${PIPESTATUS[0]}"
```

If the historical SHA is absent/mismatched, **stop**, do not regenerate or substitute the original parent. Report the observed blocker. If the self-test fails, fix **G1I implementation** without altering the frozen original source.

## Next physics gate, not another interpolation comparison

After freezing G1I's rigorous source-polynomial bounds, allocate the next computation to a verified **coefficient/enclosure oracle for `M_action,F_action`** on original `C_star` Nt128 m20 across **all 127 time intervals**. This requires outward-rounded evaluation of the original source-derived GE06+GE07+Λ `Cmat` symbolic coefficients and certified `H,Q,Z` background, including the six-by-six algebraic inversion `Az^{-1}`; check its invertibility **over the full interval**, not just at sampled points. Need interval range enclosures for `M,F`, `WY,WR` and independent Noether/constraint row coefficients. A full trusted interval IVP can then use verified defect/Taylor or collocation enclosures to propagate the original physical Z11 and the true bath-source uncertainty.

Only after the m20 pilot is validated should it expand to all 6 modes and original C_min/C_star/C_max/Nt128/Nt64 cohorts and combine original continuous H1 and GE05-bath errors plus source/boundary cross terms, then freeze the original D9/D12R3 FD4/FD8 + roundoff `B_total`. No new H4 Ward cancellation has been tested and original `1e-6` H4 shift and temporal-order `>=2.5` gates are not relaxed.

```text
G1I_FROZEN_PCHIP_SOURCE_POLYNOMIAL_CONTINUOUS_ENVELOPE = prepared, NOT YET EXECUTED
TRUE_GE05_B10_SOURCE_ERROR_ENCLOSED = false
ORIGINAL_ACTION_M_F_CONTINUOUS_INTERVAL_ENCLOSED = false
Z11_8D_TRUE_CONTINUOUS_IVP_ERROR_ENCLOSED = false
G1_PHYSICAL_CLOSED = false
G3_B_TOTAL_FROZEN = false
FULL_H4_WARD_CERTIFIED = false
Z21_CERTIFIED = false
LENSING_LICENSED = false
```
