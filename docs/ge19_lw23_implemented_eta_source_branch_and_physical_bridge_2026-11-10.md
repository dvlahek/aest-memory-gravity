# GE19 LW23 — implemented eta source, retarded branch and physical bridge

**2026-11-10.** This is a bounded physics milestone, not a DES observation. Independent SymPy checks: **10/10 PASS**; required anchor strings in **10 original GitHub source files verified**. Canonical source-locked WSL runner is committed but **not yet executed**.

## 1. Exact implemented source normalization

Original CLASS v019j memory patch, with Fourier convention fixed:
\[
\chi=Q(a\theta_A/k^2+\alpha_A),\quad
B_{\chi,\rm raw}=\sum_j[w_j\chi-\sqrt{w_j}(a\omega_j/k)q_j].
\]
The positive normalized oscillator coordinate is \(q_j=\sqrt{w_j}u_j\); introduce \(z_j=\omega_j u_j/k\). For normalized positive weights \(\sum_j w_j=1\):
\[
B_{\chi,\rm raw}=\chi-a\sum_jw_jz_j
=a\left(\chi/a-\sum_jw_jz_j\right)=a\,y_{\rm offline}.
\]
Hence the actual *implemented E-row* first-order eta forcing is
\[
\boxed{F_E=-aQ B_{\chi,\rm raw}/(2K_B)
=-a^2Q\,y_{\rm offline}/(2K_B).}
\]
This exact coefficient agrees with the literal lines in original \`v019j\`, \`v019w\` and \`v039\`. Negative controls with a missing factor of \(a\) or 1/2 fail. No physical parameter was changed. The offline order-1024 continuum approximation is **not identical** to the finite bath order 16/20 without a convergence/error bridge.

## 2. Eta=0 auxiliary singular branch

The original one-mode normalized auxiliary bath action is
\[
\mathcal L_{\rm bath}=\frac{\eta}{4}
[(Aq)^2-(\omega q-\sqrt w X)^2].
\]
Its Euler equation is \(\eta\mathcal E_q^{\rm norm}=0\).
At exactly eta=0, this does not determine q; for eta>0, dividing by eta gives the regular retarded oscillator. Hence a physical eta derivative at zero requires selecting a continuous **retarded auxiliary branch** \(q_0\) with matched initial data. The eta=0 memory-disabled CLASS baseline and the separately reconstructed retarded auxiliary history are not by themselves a proof of full covariant action equivalence.

For a smooth *implemented triangular* evolution
\[
u'=F_0(u)+\eta e_E S(u,q),\quad q'=H(u,q),
\]
with causal \(q_0\) and matched initial state, direct differentiation gives
\[
\boxed{u_\eta' = D_u F_0(u_0)u_\eta+e_E S(u_0,q_0).}
\]
The auxiliary derivative \(q_\eta\) does not enter the first-order *inhomogeneous* forcing because it is multiplied by eta. This is a **conditional first-order implemented-ODE lemma**, not the fully constrained Einstein–AeST retarded Green operator. Numerical \(\lambda\) in LW01 amplifies the external forcing; it is not a finite physical eta.

## 3. Reduced action Ward companion

Previous exact LW17/LW18 reduced GE05+GE06 variation, independently rechecked algebraically:
\[
E_{\phi,\rm bath}^{(1)}=-\eta ak^2B_{\chi,\rm raw}/2,\quad
E_{u,\rm bath}^{(1)}=-i\eta a^2kQ B_{\chi,\rm raw}/2,
\]
\[
\boxed{Q E_{\phi,\rm bath}^{(1)}+(ik/a)E_{u,\rm bath}^{(1)}=0.}
\]
The scalar and aether Euler sources are linked, and deleting one violates the reduced time-Ward relation. This **does not prove** that inserting only the E-row source reproduces the entire 3+1 action-to-CLASS fluid and metric constraints. That remains the principal physical gate.

## 4. From source to actual observer

Original effective-fluid derivatives from LW10, fixing other states:
\[
\partial_{E_A}\Pi_A=c_a^2 K_B k^2/(3a^2\rho_A),\quad
\partial_{E_A}\alpha_A'=a,
\]
\[
\partial_{E_A}\theta_A'=c_a^2K_B k^4/[3a^2\rho_A(1+w_A)],\quad
\partial_{E_A}\delta_A'=-\mathcal H c_a^2 K_B k^2/(a^2\rho_A).
\]
They establish potential Jacobian paths, not the fully constrained propagator. Photon, baryon, neutrino, effective-fluid density and momentum, anisotropic stress and Einstein constraint feedback must enter \(A_{\rm eff}\).

For a single common primordial mode,
\[
\partial_\eta P_{\delta W}=\mathcal P_\mathcal R^{3D}
(T_{\delta,\eta}T_W+T_\delta T_{W,\eta}).
\]
The product rule is exact; it is not a proof that the currently archived LW06 numerically amplified response has been fully normalized to the physical eta from the **complete** original 3+1 action.

**LW23 classification:** implemented source coefficient and causal auxiliary branch algebra PASS; complete physical Einstein–AeST source-to-observer equivalence **OPEN**. LW22 background source geometry PASS stays valid. LW08 antisymmetric response unresolved; LW03 radial FAIL, LW05 cosmic shear LOS BLOCK and H4/Z21 uncertified are preserved. No DES gamma_t prediction, Asimov significance or observed discovery.

## 5. Frozen code and execution

Predata file \`ge19/lw23_implemented_eta_source_vs_action_branch_predata_20261110.json\` was committed first at \`b21966856f70c031b15e883c693fbaaac86fa710\` (blob \`3dbeba3ea52776d9cda6e85b5dcabda937659a81\`).

Canonical auditor \`ge19/lw23_implemented_eta_source_action_branch_audit_20261110.py\` was committed at \`83a62a74710f34fafd654c52720bd427926d0caa\`. The ten algebraic identities were independently executed with SymPy and passed, and all ten exact GitHub source files were separately checked for anchored source text. The new Python runner itself has **not** been run in WSL; no actual LW23 researcher JSON is yet available.

One local check; no CLASS numerical run, no DES observed data and no GitHub Actions:

~~~bash
cd ~/aest-memory-gravity
git pull --ff-only
source .venv/bin/activate
set +e
set -o pipefail
python3 -u -m ge19.lw23_implemented_eta_source_action_branch_audit_20261110 --self-test
python3 -u -m ge19.lw23_implemented_eta_source_action_branch_audit_20261110 \
  --out results/ge19_lw23_implemented_eta_source_action_branch_20261110_r1.json \
  2>&1 | tee results/ge19_lw23_r1.log
echo "EXIT=$?"
~~~

Expected \`GE19_LW23_SYMBOLIC_SELFTEST_PASS 10\` and \`GE19_LW23_SOURCE_ANCHORS_PASS 10\`. A missing/mismatched frozen source is a fail-closed provenance result, not a physics FAIL.

**Next physics task (not another parameter sweep):** complete action-to-fluid source/change-of-variables for scalar, aether, lapse/shift and metric, including the \(\delta_A,\theta_A,\Phi,\Psi\) CLASS rows. Only then project physical \(\partial_\eta P_{\delta W}\) through the successfully frozen LW22 DES Y3 geometry and actual measured gamma_t windows/nuisance covariance.
