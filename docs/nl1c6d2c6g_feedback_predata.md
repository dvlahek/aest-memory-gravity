# D2C6G pre-data declaration — direct-memory weak-field metric feedback

Date: 2026-09-11

This declaration is frozen before any D2C6G target result is evaluated.

Parent chain:

- `NL1C6D2C6E_LARGER_ETA_RETAINED_SCALAR_CURRENT_PASS`;
- historical `NL1C6D2C6F_FINITE_ETA_DIRECT_GRAVITATIONAL_SOURCE_FAIL` retained unchanged;
- `NL1C6D2C6F_R1_DIRECT_BATH_SOURCE_CONVERGENCE_PASS`;
- D2C6F-R1 result record commit `3177e315a85fe95196840ba66765a294ed3e3260`.

D2C6F-R1 licenses direct `N_bath=256` as the primary bath and direct `N_bath=512` as the bath-order control for a separately preregistered weak-field feedback stage.

## Scientific question

Determine the first self-consistent gravitational backreaction of the certified finite-positive-eta memory sector on the scalar/aether trajectory over the already validated `z=6..0.2` nonlinear interval:

`memory state -> direct memory stress -> Newtonian-gauge metric response -> memory/scalar state`.

This stage is physics, not a further bath-fitting exercise. It asks how large the action-derived metric response is, whether it remains inside the weak-field domain, how it changes the finite-memory trajectory, and how strongly that response depends on the 27 frozen nonlinear completions.

## Scope boundary

D2C6G is **not** called full nonlinear AeST+memory and does not perform an observational likelihood.

The direct memory metric source is fed back self-consistently into the scalar/aether evolution, but the non-memory CLASS matter/radiation and the baseline AeST effective-fluid stress histories remain frozen to the certified CLASS trajectory. Their induced response to the new memory metric is deferred to the next stage.

The certified modewise finite-memory prehistory is retained as the boundary state at `z=6`. Direct memory metric feedback is activated algebraically from the first D2C6G RHS evaluation at `z=6`; no claim is made here about accumulated metric feedback at `z>6`. Thus D2C6G is a `z=6`-initialized weak-field feedback experiment over the frozen nonlinear science interval.

## Frozen physics and ensemble

Freeze exactly:

- `K_B=0.0665` and the corrected Exp AeST background already used by D2C6E/F;
- `tau H0=1`;
- physical `eta=0.125` only;
- all 27 D2C6B completions, `sigma in {-1,0,+1}`, `kind in {simple,exponential,sharp}`, `beta0 in {1,0.5,0.1}`;
- the same six seeded spatial modes/phases, periodic box and checkpoints `z={6,5,4,3,2,1.5,1,0.5,0.2}`;
- primary `Nx=128`, `Nstep=4096`;
- direct tan-Gauss-Legendre Drude bath `N_bath=256` primary;
- direct `N_bath=512` only as a bath-order control;
- the D2C6D finite-memory scalar-current source and D2C6F action-derived direct metric sources without refitting or amplitude rescaling.

No eta scan is performed in D2C6G. No source sign or desired amplitude is a gate.

## Action-to-CLASS stress normalization

The frozen NL0B memory action is in the **same gravitational normalization as AeST**,

`S_mem = (1/(16 pi G_tilde)) integral sqrt(-g) L_mem`.

Define the raw tensor associated with `L_mem` by

`delta(sqrt(-g)L_mem) = -(1/2) sqrt(-g) Traw_mem^{mu nu} delta g_{mu nu}`

with the corresponding index placement used consistently below. Because this sector shares the gravitational prefactor, the Einstein equation receives `Traw_mem/2`, rather than `8 pi G_tilde Traw_mem`.

CLASS stores geometric stress sums in the convention in which the Newtonian-gauge constraints carry the coefficient `3/2`. Therefore the CLASS-equivalent direct-memory stress variables are the raw action stress divided by six.

For the D2C6F ADM source derivatives on flat FLRW,

- raw energy density: `rho_raw = -S_N/a^3`;
- raw longitudinal momentum component: `T0x_raw = S_b/a^3`;
- raw longitudinal pressure: `p_parallel_raw = S_L/a^2`;
- raw transverse pressure: `p_perp_raw = S_R/(2 a^2)`.

The frozen CLASS-equivalent fields are therefore

`delta_rho_mem = -S_N/(6 a^3)`,

`q_mem = (1/6) d_x(S_b/a^3)`,

`rho_plus_p_shear_mem = -S_shear/(9 a^2)`,

where `S_shear=S_L-S_R/2`. For diagnostics only,

`delta_p_mem=(S_L+S_R)/(18 a^2)`.

The momentum sign is fixed by the action: at zero shift `S_b/a^3 = -(1/2) qdot q_x`, equal to the canonical raw `T^0_x` for the frozen per-node normalization. The shear factor follows from the CLASS scalar convention `(rho+p)sigma=-(2/3)(p_parallel-p_perp)`.

These factors are frozen before the feedback result is inspected.

## Frozen metric closure

Use the exact flat Newtonian-gauge CLASS scalar constraints already frozen in D2B/D2C5. For each nonzero Fourier mode,

`delta_phi_k = -(3/2) a^2/k^4 [ k^2 delta_rho_mem,k + 3 Hconf q_mem,k ]`,

`delta_psi_k = delta_phi_k - (9/2) a^2/k^2 rho_plus_p_shear_mem,k`,

with `Hconf=a H`.

The direct-memory zero mode is excluded from this perturbative metric closure because NL0B freezes the homogeneous memory background correction to zero. Set `delta_phi(k=0)=delta_psi(k=0)=0`.

The D2C6F/R1 gravitational-source certification was explicitly frozen over Fourier indices `n=0..32`. D2C6G therefore feeds back only the validated nonzero band `1<=|n|<=32`; higher direct-stress harmonics are set to zero in the feedback metric. This is a numerical validity cutoff, not a fitted physical scale.

The scalar/aether RHS uses

`psi_total = psi_CLASS_base + delta_psi_mem`.

In the stable canonical equations this changes only the defining relation `d alpha/d tau = a(E-psi_total)` at the retained weak-field order. The already certified finite-memory scalar-current source remains unchanged.

## Primary run

For every one of the 27 frozen completion members, evolve from `z=6` to `z=0.2` with:

- `eta=0.125`;
- direct bath 256;
- `Nx=128`, `Nstep=4096`;
- direct-memory metric feedback enabled at every RK stage.

At every checkpoint report the action stress, `delta_phi_mem`, `delta_psi_mem`, `delta(phi+psi)_mem`, scalar state, `E`, scalar-current constraint, `min(1+j_eff)`, and completed-square energy identity.

## Frozen control members

To avoid turning the first feedback experiment into another full numerical campaign, the expensive bath/time/space controls are frozen to exactly three sentinels spanning all sigma, kind and beta categories:

1. `sigma=+1 | kind=simple | beta0=0.1` — the historical worst compressed-bath source sector;
2. `sigma=0 | kind=exponential | beta0=0.5` — central completion;
3. `sigma=-1 | kind=sharp | beta0=1` — opposite completion corner.

No sentinel is changed after D2C6G output is inspected.

## Frozen gates

### G1 — provenance and exact coverage

PASS requires:

- D2C6F-R1 PASS/result record is an ancestor;
- this preregistration is an ancestor;
- exact 27-member primary coverage;
- `eta=0.125`, primary bath 256, control bath 512;
- no observational likelihood or data-dependent parameter choice.

### G2 — action-stress / CLASS-map identity

A deterministic independent audit must verify:

- `rho_raw=-S_N/a^3`;
- `T0x_raw=S_b/a^3` including its canonical sign;
- `p_parallel_raw=S_L/a^2`;
- `p_perp_raw=S_R/(2a^2)`;
- shared-gravitational-prefactor to CLASS normalization `1/6`;
- CLASS shear mapping `-(p_parallel-p_perp)/9` after the `1/6` normalization;
- metric Fourier constraints reconstructed from the mapped stresses.

Required normalized discrepancy: `<=1e-12` for algebraic identities and `<=1e-10` for the numerical Fourier reconstruction.

### G3 — feedback-off parent regression

For the three frozen sentinel members, the D2C6G integrator with the metric feedback switch set exactly to zero must reproduce the D2C6F-R1/direct-256 no-feedback trajectory using the same z=6 boundary state.

Required relative L2 for canonical state and `E`: `<=1e-10`.

This is a code-path regression only; it is not a physics-amplitude gate.

### G4 — all-27 feedback health and weak-field domain

All 27 primary feedback trajectories must:

- remain finite;
- retain scalar-current constraint `<=1e-10`;
- retain `min(1+j_eff)>0`;
- retain completed-square energy identity `<=1e-12`;
- have finite mapped stress and finite metric response;
- remain within the declared weak-field metric domain `max(|delta_phi_mem|,|delta_psi_mem|) <= 1e-2`.

The `1e-2` metric bound is a validity bound for the weak-field derivation, not a target signal size.

### G5 — Einstein-constraint reconstruction

At every stored checkpoint the metric increments reconstructed from the mapped direct-memory stresses must satisfy the frozen Hamiltonian/momentum combined constraint and the shear constraint with normalized Fourier residual `<=1e-10` over `1<=|n|<=32`.

### G6 — bath-order convergence on the three sentinels

For each sentinel, compare direct-256 with direct-512 feedback runs at the same `Nx=128`, `Nstep=4096`.

The maximum relative L2 over low-band signatures of canonical state, `E`, `delta_phi_mem`, and `delta_psi_mem` must be `<=1e-2`.

### G7 — time convergence on the three sentinels

Compare `Nstep=4096` with `8192`, direct-256, `Nx=128`.

The same maximum low-band relative L2 must be `<=2e-3`.

### G8 — space convergence on the three sentinels

Compare `Nx=128` with `Nx=256`, direct-256, `Nstep=4096`, using the common validated Fourier band `1<=|n|<=32`.

The same maximum relative L2 must be `<=5e-3`.

### G9 — scope integrity

No PASS condition may depend on:

- the sign of `delta_phi_mem` or `delta_psi_mem`;
- a minimum feedback amplitude;
- a preferred completion ordering;
- a desired lensing/growth direction;
- Planck, ACT, SPT, DESI or other observational likelihood improvement.

## Non-gating physics diagnostics

Report for all 27 members:

- checkpoint RMS/max of `delta_phi_mem`, `delta_psi_mem`, and `delta(phi+psi)_mem`;
- global relative L2 of `delta_psi_mem` to the frozen CLASS base `psi`;
- feedback-on versus feedback-off displacement in `alpha`, `chi`, `E` and canonical state;
- direct stress component RMS and the density/momentum/shear decomposition of the metric response;
- completion-family min/median/max spread;
- which redshift and member maximize the feedback metric response.

These diagnostics are scientific results and are not tuned into gates after inspection.

## Classification and continuation

PASS label:

`NL1C6D2C6G_DIRECT_MEMORY_METRIC_FEEDBACK_PASS`

FAIL label:

`NL1C6D2C6G_DIRECT_MEMORY_METRIC_FEEDBACK_FAIL`

INCOMPLETE is reserved for a technical execution failure that prevents evaluation of the frozen gates.

A PASS means that direct finite-memory stress produces a numerically certified, self-consistent weak-field metric feedback over `z=6..0.2` with the external non-memory stress histories frozen. It licenses the next **CLASS matter/AeST response** step, in which the mapped memory stress is injected into the CLASS metric sums so ordinary matter/radiation and the AeST effective-fluid perturbations respond dynamically.

A D2C6G PASS does **not** by itself license Planck/ACT/SPT/DESI inference and does not establish a full arbitrary-amplitude nonlinear GR/AeST solution.
