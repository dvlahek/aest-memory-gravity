# GE19 — Physical primordial source inserted into the restricted delayed metric jet

19 November 2026. **One bounded physics synthesis, not another simulation or independent full-physics theorem.** No CLASS, DES, H4/Z21, fit, or parameter scan.

**Classification: RADIATION_DUST_PROXY_SOURCE_INSERTION_EXACT_AT_RETAINED_ORDER / FULL_EINSTEIN_AEST_NL0B_PRIMORDIAL_WARD_UNRESOLVED / OBSERVABILITY_BLOCK.**

## Frozen inputs

The original reduced first-onset equations in \`ge19/physics_gate/first_retarded_memory_onset_20261111.py\`, at regular finite initial time t_i, zero chi_i=E_i=q_i=qdot_i=0 and specified comoving effective AeST source Delta_A, imply
\`\`\`math
D_i:=\dot\chi_0(t_i)=Q_i c_{a,i}^2\Delta_{A,i}.
\`\`\`
The already recorded original \`ge19/physics_gate/radiation_neutrino_delta_source_20261111.py\` gives at **leading nontrivial order in radiation-dominated, leading dustlike AeST and negligible AeST/radiation backreaction**,
\`\`\`math
\Delta_A(\tau_i)
=-\frac{15+4R_\nu}{40}\Psi_0(k\tau_i)^2
+O((k\tau_i)^4)
+\hbox{neglected pressure/backreaction corrections}.
\`\`\`
The prior frozen reduced AeST-only four-state metric theorem gives, for M2 = sum_j w_j omega_j^2 > 0 and h = t-t_i,
\`\`\`math
\Delta\Phi_{\mathrm{hist}}(t_i+h)
=\frac{c_{a,i}^2 k^2 Q_iD_iM_2}{5760a_i^2}h^6+O(h^7).
\`\`\`
For a **shear-free AeST-only frozen metric** this equals the restricted W=(Phi+Psi)/2 history-only response. There is no claim that this AeST-only metric and radiation-neutrino source are already a self-consistent complete coupled cosmological solution. We are *inserting a proxy* source into a restricted response formula.

## Substitution and its precise meaning

Substitute D_i and then the radiation-era leading proxy:
\`\`\`math
\boxed{
\Delta W_{\mathrm{hist,proxy}}(t_i+h)
=-\frac{(c_{a,i}^2)^2\,Q_i^2\,k^2}{230400a_i^2}
(15+4R_\nu)\Psi_0(k\tau_i)^2 M_2 h^6
+O[h^6(k\tau_i)^4]+O(h^7)+\text{uncontrolled pressure/backreaction terms}.
}
\`\`\`
The \`O[h^6(k tau_i)^4]\` term is shorthand only for the omitted analytic radiation-gradient expansion and has the appropriate coefficient dimensions from the preceding leading factors. This formula has no certified uniform remainders in any two-parameter limit (k*tau_i,h)->0. At fixed finite t_i and for the retained proxy, this channel has two explicit factors of c_a² and a finite-k gradient. At strictly k=0 and zero free-bath branch, it disappears in this regular sector. If c_a² ≈ 1e-14 for frozen Exp, its square is ≈1e-28, **not** an observed amplitude or a bound on total DES response.

The sign follows for positive Q_i², M2, c_a², k², and Psi0>0 on this specified proxy. No sign claim is made for the full physical transfer at lensing redshifts.

## Why this is not the missing full theorem

1. The radiation/nu source is derived with AeST as a **test dustlike constituent** at leading order. It is not an action-derived coupled finite-k growing eigenvector including all AeST E/chi corrections, bath free mode choice, and full Einstein feedback.
2. The reduced h^6 coefficient uses an *externally prescribed Delta_A*, a finite initial time and a shear-free AeST-only frozen metric operator. The radiation-neutrino background has nonzero anisotropic slip, so identifying its physical Weyl potential with the AeST-only Phi is not allowed. This is a mixed-order **proxy** calculation, not a closed cosmological solution.
3. The physical earliest nonzero chi and E for the finite-k coupled growing mode can themselves contain contributions at the same retained expansion order, and the physical eta derivative of that mode may add initial/interface terms. Therefore no theorem that the genuine physical delayed Weyl mode begins at h^6 or has the displayed coefficient is asserted.
4. The original full production source-to-metric operator remains uncertified. The generic Noether identity and restricted Ward identity do not replace the independent full action Euler equations.

## Decision and observability

This is the clearest *bounded* conclusion available from presently archived source-locked physics: the restricted local response can be nonzero, but the physically motivated superhorizon proxy renders this particular channel doubly suppressed and **does not** establish a late-time measurable physical Weyl memory. Do not advertise this as an observational prediction.

**Next single necessary acceptance item:** provide one independently derived, full Einstein–AeST–NL0B action-to-all-species finite-k adiabatic constrained operator **including true Delta_A, initial chi/E and shear**, and the delayed-only Weyl output with error bound. If unavailable, record PHYSICS_BLOCK and move only to data/projection *readiness* and conditional Asimov methodology; do not use observed DES residuals, claim forecast detection or start undirected new numeric series.

The requested observability return is a decision gate, **not a promise of positive detection**.

## Frozen sources
- [Reduced first memory onset](../ge19/physics_gate/first_retarded_memory_onset_20261111.py)
- [Radiation-neutrino dustlike Delta_A proxy](../ge19/physics_gate/radiation_neutrino_delta_source_20261111.py)
- [Restricted metric h6 proof](ge19_20261119_first_delayed_metric_jet_reduced_operator.md)
- [Leading Exp primordial mode](../ge19/physics_gate/frozen_exp_superhorizon_growing_mode_20261111.py)
- [Full physical/observation single gate](ge19_20261119_observability_return_single_gate_decision.md)
