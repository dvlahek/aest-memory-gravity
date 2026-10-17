# Independent mathematical audit — B0–B3 failure-aware defect certification

This audit re-derives the benchmark mathematics independently of the frozen numerical outputs. It distinguishes mathematical validity from floating-point evaluation quality.

## Audit verdict

The analytical core of B0–B3 is correct. No sign, derivative-order, power-of-`r`, or asymptotic-scaling error was found.

One implementation issue was found: several tail integrals were evaluated through differences of nearly equal elementary antiderivatives, such as

\[
\log R-\tfrac12\log(1+R^2),
\qquad
\tfrac\pi2-\arctan R,
\qquad
R^{-1}+\arctan R-\tfrac\pi2.
\]

These formulas are mathematically correct but lose relative precision for large `R`. The post-audit implementation therefore uses algebraically equivalent stable forms. The frozen B1R1–B3R1 conclusions are unchanged; only the last digits of some finite-`h` crossover values move.

## 1. FD8 algebra

For the 9-point centered first-derivative stencil

\[
(w_{-4},\ldots,w_4)=
\left(\frac1{280},-\frac4{105},\frac15,-\frac45,0,
\frac45,-\frac15,\frac4{105},-\frac1{280}\right),
\]

the exact moments are

\[
\sum_j w_j=0,
\qquad
\sum_j j w_j=1,
\]

and

\[
\sum_j j^p w_j=0,
\qquad p=2,\ldots,8.
\]

The ninth moment is

\[
\sum_j j^9w_j=-576.
\]

Therefore the leading modified-wavenumber error is

\[
S(\xi)-\xi=-\frac{\xi^9}{630}+O(\xi^{11}),
\]

because

\[
\frac{576}{9!}=\frac1{630}.
\]

The standard pointwise FD8 remainder

\[
|D_hf(x)-f'(x)|
\le \frac{h^8}{630}\|f^{(9)}\|_{\infty,I_h}
\]

is consistent with the interpolation/Rolle remainder for this stencil.

The stencil `L1` norm is

\[
\|w\|_1=\frac{25}{12}.
\]

For the positive-side symbol coefficients,

\[
C_9=\frac{2}{9!}\sum_{j=1}^{4}|w_j|j^9
=\frac{1957}{198450}
\approx0.00986142605190224.
\]

This is a conservative sine-remainder constant. It is intentionally larger than the exact leading coefficient `1/630`.

## 2. B0 separation theorem

For

\[
f_\kappa(x)=\kappa^{-\beta}\sin(\kappa x),
\qquad 1<\beta<9,
\]

we have

\[
\|f_\kappa^{(9)}\|_\infty=\kappa^{9-\beta},
\]

so

\[
B_T=\frac{h^8}{630}\kappa^{9-\beta}\to\infty.
\]

Also

\[
|D_hf_\kappa|
\le \frac{\|w\|_1}{h}\kappa^{-\beta},
\qquad
|f_\kappa'|\le\kappa^{1-\beta},
\]

and hence

\[
B_D\le\frac{\|w\|_1}{h}\kappa^{-\beta}+\kappa^{1-\beta}\to0.
\]

Thus `B_T/B_D -> infinity`. This proof is correct and requires no quadrature or solver argument.

## 3. B1 continuum spectral benchmark

The model is

\[
F_R(x)=\int_1^R\frac{\sin(rx)}{r^2(1+r^2)}\,dr.
\]

Its ninth derivative has absolute integrand

\[
\frac{r^7}{1+r^2},
\]

with antiderivative

\[
\frac{r^6}{6}-\frac{r^4}{4}+\frac{r^2}{2}
-\frac12\log(1+r^2).
\]

Therefore

\[
B_T\sim\frac{h^8R^6}{3780}.
\]

For the FD8 symbol `S`, the exact defect integrand is

\[
\frac{[S(hr)/h-r]\cos(rx)}{r^2(1+r^2)}.
\]

### Resolved part: `hr <= 1`

Stencil exactness cancels the sine terms through degree seven. The degree-nine sine remainder gives

\[
|S(hr)-hr|\le C_9(hr)^9.
\]

After division by `h r^2(1+r^2)`, this yields

\[
C_9 h^8\frac{r^7}{1+r^2}.
\]

### Unresolved part: `hr >= 1`

Since `|S(\xi)| <= A` with

\[
A=2\sum_{j=1}^{4}|w_j|=\frac{25}{12},
\]

we obtain

\[
\left|\frac{S(hr)}{hr}-1\right|
\le1+\frac{A}{hr}.
\]

Hence the tail is bounded by

\[
\frac1{r(1+r^2)}
+\frac{A}{h}\frac1{r^2(1+r^2)}.
\]

Both terms are integrable at infinity. The direct certificate is therefore cutoff-uniform for fixed `h`.

With `R=rho/h` and `h->0`,

\[
\frac{B_T}{h^2}\to\frac{\rho^6}{3780},
\]

and for `rho>1`,

\[
\frac{B_D}{h^2}\to
\frac{C_9}{6}
+\frac12(1-\rho^{-2})
+\frac{A}{3}(1-\rho^{-3}).
\]

The independently recomputed nontrivial root is

\[
\rho_*^{B1}=4.042760931785982416999318698\ldots
\]

and

\[
\frac{B_{\rm cross}}{h^2}
=1.15498557706004488267\ldots
\]

The previous frozen value differs only in the last `~1e-14` of `rho_*` because it was obtained in double precision.

## 4. B2 generalized Maxwell benchmark

The mode equation

\[
q_t+r q=1,
\qquad q(0,r)=0
\]

has solution

\[
q(t,r)=\frac{1-e^{-rt}}r.
\]

For `n>=1`,

\[
q^{(n)}(t,r)=(-1)^{n-1}r^{n-1}e^{-rt}.
\]

Thus on the stencil interval `[0,8h]`,

\[
\sup_t|q^{(9)}|=r^8,
\]

and the weighted high-jet certificate grows as

\[
B_T\sim\frac{h^8R^7}{4410}.
\]

At `t0=4h`, write `x=hr`. The constant `1/r` term is annihilated by the derivative stencil. On the unresolved tail `x>=1`,

\[
|D_hq-q_t|
\le
\frac{A_{\rm tail}}{hr}+e^{-4},
\]

where

\[
A_{\rm tail}
=\sum_{j=-4}^{4}|w_j|e^{-(4+j)}
=0.09040463929081963139\ldots
\]

Multiplication by `1/(1+r^2)` gives two integrable tail terms.

For `R=rho/h`,

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

The independently recomputed root is

\[
\rho_*^{B2}=2.130579353067410541969818658\ldots
\]

with

\[
\frac{B_{\rm cross}}h
=0.0451903192003930098612\ldots
\]

## 5. B3 Volterra ramp-memory benchmark

The auxiliary mode

\[
z_t+r z=t,
\qquad z(0,r)=0
\]

has solution

\[
z(t,r)=\frac tr-\frac{1-e^{-rt}}{r^2}
=\frac tr-\frac1{r^2}+\frac{e^{-rt}}{r^2}.
\]

FD8 differentiates `t/r` exactly and annihilates `-1/r^2`. Only the exponential contributes to the defect.

Its ninth derivative has magnitude

\[
r^7e^{-rt},
\]

so the global high-jet certificate grows as

\[
B_T\sim\frac{h^8R^6}{3780}.
\]

For `x=hr>=1`,

\[
|D_hz-z_t|
\le
\frac{A_{\rm tail}}{hr^2}
+\frac{e^{-4}}r.
\]

After multiplication by `1/(1+r^2)`, both tail contributions are integrable.

For `R=rho/h`,

\[
\frac{B_T}{h^2}\to\frac{\rho^6}{3780},
\]

and

\[
\frac{B_D}{h^2}\to
\frac1{3780}
+\frac{A_{\rm tail}}3(1-\rho^{-3})
+\frac{e^{-4}}2(1-\rho^{-2}).
\]

The independently recomputed root is

\[
\rho_*^{B3}=2.258910484064123180273276367\ldots
\]

with

\[
\frac{B_{\rm cross}}{h^2}
=0.0351481383009534775578\ldots
\]

## 6. Stable tail evaluation

For positive `a <= b`, the following equivalent formulas avoid subtracting large nearly equal quantities:

\[
\int_a^b\frac{dr}{r(1+r^2)}
=\frac12\left[\log(1+a^{-2})-\log(1+b^{-2})\right],
\]

\[
\int_a^b\frac{dr}{r^2(1+r^2)}
=J(a)-J(b),
\qquad
J(r)=\frac1r-\arctan\frac1r,
\]

and

\[
\int_a^b\frac{dr}{1+r^2}
=\arctan\frac1a-\arctan\frac1b.
\]

For `b=infinity`, the second terms vanish.

The audited implementation in `stable_tail_integrals.py` and `audited_certificates.py` uses these forms.

At `h=0.001`, the stable finite-`h` crossover products are approximately

| benchmark | stable `h R_cross` | previous frozen value | interpretation |
|---|---:|---:|---|
| B1 | 4.042760599594705 | 4.042760551071087 | same result, last digits improved |
| B2 | 2.130579254181833 | 2.130579253958236 | same result, last digits improved |
| B3 | 2.258910345429267 | 2.258910220656792 | same result, B3 was most cancellation-sensitive |

No route classification changes.

## 7. Direct-defect identity assumptions

The identity

\[
D_hF_\lambda(x_0)-F_\lambda'(x_0)
=\int\left[\frac1h\sum_jw_jS_\lambda(x_0+jh,r)
-\partial_xS_\lambda(x_0,r)\right]d\mu(r)
\]

is exact when the finite sum is integrable and differentiation under the integral is justified.

For cutoff families such as B1–B3, the clean functional-analytic formulation uses a fixed measure space, for example `Omega=[1,infinity)`, with the cutoff represented by an indicator `1_{r<=R}`. A single integrable envelope on this fixed domain then gives the stated parameter-uniform corollary.

The phrase "weaker regularity contract" should be interpreted specifically as lower derivative order in the certification argument. It does not by itself imply weaker assumptions in every functional-analytic sense.

## 8. What is proved and what is not

The audit supports:

- exact FD8 algebra and remainder coefficient
- B0 certificate separation
- B1 cutoff-uniform direct envelope
- B2 and B3 cutoff-uniform split-direct envelopes
- the three asymptotic `rho=hR` transition equations
- `R_cross=Theta(h^-1)` for B1–B3
- model-dependent crossover amplitude scaling

It does not add a global solution-error theorem. A stability lift remains necessary for any claim beyond local/discrete defect certification.

It also does not close the AeST UV continuum envelope. The finite AeST quadrature evidence remains diagnostic until a genuine uniform integrable tail majorant is proved.
