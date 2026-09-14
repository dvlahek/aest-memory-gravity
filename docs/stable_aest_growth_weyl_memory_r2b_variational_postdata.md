# Stable AeST growth–Weyl memory R2b — post-data checkpoint

Date: 2026-09-14
Branch: `fullj-evolving-weyl-bridge`

## Frozen parent

R2b was preregistered in commit

`fc118356ea77be3b81854a95992a89ff7a1630bc`

after the historical parent

`STABLE_AEST_GROWTH_WEYL_MEMORY_R2A_SEPARATION_UNRESOLVED`.

All earlier R1/R1b/R2/R2a classifications remain unchanged.

## Formal R2b result

The completed variational run returned

`STABLE_AEST_GROWTH_WEYL_MEMORY_R2B_COMMON_MODE_BOUND_CERTIFIED`

with exit code 0.

All provenance, force-trace, patch-neutrality, and individual amplified-tangent gates passed. The positive separation gate did not pass, while the preregistered common-mode gate passed at all three anchors.

Per-anchor primary lambda=10 versus lambda=30 diagnostics were:

- k_h=0.09875: E_G=5.806e-4, E_L=5.125e-4, E_R=6.929e-1, cosine_R=0.990232, Q_R=0.4496, B_30=4.1717e-5.
- k_h=0.16125: E_G=3.405e-5, E_L=2.666e-5, E_R=1.0263, cosine_R=0.222279, Q_R=0.5289, B_30=1.4183e-5.
- k_h=0.19500: E_G=6.486e-6, E_L=5.169e-6, E_R=2.368e-1, cosine_R=0.974508, Q_R=4.2228, B_30=1.4672e-5.

Thus zero of three anchors met the complete resolved-separation criterion, but all three met the preregistered one-percent common-mode bound.

Patch neutrality was exact at the stored precision for both CLASS `d_m` and `phi+psi` at all three anchors.

## Licensed interpretation

R2b certifies only

    ||L-G|| / max(||G||,||L||) <= 0.01

for the first-order stable-AeST response over the locked redshift vector, in the certified tau H0=10, order-20 regime.

It does not establish exact equality of growth and Weyl responses. In particular, the much smaller observed B_30 values cannot be promoted to a physical 1e-5 equality claim because R=L-G itself was not reproducible at two of the three anchors.

R2b therefore does not certify a positive growth–Weyl separation and does not license the positive MCMG shape bridge. It instead establishes a model-discriminating common-mode null bound.

No observational detection, permanent elasticity loss, or fundamental new-physics claim is licensed.

## Posthoc absolute-normalization cross-check

After the formal classification was fixed, the lambda=30 variational G and L vectors were compared with the already existing finite-eta R2 tangents at eta=0.005 and eta=0.01. This comparison is posthoc and is not a new R2b gate.

The temporal/redshift shapes agree extremely well: the finite-eta versus variational cosines are above 0.999998 across the tested anchors/channels. However, the finite-eta tangent norms are only approximately 0.488--0.494 times the lambda=30 variational tangent norms. Equivalently, the variational amplitudes are about 2.02--2.05 times larger.

Representative z=0.2 Weyl values are

- k_h=0.09875: finite eta=0.01 L ~= 1.741e-9, variational L_30 ~= 3.546e-9;
- k_h=0.16125: finite eta=0.01 L ~= 1.887e-8, variational L_30 ~= 3.845e-8;
- k_h=0.19500: finite eta=0.01 L ~= 4.565e-8, variational L_30 ~= 9.326e-8.

The historical finite-memory equation contains

    Bchi_aest *= aest_eta
    E_rhs_aest -= 0.5*Q_aest*Bchi_aest
    E' = a*E_rhs_aest/K_B - Hconf*E,

so the nominal eta=0 forcing used by R2b,

    F_eta = -a Q B_chi,raw/(2 K_B),

has the expected analytic prefactor. The approximately factor-two discrepancy is therefore not presently attributed to a missing explicit 1/2.

The leading numerical hypothesis is source-grid forcing interpolation: R2b freezes the baseline forcing on the CLASS native source grid, with only 26 target-k time samples in the completed run, and linearly interpolates that table during the signed variational probes. The physical finite-eta memory closure is instead evaluated continuously during perturbation integration.

A separate prospective normalization audit is required before the R2b variational vector is used as an absolutely normalized estimate of partial_eta. This follow-up must not reclassify R2b.

## Next step

Run a separately preregistered R2c source-grid densification / absolute-normalization audit. Its purpose is to determine if the variational tangent amplitude converges to the finite-eta tangent as the frozen forcing table is sampled more densely. The formal R2b common-mode certification remains fixed regardless of that outcome.
