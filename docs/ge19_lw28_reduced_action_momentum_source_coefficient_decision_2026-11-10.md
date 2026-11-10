# GE19 LW28 — reduced-action momentum/charge closure and conditional source normalization decision

**2026-11-10.** Scope: linear scalar-longitudinal perturbations of original analytic, plane-symmetric **GE06+GE05 reduced action**, around relaxed FLRW. **12/12 exact SymPy checks PASS**, independently run in the analysis Python container. No CLASS run, no DES Y3 residuals, no tuning, no source code patch. This note does **not** certify the full 3+1 covariant AeST + nonanalytic Y action, its complete constraint dictionary, or physical Weyl/detection.

## Frozen original LW27 WSL evidence

The user's uploaded original local WSL results were independently inspected:
- \`results/ge19_lw27_r1.log\`: 338 bytes; SHA-256 \`252c8904a20f735d6d6f1dbf372d3c53c25a62681a616ccc1717fdb00ae4fb99\`; Git blob \`3f5bca899b1f2e214aa905a0498f571b658840aa\`.
- \`results/ge19_lw27_scalar_charge_velocity_source_closure_20261110_r1.json\`: 3127 bytes; SHA-256 \`0ebbe0aa34affae337bc4367ae6c25181ff8c8768f81c732d8e1ab12cf271cea\`; Git blob \`522f04288f0ffc52fc0fc4e306770eb1a13f5e26\`.

Both were archived on GitHub; readback Git blob hashes **match both originals**. The initial JSON upload commit accidentally lost one hexadecimal digit in a quoted source-blob SHA. That archival transcription error was repaired in commit \`9a3f33859a8d06b0a6edd25a37b2ed47de3fa79d\` and readback matches the uploaded original exactly. This did not modify the physical LW27 result. LW27 original researcher WSL: **20/20 exact symbolic PASS, 8/8 original source locks PASS**, classification \`...FACTOR_TWO_COMPATIBILITY_REVIEW_FULL_3PLUS1_OPEN\`. Duplicate LW26 files match previously archived originals and were not re-archived.

## 1. Momentum of the original reduced action independently fixes the phase-velocity *ratio*

The frozen reduced action matter density in the 1+1 scalar-longitudinal coframe is

\[
\mathcal L_{\rm mat}=NLR^2\left[K_BE^2+2(2-K_B)EX-(2-K_B)X^2+2K(Q)+\frac{\eta}{4}((Aq)^2-(\omega q-\sqrt w X)^2)\right].
\]

Holding relaxed FLRW \(E_0=X_0=q_0=0\), and perturbing only the scalar spatial derivative \(\partial_x\varphi\), direct exact variation of the **total original reduced matter Lagrangian** with respect to the ADM shift \(b\) gives

\[
\boxed{(E_b^{\rm mat})_1=-2a^3 K_Q\,\partial_x\varphi.}
\]

The GE05 bath contributes no direct linear shift Euler source in this reduced field basis. Also \((\partial\mathcal L/\partial b_x)_1=0\) for this scalar-only perturbation; LW25/LW26 separately checked the broader linear coframe directions. Original background CLASS stress normalization verified by LW24 is

\[
\rho_A=\frac{QK_Q-K}{3},\quad p_A=\frac K3,\quad
\boxed{\rho_A+p_A=QK_Q/3}.
\]

Combining the independently action-derived momentum variation and enthalpy,
\[
\boxed{(E_b^{\rm mat})_1=-6a^3(\rho_A+p_A)\partial_x(\varphi/Q).}
\]

Thus the original reduced matter momentum/enthalpy ratio is proportional to \(\varphi/Q\) and has **no explicit bath eta correction at this order**. This supports the previously used scalar-phase velocity dictionary \(\theta_A=k^2\varphi/(aQ)\) in the established CLASS gauge convention. It does **not** separately derive the full 3+1 metric ADM shift constraint, fix all gauge sign conventions, or exclude an eta-dependent change in the *full* theory's fluid frame.

## 2. The full reduced scalar charge selects a unique coefficient under the *fixed* dictionary

With original LW17 scalar bath flux and LW24 density/pressure dictionary, the exact **explicit eta source** identity is

\[
\frac{6a^3}{Q}\,\partial_\eta\dot{\delta\rho}_A
+\frac{2ak^2}{Q}\left[K_B\partial_\eta\dot E_A+(2-K_B)\partial_\eta\dot\chi\right]
+\frac{ak^2 B_\chi}{2}=0.
\]

All derivatives in this identity mean **explicit eta partials of the first-order evolution right-hand sides at fixed state**, not total derivatives of fully evolved observables.

Parameterize the implemented E-equation memory source as
\[
\partial_\eta\dot E_A=-\gamma\, Q B_\chi/K_B.
\]

For the unchanged action-derived scalar phase/velocity dictionary, \(\partial_\eta\dot\chi=0\), and the unchanged fluid-density evolution has no new explicit bath term \(\partial_\eta\dot{\delta\rho}_A=0\). Therefore the *reduced-action scalar Euler identity* fixes, uniquely,

\[
\boxed{\gamma=\tfrac14.}
\]

If instead \(\gamma=\tfrac12\), as the current original v019j code injects in \`E_rhs_aest -= 0.5*Q_aest*Bchi_aest;\`, the reduced scalar charge requires

\[
\boxed{
\left.\partial_\eta\dot{\delta\rho}_A\right|_{\gamma=1/2}
=\frac{Qk^2B_\chi}{12a^2}\neq0
}
\]
for a generic nonzero physical source. The existing original v019j memory patch has no additional explicit bath source in \(\delta_A'\) or \(\theta_A'\). The ad hoc LW25 velocity compensator would violate the retained phase-velocity dictionary unless separately derived from the full action.

The coefficient \(\tfrac14\) is also independently obtained from the exact normalized GE05 aether Euler force divided by the \(\mathcal L_{\rm AeST}\) kinetic coefficient, as in LW25. Thus **both reduced-action equations (scalar charge and aether Euler), plus momentum/enthalpy**, consistently select one-quarter under the identical frozen reduced-model conventions. This is a substantive advance over matching only the pre-existing implemented CLASS source against its own external forcing.

## 3. Physical model decision and stop

The correct interpretation is:

- **Established for the original reduced linear model:** coefficient \(\gamma=\tfrac14\) is required by the original action with fixed scalar-phase fluid dictionary and no explicit added density/velocity source. It passes the action-derived aether and scalar equations; the original patched \(\tfrac12\) creates a conditional source-compatibility defect.
- **Not established:** whether the full covariant AeST action plus the \(Y\)-sector, general scalar metric constraints and full CLASS fluid variable redefinition keep exactly that mapping or generate other physical terms. It is **not yet a proof** that changing one C line makes a complete physically correct cosmological model.
- **Do not silently modify** original v019j or patched official CLASS checkout; both are frozen provenance. Keep LW01–LW08 original numerical claims as **implemented externally forced response only**, not physical eta-normalized detection.
- **Future correction, only with a new clearly versioned theory/implementation:** derive the full 3+1 scalar+aether+GR/source-to-C\_ell dictionary. If its theta/density definition matches the reduced limit, create a separate action-consistent branch with \(\gamma=1/4\) (not a retroactive rewrite) and test both action scalar charge and aether constraints, then its matter–Weyl transfer. If the full action has extra sources, include them *only when derived*, not to force a PASS.
- **No DES data/forecast yet:** LW22 real source geometry PASS remains scientifically useful. Observed \(\gamma_t\), nuisance-marginal Asimov distinguishability, actual \(\partial_\eta P_{\delta W}\) and detection remain OPEN. Prior LW03 radial FAIL, LW05 cosmic shear LOS BLOCK, LW08 differential source UNRESOLVED and H4/Z21 uncertified are untouched.

## 4. Reproducibility, with independently executed bounded proof

Python source \`ge19/lw28_reduced_momentum_scalar_continuity_proof_20261110.py\`, commit \`544d1436dc37c095d3d2bdde35dc6fd8873c1c1c\`, exact Git blob \`2084d78c05b192048bf121dae657e1d7396f254c\`; local original file SHA-256 \`b11165a16bc03d45d0a8298edc9b5a9efda20fe2a35c391e55914c2ea7ef2024\`. This source was run with local SymPy; **12/12 analytic checks PASS** and the GitHub source readback is byte-identical to the actually executed Python file. It requires no project venv, no official CLASS, no network, no observational files, no parameter sweeps. It is a post-hoc physics derivation, not an independent pre-data preregistration.

**Required next step:** leave the reduced-model proof as is and focus specifically on the missing full 3+1 action-derived velocity/ADM Einstein constraint dictionary and physical Weyl output. If that full bridge cannot be established, report a conditional reduced-model consistency result and stop before claiming observability.
