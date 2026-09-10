# NL1C6D2C2 pre-data: A1 derivative-level preservation audit

Status: **PREREGISTERED BEFORE THE NL1C6D2C2 A1 NUMERICAL RESULT**.

## Purpose

A0 certified the corrected homogeneous normalization, D1A operator identity, completion value slices, and published linear-to-CLASS variable mapping. A1 now applies the stronger action-level requirement needed for a completion to preserve the inherited quasistatic equations: equality of the free function on a slice is not sufficient; the first derivatives that enter the Euler-Lagrange equations must also agree.

No physical nonlinear trajectory is evolved in A1.

## Frozen completion family

Retain without modification the already preregistered D2C family on the corrected Exp normalization:

\[
F_\sigma(Y,Q)=A J(Y)-2K(Q)+\sigma\epsilon A\lambda_s B(Y)G(Z),
\]

with

\[
A=2-K_B,\quad B(Y)=\frac{Y^2}{a_0^2+Y},\quad G(Z)=\tanh Z,
\quad Z=(Q-Q_0)/Z_0,
\]

\[
\epsilon=0.25,\qquad \sigma\in\{-1,0,+1\}.
\]

All three J families and all three beta0 values remain co-primary.

## Action-level derivatives

The exact derivatives are

\[
F_Y=A J_Y+\sigma\epsilon A\lambda_s B_Y\tanh Z,
\]

\[
F_Q=-2K_Q+\sigma\epsilon A\lambda_s B(Y)\frac{\operatorname{sech}^2 Z}{Z_0},
\]

\[
F_{YQ}=\sigma\epsilon A\lambda_s B_Y\frac{\operatorname{sech}^2 Z}{Z_0},
\]

where

\[
B_Y=\frac{Y(2a_0^2+Y)}{(a_0^2+Y)^2}.
\]

The scalar Euler-Lagrange equation obtained directly from the covariant AeST action can be written as conservation of the shift current

\[
\nabla_\mu S^\mu=0,
\]

\[
S^\mu=F_Q A^\mu+2(A+F_Y)D^\mu\phi-2A J^\mu,
\]

with

\[
D^\mu\phi=(g^{\mu\nu}+A^\mu A^\nu)\nabla_\nu\phi.
\]

Therefore `F_Q` is an equation-level coefficient, not merely a background diagnostic. The aether Euler-Lagrange equation likewise receives a direct `F_Q nabla_mu phi` contribution from varying `Q=A^mu nabla_mu phi`.

## Gates

### A1.1 analytic derivative identity

For deterministic finite positive Y values spanning `x=sqrt(Y)/a0` from `1e-6` to `1e6`, compare the analytic `F_Y`, `F_Q`, and `F_YQ` expressions against independent central finite differences where numerically resolvable and exact symbolic/algebraic identities on the special slices. Numerical derivative discrepancies must be <= `1e-6`; exact slice identities use <= `1e-12` normalized discrepancy.

### A1.2 homogeneous FLRW preservation

At `Y=0`, require for every sigma, J, beta0 and deterministic Q point:

\[
F(0,Q)=-2K(Q),\qquad F_Q(0,Q)=-2K_Q(Q),
\]

and the mixed contribution to `F_Y(0,Q)` vanishes. Required normalized discrepancy <= `1e-12`.

### A1.3 quasistatic tracking equation-level preservation

At `Q=Q0`, exact preservation of the inherited R3/D1 equations requires

\[
F(Y,Q_0)=A J(Y),
\]

\[
F_Y(Y,Q_0)=A J_Y(Y),
\]

and, because the parent action is stationary in the Q direction on the tracking slice used by D1/R3,

\[
\boxed{F_Q(Y,Q_0)=0}
\]

for every co-primary completion and deterministic finite Y point.

The normalized discrepancy gate is `1e-12`, with scale `max(A a0^2, |A J(Y)|, |Y F_Y|, |Z0 F_Q|)` as appropriate.

If any sigma/J/beta combination violates this requirement, the conjunctive D2C2 completion campaign cannot PASS.

### A1.4 homogeneous shift-charge regression

At `Y=0`, the exact shift-current equation must reduce to

\[
\partial_t[a^3 F_Q(0,Q)]=0
\]

which is equivalent under `F_Q(0,Q)=-2K_Q(Q)` to

\[
\partial_t[a^3K_Q(Q)]=0.
\]

Verify algebraically and on deterministic manufactured background states with normalized discrepancy <= `1e-12`.

### A1.5 scope

No replacement of `G(Z)`, no retuning of epsilon, no solver change, no nonlinear FLRW trajectory, no memory/eta/likelihood/refit, and no branch selection is allowed within D2C2 A1.

## Classification

All A1.1-A1.5 pass for all 27 co-primary combinations:

`NL1C6D2C2_CORRECTED_COVARIANT_A1_DERIVATIVE_PASS`

otherwise:

`NL1C6D2C2_CORRECTED_COVARIANT_A1_DERIVATIVE_FAIL`

An A1 FAIL caused specifically by nonzero `F_Q(Y,Q0)` is a theory-completion preservation failure, not a numerical solver failure and not a physical exclusion of AeST. A replacement completion may be proposed only as a separately preregistered new model-completion phase; historical D2C2 remains FAIL.
