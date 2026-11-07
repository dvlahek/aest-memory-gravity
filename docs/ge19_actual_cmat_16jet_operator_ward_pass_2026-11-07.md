# GE19 — actual production Cmat 16/16 source-bound analytic Ward PASS (2026-11-07)

**Classification:** `GE19_ACTUAL_FROZEN_CMAT_16JET_EXACT_WARD_SYZYGY_PASS_H4_OPEN`  
**Source:** user-executed `ge19/h4f3d_actual_cmat_16jet_source_bound_analytic.py`, on `physics-first-gravitational-elasticity`.  
**Local output evidence:**
- `results/ge19_h4f3d_actual_cmat_16jet_20261107.json` — SHA-256 **`ad61f5b9ce326fdd8ec6991274c8737ec26b40f6178f60200ad70a9e603c00ed`**, size 4,954 bytes
- `results/ge19_h4f3d_actual_cmat_16jet_20261107.log` — SHA-256 **`7d7d56f18340931298f7b0755022d66545dc65bbcabaef03fe4baddf9dff2d3f`**, size 1,423 bytes.

The researcher supplied both files; their local hashes, classification, 16/16 exact zeros, 6/6 immutable source blobs, 15/15 source-row/background bindings and three FALSE science flags were independently checked against these bytes. These *local data files* are not represented as GitHub Actions or as committed artifacts.

## What has now actually closed

The frozen source-derived linear Euler operator is built from the original GE06 + GE07 + Lambda rows (NOT manufactured test matrices), and the original 16x10 Cmat storage conventions:

```
w = (N,drho,S,u,phi,T,Sdot,udot,phidot,Tdot)
B = C10 + C11
P = C14
J = [C6 + 2(C12+C13)] / 3
E_b = B w
E_L = J w - d_t(Pw)
D_W(E) = -d_t E_b - i k a E_L.
```

The 16 independent *integrable temporal jet* coefficients of
`D_W(L_total(w))` all vanish exactly upon polynomial elimination by the original Repair13 Friedmann constraint, using the exact Repair13 analytic background derivatives:

```
dot(a)=a H,
dot(H)=-(Q K_Q + 3 C/a^3)/2,
dot(Q)=-3 H K_Q/K_QQ,
H^2 = (Q K_Q-K)/3 + C/a^3 + rho_L.
```

The exact number of conditions is 16: six amplitude coefficients; two independent first derivatives of N and dust density; four second derivatives of S,u,phi,T; four combined first derivatives of those same dynamical variables. `P=C14` is retained **inside the time derivative**, rather than treating the longitudinal momentum as a static row. The original GE07 dust background lapse Euler coefficient cancels GE06+Lambda **only after combining the action sectors**. No physical source terms or coefficients were tuned.

**Conclusion in narrow logical scope:** the original source-bound *continuum* GE06+GE07+Lambda linear canonical Euler operator satisfies its first-order spatial Noether/Ward syzygy for arbitrary sufficiently regular admissible time jets on an exact Repair13 background. This is a genuine analytic subproof of G2 and supersedes the earlier status `ACTUAL_CMAT_16_COEFFICIENTS_OPEN`; older formal/manufactured and sector proofs remain valid precursors, not redundancies.

## What this PASS does not establish

This test did NOT evaluate any original H4F3B physical-source/parent/boundary arrays, actual physical-grid `FD4` or `FD8` Ward truncation, an all-cohort H4 Ward defect or its preregistered `B_total`, or a new Z21 solve. The continuum operator syzygy is **not a discrete finite-difference identity**, and valid symbolic background derivatives are not a bound on PCHIP/Radau sampled-parent interpolation errors.

In particular:

```text
full_H4_Ward_certified = false
Z21_certified = false
lensing_licensed = false
B_total_defined = false
```

Historical Repair37/Cr12ac/D22A science FAILs, the original `H4_active_shift_Nt128_Linf <= 1e-6` gate and temporal-order `>=2.5` remain unchanged.

## Next science task: G1 and G3, not a new operator replay

The existing H4F3D4 *formal* mixed identity, combined with D12R2 eliminating background unknown-state terms, leaves the lower-parent Ward remainder

```text
P_lower =
  2 SUM_i[E_i10 d_x F_i11 + E_i11 d_x F_i10]
 +4 SUM_j E_qj10,GE05 d_x q_j10
 -d_x[2L10 E_L11 + 2L11 E_L10 -2b10 E_b11 -2b11 E_b10].
```

On an **exact all-sector H1/Z11/GE05 first-order solution**, all on-shell first-order Euler residuals vanish, including corresponding L/b rows, so `P_lower=0` as a formal continuum statement. That is a *conditional implication*, not certification that discrete archived parent arrays satisfy it on the original physical grids or all relevant time intervals. H3F `Z20` and H3G `q20` feed the actual H4 source and must not be discarded.

**The actual outstanding physical gate is therefore:**

1. **G1 (parent quality):** show independently controlled, original-action Euler residuals and signed lower-boundary terms for the fixed H1/Z11/GE05 parents on the correct physical time windows, including continuum/interpolation defects. Do not infer an all-interval C5/C9 bound from sampled nodes. D55 GE05 on-shell PASS is scoped and cannot unconditionally be extended to all H4 cohorts.
2. **G3 (budget):** derive preregistered physical FD4/FD8 derivative and roundoff envelopes on those validated parent trajectories, handle any Y zero-gradient regularity along its actual entry routes, and define `B_total` **before observing an integrated full-H4 Ward defect**.
3. Once G1+G3 PASS, execute **one** real common-grid all-sector H4 Ward including all six sources and all parent/boundary terms. Only after its physical PASS is a new action-completed Z21 solve licensed.

Local D12R9B/C/D resource/provenance investigations have been reported earlier but **were not re-inspected from their exact user-local files in this result**. Earlier reported results indicate that candidate derivative formulas were found but rigorous M5/M9 suprema and whole-interval parent regularity remained open. They must not be silently marked PASS or replaced by a posteriori fit.

Use `docs/CURRENT_GE19_STATUS.md` as the living overview; preserve this note as a dated source-backed PASS.
