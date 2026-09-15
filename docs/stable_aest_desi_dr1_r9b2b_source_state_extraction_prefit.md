# Stable AeST DESI DR1 R9b2b source-state extraction closure preregistration

## Purpose

R9b2a completed with historical classification

`STABLE_AEST_DESI_DR1_R9B2A_SERIALIZATION_FREE_EXTRACTION_UNRESOLVED`.

It falsified the preregistered `k_output_values` contamination hypothesis in the DESI extraction path: locked, adjacent-ULP, and no-`k_output_values` variants agreed to approximately 1e-11. However, the external extraction itself produced nonphysical density and/or velocity spectra at several frozen DESI effective redshifts while the internal growth observables remained stable and eta=0 tau-invariant.

The preserved v0.76-v0.78 audits already established the relevant numerical mechanism. Native source-to-Fourier closure is essentially exact, the native state tangent is stable, and v0.78 localized large off-native-time source-versus-`pk_lin` discrepancies to distinct CLASS time-interpolation operators. v0.76 additionally showed that fractional quantities formed by division through deep transfer minima are ill-conditioned.

R9b2b therefore tests one specific repair of the *extraction representation only*: construct density and velocity power from the same transfer state and the same primordial prefactor, without `pk_cb_lin` and without the ratio `v_cb/d_cb`.

This is a theory-only prefit diagnostic. No DESI data vector, covariance, likelihood, eta derivative, matched filter, or physical eta preference is evaluated.

## Frozen provenance

Required ancestors/results:

- R9b2a post-result record: `00d06aa140fc8e9097be3df62ecd6013f0c8b312`
- R9b2 historical postdata: `5f453a296d367556927cfa8e1e86b7ea103a9b52`
- R9b2 velocity-adapter result: `f5484b4572b673dfcead51875e3aa790c698a18c`
- v0.78 successful implementation/result commit: `31c05c22b86e8ac01ce822306efecdcb03cff1d5`
- frozen CLASS parent remains `e85808324f51fc694d12e3ed7439552a3c3f9540`

Required historical classifications remain unchanged:

- `STABLE_AEST_DESI_DR1_R9B2_CENTRAL_DERIVATIVE_FAIL`
- `STABLE_AEST_DESI_DR1_R9B2A_SERIALIZATION_FREE_EXTRACTION_UNRESOLVED`
- `STABLE_AEST_DESI_DR1_R9B2_VELOCITY_ADAPTER_VALIDATED`
- `V078_TIME_INTERPOLATION_OPERATOR_CLOSURE_PASS`
- `V078_TIME_INTERPOLATION_OPERATOR_DISCREPANCY_LOCALIZED`

No earlier FAIL may be reclassified by R9b2b.

## Frozen redshifts and model settings

Effective-redshift grid, in the existing order:

- 0.29536404346937617
- 0.5096288678782911
- 0.7057956472488681
- 0.9185851971138159
- 1.3170658832980264
- 1.4905017757527006

Stable AeST eta=0 checks use

- `tau_H0 = {10, 5, 2.5, 1.25}`
- `eta = 0`
- `tol_perturbations_integration = 3e-8`
- `aest_memory_order = 20`
- `output = mPk,mTk,vTk`
- `P_k_max_h/Mpc = 5`
- `z_max_pk >= 2.3`
- no nonlinear correction
- no lensing
- no `k_output_values` request for the source-state extraction check.

The GR control uses the same background/numerical setup with `aest_enabled=no` and `aest_memory_enabled=no`.

## Frozen source-state construction

At each requested redshift, use CLASS `get_transfer(z, output_format="class")` and its native returned k grid. Require fields

- `k (h/Mpc)`
- `d_b`, `d_cdm`
- `t_b`, `t_cdm`.

Use

`fb = Omega_b / (Omega_b + Omega_cdm)`

`fc = 1 - fb`

`d_cb = fb d_b + fc d_cdm`

`Hconf = Hubble(z)/(1+z)`

`v_b = -t_b/Hconf`

`v_cdm = -t_cdm/Hconf`

`v_cb = fb v_b + fc v_cdm`.

For physical `k = h k_h`, use the dimensionless primordial curvature spectrum

`P_R(k) = A_s (k/0.05 Mpc^-1)^(n_s-1)`

and common source prefactor

`C(k) = (2 pi^2 / k^3) P_R(k)`.

Construct directly

`P_dd_phys = C(k) d_cb^2`

`P_tt_phys = C(k) v_cb^2`.

Convert to `(Mpc/h)^3` for the cosmoprimo interpolators by multiplying the physical-Mpc spectrum by `h^3`.

**Forbidden inside this construction:**

- `pk_cb_lin`
- `pk_lin`
- multiplication by `(v_cb/d_cb)^2`
- division by `d_cb` or by local density power.

This is intentionally the same source-state logic certified by the preserved v0.78 diagnosis, extended to the cb velocity state.

## Frozen sigma8 and growth construction

Build `PowerSpectrumInterpolator1D(k_h, P_dd)` and `PowerSpectrumInterpolator1D(k_h, P_tt)` on the same retained transfer nodes and compute

`sigma8_dd = sigma8(P_dd)`

`sigma8_tt = sigma8(P_tt)`

`f_source = sigma8_tt / sigma8_dd`.

The ratio is taken only after the two positive integrated RMS quantities have been formed. No local transfer ratio is permitted.

## Gates

All thresholds are frozen before the run.

### R9B2B_B1 — provenance and historical-lock gate

PASS if all required commits are ancestors, the locked R9b2/R9b2a/adapter classifications match exactly, and the preserved v0.78 interpretation contains both

- `V078_TIME_INTERPOLATION_OPERATOR_CLOSURE_PASS`
- `V078_TIME_INTERPOLATION_OPERATOR_DISCREPANCY_LOCALIZED`.

### R9B2B_B2 — source-state construction gate

PASS if the implementation source contains the direct `d_cb^2` and `v_cb^2` construction and the extraction helper contains no call to `pk_cb_lin`, no call to `pk_lin`, and no local `v_cb/d_cb` or equivalent division.

### R9B2B_B3 — pure-GR benchmark gate

For all six frozen redshifts, compare the source-state GR result to the already locked R9b2 velocity-adapter CLASS and CAMB values.

PASS if each of

- relative `sigma8_dd` difference versus locked CLASS adapter <= 5e-3
- relative `sigma8_tt` difference versus locked CLASS adapter <= 5e-3
- relative `f_source` difference versus locked CLASS adapter <= 5e-3
- relative `f_source` difference versus locked CAMB <= 5e-3

and all source spectra/RMS values are finite and positive.

This retains the original adapter tolerance and does not introduce a looser post-result criterion.

### R9B2B_B4 — eta=0 AeST source/internal consistency gate

At `tau_H0=10`, PASS if at all six redshifts

- `0.1 < sigma8_dd_source < 2`
- `0.05 < f_source < 2`
- relative difference between `sigma8_dd_source` and CLASS internal `sigma(8,z,h_units=True)` <= 5e-3
- relative difference between `f_source` and the non-gating historical diagnostic `effective_f_sigma8/sigma8` <= 5e-3.

The internal proxy remains only a closure control and is not adopted as the DESI df definition.

### R9B2B_B5 — eta=0 tau-invariance gate

Using source-state extraction at `tau_H0={10,5,2.5,1.25}`, compare each tau to tau=10 at all six redshifts.

PASS if the maximum relative change in each of

- `sigma8_dd_source`
- `sigma8_tt_source`
- `f_source`

is <= 5e-3.

### R9B2B_B6 — pathological-point removal gate

PASS if every source-state point for all four eta=0 tau values is finite/positive and has

- `0.1 < sigma8_dd_source < 2`
- `0.05 < f_source < 2`.

This gate is specifically intended to reject the R9b2a-type explosions (`sigma8_dd ~ 1e4-1e12`, `f ~ 1e7-1e58`).

## Classification

If B1-B6 all pass:

`STABLE_AEST_DESI_DR1_R9B2B_SOURCE_STATE_EXTRACTION_VALIDATED`

Otherwise use the first applicable failure class:

- `STABLE_AEST_DESI_DR1_R9B2B_PROVENANCE_FAIL`
- `STABLE_AEST_DESI_DR1_R9B2B_SOURCE_CONSTRUCTION_FAIL`
- `STABLE_AEST_DESI_DR1_R9B2B_GR_BENCHMARK_FAIL`
- `STABLE_AEST_DESI_DR1_R9B2B_AEST_ETA0_CLOSURE_FAIL`
- `STABLE_AEST_DESI_DR1_R9B2B_ETA0_TAU_INVARIANCE_FAIL`
- `STABLE_AEST_DESI_DR1_R9B2B_SOURCE_STATE_SANITY_FAIL`
- `STABLE_AEST_DESI_DR1_R9B2B_RUN_FAIL` for a technical exception.

## Interpretation policy

A PASS validates only the source-consistent extraction representation needed for a later separately locked DESI ShapeFit projection. It does not reclassify R9b2, does not evaluate DESI evidence, does not establish a nonzero eta, and does not constrain tau.

A PASS may license a separately preregistered R9b2c source-consistent ShapeFit projection that constructs the density-shape (`m`, `Ap`) and velocity (`df`) pieces from the same source-state density/velocity spectra.

A FAIL stops that route and must be diagnosed before any new DESI science likelihood is run.
