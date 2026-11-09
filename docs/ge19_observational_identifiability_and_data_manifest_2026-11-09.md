# GE19 — observation-first hypothesis: identifiability, controls, and accessible public data

**Date:** 2026-11-09. **Status:** READ-ONLY DATA-MANIFEST / THEORY DESIGN; NO FIT OR OBSERVATIONAL RESULT. This is not a preregistered detection experiment or a substitute for LW04 and line-of-sight theory closure.

## The physical identification problem — one curve is not proof of memory

The positive-Drude model predicts a retarded linear source functional in the idealized constant-H approximation,

\[
B_k(t)=\int_{-\infty}^t f_H(t-u)\,\dot X_k(u)\,du.
\]

For **one fixed history** with \(X_k(t)\ne0\), define \(\gamma_{\mathrm{eff}}(k,t)=B_k(t)/X_k(t)\). Then an instantaneous equation \(B_k(t)=\gamma_{\mathrm{eff}}(k,t)X_k(t)\) reproduces exactly that *same history*. Therefore **an arbitrary scale- and time-dependent instantaneous effective coupling is observationally degenerate with a memory response on a single collection of unconstrained histories**. This is a basic functional identifiability issue, not an argument that the memory model is false. Singular points \(X=0\) require additive rather than local-ratio treatment; the logic extends away from those points and in terms of arbitrarily flexible effective operators.

A causal-memory discovery therefore requires **restricted, independently motivated physical alternatives**, not simply rejecting one fixed \(\Lambda\)CDM spectrum. Cosmological fields provide many mode histories; compare them jointly across scales and redshifts, use matched-background alternatives with a small explicit parameter family, and test whether history dependence buys uniquely predictive structure. A generic unconstrained modified-gravity function \(\mu(k,z)\) cannot be uniquely defeated by one set of linear two-point functions.

**Precommit novelty test before observed residual inspection:** can the *frozen* positive-Drude theory predict a distinguishable multipole-/tomography-dependent shape in lensing + velocity/growth/clustering, or do its templates collapse into combinations of \(S_8\), growth rate, galaxy bias, intrinsic alignment, photo-z, baryonic effects, and ordinary restricted modified gravity? Use an Asimov (noise-free) forecast and released covariance to project the memory template away from nuisance/instantaneous-model tangent spaces. If orthogonal distinguishability is too small under credible priors, do **not** seek a posthoc significant bin.

## Public data sources to prepare, but not yet statistically inspect

1. **DES Y3 cosmology data release:** [DES public Y3A2](https://des.ncsa.illinois.edu/releases/y3a2), [DES Y3 papers](https://www.darkenergysurvey.org/des-year-3-cosmology-results-papers/). Target the public 3x2pt data-vector/covariance, tomographic lens/source \`n(z)\`, and original scale-cut mask. User's earlier local OBS work has \`des_y3_observed_gammat.csv\`, \`des_y3_observed_gammat_covariance.npz\`, \`des_y3_gammat_theory_input_480.csv\`, and \`des_y3_nz_and_theory_index.npz\`; **existence/provenance must be rechecked** before use. Only schema/units/bin-index/mask/positive-semidefinite covariance audits are permissible now, not observing data residuals to select a model.
2. **ACT DR6 lensing:** [NASA LAMBDA derived lensing likelihood data](https://lambda.gsfc.nasa.gov/product/act/actadv_dr6_lensing_lh_info.html) explicitly include bandpowers, covariance, binning, fiducial spectra and likelihood correction matrices; [ACT Princeton full DR6.02 release](https://act.princeton.edu/act-dr6-data-products). Do not confuse the **primary CMB** DR6.02 likelihood with ACT **lensing** \`act_dr6_lenslike\`, and do not compare only a projected low-redshift GE19 \`k,z\` sliver to a CMB full LOS kernel.
3. **Existing small cross-probe pilot data:** [NASA LAMBDA ACT DR4 kappa × DES Y3 cosmic shear](https://lambda.gsfc.nasa.gov/product/act/act_xdes_cosmic_shear_get.html) supplies a FITS with bandpowers, covariance and redshift distribution. This combines different instruments but shares DES Y3 shear input; it is **not an independent full replication** of a DES Y3 shear discovery.
4. **DES Y6:** [DES Y6 cosmology results and methodological papers](https://www.darkenergysurvey.org/des-y6-cosmology-results-papers/) are public. Their 3x2pt galaxy/shear fields overlap DES Y3 substantially; Y6 is improved precision, not an independent holdout by itself. Confirm **product-level** availability and identical data-covariance conventions before any evaluation.
5. **Euclid:** [official public data timeline](https://euclid.caltech.edu/page/data-release-timeline) indicates DR1 Foundation **November 12, 2026**, future relative to this note, and complete higher-level weak-lensing DR1 **mid-2027**. Do not assume the later science products are currently public.

## Three-stage experiment (not yet authorized to analyze observed values)

**A. Theory P0:** fixed memory action and source, full LOS, independently converged source-time sampling, radial integration, k-resolution, physical eta or a well-defined tangent normalization, gauge consistency. Original LW03 radial FAIL is a hard STOP; LW04 alone cannot clear P0.

**B. Distinguishability P1 (synthetic/Asimov only):** forward-predict \`gamma_t\`, galaxy clustering, redshift-space distortions/growth or E_G-type combinations on strictly shared linear scales and survey windows. Explicitly orthogonalize memory template against cosmological+nuisance and controlled instantaneous gravity templates. Choose a single **primary** statistic, held-out redshift/multipole checks, null controls and a physically grounded stop threshold before the real residuals are inspected.

**C. Data P2:** only after P0 and P1 pass, reproduce the standard survey baseline and evaluate the predeclared test with appropriate covariance, trials control, systematic errors, and independently instrumented confirmation.

## Critical safeguards

- No claimed "memory detection" from a nonzero Weyl transfer, from a best-fit change in \(S_8\), from one favorable data bin, or from a decrease in \(\chi^2\) absent nuisance and model-penalty control.
- A strong null bound on a model is not automatically a Nature-level result; novelty depends on broad physical significance, robustness, and comparison to relevant alternatives.
- Source-operator convergence and full causal memory theory are distinct concepts. Keep the archived LW01 theory-side PASS, LW03 FAIL and H4/Z21 uncertified unchanged.
- No real data vector values were evaluated to write this design; URL/content availability has been reviewed at the dataset description level only.
