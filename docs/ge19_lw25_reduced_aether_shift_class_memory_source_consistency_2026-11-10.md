# GE19 LW25 — reduced aether/shift Euler versus CLASS memory source

**2026-11-10: CONDITIONAL_REVIEW_REQUIRED, not a full-theory FAIL.** This is an exact algebraic comparison in the original GE06/GE05 analytic reduced plane-symmetric longitudinal model, not a certification of the full 3+1 nonanalytic Y action or an observational result.

## Original LW24 researcher WSL evidence archived byte-identically

- \`results/ge19_lw24_r1.log\`: 371 bytes, SHA-256 \`0f7b81a225053ce9bc4965829f5ca7404df90ad36112cdd0cb8b12265ab5a217\`, Git blob \`88bfc5fa653db0d78ef379da8ac8764dedc698b2\`.
- \`results/ge19_lw24_reduced_action_class_density_pressure_dictionary_20261110_r1.json\`: 2,218 bytes, SHA-256 \`f2b8c8bade6cad1d0ca48e11e56dd19bdecfd597fc20d99b5afdd5506a5c33d5\`, Git blob \`c88fb76da60d4647744b1324776633dfd5dfbdc7\`.

GitHub archive blobs independently matched the original uploads. LW24 WSL: **17/17** exact symbolic checks PASS and **four source locks PASS**. Scope: reduced action density/pressure dictionary only, physical eta transfer and metric observer NOT certified.

## First-order exact reduced Euler rows

Original combined action with \(\eta\) multiplying GE05 bath:
\[
\mathcal L=NLR^2\left[K_BE^2+2CEX-CX^2+2K(Q_{\rm inv})
+\frac{\eta}{4}((Aq)^2-(\omega q-\sqrt w X)^2)\right],\qquad C=2-K_B.
\]
At relaxed FLRW use proper time \(t\), \(H=\dot a/a\):
\[
E_1=\dot u_1+\partial_x\Psi/a+Hu_1,\quad
X_1=Qu_1+\partial_x\varphi/a,\quad
B_{X,1}=wX_1-\omega\sqrt w q_1,\quad
A_1=K_BE_1+CX_1.
\]
Independent differentiation of this exact reduced Lagrangian yields
\[
(\partial_u\mathcal L)_1
=2a^3[H A_1+CQ(E_1-X_1)+K_QX_1]
-\eta a^3QB_{X,1}/2,
\]
\[
(\partial_{\dot u}\mathcal L)_1=2a^3A_1,\qquad
(\partial_{u_x}\mathcal L)_1=0.
\]
Therefore \(E_u^{(1)}=2a^3[-(\partial_t+2H)A_1+CQ(E_1-X_1)+K_QX_1]-\eta a^3 QB_{X,1}/2\).
The linear ADM shift Euler is independently
\[
\boxed{E_b^{(1)}=-2a^3 K_Q\partial_x\varphi},\qquad
(\partial_{b_x}\mathcal L)_1=0.
\]
No direct linear bath shift source; indirect metric coupling is not excluded.

## The conditional factor-two issue

Under the previously frozen Newtonian projection
\[
E_1=(ik/a)E_A,\quad X_1=(ik/a)\chi,\quad B_{X,1}=(ik/a)B_\chi,
\quad E_A=\dot\alpha+\Psi,\quad \chi=\varphi+Q\alpha,
\]
dividing \(E_u^{(1)}=0\) by \(2ika^2\) gives the **reduced action's aether equation**
\[
\boxed{
K_B(\dot E_A+H E_A)
=K_Q\chi-C[\dot\chi-QE_A+(H+Q)\chi]
-\eta Q B_\chi/4.}\tag{A}
\]
The original \`v019j\` patched CLASS E-row, after converting from conformal \(\tau\) to proper time \(t\), is
\[
\boxed{
K_B(\dot E_A+HE_A)=K_Q\chi-
C[Q\Pi_A/(1+w_A)+(H+Q)\chi-3c_a^2HQ\alpha]
-\eta Q B_\chi/2.}\tag{C}
\]
The **original unmodified** CLASS theta and alpha equations, plus \(\dot Q=-3Hc_a^2Q\), imply exactly
\[
\boxed{
\dot\chi=Q[E_A+\Pi_A/(1+w_A)-3Hc_a^2\alpha].}\tag{T}
\]
Substituting (T) into the reduced-action equation (A) gives \(-\eta QB_\chi/4\), but CLASS equation (C) contains \(-\eta QB_\chi/2\). This is an exact **factor two conditional mismatch** for nonzero \(\eta QB_\chi\) if all those mappings/equations are simultaneously maintained.

A sufficient mathematical compensation **under the same frozen field dictionary** would be
\[
\boxed{\Delta\dot\chi=\eta QB_\chi/(4C),\qquad
\Delta\theta'_A=\eta k^2B_\chi/(4C)}
\]
(prime is conformal time). This is **NOT an action-derived proposed modification** and must NOT be inserted ad hoc into CLASS. An alternative physical Euler/constraint field redefinition could resolve the discrepancy differently.

**Interpretation:** LW23's isolated E-row offline source matches its source coefficient, but full normalization in the combined GE06+GE05 action is not yet proven. The scalar/aether temporal Ward relation from LW18 must coexist with the momentum/velocity and metric constraints. This calculation does **not** prove a bug in the original full theory, nor is it evidence for/against gravitational-memory observation.

## Frozen test and stop rules

Predata: \`ge19/lw25_aether_shift_class_memory_source_consistency_predata_20261110.json\`, commit \`f399b5576e54163171c3d1c4128298d36c4145fd\`, Git blob \`80afe36c4ea5859f3f0e4f76e9f5814f99b7290f\`. Exploratory derivation preceded the freeze; no blind preregistration claim.

Executable: \`ge19/lw25_aether_shift_class_source_consistency_20261110.py\`, commit \`aa7fee69c170efc747181257c73982a3a58ce412\`, 15 symbolic checks, six original-source locks, exact LW24 original SHA lock. **Not yet independently run in researcher WSL**.

Local run (no CLASS, no DES, no GitHub Actions):
~~~bash
cd ~/aest-memory-gravity
git pull --ff-only
source .venv/bin/activate
set +e
set -o pipefail
python3 -u -m ge19.lw25_aether_shift_class_source_consistency_20261110 --self-test
python3 -u -m ge19.lw25_aether_shift_class_source_consistency_20261110 \
  --out results/ge19_lw25_aether_shift_class_source_consistency_20261110_r1.json \
  2>&1 | tee results/ge19_lw25_r1.log
echo "EXIT=$?"
~~~

Expected label: \`GE19_LW25_REDUCED_AETHER_CLASS_ETA_SOURCE_FACTOR_TWO_CONDITIONAL_REVIEW_REQUIRED\`. This is a *review*, not a full-theory FAIL and not a detection. Keep LW22 geometry PASS, LW23 source PASS, LW24 restricted density/pressure PASS, LW08 differential UNRESOLVED, H4/Z21 uncertified.

**Next physics-only task:** independently derive the correctly constrained scalar+aether+ADM/Einstein Euler combination and the physical \(\eta\)-dependent momentum/velocity source, resolving or preserving this factor-two gap. Do not adjust the coefficient to force a PASS and do not fit DES residuals before full physical normalization.
