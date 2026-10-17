# B2 generalized Maxwell continuum-memory benchmark

This benchmark is the first gravity-independent continuum-memory test in the failure-aware certification project.

## Model

For relaxation rate `r in [1,R]`, define the Maxwell mode

\[
q_t+r q=1,\qquad q(0,r)=0,
\]

so that

\[
q(t,r)=\frac{1-e^{-rt}}{r}.
\]

The continuum memory observable is

\[
M_R(t)=\int_1^R\frac{q(t,r)}{1+r^2}\,dr.
\]

The FD8 derivative is evaluated at `t0=4h`, so the 9-point stencil lies exactly on `[0,8h]` and includes the initial layer at `t=0`.

## Why the high-jet route fails

The ninth derivative of a mode is

\[
|q^{(9)}(t,r)|=r^8e^{-rt}.
\]

Because the stencil interval includes `t=0`, the interval supremum is `r^8`. Therefore the conventional global FD8 certificate is

\[
B_T(R;h)=\frac{h^8}{630}\int_1^R\frac{r^8}{1+r^2}\,dr
\sim\frac{h^8R^7}{4410}.
\]

For fixed `h`, this diverges as the relaxation-spectrum cutoff `R` grows.

## Failure-aware direct split

Split the spectrum at

\[
r=1/h.
\]

For `r<=1/h`, the modes are resolved and the usual FD8 remainder is retained locally.

For `r>=1/h`, use the actual Maxwell-mode values at the stencil nodes and the exact first derivative at the target. With `x=hr>=1`, the constant `1/r` part of the mode cancels exactly under the derivative stencil. The remaining exponential terms satisfy

\[
e^{-(4+j)x}\le e^{-(4+j)}.
\]

Hence the unresolved tail obeys

\[
|D_hq-q_t(4h,r)|
\le
\frac{A_{\rm tail}}{hr}+e^{-4},
\]

where

\[
A_{\rm tail}=\sum_{j=-4}^{4}|w_j|e^{-(4+j)}
\approx 9.0404639291\times10^{-2}.
\]

After multiplication by `1/(1+r^2)`, both tail integrals converge. Thus the direct split certificate remains finite as `R->infinity` even though the global high-jet certificate diverges.

## Asymptotic route transition

Let

\[
\rho=hR.
\]

As `h->0` with `R=rho/h`, the two rigorous certificates satisfy

\[
\frac{B_T}{h}\to\frac{\rho^7}{4410},
\]

and

\[
\frac{B_D}{h}\to
\frac1{4410}
+\frac{A_{\rm tail}}2(1-\rho^{-2})
+e^{-4}(1-\rho^{-1}).
\]

Their nontrivial asymptotic crossover is

\[
\rho_*=2.1305793530674104.
\]

Therefore

\[
R_{\rm cross}(h)\sim\frac{2.1305793530674104}{h}.
\]

The certificate scale at the transition is linear in `h`:

\[
B_T\sim B_D\sim 0.045190319200393\,h.
\]

This differs from B1, where the transition certificate scales as `h^2`. The dimensionless route parameter `hR` persists, but the certificate scaling reflects the initial-layer structure of the memory model.

## Claim boundary

The rigorous B2 claim uses only the closed-form high-jet and direct-split bounds. QUADPACK values printed by the script are diagnostic references only.

The direct route is not claimed to remove all high derivatives everywhere. It confines the conventional high-jet argument to the resolved spectral band `r<=1/h` and removes the global ninth-derivative requirement from the unresolved relaxation tail, where the proof-width explosion originates.
