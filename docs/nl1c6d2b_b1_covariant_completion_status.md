# NL1C6D2B B1 — covariant nonlinear FLRW completion status

Status: **B1_INCOMPLETE_MIXED_F_YQ_COMPLETION_NOT_FROZEN**

This note records the theory-level resolution of the B1 blocker identified by the preregistered `NL1C6D2B_FLRW_SOURCE_GRAVITY_COUPLING_AUDIT`. It does not change the locked D2B classification

`NL1C6D2B_FLRW_SOURCE_GRAVITY_COUPLING_AUDIT_INCOMPLETE`

and it does not authorize D2 nonlinear branch evolution or NL1C7.

## 1. Covariant starting point

AeST is defined by a free function `F(Y,Q)` of the two covariant invariants

\[
Q=A^\mu\nabla_\mu\phi,
\qquad
Y=(g^{\mu\nu}+A^\mu A^\nu)\nabla_\mu\phi\nabla_\nu\phi.
\]

The full 3+1/Hamiltonian formulation is therefore sufficient in principle to derive a nonlinear FLRW longitudinal system once the full two-variable function `F(Y,Q)` is specified.

Primary theory references:

- C. Skordis and T. Zlosnik, Phys. Rev. Lett. 127, 161302 (2021), arXiv:2007.00082.
- M. Bataki, C. Skordis and T. Zlosnik, Phys. Rev. D 110, 044015 (2024), arXiv:2307.15126.

## 2. Action-derived weak-field FLRW invariant reduction

Take Newtonian-gauge weak fields on a spatially flat FLRW background,

\[
ds^2=-(1+2\Psi)dt^2+a^2(t)(1-2\Phi)\,\delta_{ij}dx^idx^j,
\]

with

\[
\phi=\bar\phi(t)+\varphi(t,\mathbf x),
\qquad
A_i=\partial_i\alpha
\]

in the scalar longitudinal sector. Let

\[
\bar Q=\dot{\bar\phi}.
\]

The 3+1 identity

\[
Y=|D\phi|^2+Q^2-\sigma^2
\]

and the unit-aether constraint give, at the weak-field order relevant here,

\[
Q=\bar Q+\gamma+O(\epsilon^2),
\qquad
\gamma=\dot\varphi-\bar Q\Psi,
\]

while the leading spatially nonlinear invariant is

\[
Y=\frac{1}{a^2}\left|\nabla\left(\varphi+\bar Q\alpha\right)\right|^2+
O(\epsilon^3).
\]

Thus the longitudinal combination is

\[
\chi=\varphi+\bar Q\alpha,
\]

and the full spatial nonlinearity enters through the physical-gradient invariant

\[
Y=a^{-2}|\nabla\chi|^2
\]

at this order. The factor `a^{-2}` follows from the action/3+1 geometry; it is not an inserted Hubble or damping prescription.

This establishes that retaining a full nonlinear `J(Y)` spatial operator on FLRW is structurally compatible with the covariant theory.

## 3. What the repository has actually frozen

The repository fixes two different pieces of the covariant free-function information.

### 3.1 Background / linear-cosmology Q-sector

The frozen CLASS bridge specifies the homogeneous background through the selected `Exp` `K(Q)` sector, with

\[
K(Q)=-\frac12 F(0,Q)
\]

in the AeST cosmological convention. It also fixes the corresponding linear scalar perturbation system on that FLRW trajectory.

Therefore the slice

\[
F(0,Q)
\]

and the derivatives of `F` sampled by the frozen linear trajectory are constrained.

### 3.2 Nonlinear spatial Y-sector

NL1C1 independently freezes the full published interpolation family

\[
j(x)=\frac{dJ}{dY},
\qquad x=\sqrt{Y}/a_0,
\]

and fixes the additive normalization

\[
J(0)=0.
\]

The quasistatic convention is

\[
J(Y)=\frac{F(Y,Q_0)}{2-K_B},
\]

with the frozen `Exp` background satisfying `K(Q0)=0`. NL1C6/D1A then certify the corresponding full-`J` static spatial operator.

Neither freeze specifies the full mixed dependence of `F(Y,Q)` away from those slices.

## 4. Strong non-uniqueness proof preserving the full linear trajectory

Let `Q_* = Q0` denote the tracking/quasistatic value at which the frozen full-`J` spatial slice is defined, and let `F_*(Y,Q)` be any completion consistent with all already frozen background, linear and static information.

For any sufficiently regular function `C(Y,Q)` with the required dimensions, define

\[
F_C(Y,Q)=F_*(Y,Q)+Y^2(Q-Q_*)C(Y,Q).
\]

Then

\[
F_C(0,Q)=F_*(0,Q)
\]

for every `Q`, so the complete homogeneous background slice is unchanged, and

\[
F_C(Y,Q_*)=F_*(Y,Q_*)
\]

for every `Y`, so the complete frozen quasistatic/full-`J` spatial slice is unchanged.

Moreover, because the deformation starts at quadratic order in `Y`,

\[
\left.\frac{\partial F_C}{\partial Y}\right|_{Y=0,Q}
=
\left.\frac{\partial F_*}{\partial Y}\right|_{Y=0,Q}
\]

for every `Q` on the homogeneous FLRW trajectory. Hence the already frozen linear `Y` coefficient and the quadratic action for linear scalar perturbations are unchanged along the full background history, not merely at the point `Q=Q_*`.

Nevertheless the nonlinear mixed sector changes. In particular,

\[
\left.\frac{\partial^3 F_C}{\partial Y^2\partial Q}\right|_{(0,Q_*)}
=
\left.\frac{\partial^3 F_*}{\partial Y^2\partial Q}\right|_{(0,Q_*)}
+2C(0,Q_*).
\]

Away from the two frozen slices, higher nonlinear `Y-Q` derivatives generally differ as well.

Therefore the existing background, full linear cosmology and full-`J` static information does **not** uniquely determine the mixed nonlinear `Y-Q` couplings required by nonlinear FLRW dynamics.

This is a structural underdetermination, not a numerical solver problem.

## 5. Consequence for a separable completion

A natural candidate is the additive/separable completion

\[
F_{\rm sep}(Y,Q)=(2-K_B)J(Y)-2K(Q),
\]

using the already frozen `J(0)=0` and `K(Q0)=0` conventions. It exactly reproduces

\[
F_{\rm sep}(0,Q)=-2K(Q),
\qquad
F_{\rm sep}(Y,Q_0)=(2-K_B)J(Y).
\]

Such a completion is mathematically admissible, but it sets the unfrozen nonlinear mixed `Y-Q` couplings to zero by choice. It is therefore a **new theory/model-completion assumption** relative to the current frozen repository. It cannot be silently inserted into D2B and called a derivation of the already frozen model.

The same applies to any nonseparable completion: its mixed sector must be declared before inspecting nonlinear branch-evolution outputs.

## 6. B1 decision

The action-level invariant reduction establishes

\[
Q=\bar Q+\gamma+\cdots,
\qquad
Y=a^{-2}|\nabla\chi|^2+\cdots,
\]

but the repository does not freeze enough information to evaluate the required nonlinear FLRW equations uniquely because the nonlinear mixed `F(Y,Q)` sector remains unspecified even after demanding exact preservation of the frozen background and full linear trajectory.

Hence

\[
\boxed{\text{B1 = INCOMPLETE: NONLINEAR MIXED }F(Y,Q)\text{ COMPLETION NOT FROZEN}.}
\]

This strengthens the interpretation of the existing D2B result: B1 cannot be closed merely by more algebra on the currently frozen model. A model-completion choice is required first.

## 7. What remains valid

This result does not change any earlier classification:

- NL1C6R3 remains a numerical/static reclosure FAIL, not a physical exclusion.
- D1 remains PASS for the certified 1D longitudinal gravitational formulation audit.
- D2A remains PASS for the baryon density/momentum history and continuity audit.
- D2B remains INCOMPLETE with no hard contradiction.
- The exact fixed-`a` full-`J` identity remains certified.
- The frozen linear CLASS AeST trajectory remains certified within its stated scope.

## 8. Correction provenance

The first version of this note used the illustrative deformation `Y(Q-Q_*)C`. That is sufficient to preserve the homogeneous and static slices but can alter `F_Y(0,Q)` away from `Q_*`, and therefore is not the strongest proof when the full frozen linear FLRW trajectory is also to be preserved. The corrected deformation `Y^2(Q-Q_*)C` preserves `F_Y(0,Q)` for every background `Q`. The B1 classification is unchanged; only the non-uniqueness proof has been strengthened.
