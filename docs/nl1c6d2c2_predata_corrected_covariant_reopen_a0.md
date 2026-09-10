# NL1C6D2C2 pre-data: corrected covariant completion reopen — A0 structural action regression

Status: **PREREGISTERED BEFORE ANY NL1C6D2C2 A0 RESULT**.

## 1. Purpose and immutable history

Historical `NL1C6D2C_COVARIANT_MIXED_SECTOR_COMPLETION_FAIL` remains unchanged. It failed because the historical factor-2 Exp normalization had local `K_QQ(Q0)=4 K2`, while D1A/Minkowski AeST requires `K_QQ(Q0)=2 K2`.

The corrected branch `v053-exp-normalization-corrected` has independently established:

- `NL1C6D2N_EXP_NORMALIZATION_AUDIT_PASS`;
- `NL1C6D2N_CORRECTED_CLASS_BASELINE_R1_PASS`;
- `NL1C5BC_CORRECTED_BARYON_SOURCE_FREEZE_PASS`;
- `NL1C6D2AC_CORRECTED_BARYON_MATTER_SECTOR_AUDIT_PASS`;
- `NL1C6R3C_CORRECTED_BLOCKING_SNAPSHOT_BLOCKING`.

The last result means the corrected source did not remove the frozen static R3 numerical blocker. D2C2 therefore does not attempt another static solver repair. It reopens only the covariant nonlinear FLRW formulation after the normalization inconsistency has been corrected.

## 2. Primary action convention

Use the AeST action

\[
S=\int d^4x\,\frac{\sqrt{-g}}{16\pi\tilde G}
\left[R-\frac{K_B}{2}F_{\mu\nu}F^{\mu\nu}
+2(2-K_B)J^\mu\nabla_\mu\phi
-(2-K_B)\mathcal Y-\mathcal F(\mathcal Y,\mathcal Q)
-\lambda(A^\mu A_\mu+1)\right]+S_m[g],
\]

with

\[
\mathcal Q=A^\mu\nabla_\mu\phi,
\qquad
\mathcal Y=(g^{\mu\nu}+A^\mu A^\nu)\nabla_\mu\phi\nabla_\nu\phi.
\]

Primary provenance is Skordis & Zlosnik, PRL 127, 161302 (2021), and PRD 106, 104041 (2022). The full 3+1 Hamiltonian provenance is Bataki, Skordis & Zlosnik, PRD 110, 044015 (2024).

The corrected homogeneous function is frozen as

\[
K_{\rm Exp}(Q)=K_2 Z_0^2\left(e^{Z^2}-1\right),
\qquad Z=(Q-Q_0)/Z_0,
\]

so

\[
K_{QQ}(Q_0)=2K_2.
\]

No return to the historical factor-2 Exp expression is allowed in D2C2.

## 3. Completion family inherited without retuning

Retain the already preregistered co-primary D2C family, changing only the homogeneous Exp normalization already fixed before this reopen:

\[
F_0(Y,Q)=(2-K_B)J(Y)-2K_{\rm Exp}(Q),
\]

\[
F_\sigma(Y,Q)=F_0(Y,Q)
+\sigma\epsilon_{\rm mix}(2-K_B)\lambda_s
Y\tanh Z\,\frac{x^2}{1+x^2},
\]

where

\[
x=\sqrt{Y}/a_0,
\qquad \epsilon_{\rm mix}=0.25,
\qquad \sigma\in\{-1,0,+1\}.
\]

All three `sigma`, all three frozen `J` interpolation families, and `beta0 in {1,0.5,0.1}` remain co-primary. No member may be selected by outcome.

## 4. A0 weak-field FLRW ordering

Use cosmic-time Newtonian gauge

\[
ds^2=-(1+2\Psi)dt^2+a^2(t)(1-2\Phi)d\mathbf x^2,
\]

\[
\phi=\bar\phi(t)+\varphi,
\qquad
A_\mu=(-1-\Psi,\partial_i\alpha)+O(\epsilon^2).
\]

Metric, scalar-time, and aether perturbation amplitudes are weak-field quantities. Do **not** expand in the dimensionless MOND ratio `x=sqrt(Y)/a0`; full `J(Y)` dependence is retained when D2C2-A1 is reached.

At A0 the action-derived invariant identities to be tested are

\[
\delta Q\equiv\gamma=\dot\varphi-\bar Q\Psi+O(\epsilon^2),
\]

\[
D_i\phi\equiv(g_i{}^\nu+A_iA^\nu)\nabla_\nu\phi
=\partial_i(\varphi+\bar Q\alpha)+O(\epsilon^2),
\]

hence

\[
\chi=\varphi+\bar Q\alpha,
\qquad
Y=a^{-2}|\nabla\chi|^2+O(\epsilon^3).
\]

A0 does not yet claim the full nonlinear FLRW field equations. It certifies the action, variables, time convention, corrected local curvature, and published linear limit before nonlinear mixed terms are derived.

## 5. Published linear variables and exact CLASS conversion

Use the published cosmic-time variables

\[
\chi=\varphi+\bar Q\alpha,
\qquad
\gamma=\dot\varphi-\bar Q\Psi,
\qquad
E=\dot\alpha+\Psi,
\qquad
\theta_{\rm pot}=\varphi/\bar Q.
\]

The repository CLASS variable is a velocity divergence

\[
\Theta=\frac{k^2}{a}\theta_{\rm pot},
\qquad
\mathcal H=aH,
\qquad
X'=a\dot X.
\]

Therefore the published fluid/vector equations must transform identically to

\[
\delta'=3\mathcal H(w\delta-\Pi)-(1+w)(\Theta-3\Phi'),
\]

\[
\Theta'=(3c_{ad}^2-1)\mathcal H\Theta
+\frac{k^2\Pi}{1+w}+k^2\Psi,
\]

\[
\alpha'=a(E-\Psi),
\]

\[
E'=\frac{a}{K_B}\left\{
K_Q\chi-(2-K_B)\left[
\frac{Q\Pi}{1+w}+(H+Q)\chi-3c_{ad}^2HQ\alpha
\right]\right\}-\mathcal H E.
\]

For the nonstandard pressure, CLASS stores the homogeneous effective density as

\[
\rho_{\rm CLASS}=\frac{8\pi\tilde G}{3}\bar\rho,
\]

so the Fourier-space published pressure law becomes

\[
\Pi=c_{ad}^2\delta+
\frac{c_{ad}^2 k^2}{3a^2\rho_{\rm CLASS}}
[K_BE+(2-K_B)\chi].
\]

This conversion is a theory-to-code comparison. The independent theory evaluator must be coded from the equations above; source-text anchors are checked separately.

## 6. A0 gates

### A0.1 corrected Minkowski curvature

Require exactly

\[
K_{QQ}(Q_0)=2K_2,
\qquad
\mu^2=\frac{2K_2Q_0^2}{2-K_B},
\]

with numerical relative discrepancy `<=1e-12` against the frozen D1A value.

### A0.2 D1A canonical regression

Re-run the existing independent D1A canonical regression unchanged. Require maximum relative error `<=1e-12`.

### A0.3 fixed-a full-J operator regression

Re-run the existing independent D1A static reduction regression unchanged for all three `J`, all three `beta0`, and `a in {1/7,0.5,1}`. Require maximum relative error `<=1e-12`.

This is an operator identity only. It does not require or claim a numerical R3 root.

### A0.4 completion exact slices

For every co-primary completion require, at deterministic finite test points,

\[
F_\sigma(0,Q)=-2K_{\rm Exp}(Q),
\]

\[
F_\sigma(Y,Q_0)=(2-K_B)J(Y),
\]

and the mixed deformation plus its first Y derivative vanish at `Y=0`. Maximum normalized discrepancy `<=1e-12`.

### A0.5 published-linear to CLASS-convention manufactured regression

Use 64 deterministic manufactured states spanning finite positive `a,H,Q,rho_CLASS`, `w>-1`, `cad2>=0`, nonzero `k`, and signed perturbation variables. Independently evaluate the published cosmic-time equations and transform them with `Theta=k^2 theta_pot/a`, `prime=a dot`, `mathcal H=aH`. Compare against a separately implemented evaluator in repository CLASS conventions for `Pi`, `delta'`, `Theta'`, `alpha'`, and `E'`.

Maximum relative discrepancy for every quantity: `<=1e-12`.

### A0.6 source-anchor provenance

The corrected CLASS patch must contain the frozen corrected Exp `K/KQ/KQQ/inverse` formulas and the exact structural AeST perturbation anchors corresponding to:

- `chi = Q*(a*theta/k^2 + alpha)`;
- nonstandard pressure using `K_B E + (2-K_B) chi`;
- `alpha' = a(E-Psi)`;
- `E' = a E_rhs/K_B - mathcal H E`;
- AeST fluid density and velocity evolution.

Historical factor-2 Exp anchors must be absent. This is a provenance gate, not the independent numerical theory regression.

### A0.7 scope

No full nonlinear FLRW trajectory, branch selection, memory forcing, finite eta, likelihood, cosmological refit, R3 solver change, or NL1C7 is allowed.

## 7. Classification

All A0.1–A0.7 pass:

`NL1C6D2C2_CORRECTED_COVARIANT_A0_STRUCTURAL_PASS`

Otherwise:

`NL1C6D2C2_CORRECTED_COVARIANT_A0_STRUCTURAL_FAIL`

A PASS licenses only D2C2-A1: derivation and audit of the nonlinear terms generated by `F_sigma,Y`, `F_sigma,Q`, and mixed derivatives on FLRW. It does not license physical nonlinear branch evolution.
