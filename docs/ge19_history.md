# GE19 reduced weakly nonlinear track — persistent history

Last updated: 2026-09-21

Branch:

`physics-first-gravitational-elasticity`

This file is the persistent scientific history for the GE19 reduced weakly nonlinear construction.

Historical classifications are immutable. A FAIL is never relabelled after a later repair succeeds. Implementation failures, diagnostic audits, science FAILs and certified PASS results are kept distinct.

## Current checkpoint

The latest **executed** science/diagnostic result is Repair16:

`GE19_REPAIR16_CANONICAL_ZERO_INITIAL_STATE_AUDIT_COMPLETE`

with route

`QUADRATIC_SOURCE_NOETHER_INCOMPATIBILITY_REMAINS`.

Repair16 result-freeze commit:

`d5a619495f0f8fb2da53528b46476a15c1a32922`

Repair16 JSON SHA-256:

`768d5a2de7cd62059e7149a4765ab5a9663eef708fc29989c05192f607c5bf68`.

The locked Repair17 science-runner HEAD is:

`152da4a51e89c318aa97632815ea714b8f61ef3c`.

Later documentation-only commits may advance the branch HEAD without changing the locked Repair17 science blobs. The local runner verifies the frozen blobs and ancestry before execution.

Repair17 is **LOCKED AND READY, NOT YET LOCALLY EXECUTED**.

Dedicated Repair17 prelock:

- workflow run `35609640571`: SUCCESS;
- terminal marker `GE19_REPAIR17_PRELOCK_AUDIT_PASS`.

Runner-head static audit:

- workflow run `35609805995`: SUCCESS.

The next command is therefore the local Repair17 canonical initial-manifold audit. No Repair18, no new H3 trajectory, no q20 and no H4/Z21 are licensed before the Repair17 result is frozen.

---

## Scientific status in one line

`H1/background certified -> first H3/Z20 attempt failed shift constraint -> zero-velocity and canonical-zero initial boundaries both excluded -> full canonical initial constraint-manifold existence test is next`.

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

## Repair17 — current locked next gate

Preregistration commit:

`7d5664743b2bda32fcd1a444ece37cdc14a3d96d`.

Implementation commit:

`753015f7a377ca8bfe541cace99fb239b49a7654`.

Prelock workflow commit:

`159f68307990ab6a1b131a9b74c350c831f5ecdb`.

Implementation-lock commit:

`17487d847ddfaf6ac64b0c648156f1b69295b3ec`.

Locked local-runner HEAD:

`152da4a51e89c318aa97632815ea714b8f61ef3c`.

Repair17 asks a stronger and cleaner question.

At z=1.5, after the frozen algebraic reconstruction

`w(y)=WY y + WR source`,

does **any** canonical state

`y=(S,u,phi,T,pS,pu,pphi,pT)`

exist that satisfies the independent lapse and shift constraints?

Tests:

1. full canonical y: 2x8;
2. q-only: 2x4 with p=0;
3. p-only: 2x4 with q=0.

No time integration is performed.

Frozen possible routes:

### Route A

`FINITE_WINDOW_ZERO_BOUNDARY_INADMISSIBLE_SOURCE_COMPATIBLE`.

Meaning:

the full canonical initial constraint manifold exists. Repair15/16 then diagnose inadmissible zero-boundary choices, not a broken quadratic source.

A later separately preregistered propagation repair may initialize on a constraint-compatible y0 and retest H3/Z20.

### Route B

`QUADRATIC_SOURCE_INITIAL_NOETHER_INCOMPATIBILITY_CONFIRMED`.

Meaning:

even the full 2x8 canonical state cannot satisfy lapse+shift for the frozen source.

Only then is a direct sector-by-sector GE06+GE07+Lambda quadratic Noether/source audit licensed.

---

## What is certified now

Certified:

- NL0B covariant memory construction;
- weakly nonlinear source infrastructure;
- GE06 analytic Einstein+AeST directional generator;
- GE07 pressureless-matter directional generator;
- Repair13 self-consistent reduced background;
- Repair13 reduced H1 / Z10 Stage-A closure.

Not certified:

- Z20;
- q20;
- H4/Z21;
- finite-eta nonlinear trajectory;
- nonlinear lensing or nonlinear matter observables;
- any real-data nonlinear-memory inference.

## Data-readiness boundary

The project is **not yet ready for a nonlinear real-data claim**.

The shortest valid route is:

`Repair17 -> constraint-certified Z20 propagation -> observable bridge -> real-data confrontation`.

For the full nonlinear-memory state claim:

`constraint-certified Z20 -> q20 -> H4/Z21 -> observable bridge -> data`.

Lensing remains a natural first observable after state certification because the model acts directly through gravitational potentials. CMB/SPT high-l and structure probes remain later comparison channels.

No observational result may be used to choose or tune a repair in the theory chain.

---

## Immediate action

Run the locked local Repair17 audit using runner/blob lock rooted at

`152da4a51e89c318aa97632815ea714b8f61ef3c`.

A later documentation-only branch HEAD is allowed because the runner rechecks the frozen science blobs and lock ancestry.

Until that result is frozen, the canonical project status is:

**Repair13 H1 PASS; Repair14 H3/Z20 FAIL; Repair15 and Repair16 diagnostic incompatibility results frozen; Repair17 READY / NOT YET EXECUTED.**
