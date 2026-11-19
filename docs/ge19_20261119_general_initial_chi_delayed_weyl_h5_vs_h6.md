# GE19 — General retarded initial-state jet: h5 or h6, and why the physical primordial amplitude is decisive

19 November 2026. Physics-first analytic correction and refinement of the frozen 19 November h6 metric result. No CLASS/DES runs, fitting or new cosmological numerical campaign.

**Classification: RESTRICTED_REDUCED_GENERAL_INITIAL_CHI_H5_THEOREM / SPECIAL_ZERO_CHI_H6_THEOREM_RETAINED / FULL_PHYSICAL_FINITE_K_INITIAL_MODE_OPEN / NO_OBSERVABILITY_GO.**

## Frozen equations and comparison

Use the **same** original reduced positive finite NL0B oscillator bath and the same restricted/frozen AeST-only four-state operator as in the archived h6 note, with cosmic-time variable h=t-ti, a_i>0 and regular background at finite ti. With no free-bath data q_j(ti)=dot q_j(ti)=0,
\`\`\`math
\ddot q_j+3H\dot q_j+\omega_j^2q_j
=\omega_j\sqrt{w_j}\,\frac{k\chi}{a}.
\`\`\`
Let M2=sum_j w_j omega_j² >0. The instantaneous comparator B_inst=Wb chi is a *first-order source decomposition*, not an independently postulated physical action. The history-only source difference is
\`\`\`math
B_{\rm delayed}=-\frac{a}{k}\sum_j\omega_j\sqrt{w_j}\,q_j,
\qquad f_{E,\rm hist}=-\frac{Q}{4K_B}B_{\rm delayed}
\`\`\`
in the frozen cosmic-time E-tangent normalization. Both comparison problems have the same eta=0 physical baseline, initial first-order tangent and retarded bath history.

At ti, regardless of the finite value chi_i,
\`\`\`math
q_j''(t_i)=\omega_j\sqrt{w_j}\,k\chi_i/a_i.
\`\`\`
Therefore for **nonzero chi_i**,
\`\`\`math
\boxed{B_{\rm delayed}(t_i+h)
=-\frac12 M_2\chi_i h^2+O(h^3),}
\qquad
\boxed{f_{E,\rm hist}(t_i+h)
=\frac{Q_i M_2\chi_i}{8K_B}h^2+O(h^3).}
\`\`\`
This h2 delayed force is a general retarded onset under these selected initial conditions; it does **not** imply any small-time physical observer mode without the full constraints.

For **chi_i=0** with D_i=dot chi_0(ti) !=0, the earlier special result is
\`\`\`math
B_{\rm delayed}(t_i+h)=-M_2D_i h^3/6+O(h^4),
\qquad f_{E,\rm hist}(t_i+h)=Q_i M_2D_i h^3/(24K_B)+O(h^4).
\`\`\`

## Restricted metric onset: exact leading coefficients

From the source-locked 12 November frozen restricted four-state operator Y=(Phi,varphi,chi,E_A), with g_i=c_ai² k²/(a_i² K_Qi),
\`\`\`math
e_\Phi^\mathsf T e_E=0,\qquad
e_\Phi^\mathsf T A_0e_E=0,\qquad
e_\Phi^\mathsf T A_0^2e_E=K_{Q,i}g_iK_B/2.
\`\`\`
Hence the impulse response leading term is (K_Q g K_B/4)(h-u)^2. Evaluate exactly
\`\`\`math
\int_0^h\frac{(h-u)^2}{2}u^2du=h^5/60,
\qquad
\int_0^h\frac{(h-u)^2}{2}u^3du=h^6/120.
\`\`\`

**General finite nonzero initial chi_i, restricted shear-free operator**:
\`\`\`math
\boxed{
\delta_h W(t_i+h)=\delta_h\Phi(t_i+h)
=\frac{c_{a,i}^2k^2 Q_i M_2 \chi_i}{960a_i^2}h^5+O(h^6).
}\tag{1}
\`\`\`

**Special exact initial chi_i=0, D_i !=0, same restricted operator**:
\`\`\`math
\boxed{
\delta_h W(t_i+h)=\delta_h\Phi(t_i+h)
=\frac{c_{a,i}^2k^2 Q_i M_2 D_i}{5760a_i^2}h^6+O(h^7).
}\tag{2}
\`\`\`
These formulas are first-order eta derivatives of delayed-only metric source-decomposition differences, not absolute finite-eta metric shifts. Coefficient time derivatives, other four-state couplings and residual variations enter at the displayed higher orders for a smooth finite-ti linear evolution.

## All-species Einstein constraint caveat

In the archived all-species symbolic source operator, \`Phi_dot = K_Q varphi/2 + 3a T_s/(2k²) - H Psi\`, \`Psi=Phi-9a² S_s/(2k²)\`. The source E has **no direct linear bath stress** in the original reduced relaxed FLRW state. If each ordinary minimally coupled species' shear and momentum respond causally only via the metric and its own stress hierarchy, and the physical source projection preserves exactly these rows, the leading source-to-Phi two-step path is compatible with an all-species extension. In such a conditional extension, no immediate photon/neutrino E-source exists. Nevertheless, this document **does not** equate its AeST-only shear-free W coefficients with the true neutrino-containing gauge-invariant W: ordinary species, metric constraints and physical initial modes must be included and verified before such a claim.

For the genuine physical growing adiabatic branch, the previous leading \`k tau->0\` proxy gives chi=0 at leading order only, **not** chi_i=0 at a fixed nonzero k and finite ti. Subleading chi_i and the eta derivative of its allowed primordial initial state can matter at precisely the leading history-only order. The radiation/neutrino test-fluid value of Delta_A is not enough to decide between (1) and (2) because the full physical state can have chi_i !=0.

The previously proposed strong statement that the *physical* delayed Weyl onset must be h6, or must inherit two factors of c_a² and be too small for DES, is **not established**. It is a proxy restricted-channel inference only.

## One remaining decision, not a theorem treadmill

Starting from the fixed original full covariant action, derive the finite-k adiabatic growing state at a declared finite ti, including chi_i, E_i, q_i, p_i and its one-sided eta derivative, with lapse/shift and scalar/aether Ward enforcement. Use the same fully constraint-projected physical operator and complete shear Weyl observer to decide whether the h5/h6 channel survives or cancels. If nonzero transfer and an error-controlled later-time projection are certified, return to the preselected DES Y3 MagLim4×Source4 Asimov forecast. If no physical certification, retain PHYSICS_BLOCK, without a claim of detection.

## Sources
- [Prior restricted h6 metric theorem](ge19_20261119_first_delayed_metric_jet_reduced_operator.md)
- [11 Nov leading primordial growing-state proxy](../ge19/physics_gate/frozen_exp_superhorizon_growing_mode_20261111.py)
- [11 Nov radiation/neutrino Delta source proxy](../ge19/physics_gate/radiation_neutrino_delta_source_20261111.py)
- [12 Nov source-locked projected operator](../ge19/physics_gate/constraint_projected_joint_operator_20261112.py)
- [19 Nov mixed proxy warning](ge19_20261119_primordial_proxy_delayed_metric_source_decision.md)
- [Single observability return gate](ge19_20261119_observability_return_single_gate_decision.md)
