# D2C6G pre-data — eta=0 direct-metric tangent and weak-field amplitude calibration

Date: 2026-09-11

Status: preregistered after D2C6F-R2 completed and before any D2C6G target output.

Frozen label:

`NL1C6D2C6G_ETA0_DIRECT_METRIC_TANGENT_CALIBRATION`

## Motivation

D2C6F-R2 recertified the direct memory stress with the action-consistent signed longitudinal vector phase and passed all source, bath, time, space, health and action identities. Its non-gating one-way metric diagnostic at `eta=0.125`, however, produced metric responses far outside the weak-field regime. A self-consistent feedback run at that amplitude would therefore not be a controlled continuation of the weak-field derivation.

D2C6G does **not** close the feedback loop yet. It determines the physically admissible eta scale from the independently certified eta=0 nonlinear trajectories.

The key identity is that the local memory action contains `sqrt(eta) U_j`, so its direct metric stress is exactly proportional to eta when evaluated on a fixed eta=0 trajectory. Thus D2C6G computes

`d S_mem / d eta |_(eta=0)`

and the corresponding one-way Newtonian-gauge metric tangent

`d deltaPhi_mem/deta`, `d deltaPsi_mem/deta`.

No finite-eta output is used to choose this tangent.

## Frozen inputs

Retain exactly:

- all 27 D2C6B nonlinear completion members;
- the certified eta=0 nonlinear trajectory equations and full retarded bath prehistory;
- `tau H0 = 1`;
- direct tan-Gauss-Legendre Drude bath `N=256` primary;
- direct bath `N=512` control;
- `Nx=128`, `Nstep=4096`;
- the nine checkpoints `z={6,5,4,3,2,1.5,1,0.5,0.2}`;
- corrected R2 signed-vector stress reconstruction;
- the R2 action-to-CLASS stress normalization and one-way Newtonian-gauge metric projection;
- the frozen external CLASS `psi` history for comparison to the cosmological baseline.

The physical trajectory coupling is exactly `eta=0`. The reported direct stress is a **unit-eta coefficient** evaluated on that eta=0 state, not a finite-eta trajectory.

## Unit-eta source construction

For each eta=0 completion trajectory and its passive direct bath, evaluate the corrected R2 direct source formulas with the explicit overall eta factor removed. Denote these unit coefficients by

`S_hat = d S_mem/d eta |_(eta=0)`.

The actual direct stress in the infinitesimal eta limit is

`S_mem(eta) = eta S_hat + O(eta^2)`.

Project `S_hat` through the same preregistered R2 one-way metric constraints to obtain

`Phi_hat = d deltaPhi_mem/deta |0`,
`Psi_hat = d deltaPsi_mem/deta |0`,
`Weyl_hat = d delta(Phi+Psi)_mem/deta |0`.

## Baseline comparison and frozen amplitude definitions

At each checkpoint reconstruct the frozen CLASS baseline `psi_base(x)` from the same six seeded modes used by the nonlinear box.

Report its RMS and maximum absolute amplitude.

For each member and checkpoint define the eta values at which the **one-way tangent** reaches fixed fractions of the baseline psi RMS:

`eta_1pct = 0.01 * psi_base_rms / Psi_hat_rms`,
`eta_10pct = 0.10 * psi_base_rms / Psi_hat_rms`,
`eta_100pct = 1.00 * psi_base_rms / Psi_hat_rms`.

Also report absolute weak-field scales

`eta_abs_1e-2 = 1e-2 / Psi_hat_maxabs`,
`eta_abs_1e-1 = 1e-1 / Psi_hat_maxabs`,
`eta_abs_1 = 1 / Psi_hat_maxabs`.

No threshold amplitude is a D2C6G PASS/FAIL gate.

The conservative feedback calibration is frozen **before output** as

`ETA_FEEDBACK_CAP = min_all_members,checkpoints(eta_1pct)`.

If D2C6G passes, the first separately preregistered self-consistent feedback run is licensed only on the dyadic ladder

`{ETA_FEEDBACK_CAP/4, ETA_FEEDBACK_CAP/2, ETA_FEEDBACK_CAP}`.

This rule is fixed now and may not be changed after inspecting D2C6G output.

## Frozen control members

Use the same three R2 sentinels for the direct-512 control:

1. `sigma=+1 | kind=simple | beta0=0.1`;
2. `sigma=0 | kind=exponential | beta0=0.5`;
3. `sigma=-1 | kind=sharp | beta0=1`.

No new completion is selected from D2C6G output.

## Gates

### G1 — provenance and exact coverage

Require the D2C6F-R2 preregistration, R2 implementation/result record and this D2C6G preregistration to be ancestors. Require exact all-27 primary coverage, physical trajectory `eta=0`, direct-256 primary and direct-512 control.

### G2 — eta=0 trajectory/source identity

The physical direct memory stress at exact eta=0 must be identically zero by the explicit action prefactor. The eta=0 canonical trajectory must remain the certified memory-off nonlinear trajectory; no direct metric source may be fed back in D2C6G.

### G3 — all-27 health

All 27 eta=0 trajectories and passive baths must remain finite; retained scalar-current constraint `<=1e-10`; `min(1+j_eff)>0`; completed-square unit-source energy finite and non-negative up to `-1e-14`.

### G4 — direct bath convergence of the metric tangent

For the three frozen sentinels compare direct-256 versus direct-512 unit source and one-way metric-tangent signatures over the frozen low Fourier band. Maximum relative L2 difference must be `<=1e-2`.

### G5 — baseline metric calibration well-defined

All frozen CLASS `psi_base` checkpoint fields must be finite and have strictly positive RMS. All derived eta calibration scales must be finite and positive.

### G6 — scope integrity

No gate depends on the magnitude or sign of the calibrated eta scale, source amplitude, completion ranking, lensing direction, or observational likelihood.

The R2 time/space convergence and R7 eta=0 trajectory convergence are inherited; D2C6G does not repeat those expensive controls because no evolution equation, resolution or local stress operator is changed.

## Classification

PASS:

`NL1C6D2C6G_ETA0_DIRECT_METRIC_TANGENT_CALIBRATION_PASS`

FAIL:

`NL1C6D2C6G_ETA0_DIRECT_METRIC_TANGENT_CALIBRATION_FAIL`

INCOMPLETE is reserved for execution failure before gates can be evaluated.

A PASS licenses only a separately preregistered self-consistent weak-field feedback run on the frozen derived ladder `{cap/4,cap/2,cap}`. It does not license an observational likelihood.
