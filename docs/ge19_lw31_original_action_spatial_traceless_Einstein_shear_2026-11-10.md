# GE19 LW31 — original Einstein+AeST+NL0B traceless spatial Euler bridge

**Date: 2026-11-10.** Independent reduced-action SymPy calculation: **15/15 exact algebraic checks PASS**. The newly committed source-locked WSL runner has **not** yet been executed by the researcher. This closes a scalar spatial-shear *equation only in the plane-symmetric linear analytic GE06+GE05 coframe*. Full covariant 3+1 AeST/Y, ordinary species, unit-aether/auxiliary multipliers, physical eta-normalized matter–Weyl response and observational memory detection are **not certified**.

## 1. Original LW30 user WSL evidence and provenance

Original user-uploaded WSL result \`ge19_lw30_exact_adm_hamiltonian_momentum_constraints_20261110_r1.json\`: 2,902 bytes, SHA-256 \`cb09073a4bcfa2f18e003d4cfba08ac08fda315784a6105338d464b9a47fdfbc\`, Git blob \`53e1d2d021d60d9a17464c5c2894f789cb4cf1be\`.

Original \`ge19_lw30_r1.log\`: 361 bytes, SHA-256 \`315326add7bfb7019464ec850dad47cb51ea309e778e208a64646d867ebe1f04\`, Git blob \`456de26a8f02d6e299d5d94481776d9a5bad7441\`.

Both original files were archived on GitHub, with **byte-identical readback Git blobs**. LW30 on researcher WSL reported **17/17 symbolic PASS, 6/6 frozen source locks PASS**, classification \`...ADM_SCALAR_CONSTRAINTS_PASS_FULL_ACTION_TO_CLASS_OPEN\`. Repeated LW29 uploads were unchanged from the archive.

## 2. Derive both metric spatial variations before fixing the gauge

The original plane-symmetric 3+1 GR action after its frozen spatial integration by parts is
\[
\mathcal L_{\mathrm{GR}}
=NLR^2(-4k_Lk_R-2k_R^2)
+\frac{2NR_x^2}{L}+\frac{4N_xRR_x}{L}.
\]
The original analytic AeST sector is
\[
\mathcal L_A=NLR^2[K_BE^2+2(2-K_B)EX-(2-K_B)X^2+2K(Q_{\rm inv})],
\]
and the original GE05 NL0B auxiliary bath contributes
\[
\mathcal L_{\rm bath}=\frac{\eta NLR^2}{4}
[(Aq)^2-(\omega q-\sqrt w X)^2].
\]

Define complete first-jet spatial Euler equations
\[
E_L=\partial_L\mathcal L-\partial_t\partial_{L_t}\mathcal L-\partial_x\partial_{L_x}\mathcal L,\quad
E_R=\partial_R\mathcal L-\partial_t\partial_{R_t}\mathcal L-\partial_x\partial_{R_x}\mathcal L.
\]
Since \(R\) represents two transverse directions, the **traceless** spatial Euler combination is
\[
\boxed{\mathscr S=L E_L-\frac R2 E_R}.
\]
Vary independently in \(L\) and \(R\), **then** impose Newtonian gauge \(N=1+\Psi\), \(L=R=a(1-\Phi)\), \(b=0\) and scalar Fourier \(e^{ikx}\). Its first perturbative coefficient must include the background spatial Euler amplitudes (they cancel in the anisotropic combination).

## 3. Exact symbolic result, including GR curvature and background dependence

For the original GR action, without imposing the background Friedmann equation,
\[
E_{L,0}^{\rm GR}=2a^2(3H^2+2\dot H),\qquad
E_{R,0}^{\rm GR}=4a^2(3H^2+2\dot H).
\]
For AeST, \(E_{L,0}^A=2a^2 K(Q)\), \(E_{R,0}^A=4a^2K(Q)\); the bath has zero background spatial Euler.

The full first-order **traceless** result is
\[
\boxed{\mathscr S_{\rm GR}^{(1)}=2ak^2(\Phi-\Psi)},\quad
\boxed{\mathscr S_A^{(1)}=0},\quad
\boxed{\mathscr S_{\rm bath}^{(1)}=0}.
\]
Hence, in the **restricted AeST-only linear scalar sector with no other anisotropic stress**,
\[
\boxed{\mathscr S_{\rm total}^{(1)}=0\ \Longrightarrow\ \Phi=\Psi\quad (k\neq0).}
\]
The bath has no *direct* linear shear source, but it can change \(\Phi\) and \(\Psi\) indirectly by changing the scalar/aether state. The corresponding restricted Weyl definition \(W=(\Phi+\Psi)/2\) becomes \(W=\Phi\), **not** a new computed physical Weyl transfer.

**Physical caveat:** the real multi-species CLASS universe includes shear sources (e.g. free-streaming neutrinos). This action-only result cannot impose \(\Phi=\Psi\) on the full DES cosmology, nor does it include full 3+1 perturbations or Y-nonanalytic sector.

## 4. Deliberate original-action negative controls

Omitting the **actual** GR term \(4N_xRR_x/L\) gives the incorrect \(2ak^2\Phi\), losing the \(\Psi\) term. Omitting \(2NR_x^2/L\) gives the incorrect \(-2ak^2\Psi\), losing the \(\Phi\) term. Halving the shear coefficient also fails. The original GR action was left intact in the committed code; these changes only exist inside algebraic negative controls.

The **15 local SymPy gates** check separate GR/AeST background isotropy, bath background zero, exact GR/AeST background expressions, full GR slip, AeST and bath zero direct stress, their total, its on-shell consequence for nonzero k, cancellation of Hdot, k parity, and the three negative controls.

## 5. Relationship to the factor-two open problem

LW30 closed the **restricted action-to-CLASS Hamiltonian and momentum metric equations**. LW31 adds the **restricted spatial traceless/shear metric equation**. This is genuine progress in the Einstein *metric* half of the observer pipeline.

The remaining **decisive** obstruction is the complete scalar/aether/unit-norm/auxiliary-orthogonality field-equation-to-effective-fluid mapping. The earlier scalar quadratic action still gives an inhomogeneity \(-a\eta QB_\chi/(4K_B)\), while the original frozen v019j patched CLASS E-row uses \(-a\eta QB_\chi/(2K_B)\). Neither LW30 nor LW31 removes this normalization discrepancy. No ad hoc changes were made to original v019j. The LW22 DES Y3 source geometry remains PASS; LW08 differential matter–Weyl signal and physical \(\partial_\eta P_{\delta W}\), full GGL angular \(\gamma_t\), nuisance marginalization and observation remain unavailable.

## 6. Reproducibility

Question/provenance lock created after preliminary exploratory algebra:
\`ge19/lw31_action_spatial_traceless_shear_predata_20261110.json\`, commit \`76cb1c30eba956b5f05645d0751530c4733ef3c2\`, Git blob \`f0236ab323b286efb0dd325d2ab99e11b2c47629\`. **Not** an independent blind preregistration.

Canonical Python auditor: \`ge19/lw31_action_spatial_traceless_shear_20261110.py\`, initial commit \`41d74a3101dc8c25c3c2cc03cef47b83b252ed7a\`, Git blob \`6e41aebf8fdd4f1bc3339e92b9183fecb1503ed3\`. It has five frozen original source blob locks and requires the **actual original LW30 JSON SHA**. A separate local SymPy replay of its exact spatial Euler formula and the negative controls passed **15/15**, while **researcher WSL execution is pending**.

Run without CLASS, H4, new numerical sweeps or observed DES data:

~~~bash
cd ~/aest-memory-gravity
git pull --ff-only
source .venv/bin/activate
python3 -u -m ge19.lw31_action_spatial_traceless_shear_20261110 --self-test
set +e
set -o pipefail
python3 -u -m ge19.lw31_action_spatial_traceless_shear_20261110 \
  --out results/ge19_lw31_action_spatial_traceless_shear_20261110_r1.json \
  2>&1 | tee results/ge19_lw31_r1.log
~~~

Expected labels \`GE19_LW31_ACTION_TRACeless_SHEAR_SYMBOLIC_PASS 15\`, \`GE19_LW31_SOURCE_LOCKS_PASS 5\`, classification \`...TRACeless_SHEAR_PASS_FULL_ACTION_BRIDGE_OPEN\`. Do not claim local execution success before the WSL evidence arrives.

**Next physics priority:** finish the *combined off-shell scalar/aether/unit-aether multiplier and auxiliary-orthogonality Euler-to-fluid mapping* in the full original covariant action. Only if the eta factor is determined without changing old provenance should a clearly versioned action-consistent CLASS branch and true physical DES lensing detectability test be attempted.
