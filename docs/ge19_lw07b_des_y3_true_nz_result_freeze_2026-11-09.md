# GE19 LW07b — official DES Y3 calibrated lens n(z) support audit

**Date:** 2026-11-09. **Executed classification:** \`GE19_LW07B_TRUE_NZ_SUPPORT_MEASURED_OBSERVATION_STILL_BLOCKED\`. This was an *official DES Y3 FITS NZ_LENS-only inspection* in the researcher's local WSL. **No observed shear values, covariance, likelihood, source-plane shear or cosmological fit were analyzed.**

## Unmodified original outputs now on GitHub

- [Original output JSON](../results/ge19_lw07b_des_y3_nz_only_audit_20261109.json), SHA-256 \`176046fd3893b5aa9b0f0e8922dfa6b33743ab07747f9803996272ea4b4cbbe6\`, 16870 bytes, archived commit \`d7386e85598d2d3df2668b1b2c7d5365a1b9db74\`.
- [Original WSL log](../results/ge19_lw07b_des_y3_nz_only_audit_20261109.log), SHA-256 \`0dffc788a5af6d337c70808ac58e90fec8db50bd3ebb2dd90e64f808d2d835a5\`, 1620 bytes, archived commit \`c5ae23120f0d2192fced32cee59e05e14a8121a0\`.
- Original predata \`ge19/lw07b_des_y3_nz_only_predata_20261109.json\` committed before accessing FITS; official NCSA redMaGiC filename correction was also saved **before any NZ_LENS values were read** in \`ge19/lw07b_des_y3_nz_only_predata_officialname_20261109.json\`, commit \`81ac521de2659e5ddac809ef4f05ecef2906f953\`, Git blob \`1566d00f34105497c1f1c13d8e364331d9f60fe0\`.
- Canonical script \`ge19/lw07b_des_y3_nz_only_audit_20261109.py\`, commit \`8e0538294e66b15a904bb7e189a0d5b1de1646fa\`, loads *only the \`NZ_LENS\` FITS extension*, not observed two-point function rows or covariance.
- Original LW02 geometry parent SHA256 \`1aec3ddcbe84e473dbb5edb5640cf923ac1db4d9fb1fe37ab32424bd4d05f086\`, as confirmed by the submitted LW07b JSON.

Official FITS provenance saved inside the output, **not committed as 27–28 MB survey binaries**:
- MagLim \`2pt_NG_final_2ptunblind_02_26_21_wnz_maglim_covupdate.fits\`, SHA256 \`83efa43f6609ff07248b9c4e411b9ab386ec569cba402364fb21edff456e8b76\`, six \`NZ_LENS\` kernels.
- redMaGiC \`2pt_NG_final_2ptunblind_02_24_21_wnz_redmagic_covupdate.fits\`, SHA256 \`a72a8ee02fa72474ad859edab27d946991901e3d9a5bdc95cc9a961b244a32a6\`, five \`NZ_LENS\` kernels.

**Source k,z envelope from LW01/LW02:** \`0.03 ≤ k/(h/Mpc) ≤ 0.20\`; actual original native z \`0.2476197546610166 ≤ z ≤ 1.3852368768513288\`. Original h \`0.673324639084866\`. Each information-only fraction is the integral of *calibrated normalized lens n(z)* within the original k,z support for the given \`ell\`, with Limber \`k_h=(ell+.5)/(h chi(z))\`. Fractions do **not** represent lensing amplitude, galaxy shear covariance, admissible theta bins, or a strict bound on excluded power.

## Complete metadata-only screening summary

| Lens sample/bin | n(z) inside native z | ell=100 | ell=150 | ell=200 | ell=300 |
|---|---:|---:|---:|---:|---:|
| MagLim 1 | 71.4612% | 71.4612% | 61.6934% | 19.1674% | 0.3069% |
| MagLim 2 | 97.7818% | 97.7818% | 96.7558% | 86.6857% | 2.7383% |
| MagLim 3 | 99.5573% | 99.5573% | 99.3852% | 97.8386% | 72.9662% |
| MagLim 4 | 99.6762% | 99.6762% | 99.6308% | 99.2782% | 97.5560% |
| MagLim 5 | 99.5905% | 99.5905% | 99.5558% | 99.3819% | 98.4044% |
| MagLim 6 | 99.0898% | 99.0898% | 99.0070% | 98.6422% | 97.3721% |
| redMaGiC 1 | 66.9471% | 66.9471% | 56.2690% | 3.3179% | 0.0015% |
| redMaGiC 2 | 99.9946% | 99.9946% | 99.9827% | 88.5485% | 0.0069% |
| redMaGiC 3 | 99.9992% | 99.9992% | 99.9988% | 99.9932% | 45.8138% |
| redMaGiC 4 | 99.9998% | 99.9998% | 99.9998% | 99.9997% | **99.9346%** |
| redMaGiC 5 | 100.0000%* | 100.0000%* | 100.0000%* | 99.9997% | **99.9839%** |

*At the released FITS table's numeric precision and for this finite-support mass integration; do not assume the true physical distribution has exactly zero tails. Values are not percentages of the observed g×κ signal.*

The preregistered information-only marker \`fraction >= 0.99\` is achieved by **8/11 lens bins** at ell100, **8/11** at ell150, **5/11** at ell200 and **2/11** at ell300. At all four specific ells simultaneously only **redMaGiC 4 and 5** reach that threshold. Do not modify this 99% threshold or infer it is a physically meaningful lower bound on observable signal completeness.

## Physics interpretation: promising candidates, not a DES fit

**Candidate primary for the next theory-only study:** redMaGiC bin 4 (photo-z selection \`0.65-0.80\`), because its calibrated n(z) lies nearly entirely in the original native k,z support across the four fixed multipoles, and its lens redshift is in the region tested by the previous LW01/LW04 native-source comparisons. **Candidate sensitivity cross-check:** redMaGiC 5 (\`0.80-0.90\`). This selection is based on published lens metadata and theoretical geometry only; it was made *before observing any DES shear residuals*, but **after inspecting n(z) supports** and must be reported as such, not as a fully blind survey selection. The output and figure should show all 11, including failures.

**Do not** claim observational support for gravitational memory yet, because:
1. The true n(z) support fraction weights galaxy *counts*, not the lensing or signed \`P_deltaW\` integrand; a very small n(z) tail could matter disproportionately in the observable without a bound on the integrand.
2. Real DES Y3 galaxy-galaxy lensing is measured in **real-space \`gamma_t(theta)\`**, which mixes a broad range of \`ell\` through a \`J_2\` Bessel transform; the four fixed supported multipoles are NOT four independently admissible DES theta bins. Finite \`ell\` coverage alone is insufficient without validated bandlimited pseudo-Cl windows and leakage bounds or a **full** physically supported \`C_ell\` forward model.
3. The archived \`LW06 P_{d_m W}\` is a mathematical Newtonian-gauge *matter–Weyl* transfer, not a directly observable galaxy position–shear correlation. Need a gauge-consistent galaxy tracer/bias prescription, matter-lensing source convention, source n(z), galaxy magnification / intrinsic alignments where applicable, and a physical-eta normalization.
4. \`LW03\` radial quadrature FAIL remains in force; \`LW04\` source-time-sampling PASS does not close it; \`LW05\` full cosmic-shear LOS support BLOCK remains in force; H4/Z21 not certified. No DES shear or covariance were read in LW07b.

## Bounded stop/go decision toward Nature Astronomy

**LW07b is COMPLETE as a metadata-only source support audit; do not repeat it.** The next step should be primarily analytic / software-forward modeling, not repeated CLASS solves:
- Write the gauge and sign dictionary for the observed galaxy–Weyl cross spectrum, including selection and bias, in the same CLASS perturbation conventions.
- Confirm whether a genuinely band-limited *observable* exists with released DES Y3 g×κ harmonic-space bandpowers, coupling/window matrix and covariance whose leakage outside the supported \`k,z,ell\` domain can be estimated **without inventing unconstrained tails**. If only real-space gamma_t is available, the full Hankel/Bessel forward model is necessary. Don't inspect observed residuals until the model and decision rules are frozen.
- Construct a **synthetic/Asimov** covariance-aware sensitivity / identifiability comparison of the fixed memory template against restricted instantaneous-gravity and nuisance templates. If no genuine separation or no supported angular observable exists, stop the Nature-level observation route rather than declare a detection.

**Frozen classification retained:** \`GE19_LW07B_TRUE_NZ_SUPPORT_MEASURED_OBSERVATION_STILL_BLOCKED\`; \`observational_likelihood_authorized=false\`; \`observational_detection=false\`.
