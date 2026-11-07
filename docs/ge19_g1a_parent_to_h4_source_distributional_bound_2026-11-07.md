# GE19 G1A — parent-residual control of the H4 source Ward compatibility (analytic lemma)

Date: 2026-11-07  
Branch: `physics-first-gravitational-elasticity`  
**Classification:** `GE19_G1A_CONTINUUM_PARENT_TO_H4_SOURCE_WARD_BOUND_DERIVED_PHYSICAL_PARENT_ENCLOSURES_OPEN`

This is a **new exact mathematical consequence**, not a new solver, numerical H4 Ward PASS, FD4/FD8 budget, Z21 science certificate or alternative interpretation of old FAIL runs. It reuses the frozen original source/noether identities and the **user-executed 16/16 actual Cmat continuum syzygy PASS** from `docs/ge19_actual_cmat_16jet_operator_ward_pass_2026-11-07.md`.

## 1. Premises, geometry, and immutable inputs

- Exact mixed Noether coefficient: `ge19/h4f3d4_complete_eta_regularized_mixed_ward_ledger.py` (Git blob `87d8be9ec44ecb099feecbaf59a904bd989da2fb`), including bath coefficient **4** from physical eta rescaling.
- Exact homogeneous background Euler elimination: D12R2, `ge19/h4f3d12r2_exact_background_onshell_elimination.py` (blob `df5d0b384747edefaab2878e1a9fe6d174d2da29`).
- Actual GE06+GE07+Lambda canonical linear Euler syzygy: `ge19/h4f3d_actual_cmat_16jet_source_bound_analytic.py` (local result: 16/16 exact Repair13-on-shell coefficients, `GE19_ACTUAL_FROZEN_CMAT_16JET_EXACT_WARD_SYZYGY_PASS_H4_OPEN`).
- Lossless **sample** archive of eight lower nonbath parent pieces and two longitudinal/shift boundary crosses: `ge19/h4f3d10r1_lossless_known_parent_boundary_assembly.py` (blob `d4f67adc2c9267cd3e4fd0e6dd1358c2c97a8545`).
- Frozen H4F3B signed six-source and Stage E corrected-Y model remain unchanged. D12R3 original preregistration and original H4 shift `<=1e-6` remain unchanged.
- Let `t` denote **physical time**, and `chi` denote the **periodic spatial coordinate** (do not confuse `chi` with the actual numerical clock coordinate `xi=ln(a)`).

All equalities below are at continuum-action level in distributional sense, for compatible physical parents and fields with enough regularity to define the indicated products. The GE05 bath node sum must be convergent/controlled under its frozen positive Drude realization; never silently replace the finite/continuum bath with an unrelated coupling.

## 2. Collapse of unknown Z21 from the full H4 Ward

After D12R2 background on-shell elimination, the signed mixed Ward is

```text
0 = D_W(E21) + R_parent - d_chi B_parent,
D_W(E) = -d_t E_b - d_chi(a E_L),
E21 = L_total(F21) - S21.
```

Here `R_parent` and `B_parent` are EXACTLY the H4F3D4 lower-parent objects (no omitted GE05 and no source fitting):

```text
R_parent =
  2 SUM_i [E_i10 d_chi F_i11 + E_i11 d_chi F_i10]
  +4 SUM_j E_qj10,GE05 d_chi q_j10

B_parent =
  2 F_L10 E_L11 + 2 F_L11 E_L10
 -2 F_b10 E_b11 - 2 F_b11 E_b10
```

where `i` ranges across `{N,L,R,b,u,phi,T,rho}`. The first-order parent Euler coefficients `E_i10,E_i11,E_qj10` use the actual signed GE19 Euler convention. In particular no direct `E_i20 dF01` appears because the homogeneous background is eta-independent.

The source Euler projection is `S_L=(S_iso+2*S_aniso)/3`; the signed source-side Ward is

```text
W_source = d_t S_b + d_chi(a S_L).
```

The now-verified continuum canonical operator syzygy `D_W(L_total F21)=0` for arbitrary admissible integrable perturbative jets implies the **exact reduced compatibility condition**

```text
W_source + R_parent - d_chi B_parent = 0.
```

**No numerical or analytic solution for F21/Z21 is required to derive this identity.** On exact common first-order parent Euler solutions, `R_parent=B_parent=0`, giving `W_source=0` as a continuum *compatibility consequence*. That does not prove the sampled H4F3B right-hand side or its numerical FD derivatives satisfy the physical identity.

## 3. A priori parent-error inequality without M5/M9

At fixed physical time, let `Pi_K` be the **continuous orthogonal Fourier projection** on spatial modes `|k|<=K` (K is physical wavenumber, not integer mode ID). Then

```text
W_source = - R_parent + d_chi B_parent
```

implies, in spatial L2,

```text
||Pi_K W_source||_2
  <= ||R_parent||_2 + K ||B_parent||_2.
```

For finite `Linf_chi` amplitudes and exact L2 Euler residuals:

```text
||R_parent||_2 <=
  2 SUM_i [ ||E_i10||_2 ||d_chi F_i11||_infty
           +||E_i11||_2 ||d_chi F_i10||_infty ]
  +4 SUM_j ||E_qj10||_2 ||d_chi q_j10||_infty

||B_parent||_2 <=
  2[ ||F_L10||_infty ||E_L11||_2
    +||F_L11||_infty ||E_L10||_2
    +||F_b10||_infty ||E_b11||_2
    +||F_b11||_infty ||E_b10||_2 ].
```

Combining yields a fully explicit **coefficient-one conservative projected source-Ward error majorant** in terms of physical, *first-order* parent Euler residuals and finite spatial field/gradient amplitudes. For the continuous-in-time claim take e.g. L2 in time on both sides and impose independent L∞_time bounds on the field/gradient multipliers and L2_time L2_space bounds on Euler residuals. Equivalently the distributional identity can be tested against compactly time-supported smooth functions, avoiding pointwise temporal differentiability of the projected source.

This majorant does not require separately bounding `d_t^5 S_b` or `d_t^9 S_b` **for the mathematical continuum compatibility statement**. It also needs no Y flux C9 assumption in the direct source Ward because the Stage E Y shift/isotropic/anisotropy rows are identically zero.

## 4. Distributional / weak Ward formulation

Define

```text
J_t = S_b,
J_chi = a S_L - B_parent.
```

Then in distributions,

```text
d_t J_t + d_chi J_chi + R_parent = 0.
```

For every smooth test function `psi(t,chi)`, periodic in `chi` and compactly supported inside the time interval,

```text
-INT J_t d_t psi dt dchi
-INT J_chi d_chi psi dt dchi
+INT R_parent psi dt dchi = 0.
```

No time-boundary contributions appear only because the test is compactly time-supported. For full-time tests, the physical temporal boundary term `[INT J_t psi dchi]_{t_i}^{t_f}` is mandatory. This is a **distributional identity derived from the action**, not a new replacement numerical tolerance. A legitimate weak-form test would require separately frozen quadrature/reconstruction bounds, function-space assumptions, and finite-bath remainder bounds.

## 5. Exact place where G1 must now supply physics

D12R9B/C/D prior audits (discussed in earlier project conversations, reports not directly re-opened in this checkpoint) identified three logically distinct obstacles:

1. D17 / original-action H1 **continuous first-order Euler residual** and interval stability/integrator enclosure, not just time-node residuals. Some D47/D55 PASSes apply only to declared trajectories/cohorts.
2. Z11 corrected-parent independent continuous Euler residual and inherited temporal interpolation/integration defect; PCHIP + `solve_ivp(t_eval)` sampling is not an interval certificate. The Z11 `E_i11` terms cannot be omitted from the bulk or boundary.
3. GE05 q10 each bath node: consistent eta-normalized Euler residual and controlled sum/integral `4 SUM_j E_qj10 d_chi q_j10`, including the full relevant H4 cohort. D55 first-order GE05 on-shell PASS cannot automatically be extrapolated beyond its certified scope.

Existing H3F Z20 and H3G q20 are **not directly present in the lower-parent product**: they enter the genuine H4F3B source (e.g. GE05 M1). Thus source compatibility is not a license to drop those previously certified higher parents.

Spatial derivatives `d_chi F` and `d_chi q` can be bounded independently from suitable certified Fourier coefficient envelopes. **Important:** D10R1 lossless reconstruction of the *128 sampled spatial nodes* is **not by itself** a proof of alias-free continuous Fourier products above Nyquist; spatial de-aliasing or projection-error control must be separately established if a continuum Pi_K estimate is claimed from discrete data.

## 6. What this does and does not change in the frozen gate structure

**Derived / narrowed:**
- Unknown F21 disappears *from the exact continuum source compatibility condition*, due to the actually proved continuum 16/16 canonical operator syzygy.
- A complete first-order parent Euler residual envelope, with original spatial mode/gradient control, would yield a priori explicit continuum source-Ward compatibility bounds **without a separate source M9 bound** for this mathematical result.
- The unambiguously necessary missing evidence is now the physical continuous parent Euler enclosure for common H1/Z11/GE05 cohorts and source-reconstruction error control.

**Not closed:**
- Original D9/D12R3 **FD4/FD8 pointwise** full-Ward numerical budget; its M5/M9, roundoff and Y regularity tasks cannot be silently deleted from immutable preregistration.
- Physical all-cohort H4 source-array reconstruction, parent/boundary, sampling/aliasing, time interpolation or full integrated-grid error.
- Original `H4_active_shift_Nt128_Linf <=1e-6` and temporal order `>=2.5` gates, original negative science runs, and the final Z21/lensing license.

**Scientific decision:** Work G1 first on a **common, independently certified continuous first-order parent residual envelope** for D17/R5g H1, Z11 and frozen GE05 bath. Only after that decide transparently whether to complete the original D9 strong FD4/FD8 route or to *separately preregister* an independent weak-form structural theorem/test; neither is a retrospective redefinition of the original H4 science gate.

```text
G1A_CONTINUUM_PARENT_TO_SOURCE_BOUND = DERIVED (conditional)
G1_PHYSICAL_PARENT_INTERVAL_ENCLOSURES = OPEN
G3_ORIGINAL_D9_B_TOTAL = OPEN
FULL_H4_WARD_CERTIFIED = false
Z21_CERTIFIED = false
LENSING_LICENSED = false
```

No numerical H4 Ward defect or observational data were used, no source or threshold coefficients changed.
