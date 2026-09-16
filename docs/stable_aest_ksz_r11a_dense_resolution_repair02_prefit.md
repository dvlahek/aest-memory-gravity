# Stable AeST kSZ R11a Repair02 — asymptotic dense-resolution closure (pre-data)

Date: 2026-09-16
Branch: `fullj-evolving-weyl-bridge`

## Purpose

Historical R11a failed native-grid density/operator robustness. Repair01 formed the signed source response before the oscillatory Bessel integration and fixed both failures, but its preregistered dense-resolution gate failed.

Repair01 established two separate facts:

- 4096 -> 8192 is strongly under-resolved;
- 8192 -> 16384 improves dramatically, but still has `E ~ 0.0393`, which does **not** satisfy the original Repair01 dense-resolution threshold `E <= 0.01` even though it satisfies the looser general tangent threshold.

Repair02 therefore tests a genuinely finer asymptotic regime without relaxing any convergence threshold.

No physical model, eta range, tau grid, separation range, source-state definition, interpolation family, likelihood, or convergence threshold is changed.

## Frozen parents

- R11a postdata: `94efaf95b4582a177bd80dd566d5d2c26b4e212c`
- R11a Repair01 preregistration: `608851bff8d4fc8ab063cc338ec0cd102a9f74f8`
- R11a Repair01 implementation: `11f51614a5c5ddecdcb24e898011d0d47df2b7ea`
- R11a Repair01 runner: `d2c1b9d811cdc7344039a015210a675ec7361360`
- R11a Repair01 postdata: `43ce2d7cd772438efe34edabc25572c7b7516bee`
- Repair01 JSON SHA256: `4fc3612674ae5ae6b2093e9642a3984bf4c7a3dbcd72b6b9eba6d9e664caa239`
- R9b2k saved work directory remains the only theory-state input.

Repair02 must not call CLASS or regenerate any source state.

The earlier unrun Repair02 draft commit `855bd48089b915b810f81c2b1399bc4713e55af4` is superseded by this corrected preregistration because that draft accidentally quoted the general tangent threshold for the dense-resolution gate. No Repair02 data were generated under that draft.

## Frozen physical domain

Exactly retain Repair01:

- tau H0 = `[10, 5, 2.5, 1.25]`;
- eta stencil = `0, +/-0.025, +/-0.05`;
- primary epsilon = `0.025`;
- control epsilon = `0.05`;
- redshifts = the six frozen R9b2k/DESI effective redshifts;
- separations = `40, 50, ..., 200 Mpc/h`;
- one common bounded native support per redshift across all 25 checkpoints;
- no extrapolation, smoothing, clipping, fitted transfer template, or post-data scale selection.

## Frozen response construction

Use exactly the Repair01 response-before-integration definition:

`Dp = [Pdd(+eps)-Pdd(-eps)]/(2 eps)`

`Df = [Pdf(+eps)-Pdf(-eps)]/(2 eps)`

with sign-preserving `Pdf`, and

`T_v12 = Dln(H/h) + DI/I0 - Dxi/(1+xi0)`.

## Dense grids

Primary science grid: `32768` equally spaced nodes in `ln k` on the common bounded support.

Resolution controls: `16384` and `65536` nodes.

Primary interpolation: linear interpolation of signed responses in `ln k`, with positive baseline `Pdd` treated logarithmically exactly as in Repair01.

Independent shape control: PCHIP at `32768` nodes.

The use of 32768 as the primary grid is fixed before Repair02 is run. It is motivated only by Repair01 showing that 8192 -> 16384 had not yet met the original dense-resolution threshold.

Historical R11a and Repair01 remain FAIL and are never reclassified.

## Frozen gates

### G1 — provenance and checkpoints
All frozen parent locks/hashes and all 25 R9b2k checkpoints must validate.

### G2 — support and baseline
Common bounded support and finite nonzero eta-zero pairwise velocities must remain valid at 32768 for linear and PCHIP baselines.

### G3 — asymptotic dense-resolution closure
For every tau and both epsilon values, require both:

- LINEAR16384 vs LINEAR32768: `E <= 0.01`, `C >= 0.999`;
- LINEAR32768 vs LINEAR65536: `E <= 0.01`, `C >= 0.999`;
- all norms > `1e-12`.

These are exactly the Repair01 dense-resolution thresholds. No threshold relaxation is allowed.

### G4 — epsilon consistency at primary grid
At LINEAR32768 and PCHIP32768, eps=0.025 vs eps=0.05 must satisfy `E <= 0.05`, `C >= 0.995`, norms > `1e-12`.

### G5 — native-density convergence at primary grid
At tau10, D1 vs D2 at 32768 must satisfy `E <= 0.05`, `C >= 0.995` for both interpolation operators and both epsilon values.

### G6 — cross-operator agreement at primary grid
At D2, LINEAR32768 vs PCHIP32768 must satisfy `E <= 0.05`, `C >= 0.995` for every tau and both epsilon values.

### G7 — local eta=0.05 linearity
At LINEAR32768, direct eta=0.05 fractional shift versus `0.05*T(eps=0.025)` must satisfy `E <= 0.10`, `C >= 0.99` for every tau.

### G8 — background audit
All `Dln(H/h)` values must be finite. They are not required to vanish.

### G9 — physical-shift dense-resolution closure
The direct eta=0.05 fractional-shift vectors from LINEAR32768 and LINEAR65536 must satisfy the original dense-resolution criterion `E <= 0.01`, `C >= 0.999` for every tau.

## PASS classification

`STABLE_AEST_KSZ_R11A_REPAIR02_DENSE_RESOLUTION_CERTIFIED`

Otherwise use a gate-specific FAIL classification. No historical result is reclassified.

## Licensed claim after PASS

PASS licenses only the numerically controlled linear-theory unbiased-matter pairwise-velocity response over the frozen domain and the physical eta=0.05 response amplitude within that model.

It does not license a kSZ detection, optical-depth inference, halo/galaxy prediction, eta/tau bound, nonlinear small-scale statement, or observational kSZ likelihood claim.

If PASS confirms a physical response that is far below realistic velocity/kSZ sensitivity, the kSZ route may be closed as amplitudinally unpromising without constructing R11b.