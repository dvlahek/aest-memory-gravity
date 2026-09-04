# v0.19s — stable source-weighted positive bath compression

v0.19r closed the numerical reference problem for the conservative Drude continuum on actual eta=0 AeST CLASS trajectories. A direct positive Gauss–Legendre quadrature after

\[
\omega=\tan\theta,\qquad \frac{2}{\pi}\frac{d\omega}{1+\omega^2}=\frac{2}{\pi}d\theta
\]

converges against an N=16384 continuum reference, with N=2048 already passing the held-out source-history gate.

The direct N=2048 bath is too large for a practical full Boltzmann run because it would add 4096 oscillator state variables per scalar k mode. v0.19s therefore revisits the source-weighted compression idea from v0.19q, but now against the stable v0.19r continuum target rather than the rejected logarithmic reference.

## Construction

The eta=0 Cosh and Exp CLASS trajectories are traced at

```text
1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 1e-1, 3e-1 Mpc^-1
```

and tested for

```text
tau H0 = 1, 0.1, 0.01, 0.001.
```

For every history the target response is the direct N=16384 tan-theta Drude continuum. A broad fixed-frequency dictionary is then compressed with non-negative least squares and greedy positive mode selection. The oscillator frequencies are global constants and all weights are constrained positive.

No H-dependent rational coefficients are introduced.

## Held-out validation

Alternating k values are withheld from the fit. The primary gate requires

\[
\text{median L2}<5\times10^{-4},\qquad
p_{95}<10^{-3},\qquad
\max L2<3\times10^{-3},
\]

with at most 96 active positive modes, positive fixed frequencies, and normalized total weight.

If the gate passes, the resulting compressed bath is small enough to return to CLASS for the first controlled small-eta response campaign.

## Scope

A v0.19s PASS validates only the reduced memory representation on the eta=0 AeST source manifold. It does not by itself establish a physical finite-eta CMB prediction or a Planck constraint.
