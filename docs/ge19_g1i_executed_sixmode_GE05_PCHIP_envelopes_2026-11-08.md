# GE19 G1I — executed exact-input six-mode continuous GE05 PCHIP forcing envelope

**Date:** 2026-11-08.  
**Repo/branch:** `dvlahek/aest-memory-gravity` / `physics-first-gravitational-elasticity`  
**Executed classification:** `GE19_G1I_EXACT_INPUT_BERNSTEIN_GE05_PCHIP_CONTINUOUS_FORCING_CERTIFIED_TRUE_GE05_AND_Z11_OPEN`

## Frozen actual research evidence, not a planned run

Researcher-uploaded **executed** original G1I artifacts:

- `results/ge19_g1i_Cstar_primary_all6_20261108.json` **221,340 bytes**, SHA-256 **`e7859fb535f1ffbd254eda01075f204c4c4a9502b275fa27243e853adbbd9534`**.
- `results/ge19_g1i_Cstar_primary_all6_20261108.log` **919 bytes**, SHA-256 **`394dd35ccfea3fb238e9a7fc10628872b758859e7ce4c8ac7e068030cd3fdc26`**.

The executable `ge19/h4f3d_g1i_exact_pchip_ge05_forcing_interval_bound.py` was committed at `d6dca436d3b7b7598c889c988c8dc65b008fac93`, Git blob `d33f70509f8e710157cd57423350d2dd84ff1a25`. Original source Git blobs are locked and the reported original frozen Repair32B NPZ SHA is `5d4a0a72c08d09d096a8de0b428b3c8443fc33e8ad442ed6d997d6bf2bc6e327`. Scope: **original C_star, primary Nt128, six positive modes m=3,5,8,10,15,20, all 127 source intervals per mode**. Original scalar/aether GE05 factor-two dictionary and all old research science thresholds/failures preserved.

## Computed global all-interval source-polynomial envelopes

Each inequality is on the entire declared mathematical original Repair32B complex PCHIP source polynomial **s_h(x)**, with the generated real/imag binary64 polynomial coefficients treated as *exact rational inputs*, and exact interval endpoints of the represented x floats. Original raw Euler source row order: (lapse, isotropic, aether, scalar, dust-potential, dust-density).

| mode | bound sup_x ||s_h||_2 | bound integral ||s_h||_2 dx | bound sup_x ||s_h'||_2 |
|---:|---:|---:|---:|
| 3 | 4.1711194087590324985230e-8 | 9.079618278161878948932e-9 | 1.45283796522962349787479e-7 |
| 5 | 4.25877360786473466754846e-7 | 9.2704361490216956788473e-8 | 1.483363402462051056735838e-6 |
| 8 | 2.158443782896145014647921e-6 | 4.69847127855999849024503e-7 | 7.518015482876104647361435e-6 |
| 10 | 4.724373872820023547595775e-6 | 1.028395445646255837589531e-6 | 1.6455330532216590741866665e-5 |
| 15 | 2.1506990067210273480690128e-5 | 4.681613653102750912784391e-6 | 7.4910356565953712508685982e-5 |
| 20 | 3.7629093376111272140543802e-5 | 8.191052483872821567231423e-6 | 1.31064761598412889807384550e-4 |

These are **upper bounds on s_h amplitude and smoothness**, NOT true GE05 source errors, not shift errors, not Z11 physical solution error bars. The upper bounds are not the actual physical source or a claim of source numerical roundoff certification.

The maximal Bernstein source control in **all six modes** is control `B3` in the **last coarse source interval 126**. Every mode's interval source-vector L∞ upper values are nondecreasing along all 127 intervals. The dominant raw source row is **scalar row index 3**, with a smaller aether row index 2; original rows 0,1,4,5 are identically zero for this frozen mathematical source. For m20 scalar `sup_x |s_3| <= 3.7629086171307832982595034e-5`, aether `sup_x |s_2| <= 2.3285626270899642026531e-8`.

## Post-run independent structural checks on uploaded report

- Exactly six requested original modes, each with exactly 127 interval source/derivative/integral upper-bound triples, and the declared `C_star`/Nt128/primary scope.
- Self tests all true: exact-rational power↔Bernstein cubic identity; derivative Bernstein identity; integer-square-root upper rounding; zero polynomial.
- Per-mode global upper `Linf` equals the maximum of the reported interval-source `Linf` upper bounds; same for global upper derivative `Linf`. All six source upper sequences are nondecreasing.
- Sum of individually rounded-up per-interval L1 upper decimal values is slightly **larger** than the rounded-up accumulated exact-rational global L1 result by approximately `(6.2–6.7)e-29`; correct expected outward rounding, not a mismatch.
- Frozen source row indices nonzero only {2,3} in each mode.
- All original source-encoding flags `coefficient_generation_roundoff_enclosed=false`, `true_physical_GE05_source_error_enclosed=false`, `original_action_canonical_M_F_interval_enclosed=false`, `original_forced_Z11_8D_IVP_error_enclosed=false`, `G1_PHYSICAL_CLOSED=false`, `G3_B_total_frozen=false`, `full_H4_Ward_certified=false`, `Z21_certified=false`, `lensing_licensed=false` remain **false**, as required. No cutoff/threshold adjusted.

## Exact proof scope and mathematical caveats

For each original interval I_j, the actually generated PCHIP cubic source is converted with exact Fraction arithmetic to Bernstein coefficients B_0,…,B_3; its derivative is a quadratic Bernstein polynomial with coefficients D_0,D_1,D_2. The convex-hull norm bound yields `sup_I ||s_h||_2 <= max_k ||B_k||_2` and `sup_I ||s_h'||_2 <= max_k ||D_k||_2`, while `integral_I ||s_h||_2 <= h/4 sum_k ||B_k||_2`. The script rounds Euclidean vector norms upward using rational integer-square-root ceilings to 1e-30, not sampled time evaluations.

**Strict limitation:** these enclosures apply to the polynomial defined by the SciPy-generated stored-in-memory binary64 coefficients, interpreted as exact rational mathematical coefficients, not necessarily the exact ideal PCHIP interpolant before floating-point coefficient creation, the machine-evaluated polynomial with floating-point errors, or the true GE05 memory/bath source. In particular `coefficient_generation_roundoff_enclosed=false`; the generated SciPy coefficient-roundoff is not certified.

## What is next, scientifically (not another source/provenance microsweep)

The next proof block is **original-action continuous 8D coefficient/inversion bounds** for m20 first: `Cmat(x)` from source-derived GE06+GE07+Lambda, the six-by-six Noether-regularized algebraic submatrix `Az(x)=Calg(x)[:,ZIDX]`, continuous invertibility on all 127 subintervals (using verified interval arithmetic, interval determinant/inverse or a radii-polynomial/Krawczyk method), then `M_action(x)`, `F_action(x)`, `WY(x)`, `WR(x)` interval upper bounds. Avoid giving a mere sampled condition number the label interval certification. The original offclock background must have a justified interval representation of `H,Q,Z`, including scalar-charge exp, Lambda H, and fixed values of all frozen physical parameters.

After **actually certifying** the full operator, assemble a validated numerical reference polynomial `y_h(x)`, interval residual `r=y'_h-M y_h-F s_h`, local stability bounds and source error `s_true-s_h`; propagate to full physical Z11 Euler/shift/anisotropy and original boundary. Only then extend to original H4 cohorts, original H1/GE05 source envelopes, G3 D9/D12R3 FD4/FD8+roundoff `B_total`, full H4 Ward and Z21. No lensing license before these gates.

**Freeze decision:** `G1I_EXACT_INPUT_GE05_PCHIP_CONTINUOUS_SOURCE_ENVELOPE = EXECUTED_PASS_IN_DECLARED_SCOPE`; `G1_PHYSICAL_CLOSED = false`.
