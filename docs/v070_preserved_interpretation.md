# Preserved interpretation of v0.70

This note is result-informed and was added after completion of v0.70. It does not alter, relabel, rerun, or rescue the historical v0.70 classification.

## Historical classification retained unchanged

- v0.70: `V070_BROADBAND_NONLINEAR_ONSET_TANGENT_FAIL`

The FAIL remains authoritative for the preregistered v0.70 estimator and numerical gates.

## What v0.70 established

The broadband construction removed the dominant grid-branch pathology seen in v0.69. The baseline crossing-resolution audit passed with a maximum relative difference of about 8.29e-4, the implicit-shift fine/coarse normalized RMS passed at about 4.67e-2, all spectra and threshold crossings were finite, and the minimum absolute broadband log-slope was far above the preregistered floor.

The sole failed primary gate was the four-lambda affinity of the implicit shift: the maximum normalized RMS was about 0.147 versus the preregistered limit 0.05. Therefore no v0.70 delay/advance label is promoted.

Descriptively, the order-unity broadband threshold shift was positive at 5/7 redshifts for W=0.1 and 6/7 for W=0.2, with sign agreement between widths at 6/7 redshifts. These facts are retained only as motivation for a new estimator-level follow-up.

## Estimator issue identified after the result

v0.70 preregistered

`[ln Dbar(+lambda)-ln Dbar(-lambda)]/(2 lambda)`

as the finite-lambda estimator of `partial_eta ln Dbar` at eta=0. For an affine perturbation-state response, the power and hence the arithmetic broadband power are generically quadratic in lambda,

`Dbar(lambda)=A + lambda B + lambda^2 C`.

The centered derivative of Dbar itself,

`[Dbar(+lambda)-Dbar(-lambda)]/(2 lambda)`,

recovers the eta=0 odd coefficient exactly under that affine-state hypothesis, whereas the centered derivative of `ln Dbar` contains intrinsic O(lambda^2) terms. Thus the v0.70 lambda-affinity failure can include estimator nonlinearity even when the underlying odd tangent is well behaved.

A later version may test the mathematically corresponding eta=0 tangent

`partial_eta ln Dbar|0 = ([Dbar(+lambda)-Dbar(-lambda)]/(2 lambda))/Dbar(0)`

at the same frozen baseline broadband crossings. Such a follow-up must be preregistered as result-informed and must leave the v0.70 FAIL unchanged.
