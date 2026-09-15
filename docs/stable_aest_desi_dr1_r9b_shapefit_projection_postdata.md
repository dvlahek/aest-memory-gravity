# Stable-AeST DESI DR1 R9b ShapeFit projection — post-data record

## Formal result

Historical classification (must not be reclassified):

`STABLE_AEST_DESI_DR1_R9B_CENTRAL_DERIVATIVE_FAIL`

The run completed the official-data and direct-physical theory stage. All 20 frozen `(tau H0, eta)` theory evaluations were finite and completed successfully for

- `tau H0 = {10, 5, 2.5, 1.25}`
- `eta = {0, +/-0.025, +/-0.05}`.

Frozen gates:

- G1 parent + official DESI data provenance: PASS
- G2 direct physical source topology: PASS
- G3 official ShapeFit data construction: PASS
- G4 central-derivative consistency: FAIL
- G5 nuisance projection algebra: not licensed after G4
- G6 matched-filter/GLS identity: not licensed after G4

No DESI memory likelihood preference, `eta_hat`, `Delta chi2`, detection, exclusion, or tau bound is licensed by R9b. The hierarchy stopped before the likelihood stage and `tau_likelihood` is empty.

## Frozen central-derivative metrics

Primary derivative: central `eta = +/-0.025`.
Control derivative: central `eta = +/-0.05`.

| tau H0 | E | cosine | primary norm |
|---:|---:|---:|---:|
| 10 | 0.3516819738456312 | 0.9410421261089041 | 4.1868692009990785e-6 |
| 5 | 0.3396198447582837 | 0.9452407453520312 | 4.162708260364605e-6 |
| 2.5 | 0.3191342588789814 | 0.9521151588254158 | 4.094068471377883e-6 |
| 1.25 | 0.2720351121785079 | 0.9658352354062515 | 3.983799311275194e-6 |

These values fail the preregistered local-derivative consistency requirement and therefore R9b remains a formal FAIL.

## Post-data diagnostic decomposition

This diagnostic does not alter the formal classification.

The 24-dimensional ShapeFit theory vector contains six bins with parameter ordering `(qiso, qap, df, dm)`.

- `qiso` and `qap` have exactly zero memory derivative in this locked fixed-background implementation.
- `dm` derivatives are at approximately `1e-9` to `1e-8` and are numerically floor-sensitive.
- The G4 failure is dominated by the `df` construction.
- The largest discrepancy is around the LRG `z_eff = 0.5096288678782911` bin. For `tau H0 = 10`, the `df` central derivative is approximately `1.42936e-6` from `+/-0.025` but `3.16063e-6` from `+/-0.05`.

R9b constructed ShapeFit `df` through the local proxy

`f_eff = effective_f_sigma8(z) / sigma8(z)`

and then `f_eff * sqrt(Ap)`. This is not the exact velocity-power construction used by the official DESI ShapeFit likelihood, whose implementation builds the growth quantity from density and velocity linear-power grids. Therefore the R9b failure cannot be interpreted as DESI excluding the physical memory model. It demonstrates that this proxy is not sufficiently derivative-stable for a licensed DESI ShapeFit projection at the extremely small certified memory amplitudes.

## Official DESI DR1 data used

Six official DESI DR1 ShapeFit HDF5 files were read, spanning BGS, three LRG bins, ELG and QSO. The assembled data vector has dimension 24, with positive-definite symmetric covariance.

Effective redshifts were read from the official files:

- BGS: 0.29536404346937617
- LRG0: 0.5096288678782911
- LRG1: 0.7057956472488681
- LRG2: 0.9185851971138159
- ELG: 1.3170658832980264
- QSO: 1.4905017757527006

Official DESI likelihood repository commit:

`7d51f4f86dc3bee6bf10f1a684913c943a89a844`

The source topology remained the direct physical R7a stable-AeST closure with no diagnostic replay/trace hook.

## Result hashes

- JSON SHA-256: `f258dc4eb0e9f8d4ffb7b97e5a8ad8d4a15cc6146371bd2bac48fd619b1db653`
- NPZ SHA-256: `5dac6ce29f487e6279c21cdbe1c8bcc5af8db1d1243d8ce375d56a898d4b3b31`
- inner log SHA-256: `67a709fee24d3607789ca63e2ad7f789a98d53a0b2658b1ff989bc9da4bc4b1f`
- full runner log SHA-256: `58fc9d28efd010c4084347b34a0d014d205a762567002fe914b357bc1a810784`
- bundle SHA-256: `fe0120da5127474029dabb972fb0181a9d2df8d0b721107464fae2ec8f02ab1a`

## Licensed interpretation

R9b licenses only the statement that the official DESI DR1 ShapeFit data interface and all frozen direct-physical CLASS runs were reached successfully, but the manually constructed `f_sigma8/sigma8` ShapeFit-growth proxy failed the preregistered central-derivative stability gate. No observational claim follows.

The next test must be a separate follow-up and must not relax R9b's frozen gate. The preferred follow-up is an end-to-end official DESI ShapeFit evaluation through Cobaya with the modified CLASS supplying the density/velocity `Pk_grid` quantities requested by the official likelihood.