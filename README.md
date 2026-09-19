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

Latest completed structural result:

`NL1C7B6_SYMBOLIC_RADIAL_REDUCTION_PASS`.

The previous pointwise differential Gauss-Newton route and the B5 conservative cell-integrated constructor both failed to produce a state satisfying the unchanged exact B4 differential constraint threshold `1e-7`.

NL1C7B6 therefore changed the numerical representation rather than tuning those solvers.

Using the same frozen eta=0 physics and the same physical pair `(L,R_t)`, the exact Hamiltonian and radial-momentum constraints were reconstructed from the frozen action-derived source dictionary and reduced symbolically.

After exact-Q substitution:

- H is affine in `L_r`;
- H is quadratic in algebraic `R_t`;
- H contains no `R_{t,r}`;
- M is affine in `R_{t,r}`;
- the GR algebraic `R_t` terms cancel exactly in M;
- all non-GR momentum sectors are independent of algebraic `R_t`;
- no second derivative of either solved field is present.

The solved derivative coefficients are

`A_H=[4 R R_r + 2 K_B R^2 cosh(u)sinh(u)(L_t+u_r) + 2 C R^2 phi_r]/L^2`

and

`A_M=-4LR`.

Hence, away from the analytic center,

`L_r=-B_H/A_H`

and

`R_{t,r}=B_M/(4LR)`.

All six frozen scale/grid cases pass the nondegeneracy audit on every noncenter point. The coefficients are positive and show no interior zero or sign change.

Near the regular center,

- `A_H/r ≈ 4`;
- `(4LR)/r ≈ 1.6000e-3`;

so the only coefficient degeneracy is the expected spherical `O(r)` behavior at `r=0`.

The preferred next step is therefore no longer residual minimization. It is a separately preregistered numerical construction of this exact coupled first-order radial system.

The historical Repair18d1 `Y4/Qmean` conditions remain projection-nullspace transversality functionals and are not treated as physical radial boundary conditions.

A future reduced-radial construction must specify the regular-center and asymptotic-background boundary policy before execution and must still pass the original B4 differential certification

`max epsilon_H,max epsilon_M <=1e-7`

on both Nr=256 and Nr=512 before eta=0 short-time evolution is licensed.

Full chronology and frozen provenance are maintained in:

`docs/nl1c7b4_history.md`.
