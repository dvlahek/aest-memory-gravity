# NL1C6D2C5 pre-data: action-level nonlinear FLRW longitudinal weak-field reduction

Status: **PREREGISTERED BEFORE ANY D2C5 RESULT**.

## 1. Purpose and immutable history

D2C5 asks whether the corrected AeST model with the D2C4 derivative-bounded mixed completion admits a controlled FLRW longitudinal weak-field reduction directly from the covariant AeST action, retaining the full nonlinear MOND spatial response while reproducing the corrected frozen CLASS linear system and the D1A/R3 limits.

Historical D2B, D2C, D2C2, D2C3, D2C4, and D2C4R1 classifications remain unchanged. D2C4R1 PASS licenses this derivation stage only. No nonlinear FLRW branch is evolved here.

## 2. Covariant starting point

Use the published AeST action

\[
S=\frac{1}{16\pi\tilde G}\int d^4x\sqrt{-g}\left[
R-\frac{K_B}{2}F_{\mu\nu}F^{\mu\nu}
+2A J^\mu\nabla_\mu\phi
-A Y-\mathcal F(Y,Q)
-\lambda(A^\mu A_\mu+1)
\right]+S_m[g],
\]

with

\[
A=2-K_B,\quad
Q=A^\mu\nabla_\mu\phi,\quad
Y=(g^{\mu\nu}+A^\mu A^\nu)\nabla_\mu\phi\nabla_\nu\phi,
\]

\[
J^\mu=A^\alpha\nabla_\alpha A^\mu,\qquad
F_{\mu\nu}=2\nabla_{[\mu}A_{\nu]}.
\]

For the corrected D2C4 family,

\[
\mathcal F_\sigma(Y,Q)=A\left[J(Y)+\sigma\epsilon_{\rm mix}H(Y)G_2(Z)\right]-2K(Q),
\]

\[
G_2(Z)=\tanh^2 Z,\quad Z=(Q-Q_0)/Z_0,\quad \epsilon_{\rm mix}=0.25,
\]

\[
H_Y(Y)=j(x)\frac{x^2}{1+x^2},\qquad x=\sqrt{Y}/a_0,
\]

with the same 27 co-primary `(sigma, interpolation, beta0)` members as D2C4.

## 3. Controlled MOND weak-field ordering

Introduce a bookkeeping weak-field amplitude `eps` with

- `Phi, Psi, alpha gradients, varphi/Q0` of ordinary weak-field order;
- `a0` counted as the same weak acceleration scale, so `Y=O(eps^2)` while `x=sqrt(Y)/a0=O(1)` is not expanded;
- the action is retained through quadratic order in ordinary perturbation amplitudes;
- functions of `Y/a0^2` are kept nonperturbatively;
- the homogeneous background `a(t), H(t), Qbar(t), K_Q(Qbar), K_QQ(Qbar)` is retained exactly;
- terms in which a perturbative `delta Q` multiplies an already quadratic spatial invariant `J(Y)` or `H(Y)` are cubic and are omitted at this weak-field order.

This is the only permitted resummation. No Hubble damping, pseudo-time, continuation parameter, branch preference, or phenomenological evolution term may be added by hand.

## 4. Longitudinal variables and geometric identities

Use cosmic time and Newtonian gauge

\[
ds^2=-(1+2\Psi)dt^2+a^2(t)(1-2\Phi)d\mathbf x^2.
\]

At first weak-field order,

\[
A_\mu=(-1-\Psi,\partial_i\alpha),
\]

and define

\[
\chi=\varphi+\bar Q\alpha,\qquad E=\dot\alpha+\Psi,
\]

\[
U=\dot\chi-\bar Q E-\dot{\bar Q}\alpha.
\]

The reduction must establish directly from the covariant definitions that

\[
Q=\bar Q+U+\delta Q^{(2)}+\cdots,
\]

with the spatial second-order piece, in the background-metric part,

\[
\delta Q^{(2)}_{\rm spatial}
=a^{-2}\left(\nabla\alpha\cdot\nabla\chi
-\frac{\bar Q}{2}|\nabla\alpha|^2\right),
\]

and

\[
Y=a^{-2}|\nabla\chi|^2+O(\mathrm{eps}^3),
\]

\[
F_{0i}=\partial_i E+O(\mathrm{eps}^2),\qquad
J_i=\partial_i E+O(\mathrm{eps}^2).
\]

No factor of `a` may be inserted by analogy; all factors must follow from the metric and cosmic-to-conformal conversion.

## 5. Scalar/vector reduced action that must be obtained

After use of the homogeneous shift-charge background equation and dropping background/total-derivative terms, the background-metric scalar/vector block must reduce to

\[
L_{sv}=a^3K_{QQ}(\bar Q)U^2
+aK_B|\nabla E|^2
+2Aa\,\nabla E\cdot\nabla\chi
-Aa|\nabla\chi|^2
-a^3A J_{\rm eff}(Y,\bar Q)
\]

\[
\qquad +2aK_Q(\bar Q)\left[
\nabla\alpha\cdot\nabla\chi
-\frac{\bar Q}{2}|\nabla\alpha|^2
\right],
\]

where

\[
J_{\rm eff}(Y,\bar Q)=J(Y)+\sigma\epsilon_{\rm mix}H(Y)G_2(\bar Z),
\quad \bar Z=(\bar Q-Q_0)/Z_0.
\]

The corresponding generalized canonical momenta are frozen as derivation targets:

\[
P_\chi=2a^3K_{QQ}U,
\]

\[
P_\alpha=-2a^3\bar QK_{QQ}U
-\nabla\cdot\left(2aK_B\nabla E+2Aa\nabla\chi\right).
\]

The scalar/vector Euler equations from this block are

\[
\dot P_\chi
+2Aa\nabla^2E
-2Aa\nabla\cdot[(1+j_{\rm eff})\nabla\chi]
+2aK_Q\nabla^2\alpha=0,
\]

\[
\dot P_\alpha
+2a^3K_{QQ}U\dot{\bar Q}
+2aK_Q\nabla^2\chi
-2aK_Q\bar Q\nabla^2\alpha=0,
\]

with

\[
j_{\rm eff}=\partial_YJ_{\rm eff}
=j(x)\left[1+\sigma\epsilon_{\rm mix}\frac{x^2}{1+x^2}G_2(\bar Z)\right].
\]

These equations are targets to be checked against an independent component expansion of the covariant scalar/vector field equations; writing them here does not count as a PASS by itself.

## 6. Linear-cosmology bridge: explicit -A Y versus full J

The corrected frozen CLASS perturbation bridge contains no `lambda_s` parameter. Its linear pressure closure contains `K_B E + A chi`, and its linear vector equation uses the same `A=2-K_B` coefficient.

This is the required action-level mapping:

- `j(0)=0` for all three frozen full-J interpolation families;
- `H_Y(0)=0`;
- therefore `F_Y(0,Qbar)=0` for the D2C4 completion;
- the nonzero linear spatial coefficient is supplied by the explicit covariant action term `-A Y`, so the total projected-gradient coefficient is `A+F_Y -> A`.

The separate D1B `lambda_s=1/beta0` Minkowski dispersion regression is a tracking/high-gradient limit where `F_Y -> A lambda_s`; it is not the `Y->0` cosmological linearization and must not be used as the corrected CLASS linear coefficient.

## 7. Metric constraints and nonlinear power counting

D2C5 may PASS only if the metric sector is closed from the same action/order counting.

The derivation must explicitly show that dependence of `J_eff(Y,Qbar)` on `Psi` or `Phi` first enters the action at cubic weak-field order (`metric perturbation * spatial invariant`) and therefore does not add a new full-J term to the retained linear Einstein Hamiltonian/momentum/shear constraints. The remaining linear AeST stress/momentum terms must be derived from the temporal/background pieces of the same action and mapped to the corrected CLASS effective-fluid convention, including `(rho_A+p_A) theta_A`.

If this cannot be established without importing a constraint by analogy, the overall D2C5 classification is `INCOMPLETE`, even if the scalar/vector subsystem passes.

## 8. Preregistered gates

### A5.1 covariant geometry/order audit

Independently evaluate the longitudinal weak-field expansion and require the identities for `Q`, `delta Q^(2)_spatial`, `Y`, `F_0i`, and `J_i` with maximum normalized algebraic/manufactured-field discrepancy <= `1e-12`.

### A5.2 reduced-action Euler audit

Derive the scalar/vector Euler equations independently from the reduced action and from the leading component expansion of the covariant scalar and vector equations. On deterministic manufactured Fourier states, require coefficient/residual agreement <= `1e-12`.

### A5.3 zero-expansion/D1A regression

Set `a=1`, `H=0`, `Qbar=Q0`, `Qdot=0`, `K_Q=0`, `K_QQ=2K2`, `G_2(0)=0`. Require

\[
P_\chi=4K_2U,
\]

\[
P_\alpha=-4K_2Q_0U+2K_Bk^2E+2Ak^2\chi
\]

and the D1A canonical regression at <= `1e-12`.

### A5.4 fixed-a quasistatic/R3 regression

Require the independent fixed-a full-J operator/source-coupling regression to remain <= `1e-12` for all frozen interpolation/beta families. No static solver or branch continuation is run.

### A5.5 corrected CLASS linearization

Take `Y->0`, hence `j_eff->0`. Require the resulting linear coefficient structure to reproduce the frozen corrected CLASS AeST equations in Newtonian gauge. Reuse deterministic manufactured-state comparison with maximum relative discrepancy <= `1e-12`, but additionally require source-code anchors showing that the CLASS bridge contains `K_B E + A chi` and no `lambda_s`/`beta0` coefficient in the linear AeST perturbation equations.

### A5.6 metric Hamiltonian/momentum/shear closure

Require an action-derived power-counting and component mapping for the retained metric constraints. The nonlinear `J_eff` metric correction must be shown to start beyond retained order. Linear AeST density, pressure, momentum and shear conventions must map to the frozen CLASS effective-fluid stress. Exact algebraic/source-anchor checks use `1e-12` where numerical comparison is applicable.

If the metric mapping is not fully established, A5.6=`INCOMPLETE`, not FAIL unless a derived identity is contradicted.

### A5.7 matter convention

The corrected D2AC result must remain PASS. No new theta convention is introduced.

### A5.8 scope

No nonlinear FLRW trajectory, finite eta, memory forcing, observational likelihood, cosmological refit, or branch selection.

## 9. Classification

All A5.1-A5.8 established and passed:

`NL1C6D2C5_ACTION_LEVEL_FLRW_LONGITUDINAL_REDUCTION_PASS`

A derived/evaluated required identity is contradicted:

`NL1C6D2C5_ACTION_LEVEL_FLRW_LONGITUDINAL_REDUCTION_FAIL`

No hard contradiction, but one or more required action-derived mappings cannot be closed without an additional theory/ordering choice:

`NL1C6D2C5_ACTION_LEVEL_FLRW_LONGITUDINAL_REDUCTION_INCOMPLETE`

Only PASS licenses a nonlinear FLRW branch-evolution implementation. INCOMPLETE or FAIL forbids it. Historical classifications are never reclassified by D2C5.
