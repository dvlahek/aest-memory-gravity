# GE19 LW13 — exact Hamiltonian constraint-propagation identity and physical Noether gap

**Date: 2026-11-09. Outcome: GE19_LW13_CONDITIONAL_TOTAL_CONSERVATION_HAMILTONIAN_PROPAGATION_IDENTITY_PASS_ACTION_WARD_OPEN.**

This is a **conditional exact analytic theorem** of the complete **total conserved stress-energy** scalar Einstein equations in flat FLRW/CLASS Newtonian-gauge conventions. It is **NOT** a certification that the modified AeST/NL0B action satisfies its full Noether/Ward identities, that CLASS approximation transitions preserve the constraint, that a retarded metric Green has been computed, or that any astronomical memory signal is detected.

## Provenance and frozen inputs

The **actual researcher WSL LW12** 5×5 AeST–Phi **partial** Jacobian result is byte-preserved in [LW12 original local JSON](../results/ge19_lw12_aest_metric_partial_jacobian_20261109.json), SHA256 **fdec5a67d0ba5a7f22fa9b59e22116b18e6b94dce8e18578a526c36164d0b00f**, commit **428cd02b97ccc0761975e8a4d9d9671c60ced4eb**, with **8/8 exact symbolic gates PASS**. Its original LW10 source code ancestry and pin are verified. [Local result qualification](ge19_lw12_local_validation_and_next_constraint_gate_2026-11-09.md) records the original WSL run separately from independent archive replay.

LW13 analytic proof protocol: [frozen exact equations](../ge19/lw13_hamiltonian_constraint_propagation_protocol_20261109.json), commit **e60190a5eb9a10957405caecc4975bfb4c7bb0db**, Git blob **859e2a2c2f65008987c342c2ed51437b7ebf5949**. The algebraic identity was already formulated before predata publication, **so this is not an independently blind experimental test**. Reproducible canonical runner: [LW13 symbolic script](../ge19/lw13_hamiltonian_constraint_propagation_20261109.py), commit **5b59acd46070655cb7a8aa5c6e1ee9c3f94c0364**. Actual independent SymPy 1.14.0 check, with no CLASS computation, is archived in [LW13 source/constraint JSON](../results/ge19_lw13_hamiltonian_constraint_symbolic_replay_20261109.json), commit **5c5dfa22c8b890e7ddd279b2e404c20683c69fc5**.

The pinned original CLASS source/perturbations.c at original commit **e85808324f51fc694d12e3ed7439552a3c3f9540** contains, in Newtonian gauge, the **Hamiltonian scalar constraint (commented as an alternative phi expression)**, the actual **psi shear relation** and **phi-prime momentum evolution**. We use the spatially flat \`K=0\` specialization of that implementation, not a generalized curved-space identity.

## 1. Exact flat scalar equations in original CLASS normalization

Let a prime denote conformal time and define the following **total** perturbed matter sources, including all active species and the AeST effective fluid:

\[
\mathcal H=a'/a,\quad
R=\rho_{\rm total}+p_{\rm total},\quad
D=\delta\rho_{\rm total},\quad P=\delta p_{\rm total},
\]
\[
T=\sum_i(\rho_i+p_i)\theta_i,\qquad
S=\sum_i(\rho_i+p_i)\sigma_i.
\]

The unmodified CLASS Newtonian-gauge Einstein shear and momentum equations are

\[
\Psi=\Phi-\frac92\frac{a^2}{k^2}S,\qquad
\Phi'=-\mathcal H\Psi+\frac32\frac{a^2}{k^2}T.
\]

The **flat** Hamiltonian scalar constraint, in the CLASS source code normalization, is

\[
\boxed{
\mathcal C_H =
k^2\Phi+\frac32a^2\left(D+\frac{3\mathcal H}{k^2}T\right)=0.}
\]

The original CLASS code evolves Phi using the **momentum** equation rather than solving this constraint on every time step. This makes **constraint propagation** rather than merely source presence a crucial physics test.

## 2. Conditional exact constraint propagation

Assume the *complete aggregate* effective stress-energy obeys the linear total conservation equations. To expose possible missing physical source terms, introduce residual source functions \(J_D\) and \(J_T\):

\[
D'=-3\mathcal H(D+P)-T+3R\Phi'+J_D,
\]
\[
T'=-4\mathcal H T+k^2P+k^2R\Psi-k^2 S+J_T.
\]

These expressions are the total-fluid energy/momentum conservation laws in the same conformal Newtonian variables. The flat background Friedmann/Raychaudhuri identity is

\[
\mathcal H'=\mathcal H^2-\frac32 a^2R.
\]

Differentiate \(\mathcal C_H\) with all sources evolved; insert the exact three equations above and the original Einstein metric relations. Pressure P, shear S, and all background rho/p terms cancel **algebraically**. The result is

\[
\boxed{
\mathcal C_H'
=-\mathcal H\mathcal C_H+
\frac32a^2J_D+
\frac92\frac{a^2\mathcal H}{k^2}J_T.}
\]

The independent SymPy check returned exactly
\[
\mathcal C_H'+\mathcal H\mathcal C_H=
\frac{3a^2}{2k^2}(k^2J_D+3\mathcal H J_T),
\]
with zero remaining symbolic residual. In the **source-free total conservation case** \(J_D=J_T=0\),

\[
\boxed{
\mathcal C_H'=-\mathcal H\mathcal C_H,\qquad
\mathcal C_H(\tau)=
\mathcal C_H(\tau_i)\frac{a(\tau_i)}{a(\tau)}.}
\]

Thus a correctly initialized zero Hamiltonian constraint **remains zero on one smooth exact continuum branch**, *if all stated hypotheses hold*. It is not enough for the five-variable LW12 block to have the correct algebraic entries: the **total** stress-energy and complete Einstein system must obey the conservation identities. Conversely, a nonzero \(J_D\) or \(J_T\) directly shows the combination that would source a Hamiltonian residual; particular combinations can cancel in \(\mathcal C_H'\), so this identity alone does not certify both individual Ward components.

## 3. What it tells us about the actual NL0B memory source

The original modified AeST v019/v019j effective-fluid implementation updates its dark density and velocity using

\[
\delta_A'=3\mathcal H(w_A\delta_A-\Pi_A)
-(1+w_A)(\theta_A-3\Phi'),\quad
\theta_A'=(3c_a^2-1)\mathcal H\theta_A+
\frac{k^2\Pi_A}{1+w_A}+k^2\Psi.
\]

These are conservation-form effective-fluid equations; the positive memory bath enters **only** in the E_aether **evolution** source \(\Delta E'=-aQB_{\chi,\rm raw}/(2K_B)\). The memory changes \(\Pi_A\) through the E state, and therefore changes the fluid evolution, but the original **implemented** conservation equations continue to use that same \(\Pi_A\) consistently. Formally this has *no new explicit* \(J_D\) or \(J_T\) in the **implemented hydrodynamic equations**.

However, the last statement is **NOT a full action-level derivation** of \(\nabla_\mu T_{\rm tot}^{\mu\nu}=0\). The positive bath has its own local auxiliary oscillator state, covariant metric variation and potential source exchange. In particular, one must verify that the direct first-order bath Einstein stress is truly absent in the **complete** action-based perturbation system, and that the original effective AeST stress and Noether identities remain closed. Setting \(J_D=J_T=0\) by writing conservation-form fluid equations **cannot prove** that the stress source used in Einstein equations is the physically complete stress of the action.

This is exactly why LW13 is a *necessary conditional consistency lemma*, **not** a physical theory certification.

## 4. Remaining genuine closure work

1. **Action/Noether**: derive the first-order metric variation of the *complete NL0B action* (AeST scalar+aether+positive memory bath) and obtain the total energy/momentum Ward identities, including auxiliary-field exchanges. Audit \(J_D,J_T\) against original implemented stress, not assumed textbook conservation.
2. **Full smooth-regime perturbation operator**: extract photon, baryon, neutrino and relevant other-species dynamical blocks \(A_{AO},A_{OA},A_{OO}\), plus \(C_W=(e_\Phi,-\tfrac12 H_{\rm shear,O})\), in the same gauge and approximation branch. Approximation switches, free-streaming hierarchies and initial condition constraints need explicit handling.
3. **Physical-history observer**: only then construct physically admissible distinct past histories, hold specified present observable controls matched, and compute a nonzero *full* retarded difference \(\Delta W\) and its calibrated finite-eta normalization, rather than injecting arbitrary E impulses.
4. **Astronomical window**: only afterward evaluate a legitimate DES/ACT lensing observable with full necessary k,z/angular kernels and restrictive competing models under prior Asimov nuisance forecasts. LW03 radial FAIL, LW05 full cosmic-shear LOS BLOCK, LW08 differential source UNRESOLVED and H4/Z21 unfinished remain unchanged.

Do not suggest multiple additional small numerical CLASS resolution sweeps or treat LW13 as a Nature Astronomy observation.

## Optional exact local reproduction, zero CLASS executions

\`\`\`bash
set +e
cd ~/aest-memory-gravity
git pull --ff-only
source .venv/bin/activate
python3 -u -m ge19.lw13_hamiltonian_constraint_propagation_20261109 --self-test
python3 -u -m ge19.lw13_hamiltonian_constraint_propagation_20261109
\`\`\`

Requires the existing unmodified local LW10 and LW12 JSON files under \`results/\` and SymPy. The independent symbolic result has already been archived to GitHub, so reexecution is optional.
