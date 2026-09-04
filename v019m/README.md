# v0.19m — time-dependent-H memory audit

v0.19l proved that for every *frozen* value of

\[
h=H\tau
\]

the Hubble-dressed Drude kernel admits a positive Debye/Stieltjes representation and that a 24-mode positive rational fit reaches sub-`1e-3` complex-frequency error on the tested `1 <= H tau <= 1000` domain.

That does **not** by itself prove that replacing `H` by `H(t)` inside those fitted rates and weights reproduces the original covariant conservative oscillator bath.

v0.19m tests exactly that point.

## Reference system

The reference is the original positive Drude oscillator continuum, discretized only for numerical quadrature:

\[
\ddot y_\omega+3H(t)\dot y_\omega+\omega^2 y_\omega=c_\omega X(t),
\]

with

\[
\frac{c_\omega^2}{\omega^2}\,d\omega
=\frac{2}{\pi}\frac{d\omega}{1+\omega^2}
\]

in units `tau=1`, `g=1`.  Its output is

\[
B_{\rm ref}(t)=\int d\omega\,\frac{c_\omega^2}{\omega^2}
\left[X(t)-Q_\omega(t)\right],
\]

where `Q_omega` is the oscillator coordinate normalized to unit static response.

The dense reference uses positive log-frequency quadrature and an exact piecewise-constant damped-oscillator update, so high-frequency modes do not impose an explicit CFL step.

## v0.19l non-autonomous realization under test

For the v0.19l positive rational table,

\[
K_h(z)\simeq\sum_j w_j(h)\frac{z}{z+r_j(h)},
\qquad r_j(h)=h q_j,
\]

v0.19m evolves

\[
\dot m_j=-r_j[H(t)]\,[m_j-X]
\]

and evaluates

\[
B_{\rm rat}(t)=\sum_j w_j[H(t)]\,[X-m_j].
\]

This is the natural instantaneous-coefficient first-order realization.  The audit asks whether it is also a faithful approximation to the original time-dependent conservative bath.

## Histories and drives

The comparison includes:

- a flat radiation+matter+Lambda `H(a)` history restricted to the validated `1 <= H tau <= 1000` table interval;
- pure radiation-like `H proportional to a^-2`;
- pure matter-like `H proportional to a^-3/2`;
- smooth drives with approximately constant `omega_drive/H` across each history.

The main metric is the normalized time-domain L2 difference, supplemented by waveform cosine and peak-normalized error.

## Coverage audit

The campaign separately checks whether the v0.19l table range is wide enough for a full CMB run.  For `tau H0 = 1`, recombination and equality occur at `H tau` far above 1000.  This is treated as a coverage issue independent of the non-autonomous accuracy test.

## Positive fixed-oscillator rescue candidate

If the instantaneous rational realization fails, v0.19m also fits a smaller **fixed-frequency positive oscillator bath directly in the time domain**.  Unlike the H-dependent rational basis, fixed oscillator frequencies preserve the original covariant time-dependent structure exactly; only the positive spectral quadrature is reduced.

This candidate is diagnostic only.  It is not inserted into CLASS in v0.19m.

## Gates

- `M1`: CMB `H tau` coverage of the v0.19l table.
- `M2`: dense-reference convergence.
- `M3`: instantaneous N=24 rational vs conservative bath for time-dependent H.
- `M4`: positive fixed-oscillator reduced candidate.
- `M5`: implementation recommendation.

No finite-eta CMB or likelihood claim is made in v0.19m.
