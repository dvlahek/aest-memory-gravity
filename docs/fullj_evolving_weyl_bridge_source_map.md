# Full-J evolving-FLRW Weyl bridge — locked canonical source map

Status: **SOURCE MAP LOCKED BEFORE EVOLVING-WEYL OUTPUT**.

This note records the source mapping implemented after the preregistration in
`docs/fullj_evolving_weyl_bridge_predata.md` and before evaluating any evolving-Weyl result.
It introduces no new parameter and does not alter the already locked D2C6 nonlinear
scalar-current trajectories.

## 1. D2C5 canonical density source

The retained D2C5 action gives

\[
P_\chi=2a^3K_{QQ}U,
\qquad
U=\dot\chi-QE-\dot Q\,\alpha.
\]

The corrected effective-component background is

\[
\rho_A=\frac{QK_Q-K}{3},
\qquad
p_A=\frac{K}{3}.
\]

At linear metric-source order, varying the background energy density with respect to
`Q` gives

\[
\delta\rho_A
=\frac{1}{3}\frac{d(QK_Q-K)}{dQ}\,U
=\frac{QK_{QQ}}{3}U.
\]

Therefore the canonical density source is fixed algebraically:

\[
\boxed{\delta\rho_A=\frac{Q P_\chi}{6a^3}}.
\]

No density amplitude is fitted.

## 2. D2C5 canonical momentum source

The already derived D2C5 velocity mapping is

\[
\theta_{\rm pot}=\frac{a\Theta_A}{k^2},
\qquad
\chi=Q(\theta_{\rm pot}+\alpha).
\]

Hence

\[
\boxed{
\Theta_A=\frac{k^2}{a}\left(\frac{\chi}{Q}-\alpha\right)
}
\]

or, in the periodic real-space representation,

\[
\boxed{
\Theta_A=-\frac{1}{a}\nabla^2\left(\frac{\chi}{Q}-\alpha\right).
}
\]

Since

\[
\rho_A+p_A=\frac{QK_Q}{3},
\]

the scalar momentum-divergence source is

\[
\boxed{
q_A=(\rho_A+p_A)\Theta_A.
}
\]

## 3. Shear source

The D2C5 weak-field power counting showed that the nonlinear `J_eff(Y,Qbar)` completion
adds no retained quadratic metric-coupling term to the Hamiltonian, momentum, or shear
constraints. The effective-fluid scalar equations contain density, pressure, and momentum
but no new completion-dependent anisotropic-stress variable at this order.

Therefore the **nonlinear-completion correction** to the AeST scalar shear source is

\[
\boxed{\Delta s_A=0}.
\]

This does **not** impose `Psi=Phi` in evolving FLRW. The corrected CLASS baseline retains
its full evolving Newtonian-gauge slip from the already locked metric/matter/radiation
sector. Only the additional nonlinear full-J correction has zero new shear source at the
retained D2C5 order.

## 4. Correction construction

The locked D2C6 trajectory was evolved with the corrected CLASS metric/matter history.
The bridge therefore does not replace the full cosmological source by the AeST source.
Instead it computes

\[
\Delta\rho_A=\delta\rho_A^{\rm canonical}-\delta\rho_A^{\rm CLASS},
\]

\[
\Delta q_A=q_A^{\rm canonical}-q_A^{\rm CLASS},
\qquad
\Delta s_A=0,
\]

where the CLASS effective-component reference uses the existing `delta_cdm` and
`theta_cdm` slots that the corrected AeST bridge already uses for the effective component.
All non-AeST matter/radiation metric sources remain in the corrected CLASS baseline.

Thus

\[
\Phi=\Phi_{\rm CLASS}+\Delta\Phi,
\qquad
\Psi=\Psi_{\rm CLASS}+\Delta\Psi.
\]

## 5. Metric projection convention

Use the same Newtonian-gauge normalization as D2C6G. Let

\[
X\equiv\Delta\Phi'+\mathcal H\Delta\Psi,
\qquad \mathcal H=aH.
\]

For each nonzero retained Fourier mode,

\[
k^2X=\frac32a^2\Delta q_A,
\]

\[
k^2\Delta\Phi+3\mathcal H X+rac32a^2\Delta\rho_A=0,
\]

\[
k^2(\Delta\Psi-\Delta\Phi)+\frac92a^2\Delta s_A=0.
\]

Equivalently,

\[
\Delta\Phi_k=-\frac32a^2
\frac{k^2\Delta\rho_{A,k}+3\mathcal H\Delta q_{A,k}}{k^4},
\]

\[
\Delta\Psi_k=\Delta\Phi_k-\frac92a^2\frac{\Delta s_{A,k}}{k^2}.
\]

No post-data normalization or sign fit is permitted.

## 6. Linear and static limits

If the canonical trajectory equals the corrected linear AeST effective-component
trajectory, all source corrections vanish and the bridge returns exactly the corrected
CLASS `Phi`, `Psi`, and `W=Phi+Psi`, up to the independently frozen D2C6 numerical
trajectory error.

In the fixed-a static limit, the D2C5 scalar-current equation gives

\[
\nabla^2\Psi=\nabla\cdot[(1+j)\nabla\chi].
\]

Writing `tildePhi=Psi-chi` yields

\[
\nabla^2\tilde\Phi=\nabla\cdot[j\nabla\chi],
\]

which is exactly the locked frozen full-J operator. The static dust constraint then gives
`Psi=Phi` and hence `W=2 Phi`. This identity is used only as a static regression target and
is never promoted to evolving FLRW.

## 7. Scope

The resulting object is a one-way evolving metric reconstruction on the already locked
D2C6 nonlinear scalar-current trajectories. It does not re-evolve baryons, radiation, or
the other matter species under the reconstructed nonlinear metric. A PASS licenses only
the separately preregistered evolving-Weyl covariance/power diagnostic, not ACT or an
observational claim.

Always:

- `ACT_LIKELIHOOD_LICENSED=False`
- `OBSERVATIONAL_CLAIM_LICENSED=False`
- `NO_STATIC_W_EQUALS_2PHI_PROMOTION=True`
