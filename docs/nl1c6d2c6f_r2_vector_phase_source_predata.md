# D2C6F-R2 pre-data declaration — action-consistent vector-phase direct stress

Date: 2026-09-11

This follow-up is declared before any D2C6F-R2 target result.

Historical records remain unchanged:

- D2C6F direct-source classification remains `FAIL` because its compressed 39/47 bath source convergence gate failed;
- D2C6F-R1 remains a numerical `PASS` for the old direct-stress reconstruction, but its feedback license is superseded by `docs/nl1c6d2c6g_blocked_pending_r2.md` after the vector-phase issue was identified before D2C6G implementation.

## Scientific issue

The certified scalar bath bridge is

`z_j = omega_j q_{j,L}/(k sqrt(w_j))`

for longitudinal Fourier amplitudes. In the local NL0B/NL1C3B action, however, the direct metric stress is built from the physical real-space vector component `U_{j,x}` and the projected scalar gradient `X_x`.

For a scalar real-space bath potential `z_j(x)`, the action-consistent longitudinal vector component is

`q_{j,x}(x) = sqrt(w_j)/omega_j * d_x z_j(x)`,

and

`qdot_{j,x}(x) = sqrt(w_j)/omega_j * d_x z'_j(x)/a`.

The scalar-gradient drive is

`X_x(x)=d_x chi(x)/a`.

Thus `q_{j,x}` and `X_x` carry the same signed spatial-derivative phase. The inherited D2C6F source code used the positive spectral operator `|d_x| z_j` for the bath vector while using `d_x chi` for `X_x`. For a cosine mode this puts the two terms in quadrature and is not the local-vector realization of the frozen action.

R2 changes **only** this direct-stress reconstruction:

`|d_x| z_j  ->  d_x z_j`,

`|d_x| z'_j ->  d_x z'_j`.

The finite-memory scalar-current trajectory, bath evolution, eta, nonlinear completion, background, and all previously certified retained equations are unchanged.

## Frozen physical configuration

Use:

- `eta=0.125`;
- `tau H0=1`;
- all 27 frozen D2C6B completions;
- same six seeded modes/phases and checkpoints `z={6,5,4,3,2,1.5,1,0.5,0.2}`;
- direct tan-Gauss-Legendre bath 256 as primary;
- direct bath 512 as bath-order reference;
- primary `Nx=128`, `Nstep=4096`;
- the same NL0B/NL1C3B local action source formulas for `S_N,S_b,S_L,S_R` after the vector reconstruction is corrected.

No physics parameter or source amplitude is fitted.

## Frozen sentinel controls

The expensive 512/time/space controls are fixed to:

1. `sigma=+1 | kind=simple | beta0=0.1`;
2. `sigma=0 | kind=exponential | beta0=0.5`;
3. `sigma=-1 | kind=sharp | beta0=1`.

These span all sigma, kind and beta categories and include the historical worst compressed-bath sector.

## Frozen gates

### R2-1 — provenance and exact coverage

Require the D2C6G block note and this preregistration to be ancestors, exact 27-member primary coverage, `eta=0.125`, primary direct bath 256 and control direct bath 512.

### R2-2 — local vector-phase identity

Use deterministic manufactured periodic fields with `z=chi/a` at fixed `a`. For every tested node, reconstruct

`q_x=sqrt(w)/omega*d_x z`

and verify the completed-square alignment

`omega q_x - sqrt(w) X_x = 0`, `X_x=d_x chi/a`,

with relative/normalized residual `<=1e-12`.

Also verify the derivative bridge for `z'` and an independent Fourier-mode reconstruction of `d_x z` to `<=1e-12`.

The old `|d_x|` reconstruction is reported only as a forensic diagnostic and is not allowed in the R2 target source.

### R2-3 — action-source identity

Retain the D2C6F finite-difference variation audit of the local `N,b,L,R` action source with maximum relative error `<=1e-6`, and the completed-square energy identity `<=1e-12` on all primary runs.

### R2-4 — all-27 trajectory/source health

All 27 primary runs must remain finite and source-finite, retain scalar-current constraint `<=1e-10`, retain `min(1+j_eff)>0`, and have non-negative completed-square energy up to numerical tolerance `>=-1e-14`.

### R2-5 — direct bath convergence

For the three frozen sentinels, direct 256 versus direct 512 corrected-source low-band relative L2 over each of `S_Psi,S_Phi,S_b,S_shear` must be `<=1e-2`.

The canonical state and `E` difference must also be `<=1e-2`.

### R2-6 — time convergence

For the three sentinels compare direct-256 `Nstep=4096` versus `8192` at `Nx=128`. Maximum corrected-source low-band relative L2 must be `<=2e-3`.

### R2-7 — space convergence

For the three sentinels compare direct-256 `Nx=128` versus `Nx=256` at `Nstep=4096` over the common Fourier band `n=0..32`. Maximum corrected-source low-band relative L2 must be `<=5e-3`.

### R2-8 — scope integrity

No gate depends on source sign, minimum amplitude, completion ranking, metric/lensing direction, or observational likelihood.

## Non-gating physics diagnostics

Report for all 27 primary members:

- corrected source RMS by checkpoint;
- ratio of corrected-source RMS to the historical old-phase source RMS when the old reconstruction is evaluated on the same trajectory;
- completed-square kinetic and potential contributions;
- density/momentum/spatial/shear source hierarchy;
- completion-family min/median/max spread.

Additionally project the corrected source **one way** through the exact frozen Newtonian-gauge metric constraints, solely as a non-gating diagnostic. The normalization is frozen here before implementation.

The NL0B memory action carries the same overall `1/(16 pi G_tilde)` prefactor as the AeST gravitational action. Defining the raw tensor from the memory Lagrangian bracket, its contribution to the Einstein equation is one half of that raw tensor. CLASS geometric stress sums use the scalar-constraint coefficient `3/2`. Therefore the equivalent direct-memory contribution to CLASS stress sums is the raw action stress divided by six.

Use

- `delta_rho_mem = -S_N/(6 a^3)`;
- `T0x_mem = S_b/(6 a^3)`;
- `q_mem = d_x T0x_mem`;
- `rho_plus_p_shear_mem = -S_shear/(9 a^2)`.

For `1<=|n|<=32`, with `Hconf=a H`, use

`delta_phi_k = -(3/2) a^2/k^4 [k^2 delta_rho_mem,k + 3 Hconf q_mem,k]`,

`delta_psi_k = delta_phi_k - (9/2) a^2/k^2 rho_plus_p_shear_mem,k`.

Set the zero mode to zero and omit modes above `|n|=32` from this one-way diagnostic because the source comparison band was frozen at `n=0..32`.

Report `delta_phi_mem`, `delta_psi_mem`, and `delta(phi+psi)_mem`, but do not feed them back into the trajectory in R2. Their amplitudes and signs are not R2 gates.

## Classification

PASS:

`NL1C6D2C6F_R2_VECTOR_PHASE_DIRECT_SOURCE_PASS`

FAIL:

`NL1C6D2C6F_R2_VECTOR_PHASE_DIRECT_SOURCE_FAIL`

INCOMPLETE is reserved for technical execution failure before the gates can be evaluated.

Only an R2 PASS may re-license a newly preregistered D2C6G metric-feedback implementation. R2 itself is not an observational result.
