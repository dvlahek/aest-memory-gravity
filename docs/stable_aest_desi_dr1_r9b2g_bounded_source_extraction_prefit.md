# Stable AeST DESI DR1 R9b2g bounded source-state extraction preregistration

## Purpose

R9b2f certified

`STABLE_AEST_DESI_DR1_R9B2F_HIGH_K_EXTRAPOLATION_DEFECT_CERTIFIED`.

The defect is caused by generic power-spectrum extrapolation beyond the actual CLASS transfer support. The same transfer state becomes healthy when the cosmoprimo interpolator is bounded to the true CLASS k interval, and an independent bounded log-linear integration reproduces that result.

R9b2g validates a corrected theory-only extraction over the complete frozen R9b2 `(tau, eta)` grid before any DESI likelihood is re-run.

No DESI data vector, covariance, residual, likelihood, eta preference, or tau constraint is loaded or evaluated.

## Frozen provenance

Required ancestors:

- R9b2f postdata: `b569aebc41efc841755f5fcec63b91092c192ba3`
- R9b2f preregistration: `8413ed74450e387b3dee543ff67b39bf2cbb31bc`
- R9b2f implementation: `1c1cbbbdc2fcb43441c1659f7282ae40c3b18487`
- R9b2e postdata: `f1f2bfd032065360ec7a18c080403d6e39f54dc7`
- corrected CLASS parent remains `e85808324f51fc694d12e3ed7439552a3c3f9540`.

Historical FAIL classifications remain unchanged.

## Frozen physics and theory coordinates

Use exactly the original R9b2 grids:

- `tau_H0 = {10, 5, 2.5, 1.25}`
- `eta = {0, +0.025, -0.025, +0.05, -0.05}`
- `aest_memory_order = 20`
- `tol_perturbations_integration = 3e-8`
- `AEST_R7A_EPOCH_MODE=full`
- same corrected/stable-chi CLASS source
- no nonlinear correction
- no lensing.

Use the same six theory redshifts:

`{0.29536404346937617, 0.5096288678782911, 0.7057956472488681, 0.9185851971138159, 1.3170658832980264, 1.4905017757527006}`.

Use DEFAULT CLASS k sampling. Remove inherited forensic `k_per_decade_for_pk`, `k_per_decade_for_bao`, and `k_output_values`.

## Frozen source-state construction

At each z read the complete finite common transfer grid `k,d_b,d_cdm,t_b,t_cdm` and construct

- `d_cb = f_b d_b + f_c d_cdm`
- `v_cb = -(f_b t_b + f_c t_cdm)/Hconf`
- `P_dd = C(k) d_cb^2`
- `P_tt = C(k) v_cb^2`

with the same primordial prefactor already frozen in R9b2b/f.

Forbidden:

- `pk_lin` or `pk_cb_lin` inside the growth extraction
- local `v_cb/d_cb`
- removal/clipping of individual k nodes
- extrapolation outside the actual retained CLASS transfer support.

## Two independent bounded integrals

For every `(tau,eta,z)` compute:

### BOUNDED_COSMO

`PowerSpectrumInterpolator1D(k,P, extrap_kmin=k[0], extrap_kmax=k[-1]).sigma8()`.

### BOUNDED_LOGLINEAR

Direct Simpson integration over 8192 equally spaced log-k samples on `[k[0],k[-1]]`, linearly interpolating `log P` versus `log k`, with no extrapolation:

`sigma8^2 = 1/(2 pi^2) int dlnk k^3 P(k) W_TH(8k)^2`.

Define `f = sigma8_tt/sigma8_dd` only after the two positive variance integrals.

## Frozen gates

Use `REL_GATE=5e-3`, and retain the original R9b/R9b2 central-derivative thresholds `E<=0.05`, `C>=0.995`.

### G1 provenance / construction
PASS if all frozen ancestors exist and source inspection confirms bounded support, source-state `d_cb^2/v_cb^2`, no pk_lin/pk_cb_lin, no local velocity/density ratio, and DEFAULT k sampling.

### G2 full-grid finiteness and physicality
PASS if all 20 x 6 BOUNDED_COSMO and BOUNDED_LOGLINEAR rows are finite and positive, with
- `0.1 < sigma8_dd < 2`
- `0.05 < f < 2`.

### G3 independent bounded-integral agreement
PASS if maximum relative BOUNDED_COSMO vs BOUNDED_LOGLINEAR difference over all 120 rows is <= `5e-3` for each of `sigma8_dd`, `sigma8_tt`, and `f`.

### G4 eta=0 internal closure
For all four tau values and six redshifts, PASS if BOUNDED_COSMO eta=0 obeys
- relative `sigma8_dd` vs CLASS internal `sigma(8,z)` <= `5e-3`
- relative `f` vs historical internal `effective_f_sigma8/sigma8` <= `5e-3`.

The internal growth proxy remains diagnostic only and is not adopted as the DESI df definition.

### G5 eta=0 tau invariance
At each z compare eta=0 across all four tau values. PASS if maximum relative variation in `sigma8_dd`, `sigma8_tt`, and `f` is <= `5e-3`.

### G6 original central-derivative consistency
For each tau define six-component bounded-f vectors `F(eta)` and

- `T_primary = [F(+0.025)-F(-0.025)] / 0.05`
- `T_control = [F(+0.05)-F(-0.05)] / 0.10`.

Compute the same consistency quantities used by R9b/R9b2:

- `E = ||T_primary-T_control|| / max(||T_primary||,||T_control||,1e-300)`
- `C = cosine(T_primary,T_control)`.

PASS for each tau if `E<=0.05`, `C>=0.995`, and `||T_primary||>1e-12`.

## Classification

If G1-G6 pass:

`STABLE_AEST_DESI_DR1_R9B2G_BOUNDED_SOURCE_EXTRACTION_VALIDATED`.

Otherwise use the first failed gate in order:

- `...PROVENANCE_OR_CONSTRUCTION_FAIL`
- `...FINITE_PHYSICALITY_FAIL`
- `...BOUNDED_INTEGRAL_CROSSCHECK_FAIL`
- `...ETA0_INTERNAL_CLOSURE_FAIL`
- `...ETA0_TAU_INVARIANCE_FAIL`
- `...CENTRAL_DERIVATIVE_FAIL`
- technical exceptions: `...RUN_FAIL`.

## Interpretation policy

A PASS licenses only a separately preregistered corrected compressed-ShapeFit projection using this bounded direct growth extraction. It does not itself constitute observational evidence, a detection, an eta bound, a tau bound, or a raw EFT modified-gravity analysis.
