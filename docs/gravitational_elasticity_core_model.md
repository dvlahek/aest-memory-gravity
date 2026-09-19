# Gravitational Elasticity — physics-first core model

## Purpose

The central physical idea is simple:

> gravity produces tidal deformation; the deformation is stored as an elastic strain; the resulting elastic stress backreacts on gravity.

The nonlinear B4–B8 spherical-constraint programme is retained as a historical validation track, but it is no longer the primary route to establish the model.

The primary route is now:

1. define gravitationally driven strain;
2. derive its causal memory response;
3. couple the elastic stress to the standard gravitational field equations;
4. validate the linear and weak-field limits;
5. only then return to the fully nonlinear spherical problem.

No post-hoc reinterpretation of B4–B8 is made.

---

## 1. Physical principle

A locally uniform gravitational acceleration can be removed in a freely falling frame.

Therefore the quantity that can physically deform an elastic medium is not a coordinate acceleration `g_i`, but the tidal gravitational field.

With a preferred unit timelike field `u^mu` already available in the AeST framework, define the spatial projector

`h_{mu nu}=g_{mu nu}+u_mu u_nu`.

Define the covariant tidal tensor

`T_{mu nu}=h_mu^a h_nu^b R_{a c b d} u^c u^d`.

It is spatial and symmetric.

In the Newtonian weak-field limit,

`T_ij -> partial_i partial_j Phi`.

Thus the construction respects the equivalence-principle statement that only gravitational gradients produce local relative deformation.

---

## 2. Internal elastic strain

Introduce a spatial symmetric strain tensor `E_{mu nu}` satisfying

`u^mu E_{mu nu}=0`.

For the minimal causal model use the projected convected derivative

`D_u E_{mu nu}=h_mu^a h_nu^b L_u E_{ab}`.

The single-relaxation constitutive equation is

`tau D_u E_{mu nu}+E_{mu nu}=alpha tau^2 T_{mu nu}`.

Parameters:

- `tau>0`: memory / relaxation time;
- `alpha`: dimensionless gravitational compliance.

The GR limit is `alpha=0`.

The instantaneous-elastic limit is approached when the forcing changes slowly compared with `tau`:

`E_{mu nu} ~= alpha tau^2 T_{mu nu}`.

---

## 3. Memory is not added by hand

For vanishing initial transient, the constitutive equation has the exact retarded solution

`E_{mu nu}(t)=alpha tau integral_{-infinity}^t exp[-(t-t')/tau] T_{mu nu}(t') dt'`

along the preferred congruence.

Thus the gravitational response depends on the past tidal field.

The memory kernel is

`K(Delta t)=alpha tau exp(-Delta t/tau) Theta(Delta t)`.

This is the simplest member of the positive memory family already explored numerically in the repository.

A multi-timescale model is obtained only after the one-timescale model is validated:

`E=sum_n E_n`

with positive weights and fixed relaxation/oscillator scales.

The existing fixed-frequency positive-bath work is therefore reinterpreted as a possible microscopic/conservative realization of the constitutive kernel, not as the starting point of the physics argument.

---

## 4. Elastic stress

Decompose the strain into trace and traceless pieces:

`E = h^{mu nu} E_{mu nu}`

and

`E^TF_{mu nu}=E_{mu nu}-(E/3)h_{mu nu}`.

The minimal isotropic elastic stress is

`Pi_{mu nu}=K_E E h_{mu nu}+2 mu_E E^TF_{mu nu}`

with

- bulk modulus `K_E>=0`;
- shear modulus `mu_E>=0`.

The elastic contribution enters the gravitational equations through a conserved total stress tensor.

The core phenomenological statement is

`G_{mu nu}=8 pi G (T^matter_{mu nu}+T^elastic_{mu nu})`.

A fully local conservative completion must supply the energy-density and energy-flux pieces required by `nabla_mu T_total^{mu nu}=0`.

Until that completion is written, only linear combinations whose conservation closure is explicit may be implemented.

This is an explicit theory boundary, not a numerical issue.

---

## 5. Minimal scalar cosmological sector

For the first falsifiable implementation, do not evolve the full tensor.

Use the scalar tidal amplitude built from the gauge-invariant Weyl/Bardeen potential

`Phi_W=(Phi+Psi)/2`.

Define

`T_k=-(k^2/a^2) Phi_W`.

Introduce one dimensionless scalar strain `s_k`:

`dot s_k + s_k/tau = alpha tau T_k`.

Its exact retarded solution is

`s_k(t)=alpha tau integral^t exp[-(t-t')/tau] T_k(t') dt'`.

Let the scalar elastic anisotropic stress amplitude be

`Pi^el_k = M_E s_k`

with `M_E>=0`.

This stress enters the standard traceless spatial Einstein equation.

No modified Poisson equation is postulated independently.

Matter remains minimally coupled and follows the standard conservation equations.

Therefore all changes to growth and lensing occur through the self-consistent metric response to `Pi^el_k`.

### Zero-coupling gate

For

`alpha M_E=0`

the model must reproduce the GR/LambdaCDM baseline exactly.

### Small-coupling gate

For small

`g_E = 8 pi G M_E alpha tau^2`

all observable changes must be linear in `g_E` before any finite-coupling interpretation.

---

## 6. Static spherical weak-field limit

For

`ds^2=-(1+2 Psi)dt^2+(1-2 Phi)delta_ij dx^i dx^j`

the Newtonian tidal tensor is

`T_ij=partial_i partial_j Phi`.

For a spherical potential `Phi(r)`, the independent shear-driving tidal amplitude is

`T_s = Phi''-Phi'/r`.

The static strain is

`s(r)=alpha tau^2 [Phi''(r)-Phi'(r)/r]`.

The elastic radial/tangential stress difference is proportional to

`Pi_r-Pi_t = 2 mu_E s(r)`.

This gives a direct weak-field prediction:

- no response to a uniform field;
- no shear response in an exactly homogeneous FLRW background;
- a nonzero response around an inhomogeneous gravitating source;
- the sign and scale dependence are fixed by the tidal field and the positive elastic modulus.

The first spherical calculation should use this weak-field system.

It should not start from the fully nonlinear B4–B8 initial-data machinery.

---

## 7. What must be derived before further large numerics

### GE1 — conservation closure

Construct a local covariant completion, or an explicitly conservative auxiliary-state realization, for the elastic sector.

Required output:

`nabla_mu (T_matter^{mu nu}+T_elastic^{mu nu})=0`

identically on the auxiliary equations of motion.

A dissipative single-`tau` constitutive law may be retained as an effective limit only if its energy sink/reservoir is represented explicitly.

### GE2 — linear stability and passivity

Around FLRW and Minkowski require:

- no ghost kinetic sign;
- no exponentially growing mode in the zero-source homogeneous system;
- causal retarded response;
- non-negative spectral weights in any bath representation;
- exact GR recovery at zero coupling.

### GE3 — one-state CLASS proof

Before any multi-mode bath:

- one scalar strain state per `k`;
- exact zero regression;
- small-coupling tangent linearity;
- resolution convergence;
- lensing and growth outputs.

Only if this passes should the positive fixed-frequency bath be restored.

### GE4 — weak-field spherical proof

Solve the linear/static spherical equations sourced by a smooth density profile.

Test:

- regular center;
- asymptotic decay;
- no free post-hoc boundary shift;
- convergence under radial refinement.

Only after GE1–GE4 pass is there a reason to return to a fully nonlinear spherical constraint construction.

---

## 8. What is no longer the main problem

The immediate scientific question is not

> can a particular frozen `(L,R_t)` projection pass a `1e-7` discrete nonlinear constraint gate?

The immediate scientific question is

> does a causal, stable, conservative gravitationally driven elastic strain produce a distinct and testable metric response while reducing exactly to GR at zero coupling?

B4–B8 remain useful numerical evidence about one nonlinear representation.

They do not define the gravitational-elasticity idea.

---

## 9. Minimal falsifiable parameter set

Start with only

- `tau`: memory time;
- `g_E`: overall elastic gravitational coupling.

Do not fit separate bulk/shear spectra initially.

For the first scalar cosmology test, absorb `alpha M_E` into `g_E`.

A successful first model must therefore produce a two-dimensional response surface

`observable = observable(tau, g_E)`

with an exact GR edge at `g_E=0`.

---

## 10. Immediate project decision

Freeze B4–B8 as the nonlinear exploratory track.

Do not spend further time tuning its discretization.

The active physics-first sequence is now:

`GE1 conservation -> GE2 stability -> GE3 linear cosmology -> GE4 weak-field sphere -> nonlinear return only if justified`.

The conceptual statement of the project is:

> Gravitational curvature acts as the deformation driver of an elastic internal state. The state stores a causal memory of past tidal gravity and returns an elastic stress that backreacts on the metric.
