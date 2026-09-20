# GE14 chi-cancellation stiff-seed audit — result freeze

## Status

Frozen first locked GE14 execution.

Terminal classification:

`GE14_CHI_CANCELLATION_STIFF_SEED_LOCALIZED`.

GitHub Actions run:

`35502859300`.

Execution HEAD:

`61d75feb043d35367452531f0994fc8af81d9519`.

Artifact:

- ID: `10602359904`;
- name: `results_bundle_ge14_chi_cancellation_stiff_seed`;
- ZIP SHA-256:
  `af145139d6c8f64a54f3052e218dff50bc170d250adf6d8e2f91937397cc7775`.

## Frozen output hashes

Result JSON:

- bytes: `16059`;
- SHA-256:
  `50f08e5718e7b6e640bff618fa5bce08c6fcfb020d14353918fc644d616c36f7`.

Result log:

- bytes: `16059`;
- SHA-256:
  `50f08e5718e7b6e640bff618fa5bce08c6fcfb020d14353918fc644d616c36f7`.

Parent metadata JSON:

- bytes: `852`;
- SHA-256:
  `9e41662bc3b62d1717815e5f962fc6600057d86971be78db185be77e6879720e`.

## Gate result

Every locked GE14 gate passes.

Across both R1 and R2 and all six frozen k modes:

- the initial residual
  `s=a theta/k^2+alpha`
  is at most
  `6.095146620860508`
  double-precision machine-epsilon units relative to the cancelling terms;
- the stiff contribution
  `(a/KB) KQ chi`
  reproduces the full traced `E'` with worst relative error
  `7.786404330202369e-8`;
- the complete analytic E-prime reconstruction agrees with the trace to
  `3.697785493223493e-32`
  abs-or-rel error.

## Physical finite-gradient source versus roundoff seed

At the same first accepted endpoints, the direct finite-gradient source

`-(a/KB)(2-KB)Q cad2[delta/(1+w)-3H alpha]`

is only

`3.38824324053177e-10 -- 5.13783517211051e-9`

of the cancellation-induced stiff `KQ chi` term.

Therefore the first nonzero E derivative in the frozen R1/R2 histories is overwhelmingly controlled by floating-point cancellation in the recovered chi variable, not by the physical finite-gradient source.

## Mechanism

The historical state representation evolves `alpha` and `theta` separately and reconstructs

`chi=Q(a theta/k^2+alpha)`.

The leading adiabatic initial condition enforces

`alpha=-a theta/k^2`.

At the first accepted endpoint each cancelling term is typically
`O(1e-7--1e-5)`,
while their residual is only
`O(1e-23--1e-21)`.

That residual is ordinary double-precision cancellation noise.

The Exp background simultaneously has very large early-time `KQ`.

The E equation contains

`(a/KB)KQ chi`.

Consequently a few machine-epsilon units in the reconstructed adiabatic cancellation generate the dominant initial E derivative.

The sign and amplitude of this seed differ between R1 and R2.

Together with GE13, which shows later growth into a fixed per-k amplitude mode, this supplies a concrete numerical mechanism for the observed precision bifurcation.

## Cancellation-free exact state variable

Define

`s = a theta/k^2 + alpha = chi/Q`.

Then

`alpha=s-a theta/k^2`

and

`chi=Q s`

without subtracting two independently evolved near-equal variables.

Using the exact background identity

`Q'/Q=-3 cad2 (aH)`,

the eta=0 linear system gives

`s' = a[E+Pi/(1+w)] + 3 cad2 (aH)(a theta/k^2)`.

The E equation remains

`E' = a/KB[KQ chi-(2-KB)(Q Pi/(1+w)+(H+Q)chi-3 cad2 H Q alpha)]-(aH)E`

with `chi=Qs` and
`alpha=s-a theta/k^2`.

This is an exact change of variables, not a modified physical model.

## Consequence for the finite-gradient IC programme

The omitted physical finite-gradient source remains real.

However GE14 establishes that, in the historical alpha representation, it is initially many orders of magnitude below the cancellation-induced stiff seed.

Therefore deriving a more accurate `O((k/H)^2)` IC while retaining the same cancellation-prone state representation would not address the dominant numerical pathology.

The correct order of operations is:

1. implement the exact cancellation-free `s=chi/Q` state;
2. validate R1/R2 precision closure using the same physical equations;
3. only if a residual precision bifurcation remains, derive and test the finite-gradient regular IC completion.

## Licensed continuation

A separately preregistered state-reparameterization test may replace the internal AeST alpha state by the exact variable

`s=chi/Q`

while reconstructing physical alpha algebraically.

It must not:

- change the physical equations;
- change KB or the Exp background;
- change R1/R2 numerical precision values;
- relax the historical cross-level local-jet thresholds;
- introduce finite eta.

The primary question is if the R1/R2 per-k amplitude bifurcation disappears when the cancellation is removed at the variable level.

## Claim boundary

GE14 localizes the initial numerical seed.

It does not retroactively relabel GE11 or prove that every later deviation is numerical.

It does, however, identify a concrete representation pathology that must be removed before interpreting the R1/R2 bifurcation physically.
