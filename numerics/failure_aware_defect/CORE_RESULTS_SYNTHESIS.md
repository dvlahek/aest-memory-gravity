# Core results synthesis — failure-aware defect certification

This file freezes the gravity-independent numerical-methods story before any AeST case study is promoted into the paper.

## 1. Problem class

The project studies centered finite-difference certification for stiff continuum and memory models in which a conventional high-order Taylor remainder is formally valid but becomes non-informative because its derivative majorant grows with a stiffness or spectral-cutoff parameter.

The target defect is

\[
E_h(f;x)=D_hf(x)-f'(x).
\]

The key methodological distinction is between

- numerical or solver failure, and
- certificate-width failure, where the computed solution can remain regular while the chosen proof object becomes excessively wide.

The direct route changes the certified object before increasing derivative order or precision. It bounds the actual stencil defect from source values at stencil nodes together with a first derivative at the target, or applies this construction only to the unresolved spectral tail.

## 2. Frozen benchmark chain

### B0 — analytical separation witness

\[
f_\kappa(x)=\kappa^{-\beta}\sin(\kappa x),\qquad 1<\beta<9.
\]

For fixed `h`, the standard FD8 high-jet certificate satisfies

\[
B_T\sim h^8\kappa^{9-\beta}\to\infty,
\]

while the elementary direct certificate satisfies

\[
B_D\le \|w\|_1 h^{-1}\kappa^{-\beta}+\kappa^{1-\beta}\to0.
\]

This proves certificate separation without quadrature, solver effects, or a physical model.

### B1 — continuum spectral model

\[
F_R(x)=\int_1^R\frac{\sin(rx)}{r^2(1+r^2)}\,dr.
\]

The standard ninth-derivative certificate diverges as

\[
B_T\sim \frac{h^8R^6}{3780}.
\]

The direct continuum-symbol certificate remains finite as `R -> infinity`. With the dimensionless coordinate

\[
\rho=hR,
\]

the asymptotic route transition is

\[
R_{\rm cross}(h)\sim\frac{\rho_*}{h},
\qquad
\rho_*=4.042760931785968.
\]

The crossover certificate scales as

\[
B_{\rm cross}\sim1.15498557706\,h^2.
\]

The frozen finite-h fit is approximately

\[
R_{\rm cross}\approx4.03966311\,h^{-1.00013338}.
\]

### B2 — generalized Maxwell continuum memory

For each relaxation rate `r`,

\[
q_t+r q=1,\qquad q(0,r)=0,
\]

and

\[
M_R(t)=\int_1^R\frac{q(t,r)}{1+r^2}\,dr.
\]

At `t0=4h`, the FD8 stencil reaches the initial layer. The global ninth-derivative certificate grows as

\[
B_T\sim\frac{h^8R^7}{4410}.
\]

The failure-aware route keeps the high-jet argument only on the resolved band `r<=1/h` and directly certifies the unresolved tail. The direct certificate is cutoff-uniform.

The asymptotic route transition is

\[
R_{\rm cross}(h)\sim\frac{2.1305793530674104}{h},
\]

with crossover scale

\[
B_{\rm cross}\sim0.045190319200393\,h.
\]

The frozen finite-h fit is approximately

\[
R_{\rm cross}\approx2.12965814\,h^{-1.00007525}.
\]

### B3 — manufactured Volterra ramp memory

Define

\[
K_R(\tau)=\int_1^R\frac{e^{-r\tau}}{1+r^2}\,dr,
\]

and for the ramp input `u(t)=t`,

\[
M_R(t)=\int_0^tK_R(t-s)s\,ds.
\]

The auxiliary mode is

\[
z_t+r z=t,\qquad z(0,r)=0,
\]

with

\[
z(t,r)=\frac{t}{r}-\frac{1-e^{-rt}}{r^2}.
\]

FD8 differentiates the linear part exactly and annihilates the constant part. The unresolved-tail direct route therefore isolates the stiff exponential contribution.

The global high-jet certificate grows as

\[
B_T\sim\frac{h^8R^6}{3780},
\]

while the direct split certificate is cutoff-uniform. The asymptotic route transition is

\[
R_{\rm cross}(h)\sim\frac{2.258910484064123}{h},
\]

with

\[
B_{\rm cross}\sim0.0351481383009535\,h^2.
\]

The frozen B3R1 fit is

\[
R_{\rm cross}\approx2.25761912735\,h^{-1.00009949201}.
\]

## 3. Shared structure across B1–B3

The three continuum benchmarks have different source structures, different high-jet growth powers, and different crossover-certificate amplitudes. They nevertheless share the same stiffness-resolution coordinate

\[
\rho=hR
\]

and the same asymptotic route law

\[
R_{\rm cross}(h)=\Theta(h^{-1}).
\]

This supports the interpretation that the route transition is controlled by whether the upper relaxation or spectral scale is resolved by the stencil spacing.

The constants are model-specific:

| Benchmark | Model | `rho_*` | crossover certificate |
|---|---|---:|---:|
| B1 | continuum oscillatory spectral source | 4.0427609318 | `1.1549855771 h^2` |
| B2 | generalized Maxwell memory | 2.1305793531 | `0.0451903192 h` |
| B3 | Volterra ramp memory | 2.2589104841 | `0.0351481383 h^2` |

The shared `hR` law should therefore be presented as a route-resolution structure, not as a universal transition constant.

## 4. General direct-defect identity

For

\[
F_\lambda(x)=\int_\Omega S_\lambda(x,r)\,d\mu(r),
\]

if the finite stencil sum and first derivative can be interchanged with the integral, then

\[
D_hF_\lambda(x_0)-F_\lambda'(x_0)
=
\int_\Omega
\left[
\frac1h\sum_jw_jS_\lambda(x_0+jh,r)
-\partial_xS_\lambda(x_0,r)
\right]d\mu(r).
\]

A parameter-uniform integrable envelope for the bracket gives a parameter-uniform defect certificate without requiring a global high-order derivative majorant.

This identity is the central theorem-level object. B1 is a direct full-spectrum realization. B2 and B3 are resolved/unresolved split realizations.

## 5. Failure-aware route rule

Given two independently valid certificates for the same defect,

- `B_T`: conventional high-jet certificate
- `B_D`: direct or direct-split certificate

and a requested tolerance `T`, use only certified quantities:

1. evaluate `B_T`
2. accept the conventional route if `B_T<=T`
3. if `B_T` is too wide, non-finite, or requires an unavailable high-order enclosure, evaluate `B_D`
4. if `B_D<=T`, classify the event as high-jet certificate-width failure
5. if neither route closes, report the result as inconclusive

The unknown actual error must not be used for route selection.

If both routes return interval enclosures of the same defect, their intersection may be returned.

## 6. What the current evidence supports

The gravity-independent core now supports the following claims:

1. A formally valid high-order truncation certificate can become arbitrarily non-informative under stiffness while another rigorous certificate of the same defect remains informative.
2. Direct continuum-defect certification can replace a global ninth-derivative requirement with source values and a first derivative at the target.
3. In continuum-memory problems, a resolved/unresolved split can confine high-order derivative reasoning to the resolved band and remove it from the stiff spectral tail.
4. Across three independent continuum constructions, the certificate-route transition satisfies `R_cross=Theta(h^-1)` and is naturally expressed through `rho=hR`.
5. The crossover amplitude scaling is model dependent, so the method does not assume a universal threshold or universal effectivity constant.
6. The route selector can be proof preserving because it uses only independently valid certificates and never the unknown actual defect.

## 7. Claims that remain out of scope

The current evidence does not establish:

- a universal `rho_*` across models
- a universal direct-certificate effectivity bound
- a global solution-error theorem without a separate stability lift
- a full AeST continuum certificate
- that all stiff problems admit a cutoff-uniform direct envelope
- that high-jet certificate failure implies physical, solver, or discretization failure

## 8. Next scientific step

Do not add another toy benchmark at this stage.

The next step is to organize the paper around the theorem core and the B0–B3 evidence, then introduce AeST only as a hard case study showing why the method was needed and how the regularized direct-defect route changes the proof contract in a real scientific model.
