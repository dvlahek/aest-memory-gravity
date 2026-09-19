# NL1C7B eta=0 spherical constraint track — history

Last updated: 2026-09-19

This file is the persistent project history for the nonlinear eta=0 spherical initial-data track on branch

`nl1c7b-eta0-spherical-evolution`.

It records scientific classifications exactly as obtained. A failed or implementation-failed repair is never relabelled after the fact.

## Current checkpoint

Repair19c3 is frozen as:

`NL1C7B4_REPAIR19C3_SELECTED_JACOBIAN_NONLINEAR_CLOSURE_FAIL`.

Result JSON SHA-256:

`aa19480ce4d41f649368f192f27d85b823e0247aa6f9bcc9eb7a9d23b60ac5b0`.

The Repair19c2-selected Jacobian is reproduced exactly, but exact nonlinear closure still fails:

- canonical PASS: `0/24`
- lambda=1 PASS: `0/6`
- all failures terminate through `backtracking_failed`
- no corrected-state NPZ is written.

The failure remains momentum dominated. For lambda=1, the best momentum residual is scale 20 / Nr256 at

`6.2117247534723366e-06`,

while the Hamiltonian residual there is

`7.743932006594966e-11`.

The selected `3-point, abs_step=3e-6` Jacobian fixes the first-step fidelity problem identified by Repair19c1/2, but after the first accepted step the requested Newton correction collapses from approximately `1e-5--1e-4` to `1e-9--1e-13`, while the finite-difference probe remains fixed at `3e-6`.

This establishes a post-first-step derivative-scale floor.

### Project decision

Repair19c3 is the stopping point for open-ended nonlinear solver repair.

At most one separately preregistered post-first-step derivative-scale diagnostic is licensed before deciding if the strict `1e-7` closure track is worth continuing.

In parallel, observational/data-side infrastructure may proceed immediately. No real-data analysis may be presented as a tested AeST prediction until the finite-eta model prediction and its numerical limitations are explicit.

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


### Repair19c1 — directional Jacobian fidelity characterization

Class:

`NL1C7B4_REPAIR19C1_FIRST_STEP_DIRECTIONAL_JACOBIAN_FIDELITY_CHARACTERIZED`.

Result freeze commit:

`cbf05b2a2845cda70fb962b20c5062d516b24a5b`.

Frozen local output:

- JSON SHA-256:
  `b4898fed6c6bbe7d4c91f8144ed35d03e6f318b298a2fc13c0daaef038c0e3cd`
- evaluator log SHA-256:
  `0db205484be993b7c9732afa2cea96df281279a6956bc4b1ba5b8c831ff3f89b`
- local runner log SHA-256:
  `63d6f55bfd067a770568669dcf5ff78d53b1c7428dfd6adce194282cade9ca6e`.

All eight gates PASS.

Global alpha=1 exact/predicted residual ratio:

- minimum:
  `50334591.40411471`
- maximum:
  `961747913.6033223`.

The leading discrepancy behaves approximately as `alpha deltaD`, not as an ordinary quadratic nonlinear remainder.

This identifies loss of local derivative fidelity in the frozen finite-difference Jacobian action, concentrated in the momentum block.

### Repair19c2 — finite-difference step-scale audit

Status:

**PREREGISTERED / IMPLEMENTED / IMPLEMENTATION-LOCKED / RUNNER READY / NOT YET EXECUTED**.

Preregistration commit:

`a094d9b660b346c3fcf03f6b26f2ce39ce263894`.

Implementation commit:

`515cc6c0ed04ec02d6dd48422bb0e96cf6575373`.

Implementation-lock commit:

`33190d51827fdfd84c5b4a7ed200f4ceac764045`.

Runner commit/current pre-run HEAD:

`e539011b888a4853f6f602de0ec7b71cb8c89a77`.

Runner blob:

`69d781af27f68b1aa72a440d539b83c796d15a11`.

Target successful characterization class:

`NL1C7B4_REPAIR19C2_FINITE_DIFFERENCE_STEP_SCALE_CHARACTERIZED`.



### Repair19c2 — finite-difference step-scale characterization

Class:

`NL1C7B4_REPAIR19C2_FINITE_DIFFERENCE_STEP_SCALE_CHARACTERIZED`.

Result-freeze commit:

`5f51cae7943679f6e96dcdefc7814c0f1551e244`.

Frozen local outputs:

- JSON SHA-256:
  `6a724f46a70be8d23e7b9898fe6e70073879c12f77eefbdbddc63d87fb47a17c`
- evaluator log SHA-256:
  `01902b0a920041c22eacc6a24bca22478f90e2d6d1b1a155695ae5720d978e60`
- local runner log SHA-256:
  `74992b9e84560391f9150e7a94fed26c094b27b4b0228706202a029546f735dc`.

Selected candidate:

`3-point, abs_step=3e-6`.

Aggregate selected mismatch:

- max:
  `1.3488978416629585e-4`
- median:
  `4.24433123436393e-5`.

Compared with the frozen default control, this improves worst-case directional fidelity by about `354.5x` and median fidelity by about `49.5x`.

The result confirms that finite-difference Jacobian fidelity was a major source of the Repair19c momentum-direction discrepancy.

### Repair19c3 — selected-Jacobian nonlinear closure

Class:

`NL1C7B4_REPAIR19C3_SELECTED_JACOBIAN_NONLINEAR_CLOSURE_FAIL`.

Result-freeze commit:

`b15eee7f15a5ef4dbb2c87050f4a55983d688d88`.

Frozen local outputs:

- JSON SHA-256:
  `aa19480ce4d41f649368f192f27d85b823e0247aa6f9bcc9eb7a9d23b60ac5b0`
- evaluator log SHA-256:
  `2483f37b8184783710b0f6e616d57c856e0291a3d136c3b682e58636754202b9`
- local runner log SHA-256:
  `79933aa6817daf52a084cb0fecb6c05ba673954f8583c1767befb5100de1c4f1`.

Result:

- canonical PASS: `0/24`
- lambda=1 PASS: `0/6`
- selected first-step reproduction PASS
- two-grid control PASS
- field freeze PASS
- no state NPZ written.

Lambda=1 momentum residuals remain above `1e-7`; the best case is scale 20 / Nr256 at `6.2117247534723366e-06`.

The main new diagnostic fact is post-first-step scale separation: first corrections are `O(1e-5--1e-4)`, while later requested Newton steps collapse to `O(1e-9--1e-13)` under the still-fixed `3e-6` finite-difference probe.

Interpretation:

the selected Jacobian repaired the parent-state directional fidelity but does not remain appropriately scaled throughout the nonlinear iteration. Repair19c3 does not establish physical infeasibility of the `(L,R_t)` ansatz.


---

## Global methodological rule

This track follows:

`preregistration -> implementation -> implementation lock -> execution -> result freeze`.

A GitHub Actions green status is not by itself a scientific PASS.

Local WSL runs remain local and are never described as official runs.

Frozen evaluators, thresholds, source coefficients, signs, point sets, and earlier classifications are not silently changed to rescue a later result.
