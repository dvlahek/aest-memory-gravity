# GE19 reduced weakly nonlinear track — persistent history

Last updated: 2026-09-25

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


**NEXT H4F3d7 diagnostic is preregistered (not numerically run):**

- predata `ge19/h4f3d7_predata_bath_fd4_vs_original_r1_interval_ode.json`,
  blob `ccf3185b4f790d9d6068f80beb39a442b186158c`;
- independent prelock workflow
  `.github/workflows/ge19-h4f3d7-bath-fd4-r1-prelock.yml`,
  GitHub Actions run `36137851501`, SUCCESS,
  `GE19_H4F3D7_BATH_FD4_R1_PREDATA_PRELOCK_PASS`.

The registered decomposition uses the ORIGINAL Repair24
step-linear bath ODE, physical `H FD4_x(a^3v/tau)`,
both one-sided interval-H currents at interior nodes and
predeclared per-frequency phase bins. It distinguishes
sampled FD4 derivative error from the frozen step's
piecewise-H background mismatch. No on-shell smallness
gate, time-stencil/source fitting or high-frequency
node exclusion was introduced. This prelock is NOT a
physical H4F3d7 result. Independent nonbath parent and
canonical operator full-Ward work remains a separate
necessary component.


---

## Latest checkpoint — H4F3d7 frozen R1/FD4 compiler PASS; genuine physical decomposition pending (2026-09-25)

This entry supersedes only older NEXT-action wording. Original Repair22/27/32, certified corrected-Y H3F Z20/H3G q20, actual physical H4F3b six-piece source PASS, H4F3d6 *subset* PASS, and formal H4F3d1--d5 results remain immutable. Historical Repair37 H4 SCIENCE_FAIL and Repair38--44 diagnostics are not relabelled. Original active-shift <=1e-6 and matched temporal orders >=2.5 are unchanged.

**Latest verified GitHub Actions:**

- H4F3d7 preregistration prelock run `36137851501`: SUCCESS.
- H4F3d7 original R1 ODE versus FD4 *compiler/manufactured* run `36148151670`: SUCCESS, job `108114383440`; terminal marker `GE19_H4F3D7_R1_FD4_COMPILER_PASS_PHYSICAL_OPEN`. Artifact `10869873062`; result JSON 10828 bytes, SHA-256 `6a6fb22b1c25ee0ee66755eb8a82899b3cdf8292c1678e7f4c989922b94ed66d`.
- Valid result freeze `docs/ge19_h4f3d7_r1_fd4_compiler_valid_freeze.md`, blob `620cec44adce30fbaa8cd25c569872227af3831e`.
- Prereg `ge19/h4f3d7_predata_bath_fd4_vs_original_r1_interval_ode.json`, blob `ccf3185b4f790d9d6068f80beb39a442b186158c`. Locked code `ge19/h4f3d7_bath_fd4_vs_original_r1_interval_ode.py`, blob `b598a5cc49b3d87827b4758c55d3ce7f3a1198a8`.

The exact component identity on EACH original R1 interval side was derived and manufactured-checked:

`R_FD4 = R_ODE,side + [H_i FD4_x(J)-J_t,side]`,
with `J=a^3v/tau`, `R_ODE,side=3 a_i^3(H_i-h_mid,side/tau)v_i/tau`. At every interior physical node report BOTH original interval sides; do not select/average favorable sides. Retain all 2048 nodes and preregistered `omega*Delta_t` phase bins (<0.25, [0.25,0.5), [0.5,1), >=1). The original Repair24 stepper, R1 trace and FD4 current remain unchanged.

**Actual physical H4F3d7 run HAS NOT OCCURRED.** The compiler succeeded on deterministic manufactured R1 trajectories only. The first valid physical H4F3d6 subset remains
`GE19_H4F3D6_ACTUAL_BATH_PARENT_WARD_SUBSET_PASS_FULL_OPEN`; JSON SHA `4607edde17c6820c85f32c0bbd774d5a58148eb01bfd0c81ce592e8c1b907791`, NPZ SHA `17b50c6ee584b2a8886f7114a90ea9396a127172dd9e02976b0e6275fe2fedc0`. Its actual sampled normalized bath Euler natural-scale relative L2 ~0.9985018--0.9993412 is report-only and does **not** establish an on-shell bath. The physical d7 diagnostic must reproduce d6's original absolute FD4 Euler norm to <=1e-10 relative, and separate original interval-H mismatch from sampled FD4 derivative defect.

Required physical files are the ORIGINAL hash-locked actual H4F3b JSON/NPZ (SHA `1ec88fd3fd6b81bf30614b0cb78d722a02dd4f745e1f22cb9b8f956a44bac6c1`, `787d5d177838b05078057aa932f379dd529449ce203f5664c36cf723acb0116b`), H4F3d6 JSON/NPZ above, H3F/H3G, Repair13, exact certified Repair32B Z11 NPZ `5d4a0a72c08d09d096a8de0b428b3c8443fc33e8ad442ed6d997d6bf2bc6e327`, and Repair26 R1 trace `608ee0b4c868a701db6976f756b9a551cd9ddffe1e8e4ab37c5cd2361405a6f8`. These physical binaries are available from the user's prior *local* successful execution but are not automatically present in Actions checkout; manufactured data must not replace them.

**NEXT (two independent workstreams):** (1) run exact H4F3d7 physical diagnostic on the original hash-verified local files in an ISOLATED temporary CWD, with absolute input/output paths and no historical output overwrite, freeze physical result separately; (2) independently derive/evaluate all signed NONBATH background/H1/Z11/H3F/H3G/dust/metric/aether/scalar parent Euler plus action boundary terms and original canonical operator on same H4F3b Nt128/Nt64 grids. Derive/preregister the complete FD4/FD8 structural truncation budget BEFORE the first full integrated actual-grid H4F3d Noether gate. Source-only Ward magnitude is report-only.

**Full actual all-sector H4 structural Noether PASS NOT PRODUCED. Z21 NOT CERTIFIED. Lensing blocked.**

New-chat transfer document: `docs/ge19_new_chat_handoff_2026_09_25.md`. This standalone handoff includes verified H4F3d7 CI results, exact original physical input hashes, the pending physical d7 diagnostic and independent nonbath full-Ward steps.

---

## Latest checkpoint — H4F3d7 physical local runner STATIC PASS; physical measurement open (2026-09-25)

This supersedes only previous NEXT-step text. The complete new-chat
handoff in `docs/ge19_new_chat_handoff_2026_09_25.md`, all historical
Repair22/27/32, corrected H3F/H3G and actual H4F3b/H4F3d6
certificates, the H4F3d4 formal ledger, Repair37 SCIENCE_FAIL
and Repair38–44 diagnostics remain immutable.

**New implementation/static result:** `GE19_H4F3D7_PHYSICAL_LOCAL_RUNNER_STATIC_PASS_PHYSICAL_OPEN`.

The locked original physical local runner
`ge19/run_local_h4f3d7_physical_r1_fd4_vs_interval_ode.sh`,
blob `6fe12ef99f9a469da8f5913121d3301df519aae2`,
was created in commit `a6e1137b7d8e74c82466d98540c733aa72e1241f`.
The separate static CI workflow
`.github/workflows/ge19-h4f3d7-physical-local-runner-static.yml`,
blob `632aefa190722ad273beca15f3743c941a866372`,
passed [Actions 36150787708](https://github.com/dvlahek/aest-memory-gravity/actions/runs/36150787708),
job `108123212034`, on 25 September 2026. The static CI
checked pinned source, Bash and Python-heredoc syntax,
physical CLI arguments, no manufactured execution,
absolute hashes, temp-CWD-before-import isolation and
non-overwriting outputs. It DID NOT load the original
physical NPZ binaries.

Immutable runner freeze:
`docs/ge19_h4f3d7_local_physical_runner_lock.md`,
blob `67cd27ea11a24e93f8f4cd5a9a181ccec65112c1`.

The local physical runner is now prepared to use exactly the
original physical H4F3b JSON/NPZ, actual H4F3d6 JSON/NPZ,
certified H3F/H3G/Repair32B Z11/Repair32C/Repair13
and exact 26,643,162-byte Repair26 R1 full-history trace.
Its isolated preflight delegates all parent hashes to the
existing frozen `s.frozen_inputs` and verifies the current
original d7 code, Repair24 stepper AST and H4F3b/H4F3d6
certifications. The physical d7 code and preregistration
are unchanged. It preserves BOTH original R1 interval
sides, all original 2048 frequency nodes, six original modes
and all fixed phase bins. No new bath-on-shell threshold,
source fitting, exclusions, or clock refit is introduced.

**NEXT:** execute this runner only in the user-local
scientific environment where the exact original physical
binaries are present. Independently verify output JSON/NPZ/FULL
hashes and freeze the actual physical classification
without changing any previous result. Independently
derive/evaluate the remaining signed nonbath H4 Euler
parents and action boundary and preregister a separate
FD4/FD8 structural error budget BEFORE the all-sector
physical Ward test. Source-only Ward is report-only.
Original active shift <=1e-6 and temporal order >=2.5
are unchanged.

**H4F3d7 physical decomposition NOT YET EXECUTED;
full actual H4 Noether NOT CERTIFIED; Z21 NOT CERTIFIED;
lensing blocked.**

---

## Latest checkpoint — H4F3d8 restricted independent nonbath symbolic PASS; physical parent arrays open (2026-09-25)

A distinct, **restricted** independent nonbath analytic compiler was
preregistered as
`ge19/h4f3d8_predata_independent_nonbath_euler_and_boundary.json`
(blob `007bec20e450dd67263d32a33476dcb8a5c33996`).
Its source-bound final code
`ge19/h4f3d8_independent_nonbath_euler_and_boundary.py`
(blob `861cd5a81c17380a727777a4e1ff08cd7e857522`)
and exact-pinned CI workflow (blob
`3e477da1801e78695acad291bddcbf9020bbcc2c`)
passed [Actions 36151870934](https://github.com/dvlahek/aest-memory-gravity/actions/runs/36151870934),
job `108126857772`, terminal marker
`GE19_H4F3D8_INDEPENDENT_RESTRICTED_COMPILER_PASS_ACTUAL_OPEN`.
Successful JSON SHA-256
`d9f30c9632d06dd8412ef36e1a2f4ee43d7cbe7922c6d780d3376b5d0f6220fd`;
artifact ID `10871858033`.

Freeze:
`docs/ge19_h4f3d8_independent_nonbath_euler_boundary_compiler_valid_freeze.md`,
blob `b51117333d652edf8826b085bf65bbd39776fdb2`.

Independent exact checks derive the eight-field mixed
`E00*F21_chi+2 E10*F11_chi+2 E11*F10_chi` parent
and `B_lower=L21*EL00+2L10*EL11+2L11*EL10
-b21*Eb00-2b10*Eb11-2b11*Eb10` from the original
action product. Frozen GE07 dust current/Euler and
Lambda metric Euler/first-order terms pass independent
symbolic gates; original GE06 action jet dictionary is
source-bound and NL0C Y zero-set one-sided limits pass.
The first d8 run `36151698788` was an
implementation `NameError` in the static GE06 text
binding; this was fixed without changing source/action
parents, and only the subsequent CI run is PASS.

**Scope stop:** restricted symbolic/compiler PASS only.
No actual GE06/Y/background/first-order nonbath Euler
arrays or exact complete physical boundary evaluated;
original R1 physical H4F3d7 not yet executed;
full physical FD4/FD8 structural error budget NOT YET
PREREGISTERED/VALIDATED for full H4 gate. Do not equate
the H4F3d8 compiler with actual all-sector Noether.
No Z21, no lensing, no old Repair37 result change.

---

## Latest checkpoint — H4F3d9 exact original FD4/FD8 stencil constants PASS; physical numeric budget open (2026-09-25)

The original FD4/FD8 source-based numerical error-budget
preregistration is
`ge19/h4f3d9_predata_original_fd4_fd8_structural_error_budget.json`
(blob `98e6fd8835fdbe3bd169d062431eefe80a3e9232`).
A distinct versioned single-SHA provenance amendment
`ge19/h4f3d9_predata_amendment01_correct_d7_git_blob.json`
(blob `34cea0c62ef2dc962bc43ef93b2fbbd70b9c2180`)
corrects only a copied H4F3d7 source blob typo in the
immutable original preregistration. The initial CI
`36152370247` correctly STOPPED on that mismatch before
doing any stencil derivation. Nine original source SHA
checks established that no other pin differed.

The final independent rational AST-only compiler
`ge19/h4f3d9_exact_original_fd4_fd8_stencil_budget_compiler.py`
(blob `03864a08110e341038056dd4cefd5842d4a5eb1e`)
and dedicated CI workflow (blob
`d708be67bf9a6bc139c83951160cc36939c4f9a2`)
passed [Actions 36152551838](https://github.com/dvlahek/aest-memory-gravity/actions/runs/36152551838),
job `108129154468`, terminal marker
`GE19_H4F3D9_ORIGINAL_STENCIL_CONSTANTS_PASS_PHYSICAL_BUDGET_OPEN`.
JSON SHA-256 `27ba90ea35b074f6036aff7a41fbc4e27c4a2ead2291daf806f8bdc2e3d40461`,
artifact ID `10871484108`.

Freeze:
`docs/ge19_h4f3d9_original_fd4_fd8_stencil_budget_compiler_valid_freeze.md`,
blob `e77d5d19125ed03a4d15bd71a4eb9d21695f07f4`.

The exact ORIGINAL 5-point FD4 and 9-point FD8
boundary/interior rational weights and polynomial moment
constraints pass for every row, producing exact conditional
`K_(p,i)=sum_j|c_ij||j-i|^(p+1)/(p+1)!`
Taylor constants. The source-only symbolic compiler does
not import historical result-writing modules or replace the
original production matrices. The full physical error-budget
formulas are preregistered, but independent actual physical
`M5/M9` derivative/regularity envelopes, piecewise original
R1 and Y zero-gradient regularity and operation-level
roundoff bound are UNAVAILABLE. Consequently NO full
numerical all-sector H4 tolerance is certified or chosen.
The near-unit GE05 sampled Euler cannot be hidden
inside a fitted tolerance.

**Current state:** physical H4F3d7 local runner STATIC PASS;
actual original H4F3d7 measurement OPEN; restricted
H4F3d8 nonbath symbolic PASS; H4F3d9 exact stencil
constants PASS, physical error budget OPEN; full H4
physical Noether NOT CERTIFIED; Z21 NOT CERTIFIED;
lensing blocked. Preserve historical Repair37 SCIENCE_FAIL,
Repair38–44 diagnostics, original shift 1e-6 and
temporal-order >=2.5 gates.

---

## Latest checkpoint — H4F3d7r1 one-expression physical output gate implementation repair; STATIC PASS, physical OPEN (2026-09-25)

The user-local ORIGINAL H4F3d7 physical run reached
`physical_run`'s final `valid` gate and stopped with
`AttributeError: 'list' object has no attribute 'values'`
at source lines 422–423. Its uploaded original
`ge19_h4f3d7_physical_r1_fd4_vs_interval_ode_FULL.log`
contains the traceback, not a certified JSON/NPZ
physics result. This is a NEW local implementation failure,
not a retroactive alteration of original H4F3d7 compiler
PASS `36148151670` or any physical science verdict.

The original source blob
`b598a5cc49b3d87827b4758c55d3ce7f3a1198a8`,
original runner
`6fe12ef99f9a469da8f5913121d3301df519aae2`
and frozen H4F3d7 predata
`ccf3185b4f790d9d6068f80beb39a442b186158c`
remain immutable. New separate one-expression implementation
preregistration
`ge19/h4f3d7r1_predata_physical_output_finite_check_repair.json`
(blob `f404c1b910e9dbcb342fbc4d3403fb83108697f7`),
repaired physical implementation
`ge19/h4f3d7r1_physical_output_finite_check_repair.py`
(blob `e4cb9d6638b427368647a29b86ccf5445b43d7a2`)
and versioned isolated local runner
`ge19/run_local_h4f3d7r1_physical_output_finite_check_repair.sh`
(blob `6bdee189cf795a04e4d1b19822af6ed778b5af46`)
do not overwrite the old log or files.
The ONLY Python source difference is replacing
a broken `stored.values()` call on a list by
`all(np.isfinite(arr).all() for arr in outputs.values())`
inside the final original six-case `valid` gate.
Original physical equations, both R1 interval sides,
all 2048 nodes and frequency bins, FD4, all input hashes
and all threshold values remain unchanged.

Versioned static regression workflow blob
`f0452ff9667e734bd39d45c692020ebe49e913eb`
passed [Actions 36153973088](https://github.com/dvlahek/aest-memory-gravity/actions/runs/36153973088),
job `108133895719`. Terminal marker:
`GE19_H4F3D7R1_EXACT_SINGLE_FINITE_GATE_REPAIR_STATIC_PASS_PHYSICAL_OPEN`.
CI checked the exact one-expression old/new diff and the
actual new AST valid gate with finite, NaN and +/-Inf arrays,
six-case/pass failures, locked source, isolated bash
and distinct output paths. The preceding static workflow
`36153886957` was an implementation-only YAML heredoc
test-fixture indentation FAIL, corrected without modifying
the new physics-source blob.

Separate frozen document:
`docs/ge19_h4f3d7r1_physical_output_finite_repair_static_valid_freeze.md`,
blob `e1f8aaa72123bebcc35227c4a7560da7eef167d9`.

**NEXT:** execute the versioned local physical runner
ONLY on exact user-local certified original H4F3b/d6,
H3F/H3G, Repair32B/32C Z11, Repair13 and Repair26
R1 bytes; save its *distinct* `ge19_h4f3d7r1_...`
JSON, NPZ, FULL and runner logs, independently verify
hashes and all six physical cases, then freeze physical
decomposition or its precise remaining gate failure.
The original H4F3d6 near-unit sampled GE05 bath Euler
remains open until the actual physical FD4/ODE diagnostic.
H4F3d8 restricted symbolic PASS and H4F3d9 stencil
constants PASS remain separately frozen; missing actual
nonbath physical residuals and complete preregistered
FD4/FD8 physical error bound still block the integrated
H4 Ward. No new bath-on-shell gate, no Repair37
SCIENCE_FAIL relabel, original active shift `1e-6`
and order `>=2.5` unchanged.

**Full actual H4 Noether NOT CERTIFIED;
Z21 NOT CERTIFIED; lensing blocked.**

---

## Latest checkpoint — original physical H4F3d7r1 FD4-versus-R1 diagnostic PASS, full Noether OPEN (2026-09-25)

The user executed versioned H4F3d7r1 from local locked
`CODE_HEAD=e9987882493feee2461c43c969b4624cff3ba4eb`
and uploaded **all four** actual physical outputs:
JSON `031229d570d29ae9c4ea0ab8e25222d94e9cda4520c991cd203e9d7b97e01dc9`,
NPZ `4f011c96c2c11165df6332eafc459c5d2c5e7bc5164a436bde3d1563696f0e13`,
FULL log `031229d570d29ae9c4ea0ab8e25222d94e9cda4520c991cd203e9d7b97e01dc9`,
runner log `39b1809b22c817ae25cb81ffaa7f52d7f2e2d537a86c90346515405a5d5b997f`.
Original local runner reports
`GE19_H4F3D7R1_PHYSICAL_DECOMPOSITION_PASS_FULL_NOETHER_OPEN`
with all original physical parent/trace SHA, exact
Repair24 stepper and six original `C_min,C_star,C_max`
by `Nt=128,64` gates PASS. Its JSON classification
is `GE19_H4F3D7_FD4_INTERVAL_ODE_DISCREPANCY_DECOMPOSED`.

Independent uploaded artifact audit checked exact
SHA/length cross-match, FULL=JSON byte-for-byte,
all **44** exact NPZ arrays/finite/shapes/x, the five
saved NPZ-vs-JSON global L2 norms in each of six
cases, and complete four-bin norm/count reconstruction
over **all original 2048 R1 nodes, six modes, both
sides and all original node-intervals**.
Maximum normalized algebraic identity discrepancy:
`2.289808148773898e-16`. Original R1 weighted
Z10 and D6 sampled bath Euler absolute-norm
reproduction: exactly zero in every case.
No actual raw parent complex trajectories were
uploaded, so parent-propagator reproduction relies
on the original hash-locked local runner, not an
independent physical rerun here.

Primary `Nt=128`: sampled FD4 bath Euler L2
`9.27e-5–9.68e-5`, original R1 interval
ODE both one-sided L2 about `2.20e-11–2.24e-11`;
control `Nt=64`: FD4 `6.58e-5–6.72e-5`,
original interval ODE `3.10e-11–3.22e-11`.
Original `phase>=1` bins (2527/260096 primary
and 1789/129024 control node-interval pairs)
contain essentially **all** squared norm of sampled
left-derivative defect, with original unchanged
bins and no exclusions. The original H4F3d6
near-unit **FD4** Euler ratio remains real as
a sampled diagnostic but is explained by the
sampled-versus-original interval-derivative defect;
it must NOT be construed as verified physical
original-ODE bath on-shell violation or as a
newly certified covariant bath on-shell condition.
The diagnostic separates the two formulations,
not a physical all-sector H4 Ward.

New immutable archive audit manifest:
`ge19/h4f3d7r1_actual_physical_discrepancy_independent_archive_audit.json`,
Git blob `b85b3bbd80603ed324a6cc54b0080489167fef31`.
Detailed physical freeze:
`docs/ge19_h4f3d7r1_actual_physical_r1_fd4_discrepancy_diagnostic_freeze.md`,
blob `7f34ffbd829353028d41c620334e2c01b273917e`.
No binary user artifact was claimed as committed
to GitHub. Original H4F3d7 broken local FULL.log
and its versioned implementation repair/CI
static PASS are retained separately; old physical
and science history is untouched.

**NEXT:** evaluate actual nonbath H4 parent Euler
and boundary arrays on exact original frozen parents
using H4F3d8's restricted symbolic independent
compiler, then complete original source/bath/
nonbath/boundary/operator integrated H4 Ward
with physically justified original derivative error
bound (H4F3d9 structural stencil constants do
not yet constitute actual physical bound).
No retuning source, physics equations, time grid,
2048-node R1 bath, preregistered thresholds
or observations; Repair37 SCIENCE_FAIL immutable.
**Full actual H4 Noether NOT CERTIFIED; window-local
particular reduced Z21 NOT CERTIFIED; lensing BLOCKED.**

---

## H4F3d10r1 actual known nonbath and H4F3d11 source-bound E00 preregistration (2026-09-25)

Original user-local H4F3d10 actually completed all six
C/Nt eight-field nonbath first-order parent/boundary
cohorts but failed its lossy m0..40 archive recovery
on tiny high-frequency individual Euler rows.
Its original `GE19_H4F3D10_ACTUAL_PARENT_INTERFACE_UNRESOLVED`
classification and six original FAIL flags are immutable.
Separate preregistered H4F3d10r1 archived all
m0..64 Fourier coefficients without changing original
m0..40 arrays or full-resolution physics. It PASSED
original actual physical local execution and subsequent
independent NPZ audit: 530 original arrays bitwise
identical, 528 new full-Nyquist high arrays finite,
six cases and both original FD4/FD8, max full-grid
archive-only inverse error `2.8428133461119143e-16`
(original `1e-12` archive-only comparator).
All 12 original signed full-real P_known/B_known/W_known
assembled independently. Original actual H4F3d10r1
JSON SHA256 `69eabf101a6ec1939b32323e25b207dc419fad57eb5b2cef0858874a50cfa1d2`,
NPZ SHA256 `85c0fbd8b56037aae98615926b70bd60739a1af2fa1ff666ffc2e95485c2749b`.
Freeze `docs/ge19_h4f3d10r1_actual_physical_lossless_known_boundary_freeze.md`
(blob `e9329cd24631241d0ef9610d104336cf4f6590b9`);
independent machine audit
`ge19/h4f3d10r1_actual_physical_lossless_archive_independent_audit.json`
(blob `2921f79dbb0ce99200418bfba924b699ff8cd67f`).
This actual diagnostic does NOT establish full H4 Noether.

Next H4F3d11 preregistered original-action
eight-field homogeneous GE06/GE07/Lambda background
Euler `E_i00` on the same original frozen
Repair13 C_min/C_star/C_max x Nt128/Nt64
backgrounds, with separate original FD4 and FD8
physical-time derivatives and source-stable Z.
Original GE06 15 and GE07 7 exact source
partial-map FLRW expressions symbolically verified,
including nonzero GE06 homogeneous spatial shift
momentum p_bx00, scalar time current and negative
controls. Source [static CI 36189149840](https://github.com/dvlahek/aest-memory-gravity/actions/runs/36189149840)
PASS; no-overwrite/isolated driver/synthetic assembly
[static CI 36189465789](https://github.com/dvlahek/aest-memory-gravity/actions/runs/36189465789)
PASS. Initial workflow 36189057213 failed only a
literal test-string comparison before importing
the physical action; separately versioned CI r1
fixed the harness test, not physics. Frozen D11
predata blob `deb4b35e6a147b48fe93d6c99d798572650000ac`,
source compiler `1f085efec4ea64b42822ddeaac566f532d9dccf1`,
actual physical driver `b162fad1db2a855917b5f8e29fce10c67d30737f`,
locked local runner
`8c4f34ad79b347b3810093a1bba0b4129468f7fc`.
Static freeze
`docs/ge19_h4f3d11_source_bound_actual_background_e00_static_freeze.md`
(blob `bf178afbaa6886202b857503d8cc6e1a39b80290`).

**Actual H4F3d11 physical E00 output NOT YET RUN.**
Local command `bash ge19/run_local_h4f3d11_actual_original_action_background_e00.sh`
after `git pull --ff-only` and activating `.venv`.
Required four new JSON/NPZ/FULL/LOCAL logs must be
independently audited. No E00 on-shell assertion
or omitted `sum_i E_i00 F_i21,chi` and
`L21 E_L00-b21 E_b00` products, no full integrated
H4 Ward, no certified Z21, no lensing. All older
Repair37 SCIENCE_FAIL, original bath 2048 nodes,
shift `1e-6` and temporal order `>=2.5` unchanged.

---

## H4F3d11 actual physical original-source E00 and finite-difference defect audit (2026-09-26)

Actual original-local H4F3d11 output uploaded and
independently hash-checked:
JSON `d62436b12bb5e5d9b7cbf1ea24abd0e6c06ac3ff1bfd43a41556aef284e3d3df`,
NPZ `7679dc6765b87c0b1294b3915d0d1305e4fa59ac86a18d75621d5bf85c616229`,
FULL log byte-identical to JSON, runner SHA/lengths exact.
Physical classification
`GE19_H4F3D11_ACTUAL_BACKGROUND_E00_ARRAYS_DIAGNOSTIC_PASS_ONSHELL_OPEN`.
Source locks and frozen parent inputs PASS by
original local runner; independent audit verifies
578 finite NPZ arrays in six original cases,
eight Euler fields, both original FD4/FD8,
exact reassembly of all 96 E00 arrays and all
48 original temporal derivative components.
Original GE07 dust action varrho_b=3*C/a^3
vs Repair13 rho_dust=C/a^3 preserved exactly.
Original scalar charge a^3*KQ constant to
`1.0842e-19` span and rho_lambda constant
exactly on saved grid. Conditional exact
homogeneous GE06/GE07/Lambda pressure equation
reduction gives analytic E_L L2 `<=4.961e-22`;
FD4/FD8 E_L-minus-analytic difference matches
original finite-difference temporal defect
to `6.484e-23` absolute L2. This localizes
FD4 pressure residual to temporal discretization
without changing old thresholds.
Original H4F3d10r1 known nonbath PASS unchanged;
original D10 UNRESOLVED and Repair37 SCIENCE_FAIL
unchanged. Original complete GE05 bath E00,
actual E00*F21, L21*EL00-b21*Eb00, complete
integrated H4 Ward, Z21 and lensing remain OPEN.
Machine audit
`ge19/h4f3d11_actual_original_background_e00_independent_archive_audit.json`
(blob `c3f238c2914ff18e43030ec31a3debb0edab81f1`);
science freeze
`docs/ge19_h4f3d11_actual_original_background_e00_independent_freeze.md`
(blob `5d38c45430bf0207d5e0b383f9c3f6be6d7e7613`).

---

## H4F3d12 restored GitHub freeze and next original GE05 bath gate (2026-09-26)

GitHub write access restored; first checkout-backed write
`003ce380f65da913e8ec616ea6d9342fc7e454b1` was
confirmed. Original D12 prereg, original failed r0,
corrected r1, original manifest and scientific report
have been committed **byte-for-byte** to
`physics-first-gravitational-elasticity`; historical
pre-GitHub rejection remains unchanged in the
original manifest/report and is reconciled only
by the newer `docs/ge19_h4f3d12_checkpoint.md`.
Original actual D11-derived machine JSON is committed
losslessly in `ge19/h4f3d12_actual_d11_conditional_f21_bound.json.gz`,
blob `30cae15e4c2992484d96d3ba0f3f02e8ea8969b1`,
decompressed JSON SHA256
`5d94ac19e3176e8e6d2948260b957718eba9620ea9fced2981fe2e6df2c5837e`.
Corrected r1 implementation blob
`794df05d6c2c7572a435ba617b0c22649a28b318`;
original prereg blob
`97b513c176f9de6e1ee55cc21d87cb23103fc707`.
Reproducible no-overwrite original-parent local replay
`ge19/run_local_h4f3d12r1_restricted_background_and_f21_bound.sh`
blob `857765404ad013175d69be91c0f3d8428f647228`.
[GitHub D12 CI 36223812141](https://github.com/dvlahek/aest-memory-gravity/actions/runs/36223812141)
completed SUCCESS and checked frozen source,
full archived actual result, 23 symbolic gates,
12 actual D11 Fourier multiplier rows, original
D11 claim boundaries, synthetic FFT controls and
runner syntax. Independent original D11 replay
was byte-identical; original numerical and
scientific gates were unchanged.

Physical scope remains conditional original
homogeneous GE06/GE07/Lambda background Euler
cancellation and the actual-D11-dependent
coefficient times UNKNOWN `||F21||`.
For C_star/Nt128, original full-band
B(FD4)=`6.858137595155815e-16`,
B(FD8)=`5.98037737151968e-18`;
these are NOT complete all-sector H4 smallness
certificates. Original full bath, nonzero
Fourier F21, L21/b21 boundary, full H4 Noether,
Z21 and lensing remain OPEN. Original Repair37
SCIENCE_FAIL immutable.

Next original-action step: preregister the
independent GE05 per-node 2048-node original
R1 interval bath Euler and signed mixed
`+4 sum E_qj10*dchi q_j10`; preserve original
D7r1 FD4 versus one-sided interval ODE
discrepancy. 1024-node quadrature and Nt64
controls stay independent. Do not upgrade
D7r1 diagnostic to bath on-shell.

---

## H4F3d13 actual signed one-sided R1 GE05 bath parent independent audit (2026-09-26)

Original local 12-cohort D13 diagnostic PASS,
original source and parent SHA locks PASS;
actual JSON SHA `2b4dfbd30ec6466292e0dcf62eeed8b723555d1890a127a5e0a6ff761d2ebe76`,
NPZ SHA `1608fe98dd924b2b235ecf0f8fce768f2f3a2fa4a2854de04a56fe622ad3df89`,
FULL log byte-identical. Independently
verified 134 finite distinct arrays, original
signed left/right interval W + derivative
defect = original sampled FD4 W to max
`4.7783e-16` relative. Original prior D7r1
mode-time per-side Nq2048 arrays 24/24
bitwise equal and original six phase-bin
counts identical. Original signed interval
W quadrature difference Nq2048/1024 max
`7.661e-8` but cancellation-sensitive
original sampled FD4 signed W changes up to
`1.35477%` relative. Original signed interval
W / FD4 W ranges `14.38..29.61` in norm;
sum-component amplification up to `60.185`;
C_star/Nt128 left signed interval and
sampled derivative defect correlation
`-0.999959`. Original phase high-tail
>pi requires source-weighted audit, not
unweighted node-count science gate. Original
GE05 bath on-shell and full all-sector H4
Ward remain OPEN; no Z21/lensing.
Machine audit blob
`886ac54bd7ad6f802895145fd7776f2ebd6c64d1`,
science freeze blob
`6e611bbe8dcf3584b5e27c55cda4eafd0e342141`.
Original D10 FAIL and Repair37 SCIENCE_FAIL
unchanged. Next predata D14 source-weighted
bath high-phase and signed cancellation
error budget using original R1 state and GE05 action.

---

## H4F3d14 source-weighted phase-bin signed GE05 bath predata and static PASS (2026-09-26)

Following independently audited D13 user-local
actual signed bath diagnostic PASS and discovery
of cancellation-sensitive original sampled
FD4 quadrature variation up to `1.35477%`
relative despite one-sided signed interval
quadrature variation < `7.661e-8` relative,
pre-registered D14 original source-weighted
R1 bath phase-tail diagnostic. Frozen original
phase bins [0,.25),[.25,.5),[.5,1),[1,pi),
[pi,infinity); original D7r1 bins unchanged.
Original GE05 E_q10 and original signed +/- six
Fourier mode convolution separately retain
ODE interval, sampled derivative defect and
FD4 total for all m0..40; each phase bin
also records a conservative absolute-sum
source-node/mode-pair envelope. Original
Nq2048/1024 quadrature/timing report-only.
New actual original physical driver hash-locks
D13 JSON/NPZ original physical SHA and original
Repair26 R1 trace. Synthetic source static
[CI 36225513503](https://github.com/dvlahek/aest-memory-gravity/actions/runs/36225513503)
PASS; actual original local D14 physical result OPEN.
Detailed static freeze blob
`37cc2c32438bbdfba8763e9f8f2d99c4ec1de898`.
No GE05 bath on-shell, complete all-sector
H4 Ward, Z21 or lensing claim.

---

## H4F3d14 actual original source-weighted GE05 bath independent archive freeze (2026-09-26)

User-local D14 original physical result
`GE19_H4F3D14_ACTUAL_ORIGINAL_R1_SOURCE_WEIGHTED_PHASE_BATH_DIAGNOSTIC_PASS_ONSHELL_OPEN`.
Original actual JSON SHA
`8d8244cf810447c96df82f6ece6c161a4dd0553f707e3a698ed0b29f37ff3c6e`
(290019 bytes); NPZ SHA
`f79d87f10dc1561ef2c61997b7952d62d85eda6674abaa015e5d38e161b55c48`
(31955470 bytes); FULL log identical to JSON,
original code, R1 trace and D13 physical SHA
local runner PASS. Independently verified
746 finite distinct arrays, 12 original
C/Nt/Nq cohorts, 1,751,040 original
node-interval phases, all original D13
parent JSON/NPZ SHA and 12/12
sampled signed FD4 arrays bitwise.
Five signed phase-bin ODE/derivative defect/
FD4 complex array sums match original D13
with max relative 5.15012e-16.
Per-bin original FD4=ODE+defect
max relative 4.16854e-16. Original
unsigned source-node/signed-mode
envelope componentwise valid to
absolute 4.544e-28 roundoff.

In original primary C_star/Nt128/Nq2048
phase>=pi unweighted count 0.54326%;
source-weighted conservative unsigned
L2 fractions: one-sided interval ODE
1.88360e-7 (left), FD4 derivative defect
5.20884e-4, original sampled FD4 total
0.0146093. Original FD4 relative Nq2048/
Nq1024 difference up to 1.35477%;
individual nonnested hard-phase bin
Nq relative differences can be 0.79
or greater and are NOT independent
physical quadrature error bars.
High-phase interval-ODE source
weight is small on the ORIGINAL
DISCRETE signed bath parent only.
No continuous GE05 on-shell inference.

Machine D14 audit blob
`3f7acc17aee24c6b776578ef2b654a40b2db6af0`,
science freeze blob
`eba18e11006abcd837f1532850014e9daab53bf2`.
D15 predata original GE05 variable
H(t),X10(t) continuous R1-step defect
is registered separately; actual
continuous background/drive
enclosures and physical D15 execution
OPEN. Full all-sector action Ward,
Z21 and lensing blocked; original
Repair37 SCIENCE_FAIL preserved.


---

## D47 validated continuous-H1 enclosure campaign (2026-09-30)

D47 moved the original-action H1 line from sampled numerical diagnostics to
validated-numerics pilots using python-flint/Arb, while preserving all earlier
claim boundaries. Frozen parents remain:
D17 NPZ SHA256 `cd3bcf8cf5ac9ab14385baa4d90bd53400daae9f2bb89d4d22bfa2a581846359`,
D16R1 NPZ SHA256 `915709b21bae65c53f9521325a3920d4e0320b650e43458cad03109733d27a36`,
R13 NPZ SHA256 `011c0ae54fd21d70c0e2c695ce62e7b74a3c5529a07c9023c882a447d5b40ca3`,
and Repair07 local-source SHA256
`ce308f85d14d0feece720db18c77a618c1c828447b09c6225a47b80200bc42a3`.

D47 r3 sampled 108 independent off-clock operator evaluations over
primary/control, C_min/C_star/C_max, first/middle/last interval midpoint,
and six Fourier modes. Max algebraic cancellation-safe backward error was
`2.5627728818676326e-16`; max lapse backward error
`1.0143577850211808e-13`. This remained a sampled numerical diagnostic,
not a continuous enclosure.

D47 r4 compared the shared middle midpoint on Nt128/Nt64. High modes
m=15,20 showed approximately third-order two-grid scaling
(p_obs about 2.88--3.10); low modes were contaminated by machine-floor
effects. This was descriptive convergence evidence only.

D47 r5 source audit established that the active local map is homogeneous
linear in the perturbation variables, GE06 exposes symbolic
`coeff1_expr`, GE07 exposes symbolic first-order coefficients, and the
original-action background can be translated into Arb balls. python-flint
0.9.0 with Arb was installed in the project .venv.

The first rigorous Arb slice certified interval Az regularity and float
operator containment. A scalar norm majorant was unusably conservative,
so the validated propagation was reformulated with fixed diagonal scaling
and then a componentwise Metzler comparison system.

D47 r5a v5 rigorously enclosed the first
primary/C_star/m=20 fine Radau substep. At nsplit=32 the final original
L1 error upper bound was `1.4046888124825654e-4`, corresponding to
`3.8241950989669635e-4` of the archived L2 norm. The previously dominant
component-6 bound dropped to `2.3818878054467154e-5`.
Thus `first_substep_continuous_H1_error_enclosed=true` for that slice.

D47 r5b then propagated the same validated mechanism through the complete
primary/C_star/m=20 D17 window: 508 fine substeps, 8 Arb subdivisions per
fine substep, 4064 certified x-segments. Endpoint Radau replay was exact,
max scaled stage residual `3.613811247327609e-16`, minimum certified
Az determinant magnitude lower bound about `1.8576739053e10`, and
boundary-jump total was zero. Therefore
`case_mode_fullwindow_continuous_H1_error_enclosed=true` for this single
case/mode. However, the enclosure wrapped severely over the long window:
final original L1 upper bound `48675.85992551011`, or
`10867.933581224325` times the archived final L2 norm. This is a valid
but physically uninformative error enclosure and MUST NOT be generalized
to all modes/C cases.

D47 r5c independently reconstructed the full discrete Radau fundamental
propagator for the same case/mode. Global state replay relative error was
`4.112904877298e-15`, confirming the reconstructed dynamics. The full
propagator had 2-norm `4.662693544964e5`, smallest singular value
`1.260710881584e-6`, and condition number `3.698463789815e11`.
The progressive anisotropy is therefore genuine for this representation,
not a simple operator-reconstruction bug. A global inverse fundamental
frame is not suitable for a rigorous enclosure.

**Current next gate:** D47 r5d moving-balance / local QR-Lohner diagnostic.
Test stepwise/frequent coordinate frames that retain correlations without
forming a global ill-conditioned inverse. Do not launch all 18 case/mode
validated runs until the long-window wrapping problem is controlled.

Claim boundary unchanged:
`full_continuous_H1_error_enclosed=false`,
`rigorous_original_action_H1_integrator_error_enclosed=false`,
`GE05_bath_onshell_certified=false`,
`Z21_certified=false`.
No observation-based tuning and no lensing claim.


---

## D47 r5d fixed-vs-moving balance diagnostic (2026-09-30)

User-local r5d float diagnostic completed for the locked
primary/C_star/m=20 D17 full window. Original discrete fundamental
propagator reproduced prior r5c exactly:
2-norm `4.662693544964e5`, sigma_min
`1.260710881584e-6`, condition number
`3.698463789815e11`; global state replay relative
`4.112904877298e-15`.

A single fixed global diagonal balance selected at the midpoint reduced the
full-window propagator to norm `7.296925325302e1` and condition number
`5.651342638298e3`. More importantly, every transformed fine-step matrix
was near identity: maximum step 2-norm `1.022073939665`, maximum step
condition number `1.044910357879`.

A moving boundary balance reduced the full-window condition number further
to `1.202492459418e3` and norm to `6.883165847857e1`, but introduced
boundary scale transfers up to factor 2 and maximum transformed step norm
`2.005772664381`, condition number `2.035524800619`. Scale drift over
the window remained modest componentwise (ratios 1--8). Fixed and moving
reconstruction residuals were exactly zero in binary64.

Interpretation: the catastrophic r5b long-window box growth is primarily a
representation/wrapping problem. The fixed balanced frame is especially
attractive for validated propagation because it removes approximately six
orders of magnitude of raw conditioning while keeping every discrete step
close to identity and avoids moving-frame boundary transfers.

**Current next gate:** D47 r5e fixed-balance block/QR diagnostic to choose a
reconditioning block length and measure sequential-absolute box inflation
against signed block propagation. If local block products remain well
conditioned while unsigned propagation inflates strongly, implement the
validated Arb/Lohner-style correlated enclosure in the fixed frame before
running all 18 C/mode cases.

Claim boundaries unchanged:
`full_continuous_H1_error_enclosed=false`,
`rigorous_original_action_H1_integrator_error_enclosed=false`,
`GE05_bath_onshell_certified=false`,
`Z21_certified=false`.


---

## D47 r5d-r5e balanced-frame diagnostics (2026-09-30)

After the r5b full-window primary/C_star/m=20 Arb enclosure became
mathematically valid but physically uninformative because of long-window
wrapping, r5c reconstructed the discrete Radau fundamental propagator and
showed that the original-coordinate dynamics are genuinely highly
anisotropic: full 2-norm `4.662693544964e5`, smallest singular value
`1.260710881584e-6`, condition number `3.698463789815e11`, with global
state replay `4.112904877298e-15`.

D47 r5d tested fixed and moving diagonal balance frames. One fixed,
mid-window, power-of-two diagonal balance reduced the full propagator to
2-norm `72.96925325302` and condition number `5651.342638298`.
In that same fixed frame every individual Radau step was close to identity:
maximum step 2-norm `1.022073939665`, maximum step condition number
`1.044910357879`. A moving boundary balance reduced the full-product
condition number further to `1202.492459418`, but introduced boundary scale
transfers up to factor 2 and individual transformed step norms up to
`2.005772664381`. Fixed and moving reconstructions both matched the
original product to displayed zero; global state replay remained
`4.112904877298e-15`.

D47 r5e measured cancellation loss under sequential absolute-value box
propagation in the fixed balanced frame. Full signed product norm was
`72.96925325302408`; sequential absolute product norm
`6344.427662350447`, ratio `86.94658886463955`.
Local block behavior stayed well-conditioned:
block sizes 1,2,4,8,16,32,64 had maximum box/signed norm ratios
`1.00579, 1.01161, 1.02341, 1.04769, 1.10034, 1.22934, 1.62526`
respectively. At block size 8 the maximum signed block condition number was
only `1.41594`; at block size 16 it was `1.97844`.

Interpretation: the catastrophic r5b growth is dominated by repeated
componentwise wrapping, not failure of the local Radau map. The fixed
power-of-two balance is preferable for the next validated pilot because it
avoids moving-frame boundary terms while retaining near-identity local maps.

**NEXT D47 r5f:** certify one 8-step block using the fixed balanced frame,
rigorous Arb enclosures of each exact homogeneous step transfer around the
nominal Radau matrix, rigorous local collocation-defect forcing boxes, and
blockwise signed-product aggregation before collapsing to a box. If this
substantially improves the r5b eight-step endpoint bound, extend the same
validated block-transfer scheme through the full primary/C_star/m=20 window.

Claim boundary unchanged:
`full_continuous_H1_error_enclosed=false`,
`rigorous_original_action_H1_integrator_error_enclosed=false`,
`GE05_bath_onshell_certified=false`,
`Z21_certified=false`.


---

## D47 r5f fixed-balance first-8 Arb block result (2026-09-30)

D47 r5f rigorously enclosed the endpoint H1 error after the first eight
primary/C_star/m=20 D17 fine Radau substeps in one fixed power-of-two
balanced frame. Scope: Arb 192 bits, 8 x-subdivisions per fine substep.
Parent locks and original local-source SHA locks passed; endpoint replay was
exact and maximum scaled stage residual was
`3.5004747272454526e-16`. Minimum certified Az determinant magnitude
lower bound remained about `1.8576739053e10`.

The nominal eight-step block stayed benign:
2-norm `1.188672010731`, condition number `1.415943339927`.
However, the rigorous homogeneous transfer enclosure around each nominal
Radau step was very wide: maximum single-step fundamental radius entry
`0.7693889759130575`; the assembled eight-step transfer radius infinity
norm was `6.3392230066517845`.

The local archived-state collocation-defect forcing itself remained small:
maximum per-step weighted local forcing entry
`3.8010366584467623e-6`. The rigorous first-eight-step endpoint original
L1 error upper bound was `0.00489085394620988`, relative to archived
endpoint L2 norm `0.012718567258158483`.

This does NOT improve the existing r5b box propagation at the same endpoint
(`0.0048029868174418915`, relative `0.01249007055813272`);
the reported r5f/r5b "improvement" factor was `0.9820343993637`, i.e. r5f
is about 1.8% worse. Therefore signed block multiplication is not yet the
limiting issue in the rigorous implementation. The current bottleneck is the
over-wide interval enclosure of the homogeneous fundamental transfer, not the
local state residual.

r5f certifies only the eight-step endpoint error:
`first8_block_endpoint_H1_error_enclosed=true`.
It explicitly does NOT establish continuous H1 enclosure inside all eight
steps, full-window/all-mode H1, GE05 bath on shell, or Z21.

**NEXT D47:** diagnose and tighten the per-step fundamental transfer
enclosure before any full-window block run. First sweep x-subdivision and
fixed-vs-local balance on the first step, and measure interval operator /
fundamental-residual overestimation. Do not launch r5g full-window yet.


---

## D47 r5f2 subdivision convergence (2026-09-30)

D47 r5f2 swept the existing validated first-step fixed-balance construction
for primary/C_star/m=20 over x-subdivision counts 8,16,32,64. The
homogeneous fundamental-transfer radius converged almost exactly linearly
with segment width:
`0.7669195410 -> 0.3824449852 -> 0.1911268274 -> 0.09571683966`.
The local state collocation-defect forcing showed the same halving:
`3.6460891e-6 -> 1.8221506e-6 -> 9.1086272e-7 -> 4.5538896e-7`.

The rigorous first-step endpoint original-L1 / archived-L2 upper bound also
halved:
`1.530645891e-3 -> 7.649932037e-4 -> 3.824195094e-4 -> 1.911957144e-4`.
At nsplit=64 the endpoint L1 upper bound was
`7.02292833158882e-5`. Az remained strongly regular, endpoint replay was
zero, and the stage scaled residual remained
`3.5004747272454526e-16`.

Interpretation: the wide r5f homogeneous-transfer enclosure is dominated by
ordinary x-interval dependency proportional to segment width; there is no
current evidence that a centered/Neumann Az/operator reformulation is needed
before testing finer subdivision. This is diagnostic convergence evidence,
not a new all-window physics certificate.

**NEXT D47 r5f3:** repeat the complete first eight-step fixed-balance block
for nsplit 8,16,32,64 and test whether the block endpoint enclosure and block
transfer radius retain the same approximately 1/nsplit convergence. Do not
launch the 508-step full-window block run until this block-level convergence
is demonstrated.

Claim boundary unchanged: full all-case continuous H1, GE05 bath on shell,
full H4 Ward, Z21 and lensing remain OPEN.


---

## D47 r5f3 block-level subdivision convergence (2026-09-30)

D47 r5f3 repeated the complete first eight-step primary/C_star/m=20
fixed-balance Arb block for nsplit 8,16,32,64. The full block retained clean
first-order subdivision convergence. Maximum fundamental step radius:
`0.7693889759, 0.3836787336, 0.1917185089, 0.09601517227`.
Eight-step block transfer radius infinity norm:
`6.3392230067, 3.1159507421, 1.5470759960, 0.7724368553`.
Endpoint original-L1 upper bound:
`4.8908539462e-3, 2.4223367897e-3, 1.2054430923e-3, 6.0131180913e-4`.
Observed orders for endpoint L1 were
`1.01369, 1.00684, 1.00338`, essentially exact 1/nsplit behavior.

At nsplit=64 the first-eight-step endpoint relative upper bound was
`1.5636992582e-3`, improving the same-endpoint r5b bound by factor
`7.9875145383`. The nominal block remained unchanged and benign:
2-norm `1.1886720107`, condition number `1.4159433399`.

This establishes block-level interval-width dependency as the dominant
current enclosure error and shows that finer subdivision systematically
controls it. However, before a full-window run, close the formal archived-grid
parameterization gap: the r5f family currently parameterizes x using the
binary64 Radau step h=fl(xb-xa), while the exact archived endpoint interval is
defined by the two stored binary64 endpoints xa,xb. The difference is tiny but
must be included in a rigorous certificate.

**NEXT D47 r5f4:** exact-width endpoint correction on the first 8-step,
nsplit=64 block. Parameterize x by exact stored-endpoint width
`xb_exact-xa_exact`, retain the numerical Radau h in the collocation
polynomial, scale dp/dx by h/width, and explicitly add exact-real polynomial
endpoint-to-archived binary64 jumps for both the state and homogeneous step
map. Only if r5f4 is stable should the block method be extended full-window.

Claim boundary unchanged: full all-case continuous H1, GE05 bath on shell,
full H4 Ward, Z21 and lensing remain OPEN.


---

## D47 r5f4 exact-width formal closure (2026-09-30)

D47 r5f4 repeated the first eight-step primary/C_star/m=20 validated
fixed-balance block at nsplit=64 with exact stored-endpoint-width
parameterization. The continuous coordinate is
theta=(x-xa)/(xb_exact-xa_exact), the original binary64 Radau step
h=fl(xb-xa) is retained in the numerical polynomial, dp/dx includes the
exact h/width factor, and exact-real polynomial endpoint jumps are added
explicitly to both the homogeneous step map and archived state.

The formal correction was numerically negligible, as expected:
maximum homogeneous endpoint jump
`1.0794223306922099e-16`,
maximum state endpoint jump
`2.1357830058834712e-19`.
For these first eight adjacent stored points the exact binary64 subtraction
matches the exact stored-endpoint width, so the h/width mismatch is zero.

The validated block result is unchanged to displayed science precision:
nominal block 2-norm `1.188672010730937`,
condition number `1.415943339927396`,
transfer radius infinity norm `0.7724368553253664`,
endpoint original-L1 upper `6.013118112393102e-4`,
relative upper `1.5636992636631221e-3`.
This remains about `7.9875x` tighter than r5b at the same endpoint.

r5f4 therefore closes the archived-grid parameterization bookkeeping for the
pilot. It certifies the eight-step endpoint error only; continuous enclosure
inside all eight steps, the full window/all modes, GE05 bath on shell, full
H4 Ward, Z21 and lensing remain OPEN.

**NEXT D47 r5g0:** extend exactly the same formalized fixed-balance
construction from the locked initial state through the first 64 fine
substeps at nsplit=64. This is a medium-window endpoint pilot before paying
for all 508 fine substeps. If the 64-step bound remains controlled, proceed
to checkpointed full-window propagation.


---

## D47 r5g0 first-64 exact-width endpoint enclosure (2026-09-30)

D47 r5g0 extended the formalized r5f4 fixed-balance Arb construction to the
first 64 primary/C_star/m=20 fine Radau substeps at nsplit=64. All parent and
source locks passed. Exact stored-endpoint-width bookkeeping remained clean:
max h/width relative difference was zero on these stored points, max
homogeneous endpoint jump `1.1187071496204896e-16`, and max state endpoint
jump `3.923154623343181e-19`. Endpoint replay remained zero and the maximum
scaled stage residual remained `3.5004747272454526e-16`.

The local validated transfer remained stable across the 64-step window:
maximum fundamental step radius entry increased only from about 0.09572 to
`0.09835740897757052`; maximum local state forcing entry was
`6.544681307202042e-7`.

The 64-step nominal signed block had 2-norm `3.0722158054808117` and
condition number `9.605633868698574`. Its validated transfer-radius
infinity norm was `7.4177542045356315`. The rigorous endpoint original-L1
error upper bound was `0.007874136064092228`, relative to the archived
endpoint L2 norm `0.014293921320196266`.

At the same 64-step endpoint, the old r5b componentwise propagation gave
L1 upper `0.06242134929692224`, relative `0.11331349220894592`.
Thus r5g0 is tighter by factor `7.927390229079` while preserving the same
underlying original-action H1 dynamics.

r5g0 therefore demonstrates that the fixed-balance signed-block method
remains controlled over a medium window. It certifies the 64-step endpoint
only, not continuous enclosure throughout all 64 steps and not the full
508-step window/all modes.

**NEXT D47 r5g1:** run the same exact-width nsplit64 construction over the
full 508-step primary/C_star/m=20 window with checkpoint/resume support.
Record endpoint bounds and intermediate checkpoints; do not yet expand to
other modes/C cases. If the full-window endpoint bound remains informative,
add a separate continuous-within-step envelope pass before upgrading the
full H1 claim.

GE05 bath on shell, full H4 Ward, Z21 and lensing remain OPEN.


---

## D47 r5g0 formal block-algebra correction (2026-09-30)

While preparing the 508-step extension, a final rigor bookkeeping issue was
identified in the r5f/r5g block composition layer. Local x-segment operator,
Az, collocation-defect, and per-step transfer-radius quantities are Arb
outward-rounded. However, after converting those certified per-step upper
bounds to binary64, the multi-step center/radius recurrence and forcing
aggregation were performed by NumPy matrix products without an explicit
outward-rounding allowance for those matrix multiplications.

The missing allowance is expected to be at floating roundoff scale and does
not change the strong numerical diagnosis: r5g0 endpoint bound
`7.874136064092228e-3` is ~7.93x tighter than r5b, with stable local
transfer radii. But until the block algebra itself is recomposed in Arb, the
r5f4/r5g0 multi-step endpoint values are VALIDATED-CANDIDATE bounds, not the
final rigorous certificate.

**NEXT D47 r5g0r1:** rerun the first-64 nsplit64 calculation with the same
local certified step data but perform all signed nominal product,
center/radius recurrence, suffix propagators, and forcing accumulation in
Arb/acb matrices. Compare against r5g0. Only after this outward-rounded block
algebra agrees should the checkpointed 508-step r5g1 be launched.

No physics inputs or observational data are changed. GE05 bath, full H4 Ward,
Z21 and lensing remain OPEN.


---

## D47 r5g0r1 outward-rounded block algebra closure (2026-09-30)

D47 r5g0r1 repeated the first-64 primary/C_star/m=20 nsplit64 endpoint
calculation with the entire multi-step block algebra moved into Flint:
signed center products use acb, radius recurrences use arb, forcing
aggregation uses arb, and binary64 NumPy matrix products are excluded from
the certificate.

The result agrees with r5g0 to displayed science precision:
64-step block nominal norm `3.0722158054808113`, condition number
`9.60563386869856`, certified transfer-radius infinity norm
`7.417754204535626`, endpoint original-L1 upper
`0.007874136064092228`, and endpoint relative upper
`0.014293921320196268`. This is still about `7.92739x` tighter than
r5b at the same endpoint.

Formal controls remain clean: endpoint replay zero, max stage scaled residual
`3.5004747272454526e-16`, max homogeneous endpoint jump
`1.1187071496204896e-16`, max state endpoint jump
`3.923154623343181e-19`, and Az remains strongly regular.

Therefore the outward-rounding gate identified after r5g0 is closed for the
64-step pilot. The first-64 endpoint H1 enclosure is now rigorous under the
current source/parent locks. Continuous enclosure inside all steps, the full
508-step endpoint/window, other modes/C cases, GE05 bath on shell, Z21 and
lensing remain OPEN.

**NEXT D47 r5g1:** checkpointed full 508-step primary/C_star/m=20 endpoint
run at nsplit64. Use 64-step rigorous Arb/acb chunks, propagate the incoming
componentwise error through each chunk, checkpoint after every chunk, and
support safe resume after interruption. No observational data enter this
calculation.


---

## D47 r5g1 full-window endpoint result (2026-09-30)

D47 r5g1 completed the full 508-step primary/C_star/m=20 endpoint campaign
at nsplit=64 with exact-width Arb operator enclosures, outward-rounded acb/arb
64-step chunk algebra, rigorous incoming-error propagation between chunks,
and checkpoint/resume support.

The run completed all checkpoints 64,128,192,256,320,384,448,508 and ended
with classification
`GE19_D47_R5G1_FULLWINDOW_CSTAR_M20_ENDPOINT_ARB_PASS`.
The final endpoint original-L1 error upper bound is
`4.267278669717265`, versus archived endpoint L2 norm
`4.478851435897949`, giving relative upper
`0.9527618253901144`.

This is mathematically valid and dramatically tighter than the old r5b
full-window bound (L1 `48675.85992551011`, relative
`10867.933581224324`), an improvement factor of about `1.14e4`.
However, a ~95% relative endpoint bound is still too loose for a useful
physics-level H1 certificate.

The chunk trajectory shows smooth growth:
relative endpoint bounds at 64,128,192,256,320,384,448,508 steps were
approximately
`0.0143, 0.0320, 0.0549, 0.0889, 0.1468, 0.2558, 0.4805, 0.9528`.
Local step radii remained benign throughout (max fundamental step radius
~0.1036), so the remaining growth is not a local operator failure. It is
dominated by long-range enclosure/wrapping and the componentwise error-box
collapse at chunk boundaries.

Formal controls remain clean: endpoint replay zero, max scaled stage residual
~`3.61e-16`, exact-width mismatch zero, endpoint jumps ~1e-16/1e-18, and
Az remains strongly regular.

**NEXT D47 r5g2:** keep the same nsplit64 local step enclosures but remove the
64-step error-box collapse. Cache all 508 local nominal step maps, certified
step radii, and local forcing vectors, then perform one global backward
acb/arb suffix sweep across all 508 steps and aggregate every local forcing
term against its full signed suffix enclosure. This directly tests how much
of the 0.9528 bound is caused by chunk-boundary wrapping. Do not increase
nsplit or expand modes/C cases until this is measured.

Claim boundary unchanged:
`fullwindow_endpoint_H1_error_enclosed=true` only for this one
primary/C_star/m=20 endpoint;
`full_continuous_H1_error_enclosed=false`,
`rigorous_original_action_H1_integrator_error_enclosed=false`,
`GE05_bath_onshell_certified=false`,
`Z21_certified=false`.


---

## D47 r5g2 global signed-suffix endpoint result (2026-09-30)

D47 r5g2 reused the fully certified nsplit64 local step cache for all 508
primary/C_star/m=20 D17 fine steps and removed the 64-step endpoint-box
collapse. It performed one global backward signed suffix sweep with acb
center products, arb radius recurrence, and full-suffix forcing aggregation.

The run passed with classification
`GE19_D47_R5G2_GLOBAL_SIGNED_SUFFIX_FULLWINDOW_CSTAR_M20_ENDPOINT_ARB_PASS`.
The final endpoint original-L1 upper bound is
`2.6964426512869193`, archived endpoint L2 norm
`4.478851435897949`, relative upper `0.6020388686427415`.
This is a factor `1.5825586602706494` tighter than r5g1
(`4.267278669717265`, relative `0.9527618253901144`).

Therefore chunk-boundary componentwise collapse was a real loss, but not the
dominant remaining one. The global transfer radius still grows to
`8036.409106873319` while the nominal global product has 2-norm
`72.96925325302405` and condition number `5651.34263829795`.
This identifies long-range box/radius wrapping in the global transfer
enclosure as the main remaining bottleneck.

Local controls remain clean and unchanged: maximum single-step radius
~`0.1035866574`, max local forcing ~`1.0090910e-5`, endpoint replay zero,
stage residual ~`3.61e-16`, exact-width mismatch zero, and endpoint jumps
remain at floating roundoff scale.

A cache-only diagnostic using the certified A,D,q arrays shows that preserving
signed generator correlations is worth testing before increasing nsplit.
NEXT is therefore an affine complex-polydisc (no generator reduction)
propagation: carry all nominally propagated forcing/uncertainty generators
through the 508 steps, add only the new step uncertainty as eight diagonal
disc generators, and compute the final row-sum radius in Arb/acb. This avoids
both chunk-box collapse and the single global center/radius collapse.

Claim boundary unchanged: current result is a rigorous endpoint enclosure
for primary/C_star/m=20 only. Continuous H1, other modes/C cases, GE05 bath,
Z21 and lensing remain OPEN.


---

## D47 r5g3 affine-polydisc full-window endpoint result (2026-09-30)

D47 r5g3 propagated the certified r5g2 local A,D,q cache through all 508
primary/C_star/m=20 steps using an unreduced complex-polydisc generator set
in Arb/acb. Every historical generator is propagated through the signed
nominal step map; only the new multiplicative uncertainty and local forcing
are appended as eight fresh diagonal disc generators. No generator reduction
or NumPy product enters the certificate.

The run passed with classification
`GE19_D47_R5G3_AFFINE_COMPLEX_POLYDISC_FULLWINDOW_CSTAR_M20_ENDPOINT_ARB_PASS`.
Final generator count was 4064. The endpoint original-L1 upper bound is
`1.2668970351936948`, archived endpoint L2 norm
`4.478851435897949`, giving relative upper
`0.28286203579773334`.

This improves r5g2 by factor `2.1283834253149565` and r5g1 by factor
`3.3682916221086936`. The result confirms that preserving signed nominal
correlations is materially better than a single global center/radius box.

The remaining dominant loss is now the new per-step uncertainty box
`D_j * rad(E_j) + q_j`. A cache-only scaling diagnostic (not a certificate)
using the same affine propagation predicts relative endpoint bounds of about
0.1175, 0.0545, 0.0263, and 0.0129 if both local D and q were reduced by
factors 2,4,8,16 respectively. This is consistent with the previously
observed ~1/nsplit local convergence and motivates skipping nsplit128 as an
intermediate production run.

**NEXT D47 r5g4:** recompute all 508 local step enclosures at nsplit=256 with
checkpoint/resume, then run the same unreduced affine complex-polydisc
propagation. Target: a full-window endpoint relative upper bound near the
few-percent regime. This extrapolated target is diagnostic only until the
n256 run completes.

Continuous H1 inside every step, other modes/C cases, GE05 bath on shell,
Z21 and lensing remain OPEN.


---

## D47 r5g4 nsplit256 affine full-window endpoint result (2026-09-30)

D47 r5g4 recomputed the complete 508-step primary/C_star/m=20 local
original-action enclosure cache at nsplit=256 and then propagated the error
set with the unreduced affine complex-polydisc construction from r5g3.

The local refinement behaved as intended. Maximum certified single-step
homogeneous radius fell to `0.0262597739924021` and maximum local state
forcing to `2.522842970187365e-6`, close to the expected factor-four
reduction from nsplit64. Endpoint replay remained zero, max scaled stage
residual `3.613811247327609e-16`, exact-width mismatch zero, and endpoint
jump corrections remained at roundoff scale.

The nsplit256 affine run passed with classification
`GE19_D47_R5G4_N256_AFFINE_COMPLEX_POLYDISC_FULLWINDOW_CSTAR_M20_ENDPOINT_ARB_PASS`.
Final endpoint original-L1 upper bound is `0.24408679260001528`, archived
endpoint L2 norm `4.478851435897949`, and relative upper
`0.05449763094253632`. This is a factor `5.190354716446119` tighter than
the nsplit64 affine result. The companion n256 global signed-suffix enclosure
was `0.07208063466413411` relative, confirming that the affine generator
representation still provides additional tightening.

This is the first full-window endpoint result in the few-percent regime for
the locked primary/C_star/m=20 case. The remaining required gate before
calling this case a rigorous H1 integrator enclosure is continuous-in-x
control inside every fine Radau step.

**NEXT D47 r5g5:** continuous-within-step nsplit256 H1 enclosure for the same
locked primary/C_star/m=20 case. Reuse the certified r5g4 endpoint A,D,q
cache to provide the incoming endpoint error set at each fine step, and
recompute only the state collocation residual and interval original-action
operator inside each of the 256 x-subsegments. Use an entrywise-nonnegative
majorant of the Metzler comparison generator so its end-of-subsegment value
bounds the entire subsegment. Keep the affine endpoint propagation unchanged
between fine steps.

Other modes/C cases, GE05 bath on shell, Z21 and lensing remain OPEN.


---

## D47 r5g5 continuous H1 closure for primary/C_star/m20 (2026-09-30)

D47 r5g5 completed the continuous-in-x original-action H1 enclosure for the
locked primary/C_star/m=20 case. It reused the certified r5g4 nsplit256
affine-polydisc endpoint set as the incoming error at every D17 fine step and
recomputed the original-action state residual/operator on 256 x-subsegments
inside each fine Radau step.

The run passed with classification
`GE19_D47_R5G5_N256_CONTINUOUS_H1_CSTAR_M20_ARB_PASS`.
The maximum continuous original-coordinate L1 error upper bound over the
entire 508-step window is `0.2488989256895909`. The maximum rigorous
L1-error / D17-polynomial-L2 upper ratio is `0.05557368635602259`.
No subsegment had a zero polynomial-norm lower bound, so this relative
diagnostic is available globally.

The final endpoint exactly reproduces r5g4:
L1 upper `0.24408679260001528`, archived endpoint L2
`4.478851435897949`, relative upper `0.05449763094253632`, with affine
endpoint reproduction relative error exactly zero. Endpoint replay is zero,
max scaled stage residual is `3.613811247327609e-16`, and Az remains
strongly regular.

Therefore primary/C_star/m=20 now has a rigorous continuous original-action
H1 integration-error enclosure across the full D17 window. The global all
case/mode H1 flag remains OPEN because the other five positive Fourier modes
have not yet received this continuous enclosure.

**NEXT D47 r5g6:** screen the remaining primary/C_star modes
m={3,5,8,10,15} with the already validated nsplit64 affine endpoint pipeline.
This is the minimum next campaign needed for the central C_star physical
branch. Use the screen to choose per-mode refinement; do not yet spend n256
on all five modes. C_min/C_max and control-grid cases remain robustness
extensions, not the immediate GE05 gate.

GE05 bath on shell, full H4 Ward, Z21 and lensing remain OPEN.


---

## D47 r5g6r1 remaining C_star mode screen (2026-09-30)

The corrected r5g6r1 campaign completed the nsplit64 affine endpoint screen
for the five remaining primary/C_star modes. The original r5g6 failure was
only an implementation lock error: it incorrectly forced every mode to reuse
the m=20 fixed-balance scale vector. r5g6r1 instead uses the deterministic
mode-specific power-of-two balance and replays/locks it per mode.

All five science runs passed. Their nsplit64 affine endpoint relative upper
bounds are:

- m=3:  0.2476360721497, L1 upper 8.379641830487e-3
- m=5:  0.2371965289578, L1 upper 4.450045562574e-2
- m=8:  0.2379299903999, L1 upper 1.421474261854e-1
- m=10: 0.2423610064199, L1 upper 2.555628808684e-1
- m=15: 0.2599168590706, L1 upper 8.551946144190e-1

For reference, the existing m=20 nsplit64 affine endpoint relative upper is
0.2828620357977. Therefore all six C_star modes occupy the same broad
~0.24-0.28 relative-error regime at nsplit64. No remaining mode is already
tight enough to skip refinement.

The final all-six summary script itself failed only because it looked for the
old r5g6 m=3 output pathname instead of the r5g6r1 pathname. This occurred
after all five mode calculations had completed successfully and does not
invalidate any mode result.

**NEXT D47 r5g7:** recompute m={3,5,8,10,15} at nsplit256 with the same
mode-specific affine-polydisc method. m=20 already has nsplit256 endpoint
relative upper 0.05449763094 and continuous relative upper 0.05557368636.
Use the nsplit256 five-mode screen to decide if any mode needs more than
n256; otherwise proceed directly to their continuous-in-x passes.

GE05 bath on shell, full H4 Ward, Z21 and lensing remain OPEN.


---

## D47 r5g7 all-six C_star nsplit256 endpoint screen (2026-09-30)

D47 r5g7 completed the nsplit256 affine endpoint campaign for the five
remaining primary/C_star modes m={3,5,8,10,15}, using the corrected
mode-specific deterministic power-of-two balances from r5g6r1. Together
with the existing r5g4 m=20 result, all six positive Fourier modes now have
full-window nsplit256 affine endpoint enclosures.

Relative endpoint upper bounds:
- m=3:  0.05740451563496902
- m=5:  0.05012443707754402
- m=8:  0.049012960568540265
- m=10: 0.04957901154055716
- m=15: 0.05212792765546878
- m=20: 0.05449763094253632

The best endpoint relative bound is m=8 at ~4.90%; the worst is m=3 at
~5.74%. Thus every C_star positive mode is now in the same few-percent
endpoint regime at nsplit256. No additional endpoint-method development or
higher nsplit is justified before the continuous-in-x gate.

All five new affine runs passed. As a representative higher mode, m=15 used
508 fine steps, nsplit256, Arb precision 192, exact mode-specific balance,
and ended with L1 upper 0.171514549503219 and relative upper
0.05212792765546878. Local controls remained clean: zero endpoint replay,
stage residual ~4.30e-16, exact-width mismatch zero, and max local radius
~0.01499.

**NEXT D47 r5g8:** continuous-in-x nsplit256 H1 passes for
m={3,5,8,10,15}, reusing each r5g7 certified affine endpoint cache exactly
as r5g5 did for m=20. If all five pass with similarly modest continuous
inflation, the full primary/C_star six-mode continuous H1 branch is closed
and the project returns immediately to GE05 bath on-shell certification.

C_min/C_max and control-grid cases remain robustness extensions unless GE05
or the final theorem requires them. GE05 bath, full H4 Ward, Z21 and lensing
remain OPEN.


---

## D47 r5g8 all-six C_star continuous H1 closure (2026-10-01)

D47 r5g8 completed the continuous-in-x nsplit256 original-action H1
campaign for the five remaining primary/C_star positive Fourier modes
m={3,5,8,10,15}. Together with the existing r5g5 m=20 certificate,
the complete six-mode primary/C_star branch is now continuously enclosed.

All five new mode runs passed and the final summary classification is
`GE19_D47_R5G8_PRIMARY_CSTAR_ALL6_N256_CONTINUOUS_H1_COMPLETE`.

Maximum continuous L1 / D17-polynomial-L2 upper bounds:
- m=3:  0.0581383470072098
- m=5:  0.0509709529145299
- m=8:  0.04991644368061971
- m=10: 0.0505165897113902
- m=15: 0.0531416787551773
- m=20: 0.05557368635602259

The worst continuous relative upper bound is m=3 at ~5.814%.
No mode has a zero polynomial-norm lower segment, so the continuous
relative diagnostic is available globally across all six modes.

Final endpoint relative uppers exactly reproduce the already-certified
n256 affine endpoints:
m3 0.05740451563496902,
m5 0.05012443707754402,
m8 0.049012960568540265,
m10 0.04957901154055716,
m15 0.05212792765546878,
m20 0.05449763094253632.

Therefore the central primary/C_star six-mode continuous original-action H1
branch is closed at nsplit256. No further H1 endpoint/continuous refinement
is planned unless a later GE05 source term exposes a specific missing
componentwise requirement.

**NEXT PHYSICS GATE:** return to the preregistered GE05 bath on-shell line.
D13/D14 established the original signed bath structure and source-weighted
phase behavior but left continuous on-shell status open. D15 already
registered the exact variable-background step-defect identity
`R_GE05 = 3 a^3 v/tau (H_true-h_mid/tau)
          + a^3 (r/tau)^2 (X_lin-X_true)`.
Use the now-certified continuous H1 branch to construct rigorous continuous
H/X10 driver enclosures for the central C_star six-mode branch, then close
or explicitly fail the GE05 bath on-shell bound without relaxing any prior
science target.

Full all-sector H4 Ward, Z21 and lensing remain OPEN.


---

## D48 continuous X10 envelope and sampled GE05 bridge (2026-10-01)

D48 consumed the closed D47 primary/C_star six-mode continuous-H1 branch
and produced a rigorous continuous absolute error envelope for the
original-action D17 X10 representation:
`|X_true-X_D17poly| <= (sup|Q|+sup|k/a|) E_L1`
on every D17 fine step.

The run passed with classification
`GE19_D48_CSTAR_CONTINUOUS_X10_ENVELOPE_PASS_D15_SAMPLED_BRIDGE_GE05_ONSHELL_OPEN`.
Uploaded result SHA-256:
JSON `f1ab1be3f5ce7c486bc45ec1776ef4c8e8a2b7fd81dfa7d9302659df8659cff5`,
NPZ `9046b5772fc7bcac704d163351cea1c5815d9bfab03f7c8aeebf98a04b469a1e`,
log `0a0b34b71d5a13d9b7e6e67f36129ca7fe0a4df56ad2889572179532285dbd31`.

Maximum continuous absolute X10-error uppers by mode:
m3 4.795165767189028e-5,
m5 3.8783142096444277e-4,
m8 1.9333727155863526e-3,
m10 4.315459400535249e-3,
m15 2.1239082720809238e-2,
m20 4.030459203432021e-2.
The global maximum is the m20 value 0.04030459203432021.

At the frozen D15a theta={0,1/2,1} samples, the provisional drive-envelope
L2 values using only the D47/D48 true-minus-D17-polynomial error were about
8.86e-7, 9.03e-7 and 9.20e-7 for Nq2048, with Nq1024 agreeing to roughly
1e-7 relative. These drive terms dominate the previously frozen clock-only
unsigned envelope by factors ~2.7e3--2.9e3.

**Formal correction before GE05 promotion:** D15's exact defect is written
relative to the frozen original R1 affine drive X_lin, while D48 rigorously
bounds X_true relative to the D17 continuous collocation polynomial.
Therefore the sampled D15 bridge must also include the known center
displacement `|X_D17poly-X_R1lin|` at theta=0,1/2,1. The continuous
D48 X10 envelope itself remains valid; only the provisional
`sampled_D15_drive_uncertainty_bounded` promotion is suspended until this
center-displacement term is added.

**NEXT D48r1:** compute the exact frozen D17-vs-R1-affine X10 displacement
at theta=0,1/2,1 from the D17 dense archive, add it modewise to the rigorous
D48 epsilon_X, and rebuild the sampled D15a U_X source envelope. Do not
launch a continuous GE05 on-shell certification before this corrected bridge
is frozen.

GE05 bath on shell, full H4 Ward, Z21 and lensing remain OPEN.


---

## D48r1 sampled D15 center-displacement correction (2026-10-01)

D48r1 corrected the D48 sampled D15 bridge by adding the deterministic
D17-collocation-center minus original-R1-affine center displacement at the
already-frozen theta={0,1/2,1} samples.

The run passed with classification
`GE19_D48R1_CSTAR_SAMPLED_D15_CENTER_CORRECTED_BRIDGE_PASS_GE05_ONSHELL_OPEN`.
Uploaded result SHA-256:
JSON `e7b4c6579a84225c3ebb49be738f81f889d323f42fabed7a11fb238a5fd89537`,
NPZ `0413553dc4dcfe34eeb2747cd5f65a5e4e0002bbf7aef631b32b272feb0af90e`,
log `7209a2b9822beb9ea88c9e40d1ae44884cfe9a9b38219515115fdc7845f8a251`.

The missing center term is numerically negligible. The largest sampled
center displacement occurs for m=20 at theta=1/2 and is
`8.313899903915263e-9`. The corrected m20 epsilon_X maximum at theta=1/2
is `0.04030460034822011`.

For Nq2048 the corrected sampled drive L2 values are
`8.858717147305045e-7`, `9.030010941695075e-7`,
and `9.204007942358936e-7` at theta=0,1/2,1. The maximum correction
factor relative to the provisional D48 bridge is only
`1.000000161611577`. Thus the D48 sampled numerical conclusion is stable,
but D48r1 remains a sampled bridge only.

**NEXT D48r2:** bound the D17-collocation versus original-R1-affine X10
center displacement continuously over every original interval, and in the
same original-action interval pass construct rigorous
`epsilon_H = |H_true-sqrt(H_i H_{i+1})|` envelopes. Combine the continuous
center bound with D48's true-minus-D17-polynomial envelope to obtain the
continuous D15 `epsilon_X` parent required by the exact GE05 defect
identity.

GE05 bath on shell, full H4 Ward, Z21 and lensing remain OPEN.


---

## D48r2r1 index-mapping correction gate (2026-10-01)

D48r2r1 completed numerically, but its own endpoint replay control exposed an
implementation error in the continuous X-center reconstruction. The reported
`D17_dense_X_endpoint_replay_abs_upper_max` was
`6.705324376892e-4`, far too large for a reconstruction of the archived
D17 action X10 center.

Source audit identified the exact cause. D17 canonical state is
`y=(S,u,phi,T,pS,pu,pphi,pT)`, and the archived D17 action drive is built as
`X10 = Q_action*y[1] + (i k/a)*y[2]`. D48r2/r2r1 mistakenly used
`y[2]` and `y[3]` (phi,T), shifting both drive components by one slot.
This explains both the large endpoint replay and the inflated continuous
center-displacement values (~3e-4--7e-4), which must not be used as certified
epsilon_X parents.

The D48 and D48r1 results remain valid: D48 only used a componentwise H1 L1
error bound to enclose true-minus-D17 X10, and D48r1 compared archived
Xdense directly to archived original-R1 X knots. The independently computed
D48r2 epsilon_H background envelope (~2.0204e-6) is not affected by this
canonical-index bug, but the D48r2 continuous epsilon_X/center certificate is
withdrawn pending rerun.

**NEXT D48r2r2:** rerun the continuous R1 center construction with the exact
D17 mapping `u=y[1], phi=y[2]`, including matching stage derivatives
`fy[1],fy[2]`. Add a hard endpoint-replay gate before accepting any
continuous-center result.

GE05 bath on shell remains OPEN.


---

## D48r2r2r1 continuous R1 epsilon_H / epsilon_X closure (2026-10-01)

The corrected D48r2r2r1 run passed for primary/C_star with the exact D17
canonical X10 mapping `X10=Q_action*y[1]+(i*k/a)*y[2]`. Parent locks passed,
Arb precision was 192 bits, and the exact-rational original-theta check was
active.

The hard D17 dense-X endpoint replay control passed decisively:
maximum absolute replay upper `6.263278924221237e-20` against the frozen
gate `1e-10`. Radau stage scaled residual remained
`4.304149139297149e-16`; the D48r1 sampled center corrections are contained
with positive minimum margin `8.51842556708393e-11`.

Continuous original-R1 driver parents are now closed for the central C_star
six-mode branch:
- epsilon_H max upper = `2.020375979332667e-6`
  (median `1.0491107239353201e-6`);
- epsilon_X global max upper = `0.04030463514324942`.
Modewise epsilon_X max uppers:
m3 `4.795197873549524e-5`,
m5 `3.8783337602686034e-4`,
m8 `1.933378900370822e-3`,
m10 `4.31547022757525e-3`,
m15 `2.1239115574250542e-2`,
m20 `4.030463514324942e-2`.
The continuous D17poly-minus-R1lin center itself is tiny: from
`3.914187112451229e-10` (m3) to `5.260475954838029e-8` (m20).

Uploaded result SHA-256:
JSON `cabb027ca83636501d7b9050550b5fe051b037ac90505d5340586a72b6c5d42c`,
NPZ `a5b37563b8a9666900b52e37f71bfa70860fde9a8d3eb466f126c63c601fb19c`,
log `7e4188c32c62b9d90c69749b3a0f1bbb202dcb7066225465dcdf27bced451a22`.

Metadata note: the JSON `continuous_epsilon_X.construction` prose inherited
an old phi/T wording. The actual accepted code path and the explicit control
field use the correct y[1],y[2] mapping, and the 6.26e-20 endpoint replay
hard-gates this source contract. Do not copy the stale prose into a paper.

**NEXT D49:** construct a rigorous continuous envelope for the frozen
Repair24 first-order bath z_step and v_step on every quadrature node, input
mode and original R1 interval. Combine it with the certified D48r2r2r1
epsilon_H/epsilon_X/a^3 parents in the exact D15 GE05 residual identity,
then propagate the resulting residual through the full signed +/- six-mode
bath source. Report the noncancelling source envelope against the frozen D14
unsigned ODE/FD4 source scales; do not invent a post-hoc smallness threshold.

GE05 bath on shell, full H4 Ward, Z21 and lensing remain OPEN until D49.


---

## D49 continuous GE05 residual/source envelope decision (2026-10-01)

D49 completed the preregistered primary/C_star continuous frozen-bath
z/v envelope, exact D15 residual inequality, and full noncancelling signed
+/- six-mode source propagation. Construction PASS classification:
`GE19_D49_CSTAR_CONTINUOUS_GE05_RESIDUAL_SIGNED_SOURCE_ENVELOPE_PASS_ONSHELL_DECISION_OPEN`.

Uploaded result SHA-256:
JSON `4d74685f3b41e33c7a579d2a2b82af5fe496d5870dcf22a0f250953ed5a97f45`,
NPZ `63d348642010476099ed491b957c9fac4235bf0ca08c0af7772535012caf074f`,
log `e2449a86477250a0a459cd25b03c3058c9bab2bf0f7377eba7f0364d0df4a3d8`.

The envelope is NOT negligible on the already-frozen D14 physical source
scale, so GE05 on-shell cannot be promoted from D49. For Nq2048,
W_total unsigned L2 upper is `15.5869874145`, about
`5.4478e12` times the frozen D14 ODE unsigned L2 scale and
`1.5735e14` times the frozen D14 FD4 unsigned L2 scale. Nq1024 gives
`3.89869201357` with ratios `1.3626e12` and `3.9049e13`.

Two distinct effects are visible and must not be conflated:
1. The H-clock piece is infrared-nonuniform under the D49 energy majorant.
   Its W_H L2 changes by factor `3.99805` between Nq1024 and Nq2048,
   matching the low-r quadrature scaling. This is a certificate-looseness
   issue, not evidence of a physical divergence.
2. The X-driver piece is quadrature-stable:
   W_X L2 is `6.94932926e-5` (2048) and `6.94932921e-5` (1024),
   ratio `1.00000000746`. Yet W_X alone is already about
   `2.4289e7` times the frozen D14 ODE unsigned scale and about
   `7.0e8` times the D14 FD4 unsigned scale. Therefore fixing only the
   low-r H majorant cannot close GE05.

The immediate blocker is the current rigorous continuous X10 error parent:
D48r2r2r1 epsilon_X is mathematically valid but much too loose for the tiny
second-order GE05 source scale. Do not spend the next run only tightening
the bath-v infrared bound.

**NEXT D50:** run a source-locked high-resolution original-action H1/X10
numerical convergence diagnostic on primary/C_star using Radau substeps
4,8,16 for all six modes. Reproduce the archived D17 sub4 solution exactly,
then measure X10 sub4-vs-sub8 and sub8-vs-sub16 differences and observed
order. This is diagnostic only, not a new certificate. Its purpose is to
decide if the large D48 epsilon_X is wrapping/conservatism (then build a
targeted adjoint/functional X10 certificate) or reflects a genuinely large
integration uncertainty.

GE05 bath on shell, full H4 Ward, Z21 and lensing remain OPEN.
