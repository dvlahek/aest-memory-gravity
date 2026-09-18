# NL1C7B4 Repair12 — full raw-constraint perturbative-order audit

## Status

Locked before implementation and before any Repair12 execution.

Repair12 is licensed only by the frozen Repair11 E-sector analytic/covariant audit PASS at commit `559650a2de9bf57a344401ba459adf2268212b81`.

Repair12 does not change the Repair08 state, the B4 equations, any source coefficient, any sign, or the historical B4 `1e-7` gate. It asks one diagnostic question only:

**Does the complete signed raw Hamiltonian and radial-momentum residual of the first-order Repair08 growing-mode state begin at second perturbative order when evaluated with the exact nonlinear frozen B4 source dictionary?**

## Frozen parent results

- Repair08 identity-preserving state:
  - JSON SHA-256 `054851decab71e79a05aca2bc9fb287bb1239c8fb425989f40920004c3d88453`;
  - NPZ SHA-256 `4639f3b5c0afcddb2f98c8b9f6a9dbbf8661dac685b12d235c09075a106dafa7`.
- Repair10 source-localization JSON SHA-256:
  `f1fc1a86d2d488f5e88f0d32b0d3d1d5ce9dab22f52e51fa69801948aeb6de9d`.
- Repair11 E-sector audit JSON SHA-256:
  `48c8caf0c5758b089318bcd18885c87725bc244ed5a47862ac841b37b834742d`.
- Repair11 result-freeze commit:
  `559650a2de9bf57a344401ba459adf2268212b81`.
- Repair11 terminal classification:
  `NL1C7B4_REPAIR11_ESECTOR_ANALYTIC_COVARIANT_AUDIT_PASS`.

The same exact dense trace/coverage and B3 homogeneous background used by Repair08-11 are retained.

## Frozen exact source dictionary

Repair12 must evaluate exactly the same 11 signed Euler-Lagrange source contributions as Repair10:

1. `GR_kin`
2. `GR_curv_NL`
3. `GR_curv_Rr`
4. `GR_Nr_boundary`
5. `AeST_E2`
6. `AeST_EX`
7. `AeST_X2`
8. `AeST_J`
9. `AeST_K`
10. `dust`
11. `standard_bg`

For each case,

`N_H = sum_i C_H_i`

and

`N_M = sum_i C_M_i`.

No term may be removed, merged, rescaled, sign-flipped, linearized, clipped, or refitted.

## Diagnostic perturbation family

No official state is modified or written.

For diagnostic copies only, define a one-parameter path from the same homogeneous B3 background to the frozen Repair08 state. For every scale/grid pair:

`L(lambda)=a+lambda(L-a)`

`R(lambda)=ar+lambda(R-ar)`

`L_t(lambda)=aH+lambda(L_t-aH)`

`R_t(lambda)=aHr+lambda(R_t-aHr)`

`u(lambda)=lambda u`

`u_t(lambda)=lambda u_t`

`phi(lambda)=lambda phi`

`delta Q(lambda)=lambda delta Q`

`delta_b(lambda)=lambda delta_b`

`v_r(lambda)=lambda v_r`.

The exact scalar quantity is enforced along the diagnostic path by

`Q(lambda)=Q_bg+lambda delta Q`

and the coordinate `phi_t(lambda)` is reconstructed from the exact frozen spherical Q definition, exactly as in Repair09-11.

The diagnostic amplitudes are frozen as

`lambda in {0, 1, 1/2, 1/4, 1/8}`.

The `lambda=0` evaluation is a numerical B3 background baseline only.

## Baseline subtraction

Because Repair12 measures perturbative order, define for every radial point

`Delta N_H(lambda)=N_H(lambda)-N_H(0)`

and

`Delta N_M(lambda)=N_M(lambda)-N_M(0)`.

The unsubtracted `N_H(0)` and `N_M(0)` arrays and their norms must be reported. They are not used to erase a historical B4 failure; subtraction is used only to isolate the perturbative increment around the already certified B3 background.

No lambda-dependent baseline or fitted offset is permitted.

## Frozen cases

Retain all:

- scales `5,10,20 h^-1 Mpc`;
- radial grids `Nr=256,512`;
- Y families `Simple, Exponential, Sharp`;
- beta values `1.0,0.5,0.1`.

Thus all 54 Repair10 cases are retained.

No point, scale, Y family, beta value, or grid may be selected after execution.

## Primary order diagnostic

For every one of the 54 cases and for both constraints, compute on all non-center radial points:

- `||Delta N_H(lambda)||_2`;
- `||Delta N_M(lambda)||_2`;
- `max |Delta N_H(lambda)|`;
- `max |Delta N_M(lambda)|`.

For adjacent positive amplitudes define the L2 order estimate

`p = log(norm(lambda_i)/norm(lambda_{i+1}))/log(2)`.

All three adjacent slopes are reported.

The **asymptotic gate** is preregistered only on the two smaller-amplitude intervals:

- `lambda=1/2 -> 1/4`;
- `lambda=1/4 -> 1/8`.

For both H and M, every finite gated slope in every frozen case must satisfy

`1.8 <= p <= 2.2`.

The `1 -> 1/2` slope is reported but is not a gate because higher-order contamination is expected to be largest at full amplitude.

The L-infinity slopes are diagnostic-only and are not used as a terminal gate.

## Repair10 reproduction at lambda=1

At `lambda=1`, Repair12 must reproduce all 54 frozen Repair10 case values of:

- max epsilon_H;
- max epsilon_M;
- H-hotspot signed numerator;
- M-hotspot signed numerator;

to absolute-or-relative tolerance `1e-12`.

This ensures that the perturbative-order evaluator is the same exact nonlinear constraint evaluator at full amplitude.

## E-sector consistency anchor

Repair11 already proves symbolically that `AeST_E2` and `AeST_EX` have zero first-order momentum source and quadratic leading order.

Repair12 must verify that the E2/EX components generated internally at `lambda=1` reproduce the Repair10 stored hotspot values exactly to the same `1e-12` tolerance. No new E-sector physics inference is introduced.

## Gates

### R12_G1 — frozen provenance

Require exact Repair08, Repair10, and Repair11 hashes/classifications, Repair11 result-freeze ancestry, exact dense coverage, 128 native k modes, and frozen imported-code blobs.

### R12_G2 — lambda=1 exact Repair10 reproduction

All 54 cases must reproduce the frozen Repair10 epsilon and hotspot-numerator values to absolute-or-relative tolerance `1e-12`.

### R12_G3 — source bookkeeping closure

At every lambda, every non-center radial point, and every frozen case, the named 11-source sum must close to the direct signed numerator to normalized error `<=1e-12` for H and M.

### R12_G4 — finite fixed B3 baseline

The single `lambda=0` baseline for each scale/grid/Y/beta case must be finite and explicitly reported. No physical pass threshold is introduced for its magnitude in Repair12.

### R12_G5 — full Hamiltonian asymptotic second-order scaling

Every gated L2 slope of `Delta N_H` must lie in `[1.8,2.2]`.

### R12_G6 — full momentum asymptotic second-order scaling

Every gated L2 slope of `Delta N_M` must lie in `[1.8,2.2]`.

### R12_G7 — complete case/grid reporting

Require all 54 cases, all five lambda values, all six scale/grid pairs, and no excluded non-center points.

### R12_G8 — Repair11 consistency and claim boundary

Require the frozen Repair11 PASS and explicitly preserve:

- historical B4 raw exact-nonlinear FAIL;
- no state write/projection;
- no nonlinear constraint correction;
- no coefficient fit/rescale;
- no source insertion/removal;
- no sign change;
- no K clipping;
- no Q linearization;
- no threshold change;
- no radial-point removal;
- no Y/beta/scale selection;
- no nonlinear evolution;
- no finite eta;
- no B4-PASS relabel;
- no observational-detection claim.

## Terminal classifications

Allowed:

- `NL1C7B4_REPAIR12_FULL_CONSTRAINT_SECOND_ORDER_AUDIT_PASS`;
- `NL1C7B4_REPAIR12_FULL_CONSTRAINT_FIRST_ORDER_RESIDUAL`;
- `NL1C7B4_REPAIR12_IMPLEMENTATION_FAIL`.

If G1-G4, G7, and G8 pass but G5 or G6 fails, classify as `FULL_CONSTRAINT_FIRST_ORDER_RESIDUAL`.

A PASS means only that the exact nonlinear residual of the frozen first-order growing-mode state is asymptotically consistent with leading second-order truncation around B3. It does not make the historical exact-nonlinear B4 test pass and does not create nonlinear constraint-corrected initial data.

A later distinction between (i) first-order constraint certification and (ii) genuine nonlinear constraint solving requires a separate preregistration. Historical B4 results remain unchanged.
