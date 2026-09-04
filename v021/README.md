# v0.21 — Exp memory-timescale revolution sweep

v0.20 established a distinct unlensed TT/EE/TE memory tangent at `tau H0 = 1`, but with very low cosmic-variance significance per unit eta. v0.21 tests whether that conclusion is specific to the memory timescale.

The sweep does **not** rescale the tau=1 sparse compressed bath. Earlier diagnostics showed that one sparse source-weighted bath is not uniformly accurate over the full tau family, especially at small tau.

Instead, v0.21 returns to the original positive Drude continuum

\[
d\mu(\omega)=\frac{2}{\pi}\frac{d\omega}{1+\omega^2},
\qquad \omega\tau=\tan\theta,
\]

and inserts direct positive Gauss–Legendre quadratures into CLASS. N=512 is the primary bath and N=256 is a convergence control. The existing CLASS equations scale each physical oscillator frequency as

\[
\omega_j = r_j H_0/(\tau H_0),
\]

so the quadrature nodes and positive weights are structural and the timescale dependence enters only through the physical frequency scale.

The tested grid is

```text
0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1, 3, 10
```

For every tau point the workflow:

1. traces the eta=0 first-order forcing with N=256 and N=512 positive baths;
2. compares the two force tables;
3. propagates the N=512 forcing through the eta=0 variational CLASS system at lambda=300 and 1000;
4. recomputes the six core LambdaCDM nuisance directions using central half-step derivatives;
5. projects the memory tangent with the full-sky TT/EE/TE cosmic-variance metric over 30 <= ell <= 2500;
6. reports the retained orthogonal fraction, raw and marginalized S/N per unit eta, eta required for CV S/N=1, and multipole-band contributions.

Primary per-point numerical gates are:

- N256 vs N512 force-table relative L2 < 5% and cosine > 0.999;
- lambda300 vs lambda1000 tangent relative CV norm < 5% and cosine > 0.999;
- six-dimensional nuisance basis retained.

The aggregate gate also cross-checks the tau=1 direct-bath result against v0.20. A timescale is observationally interesting only if the marginalized CV S/N per unit eta rises by many orders of magnitude relative to the v0.20 value, while the numerical and distinctiveness gates remain satisfied.
