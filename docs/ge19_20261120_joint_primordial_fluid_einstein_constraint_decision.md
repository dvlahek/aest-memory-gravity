# GE19 — Joint primordial action/fluid versus full Einstein constraint: decisive fixed-radiation boundary

20 November 2026. Physics-first exact symbolic check, **one** source-locked executable. No new CLASS/DES numerical campaign or fitting.

**Classification: REDUCED_PRESSUREFUL_AEST_FLUID_ACTION_IDENTITIES_PASS / UNMODIFIED_TEST_RADIATION_FULL_EINSTEIN_CONSTRAINT_NO_GO / COMPLETE_COUPLED_PHYSICAL_MODE_OPEN.**

## 1. What is now jointly established in the original reduced dictionary

Define \`R_A=rho_A+p_A\`, \`d_A=delta_A/(1+w_A)\`, \`Delta_A=d_A+3 mathcal H theta_A/k²\`, \`S_A=K_B E_A+(2-K_B)chi\` and \`c=c_a²\`. The archived original AeST effective pressure is \`Pi_A=c delta_A+c k² S_A/(3a² rho_A)\`, and the frozen homogeneous action implies \`w_A'=-3 mathcal H(1+w_A)(c-w_A)\`. Thus **without assuming constant w or c**, the archived AeST density and Euler fluid rows exactly reduce to
\`\`\`math
\boxed{
d_A'=-\theta_A+3\Phi'
-\frac{\mathcal H c\,k²}{a²R_A}S_A, }\tag{1}
\`\`\`
\`\`\`math
\boxed{
\theta_A'+\mathcal H\theta_A=k²(\Psi+c\Delta_A)
+\frac{c\,k⁴}{3a²R_A}S_A. }\tag{2}
\`\`\`
Using the original phase definition \`varphi=aQ theta_A/k²\`, \`Q'/Q=-3 mathcal H c\`, the action pressure map requires
\`\`\`math
\boxed{
\frac{\delta Q}{Q}=
\frac{\theta_A'+\mathcal H\theta_A}{k²}-\Psi-
\frac{3c\mathcal H\theta_A}{k²}
=c\left(d_A+\frac{k²S_A}{3a²R_A}\right). }\tag{3}
\`\`\`
Substituting (2) into (3) gives **zero residual** identically for arbitrary \`w,c,S_A,theta_A,mathcal H\`. This is a nontrivial combined fluid/phase consistency check, **not** an independent full scalar Euler+Noether or action-to-CLASS equivalence certificate.

An important bookkeeping distinction: \`d_A=delta_A/(1+w_A)\` is **enthalpy-normalized density**; it is not the raw density contrast. The previous 16-gate \`dnorm\` radiation proxy represents this normalized variable. Consequently its first-order velocity correction is compatible with the density/phase dictionary; continuity also requires evolution of the actual \`delta_A=(1+w_A)d_A\`, not treating it as a literal dust density with w=0.

## 2. Why the fixed-radiation proxy does NOT pass the full Einstein constraint

The full comoving Einstein condition from the archived all-species projected operator is
\`\`\`math
\boxed{\mathcal C_{\rm com}=R_A\Delta_A+\Omega_s+\frac{2k²}{3a²}\Phi=0.}\tag{4}
\`\`\`
The six-equation original radiation+neutrino **test-fluid** solution obeys \`Omega_s+2k² Phi/(3a²)=0\` **only when AeST is omitted from the metric source**. In that same solution, the dustlike test-AeST comoving density is
\`\`\`math
\Delta_A=f k²\tau²+\cdots,\qquad
f=-\frac{15+4R_\nu}{40}\Psi_0.
\`\`\`
Consequently, if one inserts a genuinely nonzero AeST component while leaving those radiation metric and ordinary-species fields completely unchanged, the leading full constraint defect is
\`\`\`math
\boxed{
\mathcal C_{\rm com}^{\rm fixed\ rad}=
-\frac{R_A(15+4R_\nu)}{40}\Psi_0\,k²\tau²
+\cdots\ne0
}\tag{5}
\`\`\`
for generic \`R_A>0\`, nonzero primordial curvature amplitude and \`0<=R_nu<=1\`. This residual was independently evaluated with SymPy; 8/8 joint tests passed, including this required **nonzero negative control**.

This is **not** a no-go theorem against the Einstein–AeST–NL0B theory! It rejects the incorrect step of promoting a test-fluid radiation solution into a full finite-\`R_A\` cosmology without adding its first-order metric and species backreaction. At a *shared held-fixed background* the necessary correction obeys
\`\`\`math
\boxed{
\frac{2k²}{3a²}\delta\Phi+\delta\Omega_s
=-R_A\Delta_A.
}\tag{6}
\`\`\`
The correction to the physical expanding background, neutrino shear, and momentum evolution must also be included in the full coupled calculation; (6) is not a standalone solver for \`delta\Phi\`.

Since the AeST stress-to-radiation ratio is a separate expansion parameter, suppression of c_a² **does not** justify neglecting AeST's gravitational background or metric effect. The previous 16/16 action/velocity audit is still valid *within its declared test-fluid approximation*, and cannot by itself certify the full Weyl response.

## 3. What remains and what must NOT be inferred

- The reduced pressureful fluid+phase dictionary passes this exact combined identity. It does not independently close the original scalar Euler/Ward equation. The existing LW33 residual identity requires the original quarter source (not the historical v019j half) and matched action density dictionary.
- The genuine finite-k coupled regular adiabatic growing state must solve the photon/neutrino hierarchy and baryons with AeST stress, including its induced \`delta\Phi,\delta\Psi,\delta\Omega_s\` and preserved original history of all bath q/p variables.
- Only after such an action-normalized state and Einstein/Noether propagation pass may a delayed-only Weyl tangent \`W_1\` be used for DES Y3 MagLim4 x Source4 Asimov. The archived single CLASS W1 remains an **uncertified implementation tangent**, not a measured lensing effect.
- No extra free eta tuning or numerical reset of q/p at a finite checkpoint is supported. The required corrections must be derived from the original action and fluid hierarchy.

## Reproducible single check

Original-source-locked script:
\`ge19/physics_gate/joint_primordial_fluid_einstein_decision_20261120.py\`.
**Independent SymPy 1.14 prototype: 8/8 exact gates PASS**; the canonical researcher WSL source-lock execution is pending.

\`\`\`bash
cd ~/aest-memory-gravity
git switch physics-first-gravitational-elasticity
git pull --ff-only origin physics-first-gravitational-elasticity
source .venv/bin/activate
python -u ge19/physics_gate/joint_primordial_fluid_einstein_decision_20261120.py \
  --out results/ge19_joint_primordial_fluid_einstein_20261120_r1.json \
  2>&1 | tee results/ge19_joint_primordial_fluid_einstein_20261120_r1.log
\`\`\`
Expected:
\`GE19_JOINT_PRIMORDIAL_SOURCE_LOCKS_PASS 5\`;
\`GE19_JOINT_PRIMORDIAL_REDUCED_ACTION_SYMBOLIC_PASS 8\`;
\`GE19_FIXED_RADIATION_FULL_EINSTEIN_NO_GO\`;
\`GE19_FULL_PHYSICS_GO False\`.
This is **successful negative-control behavior**, not a solver failure.

## Frozen sources
- [Joint original action and CLASS source map](ge19_20261111_joint_action_to_CLASS_scalar_source_matrix.md)
- [Original all-species constraint projected operator](../ge19/physics_gate/constraint_projected_joint_operator_20261112.py)
- [Independent radiation+neutrino test fluid](../ge19/physics_gate/radiation_neutrino_delta_source_20261111.py)
- [WSL pressureful velocity report (16/16)](../results/ge19_primordial_pressureful_velocity_20261120_r1.json)
- [Original off-shell scalar Ward](ge19_lw33_exact_scalar_action_to_CLASS_offshell_source_decision_2026-11-10.md)
