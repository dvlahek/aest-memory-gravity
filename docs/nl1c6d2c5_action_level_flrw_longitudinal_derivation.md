# NL1C6D2C5 action-level FLRW longitudinal weak-field derivation

This document implements the preregistered D2C5 derivation from the covariant AeST action. It does not evolve a nonlinear cosmological branch.

## 1. Ordering and variables

Write `A = 2-K_B` and use cosmic-time Newtonian gauge

\[
ds^2=-(1+2\Psi)dt^2+a^2(1-2\Phi)d\mathbf x^2,
\qquad A_i=\partial_i\alpha.
\]

Define

\[
\chi=\varphi+\bar Q\alpha,\qquad E=\dot\alpha+\Psi,
\]

and, because the homogeneous scalar charge is time dependent on FLRW,

\[
U=\dot\chi-\bar Q E-\dot{\bar Q}\alpha.
\]

The weak-field amplitudes are counted as `O(eps)`, while `a0` is counted as the same weak acceleration scale. Hence `Y=O(eps^2)` but `x=sqrt(Y)/a0` can remain `O(1)`. We retain the action through quadratic ordinary weak-field order without Taylor expanding functions of `x`.

## 2. Direct geometric expansion

On the unperturbed spatial background, unit normalization gives

\[
A^0=1+\frac{|\nabla\alpha|^2}{2a^2}+O(\epsilon^3),
\qquad A^i=a^{-2}\partial^i\alpha+O(\epsilon^2).
\]

With metric lapse restored, the first-order lapse pieces cancel in `Q` after `E` is introduced. Direct expansion gives

\[
Q=\bar Q+U+\delta Q^{(2)}+O(\epsilon^3),
\]

where the background-metric spatial part is

\[
\delta Q^{(2)}_{sp}=a^{-2}\left(
\nabla\alpha\cdot\nabla\chi-\frac{\bar Q}{2}|\nabla\alpha|^2
\right).
\]

The projected scalar gradient is

\[
q_i{}^\nu\nabla_\nu\phi=\partial_i\chi+O(\epsilon^2),
\]

so

\[
Y=a^{-2}|\nabla\chi|^2+O(\epsilon^3).
\]

For the longitudinal aether,

\[
F_{0i}=\partial_i(\dot\alpha+\Psi)=\partial_iE.
\]

The FLRW connection terms in the acceleration cancel at first order:

\[
A^0\nabla_0A_i=\partial_i\dot\alpha-H\partial_i\alpha+\partial_i\Psi,
\]

\[
A^j\nabla_jA_i=H\partial_i\alpha,
\]

therefore

\[
J_i=\partial_iE+O(\epsilon^2).
\]

This cancellation is why no independently chosen `H alpha` term may be added to `J_i`.

## 3. Expansion of the corrected Q sector

The corrected model has

\[
K(Q)=K_2Z_0^2(e^{Z^2}-1),\qquad Z=(Q-Q_0)/Z_0.
\]

The covariant action contains `-F`, and `F(Y,Q)` contains `-2K(Q)`, hence the action contains `+2K(Q)`.

Expanding around `Qbar` gives

\[
2K(Q)=2K(\bar Q)+2K_Q U+K_{QQ}U^2+2K_Q\delta Q^{(2)}+O(\epsilon^3).
\]

The first-order `2K_Q U` term is a total/background term after using the homogeneous shift-charge law

\[
\frac{d}{dt}(a^3K_Q)=0.
\]

Its background-metric quadratic spatial remainder is

\[
2aK_Q\left(
\nabla\alpha\cdot\nabla\chi-rac{\bar Q}{2}|\nabla\alpha|^2
\right).
\]

The temporal kinetic term is `a^3 K_QQ U^2`. At the tracking point `Qbar=Q0`, corrected normalization gives `K_Q=0` and `K_QQ=2K2`.

## 4. MOND-resummed spatial sector

For D2C4/D2C4R1,

\[
\mathcal F_\sigma(Y,Q)=A\,J_{eff}(Y,Q)-2K(Q),
\]

\[
J_{eff}=J(Y)+\sigma\epsilon_{mix}H(Y)\tanh^2 Z,
\]

\[
\partial_YJ_{eff}=j_{eff}
=j(x)\left[1+\sigma\epsilon_{mix}\frac{x^2}{1+x^2}\tanh^2Z\right].
\]

Because `Y` itself is already quadratic in ordinary weak-field amplitudes, a perturbative `delta Q` multiplying `J_eff(Y,Qbar)` is cubic. Therefore at retained order the nonlinear spatial function is evaluated on the homogeneous `Qbar(t)` but is not expanded in `Y/a0^2`.

The explicit covariant `-A Y` term is separate from `-F`. Thus the total spatial derivative coefficient in the scalar current is

\[
A+\mathcal F_Y=A(1+j_{eff}).
\]

This resolves the apparent linear-cosmology/tracking ambiguity. In the cosmological `Y->0` limit, `j_eff->0`, so the coefficient is `A`, exactly as in the corrected frozen CLASS bridge. In a high-gradient tracking limit, `j->lambda_s`, giving `A(1+lambda_s)`, which is the separate D1B/Minkowski tracking coefficient.

## 5. Background-metric scalar/vector action

The Maxwell term, acceleration coupling, explicit `-A Y`, full `-F`, and corrected Q expansion give

\[
L_{sv}=a^3K_{QQ}U^2+aK_B|\nabla E|^2
+2Aa\nabla E\cdot\nabla\chi
-Aa|\nabla\chi|^2-a^3A J_{eff}(Y,\bar Q)
\]

\[
\qquad +2aK_Q\left(
\nabla\alpha\cdot\nabla\chi-\frac{\bar Q}{2}|\nabla\alpha|^2
\right).
\]

The generalized momenta are

\[
P_\chi=2a^3K_{QQ}U,
\]

\[
P_\alpha=-2a^3\bar QK_{QQ}U
-\nabla\cdot(2aK_B\nabla E+2Aa\nabla\chi).
\]

Variation gives the background-metric scalar equation

\[
\dot P_\chi+2Aa\nabla^2E
-2Aa\nabla\cdot[(1+j_{eff})\nabla\chi]
+2aK_Q\nabla^2\alpha=0,
\]

and the longitudinal aether equation at fixed `chi`

\[
\dot P_\alpha+2a^3K_{QQ}U\dot{\bar Q}
+2aK_Q\nabla^2\chi
-2aK_Q\bar Q\nabla^2\alpha=0.
\]

The scalar equation is independently obtained from the exact shift-current form

\[
\nabla_\mu I^\mu=0,
\]

\[
I^\mu=\mathcal F_QA^\mu
+2(A+\mathcal F_Y)q^{\mu\nu}\nabla_\nu\phi
-2AJ^\mu.
\]

At retained order its spatial component is

\[
a^3I^i=a\left[-2K_Q\partial^i\alpha
+2A(1+j_{eff})\partial^i\chi
-2A\partial^iE\right],
\]

while its temporal perturbation gives `-P_chi`; multiplying current conservation by `-1` reproduces the scalar Euler equation above. This is the direct covariant check that the full nonlinear `j_eff` enters only through the projected scalar-current divergence at this order.

## 6. Metric sector and why the nonlinear J term does not alter the retained constraints

The nonlinear spatial action density `J_eff(Y,Qbar)` is `O(eps^2)`. Its dependence on a scalar metric perturbation can arise only through

1. `sqrt(-g)=a^3[1+O(Psi,Phi)]`, or
2. the metric inside `Y=a^{-2}|grad chi|^2[1+O(Phi,...)]`, or
3. a perturbative `delta Q` in the mixed temporal factor.

Each adds another ordinary weak-field amplitude. Therefore every completion-dependent metric term is `O(eps^3)` or higher and is absent from the quadratic weak-field action. The D2C4 resummation consequently changes the nonlinear scalar-current equation but does not introduce an additional completion-dependent term into the retained Hamiltonian, momentum, or shear constraints.

The remaining metric perturbation sector is exactly the linear AeST metric sector derived from the same covariant action. In the effective-fluid variables used by the frozen CLASS bridge it obeys

\[
\dot\delta_A=3H(w_A\delta_A-\Pi_A)
+(1+w_A)\left(3\dot\Phi-\frac{k^2}{a^2}\theta_A\right),
\]

\[
\dot\theta_A=3c_{ad}^2H\theta_A+\frac{\Pi_A}{1+w_A}+\Psi,
\]

with

\[
\Pi_A=c_{ad}^2\delta_A+
\frac{c_{ad}^2k^2}{3a^2\rho_A}
\left[K_BE+A\chi\right]
\]

in the repository sign/Fourier convention, and

\[
K_B(\dot E+HE)=K_Q\chi-A\left[
\frac{Q\Pi_A}{1+w_A}+(H+Q)\chi-3c_{ad}^2HQ\alpha
\right].
\]

The effective momentum source entering the Einstein momentum constraint is `(rho_A+p_A) theta_A`. The repository bridge implements precisely this convention.

The mapping between the effective velocity potential and the longitudinal fields is

\[
\theta_{pot}=\frac{a\,\Theta_A}{k^2},\qquad
\chi=Q(\theta_{pot}+\alpha),
\]

where `Theta_A` is the CLASS velocity-divergence variable. Thus no extra factor of `a` is free to choose.

The Einstein-Hilbert part remains the standard GR one. Since the nonlinear completion adds no quadratic metric-coupling term, the standard Newtonian-gauge Hamiltonian/momentum/shear constraints with the AeST effective density, pressure and `(rho+p)theta` above are the complete retained metric constraints for this ordering.

## 7. Limits

### Tracking/Minkowski point

At `a=1`, `H=0`, `Qbar=Q0`, `Qdot=0`, `K_Q=0`, `K_QQ=2K2`, and `tanh(Z)=0`,

\[
U=\dot\chi-Q_0E,
\]

\[
P_\chi=4K_2U,
\]

\[
P_\alpha=-4K_2Q_0U+2K_Bk^2E+2Ak^2\chi
\]

for a Fourier mode, exactly reproducing D1A.

### Fixed-a quasistatic limit

At zero time derivatives, `E=Psi`, and the scalar-current equation gives

\[
\nabla^2\Psi=\nabla\cdot[(1+j)\nabla\chi]
\]

at `Q=Q0`. Therefore, defining `tildePhi=Psi-chi`,

\[
\nabla^2\tilde\Phi=\nabla\cdot[j\nabla\chi],
\]

which is the frozen R3/D1A full-J operator.

### Linear cosmological limit

At `Y->0`, `j_eff->0`. The explicit `-A Y` term supplies the `A chi` contribution in the pressure/vector closure. No `lambda_s` or `beta0` enters the corrected CLASS linear perturbation equations. The D1B `lambda_s` dispersion relation is a distinct high-gradient/tracking Minkowski control and is not substituted into this limit.

## 8. Derivation status

Within the preregistered MOND weak-field ordering, the nonlinear completion modifies the scalar projected-gradient response while the metric/effective-fluid constraint sector remains the published linear AeST one. This follows from the covariant action power counting, not from adding a phenomenological damping/evolution law.

The accompanying numerical/algebraic audit must still pass every preregistered D2C5 gate before nonlinear FLRW evolution is licensed.
