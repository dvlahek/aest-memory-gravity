# B3 manufactured Volterra ramp-memory benchmark

B3 is the second gravity-independent memory benchmark. Unlike B2, which uses a constant ramp-rate forcing of a Maxwell mode, B3 is written explicitly as a Volterra convolution driven by the manufactured input `u(t)=t`.

## Model

Define

\[
K_R(\tau)=\int_1^R \frac{e^{-r\tau}}{1+r^2}\,dr
\]

and

\[
M_R(t)=\int_0^t K_R(t-s)s\,ds.
\]

Introducing the auxiliary mode

\[
z_t+r z=t,\qquad z(0,r)=0
\]

gives

\[
z(t,r)=\frac{t}{r}-\frac{1-e^{-rt}}{r^2}
\]

and therefore

\[
M_R(t)=\int_1^R\frac{z(t,r)}{1+r^2}\,dr.
\]

The FD8 derivative is evaluated at `t0=4h`, so the stencil touches the initial layer at `t=0`.

## High-jet route

For derivative order at least two, only the exponential initial-layer term contributes. In particular,

\[
|z^{(9)}(t,r)|\le r^7
\]

on the stencil interval. Thus

\[
B_T(R;h)=\frac{h^8}{630}\int_1^R\frac{r^7}{1+r^2}\,dr
\sim \frac{h^8R^6}{3780}.
\]

For fixed `h`, the conventional certificate diverges with the relaxation-spectrum cutoff.

## Direct split

Split the spectrum at `r=1/h`.

For `r<=1/h`, retain the local FD8 Taylor remainder.

For `r>=1/h`, the smooth terms `t/r` and `-1/r^2` are handled exactly by the derivative stencil. Only the exponential layer remains. With `x=hr>=1`,

\[
|D_hz-z_t(4h,r)|
\le
\frac{A_{\rm tail}}{h r^2}
+\frac{e^{-4}}{r},
\]

where

\[
A_{\rm tail}=\sum_{j=-4}^{4}|w_j|e^{-(4+j)}
\approx 9.0404639291\times10^{-2}.
\]

After multiplication by `1/(1+r^2)`, both unresolved-tail integrals converge. Hence the direct certificate is cutoff-uniform.

## Asymptotic route transition

Let

\[
\rho=hR.
\]

As `h->0` with `R=rho/h`,

\[
\frac{B_T}{h^2}\to\frac{\rho^6}{3780},
\]

while

\[
\frac{B_D}{h^2}\to
\frac1{3780}
+\frac{A_{\rm tail}}3(1-\rho^{-3})
+\frac{e^{-4}}2(1-\rho^{-2}).
\]

The unique nontrivial crossover is

\[
\rho_*=2.258910484064123.
\]

Therefore

\[
R_{\rm cross}(h)\sim\frac{2.258910484064123}{h}.
\]

The certificate at the crossover satisfies

\[
B_{\rm cross}(h)\sim0.0351481383009535\,h^2.
\]

This gives a useful comparison across the gravity-independent benchmarks:

- B1: `R_cross ~ 4.04276093/h`, crossover certificate `O(h^2)`
- B2: `R_cross ~ 2.13057935/h`, crossover certificate `O(h)`
- B3: `R_cross ~ 2.25891048/h`, crossover certificate `O(h^2)`

The shared `hR` transition coordinate persists, while the certificate amplitude reflects the regularity and initial-layer structure of the specific memory response.

## Claim boundary

The rigorous B3 claim uses only the closed-form high-jet and direct-split certificates. QUADPACK values produced by the script are diagnostic references only.

B3 does not claim a new Volterra solver. It is a manufactured continuum-memory benchmark designed to test certificate-width failure and a proof-preserving direct-tail alternative independently of the AeST application.
