# GE19 — First nonzero delayed metric jet in the frozen constrained AeST scalar operator

19 November 2026. One analytic continuation of the existing, frozen \`ge19/physics_gate/constraint_projected_joint_operator_20261112.py\`. No CLASS, DES, new numerical transfer, arbitrary parameter scan or significance claim.

**Classification: FROZEN_REDUCED_AEST_ONLY_DELAYED_METRIC_NONZERO_LEADING_JET_PROVED_CONDITIONALLY / FULL_PHYSICAL_WEYL_NOT_PROVED / OBSERVABILITY_BLOCK.**

## 1. Exact scope

Take the existing frozen *AeST-only* four-state symbolic operator \`Y=(Phi,varphi,chi,E_A)^T\` from \`constraint_projected_joint_operator_20261112.py\`, with constant or smooth regular coefficients at the initial instant, zero AeST-only shear, and a prescribed external original reduced-fluid driving history \`Delta_A(t)\`. The source is the original quarter-normalized longitudinal action coupling at first order in eta; the finite positive bath has \`q_j(t_i)=dot q_j(t_i)=0\`.

The relevant original matrix entries are
\`\`\`math
\dot\Phi=-H\Phi+\frac{K_Q}{2}\varphi,\qquad
\dot\varphi=\ldots+gK_BE_A,\qquad
g=\frac{c_a^2k^2}{a^2K_Q}.
\`\`\`
This is **not** a completed full Einstein–AeST–NL0B all-species dynamical operator. In particular \`Delta_A\` is externally prescribed for the earlier local-onset theorem, not the jointly solved physical growing mode. The frozen local approximation is meaningful at a regular finite \`t_i\`; it cannot be extrapolated to the big-bang singular limit.

Let the zero-eta baseline satisfy initial \`chi_i=E_{A,i}=q_{j,i}=dot q_{j,i}=0\` and \`D_i=dot chi_0(t_i)=Q_i c_{a,i}^2 Delta_{A,i} != 0\`. Let \`M_2=sum_j w_j omega_j^2>0\`. Assume \`Q_i,K_B,K_{Q,i},g_i\` are finite and nonzero.

As in the original 14 November theorem, define the **first-order source-decomposition difference** between full-retarded and instantaneous-stiffness-only forcing, with *the same eta=0 trajectory*, same initial tangent and same frozen operator. It is a mathematical comparator, not a second physical action. Denote the difference by \`delta_h\`.

## 2. First nonzero delayed source

The prior exact local Taylor coefficient gives
\`\`\`math
B_{\rm delayed}(t_i+h)=-\frac{D_i M_2}{6}h^3+O(h^4).
\`\`\`
Consequently the difference of the **cosmic-time** E-row sources is
\`\`\`math
f_{E,\rm hist}(t_i+h)
=-\frac{Q_i}{4K_B}B_{\rm delayed}(t_i+h)
=\frac{Q_iD_iM_2}{24K_B}h^3+O(h^4).
\`\`\`
This is the derivative in eta at zero, not the full finite-eta source.

## 3. A nonzero metric Taylor coefficient in the restricted frozen operator

The difference state solves \`dot(delta_h Y)=A_0 delta_h Y+e_E f_{E,hist}\`, with zero initial difference. From the actual original frozen four-state matrix entries,
\`\`\`math
e_\Phi^T e_E=0,\qquad e_\Phi^T A_0 e_E=0,\qquad
e_\Phi^T A_0^2e_E=\frac{K_QgK_B}{2}.
\`\`\`
The last factor is **nonzero when** \`K_Q,g,K_B\` are nonzero. This is a rigorous structural source-to-metric coupling in the *restricted frozen operator*. It does **not** prove the same Markov coefficient for a complete full-physics projected operator, which may have additional algebraic constraint mappings or cancellations.

Using the Duhamel series, the leading metric source difference is
\`\`\`math
\begin{aligned}
\delta_h\Phi(t_i+h)
&=\frac{K_QgK_B}{2}\frac{Q_iD_iM_2}{24K_B}
\int_0^h\frac{(h-s)^2}{2}s^3\,ds+O(h^7)\\
&=\boxed{\frac{K_{Q,i}g_iQ_iD_iM_2}{5760}h^6+O(h^7)}\\
&=\boxed{\frac{c_{a,i}^2k^2Q_iD_iM_2}{5760a_i^2}h^6+O(h^7)}.
\end{aligned}
\`\`\`
Here the integral is \`h^6/120\`. Smooth time-dependent coefficients produce the same leading coefficient when their initial values are used, provided the causal jet exists; all coefficient time-derivative corrections enter at higher order. If \`D_i\` itself scales with k under physically constrained primordial conditions, the actual long-wavelength order is correspondingly higher.

For zero AeST-only anisotropic shear, the *restricted Einstein* relation is \`Psi=Phi\`, hence \`W=(Phi+Psi)/2=Phi\` and the same local h^6 coefficient gives a nonzero **restricted metric/Weyl** delayed perturbation for sufficiently small h>0.

**Important nuance:** Nonzero at sufficiently early h does not imply nonzero at a later DES lens redshift, where oscillatory or multi-species cancellations are allowed. This theorem is also conditional on the externally supplied reduced fluid source and the same-aether-only constrained operator, and therefore does **not** certify a physical adiabatic growing cosmological mode, the full scalar Ward identity, or any observer.

## 4. Meaning for observability

This resolves one narrowly stated question: in the already archived reduced frozen AeST-only operator, the noninstantaneous bath memory *does* reach the metric with a computable nonzero leading coefficient. The earlier mere structural statement \`K_B E/2\` is sharpened into a local causal nonzero metric jet within that same restricted state space.

It **does not** resolve the truly physical source, which must supply \`D_i\` from the full finite-k radiation-era growing eigenvector. The small \`c_a²\` coefficient in the Exp benchmark and the additional k² suppression are relevant but do not define a DES sensitivity without all-species transfer, normalization and numerical error. Do not substitute the previous one-point native W1 (instantaneous+delayed) as this new delayed-only amplitude.

**Final decision:** restricted local delayed-Weyl response: conditional nonzero theorem. Full physical full-action/primordial/observer equivalence: OPEN. Return to DES Asimov only after this one full gate; do not open a new series of LW stages.

## Frozen references

- [Original frozen projected symbolic operator](../ge19/physics_gate/constraint_projected_joint_operator_20261112.py)
- [Original delayed-onset h^4 aether theorem](ge19_20261114_noether_constraint_and_eta0_retarded_branch_theorems.md)
- [Action stress and scalar dictionary](ge19_20261111_joint_action_to_CLASS_scalar_source_matrix.md)
- [All-species primordial initial-state BLOCK](ge19_20261111_all_species_Einstein_operator_and_adiabatic_IC_block.md)
- [Physical Weyl cancellation identity](ge19_20261115_constraint_eliminated_weyl_memory_cancellation_identity.md)
- [Observability return decision](ge19_20261119_observability_return_single_gate_decision.md)
