# v0.19k — complex-frequency and time-domain bath audit

v0.19j established that the finite-memory CLASS path compiles, preserves the eta=0/background controls, and produces a finite response. It did **not** pass eta-linearity or N=16/N=20 response convergence.

v0.19k tests the most direct suspected cause before any new CMB sweep: the v0.17 bath weights were fitted on the positive real axis, while acoustic/CMB perturbations probe an oscillatory, complex-frequency response.

For locally constant H define

\[
z=s\tau,\qquad h=H\tau,\qquad
A=\sqrt{z(z+3h)},\qquad \Re A\ge0.
\]

The exact Hubble-dressed Drude kernel is

\[
K(A)=\frac{A}{1+A}.
\]

A positive finite oscillator bath gives

\[
K_N(A)=\sum_j w_j\frac{A^2}{r_j^2+A^2}.
\]

The same formula follows directly from the CLASS time-domain oscillator equations

\[
\ddot q_j+3H\dot q_j+\omega_j^2q_j
=\omega_j\sqrt{w_j}\,\chi
\]

in local physical units.

## Tests

1. `01_complex_kernel_audit.py` evaluates the existing N=16 and N=20 designs on a complex-frequency grid relevant to `tau H0 = 1`, with `H tau >= 1` and a wide range of `omega/H`.
2. `02_spectral_identity.py` verifies numerically that the positive continuum representation

   \[
   \frac{A}{1+A}=\frac{2}{\pi}\int_0^\infty
   \frac{A^2}{(r^2+A^2)(1+r^2)}dr
   \]

   remains correct for complex A on the retarded branch.
3. `03_time_domain_drive.py` drives the finite bath sinusoidally, measures the steady complex response, and compares it with the algebraic finite-bath transfer function. This audits the factors of `H`, `omega_j`, and the shifted-square response independently of CLASS.
4. `04_positive_quadrature_scan.py` compares the present fitted designs with direct positive log-quadratures at N=20,32,48,64,96. This determines whether simply increasing bath order is enough or whether a different rational realization is needed.
5. `05_make_report.py` classifies the result.

## Interpretation rule

A failure of the existing N=16/N=20 design on the complex grid is **not** a failure of the Drude-bath theory. It means only that a real-axis optimized finite representation is not yet a controlled numerical realization for oscillatory cosmological perturbations.

No new finite-eta CLASS/Planck claim is made in v0.19k.
