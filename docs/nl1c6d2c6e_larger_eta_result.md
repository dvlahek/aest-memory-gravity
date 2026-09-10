# D2C6E larger-amplitude retained-eta result

Date: 2026-09-10

This note records the first frozen local output of the preregistered D2C6E larger-amplitude retained scalar-current continuation.

## Provenance

- Parent certified D2C6D run: `34507347610`, HEAD `0e596eb342e56fae56287017876fb2ee07c4c2b4`.
- D2C6E pre-data commit: `38d37b65447108a2e9ae39e991bfe3adf9f1682e`.
- Executed D2C6E code HEAD reported by output: `e51748d58c9cb43340e2ad583c5985641fa9aad6`.
- Frozen eta ladder: `eta = {0.03125, 0.0625, 0.125}`.
- Same 27 retained nonlinear completion members as D2C6B/C/D.
- Primary coverage: 27 x 3 = 81 finite-eta trajectories.
- Controls at eta=0.125: bath order 39/47, time 4096/8192, space Nx 128/256.

## Formal result

`NL1C6D2C6E_LARGER_ETA_RETAINED_SCALAR_CURRENT_PASS`

All preregistered E1-E7 gates passed.

- E1 parent/prereg provenance and exact 27x3 coverage: PASS.
- E2 finite-eta source identity: PASS. Elliptic relative L2 = `3.722320738534e-15`; increment relative L2 = `0`.
- E3 all primary and control health: PASS. All 81 primary trajectories and all 27 control bundles are healthy.
- E4 bath-order displacement convergence: PASS. Worst = `1.083471836006e-04` <= `1e-2`.
- E5 time displacement convergence: PASS. Worst = `1.521400370660e-04` <= `2e-3`.
- E6 spatial displacement convergence: PASS. Worst = `1.456214012569e-04` <= `5e-3`.
- E7 scope clean: PASS.

Maximum full canonical constraint residual over primary trajectories is approximately `1.04785e-14`. The minimum observed `1 + j_eff` is approximately `1.728865`, remaining comfortably positive.

## Non-gating nonlinear diagnostics

The maximum tangent remainder increases regularly across the dyadic eta ladder:

- eta = 0.03125: `1.321343240994e-03`
- eta = 0.0625: `2.640990574831e-03`
- eta = 0.125: `5.275205029924e-03`

The ratios are approximately 1.999 and 1.997. Since the reported quantity is the finite displacement remainder normalized by `eta * tangent`, this near-linear growth with eta is consistent with a regular leading absolute nonlinear correction of order eta^2. No field/member exceeds the preregistered diagnostic 1% visible-nonlinearity threshold, and none exceeds 5%.

The worst tangent departure occurs in the sigma=-1, beta0=0.1 sector, in E, at eta=0.125, with relative remainder about 0.5275%. Alpha and chi remain closer to the tangent prediction.

Dyadic quotient changes are also small; the largest is approximately `2.64218e-03` in E between eta=0.0625 and eta=0.125 for sigma=-1, beta0=0.1 completions.

## Interpretation

D2C6E shows that the retained scalar-current finite-memory system remains finite, healthy, and numerically converged through eta=0.125, eight times the maximum eta used in D2C6D. The finite response remains very close to the independently certified eta=0 tangent across the entire completion family. The observed departure is smooth and perturbative rather than a numerical instability.

This result strengthens the retained-sector consistency chain:

`eta=0 nonlinear base -> certified eta=0 tangent -> small finite eta D2C6D -> larger finite eta D2C6E`.

It does **not** certify the theory-complete nonlinear AeST+memory system because external metric/matter histories remain frozen, direct nonlinear memory Einstein stress is still omitted, and nonlinear matter evolution is not included. It also does not license an observational claim.

Formal output flags:

- `STILL_LARGER_RETAINED_ETA_STEP_LICENSED=True`
- `FULL_NONLINEAR_OR_OBSERVATIONAL_STEP_LICENSED=False`

The scientific priority after D2C6E should therefore be the separately preregistered theory-complete nonlinear step, rather than more debugging of the retained implementation. A still-larger retained eta scan is licensed but is secondary unless needed to map the breakdown scale of the tangent approximation.
