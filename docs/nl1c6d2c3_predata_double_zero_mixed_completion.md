# NL1C6D2C3 pre-data: double-zero covariant mixed-sector completion

Status: **PREREGISTERED BEFORE ANY D2C3 RESULT**.

## 1. Motivation and immutable history

Historical D2C and D2C2 results remain unchanged.

- Historical D2C failed on the old factor-2 Exp normalization.
- Corrected D2C2 A0 passed after the Exp normalization was corrected.
- Corrected D2C2 A1 failed because the nonseparable control proportional to `tanh Z` preserved the value `F(Y,Q0)` but not the first derivative `F_Q(Y,Q0)` that enters the Euler-Lagrange equations.

D2C3 introduces a new completion family. It does not modify or reclassify D2C2.

## 2. Frozen corrected homogeneous sector

\[
K(Q)=K_2Z_0^2\left(e^{Z^2}-1\right),
\qquad Z=(Q-Q_0)/Z_0,
\]

with the already certified corrected normalization

\[
K_{QQ}(Q_0)=2K_2.
\]

All cosmological/AeST parameters remain unchanged.

## 3. New double-zero completion family

Let

\[
A=2-K_B,
\qquad
B(Y)=\frac{Y^2}{a_0^2+Y},
\qquad
G_2(Z)=\tanh^2 Z.
\]

Define

\[
F_\sigma^{(2)}(Y,Q)=A J(Y)-2K(Q)
+\sigma\epsilon_{\rm mix}A\lambda_s B(Y)G_2(Z),
\]

with

\[
\epsilon_{\rm mix}=0.25,
\qquad
\sigma\in\{-1,0,+1\},
\qquad
\lambda_s=1/\beta_0,
\]

and the same three frozen `J`/`j` interpolation families and `beta0 in {1,0.5,0.1}`. All 27 combinations are co-primary. No outcome-based member selection is permitted.

The choice `G_2=tanh^2 Z` is frozen because it is the minimal bounded replacement of the rejected `tanh Z` control with a double zero at the tracking point:

\[
G_2(0)=0,
\qquad
G_2'(0)=0.
\]

No coefficient is fitted to any nonlinear trajectory or observational result.

## 4. Exact derivatives

Writing `T=tanh Z` and `S_Z=sech^2 Z`,

\[
B_Y=\frac{Y(2a_0^2+Y)}{(a_0^2+Y)^2},
\]

\[
F_Y=A J_Y+\sigma\epsilon_{\rm mix}A\lambda_s B_Y T^2,
\]

\[
F_Q=-2K_Q+\sigma\epsilon_{\rm mix}A\lambda_s B(Y)\frac{2TS_Z}{Z_0},
\]

\[
F_{YQ}=\sigma\epsilon_{\rm mix}A\lambda_s B_Y\frac{2TS_Z}{Z_0}.
\]

At `Q=Q0`, all mixed contributions to `F`, `F_Y`, and `F_Q` therefore vanish exactly.

## 5. Pre-evolution gates

### C3.1 corrected homogeneous slice

For all co-primary members and deterministic `Z in {-8,-2,-0.5,0,0.5,2,8}` require

\[
F(0,Q)=-2K(Q),
\qquad
F_Q(0,Q)=-2K_Q(Q),
\]

and zero mixed contribution to `F_Y(0,Q)`. Normalized discrepancy <= `1e-12`.

### C3.2 tracking value and first-derivative slice

For deterministic `x=sqrt(Y)/a0 in {1e-6,1e-4,1e-2,1,1e2,1e6}` require

\[
F(Y,Q_0)=AJ(Y),
\]

\[
F_Y(Y,Q_0)=AJ_Y(Y),
\]

\[
F_Q(Y,Q_0)=0.
\]

Maximum normalized discrepancy <= `1e-12` for all 27 co-primary combinations.

### C3.3 deep-MOND subleading behavior

At fixed finite `Z` and every nonzero sigma, the absolute mixed/base action-density ratio must decrease toward zero as `x -> 0`. Use preregistered sequence

`x = [1e-2, 5e-3, 2.5e-3, 1.25e-3]`

at `Z=1`, all J families and beta values. Require strict monotone decrease and final ratio <= `5e-4`.

### C3.4 high-gradient boundedness

For `x in {1e2,1e3,1e4}`, `Z in {-8,-2,-0.5,0,0.5,2,8}`, all J/beta/sigma, evaluate the multiplicative high-gradient `F_Y` coefficient relative to `A lambda_s`. Require it remain within `[0.75,1.25]`, up to `1e-10` numerical slack. No positivity-sign flip is allowed.

### C3.5 analytic derivative control

Check the analytic mixed derivatives against high-accuracy dimensionless central differences at deterministic moderate `(x,Z)` points away from the sharp interpolation kink. This is a diagnostic gate with relative tolerance `2e-6`. The tolerance is fixed before results and is deliberately above the D2C2 finite-difference noise level `1.1718e-6`; exact slice gates remain `1e-12` and are the primary preservation tests.

### C3.6 scope

No nonlinear FLRW trajectory, no R3 solver change, no memory/eta/likelihood/refit, and no branch selection.

## 6. Classification

All C3.1-C3.6 pass:

`NL1C6D2C3_DOUBLE_ZERO_COMPLETION_IDENTITY_PASS`

otherwise:

`NL1C6D2C3_DOUBLE_ZERO_COMPLETION_IDENTITY_FAIL`

Only PASS licenses the next stage: action-level nonlinear FLRW current/vector/constraint derivation for this already-frozen family. It does not license physical nonlinear branch evolution.
