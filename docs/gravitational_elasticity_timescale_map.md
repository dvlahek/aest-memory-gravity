# Gravitational elasticity — timescale map

## Purpose

The frozen Drude/Maxwell response is controlled by a dimensionless deformation-rate variable, not by tau alone.

For constant H,

`A^2=tau^2 s(s+3H)`

and

`K(A)=A/(1+A)`.

This note identifies the physical regime sampled by cosmological growth.

## 1. Growing-mode reduction

For a growing mode

`delta ~ exp[integral f H dt]`

the local growth rate is

`s=fH`.

Therefore

`A=(H tau) sqrt[f(f+3)]`.

The normalized elastic response is

`K=(H tau sqrt[f(f+3)])/[1+H tau sqrt[f(f+3)]]`.

This is the natural physical control variable for linear structure growth.

## 2. Relaxation crossover

The halfway point between relaxed and unrelaxed response is

`K=1/2`.

Because K=1/2 exactly when A=1,

`(H tau)_cross = 1/sqrt[f(f+3)]`.

Representative values:

| f | sqrt[f(f+3)] | (H tau)_cross |
|---:|---:|---:|
| 0.4 | 1.1662 | 0.8575 |
| 0.5 | 1.3229 | 0.7559 |
| 0.6 | 1.4697 | 0.6804 |
| 0.8 | 1.7436 | 0.5735 |
| 1.0 | 2.0000 | 0.5000 |

Thus for ordinary cosmological growing-mode rates the viscoelastic crossover lies around

`H tau ~ 0.5--0.9`.

The strongest distinction between relaxed and unrelaxed behavior is therefore expected for tau of order the Hubble time, not ten Hubble times.

## 3. Historical frozen tauH0=10 regime

The historical linear-memory campaigns used

`tau H0=10`

for the frozen model.

At H=H0 this gives:

| f | A at H tau=10 | K |
|---:|---:|---:|
| 0.4 | 11.6619 | 0.9210 |
| 0.5 | 13.2288 | 0.9297 |
| 0.6 | 14.6969 | 0.9363 |
| 0.8 | 17.4356 | 0.9458 |
| 1.0 | 20.0000 | 0.9524 |

Therefore the historical tauH0=10 model is already deep in the **unrelaxed elastic plateau** for a broad range of late-time growing-mode rates.

At earlier epochs H/H0>1, H tau is larger still, and K moves even closer to unity.

## 4. Consequence

This changes the physical interpretation of the old linear campaign.

The historical tauH0=10 response primarily tests the nearly frozen/unrelaxed elastic limit.

It is not an optimized test of the Maxwell relaxation crossover.

Therefore a future physics-first tau scan should center on

`tau H0 ~ 0.1--3`

with especially dense coverage around

`tau H0 ~ 0.3--1`.

This is not a fitted interval and is not inferred from observational data.

It follows directly from the analytic response law.

## 5. Suggested minimal scan

For a first clean physics map use

`tau H0 in {0.1,0.3,0.5,0.7,1.0,3.0,10.0}`.

Interpretation:

- 0.1: mostly relaxed;
- 0.3: entering the crossover;
- 0.5--1.0: primary viscoelastic transition;
- 3: mostly elastic;
- 10: historical unrelaxed control.

Keep the elastic amplitude/coupling fixed while varying tau.

Do not refit the bath independently at each tau if the same positive continuum scaling can be used.

## 6. Collapse-timescale interpretation

For a general dynamical process with characteristic rate s_dyn,

`A_dyn=tau sqrt[s_dyn(s_dyn+3H)]`.

The strongest history dependence occurs near

`A_dyn~1`.

For rapid nonlinear collapse with

`s_dyn >> H`,

this reduces approximately to

`tau s_dyn ~1`.

Thus the same theory predicts a scale/time-selective response:

- slow evolution: relaxed;
- intermediate evolution: memory dominated;
- fast evolution: elastic/frozen.

This is the clean physical signature of the model.

## 7. Immediate project implication

Before returning to nonlinear cosmological initial-data construction, the existing certified linear infrastructure should map the response across the analytic crossover in tau.

The central question is no longer simply

`is eta nonzero?`

It is

`where does tau/t_dyn place the system relative to the Maxwell crossover?`

That is the physically interpretable parameter study.
