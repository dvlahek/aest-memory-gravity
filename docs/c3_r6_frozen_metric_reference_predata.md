# C3 R6 pre-data declaration — frozen-metric CLASS-variable tangent reference repair

## Historical status

Historical D2C6C R2/R3/R4 and R5 outcomes remain unchanged. In particular, R5 run 34496088156 and the post-data scale/sign run 34498747055 remain `C3_R5_ZERO_SAFE_TANGENT_FAIL`. Finite-positive-eta nonlinear memory remains unlicensed.

## Technical fault being repaired

The original D2C6C pre-data declaration explicitly froze background quantities and the external CLASS metric/matter fields at eta=0. The R5 CLASS reference nevertheless generated the signed-lambda tangent by perturbing the full coupled CLASS system. That allows the forced AeST perturbation to alter the Einstein metric sector and feed back into the AeST variables. The R5 post-data scale/sign audit showed strongly mode-dependent shape differences, inconsistent with a single normalization/sign error.

R6 repairs only this reference-boundary-condition mismatch. It does not modify the D2C6C offline tangent equations, bath equations, physical parameters, constitutive family, or gates.

## Frozen reference equations

For each of the same six frozen Fourier modes, integrate the linearized AeST CLASS-variable subsystem with state

`u=(delta_delta, delta_theta, delta_alpha, delta_E)`

while holding the eta=0 background and external metric perturbations fixed. The equations are the direct variational form of the existing patched CLASS AeST block:

`delta_chi = Q (a delta_theta/k^2 + delta_alpha)`

`delta_Pi = cad2 delta_delta + cad2 k^2/(3 a^2 rho) [K_B delta_E + (2-K_B) delta_chi]`

`delta_delta' = 3 a H [w delta_delta - delta_Pi] - (1+w) delta_theta`

`delta_theta' = (3 cad2 - 1) a H delta_theta + k^2 delta_Pi/(1+w)`

`delta_alpha' = a delta_E`

`delta_E' = a/K_B {KQ delta_chi - (2-K_B)[Q delta_Pi/(1+w) + (H+Q) delta_chi - 3 cad2 H Q delta_alpha]} - a H delta_E + F_mem`

with the same eta=0 memory forcing

`F_mem = -a Q B_chi^(0)/(2 K_B)`.

No metric-continuity or metric-Euler tangent term is included, because their eta-variation is frozen by the original D2C6C declaration.

Background effective-fluid coefficients use the already certified corrected Exp background:

`rho=(Q KQ-K)/3`, `p=K/3`, `w=p/rho`, `cad2=KQ/(Q KQQ)`.

## Bath/source and prehistory

Use the R5 zero-safe memory-off CLASS core trajectory and the already validated order-39 tauH0=1 offline bath propagation to construct `F_mem`. The six exact k modes, regular zero tangent at each mode's earliest available retarded-history time, and full pre-z=6 propagation convention are unchanged from R3/R5. The force table is linearly interpolated in conformal time, matching the existing CLASS external-force convention. No backward extrapolation is allowed.

## Numerical rule

Use deterministic RK4 independently for each mode with step no larger than the frozen D2C6C main step `(tau(z=0.2)-tau(z=6))/4096`. Frozen checkpoints are evaluated exactly by ending a step at each checkpoint. A descriptive half-step control may be reported but does not replace any scientific gate.

## Gate

The repaired reference is converted to the same `alpha`, `E`, and `theta` modal arrays expected by the unchanged D2C6C `reference_compare` function. The original C3 gate is unchanged:

- alpha relative L2 <= 5e-3
- E relative L2 <= 5e-3
- chi relative L2 <= 5e-3

No post-data scale fit, sign flip, amplitude rescaling, mode removal, checkpoint removal, or threshold change is permitted.

A PASS only repairs the eta=0 linear-reference consistency test and does not retroactively alter historical FAIL classifications. A FAIL remains a genuine mismatch between the frozen-metric CLASS-variable tangent and the offline stable-canonical tangent, requiring equation-level follow-up. Finite-positive-eta nonlinear memory remains unlicensed in either case until the full D2C6C repair sequence is explicitly completed.