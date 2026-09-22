# GE19 Repair33 first valid H4/Z21 result — FAIL freeze and implementation localization

## Frozen result

Classification:

`GE19_REPAIR33_WINDOW_LOCAL_REDUCED_H4_Z21_PARTICULAR_FAIL`.

The result is frozen exactly as emitted and is not relabelled.

Local artifacts:

- JSON SHA-256:
  `62da23947b59ae0ee20b858ee2dcbf394e6dcb91b85b0faae07fa5bf91366f07`;
  bytes:
  `142659`;
- NPZ SHA-256:
  `80fbd027b8392bed25beb6ebd7111507be36c24d5f21a1ba218c9e3594bec407`;
  bytes:
  `25340264`;
- FULL log SHA-256:
  `62da23947b59ae0ee20b858ee2dcbf394e6dcb91b85b0faae07fa5bf91366f07`;
  bytes:
  `142659`;
- local runner log SHA-256:
  `bc106bd7665512078c7e2694ab5d29d627ce28dd9d8b2b54b3207f4e668805d6`;
  bytes:
  `248992`.

The JSON and FULL log are byte-identical.

Runner terminal route:

`GE19_REPAIR33_VALID_SCIENCE_FAIL_FREEZE_REQUIRED`.

## Passed source-side controls

The H4 source itself is numerically stable under the preregistered resolution
controls:

- DY2 Nx1024/Nx2048 relative L2:
  `2.9384475883958845e-05`;
- total H4 source Nx1024/Nx2048 relative L2:
  `4.7580125292267077e-17`;
- memory source Nq1024/Nq2048 relative L2:
  `1.0712218077978013e-06`;
- total H4 source Nt128/Nt64 relative L2:
  `1.870408489003643e-04`.

Frozen parent reconstruction also closes exactly:

`Repair27_bath_projection_reconstruction_relative_L2_max = 0.0`.

Thus the dominant failure is not a spatial, bath-quadrature or time-grid
instability in source assembly.

## Failed gates

The emitted FAIL contains five failed gates:

1. Q-cross polarization self-consistency:
   `3.683354016827578e-08 > 1e-12`;
2. H4 linear-system relative L2 residual:
   `1.0418920734187787 > 1e-8`;
3. H4 state Nt128/Nt64 global relative L2:
   `0.21620025791599926 > 5e-3`;
4. anisotropy global relative to operator scale:
   `1.731327544676648e-05 > 1e-6`;
5. zero dynamic boundary metric:
   `6.664001874625056e-08 > 1e-12`.

Shift passes:
`4.429311491495022e-07 < 1e-6`.

All outputs are finite.

## Localization 1 — wrong H4 propagation solver path

Repair33 implementation called the historical global sparse BVP helper:

`r7.solve_case(...)`.

That helper builds the full all-time sparse matrix, overwrites early dynamic
rows with zero-value/zero-derivative boundary equations, and solves the entire
system through `equilibrated_solve`.

This is not the solver/boundary path used by the certified H3/Z20 chain.

The certified Repair22 H3/Z20 parent explicitly inherits:

- zero canonical coordinates
  `q0=(S,u,phi,T)=0`;
- constraint-projected canonical momenta
  `p0=(pS,pu,pphi,pT)`;
- Repair18 doubly equilibrated minimum-norm lapse+shift projection;
- Repair07 two-stage Radau IIA canonical march.

Repair21, whose state is certified by Repair22, constructs exactly this
boundary and propagates with:

`r7._radau2_integrate_canonical(...)`

followed by

`r7._reconstruct_canonical_solution(...)`.

Therefore Repair33 did not actually implement its preregistered statement

`zero homogeneous H4 boundary, identical particular-state convention to the certified H3/Z20 chain`.

This mismatch is implementation-level and directly explains the extreme
all-time sparse conditioning and large low-mode residuals.

Examples from the frozen Repair33 result:

- C_min, m=1 row-scale dynamic range:
  `5.917308675125254e+16`;
- C_min, m=1 final unscaled residual:
  `0.4552463797033176`;
- C_star, m=1 final unscaled residual:
  `0.2521412721029271`.

The resulting state-time and anisotropy failures are downstream consequences
of this wrong propagation path and must not be interpreted as a physical H4
inconsistency.

## Localization 2 — incorrect zero-boundary monitor

Repair33 `zero_boundary_control` required both the dynamic coordinates and
their finite-difference time derivatives to vanish at the left boundary.

The certified H3 particular convention does not impose zero canonical
momenta/derivatives. It imposes zero coordinates and determines the compatible
canonical momenta from lapse+shift constraints.

Therefore the Repair33
`zero_dynamic_boundary_abs_max`
implementation is not a valid audit of the preregistered H3-matched particular
boundary.

The correct follow-up must audit:

- exact zero canonical coordinates q0;
- projected-momentum solver residual;
- initial lapse backward error;
- initial shift backward error;
- initial algebraic closure.

## Localization 3 — Q-cross polarization cancellation

The GE06/GE07 Q cross was evaluated by subtractive polarization:

`[Q2(Z10+lambda Z11)-Q2(Z10-lambda Z11)]/(4 lambda)`.

Mathematically this is exact for a quadratic form, but the current lambda=1
and lambda=0.5 self-consistency test subtracts large nearly equal floating
point values. The observed mismatch

`3.683354016827578e-08`

is therefore an arithmetic cancellation floor.

This does not track the source-grid or time-grid controls, both of which pass
by orders of magnitude.

A follow-up may use the same exact quadratic identity with a deterministic
balancing scale chosen from the frozen Z10/Z11 norms, and must preregister the
balancing rule before execution. No source rescaling or fitted physics factor
is permitted.

## Frozen interpretation

Repair33 remains a historical FAIL and is not rerun.

However, this FAIL is implementation-confounded because the propagation and
boundary implementation did not realize the certified H3 particular-state
convention explicitly referenced by the Repair33 preregistration.

The H4 source-side convergence evidence remains useful diagnostic evidence,
but no Z21 state is certified.

## Licensed next step

A separately preregistered Repair34 may:

1. retain the exact same H4 physical equation and frozen parents;
2. retain the exact GE05->GE06 factor two;
3. use a numerically balanced but algebraically identical Q polarization;
4. replace the wrong sparse BVP propagation with the already certified
   Repair18 projected-q0/p0 boundary plus Repair07 canonical Radau IIA march;
5. replace the invalid zero-qdot monitor with the existing Repair18 boundary
   closure metrics.

No observational input, finite eta, threshold fitting or post-hoc source
normalization is permitted.

## Canonical status

**Repair33 = historical FAIL, implementation-confounded. Z21 is NOT
CERTIFIED. Z11 remains CERTIFIED. The next step is a separately preregistered
Repair34 that restores the already certified H3 canonical boundary/propagator
without changing H4 physics.**
