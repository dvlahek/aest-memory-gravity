# GE19 H4F3 D18 — frozen source-action canonical H1 Bernstein diagnostic

**Scope.** The source of the continuous operator is exactly the original locked GE06/GE07 canonical H1 operator evaluated on the D17 original Repair13 scalar-charge/Lambda action background. The initial canonical H1 data and all 6 positive Fourier modes for 3 original C values, Nt=128/64, are frozen D17. No bath propagation, H4 repair, observation or fitted parameter is allowed.

## Mathematical construction

For every original D17 fine subinterval `I=[a,b]` with `h=b-a`, retain its numerical endpoint states `y_a,y_b` and independently reconstruct original-action matrices `M_a,M_b`. Define `u=(x-a)/h`, `M_aff(u)=(1-u) M_a+u M_b`. Let `P(u)` be the cubic Hermite interpolant with endpoint `x`-derivatives `M_a y_a,M_b y_b`. The **surrogate** residual `r_aff(x)=P_x-M_aff P` is a polynomial of degree at most four. Convert its power coefficients exactly algebraically to degree-four Bernstein controls `b_0,...,b_4`. By convexity, in exact arithmetic on the given coefficients,

`sup_I ||r_aff||_2 <= max_{0<=j<=4} ||b_j||_2`.

Likewise, the cubic Bernstein control norms enclose `sup_I ||P||_2`, and the maximum of the endpoint Frobenius norms encloses `sup_I ||M_aff||_2`. The inequalities hold **for the affine surrogate**, not for the original source-action operator and not automatically for floating-point estimates lacking outward rounding.

The actual action residual is `P_x-M_action P=r_aff-(M_action-M_aff)P`. A valid action-operator curvature enclosure `B_i >= sup_I ||M_action,xx||_2` would imply `epsilon_M,i <= h^2 B_i/8` and the conditional residual bound `R_i <= R_aff,i+epsilon_M,i Y_i`. With `L_i<=L_aff,i+epsilon_M,i`, the error with an exact initial condition would satisfy `E_{i+1}<=exp(L_i h) E_i + (exp(L_i h)-1) R_i/L_i`. The zero-`L_i` limit is `E_i+h R_i`. The original-source curvature `B_i` is **not available or supplied by D17**, so `E_i` for the actual source action **must remain OPEN**.

## Diagnostic-only measurements

For each fine interval, also evaluate the original action operator at its midpoint to measure `||M_action(mid)-M_aff(mid)||_F`. A midpoint deviation is not `epsilon_M,i` and must not be used as a supremum. The exact-input affine-only Grönwall profile is computed and stored as `log10(1+E)` **counterfactual scenario only** to avoid floating overflow. This profile is neither an action-error bound nor an on-shell certification. D18 also recomputes the original action midpoint ODE defect, preserving its sampled-only status.

## Locked gates and physical claim boundary

- Do not edit D17, D16R1, original H3F/H3G/Z11, Repair13, GE05/GE06/GE07 or the original Repair37 SCIENCE_FAIL. Every parent hash is checked before a run. Refuse to overwrite output files.
- All six original positive modes, all source C values, both original Nt grids and **every D17 fine interval** must be retained. No high-phase or bath-node deletion is permitted; bath is not rerun here.
- Missing curvature is **not** zero, missing outward-rounding certification is **not** machine precision, and original H1 initial numerical error has not been rigorously enclosed.
- Classification on successful execution is **a conditional affine-surrogate polynomial diagnostic only**. True original continuum H1/X10, GE05 first-order bath on-shell, full H4 Ward, particular Z21, lensing and observable fitting remain OPEN.

Next source-certified stage: obtain interval-valid `M_action` curvature or direct `M_action-M_aff` enclosures from symbolic original GE06/GE07 linear operator and original-action `H,Q,Z`, with outward rounding, then validate the initial state and propagate the bounds to `X10` and its derivative. Only subsequently rerun the physical GE05 bath with an independent numerical propagation enclosure.
