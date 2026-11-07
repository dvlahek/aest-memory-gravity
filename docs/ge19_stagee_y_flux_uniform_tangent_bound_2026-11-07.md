# GE19 — uniform tangent bound for Stage E nonanalytic Y flux

**Date:** 2026-11-07  
**Class:** `GE19_STAGEE_Y_FLUX_UNIFORM_TANGENT_REMAINDER_ANALYTIC_LEMMA_ONLY`  
**Scope:** mathematical lemma for an *existing* source; NOT a new certified FD8 clock budget, all-parent Noether test, or H4 science PASS.

## Frozen Stage E action-source binding

Original `ge19/h4_stagee_versioned_y_source_rows.py`, blob `282166ea5840d7fba4dbc328d40d7687afa6fa0f`, explicitly defines

```text
g10 = Q*u10 + phi10_x/a
g11 = Q*u11 + phi11_x/a
F(g) = |g| g
flux_H3 = F(g10)
flux_H4 = 2 |g10| g11
```

and uses the **same frozen finite Fourier projector** `P_K` before taking spatial derivatives. The u and phi source rows are `S_u = 2 a^3 Q kappa P_K(flux)` and `S_phi=-2 a^2 kappa d_x P_K(flux)`. All Y shift/isotropic/anisotropy rows are exactly zero, so the **direct Y source-Ward** term is exactly zero regardless of its flux differentiability. This is the previously recorded Stage E support lemma; do not replace it by a fictitious global Y C9 regularity assumption.

## Uniform analytic lemma at zero-gradient crossings

For the real scalar `f(g)=g|g|`, `f'(g)=2|g|` for **all real g**, including `g=0`. Moreover the derivative is globally Lipschitz with constant 2, since `|f'(x)-f'(y)|=2 ||x|-|y|| <=2|x-y|`.

Therefore the integral remainder is bounded, for any real `g,h`:

```text
f(g+h)-f(g)-2|g|h
 = int_0^1 [f'(g+s*h)-f'(g)] h ds

|f(g+h)-f(g)-2|g|h| <= |h|^2.
```

Setting `h=eta*g11` proves the **uniform (including zero-set) tangent estimate**:

```text
|F(g10+eta*g11)-F(g10)-2 eta |g10|g11|
    <= eta^2 |g11|^2.
```

On a periodic finite spatial domain and in the standard L2 norm, for `g11 in L4`,

```text
||R_eta||_L2 <= |eta|^2 ||g11||_L4^2.
```

If `P_K` is the existing orthogonal Fourier truncation to spatial physical wavenumbers `|k|<=K`, then

```text
||P_K R_eta||_L2 <= |eta|^2 ||g11||_L4^2,
||d_x P_K R_eta||_L2 <= K |eta|^2 ||g11||_L4^2.
```

These are **fixed-spatial-resolution bounds on the eta-tangent remainder**, not timestep or clock-grid derivative error bounds. They hold without a globally smooth second derivative of `f`, are uniform across arbitrary gradient-zero crossings, and preserve the exact frozen Stage E H3/H4 flux factors and source signs.

## The important limitation

Although `f` is C1 with Lipschitz first derivative, `f''` jumps in sign at `g=0`; the **eta-tangent flux** `2|g10|g11` is in general only Lipschitz across a simple zero of `g10` when `g11 != 0`. Its spatial derivative can jump. Thus it would be mathematically **wrong to promote a standard C9 / M9 FD8 Taylor remainder bound for the Y scalar row merely from this lemma**. The Fourier-projected derivative is a well-defined fixed-mode quantity, but control of actual physical time derivatives, parent trajectories, projector dependence and original FD8 clock truncation remains a separate pre-registered G3 obligation.

For the *direct* H4 source-Ward, which reads only the identically zero Y shift/isotropic/anisotropy rows, the zero-support lemma already removes any need for a Y flux M9 bound at this specific projection. If the flux contributes indirectly to the actual H4 dynamics or parent/metric reconstruction, it must be bounded **there**, with the appropriate lower-regularity or weak-norm method and without hiding discontinuities.

## Relation to current project status

The actual GE06+GE07+Lambda production `Cmat` 16/16 *continuum linear* syzygy is now a locally executed source-bound analytic PASS, recorded separately in `docs/ge19_actual_cmat_16jet_operator_ward_pass_2026-11-07.md`. This lemma makes **no change** to the remaining G1 (continuous action-parent Euler and lower boundary) or G3 (independent FD4/FD8 physical derivative/roundoff) gates, the original frozen D12R3 predata, or any H4 science classification.

Historical D12R9C/D audits were reported to have identified insufficient C5/C9 parent regularity; their original reports were not independently re-read for this lemma. No a posteriori B_total is defined.

**Unchanged:** `full_H4_Ward_certified=false`; `Z21_certified=false`; `lensing_licensed=false`. No observation tuning; original `H4_active_shift_Nt128_Linf <= 1e-6` and original temporal order `>=2.5` untouched.
