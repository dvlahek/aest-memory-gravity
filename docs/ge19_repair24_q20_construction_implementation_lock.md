# GE19 Repair24 q20 construction implementation lock

## Status

**SCIENCE IMPLEMENTATION LOCKED BEFORE REPAIR24 RESULT**

Repair22 remains frozen:

`GE19_REPAIR22_ON_SHELL_PARENT_Z20_CERTIFICATION_PASS`

with

`Z20_certified = true`.

Repair23 remains frozen:

`GE19_REPAIR23_Q20_NORMALIZED_BATH_BRIDGE_AUDIT_PASS`.

Repair24 is the first actual q20 construction. No H4/Z21 solve is included.

## Frozen parent chain

Repair22 result-freeze commit:

`9174f2e622f42851474ed124b429bf07b2db3ac7`.

Repair22 freeze blob:

`fb4ef607d17b5545985edf557aa67d02bc4dff0f`.

Repair23 result-freeze commit:

`79597296185209e50ef133f680d7b3d3481bac86`.

Repair23 freeze blob:

`5081fdf87e7e7f76849cf94e01f74c8df5dcca80`.

## Frozen Repair24 files

Preregistration:

`ge19/repair24_predata_q20_construction.json`

final blob:

`df2a197a87c426b2b45aca8ab95bbdbbbbc19fbf`.

Science implementation:

`ge19/repair24_q20_construction.py`

final blob:

`fc271987d1bddcd023cc9c057ddcad036b1d72fb`.

Dedicated prelock:

`.github/workflows/ge19-repair24-prelock-audit.yml`

final blob:

`bc6bd4d441b7322a42f0f27094e0360370796a6f`.

## Frozen numerical scope

- tau H0 = 10;
- C = C_min, C_star, C_max;
- beta0 = 1, 0.5, 0.1;
- m = 1..40;
- Nt primary/control = 128/64;
- Nx primary/control = 512/256;
- positive Drude quadrature primary/control = 2048/1024;
- GE19 window 0.2 <= z <= 1.5.

## Frozen normalized bath equation

[
z_j = omega_j q_j/sqrt{w_j}.
]

The second-order normalized bath equation is

[
G_1[Z_{20},z_{20}]
+
G_2[(Z_{10},z_{10}),(Z_{10},z_{10})]
=0.
]

Equivalent forced form:

[
ddot z_{20,j}+3Hdot z_{20,j}
+omega_j^2(z_{20,j}-X_{20})
=
-G_{2,j}^{m norm}.
]

No new physical parameter is introduced.

## Frozen first-order bath boundary

Frozen v0.77 artifact:

- run ID: `34315590099`;
- artifact ID: `10090367181`;
- artifact name: `results_bundle_v077_native_state_tangent_affinity`;
- artifact digest:
  `sha256:24b97e5738eb07be4f12d433ff5f9fe22249e199e186d5617aca5dc81f748378`.

Frozen base trace:

- file: `v076_v077_base_trace.dat`;
- SHA-256:
  `98c8468e8ccdf902cad8d6e65f3852e863c6fd19df62ece61353ab725ac5a43e`;
- bytes: `2657188`.

The frozen trace has no native sample exactly at a=0.4.

Prelock proves the exact bracket:

- lower index 10:
  `a_lo = 0.3799548579266745`;
- upper index 11:
  `a_hi = 0.41924557250685585`;
- ln(a) interval width:
  `0.09840438940521079`;
- k relative mismatch:
  `0.0`;
- common-time mismatch:
  `0.0`.

Repair24 therefore transports the retarded bath to exactly a=0.4 by:

1. integrating the frozen full-history bath through the lower native node;
2. taking one partial step of the **same frozen NL1C4 step_linear interval model**;
3. using the same parent-interval constant
   `h_m=sqrt(h_lo h_hi)`;
4. using the same source-linear-in-xi convention;
5. stopping at exactly `ln a = ln 0.4`.

Because h_m is fixed on the parent interval, the target source is the corresponding ln(a)-linear interpolation of chi/a.

The GE19 initial surface is not moved.

## Frozen second-order boundary

Window-local particular bath boundary:

- `z20(a=0.4)=0`;
- `dz20/dxi(a=0.4)=0`.

No primordial/homogeneous second-order bath mode is claimed.

## Frozen source construction

The nonlinear bath source is generated from the frozen GE05 second directional bath Euler-Lagrange residual.

Normalized source:

[
G_2^{m norm}
=
-rac{2omega}{sqrt w},E_{q}^{(2)}.
]

The symbolic normalized generator removes sqrt(w) exactly before numerical evaluation.

Prelock verifies:

`NORMALIZED_C2_SQRTW_ABSENT = True`.

The vectorized interval propagator is algebraically matched to the frozen NL1C4 per-node propagator.

Prelock verifies:

`STEP_ND_SELF_TEST = 0.0`.

## Certified q20 projection

The persisted physical q20 object is

[
sum_j w_j z_{20,j}.
]

This is the bath combination required by the completed-square linear memory block in the future H4 source.

Full node states are deterministic auxiliaries and are recomputable from the frozen inputs; they are not persisted in the final NPZ.

Also persisted:

- weighted z10;
- weighted G2;
- X20;
- B20_linear = X20 - weighted z20;
- quadrature and time controls.

## Frozen gates

- Repair22 Z20 certified;
- Repair23 bridge PASS;
- frozen v0.77 bracket exactly reproduced;
- partial step reaches a=0.4 to <= 1e-15;
- H1 X10 at initial surface matches transported v0.77 drive to <= 1e-10;
- G2 Nx256/Nx512 low-mode relative L2 <= 1e-10;
- q20 weighted-z20 Nq1024/Nq2048 relative L2 <= 1e-2;
- q20 weighted-z20 Nt64/Nt128 relative L2 <= 5e-3;
- z10 weighted response Nt64/Nt128 relative L2 <= 5e-3;
- all weighted outputs finite;
- all C,beta,m cases complete;
- normalized c2 sqrt(w) cancellation exact;
- vectorized interval propagator self-test <= 1e-12.

No threshold may be changed after seeing Repair24 output.

## Prelock history

Several pre-science implementation/audit failures occurred and remain historical:

- relative-path quiet-loader failure;
- reference self-test wiring failure;
- discovery that the frozen v0.77 trace has no exact a=0.4 native sample;
- syntax-only artifacts introduced while amending the bracketed boundary code/workflow.

None executed the q20 science construction.

The exact trace bracket was established by prelock run

`35652450043` — SUCCESS.

The pre-fix amended implementation prelock was

`35653683119` — SUCCESS.

A first local execution then failed before any q20 science output because `reconstruct_backgrounds()` incorrectly mapped Repair24 Nt128 `primary` onto Repair13's frozen `primary` array, which is Nt64. NumPy therefore raised a `(128,)` versus `(64,)` broadcast error during provenance checking.

This is classified as an **implementation failure before science**. No q20 state, source-convergence value, quadrature-convergence value, time-convergence value, gate result or classification was produced.

Implementation-only repair commit:

`7218e049e5e3a1a413663f587d98f8100f22cfa4`.

The repair changes only background provenance checking:

- Repair24 Nt64 control is compared elementwise to frozen Repair13 Nt64 primary;
- Repair24 Nt128 background is rebuilt deterministically with the same frozen Repair13 `reduced_background` function, as already done by Repair22;
- the existing exact Repair22 Nt128 x-grid check remains unchanged.

No q20 equation, source, boundary, Drude measure, grid, threshold or physics parameter changed.

A dedicated regression guard was added to the prelock in commit

`3027179251e227cf4285cc9ae75d2c20770a96b2`.

The final post-fix implementation prelock is

`35696839240` — SUCCESS.

Final prelock controls include:

- compile PASS;
- frozen provenance PASS;
- normalized c2 sqrt(w) cancellation PASS;
- vectorized propagator self-test exactly `0.0`;
- exact frozen v0.77 artifact download PASS;
- exact a=0.4 trace bracket PASS.

## Routing

Only:

- `GE19_REPAIR24_Q20_CONSTRUCTION_PASS`;
- `GE19_REPAIR24_Q20_CONSTRUCTION_FAIL`;
- implementation failure before valid science output.

## Stop rule

No H4/Z21 until Repair24 q20 is executed, frozen and PASS.

No finite eta.

No observational inference.
