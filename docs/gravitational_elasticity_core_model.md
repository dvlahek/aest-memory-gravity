# Gravitational Elasticity — canonical core model

## Status

This document states the active physics interpretation after consolidation with the already certified NL0B covariant memory completion.

The active theory is the frozen NL0B auxiliary-vector action.

Earlier exploratory language based on a directly tidal-tensor-driven strain is not the canonical model and must not be mixed with NL0B without a separate theory comparison.

## 1. Central idea

The project is based on one simple mechanism:

> gravity changes a covariant deformation variable; internal elastic modes cannot follow that change instantaneously; the resulting mismatch stores energy and returns a restoring force to the gravitational sector.

In the frozen AeST completion, the deformation driver is

`X_mu=h_mu^nu nabla_nu phi`

with

`h_mu nu=g_mu nu+A_mu A_nu`.

On homogeneous FLRW,

`X_mu=0`.

For scalar perturbations,

`X_hat{i}=(1/a) partial_i chi`

with the already certified AeST variable

`chi=varphi+Q alpha=Q(u_A+alpha)`.

Thus the elastic sector is driven by spatially inhomogeneous gravitational/AeST structure and vanishes on the homogeneous background.

## 2. Internal elastic coordinates

For each positive mode introduce an aether-orthogonal internal coordinate

`A^mu U_{j mu}=0`.

The projected derivative along the aether is

`D_A U_{j mu}=h_mu^nu A^rho nabla_rho U_{j nu}`.

The frozen conservative action is

`S_mem=(16 pi Gtilde)^(-1) integral d4x sqrt(-g) (1/4) sum_j [
 |D_A U_j|^2
 - |omega_j U_j-sqrt(eta w_j)X|^2
]`.

with

`omega_j>0, w_j>0, eta>=0`.

This action already passed NL0B.

## 3. Elastic strain

Define the elastic mismatch

`e_{j mu}=sqrt(eta w_j)X_mu-omega_j U_{j mu}`.

The stored potential energy of the internal mode is proportional to

`|e_j|^2/4`.

This is the strain variable in the mechanical interpretation.

A change in gravity changes X immediately.

U is dynamical and remains continuous.

Therefore e becomes nonzero and generates a restoring force.

## 4. Restoring stress / force

Write

`U_j=sqrt(eta) q_j`.

The normalized backreaction is

`B_mu=sum_j [w_j X_mu-omega_j sqrt(w_j)q_{j mu}]`.

Algebraically,

`B_mu=(1/sqrt(eta)) sum_j sqrt(w_j)e_{j mu}`

for eta>0, with a regular normalized eta->0 limit.

The already certified scalar AeST closure

`Delta E_rhs=-(eta Q/2) B_chi,raw`

is therefore the scalar projection of the elastic restoring force.

## 5. Why this is memory

The internal coordinates obey oscillator equations.

On FLRW,

`ddot q_j+3H dot q_j+omega_j^2 q_j
 =omega_j sqrt(w_j) X`.

Their present value depends on the past history of X.

Eliminating q therefore gives a retarded nonlocal response for B.

Memory is not added phenomenologically.

It is the effective description obtained after internal elastic coordinates are eliminated.

## 6. Maxwell limit

The positive Drude continuum already frozen in the project gives

`K(A)=A/(1+A)`

with

`A^2=tau^2 s(s+3H)`.

At H=0,

`A=tau s`

on the causal branch, hence

`B/X=tau s/(1+tau s)`.

Therefore

`tau dot B+B=tau dot X`.

This is the Maxwell viscoelastic constitutive law.

The model is therefore most cleanly described as **gravitational Maxwell viscoelasticity with a conservative microscopic bath**.

## 7. Physical regimes

### Slow gravity

If the gravitational deformation changes on a timescale much longer than tau,

`Omega tau <<1`,

the internal sector follows it and the restoring mismatch is small.

### Memory regime

For

`Omega tau ~1`,

the phase lag is largest and the history dependence is strongest.

### Fast gravity

For

`Omega tau >>1`,

the internal state cannot follow quickly and the response approaches the unrelaxed elastic limit.

## 8. Static versus dynamic gravity

The memory sector has

`K(0)=0`.

Thus it does not create a permanent extra static force after complete relaxation.

Static modified-gravity behavior remains in the AeST Y-sector.

The active physical division is:

- AeST Y-sector: static/gradient-dependent response;
- NL0B elastic bath: time/history-dependent response.

This separation is useful because it prevents the memory parameter tau from being misused as a static MOND fitting parameter.

## 9. Existing theory status

The relevant successful chain is already:

- NL0B covariant memory completion: PASS;
- NL0C weakly nonlinear Y-sector: PASS;
- NL1A pseudospectral Y-operator bridge: PASS;
- NL1B2 directional second-order eta tangent: PASS;
- NL1C5 spherical variational bridge: PASS;
- NL1C6 spherical self-gravity closure: PASS;
- v0.77 native-state tangent affinity: PASS;
- v0.78 time-interpolation closure: PASS.

Therefore the theory and its controlled linear response are not waiting for B4-B8.

## 10. Meaning of the B4-B8 failure

B4-B8 attempted one specific nonlinear cosmological/spherical initial-data construction.

That route became dominated by constraint discretization and boundary representation.

Its failures do not invalidate the frozen covariant elastic action.

No further B4-B8 solver tuning belongs to the active programme.

## 11. Next physical question

The main question is now

> For which gravitational evolution timescales does tau/t_dyn become order unity, and what observable growth/lensing/collapse response follows from the already certified elastic action?

This can first be answered in linear and weak-field dynamical regimes.

There is no reason to solve the full nonlinear cosmological initial-data problem before that question is answered.

## 12. Compact project statement

> Spatially inhomogeneous gravity drives internal covariant deformation modes. Their delayed response stores elastic energy and returns a restoring force to the gravitational sector. A positive conservative bath reduces macroscopically to a Maxwell-type gravitational viscoelastic memory law.
