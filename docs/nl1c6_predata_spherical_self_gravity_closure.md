# NL1C6 predata — spherical self-gravity closure

Classification before derivation: **NL1C6_PREDATA_SPHERICAL_SELF_GRAVITY_CLOSURE**

This checkpoint begins only after `NL1C5_SPHERICAL_VARIATIONAL_BRIDGE_PASS`. It is a theory/component-closure gate. No turnaround, collapse, splashback, halo mass, lensing statistic, finite physical eta outcome, likelihood or observational data may be inspected here.

## Frozen provenance

- parent NL1C5 result commit: `226f57f8c5d978c52646d2911a518765c882274d`;
- NL1C5 official run: `35087054333`;
- NL1C5 artifact ID: `10441759239`;
- NL1C5 artifact digest: `sha256:6831d0f81022a8c57d7f623fafc9ecfc1ef1f2cb94abd44cd84bed837cb290af`;
- NL1C1 full Y-operator family: `NL1C1_FULL_Y_OPERATOR_BRIDGE_PASS`;
- NL1C5 spherical memory reduction: `NL1C5_SPHERICAL_VARIATIONAL_BRIDGE_PASS`.

Historical classifications remain immutable.

## Theory frozen before component results

Use the already frozen covariant AeST action and NL0B memory action. The AeST Y-sector must retain all nine co-primary combinations

- `Simple`, `Exponential`, `Sharp`;
- `beta0 = {1, 0.5, 0.1}`.

No interpolation/beta0 pair may be selected after seeing a spherical result. The full `j(x)=dJ/dY` function is used locally. The replacement `j=1/beta0` is permitted only as a diagnostic high-gradient limit, never as a global spherical-profile substitution because regular spherical configurations contain regions where the radial gradient approaches zero.

The Q-sector remains the frozen Exp cosmological branch and frozen parameters already used by the closed linear chain. No new Q-Y cross term is introduced.

The memory sector is exactly NL0B/NL1C5. No phenomenological radial drag or shell acceleration may be appended.

## Spherical variables

Retain the ungauged spherical coframe

\[
\theta^0=Ndt,\qquad
\theta^1=L(dr+b\,dt),\qquad
\theta^2=R d\theta,\qquad
\theta^3=R\sin\theta\,d\varphi,
\]

with aether rapidity `u(t,r)`, scalar `phi(t,r)`, frozen bath scalars `q_j(t,r)`, and pressureless minimally coupled matter.

Do not impose `R=r`, `b=0`, synchronous gauge, aether-comoving gauge or matter-comoving gauge until the ungauged Euler-Lagrange/constraint system has been generated and its redundancy structure identified.

## Primary target

Generate a closed spherical component system for

\[
(g_{ab},R;\,u,\phi,q_j;\,T^{\mu\nu}_{m})
\]

directly from the frozen action, retaining lapse and shift equations as constraints before any gauge fixing.

The result must distinguish:

1. evolution equations;
2. Hamiltonian/radial-momentum or equivalent scalar constraints;
3. aether/unit-frame constraint already parameterized by `u`;
4. scalar equation;
5. bath equations;
6. pressureless-matter conservation/geodesic equations.

## Locked gates

### C6-G1 — provenance

The NL1C5 result commit, official run and artifact digest must match exactly.

### C6-G2 — exact spherical invariant dictionary

The direct four-dimensional tensor definitions and their spherical expressions must agree exactly for

\[
Q=A^\mu\nabla_\mu\phi,
\qquad
Y=(g^{\mu\nu}+A^\mu A^\nu)\nabla_\mu\phi\nabla_\nu\phi,
\]

\[
F_{\mu\nu}F^{\mu\nu},
\qquad
J^\mu\nabla_\mu\phi,
\]

and the NL0B memory invariants. On the scalar-longitudinal spherical ansatz, `Y=X^2` must be recovered exactly.

### C6-G3 — full Y-family retention

For every local `x=sqrt(Y)/a0`, the generated scalar/aether source must use the frozen full `j(x)` operator for all nine co-primary cases. Automated code audit must reject a global replacement by `1/beta0`, reject a deep-MOND-only `Y^(3/2)` closure, and reject post-result interpolation selection.

### C6-G4 — spherical Einstein/AeST variational completeness

After angular reduction, independent variations with respect to

`N, b, L, R, u, phi`

must all be generated. The memory sector additionally retains every `q_j` equation and all NL1C5 direct metric sources.

On deterministic nonzero fields, automatic/component source blocks must agree with an independent action variation check to relative error `<=1e-6` for every block tested.

If an exact component block cannot be generated from the frozen action without a new physical choice, classification is `INCOMPLETE`, not PASS.

### C6-G5 — constraint structure

Before gauge fixing, lapse and shift variations must be retained as independent constraints. The generated system must exhibit the expected diffeomorphism redundancy/Noether relation numerically or symbolically. A normalized redundant-equation residual `<=1e-8` is required on deterministic smooth test fields.

No constraint may be deleted only because it is inconvenient for evolution.

### C6-G6 — FLRW recovery

Under the homogeneous FLRW specialization, the spherical equations must recover the frozen Exp background and exact zero memory background source. The NL1C5 bath must reduce to the exact `3H` cosmic-time equation. Normalized residuals must be `<=1e-10` for algebraic/background identities.

### C6-G7 — Minkowski/GR geometry control

With AeST/memory source fields set to their trivial reference values and matter absent, the spherical gravitational subsystem must admit Minkowski space

\[
N=L=1,\quad b=0,\quad R=r
\]

with normalized equation/constraint residual `<=1e-10` away from the coordinate center and a regular `r->0` limit.

### C6-G8 — published static spherical AeST control

The time-independent weak-field/quasistatic limit must reproduce the already frozen spherical AeST operator, including the NL1C1 full-Y family and the NL1C2 Helmholtz/high-gradient limit when `x>>1`.

For the NL1C2 diagnostic limit, the normalized static operator residual must be `<=1e-8` for all `beta0={1,0.5,0.1}`.

### C6-G9 — matter conservation

Pressureless matter remains minimally coupled. The reduced equations must follow from

\[
\nabla_\mu T_m^{\mu\nu}=0
\]

and reproduce the standard weak-field spherical continuity/Euler equations in the corresponding limit. No direct memory-matter force is allowed.

### C6-G10 — eta=0 identity

With memory backreaction disabled, the generated state/equation system must be exactly independent of bath initial data. Any numerical reference implementation must satisfy relative L2 state difference `<=1e-10` between the no-bath and eta=0/backreaction-off paths.

### C6-G11 — solver-readiness gate

Only after C6-G1 through C6-G10 pass may a numerical gauge be frozen. The chosen gauge must leave a closed evolution-plus-constraint system with no singular principal solve on the preregistered deterministic smooth states. If this cannot be established without an extra physical closure, classify `INCOMPLETE`.

## Forbidden shortcuts

- no GR/Poisson force substituted for the AeST closure;
- no linear CLASS `E_rhs` inserted as a spherical force;
- no memory drag law;
- no global high-gradient saturation across the entire spherical profile;
- no interpolation selection after a result;
- no finite physical eta before the eta=0/self-gravity baseline is closed;
- no collapse/turnaround/splashback statistic in C6.

## Classification

All C6-G1 through C6-G11 pass with no new physical freedom:

**NL1C6_SPHERICAL_SELF_GRAVITY_CLOSURE_PASS**

A frozen equation/variation/control is inconsistent:

**NL1C6_SPHERICAL_SELF_GRAVITY_CLOSURE_FAIL**

The covariant theory is defined, but the required gauge-fixed closed spherical component system cannot be generated without an additional theory choice:

**NL1C6_SPHERICAL_SELF_GRAVITY_CLOSURE_INCOMPLETE**

## Claim boundary and continuation

A PASS licenses a separate numerical spherical-evolution checkpoint. It still does not establish a memory-induced collapse or halo signal.

Only after PASS may NL1C7 preregister a physical spherical initial-value problem and measure turnaround/collapse/infall/splashback shifts for the frozen `tau H0` and finite physical eta values.
