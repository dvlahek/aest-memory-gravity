# v0.19o — global fixed-frequency positive bath reduction

v0.19m showed that an `H(t)`-dependent rational table is not dynamically equivalent to the original conservative bath. The preferred route is therefore to keep **fixed physical oscillator frequencies** and compress only the positive spectral measure.

For the dimensionless continuum Drude bath,

\[
K_h(z)=\frac{A}{1+A},\qquad A=\sqrt{z(z+3h)},
\]

and the exact oscillator representation is

\[
K_h(z)=\frac{2}{\pi}\int_0^\infty\frac{d\omega}{1+\omega^2}
\frac{A^2}{A^2+\omega^2}.
\]

A finite positive approximation has

\[
K_N(z,h)=\sum_j w_j\frac{A^2}{A^2+\omega_j^2},
\qquad w_j\ge0,\quad \omega_j>0.
\]

Unlike the v0.19l local rational table, the frequencies and weights do **not** depend on `H(t)`. Therefore each retained mode obeys exactly the same non-autonomous covariant oscillator equation as the underlying conservative bath.

## v0.19o goals

1. Fit positive fixed-frequency weights directly on a broad retarded complex-frequency training domain covering `H tau` from `1e-4` to `1e8`.
2. Validate on independent interlaced complex-frequency points.
3. Validate in the time domain on LCDM-like, pure-radiation, and pure-matter expansion histories with oscillatory and pulse drives.
4. Check positivity, high/low-frequency limits, and conservative-mode structure.
5. Select the smallest candidate representation satisfying the numerical gate.

## Target gate

For the selected finite bath:

- all weights non-negative;
- all frequencies strictly positive and time-independent;
- complex-domain `p95 < 1e-3`;
- complex-domain `p99 < 3e-3`;
- complex-domain worst case `< 1e-2`;
- independent time-domain `p95 < 1e-3`;
- independent time-domain worst case `< 3e-3`.

The time-domain criteria are the primary physics gate because they compare directly with the dense conservative bath under changing `H(t)`.

## Scope

Memory remains outside CLASS in v0.19o. If this gate passes, the selected fixed-frequency bath is the representation to insert into CLASS for the first controlled tangent finite-`eta` CMB test.
