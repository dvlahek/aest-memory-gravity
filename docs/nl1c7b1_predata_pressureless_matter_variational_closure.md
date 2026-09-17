# NL1C7B1 predata — pressureless-matter variational backreaction closure

Status: **PRE-RESULT / FROZEN BEFORE IMPLEMENTATION**

Classification before derivation:

`NL1C7B1_PREDATA_PRESSURELESS_MATTER_VARIATIONAL_CLOSURE`

## Parent result and purpose

Parent audit:

`NL1C7B_MATTER_BACKREACTION_CLOSURE_INCOMPLETE`

Official audit provenance:

- audit run: `35184894658`
- workflow head: `c4c47fcc2800d42b21625629dba3e484d2913410`
- artifact: `10481538329`
- artifact SHA256: `a7f57e6db952a7dae94211e44ef7f7b012e8bdf3fb789dc9a57b9b46e8f1853d`
- frozen audit-result commit: `6d663c661159744c44acfc919ea9d604fa6f7651`

The audit established that the frozen NL1C6 variational action has no pressureless-matter stress-energy backreaction. NL1C7B1 adds only the missing minimally coupled pressureless-matter variational sector. It does not execute a nonlinear trajectory and does not introduce finite eta.

## Frozen covariant matter action

Use an irrotational pressureless-dust velocity potential `T` and Lagrange-multiplier rest density `rho_phys`:

\[
S_d=-\frac12\int d^4x\sqrt{-g}\,\rho_{\rm phys}
\left(g^{\mu\nu}\partial_\mu T\partial_\nu T+1\right).
\]

This is minimally coupled to the same physical metric as the AeST gravitational action. In spherical radial flow there is no independent vorticity degree of freedom, so the velocity-potential representation does not remove a physical rotational mode from the frozen benchmark.

The total-action normalization is not fitted. With the AeST/gravitational sector written with its standard common prefactor `1/(16 pi G)`, define

\[
\varrho \equiv 8\pi G\rho_{\rm phys}.
\]

After removing the same common gravitational prefactor and the common angular factor used by the C6 radial action, the dust contribution is frozen as

\[
L_d=NLR^2\varrho\left(W^2-V^2-1\right),
\]

with

\[
W=\frac{T_t-bT_r}{N},\qquad V=\frac{T_r}{L}.
\]

No free multiplicative matter-coupling coefficient is allowed.

## Frozen map to the existing C6 dust variables

The density-multiplier equation imposes

\[
W^2-V^2=1.
\]

Choose the future-directed branch continuously connected to the homogeneous background:

\[
W=\cosh v,\qquad V=-\sinh v.
\]

Equivalently,

\[
T_r=-L\sinh v,\qquad T_t=N\cosh v-bL\sinh v.
\]

The additive constant in `T` is unphysical and is fixed to `T(t_i,0)=0`; no free matter mode is associated with it.

## Required exact identities

### B1-G1 — provenance

The parent audit artifact/digest and frozen C6/C7A source hashes must match exactly.

### B1-G2 — normalization constraint

Variation with respect to `varrho` must give exactly

`W^2 - V^2 - 1 = 0`.

The future-directed branch must give the frozen `cosh(v), sinh(v)` parameterization above.

### B1-G3 — continuity equation

Variation with respect to `T` must give exactly

\[
\partial_t(LR^2\varrho\cosh v)+
\partial_r\left(NR^2\varrho\sinh v-bLR^2\varrho\cosh v\right)=0,
\]

which is the already frozen C6 pressureless-matter continuity equation up to the constant density rescaling `varrho=8 pi G rho_phys`.

### B1-G4 — geodesic equation

The integrability identity `partial_t(T_r)=partial_r(T_t)`, after the frozen rapidity map, must give exactly

\[
\cosh v\left[\frac{v_t-bv_r}{N}+\frac{N_r}{NL}\right]
+\sinh v\left[\frac{v_r}{L}+k_L\right]=0,
\]

with `k_L=(L_t-bL_r-L b_r)/(N L)`, matching the frozen C6 geodesic equation.

### B1-G5 — action-derived gravitational sources

Independent variations of `L_d` with respect to `N,b,L,R`, evaluated only after variation on the dust normalization shell, must reproduce the pressureless stress-energy projections. In particular the source identities must reduce exactly to

- lapse: `dL_d/dN = -2 L R^2 varrho cosh(v)^2`;
- shift: `dL_d/db = +2 L^2 R^2 varrho cosh(v) sinh(v)`;
- radial metric: `dL_d/dL = +2 N R^2 varrho sinh(v)^2`;
- angular/areal metric: `dL_d/dR = 0` on shell.

No source may be inserted by hand outside the action variation.

### B1-G6 — FLRW normalization

For homogeneous comoving dust (`b=0`, `v=0`, `L=a`, `R=a r`), the dust lapse source must combine with the standard Einstein-Hilbert FLRW kinetic lapse variation to give

\[
3H^2=\varrho=8\pi G\rho_{\rm phys}
\]

for the pure-GR dust normalization control.

This gate fixes the relative matter/gravity coefficient and forbids post-result rescaling.

A separate diagnostic must report, but not silently repair, any mismatch between this dust-only normalization control and the full frozen CLASS/AeST homogeneous background at `a_i=0.02`. If the later NL1C7 initial constraint requires an additional standard-matter background sector not represented by this closure, that is a new explicit `INCOMPLETE` result, not permission to alter this action.

### B1-G7 — field principal-block preservation

Because `L_d` contains no `L_t`, `R_t`, `u_t`, or `phi_t`, adding dust must leave the already certified C6 field-sector principal Hessian for `(L_t,R_t,u_t,phi_t)` unchanged exactly. The G11 determinant/nonsingularity certificate therefore must remain applicable to the field block.

### B1-G8 — matter transport regularity before crossing

The dust characteristic radial transport speed in coordinates must be derived from the conserved current and reported as

\[
\frac{dr}{dt}=-b+\frac{N}{L}\tanh v.
\]

No pressure, sound speed, artificial viscosity or caustic continuation is allowed. Loss of radial ordering remains a hard NL1C7 stop event.

### B1-G9 — no direct AeST/memory matter force

The dust action may depend only on the physical metric, `T`, and `varrho`. It must contain no `u`, `phi`, `q_j`, `eta`, `J(Y)`, `K(Q)`, or memory kernel except indirectly through the metric solution. This preserves minimal coupling and the frozen C6 no-direct-memory-force requirement.

## Numerical/source audit

In addition to symbolic identities, perform a deterministic finite-difference action-variation audit for `N,b,L,R,T,varrho` on smooth nonzero two-dimensional fields. For every tested action-derived block, the relative finite-difference/component mismatch must be `<=1e-6`.

No trajectory or turnaround statistic may be evaluated in NL1C7B1.

## Classification

All B1-G1 through B1-G9 and the independent action-variation audit pass:

`NL1C7B1_PRESSURELESS_MATTER_VARIATIONAL_CLOSURE_PASS`

An exact frozen identity or normalization is inconsistent:

`NL1C7B1_PRESSURELESS_MATTER_VARIATIONAL_CLOSURE_FAIL`

The dust action is consistent but coupling it to the frozen spherical system requires another physical matter/background prescription not fixed here:

`NL1C7B1_PRESSURELESS_MATTER_VARIATIONAL_CLOSURE_INCOMPLETE`

## Claim boundary

A PASS certifies only the missing pressureless-matter variational backreaction sector and licenses an NL1C7 eta=0 short-time evolution/constraint test. It does not certify the long nonlinear trajectory, turnaround, collapse, shell crossing, finite eta, splashback, lensing, or an observable.