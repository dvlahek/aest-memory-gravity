# NL1C7B eta=0 spherical constraint track — history

Last updated: 2026-09-19

This file is the persistent project history for the nonlinear eta=0 spherical initial-data track on branch

`nl1c7b-eta0-spherical-evolution`.

It records scientific classifications exactly as obtained. A failed or implementation-failed repair is never relabelled after the fact.

## Current checkpoint

The linear gauge-fixed `(L,R_t)` problem remains certified feasible from Repair19b1, but the first locked nonlinear direct Gauss-Newton closure attempt has now failed scientifically.

Latest completed nonlinear checkpoint:

`NL1C7B4_REPAIR19C_ORTHONORMAL_DIRECT_GN_NONLINEAR_CLOSURE_FAIL`

with

- `SCIENCE_RC=2`
- execution HEAD:
  `2d59ebeef39bc2c4936eb3d6a465da25cc9613cf`
- result JSON SHA-256:
  `5ad02254c512f90d0f82a42d0f5aa00f15c1dae6248bdbe7ad69addb183b600a`
- canonical PASS:
  `0/24`
- lambda=1 PASS:
  `0/6`
- no state NPZ written.

Repair19c preserves exact provenance, the orthonormal gauge, parent reproduction, the certified Repair19b1 first step, two-grid control, field freeze, output integrity and the claim boundary.

The failed science gates are exact canonical nonlinear closure, one marginal small-lambda scaling path, and the downstream branch-retest gate.

The central new result is that the first direct GELSY linear step predicts residuals near `1e-11` to `1e-9`, but exact nonlinear evaluation of that same physical step leaves residuals around `1e-2` to `1` depending on scale/grid. The mismatch is approximately `1e7-1e9` at lambda=1.

Hamiltonian closure becomes very small in the final lambda=1 states, while momentum remains above the historical `1e-7` threshold.

The physical correction amplitude remains grid-stable, with lambda=1 Nr512/Nr256 ratios near `1.003` for all three scales.

### Next executable gate

Repair19c1 is preregistered, implemented, implementation-locked, and runner-ready.

It is a diagnostic only:

`NL1C7B4_REPAIR19C1_FIRST_STEP_DIRECTIONAL_JACOBIAN_FIDELITY_CHARACTERIZED`

is the successful characterization class.

Repair19c1 reproduces the same six lambda=1 first GELSY directions and evaluates the exact residual along

`alpha = 1 ... 1/4096`.

It measures:

- exact versus linear-predicted residual;
- nonlinear remainder scaling;
- directional derivative mismatch;
- Hamiltonian and momentum blocks separately;
- exact Q and gauge preservation;
- field freeze.

It does not run a new nonlinear optimizer or change the physical ansatz.

The purpose is to distinguish genuine nonlinear curvature from loss of finite-difference/local-Jacobian fidelity before any solver repair is proposed.

---

## Historical checkpoints

### C7A — certified growing-mode spherical bridge

Certified class:

`NL1C7A_REPAIR01_DENSE_TIME_SPHERICAL_BRIDGE_CERTIFIED`.

Key role:

- establishes the eta=0 linear spherical bridge;
- supplies the frozen dense trace and reconstruction identities later inherited by NL1C7B.

Official final run:

- run `35183893359`
- artifact `10481526695`
- digest `c2ede2e602e35bbd52afdc0a5eee22cb1bf5c6efc2e1063bf8f2b91a0554fb6c`.

### Repair08 — identity-preserving scalar representation

Certified class:

`NL1C7A_REPAIR08_IDENTITY_PRESERVING_SCALAR_REPRESENTATION_CERTIFIED`.

Frozen representation:

`varphi(k,a_i)=PCHIP(log a, a Q theta_A/k^2)(log a_i)`.

Freeze commit:

`6a8812f9b8d9f4fa373212376b6c01b4649076aa`.

### Repair09 — raw exact nonlinear B4 retest

Class:

`NL1C7B4_REPAIR09_REPAIR08_RAW_CONSTRAINT_FAIL`.

Result:

- 0/54 cases pass historical `1e-7`;
- Hamiltonian residual at roughly `1e-6` to `1e-4`;
- momentum residual near unity.

Interpretation:

the certified linear representation does not by itself satisfy the exact nonlinear B4 constraints.

### Repair10 — source localization

Class:

`NL1C7B4_REPAIR10_RAW_SOURCE_LOCALIZATION_DIAGNOSTIC_PASS`.

Result:

- H dominant source: `GR_Nr_boundary`;
- M dominant source: `AeST_E2`;
- M second source: `AeST_EX`.

### Repair11 — E-sector analytic momentum audit

Class:

`NL1C7B4_REPAIR11_ESECTOR_ANALYTIC_COVARIANT_AUDIT_PASS`.

At the B3 background:

- `E_bg=X_bg=0`;
- E2 and EX momentum contributions vanish at first order;
- both begin at quadratic order.

### Repair12 — full perturbative constraint audit

Class:

`NL1C7B4_REPAIR12_FULL_CONSTRAINT_FIRST_ORDER_RESIDUAL`.

Result:

- H increment is first order;
- momentum residual begins quadratically.

### Repair13 / Repair13a — stable source localization harness

Repair13 science payload was valid but the implementation classification failed because cancellation-sensitive parser/closure gates used an overly strict floating-point comparison.

Repair13a repaired only that numerical harness.

Class:

`NL1C7B4_REPAIR13A_ROUNDOFF_STABLE_SOURCE_LOCALIZATION_PASS`.

The physical source ordering remained unchanged.

### Repair14 / Repair14a — density-Q bridge omission

The full first-order Hamiltonian audit identified the missing density-Q contribution

`delta rho_A = Q K_QQ delta Q - (k^2/a^2)(K_B E_A + C chi)`.

Therefore the completed Fourier-space bridge is

`deltaQ_full = deltaQ_current + k^2(K_B E_A+C chi)/(a^2 Q K_QQ)`.

Repair14a certified the omission.

Class:

`NL1C7B4_REPAIR14A_DENSITY_Q_BRIDGE_OMISSION_IDENTIFIED`.

Interpretation:

this was an interface-completion error, not a wrong AeST sign or coefficient.

### Repair15 / Repair15a — density-Q-completed state

Repair15a certified the corrected state representation.

Class:

`NL1C7B4_REPAIR15A_DENSITY_Q_COMPLETED_STATE_CERTIFIED`.

Only `phidot_minus_Q` is changed by the Fourier density-Q correction.

State identity errors remain at machine precision.

Repair15a is a state-representation certification, not an exact B4 constraint certification.

### Repair16 — exact nonlinear retest after density-Q completion

Class:

`NL1C7B4_REPAIR16_REPAIR15A_RAW_CONSTRAINT_FAIL`.

All provenance/state/dictionary/grid gates pass.

The historical exact B4 gate still fails.

Representative scale 5 / Nr256:

- H `2.8244907235774306e-7`
- M `0.99999392720923`.

### Repair17 — remaining source localization

Class:

`NL1C7B4_REPAIR17_REPAIR16_SOURCE_LOCALIZATION_PASS`.

Global 54/54 source ordering:

- H dominant: `GR_Nr_boundary`
- H second: `GR_curv_NL`
- M dominant: `AeST_E2`
- M second: `AeST_EX`.

Interpretation:

the remaining failure is nonlinear geometric/E-sector closure, not a new first-order bridge omission.

### Repair18 — minimal nonlinear `(L,R_t)` projection feasibility

Physical correction pair:

- `L=L_p exp(y_L)`
- `R_t=R_{t,p}+delta R_t`.

Class:

`NL1C7B4_REPAIR18_MINIMAL_NONLINEAR_PROJECTION_FEASIBILITY_FAIL`.

Important payload:

- 24/24 optimizer calls report numerical success;
- 0/24 exact canonical closures pass;
- correction norm scales cleanly as `O(lambda^2)`;
- two-grid correction amplitude is stable;
- optimizer terminates by step stagnation with large optimality.

Interpretation:

the result does not establish that the physical `(L,R_t)` ansatz has no solution.

### Repair18a — dimensionless `R_t` coordinate

Coordinate repair only:

`q_Rt = delta R_t/(a H R_s)`.

No physics or bound changed.

This removed a physical-unit scaling problem but did not by itself solve exact nonlinear closure.

### Repair18b / Repair18b1 — Jacobian fidelity and local rank

The Jacobian audit identified a local rank deficiency.

Repair18b1 class:

`NL1C7B4_REPAIR18B1_LOCAL_PROJECTION_RANK_DEFICIENCY`.

At Nr=256 the full physical Jacobian has rank

`508/510`.

Dense direct linear least squares can nevertheless reduce the linearized residual essentially to zero.

### Repair18c — two-mode null-space characterization

Class:

`NL1C7B4_REPAIR18C_TWO_MODE_NULLSPACE_CHARACTERIZED`.

The two right-null modes were characterized.

The parent residual projection onto the two left-null directions is tiny:

- scale 5: `9.707232843664437e-11`
- scale 10: `2.1911761962074124e-10`
- scale 20: `1.6006841801170347e-10`.

Interpretation:

the parent residual is essentially in the Jacobian range. There is no demonstrated first-order residual-space incompatibility.

### Repair18d / Repair18d1 — transverse gauge pair

Repair18d1 class:

`NL1C7B4_REPAIR18D1_NULLSPACE_TRANSVERSALITY_AUDIT_PASS`.

Certified gauge pair:

`Y4+Qmean`.

The selected pair remains well-conditioned through all tested scales.

This licenses exact removal of the two right-null directions.

### Repair19 — gauge-fixed exact nonlinear least-squares attempt

Exact gauge constraints:

- `Y4=0`
- `Qmean=0`.

Class:

`NL1C7B4_REPAIR19_GAUGE_FIXED_EXACT_NONLINEAR_CONSTRAINT_FAIL`.

Important payload:

- gauge residuals are at roundoff;
- corrections retain clean `O(lambda^2)` scaling;
- exact nonlinear closure fails;
- SciPy TRF frequently exits by `xtol` with very large optimality.

Interpretation:

the null freedom was removed correctly, but the nonlinear least-squares route remained numerically stagnant.

### Repair19a — chain versus orthonormal coordinates

Class:

`NL1C7B4_REPAIR19A_GAUGE_FIXED_LINEAR_INFEASIBILITY`.

This classification is frozen and must not be relabelled.

Diagnostic payload:

- chain-basis condition number:
  - Nr=256: `162.33598862000716`
  - Nr=512: `325.3116790240505`
- orthonormal Helmert basis:
  - condition number `1`.

However all LSMR solves reached the fixed `10000` iteration ceiling and retained large residuals.

Because earlier dense audits showed near-perfect compatibility, this result did not establish physical linear infeasibility.

### Repair19b — direct reduced linear audit

Class:

`NL1C7B4_REPAIR19B_IMPLEMENTATION_FAIL`.

This classification is also frozen.

The failure came from preregistered gates requiring:

- full numerical rank for every basis/driver;
- physical correction-vector agreement across rank-sensitive solves.

The payload nevertheless showed that the orthonormal representation was directly residual-space feasible under both GELSD and GELSY.

That motivated a narrower preregistered certification repair rather than relabelling Repair19b.

### Repair19b1 — orthonormal direct linear feasibility certification

Class:

`NL1C7B4_REPAIR19B1_ORTHONORMAL_DIRECT_LINEAR_FEASIBILITY_LSMR_STAGNATION_PASS`.

Result freeze commit:

`5f33dd543f9b722438faa9659858be942287f14f`.

Result JSON:

- SHA-256:
  `33774c721bfd15c1c2f6b776408b3fc4623e3720f9199aa04fc43e8415be1a26`
- bytes:
  `36865`.

Evaluator log:

- SHA-256:
  `7aee53ebc12e808099cab27992bc62b86eb0c7fff348ce54fe971cb51ec6a3e5`.

Local runner log:

- SHA-256:
  `1b2457a8b32ede3a40dc6a6cca715a3affb6d97dea55224ebf983e5ce996e4fa`.

All nine gates PASS.

Direct orthonormal residuals satisfy the unchanged `1e-6` threshold for both LAPACK drivers in all six canonical cases.

Worst direct residual:

`1.1984362607786484e-07`.

Minimum LSMR/direct improvement factor:

`4833536.02985291`.

Returned rank remains descriptive:

- Nr=256: 508/508 for both drivers at all scales;
- Nr=512, scale 5: GELSD 1019/1020, GELSY 1020/1020;
- Nr=512, scale 10: GELSD 1019/1020, GELSY 1020/1020;
- Nr=512, scale 20: both 1020/1020.

Scientific conclusion:

the frozen physical `(L,R_t)` gauge-fixed subspace is linearly residual-space feasible, and the earlier LSMR failure was numerical stagnation.

### Repair19c — orthonormal direct Gauss-Newton nonlinear closure

Class:

`NL1C7B4_REPAIR19C_ORTHONORMAL_DIRECT_GN_NONLINEAR_CLOSURE_FAIL`.

Result freeze commit:

`e0d7415be5da36757327c0d36cc2eaaae2ecc2d5`.

Frozen local output:

- JSON SHA-256:
  `5ad02254c512f90d0f82a42d0f5aa00f15c1dae6248bdbe7ad69addb183b600a`
- evaluator log SHA-256:
  `69c1c31de071087fd2cb06f291037903ee71da2524351780b5add081a8b76b6e`
- local runner log SHA-256:
  `6f686fe7dca26eb5aca65c536b9fc1f4ffc7b490f35ca3df31ea4cbcb6dfeabb`.

Science result:

- canonical exact closure: `0/24`
- lambda=1 exact closure: `0/6`
- every canonical solve ends in `backtracking_failed`
- no state NPZ written.

PASS controls include:

- provenance;
- orthonormal constrained basis;
- exact parent reproduction;
- exact Repair19b1 first-step reproduction;
- two-grid correction control;
- field freeze;
- output integrity;
- claim boundary.

The final lambda=1 Hamiltonian residuals are very small, while momentum remains above threshold. Representative momentum values are:

- scale 5 / Nr256:
  `1.0025853680751008e-4`
- scale 10 / Nr256:
  `2.093034986286432e-4`
- scale 20 / Nr256:
  `5.730951320826147e-6`.

The correction amplitude remains extremely grid-stable:

- scale 5 ratio:
  `1.0034811583557677`
- scale 10:
  `1.0028899322177636`
- scale 20:
  `1.0034806074679696`.

Five of six small-lambda scaling paths pass. The only scaling failure is scale 10 / Nr512 with final slope `2.2059300525270347` against the frozen upper limit `2.2`.

The main diagnostic finding is the first-step linear/nonlinear mismatch. For scale 5 / Nr256 / lambda=1, the direct Jacobian predicts residual L2 `2.449845864172695e-11`, while the exact nonlinear residual after the accepted full step is `1.459496330366806e-2`. Similar discrepancies of roughly `1e7-1e9` occur across all six lambda=1 cases.

Interpretation:

the failure does not license a new field or physics change. It licenses a directional Jacobian-fidelity audit of the already certified first step.

### Repair19c1 — first-step directional Jacobian fidelity audit

Status:

**PREREGISTERED / IMPLEMENTED / IMPLEMENTATION-LOCKED / RUNNER READY / NOT YET EXECUTED**.

Preregistration:

- commit:
  `6318ce0f3a61a6503c4090bde6f4f247563cb704`
- blob:
  `9388ef43b7e6e215f89383d154a04a266d385ef8`.

Implementation:

- commit:
  `cbbbdf0db23b65412f99ce73b2c1c15aaac989da`
- blob:
  `616570dd106d92ffcb08bdaed99b646dd08a12e1`.

Implementation lock:

- commit:
  `63345a1c95ee5b945f4565651ef1df6aa5bc3c85`
- blob:
  `ca1837723f70a8b54c049192b85c992a197c24af`.

Runner:

- commit/current pre-run HEAD:
  `d7894886216ed96d6a7ed7ccc6816f3674c5b1db`
- runner blob:
  `acbeb7a66d06769cf0c97114b40b2a060612994b`.

Repair19c1 uses only the six lambda=1 canonical cases and one frozen x=0 GELSY direction per case.

It samples exact directional amplitudes from 1 down to 1/4096 and records secant/Jacobian fidelity without running a new nonlinear optimizer.

---

## Global methodological rule

This track follows:

`preregistration -> implementation -> implementation lock -> execution -> result freeze`.

A GitHub Actions green status is not by itself a scientific PASS.

Local WSL runs remain local and are never described as official runs.

Frozen evaluators, thresholds, source coefficients, signs, point sets, and earlier classifications are not silently changed to rescue a later result.
