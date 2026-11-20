# GE19 — R2 WSL confirmation and first coupled radiation–AeST gravitational backreaction

20 November 2026. One scientifically bounded return toward the **joint physical primordial mode**. No full Einstein–AeST–NL0B physical certification, CLASS solver output or DES analysis.

**Classification: R2_REPRODUCED_IDENTICAL_R1 / COUPLED_RADIATION_NEUTRINO_DUSTLIKE_AEST_LEADING_Y_SYMBOLIC_PASS / FULL_AEST_WARD_NL0B_AND_OBSERVER_NOT_READY.**

## 1. Researcher r2 output: previous file-overwrite error was administrative

The uploaded r2 JSON is byte-for-byte identical to the already archived original r1 JSON:
- SHA-256 = \`9ccef141eef6f8cdf3a64c07e20db6cf0dcc1c883f4716655d92ef665d57f26d\`;
- Git blob = \`c95101020b40151fc928d8a8b3f3317cc776bc56\`.
The r2 log contains \`GE19_JOINT_PRIMORDIAL_SOURCE_LOCKS_PASS 5\`, \`...SYMBOLIC_PASS 8\`, \`GE19_FIXED_RADIATION_FULL_EINSTEIN_NO_GO\` and \`GE19_FULL_PHYSICS_GO False\`, with **no overwrite exception**. Log SHA-256 = \`dd90637b5c9848282f817d41da79197f852b4635a77298d4c8f4ef739e217327\`. The older r1 JSON is authoritative; do not duplicate identical content merely to increase checkpoint counts. The NO_GO is a deliberate negative control for **fixed-radiation sources**, not a theory failure.

## 2. First *coupled* metric response at O(y), including the neutrino anisotropic stress

Solve a mathematically specified smaller physical system, not an externally fixed-radiation proxy: photons, **free-streaming massless neutrinos** of radiation share R_nu, and one separately conserved **pressureless AeST-like species** that gravitates consistently. Define \`y=rho_A/rho_r << 1\`, \`P=Psi0\`, and expand at \`k tau -> 0\`, to order y, with \`c_a²,w_A->0\` **only as the leading dusty approximation**. Baryon-photon tight coupling inertia and additional matter species are excluded. The auxiliary NL0B bath, eta forcing and full AeST scalar/aether Ward are also **excluded**. Consequently this is a valid self-contained Einstein–Boltzmann model, not the final GE19 cosmology.

In conformal time y~tau, Friedmann determines
\`\`\`math
\mathcal H=\frac1\tau(1+\tfrac14y)+O(y²),\quad
a²\rho_r=\frac1{\tau²}(1-\tfrac12y)+O(y²),\quad
a²\rho_A=\frac y{\tau²}+O(y²).
\`\`\`
Use the regular adiabatic density modes \`delta_r=-2P+4 Phi_1 y\` and \`delta_A=-3P/2+3Phi_1 y\`. Photon and neutrino Euler, dust Euler, continuity and the leading neutrino quadrupole then determine
\`\`\`math
\theta_{\gamma,\nu}=k²\tau[\tfrac12P+\tfrac12(\Phi_1+\Psi_1)y]+\cdots,\quad
\theta_A=k²\tau[\tfrac12P+\tfrac13(\Psi_1-\tfrac18P)y]+\cdots,
\`\`\`
\`\`\`math
\sigma_\nu=k²\tau²[\tfrac1{15}P+\tfrac2{45}(\Phi_1+\Psi_1)y]+\cdots.
\`\`\`
At leading k-tau order the Einstein Hamiltonian and traceless shear equations are the nondegenerate 2x2 matrix
\`\`\`math
3\Phi_1+\Psi_1=-\frac14P,\qquad
\Phi_1-\Psi_1=R_\nu[\frac4{15}(\Phi_1+\Psi_1)-\frac15P].
\`\`\`
The **unique** solution is
\`\`\`math
\boxed{\Phi_1=-\frac{15+16R_\nu}{16(15+2R_\nu)}P,\quad
\Psi_1=\frac{40R_\nu-15}{16(15+2R_\nu)}P.}
\`\`\`
Consequently the full metric in this restricted coupled model, at leading \`k\tau\to0\`, is
\`\`\`math
\boxed{\Phi=(1+\frac25R_\nu)P
-\frac{15+16R_\nu}{16(15+2R_\nu)}P\,y+O(y²,(k\tau)²),}
\`\`\`
\`\`\`math
\boxed{\Psi=P+\frac{40R_\nu-15}{16(15+2R_\nu)}P\,y+O(y²,(k\tau)²).}
\`\`\`
The Einstein momentum equation and the first-order photon, neutrino quadrupole and matter Euler equations **all agree**. Neutrino anisotropic stress is **not set to zero**. At \`R_nu=0\` both potential corrections reduce to \`-P y/16\`, a strong independent limit.

A local SymPy script with **16/16 exact symbolic gates** was run in an independent container. Canonical source-locked researcher WSL execution is still pending. Code:
\`ge19/physics_gate/coupled_radiation_aest_leading_backreaction_20261120.py\`.

## 2A. A useful observer distinction: the ordinary AeST-density Weyl correction is not delayed memory

The newly source-locked *pressureless* model gives an exact additional algebraic prediction for the gauge-invariant Newtonian Weyl combination \`W=(Phi+Psi)/2\`, at the same leading \`k tau ->0\` and \`O(y)\` truncation:
\`\`\`math
\boxed{
\frac{W}{\Psi_0}
=1+\frac{R_\nu}{5}
+\frac{3(4R_\nu-5)}{16(15+2R_\nu)}y
+O(y²,(k\tau)²).
}
\`\`\`
Equivalently, the relative change against the *same radiation-only metric* is
\`\`\`math
\boxed{\frac{\delta_y W}{W_{\rm radiation}}
=\frac{15(4R_\nu-5)}{16(R_\nu+5)(15+2R_\nu)}\,y
+O(y²,(k\tau)²).}
\`\`\`
The new neutrino-shear/anisotropic stress contribution has \`(\Phi_1-\Psi_1)/\Psi_0=-7R_\nu/[2(15+2R_\nu)]\`. At \`R_\nu=0\`, \`W/\Psi_0=1-y/16\` and the shear correction vanishes. For illustrative \`R_\nu=0.41\`, \`W_y/\Psi_0\approx -0.0398230\` and \`(\delta_y W/W_{\rm radiation})/y\approx -0.0368050\`. These ratios are determined by exact symbolic algebra from the certified two potential coefficients, not an added numerical cosmology.

**This is an eta-independent, ordinary gravitational-matter backreaction of an AeST-*like* dust species. It is NOT a delayed NL0B retarded memory signature and is not a DES shear/lensing prediction.** A future physical memory forecast must form the corrected eta=0 Weyl baseline *and* take the separately action-normalized derivative in eta with the complete no-free-history branch. The already archived v019j forced CLASS tangent cannot be subtracted from the new analytic O(y) coefficient to extract memory: they are distinct models/orders/normalizations, with original source mismatch and incomplete primordial initialization.

## 3. What this changes—and does not change

The previous fixed-radiation negative-control Einstein residual was \`R_A Delta_A\ne0\` because it prohibited compensating metric/radiation perturbations. Equations above explicitly exhibit **one consistent leading-order coupled compensation** in the physically meaningful pressureless, baryon-free submodel. Therefore this is real forward progress beyond merely diagnosing a missing source. It does **not** establish finite-k \`O(k²\tau²)\` AeST comoving density or fully close the primordial memory forcing. The actual Exp AeST species has nonzero (though small) \`w_A,c_a²\`, the baryon-photon loading changes the radiation Euler at order y, and the original scalar phase/Ward relation and positive NL0B bath history still must propagate together.

**Physically decisive next calculation:** elevate this finite-y coupled radiation seed to the actual action-normalized pressureful Einstein–AeST–NL0B hierarchy, including baryons, the photon–baryon tight-coupling momentum law, neutrino shear, original quarter memory force, scalar charge and transported auxiliary history. The full, source-normalized late Weyl tangent must be derived and independently validated before reusing predeclared DES Y3 MagLim4 × Source4 geometry. The historical W1=1.839077e-9 remains an implementation diagnostic, not a detection.

**FULL_PHYSICS_GO = FALSE. DES_DETECTION = FALSE.**

## Source references
- [Original r1 joint result](../results/ge19_joint_primordial_fluid_einstein_20261120_r1.json)
- [Source-locked joint WSL log](../results/ge19_joint_primordial_fluid_einstein_20261120_r1.log)
- [First new coupled leading-y symbolic operator](../ge19/physics_gate/coupled_radiation_aest_leading_backreaction_20261120.py)
- [Previous fixed-radiation obstruction](ge19_20261120_researcher_wsl_joint_gate_radiation_feedback_closure.md)
- [Original radiation+neutrino source](../ge19/physics_gate/radiation_neutrino_delta_source_20261111.py)
