# GE19 LW29 — covariant 3D scalar quadratic normalization / historical NL0B bridge erratum

**Date 2026-11-10.** **Classification: GE19_LW29_ORIGINAL_COVARIANT_3D_QUADRATIC_NORMALIZATION_QUARTER_PASS_FULL_ADM_BRIDGE_OPEN (theory-level, pending source-locked WSL execution).** This is an action-based statement in the **linear scalar spatial block about relaxed FLRW**. It does not certify a complete 3+1 constrained Einstein–AeST metric/observer calculation, finite-eta dynamics, or DES detection. The result was explored analytically before the predata freeze; no blind-preregistration claim.

## 1. Original canonical action normalization is the issue, not the sign of the bath force

Two original, frozen source definitions share the gravitational normalization \((16\pi\widetilde G)^{-1}\):

1. The published AeST kinetic term in Skordis & Zlošnik (2021) is \(-K_B F_{\mu\nu}F^{\mu\nu}/2\). In the original GE06 longitudinal coframe its scalar electric/acceleration spatial piece is **\(+K_B E_iE^i\)**, together with \(+2C E_iX^i-CX_iX^i\) (\(C=2-K_B\)). See original \`ge06/analytic_aest_directional_source_generator.py\`, fixed blob \`a7afe0035054a9dca55d74a6497c081422114b4c\`.
2. The original NL0B frozen positive auxiliary vector completion uses
   \[
   \mathcal L_{\rm bath}=\frac14\sum_j\bigl[|\mathscr D_AU_j|^2-|\omega_jU_j-\sqrt{\eta w_j}X|^2\bigr].
   \]
   On a fixed normalized causal branch \(U_j=\sqrt\eta\,q_j\) it is \(\eta/4[(\mathscr D_Aq)^2-(\omega q-\sqrt w X)^2]\). See original \`docs/nl0b_predata_covariant_memory_completion.md\`, Git blob \`9b1c013153faeddbd2add3d80eb29f673bc7748f\`.

The **raw bath variation** with respect to the spatial aether perturbation is indeed proportional to \(-\eta Q B_\chi/2\). The old NL0B frozen note establishes that raw term correctly. **But a raw Euler force is not yet the \(\dot E_A\) source.** The complete aether kinetic Hessian from the AeST part must be included before solving the equation for \(\dot E_A\).

## 2. Arbitrary 3D spatial orientation, not just the x-direction reduction

For a nonzero scalar Fourier vector \(\mathbf k=(k_x,k_y,k_z)\), \(k^2=k_x^2+k_y^2+k_z^2>0\), on flat FLRW in Newtonian gauge define
\[
E_i^{(1)}=(k_i/a)E_A,\ E_A=\dot\alpha+\Psi,\quad
X_i^{(1)}=(k_i/a)\chi,\ \chi=\varphi+Q\alpha.
\]
The real-mode cosine-amplitude notation suppresses the matching sine \(i\) factors; the \(k\)-quadratic spatial scalar action is independent of Fourier orientation. For a normalized longitudinal bath coordinate \(q_i=(k_i/k)q\), the original local quadratic Lagrangian (without overall gravitational prefactor) is
\[
\mathcal L_{\rm scalar}^{(2)}
=a^3\left[K_B\frac{k^2}{a^2}E_A^2+
 2C\frac{k^2}{a^2}E_A\chi-
 C\frac{k^2}{a^2}\chi^2+
 \frac{\eta}{4}\left(\dot q^2-
  (\omega q-\sqrt w\,k\chi/a)^2\right)\right]
+\mathcal L^{(2)}_{Q,Y,\mathrm{metric}}.
\]
Any *analytic* quadratic \(Y\propto|X|^2\) correction changes only the scalar-gradient stiffness and does **not** change the kinetic coefficient \(2K_B\). The frozen nonanalytic \(Y^{3/2}\) branch has no quadratic contribution around zero gradients, though it has non-smooth higher directional derivatives.

Vary this action at fixed q and matched retarded branch. Its \(\dot\alpha\) Hessian is
\[
\boxed{
\frac{\partial^2\mathcal L}{\partial\dot\alpha^2}
=2aK_Bk^2}.
\]
The original bath *raw* aether potential source is
\[
\boxed{
\frac{\partial\mathcal L_{\rm bath}}{\partial\alpha}
=-\frac{\eta a k^2Q}{2}B_{\chi,\rm raw}},
\quad
B_{\chi,\rm raw}=w\chi-\frac{a\omega\sqrt w}{k}q,
\]
while the scalar source obeys
\[
\frac{\partial\mathcal L_{\rm bath}}{\partial\varphi}
=-\frac{\eta a k^2}{2}B_{\chi,\rm raw},\qquad
\frac{\partial\mathcal L_{\rm bath}}{\partial\alpha}
=Q\frac{\partial\mathcal L_{\rm bath}}{\partial\varphi}.
\]

In the aether Euler equation \(\partial_t(\partial L/\partial\dot\alpha)=\partial L/\partial\alpha\), the *explicit eta part of the time derivative of \(E_A\) at fixed baseline state* is therefore
\[
\boxed{
\Delta\dot E_A=-\frac{\eta Q}{4K_B}B_{\chi,\rm raw}.}
\]
Conformal time \(\tau\) gives \(\Delta E_A'=-a\eta Q B_{\chi,\rm raw}/(4K_B)\).

The original frozen v019j CLASS patch instead assigns
\[
\Delta E_A'{}_{\rm original\ code}
=-\frac{a\eta Q}{2K_B}B_{\chi,\rm raw}.
\]
This source is **twice** the normalized aether-kinetic ratio of the explicitly fixed AeST+NL0B quadratic action. The result agrees with LW25's full reduced aether Euler derivation, LW27's scalar charge condition, and LW28's momentum/enthalpy condition. This calculation independently checks **all three spatial orientations**, unlike the earlier single-direction reduction.

**Technical limit:** this calculation is the original covariant action's local 3D **scalar quadratic** block, not the complete constraint-eliminated 3+1 quadratic action. The exact full metric lapse/shift, unit-aether multiplier, projected auxiliary orthogonality constraints, other-species couplings and global gauge map still require their own action-to-CLASS equivalence audit. The missing constraints cannot be assumed to cancel or double a source merely by citation to Bianchi identities.

## 3. Explicit historical NL0B erratum — preserve original documents without rewriting history

The original \`docs/nl0b_covariant_memory_completion_result.md\` identified the raw source \(-\eta QB_\chi/2\), declared **Identity 5 'Frozen E closure PASS'**, and concluded that its scalar Ward partner with no direct linear metric stress ensures the old CLASS fluid rows require no independent correction (**Identity 7 PASS**). Those original proof steps did **not** divide the raw force by the full AeST kinetic Hessian \(2K_B\), nor construct the complete action-to-CLASS fluid dictionary. A raw force source PASS cannot itself certify the **normalized** E evolution.

The prior archive label \`NL0B_COVARIANT_MEMORY_COMPLETION_PASS\` remains an immutable historical fact: the file is not modified or silently relabeled. **Current research claim is explicitly qualified:** original NL0B action's sign, positive bath, rank-one scalar/aether source, Drude kernel and FLRW null remain useful; old Identity 5 **as a physical equation-equivalence claim is unverified and contradicted in the fixed scalar quadratic normalization**. Old Identity 7's fluid-equivalence inference is likewise insufficient; neither raw Ward proportionality nor a code-internal conservation identity proves equivalence.

This is a stronger **theory/implementation consistency objection** than a numerical interpolation issue, but it is **NOT** proof that original full covariant AeST is invalid or that a one-line coefficient substitution automatically produces a fully physical numerical cosmology.

Do not change \`v019j/apply_memory_patch.py\` or the official patched CLASS v077 checkout. An action-consistent model must be a separate version after full 3+1 mapping, with independent equation and constraint verification. Existing LW01/LW06 responses are results of the **implemented externally forced** model; their physical eta calibration is currently **uncertified**. LW22 DES Y3 background geometry PASS remains valid independently of this issue.

## 4. Bounded reproducibility

Frozen source/physics question \`ge19/lw29_covariant_scalar_quadratic_normalization_predata_20261110.json\`, commit \`0de136b50cf74c33f150d64725d5859ea512bdb3\`, Git blob \`53b4baf3484ddac7c272a4dd3b9d3eeee2388bd7\`. Exploratory algebra preceded this freeze.

Auditor \`ge19/lw29_covariant_3d_scalar_quadratic_eta_normalization_20261110.py\`, latest commit \`bd10af45ea4103ca0e85bd6b7bb9c4e09e96b0f3\`, 15 symbolic gates, seven original source blob locks, checks the original v019j literal source. The central identities were independently tested with SymPy and passed; the complete newly committed runner has **not yet been executed in researcher's WSL**.

Run one lightweight physics-only WSL check (no CLASS, DES, H4, or parameter sweep):

~~~bash
cd ~/aest-memory-gravity
git pull --ff-only
source .venv/bin/activate
set +e
set -o pipefail
python3 -u -m ge19.lw29_covariant_3d_scalar_quadratic_eta_normalization_20261110 --self-test
python3 -u -m ge19.lw29_covariant_3d_scalar_quadratic_eta_normalization_20261110 \
  --out results/ge19_lw29_covariant_3d_scalar_quadratic_normalization_20261110_r1.json \
  2>&1 | tee results/ge19_lw29_r1.log
echo "EXIT=$?"
~~~

Expected symbolic label \`GE19_LW29_3D_QUADRATIC_SYMBOLIC_PASS 15\`, original source locks \`7\`. Output classification will explicitly state \`FULL_ADM_BRIDGE_OPEN\`. Do not treat a local run as a detection or a physical lensing signal.

## 5. One next decisive physics milestone

Reconstruct the **complete 3+1 constrained scalar quadratic system**, including the unit-aether and auxiliary-orthogonality multipliers and metric lapse/shift, then map all Euler/source rows into the original CLASS \((\delta_A,\theta_A,\alpha_A,E_A,\Phi,\Psi)\) basis. Require both source-level action equivalence and Hamiltonian/momentum constraint propagation. If the source still differs, create a *new* action-consistent implementation variant only after it is justified. Only then physically normalize \(\partial_\eta P_{\delta W}\) and use the frozen LW22 real DES Y3 geometry; do not claim detection before the real \(\gamma_t\) angular-window + bias/IA/covariance nuisance test.
