# GE19 reduced weakly nonlinear track — persistent history

Last updated: 2026-09-23

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

## Repair24 — q20 construction

Classification:

`GE19_REPAIR24_Q20_CONSTRUCTION_FAIL`.

This is the first valid Repair24 science execution. The q20 construction ran to completion, but certification failed on exactly one frozen upstream bridge gate.

Result-freeze commit:

`82f1f56912f92e628797997d82ffd64de2a4a926`.

Frozen controls:

- H1 X10 initial bridge mismatch: `0.9999999471925649` — FAIL vs `1e-10`;
- G2 spatial Nx256/Nx512 relative L2: `2.2947298319652412e-15` — PASS;
- q20 Nq1024/Nq2048 weighted-z20 relative L2: `8.251855068695476e-05` — PASS;
- q20 Nt64/Nt128 weighted-z20 relative L2: `3.245459862000118e-05` — PASS;
- z10 Nt64/Nt128 weighted-z10 relative L2: `0.003453755379112942` — PASS;
- all outputs finite — PASS;
- all cases complete — PASS.

Thus 12/13 frozen Repair24 gates pass. The remaining blocker is the initial first-order bath-drive dictionary between frozen v0.77 chi/a and the GE19 on-shell X10 representation.

No q20 certification and no H4/Z21 license.

## Immediate action

Preregister Repair25 as a first-order boundary-dictionary audit only. Compare on the exact a=0.4 surface:

- transported frozen v0.77 chi/a;
- GE15 certified chi = Q(a theta/k^2 + alpha);
- Repair22 on-shell X10 = Q_action u10 + partial_x(varphi10)/a.

Report per-mode ratios/phases and candidate normalization residuals before any q20 rerun.

Canonical project status:

**Repair22 Z20 CERTIFIED; Repair23 bath bridge PASS; Repair24 q20 science FAIL localized to the initial X10 bridge; q20 NOT CERTIFIED; H4/Z21 NOT LICENSED.**


---

## Repair25 — first-order bath boundary dictionary audit

Classification:

`GE19_REPAIR25_FIRST_ORDER_BATH_BOUNDARY_DICTIONARY_AUDIT_COMPLETE`.

Route:

`LEGACY_V077_BOUNDARY_TRACE_INCOMPATIBLE_GE15_CERTIFIED`.

Result-freeze commit:

`c6eb792ff43ffada69f1fb5cc59cf57c52c1f602`.

Frozen JSON/FULL SHA-256:

`ccf30e5d706f91c023e31526a9ae66154ecadbfa15e3f90a5239824ad74c7a05`.

Locked runner SHA-256:

`64100b1960050ecb194579357db3d383866a068788523dd3f159558a7087280b`.

The execution passed all provenance checks and exited with `SCIENCE_EXIT=0`.

Exact a=0.4 closure:

- GE15 algebraic X versus grad(chi)/a relative L2:
  `6.961752470055609e-17`;
- Repair22/GE19 X10 versus GE15 relative L2:
  `7.819918013124737e-17`;
- Q_action versus GE15:
  `1.1102230246251565e-16`;
- v0.77 Q_trace versus GE15:
  `1.1065592085855149e-16`.

Thus GE15 and Repair22/GE19 agree to machine precision, including the Q dictionary.

The legacy v0.77 chi/a boundary is not compatible in amplitude:

- direct relative L2 at a=0.4:
  `0.9999998670367867`;
- direct overlap-window relative L2:
  `0.9999998669793289`.

The six v0.77/GE15 amplitude ratios at a=0.4 span approximately

`6.43e4` to `1.85e7`

and are mode dependent.

Their phase differences are zero to floating-point accuracy.

Across the common a=0.4..0.8333333 overlap, each mode separately has almost identical temporal shape:

- per-mode post-fit relative L2:
  approximately `3.01e-4`;
- per-mode temporal cosine:
  approximately `0.999999954`.

However a single global real or complex scale does not close the mismatch:

- global real post-fit relative L2:
  `0.5484311025444283`;
- global complex post-fit relative L2:
  `0.46599450356276223`.

No tested simple convention factor closes it. The best report-only tested candidate, `1/k`, still leaves relative L2

`0.25783615676918054`

after an additional complex scalar.

Scientific conclusion:

Repair24's unique X10 bridge failure was not caused by the GE15/Repair22 first-order physics dictionary. It was caused by using the historical v0.77 boundary trace in a different mode-amplitude normalization convention.

Repair25 adopts no fitted normalization.

No q20 rerun occurred.

q20 remains not certified and H4/Z21 remains unlicensed.

Next required object:

derive and certify the exact legacy v0.77 mode-amplitude normalization map from the frozen generating construction into the GE15/GE19 convention before any q20 rerun.

Canonical project status:

**Repair22 Z20 CERTIFIED; Repair23 bath bridge PASS; Repair24 q20 science FAIL; Repair25 localizes the blocker to the legacy v0.77 mode-amplitude normalization; q20 NOT CERTIFIED; H4/Z21 NOT LICENSED.**


---

## Repair26 — cancellation-free full-history first-order bath boundary

Classification:

`GE19_REPAIR26_CANCELLATION_FREE_FULL_HISTORY_BATH_BOUNDARY_PASS`.

Route:

`CANCELLATION_FREE_FULL_HISTORY_BATH_BOUNDARY_CERTIFIED`.

Successful workflow:

- run `35721220889`;
- job `106724330805`;
- artifact `10690709843`;
- artifact ZIP digest:
  `sha256:33faae31aae0ebe3cc52ac2083193ec8ba3dfe284fb07f06ef2568cad8e3938f`.

Result-freeze commit:

`6564ae09e808bc29889cc11c7f5ab34590452d19`.

Frozen outputs:

- JSON/FULL:
  `80ba0b5927217be000991c82b4afb5f39b5e0ff369bc9b630a88ec11dabdedb6`;
- NPZ:
  `ba6265af81e440c610a4ac4805e7c55b45f3bd681e14731b8d067e47a979fdd8`;
- R1 full-history cancellation-free trace:
  `608ee0b4c868a701db6976f756b9a551cd9ddffe1e8e4ab37c5cd2361405a6f8`;
- R2 full-history cancellation-free trace:
  `a3fee42d20b94813c2f5e58ca9c77237e7cf7ebf313dac937bdad750554d8f5f`.

The initial dependency-only run `35721094832` remains a frozen implementation failure and produced no science result.

Repair26 regenerates the first-order eta=0 bath-drive history in the exact GE15 state

`s=chi/Q`, `alpha=s-a theta/k^2`, `chi=Q s`,

with exact initial `s=0`.

No physics equation or model parameter changes.

At a=0.4:

- R1 trace X10 vs GE15 dense:
  `3.9819456608594117e-11`;
- R2 trace X10 vs GE15 dense:
  `3.163231556278803e-11`;
- R1 vs R2 trace X10:
  `7.11299054009343e-12`.

Retarded bath boundary precision closure:

- R1/R2 z10:
  `3.5309623104625126e-06`;
- R1/R2 v10:
  `0.0023720775441813187`;
- Nq1024/Nq2048 weighted z10:
  `4.492427062849641e-06`;
- Nq1024/Nq2048 weighted v10:
  `0.0018366352033811495`.

Every frozen Repair26 gate passes.

Scientific conclusion:

the Repair24/25 discrepancy is explained by the historical cancellation-prone alpha-coordinate first-order trace, not by a physical mode-dependent Fourier normalization. No Repair25 fitted scale is adopted.

The cancellation-free full-history first-order parent and its retarded z10/v10 boundary are now certified.

q20 is still not certified and H4/Z21 remains unlicensed.

Next licensed object:

a separately preregistered q20 reconstruction rerun that changes only the first-order bath parent from the historical v0.77 trace to the frozen Repair26 R1 cancellation-free trace/boundary.

Canonical project status:

**Repair22 Z20 CERTIFIED; Repair23 bath bridge PASS; Repair24 q20 historical FAIL; Repair25 localized the bridge discrepancy; Repair26 cancellation-free full-history bath boundary CERTIFIED; q20 NOT CERTIFIED; H4/Z21 NOT LICENSED.**


---

## Repair27 — cancellation-free-parent q20 reconstruction

Classification:

`GE19_REPAIR27_CANCELLATION_FREE_PARENT_Q20_RECONSTRUCTION_PASS`.

Route:

`CANCELLATION_FREE_PARENT_Q20_CERTIFIED`.

Result-freeze commit:

`514dc6b9d26d0b6b7360b7f3cbe1397371bb4baf`.

Frozen local outputs:

- JSON/FULL:
  `99a2183e7088c7492f624cae2d294612380714c1d81aa7ff49cc4fcd1c62c74b`;
- NPZ:
  `2b1566d402e4c9e8daee8e5c7084b3da7735442b4fb604d51489b708662fd9c0`.

The Repair26 cancellation-free R1 parent is used directly; the historical v0.77 trace is not used and no Repair25 fitted normalization is adopted.

All inherited Repair24 gates pass without modification:

- H1 X10 bridge:
  `3.981945660904338e-11 <= 1e-10`;
- G2 Nx256/Nx512:
  `3.4518767056924556e-15 <= 1e-10`;
- q20 Nq1024/Nq2048:
  `8.23684251511779e-05 <= 1e-2`;
- q20 Nt64/Nt128:
  `3.2441966579873734e-05 <= 5e-3`;
- z10 Nt64/Nt128:
  `2.567987045993896e-05 <= 5e-3`.

All outputs are finite and all cases complete.

Therefore q20 is now certified on the frozen window-local particular low-mode scope.

Repair24 remains historical FAIL.

Repair27 licenses a separately preregistered H4/Z21 construction.

Canonical project status:

**Repair22 Z20 CERTIFIED; Repair23 bath bridge PASS; Repair24 historical q20 FAIL; Repair25 localization complete; Repair26 cancellation-free first-order bath boundary CERTIFIED; Repair27 q20 CERTIFIED; H4/Z21 CONSTRUCTION LICENSED BUT NOT YET CERTIFIED.**


---

## Repair28 — cancellation-free complete first-order eta tangent

Classification:

`GE19_REPAIR28_CANCELLATION_FREE_FULL_STATE_ETA_TANGENT_FAIL`.

Workflow run:

`35723905248`.

Artifact:

`10692716361`.

Result-freeze commit:

`6616cb8c1d25edc85b6727a157ba30618c323857`.

Frozen outputs:

- JSON:
  `1fd3a4310ea737f6da0d16fa37572c175c26005f6a3ee3f84e5e74f9c82b05a0`;
- NPZ:
  `101c38d91344d12071ecb343c35769326f80975e013b7d159f573aae73879705`;
- FULL log:
  `694fda61ad3f460e79f32ea35ecf6fda0c2a5933f3230b766485518f82af8cc5`.

All preregistered gates pass except one:

- R1 even residual:
  `0.006093567316834002 > 0.005` — FAIL.

The corresponding R2 even residual is

`0.002932307980192869 < 0.005` — PASS.

Other important controls pass:

- R1 lambda affinity max:
  `0.0032350146226643416`;
- R2 lambda affinity max:
  `0.003920019104722244`;
- R1/R2 full-state consensus relative L2 max:
  `0.0021596786199411513`;
- a=0.4 R1/R2 state mismatch max:
  `3.757145306980154e-06`;
- R1/R2 chi11 relative L2:
  `3.0996811715058834e-07`;
- forcing 1024/2048 relative L2:
  `7.3452194491696035e-09`.

Interpretation:

the failure is localized to the even-in-lambda contamination of the coarser R1 signed runs. The tighter R2 level passes the same frozen gate and the R1/R2 tangent itself closes. This is suggestive of a precision effect, but Repair28 remains historical FAIL and no threshold is relaxed.

Next licensed step:

a separately preregistered Repair29 precision/localization audit of the Repair28 even residual before any reduced Z11 or H4/Z21 solve.

Canonical project status:

**Repair22 Z20 CERTIFIED; Repair26 first-order cancellation-free bath boundary CERTIFIED; Repair27 q20 CERTIFIED; Repair28 full-state eta tangent FAIL on one R1 even-residual gate; reduced Z11 NOT CERTIFIED; H4/Z21 NOT YET LICENSED.**


---

## Repair29B — R2-primary / R3-control complete eta tangent

Classification:

`GE19_REPAIR29B_R2_PRIMARY_R3_CONTROL_FULL_STATE_ETA_TANGENT_PASS`.

Workflow run:

`35744723602`.

Artifact:

`10701244502`.

Artifact digest:

`sha256:a52c1ff21d6a83cf122db412be40a223996015886e06007a03cf93080c3a1459`.

Result-freeze commit:

`b686e50a2a070113ca72b953a82eb868d0bbf841`.

Frozen outputs:

- JSON:
  `081a80fe892f9cddf5ad38a69e43b82c24887e67a8b26162a2d4a229d04f8890`;
- NPZ:
  `c97afa5f42e4066239955ac98475c70e37e14c8f0abc373050cc38bbf10c2f81`;
- FULL log:
  `e402030a244b2ae26d084a565cef4033abb90fb0cfe307d1c8944f874dd9c5e4`.

Repair29A froze target lambdas `[5.0,1.25]` and the tracked pairs:

- phi, lambda=5.0;
- phi, lambda=1.25;
- psi, lambda=1.25.

All Repair29B gates pass.

Key controls:

- R3/R2 same-lambda tangent relative L2 max:
  `0.0032949735424532643 <= 0.005`;
- tracked R3 even residual max:
  `0.0026472718092593337 <= 0.005`;
- all tracked R3 even residuals are <= their R2 values;
- forcing 1024/2048 relative L2:
  `7.3452194491696035e-09`;
- requested-k mismatch:
  `0.0`;
- background-grid mismatch:
  `0.0`.

Certified representation:

**R2 primary complete eta-tangent representation with targeted R3 numerical control.**

Repair28 remains historical FAIL and is not relabelled.

Next licensed step:

a separately preregistered reduced H2/Z11 reclosure on the Repair22/Repair27 reduced coordinate system using the Repair29B-certified R2 full-state tangent as reference/boundary parent.

Canonical project status:

**Repair22 Z20 CERTIFIED; Repair26 first-order cancellation-free bath boundary CERTIFIED; Repair27 q20 CERTIFIED; Repair28 historical full-state eta-tangent FAIL at coarse R1; Repair29A localization COMPLETE; Repair29B complete eta tangent CERTIFIED as R2 primary with R3 control; reduced Z11 NOT YET CERTIFIED; H4/Z21 NOT YET LICENSED.**


---

## Repair37 — cancellation-safe FD8 H4/Z21 reclosure

Classification:

`GE19_REPAIR37_CANCELLATION_SAFE_FD8_H4_Z21_RECLOSURE_FAIL`.

Result-localization freeze commit:

`8ef52885d33aac1f91bc75261d53ce8b3b4c54dc`.

Frozen outputs:

- JSON/FULL:
  `da8f2f00c22c866ec3f82381d23f69bf036e630fe2a29c5c44657984b760f61a`;
- NPZ:
  `572d8937c1d742b10da66e34cc076377c1b2feb20b8f72eb25c3eaf31a59829f`;
- outer runner:
  `e3ca1f3c049b45b320c5cdd7db752fa790ed5969de1f9ef350eed0ca72e64522`.

Repair37 is a historical valid FAIL and is not relabelled.

Repair37 closes both numerical targets inherited from Repair36:

- Lambda direct-vs-expanded exact bilinear audit:
  `1.9148071003126113e-16`;
- 9-point degree-8 exact GE06/GE07 nonlinear Euler-Lagrange
  `Dt @ partial` source assembly.

Exactly one gate remains false:

`H4_active_shift_Nt128_Linf_le_1e6`.

Frozen matched-shift values:

- Nt128 active Linf:
  `1.1749387207106255e-06`;
- Nt64 matched Linf:
  `1.1134127189405345e-05`;
- observed Linf order:
  `3.2077474489146236`;
- Nt128 active RMS:
  `1.0515104304068532e-06`;
- Nt64 matched RMS:
  `8.780910986609813e-06`;
- observed RMS order:
  `3.027380898364344`.

Frozen-NPZ localization shows:

- ~99.72% of active samples improve Nt64 -> Nt128;
- 100% of samples still failing at Nt128 improve;
- failed-sample pointwise order is approximately 2.95--3.03;
- the median per-mode active order is approximately 2.98055.

The frozen Repair07 propagation path uses PCHIP stage-source interpolation
and a two-stage Radau IIA march. After the FD4 source derivative is removed,
the remaining defect therefore has the expected approximately third-order
propagation signature.

The result is numerical, not evidence for a physical H4 inconsistency.

No Repair37 rerun, threshold relaxation or observational tuning is licensed.

Next licensed step:

a separately preregistered propagation-accuracy localization, keeping the
Repair37 physics, parents, source arrays, boundary and `1e-6` science target
fixed. Internal Radau substepping is the minimal first diagnostic; if that
plateaus, localize the PCHIP stage-source representation.

Canonical project status:

**Repair22 Z20 CERTIFIED; Repair27 q20 CERTIFIED; Repair32B/32C reduced Z11
CERTIFIED and H4 licensed; Repair33--Repair37 remain immutable historical
FAILs; Repair37 closes the Lambda-audit and FD4-source issues but exposes a
convergent approximately third-order propagation floor. Window-local
particular Z21 remains NOT CERTIFIED. Lensing remains blocked pending a
separately preregistered numerical reclosure.**


---

## Repair38 — frozen-source Radau substep localization

Classification:

`GE19_REPAIR38_FROZEN_SOURCE_RADAU_SUBSTEP_LOCALIZATION_COMPLETE`.

Valid-diagnostic freeze commit:

`ada593c99c7bc217313b1f7c8ff99504f13e8d10`.

Frozen outputs:

- JSON/FULL:
  `08dd95c614118c66e37349e2b8d058e85163812fed77c9b048e0ce57e339e5dd`;
- NPZ:
  `aff63771c1800b0db236cd020cf0d2772f6d9a0fd0328573d055392f2c60da67`;
- outer runner:
  `6e6b4477528ca63858a14f2fecf7bd2183498739b4c6a4d8db2d4cf3ba10dd16`.

Repair38 is diagnostic-only and does not relabel Repair37.

Factor-1 reproduces frozen Repair37 exactly:

- Z21 global relative L2:
  `0.0`;
- shift-metric global relative L2:
  `0.0`;
- projected p0 exact:
  `true`;
- frozen active sample count:
  `23850`.

All implementation gates pass.

Frozen active-shift results:

- substep 1 Linf:
  `1.1749387207106255e-06`;
- substep 2 Linf:
  `1.341600178925417e-06`;
- substep 4 Linf:
  `1.3797699672147026e-06`;
- substep 1 RMS:
  `1.0515104304068532e-06`;
- substep 2 RMS:
  `1.1859570854138313e-06`;
- substep 4 RMS:
  `1.2040175184159568e-06`.

The preregistered Radau-floor hypothesis is not confirmed. The frozen route is:

`PCHIP_OR_OTHER_FLOOR_REMAINS`.

Post-freeze NPZ localization shows that the propagated Z21 state itself
converges cleanly under substepping:

- ||Z1-Z2|| / ||Z2-Z4|| =
  `8.030548956166639`;
- observed state order =
  `3.0054986115619555`.

The complete shift-metric field differences also converge with the expected
third-order Radau signature:

- ||m1-m2|| / ||m2-m4|| =
  `7.9105878110222365`;
- observed metric-difference order =
  `2.983784900834436`.

Thus internal Radau discretization converges as expected, but toward a
nonzero shift floor. A report-only p=3 Richardson estimate gives a limiting
active Linf of approximately `1.385222794113172e-06` and limiting RMS of
approximately `1.2065975802734033e-06`.

This removes insufficient Radau internal step resolution as the leading
explanation for the Repair37 threshold miss.

Next licensed step:

a separately preregistered frozen-source stage-representation diagnostic,
keeping the same Repair37 source nodes, projected boundary, H4 operator and
`1e-6` science target fixed, and localizing the Repair07 PCHIP
source-at-stage representation against an independently frozen alternative
before any new science reclosure.

Canonical project status:

**Repair22 Z20 CERTIFIED; Repair27 q20 CERTIFIED; Repair32B/32C reduced Z11
CERTIFIED and H4 licensed; Repair33--Repair37 remain immutable historical
FAILs; Repair38 is a valid diagnostic COMPLETE result and excludes internal
Radau step resolution as the dominant remaining floor. Window-local
particular Z21 remains NOT CERTIFIED. Lensing remains blocked.**


---

## Repair39 — frozen-source stage interpolation localization

Classification:

`GE19_REPAIR39_FROZEN_SOURCE_STAGE_INTERPOLATION_LOCALIZATION_COMPLETE`.

Result-freeze commit:

`5c6740d3ca4dbc49f148c869a2cbcca092b844cb`.

Frozen outputs:

- JSON/FULL:
  `b058d4acb51dd4e0b964fcccb306b7eb105466941b5e0900ae0c84a29374624e`;
- NPZ:
  `0bf5b0c2f26cc06b98eab1fb326757ed409cf91c86c23e995251dfd32571c451`;
- outer runner:
  `d2470549728e2a34256753baa6330267ed1ba5df7d4ff23e8ffbbd1adf786504`.

Repair39 is diagnostic-only and does not relabel Repair37 or Repair38.

All implementation gates pass.

PCHIP factor4 reproduces frozen Repair38 substep4 with:

- Z21 relative L2:
  `3.7172606261726e-18`;
- active shift-metric relative L2:
  `3.882369515821824e-12`.

All three interpolation methods reproduce the frozen Nt128 source nodes to
approximately machine precision; the maximum nodal relative L2 is
`3.1222622128280023e-16`.

Frozen active shift results:

- PCHIP Linf:
  `1.3797699672147026e-06`;
- CubicSpline Linf:
  `1.4170655920646319e-06`;
- Akima Linf:
  `1.2068124462343292e-06`.

The frozen Repair38 PCHIP factor2-to-factor4 active-field difference RMS is

`2.4751527730021507e-08`.

Relative to that scale:

- CubicSpline/PCHIP active-field difference ratio:
  `3.4334457790648143`;
- Akima/PCHIP active-field difference ratio:
  `15.280884251999465`.

The preregistered route is therefore:

`STAGE_SOURCE_REPRESENTATION_DEPENDENCE_CONFIRMED`.

This establishes that the remaining shift floor materially depends on the
off-node H4 source representation. It does not identify a physically
preferred interpolant.

Because PCHIP and Akima slope construction is nonlinear in nodal data, the
next localization must decompose the Akima-PCHIP dependence into the six
frozen Repair37 H4 source pieces plus an explicit interpolation-coupling
residual.

Next licensed step:

Repair40 piecewise stage-source decomposition. No new Z21 science reclosure is
licensed until the leading source-representation target is localized.

Canonical project status:

**Repair22 Z20 CERTIFIED; Repair27 q20 CERTIFIED; Repair32B/32C reduced Z11
CERTIFIED and H4 licensed; Repair33--Repair37 immutable historical FAILs;
Repair38 excludes insufficient Radau internal resolution as the dominant
floor; Repair39 confirms material off-node H4 source-representation
dependence. Window-local particular Z21 remains NOT CERTIFIED. Lensing
remains blocked.**


---

## Repair40 — piecewise stage-source decomposition

Classification:

`GE19_REPAIR40_PIECEWISE_STAGE_SOURCE_DECOMPOSITION_COMPLETE`.

Valid-diagnostic freeze commit:

`bd9446feccb28779fa3f59bd0206e18d2ebaed4e`.

Frozen outputs:

- JSON/FULL:
  `f5618344db31328dc4e680eb41bb6a715da3fbe7e54ddff3cb53bc027386bf44`;
- NPZ:
  `06c7799787abcc510259c626bcb9ca925f96efce13c7949a89690f243fbf01b5`;
- outer runner:
  `112bffc28a638bff5a1148795068111475ee4781a923432b6b52cd5a34ec72f4`.

Repair40 is diagnostic-only. The initial Repair40 cancellation-contaminated
attempt remains immutable IMPLEMENTATION_FAIL and is not relabelled.

All Repair40 gates pass after repair01:

- PCHIP Repair39 reproduction exactly zero relative L2;
- Akima Repair39 reproduction exactly zero relative L2;
- frozen source-node reproduction max `5.669184795383803e-16`;
- stage-source decomposition closure `7.050062442856047e-19`;
- direct-delta Z21 response closure `2.8954027388379403e-14`
  under the unchanged preregistered `1e-9` gate;
- all outputs finite.

The two deterministic rankings separate the remaining representation
sensitivity:

- largest propagated Z21-response component:
  `2M1_GE05_mapped`;
- largest active shift-response component:
  `2Q_GE06_cross`.

The preregistered mandatory follow-up targets are therefore both:

- `2M1_GE05_mapped`;
- `2Q_GE06_cross`.

Frozen follow-up kind:

`DIRECT_FINE_GRID_RECONSTRUCTION_OF_TARGET_PHYSICAL_PIECES`.

For the shift-sensitive GE06 cross term, replacing only its stage
representation by the Akima-minus-PCHIP delta changes active Linf from
`1.3797699672147026e-6` to `1.2156072341464537e-6`, with active shift
difference RMS `3.3448872380344193e-7`, equal to about 88.4% of the full
Akima-minus-PCHIP shift response and aligned at `0.9896848662049436`.

For the mapped GE05 M1 term, the propagated direct-delta Z21 response has
relative norm `1.000000025452115` and complex alignment
`0.9999999999999967` with the full Akima-minus-PCHIP Z21 response, while
its direct shift-metric effect is negligible.

Next licensed step:

a separately preregistered fine-time reconstruction diagnostic for both
mandatory physical source targets. No new H4/Z21 science reclosure is
licensed before that direct target check.

Canonical project status:

**Repair22 Z20 CERTIFIED; Repair27 q20 CERTIFIED; Repair32B/32C reduced Z11
CERTIFIED and H4 licensed; Repair33--Repair37 immutable historical FAILs;
Repair38 excludes Radau step resolution as the dominant floor; Repair39
confirms off-node source-representation dependence; Repair40 localizes the
mandatory direct fine-grid targets to 2M1_GE05_mapped and 2Q_GE06_cross.
Window-local particular Z21 remains NOT CERTIFIED. Lensing remains blocked.**
