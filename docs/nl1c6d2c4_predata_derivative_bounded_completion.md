# NL1C6D2C4 pre-data: derivative-bounded covariant mixed-sector completion

Status: **PREREGISTERED BEFORE ANY D2C4 RESULT**.

## 1. Motivation and immutable history

Historical D2C, D2C2, and D2C3 classifications remain unchanged.

D2C3 established that the double-zero temporal factor `G_2(Z)=tanh^2 Z` correctly preserves the tracking value and first derivatives, but the additive spatial shape `B(Y)=Y^2/(a0^2+Y)` failed two preregistered shape gates. Its deep-MOND action correction was not sufficiently subleading at the frozen test points, and its additive `F_Y` term could push the finite-x constitutive coefficient below the D2C3 asymptotic-coefficient bound before the base `j(x)` itself had saturated.

D2C4 is a new completion family. No D2C3 threshold is changed and no D2C3 result is reclassified.

## 2. Frozen corrected homogeneous and temporal sectors

Keep

\[
K(Q)=K_2 Z_0^2(e^{Z^2}-1),\qquad Z=(Q-Q_0)/Z_0,
\]

and

\[
G_2(Z)=\tanh^2 Z.
\]

Thus `G_2(0)=G_2'(0)=0`. All cosmological/AeST parameters remain unchanged.

## 3. Derivative-bounded spatial primitive

Let

\[
x=\sqrt{Y}/a_0,\qquad S(x)=\frac{x^2}{1+x^2}=\frac{Y}{a_0^2+Y}.
\]

For each frozen interpolation family define `H(Y)` by

\[
H(0)=0,\qquad H_Y(Y)=j(x)S(x).
\]

Equivalently,

\[
H(Y)=2a_0^2\int_0^x u\,j(u)\frac{u^2}{1+u^2}\,du.
\]

No new fitted coefficient is introduced.

The D2C4 completion family is

\[
F_\sigma^{(4)}(Y,Q)=A J(Y)-2K(Q)+\sigma\epsilon_{\rm mix}A H(Y)G_2(Z),
\]

with

\[
A=2-K_B,\qquad \epsilon_{\rm mix}=0.25,\qquad \sigma\in\{-1,0,+1\}.
\]

The same three frozen `j/J` interpolation families and `beta0 in {1,0.5,0.1}` are co-primary, for 27 combinations total. No outcome-based member selection is permitted.

## 4. Exact derivative structure

By construction,

\[
F_Y=A j(x)\left[1+\sigma\epsilon_{\rm mix}S(x)G_2(Z)\right].
\]

Also

\[
F_Q=-2K_Q+\sigma\epsilon_{\rm mix}A H(Y)\frac{G_2'(Z)}{Z_0},
\]

\[
F_{YQ}=\sigma\epsilon_{\rm mix}A j(x)S(x)\frac{G_2'(Z)}{Z_0}.
\]

At `Q=Q0`, the mixed contributions to `F`, `F_Y`, `F_Q`, and `F_YQ` vanish exactly.

For every finite `x,Z`, since `0<=S<1` and `0<=G_2<1`,

\[
0.75\le \frac{F_Y}{A j(x)}\le1.25
\]

for nonzero `j`. This is a bound relative to the actual frozen local full-`j` constitutive response, not to its not-yet-reached asymptotic value at finite `x`.

In the deep-MOND regime `j=O(x)`, `J=O(x^3)`, while `S=O(x^2)` and therefore `H=O(x^5)`. Hence `H/J=O(x^2)`.

## 5. Pre-evolution gates

### C4.1 corrected homogeneous slice

For all co-primary members and `Z in {-8,-2,-0.5,0,0.5,2,8}`, require the same corrected homogeneous identities as D2C3 with maximum normalized discrepancy <= `1e-12`.

### C4.2 tracking Euler-Lagrange slice

For `x in {1e-6,1e-4,1e-2,1,1e2,1e6}` require at `Q=Q0`:

\[
F=AJ,\quad F_Y=Aj,\quad F_Q=0,\quad F_{YQ}=0.
\]

Maximum normalized discrepancy <= `1e-12` across all 27 co-primary members.

### C4.3 deep-MOND subleading behavior

At `Z=1`, nonzero sigma, all J families and beta values, use the unchanged D2C3 sequence

`x = [1e-2, 5e-3, 2.5e-3, 1.25e-3]`.

Require the absolute mixed/base action-density ratio to decrease strictly and the final ratio <= `5e-4`. The D2C3 gate is not relaxed.

### C4.4 local constitutive boundedness

For

`x = [1e-4,1e-2,1,1e2,1e3,1e4,1e6]`

and the frozen Z grid, evaluate

\[
R_Y=F_Y/(A j(x)).
\]

Require `0.75 <= R_Y <= 1.25` up to `1e-12` numerical slack for all co-primary members. This directly tests the defining derivative-bound property of the new completion.

### C4.5 high-gradient recovery

For `x in {1e2,1e3,1e4,1e6}` verify that the underlying frozen `j(x)` remains positive and approaches its unchanged asymptote `lambda_s=1/beta0`; the mixed modulation must not alter that asymptote except by the bounded factor `1+sigma*epsilon_mix*G_2(Z)` as `x->infinity`. This is evaluated from the exact analytic `F_Y` expression, with no finite-difference inference.

### C4.6 analytic derivative control

Check analytic `F_Y`, `F_Q`, and `F_YQ` against dimensionless central differences at deterministic moderate points away from the sharp kink. Tolerance `2e-6`, unchanged from D2C3.

### C4.7 scope

No nonlinear FLRW trajectory, R3 solver modification, memory/eta/likelihood/refit, or branch selection.

## 6. Classification

All C4.1-C4.7 pass:

`NL1C6D2C4_DERIVATIVE_BOUNDED_COMPLETION_IDENTITY_PASS`

otherwise:

`NL1C6D2C4_DERIVATIVE_BOUNDED_COMPLETION_IDENTITY_FAIL`

Only PASS licenses the next action-level nonlinear FLRW current/vector/constraint derivation. It does not license physical nonlinear branch evolution.
