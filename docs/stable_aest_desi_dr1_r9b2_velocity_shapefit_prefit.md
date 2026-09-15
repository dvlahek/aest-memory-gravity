# Stable AeST DESI DR1 R9b2 — direct-velocity ShapeFit projection pre-fit declaration

Date: 2026-09-15
Branch: `fullj-evolving-weyl-bridge`

## Status before R9b2

R9b completed as

`STABLE_AEST_DESI_DR1_R9B_CENTRAL_DERIVATIVE_FAIL`.

That historical result is not modified or reclassified. R9b established that the official DESI DR1 ShapeFit files, covariance construction, frozen stable-AeST source topology, and all 20 `(tau, eta)` CLASS runs were valid, but the first ShapeFit growth mapping failed the preregistered central-derivative consistency gate.

No nuisance-projected DESI memory estimate, likelihood preference, physical-interval Delta chi2, detection claim, or tau bound was produced by R9b because G4 failed before those quantities were evaluated.

A post-run code audit identified the methodological cause: R9b approximated the ShapeFit growth quantity with

`f_eff = effective_f_sigma8(z) / sigma8(z)`.

The pinned official DESI implementation instead constructs a density-density spectrum and a velocity-velocity spectrum, then defines

`f = sigma8[P_theta_theta] / sigma8[P_delta_delta]`,

with the velocity field formed from the baryon and CDM Newtonian-gauge velocity transfers. R9b2 replaces only this growth adapter.

## Frozen parents and historical lock

R9b2 must lock the R9b post-result commit

`22583094f3c5a417e7af6b1d7f284f739553048b`

and require its classification to remain exactly

`STABLE_AEST_DESI_DR1_R9B_CENTRAL_DERIVATIVE_FAIL`.

R9b2 also retains the certified R9a, R8b, R8a2, and R7a parents used by R9b. No earlier result is reclassified.

## Official DESI definition

Use the same official DESI Key Project likelihood repository and exact commit as R9b:

`cosmodesi/desi-kp-cosmological-likelihoods`

`7d51f4f86dc3bee6bf10f1a684913c943a89a844`.

Use the same six non-Lyman-alpha ShapeFit HDF5 products and observable

`spectrum-poles-rotated+bao-recon`.

The direct-velocity construction must reproduce the structure of the pinned official `desi_shapefit_bao_all.py` implementation:

1. density spectrum from clustering species;
2. baryon/CDM velocity fields combined with the same baryon fraction weights used by the official likelihood;
3. velocity-velocity spectrum from that combined field;
4. `f = sigma8[P_theta_theta] / sigma8[P_delta_delta]`;
5. `f_sqrt_Ap = f * sqrt(Ap)`;
6. `df = f_sqrt_Ap / f_sqrt_Ap_fid`.

## Frozen direct CLASS velocity adapter

The frozen stable-AeST baseline runs CLASS in Newtonian gauge. R9b2 requests CLASS transfer outputs with `mTk,vTk` in addition to the linear matter spectrum.

At each DESI effective redshift `z`, read the CLASS transfer dictionary and require the fields

- `k (h/Mpc)`;
- `d_b`, `d_cdm`;
- `t_b`, `t_cdm`.

CLASS source inspection fixes the meaning of the velocity columns: in CLASS-format transfer output, `t_b` stores the baryon velocity-divergence source `theta_b`, and `t_cdm` stores `theta_cdm` in Newtonian gauge. They are not velocity potentials.

Let

`f_b = Omega_b / (Omega_b + Omega_cdm)` and `f_c = 1 - f_b`.

Construct the clustering-species density transfer

`delta_cb = f_b d_b + f_c d_cdm`.

For Newtonian gauge, define the CAMB/DESI dimensionless Newtonian-velocity transfer candidate from the CLASS divergence by

`v_newtonian_x = - t_x / Hconf`,

where `Hconf = a H` is the conformal Hubble rate in `1/Mpc`. No extra factor of `k` is inserted. This follows the standard relation between velocity divergence and scalar velocity amplitude and the CAMB definition `v_newtonian_x = -v_N,x k/Hconf`.

This normalization is not accepted on convention alone: it must pass the frozen GR cross-code validation below before any AeST R9b2 science result is evaluated.

Then construct

`v_cb = f_b v_newtonian_b + f_c v_newtonian_cdm`.

For adiabatic scalar initial conditions, the auto/cross velocity combination used by the official likelihood is equivalently represented on the same CLASS mode grid by

`P_theta_theta(k,z) = P_cb(k,z) * [v_cb(k,z) / delta_cb(k,z)]^2`.

The density spectrum remains the direct modified-CLASS linear `P_cb(k,z)`. No numerical redshift derivative is used in the primary `df` construction.

The old `effective_f_sigma8/sigma8` value may be recorded only as a non-gating diagnostic. It cannot enter `df`, the central tangent, nuisance projection, matched filter, or classification.

## Frozen GR cross-code validation before AeST science

Before evaluating any `eta != 0` AeST R9b2 point, run a pure GR/LambdaCDM control at the same six DESI effective redshifts and with the same background/primordial parameters in CLASS and CAMB.

From CLASS construct

- `P_delta_delta^CLASS` from the direct linear clustering-species spectrum;
- `P_theta_theta^CLASS` from `t_b,t_cdm` using the adapter above;
- `f^CLASS = sigma8[P_theta_theta^CLASS] / sigma8[P_delta_delta^CLASS]`.

From CAMB request the native transfer/power variables

- `delta_nonu`;
- `v_newtonian_cdm`;
- `v_newtonian_baryon`;

and reproduce the official DESI baryon/CDM weighted velocity combination and corresponding `f^CAMB`.

The validation is performed only on theory outputs, before reading any DESI residual or likelihood preference.

The direct-velocity adapter is accepted iff, for all six effective redshifts,

- the CLASS and CAMB density-spectrum sigma8 values agree to relative `<= 5e-3`;
- the CLASS and CAMB velocity-spectrum sigma8 values agree to relative `<= 5e-3`;
- the resulting `f` values agree to relative `<= 5e-3`;
- the sign/orientation is common across the retained linear k range and all reconstructed spectra are finite and nonnegative.

If this validation fails, R9b2 stops as an adapter-validation failure. No alternative normalization is selected after looking at AeST/DESI science output. A corrected adapter requires a new pre-result repair declaration.

## Unchanged physics and analysis settings

Everything below is unchanged from R9b:

- frozen CLASS parent `e85808324f51fc694d12e3ed7439552a3c3f9540`;
- direct physical stable-chi memory closure;
- memory order 20;
- `tol_perturbations_integration = 3e-8`;
- no external tangent forcing and no R2d replay/trace forcing;
- epoch mode `full`;
- `tau H0 = {10, 5, 2.5, 1.25}`;
- central derivative `eta = +/-0.025`;
- control derivative `eta = +/-0.05`;
- one `eta=0` baseline per tau;
- physical interval `0 <= eta <= 0.05`;
- same ShapeFit BAO smoothing, pivot, `Ap`, `m`, AP geometry, data vectors, covariance matrices, bin ordering, and fiducial cosmology;
- exactly two global nuisance columns: one common `df` scale and one common `dm` offset;
- no AP nuisance deprojection.

## Gates

### R9B2-G1 historical parent and official-data provenance

PASS iff the frozen R9b post-result commit is an ancestor of HEAD with exact historical classification `STABLE_AEST_DESI_DR1_R9B_CENTRAL_DERIVATIVE_FAIL`, its G1-G3 remain true, and the same official DESI repository/data provenance checks used by R9b pass.

### R9B2-G2 direct physical source topology

Identical to R9b G2.

### R9B2-G3 direct-velocity adapter validation and ShapeFit construction

PASS iff the frozen GR CLASS-vs-CAMB cross-code validation above passes, all six ShapeFit bins are valid, all eta=0 theory vectors are finite, every requested CLASS transfer dictionary contains the frozen density and velocity fields, the transfer k grid is finite/strictly positive, `delta_cb` is nonzero on the retained grid, the reconstructed `P_theta_theta` is finite and nonnegative, and every resulting `df` and `dm` is finite.

### R9B2-G4 central derivative consistency

Unchanged from R9b. For each tau compare the full concatenated ShapeFit tangent from epsilon=0.025 with epsilon=0.05 after excluding exactly-zero AP entries.

PASS iff

`relative L2 difference <= 0.05`

and

`cosine >= 0.995`.

The thresholds are not relaxed in response to the failed R9b proxy result.

### R9B2-G5 nuisance-projection algebra

Unchanged from R9b: finite/invertible nuisance normal matrix, positive deprojected Fisher information, and covariance-metric projector idempotence error `<= 1e-8`.

### R9B2-G6 matched-filter / GLS identity

Unchanged from R9b: matched-filter and independent GLS `eta_hat` agree to relative `<= 1e-8` or absolute `<= 1e-10` near zero.

If G1-G6 all pass, classification is

`STABLE_AEST_DESI_DR1_R9B2_DIRECT_VELOCITY_SHAPEFIT_MEMORY_PROJECTION_CERTIFIED`.

## Claim discipline

A PASS licenses a reproducible projection of the frozen stable-AeST local memory tangent onto the official DESI DR1 ShapeFit compression using a direct CLASS velocity-transfer construction cross-validated against CAMB and consistent with the official DESI velocity/density definition.

It still does not license an observational detection, a tau/eta bound beyond the validated local interval, or a raw full-EFT modified-gravity claim. Any interesting nonzero DESI preference remains subject to the separately preregistered R9c full power-spectrum/EFT confirmation.