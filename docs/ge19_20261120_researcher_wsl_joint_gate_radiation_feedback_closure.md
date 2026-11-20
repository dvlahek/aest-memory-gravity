# GE19 — WSL-confirmed joint primordial gate and the compulsory radiation backreaction combination

20 November 2026. User-executed WSL gate archived **byte-exactly**, followed by a new pencil-and-SymPy joint Einstein-source implication. No new CLASS, DES, parameter sweep, observed-shear fit, or claim of physical memory detection.

**Classification: RESEARCHER_WSL_SOURCE_LOCKS_5_OF_5_AND_SYMBOLIC_8_OF_8_PASS / FIXED_RADIATION_NEGATIVE_CONTROL_CONFIRMED / LINEARIZED_MOMENTUM_AND_HAMILTONIAN_BACKREACTION_CLOSURE_EXACT_ON_FIXED_BACKGROUND / FULL_PHYSICAL_PRIMORDIAL_MODE_NOT_CERTIFIED.**

## 1. Actual researcher evidence (not just an anticipated pass)

The WSL log at \`results/ge19_joint_primordial_fluid_einstein_20261120_r1.log\` is 285 bytes, SHA-256 \`79617a6423223dde280355db40dcde20f6b79be1e2439cb056064bf1225c1d94\` and Git blob \`5d38007df459445a215c0fb700df00a0fed7223b\`; it records:

- \`GE19_JOINT_PRIMORDIAL_SOURCE_LOCKS_PASS 5\`;
- \`GE19_JOINT_PRIMORDIAL_REDUCED_ACTION_SYMBOLIC_PASS 8\`;
- \`GE19_FIXED_RADIATION_FULL_EINSTEIN_NO_GO\`;
- \`GE19_FULL_PHYSICS_GO False\`.

Its matching JSON, \`results/ge19_joint_primordial_fluid_einstein_20261120_r1.json\`, is 1,609 bytes, SHA-256 \`9ccef141eef6f8cdf3a64c07e20db6cf0dcc1c883f4716655d92ef665d57f26d\`, Git blob \`c95101020b40151fc928d8a8b3f3317cc776bc56\`, classification \`GE19_PRIMORDIAL_REDUCED_ACTION_FLUID_PASS_FIXED_RADIATION_FULL_CONSTRAINT_NO_GO\`. All eight symbolic tests are true. The 16-gate pressureful velocity JSON reupload is identical to the previously archived researcher artifact (SHA-256 \`2b0557b7d39394340c552d87f5d2692340c6e4038597eb6342d4ab9ce115f762\`); it remains a test-source approximation, not full physics.

This establishes that the canonical source-locked WSL joint diagnostic **ran successfully**. The NO_GO belongs to the **unmodified fixed-radiation proxy**, *not* the full GE19 theory.

## 2. A stronger necessary source correction from all three Einstein rows

Work in conformal time, \`\mathcal H=a'/a\`, at a *fixed shared background* \`a(\tau)\`, and only in a perturbative comparison of a radiation-only test-source solution to a candidate that includes AeST stress. This is **not** a full expansion about the correct radiation-plus-AeST background. Define

\`\`\`math
\Omega_s=\sum_s\left[\delta\rho_s+\frac{3\mathcal H}{k^2}T_s\right],
\quad T_A=R_A\theta_A,\quad
R_A=\rho_A+p_A,\quad
\Delta_A=d_A+\frac{3\mathcal H}{k^2}\theta_A,\quad
S_s=\sum_s(\rho_s+p_s)\sigma_s.
\`\`\`

For an ordinary-species response \`(\delta\Omega_s,\delta T_s,\delta S_s)\` plus first-order metric response \`(\delta\Phi,\delta\Psi)\`, the *linearized fixed-background* comoving Einstein, momentum and shear constraints read

\`\`\`math
\boxed{\delta\Omega_s+R_A\Delta_A+\frac{2k^2}{3a^2}\delta\Phi=0,}\tag{1}
\`\`\`math
\boxed{\delta\Phi'+\mathcal H\delta\Psi
=\frac{3a^2}{2k^2}(\delta T_s+R_A\theta_A),}\tag{2}
\`\`\`math
\boxed{\delta\Phi-\delta\Psi
=\frac{9a^2}{2k^2}\delta S_s.}\tag{3}
\`\`\`

Set \`B=\delta\Omega_s+R_A\Delta_A\`. Equations (1),(3) eliminate both potentials:
\`\`\`math
\delta\Phi=-\frac{3a^2}{2k^2}B,\qquad
\delta\Psi=-\frac{3a^2}{2k^2}(B+3\delta S_s).
\`\`\`
Their substitution into (2) gives the **exact fixed-background necessary compatibility equation**

\`\`\`math
\boxed{
B'+3\mathcal H(B+\delta S_s)+\delta T_s+R_A\theta_A=0.
}\tag{4}
\`\`\`

This was checked independently in SymPy by differentiating the eliminated metric potentials and reducing the resulting momentum residual to exact zero. It is a direct Einstein identity, not an independent proof that ordinary species or the aether obey their full evolution equations.

Using the original separately conserved AeST homogeneous enthalpy law \`R_A'=-3\mathcal H(1+c_a^2)R_A\`, the **required ordinary-species backreaction combination** is

\`\`\`math
\boxed{
\delta\Omega_s'+3\mathcal H(\delta\Omega_s+\delta S_s)+\delta T_s
=-R_A\left[\Delta_A'-3\mathcal H c_a^2\Delta_A+\theta_A\right].
}\tag{5}
\`\`\`

## 3. The early radiation test-state forces a nonzero correction

For the archived dustlike test source \`f=-(15+4R_\nu)/40\`, with leading \`c_a^2=0\`,
\`\`\`math
\Delta_A=f\Psi_0 k^2\tau^2+\cdots,\qquad
\theta_A=\Psi_0 k^2\tau/2+\cdots,
\quad \mathcal H=1/\tau.
\`\`\`
Then equation (5) *requires* at this retained order
\`\`\`math
\boxed{
\delta\Omega_s'+3\mathcal H(\delta\Omega_s+\delta S_s)+\delta T_s
=\frac{5+4R_\nu}{20}R_A\Psi_0 k^2\tau+\cdots .
}\tag{6}
\`\`\`
The coefficient does not vanish for the physical neutrino fraction and nonzero AeST enthalpy. In particular, **correcting the metric while freezing the ordinary radiation density, momentum and shear does not satisfy all three Einstein equations simultaneously** under these assumptions. Ordinary-species (and in the real cosmology background) feedback is indispensable.

The same condition may be written as a formal integrating-factor identity for the ordinary comoving stress \`δΩ_s\` given \`δT_s,δS_s\`, but these are set by the photon/neutrino Boltzmann hierarchy, **not free knobs**. The full radiation-plus-AeST background perturbation must be treated consistently; the numerical coefficient in (6) is a **fixed-background negative-control diagnostic**, not a claimed physical radiation-feedback solution.

## 4. Scientific next step and decision

- **Established:** source-locked WSL joint 8-gate negative-control result. Also the exact fixed-background Einstein row compatibility (4)-(5), which identifies the needed combined ordinary-species response.
- **Not established:** independently solved finite-\`R_A\` radiation-era Einstein–AeST–NL0B plus photons/neutrinos growing eigenmode with the *correct expanding background* and original scalar/aether Ward equations, nor a causal initial tangent satisfying all constraints.
- **Single physical action next:** assemble the *coupled background plus photon/neutrino hierarchy* with the original \`quarter\` AeST bath source, use (4)-(5) as a non-tuning constraint gate, and solve the growing adiabatic state at finite k. Only then evaluate a history-preserving delayed-only Weyl response and the preselected DES Y3 MagLim4 x Source4 Asimov observer. No more narrow Taylor-onset campaigns or after-the-fact eta fitting.

**FULL_PHYSICS_GO: FALSE. DES detection: FALSE.**

## Frozen sources

- [WSL original joint JSON](../results/ge19_joint_primordial_fluid_einstein_20261120_r1.json)
- [WSL original joint log](../results/ge19_joint_primordial_fluid_einstein_20261120_r1.log)
- [Executable joint negative-control gate](../ge19/physics_gate/joint_primordial_fluid_einstein_decision_20261120.py)
- [Original all-species Einstein projected operator](../ge19/physics_gate/constraint_projected_joint_operator_20261112.py)
- [Original pressureful fluid and action dictionary](ge19_20261111_joint_action_to_CLASS_scalar_source_matrix.md)
- [Original radiation+neutrino leading source](../ge19/physics_gate/radiation_neutrino_delta_source_20261111.py)
