# GE19 G1 — direct physical Z11 / GE05 forcing-error propagation theorem

**Date:** 2026-11-08. **Branch:** `physics-first-gravitational-elasticity`.  
**Classification:** `GE19_G1_Z11_GE05_SOURCE_ERROR_TRANSPORT_EXACT_ANALYTIC_BOUND_CONTINUOUS_EULER_CERTIFICATION_OPEN`.

## Provenance: missing D47 m20 is only an unavailable historical artifact

The user executed a recursive local `find results -type f -iname '*r5g8*m20*n256*json' -print` and **obtained no path**. The frozen source-verified G1 report (2026-11-08) had five original R5g8 continuous-H1 certs m=3,5,8,10,15, with all checked classifications and D17 provenance matching. **The sixth m20 file is missing across this searched local `results` tree**. This is not a failed numerical integration, and does NOT permit fabricated or reconstructed certification. The D47 original-action continuum H1 proof still has only the accessible five-mode local scope. No immediate expensive R5g8 rerun is justified while Z11/GE05 continuous Euler and H4 cohort/source mapping remain open.

## Source-exact Z11 memory forcing

The original source `ge19/repair32b_factor2_corrected_reduced_h2_z11_reconstruction.py`, pinned original Git blob `6ece578e8a30f48faaded8808687a9bd5c114608`, explicitly defines:

```python
RAW_RESIDUAL_DICTIONARY_SCALE = 2.0

rhs[im,2] = RAW_RESIDUAL_DICTIONARY_SCALE*0.5*Q*a**3*B10[im]
rhs[im,3] = RAW_RESIDUAL_DICTIONARY_SCALE*(-0.5)*a**2*(1j*k)*B10[im]
```

The factor two is from the original Repair32A signed GE05-to-GE06 raw-Euler dictionary, not an adjustable calibration. Consequently, in each original Fourier mode `k`, with frozen real positive background `a(x)` and real `Q(x)`, the actual *two-component driven raw Euler RHS* is exactly

```text
s11(B) = (a^3 Q B, - i k a^2 B)   # driven rows aether, scalar
```

and all four other raw main Euler source rows are identically zero in the Repair32B forcing. For **the same exact background** and any two memory-source histories `B_exact`, `B_approx`,

```text
|| s11(B_exact) - s11(B_approx) ||_2
   = a^2 * sqrt((a*Q)^2 + k^2) * |B_exact - B_approx|.
```

This is an **equality** in the Euclidean norm of exactly these two raw-Euler rows, no hidden Lipschitz constant and no numerical finite difference. For the original six positive modes, setting `k_max` to the maximum physical Fourier wavenumber and summing squared norm over modes,

```text
||delta s11||_{l2(mode,driven row)}
 <= [a^2 sqrt((a Q)^2 + k_max^2)] ||delta B10||_{l2(mode)} .
```

On an interval `I`, define `L_B = sup_{x in I} a^2 sqrt((a Q)^2+k_max^2)`, using a rigorously enclosed **Repair13 action background**. Then `sup_I ||delta s11|| <= L_B sup_I ||delta B10||`.

If the background is also reconstructed with error, the identity **cannot** be used without additional terms: for `s_u=a^3 Q B` and `s_phi=-ik a^2 B`, valid decompositions include

```text
|delta s_u| <= |a^3 Q| |delta B|
                + |delta(a^3 Q)| |B_approx|,
|delta s_phi| <= |k| a^2 |delta B|
                  + |k| |delta(a^2)| |B_approx|.
```

Use an independently certified background envelope before applying these to the H4 cohort; do not quietly set `delta a` or `delta Q` to zero for interpolated-vs-action backgrounds.

## Conditional original-action variation-of-constants enclosure for Z11

Original Repair32B reconstructs and propagates a reduced canonical 8D state using frozen Repair07 `_initial_canonical_state`, `_canonical_operator_matrices` and `_radau2_integrate_canonical`, with a **PCHIP-interpolated** frozen M1 raw source at off-grid points:

```text
y=(S,u,phi,T,pS,pu,pphi,pT)
y_x=M(x)y+G(x)s11(x)             # effective reduced canonical coefficients
```

Here `G` denotes the genuine canonical source-map derived from the original `F` matrix, including the correct raw source order and any algebraic rows; it must NOT be assumed equal to the identity. Denote the true action-coefficient IVP by `y_*(x)` with physical memory source `s_*(x)`. For a fixed, explicitly defined piecewise-smooth numerical representation `y_h(x)`, its *actual action residual* is

```text
r_h(x) = y_h'(x) - M(x)y_h(x) - G(x)s_h(x).
```

On an interval where `M,G` are well-defined and the system is unique, with `e=y_*-y_h`,

```text
e' = M e + G(s_*-s_h) - r_h .
```

Let `L(x)` be an **independently enclosed induced operator norm** of `M(x)`, `g(x)` a bound of `||G(x)||`, `eps_r(x)>=||r_h(x)||` and `eps_B(x)>=|B_*(x)-B_h(x)|`. An explicit a priori Grönwall majorant is

```text
||e(x)|| <= exp(INT_{x0}^x L)
    * [ ||e(x0)|| + INT_{x0}^x
        (eps_r(s) + g(s) a(s)^2 sqrt((a(s)Q(s))^2+k^2) eps_B(s)) ds ] .
```

This bound is **analytically correct but conditional**: every `L,g,eps_r,eps_B`, endpoint uncertainty and source representation must be independently proved as a continuous interval enclosure. It is NOT a PASS because the formula exists. Replacing `eps_r` by a midpoint/sample global-L2 residual, or `eps_B` by a difference of two surrogate X10 interpolants, is invalid.

### Required algebraic first-order Euler rows

The canonical 8D ODE is not the whole covariant Euler system. Frozen Repair07 uses `WY,WR` to reconstruct algebraic lapse/dust-density and `r7.linear_operator_batch` returns the original signed main and constraint rows. A **complete G1** must also enclose algebraic reconstruction and *all first-order Euler components entering H4F3D4*, including shift and independent longitudinal projection in original Ward dictionary. A small reduced ODE defect is insufficient if an eliminated algebraic or constraint row remains unbounded.

Likewise, Z11's original PCHIP forcing and the q10 bath were constructed from earlier frozen Repair26/Repair27/Repair28, whereas the D55 original GE05 continuous-on-shell certificate has a **separate stated numerical scope**. It needs source-normalization, bath quadrature and full H4 cohort/interval traceability, not merely matching output JSON flags.

## Physical next computation (G1; not another G1B/G1C ancestry comparison)

1. Identify the **exact reconstructed Z11 numerical representation actually consumed by H4F3B**, from original Repair32B `Z11` and `Z11dot`, for all original C_min/C_star/C_max and Nt128/Nt64, mode set `m=3,5,8,10,15,20`.
2. Construct **a priori physical action coefficient intervals** for `M(x)`, source map `G(x)`, original Repair13 `a,H,Q`, and the true GE05 memory drive. Respect mode/clock and q-node coupling; do not fit source errors to H4 Ward cancellation. Test the *actual interval supremum* of the full original-action Z11 Euler residual and all required constraint components, not only a collocation or Hermite proxy at sampled times. Allow domain partition / interval arithmetic if coarse bounds are too conservative.
3. Use the exact source-row Lipschitz factor above to transport **independently bounded** GE05 `delta B10` into driven Z11 source uncertainty. Propagate with the actual canonical `M,G` stability bound and then the original algebraic reconstruction map. Include all cohort/mode/parent-boundary Fourier products.
4. Only if all continuous H1 + Z11 + GE05 + boundary envelopes close, freeze G1; then finish the previously preregistered D12R3 / D9 M5/M9/roundoff `B_total`; then one common-grid complete H4 Ward. Do not solve Z21 or open lensing as a new physics claim before the original gates.

This is a **physics-first interval-error theorem and numerical program specification**, not another claim that original parent certificates extended beyond their declared physical scope. Existing G1B, G1C2 and exact-rational X10 Hermite representation proof remain valid in their own scope; do not repeat them.

**Locked flags:** `G1_PHYSICAL_CLOSED=false`, `G3_B_TOTAL_FROZEN=false`, `FULL_H4_WARD_CERTIFIED=false`, `Z21_CERTIFIED=false`, `LENSING_LICENSED=false`. Source-weight, factor-two dictionary, old failures, original active shift `<=1e-6` and temporal order `>=2.5` unchanged.
