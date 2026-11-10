# GE19 LW33 — full reduced scalar Euler in original CLASS variables: an exact off-shell source identity

**2026-11-10; scientific decision: conditional normalization mismatch of the *reduced analytic* Einstein–AeST+NL0B linear theory with the historical frozen CLASS half source.** Independent local SymPy derivation: **19/19 exact symbolic gates PASS**, including the complete off-shell identity with the action density dictionary *not* assumed in advance. The canonical source-locked researcher WSL run is pending. **This is not a proof of full 3+1 AeST+Y action-to-CLASS equivalence and not a GW or DES observation.** No CLASS sweep, observational data, nuisance fitting or frozen-patch modification.

## 1. Original WSL LW32 parent: independently verified, archival identity

The researcher-supplied original WSL files were read and SHA-256 validated:
- JSON 2,943 bytes, SHA-256 \`1990409ccc8529ea6725ca4dbf13aa80f5639d5b5adce33e801f7be8b7a9f884\`, original Git blob \`852fc07083745865307150d759cb53ba230fe3ad\`, archived as \`results/ge19_lw32_covariant_aether_auxiliary_multiplier_elimination_20261110_r1.json\`.
- log 355 bytes, SHA-256 \`e7d1c2ed5b01ee8443587741338897f91a648dc58bdefdf6c7598be250ec9885\`, original Git blob \`3d3d2488184a41f2516bf41348c221a9e19254e2\`, archived as \`results/ge19_lw32_r1.log\`.
Both were independently retrieved from GitHub after creation and their Git blobs match original uploaded bytes. The repeated LW31 uploads match previous archives. Actual LW32 WSL result: **20/20 symbolic gates PASS, 5/5 original-source locks PASS**, full physical CLASS eta source still OPEN.

## 2. Exact full scalar current before imposing *any* perturbed equation of motion

Use the original frozen analytic longitudinal GE06+GE05 reduced action about relaxed FLRW, in cosmic proper time \(t\) with \(H=\dot a/a\), scalar Fourier \(k\ne0\), \(C=2-K_B\). Define \(\delta Q=\dot\varphi-Q\Psi\), \(E=\dot\alpha+\Psi\), \(\chi=\varphi+Q\alpha\), normalized auxiliary memory force \(B_\chi\), and original scalar charge and spatial flux:
\[
J_\phi^t=2a^3K_{QQ}\delta Q-6a^3K_Q\Phi,\qquad
J_\phi^x=ika\bigl[2C(E-\chi)+2K_Q\alpha-\eta B_\chi/2\bigr].
\]
The original scalar equation is \(-\dot J_\phi^t-ikJ_\phi^x=0\), equivalently
\[
\mathscr S_\phi
=\dot J_\phi^t-ak^2[2C(E-\chi)+2K_Q\alpha-\eta B_\chi/2]=0.
\]
Retain original background laws \(\dot K_Q=-3HK_Q\), \(\dot Q=-3HK_Q/K_{QQ}\). There is no assumed constraint propagation in this calculation and no numerical CLASS result.

From the original action density and pressure dictionary:
\[
D_A^{\rm action}=\frac13\left[QK_{QQ}\delta Q-\frac{k^2}{a^2}(K_B E+C\chi)\right],
\quad P_A=\frac{K_Q\delta Q}{3},\quad R_A=\rho_A+p_A=\frac{QK_Q}{3},
\quad T_A=R_A\frac{k^2\varphi}{aQ}.
\]
Introduce an **independent** fluid density state variable \(D_A\); do not assume \(D_A=D_A^{\rm action}\) in the proof.

## 3. The complete exact off-shell residual decomposition

For an arbitrary proposed explicit eta-source coefficient \(\gamma\), parameterize the CLASS-form proper-time aether evolution as
\[
\dot E_\gamma=-HE+\frac{1}{K_B}\{K_Q\chi
-C[\dot\chi_{\rm kin}-QE+(H+Q)\chi]
-\eta\gamma Q B_\chi\},
\]
where \(\dot\chi_{\rm kin}=\delta Q+QE+\dot Q\,\alpha\) follows from the frozen \(\chi=\varphi+Q\alpha\), \(\dot\alpha=E-\Psi\), and the original scalar definition.

The original CLASS-form effective-fluid energy equation is
\[
\dot D_{\rm fluid}=-3H(D_A+P_A)-T_A/a+3R_A\dot\Phi.
\]
Define the following *separately identifiable, unconstrained residuals*:
\[
\begin{split}
R_D&=\dot D_A-\dot D_{\rm fluid},\\
R_E&=\dot E-\dot E_\gamma,\\
R_\chi&=\dot\chi-\dot\chi_{\rm kin},\\
R_{\rm geo}&=\chi-\varphi-Q\alpha,\\
R_\rho&=D_A-D_A^{\rm action}.
\end{split}
\]

**Directly differentiating the full original scalar charge gives the following exact off-shell algebraic identity:**
\[
\boxed{\begin{aligned}
\mathscr S_\phi={}&\frac{6a^3}{Q}R_D
 +\frac{2ak^2K_B}{Q}R_E
 +\frac{2ak^2C}{Q}R_\chi
 +\frac{2ak^2K_Q}{Q}R_{\rm geo}\\
 &-\frac{6a^3}{Q}\dot R_\rho
 -\frac{18a^3H}{Q}R_\rho
 +\frac{a\eta k^2 B_\chi}{2}(1-4\gamma).
\end{aligned}}\tag{*}
\]

**The density dictionary residual and its time derivative are explicitly retained.** Consequently (*) is not a tautology that prematurely sets the action density definition, the fluid evolution, the aether evolution or the phase-velocity identity on shell. Its proof uses only the stated FLRW background laws and symbolic first-order action currents; SymPy reduces the difference to **exact zero** for arbitrary independent field amplitudes, derivatives and \(\gamma\).

Because (*) is independent of the Einstein Hamiltonian/momentum/shear equations, setting the three already-proven reduced metric constraint residuals to zero **cannot by itself** eliminate a nonzero final bath term while retaining the fixed other definitions and equations. This does not rule out extra *unmapped* terms from a different full 3+1 action-to-fluid projection.

## 4. Consequence for the frozen v019j coefficient — the first complete reduced Euler compatibility decision

If the full original reduced-model state dictionary is enforced over time (\(R_\rho=\dot R_\rho=R_{\rm geo}=R_\chi=0\)), and the CLASS-form fluid and E evolution rows are both obeyed (\(R_D=R_E=0\)), (*) reduces to
\[
\boxed{\mathscr S_\phi=\frac{a\eta k^2B_\chi}{2}(1-4\gamma).}
\]
For generic nonzero physical memory force, action scalar conservation requires uniquely \(\gamma=1/4\). The historical original v019j patch uses \(\gamma=1/2\), leaving
\[
\boxed{\left.\mathscr S_\phi\right|_{\gamma=1/2}=-\frac{a\eta k^2 B_\chi}{2}.}
\]

At fixed original density/velocity dictionaries, restoring scalar charge with the original half source would require an *additional* explicit density evolution source
\[
\boxed{\Delta\dot D_A=+\frac{\eta Qk^2B_\chi}{12a^2},}
\]
which is not in the frozen v019/v019j fluid equation. Alternatively a *formal* \(\Delta\dot\chi=\eta Q B_\chi/[4(2-K_B)]\) would cancel the algebra, but cannot be inserted while keeping the same \(\chi=\varphi+Q\alpha\) and phase definition. No numerical or phenomenological compensation is licensed.

This reconciles the history:
- Old NL0B raw aether bath Euler source proportional to \(-\eta QB_\chi/2\) was correctly derived.
- LW25/LW29 full kinetic normalization divides by \(2K_B\), giving a one-quarter **local E-evolution** source in the original fixed analytic action.
- LW27 identified a fixed-state source contradiction.
- **LW33 upgrades this to the complete linear reduced scalar charge equation as an exact residual identity**, including all algebraic dictionary residuals and their derivatives.
- LW30/LW31 establish restricted metric constraints, LW32 rigorously eliminates two algebraic multipliers. All of these do **not** yet prove that the completely unreduced 3+1 AeST+nonanalytic-Y+multi-species theory has no different, required terms.

## 5. Stop and version decision; no more unrelated symbolic audits

**Outcome:** a **demonstrated reduced-model source normalization incompatibility** of the historical half-source CLASS bridge with the original fixed reduced action. The complete covariant action-to-original CLASS gauge/effective-fluid mapping is still open. The historical \`v019j/apply_memory_patch.py\` and original official CLASS checkout remain frozen, unchanged, and their prior implemented response cannot be rebranded as a physically normalized observation.

**Concrete next step (not another blind sweep):** one finite audit of the original full covariant **quadratic scalar action** and the *joint* scalar/aether/metric constrained evolution, using all relevant multipliers and proper CLASS time conventions. Its only decision is whether the new, separately versioned, action-consistent CLASS candidate should use the quarter source with unchanged fluid definitions or whether an independently action-derived additional source/mapping exists. If unresolved, publish the bounded analytic consistency result as such rather than claim lensing detectability.

No physical \(\partial_\eta P_{\delta W}\) or DES Y3 \(\gamma_t\) prediction is certified yet. LW22 observed source-geometry is sound; LW08 differential tangent remains unresolved. Do not retune based on DES residuals.

## 6. One reproducible short WSL run

Frozen predata \`ge19/lw33_action_scalar_euler_class_residual_predata_20261110.json\`, commit \`1c12d8ac26d01e6e6eabcc34da2f5a863c5532a9\`, Git blob \`19b1e2cfca8937c7af4beb6bf9784bd9a1372c7e\`. Algebra was explored before freeze; no blind preregistration.

Canonical test \`ge19/lw33_action_scalar_current_class_residual_20261110.py\`, commit \`15256006aaa051c51baa1ba0c9ca09852110dfee\`. Nineteen independent SymPy checks passed in the analysis container. The canonical new file, source locks against seven unchanged original paths, and byte-exact researcher LW32 JSON parent require **researcher WSL verification**. No GitHub Actions or numeric CLASS work.

One WSL command:
~~~bash
cd ~/aest-memory-gravity
git pull --ff-only
source .venv/bin/activate
python3 -u -m ge19.lw33_action_scalar_current_class_residual_20261110 --self-test
set +e
set -o pipefail
python3 -u -m ge19.lw33_action_scalar_current_class_residual_20261110 \
  --out results/ge19_lw33_action_scalar_current_class_residual_20261110_r1.json \
  2>&1 | tee results/ge19_lw33_r1.log
echo "EXIT=$?"
~~~
Expected \`GE19_LW33_OFFSHELL_SCALAR_CLASS_IDENTITY_PASS 19\`, \`GE19_LW33_SOURCE_LOCKS_PASS 7\`. If WSL gives a real failure, preserve the failure and inspect it; do not change physical normalizations to force success.
