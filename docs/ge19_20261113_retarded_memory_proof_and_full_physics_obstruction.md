# GE19 — Retarded gravitational-memory theorem and the full-physics obstruction

13 November 2026. Frozen GE05/GE06 action and fixed Exp benchmark. No new CLASS run, parameter sweep or DES data fit.

**Classification** — RESTRICTED_RETARDED_ACTION_MEMORY_THEOREM_PROVED / FULL_CONSTRAINED_WEYL_MODE_NOT_PROVED / OBSERVABILITY_BLOCK.

The scientific question is whether the original Einstein–AeST–NL0B action generates a causal, physically admissible, gauge-invariant memory response. The following proof separates a theorem **within the original quadratic longitudinal action** from a **conditional full-physics representation**. The latter is not a demonstration that the presently patched CLASS solution satisfies the complete original field equations.

## Theorem 1 — the finite positive NL0B bath has genuine causal gravitational-memory response

Assume a prescribed regular FLRW scale factor a(t)>0, a finite set of auxiliary frequencies ω_j>0 and weights w_j>=0 with at least one positive weight, η>0, and one Fourier scalar k>0. Take the **original restricted quadratic longitudinal bath action**
\[
L_{{\rm b},j}^{(2)}
=\frac{\eta a^3}{4}
\left[\dot q_j^{\,2}
-\left(\omega_jq_j-\sqrt{w_j}\frac{k\chi}{a}\right)^2\right],
\qquad \chi=\varphi+Q\alpha_A .
\tag{1}
\]
Choose the no-free-bath branch at finite initial t_i by q_j(t_i)=dot q_j(t_i)=0.

**Claim.** On any finite regular FLRW interval, the unique forced auxiliary solution has the retarded representation
\[
q_j(t)=\omega_j\sqrt{w_j}k
\int_{t_i}^t G_{R,j}(t,s)\frac{\chi(s)}{a(s)}\,ds,
\qquad (\partial_t^2+3H\partial_t+\omega_j^2)G_{R,j}=\delta(t-s).
\tag{2}
\]
Its original aether driving source is the causal Volterra functional
\[
\boxed{
B_\chi(t)=\sum_jw_j\chi(t)
-a(t)\sum_jw_j\omega_j^2
\int_{t_i}^t G_{R,j}(t,s)\frac{\chi(s)}{a(s)}\,ds .
}
\tag{3}
\]
With the already derived AeST electric Hessian 2a K_B k² and K_B>0, the action fixes the restricted scalar aether source
\[
\boxed{\Delta E_A'=-\frac{a\eta Q}{4K_B}B_\chi .}\tag{4}
\]
Therefore the force depends on the past history of χ, not solely its instantaneous value.

**Proof.** Variation of the action (1) with respect to each q_j yields a linear damped oscillator forced by ω_j sqrt(w_j) kχ/a. Standard linear IVP existence and uniqueness and variation of constants give (2) with a retarded Green function. Substitution into the definition Bχ=Σ_j[w_jχ-(aω_j sqrt(w_j)/k)q_j] proves (3). Variation in the aether longitudinal variable acts through δχ=Qδα_A, and normalizing by the independently fixed AeST electric Hessian gives (4) with the previously frozen sign convention. No later source contributes to an earlier state. QED.

**Strict noninstantaneity, rather than formal convolution.** For a constant background a=1,H=0 and zero auxiliary initial state, the Laplace-domain source for Re(s)>0 is
\[
\boxed{\frac{\widehat B_\chi(s)}{\widehat\chi(s)}
=\sum_j w_j\frac{s^2}{s^2+\omega_j^2}.}\tag{5}
\]
Since the low-frequency limit is 0 while the high-frequency limit is Σ_jw_j>0, no universal instantaneous constant coefficient can reproduce (5) for all allowed histories. This is a constructive proof of **genuine temporal memory** in the restricted model.

**Passive channel in the same static limit.** If χ(0)=q_j(0)=dot q_j(0)=0, define the nonnegative energy
\[
\mathcal E_{\rm b}=\frac{\eta}{4}
\sum_j\left[\dot q_j^2+(\omega_jq_j-\sqrt{w_j}k\chi)^2\right]\ge0.
\]
Differentiating and substituting qddot_j=-ω_j(ω_jq_j-sqrt(w_j)kχ) gives the *exact* identity
\[
\boxed{\frac{d\mathcal E_{\rm b}}{dt}
=\frac{\eta k^2}{2}B_\chi\dot\chi,\qquad
\int_0^T B_\chi\dot\chi\,dt
=\frac{2\mathcal E_{\rm b}(T)}{\eta k^2}\ge0 .}\tag{6}
\]
Equivalently the impedance Σ_jw_j s/(s²+ω_j²) is positive-real for Re(s)>0, since
\[
\Re\frac{s}{s^2+\omega_j^2}
=\frac{(\Re s)(|s|^2+\omega_j^2)}{|s^2+\omega_j^2|^2}>0 .
\]
This proves passivity in the **static-background channel**. The expanding-background energy balance contains H-dependent terms, so (6) is NOT a global stability theorem for the full coupled expanding Einstein–AeST system.

**Scope.** Theorem 1 proves a causal action-derived memory functional in the chosen longitudinal scalar sector and selected no-free-bath branch. It does not prove a uniquely excited physical primordial cosmological mode, full action equivalence or lensing detectability.

## Theorem 2 — exact conditional Weyl response formula for a constrained full system

Assume that a completed original quadratic Einstein–AeST–NL0B action gives a regular **constraint-reduced** all-species scalar evolution on a physically fixed state space,
\[
Y_\eta'=[A_0(\tau)+\eta A_1(\tau)]Y_\eta .
\tag{7}
\]
This assumes that the Einstein, scalar-charge Ward, aether and auxiliary Euler constraints hold, with physically correct and eta-independent approximation-state maps. Assume the true primordial adiabatic initial state is differentiable in η, with derivative Y_ic,1. Assume the only explicit linear η forcing is the action-derived quarter aether-E source (4) and q_j,0 follows the selected continuous retarded eta->0+ branch. Finally let the Weyl potential be the gauge-invariant Bardeen combination W=ell(τ)Y with no direct observer dependence on η.

Let U_0(τ,s) be the propagator of A_0, including only genuinely physical state-transition maps. Then the derivative Y_1=∂ηY|_0 and W_1=∂ηW|_0 obey
\[
Y_1'=A_0Y_1+e_E f_0,\qquad
f_0=-\frac{aQ}{4K_B}B_{\chi,0},\qquad Y_1(\tau_i)=Y_{{\rm ic},1},
\tag{8}
\]
and the exact Duhamel representation
\[
\boxed{
W_1(\tau)
=\ell(\tau)U_0(\tau,\tau_i)Y_{{\rm ic},1}
-\int_{\tau_i}^\tau
\ell(\tau)U_0(\tau,s)e_E
\frac{a(s)Q(s)}{4K_B}B_{\chi,0}(s)\,ds .}\tag{9}
\]
If the propagator is bounded, one obtains the rigorous finite-time estimate
\[
|W_1(\tau)|
\le \|\ell U_0(\tau,\tau_i)\|\|Y_{{\rm ic},1}\|
+\int_{\tau_i}^\tau
|\ell U_0(\tau,s)e_E|\,\frac{a|Q|}{4K_B}|B_{\chi,0}(s)|\,ds .
\tag{10}
\]

**Proof.** Differentiate (7) with respect to η at zero. Under the stated action-equivalence hypothesis, A_1Y_0 is solely e_Ef_0 with the source (4), giving (8). Apply variation of constants to this linear constrained IVP and project with ell to obtain (9). Absolute values and operator norms give (10). QED.

**The theorem is conditional.** It does NOT prove that the actual patched CLASS evolution realizes the complete original covariant action, that the actual primordial physical Y_ic,1 vanishes, or that the physical constraints are propagated across all CLASS approximation changes. These are assumptions whose independent verification would be required before calling (9) a full physical prediction. If eta-dependent matching maps or initial data exist, omitted interface/initial terms invalidate the simplified numerical interpretation.

## Concrete existing obstructions and evidence

**Original action and Ward equation.** The independently archived LW33 reduced scalar-charge identity gives, conditional on the other independent field residuals being zero,
\[
\dot R_\rho+3HR_\rho
=\frac{\eta Qk^2B_\chi}{12a^2}(1-4\gamma),
\quad R_\rho=D_A-D_A^{\rm action}.
\]
It selects γ=1/4 for homogeneous dictionary drift, not a proof that all CLASS trajectories solve the independent scalar equation.

**Primordial state.** Original v019 CLASS repurposes ordinary CDM density and velocity indices for a pressureful AeST effective component but retains dust IC and dust Newtonian gauge transformation. The resulting necessary relative-entropy defect is
\[
S_{A\gamma}^{\rm code}
=-\frac{3w_A}{4(1+w_A)}\delta_\gamma^N .
\]
In the frozen Exp background this coefficient is approximately -4.93e-15 at the earliest actual recorded time, yet there is no independently proved physical Green bound on its later influence. Zero auxiliary q/p selects a no-free-bath history but regular nonzero homogeneous Bessel modes also exist. Hence the physical eta-dependence of the true constrained growing-mode IC is unresolved.

**What the recent CLASS result demonstrates.** The source-locked original isolated CLASS integration, in the chosen branch, produced the preliminary one-point numerical derivative at k=0.1 h/Mpc and z=0.5,
\[
W_0=0.07009097715416947,\quad
W_1=1.8390770226818281\times10^{-9},\quad
W_1/W_0=2.6238427503110188\times10^{-8}.
\]
That is an implemented forced response. It does NOT independently certify the action, Ward, primordial state, numerical uncertainty or gauge-invariant galaxy–Weyl observer. The earlier positive root of the restricted frozen subsystem with externally chosen Δ_A is not an eigenmode proof of the fully constrained Einstein system. A nonzero *driven response* need not be a new freely propagating physical mode.

**Exact upgrade needed for physical proof.** The original full scalar quadratic action, including lapse/shift variation before gauge fixing and all unit-aether and auxiliary multipliers, must yield one closed constraint-invariant physical evolution, with the same propagation and source as (7)–(9). Its primordial radiation-era constrained adiabatic eigenvector, including eta derivative and the selected bath branch, must be fixed. Only then can an independently bounded and nonzero physical Weyl transfer be claimed. Detectability needs a physical tracer and lensing projection and survey covariance in addition.

## Decision

**PROVED now** — genuine retarded action-derived scalar memory, its quarter forcing under the frozen reduced Hessian, and static passive-channel identity.

**PROVED conditionally** — exact full-physics Duhamel formula (9) and finite-time bound (10), assuming the complete original constrained action evolution and physically correct initial data.

**NOT PROVED** — an excited, independently certified physical matter-memory eigenmode, full time-dependent Einstein–AeST–NL0B cosmological constraint closure, physical numerical Weyl gain, or DES observability.

The next research deliverable is a single *joint constrained action and primordial initial-state proof*, not another series of numerical PASS stages. If the constraints close and the source excites a physical mode, upgrade the claim. If not, do not describe the preliminary CLASS tangent as an observational prediction.

Existing sources
- [Joint GE05/GE06 restricted action and scalar-charge Ward source](ge19_20261111_joint_action_to_CLASS_scalar_source_matrix.md)
- [Exact original CLASS all-species and primordial IC defect](ge19_20261111_all_species_Einstein_operator_and_adiabatic_IC_block.md)
- [Auxiliary regular mode and retarded initial-state choice](ge19_20261111_auxiliary_initial_state_and_physical_observer_decision.md)
- [Original oscillator-energy and Volterra bound](ge19_20261112_retarded_bath_energy_amplification_gate.md)
- [Constrained frozen operator derivation](../ge19/physics_gate/constraint_projected_joint_operator_20261112.py)
- [Actual source-locked native CLASS numerical result](../results/ge19_one_forced_tangent_20261113/GE19_ONE_FORCED_TANGENT_SCREEN.json)
