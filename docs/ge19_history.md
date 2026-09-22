# GE19 reduced weakly nonlinear track — persistent history

Last updated: 2026-09-21

Branch:

`physics-first-gravitational-elasticity`

This file is the persistent scientific history for the GE19 reduced weakly nonlinear construction.

Historical classifications are immutable. A FAIL is never relabelled after a later repair succeeds. Implementation failures, diagnostic audits, science FAILs and certified PASS results are kept distinct.

## Current checkpoint

Repair22 is frozen as the first certified reduced second-order physical state:

`GE19_REPAIR22_ON_SHELL_PARENT_Z20_CERTIFICATION_PASS`

with

`Z20_certified = true`.

Repair22 result-freeze commit:

`9174f2e622f42851474ed124b429bf07b2db3ac7`.

Repair23 is also now frozen PASS:

`GE19_REPAIR23_Q20_NORMALIZED_BATH_BRIDGE_AUDIT_PASS`.

Repair23 result-freeze commit:

`79597296185209e50ef133f680d7b3d3481bac86`.

Repair23 closes the normalization/equation bridge needed before q20:

- exact q->z FLRW identity: PASS;
- exact cosmic->dimensionless bath identity: PASS;
- GE05 c1 normalized-z residual relative L2: `4.776595495173347e-16`;
- GE05 c2 analytic vs finite difference: `9.244401818347801e-09`;
- weight-scaling residuals: `0.0`;
- NL1C4 exact interval propagator vs DOP853:
  q `6.796235773486602e-15`,
  v `1.6810014932296363e-14`;
- all 10 frozen Repair23 gates PASS.

The exact normalized bath dictionary is now frozen:

`z_j = omega_j q_j / sqrt(w_j)`.

The second-order bath equation is frozen as

`G1[Z20,z20] + G2[(Z10,z10),(Z10,z10)] = 0`.

Repair24 has now produced its first valid science result and is frozen as

`GE19_REPAIR24_Q20_CONSTRUCTION_FAIL`.

Repair24 result-freeze commit: `82f1f56912f92e628797997d82ffd64de2a4a926`.

Frozen science JSON SHA-256: `71f463524b47f72d2c5082667fe99141d2286ebc2938c4eed6b89a1583339f2a`.

Frozen science NPZ SHA-256: `6591adf8659cb96eda55eae32613424c0464cd42a9d20e0872371fb9254814f4`.

All Repair24 numerical convergence gates pass except the initial first-order bath-drive bridge:

- G2 Nx256/Nx512 relative L2: `2.2947298319652412e-15` PASS;
- q20 Nq1024/Nq2048 relative L2: `8.251855068695476e-05` PASS;
- q20 Nt64/Nt128 relative L2: `3.245459862000118e-05` PASS;
- z10 Nt64/Nt128 relative L2: `0.003453755379112942` PASS;
- all outputs finite and all cases complete;
- H1 X10 initial match: `0.9999999471925649` FAIL versus `1e-10`.

Therefore Repair24 localizes the remaining q20 blocker to the v0.77 -> GE19 first-order bath-boundary bridge. q20 is not certified and H4/Z21 remains blocked.

Initial locked prelock: `35653683119` — SUCCESS.

The first local Repair24 execution failed before any q20 science output with a `(128,)` versus `(64,)` background-array broadcast error. Cause: Repair24 incorrectly mapped its Nt128 `primary` label to Repair13's frozen `primary`, which is Nt64. This is frozen as an implementation failure only.

Background-grid repair commit: `7218e049e5e3a1a413663f587d98f8100f22cfa4`.

Post-fix dedicated prelock: `35696839240` — SUCCESS.

Updated implementation lock commit: `18c80840855480130cc08345e097d487a6ed5991`.

Updated locked local runner commit: `e2d6b592ce90471f6576149cecbc0d8d79ddeb68`.

Post-fix runner-head static audit: `35697045877` — SUCCESS.

The frozen v0.77 trace does not contain a native sample exactly at `a=0.4`; Repair24 therefore uses the exact prefix of the frozen NL1C4 interval model across the certified bracket `0.3799548579266745 < 0.4 < 0.41924557250685585`. The GE19 initial surface is not moved.

Frozen q20 boundary convention:

- z10 at z=1.5 inherits the full-history positive-Drude retarded state and then evolves on the reduced on-shell H1 parent;
- z20(z=1.5)=0;
- dz20/dxi(z=1.5)=0.

No H4/Z21 solve is licensed until the first-order bath-boundary mismatch is localized and a later q20 construction is frozen PASS.
---

## Scientific status in one line

`H1/background certified -> Repair22 certifies Z20 -> Repair23 bath bridge PASS -> Repair24 q20 FAIL only on initial X10 bridge -> Repair25 boundary-dictionary audit next`.

---

## Certified base

### Repair13 — self-consistent reduced-background H1 reclosure

Classification:

`GE19_REPAIR13_SELF_CONSISTENT_REDUCED_BACKGROUND_H1_RECLOSURE_PASS`.

Result-freeze commit:

`5461f89f77f91e931f14abb6a2e5014597e0cb6f`.

This is the current certified first-order parent.

Reduced homogeneous background:

`H_red(a)^2 = (Q K_Q-K)/3 + C/a^3 + rho_lambda`.

Frozen scalar charge:

`a^3 K_Q = I0`.

Global Stage-A controls:

- Friedmann relative L2 max: `5.3148141262610533e-17`;
- pressure identity relative L2 max: `4.9400107598617e-16`;
- canonical/linear residual max: `4.3389056048311334e-16`;
- shift backward error max: `4.54500027983174e-7`;
- anisotropy backward error max: `2.0133086499281873e-16`;
- initial dynamic match max: `5.826069165486057e-14`;
- Nt64/Nt32 state relative L2 max: `1.317515813217615e-4`.

All frozen Stage-A gates PASS.

Scientific conclusion:

the reduced Einstein+AeST+dust+Lambda first-order system closes on its own homogeneous on-shell background.

The previous Repair11 residual was dominated by background/operator inconsistency, not by a missing post-hoc CLASS momentum source.

---

## H3 / Z20 attempt

### Repair14 — first self-consistent reduced H3/Z20 particular solve

Classification:

`GE19_REPAIR14_SELF_CONSISTENT_REDUCED_H3_Z20_PARTICULAR_FAIL`.

Result-freeze commit:

`7ba8b312f7dd8ca7035958be2abdf03df98a5bae`.

Frozen output hashes:

- JSON/FULL log:
  `741da95a0aaffa31e27f2b05d42b8a7f011574013de8639812e453d7b130fe57`;
- NPZ:
  `b72626bd45b02b537d21f035fc8c746eb06eee669869c4aea921861328303c42`.

Solved equation:

`L_total Z20 = -Q_total(Z10,Z10) - 2 Y2[Z10]`.

The exact Lambda common-direction second source was included.

PASS controls:

- frozen Repair13 provenance exact;
- all sources finite;
- Nx1024/Nx2048 source convergence:
  `1.1166216258507802e-12`;
- anisotropy constraint:
  `5.176430012533252e-16`;
- Nt64/Nt32 state convergence:
  `5.470805059400488e-4`;
- all C and beta cases complete;
- all outputs finite.

FAIL controls:

- primary linear residual:
  `1.3665579847915249e-8 > 1e-8`;
- primary shift backward error:
  `1.6504055271415055 >> 1e-6`.

Control-grid shift is similarly large:

`1.6473553166699726`.

Interpretation:

the candidate Z20 is numerically stable and converged in space/time but is **not constraint-certified**.

Repair14 does not license q20 or H4/Z21.

### Descriptive source hierarchy from Repair14

Across the frozen C envelope:

- Einstein+AeST quadratic source L2: approximately `1.446e10`;
- dust quadratic source L2: approximately `8.4e-6`;
- Lambda quadratic source L2: approximately `3.09e-16`;
- Y_H3 L2: approximately `0.030--0.055`.

Thus the H3 memory Y source is only approximately `2e-12--4e-12` of the baseline analytic quadratic source for this frozen direction.

The beta0={1,0.5,0.1} Z20 candidates are correspondingly almost identical at approximately `1e-12` relative level.

This is descriptive because Repair14 failed Stage B.

---

## Initial-surface diagnostics after Repair14

### Repair15 — zero-dynamic-velocity compatibility audit

Classification:

`GE19_REPAIR15_H3_INITIAL_SHIFT_NOETHER_COMPATIBILITY_AUDIT_COMPLETE`.

Route:

`INITIAL_SOURCE_INCOMPATIBILITY`.

Result-freeze commit:

`e2d642eb528fab10aa4d3ba0a2afc94b2dcacbaf`.

JSON SHA-256:

`a8c86b6056a3d6ab2f6f443850bef34881452b4a11b32bb6a66e2ac7920f1e50`.

Frozen test:

- q20 values zero;
- q20 cosmic-time derivatives zero;
- only N20 and delta_varrho20 algebraic.

For material cases, the row-scaled 3x2 system formed by lapse, dust density and shift has coefficient rank 2 but augmented rank 3.

Global compatibility residuals:

- least-squares relative residual max:
  `0.24244997981714522`;
- left-null compatibility residual max:
  `0.2424499798171455`.

Threshold:

`1e-6`.

Conclusion:

no choice of only N20 and delta_varrho20 can close lapse+density+shift under the frozen q=0,qdot=0 initial convention.

This result does not prove that the quadratic source itself violates Noether/Bianchi compatibility.

### Repair16 — canonical-zero initial-state audit

Classification:

`GE19_REPAIR16_CANONICAL_ZERO_INITIAL_STATE_AUDIT_COMPLETE`.

Route:

`QUADRATIC_SOURCE_NOETHER_INCOMPATIBILITY_REMAINS`.

Result-freeze commit:

`d5a619495f0f8fb2da53528b46476a15c1a32922`.

JSON SHA-256:

`768d5a2de7cd62059e7149a4765ab5a9663eef708fc29989c05192f607c5bf68`.

Frozen canonical boundary:

`y0=(S,u,phi,T,pS,pu,pphi,pT)=0`.

The algebraic reconstruction is allowed to determine N20, delta_varrho20 and qdot20.

Global material-case controls:

- algebraic residual max:
  `7.465407808870082e-16`;
- independent lapse backward error max:
  `1.0`;
- independent shift backward error max:
  `1.0`;
- anisotropy backward error max:
  `6.394777335818628e-16`;
- local algebraic scaled condition number max:
  `3.1343173893632996`;
- all outputs finite.

Conclusion:

canonical y0=0 is not on the forced H3 constraint manifold.

Important interpretation boundary:

this still does not prove that the frozen quadratic source is intrinsically inconsistent. At finite z=1.5, a nonzero forcing source need not admit the zero canonical state.

---

## Repair17 — full canonical initial-manifold audit

Classification:

`GE19_REPAIR17_FULL_CANONICAL_INITIAL_MANIFOLD_AUDIT_COMPLETE`.

Route:

`FINITE_WINDOW_ZERO_BOUNDARY_INADMISSIBLE_SOURCE_COMPATIBLE`.

Result-freeze commit:

`1ce72e3c3a732be59c1e390c8ef67859348b76c6`.

Frozen output hashes:

- JSON/FULL log:
  `f81ad8ef52eb3a7ff4d4286670a62c830f17872459f43812b059447f85e14184`;
- outer runner:
  `8cb82e530f104895bd2d22cd6ae1bb86c36d64dd80eb9418b3c6a6bbe7a5c1e0`.

Repair17 tests the exact same frozen Repair14 source on the full canonical initial manifold

`y=(S,u,phi,T,pS,pu,pphi,pT)`.

Full-y result:

- material cases: `714/714` pass;
- constraint residual max: `8.892022036425179e-13`;
- lapse backward error max: `2.6457320679749983e-16`;
- shift backward error max: `1.8699495216551784e-10`;
- eliminated algebraic residual max: `2.388467729664837e-16`;
- rank 2 and augmented rank 2 throughout;
- all finite.

Restricted q-only states fail the eliminated algebraic gate in all material cases.

Restricted p-only states are much closer:

- algebraic residual max `1.6529397640806795e-16`;
- constraint residual max `1.9160597062254987e-10`;
- shift backward error max `1.0092587566692186e-5`;
- `396/714` satisfy all current gates.

Scientific conclusion:

the quadratic source is not shown to violate the initial Noether/constraint compatibility. The finite-window zero boundaries used in Repairs 14-16 were inadmissible.

Boundary-selection caveat:

the full 2x8 system has six null directions. Repair17's Euclidean minimum-norm representative is an existence witness, not yet a physical initial prescription. Its norm reaches `1908119.6665826605` in the strongest material case.

The next gate must therefore freeze and certify a coordinate/physics-motivated constraint-compatible boundary before any H3 propagation is rerun.
---

## Repair18 — zero-coordinate projected-momentum boundary

Classification:

`GE19_REPAIR18_ZERO_COORDINATE_CONSTRAINT_PROJECTED_MOMENTUM_BOUNDARY_AUDIT_COMPLETE`.

Route:

`ZERO_COORDINATE_CONSTRAINT_PROJECTED_MOMENTUM_BOUNDARY_CERTIFIED`.

Result-freeze commit:

`3892ee81c8030ee7c5131d1aaf1f333cbdbe6509`.

Frozen output hashes:

- JSON/FULL log:
  `d5603138c2f488413686323d1241613f6ef707b586116aa7fe865ae25ceb0edc`;
- outer runner:
  `f50fe69000c31ddbb57228ae5dc15c2fc6c641e4adb08e30fda6ad3e0677f2c5`.

Boundary:

- `q0=(S20,u20,phi20,T20)=0` exactly;
- `p0=(pS20,pu20,pphi20,pT20)` from the frozen 2x4 lapse+shift projection;
- doubly equilibrated GELSD minimum norm;
- exactly four iterative-refinement sweeps.

Global result:

- `714/714` material cases PASS;
- scaled constraint residual max `2.482534153108436e-16`;
- lapse max `2.639993079262776e-16`;
- shift max `3.2234628832120975e-16`;
- algebraic residual max `2.457039030496151e-16`;
- anisotropy max `6.394777335818628e-16`;
- rank 2 throughout.

Primary/control projected p0 is identical to machine representation, with qdot0 relative L2 mismatch <= `6.468697709110601e-15`.

Raw p0 and qdot0 norms are coordinate-scale sensitive and are monitored descriptively only. The scaled solution norm remains <= `0.577350276667655`.

Scientific conclusion:

the finite-window initial boundary is now uniquely and reproducibly certified. The next licensed step is H3/Z20 propagation with this exact boundary and unchanged Stage-B gates.
---

## Repair19 — projected-boundary H3/Z20 propagation

Classification:

`GE19_REPAIR19_PROJECTED_BOUNDARY_REDUCED_H3_Z20_PROPAGATION_FAIL`.

Result-freeze commit:

`71e1e60e133b79828163fe077f5991e98d40d6bb`.

Frozen output hashes:

- JSON/FULL log:
  `32837e04a9ea6c83642a0d465f0312cc17a02ddad168760764f3c7b999a0a14d`;
- NPZ:
  `d638c86e48dd5c912629068f56c3780d0a611ed26ff5c161cd792a14328f7215`;
- outer runner:
  `6bdff0aaee50f242b51df735acb2a6bc1277bfb5aa8231dbc60c94704fb19d35`.

Repair19 changes only the initial canonical boundary relative to Repair14:

- q0=0;
- p0 from the certified Repair18 projection.

The Repair18 boundary reproduces exactly.

PASS controls:

- source convergence `1.1166216258507802e-12`;
- primary linear residual `1.2568088493786592e-13`;
- anisotropy `5.176430012533252e-16`;
- Nt64/Nt32 state convergence `3.77673237391757e-4`;
- all outputs finite.

FAIL control:

- primary all-row shift `1.8946212213942455`;
- control all-row shift `1.9278909582169974`.

The largest relative shift failures are near-null rows: residual and row scale are both approximately `1e-18`.

On active rows the primary shift residual is approximately `7e-6`, above the frozen `1e-6` gate but far below the near-null O(1) metric.

Repair19 remains historical FAIL. It does not certify Z20.

## Repair20 — shift near-null + time-resolution audit

Classification:

`GE19_REPAIR20_SHIFT_NEAR_NULL_TIME_RESOLUTION_AUDIT_COMPLETE`.

Route:

`ACTIVE_SHIFT_PROPAGATION_ISSUE_REMAINS`.

Result-freeze commit:

`317b4219f6630b0c1f0f15081e8db62e6470a47c`.

Frozen output hashes:

- JSON/FULL: `5f1dc8e48963c6403f142958c8ce34ab1457953b47868d1a65317655cd0644eb`;
- NPZ: `99937112b889bc556ada756bc7b4e834991a6019596fdbc353a40294ad3968a6`;
- runner: `e251e3c226201eca22e3a839b16e0f49a5187eea8e75d57a5e7df48878d0521e`.

Near-null diagnosis:

- Nt128 S_ref `0.0030030102311219666`;
- near-null threshold `4.474833952072213e-11`;
- near-null abs residual / S_ref `7.780179533808193e-14`, PASS.

Active shift:

- Nt32 `8.140088658740307e-5`;
- Nt64 `7.796797901197683e-6`;
- Nt128 `9.588510852544816e-6`.

The Nt128 active gate remains above the original `1e-6` threshold.

State, linear and anisotropy controls all pass strongly.

The preregistered global-max observed order is not a matched-sample order because the worst active sample moves from m=8 to m=6 to m=17 across the three grids.

Therefore Repair20 confirms near-null monitor pathology but leaves an active shift propagation/certification issue unresolved.

## Repair21 — on-shell H1 parent + matched-shift audit

Classification:

`GE19_REPAIR21_ON_SHELL_H1_PARENT_MATCHED_SHIFT_AUDIT_COMPLETE`.

Route:

`INTERPOLATED_H1_PARENT_DEFECT_CONFIRMED`.

Result-freeze commit:

`a6fea1e32aebef65e43151030fe90fc6263d6ce0`.

Frozen output hashes:

- JSON/FULL:
  `e27d12f18a992a1c8c3217e67c0efd39dcf7c9d7aadcfbbb3220f7508bca1bb2`;
- NPZ:
  `c6fcde7d39480ec7f03de2acf0f33f648a997404c9cca8f83990ed7b50667f3b`;
- runner:
  `3cb6061fedac996e52ecc9a72cd15b5e6da9563010d47ab487977aef8b9ffb02`.

Repair21 independently solves H1 on Nt64 and Nt128.

H1 controls all PASS.

The Repair20 PCHIP parent differs from the genuine Nt128 parent only at approximately `1e-5` state level, but changes the H3 RHS by `2.486632550432435e-4`.

With the genuine on-shell parent:

- active Nt128 shift Linf = `8.067171929789269e-7`;
- matched Linf order = `3.2357755356022007`;
- matched RMS/L2 order = `3.1225511606202474`;
- near-null abs residual / S_ref = `9.599035682049098e-15`;
- H3 state Nt64/Nt128 = `1.520874923438771e-5`;
- linear residual = `2.1762890113126683e-13`;
- anisotropy = `6.391121604651976e-16`;
- boundary p0 reproduction = `0.0`.

All preregistered Repair21 H1 and H3 gates PASS.

Scientific conclusion:

the unresolved active Repair20 shift residual was caused by the off-shell separately interpolated H1 parent.

Repair21 is diagnostic and does not itself certify Z20.

## Repair22 — on-shell-parent Z20 certification

Classification:

`GE19_REPAIR22_ON_SHELL_PARENT_Z20_CERTIFICATION_PASS`.

Result-freeze commit:

`9174f2e622f42851474ed124b429bf07b2db3ac7`.

Frozen output hashes:

- JSON/FULL:
  `7d53b2458183c6b2cc326acdded70b2c3ce1fab959d8456e56d3b4f1f86ef374`;
- NPZ:
  `3020e0d040f902ab2609e05705f4508d9919665b1344fa0e641644ea8fc41a16`;
- outer runner:
  `52f01d0991e72737b464e025bd996f260db9bc47e55dbe82165d42fc0636dbaf`.

Repair22 recomputes the on-shell Repair21 core before certification and adds the frozen Nx1024/Nx2048 source control and full Repair18 boundary re-audit.

All 26 frozen gates PASS.

Source spatial convergence:

`1.396726236718744e-12`.

Boundary:

- p0 reproduction `0.0`;
- scaled constraint residual `2.482534153108436e-16`;
- lapse `2.639992134386278e-16`;
- shift `3.321187887383499e-16`;
- algebraic residual `2.457039030496151e-16`;
- rank 2 / augmented rank 2.

Active shift certification:

- Nt128 Linf `8.067171929789269e-7`;
- original active threshold `1e-6`;
- matched Linf order `3.2357755356022007`;
- matched RMS/L2 order `3.1225511606202474`;
- near-null absolute residual / S_ref `9.599035682049098e-15`.

Other H3 controls:

- Nt64/Nt128 state relative L2 `1.520874923438771e-5`;
- linear residual `2.1762890113126683e-13`;
- anisotropy `6.391121604651976e-16`;
- all outputs finite.

Scientific conclusion:

`Z20_certified = true`

for the low-mode constraint-certified window-local reduced-H3 particular directional state only.

Repair14 and Repair19 remain historical FAIL results; Repair20/21 remain diagnostic results and are not relabelled.

Next licensed object:

`q20`, the baseline second-order normalized bath response fixed by the second directional expansion of `G[Z,q]=0`.
---

## Repair23 — q20 normalized-bath bridge

Classification:

`GE19_REPAIR23_Q20_NORMALIZED_BATH_BRIDGE_AUDIT_PASS`.

Result-freeze commit:

`79597296185209e50ef133f680d7b3d3481bac86`.

Successful execution: workflow `35645649788`, job `106485343261`, artifact ID `10659908576`.

Frozen JSON/FULL SHA-256:

`20ce1c8d7faca45fe61b68bd0c451a616c00b0bd3e22504e83467877b8a3e6c6`.

All ten frozen gates PASS.

Exact normalized variable:

`z_j=omega_j q_j/sqrt(w_j)`.

Exact FLRW bath equation:

`zddot_j+3H zdot_j+omega_j^2(z_j-X)=0`.

Dimensionless form:

`z_j,xi,xi+3h z_j,xi+r_j^2(z_j-X)=0`.

Second directional equation:

`G1[Z20,z20]+G2[(Z10,z10),(Z10,z10)]=0`.

Repair23 freezes the q20 dictionary and window-local boundary convention but does not construct q20.

The first execution wrapper run `35645459393` failed only because `tee` opened the log before `results/` existed. Wrapper-only fix `02b205d82ef9c89cfcbccd1a5ec2e5429a0cc2f8` changed no science code or gate.
---

## What is certified now

Certified:

- NL0B covariant memory construction;
- weakly nonlinear source infrastructure;
- GE06 analytic Einstein+AeST directional generator;
- GE07 pressureless-matter directional generator;
- Repair13 self-consistent reduced background;
- Repair13 reduced H1 / Z10 Stage-A closure;
- Repair22 low-mode window-local reduced-H3 particular Z20.

Not certified:

- homogeneous/primordial or full-species Z20;
- q20;
- H4/Z21;
- finite-eta nonlinear trajectory;
- nonlinear lensing or nonlinear matter observables;
- any real-data nonlinear-memory inference.

## Data-readiness boundary

The project is **not yet ready for a nonlinear real-data claim**.

The shortest valid route is:

`Repair24 q20 construction -> H4/Z21 -> observable bridge -> real-data confrontation`.

For the full nonlinear-memory state claim:

`certified reduced Z20 -> q20 -> H4/Z21 -> observable bridge -> data`.

Lensing remains a natural first observable after state certification because the model acts directly through gravitational potentials. CMB/SPT high-l and structure probes remain later comparison channels.

No observational result may be used to choose or tune a repair in the theory chain.

---

## Immediate action

Run a separately preregistered Repair25 first-order bath-boundary dictionary audit. Do not rerun q20 yet.

Canonical project status:

**Repair13 H1 PASS; Repair18 boundary PASS; Repair22 Z20 CERTIFIED; Repair23 q20 bridge PASS; Repair24 science FAIL only on v0.77->GE19 initial X10 matching; Repair25 NEXT; H4/Z21 NOT YET LICENSED.**
