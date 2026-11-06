# GE19 — integrated H4 Ward gap map (2026-11-06)

Status: **ANALYTIC INVENTORY / NO NEW SCIENCE CERTIFICATION**  
Branch: `physics-first-gravitational-elasticity`  
Canonical navigational checkpoint: `docs/CURRENT_GE19_STATUS.md`.

## Purpose

Stop the accumulation of exploratory single-mode numerical replays and identify the *precise outstanding proof obligations* before an action-completed `Z21` science solve. This is a source-bound integration map, not a new physical Ward or lensing result. It retains original historical failures and thresholds unchanged.

## What is already proven or prepared

1. **Action and physics:** frozen covariant NL0B (positive Drude/Maxwell elastic memory), NL0C corrected nonanalytic Y, actual GE06/GE07/Lambda/dust sectors. See `docs/gravitational_elasticity_canonical_nl0b_interpretation.md` and `docs/gravitational_maxwell_viscoelasticity.md`. No new action is required.
2. **Actual H4 sources:** `ge19/h4f3b_actual_corrected_six_piece_source.py`; certified corrected H3F `Z20`, H3G `q20`, H1 and Z11 parents, and six original signed source families. H4F3B is a source-only PASS.
3. **Formal action-level Ward:** `ge19/h4f3d4_complete_eta_regularized_mixed_ward_ledger.py` derives exact mixed `d_eta d_epsilon^2` off-shell identity, including the original `E_L=(E_iso+2E_aniso)/3` and exact GE05-to-GE06 eta-bath factor. **This formal identity does not certify actual-grid residuals.**
4. **Canonical linear operator:** `ge19/h4f3d1_frozen_canonical_operator_ward.py` specifies original 16x10 Euler Cmat rows, spatial projection and physical-time FD4 derivative of **entire** `Cmat*w` products. It is a compiler/manufactured-test PASS, not an independently closed physical operator Ward on the corrected actual grids.
5. **Lower nonbath parent archive:** `ge19/h4f3d10r1_lossless_known_parent_boundary_assembly.py` preserves full-Nyquist first-order products and the two L/shift boundary crosses; exact archiving does not prove that physical first-order Euler residuals vanish.
6. **Known unknown-state obstruction eliminated:** `ge19/h4f3d12r2_exact_background_onshell_elimination.py` proves background `E_i00=0` under the frozen Repair13 homogeneous equations and eliminates `E_i00*d_x F_i21` and `L21*E_L00-b21*E_b00` **for arbitrary mixed-H4 states**, without assigning those states. This is a real on-shell symbolic PASS.
7. **FD schemes:** `ge19/h4f3d9_exact_original_fd4_fd8_stencil_budget_compiler.py` and `docs/ge19_h4f3d9_original_fd4_fd8_stencil_budget_compiler_valid_freeze.md` establish exact original stencil coefficients and conditional Taylor constants, **not** physical M5/M9 regularity bounds. `ge19/h4f3d12r3_full_ward_numerical_budget_prelock.py` records that the total physical error budget remains unlicensed.

## The already-derived identity in source-bound notation

Use a physical-time and spatial-coordinate convention identical to the frozen GE19 action:
`F_i = F_i00 + eps(F_i10+eta F_i11) + eps^2(F_i20+eta F_i21)/2 + ...`, with analogous Euler coefficients. For nonbath `i in {N,L,R,b,u,phi,T,rho}`, the D4 mixed Ward identity is

```text
W21 =
    SUM_i [ E_i00 * d_x F_i21
           +2 E_i10 * d_x F_i11
           +2 E_i11 * d_x F_i10 ]
  + 4 SUM_j (E_qj10,GE05 * d_x q_j10)
  - d_x [ a E_L21
          +L21 E_L00 +2 L10 E_L11 +2 L11 E_L10
          -b21 E_b00 -2 b10 E_b11 -2 b11 E_b10 ]
  - d_t E_b21
= 0.
```

The `4 SUM_j E_qj10 d_x q_j10` term is the **physical eta-regularized bath** contribution (D3/D4). A naive integer-eta bath expansion is incorrect; the normalization is not adjustable.

D12R2 removes **only the exact background-multiplied unknown-state terms**. The remaining lower-parent term is therefore

```text
P_lower =
    2 SUM_i [ E_i10 * d_x F_i11 + E_i11 * d_x F_i10 ]
  + 4 SUM_j E_qj10,GE05 * d_x q_j10
  - d_x [ 2 L10 E_L11 +2 L11 E_L10
          -2 b10 E_b11 -2 b11 E_b10 ].
```

Keep all of these terms, with actual signed Euler row conventions and boundary conditions, until verified on the correct physical parents. D55 primary/C-star GE05 bath on-shell certification is **not automatically** a certification of the all-cohort H4 parent product.

For `E21 = L[F21] - S21` and six fixed H4 source pieces `p`, the full identity is

```text
W_total = W_operator + SUM_p W_source,p + P_lower = 0.
```

In the original GE19 Fourier row convention, D1 defines the operator term as

```text
E_b^lin = [Cmat10 + Cmat11] w
E_L^lin = { [Cmat6 + 2(Cmat12+Cmat13)] w }/3
          - H * D4_x([Cmat14]w)
W_operator = - H * D4_x(E_b^lin) - i*k*a*E_L^lin.
```

With exact frozen support and source signs, H4F2h provides

```text
W_source,p = H * D_p,x(S_b,p)
             + i*k*a*(S_iso,p + 2*S_aniso,p)/3.
```

Use `D_p=FD8` for GE06/GE07/Lambda and the Y source, `D_p=FD4` for GE05 M1/M2. The action-completed Y shift/isotropic/anisotropy rows are zero, so its projected source-Ward contribution vanishes *in this source projection only*. Do not assert each source-Ward contribution or their sum must separately vanish.

**Key conceptual distinction:** a symbolic continuum Noether identity, a numerical FD4/FD8 approximation to its terms, and the original `Z21` shift constraint are **three different assertions**. A very small V10 source-Ward or V11 split shift residue is not a substitute for the actual parent/boundary/operator balance.

## Precisely unresolved integration obligations

| ID | Missing evidence or proof | Existing partial prerequisite | Stop condition |
| --- | --- | --- | --- |
| G1 | Instantiate and independently verify the on-shell/controlled off-shell `E_i10,E_i11` and `E_qj10` *in the same action normalization and common corrected grids*, including dust, GE05 per-node variables and corrected Y parents | D2/D3/D4 formal; D10R1 lossless known-parent archive; D55 locked first-order bath; H3F/H3G | Unknown physical Euler residual or provenance => `H4F3D_UNRESOLVED` |
| G2 | Establish the physical operator Ward and the **complete signed** nonbath/bath lower-boundary combination using those actual parent arrays; any continuum cancellation of a trial `F21` must be derived rather than inferred from a single manufactured field | D1 original Cmat formula, D4 exact template, D12R2 background elimination, H4F3B six-source data | Source-only cancellation or missing operator/boundary term => not a full Ward PASS |
| G3 | Freeze, *before examining total physical Ward defect*, independent FD4/FD8 physical derivative envelopes (M5/M9 or justified lower-regularity alternative at Y zero set), R1 piecewise interval regularity, signed parent/boundary truncation and roundoff propagation; define a defensible structural `B_total` | D9 exact stencil constants, D12R3 prelock | No certified budget => `full_Ward_execution_licensed=false` |
| G4 | Perform one **integrated**, predeclared all-cohort actual-grid H4 source + operator + all-parent + boundary audit, using the original fixed source/parent hashes and registered hotspot/full active window | G1–G3, H4F3B and D12R2 | PASS licenses only a separate Z21 solve, not immediate lensing |

The 2026-10-10 canonical status and D12R3 prelock do not establish that G1–G3 have since closed. Locally reported D12R9 provenance/regularity work must be inspected in its *actual* frozen files before any upgraded claim; unavailable evidence is not an implicit PASS.

## Research decision

**Do not run V12/V13 single-mode replay or a new candidate Z21 solve now.** The next work is the exact G1/G2 parent/operator/boundary instantiation and G3 physical pre-residual numerical budget, reusing the current frozen derivations. No action rewrite, no fitted RHS factor, no observational tuning, and no change to `H4_active_shift_Nt128_Linf <= 1e-6` (nor original temporal order >=2.5).

Once G1–G3 are independently verified: one preregistered actual common-grid H4 Ward test. If it PASSes: one new action-completed Z21 certification. Only then: gauge-invariant weakly nonlinear Weyl/null-geodesic lensing.

## Local diagnostic context — not a science gate

V9–V11 (2026-11-06) verified a targeted m=5 replay and near-antiparallel signed split-source/shift residuals under a single frozen **full-memory** linear operator. This is expected linear superposition, not an independent memory-free comparison or a full H4 action Noether proof. Large ~1e11 aether coefficient `u` also requires perturbative scaling checks before physical interpretation.

**Frozen classifications unchanged:** `full_H4_Ward_certified=false`, `Z21_certified=false`, `lensing_licensed=false`.
