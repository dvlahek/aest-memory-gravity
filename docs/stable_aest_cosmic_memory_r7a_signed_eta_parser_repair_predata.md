# Stable AeST cosmic-memory R7a — signed-eta parser repair pre-data note

Date: 2026-09-15
Branch: `fullj-evolving-weyl-bridge`

## Status of the first R7a attempt

The first R7a execution did not produce a complete scientific diagnostic. It returned

`STABLE_AEST_COSMIC_MEMORY_R7A_RUN_FAIL`

because every preregistered negative-eta worker was rejected by the frozen AeST CLASS input parser before cosmological integration with

`AeST memory requires aest_eta >= 0`.

The positive-eta and eta=0 workers that ran before/around those parser failures are not interpreted as a scientific R7a result. The failed attempt is not reclassified.

## Cause

R7a preregistered a symmetric local derivative using `eta = +/-0.025` and a full-mode amplitude-control pair `eta = +/-0.05`. The physical perturbation equations themselves multiply the memory feedback by `aest_eta`, but the frozen parent input parser contains a domain guard that forbids `aest_eta < 0`.

Therefore the negative-side runs were blocked at parameter parsing. This is an interface/domain restriction, not a finite-run physics failure.

## Frozen repair

Before any complete R7a result, the disposable R7a CLASS source will be modified only so that the existing parser guard `aest_eta >= 0` is disabled for the R7a diagnostic build. The perturbation equations, memory bath evolution, epoch windows, stable-chi patch, initialization, tolerances, observables, eta magnitudes, redshift bins, classification logic, and all preregistered numerical thresholds remain unchanged.

The signed continuation is diagnostic only. It is used to estimate the derivative at eta=0 by a symmetric finite difference. It does not license negative physical eta as part of the model parameter domain or any observational claim at eta<0.

The repaired source must audit all of the following before execution:

- the frozen parent contains exactly one parser message `AeST memory requires aest_eta >= 0`,
- the corresponding `pba->aest_eta < 0.` parser condition is neutralized exactly once in the disposable R7a tree,
- the physical feedback still contains exactly one live windowed multiplier `Bchi_aest *= pba->aest_eta*aest_r7a_epoch_weight(a);`,
- no R2d trace hook is present,
- no external replay hook is present,
- all original R7a science constants and gate thresholds are unchanged.

If any source-level audit fails, the repaired run is invalid and no scientific interpretation is made.
