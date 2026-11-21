# GE19 — First joint mixed O(y_m (kτ)²) Einstein–Boltzmann source in a dustlike AeST proxy

**21 November 2026 — physics-first derivation. No CLASS, DES, eta search or numerical fitting.**

**Classification:** \`COUPLED_TIGHT_COUPLING_PHOTON_BARYON_NEUTRINO_DUSTLIKE_AEST_MIXED_NLO_SYMBOLIC_PASS\` **subject to a pressureless AeST-like source approximation**. The full original AeST scalar/aether/auxiliary Ward-compatible physical growing mode remains **open**. A standalone local SymPy calculation verified 42 coefficient-level Einstein/continuity/Euler/quadrupole/octupole residuals, with arbitrary symbolic \`R_nu\` and baryon fraction \`beta\`. Source-locked researcher WSL run of the committed script remains pending.

## 1. Why this actually advances the source-to-memory problem

Prior work completed two separate *edges* of the primordial double expansion:

1. \`O(y_m)\` at \`kτ -> 0\`, including baryons, photons, neutrinos and gravitational matter backreaction: 31/31 WSL-verified.
2. \`O((kτ)²)\` at \`y_m=0\`, including the neutrino quadrupole and octupole: 37/37 WSL-reported (with the **one original octupole coefficient-selection defect fixed separately** in [the corrected causal-onset proof](ge19_20261121_corrected_f3_and_cubic_delayed_memory_onset.md)).

The **mixed** \`O(y_m(kτ)²)\` coefficient is not obtainable by simply adding those two edge solutions. We now solve it using the full combined Einstein-source constraints and tight-coupled photon–baryon, free-neutrino and dust-AeST-like ODEs.

## 2. Definition of the controlled two-parameter model

Let \`R=R_nu=rho_nu/rho_r\`, \`y=y_m=(rho_A+rho_b)/rho_r\`, \`beta=rho_b/(rho_A+rho_b)\`, \`x=kτ\`, and \`P=Psi0\`; \`0<R<1\`, \`0<=beta<=1\`. The background to first order in y is
\`\`\`math
\mathcal H=\frac{1+y/4}{\tau},\quad
a²\rho_r=\frac{1-y/2}{\tau²},\quad
a²\rho_A=\frac{(1-\beta)y}{\tau²},\quad
a²\rho_b=\frac{\beta y}{\tau²},\quad
\frac{dy}{d\tau}=\frac{y}{\tau}.
\`\`\`
We use the same normalized Einstein units as the earlier GE19 tests. Baryon-photon tight coupling includes \`R_b=3 beta y/[4(1-R)]\`; massless neutrinos retain the leading nonzero anisotropic stress and octupole. AeST is here *only* a separately conserved pressureless dustlike effective species in the metric/ordinary-stress calculation. **The original Exp scalar/aether action, c_a² corrections, NL0B memory and Ward identities have not yet been inserted in this test.** The model is a near-radiation growing-mode expansion, not a global evolution through recombination.

## 3. Closed mixed gravitational potentials

Expand
\`\`\`math
\Phi/P=1+\frac{2R}{5}+f_y\,y+f_k\,x²+\boxed{f_{yk}\,yx²}+\cdots,\qquad
\Psi/P=1+g_y\,y+g_k\,x²+\boxed{g_{yk}\,yx²}+\cdots
\`\`\`
with prior coefficients
\`\`\`math
f_y=-\frac{15+16R}{16(15+2R)},\quad
g_y=\frac{40R-15}{16(15+2R)},\quad
f_k=-\frac{56R²+580R+525}{630(2R+25)},\quad
g_k=\frac{56R²+10R-525}{630(2R+25)}.
\`\`\`
The newly solved mixed coefficients are
\`\`\`math
\boxed{f_{yk}=
\frac{896R^4+66160R^3+1023300R²+5386500R+4659375}
{10080(2R+15)(2R+25)(4R+75)}},
\`\`\`
\`\`\`math
\boxed{g_{yk}=
-\frac{896R^4+116080R^3+1050900R²+1074000R-4659375}
{10080(2R+15)(2R+25)(4R+75)}}.
\`\`\`
The Hamiltonian and momentum residuals at mixed order are not algebraically independent (they share the same proportional coefficient on \`f_{yk},g_{yk}\` after the other conservation equations are enforced). In the derivation, the **Hamiltonian and neutrino shear** fix the pair and the momentum and spatial-pressure-trace equations **independently check** it. This prevents overcounting these as 42 independent physical constraints.

At \`R=0\`, \`f_{yk}=g_{yk}=71/4320\`, a useful no-neutrino-slip control. For illustrative \`R=0.41\`, \`f_{yk}\approx0.0223237857\` and \`g_{yk}\approx0.0127848358\`.

The mixed metric coefficients **do not depend on beta at this order**. The individual photon-baryon velocity perturbation does depend on beta, but its contribution to the total stress cancels the corresponding baryon contribution in the momentum constraint. Thus independence of beta is an explicit constrained cancellation, not an assumption that baryon dynamics are irrelevant.

## 4. The physical-source improvement: full mixed comoving dustlike AeST density

For the normalized pressureless effective AeST species
\`\`\`math
\Delta_A=\delta_A+\frac{3\mathcal H\theta_A}{k²},
\`\`\`
the previous radiation-only NLO term was
\`\`\`math
\Delta_A/P=-\frac{15+4R}{40}\,x²+O(x^4).
\`\`\`
The **new exact** mixed correction from the jointly solved system is
\`\`\`math
\boxed{\left[\frac{\Delta_A}{P}\right]_{yx²}=\frac{15+4R}{200}},\qquad
\boxed{
\frac{\Delta_A}{P}
=-\frac{15+4R}{40}\,x²\left(1-\frac{y}{5}\right)
+\text{terms beyond the retained }\{y^0,y^1\}\times\{x^0,x²\}\text{ orders}.
}
\`\`\`
Here \`[ ]_{yx²}\` denotes the coefficient of \`y x²\`. The expansion does not certify a particular remainder scale for any uncomputed \`O(y²)\` terms.

For illustrative \`R=0.41\`, the NLO source reads \`\Delta_A/P=-0.416 x²+0.0832 yx²+\cdots\`. This is **not** a forecast for the full AeST scalar source; it is a controlled constraint-compatible **dustlike** matter seed.

## 5. Dynamical validation and its boundary

The [new source-locked executable](../ge19/physics_gate/coupled_mixed_y_k2_photon_baryon_neutrino_20261121.py) applies the exact derivative rule
\`\`\`math
D_\tau=\partial_\tau+\frac{y}{\tau}\partial_y
\`\`\`
to all fields, including the previously missed cross terms. Its 42 *coefficient-level* checks cover:
- all four Einstein equations (Hamiltonian, momentum, traceless shear, spatial trace) at \`y⁰k⁰\`, \`y¹k⁰\`, \`y⁰k²\`, \`y¹k²\` (16 checks);
- all four continuity laws for photon, neutrino, baryon and pressureless AeST-like matter at \`y⁰k²,y¹k²\` (8 checks);
- three Euler laws (joint photon–baryon, neutrino, AeST-like dust) and the neutrino quadrupole at \`y⁰k²,y¹k²,y⁰k⁴,y¹k⁴\` (16 checks);
- the neutrino octupole at the **correct** \`y⁰k³,y¹k³\` coefficient (2 checks).

The ideal tight-coupling term \`1/(1+R_b)\` is expanded consistently as \`1-R_b+O(y²)\`; treating it as an unexpanded rational expression while selecting formal y polynomial coefficients would spuriously fail valid gates. The mixed neutrino \`F_{\nu3}\` and \`\sigma_{\nu4}\` are required by the shear relation. The full local SymPy equations, not merely an asserted closed-form solution, were evaluated before committing.

**This does not prove:** the mixed result in exact nonzero-pressure Exp AeST, the original scalar/aether action-to-fluid operator, complete Noether Ward propagation, initial \`X,E_A,q_j,\dot q_j\`, or a physical delayed Weyl tangent. Even tiny \`c_a²\` does not alone control \`c_a² k²/(a²R_A)\` or small-denominator effects.

## 6. Next one missing *physical* equation family

The **ordinary stress/gravity mixed source is now closed** in the dustlike proxy. Avoid further repeating these GR controls.

Next derive the actual **original-action scalar/aether initial-data conditions** at the same \`O(y_m(k\tau)²)\` order using the exact reduced flow
\`\`\`math
\dot X=E_A+c_a²F,\quad
F=\Delta_A+\frac{k²}{3a²R_A}[K_BE_A+(2-K_B)QX],
\`\`\`
and the exact one-quarter force \`-\eta Q B_\chi/(4K_B)\`, with the offshell scalar current and the selected **history-transported** bath. This is the physical difference between "a dustlike proxy responds to matter" and "a covariant gravitational memory theory has a distinct delayed Weyl response." No \`PHYSICS_GO\`, no DES detection.

## Immutable input reports

- [Original researcher 37-gate radiation NLO JSON](../results/ge19_radiation_finite_k_NLO_20261121_r1.json) and [log](../results/ge19_radiation_finite_k_NLO_20261121_r1.log), byte-exactly archived.
- [Original researcher 31-gate baryon/Exp JSON](../results/ge19_physical_baryon_Exp_leading_seed_20261121_r1.json) and [log](../results/ge19_physical_baryon_Exp_leading_seed_20261121_r1.log), duplicate uploads matched prior Git blobs.
- [Corrected octupole gate and exact cubic source onset](ge19_20261121_corrected_f3_and_cubic_delayed_memory_onset.md).
