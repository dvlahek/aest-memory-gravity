# GE19 — formal linear Ward syzygy and direct Y-source support lemma

Date: 2026-11-06  
Classification: **GE19_H4_FORMAL_OPERATOR_SYZYGY_AND_Y_SUPPORT_SCOPE_DERIVED_FULL_ACTUAL_WARD_OPEN**  
Branch: `physics-first-gravitational-elasticity`  
Evidence: `ge19/h4f3d_ward_syzygy_y_support_scope_analytic.py`; frozen H4F3D4 mixed Ward ledger, D12R2 exact background, H4F3D1 canonical operator and Stage E source generator.

**Scope:** New compact *analytic consequence* of already derived covariant Ward and the exact support of the existing corrected Y action source. This is not a new H4 source, not a physical Cmat syzygy certification, not a physical FD4/FD8 budget, and not Z21 or lensing certification. It must not relabel or supersede earlier physical FAILs.

## 1. Conditional linear operator syzygy: no Z21 needed

The exact reduced longitudinal spatial Noether identity fixed by H4F2B/H4F3D4 is

```text
W = SUM_i E_i * d_x F_i - d_x(L*E_L - b*E_b) - d_t E_b = 0,
```

with the physical bath's eta-regularized contribution appearing only in the higher-order mixed coefficient relevant to H4. For an arbitrary first-order field displacement `f_i`, around homogeneous `N0=1, L0=R0=a(t), b0=0`, differentiation in epsilon yields

```text
W10 =
  SUM_i E_i00 * d_x f_i10
  - d_x[a E_L10 + f_L10 E_L00 - f_b10 E_b00]
  - d_t E_b10 = 0.
```

D12R2 proved the exact homogeneous background equations set **all relevant E_i00=0**. Hence

```text
      -d_t E_b10 - a d_x E_L10 = 0
```

for **arbitrary** first-order perturbation fields if `E10` is the linear Euler derivative of the **same full covariant action**. With frozen GE19 row projection `E_L=(E_iso+2E_aniso)/3`, this is a continuum linear differential-operator syzygy

```text
D_W * L_total = 0,
D_W(E) = -d_t E_b - (a/3)*d_x(E_iso+2*E_aniso).
```

This is **an action-level conditional identity**, not a claim that the H4F3D1 finite-dimensional `Cmat` implementation has now been independently proven to satisfy it on every original grid or at discrete precision. That remaining source-bound operator audit is a clearly isolated part of G2. There is no need to run an exploratory `Z21` solve merely to derive the continuum syzygy.

## 2. Implication for actual H4 source compatibility

H4F3D4 already derived the mixed identity, including

```text
P_lower =
  2 SUM_i (E_i10 d_x F_i11 + E_i11 d_x F_i10)
  + 4 SUM_j E_qj10,GE05 d_x q_j10
  - d_x[2 L10 E_L11+2 L11 E_L10
        -2 b10 E_b11-2 b11 E_b10].
```

The `4` factor follows the physical `U=sqrt(eta)*q` bath convention and GE05/GE06 action normalization, and must not be modified.

Using `E21 = L_total F21 - S21`, linearity of the signed `D_W` projection gives

```text
W21 = D_W(L_total F21) - D_W(S21) + P_lower = 0.
```

**Important sign convention:** `D_W` above is defined with *minus* derivatives on Euler rows, whereas the H4F2H source-Ward helper reports `W_source = -D_W(S21)` with **plus** derivative signs. Therefore in H4F3D4's reporting notation,

```text
W21 = W_operator + W_six_source + P_lower.
```

If the continuum action-level syzygy `D_W L_total=0` holds for the actual implementation and the lower parents are on shell, source compatibility follows without requiring a solved `Z21`. **None of these physical on-shell/implementation hypotheses is promoted by this note.** H3F Z20/H3G q20 enter S21 through the actual M1 and other nonlinear sources; they do **not** appear as independent direct `E20 F01` products in P_lower on an eta-independent FLRW background.

## 3. Exact direct Stage E H4 Y-source Ward support lemma

The frozen `ge19/h4_stagee_versioned_y_source_rows.py` computes `source_h4` through `_rhs` with

```text
main = zeros((6,nt,nx))
constraints = zeros((2,nt,nx))
main[u]   = 2 a^3 Q kappa (projected flux)
main[phi] = -2 a^2 kappa (spatial flux derivative)
```

No other rows are assigned. Hence in original eight-row source order

```text
S_Y = (0, 0, S_u,Y, S_phi,Y, 0, 0, 0, 0).
```

The H4F2H direct source-Ward projection uses only rows `b`, `isotropic` and `anisotropy`:

```text
W_source,Y =
    d_t S_b,Y + (a/3)*d_x(S_iso,Y + 2*S_aniso,Y) = 0,
```

**exactly**, including at zero-gradient crossings `g10=0`, for any finite `u10, phi10, u11, phi11` and any time/spatial derivative operator mapping the **zero arrays** to zero. In particular, a high-order `M9` bound for the nonsmooth flux `2|g10|g11` is **not needed to bound this *direct* projected Y-source Ward term**. This does **not** imply the Y u/phi forcing vanishes; it does not eliminate Y-dependent regularity requirements in state reconstruction, nonlinear H4 dynamics, parent residuals, or the physical metric.

## 4. Why D12R3 and G3 remain OPEN

D12R3 preregistration and D9's frozen budget protocol explicitly marked `Y_zero_set_lower_regularity_modulus_for_FD8=OPEN`. **Do not silently change a frozen preregistration.** This note only isolates a mathematical *support-based reduction candidate* for a separately versioned, pre-residual budget amendment. A valid new budget must first specify where Y enters the total Ward term *indirectly* (if anywhere), and prove or bound those routes. No full physical `M5/M9` derivative envelopes, roundoff propagation, per-node parent/boundary terms or pre-residual `B_total` is supplied here.

Uninspected user-local D12R9 audits may contain further regularity evidence, but this document does not claim to have validated those local files. Obtain and verify the actual frozen D12R9 reports before promoting any status.

## 5. Concrete next step, no numerical replay

1. Prove in the original `Cmat` Euler row implementation the continuum `D_W L_total=0` syzygy for arbitrary canonical jets (not just manufactured FD4 polynomials). Audit any action normalization/constraint elimination before testing physical grids. Do not solve `Z21`.
2. Precisely evaluate which of `P_lower` parent terms require actual measured residuals on the original common x=ln(a) grids versus which disappear from already certified H1/Z11/GE05 on-shell proofs.
3. Audit the D12R9 resource/regularity reports and freeze a physical error-budget scope with any proposed **versioned** support-based Y amendment explicitly distinguished from original D12R3 preregistration.
4. Only after those proofs: one integrated original-grid Ward check and, conditional on a real PASS, one final `Z21` science solve with original `1e-6` active-shift and temporal-order gates.

## Reproducibility and strict claim boundary

Local symbolic run of an independently prepared SymPy expansion verified the first-order linear coefficient and Y support projection without any physical solver. The repository script `ge19/h4f3d_ward_syzygy_y_support_scope_analytic.py` implements the corresponding algebra and explicitly checks Stage E source support in the frozen module. It should be rerun on the repo branch; creation of this script or document alone is **not** equivalent to a repo CI certification.

**No new science certification**: `full_H4_Ward_certified=false`, `Z21_certified=false`, `lensing_licensed=false`. Historical Repair37 / Cr12ac / D22A failures remain immutable.
