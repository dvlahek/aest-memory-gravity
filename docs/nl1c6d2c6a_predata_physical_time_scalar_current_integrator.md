# NL1C6D2C6A pre-data: physical-time nonlinear FLRW scalar-current integrator

Status: **PREREGISTERED BEFORE ANY D2C6A TRAJECTORY RESULT**.

## 1. Purpose and scope

D2C5 has passed and licenses nonlinear branch evolution within the frozen MOND weak-field ordering. D2C6A is the numerical implementation gate for that evolution.

The target is deliberately narrower than fully coupled nonlinear structure formation. We evolve the nonlinear AeST longitudinal scalar/vector subsystem on the **corrected physical FLRW background**, with the corrected `eta=0` CLASS metric history used as the externally supplied weak-field forcing permitted by D2C5. Matter and metric backreaction are not promoted beyond their certified linear sector in D2C6A.

Therefore a D2C6A trajectory is a **nonlinear AeST-field trajectory on a physical linear cosmological forcing history**. It is not yet a nonlinear matter-power, halo, collapse, memory, or likelihood result.

No pseudo-time, homotopy parameter, arclength parameter, constitutive continuation, or solver parameter may be interpreted as physical time.

## 2. Frozen theory and numerical pilot member

Use the corrected branch `v053-exp-normalization-corrected`, pinned CLASS commit

`e85808324f51fc694d12e3ed7439552a3c3f9540`.

Required inherited results:

- `NL1C6D2N_EXP_NORMALIZATION_AUDIT_PASS`;
- `NL1C5BC_CORRECTED_BARYON_SOURCE_FREEZE_PASS`;
- `NL1C6D2AC_CORRECTED_BARYON_MATTER_SECTOR_AUDIT_PASS`;
- `NL1C6D2C4R1_DERIVATIVE_CONTROL_REPAIR_PASS`;
- `NL1C6D2C5_ACTION_LEVEL_FLRW_LONGITUDINAL_REDUCTION_PASS`.

For this **integrator validation only**, freeze the central completion member

- `sigma = 0`;
- interpolation `simple`;
- `beta0 = 1`.

This is not outcome-based model selection. If D2C6A passes, the later D2C6B physics campaign must evaluate the full preregistered 27-member `(sigma, interpolation, beta0)` family.

Other frozen parameters are unchanged: `K_B=0.0665`, `K2=9500`, `Q0=1e-4 Mpc^-1`, `Z0=1e-17 Mpc^-1`, `a0=1.2e-10 m/s^2`, and the six physical modes `k_h=[0.03,0.05,0.08,0.10,0.15,0.20] h/Mpc` with the existing frozen phases and primordial mode amplitudes.

Memory is disabled and `eta=0` throughout.

## 3. Physical equations

Use the D2C5 action-derived variables

\[
U=\frac{P_\chi}{2a^3K_{QQ}},
\]

and recover `E` at every physical time from the canonical elliptic identity

\[
P_\alpha+\bar Q P_\chi
=-2aK_B\nabla^2E-2Aa\nabla^2\chi,
\qquad A=2-K_B.
\]

With zero spatial means fixed for `E` and `chi`, solve

\[
\nabla^2(K_BE+A\chi)
=-\frac{P_\alpha+\bar QP_\chi}{2a}.
\]

The cosmic-time kinematics are

\[
\dot\chi=U+\bar Q E+\dot{\bar Q}\alpha,
\qquad
\dot\alpha=E-\Psi.
\]

The physical dynamics are

\[
\dot P_\chi=-2Aa\nabla^2E
+2Aa\nabla\cdot[(1+j_{\rm eff})\nabla\chi]
-2aK_Q\nabla^2\alpha,
\]

\[
\dot P_\alpha=-2a^3K_{QQ}U\dot{\bar Q}
-2aK_Q\nabla^2\chi
+2aK_Q\bar Q\nabla^2\alpha.
\]

For the D2C6A pilot `sigma=0`,

\[
j_{\rm eff}=j_{\rm simple}(x),
\qquad
x=\frac{|\nabla\chi|}{a\,a_{0,geo}},
\]

with `a0_geo = a0*Mpc/c^2` and comoving spatial derivatives.

The equations are integrated in conformal time `tau`, using `d/dtau = a d/dt`. This is a coordinate conversion only; `tau` is physical FLRW conformal time from CLASS.

## 4. Corrected background and forcing

Regenerate the corrected CLASS `eta=0` run in the isolated corrected CLASS tree.

Use dense scalar histories for the six frozen `k_output_values`. Required fields are:

- `a` and `tau [Mpc]`;
- `psi`;
- `alpha_aest` (or the exact repository alias `alpha`);
- `E_aest` (or alias `E`);
- effective-AeST `theta_cdm` (or `t_cdm`) used by the frozen CLASS bridge.

If a required field is not exposed, D2C6A is `INCOMPLETE`, not a physical FAIL.

Reconstruct the homogeneous corrected charge from the already certified corrected Exp shift-charge law. Calibrate its conserved charge from the public corrected CLASS `rho_cdm(a=1)` exactly as in the R1 background audit. Use

\[
K_Qa^3=I_0,
\qquad
\dot{\bar Q}=-3H\frac{K_Q}{K_{QQ}}.
\]

The forcing field `Psi(tau,x)` is reconstructed from the six corrected CLASS mode histories using the frozen primordial mode amplitudes and phases already used by the nonlinear source program. No amplitude is fit or rescaled to improve the trajectory.

## 5. Initial physical state

Start at the physical time corresponding to `z=6` and evolve to `z=0.2`.

For each CLASS mode define

\[
\theta_{pot}=a\Theta_A/k^2,
\qquad
\chi=\bar Q(\theta_{pot}+\alpha),
\]

using the exact D2C5/frozen-CLASS convention. Construct real-space `alpha`, `E`, `chi`, and `Psi` from the six modes.

Obtain `dchi/dtau` at the initial time from a cubic spline through the corrected CLASS-derived `chi(tau)` history for each mode. Then

\[
U=\frac{1}{a}\frac{d\chi}{d\tau}-\bar QE-\dot{\bar Q}\alpha,
\]

\[
P_\chi=2a^3K_{QQ}U,
\]

and construct `P_alpha` directly from its canonical definition. No static solver, branch seed, quasistatic root, or R3 state is used as an initial condition.

## 6. Spatial and temporal discretization

Use the existing physical one-dimensional periodic box

\[
L=\frac{2\pi}{0.01h}\;{\rm Mpc},
\]

with the same six Fourier modes and frozen phases.

All spatial derivatives are pseudospectral and the nonlinear flux uses the existing 2/3 dealiasing rule.

Use explicit classical RK4 in physical conformal time with **fixed, preregistered** discretizations:

- primary: `Nx=128`, `Nstep=4096`;
- time control: `Nx=128`, `Nstep=8192`;
- spatial control: `Nx=256`, `Nstep=4096`.

The physical interval is the same `tau(z=6)` to `tau(z=0.2)` in all three runs. No adaptive tolerance, step rejection, or post-result timestep tuning is allowed in D2C6A.

## 7. Independent linear control

Run a fourth trajectory on the primary grid with the nonlinear constitutive contribution disabled only as a **numerical linearization control**, i.e. set `j_eff=0` in the scalar-current flux while keeping all background, forcing, initial conditions and canonical equations unchanged.

At 9 fixed redshifts

`z = [6,5,4,3,2,1.5,1.0,0.5,0.2]`,

reconstruct the corrected CLASS linear real-space `alpha`, `E`, and `chi` from the same six modes. Compare the integrated linear-control fields with CLASS using one global relative L2 norm per field over all checkpoint samples and spatial points. This control is not a new physical model and is not used for a science claim.

## 8. Preregistered gates

### I1 provenance/data gate

Require the corrected CLASS provenance audit PASS and all required dense fields present and finite over `0.2 <= z <= 6`.

### I2 initial-state gate

At `z=6` require:

- canonical elliptic identity residual <= `1e-12`;
- `P_chi` definition residual <= `1e-12`;
- all real-space state arrays finite;
- zero-mode residual of reconstructed perturbation fields <= `1e-12` relative to their RMS scale.

### I3 linear-control gate

For the 9 frozen checkpoints, require global relative L2 error against corrected CLASS of

- `alpha <= 5e-3`;
- `E <= 5e-3`;
- `chi <= 5e-3`.

If exact CLASS aliases required for this mapping are absent, classify `INCOMPLETE` rather than changing the gate.

### I4 physical nonlinear trajectory health

For the primary nonlinear trajectory require:

- all evolved states finite through `z=0.2`;
- no explicit branch continuation, pseudo-time, root solve, or post-step projection;
- reconstructed elliptic canonical identity normalized residual <= `1e-10` at every stored checkpoint;
- no non-finite `j_eff` or `x`;
- the maximum constitutive derivative `1+j_eff` remains strictly positive.

### I5 fixed timestep convergence

Compare primary and time-control trajectories at the 9 frozen redshift checkpoints. Require the conservative maximum global relative L2 difference over `alpha`, `chi`, `P_chi`, and `P_alpha` to be <= `2e-3`.

### I6 spatial convergence

Spectrally restrict the `Nx=256` control fields to the `Nx=128` grid and compare at the same 9 checkpoints. Require the conservative maximum global relative L2 difference over `alpha`, `chi`, `P_chi`, and `P_alpha` to be <= `5e-3`.

### I7 descriptive nonlinear response

Report, without a PASS/FAIL threshold:

- nonlinear-versus-linear global relative L2 for `alpha`, `chi`, and reconstructed `E`;
- maximum and percentile range of `x`;
- fraction of grid-time samples with `x<1`, `1<=x<10`, and `x>=10`;
- maximum `j_eff` and minimum `1+j_eff`.

These are descriptive diagnostics only and cannot be used to select a favorable completion member.

### I8 scope gate

No memory forcing, finite eta, likelihood, cosmological refit, nonlinear matter evolution, static R3 solver, or observational comparison is permitted.

## 9. Classification

All I1-I8 applicable gates pass:

`NL1C6D2C6A_PHYSICAL_TIME_SCALAR_CURRENT_INTEGRATOR_PASS`

A required exposed input/mapping is unavailable but no derived identity is contradicted:

`NL1C6D2C6A_PHYSICAL_TIME_SCALAR_CURRENT_INTEGRATOR_INCOMPLETE`

A numerical/derived preregistered gate is evaluated and fails:

`NL1C6D2C6A_PHYSICAL_TIME_SCALAR_CURRENT_INTEGRATOR_FAIL`

A FAIL here is a numerical/reduced-system implementation result. It is not evidence of physical nonexistence of an AeST cosmological branch unless a later separately preregistered convergence/singularity study establishes that claim.

Only PASS licenses the D2C6B all-27-member physical nonlinear-field trajectory campaign.