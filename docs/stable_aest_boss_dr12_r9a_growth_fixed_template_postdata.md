# Stable AeST BOSS DR12 R9a — real-data growth fixed-template projection (post-data)

Date: 2026-09-15
Branch: `fullj-evolving-weyl-bridge`

## Formal result

`STABLE_AEST_BOSS_DR12_R9A_GROWTH_TEMPLATE_PROJECTION_CERTIFIED`

All preregistered R9a gates G1--G6 passed.

## Frozen science and implementation locks

- pre-fit science lock: `63f4bea97c95a5627f659415f556636c1af21fad`
- R7a post-data: `86c03e6ba2ee9fcbf33a9d319d12ae778a747881`
- R8a2 post-data: `590dbc69e2823f583b157af2297e357991103c47`
- R8b post-data: `9e21c61210979ab841918ba16f2210020daa245a`
- R9a implementation audit checkpoint: `cbab7eabb0bbf362fa6f0f9759b28500caf5d22c`

## Observational data provenance

Pinned BOSS/Cobaya data repository commit:

`bb0c1c9009dc76d1391300e169e8df38fd1096db`

Files and hashes:

- `sdss_DR12Consensus_final.dat`: `eae45d2629dc1214b351716b3ff9a6f5a22f170b71e3d0e93aeeddc169d80e30`
- `final_consensus_covtot_dM_Hz_fsig.txt`: `dea6d8d4893d2b84772f9b83d0653bf7d4ee81a0aeb63ce04859e20d0ad3a289`

BOSS compressed RSD vector used:

- z = 0.38: f sigma8 = 0.49749
- z = 0.51: f sigma8 = 0.457523
- z = 0.61: f sigma8 = 0.436148

The extracted 3x3 covariance is positive definite and symmetric.

## Uploaded result hashes

- JSON SHA256: `d7266cedb905d606f1ccd7824aa0539f70cd5b6fb6aaed35655ac76ba0512112`
- NPZ SHA256: `a6eaee5a154d7f4b980c604818d4874c1367fbd9dc9e1f9c6244352ecf933848`
- science log SHA256: `03421514106c09d64dfb397ee89629231702957de57de3223425fe0b288678da`
- full runner log SHA256: `913c400cc57e870c99a784188b078081af9fc5a02148ac4daeb57d8bf6b0db40`
- bundle SHA256: `073b175f8710289190c625968d7e04c93ef8d871110ad864291efdfe61f702e1`

## Certified tau grid and derivative control

`tau H0 = [10, 5, 2.5, 1.25]`

For every tau, direct physical theory was evaluated exactly at z = [0.38, 0.51, 0.61] with eta = 0, +/-0.025, +/-0.05. Central derivative consistency passed for all four tau values with cosine > 0.9999989 and relative errors below 0.002.

## Likelihood construction

The ordinary broadband growth amplitude was profiled before testing the memory template. Thus R9a does not identify a uniform amplitude mismatch as memory. The memory template is tested only through the covariance-weighted redshift-dependent component orthogonal to the baseline amplitude direction.

The amplitude-memory covariance correlation is large but not singular, rho approximately 0.82 across the tau grid.

## Main quantitative result

The unrestricted signed memory-template best fits are:

| tau H0 | eta_hat_signed | sigma_eta_shape | signed S/N |
|---:|---:|---:|---:|
| 10 | 29700.13 | 28596.16 | 1.0386 |
| 5 | 29981.11 | 28870.50 | 1.0385 |
| 2.5 | 30518.92 | 29406.97 | 1.0378 |
| 1.25 | 31500.85 | 30376.66 | 1.0370 |

Thus the BOSS residual has only an approximately 1.04-sigma projection on the normalized signed memory-template direction, nearly independent of tau.

However, these unconstrained best-fit eta values are about 3e4, far outside the locally certified physical regime eta <= 0.05. They are diagnostic shape projections only and are not physically licensed parameter estimates.

Inside the certified physical interval eta in [0,0.05], the profiled fit always reaches the upper endpoint eta = 0.05, but the improvement relative to eta = 0 is negligible:

| tau H0 | Delta chi2 physical vs eta=0 |
|---:|---:|
| 10 | 3.63197e-6 |
| 5 | 3.59699e-6 |
| 2.5 | 3.52914e-6 |
| 1.25 | 3.41383e-6 |

The eta=0 profiled broadband amplitude is approximately 0.96127 for every tau, with chi2 approximately 1.1471. Thus BOSS prefers an overall growth amplitude about 3.9% below the frozen baseline, but this preference is primarily broadband and is not explained by the certified memory template.

## Interpretation

R9a is a successful real-data compressed-growth null test. It certifies the observational interface and shows that the current stable-AeST memory template is far too small in the validated eta <= 0.05 regime to produce an observable BOSS DR12 growth improvement.

The approximately 1.04-sigma signed projection is not evidence for gravitational memory because the required eta is roughly 6e5 times larger than the validated physical maximum 0.05. The physical Delta chi2 is only of order 1e-6.

R9a therefore does not license:

- an observational detection of gravitational memory;
- an eta or tau bound from BOSS;
- a claim that the unrestricted eta_hat is physically meaningful;
- a full-shape modified-gravity claim.

R9a does license reporting the compressed real-data projection and the fact that, in the currently certified stable-AeST normalization, BOSS DR12 is essentially insensitive to the physical memory amplitude.

## Next step

The next observational step should not simply add more compressed f sigma8 points. The natural follow-up is a full-shape BOSS/DESI likelihood in which the model is confronted with the clustering spectra/correlation multipoles and their full nuisance treatment, ideally jointly with the certified ACT lensing projection. This is needed to test if the scale-dependent memory fingerprint survives beyond compressed summary statistics.
