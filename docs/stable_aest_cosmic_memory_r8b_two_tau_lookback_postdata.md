# Stable AeST cosmic memory R8b — two-tau lookback decomposition (post-data)

Date: 2026-09-15
Branch: `fullj-evolving-weyl-bridge`

## Formal result

`STABLE_AEST_COSMIC_MEMORY_R8B_TWO_TAU_LOOKBACK_CERTIFIED`

All preregistered R8b gates G1--G7 passed. R8b therefore licenses the comparison of the live physical cosmic-epoch decomposition between the frozen `tau H0 = 10` R7a parent and the newly evaluated `tau H0 = 1.25` endpoint.

## Frozen provenance and result hashes

- R8b preregistration lock: `26ad0f310e0cc203c3350330a17e6822771515a0`
- R7a post-data parent: `86c03e6ba2ee9fcbf33a9d319d12ae778a747881`
- R8a2 post-data parent: `590dbc69e2823f583b157af2297e357991103c47`
- R8b JSON SHA256: `925d882609149720dc84360142085038953384b548f22945ddc58fdb83a6d861`
- R8b NPZ SHA256: `a9aaba1f0daf635358a24832bd5ccc3d606a6e70e65b4aa186dd0117ba757fa4`
- R8b science log SHA256: `34e18aa0a0fcb35524e09719a1d00e6ca5c7d3784342bbffa635bdfbb494c0de`
- R8b full runner log SHA256: `2a8c6050a4f898db16e39d1547e0cb5d14eedc71ec6ff722c3a2dc5af88b8990`
- R8b bundle SHA256: `0d6f45d68caddb9c713241b5d0101af31c21d1762c8cfa541fe4fbb27259ea20`

## Numerical closure

The `tau H0 = 1.25` baseline and full primary derivative reproduce the corresponding frozen R8a2 quantities exactly to stored precision. Primary-versus-control central derivatives remain stable:

- `sigma8`: E = 4.1823e-4, C = 0.9999999855;
- `f sigma8`: E = 1.3239e-3, C = 0.9999992262;
- `C_L^{kappa kappa}`: E = 1.9740e-4, C = 0.9999999816.

The four live epoch components reconstruct the full `tau H0 = 1.25` derivative with:

- `sigma8`: E = 1.4375e-3, C = 0.9999996278;
- `f sigma8`: E = 5.1977e-4, C = 0.9999999783;
- `C_L^{kappa kappa}`: E = 4.5271e-4, C = 0.9999998999.

## Growth lookback comparison

The aggregate growth lookback profile is nearly invariant when shortening `tau H0` from 10 to 1.25.

For `sigma8`, the signed projection assigned to the two earlier windows (`z >= 2`) changes from 0.18500 to 0.19013, a shift of only +0.00513. The combined later-window projection changes from 0.81533 to 0.81102. The dominant `0.5 <= z < 2` component remains dominant: 0.73897 at tau10 versus 0.73561 at tau1.25.

For `f sigma8`, the earlier-window signed projection changes from 0.10764 to 0.11328 (+0.00564), while the combined later-window projection changes from 0.89329 to 0.88720. The `0.5 <= z < 2` component remains dominant: 0.68347 at tau10 versus 0.68588 at tau1.25.

Thus the tested factor-eight change in relaxation time does not produce a simple migration of the growth memory kernel toward more recent cosmic epochs. The change is small and, in the aggregate vector projection used here, is slightly toward the earlier windows.

At observed z=0.2 the same stability holds. For `sigma8`, the `0.5 <= z < 2` signed fraction changes only from 0.74219 to 0.73880. For `f sigma8`, the recent-structure fraction changes from 0.54909 to 0.55488 and the `z < 0.5` fraction from 0.44243 to 0.43577.

## Lensing lookback comparison

The lensing decomposition shows a substantially larger reorganization, but primarily through cancellation rather than a simple lookback-horizon shift.

At tau10 the earlier (`z >= 2`) signed projection is -0.17667 and the later (`z < 2`) signed projection is +1.17644. At tau1.25 these become -0.07742 and +1.07749. Therefore the net early negative cancellation weakens by about 0.09925 while the compensating late positive projection decreases by about 0.09895.

The individual signed projections change as follows:

- ancient: -0.00366 -> -0.00169;
- intermediate: -0.17301 -> -0.07572;
- recent structure: +0.28958 -> +0.35825;
- late: +0.88686 -> +0.71923.

The epoch tangent shapes themselves remain extremely stable across tau: cross-tau epoch cosines are >= 0.9987 for all four lensing windows. Hence the main lensing effect of changing tau is a reweighting of nearly fixed epoch templates, not a wholesale deformation of each epoch response.

The full lensing zero crossings move from approximately L = 595.28 and 1819.16 at tau10 to L = 601.98 and 1777.59 at tau1.25.

## Physical interpretation

R8b rejects the naive picture that a shorter relaxation time simply causes the observable memory to come from more recent epochs. In the tested stable-AeST regime, the growth lookback profile is remarkably robust across a factor-eight change in tau. Lensing is more tau-sensitive because different epoch components project with opposite signs and tau changes their relative weighting, thereby changing temporal cancellation and the multipole-dependent fingerprint.

A more accurate qualitative statement is therefore:

> the relaxation time controls the weighting and cancellation of a broad causal memory history, not merely a sharp lookback horizon.

This remains a statement about the tested first-order stable-AeST response. It is not an observational detection, not a continuous-in-tau kernel theorem, and does not license extrapolation below `tau H0 = 1.25`.
