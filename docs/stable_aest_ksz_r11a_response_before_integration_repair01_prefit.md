# Stable AeST kSZ R11a Repair01 — response-before-integration pairwise velocity (pre-data)

Date: 2026-09-16
Branch: `fullj-evolving-weyl-bridge`

## Purpose

Historical R11a is frozen as

`STABLE_AEST_KSZ_R11A_NATIVE_DENSITY_FAIL`.

Its eta-zero pairwise velocity is healthy, but the tiny memory tangent fails native-density and Simpson-versus-trapezoid robustness. The failure is localized to extracting a small signed response from oscillatory spherical-Bessel integrals after separately integrating the plus/minus eta states.

Repair01 tests one preregistered numerical remedy only: **form the signed source response before the oscillatory integration**.

No kSZ data, optical-depth model, tracer-bias model, baryonic model, smoothing, clipping, extrapolation, post-data scale selection, or gate relaxation is allowed.

## Frozen parents

- R11a prefit: `a34c4d13738383c670222472b3af8ab4e1802fdf`
- R11a implementation: `44a65aea8f671a0af7534447c31f415a6c9d314c`
- R11a runner / run head: `8868dc344b83f69f7429b507e750450c724ddd63`
- R11a postdata freeze: `94efaf95b4582a177bd80dd566d5d2c26b4e212c`
- R11a JSON SHA256: `a868dbbb6b5b08bf54139abf9d3a288d52bee501f23cc4b61f9422f9fb2d98ab`
- R9b2k Stage-A postdata: `dd3981b2fd838fb24a997af77f913c3d5dd8d07b`
- R9b2k ShapeFit Repair02 postdata: `d3fd6191d55f4e74aa8666f842dae64bd8aee09b`
- R10a live-Weyl postdata: `b7da648f1810ea0c047b6e511e3f87211e830329`

Repair01 reuses the same 25 saved R9b2k checkpoints and must not call CLASS.

## Frozen domain

- `tau H0 = [10, 5, 2.5, 1.25]`
- primary central derivative: `eta = +/-0.025`
- control central derivative: `eta = +/-0.05`
- physical local point: `eta = +0.05`
- six frozen R9b2k/DESI effective redshifts
- separations `r = 40, 50, ..., 200 Mpc/h`

The separation domain is identical to the final historical R11a implementation.

## Common bounded support

For each redshift, define one common integration support before evaluating any response:

- lower bound = maximum native `k_min` over all 25 saved cases at that redshift;
- upper bound = minimum native `k_max` over all 25 saved cases at that redshift.

All baseline, response, density-tier, tau, epsilon, and operator calculations use this same per-redshift support. No extrapolation is permitted.

## Source quantities

For each saved state,

`v_cb = -t_cb/Hconf`

and

`P_df(k) = sign[d_cb(k) v_cb(k)] sqrt(P_dd(k) P_tt(k))`.

For a central eta stencil form the signed source responses **on the native common plus/minus grid before interpolation or integration**:

`D_Pdd(k) = [P_dd(+eps,k) - P_dd(-eps,k)] / (2 eps)`

`D_Pdf(k) = [P_df(+eps,k) - P_df(-eps,k)] / (2 eps)`.

The background prefactor is retained rather than assumed eta-independent. With

`A(z,eta) = H(z,eta)/h(eta)`, compute

`D_lnA = [A(+eps)-A(-eps)] / [2 eps A(0)]`.

## Dense bounded operators

All integrations are Simpson integrations on a grid uniform in `ln k`.

### Primary

`LINEAR8192`:

- positive baseline `P_dd`: linear interpolation of `ln P_dd` versus `ln k`;
- signed baseline `P_df`: linear interpolation versus `ln k`;
- signed responses `D_Pdd`, `D_Pdf`: linear interpolation versus `ln k`;
- 8192 points on the common bounded support.

### Resolution controls

- `LINEAR4096`
- `LINEAR16384`

with the identical construction and support.

### Independent shape control

`PCHIP8192`:

- positive baseline `P_dd`: PCHIP interpolation of `ln P_dd` versus `ln k`;
- signed baseline `P_df`: PCHIP interpolation versus `ln k`;
- signed responses `D_Pdd`, `D_Pdf`: PCHIP interpolation versus `ln k`;
- 8192 points on the same bounded support.

No log interpolation is applied to a signed response.

## Pairwise derivative

For each `(r,z)`, define

`xi0 = int dlnk k^3 P_dd0(k) j0(kr) / (2 pi^2)`

`I0 = int dlnk k^2 P_df0(k) j1(kr) / (2 pi^2)`

and response integrals

`D_xi = int dlnk k^3 D_Pdd(k) j0(kr) / (2 pi^2)`

`D_I = int dlnk k^2 D_Pdf(k) j1(kr) / (2 pi^2)`.

For

`v12 = -2 a A I / (1 + xi)`, 

the fractional response is evaluated analytically as

`T_v12 = D_lnA + D_I/I0 - D_xi/(1+xi0)`.

This is the primary Repair01 tangent. The response is therefore formed before the cancellation-prone Bessel integration.

For the physical eta=0.05 direct check, the eta=0 and eta=+0.05 spectra are separately evaluated with the same dense bounded baseline operator, and

`direct_shift = [v12(eta=0.05)-v12(0)]/v12(0)`

is compared with

`0.05 * T_v12(eps=0.025)`.

## Frozen gates

### R11A-R01-G1 — provenance/checkpoints

Require:

- all frozen parent commits are ancestors of HEAD;
- local historical R11a JSON has the frozen SHA256 and classification `STABLE_AEST_KSZ_R11A_NATIVE_DENSITY_FAIL`;
- historical R11a G1, G2, G3, G4, G7 are true and G5, G6 are false;
- all 25 saved checkpoints validate with the frozen R9b2k validator;
- native refinement remains D2 > D1 > 108.

### R11A-R01-G2 — common support and baseline physicality

For every redshift:

- common support is finite, positive, ordered, and contains at least `[2e-4, 2.0] h/Mpc`;
- all interpolated baseline arrays are finite;
- `1+xi0 > 0` and `|I0| > 1e-12` for every `(r,z,tau)`;
- all direct dense baseline pairwise velocities are finite and `|v12| > 1e-6 km/s`.

No amplitude statement is a gate.

### R11A-R01-G3 — dense resolution convergence

For D2, every tau and both epsilon values, compare fractional tangents:

- `LINEAR4096` vs `LINEAR8192`;
- `LINEAR8192` vs `LINEAR16384`.

Require for every comparison:

- `E <= 0.01`;
- `C >= 0.999`;
- both tangent norms > `1e-12`.

### R11A-R01-G4 — epsilon consistency

For every tau, compare `eps=0.025` vs `eps=0.05` separately for `LINEAR8192` and `PCHIP8192`.

Require:

- `E <= 0.05`;
- `C >= 0.995`;
- both norms > `1e-12`.

### R11A-R01-G5 — D1 -> D2 native-density convergence

At tau H0=10, compare D1 and D2 tangents for both epsilon values and both `LINEAR8192` and `PCHIP8192`.

Require:

- `E <= 0.05`;
- `C >= 0.995`;
- both norms > `1e-12`.

### R11A-R01-G6 — cross-operator agreement

At D2, for every tau and both epsilon values, compare `LINEAR8192` and `PCHIP8192` tangents.

Require:

- `E <= 0.05`;
- `C >= 0.995`;
- both norms > `1e-12`.

### R11A-R01-G7 — local physical linearity

For every tau, compare the primary direct eta=0.05 shift with `0.05*T_v12(eps=0.025)`.

Require:

- `E <= 0.10`;
- `C >= 0.99`.

### R11A-R01-G8 — background-prefactor audit

`D_lnA` must be finite for every redshift, tau, epsilon, and density tier. Its maximum absolute value is reported but is not required to be zero.

## Reported science quantities

Only if G1--G8 all pass, report for every tau:

- maximum and RMS `|T_v12|`;
- maximum and RMS fractional physical shift at eta=0.05;
- maximum absolute dense pairwise-velocity shift in km/s at eta=0.05;
- `(z,r)` of the largest fractional shift;
- tau tangent cosine and norm ratio relative to tau10;
- maximum `|D_lnA|`;
- direct-vs-linear physical-shift metric.

No amplitude threshold is used to force a favorable classification.

## Allowed PASS classification

`STABLE_AEST_KSZ_R11A_REPAIR01_RESPONSE_BEFORE_INTEGRATION_CERTIFIED`

Otherwise use a gate-specific FAIL classification. Historical R11a remains frozen as `STABLE_AEST_KSZ_R11A_NATIVE_DENSITY_FAIL` regardless of Repair01 outcome.

## Claim discipline

A PASS licenses a numerically controlled **linear-theory matter pairwise-velocity response** over the frozen domain only.

It does not license:

- a kSZ detection or observational null;
- a kSZ likelihood constraint;
- an eta or tau bound;
- optical-depth inference;
- a biased tracer/halo prediction;
- a nonlinear small-scale claim.

Only after Repair01 passes may its physical eta=0.05 amplitude be used to decide if an observational R11b is scientifically worthwhile.
