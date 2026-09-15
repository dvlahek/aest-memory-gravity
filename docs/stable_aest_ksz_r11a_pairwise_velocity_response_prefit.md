# Stable AeST kSZ R11a — theory-only pairwise velocity response (pre-data)

Date: 2026-09-15
Branch: `fullj-evolving-weyl-bridge`

## Purpose

R10a established a numerically certified live AeST Weyl-memory projection into ACT DR6 lensing, but the physical local signal is far below ACT sensitivity. R11a asks a different question before any kSZ likelihood is introduced:

**Does the same certified AeST source/velocity sector generate a materially larger local response in the linear-theory matter pairwise velocity?**

This is a theory-only diagnostic. No kSZ temperature data, electron optical depth model, halo/galaxy bias model, baryonic feedback model, or observational likelihood is used.

## Frozen parents

- R9b2k Stage-A native-density result postdata: `dd3981b2fd838fb24a997af77f913c3d5dd8d07b`
- R9b2k ShapeFit dm Repair02 certified postdata: `d3fd6191d55f4e74aa8666f842dae64bd8aee09b`
- R10a ACT live-Weyl postdata: `b7da648f1810ea0c047b6e511e3f87211e830329`
- R9b2k saved work directory: `results/stable_aest_desi_dr1_r9b2k_work`

R11a reuses the already generated R9b2k checkpoints. It must not call CLASS or regenerate the source states.

## Input grid

Use the six frozen R9b2k/DESI effective redshifts and the certified relaxation-time grid

`tau H0 = [10, 5, 2.5, 1.25]`.

Use the same local eta stencil:

- primary central derivative: `eta = +/-0.025`
- control central derivative: `eta = +/-0.05`
- physical local point: `eta = +0.05`
- baseline: `eta = 0`.

Use separations

`r = 20, 30, ..., 200 Mpc/h`.

The minimum separation is deliberately kept at 20 Mpc/h because R11a is a linear-theory diagnostic, not a nonlinear halo-pair model.

## Pairwise-velocity construction

For each saved source state, define the sign-preserving density-growth cross spectrum from the stored cb density and velocity-divergence state,

`P_df(k) = sign[d_cb(k) v_cb(k)] sqrt(P_dd(k) P_tt(k))`,

with

`v_cb = -t_cb / Hconf`.

This is the same velocity mapping already audited in the R9b2 chain. It retains the sign that is lost in `P_tt` alone.

For separation `r` in Mpc/h, compute

`xi(r) = int dlnk k^3 P_dd(k) j0(kr) / (2 pi^2)`

and

`I_df(r) = int dlnk k^2 P_df(k) j1(kr) / (2 pi^2)`.

The linear-theory matter pairwise velocity is

`v12(r,z) = -2 a H(z)/h * I_df(r) / [1 + xi(r)]`,

where `H(z)` is converted from the stored CLASS `Hubble_Mpc_inv` to km/s/Mpc using the speed of light. The output is in km/s.

This is an unbiased matter-field pairwise velocity. It is **not** a direct prediction for a DESI LRG/BGS kSZ sample, which would additionally require tracer bias/selection and optical-depth/baryon modeling.

## Quadrature operators

Primary operator: native-grid Simpson integration in `ln k`.

Independent control: native-grid trapezoid integration in `ln k`.

No extrapolation beyond the saved native CLASS support is allowed. No smoothing, clipping, or fitted transfer template is allowed.

## Frozen gates

### R11A-G1 — provenance and checkpoint completeness

All 25 saved R9b2k checkpoints must exist and validate with the frozen R9b2k checkpoint validator:

- D1, tau=10, all five eta values;
- D2, all four tau values, all five eta values.

The certified Repair02 result and frozen parent commits must be ancestors of HEAD.

### R11A-G2 — baseline physicality and eta-zero tau invariance

For all six redshifts and all 19 separations:

- `v12`, `xi`, and `I_df` are finite;
- `1 + xi > 0`;
- `|v12| > 1e-6 km/s`.

Across D2 eta=0 cases, the maximum relative tau variation of the Simpson baseline must be <= `5e-3`.

The actual native refinement must remain `n_k(D2) > n_k(D1) > 108` at tau=10.

### R11A-G3 — baseline quadrature agreement

For each tau, Simpson and trapezoid eta-zero pairwise-velocity vectors must satisfy

- symmetric relative norm error `E <= 0.01`;
- cosine `C >= 0.999`.

### R11A-G4 — epsilon consistency

For each tau and each quadrature operator, the fractional tangent

`T_v12 = [v12(+eps)-v12(-eps)] / [2 eps v12(0)]`

from `eps=0.025` and `eps=0.05` must satisfy

- `E <= 0.05`;
- `C >= 0.995`;
- both tangent norms > `1e-12`.

### R11A-G5 — native-density convergence

At tau=10, D1 and D2 fractional tangents must agree for both epsilon values and both quadrature operators with

- `E <= 0.05`;
- `C >= 0.995`.

### R11A-G6 — cross-quadrature tangent agreement

At D2, Simpson and trapezoid tangents must agree for every tau and both epsilon values with

- `E <= 0.05`;
- `C >= 0.995`.

### R11A-G7 — local physical eta=0.05 linearity

For every tau, compare the direct one-sided physical shift

`[v12(+0.05)-v12(0)]/v12(0)`

with the linear prediction

`0.05 * T_v12(eps=0.025)`.

Require

- `E <= 0.10`;
- `C >= 0.99`.

## Reported science quantities

Only if G1--G7 all pass, report for each tau:

- maximum and RMS `|T_v12|` over the 6 x 19 grid;
- maximum and RMS fractional physical shift at eta=0.05;
- maximum absolute velocity shift in km/s at eta=0.05;
- location `(z,r)` of the largest fractional shift;
- cosine and norm ratio of each tau tangent relative to tau=10;
- direct-vs-linear physical-shift agreement.

No amplitude threshold is itself a pass/fail gate. R11a is designed to measure the size of the effect, not to force a favorable outcome.

## Allowed classification

PASS:

`STABLE_AEST_KSZ_R11A_PAIRWISE_VELOCITY_RESPONSE_CERTIFIED`

Otherwise use a gate-specific FAIL classification. Historical DESI/ACT results are not reclassified.

## Claim discipline

A PASS licenses only a numerically controlled **linear-theory matter pairwise-velocity response** over the frozen `(r,z,tau,eta)` domain.

It does not license:

- a kSZ detection;
- an optical-depth estimate;
- a DESI/ACT kSZ likelihood constraint;
- a galaxy/halo pairwise-velocity prediction without bias modeling;
- a nonlinear small-scale claim;
- a bound on eta or tau.

A later observational R11b is permitted only after R11a quantifies a sufficiently interesting physical response to justify introducing kSZ optical-depth and tracer-bias nuisance structure.