# Paper skeleton — failure-aware direct defect certification

Working title:

**When High-Order Error Bounds Fail: Direct Defect Certification for Stiff Continuum-Memory Models**

Alternative:

**Failure-Aware Numerical Certification for Stiff Memory Models: Choosing Between High-Derivative and Direct-Defect Bounds**

## Abstract structure

1. State the problem: high-order derivative certificates may remain formally valid yet become non-informative under stiffness.
2. Introduce certificate-width failure as distinct from solver, model, and discretization failure.
3. Present the direct continuum-defect identity and resolved/unresolved split.
4. State the analytical separation result and the `hR` route-transition law observed across continuum and memory benchmarks.
5. Mention the AeST case only as a hard scientific stress test, with explicit limitation that the current gravity example is not yet a full continuum theorem.

## 1. Introduction

### 1.1 Problem

Validated numerical workflows often certify truncation error through high-order derivative suprema. In stiff continuum representations, these suprema may grow rapidly with the spectral cutoff even when the finite-difference defect remains small.

### 1.2 Failure taxonomy

Distinguish:

- solver failure
- model or physical failure
- discretization failure
- certificate-width failure

The last category is the target of the paper.

### 1.3 Contribution

Keep the contribution narrow and defensible:

- formalize certificate-width failure
- derive direct continuum-defect certification under a weaker regularity contract
- develop a proof-preserving route selector between high-jet and direct routes
- derive parameter-uniform separation examples
- identify the dimensionless route coordinate `rho=hR` and `R_cross=Theta(h^-1)` in several independent continuum-memory constructions
- demonstrate the method on an AeST-derived hard case without claiming a completed gravity theorem

Do not claim defect estimation, FD8, interval analysis, coordinate regularization, or residual methods as new.

## 2. Certification setup

### 2.1 Discrete derivative and defect

Define

\[
D_hf(x)=\frac1h\sum_jw_jf(x+jh),
\qquad
E_h(f;x)=D_hf(x)-f'(x).
\]

Introduce FD8 only as the concrete stencil used in experiments.

### 2.2 Conventional high-jet certificate

Write the standard remainder

\[
|E_h|\le C h^8\|f^{(9)}\|_\infty.
\]

Stress that the issue is effectivity, not validity.

### 2.3 Direct continuum-defect identity

For

\[
F_\lambda(x)=\int S_\lambda(x,r)\,d\mu(r),
\]

derive

\[
E_{h,\lambda}
=
\int
\left[
\frac1h\sum_jw_jS_\lambda(x_0+jh,r)
-
\partial_xS_\lambda(x_0,r)
\right]d\mu(r).
\]

This should be the main formal proposition.

### 2.4 Parameter-uniform corollary

If the bracket has a parameter-independent `L1` envelope, then the defect certificate is uniform in the stiffness parameter.

### 2.5 Resolved/unresolved split

Introduce the generic split

\[
r\le c/h,
\qquad
r>c/h,
\]

with `c=1` in the benchmark constructions.

Use the conventional high-jet remainder only on the resolved band and direct source-value certification on the unresolved tail.

## 3. Failure-aware route selection

Define

\[
\Gamma=\frac{B_T}{B_D}.
\]

Interpretation:

- `Gamma<1`: high-jet certificate is narrower
- `Gamma>1`: direct certificate is narrower
- `Gamma=1`: route transition

Given a certification tolerance `T`, formulate the route selector using only certified quantities.

Important: actual defect is diagnostic only and must not enter the decision rule.

## 4. Analytical separation

### 4.1 B0 theorem

Use

\[
f_\kappa=\kappa^{-\beta}\sin(\kappa x),
\quad1<\beta<9.
\]

Prove

\[
B_T\to\infty,
\qquad
B_D\to0.
\]

This gives the cleanest theorem-level demonstration of certificate separation.

### 4.2 Interpretation

Explain that failure of the high-jet proof object is not evidence of numerical instability.

## 5. Continuum and memory benchmarks

### 5.1 B1 continuum spectral benchmark

Report:

\[
\rho_*=4.042760931785968,
\]

\[
R_{\rm cross}\sim\rho_*/h,
\]

and

\[
B_{\rm cross}\sim1.15498557706h^2.
\]

### 5.2 B2 generalized Maxwell memory

Report:

\[
\rho_*=2.1305793530674104,
\]

\[
B_{\rm cross}\sim0.045190319200393h.
\]

Emphasize the initial-layer mechanism and the fact that the unresolved tail no longer requires a global ninth derivative.

### 5.3 B3 Volterra ramp memory

Report:

\[
\rho_*=2.258910484064123,
\]

\[
B_{\rm cross}\sim0.0351481383009535h^2.
\]

Emphasize exact differentiation of the smooth linear component and direct certification of the stiff exponential tail.

### 5.4 Shared phase structure

The important cross-benchmark result is not a universal `rho_*`. It is

\[
R_{\rm cross}=\Theta(h^{-1}),
\]

with `rho=hR` acting as a stiffness-resolution coordinate.

Use a summary table of constants and crossover scaling.

## 6. Numerical effectivity

Use actual defect only as a reference metric.

Suggested quantities:

- `B_T / |E_ref|`
- `B_D / |E_ref|`
- `B_T / B_D`
- route preference
- cutoff-uniform limit of `B_D`

Avoid making the paper depend on the reference quadrature for rigor.

## 7. AeST hard case study

### 7.1 Motivation from the failed high-jet route

Report the historical failure ladder only as motivation:

- naive high-jet majorants reaching about `1e28–1e39`
- compact core much smaller
- UV sector dominating the proof width

### 7.2 Regularized variables

Introduce the existing AeST change of variables only as a tool for constructing a better direct-defect envelope, not as a standalone novelty claim.

### 7.3 Regularity-contract reduction

Highlight the previously observed derivative-order reduction:

- parent requirement from order 10 to order 2
- bath requirement from order 10 to order 1

### 7.4 Claim boundary

Do not state that the AeST continuum theorem is closed unless a genuine uniform UV envelope has been proved. The existing finite quadrature proxy is not enough.

## 8. Stability lift

State clearly that the direct defect is a local or discrete consistency certificate.

For a global solution-error claim, require a separate stability theorem of the form

\[
\|e_h\|\le C_{\rm stab}\|\tau_h\|.
\]

Then

\[
\|e_h\|\le C_{\rm stab}B_D.
\]

Without this section being closed, keep the title and conclusions focused on defect certification rather than full solution-error certification.

## 9. Discussion

### 9.1 What fails

The high-jet route can fail by proof width while the discretization remains usable.

### 9.2 Why the direct route helps

It changes the regularity contract and certifies the discrete operation actually performed.

### 9.3 What is model-specific

- the direct envelope
- the transition constant `rho_*`
- the crossover certificate amplitude
- the stability constant

### 9.4 What appears shared

Across the current continuum and memory models, the relevant route coordinate is the highest spectral scale measured in grid units, `hR`.

## 10. Conclusion

Keep the conclusion narrow:

- certificate-width failure is distinct from numerical failure
- direct or split direct-defect certification can remain useful when global high-order majorants diverge
- the route decision can be made rigorously without access to the true error
- several continuum-memory models exhibit an `hR`-controlled transition
- the method is ready for a hard scientific case study, but not every stiff model is guaranteed to admit a cutoff-uniform direct certificate

## Figures

### Figure 1 — B0 analytical separation

Log-log plot of high-jet and direct certificates versus `kappa`.

### Figure 2 — B1 route phase diagram

`log10 Gamma` over `(h,R)` with the theoretical `R=rho_*/h` boundary.

### Figure 3 — B2/B3 transition collapse

Plot route ratio versus `rho=hR` for several `h` values. Show collapse toward the asymptotic curves.

### Figure 4 — cross-benchmark crossover law

Log-log `R_cross` versus `h` for B1, B2, B3 with slope `-1` reference.

### Figure 5 — certificate effectivity

Compare `B_T`, `B_D`, and diagnostic actual defect against increasing cutoff for representative `h`.

### Figure 6 — AeST failure ladder

Only after the AeST case is sufficiently closed. Show how naive absolute high-jet, signed finite route, compact/UV split, and direct-defect formulation change certificate width and required derivative order.

## Tables

### Table 1 — benchmark definitions

Model, stiff parameter, high-jet growth, direct-route structure, regularity requirement.

### Table 2 — route-transition constants

B1, B2, B3 with `rho_*`, fitted exponent, fitted prefactor, crossover amplitude scaling.

### Table 3 — AeST proof-contract comparison

Required parent derivative order, bath derivative order, UV treatment, certificate status.

## Work remaining before manuscript drafting

1. Produce the cross-benchmark figures from the locked outputs.
2. Add unit tests for certificate formulas, asymptotic constants, and route labels.
3. Decide if the paper will claim only local defect certification or include a stability lift.
4. Revisit the AeST UV envelope. Do not promote the finite-quadrature evidence into a continuum theorem.
5. Perform a focused literature comparison around validated defect control, stiff memory equations, interval/Taylor methods, and route or representation switching.
6. Only after those steps, write the full manuscript prose.
