# GE19 — frozen local analytic PASS and 16-jet production Cmat obligation

Date: 2026-11-07  
Branch: `physics-first-gravitational-elasticity`  
Scope: **source-bound exact sector cancellation PASS; exact integrable-jet coefficient map derived; actual all-jet Cmat identity still OPEN.**

## 1. Locally executed frozen analytic result (provided by researcher)

Source: `ge19/h4f3d_linear_sector_background_lapse_audit.py`.  
Local JSON: `results/ge19_h4f3d_linear_sector_background_lapse_audit_20261107.json`.  
JSON SHA-256: `72d1376a28d75d18b8b34f3239fef1cf4f9c681f2861f78432ff931768af2dcf`.  
Local log: `results/ge19_h4f3d_linear_sector_background_lapse_audit_20261107.log`.  
Log SHA-256: `0182b737ffb78efd936e39a5a1f70700938ae7b59ec24a25bb562f5c3dd8bc27`.

User-provided JSON and log are consistent and report exactly:

```text
GE19_EXACT_GE07_OFFSHELL_AND_LINEAR_WARD_PASS
GE19_GE06_PLUS_LAMBDA_EN00_PLUS_6C_PASS
GE19_GE07_EN00_MINUS_6C_PASS
GE19_TOTAL_BACKGROUND_LAPSE_CANCELLATION_PASS
FULL_CMAT_WARD_OPEN Z21_CERTIFIED=false LENSING_LICENSED=false
```

JSON classification: `GE19_LINEAR_GE06_LAMBDA_GE07_LAPSE_BACKGROUND_EXACT_PASS_TOTAL_CMAT_OPEN`. All six frozen source Git blob pins matched, all GE07 gates and all GE06/Lambda gates `true`. These provided local files are not automatically GitHub committed. No change to original scientific thresholds or historical FAILs.

On the frozen Repair13 background, with `D=a^3 varrho_action=3C`, the source-derived exact identity is

```text
E_N00^(GE06+Lambda) = +6 C
E_N00^(GE07)        = -6 C
E_N00^(total)       = 0 .
```

A dust-only first-order Ward test that **prematurely discards** `E_N00^(GE07)` must fail by an algebraic term `+6 i k C N10`. This is not a physical total-sector failure.

## 2. Source-bound canonical operator: coefficient decomposition

Original GE19 canonical local state is

```text
w = (N, drho, S, u, phi, T, Sdot, udot, phidot, Tdot)
```

with row conventions from `ge19/repair07_window_retarded_reduced_h3_z20_particular.py` and `ge19/h4f3d1_frozen_canonical_operator_ward.py`:

```text
B = Cmat[10] + Cmat[11]               (combined shift Euler)
P = Cmat[14]                           (GE06 independent L momentum)
J = (Cmat[6] + 2*(Cmat[12]+Cmat[13]))/3   (L Euler without pLdot)
E_b = B*w,   E_L = J*w - d_t(P*w)
W_operator = -d_t(B*w) - i*k*a*E_L .
```

For time-dependent operator row coefficients and fixed Fourier k, introduce

```text
U = -d_t B - i*k*a*J + i*k*a*d_t P
V = -B + i*k*a*P
W_operator = U*w + V*d_t w .
```

**Derivatives of Cmat rows must include derivatives of all background quantities** (`a,H,Q, K_Q, ...`) along the exact Repair13 equations. Since `w[6:10]` are already `d_t(w[2:6])`, **w and d_t(w) are not 20 independent jets.** There are exactly 16 independent coefficients of the six field functions and their admissible temporal derivatives:

| Group | Exact necessary and sufficient conditions | Count |
|---|---|---|
| Base field amplitudes | `U[0:6] == 0` | 6 |
| Independent first derivatives of lapse/dust-density | `V[0] == V[1] == 0` | 2 |
| Second derivatives of S,u,phi,T | `V[6:10] == 0` | 4 |
| First derivatives of S,u,phi,T | `U[6+j]+V[2+j] == 0`, j=0..3 | 4 |
| **Total** | **16 independently testable conditions** | **16** |

This equivalence was checked through direct SymPy product-rule differentiation, jet substitution and coefficient extraction. It is a **formal arbitrary-integrable-jet contract**, not yet a verified physical `Cmat` PASS.

**Exact GE07 sector remainder in this contract:**

```text
B_d[5] = -2 D i k             (from shift E_b = -2D i k T)
J_d[0] = -2 D/a               (from E_L = (2D/a)(Tdot - N))
J_d[9] = +2 D/a
P_d = 0

W_d = 2 i k D N = 6 i k C N .
```

The dynamic first-derivative `Tdot` terms cancel exactly; the only nonzero dust-only jet coefficient is the lapse amplitude. Accordingly, the **combined** GE06+Lambda production Cmat must produce `-6 i k C` in the corresponding amplitude coefficient and zero for the others, before declaring the *total* linear Ward syzygy.

## 3. Implementation evidence and bounded claim

Source-bound analytic program: `ge19/h4f3d_cmat_integrable_jet_analytic_gate.py` (new read-only program; fast symbolic operations, not a physical solver). It checks the 16-jet decomposition and exact dust-only leftover against frozen source hashes and source snippets. The underlying algebra has been independently checked using local SymPy, but the new GitHub program has **not yet been executed on the user's checkout**, so no new local JSON certification is claimed for it.

Remaining actual production gate is **not** a new V12 shift-source replay. It is an exact *all-16 coefficient* source-bound verification using original GE06/GE07/Lambda `Cmat`, correct `a/H/Q` background derivatives and original independent-`L` momentum row. Do not replace that with arbitrary coefficient matrices or a manufactured polynomial FD4 exercise. Do not assume each action sector is separately on shell.

A zero continuum operator identity alone does not bound discrete FD4/FD8 truncation at actual H4 parent grids; this remains separately protected by original D9/D12R3 preregistration.

## 4. Minimal local command for the new analytic contract

```bash
cd ~/aest-memory-gravity
git pull --ff-only
source .venv/bin/activate
export PYTHONPATH="$PWD"
python3 -u -m ge19.h4f3d_cmat_integrable_jet_analytic_gate \
  --json-out results/ge19_h4f3d_cmat_integrable_jet_analytic_gate_20261107.json \
  2>&1 | tee results/ge19_h4f3d_cmat_integrable_jet_analytic_gate_20261107.log
echo "EXIT=${PIPESTATUS[0]}"
```

**Claim flags unchanged:** `complete_canonical_Cmat_Ward_certified=false`, `full_H4_Ward_certified=false`, `Z21_certified=false`, `lensing_licensed=false`. Original `H4_active_shift_Nt128_Linf <= 1e-6` and original `>=2.5` temporal order untouched.
