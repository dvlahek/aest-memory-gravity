# AeST Memory Gravity

[![v018 CLASS compile and zero regression](https://github.com/dvlahek/aest-memory-gravity/actions/workflows/v018-class-compile.yml/badge.svg)](https://github.com/dvlahek/aest-memory-gravity/actions/workflows/v018-class-compile.yml)
[![v019n strict structural null](https://github.com/dvlahek/aest-memory-gravity/actions/workflows/v019n-structural-null.yml/badge.svg)](https://github.com/dvlahek/aest-memory-gravity/actions/workflows/v019n-structural-null.yml)
[![v019k complex bath audit](https://github.com/dvlahek/aest-memory-gravity/actions/workflows/v019k-complex-bath-audit.yml/badge.svg)](https://github.com/dvlahek/aest-memory-gravity/actions/workflows/v019k-complex-bath-audit.yml)
[![v019l passive rational](https://github.com/dvlahek/aest-memory-gravity/actions/workflows/v019l-passive-rational.yml/badge.svg)](https://github.com/dvlahek/aest-memory-gravity/actions/workflows/v019l-passive-rational.yml)

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
\alpha_A=-a\Theta_A/k^2,\qquad E_A=0,
\]

so `chi_i=0, E_i=0` is the leading adiabatic condition rather than an arbitrary proxy. Full higher-order Frobenius terms are not claimed to vanish identically.

**v0.19j — first finite-eta CLASS memory run: implementation PASS, physical response not converged.**

The positive finite Drude bath compiles and preserves eta=0/background controls, but the N=16/N=20 CMB response failed eta-linearity and bath-order convergence. No finite-eta CMB interpretation is made from v0.19j.

**v0.19k — complex-frequency/time-domain bath audit: PASS_DIAGNOSTIC.**

The continuum Drude identity and the finite oscillator equations are correct, but the real-axis optimized N=16/N=20 bath is underresolved for oscillatory complex-frequency cosmology. For the existing N=20 design, the tested complex-frequency grid has p95 error about `2.00e-2` and worst-case error about `1.54e-1`.

**v0.19l — passive complex-domain rational design: PASS_LOCAL_PASSIVE_RATIONAL.**

For locally constant `H`, the Hubble-dressed kernel has the exact positive Debye/Stieltjes representation

\[
K_h(z)=c_*\frac{z}{z+r_*}+\int_0^{3h}\mu_h(r)\frac{z}{z+r}\,dr,
\]

with positive measure

\[
\mu_h(r)=\frac{\sqrt{r(3h-r)}}{\pi r\,[1+r(3h-r)]}.
\]

The identity is reproduced numerically to `8.17e-13` relative precision on the audit grid.

A non-negative N=24 rational table on 97 logarithmic `H tau` anchors over `1 <= H tau <= 1000` gives, on the fitted anchor grid:

- median relative error: `2.06e-6`;
- p95: `1.76e-4`;
- p99: `4.98e-4`;
- worst case: `9.22e-4`.

Linear interpolation of the non-negative weights in `log(H tau)` remains passive and, at all midpoint tests between anchors, gives:

- median: `1.57e-5`;
- p95: `3.12e-4`;
- p99: `5.32e-4`;
- worst case: `8.60e-4`.

All fitted/interpolated weights are non-negative, all poles lie strictly on the negative real axis, and the sampled response remains positive-real.

## Next gate

v0.19l is an accurate **local constant-H** representation. Its rates and weights vary with `H(t)`, so it is not yet proven equivalent to the original covariant conservative bath when the Hubble rate changes on the memory timescale.

The next gate is therefore a non-autonomous/time-dependent-H comparison between the 24-mode first-order realization and a high-order conservative oscillator bath through a radiation-to-matter FLRW history. Only after that comparison passes should the rational realization replace the current CLASS bath and be used for a finite-eta tangent CMB response.

The field-theory results, conservative continuum Drude construction, eta=0 AeST baseline, and the central smooth-source drag law `a_drag ∝ -(v tau)^(1/3)` remain unaffected.
