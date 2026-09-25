# GE19 H4F3d7 — valid frozen R1 interval ODE versus FD4 compiler

## Exact classification and limited result

`GE19_H4F3D7_FROZEN_ODE_FD4_COMPILER_PASS_PHYSICAL_OPEN`.

The new H4F3d7 code passed its dedicated exact-source
GitHub Actions audit on deterministic Nt64/Nt128 manufactured
R1 stepper trajectories. This is a genuine implementation
and algebraic diagnostic PASS, **not a physical H4F3d7
measurement** and not a bath on-shell or full Noether
certificate. No historical GE19 source, solver, R1 interval
ODE or science target was edited.

## Frozen parents and implementation

- H4F3d7 preregistration:
  `ge19/h4f3d7_predata_bath_fd4_vs_original_r1_interval_ode.json`;
  blob `ccf3185b4f790d9d6068f80beb39a442b186158c`.
- Frozen original Repair24 propagator:
  `ge19/repair24_q20_construction.py`;
  blob `fc271987d1bddcd023cc9c057ddcad036b1d72fb`.
- Actual H4F3d6 subset source:
  `ge19/h4f3d6_actual_normalized_bath_parent_ward.py`;
  blob `0419145499f5f44e06ba0c96f779c2a604e84ce7`.
- New H4F3d7 implementation:
  `ge19/h4f3d7_bath_fd4_vs_original_r1_interval_ode.py`;
  blob `b598a5cc49b3d87827b4758c55d3ce7f3a1198a8`.
- Dedicated compiler workflow:
  `.github/workflows/ge19-h4f3d7-r1-fd4-compiler.yml`;
  blob `ded2330eb9d9853bcaf1791a93a037261b04d98d`.

Valid GitHub Actions run `36148151670`, job
`108114383440`, conclusion `success`,
terminal marker
`GE19_H4F3D7_R1_FD4_COMPILER_PASS_PHYSICAL_OPEN`.

The frozen 10,828-byte CI JSON
`results/ge19_h4f3d7_frozen_r1_fd4_compiler.json`
has SHA-256
`6a6fb22b1c25ee0ee66755eb8a82899b3cdf8292c1678e7f4c989922b94ed66d`.
Dedicated artifact ID `10869873062`.

## Exact identity implemented and tested

For the frozen normalized first-order GE05 bath

`z10=omega*q10/sqrt(w)`,
`omega=r/tau`, and `x=ln(a)`,

the unchanged Repair24 interval step propagates

`dz/ds=v`,
`dv/ds=-3h_mid v-r^2(z-X)`,
`s=t/tau`, `h_mid=tau*sqrt(H_i H_i+1)`.

Its action current and original sampled FD4 Euler are

`J=a^3 v/tau`,

`R_FD4=H FD4_x(J)+a^3 omega^2(z-X)`.

For EACH available side of a physical node, with that
side's ORIGINAL `h_mid`,

`J_t,side=3H_i a_i^3 v_i/tau+
 a_i^3[-3h_mid,side v_i-r^2(z_i-X_i)]/tau^2`,

`R_ODE,side=J_t,side+a_i^3 omega^2(z_i-X_i)
=3a_i^3(H_i-h_mid,side/tau)v_i/tau`,

`D_FD4,side=H_i FD4_x(J)-J_t,side`.

The exact preregistered decomposition is

`R_FD4=R_ODE,side+D_FD4,side`

for both left and right original intervals.
Endpoints use the only adjacent side. Every interior
node retains **both** sides; no averaged, minimum,
fitted or selectively excluded side is used.

The original per-node phase assignment

`omega_j Delta_t_interval=
 r_j(x_i+1-x_i)/(tau sqrt(H_i H_i+1))`

is reported using ONLY the preregistered bins
`<0.25`, `[0.25,0.5)`, `[0.5,1)`, `>=1`.
All nodes and modes are retained.

On original manufactured Nt64/Nt128 grids, the imported
Repair24 `step_linear_nd` implementation was checked
AST-identical to its frozen source. Algebraic and sampled
FD4/ODE decomposition tests passed at their original
`1e-11` natural-scale bound. Deliberately nonzero
sampled-derivative, variable-interval-H and mixed-phase
controls were retained.

## Exact physical-stop boundary

The compiler does not have the user's certified physical
H4F3b/H4F3d6 JSON/NPZ binaries in GitHub checkout.
It must not substitute manufactured Z11, bath trajectories
or sources to claim an actual-grid Noether result.

Next permissible step: execute the same locked
implementation on the **original exact**
H4F3b source, H4F3d6 bath, corrected H3F/H3G,
Repair32B Z11, Repair13 and Repair26 R1 files.
The physical result must reproduce the historical
H4F3d6 FD4 residual absolute norm at <=1e-10,
retain both interval sides and all frequency nodes,
and freeze separately from the compiler.

This diagnostic has **no new bath-on-shell smallness
gate**, no fitted clock, no FD4 or R1 ODE edit and
no new H4 source coefficient. Its physical PASS,
if obtained, classifies the observed discrepancy
but is not a full all-sector H4 structural PASS.

The independent signed nonbath parent, action-boundary
and canonical-operator Ward reconstruction remains
necessary. Original active shift <=1e-6 and
matched time-order >=2.5 are unchanged.

**Full actual H4 Noether NOT CERTIFIED.
Z21 NOT CERTIFIED. Lensing blocked.**
