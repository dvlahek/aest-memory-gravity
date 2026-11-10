# GE19 LW32 — exact covariant unit-aether/auxiliary multiplier elimination (restricted FLRW tangent)

**2026-11-10. Independent analytic result: 20/20 exact SymPy gates PASS.** The canonical GitHub source-locked LW32 script has **not yet been run in the researcher's WSL**. This is a proof about **algebraic constraint elimination and the Euler-chain-rule equivalence** for one unit-timelike aether plus one aether-orthogonal auxiliary mode on the regular near-FLRW branch, **not** a solution of the full 3+1 Einstein–AeST–NL0B evolution, the CLASS action-to-fluid equivalence, or a DES Y3 observation. No source coefficient or parameter has been edited.

## 1. Frozen original LW31 evidence

The user's original LW31 uploads were independently read and checked:
- \`results/ge19_lw31_action_spatial_traceless_shear_20261110_r1.json\`: 2,828 bytes, SHA-256 \`c7fc4aa0e57cd4a6a0665d5544da53a981120d2c7014a6cc9c35fc68e819f9cd\`; Git blob \`eedcf8bc4d2e5155bd40ccd218c1ce00d19898d3\`.
- \`results/ge19_lw31_r1.log\`: 340 bytes, SHA-256 \`e0842f91bd73a97af4d43539f82674951097909836927649272f7b121193d576\`; Git blob \`fd13dc9b8cbb15da49fdc9d0622cf7cde6585a35\`.

Both were archived verbatim and fetched back with matching exact Git blob hashes. The original WSL run passed **15/15** symbolic and **5/5** source locks, with full-action bridge OPEN and \`PHYSICAL_OBSERVER_READY=False\`. Duplicate LW30 files match previously archived originals.

## 2. The actual full-covariant algebraic constraints

The frozen NL0B action introduces unit-timelike aether \(A^\mu\), \(g_{\mu\nu}A^\mu A^\nu=-1\), and an auxiliary spacetime covector \(U_\mu\) constrained by \(A^\mu U_\mu=0\). Let these constraints be

\[
C=g_{\mu\nu}A^\mu A^\nu+1=0,\qquad D=A^\mu U_\mu=0.
\]

In flat zero-shift FLRW spatial coordinates, for arbitrary three-vector spatial aether \(A^i\), auxiliary covector \(U_i\), and \(g_{00}=-N^2, g_{ij}=a^2\delta_{ij}\),

\[
C=-N^2(A^0)^2+a^2\sum_i(A^i)^2+1,\qquad
D=A^0U_0+\sum_i A^i U_i.
\]
The regular future-pointing branch fixes the **two time components algebraically**:

\[
\boxed{A^0=\frac{\sqrt{1+a^2\sum_i(A^i)^2}}N,\qquad
U_0=-\frac{\sum_iA^iU_i}{A^0}.}
\]

The Jacobian of \((C,D)\) with respect to \((A^0,U_0)\) is

\[
\boxed{\det\frac{\partial(C,D)}{\partial(A^0,U_0)}
=-2N^2(A^0)^2\ne0}
\]

near regular future-timelike FLRW, so the implicit-function elimination is locally well-defined. On \(N=1+\epsilon\Psi\), \(A^i=\epsilon v_A^i\), \(U_i=\epsilon v_{Ui}\),

\[
\boxed{\delta A^0=-\Psi,\qquad \delta U_0=0,\qquad
U_0=-\epsilon^2\sum_i v_A^iv_{Ui}+O(\epsilon^3).}
\]

These are exact kinematic statements, not claims that the corresponding normal Euler equations are identically absent.

## 3. Independent chain-rule theorem retains both multipliers and normal Euler equations

Write an otherwise arbitrary complete local covariant action \(S_0[A^\mu,U_\mu,g,\ldots]\), with Lagrange-multiplier extension \(S=S_0+\int\sqrt{-g}(\lambda C+\mu D)\). The gravitational volume factor can be absorbed into the Euler densities when comparing both representations.

Let \(E_z^0\) be the **unconstrained** Euler derivative of \(S_0\). The full normal equations are

\[
E_{A^0}^0+\lambda C_{A^0}+\mu D_{A^0}=0,\qquad
E_{U_0}^0+\mu D_{U_0}=0.
\]

Because their constraint Jacobian is regular, they determine \(\lambda,\mu\). For any tangent variable \(z\in\{A^i,U_i,N,a\}\), the reduced action obtained by substituting \(A^0(A^i,N,a)\) and \(U_0(A^i,U_i,N,a)\) has Euler derivative

\[
\boxed{E_z^{\rm red}
=E_z^0+E_{A^0}^0\,\frac{\partial A^0}{\partial z}
+E_{U_0}^0\,\frac{\partial U_0}{\partial z}.}
\]

The full multiplier Euler equation evaluated on the normal equations is

\[
\boxed{E_z^{\rm full}
=E_z^0+\lambda C_z+\mu D_z
=E_z^{\rm red}.}
\]

The equality is **exact for all three spatial aether components, all three auxiliary spatial components, the lapse and the spatial scale**: 8/8 independent Euler mappings PASS. The test keeps generic, unassigned normal Euler symbols and demonstrates that omitting their contribution from the multiplier or metric chain rule fails. It does not assume that the multipliers or their background values are zero.

This proves there is **no extra freely adjustable normal linear Euler source** merely from writing the two regular algebraic constraints with multipliers. Their effect on the reduced action is captured by the chain rule. It **does not** prove that the full 3+1 reduced field equations match the current CLASS evolution state definition: those are distinct tasks.

## 4. Positive-bath source and the remaining factor-two gate

The original fixed one-mode NL0B completed-square potential depends on the linear transverse combination \(\chi=\varphi+Q\alpha\). Its off-shell variational source remains

\[
\frac{\partial\mathcal L_{\rm bath}}{\partial\alpha}
=-\frac{\eta ak^2Q}{2}B_\chi,\qquad
\frac{\partial\mathcal L_{\rm bath}}{\partial\varphi}
=-\frac{\eta ak^2}{2}B_\chi.
\]

The rank-one scalar–aether source relation is exactly maintained by the constrained representation. Alongside the AeST spatial scalar kinetic Hessian \(2aK_B k^2\), this recovers the previously isolated local source ratio \(-\eta QB_\chi/(4K_B)\). **Do not infer from the algebraic multiplier theorem alone that this is the entire constraint-eliminated CLASS \(E_A'\) source.** The latter requires the full original action's dynamical Euler-to-effective-fluid transformation, temporal constraints and other species.

The frozen original v019j CLASS patch still uses \(-a\eta QB_\chi/(2K_B)\). LW25–LW29 established a conditional discrepancy; LW30 Hamiltonian/momentum and LW31 traceless shear close the **restricted metric** sector. LW32 closes the generic **two algebraic multiplier elimination** step, **not** the full physically normalized source-to-Weyl map. A forceful replacement of the half coefficient in the old frozen CLASS checkout is not licensed.

## 5. Reproducibility and limited future work

Predata: \`ge19/lw32_covariant_aether_auxiliary_multiplier_elimination_predata_20261110.json\`, commit \`e570b9d64e7580ba1651701ff2382a88c9797b72\`, Git blob \`c62f92aa33eba2257210f9da3adb0b238ec8e50b\`. Preliminary calculations preceded the freeze; **not blind preregistration**.

Auditor: \`ge19/lw32_covariant_aether_auxiliary_multiplier_elimination_20261110.py\`, commit \`5c0098f075d54b192338b48242637b9c54923d09\`, Git blob \`b10c7c74e3fd31ed902bc76cd09878c99332cd60\`. **20/20 identical exact SymPy expressions were independently evaluated** in the analysis environment; five unchanged original source Git blobs and two original NL0B constraint anchors verified. The canonical full WSL source-locked run itself is **pending**.

Run once in WSL without CLASS, GGL data or numerical sweeps:

~~~bash
cd ~/aest-memory-gravity
git pull --ff-only
source .venv/bin/activate
python3 -u -m ge19.lw32_covariant_aether_auxiliary_multiplier_elimination_20261110 --self-test
set +e
set -o pipefail
python3 -u -m ge19.lw32_covariant_aether_auxiliary_multiplier_elimination_20261110 \
  --out results/ge19_lw32_covariant_aether_auxiliary_multiplier_elimination_20261110_r1.json \
  2>&1 | tee results/ge19_lw32_r1.log
~~~

Expected symbolic \`GE19_LW32_CONSTRAINED_VARIATION_SYMBOLIC_PASS 20\`, frozen source \`GE19_LW32_SOURCE_LOCKS_PASS 5\` and a **physical CLASS eta evolution OPEN** classification. No new physical detection claim.

**Next single physics decision:** assemble the entire original scalar–aether Euler equations after these exact constraint reductions into the original CLASS \((D_A,T_A,\alpha_A,E_A)\) basis, with temporal Bianchi/source terms. If the old factor half persists without the required action-derived companion, keep it as a demonstrated restricted-model mismatch and implement a **separately versioned** action-consistent variant only after full proof. Do not restart broad CLASS scans or fit DES to resolve a source-normalization question.
