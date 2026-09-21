# GE19 Repair23 q20 normalized-bath bridge audit lock

## Status

**DIAGNOSTIC BRIDGE IMPLEMENTATION LOCKED BEFORE REPAIR23 RESULT**

Repair22 is frozen as

`GE19_REPAIR22_ON_SHELL_PARENT_Z20_CERTIFICATION_PASS`

with

`Z20_certified = true`.

Repair23 is a normalization/equation bridge only. It does not construct q20 and does not solve H4/Z21.

## Parent Repair22 freeze

Commit:

`9174f2e622f42851474ed124b429bf07b2db3ac7`

File:

`docs/ge19_repair22_z20_certification_result_freeze.md`

Blob:

`fb4ef607d17b5545985edf557aa67d02bc4dff0f`

Frozen Repair22 artifacts:

- JSON SHA-256:
  `7d53b2458183c6b2cc326acdded70b2c3ce1fab959d8456e56d3b4f1f86ef374`;
- NPZ SHA-256:
  `3020e0d040f902ab2609e05705f4508d9919665b1344fa0e641644ea8fc41a16`.

## Repair23 preregistration

Commit:

`23dfb02064dd987a24c5bcbb2ab574b7f725dbe0`

File:

`ge19/repair23_predata_q20_normalized_bath_bridge_audit.json`

Blob:

`199fccde48fecfa143ef142015cc047ae39429be`.

## Repair23 implementation

Commit:

`314dd46026295d78aadf2066e3e0d4721d9c8cba`

File:

`ge19/repair23_q20_normalized_bath_bridge_audit.py`

Blob:

`6d85770ab03bf2ce2d9646c3396bc60047848a15`.

## Frozen theory dictionary

Per-node longitudinal NL0B action:

`N L R^2 / 4 * [(Aq)^2-(omega q-sqrt(w) X)^2]`.

Normalized bath variable:

`z_j = omega_j q_j / sqrt(w_j)`.

Therefore:

`q_j = sqrt(w_j) z_j / omega_j`.

FLRW cosmic-time equation:

`ddot z_j + 3 H dot z_j + omega_j^2 (z_j-X) = 0`.

Dimensionless time:

`xi=t/tau`.

With

`r_j=omega_j tau`

and

`h=H tau`,

the equation is

`z_xixi + 3 h z_xi + r_j^2 (z_j-X)=0`.

## Frozen second-directional bath hierarchy

First order:

`G1[Z10,z10]=0`.

Second order:

`G1[Z20,z20] + G2[(Z10,z10),(Z10,z10)] = 0`.

Factor convention:

`Z=Zbar+eps Z10+eps^2 Z20/2+...`.

The future q20 dictionary is

`q20_j=sqrt(w_j) z20_j/omega_j`.

## Frozen GE19 scalar dictionary

- N direction -> N10/N20;
- longitudinal and transverse scales -> S10/S20;
- shift b -> 0 in the frozen plane-symmetric scalar reduction;
- aether rapidity -> u10/u20;
- scalar -> phi10/phi20;
- first-order drive:
  `X10=Q_action u10 + partial_x(phi10)/a`.

No nonlinear `k chi` rule is inserted.

## Frozen future q20 boundary convention

First-order bath at z=1.5:

inherit the full-history positive-Drude retarded state, then evolve on the reduced on-shell H1 parent inside the GE19 window.

Second-order bath:

`z20=0`

and

`dz20/dxi=0`

at z=1.5.

This defines a window-local particular second-order bath state consistent with the certified window-local particular nature of Repair22 Z20. It does not claim a primordial second-order bath mode.

## Frozen gates

- exact symbolic q->z FLRW identity;
- exact cosmic->dimensionless identity;
- GE05 c1 bath residual vs standard linear z equation relative L2 <= `1e-10`;
- GE05 c2 bath residual vs centered second-directional FD <= `1e-5`;
- GE05 c2 primary/control FD <= `1e-5`;
- normalized c1/c2 weight scaling <= `1e-12`;
- NL1C4 exact interval step vs independent DOP853 q relative L2 <= `1e-8`;
- same v relative L2 <= `1e-8`;
- all outputs finite.

## Frozen source implementations

GE05 memory directional generator:

blob

`40837d77f89028da30c28899e2d0530a4401844e`.

NL1C4 expanding retarded bath integrator:

blob

`7a9ffab9fa903ca61e88627052e2aa589b4bf459`.

## Dedicated prelock

Workflow:

`.github/workflows/ge19-repair23-prelock-audit.yml`

Run:

`35645315730`

Job:

`106484222035`

Conclusion:

`success`.

Terminal marker:

`GE19_REPAIR23_PRELOCK_AUDIT_PASS`.

The prelock reproduced:

- Repair22 freeze blob:
  `fb4ef607d17b5545985edf557aa67d02bc4dff0f`;
- GE05 blob:
  `40837d77f89028da30c28899e2d0530a4401844e`;
- NL1C4 blob:
  `7a9ffab9fa903ca61e88627052e2aa589b4bf459`.

## Routing

Only:

- `GE19_REPAIR23_Q20_NORMALIZED_BATH_BRIDGE_AUDIT_PASS`;
- `GE19_REPAIR23_Q20_NORMALIZED_BATH_BRIDGE_AUDIT_FAIL`;
- implementation failure.

## Stop rule

No q20 solve before Repair23 PASS is frozen.

No H4/Z21.

No finite eta.

No observational inference.
