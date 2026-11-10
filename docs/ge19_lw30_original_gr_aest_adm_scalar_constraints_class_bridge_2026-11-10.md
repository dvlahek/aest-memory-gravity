# GE19 LW30 — original GR + AeST ADM constraints vs CLASS scalar observer

**Date:** 2026-11-10. **Classification:** \`GE19_LW30_REDUCED_3PLUS1_GR_AEST_ADM_SCALAR_CONSTRAINTS_PASS_FULL_ACTION_TO_CLASS_OPEN\` (the **restricted symbolic result**, original-source-locked WSL rerun pending). Exactly **17/17 analytic SymPy checks** passed in an independent local execution. No CLASS sweep, observed DES data, likelihood fit or change to the original source.

## Original WSL LW29 parent, byte-exact GitHub archive

Original LW29 \`results/ge19_lw29_covariant_3d_scalar_quadratic_normalization_20261110_r1.json\`: 3,027 bytes, SHA-256 \`1749dff33f327ff0bf342285d7640b48792634dcac8af8bcc0159523311e03bd\`, git blob \`6416e1fd3496d826abcb0d665d31532e1e96787b\`. Original \`results/ge19_lw29_r1.log\`: 361 bytes, SHA-256 \`00b51eb22c222481f88537a9b7b9155a58c9883fd864eebb290d21b5b24f5f9a\`, git blob \`d9afd7f73cfe25eeea581f02878070490a1ba63b\`. **Both were archived and verified by GitHub blob readback as identical to the uploads.** WSL results: 15/15 symbolic checks PASS, 7/7 original-source locks PASS. Repeated LW27 files match the earlier archive, no duplicated source.

## 1. Exact frozen GR and AeST action, with shift varied before fixing Newtonian gauge

In original GE06 plane-symmetric longitudinal coframe:
\[
ds^2=-N^2dt^2+L^2(dx+b\,dt)^2+R^2(dy^2+dz^2),
\quad k_L=\frac{\dot L-b L_x-Lb_x}{NL},
\quad k_R=\frac{\dot R-bR_x}{NR}.
\]
The original frozen Einstein density (after the established spatial integration by parts) is
\[
\mathcal L_{\rm GR}=NLR^2(-4k_Lk_R-2k_R^2)
+2NR_x^2/L+4N_xRR_x/L.
\]
The original analytic AeST matter density is
\[
\mathcal L_A=NLR^2[K_BE^2+2CEX-CX^2+2K(Q)],\quad C=2-K_B.
\]
Add the original GE05/NL0B bath. Around relaxed FLRW \(E_0=X_0=q_0=0\), the bath has **zero direct first-order lapse and shift Euler sources**, although indirect metric response through scalar/aether equations is possible. The full nonanalytic Y sector, other species, all vector/tensor perturbations, unit-aether multipliers and auxiliary orthogonality multipliers are outside this calculation.

Set \(N=1+\Psi\), \(L=R=a(1-\Phi)\), \(u=(ik/a)\alpha\), scalar perturbation \(\varphi\) and \(k>0\), then vary lapse \(N\) and shift \(b\) before setting \(b=0\).

## 2. Independent derivation of the complete GR + AeST momentum constraint within the coframe

For \(E_b=\partial_b\mathcal L-\partial_x\partial_{b_x}\mathcal L\), the exact linear Euler components are
\[
E_b^{\rm GR}=4ika^3(\dot\Phi+H\Psi),\qquad
E_b^A=-2ika^3K_Q\varphi,\qquad
E_b^{\rm bath}=0.
\]
Therefore
\[
\boxed{\dot\Phi+H\Psi=\frac12 K_Q\varphi.}\tag{M}
\]
The independent original-action effective-fluid dictionary obtained earlier is
\[
\rho_A=\frac{QK_Q-K}{3},\quad p_A=\frac K3,\quad
T_A=(\rho_A+p_A)\theta_A,\quad
\theta_A=\frac{k^2\varphi}{aQ},
\]
so \(\frac32 a T_A/k^2=\frac12 K_Q\varphi\). Hence (M) matches exactly the Newtonian CLASS momentum constraint \(\dot\Phi+H\Psi=\frac32 aT_A/k^2\) in this restricted AeST-only sector.

**This is not just a matter-source guess:** it was derived from the full original GR *and* AeST shift Euler variations, retaining their background H and spatial-gradient terms. Several apparent H Phi terms cancel between \(\partial_b\) and \(\partial_x\partial_{b_x}\).

## 3. Independent lapse/Hamiltonian constraint, including the AeST electric gradient

For \(E_N=\partial_N\mathcal L-\partial_x\partial_{N_x}\mathcal L\),
\[
(\partial_{N_x}\mathcal L_{\rm GR})_1=-4a(ik)\Phi,\qquad
(\partial_{N_x}\mathcal L_A)_1=
2a(ik)[K_B(\dot\alpha+\Psi)+C(\varphi+Q\alpha)].
\]
The bath contributes zero direct linear lapse source. The original action's background lapse residual is
\[
\mathcal B=\frac{E_N^{(0)}}{2a^3}
=3H^2-(QK_Q-K).
\]
The action-derived AeST density perturbation is
\[
D_A=\frac13\left[
QK_{QQ}(\dot\varphi-Q\Psi)
-\frac{k^2}{a^2}(K_B(\dot\alpha+\Psi)+C(\varphi+Q\alpha))
\right].
\]
Writing
\[
\mathcal C_H=\frac{k^2}{a^2}\Phi+3H(\dot\Phi+H\Psi)
+\frac32D_A,
\]
the **exact first-order off-background-shell identity**, with Newtonian shift fixed after variation, is
\[
\boxed{E_N^{(1)}|_{b=0}+4a^3\mathcal C_H+
6a^3\Phi\,\mathcal B=0.}\tag{H}
\]

For an **AeST-only** on-shell homogeneous FLRW background \(\mathcal B=0\), the action Euler equation \(E_N=0\) imposes \(\mathcal C_H=0\). Substituting the independently derived momentum relation (M) yields
\[
\boxed{k^2\Phi+\frac32 a^2
\left(D_A+\frac{3aH}{k^2}T_A\right)=0,}
\]
precisely the flat CLASS scalar Hamiltonian constraint in the same units.

Crucially, **the background Friedmann residual is retained explicitly before the on-shell specialization**. No observational data or chosen numerical background was needed. The real cosmological CLASS model also includes baryons, photons, neutrinos and possibly other components: their background and perturbation source terms are NOT included in this AeST-only action proof.

## 4. Implication for LW25–LW29 eta-source normalization

The fixed original reduced analytic action now supports the CLASS-form AeST **density, enthalpy, momentum, and both Einstein scalar constraints**; no separate explicit bath metric source supplies the missing eta correction. Under the same scalar phase/velocity dictionary, the independently derived aether/scalar Ward/source equations still give an E evolution inhomogeneity \(-a\eta QB_\chi/(4K_B)\), compared with \(-a\eta QB_\chi/(2K_B)\) in the frozen v019j code.

This makes the restricted-model **factor-two normalization discrepancy more sharply localized**, not fully resolved. LW30 does **not** derive the complete full covariant scalar/aether-to-effective-fluid evolution or metric anisotropic-stress/shear equation. It does not justify changing the original patched CLASS v077. The nonanalytic Y-sector, all other species and the genuine physical \(\partial_\eta P_{\delta W}\) remain OPEN. No DES \(\gamma_t\) calculation or detection has been obtained. LW22's real DES lensing **geometry** remains valid.

## 5. Committed reproducibility

- Formula/provenance lock: \`ge19/lw30_exact_adm_hamiltonian_momentum_constraints_predata_20261110.json\`, commit \`4b00993dca7028367745a11f80540facc72d2218\`, git blob \`5cce6d6c0736f42feff691ce4370d783dad1d8f2\`. Preliminary exploratory algebra preceded the freeze; no blind preregistration claim.
- Exact action-derived executable: \`ge19/lw30_exact_adm_hamiltonian_momentum_constraints_20261110.py\`, commit \`85e06cec6e2589c68fca18b8d660c6c8217db22f\`, git blob \`b9d2751c1a858cd00d3ef44816e7f7300113f600\`. It was independently executed in the analysis runtime with **17/17 PASS**; the GitHub byte-blob matches that executed source. Includes six frozen original-source blob locks, three original action-string anchors, and the exact uploaded LW29 parent JSON SHA.
- The new canonical GitHub runner has **not yet executed in the researcher's WSL**. A provenance failure must remain a failure until investigated; no physics threshold changes to force success.

One short local WSL run, no CLASS/observations:
~~~bash
cd ~/aest-memory-gravity
git pull --ff-only
source .venv/bin/activate
set +e
set -o pipefail
python3 -u -m ge19.lw30_exact_adm_hamiltonian_momentum_constraints_20261110 --self-test
python3 -u -m ge19.lw30_exact_adm_hamiltonian_momentum_constraints_20261110 \
  --out results/ge19_lw30_exact_adm_hamiltonian_momentum_constraints_20261110_r1.json \
  2>&1 | tee results/ge19_lw30_r1.log
echo "EXIT=$?"
~~~

Expected \`GE19_LW30_GR_AEST_ADM_SCALAR_SELFTEST_PASS 17\`, \`GE19_LW30_FROZEN_SOURCE_LOCKS_PASS 6\` and classification \`FULL_ACTION_TO_CLASS_OPEN\`.

**Next decisive physics gate:** complete full scalar+aether Euler-to-fluid and spatial Einstein shear dictionary in the actual full covariant AeST+NL0B action, with unit-aether and auxiliary multipliers and standard-species perturbations. Only after normalizing the physical \(\eta\)-dependent matter–Weyl Green can the genuine DES Y3 GGL test be started.
