# Stable AeST growth–Weyl memory R2 — post-data milestone

Date: 2026-09-14
Branch: `fullj-evolving-weyl-bridge`

## Formal classification

R2 completed with

    STABLE_AEST_GROWTH_WEYL_MEMORY_R2_TANGENT_FAIL

and exit code 1.

Historical results remain unchanged. In particular, R1c remains

    STABLE_AEST_FINITE_MEMORY_R1C_LONG_RELAXATION_CERTIFIED.

R2 does not reclassify any prior result.

## Gate outcome

Passed:

- R2-G1 provenance and certified-parent lock
- R2-G2 transfer-basis validity
- R2-G5 late-time activation
- R2-G6 cross-k temporal coherence

Failed:

- R2-G3 matched tangent reproducibility
- R2-G4 resolved growth–Weyl separation

The CLASS total-matter and Weyl transfer extraction itself was valid in all nine runs.

## Key numerical result

The separate matched fractional tangents

    G_eta = [D_m(eta)-D_m(0)]/[eta D_m(0)]
    L_eta = [W(eta)-W(0)]/[eta W(0)]

are individually highly reproducible between eta=0.005 and eta=0.01.

Across the three k anchors,

    max E_G = 3.5303590654639726e-3
    max E_L = 2.949001120528152e-3.

However, the central difference

    R_eta = L_eta - G_eta

is not reproducible:

    E_R = 0.6695, 0.7861, 0.5007

for k_h = 0.09875, 0.16125, 0.19500, respectively.

The scale-adaptive separation statistic is also unresolved:

    Q_sep = 0.5480, 1.2721, 0.9973,

so none of the three anchors reaches the preregistered Q_sep >= 3 threshold.

## Post-data cancellation diagnostic

The R2 failure is not caused by unstable total-matter or Weyl tangents. Instead, G and L are nearly common-mode, making R their small cancellation residual.

At eta=0.01 the vector relative difference

    ||L-G|| / max(||L||,||G||)

is approximately

    5.74e-4   at k_h=0.09875,
    9.04e-5   at k_h=0.16125,
    6.45e-3   at k_h=0.19500.

Best-fit scale/shape diagnostics for L relative to G at eta=0.01 are approximately

    k_h=0.09875: scale=1.000434, shape residual=3.76e-4
    k_h=0.16125: scale=1.000064, shape residual=6.4e-5
    k_h=0.19500: scale=0.993648, shape residual=1.13e-3.

Thus the two physical tangents are almost parallel on the locked redshift grid.

The strongest numerical-floor signature occurs at k_h=0.195. The norm of the *absolute* fractional separation before dividing by eta,

    || eta R_eta ||,

is

    3.0406469e-12 at eta=0.005
    3.0365904e-12 at eta=0.01.

These values are nearly identical even though eta doubles. A genuine first-order separation would give approximately eta-independent R_eta, not approximately eta-independent eta R_eta. Therefore the observed R2 residual at this anchor is consistent with an eta-independent differential numerical floor amplified by division by eta.

The two lower-k anchors also have R much smaller than G and L, but their tiny absolute residuals are more noise dominated and do not support a stronger floor claim individually.

## Physical interpretation

R2 does **not** certify a growth–Weyl separation and does not license the MCMG bridge.

What it does establish is narrower but useful:

- the certified long-relaxation memory branch gives a reproducible total-matter response;
- it gives a reproducible Weyl response;
- those two first-order responses are nearly common-mode over the tested range;
- their residual difference is below the present differential resolution;
- the residual nevertheless shows late-time enhancement and coherent temporal shape, but these post-subtraction properties are not enough to promote it to a resolved physical separation.

No observational, new-physics, MCMG-consistency, or permanent-elasticity-loss claim is licensed.

## Next step

Do not proceed directly to the MCMG first-moment bridge.

The next test should be an eta-leverage / precision audit of the small separation residual. The purpose is to distinguish a true first-order R_eta from an eta-independent numerical differential floor.

A suitable design is to extend the positive coupling lever arm while remaining perturbative,

    eta in {0, 0.01, 0.02, 0.04}

at the certified tau H0=10, order=20 branch, and independently repeat eta in {0,0.04} at a tighter tolerance. The primary observables remain CLASS d_m and phi+psi.

If G and L remain linear while R_eta stabilizes with increasing eta and reproduces at tighter tolerance, a physical separation is resolved. If G and L remain linear but eta R_eta remains approximately constant or the residual shrinks under tolerance tightening, the correct conclusion is that the finite-memory response is common-mode to the achieved numerical bound and the growth–Weyl separation remains unresolved.
