# GE19 LW17 — full scalar Euler current of the frozen combined GE06+GE05 longitudinal action

**Reproducibility erratum (2026-11-10):** The researcher's first canonical WSL run FAILED, `GE19_LW17_EXACT_ACTION_SCALAR_CURRENT_FAIL` (`EXIT=1`), contrary to any implication that the canonical LW17 script had already reproduced the independent symbolic analysis. The code had a SymPy-order bug in two FLRW gates: `sp.simplify(lin_t.subs(ksubs))`/`sp.simplify(lin_x.subs(ksubs))` tries to substitute `K_Q,K_QQ` before nested `Subs(Derivative(K(...)))` is normalized. Fixed as `sp.simplify(lin_t).subs(ksubs)` / same for `lin_x`, commit `8636184113a57f15235037d1a7a25e803309f72d`. Independent SymPy 1.14.0 reconstruction of *all 11 identical gate expressions* now returns 11/11 PASS; both previously false gates are exactly zero with corrected ordering. The fix modifies **no physics expression, model parameter, frozen protocol, or numerical threshold**. Canonical **fixed WSL rerun is still pending**. Original traceback, two failed gates and resolution are archived at `results/ge19_lw17_sympy_false_fail_root_cause_and_fix_20261110.json`, commit `56e0d99b7498726bbe99cc418edbdfefdd584c7e`. The source now prints failed gate names when appropriate. This corrected claim takes precedence over any text below implying standalone canonical-run PASS.


**2026-11-10. Classification:** GE19_LW17_REDUCED_COMBINED_AEST_MEMORY_SCALAR_CURRENT_EXACT_PASS_FULL_CLASS_ACTION_MAP_OPEN.

This is a complete **off-shell scalar** variation of the original analytic **1+1 longitudinal plane-symmetric** AeST (GE06) plus positive NL0B normalized oscillator (GE05) action. It is stronger than the isolated LW16 bath potential Euler variation because it retains the full original scalar temporal current and spatial current from both AeST and memory. **It is not** the complete 3+1 action Euler set, the time-diffeomorphism Noether identity, a full CLASS source map, a global Green function or an astronomical observation.

## Source provenance and reproducibility

Original \`ge06/analytic_aest_directional_source_generator.py\`, Git blob \`a7afe0035054a9dca55d74a6497c081422114b4c\`, original \`ge05/memory_directional_source_generator.py\`, blob \`40837d77f89028da30c28899e2d0530a4401844e\`, and original NL0B analytic theory result \`docs/nl0b_covariant_memory_completion_result.md\`, blob \`d005b1c135fead856510aa76b6174fb9051fa552\`, are the frozen action sources. Original CLASS \`v019\` patch blob \`c78484eb916bfee2730759c0bdc813a706bf9a68\` and \`v019j\` memory patch blob \`14796a5ed9e6265ed6810c792a93d7328a109364\` provide the same source dictionary and 1/2 normalization.

The researcher's actual WSL LW16 JSON (SHA256 \`665de261c6bdc569887f6eadcaf6582b39c3ce3117b95c1b3d8d64baf26d488f\`) was committed byte-identically as \`results/ge19_lw16_scalar_to_velocity_bath_euler_projection_20261110.json\`, commit \`6a2c654f4e2cb533fe383f5b9738beb37f90e610\`, and retains 11/11 exact gates and 7/7 source checks. The previous LW16 independent and LW15 original results remain controls.

LW17 formula protocol \`ge19/lw17_full_reduced_scalar_action_current_predata_20261110.json\` commit \`8f408ba5916e13c77d046694f1b0fe6b9bba5ffd\`, Git blob \`91550bc0bfc9180f0415416f08fab695a54ec277\`, **acknowledges exploratory algebra was available before preregistration**. Canonical source-locked Python \`ge19/lw17_full_reduced_scalar_action_current_20261110.py\` was committed in \`69507f7b504544cfb319e47c663fa2cd03e5104f\` and its inefficient symbolic simplifier was replaced by an equivalent expand-then-reduce exact method in \`d41096fca4c963792fe7c0bc75b970cce9c25fb9\`. **The canonical WSL runner has not yet been executed.** Independent SymPy 1.14.0 derivation and source anchors give **11/11 exact gates PASS, 7/7 literal source anchors found**; archived \`results/ge19_lw17_reduced_combined_scalar_current_independent_symbolic_20261110.json\`, commit \`623fe048dfb52f2c5398a077eaf89873e917a979\`.

## 1. Entire original scalar-dependent 1+1 Lagrangian

The original coframe is \(\theta^0=Ndt,\theta^1=L(dx+b\,dt)\), with transverse area \(R^2\), and aether rapidity \(u\). Let
\[
\sigma=(\phi_t-b\phi_x)/N,\quad
Q_{\mathrm{inv}}=\cosh(u)\sigma+\sinh(u)\phi_x/L,\quad
X=\sinh(u)\sigma+\cosh(u)\phi_x/L.
\]
The original GE06 aether spatial invariant and the GE05 one-mode normalized auxiliary derivative are
\[
E=\cosh(u)\left[(u_t-bu_x)/N+N_x/(NL)\right]
+\sinh(u)\left[(L_t-bL_x-Lb_x)/(NL)+u_x/L\right],
\]
\[
Aq=\cosh(u)(q_t-bq_x)/N+\sinh(u)q_x/L.
\]
The scalar-dependent combined action is
\[
\boxed{\mathcal L=NLR^2\left[
K_B E^2+2C EX-CX^2+2K(Q_{\rm inv})
+\frac{\eta}{4}\{(Aq)^2-(\omega q-\sqrt w X)^2\}
\right],\quad C=2-K_B.}
\]
The GR terms in the original GE06 action contain no \(\phi\) and thus no extra scalar shift current. This is the analytic K(Q) sector with the normalized one-mode physical-eta memory contribution, **not** the complete nonanalytic Y-dependent nonlinear 3+1 theory.

## 2. New exact off-shell scalar current

Only \(\phi_t,\phi_x\), not bare \(\phi\), appear in this action. Define
\[
B_X=wX-\omega\sqrt w q,\qquad
\mathscr A=2C(E-X)-\eta B_X/2.
\]
Without using any field equations, exact independent symbolic differentiation gives
\[
\boxed{J_\phi^t\equiv\partial\mathcal L/\partial\phi_t
=LR^2[2K_Q(Q_{\rm inv})\cosh u+\mathscr A\sinh u],}
\]
\[
\boxed{J_\phi^x\equiv\partial\mathcal L/\partial\phi_x
=NR^2[\mathscr A\cosh u+2K_Q(Q_{\rm inv})\sinh u]-bJ_\phi^t.}
\]
Thus the **complete scalar Euler equation of this original reduced combined action** is
\[
\boxed{\mathcal E_\phi=-\partial_tJ_\phi^t-\partial_xJ_\phi^x=0.}
\]
Auxiliary kinetic \((Aq)^2\) is retained in the action and contributes to its auxiliary Euler dynamics, but does not depend directly on \(\phi_t,\phi_x\). The bath contributes through \(-\eta B_X/2\) in \(\mathscr A\).

## 3. Entire first-order FLRW scalar current

Around \(N=1,L=R=a,b=u=q=0,\phi_t=\bar Q,X=E=0\), use \(\mathcal H_{\rm phys}=\dot a/a\) for **proper/coframe time**, and \(K_Q=I_0/a^3\). For perturbations \(n=\delta N,\ell=\delta L,r=\delta R,z=\delta b,v=\delta u\),
\[
\delta Q_{\rm inv}=\delta\phi_t-\bar Qn,\quad
X_1=\bar Qv+\delta\phi_x/a,\quad
E_1=\delta u_t+\delta N_x/a+\mathcal H_{\rm phys}v,\quad
B_{X,1}=wX_1-\omega\sqrt w\,\delta q.
\]
The exact first-order current is
\[
\boxed{\delta J_\phi^t
=2a^3K_{QQ}(\delta\phi_t-\bar Q n)
+2a^2K_Q(\ell+2r),}
\]
\[
\boxed{\delta J_\phi^x
=a^2[2C(E_1-X_1)+2K_Qv-\eta B_{X,1}/2]
-2a^3K_Q z.}
\]
In particular,
\[
\boxed{\delta J_{\phi,\rm bath}^t=0,\qquad
\delta J_{\phi,\rm bath}^x=-\eta a^2 B_{X,1}/2.}
\]
The bath thus alters the **spatial scalar-current flux** but not its first-order temporal charge density about relaxed homogeneous FLRW. Background shift charge is constant: \(J_{\phi,0}^t=2a^3K_Q=2I_0\).

With Fourier convention \(\partial_x\to ik\), and the original scalar longitudinal normalization \(B_{X,1}=(ik/a)B_{\chi,\rm raw}\),
\[
\boxed{\mathcal E_{\phi,\rm bath}^{(1)}
=-ik\delta J_{\phi,\rm bath}^x
=-\eta ak^2B_{\chi,\rm raw}/2.}
\]
The previous LW16 unweighted local bath variation is \(-\eta(k/a)^2B_{\chi,\rm raw}/2\); multiply by FLRW \(a^3\) to recover exactly the current-Euler result with correct sign and factor.

## 4. Explicit additional Newtonian-gauge projection

Inside the same original reduced longitudinal system, take
\[
N=1+\Psi,\quad L=R=a(1-\Phi),\quad b=0,\quad
v=(ik/a)\alpha,\quad\delta\phi_x=ik\varphi,\quad
\delta q=(ik/a)q_\chi,
\]
and \(\chi=\varphi+\bar Q\alpha\). Then
\[
E_1=(ik/a)(\dot\alpha+\Psi),\quad
X_1=(ik/a)\chi,\quad
B_{\chi,\rm raw}=w\chi-\omega\sqrt w\,q_\chi.
\]
Independent algebraic substitution into the original verified FLRW current gives
\[
\boxed{\delta J_\phi^t
=2a^3[K_{QQ}(\dot\varphi-\bar Q\Psi)-3K_Q\Phi],}
\]
\[
\boxed{\delta J_\phi^x
=ika[2C(\dot\alpha+\Psi-\chi)+2K_Q\alpha-\eta B_{\chi,\rm raw}/2].}
\]
So the **linearized scalar action Euler equation** in this reduced analytic Newtonian-gauge sector is
\[
\boxed{
2\partial_t\left[
a^3\{K_{QQ}(\dot\varphi-\bar Q\Psi)-3K_Q\Phi\}\right]
-k^2a[2C(\dot\alpha+\Psi-\chi)+2K_Q\alpha-\eta B_{\chi,\rm raw}/2]
=0.}
\]
The derivative acts on all time-dependent background coefficients and perturbations. This is a **real new explicit original-action scalar equation**, not merely a restatement of a rank-one bath source or the code's fluid-conservation identities.

**Do not equate it term-by-term to CLASS \(\Theta_A'\)**. The CLASS fluid equations are obtained after imposing the aether, metric, auxiliary, lapse/shift and other field equations, and a full source-to-state change of variables. This action Euler equation alone neither proves a missing CLASS term nor independently certifies the full physical \(J_D,J_T\).

## 5. Checks and physical stop

The actual independent SymPy checks PASS the exact **unexpanded combined action** \(J_\phi^t,J_\phi^x\) formulas, no bare \(\phi\), both linear FLRW currents, vanishing first-order bath charge, nonzero bath flux, Fourier Euler/volume equivalence with LW16, background conserved charge, and missing-bath/wrong-bath-sign negative controls, **11/11**. All seven required original source anchors were located. A generic high-cost trigonometric simplifier initially stalled; the canonical script now uses algebraic expansion followed by targeted \`fu\` trig reduction, independently verified as exact and without changing any physics formula.

**Completed:** whole scalar Euler current for GE06 analytic AeST + GE05 normalized NL0B bath in the frozen 1+1 longitudinal action, including physical first-order bath flux and explicit Newtonian scalar equation.

**Open:** full 3+1 unit-aether and auxiliary multipliers, metric lapse/shift equations and temporal diffeomorphism Noether, all CLASS Einstein/dark-fluid dictionary entries, complete other-species \(A_{\rm eff}\), dynamical admissibility of two histories, full retarded \(G_{WE}\), and observation. LW03 radial quadrature FAIL, LW05 cosmic-shear LOS BLOCK, LW08 differential source response unresolved and H4/Z21 uncertified remain unchanged.

**Next one physics task:** combine this exact scalar current with original GE06/GE05 lapse, shift and aether Euler equations and derive the full temporal Hamiltonian/Bianchi Noether relation **on this same reduced action**, then map its source to the CLASS dark density and momentum variables. Do not repeat numerical CLASS grid sweeps or tune a DES fit to rescue a missing action constraint.

### Optional local zero-CLASS reproduction

~~~bash
set +e
cd ~/aest-memory-gravity
git pull --ff-only
source .venv/bin/activate
python3 -u -m ge19.lw17_full_reduced_scalar_action_current_20261110 --self-test
set -o pipefail
python3 -u -m ge19.lw17_full_reduced_scalar_action_current_20261110 \
  2>&1 | tee results/ge19_lw17_full_reduced_scalar_action_current_20261110.log
~~~

The canonical runner has not been executed in the user's WSL; the independent symbolic calculation and result are already archived on GitHub. No CLASS computation is used.
