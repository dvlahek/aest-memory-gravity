# Stable AeST ACT DR6 R6a — fixed-template projection post-data

Date: 2026-09-14

## Formal classification

`STABLE_AEST_ACT_DR6_R6A_FIXED_TEMPLATE_PROJECTION_CERTIFIED`

All preregistered gates R6A-G1 through R6A-G6 passed.

## Provenance and interface control

- R6a pre-data lock: `05d338e1dde7719cc78b132cd146a408c6a90d62`
- R5b post-data parent: `3242335ece23fbeb743f075a1df1aa70acaab211`
- official ACT likelihood source commit: `b386ddbb5821c1216c709f051c9289292f174d30`
- ACT release tag: `v1.2.1`
- internal module version: `1.2.0`
- data version: `v1.2`
- variant: `act_baseline`
- `lens_only=True`
- `like_corrections=False`
- Hartlap correction enabled
- `nsims_act=796`
- `trim_lmax=2998`
- nonlinear/Halofit disabled

The independent official-interface control returned

`chi2_fiducial = 14.057911788739439`

against the frozen target `14.06 +/- 0.10`.

## ACT support and template projection

The retained ACT baseline likelihood has 10 bandpowers with centers

`[53.0, 83.5, 123.0, 172.0, 231.5, 301.5, 382.5, 476.0, 582.0, 700.5]`.

The R5b parent tangent covers `L=40,...,2000`. The retained ACT binning matrix has exactly zero support outside this certified parent interval under the preregistered support metric.

The projected memory-template Fisher quantities are

- `F_raw = 2.2548650271767184e-11`
- `F_perp = 1.3455362196425382e-11`
- broadband-amplitude correlation `rho = 0.6350387102004318`
- `F_perp/F_raw = 0.5967258365469721`
- fixed-baseline shape scale `sigma_eta_shape = 272616.60409838276`

Thus about 59.7% of the raw covariance-metric template norm survives deprojection against a pure broadband lensing-amplitude rescaling. The memory template therefore has a nontrivial ACT-bandpower shape component and is not equivalent to a single overall lensing amplitude.

## Data overlap

At fixed AeST baseline cosmology,

- `chi2(eta=0) = 218.66491129094973`
- `chi2(eta=0.01) = 218.66491025159644`
- `chi2(eta=0.025) = 218.66490869256648`
- `chi2(eta=0.05) = 218.66490609418318`

After profiling the broadband lensing amplitude,

- `chi2_prof(eta=0) = 42.185812086227045`
- `chi2_prof(eta=0.01) = 42.18581184806665`
- `chi2_prof(eta=0.025) = 42.18581149082607`
- `chi2_prof(eta=0.05) = 42.18581089542512`

The physical local interval therefore improves the profiled chi-square by only

`Delta chi2 = 1.1908019246220647e-06`

between `eta=0` and `eta=0.05`.

The unconstrained signed matched-filter diagnostic gives

- `eta_hat_signed = 885001.7769335511`
- `sigma_hat = 272616.60409838276`
- `eta_hat/sigma_hat = 3.246323824847326`
- independent two-column GLS eta = `885001.7769335511`
- matched-filter/GLS absolute difference = `0`

This signed coefficient is a template-overlap diagnostic only. It lies about `1.77e7` times beyond the largest physically licensed local value `eta=0.05`, and is therefore not interpretable as a physical AeST-memory estimate or detection.

At the edge of the certified physical interval, the amplitude-deprojected shape signal-to-noise is only

`eta * sqrt(F_perp) = 1.8340775744516223e-07`

for `eta=0.05`.

## Interpretation

R6a certifies that the R5b derivative-at-zero CMB-lensing memory template can be reproducibly projected into the official ACT DR6 baseline lensing likelihood space. It also establishes that the projected template contains a genuine shape component after broadband-amplitude deprojection.

However, in the presently certified stable-AeST regime (`tau H0=10`, local `0 <= eta <= 0.05`), the absolute observable response is far too small for ACT DR6 to constrain. The formal `3.25 sigma` signed-template overlap occurs only at an enormous extrapolated coefficient far outside the certified local regime and has no licensed physical interpretation.

The large fixed-baseline chi-square and its substantial reduction after profiling a broadband amplitude show that the frozen AeST baseline cosmology is not itself an adequate fixed observational fit. Any later parameter-inference stage would require proper cosmological and nuisance-parameter marginalization. R6a does not license such an inference.

## Claim discipline

Licensed:

- official ACT DR6 fixed-template projection is reproducible;
- the memory lensing template is not purely degenerate with an overall lensing amplitude;
- fixed-cosmology ACT overlap has been computed.

Not licensed:

- detection of gravitational memory;
- a physical estimate or bound on `eta`;
- a likelihood preference for the AeST memory model;
- cosmological parameter constraints;
- Bayes factors or tension claims;
- extrapolation of the local R5b tangent to `|eta| >> 0.05`.

## Strategic consequence

The immediate limitation is amplitude, not template distinctness. The next theory/phenomenology priority should therefore be to map the response versus relaxation time and cosmic lookback history, rather than to interpret the present ACT matched-filter coefficient as evidence. In particular, a redshift/lookback decomposition and a controlled scan toward shorter relaxation times are the natural routes to determine if a physically certified regime exists with a larger observable response.