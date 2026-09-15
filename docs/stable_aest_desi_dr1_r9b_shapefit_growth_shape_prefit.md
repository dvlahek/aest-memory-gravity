# Stable AeST DESI DR1 R9b — ShapeFit growth/shape projection pre-fit declaration

Date: 2026-09-15
Branch: `fullj-evolving-weyl-bridge`

## Purpose

R9a completed with the certified real-data compressed BOSS DR12 growth classification

`STABLE_AEST_BOSS_DR12_R9A_GROWTH_TEMPLATE_PROJECTION_CERTIFIED`.

R9a showed that the certified local-memory signal is far below the sensitivity of the three-point BOSS DR12 compressed `f sigma8` vector and that those growth points carry almost no discriminating power among `tau H0 = {10,5,2.5,1.25}`.

R9b therefore moves to the official DESI DR1 ShapeFit likelihood. ShapeFit is a compression of the DESI DR1 full-shape power-spectrum + post-reconstruction BAO analysis. It retains geometric and growth/shape information in the measured parameters `qpar/qper` (or equivalent AP combinations), `df`, and `dm` for six non-Lyman-alpha tracer/redshift bins.

R9b is not yet a full EFT/reptvelocileptors re-fit of the raw power-spectrum multipoles. That is reserved for a separate R9c follow-up. R9b is a real-data, full-shape-derived compressed likelihood test.

## Frozen parents

R9b must lock:

- R9a post-data checkpoint `a6c0ed87dbc489f929c2a62fdac93ca6e4a2fd37`, classification exactly `STABLE_AEST_BOSS_DR12_R9A_GROWTH_TEMPLATE_PROJECTION_CERTIFIED`;
- R8b post-data checkpoint `9e21c61210979ab841918ba16f2210020daa245a`, classification exactly `STABLE_AEST_COSMIC_MEMORY_R8B_TWO_TAU_LOOKBACK_CERTIFIED`;
- R8a2 post-data checkpoint `590dbc69e2823f583b157af2297e357991103c47`, classification exactly `STABLE_AEST_COSMIC_MEMORY_R8A2_TAU_GENERALITY_CERTIFIED`;
- R7a post-data checkpoint `86c03e6ba2ee9fcbf33a9d319d12ae778a747881`, classification exactly `STABLE_AEST_COSMIC_MEMORY_R7A_LIVE_LOOKBACK_DECOMPOSITION_CERTIFIED`.

Historical classifications remain unchanged.

## Official DESI data/likelihood lock

Use only the public official DESI Key Project likelihood repository

`cosmodesi/desi-kp-cosmological-likelihoods`

at exact commit

`7d51f4f86dc3bee6bf10f1a684913c943a89a844`.

The public likelihood-data root is frozen to

`https://data.desi.lbl.gov/public/dr1/vac/dr1/full-shape-bao-clustering/v1.0/data/likelihood/`.

The official repository's `dr1/cobaya/download.py` is used to obtain the likelihood HDF5 products. Runtime SHA-256 values of every ShapeFit HDF5 file used by R9b must be recorded in the result manifest and bundle. No local pre-existing copy is trusted without hash agreement with the freshly downloaded file.

The official ShapeFit construction is taken from the pinned file

`dr1/cobaya/desi_shapefit_bao_all.py`.

The observable is frozen to

`spectrum-poles-rotated+bao-recon`.

Use the six non-Lyman-alpha full-shape bins:

- `BGS_z0`: BGS_BRIGHT-21.5, z range 0.1--0.4;
- `LRG_z0`: LRG, z range 0.4--0.6;
- `LRG_z1`: LRG, z range 0.6--0.8;
- `LRG_z2`: LRG, z range 0.8--1.1;
- `ELG_z1`: ELG_LOPnotqso, z range 1.1--1.6;
- `QSO_z0`: QSO, z range 0.8--2.1.

Lyman-alpha is excluded because it has no ShapeFit full-shape component in the official implementation.

## Frozen AeST-memory model

Use the same certified direct physical stable-AeST memory realization as R8a2/R8b/R9a:

- frozen CLASS parent `e85808324f51fc694d12e3ed7439552a3c3f9540`;
- stable `chi = Q s` residual dynamics;
- memory order 20;
- `tol_perturbations_integration = 3e-8`;
- no Halofit/nonlinear correction inside CLASS for constructing the linear ShapeFit template;
- direct physical feedback only;
- zero diagnostic external tangent hooks;
- zero R2d trace/replay hooks;
- epoch mode `full`;
- `tau H0 = {10, 5, 2.5, 1.25}`;
- central derivative `eta = +/-0.025`;
- first-order control `eta = +/-0.05`;
- one `eta=0` baseline for each tau.

The signed negative-eta branch is a derivative diagnostic around eta=0 and is not interpreted as a separately physical cosmology.

## ShapeFit theory construction

Follow the pinned official DESI definitions.

For every DESI effective redshift read from the HDF5 observable:

1. construct the linear clustering-species density spectrum from the modified CLASS `P_cb(k,z)`;
2. smooth the BAO using the same `cosmoprimo.PowerSpectrumBAOFilter(..., engine='peakaverage')` construction as the official likelihood;
3. compute the broadband slope `m` around the official pivot `kp = 0.03 h/Mpc` with `dk = 1e-2`;
4. compute the density amplitude `Ap` at the same pivot and sound-horizon rescaling;
5. obtain the effective linear growth rate from the modified CLASS direct observable using `f_eff = effective_f_sigma8(z) / sigma8(z)`; this replaces the official CAMB velocity-grid implementation because the stock Cobaya CLASS backend does not expose the required velocity-velocity `Pk_grid` pairs;
6. construct `f_sqrt_Ap = f_eff * sqrt(Ap)`;
7. map to the official ShapeFit quantities: `df` is the ratio of `f_sqrt_Ap` to the pinned DESI fiducial template, and `dm` is the difference in `m` from the same fiducial template;
8. construct `qpar`, `qper`, `qiso`, or `qap` exactly as requested by each HDF5 parameter list from CLASS H(z), angular-diameter distance, and `rdrag`, using the official DESI fiducial cosmology.

Because the AeST memory term is perturbative and does not alter the frozen background in this realization, the first-order memory tangent in AP geometry is expected to be zero up to numerical noise. This expectation is diagnostic only and is not a gate on the sign of any data preference.

The use of `effective_f_sigma8/sigma8` for `f_eff` must be explicitly recorded in outputs. R9b therefore licenses a DESI ShapeFit projection for this frozen construction, not an exact claim that the stock official CAMB velocity-grid implementation has been reproduced for modified gravity.

## Likelihood and nuisance deprojection

For each bin, use the exact data vector, exact parameter order, and exact covariance matrix from the corresponding official ShapeFit HDF5 file.

Concatenate all six bins into one block-diagonal data/covariance system, matching the official implementation in which the six bin likelihoods are summed independently.

Let `b` be the eta=0 ShapeFit theory vector and `t_tau` the central derivative at fixed tau.

To avoid calling a broadband normalization mismatch "memory", define nuisance columns spanning, for every bin separately:

- one local `df` amplitude direction if `df` is present;
- one local `dm` offset direction if `dm` is present.

AP directions are not nuisance-deprojected; they remain in the baseline residual, while their memory tangent is expected to vanish because the background is unchanged.

Project `t_tau` orthogonally to the full nuisance design matrix N in the covariance metric:

`P_perp = C^-1 - C^-1 N (N^T C^-1 N)^-1 N^T C^-1`,

`F_perp = t_tau^T P_perp t_tau`.

The signed matched-filter estimate is

`eta_hat = (t_tau^T P_perp (d-b)) / F_perp`,

with

`sigma_eta = F_perp^-1/2`.

An independent generalized least-squares solve with columns `[N, t_tau]` must reproduce the same `eta_hat`.

The physical local interval remains frozen to

`0 <= eta <= 0.05`.

Report the best point in this interval and `Delta chi2_phys` relative to eta=0 after nuisance profiling.

No detection threshold is preregistered. The observed `eta_hat/sigma_eta`, sign, tau dependence and `Delta chi2_phys` are science outputs, not pass/fail criteria.

## Gates

### R9B-G1 parent and official-data provenance

PASS iff all frozen parent commits are ancestors of HEAD with exact certified classifications, the official DESI likelihood repository is at the pinned commit, all six required HDF5 products are freshly downloaded from the frozen v1.0 URL, their SHA-256 values are recorded, and all files are readable with finite data/covariance.

### R9B-G2 direct physical source topology

PASS iff the disposable CLASS source has the stable-chi marker, one physical memory closure, one physical eta multiplier, zero external variational forcing hooks, zero R2d trace hooks, and signed diagnostic eta is permitted.

### R9B-G3 ShapeFit data construction

PASS iff all six non-Lya bins are found, all official parameter lists and effective redshifts are read from the HDF5 files, every covariance matrix is finite, symmetric to numerical precision and positive definite, and every eta=0 theory vector is finite.

### R9B-G4 central derivative consistency

For each tau, compare the concatenated ShapeFit tangent from epsilon=0.025 with epsilon=0.05.

PASS iff relative L2 difference <= 0.05 and cosine >= 0.995 for the full concatenated tangent after excluding exactly-zero AP entries from the numerical comparison.

### R9B-G5 nuisance-projection algebra

PASS iff all nuisance normal matrices are finite/invertible, `F_perp > 0`, and the explicit projection is idempotent in the covariance metric to relative numerical error <= 1e-8.

### R9B-G6 matched-filter / GLS identity

PASS iff the nuisance-projected matched-filter `eta_hat` and an independent GLS solution with columns `[N, t_tau]` agree for every tau to relative difference <= 1e-8 (or absolute difference <= 1e-10 near zero).

If G1--G6 all pass, classification is

`STABLE_AEST_DESI_DR1_R9B_SHAPEFIT_MEMORY_PROJECTION_CERTIFIED`.

## Claim discipline

A PASS licenses only:

- a reproducible projection of the frozen stable-AeST local memory tangent onto official DESI DR1 ShapeFit compressed full-shape+BAO data;
- reporting signed memory-shape projections and physical-interval Delta chi2 values for the tested tau grid;
- comparison of tau sensitivity within this frozen construction.

R9b does not license:

- observational detection of gravitational memory;
- a bound on tau or eta outside the validated local interval;
- a raw power-spectrum full-EFT modified-gravity claim;
- a claim that the `effective_f_sigma8/sigma8` velocity proxy is identical to the official CAMB velocity-grid construction in modified gravity;
- reclassification of R9a or any earlier result.

A nonzero or apparently significant R9b preference must be confirmed by a separately preregistered R9c using the official DESI full power-spectrum likelihood and nonlinear RSD/EFT nuisance treatment before it can be interpreted as evidence for new gravitational physics.
