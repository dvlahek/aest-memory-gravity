# GE19 — physics-first verdict on the full-CLASS matter-memory tangent

**13 November 2026 | canonical branch \`physics-first-gravitational-elasticity\`**

**Classification:** \`RESTRICTED_ACTION_MEMORY_SOURCE_SUPPORTED / RETARDED_BRANCH_CONDITIONAL / PRIMORDIAL_ADIABATIC_PROXY_NOT_EXACT / FULL_ACTION_AND_WARD_UNCERTIFIED / FULL_CLASS_W1_NONZERO_SMALL / OBSERVABILITY_BLOCK\`

This is a **physical decision derived from frozen existing evidence**, not a fresh numeric or symbolic microcampaign. It introduces **no** new CLASS run, mode selection, eta scan, nuisance tuning or DES analysis. The aim is to decide what the reported native full-hierarchy \(\partial_\eta W\) actually demonstrates and what cannot presently be claimed.

## 1. Exact restricted action result: the quarter source is necessary under the frozen dictionary

The original reduced GE05/NL0B longitudinal action per positive auxiliary node, on relaxed FLRW, is

\[
L_{{\rm bath},j}^{(2)}
=\frac{\eta a^3}{4}\Bigg[
\dot q_j^2-
\left(\omega_jq_j-\sqrt{w_j}\frac{k\chi}{a}\right)^2
\Bigg],\qquad
\chi=\varphi+Q\alpha_A.
\]

For \(\eta>0\), varying \(q_j\) gives the retarded-oscillator equation
\[
\ddot q_j+3H\dot q_j+\omega_j^2q_j
=\omega_j\sqrt{w_j}\frac{k\chi}{a}.
\]
With \(B_\chi=\sum_j[w_j\chi-a\omega_j\sqrt{w_j}\,q_j/k]\), the bath term produces
\[
\frac{\partial L_{\rm bath}^{(2)}}{\partial\alpha_A}
=-\frac{\eta ak^2Q}{2}\,B_\chi.
\]
The independently derived AeST electric kinetic Hessian is \(2aK_Bk^2\), so the action-derived E-row candidate in conformal time has precisely
\[
\boxed{\Delta E_A'=-\frac{a\eta Q}{4K_B}B_\chi.}
\]
This is the *restricted longitudinal linear-action* result, not yet the covariant all-sector/aether-multiplier proof. Original historical v019j used a half coefficient, twice this value; the *isolated* full-CLASS tangent experiment used the quarter candidate without changing the historical original.

The already independently checked LW33 residual identity gives (using the frozen density and phase dictionary, and **only when** scalar Ward plus other component residuals are imposed)
\[
\dot R_\rho+3HR_\rho
=\frac{\eta Qk^2B_\chi}{12a^2}(1-4\gamma),
\quad R_\rho=D_A-D_A^{\rm action}.
\]
For \(\gamma=1/4\) and \(R_\rho(t_i)=0\), this reduced compatibility condition preserves \(R_\rho=0\). For \(\gamma=1/2\) it generally forces a nonzero drift. **Neither the conditional identity nor a CLASS conservation PASS independently proves the action's scalar Euler equation in the entire modified CLASS implementation.**

Source: [joint reduced action/source matrix](ge19_20261111_joint_action_to_CLASS_scalar_source_matrix.md), [original GR+AeST ADM constraints](ge19_lw30_original_gr_aest_adm_scalar_constraints_class_bridge_2026-11-10.md).

## 2. Quantified primordial adiabatic defect: real but *parametrically tiny* for frozen Exp

At linear order, adiabaticity between a separately conserved pressureful AeST effective component and photons requires
\[
\frac{\delta_A}{1+w_A}=\frac34\,\delta_\gamma,\qquad w_A=\frac{p_A}{\rho_A}.
\]
The exact original v019/v019j CLASS initial-state code inherits the ordinary CDM initialization and Newtonian gauge transform as if \(w_A=0\):
\[
\delta_A^{S,{\rm code}}=\frac34\delta_\gamma^S,\quad
\delta_A^{N,{\rm code}}=\frac34\delta_\gamma^S-3\mathcal H\alpha,\quad
\delta_\gamma^N=\delta_\gamma^S-4\mathcal H\alpha.
\]
An immediate exact simplification gives the gauge-invariant relative entropy defect:
\[
\boxed{
S_{A\gamma}^{\rm code}\equiv
\frac{\delta_A^{N,{\rm code}}}{1+w_A}-\frac34\delta_\gamma^N
=-\frac{3w_A}{4(1+w_A)}\,\delta_\gamma^N.
}
\]
Thus the inherited CLASS initial condition is not *exact* for generic \(w_A\ne0\). But the coefficient may be extremely small; its magnitude must not be exaggerated or assumed to explain the measured W1.

The **frozen Exp background**, as implemented in original [v019/patch/source/aest_memory.c](../v019/patch/source/aest_memory.c), is
\[
K_Q=\frac{I_0}{a^3},\quad
Q=Q_0+Z_0Z,\quad
K_Q=4K_2Z_0Z e^{Z^2},\quad
K=2K_2Z_0^2(e^{Z^2}-1),
\quad w_A=\frac{K}{QK_Q-K}.
\]
We can eliminate the exponential **algebraically**:
\[
\boxed{K=\frac{Z_0K_Q}{2Z}-2K_2Z_0^2},
\qquad
Z^2=\frac12\operatorname{LambertW}
\left(2\left[\frac{I_0}{4K_2Z_0a^3}\right]^2\right).
\]
With the previously **frozen**, source-locked benchmark constants
\(Q_0=10^{-4}\), \(K_2=9500\), \(Z_0=10^{-17}\),
\(I_0=0.000400912849822208377004114\), evaluating these *background algebraic expressions*, **not integrating CLASS**, yields:

| Background epoch | \(Z\) | \(w_A\) | \(c_a^2\) |
|---|---:|---:|---:|
| Native CLASS baseline start, \(a=2.251984948309577\times10^{-6}\) | 7.599986042 | \(6.5789594512\times10^{-15}\) | \(6.5224971837\times10^{-15}\) |
| \(z=19,\ a=0.05\) | 5.300586570 | \(9.4329182889\times10^{-15}\) | \(9.2679853195\times10^{-15}\) |
| \(z=0.5,\ a=2/3\) | 4.525861901 | \(1.1047619444\times10^{-14}\) | \(1.0784373135\times10^{-14}\) |
| Today, \(a=1\) | 4.392819968 | \(1.1382210096\times10^{-14}\) | \(1.1094735110\times10^{-14}\) |

At the native initial epoch,
\[
S_{A\gamma}^{\rm code}/\delta_\gamma^N
=-4.9342195884\times10^{-15}\quad \text{(approximately)}.
\]
**New scientific interpretation:** the initial-condition error is demonstrably a structural defect, *but at leading entropy order it is suppressed by only \(\sim5\times10^{-15}\) per unit initial photon perturbation in the frozen Exp model*. It is **not justified** to claim on this evidence that such a small defect explains the later W1. Conversely, even a tiny primordial defect could potentially be amplified by a growing mode, so the absence of a propagated retarded/adiabatic error bound still prohibits full physical certification. A *true finite-k growing eigenvector*, beyond this necessary leading adiabatic relation, is not established.

The original 11 Nov source review derived the defect condition exactly but did not evaluate actual \(w_A(t_i)\) in the then-unexecuted CLASS run. The presently archived baseline supplies its initial scale factor, allowing this narrower algebraic estimate with no new CLASS run.

Sources: [full-species early-state decision](ge19_20261111_all_species_Einstein_operator_and_adiabatic_IC_block.md), [source-locked frozen Exp calibration](../results/ge19_exp_local_growth_interval_20261112_wsl.json), [native full-CLASS baseline inspection](../results/ge19_existing_traces_inspection_20261113.log).

## 3. No-free-bath initial state is a **branch choice**, not a theorem

The positive auxiliary oscillator has nonzero regular homogeneous modes, including the explicitly constructed \(t^{-1/4}J_{1/4}(\omega t)\) solution in radiation domination. Therefore \(\chi_i=0\) and regularity do **not** alone force \(q_j=p_j=0\); zero auxiliary initial data select the *no-free-bath-mode* retarded history starting at a finite \(t_i\). Since the quadratic auxiliary action carries overall \(\eta\), it is degenerate at \(\eta=0\) and the \(\eta\to0^+\) derivative has meaning only in the specified continuous physical branch.

The existing 141,494-point baseline correctly preserves the selected auxiliary evolution *from \(a_i=2.25\times10^{-6}\) onward*; it does **not** retroactively reconstruct a unique history from \(t=0\), nor derive absence of primordial homogeneous bath perturbations from covariant dynamics. This is a conditional initial-state hypothesis rather than a universal prediction of the theory.

Source: [physical auxiliary initial-mode and observer decision](ge19_20261111_auxiliary_initial_state_and_physical_observer_decision.md).

## 4. One-point W1: computed source response, not the growing mode or lensing sensitivity

The exact researcher source-locked and archived [native full-CLASS result](../results/ge19_one_forced_tangent_20261113/GE19_ONE_FORCED_TANGENT_SCREEN.json) and [13-point W1 CSV](../results/ge19_one_forced_tangent_20261113/forced_single_W1.csv) report, at the predeclared \(k=0.1h/{\rm Mpc}\), \(z=0.5\):
\[
W_0=0.07009097715416947,\quad
\left.\partial_\eta W\right|_0=1.8390770226818281\times10^{-9},\quad
\frac{W_1}{W_0}=2.6238427503110188\times10^{-8}.
\]
The null control is exactly zero over its 13 output samples. The \(z=0.5\) W1 is a *linear interpolation* between the nearest two CLASS output times; alternative local interpolants of the same existing samples differ by about 2%, which is *not* a rigorous ODE error estimate. The result is \`GE19_ONE_FORCED_NATIVE_CLASS_TANGENT_PROVISIONAL_ONLY\`, not action/Ward/numerically certified.

For a single *real* deterministic scalar Weyl transfer with fixed primordial spectrum and no mode mixing, the purely algebraic **conditional** identity
\[
\left.\frac{\partial_\eta P_{WW}}{P_{WW}}\right|_0
=2\,\frac{W_1}{W_0}
=5.2476855006220376\times10^{-8}\quad\text{per unit }\eta
\]
holds **at this k,z only**. It is NOT a survey-sensitivity prediction, since the projection over k/z, physical galaxy transfer, full action consistency, primordial perturbations and covariance are open. At illustrative \(\eta=0.01\) this conditional single-point power response is about \(5.25\times10^{-10}\), but no finite-eta run or DES fit supports that extrapolation.

The separate reduced local frozen instability analysis proves only a conditional positive eigenvalue of a small subsystem with externally fixed \(\Delta_A\). In that analysis
\[
\partial_\eta\lambda
=-\frac{Q\,\mathcal W(\lambda)}{4F'(\lambda)}\le0
\]
for a simple positive real root and positive bath. **The positive memory bath may damp an already-existing local growth branch; it does NOT demonstrate that gravitational memory *creates* an observable growing mode.** The all-species, constrained, finite-k mode spectrum has not been derived.

Sources: [conditional root physics](ge19_20261112_frozen_coupled_scalar_bath_gain_conditional_root.md), [final original W1 audit](ge19_20261113_one_forced_native_class_tangent_final_artifact_audit.md).

## 5. Scientific disposition, not a new computational worklist

1. **Already supported:** reduced longitudinal Einstein+AeST+NL0B quadratic action, passive positive retarded bath and its quarter-normalized source *under the stated field/dictionary assumptions*; independent finite-bath source algebra; implemented nonzero, one-point native full-CLASS Weyl tangent.
2. **Not supported:** unique primordial physical no-free-bath mode, exact pressureful adiabatic source initialization, complete all-species action-to-CLASS and Ward-propagation equivalence, certified numerical uncertainty for W1, true full cosmological growing mode or gauge-invariant galaxy–Weyl DES likelihood/detection.
3. **Consequence for science:** the tiny one-point signal gives no present basis for a headline lensing discovery. Its existence is a useful **computational feasibility demonstration** and *not* an observational effect or a universal amplitude bound. The strongest publishable route is a carefully delimited **theoretical paper on causal gravitational memory, original action, retarded bath and conditional scalar response**, with explicit discussion of full cosmological initial conditions and observability as open. A second, observational study is justified only after those independent physical assumptions are closed **without fitting the theory to data**.

**Decision:** close the CLASS execution/patch loop. No more numerical PASS campaigns or after-the-fact eta/k/z search. The next intellectual task is *writing the scientifically bounded theoretical claim and its proofs* using existing results, not inventing a detection or promoting one k/z tangent into a lensing discovery. All existing original source/code/data remain unchanged.
