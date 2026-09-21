# AeST Memory Gravity

[![v018 CLASS compile and zero regression](https://github.com/dvlahek/aest-memory-gravity/actions/workflows/v018-class-compile.yml/badge.svg)](https://github.com/dvlahek/aest-memory-gravity/actions/workflows/v018-class-compile.yml)
[![v019n strict structural null](https://github.com/dvlahek/aest-memory-gravity/actions/workflows/v019n-structural-null.yml/badge.svg)](https://github.com/dvlahek/aest-memory-gravity/actions/workflows/v019n-structural-null.yml)
[![v019k complex bath audit](https://github.com/dvlahek/aest-memory-gravity/actions/workflows/v019k-complex-bath-audit.yml/badge.svg)](https://github.com/dvlahek/aest-memory-gravity/actions/workflows/v019k-complex-bath-audit.yml)
[![v019l passive rational](https://github.com/dvlahek/aest-memory-gravity/actions/workflows/v019l-passive-rational.yml/badge.svg)](https://github.com/dvlahek/aest-memory-gravity/actions/workflows/v019l-passive-rational.yml)
[![v019m time dependent H](https://github.com/dvlahek/aest-memory-gravity/actions/workflows/v019m-time-dependent-H.yml/badge.svg)](https://github.com/dvlahek/aest-memory-gravity/actions/workflows/v019m-time-dependent-H.yml)

Research code and validation harness for an AeST-based history-dependent gravitational memory model.

## Active GE19 checkpoint — 2026-09-21

The active weakly nonlinear gravitational-elasticity track is GE19.

**Certified parent:** Repair13

`GE19_REPAIR13_SELF_CONSISTENT_REDUCED_BACKGROUND_H1_RECLOSURE_PASS`.

The reduced Einstein+AeST+dust+Lambda H1 system is closed on its own on-shell background

`H_red^2=(Q K_Q-K)/3+C/a^3+rho_lambda`.

**First H3/Z20 attempt:** Repair14

`GE19_REPAIR14_SELF_CONSISTENT_REDUCED_H3_Z20_PARTICULAR_FAIL`.

The source is spatially converged and the candidate state is time-grid converged, but the second-order shift constraint remains O(1), so Z20 is not certified.

**Diagnostics:** Repairs 15 and 16 are frozen diagnostic results. They exclude both the zero-dynamic-velocity and canonical-zero finite-window initial boundaries as sufficient fixes.

**Repair17 diagnostic:** **PASS-FOR-EXISTENCE**.

`GE19_REPAIR17_FULL_CANONICAL_INITIAL_MANIFOLD_AUDIT_COMPLETE`

Route:

`FINITE_WINDOW_ZERO_BOUNDARY_INADMISSIBLE_SOURCE_COMPATIBLE`.

The full canonical 2x8 initial constraint manifold exists in all `714/714` material cases. The maximum full-y constraint residual is `8.892e-13`, lapse backward error `2.646e-16`, shift backward error `1.870e-10`, and eliminated algebraic residual `2.388e-16`.

This means the frozen quadratic source is compatible; the previous finite-window zero boundaries were inadmissible.

**Repair18 boundary:** **PASS / CERTIFIED** in `714/714` material cases. **Repair19 propagation:** frozen **FAIL** only on shift. **Repair20 diagnostic:** near-null normalization is confirmed, but the active shift remains above the original `1e-6` gate at Nt128 (`9.589e-6`), so ordinary H3 time truncation is not established as the explanation. **Current next gate:** Repair21 is **LOCKED / READY / NOT YET EXECUTED**. It re-solves the certified H1 system on-shell at Nt64 and Nt128, rebuilds the unchanged H3 source, and evaluates matched-grid shift convergence for fixed C,beta,m.

Until that is frozen:

- run only the locked Repair21 on-shell-H1 matched-shift diagnostic;
- do not relabel Repair19 or Repair20;
- do not construct q20 or start H4/Z21;
- do not make nonlinear real-data claims.

Persistent GE19 chronology and frozen provenance:

`docs/ge19_history.md`.


## Current status

**v0.18 — CLASS source integration and zero-regression: PASS.**

The workflow pins official CLASS v3.3.4 at commit `e85808324f51fc694d12e3ed7439552a3c3f9540`. Standard CLASS outputs remain byte-identical when the extension is inactive.

**v0.19 / v0.19p / v0.19n — eta=0 AeST CLASS bridge and numerical controls: PASS/diagnostic PASS.**

Cosh/Exp AeST backgrounds and scalar states compile and run in CLASS. Precision and strict frozen-extra-state controls exclude ordinary perturbation tolerance and ODE-vector dimension as explanations of the persistent eta=0 AeST–CDM residual.

**v0.19i — leading radiation-era adiabatic initial condition: PASS in a controlled start window.**

The leading regular superhorizon mode is

\[
\delta_A=(1+w_A)\delta_c,\qquad \Theta_A=\Theta_c,
\]

\[
\alpha_A=-a\Theta_A/k^2,\qquad E_A=0.
\]

Thus `chi_i=0, E_i=0` is the leading adiabatic condition rather than an arbitrary proxy. Full higher-order Frobenius terms are not claimed to vanish identically.

**v0.19j — first finite-eta CLASS memory run: implementation PASS, physical response not converged.**

The positive finite Drude bath compiles and preserves eta=0/background controls, but the N=16/N=20 CMB response failed eta-linearity and bath-order convergence. No finite-eta CMB interpretation is made from v0.19j.

**v0.19k — complex-frequency/time-domain bath audit: PASS_DIAGNOSTIC.**

The continuum Drude identity and finite oscillator equations are correct, but the real-axis optimized N=16/N=20 bath is underresolved for oscillatory complex-frequency cosmology.

**v0.19l — passive complex-domain rational design: PASS_LOCAL_PASSIVE_RATIONAL.**

For locally constant `H`, the Hubble-dressed kernel has an exact positive Debye/Stieltjes representation. A non-negative N=24 rational table on 97 logarithmic `H tau` anchors over `1 <= H tau <= 1000` reaches sub-`1e-3` complex-frequency error, including interpolation between anchors. All fitted weights are non-negative and all poles lie on the negative real axis.

**v0.19m — time-dependent-H audit: TIME_DEPENDENT_RATIONAL_NOT_VALIDATED.**

The dense conservative reference is numerically converged: the worst N=512 versus N=1024 waveform difference in the audit is `6.14e-5` in normalized L2.

However, replacing the frozen-H rational coefficients by instantaneous `H(t)` coefficients does **not** reproduce the original conservative bath. Across `omega/H >= 1` histories the instantaneous N=24 realization gives:

- median normalized L2 error: `2.43e-2`;
- p95: `9.47e-2`;
- worst case: `1.19e-1`.

Including slower/impulsive drives, the largest tested error reaches `1.59e-1`. Thus the excellent frozen-H fit does not survive naive non-autonomous substitution. The missing physics is history/state transport associated with changing `H`, not frozen-frequency fitting accuracy.

The current v0.19l table also does not span a full CMB history for any of the tested `tau H0` values. For `tau H0=1`, recombination occurs at approximately `H tau = 2.32e4` and equality at `1.57e5`, both above the table maximum of 1000.

A fallback reduction that keeps the **original fixed-frequency positive oscillator structure** is promising. A 64-node candidate fit has 31 active positive modes and, on independent time-dependent validation histories, gives:

- median normalized L2 error: `3.36e-4`;
- p95: `2.57e-3`;
- worst case: `3.21e-3`.

Because fixed oscillator frequencies preserve the original covariant time-dependent form, this is now the preferred numerical direction.

## Legacy v0.19 finite-eta CLASS gate

Do **not** insert the H-dependent v0.19l rational table into CLASS.

The next gate is to optimize and compress the fixed-frequency positive oscillator representation directly on the full time-dependent FLRW/CMB domain, extend the frequency/Hubble coverage to the actual CLASS history, and require convergence against the dense conservative bath. Only after that gate passes should finite-eta tangent CMB response be rerun.

The continuum field-theory construction, eta=0 CLASS baseline, leading AeST adiabatic mode, and central smooth-source drag law `a_drag ∝ -(v tau)^(1/3)` are unaffected by the v0.19m numerical finding.


## Physics-first gravitational elasticity

The active interpretation is now the already certified **NL0B covariant memory completion viewed as gravitational viscoelasticity**.

The canonical frozen action is the NL0B completed-square auxiliary-vector sector,

`S_mem ~ integral sqrt(-g) sum_j [ |D_A U_j|^2 - |omega_j U_j-sqrt(eta w_j) X|^2 ]`,

with

`X_mu=h_mu^nu nabla_nu phi`.

Define the elastic mismatch

`e_j=sqrt(eta w_j)X-omega_j U_j`.

Gravity changes `X`; the internal modes cannot follow instantaneously; the mismatch stores positive elastic energy and returns the already certified AeST memory force.

The positive Drude continuum has

`K(A)=A/(1+A)`.

For `H=0`, `A=tau s`, so

`B/X=tau s/(1+tau s)`

or equivalently

`tau dB/dt + B = tau dX/dt`.

Thus the frozen memory theory is a **Maxwell-type gravitational viscoelastic medium**.

Physical division of labor:

- AeST Y-sector: static / gradient-dependent modified-gravity response;
- NL0B elastic-memory sector: history / rate-dependent response.

The active theory chain is already substantially closed:

- NL0B covariant memory completion: PASS;
- NL0C weakly nonlinear Y-sector: PASS;
- NL1A pseudospectral operator bridge: PASS;
- NL1B2 directional second-order eta tangent: PASS;
- NL1C5 spherical variational bridge: PASS;
- NL1C6 spherical self-gravity closure: PASS.

The B4-B8 sequence is retained as a failed/blocked cosmological nonlinear initial-data construction. It is no longer the active definition of the theory and no further B4-B8 solver tuning is planned.

Canonical interpretation:

- `docs/gravitational_elasticity_canonical_nl0b_interpretation.md`;
- `docs/gravitational_maxwell_viscoelasticity.md`.

The earlier shear-strain completion draft is retained only as an exploratory alternative and is not part of the active theory.

Immediate physics target:

- Repair13: **PASS** — self-consistent reduced background and H1/Z10 closure;
- Repair14: frozen **FAIL** — first H3/Z20 particular state is not shift-constraint certified;
- Repair15/16: frozen diagnostics excluding the two naive finite-window zero-boundary conventions;
- Repair17: **PASS-FOR-EXISTENCE** — full canonical initial constraint manifold exists in 714/714 material cases;
- Repair18: **PASS** — unique reproducible zero-coordinate projected-momentum finite-window boundary certified in 714/714 material cases;
- Repair19: frozen **FAIL** — projected-boundary H3 march passes every frozen control except shift; near-null normalization dominates the O(1) maximum;
- Repair20: **COMPLETE / ACTIVE ISSUE REMAINS** — near-null O(1) monitor pathology confirmed, but active Nt128 shift remains `9.589e-6`;
- Repair21: **READY / NOT YET EXECUTED** — on-shell H1 Nt64/Nt128 parent plus matched-grid shift diagnostic;
- only after a separately certified Z20: q20 and H4/Z21 nonlinear memory correction;
- finite physical eta, lensing/data confrontation and collapse remain later stages.

GE02 first locked run:

- classification: `GE02_NONLINEAR_ELASTIC_SOURCE_TAU_CROSSOVER_PASS`;
- workflow: `35470926045`;
- artifact: `10592418646`;
- artifact SHA-256: `61c72e6cd66fc27427f15fbe7d0c9e1410096b82b99ebcd8368194f8348bc100`;
- result freeze: `docs/ge02_nonlinear_elastic_source_tau_crossover_result_freeze.md`.

Across `tau H0={0.1,0.3,0.5,0.7,1,3,10}`, both the action-derived restoring source `B_rms` and the quadratic finite-amplitude metric-energy source `rhohat_mem` increase smoothly from the relaxed regime toward the unrelaxed elastic plateau.

At `tau H0=1`, the nonlinear source norms have already reached approximately 0.88 and 0.865 of their `tau H0=10` values; at `tau H0=3` they are approximately 0.966 and 0.962.

This is a nonlinear source/stress result. It is not yet a self-consistent finite-eta nonlinear trajectory.

`identify the dynamical regimes where tau/t_dyn ~ 1 and test the resulting elastic-memory response with the already validated linear and spherical action infrastructure`.


### Weakly nonlinear Y-memory source status

GE03 remains frozen as

`GE03_WEAKLY_NONLINEAR_Y_MEMORY_CROSS_SOURCE_FAIL`

because its preregistered N256/N512 low-mode convergence gate failed at `1.16654e-3 > 5e-4`, despite all operator-identity, lambda-affinity, finite-difference and beta-scaling gates passing.

GE04 independently characterizes the same frozen source and passes:

`GE04_DY2_SPECTRAL_CONVERGENCE_PASS`.

The high-resolution ladder gives approximately third-order convergence, with

- N512/N1024: `~1.266e-4`;
- N1024/N2048: `~1.75e-5`;
- N2048/N4096: `~1.75e-6`.

Therefore later weakly nonlinear state work must use N1024 primary and N2048 control for the nonanalytic Y-memory cross-source. GE03 is not relabelled.

The descriptive high-resolution source geometry is nearly antiparallel to the baseline Y source throughout the frozen native window, with `||2DY2||/||2Y2||` increasing from about 0.015 to 0.097 per unit eta tangent.

### Physics-first checkpoint

The gravitational-elasticity programme now has controlled results at several levels.

**GE01 — PASS.** The trusted native total-matter eta=0 tangent increases smoothly with the Maxwell timescale. Relative response norms for `tau H0={0.1,0.3,0.5,0.7,1,3,10}` are approximately

`{0.580,0.809,0.878,0.912,0.939,0.983,1.000}`

relative to the historical `tau H0=10` case.

**GE02 — PASS.** The finite-amplitude action-derived restoring source and quadratic direct metric-energy source show the same relaxed-to-elastic transition. At `tau H0=1` they are already approximately 0.88 and 0.865 of their `tau H0=10` norms.

**GE03 — frozen FAIL.** The exact weakly nonlinear `DY2[chi10;chi11]` identity, finite-difference check, lambda affinity and beta scaling all pass, but the preregistered N256/N512 low-mode convergence gate fails.

**GE04 — PASS.** A separately preregistered resolution ladder shows approximately third-order convergence:
`256/512 ~1.17e-3`,
`512/1024 ~1.27e-4`,
`1024/2048 ~1.75e-5`,
`2048/4096 ~1.75e-6`.
Later weakly nonlinear state work therefore uses N1024 primary and N2048 control. GE03 is not relabelled.

**GE05 — PASS.** The longitudinal 3+1 NL0B action now has explicit first- and second-directional source generators `M1` and `M2` for scalar, bath, aether and all metric blocks. Direct metric memory stress is exactly absent at first order and nonzero at second order, as required by the covariant action.

The memory-off analytic quadratic source has now been generated and the first baseline second-order state/source `Z20` was attempted in Repair14.

That Repair14 candidate is **not certified** because the second-order shift constraint fails despite excellent source, anisotropy and time-grid controls.

The active blocker is therefore no longer source generation, manifold existence or boundary selection. Repair20 confirms the near-null part of the shift problem but leaves an active residual. Repair21 now tests the specific possibility that Repair20's separately interpolated H1 state/derivative parent is off-shell between Nt64 nodes.

Do not start a `Z21` solver until a separately frozen H3 run certifies `Z20`.

## NL1C7B eta=0 spherical nonlinear-constraint track

Latest completed construction result:

`NL1C7B7_REDUCED_RADIAL_CONSTRUCTION_FAIL`.

NL1C7B6 established that the exact eta=0 Hamiltonian and radial-momentum constraints reduce to a coupled first-order radial system for the same frozen physical pair `(L,R_t)`.

NL1C7B7 then attempted to solve that system by treating `L(0)` as a scalar shooting parameter and imposing `L(r_max)=a_i`.

The B7 implementation itself is structurally healthy:

- frozen provenance passes;
- all six parent H/M values reproduce exactly;
- the local degree-8 / nine-node frozen-field representation passes;
- the exact reduced RHS audit passes.

However, every primary and control shooting attempt fails because `ell(r_max)` has the same negative sign at both frozen bracket endpoints `ell_0=-0.5,+0.5`.

No candidate state is returned to the original B4 differential science gate.

Post-result center analysis identifies the reason the shooting parameter is nearly ineffective. At a regular spherical center, the exact Hamiltonian has leading form

`H(0)=2L_0-2R_r(0)^2/L_0`.

Thus exact regularity and positive L require

`L(0)=R_r(0)`.

So `L(0)` is not a free shooting parameter.

Together with

`R_t(0)=0`

and

`R_{t,r}(0)=L_t(0)R_r(0)/L(0)=L_t(0)`,

the regular center fixes the reduced first-order IVP with no free shooting parameter.

B7 remains frozen as a construction FAIL. Its bracket must not be expanded and its root/integrator settings must not be tuned post hoc.

The preferred next step is a separately preregistered zero-free-parameter regular-center IVP that integrates the exact B6 radial system outward and treats both outer `L` and outer `R_t` background compatibility as predictions.

Any returned state must still pass the unchanged original B4 differential certification

`max epsilon_H,max epsilon_M <=1e-7`

on both Nr=256 and Nr=512 before eta=0 short-time evolution is licensed.

Full chronology and frozen provenance are maintained in:

`docs/nl1c7b4_history.md`.
