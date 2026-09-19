# NL1C7B eta=0 spherical constraint track — history

Last updated: 2026-09-19

This file is the persistent project history for the nonlinear eta=0 spherical initial-data track on branch

`nl1c7b-eta0-spherical-evolution`.

It records scientific classifications exactly as obtained. A failed or implementation-failed repair is never relabelled after the fact.

## Current checkpoint

The linear gauge-fixed `(L,R_t)` completion problem is now certified feasible in the preregistered orthonormal `Y4=0, Qmean=0` representation.

Latest completed checkpoint:

`NL1C7B4_REPAIR19B1_ORTHONORMAL_DIRECT_LINEAR_FEASIBILITY_LSMR_STAGNATION_PASS`

with

- `SCIENCE_RC=0`
- execution HEAD:
  `17a7656e361568dd06024d13022331081edb3e7a`
- result JSON SHA-256:
  `33774c721bfd15c1c2f6b776408b3fc4623e3720f9199aa04fc43e8415be1a26`
- maximum direct relative residual:
  `1.1984362607786484e-07`
- minimum frozen LSMR/direct residual ratio:
  `4833536.02985291`
- all 9 preregistered gates PASS.

Repair19b1 establishes that the same physical `(L,R_t)` correction subspace, with exact `Y4=0` and `Qmean=0`, admits a direct linear correction in all six canonical scale/grid cases.

It also establishes that the Repair19a LSMR result was grossly underconverged. It does not yet certify exact nonlinear B4 closure.

### Next executable gate

Repair19c has been preregistered, implemented, implementation-locked, and given a local runner.

Current HEAD:

`25769ce21404efbf03e368f4cf89f446cf7c9c44`.

Repair19c is the first deterministic nonlinear direct Gauss-Newton closure test in the certified orthonormal subspace.

It keeps:

- eta=0;
- physical correction pair only `(L,R_t)`;
- exact `Y4=0,Qmean=0`;
- historical exact B4 threshold `epsilon_H,epsilon_M <= 1e-7`;
- frozen source dictionaries and coefficients;
- all nonprojection fields bitwise frozen.

It uses:

- the same grouped two-point physical Jacobian;
- algebraic projection `J_orth=J_x B_orth`;
- direct LAPACK GELSY steps;
- deterministic Armijo backtracking;
- no LSMR, TRF, LM, multistart, random perturbation, or alternate-driver fallback.

If Repair19c passes and is frozen, the next scientific stage is short-time nonlinear eta=0 evolution, not another initial-constraint repair.

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

Status:

**PREREGISTERED / IMPLEMENTED / IMPLEMENTATION-LOCKED / RUNNER READY / NOT YET EXECUTED**.

Preregistration:

- commit:
  `3eaefcccb6c44f2db12b24caf3bfa3c3ec16a712`
- blob:
  `7749938dadb43f6cff6b974a9ee4af58bdf72a09`.

Implementation:

- commit:
  `5216c1afb9e27a24957aaade43f0857641f1b12d`
- blob:
  `f27ed8b39c1351e27d4f3b43b195ff4423e04c76`.

Implementation lock:

- commit:
  `f3c93050db6b545b57d5a0de32d6fd0a56f78945`
- blob:
  `bf5b7ec878eecc06ba83f51e7662080e95fa169c`.

Runner:

- commit/current pre-run HEAD:
  `25769ce21404efbf03e368f4cf89f446cf7c9c44`
- runner blob:
  `dc02d03f1d165caf3f2e16bf596cd2a3658a0943`.

Target PASS class:

`NL1C7B4_REPAIR19C_ORTHONORMAL_DIRECT_GN_EXACT_NONLINEAR_CONSTRAINT_PASS`.

If R19c passes:

1. freeze the R19c result;
2. preserve the exact six lambda=1 nonlinear states;
3. preregister short-time nonlinear eta=0 evolution;
4. only after clean eta=0 nonlinear evolution proceed toward finite eta and observational bridges.

If R19c fails:

1. freeze the failure exactly;
2. inspect the failed preregistered gate;
3. do not change solver, line search, driver, threshold, fields, or physics inside R19c;
4. open a separately preregistered diagnostic/repair only if the frozen evidence licenses it.

---

## Global methodological rule

This track follows:

`preregistration -> implementation -> implementation lock -> execution -> result freeze`.

A GitHub Actions green status is not by itself a scientific PASS.

Local WSL runs remain local and are never described as official runs.

Frozen evaluators, thresholds, source coefficients, signs, point sets, and earlier classifications are not silently changed to rescue a later result.
