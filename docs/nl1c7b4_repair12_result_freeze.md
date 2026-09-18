# NL1C7B4 Repair12 — local result freeze

## Status

Frozen local WSL science result for the preregistered Repair12 full raw-constraint perturbative-order audit.

Terminal classification:

`NL1C7B4_REPAIR12_FULL_CONSTRAINT_FIRST_ORDER_RESIDUAL`

with `SCIENCE_RC=2`.

This is a valid negative science result, not an implementation failure and not an official GitHub Actions run.

## Execution provenance

- execution HEAD: `953f6cdba5229ec1c4713d28f40b45dbdc6142c9`;
- Repair12 preregistration commit: `d1b5c5f3aab13b3929f8c91eeea216724951c5f3`;
- Repair12 implementation commit: `85b9120781b29854f7508f1a18a77f8b42c814f2`;
- Repair12 implementation-lock commit: `ccba3e6d6b19a77032145ec65d5209710699a4fb`;
- Repair12 local-runner commit: `9e76269c0fe00043805ba7d1a37b2d42be4889c9`;
- Repair11 result-freeze commit: `559650a2de9bf57a344401ba459adf2268212b81`;
- Repair11 JSON SHA-256: `48c8caf0c5758b089318bcd18885c87725bc244ed5a47862ac841b37b834742d`;
- Repair10 JSON SHA-256: `f1fc1a86d2d488f5e88f0d32b0d3d1d5ce9dab22f52e51fa69801948aeb6de9d`;
- Repair08 NPZ SHA-256: `4639f3b5c0afcddb2f98c8b9f6a9dbbf8661dac685b12d235c09075a106dafa7`.

## Frozen local output hashes

- result JSON:
  - bytes: `1580605`
  - SHA-256: `99c963dc65cca35c90c6b892fb4192bed1a8c03776664c9da532a5702c62767c`
- evaluator log:
  - bytes: `1581051`
  - SHA-256: `92810980e8d4d994a48e2f84c77df401d2cab2f08dad50b9ff0d376ac4eb7308`
- local runner log:
  - bytes: `1583852`
  - SHA-256: `73ff81c1b57dfae3eda2ef8da13fe47038c2745fac080c2aaa4fb64e0d69bd16`

## Gate result

PASS:

- R12_G1 frozen provenance
- R12_G2 lambda=1 exact Repair10 reproduction
- R12_G3 source bookkeeping closure
- R12_G4 finite fixed B3 baseline
- R12_G6 full momentum asymptotic second-order scaling
- R12_G7 complete case/grid reporting
- R12_G8 Repair11 consistency and claim boundary

FAIL:

- R12_G5 full Hamiltonian asymptotic second-order scaling

The bookkeeping closure is exactly zero for both Hamiltonian and momentum.

## Full perturbative-order result

Across all 54 cases:

Hamiltonian gated L2 slopes:

- minimum: `1.0021920951676406`
- maximum: `1.025811179907278`

Momentum gated L2 slopes:

- minimum: `2.005507037071882`
- maximum: `2.0397790843808306`

Therefore the complete signed radial-momentum residual is asymptotically second order, but the complete signed Hamiltonian residual contains a robust first-order component.

Representative Simple, beta=1 rows:

- scale 5, Nr=256:
  - H slopes `[1.0088251259698853, 1.0043918636047062, 1.0021920951676406]`
  - M slopes `[2.021801847299085, 2.010976610024624, 2.005507037071882]`
- scale 10, Nr=256:
  - H slopes `[1.0516024963808461, 1.0258111616237517, 1.0128935980117606]`
  - M slopes `[2.0781153740097222, 2.0397790811081506, 2.020051368112854]`
- scale 20, Nr=256:
  - H slopes `[1.0218157934035812, 1.0107118364030914, 1.005303198875552]`
  - M slopes `[2.055065102167894, 2.027901910073128, 2.014037720325115]`

The Nr=512 values reproduce the same order classification.

## Baseline

The lambda=0 B3 momentum baseline is at roundoff scale, while the Hamiltonian baseline is small but finite and was frozen before baseline subtraction.

Representative scale 5, Nr=256:

- H baseline L2 `4.607645056028261e-09`
- H baseline Linf `6.641719606111684e-10`
- M baseline L2 `1.1788033836872005e-16`
- M baseline Linf `8.906720846968419e-17`

The fixed lambda=0 baseline was subtracted exactly as preregistered; no fitted offset was used.

## Interpretation

Repair12 disproves the proposed full-second-order interpretation.

It establishes:

1. the momentum constraint is first-order consistent and its exact nonlinear residual begins at second order;
2. the Hamiltonian constraint is **not** first-order consistent under the frozen 11-source B4 dictionary/state interface;
3. the remaining mismatch is not attributable to the E2/EX momentum sector audited in Repair11;
4. the historical exact-nonlinear B4 FAIL remains valid.

Repair12 does not identify which Hamiltonian source term is responsible. It does not license any coefficient, sign, state, threshold, or source change.

## Licensed next step

A separately preregistered source-by-source Hamiltonian first-order localization may use the same frozen virtual lambda path and exact 11-source matrices.

For each source `i`, define

`Delta C_H_i(lambda)=C_H_i(lambda)-C_H_i(0)`

and the one-sided first-order coefficient estimate

`A_i(lambda)=Delta C_H_i(lambda)/lambda`.

The next audit may determine:

- which source coefficients converge to nonzero first-order profiles;
- which large first-order profiles cancel pairwise/groupwise;
- which uncancelled signed profile equals the total first-order Hamiltonian residual;
- stability across scales, grids, Y families, and beta values.

No source may be modified, omitted, rescaled, or reinterpreted during that localization.
