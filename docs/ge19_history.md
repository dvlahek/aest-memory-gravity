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


---

## Repair41 — direct fine-grid target source reconstruction

Classification:

`GE19_REPAIR41_DIRECT_FINE_GRID_TARGET_SOURCE_RECONSTRUCTION_COMPLETE`.

Route:

`DIRECT_TARGET_REFERENCE_RESOLVED`.

Valid-diagnostic freeze commit:

`1e1ffa694eb9661be72907f59b1de317d87f713d`.

Frozen outputs:

- JSON/FULL:
  `1b18fede26b021e077ffe5c8b6b7ff0dc727b4defaab48e63491c86d868d1320`;
- NPZ:
  `6bfb87ea21d55e2a1d2b16aee9bc8d7246111f91a064a78b74d2ed946ec2ba45`;
- outer runner:
  `8d9360c8bad9f7f7ed985957cf2230e0713715dd7057347feb10f31f5bee4375`.

Repair41 is diagnostic-only and does not relabel Repair37--Repair40.

All implementation gates and inherited fine-grid resolution gates pass.

Direct time grids:

- Nt382 = 3x subdivision of Nt128 intervals;
- Nt763 = 6x subdivision;
- original factor-1 Radau stage coordinate mismatch:
  `1.1102230246251565e-16`.

Fine382 versus fine763 target resolution:

- `2M1_GE05_mapped` stage-source relative L2:
  `6.169210815952087e-08`;
- `2Q_GE06_cross` stage-source relative L2:
  `1.0122348516611055e-05`.

Both are far below the inherited `5e-3` parent time-resolution ceiling.

Against the direct763 reference:

- M1 PCHIP relative L2:
  `2.104807968459713e-06`;
- M1 Akima relative L2:
  `2.0255490463534962e-06`;
- Q_GE06 PCHIP relative L2:
  `1.1217479471594003e-05`;
- Q_GE06 Akima relative L2:
  `1.1561946756579428e-05`.

For the shift-critical `2Q_GE06_cross`, PCHIP is slightly closer to the
direct reference. More importantly, the PCHIP-to-Akima source displacement
has alignment `-0.34747480302850875` with the actual PCHIP-to-direct
displacement. Therefore the prior Akima response is not a faithful proxy for
the true direct correction.

Next licensed step:

Repair42 direct-target H4 propagation diagnostic. It must preserve the frozen
Repair37 total-source baseline and projected p0, use factor-1 Radau because
Repair41 direct values are defined exactly at those stage coordinates, and
propagate direct382/direct763 corrections for M1 only, Q_GE06 only and both
targets. No new arbitrary threshold is introduced: threshold-side stability
is judged only against the existing `1e-6` science target.

Canonical project status:

**Repair22 Z20 CERTIFIED; Repair27 q20 CERTIFIED; Repair32B/32C reduced Z11
CERTIFIED and H4 licensed; Repair33--Repair37 immutable historical FAILs;
Repair38 excludes Radau step resolution as the dominant floor; Repair39
confirms off-node source-representation dependence; Repair40 localizes the
mandatory targets to 2M1_GE05_mapped and 2Q_GE06_cross; Repair41 resolves
their direct fine-grid stage references. Window-local particular Z21 remains
NOT CERTIFIED. Lensing remains blocked.**


---

## Repair42 — direct target H4 propagation diagnostic

Classification:
`GE19_REPAIR42_DIRECT_TARGET_H4_PROPAGATION_DIAGNOSTIC_COMPLETE`.

Frozen preregistered route:
`DIRECT_TARGET_CORRECTION_ABOVE_SCIENCE_TARGET`.

Valid diagnostic freeze commit:
`9a7fd6262832a44ca7d0d2cb73c322b856dcf514`.

Frozen artifacts:

- JSON/FULL SHA-256:
  `4a211581a77c1ad00e14cc398ca7a19b12642f3f3e35b416314d6721f5f81e25`;
- NPZ SHA-256:
  `a60515f3d92bbd388fd2fadae6cf2dd07f3ee68e8690b07632bbe5091e9013c5`;
- outer runner SHA-256:
  `855067c5f733374d98a97e5013c0f23ea1cfbcb1f62494a596beab9768cbcf9c`.

All Repair42 implementation gates pass; the frozen Repair37 factor-1
baseline is reproduced exactly in Z21 and shift metric, projected p0 is
exact, stage coordinates and stored target PCHIP are exact, and the active
mask remains 23850 samples.

The original science target is `1e-6` and is not relaxed.

Active-shift Linf:

- frozen PCHIP baseline: `1.1749387207106255e-6`;
- direct382 M1-only: `1.174938735937822e-6`;
- direct763 M1-only: `1.1749387364482247e-6`;
- direct382 Q_GE06-only: `4.755180483851141e-4`;
- direct763 Q_GE06-only: `1.4187840843421127e-4`;
- direct382 BOTH: `4.755180486721134e-4`;
- direct763 BOTH: `1.4187840851992924e-4`.

Both combined corrections are above the frozen science target, so Repair42
does not license a Z21 science reclosure.

Post-freeze NPZ localization identifies an early-window mode-8 active
hotspot at `ln(a)=-0.8989528773447014`, Nt128 time index 3, in each C
case and beta. At C_max/beta0, frozen shift scale is
`4.457554307372833e-12`. The direct382-minus-PCHIP Q_GE06 constraint
row0 correction has magnitude `2.1600003821566376e-15`, or
`4.845707383943654e-4` of that frozen scale. The direct763 correction is
`7.310994371678159e-16`, or `1.640135793653868e-4` of the scale.
Those ratios closely match the two observed normalized shift defects.
Global absolute shift residual maxima are smaller for both corrected runs
than for the frozen PCHIP baseline.

Thus the immediate open question is **Q_GE06 main-versus-constraint
source compatibility in the mixed fine-parent/coarse-total stage
representation**, not an established defect in the non-target physics.

Next licensed step:

Repair43 diagnostic-only Q_GE06 main/constraint stage-correction split with
exact reproduction of the Repair42 Q_GE06-only variants, absolute residual
and backward-error denominator localization, unchanged factor-1
propagation, projected p0, active mask and science target.

Canonical project status:

**Repair22 Z20 CERTIFIED; Repair27 q20 CERTIFIED; Repair32B/32C reduced Z11
CERTIFIED and H4 licensed; Repair33--Repair37 immutable historical FAILs;
Repair38--Repair42 valid diagnostic localization results. Repair41 resolves
the direct source targets; Repair42 shows that partial direct target
corrections violate the active shift threshold through an early-time
constraint-row sensitivity. Window-local particular Z21 remains NOT
CERTIFIED. Lensing remains blocked.**


---

## Repair43 — GE06 main-versus-constraint stage-source split

Classification:
`GE19_REPAIR43_QGE06_MAIN_CONSTRAINT_STAGE_SPLIT_COMPLETE`.

Preregistered route:
`QGE06_CONSTRAINT_ROW_FIELD_CLOSER_TO_FULL`.

Valid freeze commit:
`91446ddb1987e834200204cb6d8c4f8c4008a5be`.

Frozen JSON/FULL SHA-256:
`559ae65ffc5d21433799e4e33aa6d91237a9aa41b9799463971bc45dabecae44`.

Frozen NPZ SHA-256:
`d5c8c02c7f8272dc390ce9e4d2374a35b2ce1b14da5b60e69dc8366499bfe71c`.

Frozen runner SHA-256:
`640c9f31959d4e5290a26c64e0dee2ec982866d942135e5261d3828ecc0afc13`.

All implementation gates pass. Frozen Repair42 baseline and both direct
Q_GE06-only variants reproduce exactly in Z21 and active shift metric.

Repair43 finds that modifying the two GE06 constraint source rows together
is closer to the full corrected GE06 active shift field than modifying the
six GE06 main rows alone for both direct382 and direct763. The active Linf
values for constraint-family-only are `4.720762493838458e-4` and
`1.340570409265403e-4`; the original target remains `1e-6`.

The registered early-time m=8 hotspot is controlled by a tiny
direct-minus-PCHIP GE06 shift-constraint row0 source displacement relative to
the frozen local backward-error denominator. However Repair43 changed both
constraint rows together. The anisotropy constraint row1 is used in local
algebraic elimination, whereas row0 is an independent shift constraint
check, so a follow-up must split the two rows before assigning an error
mechanism.

Next licensed step: Repair44 diagnostic-only Q_GE06 shift-row-versus-
anisotropy-row source-stage split, with exact Repair43 constraint-family
reproduction and unchanged projected p0, operator, active mask and target.

Z21 remains NOT CERTIFIED; lensing remains blocked.


---

## Repair44 — GE06 shift-row0 versus anisotropy-row1 stage-source split

Classification:
`GE19_REPAIR44_QGE06_SHIFT_ANISOTROPY_ROW_SPLIT_COMPLETE`.

Preregistered route:
`QGE06_SHIFT_ROW0_FIELD_CLOSER_TO_FULL`.

Valid freeze commit:
`f2935ead5e27eb99498c1e53850f551bc1bb1426`.

Frozen SHA-256:

- JSON/FULL:
  `4f59f9a1aac21b267a00f75c5d5f0a0f791cfc20a4825f78b433729a4c50d435`;
- NPZ:
  `951694b7d83cdef312b766945b1f8a9844d1d6dd3a875929c5befc834c87f051`;
- outer runner:
  `ba532ceda0cb8b3fc7ba79699d49b95c3b1517061243500efc7257475dd77103`.

All 13 implementation gates pass. Frozen Repair43 baseline and both
direct-resolution full constraint-family variants reproduce exactly in
Z21 and shift metric. The source stage x and frozen target PCHIP checks
are exact, and the frozen active mask retains 23850 samples.

For both Nt382 and Nt763 the single-row intervention closer to the full
GE06 two-constraint-row active shift field is the independent shift
source row0, not anisotropy row1.

Shift-row0-only leaves all reconstructed Z21 states **exactly unchanged**
versus PCHIP baseline (maximum absolute difference 0.0). At the frozen
early-window C_max/beta0=1/m8/it3 hotspot the complex change in shift
constraint residual equals the negative injected shift-source delta
with an absolute identity defect of 0.0 for both resolutions.

This is a decisive localization of the mixed-representation intervention:
the frozen canonical solution is held fixed while the independent shift
constraint RHS is changed. The ensuing constraint residual is algebraically
expected and is not proof of erroneous GE06 source physics.

The corrected-row active Linf values remain above the untouched
`1e-6` science target. Repair44 is diagnostic-only; Repair37 remains
immutable science FAIL.

**Structural stop boundary:** no further one-row/interpolator patch
iterations. Audit the full H4 source shift/anisotropy/main-row and
Noether compatibility on a *common* parent/time representation before
any new integrated science Z21 reclosure. If the common-representation
source is inconsistent, revise the physical derivation separately and
preserve all historical artifacts.

Window-local particular Z21 remains NOT CERTIFIED. Lensing remains blocked.


---

## Current restart checkpoint — 2026-09-24, post-Repair44

**What is certified:** Repair22 Z20, Repair27 q20 and Repair32B/32C
reduced Z11. H4 was licensed for testing, but its window-local particular
Z21 is NOT CERTIFIED. Lensing remains blocked.

**What remains immutable:** Repair37 is the last valid H4 science FAIL;
Repair38--Repair44 are diagnostics, not science PASS results.

**Last completed diagnostic:** Repair44
`GE19_REPAIR44_QGE06_SHIFT_ANISOTROPY_ROW_SPLIT_COMPLETE`,
route `QGE06_SHIFT_ROW0_FIELD_CLOSER_TO_FULL`.
All implementation gates passed. Repair43 PCHIP baseline and the two
full GE06 constraint-family interventions reproduce exactly. Changing
only independent GE06 shift source row0 leaves Z21 exactly unchanged,
and the registered hotspot shift residual changes by precisely minus
the injected source delta. This localizes a selective mixed-
representation intervention; it is NOT proof that native fine-grid
GE06 or the complete H4 equations are inconsistent.

Frozen Repair44 artifacts and exact bytes:
`docs/ge19_repair44_valid_shift_row0_localization_freeze.md`.

**Do not continue with another isolated GE06 row/interpolator patch.**

Structural stop-gate and the required next task:
`docs/ge19_h4_source_constraint_noether_structural_stop_gate.md`.

Proceed by deriving the full H4 source/constraint Noether identity and
term-by-term row dictionary from the same frozen covariant action,
including GE06, GE07, Lambda, DY2, M1 and M2 and the on-shell
parent-equation terms. Test it on one common parent/time
representation, with an independent local early-time m8 check and the
original active mask/1e-6 science target unchanged.

If full-source structural compatibility passes, separately
preregister one integrated H4/Z21 science reclosure with independent
time control. If it fails, localize the failed derivation or
parent-equation relation and version the theoretical correction
without relabeling earlier results.

This checkpoint is the canonical answer to 'where did we stop?'
for the next conversation. The old Repair43 'next Repair44' line is
historical and is superseded by this checkpoint.


---

## Current structural checkpoint — 2026-09-24, after Repair44 and Stage A/B primitives

The post-Repair44 *numerical patch loop is closed*. This entry
supersedes the older historical "next Repair44" lines and the earlier
post-Repair44 restart checkpoint for the NEXT task.

**Valid Repair44 frozen diagnostic**

`GE19_REPAIR44_QGE06_SHIFT_ANISOTROPY_ROW_SPLIT_COMPLETE`,
route `QGE06_SHIFT_ROW0_FIELD_CLOSER_TO_FULL`.

Frozen result:
`docs/ge19_repair44_valid_shift_row0_localization_freeze.md`.

JSON/FULL SHA-256:
`4f59f9a1aac21b267a00f75c5d5f0a0f791cfc20a4825f78b433729a4c50d435`.

NPZ SHA-256:
`951694b7d83cdef312b766945b1f8a9844d1d6dd3a875929c5befc834c87f051`.

Shift row0-only keeps Z21 exactly identical to baseline at both direct
resolutions. The hotspot complex shift residual changes by exactly
minus the injected shift source; this is a selective mixed-source
operator identity, **not** a native fine-grid H4 physics failure.

**Stage A full H4 source-row ledger COMPLETE**

`docs/ge19_h4_structural_stage_a_source_row_ledger.md`.

All six H4 pieces and eight source rows are mapped to frozen generator
functions and residual conventions. GE05 M1 has zero constraint
source, but GE05 M2 has a genuine shift/anisotropy source.

An independent exact action-derived check shows that the GE05
second directional FLRW shift variation is `-a^3 dqt dqx`
before the frozen `-2` H4 mapping. This proves M2 shift
contributes and cannot be silently omitted in full-source
compatibility analysis.

**Stage B reduced spatial-Ward PRIMITIVES COMPLETE**

`docs/ge19_h4_structural_stage_b_reduced_ward_primitives_freeze.md`.

Successful GitHub analytic run:
`35979279801`, head
`35343dddaf7d8ceae889fd6c344e772f26f18a7f`.

Frozen JSON SHA-256:
`53feb4cad6da7d86edfe2dc1eeecbc932c26d81063951e1a9e52bf1db676da44`.

Ten reduced geometric/AeST/dust/per-node-memory building blocks
passed exact spatial transformation checks. The formal Ward
integration-by-parts signs, isotropic/anisotropy-to-longitudinal row
projection and exact GE05 memory shift variation also pass.

This is **NOT** a full covariant bath/Y2 or mixed H4 Noether
certificate. No H4/Z21 solve has been performed in this structural
audit.

**Frozen next analytic contract**

`ge19/h4_structural_stage_b_predata_action_noether_identity.json`.

NEXT: derive the complete reduced spatial-diffeomorphism Ward
identity from the frozen all-sector action before imposing
`L=R`. Validate the true NL0B bath-vector/projector
transformation, Y2 zero-set/boundary terms, and extract the
signed mixed H4 source/parent-residual coefficient.
Only after that proof is independently frozen may the
common-representation full-source numerical compatibility
test be preregistered. Do not introduce an isolated source
patch or relax the `1e-6` science target.

**Canonical status:** Repair22 Z20, Repair27 q20 and Repair32B/32C
reduced Z11 remain certified. Repair37 remains the immutable H4
science FAIL. Repair38--Repair44 are immutable diagnostic
localizations. Source-row ledger and restricted Ward primitives
are verified; the full H4 Noether source identity remains
UNPROVED. Window-local particular Z21 remains NOT CERTIFIED.
Lensing remains blocked.


---

## Current structural checkpoint — NL0C Y variational source-row gap, 2026-09-24

**New frozen analytic result:**
`GE19_H4_STAGEB_Y_AETHER_SOURCE_ROW_COVERAGE_GAP_CONFIRMED`.
Successful GitHub Action:
`35980659010`, job `107571474311`.

Frozen JSON SHA-256:
`6f20168f0fff685d697ce5a981754513a5c8733067c22ffbbf55f2e904c1ac46`.

Valid freeze:
`docs/ge19_h4_stageb_y_aether_row_gap_valid_freeze.md`.

The independent symbolic variation of the already frozen NL0C
`Y^(3/2)` action gives a nonzero **aether rapidity** Euler
source at H3 and a nonzero eta-tangent of that row at H4, for
generic first-order physical scalar gradient `g=Q u1+phi1_x/a`.
The frozen GE19 H3 `Y2` and H4 `DY2` builders explicitly
insert the nonanalytic Y source only into scalar main row3,
not aether main row2. GE06's analytic generator explicitly
excludes Y. This is a documented explicit action-to-source
coverage gap, **not** an interpolation or step-size failure.

Action-density second directional aether row:
`E_u^(20,Y)=-6*(2-KB)*c_beta*a^3*Q*Abs(g)*g`,
`c_beta=2/[3(1+beta)*a0]`.

The eta-tangent row is
`E_u^(21,Y)=-12*(2-KB)*c_beta*a^3*Q*Abs(g10)*g11`.

The historical results remain immutable: Repair37 science FAIL,
Repair38--Repair44 diagnostics, Repair22/27 and Repair32B/32C
certifications **for their preregistered implemented equations**.
The physical completeness of the H3/H4 source has NOT been
established for the full frozen NL0C variational action.

**Next licensed analytic step:** audit the raw action-density
versus volume-normalized GE19 scalar/aether Y source
conventions, including the H3/H4 factor-two mapping, and
produce a separately versioned complete variational Y
source dictionary. Do NOT inject a source into frozen
Repair37, relabel past results or attempt lensing.

The restricted Ward primitive audit passed, but the full
all-sector H4 Noether coefficient remains UNPROVED;
a complete integrated H4 source/constraint compatibility
check remains blocked pending this source dictionary.


---

## H4 structural Stage B — Y-sector variational source-row coverage gap (2026-09-24)

The frozen NL0C action-versus-GE19 source-row audit is valid:

`GE19_H4_STAGEB_Y_AETHER_SOURCE_ROW_COVERAGE_GAP_CONFIRMED`.

Verified GitHub Actions run `35980659010`, job `107571474311`, conclusion success.
Frozen JSON SHA-256:
`6f20168f0fff685d697ce5a981754513a5c8733067c22ffbbf55f2e904c1ac46`.
Artifact ID `10799504910`.

Freeze and complete claim boundary:
`docs/ge19_h4_stageb_y_aether_row_gap_valid_freeze.md`.

The action-derived second directional NL0C aether source and its
eta-tangent are generically nonzero, but the frozen H3 `Y2` and H4
`DY2` insertions populate only scalar main row3; GE06's analytic
generator explicitly excludes the nonanalytic Y sector.
The discrepancy is an explicit action-to-implementation source-row
coverage finding, not a complete H4 Noether proof or a valid
numerical correction.

**Important additional open question:** the raw longitudinal
action-density Euler rows and the existing GE19 physical-space
`y2_source` have not yet been shown to use the same volume,
global action and perturbative normalization. Do not insert the
raw symbolic expression into GE19 or change the solver until
these conventions are audited independently.

The earlier Repair22 Z20 / Repair32B--32C reduced Z11
certifications remain immutable as tests of their preregistered
implemented equations. Their promotion to certifications of the
complete variational NL0C theory is suspended pending a separately
versioned all-row dictionary and new appropriate parent reclosure.
Repair37 remains immutable science FAIL. Repair38--Repair44
remain diagnostics. Window-local particular Z21 is NOT CERTIFIED.
Lensing remains blocked.

**Next:** independently audit raw NL0C Y action-density Euler row
normalization against the exact GE06/GE19 raw equation and the
physical-space `y2_source` conventions. This is a small symbolic
audit (GitHub CI and optionally local) with no large local
H4/Z21 solver. After the resulting mapping is frozen,
version the full variational source dictionary and only then
determine which parent/reclosure gates must be rerun.


---

## Current restart checkpoint — Stage C Y action/source conventions (2026-09-24)

The post-Repair44 one-row numerical patch loop remains **closed**.
The newest structural findings supersede the earlier "next
full H4 Noether audit" paragraph as the immediate implementation
priority, without changing that full proof obligation.

**Stage B action-derived Y aether row gap:**
`GE19_H4_STAGEB_Y_AETHER_SOURCE_ROW_COVERAGE_GAP_CONFIRMED`,
GitHub run `35980659010`, frozen JSON SHA-256
`6f20168f0fff685d697ce5a981754513a5c8733067c22ffbbf55f2e904c1ac46`.
Freeze:
`docs/ge19_h4_stageb_y_aether_row_gap_valid_freeze.md`.
The frozen NL0C Y action has a nonzero H3/H4 aether rapidity
source, but the existing H3/H4 Y2/DY2 builders explicitly
populate only scalar main row3.

**Stage C exact geometric source convention:**
`GE19_H4_STAGEC_RAW_Y_VOLUME_FACTOR_ESTABLISHED_GLOBAL_NORMALIZATION_OPEN`.
GitHub analytic run `35982602472`, frozen JSON SHA-256
`76f6af0ec5f765c2cf6cf9f33a6cb35d3bd0b8dbfbdec18832955cd8cf5ccb55`.
Freeze:
`docs/ge19_h4_stagec_y_raw_ge19_conventions_valid_freeze.md`.

The exact raw reduced Y-sector scalar Euler second-directional
coefficient is `2*a^3*y2_code`, because the source code's
`y2_source` is a physical-space divergence while frozen GE06
assembles raw action-density Euler rows without an `a^-3`
conversion. The same geometric volume relation applies
to the Y eta-tangent source. The conditional same-volume
aether Y2 row is `-Q*kappa*|g|g`, with
`kappa=2(2-K_B)/[(1+beta)a0]` and
`g=Q*u10+phi10_x/a`. It is **not** yet licensed as a
numeric source correction because the full sector global
action normalization and integrated source dictionary
still require an independently versioned proof.

**Lightweight local verification is now available:**
`ge19/run_local_h4_stagec_y_raw_ge19_convention_audit.sh`.
Runner lock:
`docs/ge19_h4_stagec_local_analytic_runner_lock.md`.
Dedicated static runner audit: run `35982909486`, PASS.
It runs only the already verified symbolic audit and writes
`results/ge19_h4_stagec_y_raw_ge19_convention_audit_LOCAL.json`,
not an expensive H3/H4/Z21 solve.

**Next analytic action:** bind the exact relative NL0C
Y-sector versus GE06 GR+AeST action prefactor and any
Euler-row division convention from the unchanged frozen
full action. If that succeeds, preregister a separate
fully variational Y aether+scalar source dictionary and
appropriate parent reclosure. If it cannot be proven,
freeze a structural unresolved outcome; never fit to the
Repair37 shift residual.

Historical Repair22/27/32 certifications remain immutable
for their originally tested equations. They do not
silently certify an action-completed H3/H4 equation.
Repair37 remains immutable historical science FAIL;
Repair38--44 remain diagnostic localizations.
Window-local particular Z21 remains NOT CERTIFIED.
Lensing remains blocked.


---

## Current structural restart checkpoint — Stage C local PASS and Stage D common Y action (2026-09-24)

This is the newest canonical restart point. Earlier Stage B/C entries are
retained as immutable history and superseded here only for the NEXT task.

**Stage C local analytic reproduction: PASS**

Frozen user-provided local JSON and FULL are byte-identical, both 4759 bytes
with SHA-256
`76f6af0ec5f765c2cf6cf9f33a6cb35d3bd0b8dbfbdec18832955cd8cf5ccb55`,
identical to the successful CI result from run `35982602472`.

The outer local runner is 5512 bytes, SHA-256
`11f2621eb33e676de247cacd98999f431f2275c2a34c72fa555401b7ea3299b5`.
The local marker is `GE19_H4_STAGEC_LOCAL_ANALYTIC_PASS`.
Local provenance and claim boundary:
`docs/ge19_h4_stagec_local_analytic_reproduction_freeze.md`.

**Stage D common GR-anchored action normalization: PASS**

Classification:
`GE19_H4_STAGED_COMMON_GR_NORMALIZATION_AND_Y_ROWS_DERIVED`.

Successful dedicated GitHub Actions run `35984187949`,
job `107582874421`, JSON SHA-256
`2d900249d1e030a9b11b2b3d3e4b65ada8cbfb39a119b40ac0aba3ce10380d11`.
Result:
`docs/ge19_h4_staged_common_y_action_rows_valid_freeze.md`.

Exact action comparison: the frozen full NL1C6 AeST action minus the
GE06 memory-off analytic AeST action is exactly
`-N L R^2 (2-KB) J(Y)`. The canonical GR ADM kinetic
normalization matches; the only spherical-versus-plane GR
difference is the expected `+2 N L` unit-sphere curvature
term. The frozen NL0C covariant J action has the same
`1/(16 pi Gtilde)` Einstein-Hilbert prefactor. Thus the
relative NL0C/GE06 raw Y action factor is **1**; the
previously open common global normalization is now resolved.

With `kappa=2(2-KB)/[(1+beta)a0]`,
`g=Q u10+phi10_x/a`, the complete **Y-only** raw
H3 GE19 source RHS rows are

`S_phi,Y20=-2 a^3 (kappa/a) partial_x(|g|g)`,
`S_u,Y20=+2 a^3 Q kappa |g|g`.

The H4 eta-tangent rows on the unchanged background Q are

`S_phi,Y21=-4 a^3 (kappa/a) partial_x(|g10|g11)`,
`S_u,Y21=+4 a^3 Q kappa |g10|g11`.

The Y metric/shift source rows vanish at this order.
This is a versioned action-derived Y-sector dictionary,
**not** a patched historical H3/H4 calculation.

The frozen H3/H4 implementations insert scalar-only physical
Y2/DY2 terms without the raw action-density `a^3`
factor and no Y aether row. Therefore old
Repair22 Z20 and dependent Repair27 q20 must not be
promoted to the corrected full variational theory
without a new preregistered parent reclosure.
Repair32B/32C Z11 remains a certified result for
its original, linear-order equation; its compatibility
with the separately versioned Y-completed parent chain
must be explicitly checked rather than silently assumed.

**Stage D lightweight local reproduction runner (static PASS):**
`ge19/run_local_h4_staged_common_y_action_rows.sh`,
locked by
`docs/ge19_h4_staged_local_runner_lock.md`.
Dedicated static runner audit `35984559448` PASS.
The runner checks exact frozen source blobs and symbolic
claims and writes separate `_LOCAL` JSON/FULL files,
without invoking any H3/H4/Z21 state solver.

**NEXT:** write and lock a separate complete-Y-source module
implementing precisely the action-derived scalar+aether
H3/H4 rows (including zero-set and factor-of-two checks)
without touching old source files. Then preregister
the minimum required parent reclosure and a separate
all-sector H4 Noether/source compatibility test.
Do not restart isolated Repair37 source patches.

Repair37 remains the immutable historical science FAIL;
Repair38--Repair44 remain diagnostic-only.
Full all-sector H4 Noether identity is still unproved.
Window-local particular Z21 remains NOT CERTIFIED;
lensing remains blocked.


---

## Latest restart checkpoint — valid local Stage D and standalone Stage E Y source (2026-09-24)

This entry is the current canonical continuation point, superseding only
the NEXT-action text of the older Stage C/D checkpoints.
The original Repair37 science FAIL and all Repair38--44
diagnostic results remain immutable.

**Stage D local reproduction: PASS.**
The user-provided local JSON and FULL log are byte-identical
at 4876 bytes with SHA-256
`2d900249d1e030a9b11b2b3d3e4b65ada8cbfb39a119b40ac0aba3ce10380d11`,
exactly matching CI run `35984187949`. The uploaded
outer runner log has SHA-256
`2bc7bd4521874a616aa0bb64c59d85d3ada73866407075bec463d145b88a2ab0`
and 6728 bytes.
Terminal marker:
`GE19_H4_STAGED_LOCAL_ANALYTIC_PASS`.
Local freeze:
`docs/ge19_h4_staged_local_analytic_reproduction_freeze.md`.

**Stage E standalone complete Y-only source implementation: PASS.**
Preregistration and source contract:
`ge19/h4_stagee_predata_versioned_y_source_rows.json`.
Source implementation:
`ge19/h4_stagee_versioned_y_source_rows.py`.
Deterministic test:
`ge19/h4_stagee_versioned_y_source_selftest.py`.

The first CI run `35995106055` stopped before executing any
source tests because its path-based Python invocation could not
import the `ge19` namespace. It is frozen as
`GE19_H4_STAGEE_FIRST_CI_PREEXECUTION_IMPORT_FAIL` in
`docs/ge19_h4_stagee_first_ci_import_failure_freeze.md`.
The sole repair was to invoke the **unchanged** test with
`python3 -m ge19.h4_stagee_versioned_y_source_selftest`.

The valid CI run `35995241998` passed all preregistered
gates and is classified as
`GE19_H4_STAGEE_Y_SOURCE_ROW_DICTIONARY_IMPLEMENTATION_PASS`.
Frozen JSON SHA-256:
`c3ff4cc18dc8c7a69ba661a68ea3de987818f1b9c1db3275b08f2976c385896e`;
3371 bytes.
Full freeze:
`docs/ge19_h4_stagee_versioned_y_rows_valid_freeze.md`.

The standalone module returns six main GE19 rows
`[N,L+R,u,phi,T,rho]` and two constraint rows
`[shift,anisotropy]`. Only the Y-only u/phi rows are
nonzero. They implement the Stage D GR-anchored,
action-derived H3 and eta-tangent H4 RHS with the common
`a^3` raw action-density factor and one fixed
2/3-projected pseudo-spectral real-space flux.
All `beta={1,0.5,0.1}` tests, zero-set controls,
eta-tangent, frozen low-mode scalar comparators,
finite/shape/sign and invalid-input gates pass.
No historical H3/H4 file was changed.

**Lightweight local Stage E source test available:**
`ge19/run_local_h4_stagee_y_source_rows.sh`;
static runner audit `35995568675` PASS.
Local runner freeze:
`docs/ge19_h4_stagee_local_runner_lock.md`.
It does not run any parent/H4 solver.

**NEXT PHYSICS/NUMERICS GATE:** preregister a separately
versioned corrected H3/Z20 parent reclosure using *both*
action-derived Y u and phi rows, unchanged analytic
GE06/GE07/Lambda operator and unchanged projected
homogeneous-boundary convention. A corrected Z20 requires
reassessment of dependent q20 bath/memory parents and
independent time/source controls. Assess unchanged
linear H2 Z11 compatibility separately. Do not reuse old
Z20/q20 as a physically corrected variational parent.

Before any integrated science H4/Z21 run, check
the complete all-sector source/Noether identity on
one common parent/time representation; the standalone
Y-sector PASS is not such a proof.

No science target relaxation, observational tuning,
finite physical eta or lensing is licensed.
Window-local particular Z21 remains NOT CERTIFIED.


---

## Latest checkpoint — Stage E valid Y rows; H3F corrected Z20 preregistered (2026-09-24)

This is the newest canonical continuation point. Historical
repair classifications and earlier analytic stages are
preserved, not relabelled.

**Stage D local reproduction:** valid analytic PASS,
local JSON/FULL SHA-256
`2d900249d1e030a9b11b2b3d3e4b65ada8cbfb39a119b40ac0aba3ce10380d11`
(4876 bytes each); outer runner SHA-256
`2bc7bd4521874a616aa0bb64c59d85d3ada73866407075bec463d145b88a2ab0`
(6728 bytes).
Freeze:
`docs/ge19_h4_staged_local_analytic_reproduction_freeze.md`.

**Stage E new Y-only source implementation:** valid
`GE19_H4_STAGEE_Y_SOURCE_ROW_DICTIONARY_IMPLEMENTATION_PASS`.
Preregistration:
`ge19/h4_stagee_predata_versioned_y_source_rows.json`,
blob `e5ff7d12e963fa7487a1dff42ce06053f4b8d82e`.
New standalone source:
`ge19/h4_stagee_versioned_y_source_rows.py`,
blob `282166ea5840d7fba4dbc328d40d7687afa6fa0f`.
Deterministic test:
`ge19/h4_stagee_versioned_y_source_selftest.py`,
blob `05bbbb5d2dba2193adcbf468efc81eda6fb71ce6`.

First CI run `35995106055` was an import-path
PREEXECUTION FAIL, with no test result; frozen in
`docs/ge19_h4_stagee_first_ci_import_failure_freeze.md`.
Changing ONLY the Python invocation to `python3 -m`
produced valid CI run `35995241998`,
job `107618483762`, terminal marker
`GE19_H4_STAGEE_VERSIONED_Y_ROWS_PASS`.
JSON SHA-256
`c3ff4cc18dc8c7a69ba661a68ea3de987818f1b9c1db3275b08f2976c385896e`
(3371 bytes).
Freeze:
`docs/ge19_h4_stagee_versioned_y_rows_valid_freeze.md`.

The standalone implementation generates all six main
and two constraint Y-only RHS rows, nonzero only for
aether u and scalar phi. It uses exact Stage D raw
GR-anchored Y coefficients and the common projected
real-space `|g|g` flux at H3 and
`2|g10|g11` at H4, including zero-set continuity.
All `beta0={1,0.5,0.1}` source, shape, source-sign,
tangent, old-scalar-comparator, flux projection and
invalid-input tests pass. Neither frozen Repair07 nor
Repair37 was edited.

**Optional local source-only check:**
`ge19/run_local_h4_stagee_y_source_rows.sh`.
Dedicated static runner audit `35995568675` PASS.
Runner freeze:
`docs/ge19_h4_stagee_local_runner_lock.md`.
This does not execute a parent or H4 solver.

**Next corrected science parent H3F is preregistered only:**
`ge19/h3f_predata_action_completed_y_z20_parent_reclosure.json`,
blob `6ae1dd8c27ee1f94d85831cd5ae7b5ec21e3794e`.
Dedicated prelock run `35995943887` PASS.
Full contract and next steps:
`docs/ge19_h3f_corrected_y_parent_predata_lock.md`.

H3F must replace, not add to, the old scalar-only Y
source with the complete Stage E aether+scalar rows.
It keeps unchanged background, non-Y sources, on-shell
H1, beta/C/m grid and **original** active-shift
1e-6 / matched-order 2.5 science gates.
It keeps Repair18's *boundary projection algorithm*
but must recompute source-aware numerical p0,
not impose the old p0 from the different Y source.

H3F has **not** been implemented or run.
A valid new Z20 parent will require new dependent
q20 reconstruction with the unchanged normalized
bath equation and cancellation-free R1 history,
then complete all-sector H4 source/Noether compatibility
before any corrected Z21 science run.

Old Repair22/27/32 certifications remain valid
only for their original equations. Repair37 remains
historical science FAIL; Repair38--44 remain
diagnostic-only. Full H4 Noether certificate is
still open. Z21 is NOT CERTIFIED. Lensing is blocked.


---

## Latest checkpoint — local Stage E PASS; H3F source and Z20 science runner ready (2026-09-24)

This entry supersedes only the NEXT-task wording of older checkpoints.
No historical GE19 classification or numerical threshold is relabelled.

**Stage E local source reproduction: PASS (user-supplied terminal output).**

The user ran
`ge19/run_local_h4_stagee_y_source_rows.sh` and reported
`GE19_H4_STAGEE_LOCAL_LOCK_PASS`,
`GE19_H4_STAGEE_LOCAL_PREEXECUTION_PASS`,
`GE19_H4_STAGEE_LOCAL_SOURCE_ROWS_PASS`,
`EXIT=0`.
Local JSON/FULL: 3371 bytes each, both SHA-256
`c3ff4cc18dc8c7a69ba661a68ea3de987818f1b9c1db3275b08f2976c385896e`,
identical to successful Stage E CI run `35995241998`.
All three beta-case, exact frozen blob, zero-set,
source-row and numerical tangent gates report PASS.
The outer runner log was not attached as bytes; no
independent outer log SHA is claimed.
Freeze:
`docs/ge19_h4_stagee_local_source_reproduction_freeze.md`.

**New H3F source adapter: valid CI PASS.**

`ge19/h3f_corrected_y_source_adapter.py`,
blob `395294868191111b9b01201315cd2e6a30e47578`.
Dedicated CI run `35997209177`,
job `107624869369`, PASS. JSON SHA-256
`9f905b09ce4ba688410fe16e917e16724ec3b39cdb8af492a332a224a669bb9d`.
Freeze:
`docs/ge19_h3f_complete_y_source_adapter_valid_freeze.md`.

The adapter verifies unchanged GE06+GE07+Lambda
non-Y source and removes the complete historical
scalar-only Y contribution before injecting both
action-derived Stage E raw Y u/phi rows with the
fixed 2/3-projected common flux. It does not
modify old modules or reclose Z20 by itself.

**First full H3F science implementation: statically ready,
NOT LOCALLY EXECUTED.**

- on-shell H1/Z20 core:
  `ge19/h3f_corrected_y_parent_core.py`,
  blob `7e1da10ae8d79b6269b306f5483783de0fd3fd30`;
- science certification:
  `ge19/h3f_corrected_y_z20_science_reclosure.py`,
  blob `31e36aaf16c8d68f0ad1ffaff97459d67a23a8b0`;
- existing immutable preregistration:
  `ge19/h3f_predata_action_completed_y_z20_parent_reclosure.json`,
  blob `6ae1dd8c27ee1f94d85831cd5ae7b5ec21e3794e`;
- implementation lock:
  `docs/ge19_h3f_corrected_y_implementation_lock.md`;
- dedicated preexecution CI `35997860156`, PASS.

The science pipeline recomputes on-shell H1 at
Nt128/Nt64, rebuilds the source with new Y u/phi
rows and original analytic non-Y pieces, uses
the **original Repair18 p0 projection algorithm**
but recomputes numerical p0 from the new source,
and applies every original H3 active shift 1e-6,
matched order >=2.5, time/source-spatial,
boundary, linear and near-null gate.

A mandatory Y-disabled control replays the same
new parent core with historical Y restored and
must reproduce the old certified Repair22
Z20 and p0 arrays to <=1e-11 relative L2.
Old Repair18 p0 numbers are otherwise report-only
for the source-corrected run.

**Locked new local science runner:**

`ge19/run_local_h3f_corrected_y_z20_science_reclosure.sh`.

Static runner audit `35998084151` PASS.
Runner lock:
`docs/ge19_h3f_local_science_runner_lock.md`.

NEXT: run this exact local H3F science runner and
preserve its result as PASS, SCIENCE_FAIL or
IMPLEMENTATION_FAIL without conflation.
This is the first actual numerical recomputation
of a corrected-Y Z20 parent, not another old
GE06 shift-row source patch.

Even if H3F succeeds, old Repair27 q20 does NOT
automatically transfer to the changed Z20.
Recompute the dependent q20 with cancellation-free
R1 history and independently controlled time,
space and quadrature. A full all-sector H4
source/Noether compatibility test remains
required before any new Z21 science reclosure.

Historical Repair22/27/32 results remain valid
for their original equations; Repair37 science
FAIL and Repair38--44 diagnostics remain immutable.
Z21 is NOT CERTIFIED; lensing is blocked.


---

## Latest checkpoint — H3F corrected-Y Z20 SCIENCE PASS; H3G corrected q20 runner ready (2026-09-24)

This is the canonical continuation point. It supersedes
only the NEXT step wording of earlier checkpoints;
historical classifications, sources and science gates
remain immutable.

**H3F independently valid local science result:**
`GE19_H3F_CORRECTED_Y_H3_Z20_CERTIFIED`;
runner marker `GE19_H3F_NEW_Z20_SCIENCE_PASS`;
all preregistered science gates true, zero failed gates.
Freeze:
`docs/ge19_h3f_corrected_y_z20_valid_local_science_result_freeze.md`,
blob `e69fd766a36c219ecf46aa7bbf547a38c244f482`.

Exact user-uploaded local result SHA-256:

- JSON, 414800 bytes:
  `0616188d2bb7a6c09b2b56433a1f8a1860f360b2e54d2cb84e1ae214a407866b`;
- FULL log, 414800 bytes, byte-identical to JSON:
  `0616188d2bb7a6c09b2b56433a1f8a1860f360b2e54d2cb84e1ae214a407866b`;
- NPZ, 14181793 bytes:
  `90840755fa9febb1d8cb84609d9e58f67dec2a0a01cd6bf8e47685b45caa4542`;
- outer runner log, 9844 bytes:
  `c38599aba33efdee9106f7f6ce198701201da543f43a6ade72dbe7d798be4bf2`.

Independent local file checks found 62 finite
NPZ arrays. The mandatory Y-disabled control
reproduced original frozen Repair22 Z20 and
projected p0 at relative L2 0.0 each. Stage E
complete Y u+phi replaced the old scalar-only
Y term; original non-Y source and frozen
operator were not modified. The new source-aware
boundary projected p0 reproduces to 0.0 and
the old p0 difference is report-only
`3.473886544805647e-16`.

New H3F science metrics:

- source Nx1024/2048 relative L2 `1.396725754522341e-12`;
- Nt64/128 state relative L2 `1.5208749234474405e-05`;
- active Nt128 shift Linf `8.067171756100188e-07` against **unchanged** `1e-6`;
- matched active Linf and L2 orders
  `3.2357755676907107` and
  `3.1225511608309504` against `>=2.5`;
- near-null absolute residual/Sref
  `9.599035641086836e-15`.

Original all-row cancellation-prone shift
metrics are retained report-only, not confused
with the preregistered active/near-null
backward-error certification. This is
a separately versioned, low-mode, window-local
particular H3/Z20 result, not full GR
or observational certification.

**Next parent H3G: separately preregistered
corrected-Y normalized q20 reconstruction.**

- preregistration:
  `ge19/h3g_predata_corrected_y_q20_reconstruction.json`,
  blob `09fc1bd7fc06459d90fc6f6ba37a84adba757d37`;
- new core:
  `ge19/h3g_corrected_y_q20_core.py`,
  blob `688920e840a0a13bc85a6f416c2573cf0472eaa3`;
- R1/provenance wrapper:
  `ge19/h3g_corrected_y_q20_reconstruction.py`,
  blob `de929ae025e3ce58e60e6d229682cf885e7b1007`;
- H3G static preexecution `36013702448`, PASS:
  original Repair24 **all numerical physics helpers
  AST-identical**, all Repair27 constants/gates
  unchanged;
- new local runner:
  `ge19/run_local_h3g_corrected_y_q20_reconstruction.sh`,
  blob `bc46078cbbbce46f5955faa7d0e8037e19905a4b`;
- dedicated runner static CI `36014109845`,
  PASS `GE19_H3G_LOCAL_RUNNER_STATIC_PASS`;
- exact first-run instructions and provenance:
  `docs/ge19_h3g_local_q20_runner_lock.md`,
  blob `5faf30fd197c0ff23bcb731fcb90c322ffe19d94`.

H3G changes **only** the Z20 parent relative
to old Repair27: frozen Repair22 Z20 ->
new certified H3F action-completed-Y Z20.
The original Repair26 cancellation-free
R1 full-history bath trace, normalized
GE05 bath equations, q20 zero-particular
boundary and all time/space/quadrature
science thresholds remain fixed.
Historical Repair27 weighted q20 is
optional report-only comparator, NEVER
the new parent.

**H3G has not been numerically executed.
The first H3G local science run is NEXT.**
Freeze the first valid H3G science result
as PASS/FAIL or any implementation FAIL
separately.

A valid new H3G q20 parent will still
require a complete, independent, all-sector
H4 source/Noether compatibility certificate
on one corrected parent/time representation,
then a separately preregistered H4/Z21
science reclosure. The Stage E Y-only
row dictionary does not itself establish
full H4 compatibility.

Old Repair22/27/32 certifications remain
valid only for their original implementations.
Repair37 historical science FAIL and
Repair38--44 diagnostics are not relabelled.
**Z21 remains NOT CERTIFIED and lensing
remains blocked.**


---

## Latest checkpoint — H3G uploaded NPZ independently verified; H4F1 Ward PASS; H4F2 full-source prelock (2026-09-24)

This is the newest continuation point. Prior Repair22/27/32
certifications, Repair37 SCIENCE_FAIL and Repair38--44
diagnostics remain immutable. No old output, physical
coefficient, hotspot mask or 1e-6 science threshold
has been changed.

**H3F corrected-Y Z20:** previously certified
`GE19_H3F_CORRECTED_Y_H3_Z20_CERTIFIED`, with
JSON SHA-256
`0616188d2bb7a6c09b2b56433a1f8a1860f360b2e54d2cb84e1ae214a407866b`
and NPZ SHA-256
`90840755fa9febb1d8cb84609d9e58f67dec2a0a01cd6bf8e47685b45caa4542`.
Existing H3F valid freeze unchanged.

**H3G corrected-Y normalized q20:** first local run
`GE19_H3G_CORRECTED_Y_Q20_RECONSTRUCTION_PASS`,
all 13 frozen gates true, original Repair26 R1 trace
and full normalized GE05 bath equations unchanged.
H3G JSON SHA-256
`9b93534e3ee90e1ce588bdbd3f271afd041f738b8dc6f62c4ec0d1413c27f2c4`.
Original result freeze:
`docs/ge19_h3g_corrected_y_q20_valid_local_science_result_freeze.md`
(blob `e5b273a16a131be324162d3e66cf799e4ac543c3`).
At first freeze, H3G NPZ was not uploaded; that
historical limitation is retained in the original
freeze, but is now **closed by an append-only audit**.

**Independent H3G NPZ upload check:**

`docs/ge19_h3g_independent_uploaded_npz_audit_addendum.md`,
blob `01046254c9cfef2aba4fa285e1b42a2eba73820a`.

The subsequently uploaded NPZ is exactly 3550825
bytes, SHA-256
`9e1bf36e1d81122225ff8c03f663501de7601a8fc9376fd86312e0ae1d809452`,
identical to the first local runner. It has 30
numeric arrays, all finite. All 27 saved
per-(C,beta) Z20/X20/B20 norm values exactly
match the uploaded JSON (max relative defect 0.0).
All three weighted-z20 primary initial slices
are exactly zero; primary/time-control shapes
are (3,40,128)/(3,40,64). This independently
validates the stored result, **not** an
independent second numerical q20 propagation.

**H4F1 reduced covariant bath spatial Ward: analytic PASS.**

Classification:
`GE19_H4F1_LONGITUDINAL_BATH_WARD_COVARIANCE_DERIVED`.
Frozen result:
`docs/ge19_h4f1_longitudinal_bath_ward_valid_freeze.md`,
blob `5aa99f10383a253e934c0c2833230fa714c3ef1d`.
Dedicated GitHub run `36017517915`, job
`107693741610`, conclusion success, JSON SHA-256
`105797e68ebb50a2b9b9cbdb78434f48a9d6f0c387bfc9fd1bbff86b7af7ef8c`.

The frozen NL0B `U_j=q_j s` covector, NL1C3B
coframe and actual GE05 per-node action imply
`delta q=xi*q_x` for spatial relabeling xi(t,x).
Exact symbolic gates verify U_t/U_x covector,
aether A^t/A^x vector, A(q) and X_phi scalar,
orthogonality A.U=0, and
`delta L_mem=partial_x(xi L_mem)`.
This establishes the reduced bath transformation
assumption left open in the restricted Stage B
Ward primitives; it **does not** derive the
mixed H4 full-source Noether coefficient or
certify a numerical constraint residual.

**H4F2 complete signed mixed-Ward/source-parent proof: PREREGISTERED ONLY.**

Frozen predata:
`ge19/h4f2_predata_complete_mixed_h4_ward_parent_dictionary.json`,
blob `8097a4770ae8aed74cb4dd0721c1c9bd6907533c`.
Dedicated prelock `36017953067`, job
`107695217272`, PASS
`GE19_H4F2_COMPLETE_MIXED_WARD_PREDATA_PRELOCK_PASS`.

H4F2 must derive the **full off-shell and mixed H4
spatial Ward identity** with signed six-piece source
rows and every background/H1/Z11/corrected H3F
Z20/corrected H3G q20/dust/bath parent residual.
It must retain the Stage E complete Y u+phi
mixed eta-tangent source and exact GE05-to-GE06
factor-two conversion. It must separately
establish the GE07 dust density/multiplier gauge
transformation and the action boundary terms.
There is NO H4F2 analytic certificate yet.

Only after the exact H4F2 identity is independently
proved may a separately preregistered **common
corrected-parent/time** structural source evaluation
test the registered early-window shift hotspot and
original active window. That structural test is
separate from a subsequent H4/Z21 science solve.

**Window-local particular Z21 is NOT CERTIFIED;
lensing and observational predictions remain blocked.**


---

## Latest checkpoint — H4F2a–d partial Ward proofs; full six-piece source still open (2026-09-24)

This is the latest canonical restart point. It supersedes
only the NEXT-task wording of older history. Prior
Repair37 science FAIL and Repair38--44 diagnostics
remain immutable. The original 1e-6 active-shift
science threshold has not changed.

The corrected-Y H3F Z20 and H3G normalized q20
parents are separately certified within their
frozen scopes. H3G uploaded NPZ 3550825 bytes,
SHA-256
`9e1bf36e1d81122225ff8c03f663501de7601a8fc9376fd86312e0ae1d809452`
has 30 finite arrays and 27 exact JSON norm
comparisons (append-only audit already frozen).

The full H4F2 preregistration remains
`ge19/h4f2_predata_complete_mixed_h4_ward_parent_dictionary.json`,
blob `8097a4770ae8aed74cb4dd0721c1c9bd6907533c`,
prelock run `36017953067` PASS. **That full
six-piece analytic contract has NOT passed.**

**H4F2a: GE07 dust off-shell covariance PASS.**
Run `36019565065`, JSON SHA-256
`3154412e7e1e337d7efe2797498b56b58b0438c1c6fcd6c03c2629a591437259`.
Freeze:
`docs/ge19_h4f2a_dust_offshell_ward_valid_freeze.md`,
blob `ca21c65ce2da8d760aa12018aefd849b3b67adf9`.
Dust varrho is a spatial scalar multiplier,
not weight-one density; the entire GE07
Lagrangian is a density **off shell**.

**H4F2b: exact signed mixed Ward template PASS.**
Run `36019774035`, JSON SHA-256
`7168fa81eeceab720d6fdb4e9d3e5ad1d4682fadcfac310ef147a72d182f7ebc`.
Freeze:
`docs/ge19_h4f2b_signed_mixed_ward_template_valid_freeze.md`,
blob `98693317485149898830eebd0f335db12024e6dc`.
Exact `d_eta d_epsilon^2` coefficient
retains background/H1/Z11 Euler residual
products and the independent shift/anisotropy
row. The formal all-sector identity is
`W21=Sigma_i[E_i00 F_i21,x+
2 E_i10 F_i11,x+2 E_i11 F_i10,x]
-d_x B21-d_t E_b21=0`,
with the B21 and row-source sign explicitly
given in the frozen result. Actual six
source coefficients are still unbound.

**H4F2c: complete reduced action spatial covariance PASS.**
Run `36025455158`, JSON SHA-256
`3fbee288b3cbd062b5b0a255712266f07b332a093c3bf47ef7a1455856bd121a`.
Freeze:
`docs/ge19_h4f2c_complete_action_spatial_ward_valid_freeze.md`,
blob `831367d223c8081f49d87210841bd0b7ba3dfaa6`.
Actual-action source bindings and exact
symbolic tests establish spatial density
covariance separately for GE06 Einstein
ADM/plane-curvature, analytic AeST, NL0C
Y (both strict-sign branches), GE07 dust,
per-node NL0B GE05 bath and Lambda.
Together with H4F2b this supplies the
formal **reduced action-level** off-shell
spatial Ward identity. This does not
instantiate real mixed H4 source arrays.

**H4F2d: exact action-flux subidentity Y and M1 PASS.**
Preregistration
`ge19/h4f2d_predata_y_m1_flux_compatibility.json`,
blob `902310e1e623cf65c3bdd5c5ecb199263558a39c`.
Run `36026024031`, JSON SHA-256
`132e8589c1793bf5591beb2c638fe0d5cefb83713df561e4586d011dedec15c6`.
Freeze:
`docs/ge19_h4f2d_y_m1_action_flux_valid_freeze.md`,
blob `647d3a8cf207fbf18fef7e0cbdb23c9bfbfc5de8`.
The frozen Stage E Y and mapped GE05 M1
actual source rows satisfy
`d_x S_u+a Q S_phi=0`.
All three beta cohorts and Fourier-source
sign/row controls passed. The implemented
M1 depends on `B20=X20-weighted_z20`,
so H3G's certified weighted q20 projection
is sufficient for that implemented source.
This does not remove the need to retain
per-node bath Euler equations in the full
off-shell Noether identity.

**NEXT:** instantiate the remaining actual
GE06, GE07, Lambda and GE05 M2 mixed
H4 source rows under the frozen action,
together with the full signed
background/H1/Z11/corrected H3F Z20/
H3G q20/bath/dust parent-residual ledger.
Verify their aggregate mixed Ward
coefficient and independently establish
which parent equations, boundary terms
and row normalizations yield its on-shell
source condition. M2 has genuine shift
and anisotropy rows; do not infer
termwise Ward cancellation from Y/M1.

Only after a separately frozen **full
six-piece H4F2 analytic identity PASS**
may the common corrected-parent/time
structural source audit run. A subsequent
new H4/Z21 science run requires its own
predata/implementation lock.

**Z21 NOT CERTIFIED. Lensing blocked.**


---

## Latest checkpoint — H4F2e actual dust/M2/Lambda shift action PASS (2026-09-24)

This supersedes only the NEXT-task wording of the preceding
H4F2a--d checkpoint. All earlier results, including historical
Repair37 science FAIL and Repair38--44 diagnostics, remain
immutable. Corrected-Y H3F Z20 and H3G q20 are still certified
within their preregistered limited scopes.

**H4F2a--d remain valid restricted analytic/source results,
but the full six-piece H4F2 Noether identity is not yet proved.**

H4F2e preregistration:
`ge19/h4f2e_predata_dust_m2_lambda_shift_action.json`,
blob `a48ea8b15bf1c1141d9407c7400f416171f4b22b`.

First H4F2e CI run `36027249827` failed before
source/physics results because deterministic test
time axis `(5,1,1)` could not broadcast with
node/space `(3,1,256)`.
Immutable failure freeze:
`docs/ge19_h4f2e_first_ci_test_grid_implementation_failure_freeze.md`,
blob `e7bc1859ca0e509dc16e32d983dc6264fd2b781d`.
The only corrective implementation change was
time-axis placement `tt=np.arange(nt)[None,:,None]`;
no action/source coefficient, science target,
frozen parent or gate changed.

**Valid H4F2e CI PASS:** classification
`GE19_H4F2E_SHIFT_ACTION_SUBIDENTITY_PASS`,
run `36027647449`, job `107728145216`;
JSON SHA-256
`32b0fbc9cddd55d51b6380e6ad36c1da39229c8820974a00eb2837ca7bcf6dd2`
(3688 bytes).
Implementation:
`ge19/h4f2e_dust_m2_lambda_shift_action_audit.py`,
blob `7dab9b996fc97ca9a291eb90166babec1abfba23`.
Valid freeze:
`docs/ge19_h4f2e_shift_action_subidentity_valid_freeze.md`,
blob `79c81ebffeca490b9dad74d812005086daa04c32`.

This exact action-level subset establishes:
- GE07 dust independent shift Euler row
  `E_b,dust=-2 L R^2 varrho W T_x`,
  with frozen mixed H4 direct-vs-polarization
  and original RHS sign exactly verified;
- frozen GE05 M2 first-order bath
  `E_b,mem^(2)=-a^3 q_j,t q_j,x`
  per node; after the exact GE05-to-GE06
  factor two and RHS minus sign,
  `S_b,M2=+2a^3 sum_j(q_j,t q_j,x)`
  before `fft_low`. The actual frozen
  `f_c2["b"]` and Fourier low-mode
  implementation passed a deterministic
  three-node finite test;
- Lambda direct shift source vanishes
  identically from the frozen
  `-6 rho_lambda N L R^2` action.

This H4F2e PASS is **not** an aggregate
six-piece H4 Ward source/parent proof.
GE06 and GE07 actual full source rows,
the GE05 M2 anisotropy/bath parent
equations and complete background/H1/Z11/
corrected H3F/H3G parent residuals still
need to be instantiated in the signed
H4F2b formula on one consistent action/time
representation. Do not infer termwise
cancellation from the Y/M1 flux subsets.

**NEXT:** exact remaining GE06 independent
shift/anisotropy and all-sector source/
parent Euler ledger, followed by a separately
prelocked common corrected-parent/time
structural evaluation if and only if the
full mixed action identity is proven.

Original active-shift `1e-6`
science target remains unchanged.
Z21 NOT CERTIFIED; lensing blocked.


**H4F2e local source-only reproduction path locked (no local execution yet).**
Runner:
`ge19/run_local_h4f2e_dust_m2_lambda_shift_action.sh`,
blob `951a51bcaacb082b581323d8190220a1b7fa7599`.
Dedicated static audit run `36028343263`,
job `107730493210`, PASS.
Lock/instructions:
`docs/ge19_h4f2e_local_shift_action_runner_lock.md`,
blob `323daba75e37fde0f0f243d5fbdf669e12e63d7c`.
The runner executes GE05/GE07 module-level
generators from an isolated temporary working
directory so they do not overwrite historical
project `results/` files; it creates only
new H4F2e `_LOCAL` outputs. It performs NO
corrected-parent/H4 state solve. A local
PASS would reproduce only the H4F2e action
subset, not the full H4F2 certificate.



---

## Latest checkpoint — H4F2f GE06 Ward/shift source valid Actions PASS (2026-09-24)

**The user requested Actions-only progress while away from
the local computer. No local run is required for H4F2f.**

All previously frozen corrected-Y H3F/Z20 and H3G/q20
science certifications, the independent H3G NPZ audit,
and H4F2a–e restricted action/ward PASS results remain
unchanged. The original Repair37 H4/Z21 science FAIL
and Repair38–44 diagnostic-only results remain immutable.

**H4F2f GE06 action/shift subset is now valid PASS.**

Preregistration:
`ge19/h4f2f_predata_ge06_shift_ward_mixed_source.json`,
blob `551294c5763b086919c9f27076a922c29ca953e5`.

Valid audit implementation:
`ge19/h4f2f_ge06_shift_ward_mixed_source_audit.py`,
blob `49e7546e5ccb76d27436486f8baddd2a4d17956e`.

Valid dedicated workflow:
`.github/workflows/ge19-h4f2f-ge06-ward-shift.yml`,
blob `17415c334d93d1e46374eca02eb9beb9e184bc11`.

Successful GitHub Actions run `36037212512`,
job `107760180126`, commit
`5f5d14d332b6d1da4b86d95d53ec4767df0029ad`,
terminal marker
`GE19_H4F2F_GE06_SHIFT_ACTION_SUBSET_PASS`.
Result artifact ID `10825093346`.
JSON/FULL are the source-only H4F2f artifact
outputs; JSON is 4200 bytes, SHA-256
`b6aca9808ae36eaebea2356c0f3443e571e6ede8a4c0436be7cd80bf2bc3eb40`.

Valid result freeze:
`docs/ge19_h4f2f_ge06_ward_shift_valid_freeze.md`,
blob `3ea436c1f535d9477847bb690c7b5fc7652951d2`.

All exact frozen source pins, ten GE06 unreduced
coframe-jet scalar/density transformations,
actual frozen action/source bindings and
both independent `b_f`/`b_x` mixed
action-source partial tests PASS. Actual
frozen generator source-only relative L2
differences are `0.0` and
`1.6592729300491167e-16`, both below
the unchanged `1e-9` numerical gate.

Previous failed executions are **preserved
without retrospective relabeling**:

- `36030973726`: audit half/full directional
  coefficient gate definition mistake
  (first failure freeze retained);
- `36031713914`: stale static code-blob
  preexecution failure;
- `36031753394`: actual tests pass but
  raw aggregate incorrectly treats exact
  zero numeric error as Boolean false;
  freeze `docs/ge19_h4f2f_second_ci_numeric_truthiness_failure_freeze.md`;
- `36036837437`: corrected audit produces
  exactly the final 4200-byte PASS JSON,
  but Actions post-audit repeats the
  same incorrect numeric truthiness
  assertion; freeze
  `docs/ge19_h4f2f_third_ci_workflow_numeric_truthiness_failure_freeze.md`.

The successful Actions run fixes ONLY
the workflow post-audit metric aggregation,
with the preregistered GE06 action,
existing source generators, parameters,
H4 shift threshold, repaired audit physics
and all historical science outputs unchanged.

**NEXT:** build the actual complete six-piece
H4 source-plus-parent Euler residual ledger,
using H4F2a–f exact restricted results,
the signed H4F2b mixed Ward template,
Stage E both u+phi Y source rows, GE05
factor-two mapping, GE07 dust and Lambda
all-row entries, and the corrected certified
H3F/H3G plus compatible frozen H1/Z11
on one parent/time representation.

No full all-sector mixed H4 source/Noether
identity or common-grid compatibility PASS
exists yet. No H4/Z21 numerical science
reclosure was performed by any H4F2
source-only Actions run.

Original active shift `1e-6` target
is unchanged. **Z21 NOT CERTIFIED.
Lensing blocked.**


---

## Latest checkpoint — H4F2g signed six-piece source ledger PASS, full Noether still open (2026-09-24)

The user requested continuation through GitHub Actions while
away from the local machine. No new local execution was required.

All previously frozen H3F corrected-Y Z20 and H3G corrected-Y q20
science certifications remain immutable. H4F2a--f action/source
subsets remain independently valid. The original Repair37 H4/Z21
science FAIL and Repair38--44 diagnostic results are not relabelled.

**H4F2g is a valid signed six-piece source-only PASS.**

Preregistration:
`ge19/h4f2g_predata_six_piece_signed_source_ward_ledger.json`,
blob `70bee663a0f529a734b586dbc8b9f6e90bc8ed9f`.

New, separately versioned source assembler:
`ge19/h4f2g_action_completed_six_piece_source_ledger.py`,
blob `d9778da0bb6cc52a15015238810c79978527ffc5`.

Selftest:
`ge19/h4f2g_six_piece_source_ledger_selftest.py`,
blob `eb33a29e4be5975cef65b5ea62ac94b79d51114d`.

Dedicated successful GitHub Actions run `36049303037`,
job `107800548909`, terminal marker
`GE19_H4F2G_SIX_PIECE_SIGNED_SOURCE_LEDGER_PASS`,
artifact ID `10830265260`.
The 8172-byte JSON SHA-256 is
`34151f1e886477f1a08546d9a493ee9e418a8890d72c006d9f7e26583176596d`.

Full result freeze:
`docs/ge19_h4f2g_signed_six_piece_source_ledger_valid_freeze.md`,
blob `9bb8d66ee6f04ec893b6523a9ce8a44c9c0867b8`.

For beta0={1,0.5,0.1}, the new source-only
assembler retains exact GE19 eight-row ordering,
five external source families and generates
the sixth from **actual frozen Stage E Y source_h4**
with BOTH u and phi rows, replacing the old
Repair37 scalar-only DY2. The actual frozen
M1 source generator is also exercised.
The GE06, GE07, Lambda and M2 numerical
arrays in this particular unit test are
deterministic synthetic controls, not
certified corrected-parent source evaluations.

The signed source Ward projection is
`D_S21=d_t S_b21+(a/3)d_x(S_iso21+2S_aniso21)`.
The test verifies exact zero Y/M1 metric
constraint projections, nonzero Lambda
isotropic/ward contribution despite
zero direct Lambda shift, preservation of
GE07 shift and M2 anisotropy, correct
six-piece summation and deterministic
negative input controls.

A source-only `D_S21` is **NOT**
the complete H4 Noether identity.
No corrected-parent fields were sampled,
and neither the linear-operator Ward
remainder nor the signed background/H1/Z11/
H3F Z20/H3G q20/dust/bath Euler residual
was evaluated. The historical frozen
Repair37 source builder still has the
old scalar-only Y term and old parent
arrays, so cannot be relabelled.

**NEXT:** separately preregister and
execute the complete signed continuum/
discrete source-plus-operator/parent
Ward-residual evaluation with one
common corrected H3F/H3G/H1/Z11
representation. Existing FD8 GE06/GE07
and FD4 GE05 temporal sources must
be audited together before any H4
science solve. The original active-shift
`1e-6` target remains unchanged.

**Full H4 Noether NOT CERTIFIED.
Z21 NOT CERTIFIED. Lensing blocked.**


---

## Latest checkpoint — H4F2h physical-clock PASS and H4F3 integrated Ward prelock (2026-09-24)

This is the latest canonical restart point. All previously certified
H3F corrected-Y Z20 and H3G corrected-Y q20 results, and H4F2a--g
restricted action/source PASS results, remain unchanged. The original
Repair37 Z21 science FAIL and Repair38--44 diagnostics are immutable.

**New explicit physical-clock defect isolated:** GE19 stores
`x=ln(a)` and physical `d_t=H(x)d_x`. Frozen Repair37 uses
`Dt=H[:,None]*FD8_x` for GE06/GE07/Lambda, while frozen
Repair07/GE05 memory uses `Dt=H[:,None]*FD4_x`. The H4F2g
source-only helper's `np.gradient(S_b,time)` is a valid
synthetic coordinate test, but passing GE19 `bg['x']` directly
would compute d/dln(a) instead of d/dt and introduce second-order
FD in place of frozen FD8/FD4. Do NOT feed H4F2g's generic
source-only Ward output to the physical H4 parent/constraint
identity without the independently checked clock bridge.

**H4F2h physical clock / discrete source Ward: valid Actions PASS.**

Predata `ge19/h4f2h_predata_physical_clock_discrete_ward_bridge.json`
blob `dc5b29219d25c89d18b1bc37a7ce116f3818e349`.
Implementation `ge19/h4f2h_physical_time_source_ward_bridge.py`
blob `65ce1e68a2f77e063c4bb8848d770abb4baeeebf`.
Selftest `ge19/h4f2h_physical_time_source_ward_selftest.py`
blob `248dc1e815d345b56ff51d065327773518a9a0ae`.
Successful dedicated GitHub Actions run `36053845610`, job
`107815811239`, marker
`GE19_H4F2H_PHYSICAL_CLOCK_DISCRETE_SOURCE_WARD_PASS`.
JSON SHA-256 `efb37f8dc66188183995ecd9909396cf58fee8ec8b819bb2a5301f4a1bca21f7`.
Valid freeze:
`docs/ge19_h4f2h_physical_clock_source_ward_valid_freeze.md`,
blob `13e508d6b9bea96cc8be25aef991df03d55d8cf3`.
All frozen source/clock, six manufactured Nt64/Nt128 beta tests,
FD8/FD4, wrong-clock negative controls and source-family
linearity checks passed. This is not an actual corrected-parent
or H4/Z21 science computation.

**H4F3 integrated full corrected-parent Ward audit: PREREGISTERED ONLY.**

Predata `ge19/h4f3_predata_integrated_corrected_parent_ward.json`,
blob `3e17163cb6f52f3a78c41e6f37f83ef682359162`.
Dedicated prelock workflow run `36054356467`, job
`107817504286`, PASS
`GE19_H4F3_INTEGRATED_PARENT_WARD_PREDATA_PRELOCK_PASS`.
The actual integrated operator/source/parent residual evaluator
has NOT been implemented or executed. Full off-shell-to-on-shell
H4 Ward identity, physical common-grid discretization and the
original early-window shift hotspot remain open.

NEXT: implement ONE integrated H4F3 structural test from actual six
source families and independent canonical operator, on the exact
certified H3F/H3G/H1/Z11 physical parent/time grid. Preserve the
formal H4F2b background/H1/Z11/Z20/q20/dust/bath Euler residuals
and boundaries, and use H4F2h's physical H*FD8/FD4 differentiation.
GitHub Actions alone cannot consume the local H3F/H3G binary
artifacts unless those exact files are made available to the workflow;
do not imply that the static CI already tested physical parents.

Only after one separately frozen full structural Ward PASS may
ONE new preregistered H4/Z21 science reclosure run. The original
active-shift target `1e-6` and matched order >=2.5 remain unchanged.
**Full H4 Noether NOT CERTIFIED; Z21 NOT CERTIFIED; lensing blocked.**


---

## Latest checkpoint — H4F3a actual H3F/H3G binary interface partial PASS (2026-09-24)

The H4F3 full operator/source/parent Ward evaluator is still NOT
implemented and has not been run. The frozen H4F3 preregistration,
H4F2a--h restricted PASS results, certified corrected-Y H3F Z20,
certified corrected-Y H3G q20, and original Repair32C Z11
classification remain unchanged. Historical Repair37 Z21 SCIENCE_FAIL
and Repair38--44 diagnostics are immutable.

**Actual H4F3a input-interface audit on real uploaded binaries:**
`GE19_H4F3A_H3F_H3G_BINARY_INTERFACE_PASS_Z11_REQUIRED`.

- code: `ge19/h4f3a_actual_parent_array_interface_audit.py`,
  blob `0b4fb3ca120f54fef3b53aab452511d374062b68`;
- true-data report:
  `results/ge19_h4f3a_actual_parent_array_interface.json`,
  blob `0e7fa9969e9c46490bf81b0073b4d4fcfcb41ae1`,
  2695 bytes, SHA-256
  `77777bf942e771c3f22dff7f43651b6f944af58790e0353e5919c9972fd7a4c9`;
- freeze:
  `docs/ge19_h4f3a_real_parent_binary_interface_valid_partial_freeze.md`.

Four actual user-provided H3F/H3G JSON/NPZ files passed **exact**
previously frozen SHA-256 and original certification checks.
The H3F and H3G physical parent `x=ln(a)` grids are
elementwise identical at Nt128 and Nt64, with zero mismatch
and the original C/beta/m cohorts. Every C has finite H3F
Z20, H1, H3G weighted q20, X20 and B20 arrays with
registered shapes; weighted q20 is exactly zero initially,
and `B20_linear=X20-weighted_z20` holds elementwise
with maximum absolute defect **0.0** for every C.

The locally executed script has the same exact Git blob
as the newly committed script. The actual source files
were read in the active runtime; **the binary files were
not uploaded into GitHub Actions**. The dedicated static
attestation workflow `.github/workflows/ge19-h4f3a-parent-interface-static.yml`,
run `36056344500`, job `107824177598`, PASS, verifies only
the script, original H4F3 parent hashes and committed true-data
report. Do not equate Actions' static PASS with a second physical
binary run.

**OPEN INPUT:** no exact frozen Repair32B `Z11` NPZ
(SHA-256 `5d4a0a72c08d09d096a8de0b428b3c8443fc33e8ad442ed6d997d6bf2bc6e327`)
was available among the current conversation's mounted
files or indexed conversation/Library file searches.
That original certified result remains valid in the
user's existing local scientific pipeline. The new
auditor accepts `--z11-npz` to verify the exact hash,
Nt128/Nt64 time grids and all C-case Z11/Z11dot shapes
once the existing frozen local file is supplied.

**NEXT ONE INTEGRATED PHYSICAL GATE:** finish the H4F3
input binding including Z11, the original Repair13 H(x)
background and frozen first-order R1 bath; instantiate
all six **actual** corrected-parent H4 RHS families on
one common time representation; evaluate independently
the canonical linear-operator Ward term and all signed
background/H1/Z11/H3F Z20/H3G q20/dust/bath Euler
residuals and boundaries, using the frozen H4F2h
physical H*FD8 / H*FD4 schemes. Do not substitute
H4F2g synthetic sources or old Repair37 parent data.
Retain the original active shift target `1e-6`.

No full H4 Noether PASS or H4/Z21 science solve exists.
**Z21 NOT CERTIFIED; lensing blocked.**


---

## Latest checkpoint — H4F3b real corrected six-source adapter preexecution PASS, local science pending (2026-09-24)

H4F3a established that the **actual** certified H3F/H3G
binary parents share exactly the same Nt128 and Nt64
x=ln(a) grids and that
`B20_linear=X20-weighted_z20` holds elementwise
with maximum absolute discrepancy 0.0. H4F3a's
three-parent input gate remains incomplete
because the exact historical certified
Repair32B Z11 NPZ was not present among the
current conversation's mounted files.
The original Repair32B/32C Z11 science
classification itself is unchanged.

**The first actual H4F3b corrected six-piece
source implementation is now preregistered
and statically audited, but NOT numerically
executed.**

- preregistration:
  `ge19/h4f3b_predata_actual_corrected_six_piece_source.json`,
  blob `c3362f5360c2a9951d77060027c82830c031c145`;
- source-only implementation:
  `ge19/h4f3b_actual_corrected_six_piece_source.py`,
  blob `0423cbc64f6cda3b2a9aeb67c734935ef3ae7f9c`;
- exact local runner:
  `ge19/run_local_h4f3b_actual_corrected_six_piece_source.sh`,
  blob `ef0fd6656add30cec667dda0d7bc9a435c3a2562`;
- first-run lock:
  `docs/ge19_h4f3b_corrected_actual_six_source_implementation_lock.md`.

Dedicated preexecution workflow
`36057797491`, job `107829030982`,
conclusion PASS
`GE19_H4F3B_ACTUAL_CORRECTED_SIX_SOURCE_PREEXECUTION_PASS`.
Dedicated static local-runner workflow
`36058048497`, job `107829870394`,
conclusion PASS
`GE19_H4F3B_LOCAL_RUNNER_STATIC_PASS`.

Both CI executions compile/import and inspect
frozen input/source/clock/no-Z21 contracts.
**Neither consumes the user's real H3F/H3G/Z11
binary data or evaluates an actual H4 source.**

The new code must compute actual source rows on
one certified H1/Z11/corrected H3F Z20/
corrected H3G q20 parent/time grid:

`2Q_GE06_cross`,
`2Q_GE07_cross`,
`2Q_Lambda_cross`,
`2DY2_action_complete_Y_u_and_phi`,
`2M1_GE05_mapped`,
`2M2_GE05_mapped`.

It reuses the original frozen Q and M2
action evaluators without invoking the
historical Repair37 source-builder or
Z21 solver; reconstructs q10 from the
exact Repair26 R1 bath trace and checks
its weighted projection against the
certified H3G q10; uses H3G's corrected
weighted q20 and a recomputed Nt64
B20; replaces scalar-only old DY2 with
actual Stage E aether+scalar Y rows.
The physically clocked signed source
projection uses H4F2h's separate
H*FD8 and H*FD4 schemes.

**NEXT ONE ACTUAL RUN:** on the user's
original local scientific setup, use
the locked H4F3b runner (exact command
in its implementation lock). It must
fail closed if frozen Z11 NPZ or any
corrected parent or Repair26 R1 hash
is missing or differs. Freeze the
first valid actual six-source PASS/FAIL
without fitting or lowering gates.

A source-only PASS will not certify
full H4F3: the independent canonical
linear-operator Ward residual,
background/H1/Z11/corrected Z20/q20/
dust/per-node bath Euler residuals
and boundary contributions must still
be evaluated consistently on that
same representation.

The original active H4 shift target
`1e-6` and matched temporal order
`>=2.5` remain unchanged.
Historical Repair37 SCIENCE_FAIL and
Repair38--44 diagnostics remain immutable.
**Full H4 Noether NOT CERTIFIED;
Z21 NOT CERTIFIED; lensing blocked.**


---

## Latest checkpoint — H4F3b synthetic production wiring PASS; actual Z11 still required (2026-09-24)

This is the newest canonical restart point. The already certified
corrected-Y H3F Z20 and H3G q20, the independent uploaded H3G
NPZ array audit and H4F2a--h restricted analytic/source-clock
PASS results remain immutable. Original Repair37 H4/Z21
science FAIL and Repair38--44 diagnostic classifications
remain unchanged.

**H4F3b actual corrected-parent six-piece source calculation:**
its existing implementation and local runner are unchanged
and statically PASS, but the true physical source run
has **NOT** occurred. The original frozen Repair32B
Z11 NPZ is missing from the currently accessible
conversation/Library/mounted data. The required SHA-256 is

`5d4a0a72c08d09d096a8de0b428b3c8443fc33e8ad442ed6d997d6bf2bc6e327`.

The historical Repair32B workflow runs
`35758781356` and `35758540985`
contain no downloadable numerical artifact.
Do not claim that Actions has the missing Z11
or substitute a made-up parent.

**New H4F3b production-path manufactured wiring runtime: valid CI PASS.**

Preregistration:
`ge19/h4f3b_predata_synthetic_production_wiring.json`,
blob `7121c2fa7ca2502dbf66923a2522fb2340003ee3`.

Unmodified true source wrapper:
`ge19/h4f3b_actual_corrected_six_piece_source.py`,
blob `0423cbc64f6cda3b2a9aeb67c734935ef3ae7f9c`.

New integration selftest:
`ge19/h4f3b_synthetic_production_wiring_selftest.py`,
blob `2daf44fa2377495eed69a7272727478426a585ad`.

Dedicated successful GitHub Actions run `36060197350`,
job `107837030623`,
classification
`GE19_H4F3B_SYNTHETIC_PRODUCTION_WIRING_PASS`,
4703-byte JSON SHA-256
`4c015f242cbbd97628c4775b4e1978b80c9d95a1e650830485aceb3c608ffd49`,
artifact `10833717959`.
Full implementation, provenance, first three
audit attempts and strict claim boundary:
`docs/ge19_h4f3b_synthetic_production_wiring_valid_freeze.md`,
blob `564211a52941976015dfec81e30618d3aacb5d3f`.

The actual frozen H4F3b source-wrapper path,
r7 complex Fourier reconstruction, M1(B20),
actual Stage E u+phi Y, H4F2g source assembly
and H4F2h H*FD8/H*FD4 physical source-Ward
were exercised with manufactured external
GE06/GE07/Lambda/M2 fixtures. All three
beta cases have exact zero six-piece
assembly and physical source-Ward sum
defects. Wrong q10 and inconsistent
physical time controls reject correctly.

This is **engineering/integration certification
only**, not an actual H3F/H3G/Z11 six-piece
source evaluation, nor a full Noether PASS.
The first two CI failures were caused by the
test expecting two instead of the actual
four GE06/GE07 direct+swapped cross calls
in the nominal and negative-control paths.
The third run was a stale workflow blob lock.
The valid final run changed only the test
call-count expectation and workflow pin,
not any frozen source, physical parameter
or historical science output.

**NEXT PHYSICAL EXECUTION:** obtain the exact
existing frozen Repair32B Z11 NPZ and run

`ge19/run_local_h4f3b_actual_corrected_six_piece_source.sh`

on the original hash-locked local H3F/H3G,
R13 and R1 bath parent files. This does
NOT run a H4/Z21 state solver.
Freeze the actual six-piece source
PASS/FAIL before deriving/evaluating the
independent linear-operator plus signed
all-parent Euler/boundary H4 Ward identity.

The original active-shift threshold
`1e-6` and matched-order threshold
`>=2.5` remain unchanged.
**Full H4 Noether NOT CERTIFIED.
Z21 NOT CERTIFIED. Lensing blocked.**


---

## Latest checkpoint — H4F3c genuine frozen mixed generators launched; exact Z11 still required (2026-09-25)

Certified H3F corrected-Y Z20, H3G corrected-Y q20,
independently uploaded H3G NPZ, original certified
Repair32B/32C Z11 **classification** and all H4F2a--h
restricted analytic/action/source-clock results remain
unchanged. The exact certified Repair32B Z11 NPZ
with SHA-256
`5d4a0a72c08d09d096a8de0b428b3c8443fc33e8ad442ed6d997d6bf2bc6e327`
has still not been supplied among the mounted
conversation/Library files. Do not relabel
a synthetic manufactured Z11 as that certified parent.

**New H4F3c preregistration and genuine frozen
source-generator manufactured Actions execution:**

- predata:
  `ge19/h4f3c_predata_real_generator_manufactured_runtime.json`,
  blob `2fab9aafd16aa6ea6b11fa6dafff3f3394d97061`;
- deterministic **manufactured**, NOT real-parent,
  selftest:
  `ge19/h4f3c_genuine_frozen_q_lambda_manufactured_selftest.py`,
  blob `be3b1d29f3f3a6110883ede801c99d121a2755ee`;
- dedicated workflow:
  `.github/workflows/ge19-h4f3c-genuine-frozen-mixed-generators.yml`,
  blob `bfcc469f34f6a0596d46ade27bec594bf2e45fbd`;
- workflow run `36096862132`, started
  `2026-09-25T05:02:05Z`;
  at this checkpoint, `status=in_progress`,
  final PASS/FAIL NOT YET KNOWN.

This Action executes the **actual frozen**
GE06/GE07 mixed-Q and Lambda source generators,
symbolic bilinear function maps, exact
polarization and direct-vs-swapped real
Fourier source evaluators on two deterministic
smooth Nt16/Nt32 manufactured backgrounds.
It does NOT mock these three expensive
source functions as the previous H4F3b
synthetic wiring test did. It does not
evaluate the real corrected-parent H4
source, independent canonical operator
Ward or all-parent Euler residual terms.
No successful H4F3c result has been claimed
from a merely running workflow.

The existing H4F3b true physical local
runner is `ge19/run_local_h4f3b_actual_corrected_six_piece_source.sh`.
Run it only on the user's exact frozen
H3F/H3G/R13/R1 parents and exact original
Repair32B Z11 NPZ, with the lock and SHA
gates left unchanged. This source-only
test precedes independent complete H4
operator+parent Noether and any subsequent
separately preregistered Z21 science solve.

Historical Repair37 H4 science FAIL and
Repair38--44 diagnostics remain immutable.
Original active shift `1e-6` and temporal
order >=2.5 remain unrelaxed. Full all-sector
H4 Noether and Z21 are NOT CERTIFIED;
lensing blocked.


---

## Latest checkpoint — actual H4F3b corrected six-source PASS and H4F3d full operator/parent Ward preregistration (2026-09-25)

This supersedes only older NEXT text. Preserve all original Repair22/27/32
certifications, Repair37 H4/Z21 SCIENCE_FAIL and Repair38--44 diagnostics
without relabeling. No source scale, active mask, hot spot or frozen
science threshold was adjusted.

**Actual local H4F3b source on corrected certified physical parents: PASS.**

User uploaded all four local H4F3b results. Their SHA-256 and byte counts
were independently verified from mounted files:

- JSON: 17898 bytes,
  `1ec88fd3fd6b81bf30614b0cb78d722a02dd4f745e1f22cb9b8f956a44bac6c1`;
- FULL log: 17898 bytes, byte-identical to JSON, same SHA-256;
- NPZ: 30913364 bytes,
  `787d5d177838b05078057aa932f379dd529449ce203f5664c36cf723acb0116b`;
- outer runner log: 3180 bytes,
  `411c72f0c54557c69883718082e030b1158cdb6fdfb6e1702abf45510e222179`.

Classification:
`GE19_H4F3B_ACTUAL_CORRECTED_SIX_SOURCE_PASS_FULL_WARD_OPEN`;
terminal marker
`GE19_H4F3B_ACTUAL_SIX_SOURCE_PASS_FULL_WARD_OPEN`;
all eight frozen gates true, no failed gates.
Full result freeze:
`docs/ge19_h4f3b_actual_corrected_six_source_valid_local_freeze.md`,
blob `578768817615807260afc2d7baaa24d2c4928858`.

Independent NPZ inspection: **146 finite numeric fields**, with all
18 original C/beta/Nt cohorts. Every total source has shape
(8,Nt,41), with all six actual source families and physical
source-only Ward arrays. The exact maximum absolute defect between
total source and direct sum of six saved source rows is **0.0**
across all cohorts. The maximum saved physical *source-only*
Ward magnitude is `3.610734858956584e-12` (Nt64);
this number is **report-only, not a smallness/pass gate**.

The original H3F/H3G/Z11, R13 and R1 hashes were checked by the
locked local runner. The user's original scientific environment
supplied the exact certified Repair32B Z11 NPZ that had been absent
from the conversation's mounted files. That missing-conversation-
attachment note is now superseded for the genuine local H4F3b
execution, but the exact original Z11 binary is not automatically
available on GitHub Actions. Old scalar-only Y and Repair27 q20
were not consumed; the Stage E action-complete Y u+phi rows were.

**H4F3c genuine unmocked generator manufactured CI: PASS.**

Previously launched workflow `36096862132` is now confirmed completed
successfully, job `107950837089`, marker
`GE19_H4F3C_GENUINE_FROZEN_GENERATORS_MANUFACTURED_PASS`.
JSON SHA-256:
`5c0288cbf836dcc260e7d0029ae644cb733dd2e141a0128595c70633d2c57992`;
artifact `10848180381`.
Frozen manufactured generator result:
`docs/ge19_h4f3c_genuine_mixed_generators_manufactured_valid_freeze.md`,
blob `a9f929203a072dae66d50d8781f64440e2ede184`.
This independently executes the genuine frozen GE06/GE07/Lambda mixed
generators on *manufactured* inputs; it is not a separate
physical-parent H4F3b run or a Noether certificate.

**NEXT integrated structural gate H4F3d: PREREGISTERED/PRELOCK PASS,
NOT YET IMPLEMENTED OR SCIENTIFICALLY EXECUTED.**

Preregistration:
`ge19/h4f3d_predata_actual_operator_all_parent_ward_closure.json`,
blob `f1bd4eb52b7da96ac2d50ed9136e3e1a74635f51`.
Dedicated prelock workflow
`36101803617`
passed at latest commit `b368073cc71cc9d3e291707566a69edf05e5d8a3`.

H4F3d must use the **exact actual H4F3b source NPZ** and the
same certified on-shell H1/Z11/corrected H3F Z20/H3G q20 and original
GE07 dust/Repair26 R1 per-node bath parents. Derive and evaluate
independently the original canonical linear-operator Ward term,
all signed background/parent Euler residual products, action boundary
terms and original six-piece source Ward on the same physical x=ln(a)
grids. Use the frozen H*FD8/H*FD4 source family derivative schemes,
original GE19 operator convention and registered early
C_max/beta=1/m8/index3 hotspot. A small source Ward on its own is
neither a full identity nor a science PASS.

The physical H4F3d structural tolerance needs its **own pre-data
derivation from the signed Ward identity and FD discretization error**.
Do not retrospectively fit it to the H4F3b source-Ward magnitude,
or substitute the later H4/Z21 active-shift target (unchanged 1e-6).
Only after a separately frozen full actual operator+parent Ward
structural PASS may a new Z21 science solver be preregistered.

**Full H4 Noether NOT CERTIFIED; Z21 NOT CERTIFIED; lensing blocked.**


---

## Latest checkpoint — H4F3d1 actual canonical operator Ward compiler PASS; full H4F3d physical Ward OPEN (2026-09-25)

The original certified corrected-Y H3F Z20, H3G q20, historical
Repair32C Z11 and valid **actual** H4F3b six-source PASS remain
immutable. H4F3c manufactured genuine-generator Actions PASS and
H4F2a--h restricted analytic/source-clock PASS remain unchanged.
Historical Repair37 H4/Z21 SCIENCE_FAIL and Repair38--44 diagnostics
are not relabelled. All original H4 science thresholds stay fixed.

**New H4F3d1 signed original canonical linear-operator Ward compiler:
valid analytic/engineering CI PASS.**

- classification:
  `GE19_H4F3D1_CANONICAL_OPERATOR_WARD_COMPILER_PASS`;
- preregistration:
  `ge19/h4f3d1_predata_frozen_canonical_operator_ward.json`,
  blob `4577de495692ecbe4c07d1156ffab2abfc99e96d`;
- code:
  `ge19/h4f3d1_frozen_canonical_operator_ward.py`,
  blob `60786ac14c9478801c5df9ccf458ead9a34ac827`;
- dedicated GitHub Actions run `36102755011`,
  job `107968605067`, conclusion `success`;
- JSON SHA-256
  `f87f77dc02ccef3862c539a4e14aa5f67b78a2c68fbb5592fb9df71a979919e6`,
  4239 bytes, artifact ID `10849404814`;
- frozen result:
  `docs/ge19_h4f3d1_canonical_operator_ward_valid_freeze.md`,
  blob `605a163fb9fa7e59e9babdbfdc279022b95d038a`.

The original frozen unconstrained GE06+GE07 Cmat 16x10
row semantics fix the **full independent L Euler row**
as

`E_L=[Cmat[6]+2(Cmat[12]+Cmat[13])]w/3
        -H FD4_x(Cmat[14]w)`,

and the independent shift Euler row as

`E_b=(Cmat[10]+Cmat[11])w`.

The signed canonical linear-operator Ward is

`W_operator=-H FD4_x(E_b)-ik a E_L`,

NOT an isolated zero/source-smallness condition.
Critically the FD4 derivative applies to the complete
`Cmat(x)w(x)` momentum product. The original
`pS=pL+pR` identity is retained and the
`E_L=(E_iso+2E_aniso)/3` projection and frozen
`E=L-S` RHS sign are exact.

Nt64/Nt128 complex manufactured polynomial
FD4 product tests and negative controls for
omitting pL momentum, omitting the background
Cmat time derivative and misusing the isotropic
row all passed. This **does not** evaluate the
actual corrected physical Cmat on the actual H4F3b
parent grid or prove a full mixed H4 Noether identity.

**NEXT physical structural work under already frozen H4F3d predata:**
instantiate this exact original operator on the
verified actual common H1/Z11/H3F Z20/H3G q20,
H4F3b six-source and Repair26 R1 data, AND
independently derive/evaluate every signed
background/parent dust/bath Euler residual
and action boundary contribution. Preserve the
separate H*FD8/H*FD4 source derivatives and
original operator FD4. Preregister structural
tolerance from the signed identity and
FD truncation before the first integrated
physical execution. A source-only Ward
magnitude is report-only, NEVER a gate.

The actual H4F3b NPZ and historical Z11 original
binary were supplied in the user's previous
scientific environment but are not automatically
present on GitHub Actions. No fake
manufactured parent can replace the
hash-locked actual physical input.

**Full H4F3d operator+all-parent Noether structural
PASS has NOT been produced. Z21 NOT CERTIFIED;
lensing blocked.**


---

## Latest checkpoint — H4F3d2 dust/bath Euler current compiler PASS; actual full H4F3d still open (2026-09-25)

This is the newest canonical restart point. Historical original-equation
Repair22/27/32 certifications, actual corrected-Y H3F Z20 and H3G q20
PASS, H4F3b **actual physical six-source** PASS, and H4F3c genuine
generator manufactured CI PASS remain immutable. Original Repair37
H4/Z21 science FAIL and Repair38--44 diagnostics are not relabelled.
Original active-shift threshold 1e-6 and matched-order >=2.5 are fixed.

**Previously frozen H4F3d1 canonical operator Ward: PASS.**
Run `36102755011`, code
`ge19/h4f3d1_frozen_canonical_operator_ward.py`,
blob `60786ac14c9478801c5df9ccf458ead9a34ac827`;
result freeze
`docs/ge19_h4f3d1_canonical_operator_ward_valid_freeze.md`.
It reconstructs exactly original independent shift and complete L Euler
rows, physical `H*FD4_x` on the full product `Cmat(x)*w(x)`,
and `W_operator=-H FD4_x(E_b)-ik a E_L`.
This alone is not full H4 Ward.

**New H4F3d2 frozen GE07 dust/GE05 bath Euler-current analytic and
engineering CI: PASS** under the pre-existing H4F3d full structural
preregistration.

- prereg `ge19/h4f3d2_predata_dust_bath_parent_euler_currents.json`,
  blob `6e9f83fc7f245bfedb82db53afd96ab2ba8616db`;
- compiler `ge19/h4f3d2_dust_bath_parent_euler_currents.py`,
  blob `42b2405759402195ffb371056d9e48b70dcded71`;
- successful dedicated Actions run `36103744644`, job
  `107971628320`, marker
  `GE19_H4F3D2_DUST_BATH_PARENT_EULER_COMPILER_PASS`;
- JSON SHA-256
  `60ff08c7ed0e47e8e52184d56c1ef329b834f1868f45e16aa8e424186df86c36`,
  artifact `10849674680`;
- immutable result freeze
  `docs/ge19_h4f3d2_dust_bath_parent_euler_currents_valid_freeze.md`.

The compiler evaluates only source-pinned original GE07 and GE05
symbolic action assignments, not their output-generating campaigns.
It independently derives both dust T and GE05 q_j temporal/spatial
currents, the exact dust rho multiplier Euler equation, first-order
FLRW perturbation coefficients, first-order metric shift/L contributions
and signed physical epsilon^2 eta mixed Ward parent coefficients
for T, rho and every bath q_j. The GE05 per-node results remain
**raw action** results; the eta-rescaled normalized bath convention
still needs binding in the full integrated proof. Exact symbolic
and independent deterministic manufactured derivatives all passed.

A first predata draft mistakenly contained an extra rho0 in
`E_rho10`. It was explicitly corrected **before implementation
testing** in commit `2d57f1cbb7574ff6218ced4c0ec904d876eb76ed`.
The valid formula is
`E_rho10=2a^3(dTt-dN)`; rho is a Lagrange multiplier.
No posthoc source fit, data-dependent control or numerical
physics change was made. Full provenance is in the result freeze.

**NEXT decisive H4F3d work:** independently derive the remaining
Einstein/analytic AeST/Y, dust/bath metric/aether/scalar parent Euler
and action boundary terms (including the normalized GE05 q_j
convention), and then execute the *complete* signed all-sector
operator+six-source+all-parent+boundary identity on exact common
physical Nt128/Nt64 corrected-parent grids. The structural FD4/FD8
truncation tolerance must be justified and frozen independently
before comparing the full physical residual.

The exact original local H4F3b result (JSON/NPZ) and original
Repair32B Z11 binary are not stored in current GitHub Actions
checkout or current mounted conversation files, even though
the user successfully supplied them in the prior scientific
local execution. Do not invent, replace with a manufactured
Z11, or claim a physical integrated Actions result using only
manufactured fixtures. The full valid H4F3d cannot be completed
on Actions until exact physical inputs are accessible there
or the hash-locked full audit is executed locally.

**Full H4 Noether structural PASS NOT YET PRODUCED;
Z21 NOT CERTIFIED; lensing blocked.**


---

## Latest checkpoint — H4F3d4 complete formal eta Ward PASS; actual-grid all-parent H4F3d open (2026-09-25)

This supersedes only outdated NEXT-step text. All historical original-equation
Repair22/27/32 results, corrected-Y H3F Z20/H3G q20 certifications,
Repair37 H4/Z21 SCIENCE_FAIL, Repair38--44 diagnostics and frozen
active-shift <=1e-6 / matched-order >=2.5 science thresholds remain
immutable.

**Actual corrected six-piece H4 source H4F3b: local PHYSICAL source-only PASS.**
All 18 C/beta/Nt cohorts and the exact original certified Z11 were
used in the user's local execution, with 146 finite NPZ fields and
exact source=six-piece sum. Frozen result:
`docs/ge19_h4f3b_actual_corrected_six_source_valid_local_freeze.md`,
JSON SHA-256
`1ec88fd3fd6b81bf30614b0cb78d722a02dd4f745e1f22cb9b8f956a44bac6c1`,
NPZ SHA-256
`787d5d177838b05078057aa932f379dd529449ce203f5664c36cf723acb0116b`.
Its source-only Ward is report-only and must NOT be independently
required to vanish.

**H4F3d1 canonical original-operator Ward: PASS.**
Run `36102755011`; retains full Cmat product derivative and the
original independent shift and L Euler row semantics.

**H4F3d2 dust/bath original-action Euler currents: PASS.**
Run `36103744644`; freezes signed dust rho/T and per-node bath
currents/parent coefficients before physical eta regularization.

**H4F3d3 physical eta-regularized bath Ward parent: PASS.**
Run `36105927210`, frozen in
`docs/ge19_h4f3d3_eta_regularized_bath_ward_valid_freeze.md`.
For the actual frozen `U_j=sqrt(eta)q_j`, the GE06 raw mixed
bath parent coefficient is exactly
`+4 sum_j E_qj10,GE05 * q_j10,x`.
It does not introduce a direct `q20` parent product in the
physical mixed coefficient. The exact first-order bath residual must
still be evaluated on the actual parent grid and must not be silently
dropped as zero.

**NEW H4F3d4 FULL FORMAL signed eta-corrected Ward ledger: PASS.**
Successful dedicated GitHub Actions run `36106532215`, job
`107980223264`, classification
`GE19_H4F3D4_FULL_FORMAL_ETA_WARD_LEDGER_PASS_ACTUAL_GRID_OPEN`.
Frozen result:
`docs/ge19_h4f3d4_complete_formal_eta_ward_valid_freeze.md`,
blob `e237626532a24bad792e5f892d4b2127fdc51e6f`.
Result JSON SHA-256
`d6fd4f79910b552238756eb9015e6a7956a8fa0892cb2a46a9bd9e2e7c8d5694`.
The complete *formal off-shell* signed mixed identity is
`W_operator + W_six_source + W_all_parent = 0`, including
all nonbath background/H1/Z11 Euler terms, action boundary terms,
correct physical bath `+4 E_q10 q10,x`, original canonical GE19
operator row projection and all six physical-clock source families.
This is an exact symbolic/source-binding result, NOT actual physical-grid
all-parent Noether certification and NOT a Z21 solve.

**NEXT decisive structural obligation under existing H4F3d predata:**
implement and preregister an *independent actual-grid* evaluation of
all Euler parent residual and action boundary arrays on the SAME
certified H1/Z11/H3F Z20/H3G q20/Repair26 R1 Nt128/Nt64 grids as
actual H4F3b six-source NPZ, with original Cmat operator FD4 and
separate source-family FD8/FD4 derivatives. Its independent numerical
Ward structural tolerance must be derived/frozen from the formal
identity and truncation errors BEFORE inspecting the physical residual.
Only an integrated full structural PASS permits a separately preregistered
new H4/Z21 science solver attempt; it is not itself a science PASS.

**Execution blocker:** the exact original certified Repair32B Z11
binary and user's actual local H4F3b NPZ are not automatically in
GitHub Actions checkout. A manufactured Z11 or synthetic source must
not be substituted for a PHYSICAL structural PASS. The exact locked
actual-source and parent inputs must be made accessible to the same
execution environment, or the completed full structural script must
be run locally with those hash-verified inputs.

**Full physical H4 Noether structural PASS NOT YET PRODUCED.
Z21 NOT CERTIFIED; lensing blocked.**


---

## Latest checkpoint — H4F3d5 normalized per-node bath Euler compiler PASS; actual-grid all-parent Ward open (2026-09-25)

The originally certified corrected-Y H3F Z20 and H3G q20,
historical certified Repair32B/32C Z11, actual physical H4F3b
six-piece source PASS, H4F3c genuine-generator manufactured PASS,
and H4F3d1--d4 exact analytic/formal Ward results remain immutable.
Original Repair37 H4/Z21 SCIENCE_FAIL and Repair38--44 diagnostics
are not relabelled. The original active shift target 1e-6 and
matched temporal order >=2.5 are unchanged.

**New H4F3d5 normalized bath Euler compiler: valid restricted CI PASS.**

- classification:
  `GE19_H4F3D5_NORMALIZED_BATH_PARENT_RESIDUAL_COMPILER_PASS`;
- predata:
  `ge19/h4f3d5_predata_normalized_bath_parent_residual_compiler.json`,
  blob `6b7519b48ace8900c8a2879f13c70db3524b366e`;
- code:
  `ge19/h4f3d5_normalized_bath_parent_residual_compiler.py`,
  blob `62cbd02902ccb514c535213ff9801a9abcd46ffb`;
- dedicated GitHub Actions run `36126850777`,
  job `108044837991`, success;
- JSON SHA-256
  `f7538b77475c0dbcab57f331770a75643216d2d3c5966e41396fded0d7b41df4`,
  6089 bytes, artifact ID `10860371141`;
- full frozen record:
  `docs/ge19_h4f3d5_normalized_bath_euler_valid_freeze.md`.

The original GE05 normalized per-node first-order bath Euler
residual is

`R_z10=H D_xi(a^3 v/tau)+a^3 omega^2(z-X10)`,

`E_q10,GE05=-sqrt(w)/(2 omega)*R_z10`.

Its signed physical eta-regularized H4 mixed Ward contribution
is `+4 sum_j E_qj10 q_j10,x`. For individual modes the
algebraic product is
`-2(w/omega^2)R_z10(ik)z10`; the Fourier coefficient
of the physical product still requires real-space convolution.

The exact action normalization/sign and the manufactured
5-node x 3-mode Nt64/Nt128 FD4, current, kinematics and
wrong-sign/omitted-H controls all passed. This is
**manufactured analytical/numerical evidence only**,
not an actual physical parent residual result.

**NEXT decisive actual H4F3d work:** compile and independently
evaluate the normalized per-node bath Euler residual and
every remaining signed background/H1/Z11, corrected-H3F/H3G,
GE07 dust and action-boundary parent term on the EXACT
user's H4F3b Nt128/Nt64 physical parent grids.
Combine with the independently frozen canonical
`W_operator` and actual signed six-source Ward,
preserving separate original FD4/FD8 schemes.
Preregister the full structural error budget from
the exact signed identity and truncation BEFORE looking
at the combined physical defect. Only a frozen
full all-sector actual-grid structural PASS permits
a new separately preregistered H4/Z21 science attempt.

The exact user-local H4F3b source NPZ and original
certified Repair32B Z11 NPZ are **not automatically
available in GitHub Actions checkout**. Do not
substitute manufactured input or claim a physical
Noether PASS from Actions without those exact
hash-verified files. A hash-locked local integrated
runner is an acceptable alternative once fully
implemented and preregistered.

**Full physical H4 Noether NOT CERTIFIED;
Z21 NOT CERTIFIED; lensing blocked.**


---

## Latest checkpoint — H4F3d6 bath-parent compiler Actions PASS; exact physical runner locked (2026-09-25)

This is the newest canonical continuation point. It supersedes only
the NEXT-task text of earlier checkpoints; every original
Repair22/27/32 certification, corrected-Y H3F/H3G and actual
H4F3b source PASS, H4F3d1--d5 analytic/formal results,
Repair37 H4 SCIENCE_FAIL and Repair38--44 diagnostics remain
immutable. No original physical source coefficient, near-null
mask, 1e-6 shift threshold or matched >=2.5 temporal order
has been changed.

**New H4F3d6 actual-bath-parent SUBSET is preregistered and
implemented, with manufactured compiler CI PASS.**

- predata:
  `ge19/h4f3d6_predata_actual_normalized_bath_parent_ward.json`,
  blob `d283086a6ae95efd184db570d6c2f9a8aa32ac7c`;
- code:
  `ge19/h4f3d6_actual_normalized_bath_parent_ward.py`,
  blob `0419145499f5f44e06ba0c96f779c2a604e84ce7`;
- compiler CI `36127944207`, job `108048299004`,
  `success`;
- classification
  `GE19_H4F3D6_BATH_CONVOLUTION_COMPILER_PASS_ACTUAL_OPEN`;
- result JSON SHA-256
  `db6eb2effc711c2c83ebeff6bbeae5e64c295e160505174d657ec676e2f8ad9f`;
- compiler freeze
  `docs/ge19_h4f3d6_bath_convolution_compiler_valid_freeze.md`.

The real GE05 normalized first-order R1 per-node bath Euler is
`R_z10=H FD4_x(a^3 v10/tau)+a^3 omega^2(z10-X10)`,
`E_q10=-sqrt(w)/(2omega) R_z10`.
The signed physical mixed H4 bath parent Ward is
`+4 sum_j E_qj10 q_j10,x`.
Original six positive H1 modes and their conjugate negative
harmonics are convolved to obtain the actual physical
Fourier coefficients `m=0..40`. Deterministic Nt64/Nt128
FD4-current and independent real-space FFT/product negative
controls passed. The original R1 weighted z10 is checked
against certified H3G on the physical run.

**Locked exact local physical bath-subset runner is ready,
NOT YET LOCALLY EXECUTED.**

- runner:
  `ge19/run_local_h4f3d6_actual_normalized_bath_parent_ward.sh`,
  blob `3690147a766f276309d628fba9f436df3941deae`;
- dedicated static runner CI `36128447037`, job
  `108049891704`, success,
  marker `GE19_H4F3D6_PHYSICAL_LOCAL_RUNNER_STATIC_PASS`;
- implementation/execution lock:
  `docs/ge19_h4f3d6_local_physical_bath_runner_lock.md`.

The local runner requires the user's ORIGINAL exact
H4F3b actual six-source JSON/NPZ, certified H3F/H3G,
Repair32B Z11 and R13, plus Repair26 R1 full-history
bath trace. The original source JSON/NPZ hashes are
`1ec88fd3fd6b81bf30614b0cb78d722a02dd4f745e1f22cb9b8f956a44bac6c1`
and
`787d5d177838b05078057aa932f379dd529449ce203f5664c36cf723acb0116b`.
The physical input files are **not automatically in
GitHub Actions checkout**, and manufactured substitutes
are explicitly prohibited for the physical result.
Historical generator imports run in a disposable CWD.

H4F3d6 saves its bath-parent Ward and the 18 actual
`W_source+W_bath` arrays, **report-only**.
Neither source-only nor source+bath Ward is
required to vanish. H4F3d6 physical-subset PASS
is not the complete Noether certificate.

**NEXT:** run the exact local H4F3d6 physical SUBSET,
freeze its exact PASS/FAIL if valid, then independently
compile/evaluate all remaining nonbath
background/H1/Z11 Euler parents and action boundary
plus frozen canonical operator Ward on the exact
same physical grids. Preregister the combined full
structural FD4/FD8 error budget from the signed
identity BEFORE evaluating the physical all-sector
Ward residual. Only a valid FULL all-sector structural
PASS permits a separately preregistered Z21 science
attempt. It is not itself a Z21 certificate.

**Full physical all-sector H4 Noether NOT CERTIFIED;
Z21 NOT CERTIFIED; lensing blocked.**


---

## Latest checkpoint — H4F3d6 actual local bath-parent Ward subset PASS; physical Euler residual open (2026-09-25)

This is the latest canonical GE19 restart point. The earlier
H4F3d6 history entry's NEXT=run local physical bath subset is
completed by the **first valid local physical run**. Every
historical Repair22/27/32, corrected H3F/H3G and H4F3b
result and Repair37 SCIENCE_FAIL / Repair38--44 diagnosis
stays frozen; no numerical target or source coefficient
is edited.

**Result:** `GE19_H4F3D6_ACTUAL_BATH_PARENT_WARD_SUBSET_PASS_FULL_OPEN`.
User supplied the original JSON, NPZ, JSON-identical FULL log
and outer runner log. Independent direct hash/array audit:

- JSON 17572 bytes SHA-256
  `4607edde17c6820c85f32c0bbd774d5a58148eb01bfd0c81ce592e8c1b907791`;
- NPZ 1315867 bytes SHA-256
  `17b50c6ee584b2a8886f7114a90ea9396a127172dd9e02976b0e6275fe2fedc0`;
- FULL log 17572 bytes, byte-identical to JSON, same SHA-256;
- outer runner log 3297 bytes SHA-256
  `74aef76c0d92b41a0e318fa1baeadbf2ecc45274b805e4e4ade16dc351fd3437`.

The 32 NPZ fields are all finite; primary source/bath fields
are (128,41) and controls (64,41). All 18 cases, all 6
preregistered **subset** gates, original H4F3b source,
H3F/H3G/Z11/R13/Repair26 R1 input hashes and unchanged
common x grids pass. The original R1 weighted z10 is
reproduced at relative L2 0.0.
All 18 W_bath/W_source/W_source+bath maxima reproduce
**exactly** from the saved NPZ (maximum discrepancy 0.0).

Immutable full freeze:

`docs/ge19_h4f3d6_valid_local_actual_bath_parent_ward_subset_freeze.md`,
blob `a78dee66657a1c9fddb952d29a1084a9f48ce3ea`.

**Important physical numerical open issue:** The actual
normalized first-order GE05 bath Euler
`R_z10=H FD4_x(a^3 v10/tau)+a^3 omega^2(z10-X10)`
has natural-scale relative L2 `0.9985018...0.9993412`
(report only) on Nt128/Nt64. The source+bath Ward has
no zero gate and reaches `3.659645217615514e-12`
(Nt64). H4F3d6 does NOT show the saved R1 bath is
numerically on shell under this FD4 Euler discretization.
The ratio also does not by itself prove an action-level
physics failure: the frozen R1 interval integrator and
sampled FD4 current derivative may differ substantially
for unresolved high-frequency bath nodes or a clock/
normalization defect. Preserve the numbers and
independently separate these alternatives before
asserting a bath on-shell approximation. Do not replace
frozen equations, fit the source or relax a gate.

**NEXT analytic/structural work:** Derive and evaluate
the remaining signed nonbath homogeneous/H1/Z11/H3F
parent Euler and action-boundary terms, then combine
with the already frozen H4F3d1 canonical operator,
genuine H4F3b six-piece source and this actual bath
contribution on the same physical grids. In parallel,
separately preregister an original R1 continuous
interval-ODE versus FD4 physical-current discrepancy
audit to classify the observed bath Euler report-only
ratio. Derive and prelock the full FD4/FD8 structural
error budget **before** any numerical full-Ward test.

A full all-sector H4 Noether PASS has NOT occurred.
The original active shift `1e-6` and matched order
`>=2.5` remain unchanged. Z21 NOT CERTIFIED;
lensing blocked.
