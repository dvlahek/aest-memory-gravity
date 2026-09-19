# NL1C7B5 Repair01 — pre-data analytic regular-center source limit

## Status

Pre-data / pre-implementation implementation-repair preregistration.

Parent frozen result:

`NL1C7B5_CONSERVATIVE_INITIAL_DATA_IMPLEMENTATION_FAIL`.

Parent execution HEAD:

`7806749a5d28c63887cd0207e366e858cdaf8c99`.

Parent result-freeze commit:

`0c7c6fcc736c2f218b5704d2c6676a20c7944861`.

Parent result JSON SHA-256:

`6f59e45621d4895ee8fbb4ce125943fcd2939a534a7266fbebae4759190f79bc`.

Repair01 is an implementation-only regular-center representation completion.

It is not a new conservative formulation, not a solver repair and not a change to the frozen physical model.

## Failure being repaired

The first locked B5 run passed:

- frozen provenance;
- source/flux differential decomposition identity;
- orthonormal gauge basis;
- output integrity;
- claim boundary.

All six nonlinear constructions then failed before the first solver step with

`ValueError: Residuals are not finite in the initial point.`

The raw lambdified spherical source expressions contain removable `0/0` forms at the analytic center `r=0`.

The historical differential B4 evaluator never requires the raw center source to be finite as a science point.

The conservative cell quadrature does require a finite center source because the first nine-node cell stencils include node zero.

## Frozen analytic center rule

For the regular spherical states used in NL1C7B5:

- `R(0)=0`;
- `R_t(0)=0`;
- `L_r(0)=0`;
- scalar quantities remain finite;
- radial fluxes vanish at the center.

The frozen total local source limits are therefore

`S_H(0)=0`

and

`S_M(0)=0`.

Repair01 implements exactly those two assignments after assembling the total source arrays.

It also retains the already frozen flux assignments

`F_H(0)=0`

and

`F_M(0)=0`.

No extrapolation, fitted center value, smoothing or additional stencil is permitted.

## Frozen noncenter identity

Every source and flux value at indices `i>=1` must remain bitwise unchanged relative to the parent B5 implementation for the same trial state.

The existing B5 decomposition test against the original differential B4 numerators remains unchanged and must pass on all noncenter points.

## Frozen B5 construction

Everything else remains exactly as preregistered and locked in NL1C7B5:

- eta=0;
- Simple, beta=1;
- same six scale/grid cases;
- same density-Q-completed parents;
- same physical variables `(L,R_t)`;
- same `Y4=0,Qmean=0` orthonormal basis;
- same degree-8 nine-node conservative cell quadrature;
- same parent-based normalization;
- same `3-point, abs_step=3e-6` Jacobian;
- same half-band 16 sparsity;
- same TRF nonlinear driver;
- same tolerances;
- same `max_nfev=200`;
- same start `z=0`;
- same safety bounds;
- same original differential `1e-7` science certification;
- same two-grid control;
- same NPZ output rule.

No new numerical candidate is introduced.

## Additional Repair01 integrity check

Before calling `scipy.optimize.least_squares`, explicitly evaluate the conservative residual at `z=0`.

Require all residual components finite.

If any component remains nonfinite after the analytic center assignments, classify the run as implementation failure and do not invoke the nonlinear driver for that case.

Record the initial conservative residual finiteness for all six cases.

## Allowed terminal interpretation

If the regular-center repair allows all six constructions to execute, the resulting science classification is determined by the already frozen B5 gates.

Repair01 does not add or relax any science PASS criterion.

The original first B5 run remains permanently frozen as

`NL1C7B5_CONSERVATIVE_INITIAL_DATA_IMPLEMENTATION_FAIL`.

If Repair01 itself still encounters a pre-solver implementation failure, no second center-representation repair is licensed without a new project-level decision.
