# Stable AeST DESI DR1 R9b2k ShapeFit dm Repair02 — postdata freeze

Date: 2026-09-15

## Classification

`STABLE_AEST_DESI_DR1_R9B2K_SHAPEFIT_DM_REPAIR02_CERTIFIED`

This is a new certified continuation result. Historical R9b2k and Repair01 classifications remain frozen and are not reclassified.

## Provenance and artifacts

- Repair02 preregistration commit: `9e9fd426e3030727f0723cf7e50ae4ef0c2799e8`
- Repair02 implementation commit: `aa3909146b438581f41f0de97171e6d0e2a34ec9`
- Repair02 runner commit: `c536e64d134f3de40af9c502807a09b431ff1566`
- Parent R9b2k JSON SHA256: `f4323f84dfa93c5ac3ef449fbe666ce3add45a50331079fe66bd27beb2b30c7e`
- Repair01 JSON SHA256: `af92b8f7c6186a5e04c7a4973840617dd64ef7afb33deddc24804c1b974f40ad`
- Repair02 JSON SHA256: `eb221160bf64b0905ec0b620fb8441aea2a1e55fc2981f8b3974954917f1cea4`
- Repair02 science log SHA256: `cb7f0d528d118c72edd7c2bd0c678bd48ab16ac6e8f580df21b1963115dd604e`
- Repair02 NPZ SHA256: `f83e7c86278891c220941f2fad13d2b21fb96cbaffd87ab91fafad557eae06ce`
- Repair02 full runner SHA256: `490f0c7c842c1974b6003b70611409128ff27924fa642984a72afcb9c1588498`
- Official DESI likelihood repository head: `7d51f4f86dc3bee6bf10f1a684913c943a89a844`
- DESI compressed vector dimension: 24

## Certified gates

All preregistered Repair02 gates passed:

- P1 parent provenance: PASS
- P2 saved D2 checkpoints: PASS
- P3 local positive pivot: PASS
- P4 local m operator agreement: PASS
- B1 DESI provenance: PASS
- B2 finite 24D ShapeFit vector: PASS
- B3 full-tangent epsilon consistency: PASS
- B4 full cross-operator agreement: PASS
- B5 nuisance projection: PASS
- B6 matched-filter / GLS identity: PASS

## Numerical localization of the previous dm failure

The raw peak-average no-wiggle spectrum is finite at all 1024 filter nodes in every saved row. The only non-positive values occur for the lowest-redshift bin, negative eta cases, at a single high-k node near `k = 4.233831910284027 h/Mpc`. They are far from the ShapeFit pivot near `k = 0.0300165756 h/Mpc`.

The local positive segment containing the pivot remains large and healthy. For the affected cases it extends at least to `k = 4.1893418468 h/Mpc`, while the pivot pair is approximately `(0.0297164, 0.0303167) h/Mpc`.

The maximum symmetric relative difference between the preregistered local linear and local PCHIP m estimates is

`4.367779654032155e-05`,

well below the frozen `m` operator gate `0.005`.

Therefore the historical six-dm NaN failure came from applying a global logarithmic smooth-spectrum interpolator to an otherwise locally healthy raw no-wiggle spectrum. It was not a failure of the local ShapeFit pivot slope.

## Full 24D tangent robustness

The complete ShapeFit tangent is stable.

Primary epsilon comparison (`eta = +/-0.025` versus `+/-0.05`) has relative errors between about `8.79e-05` and `9.77e-04`, with cosines >= `0.99999959`.

Primary-versus-control cross-operator comparison has relative errors about `9.27e-04` to `9.28e-04`, with cosines about `0.9999999935` or higher, for every tau and both epsilon values.

These are far inside the frozen `E <= 0.05`, `C >= 0.995` gates.

## DESI compressed projection

For tau/H0 = 10, 5, 2.5, 1.25 respectively:

- signed shape S/N: approximately `1.3570`, `1.3570`, `1.3572`, `1.3554`
- signed eta_hat: approximately `12370`, `12466`, `12667`, `13055`
- sigma_eta_shape: approximately `9116`, `9187`, `9333`, `9632`
- physical best fit restricted to `0 <= eta <= 0.05`: `eta = 0.05` for every tau
- physical Delta chi2 relative to eta=0: only about `1.41e-05` to `1.49e-05`

Matched-filter and GLS signed eta estimates agree to floating-point precision. Projection idempotence is about `2.24e-16`.

## Scientific interpretation

The corrected DESI DR1 compressed ShapeFit projection is now reportable as a validated null-sensitivity result in the physical eta interval.

The compressed data show an O(1.35 sigma) alignment with the signed mathematical template direction only at an amplitude eta of O(10^4), many orders of magnitude outside the physical interval `0 <= eta <= 0.05`. Within the physical interval the maximum likelihood sits at the upper boundary, but the improvement is only Delta chi2 ~ `1.5e-05`, i.e. observationally negligible.

Therefore:

- no observational detection claim is licensed;
- no useful DESI bound on eta is licensed;
- no tau bound is licensed;
- no full-EFT modified-gravity claim is licensed;
- the result does license reporting a numerically certified compressed ShapeFit null projection and the associated methodology/diagnostic chain.

This postdata freeze supersedes Repair02 as an open issue. Do not reopen the dm/global-smooth-interpolator problem unless a new independently preregistered observable requires it.