# AeST Memory Gravity

[![v018 CLASS compile and zero regression](https://github.com/dvlahek/aest-memory-gravity/actions/workflows/v018-class-compile.yml/badge.svg)](https://github.com/dvlahek/aest-memory-gravity/actions/workflows/v018-class-compile.yml)
[![v019n strict structural null](https://github.com/dvlahek/aest-memory-gravity/actions/workflows/v019n-structural-null.yml/badge.svg)](https://github.com/dvlahek/aest-memory-gravity/actions/workflows/v019n-structural-null.yml)
[![v019k complex bath audit](https://github.com/dvlahek/aest-memory-gravity/actions/workflows/v019k-complex-bath-audit.yml/badge.svg)](https://github.com/dvlahek/aest-memory-gravity/actions/workflows/v019k-complex-bath-audit.yml)

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

The continuum Drude identity and the finite oscillator equations are correct, but the real-axis optimized N=16/N=20 bath is underresolved for oscillatory complex-frequency cosmology.

For the existing N=20 design on the tested retarded complex-frequency grid:

- median relative kernel error: `3.80e-4`;
- p95 error: `2.00e-2`;
- p99 error: `6.46e-2`;
- worst case: `1.54e-1`.

The exact positive continuum spectral identity is reproduced at `2.22e-16` relative precision, and the driven time-domain oscillator system agrees with its own finite transfer function at about `1.02e-4` in the harmonic-fit audit.

Direct positive log-quadrature converges much more slowly on the complex domain than on the real axis: N=96 is the first tested order with p95 below `0.5%`, while even N=128 still has a worst-case error of about `3.1%`.

## Next gate

Do **not** run another finite-eta CMB/Planck sweep with the current N=16/N=20 bath.

Replace the numerical memory realization by either:

1. a substantially higher-order positive continuum quadrature with demonstrated complex-domain accuracy, or
2. preferably a passive rational/diffusive approximation designed directly for the retarded complex-frequency response.

Then repeat small-eta CLASS response using a tangent/linear-response formulation before any likelihood analysis.

The field-theory results, conservative continuum Drude construction, eta=0 AeST baseline, and the central smooth-source drag law `a_drag ∝ -(v tau)^(1/3)` are unaffected by the v0.19k numerical finding.
