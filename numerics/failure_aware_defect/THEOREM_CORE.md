# Theorem core — failure-aware direct defect certification

This note defines the gravity-independent mathematical core for the
failure-aware numerical-certification project.

The purpose is not to introduce a new finite-difference stencil and not to
claim that defect-based a-posteriori estimation is new. The target is more
specific:

> A high-order derivative certificate can remain formally valid but lose
> effectivity catastrophically under stiffness. A direct certificate of the
> stencil defect can remain informative under a strictly weaker regularity
> contract.

The two benchmark families below isolate that statement before any AeST case
study is used.

## 1. Discrete derivative and defect

Let

\[
D_h f(x)=\frac1h\sum_{j=-m}^{m} w_j f(x+jh)
\]

be a centered first-derivative stencil and define

\[
E_h(f;x)=D_hf(x)-f'(x).
\]

For the 9-point centered FD8 rule used in the benchmark,

\[
(w_{-4},\ldots,w_4)=
\left(
\frac1{280},-\frac4{105},\frac15,-\frac45,0,
\frac45,-\frac15,\frac4{105},-\frac1{280}
\right).
\]

Its standard high-jet remainder form is

\[
|E_h(f;x)|
\le
\frac{h^8}{630}\,
\|f^{(9)}\|_{\infty,I_h},
\]

under the usual smoothness assumptions on the stencil interval \(I_h\).

This bound is mathematically valid when its hypotheses hold. The project
studies the different question of whether the bound remains informative as a
stiffness or spectral-cutoff parameter grows.

## 2. B0 separation theorem

Consider

\[
f_\kappa(x)=\kappa^{-\beta}\sin(\kappa x),
\qquad
1<\beta<9.
\]

### Proposition B0

For fixed \(h>0\), the conventional FD8 high-jet certificate obeys

\[
B_T(\kappa)
=
\frac{h^8}{630}\kappa^{9-\beta}
\longrightarrow \infty
\qquad
(\kappa\to\infty).
\]

At the same time, the defect admits the direct elementary certificate

\[
|E_h(f_\kappa;x)|
\le
B_D(\kappa)
=
\frac{\|w\|_1}{h}\kappa^{-\beta}
+
\kappa^{1-\beta},
\]

and therefore

\[
B_D(\kappa)\longrightarrow0.
\]

Hence

\[
\frac{B_T(\kappa)}{B_D(\kappa)}
\longrightarrow\infty.
\]

### Proof sketch

The ninth derivative has amplitude
\(\kappa^{9-\beta}\), which gives the first statement.

For the direct bound,

\[
|E_h|
\le |D_hf_\kappa|+|f_\kappa'|.
\]

The stencil contribution satisfies

\[
|D_hf_\kappa|
\le
h^{-1}\|w\|_1\kappa^{-\beta},
\]

and

\[
|f_\kappa'|
\le
\kappa^{1-\beta}.
\]

Both terms vanish for \(\beta>1\). No derivative above first order is required
by this direct certificate.

### Interpretation

B0 proves a true certificate-separation result. It does not rely on roundoff,
quadrature error, solver failure, or a physical model. The high-jet
certificate can become arbitrarily non-informative while another rigorous
certificate of the same stencil defect shrinks.

## 3. B1 continuum spectral benchmark

Define

\[
F_R(x)
=
\int_1^R
\frac{\sin(rx)}{r^2(1+r^2)}
\,dr.
\]

Then

\[
F_R'(x)
=
\int_1^R
\frac{\cos(rx)}{r(1+r^2)}
\,dr.
\]

The ninth-derivative absolute majorant is

\[
M_9(R)
=
\int_1^R
\frac{r^7}{1+r^2}\,dr,
\]

with closed form

\[
M_9(R)
=
\left[
\frac{r^6}{6}
-\frac{r^4}{4}
+\frac{r^2}{2}
-\frac12\log(1+r^2)
\right]_1^R.
\]

Therefore

\[
B_T(R)
=
\frac{h^8}{630}M_9(R)
\sim
\frac{h^8R^6}{3780},
\]

so the conventional high-jet certificate diverges with the spectral cutoff.

## 4. Direct continuum defect identity

For a general continuum source

\[
F_\lambda(x)
=
\int_\Omega S_\lambda(x,r)\,d\mu(r),
\]

suppose the finite stencil sum and first derivative can be interchanged with
the integral. Then

\[
E_{h,\lambda}
=
D_hF_\lambda(x_0)-F_\lambda'(x_0)
=
\int_\Omega
\Delta_{h,\lambda}(r)\,d\mu(r),
\]

where

\[
\Delta_{h,\lambda}(r)
=
\frac1h
\sum_j
w_j S_\lambda(x_0+jh,r)
-
\partial_xS_\lambda(x_0,r).
\]

This identity changes the certification object. A direct enclosure of
\(\Delta_{h,\lambda}\) needs source values at stencil nodes and a first
derivative at the target point. It does not require a global ninth-derivative
supremum.

### Parameter-uniform corollary

If there exists \(g\in L^1(d\mu)\), independent of \(\lambda\), such that

\[
|\Delta_{h,\lambda}(r)|\le g(r)
\]

for all relevant \(\lambda\), then

\[
|E_{h,\lambda}|
\le
\int_\Omega g(r)\,d\mu(r)
\]

uniformly in \(\lambda\).

This may hold even when the conventional high-derivative majorant diverges
with \(\lambda\).

## 5. Explicit B1 cutoff-uniform certificate

For the FD8 symbol

\[
S(\xi)
=
2\sum_{j=1}^{4} w_j\sin(j\xi),
\]

the exact B1 defect integrand is

\[
\frac{[S(hr)/h-r]\cos(rx)}
     {r^2(1+r^2)}.
\]

For \(|\xi|\le1\), stencil exactness through degree eight and the sine
remainder give

\[
|S(\xi)-\xi|
\le
C_9|\xi|^9,
\]

with

\[
C_9
=
\frac{2}{9!}
\sum_{j=1}^{4}|w_j|j^9
=
\frac{1957}{198450}.
\]

For \(|\xi|\ge1\),

\[
\left|\frac{S(\xi)}{\xi}-1\right|
\le
1+\frac{A}{|\xi|},
\qquad
A=2\sum_{j=1}^{4}|w_j|
=\frac{25}{12}.
\]

Splitting at \(r=1/h\) yields a fully explicit direct certificate

\[
B_D(R;h)
=
C_9h^8
\int_1^{\min(R,1/h)}
\frac{r^7}{1+r^2}\,dr
\]

plus, when \(R>1/h\),

\[
\int_{1/h}^{R}
\frac{dr}{r(1+r^2)}
+
\frac{A}{h}
\int_{1/h}^{R}
\frac{dr}{r^2(1+r^2)}.
\]

Both tail integrals converge. Hence, for fixed \(0<h\le1\),

\[
\sup_{R\ge1} B_D(R;h)<\infty,
\]

while

\[
B_T(R;h)\to\infty.
\]

For \(h=10^{-2}\), the explicit direct certificate converges to approximately

\[
1.1960211073\times10^{-4},
\]

while the Taylor certificate grows like \(R^6\).

This is the continuum analogue of the B0 separation result.

## 6. Failure-aware route selection

A certification workflow may use two independently valid routes:

- \(B_T\): conventional high-jet certificate
- \(B_D\): direct-defect certificate

Given a prescribed certification tolerance \(T\):

1. compute \(B_T\)
2. accept if \(B_T\le T\)
3. if \(B_T\) is too wide, non-finite, or requires an unavailable high-order
   enclosure, evaluate \(B_D\)
4. if \(B_D\le T\), classify the event as high-jet certificate-width failure
5. if neither route closes, report the result as inconclusive

The classification must not use the unknown true defect.

If both routes produce interval enclosures for the same defect, the returned
certificate may be their intersection. Route selection therefore need not
weaken rigor.

## 7. Stability lift

The direct defect certificate is a local/discrete certification object. A
separate stability result is required before claiming a global solution-error
bound.

If a discrete problem satisfies

\[
\|e_h\|
\le
C_{\rm stab}\|\tau_h\|
\]

and the direct route proves

\[
\|\tau_h\|\le B_D,
\]

then

\[
\|e_h\|
\le
C_{\rm stab}B_D.
\]

This stability lift should be included if the final paper claims certified
solution error rather than certified stencil defect.

## 8. Claim boundary

The paper should not claim:

- that defect-based a-posteriori estimation is new
- that FD8 is new
- that variable regularization is new
- that every stiff problem admits a parameter-uniform direct certificate
- that a failed high-jet certificate implies solver or model failure

The intended contribution is the combination of:

1. certificate-width failure as a distinct numerical-certification failure mode
2. direct certification of the continuum stencil defect under stiffness
3. explicit reduction of the regularity contract
4. parameter-uniform separation results where the high-jet certificate diverges
5. a proof-preserving route-selection workflow

AeST should enter only after B0, B1, and at least one generic memory benchmark
have established the method independently of gravity.
