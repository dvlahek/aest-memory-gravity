# AeST Memory Gravity

[![v018 CLASS compile and zero regression](https://github.com/dvlahek/aest-memory-gravity/actions/workflows/v018-class-compile.yml/badge.svg)](https://github.com/dvlahek/aest-memory-gravity/actions/workflows/v018-class-compile.yml)
[![v019n strict structural null](https://github.com/dvlahek/aest-memory-gravity/actions/workflows/v019n-structural-null.yml/badge.svg)](https://github.com/dvlahek/aest-memory-gravity/actions/workflows/v019n-structural-null.yml)
[![v019k complex bath audit](https://github.com/dvlahek/aest-memory-gravity/actions/workflows/v019k-complex-bath-audit.yml/badge.svg)](https://github.com/dvlahek/aest-memory-gravity/actions/workflows/v019k-complex-bath-audit.yml)
[![v019l passive rational](https://github.com/dvlahek/aest-memory-gravity/actions/workflows/v019l-passive-rational.yml/badge.svg)](https://github.com/dvlahek/aest-memory-gravity/actions/workflows/v019l-passive-rational.yml)
[![v019m time dependent H](https://github.com/dvlahek/aest-memory-gravity/actions/workflows/v019m-time-dependent-H.yml/badge.svg)](https://github.com/dvlahek/aest-memory-gravity/actions/workflows/v019m-time-dependent-H.yml)

Research code and validation harness for an AeST-based history-dependent gravitational memory model.

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

## Next gate

Do **not** insert the H-dependent v0.19l rational table into CLASS.

The next gate is to optimize and compress the fixed-frequency positive oscillator representation directly on the full time-dependent FLRW/CMB domain, extend the frequency/Hubble coverage to the actual CLASS history, and require convergence against the dense conservative bath. Only after that gate passes should finite-eta tangent CMB response be rerun.

The continuum field-theory construction, eta=0 CLASS baseline, leading AeST adiabatic mode, and central smooth-source drag law `a_drag ∝ -(v tau)^(1/3)` are unaffected by the v0.19m numerical finding.


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
