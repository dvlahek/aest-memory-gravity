# GE19 LW22 — actual WSL DES Y3 source-efficiency result and next physics gate

**Date:** 2026-11-10. **Evidence:** user-supplied original WSL log, JSON and NPZ, independently read and cross-checked in the analysis runtime. **Classification:** `GE19_LW22_AEST_BACKGROUND_SOURCE_EFFICIENCY_GEOMETRY_PASS_FULL_GGL_PHYSICAL_FORWARD_OPEN`. This note is a result audit and scope freeze, **not** a detection claim. It does not replace or regenerate the original researcher artifacts.

## 1. Original local artifact provenance (not claimed GitHub-byte-archived)

- `results/ge19_lw22_des_y3_source_efficiency_20261110_r1.json`: SHA-256 `e4aea4b40d15b163c14ebe2558d8f94be2791005984285b000674151b8d66ea5` (7,667 bytes).
- `results/ge19_lw22_des_y3_source_efficiency_20261110_r1.npz`: SHA-256 `9803d2e322a4bad33f99cb0acf4df58c1c8621a4e3c77505586ff50d0da740cf`. The actual independent NPZ digest is identical to the NPZ digest recorded in the submitted JSON.
- `results/ge19_lw22_r1.log`: SHA-256 `c12d67c841a85ba1c3f5aacbb6655e330069e3a12971e01777cca918f05f3e10` (809 bytes).
- Original LW02 input: `1aec3ddcbe84e473dbb5edb5640cf923ac1db4d9fb1fe37ab32424bd4d05f086` verified equal to freeze and WSL-reported actual SHA. LW02 background comparison max relative difference `0.0`.
- Original LW21B input: SHA-256 `0223b698b13b1a36736274d6582889d66f7cf500ffe0b13eed40612fa4272de8`.
- DES MagLim FITS: SHA-256 `83efa43f6609ff07248b9c4e411b9ab386ec569cba402364fb21edff456e8b76`.
- Original patched CLASS HEAD: `e85808324f51fc694d12e3ed7439552a3c3f9540`; frozen `eta=0` background-only computation, 40,000 background redshift nodes.

The earlier failed LW22 attempt was due to a truncated SHA-256 literal in the first LW22 Python runner, not demonstrated physics. Erratum fixed in commit `63b0e151128e7fdb2adc19d3e764f3a7eef57dd0`; original failed run remains part of provenance.

## 2. Measured computation (geometric efficiencies, not observed shear)

The WSL output gives `lens_weighted_full_source_efficiency` for frozen **MagLim foreground bin 4** (source bins ordered 1–4):

| source bin | full lens-weighted efficiency | max Gauss-8 vs Gauss-16 discrepancy | at ell=100 fraction in native z-range | ell=150 | ell=200 | ell=300 control |
|---|---:|---:|---:|---:|---:|---:|
| 1 | 0.011215874944776624 | 6.450650902323218e-9 | 0.8965215159065747 | 0.8895091316719234 | 0.8573814211052193 | 0.815317276312144 |
| 2 | 0.023589876285910125 | 1.5252307750124316e-9 | 0.9297765797764538 | 0.9222849067552475 | 0.8807917182436612 | 0.8089068005864879 |
| 3 | 0.056512701041848266 | 7.914785910001498e-10 | 0.9651975639200636 | 0.9605888176621128 | 0.9306412681713826 | 0.8498808219428415 |
| 4 | 0.15070638368625014 | 1.4937414499760493e-9 | 0.986360856089048 | 0.9844611431185568 | 0.9716028678754011 | 0.9300445967350106 |

Primary frozen pair remains **MagLim4 × Source4**; Source3 is the geometry control. Full efficiency Source4/Source3 = ~2.667. This is only a kernel-weight ratio, not an observed signal, significance, best-fit parameter, or forecast.

NPZ independent structural audit: lens-z and lens-chi arrays each 159 nodes; source-z 300 nodes; 8 source-efficiency arrays each 159 nodes; no nonfinite values in source functions; signed source kernels nonnegative and decreasing on the saved lens grid. Source4 positive-part diagnostic equals original signed source function exactly; source1 signedness discrepancy max `0.00020303841381788534`, under its total-variation bound `0.00041036200246839555`. The previous LW21 hard-fail signedness threshold for Source1 is not revised.

**Critical mathematical scope:** the percentages of source efficiency in the 'native interval' are not complete true GGL signal fractions. Weighting by `P_deltaW(k,z)`, tracer bias, nonlinear contributions, magnification, IA, and observed angular windows can change support substantially. The signed source `n(z)` is a calibrated response estimate rather than automatically a literal probability distribution.

## 3. Real physical and observational stop gates

The original observable chain is

`NL0B/GE05 physical retarded bath -> full Einstein–AeST constrained state and metric -> physically normalized dP_(delta W)/d eta -> GGL C_ell or gamma_t window -> nuisance-marginal DES likelihood`.

What this LW22 result **does**: certifies the static, background-only `chi(z)`-weighted DES source efficiency for the frozen model. No perturbative CLASS calculation, observed tangential shear/covariance, or full GGL angular prediction was performed.

What remains unresolved, already identified in LW08/LW10/LW17/LW20/LW22:
1. **Physics-first**: demonstrate the correct action-to-CLASS Einstein constraint, scalar/aether/bath and ordinary-species stress/gauge dictionary. A frozen externally forced `E_A` row and numerically amplified lambda are not automatically a physical eta derivative. Get the physically normalized `partial_eta P_{delta W}(k,z)` including the full constrained response; certify its normalization/sign and whether a bias-marginal distinct memory shape exists.
2. **Projection and support**: evaluate the actual `n_L(z)g_S(z)`-weighted foreground LOS projection over the k/z support required by DES binned `gamma_t(theta)` windows, without silent padding; original LW03 radial convergence FAIL and LW05 cosmic-shear LOS BLOCK stay on record. Avoid reopening full high-z cosmic-shear campaigns just for GGL.
3. **Observational specificity**: use real released gamma_t, angular bins, scale cuts, covariance and galaxy bias/IA/magnification/shear-photoz controls, ideally galaxy clustering to constrain bias. Before inspecting shear residuals, compute an Asimov/noise+nuisance marginalized discrimination test. Published DES Weyl and geometry-vs-matter null tests already cover generic non-memory-only deviations.
4. **Memory uniqueness**: distinguish at least one physically realizable constrained past-history pair from explicitly bounded instantaneous rivals; the existence of a retarded material constitutive kernel alone does not guarantee an observable non-Markovian signature.

**Recommended next bounded task (LW23): one physical source-to-observer closure audit, not another geometry test.** Specify the full physical eta source and its projection into `delta_m`, `W=(Phi+Psi)/2` and `P_{delta W}` in the original CLASS gauge, with all normalizations and stress-energy/constraint terms. Produce explicit PASS or BLOCK with a derivation and exact source anchors; do not generate arbitrary new pseudo-observed data or claim `sigma_eta` from LW22. If that bridge remains underdetermined, stop and report exactly which field equation or dictionary row is missing.

**Status label:** `LW22_GEOMETRY_PASS_LW23_PHYSICAL_BRIDGE_OPEN_NO_OBSERVATION`.
