# Status note

This document records an exploratory shear-strain completion proposed during the physics-first reset.

It is **not the active canonical theory**.

The active theory is the already certified NL0B covariant completed-square auxiliary-vector action, reinterpreted as gravitational viscoelasticity in:

- `docs/gravitational_elasticity_canonical_nl0b_interpretation.md`;
- `docs/gravitational_maxwell_viscoelasticity.md`.

The shear-coupled construction below is retained only for provenance and possible future comparison. It must not be mixed with the frozen NL0B theory without a separate preregistered theory comparison.

---

# Gravitational Elasticity — conservative completion

## Decision

Use a conservative internal-strain sector as the fundamental model.

Do not use an intrinsically dissipative first-order relaxation law as the microscopic theory.

The existing positive fixed-frequency oscillator representation is the natural microscopic realization of gravitational elasticity.

---

## 1. Geometric deformation driver

Retain the existing unit timelike field `u^mu` of the gravitational/aether sector.

Define

`h_{mu nu}=g_{mu nu}+u_mu u_nu`.

The symmetric spatial deformation-rate tensor is

`K_{mu nu}=h_mu^a h_nu^b nabla_(a u_b)`.

Its trace is

`theta=nabla_mu u^mu`.

Its traceless part is the shear

`sigma_{mu nu}=K_{mu nu}-(theta/3)h_{mu nu}`.

The minimal elastic model couples to `sigma_{mu nu}`.

This choice is deliberate:

- an exactly homogeneous and isotropic FLRW background has `sigma_{mu nu}=0`;
- a uniform freely falling gravitational field does not create local shear;
- inhomogeneous gravity/tidal curvature generates shear through the standard congruence evolution equations;
- no background subtraction is needed.

Thus the chain is

`tidal gravity -> congruence shear -> internal strain -> elastic stress -> metric backreaction`.

---

## 2. Internal strain modes

Introduce spatial, symmetric, traceless internal strain tensors

`epsilon^(n)_{mu nu}`

satisfying

`u^mu epsilon^(n)_{mu nu}=0`

and

`h^{mu nu} epsilon^(n)_{mu nu}=0`.

Define the projected convective derivative

`D_u epsilon_{mu nu}
 =h_mu^a h_nu^b u^lambda nabla_lambda epsilon_{ab}`.

For the first model use local internal modes with no independent spatial-gradient term.

---

## 3. Conservative action

Let `S_0` denote the already validated zero-elastic-coupling gravitational sector, including the metric, existing AeST/aether variables and matter.

Add

`S = S_0 + S_el`

with

`S_el = sum_n integral d^4x sqrt(-g) [
   A_n/2 (D_u epsilon_n)_{mu nu}(D_u epsilon_n)^{mu nu}
 - A_n omega_n^2/2 epsilon^(n)_{mu nu} epsilon_n^{mu nu}
 + g_n epsilon_n^{mu nu} sigma_{mu nu}
]`.

Frozen physical sign conditions:

- `A_n>0`;
- `omega_n^2>0`.

The coupling `g_n` may have either sign, but observables after eliminating a linear mode depend on the positive spectral combination

`w_n=g_n^2/A_n>=0`.

At

`g_n=0`

the elastic sector decouples exactly.

---

## 4. Why conservation is solved at the theory level

The total action is diffeomorphism invariant when

- `g_{mu nu}`;
- `u^mu`;
- the existing gravitational fields;
- matter;
- all `epsilon_n`

are varied consistently.

Therefore the total metric equation satisfies the Noether conservation identity on the complete equations of motion.

The elastic stress tensor is not inserted phenomenologically after solving gravity.

It is

`T_el^{mu nu}= -2/sqrt(-g) delta S_el/delta g_{mu nu}`.

Consequently,

`nabla_mu(T_0^{mu nu}+T_el^{mu nu})=0`

on shell, together with the `u^mu` and strain equations.

This is the conservation closure missing from a stand-alone dissipative constitutive equation.

A full symbolic variation is still required before nonlinear implementation, but the conservation mechanism is fixed by the action rather than by a numerical prescription.

---

## 5. Strain equation

Variation with respect to a strain mode gives a projected driven oscillator.

In a local orthonormal spatial frame its leading form is

`D_u^2 epsilon^(n)_{mu nu}
 + expansion/projection terms
 + omega_n^2 epsilon^(n)_{mu nu}
 = (g_n/A_n) sigma_{mu nu}`.

In Minkowski background this is exactly

`ddot epsilon^(n)_{ij}
 + omega_n^2 epsilon^(n)_{ij}
 = (g_n/A_n) sigma_ij`.

No damping term is fundamental.

Any apparent damping in FLRW arises from expansion and energy transfer among covariant degrees of freedom.

---

## 6. Memory after eliminating the strain

For Minkowski background with retarded boundary conditions,

`epsilon_n(t)
 = (g_n/A_n) integral_{-infinity}^t
   sin[omega_n(t-t')]/omega_n
   sigma(t') dt'`.

Substituting back produces a retarded nonlocal shear response.

In frequency space,

`epsilon_n(omega)
 = (g_n/A_n)
   sigma(omega)/[omega_n^2-(omega+i0)^2]`.

The effective response kernel is

`K(omega)
 = sum_n (g_n^2/A_n)/
   [omega_n^2-(omega+i0)^2]`.

Hence the memory spectrum has non-negative weights

`w_n=g_n^2/A_n`.

This is precisely the structural reason to prefer the repository's fixed-frequency positive oscillator representation over the instantaneous H-dependent rational replacement.

---

## 7. Static elastic limit

For forcing slow compared with every active `omega_n`,

`epsilon_n ~= g_n sigma/(A_n omega_n^2)`.

The elastic sector then behaves like an additional geometric shear stiffness with total static susceptibility

`chi_el = sum_n g_n^2/(A_n omega_n^2)`.

Thus one number controls the lowest-frequency static response, while the distribution of `omega_n` controls the memory/time dependence.

---

## 8. Minimal one-mode theory

Do not start with 24 or 64 modes.

The first falsifiable model has one mode:

- frequency `omega_E`;
- coupling strength `chi_E=g_E^2/(A_E omega_E^2)`.

Choose the field normalization so `A_E=1`.

Then the independent physical parameter pair is

`(omega_E, chi_E)`.

Equivalently,

`tau_E=1/omega_E`

and `chi_E`.

The GR/AeST baseline is the exact edge

`chi_E=0`.

Only after the one-mode model is stable and observationally nontrivial should a positive multi-mode spectrum be introduced.

---

## 9. Linear cosmological reduction

Because the FLRW background shear vanishes,

`sigma_bar_{mu nu}=0`

and the background strain solution

`epsilon_bar_{mu nu}=0`

is exact.

Therefore the elastic extension begins at perturbative order and does not require retuning the homogeneous background.

For each scalar Fourier mode there is one scalar projection of the shear and one corresponding scalar projection of each strain mode.

The linear system has the form

`epsilon_n'' + Hubble terms + a^2 omega_n^2 epsilon_n
 = source_n[sigma_metric,aether]`.

The metric/aether perturbation equations acquire the variation of

`g_n epsilon_n^{mu nu} sigma_{mu nu}`.

Required coding rule:

derive these linear source terms from the quadratic action.

Do not guess an anisotropic-stress insertion by hand.

---

## 10. Weak-field spherical reduction

The same coupling gives a simple physical interpretation around a spherical source.

Tidal gravity creates differential radial/tangential deformation of the preferred congruence.

That creates

`sigma_rr - sigma_tt != 0`.

The internal strain responds to this shear and its stress modifies the radial/tangential metric equations.

The weak-field static limit must be solved before the fully nonlinear B4–B8 construction is revisited.

The required weak-field outputs are:

- regular origin;
- asymptotically decaying perturbation;
- radial strain profile;
- metric-potential correction;
- lensing-potential correction;
- exact zero-coupling recovery.

---

## 11. Immediate analytic gates

### GE1A — quadratic action

Expand

`S_0+S_el`

to second order about Minkowski and FLRW.

Identify the true scalar, vector and tensor strain components.

### GE1B — kinetic matrix

Require every propagating internal strain mode to have positive kinetic coefficient.

No ghost is allowed.

### GE1C — homogeneous spectrum

At zero external perturbation require real non-negative squared frequencies.

No exponential instability is allowed.

### GE1D — zero-coupling identity

Setting all `g_n=0` must reduce the equations exactly to the validated baseline equations.

### GE1E — fixed-frequency one-mode implementation

Only after GE1A–D pass, implement one `omega_E` strain mode in the linear cosmology code.

---

## 12. Relation to the previous repository work

The previous numerical programme is not discarded.

Its useful pieces are reclassified:

- eta=0 / zero-regression infrastructure: retained;
- linear CLASS bridge: retained;
- fixed-frequency positive oscillator bath: retained and now physically motivated;
- H-dependent instantaneous rational table: remains rejected;
- B4–B8 nonlinear spherical constraint machinery: archived as a later nonlinear-validation track;
- repeated solver/constraint repair: stopped.

The main conceptual simplification is that the memory variables are now identified with physical internal elastic strain modes.

---

## 13. Core claim

The project should be stated as:

> Inhomogeneous gravitational geometry deforms a preferred local congruence. Internal elastic degrees of freedom store that deformation and return a stress to the metric. Eliminating the internal strain produces a causal gravitational memory kernel with a positive fixed-frequency spectral representation.

This is the physics to test.
