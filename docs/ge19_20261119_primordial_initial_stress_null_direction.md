# GE19 — Initial-data stress-map null direction and the physical primordial selection obstruction

19 November 2026. Single action-based algebraic diagnostic. No CLASS, DES, new numerical experiments or observation fit.

**Classification: RESTRICTED_AEST_INSTANTANEOUS_STRESS_MAP_KERNEL_PROVED / DIFFERENT_SCALAR_EVOLUTION_EXHIBITED / FULL_PHYSICAL_PRIMORDIAL_MODE_STILL_OPEN / PHYSICS_BLOCK.**

## 1. The original fixed reduced-action initial stress map

At a finite regular initial time, fixed a,Q,K_B,K_Q,K_QQ,k>0, C=2-K_B and in the same Newtonian-gauge fluid convention as the frozen November GE19 documents:
\`\`\`math
D_A=\frac13\left[QK_{QQ}\,\delta Q-\frac{k^2}{a^2}(K_B E_A+C\chi)\right],
\quad
P_A=\frac{K_Q}{3}\delta Q,\quad
T_A=\frac{K_Q k^2}{3a}\varphi .
\`\`\`
The original relaxed bath has zero direct first-order metric stress. Fix the metric and background, as well as \`varphi\`, ordinary species and their shear/momentum at this initial instant. The linear map from variables \`(\delta Q,E_A,\chi,\varphi)\` to instantaneous \`(D_A,P_A,T_A)\` has a nontrivial kernel whenever K_B != 0, namely for arbitrary epsilon:
\`\`\`math
\boxed{\Delta\delta Q=0,\quad
\Delta E_A=-\frac{C}{K_B}\epsilon,\quad
\Delta\chi=\epsilon,\quad
\Delta\varphi=0.}\tag{1}
\`\`\`
Then \`K_B Delta E_A+C Delta chi=0\`, and thus
\`\`\`math
\boxed{\Delta D_A=\Delta P_A=\Delta T_A=0.}\tag{2}
\`\`\`
This explicitly proves that the *instantaneous stress map* and the Hamiltonian/momentum/shear constraints do **not** separately determine E_A and chi. The kernel vector is not automatically a physical growing adiabatic mode or a solution of the full Cauchy initial-value system: field kinematics, complete aether/scalar Euler constraints, gauge fixing and regularity must also be imposed. Do not mistake (1) for a new independent propagating physical memory degree of freedom.

## 2. The degeneracy is not preserved automatically by scalar evolution

The existing source-locked 14 November reduced scalar equation is
\`\`\`math
\dot\chi=QE_A-3H c_a^2\chi+\frac{c_a^2k^2}{a^2K_Q}(K_B E_A+C\chi-2\Phi)-\frac{3c_a^2}{K_Q}\Omega_s,
\`\`\`
with \`Omega_s=D_s+3aH T_s/k²\` for standard species (or equivalent AeST-fluid Delta expression when its action dictionary holds). With fixed metric, background and ordinary source, insert (1):
\`\`\`math
\boxed{
\Delta\dot\chi
=-\left(\frac{QC}{K_B}+3Hc_a^2\right)\epsilon .
}\tag{3}
\`\`\`
The gradient term is unchanged exactly because the stress-null combination is \`K_B\Delta E_A+C\Delta\chi=0\`. Hence for generic regular coefficients the two instantaneous-stress-equivalent initial states have different *next* scalar evolution. This is an example of why Einstein constraints at one instant do not select the physical primordial state. No claim that this instantaneously allowed stress-map direction survives all differential Euler/Noether constraints.

Kinematic consistency can be imposed locally by choosing \`Delta alpha_A=epsilon/Q\`, \`Delta dot alpha_A=-C epsilon/K_B\` and, with the same initial Psi, a \`Delta dot varphi\` consistent with \`Delta(delta Q)=0\`; there is no algebraic obstruction at one instant. Global physical constraint propagation and primordial regularity are separate issues.

## 3. Direct implication for delayed-only metric onset

For selected retarded no-free-bath initial q=dot q=0, \`B_delayed(t_i+h)=-M2 chi_i h²/2+...\`, with M2=sum w_j omega_j². Consequently the prior **restricted shear-free frozen** metric jet is
\`\`\`math
\Delta W_{\rm hist}(t_i+h)=
\frac{c_{a,i}^2k^2Q_iM_2\chi_i}{960a_i^2}h^5+O(h^6).
\`\`\`
Changing chi_i by epsilon within the stress-map kernel changes this conditional h5 coefficient by
\`\`\`math
\boxed{
\Delta[\mathrm{coeff}_{h^5}\,W_{\rm hist}]
=\frac{c_{a,i}^2k^2Q_iM_2}{960a_i^2}\epsilon.
}\tag{4}
\`\`\`
This establishes *sensitivity of a reduced memory prediction to an instantaneous-stress-invisible initial variable*, not that both initial data lie on the physical cosmological adiabatic branch or that such a variation is observable. Under genuine primordial selection the allowed epsilon may be fixed to zero, or the entire stress-null direction may be removed.

## 4. Scientific decision

**New proved restricted algebra:** nontrivial kernel (1), zero stress variation (2), different scalar evolution (3) and conditional difference of delayed jet (4).

**What this actually identifies as the missing proof:** the full action's finite-k radiation-era *initial-data constraint/regularity eigenproblem*, not another Einstein stress constraint or bath passivity theorem. A prescribed fluid Delta_A, leading k tau adiabatic relation, and zero free-bath q/p are insufficient on their own to fix the full chi/E initial values.

**PHYSICS_BLOCK remains:** the unreduced full action/multiplier scalar-aether Ward system, physical growing mode and all-species Weyl transfer have not been jointly certified. Do not claim nonzero physical memory detection or forecast from (4). The existing MagLim4 x Source4 DES Y3 geometric work is ready for Asimov only after physical transfer acceptance.

## Sources
- [Original frozen action stress/phase dictionary](ge19_20261111_joint_action_to_CLASS_scalar_source_matrix.md)
- [Original all-species projected scalar source](../ge19/physics_gate/constraint_projected_joint_operator_20261112.py)
- [General h5/h6 onset](ge19_20261119_general_initial_chi_delayed_weyl_h5_vs_h6.md)
- [Finite-k primordial mode scope](../ge19/physics_gate/frozen_exp_superhorizon_growing_mode_20261111.py)
- [Single return-to-observability gate](ge19_20261119_observability_return_single_gate_decision.md)
