# GE19 G1H executed: background continuation negligible; next G1 task is certified original Z11 IVP error

**Date:** 2026-11-08  
**Repo/branch:** `dvlahek/aest-memory-gravity` / `physics-first-gravitational-elasticity`  
**Classification:** `GE19_G1H_MATCHED_DOP853_Z11_BACKGROUND_DISCRIMINATION_COMPLETED_PHYSICAL_G1_OPEN`.

## User-executed, source-locked data

- `results/ge19_g1h_z11_Cstar_primary_m20_20261108.json`: **6,796 bytes**, SHA256 `c5a09124253e3a625b22386811aa584ad79f5d954d8c2700d7633b84618b75a1`.
- `results/ge19_g1h_z11_Cstar_primary_m20_20261108.log`: **247 bytes**, SHA256 `5e1750661452e0d722d1148332c266bf258d935db3a5e27781c20ea0efe1dce7`.
- All source Git blob locks and GE15 / Repair13 / Repair32B original NPZ hashes match. Both runs have identical initial 8D canonical data (exact zero difference), frozen original GE05 PCHIP forcing, time grid, DOP853 settings `rtol=1e-11`, `atol=1e-13`, `max_step=0.005779284843151045`; each uses 1,922 RHS evaluations. Only the background offclock continuation differs.
- Scientific scope **only `C_star`, primary Nt128, original m20, k=0.13466492781697323**. No other C/cohort/mode claims.

## Numerical results, in distinct genuine norms

| comparison | global relative L2 fields | max absolute field difference |
|---|---:|---:|
| Action-background DOP853 vs frozen Repair32B | `4.14818771056538e-6` | `8.39596022830895e-7` |
| Original Repair32B-PCHIP-background DOP853 vs frozen Repair32B | `4.148055458321041e-6` | `8.396240717426165e-7` |
| Action-background DOP853 vs PCHIP-background DOP853 | `1.4652177912210892e-10` | `2.933135925746686e-11` |

The **relative L2 ratio** of action-vs-PCHIP to action-vs-Radau is `3.5321877732032194e-5` (approximately **0.003532%**, or factor 28,311). **Important:** ratios of separately normalized relative errors are descriptive and do not form an additive attribution to physical true-error.

There is, however, an exact norm argument for the **given computed paths**: set A = action-DOP853, P = PCHIP-DOP853, R = original frozen Repair32B. With the same componentwise maximum absolute norm over frozen outputs,

```text
||A-R||_inf = 8.39596022830895e-7
||A-P||_inf = 2.933135925746686e-11
||P-R||_inf = 8.396240717426165e-7
```

and the triangle and reverse-triangle inequalities give

```text
||P-R||_inf >= ||A-R||_inf - ||A-P||_inf
            >= 8.395666914716375e-7.
```

Thus changing background alone cannot account for more than `2.933135925746686e-11` of the **computed solution path correction in max norm**, approximately 0.0035% of the total observed action-vs-frozen discrepancy. This does **NOT** mean the actual Radau discretization error is proven to be `8.396e-7`; both computed IVP approximations and their interpolants lack independently validated true-solution error enclosures.

At matching DOP853 solves, relative differences in actual original canonical M and F at three sampled midpoints (time coarse intervals 0,63,126) are `1.47754e-8`, `5.23337e-11`, `1.29462e-8`, respectively. Again **samples, not a uniform coefficient enclosure**.

The action-vs-PCHIP derivative difference has relative L2 `7.798936747136309e-11`; the DOP853 vs frozen Repair32B physical derivative discrepancy remains `7.034e-7` in both background variants. Original GE05 true-source error is **not** certified.

## Direct G1 scientific decision

**Background continuation is numerically negligible for this m20 experiment.** The previous G1G mismatch `4.148e-6` is still present when the **same frozen PCHIP operator/background and same GE05 source** are used in independent DOP853 versus frozen historical Repair32B Radau integration. There is therefore a **matched-equation cross-integrator/reconstruction mismatch**, not evidence that original source action coefficients or the GE05 signed forcing dictionary must be revised.

G1E's `2.47e-4` sampled PCHIP-p Euler defect is mostly a user-specified *offclock reconstruction artefact*; G1F's ~386-fold reduction via Euler-slope Hermite p confirms that interpretation **only for those polynomial surrogates**. G1G/G1H independent IVPs show an additional distinct phenomenon: genuine path differences between two numerical solvers under the same background. Do not conflate a numerical IVP disagreement with independent proof of physical parent failure.

Do not spend more effort modifying Hermite/PCHIP source, rebuilding source ancestry, rerunning background discrimination or adjusting original physics thresholds. The historical D47 R5g8 m20 report remains **MISSING locally**, not FAIL; it cannot be filled by the G1H DOP853 run.

## Next required serious physics/numerical certification

The next computation must be a **validated enclosure**, initially for this exact `C_star` / primary / m20 forced original-action 8D Z11 canonical IVP with the actual frozen **Repair32B PCHIP GE05 M1** source. A valid certificate needs:

1. **Fixed physical IVP:** original frozen `y(x_0)` via `_initial_canonical_state`, canonical `M(x),F(x)` from unchanged original GE06+GE07+Lambda `Cmat`, and signed source `s_{11}(x)=(0,0,a^3 Q B10,-ik a^2 B10,0,0)` with its original Repair32B saved M1-PCHIP convention explicitly fixed. Keep source-representation error from true GE05 B10 and background errors as **separate terms**, never silently treat PCHIP as exact physical drive.
2. **Certified continuous coefficients:** bound `M,F` and their propagation behavior on *every interval* via analytic/interval enclosures for scalar charge/Exp branch, action `H,Q,Z`, original lambda coefficients, and the signed operator/algebraic solves. A source-operator grid sample is insufficient.
3. **Certified defect:** choose the actual numerical reference trajectory and produce a continuous-in-x interpolant with derivative. Compute an **outward-rounded interval bound** `epsilon_j >= sup_{I_j} ||y_h'(x)-M(x)y_h(x)-F(x)s_h(x)||` on each interval. Do not replace it by 1/4,1/2,3/4 or midpoint residuals, nor by raw DOP853 `rtol,atol`.
4. **Stability, not just consistency:** use validated interval fundamental-matrix/logarithmic-norm bounds or a verified collocation/Taylor method to propagate true IVP error from initial enclosure, source forcing uncertainty and defect, preserving actual physical absolute units. A naïve huge global Grönwall exponent can be useless; localized bounds with scaling and enclosure subdivision may be necessary. A merely stable-looking numerical `M(x)` is not a proof.
5. **Full covariant Euler / constraints:** reconstruct lapse/dust from actual `WY,WR` and enclose all original signed main Euler rows, shift, anisotropy and boundary traces on full continuum. A canonical eight-dimensional ODE certificate **alone** does not establish Noether/lower-boundary/H4 physical Ward.
6. **Scientific scope expansion only after pilot:** the single m20 `C_star` primary proof is not all G1. Ultimately cover original H4 `C_min,C_star,C_max`, `Nt128,Nt64` and all necessary Fourier/memory bath cohorts (including original physical H1 and D55 GE05 q-source), then freeze preregistered G3 FD4/FD8/roundoff budget `B_total`; only then evaluate full H4 Ward and solve Z21.

A mathematically valid conditional error inequality is, for fixed action background and a chosen surrogate `y_h` with `r=y_h' - M y_h-Fs_h`,

```text
e'=M e + F(s_true-s_h)-r.
||e(x)|| <= exp(INT_{x0}^x mu(t) dt) ||e(x0)||
       + INT_{x0}^x exp(INT_s^x mu(t) dt)
           ( ||r(s)|| + ||F(s)|| ||s_true(s)-s_h(s)|| ) ds
```

with `mu(t)` a **certified** upper bound on the logarithmic norm of `M(t)` for the chosen compatible norm, or a rigorously upper-bounding nonnegative function `L(t)>=||M(t)||` instead. The time-dependent propagator weight must remain inside the forcing integral; pulling out an exponential with a potentially negative logarithmic norm can be unsound. Each term must be a truly enclosed continuous quantity. This formula is not itself proof that the necessary envelopes exist or are tight enough.

## Frozen claim boundary

```text
G1G_INDEPENDENT_ACTION_DOP853_IVP_COMPLETED = true
G1H_SAME_SOLVER_BACKGROUND_DISCRIMINATION_COMPLETED = true
G1_Z11_SAME_BACKGROUND_CROSS_INTEGRATOR_DIFFERENCE_FOUND = true
G1_ORIGINAL_Z11_CONTINUOUS_VALIDATED_ERROR_CERTIFIED = false
G1_GE05_TRUE_SOURCE_ERROR_ENCLOSED = false
G1_PHYSICAL_CLOSED = false
G3_ORIGINAL_D9_D12R3_FD4_FD8_B_TOTAL_FROZEN = false
FULL_H4_WARD_CERTIFIED = false
Z21_CERTIFIED = false
LENSING_LICENSED = false
```

Original active H4 shift `<=1e-6`, temporal-convergence order `>=2.5`, old science failures, frozen parent/source weights and original numerical-precision gates are unchanged. All numerical comparison claims above apply to computed arrays, not exact solutions.
