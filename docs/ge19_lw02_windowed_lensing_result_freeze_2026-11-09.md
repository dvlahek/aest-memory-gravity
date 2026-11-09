# GE19 LW02 — frozen window-restricted Weyl-lensing result and post-run quadrature audit

**Date:** 2026-11-09. **Branch:** `physics-first-gravitational-elasticity`. **Method:** original preregistered LW02, plus independent *read-only, post-run* integration-sensitivity audit. These are different evidence tiers.

## Evidence and provenance

User's local files (not automatically committed):
- `results/ge19_lw02_windowed_lensing_20261109.json`: SHA256 `1aec3ddcbe84e473dbb5edb5640cf923ac1db4d9fb1fe37ab32424bd4d05f086`;
- `results/ge19_lw02_windowed_lensing_20261109.log`: SHA256 `4be32bfe95346f02b2ae828294936e849cd3e37d455cd8709872e0960765acc0`;
- frozen parent LW01 JSON SHA256 `ae49cb0d1e63d82080c092ca938beec4608afe2a0e30650b7d47b0513512014b`, parent NPZ SHA256 `56172ff827d5314cbe066deaeec520f2062b4e4a646de7cb9fe509ae03c9dac9`;
- original CLASS HEAD `e85808324f51fc694d12e3ed7439552a3c3f9540`.

The predata was locked at `ge19/lw02_windowed_lensing_predata_20261109.json` before execution. Frozen primary: original CLASS background for source plane `z_s=2` (`chi_s=5313.976587436474 Mpc`); Born+Limber only; native LW01 `W=(phi+psi)/2`, `dW/deta`; fixed `ell=[100,150,200,300,500]`; original 0.03–0.2 h/Mpc and 0.2–1.5 z parent window; trapezoid integration on accessible native z nodes. **No observed sky data, no finite physical eta and no H4 nonlinear certification**.

## Frozen LW02 primary result: COMPLETED, not full physical lensing

Local tool produced classification `GE19_LW02_WINDOW_RESTRICTED_THEORY_ONLY_LENSING_RESPONSE_OBSERVATIONAL_OPEN`. This means a windowed model projection was computed, **not** a converged line-of-sight prediction.

| ell | native z nodes | window C_ell^kappa-kappa | d(window C_ell)/deta | (dC/deta)/C |
|---:|---:|---:|---:|---:|
| 100 | 8 | 1.730970012069732e-08 | -1.3149081636067586e-10 | -0.0075963659360829385 |
| 150 | 7 | 1.0436997819256042e-08 | -2.036267890683284e-10 | -0.019510092135177154 |
| 200 | 6 | 3.8119963549415035e-09 | -1.0196357907761596e-11 | -0.0026748078849928654 |
| 300 | 5 | 1.3163483175595075e-09 | -2.166623838062065e-12 | -0.0016459350531772298 |
| 500 | 2 | N/A | N/A | N/A — preregistered insufficient support |

Each ell has a *different* actually supported redshift window because k=(ell+0.5)/chi must remain in [0.03,0.2] h/Mpc. In fact the native z range 0.2476197547–1.3852368769 already excludes both nominal window endpoints, and there are no edge boundary corrections to the truncated integration. Relative log-vs-linear **k** interpolation discrepancies for the derivative divided by its absolute integral are 7.52e-05 (ell100), 1.66e-06 (150), 1.94e-05 (200), 1.34e-04 (300). These do *not* assess **z** quadrature convergence.

## Independent source-array reproduction and post-run z-sampling warning

Independently opened the original parent NPZ, extracted locked k, redshift, W0, signed dW/deta arrays, and reproduced the exact CLASS geometry and original trapezoidal ratios in the JSON at machine precision. For an *additional post-run sensitivity diagnostic only*, evaluated the same sparse sampled integrands using Simpson, left endpoint rectangle and right endpoint rectangle quadrature. No solver, parameter, source, CLASS or frozen output/gate was changed.

| ell | preregistered trapezoid ratio | post-run Simpson ratio | post-run left-endpoint ratio | post-run right-endpoint ratio |
|---:|---:|---:|---:|---:|
| 100 | -0.007596365936 | +0.000017961035 | -0.014737442223 | +0.000526401875 |
| 150 | -0.019510092135 | -0.013916420921 | -0.032053643475 | +0.002911612009 |
| 200 | -0.002674807885 | +0.000390519836 | -0.009915520525 | +0.004674130842 |
| 300 | -0.001645935053 | +0.001349805708 | -0.009034694655 | +0.005509717350 |

**CRITICAL INTERPRETATION:** these are sensitivity checks on only 5–8 strongly nonuniform redshift samples, not independently converged solutions. Simpson's rule on irregularly spaced nodes may exhibit unhelpful endpoint weights, so its sign is **not** necessarily more accurate than the original trapezoidal sign. Nevertheless opposite signs from different discretizations are direct evidence that the physical sign and size of the projected lensing response are **not yet numerically certified**. The pre-registered negative trapezoid result remains archived unchanged. Avoid stating gravitational memory generally suppresses weak lensing; do not compare these partial ratios as a physical multipole trend when the z support differs.

## Correct scientific status and next gate

1. `LW01_NATIVE_SIGNED_WEYL_TANGENT_NUMERICAL_PASS=true` under its original narrow conditions.
2. `LW02_WINDOWED_BORN_LIMBER_FORMULA_EVALUATED=true`, `LW02_LOS_QUADRATURE_CONVERGED=false`, `LW02_PHYSICAL_LENSING_SIGN_CERTIFIED=false`.
3. `full_lensing_spectrum_certified=false`, `observational_detection=false`, `Z21_certified=false`, `full_H4_Ward_certified=false`, historical v068 FAIL unchanged.

The scientifically justified route is **one explicitly scoped full line-of-sight geometry-and-sampling extension of the SAME frozen linear Weyl tangent**, with fixed physical parameters and a source-redshift/redshift integration convergence criterion defined in advance. Dense true CLASS transfer-redshift sampling (or separately validated interpolation operator) and sufficient k support are prerequisites for a physically interpretable signed lensing prediction; k-only interpolation tests cannot replace this. If the native z sampling cannot be densified/validated without a larger computational campaign, stop with the publishable *qualified theory-only transfer result* LW01, not a lensing detection. Observations must not be used to tune physics or loosen gates.

## Claim language

Supported: “The frozen linear AeST/positive-Drude memory tangent yields a numerically reproducible nonzero signed native Weyl transfer response; a window-restricted Born+Limber projection can be evaluated and exhibits substantial sensitivity to sparse radial quadrature.”

Not supported: “Gravitational memory suppresses the physical lensing spectrum,” “`eta=1` produces -0.76% or -1.95% observed shear,” “DES Y3 detection,” “full observable prediction,” or “a nonlinear gravitational-memory signature is certified.”
