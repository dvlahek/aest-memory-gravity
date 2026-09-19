# Gravitational Maxwell viscoelasticity

## Core result

The already certified positive Drude memory kernel has a direct mechanical interpretation.

It is the response kernel of a Maxwell-type viscoelastic gravitational medium.

This is not a new fitted model. It is a reinterpretation of the frozen NL0B/NL0C memory theory.

## 1. Deformation and restoring stress

The geometric deformation driver is

`X_mu=h_mu^nu nabla_nu phi`.

The normalized elastic backreaction is

`B_mu=sum_j [w_j X_mu-omega_j sqrt(w_j) q_{j mu}]`.

The frozen AeST memory force is proportional to B.

Thus use the mechanical dictionary

- gravitational deformation: `X_mu`;
- internal material coordinate: `q_j`;
- elastic mismatch: `sqrt(w_j)X_mu-omega_j q_{j mu}`;
- restoring stress/force: `B_mu`;
- physical memory coupling: `eta`.

The exact NL0B action supplies the conservative microscopic realization.

## 2. Continuum Drude response

The preserved positive bath gives

`K(A)=A/(1+A)`

with

`A^2=tau^2 s(s+3H)`.

The normalized restoring response is

`B(s)=K(A)X(s)`.

At H=0 and on the causal Laplace branch,

`A=tau s`.

Therefore

`B(s)/X(s)=tau s/(1+tau s)`.

Equivalently,

`(1+tau s)B=tau s X`.

In the time domain,

`tau dB/dt + B = tau dX/dt`.

This is the Maxwell stress-relaxation equation.

## 3. Step deformation

Let

`X(t)=X0 Theta(t)`

with a relaxed past state.

Then

`B(t)=X0 exp(-t/tau) Theta(t)`.

Immediately after the gravitational deformation changes,

`B(0+)=X0`.

The internal sector initially behaves elastically.

If the deformation is held fixed,

`B(t)->0`.

The stored stress relaxes as the internal modes rearrange.

This explains why the model has memory without an additional permanent static force.

## 4. Harmonic response

For

`X(t)=Re[X0 exp(i Omega t)]`,

the normalized complex modulus is

`G*(Omega)=B/X=i Omega tau/(1+i Omega tau)`.

Hence

`G'= (Omega tau)^2/[1+(Omega tau)^2]`

and

`G''= Omega tau/[1+(Omega tau)^2]`.

Interpretation:

- `Omega tau <<1`: relaxed/soft response;
- `Omega tau~1`: strongest phase-lag/memory regime;
- `Omega tau>>1`: unrelaxed elastic response.

The loss component peaks at

`Omega tau=1`.

The peak value is

`G''=1/2`.

This gives a clean physical meaning to tau: it selects the gravitational timescale at which memory is strongest.

## 5. Hubble-dressed response

On a constant-H FLRW background,

`A=tau sqrt[s(s+3H)]`.

Therefore

`B/X=A/(1+A)`.

Expansion changes the relation between temporal frequency and the internal viscoelastic response but does not change the positive Drude kernel itself.

The natural cosmological control variables are therefore

- `Omega tau`;
- `H tau`.

This is more transparent than treating tau only as a numerical bath parameter.

## 6. Microscopic conservative origin

A Maxwell equation is dissipative when written as a single effective constitutive equation.

The NL0B theory does not postulate microscopic dissipation.

Its positive fixed-frequency auxiliary oscillators form a conservative bath.

The apparent stress relaxation of the continuum response arises from energy transfer/dephasing into those internal modes, plus Hubble dilution in cosmology.

Thus:

`conservative internal elastic modes -> effective viscoelastic memory`.

This is exactly the type of microscopic-to-effective relation desired for the project.

## 7. Static-gravity consequence

Because

`K(0)=0`,

the memory sector produces no permanent restoring force after complete relaxation to a strictly static deformation.

Therefore the memory sector by itself is not intended to replace dark matter through an additional static force law.

Static modified-gravity behavior remains in the frozen AeST Y-sector.

The division of labor is:

- AeST Y-sector: static/gradient-dependent gravitational response;
- elastic memory sector: history/rate-dependent gravitational response.

This sharply separates the two physical mechanisms.

## 8. Structure-formation prediction

During gravitational collapse the deformation X changes with time.

The elastic stress B therefore does not vanish.

For a collapse timescale

`t_dyn`,

the strongest memory modification is expected parametrically near

`tau ~ t_dyn`.

If

`tau << t_dyn`,

the medium relaxes almost instantaneously and the memory force is small.

If

`tau >> t_dyn`,

the internal state is effectively frozen and the response approaches its unrelaxed elastic limit.

This identifies the clean nonlinear observable:

> compare collapse/growth histories as a function of the ratio tau/t_dyn.

No arbitrary new force law is required.

## 9. Relation to certified linear results

The v0.77 native-state tangent PASS and v0.78 interpolation-closure PASS already certify the linear response of this same frozen memory theory.

Therefore those results can now be described as the linear response of a gravitational Maxwell material, subject to the same explicit claim boundaries retained in their original result freezes.

No historical classification is changed.

## 10. Paper-level conceptual statement

A compact statement of the model is:

> Gravity drives a covariant deformation variable in the AeST sector. A positive spectrum of conservative internal modes stores that deformation. After the internal modes are eliminated, the gravitational restoring response obeys a Maxwell-type viscoelastic memory law, with relaxation time tau and an exact zero-memory limit.

This is the simplest physical interpretation of the existing theory.
