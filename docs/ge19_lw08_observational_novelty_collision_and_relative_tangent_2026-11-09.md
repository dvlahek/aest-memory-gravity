# GE19 LW08 — matter–Weyl differential tangent and 2024–2026 observational novelty audit

**Date:** 2026-11-09. **Scientific status:** source-level archive replay **PASS** for arithmetic/parent integrity; **differential matter–Weyl physical signature UNRESOLVED**; **NO observed memory detection or licensed DES likelihood**.

## Why this changes the Nature Astronomy strategy

Three prior publications materially reduce the novelty of an ordinary DES Weyl-evolution or matter–geometry comparison:

1. **I. Tutusaus, C. Bonvin, N. Grimm**, *Measurement of the Weyl potential evolution from the first three years of Dark Energy Survey data*, Nature Communications **15**, 9295 (2024), DOI [10.1038/s41467-024-53363-6](https://doi.org/10.1038/s41467-024-53363-6). Already reconstructs the bin-specific Weyl evolution parameter **J-hat** using DES Y3 lens galaxy clustering and galaxy–galaxy lensing. Final article quotes ~2.0 and ~2.8 sigma under-LambdaCDM Weyl evolution in the two lowest **MagLim** bins, with J-hat statistical precision ~5–10%. Their four fiducial mean lens redshifts: [0.295, 0.467, 0.626, 0.771]. The original posterior chains and CosmoSIS modified modules are publicly released at [itutusaus/cosmosis_weyl](https://github.com/itutusaus/cosmosis_weyl). The published J-hat reconstruction assumes GR recovery at high reference redshift **z*=10** and uses a parameterization that neglects k dependence in its primary displayed comparisons. Our LW01 only verifies a finite k,z window at z=0.2476–1.3852; **we have neither validated AeST+memory GR recovery at z=10 nor shown scale-independent model mapping**, so do not treat J-hat posteriors as automatically applicable to the current model.
2. **C. Bonvin, N. Grimm, I. Tutusaus**, *A novel test of gravity: Does spacetime geometry track matter density?*, Astronomy & Astrophysics (2026), DOI [10.1051/0004-6361/202659165](https://doi.org/10.1051/0004-6361/202659165) / arXiv [2506.04387](https://arxiv.org/abs/2506.04387). Already formulates a geometry-vs-density growth null test and applies it to data, obtaining no significant violation; reported constraint is an approximately 33% relative-evolution mismatch bound to z~0.5, with forecast stage-IV sensitivity of ~2–4%. This makes an unmodified "density and Weyl do not grow together" test **non-original** as a methodology claim.
3. **B. Rosatello et al.**, *The impact of evolving dark energy on the Weyl potential measured from the Dark Energy Survey Year 3 data* (2026), arXiv [2605.22599](https://arxiv.org/abs/2605.22599). Evolving-dark-energy backgrounds can reduce the previously noted J-hat tension with LambdaCDM to ~1.6–2.2 sigma in that analysis. **A decrease of lensing alone is therefore not a unique memory signature.**

Also, the DES Y3 harmonic-space galaxy clustering + GGL reanalysis already exists: **L. Faga et al.**, *MNRAS* **536**, 1586–1609 (2025), DOI [10.1093/mnras/stae2654](https://doi.org/10.1093/mnras/stae2654). It models galaxy bias, intrinsic alignments, magnification and photo-z nuisances and uses pseudo-C_ell bandpower windows \`F_{q ell}\` with E/B coupling. Measurement code [hocamachoc/3x2hs_measurements](https://github.com/hocamachoc/3x2hs_measurements) is public, but we did **not verify a complete released jointly compatible observed bandpower/window/covariance data package** for the exact bin configuration we would need. Standard DES Y3 2-point FITS provides configuration-space gamma_t, not automatically isolated ell windows.

## Source-level LW08 physics

At the **same original 322 native k × 8 native z nodes**, with frozen Newtonian CLASS variables \`D=d_m\`, \`W=(phi+psi)/2\` and primordial 3D factor \`P_R(k)\`, separate the **symmetric** cross response

\[
S=P_{\mathcal R}^{3D}\bigl(T_{D,\eta} W+D T_{W,\eta}\bigr)
\]

from the **antisymmetric** determinant

\[
A=P_{\mathcal R}^{3D}\bigl(D T_{W,\eta}-T_{D,\eta}W\bigr).
\]

The symmetric response is the already LW06-certified additive \`d(P_DW)/deta\`. The antisymmetric response is sensitive to *differences* in the fractional matter and Weyl source-level eta tangents when those local fractions are defined. **Neither A nor A/S is a DES J-hat or a gauge-invariant observational null statistic**; the whole-window L2 quotient avoids division by transfer zeros but still depends on the chosen native window and gauge/source normalization.

**Data ordering and reproducibility:** Prior LW06 exploratory diagnostics already showed near-alignment *before* LW08: the LW08 predata \`ge19/lw08_density_weyl_relative_tangent_predata_20261109.json\`, commit \`91bdb130605e1fb3cfdbf62b9a8f96ca9b953f7d\`, explicitly flags this and cannot be treated as an independent discovery. Canonical WSL strict-source script: \`ge19/lw08_density_weyl_relative_tangent_20261109.py\`, commit \`07e9d4de17487661475312df7658eb2832f52181\`. Actual read-only independent calculation was completed in the analysis container from SHA-locked original LW01 and LW06 archived arrays, **not from a new CLASS run**, results \`results/ge19_lw08_density_weyl_relative_tangent_20261109_archive_replay.json\`, Git commit \`ea0eb59bbcb22616397b156b83bf0154c85a8cce\`. The independently generated source script is also a downloadable conversation artifact, but it is not automatically equivalent to the canonical Git SHA checking runner in WSL. Original archived LW06 NPZ 205 kB is not committed here; the source data remains on the researcher's local filesystem and in the conversation attachments.

## Numerical result and resolution diagnosis

- Sixteen source fields (\`d_m,W\` and signed tangents for four original numeric amplifications) are finite on **2,576** common original source nodes. Exact native product-rule recomputation relative L2 difference \`1.253865292499393e-16\`. Archived LW06 symmetric \`dP_DW\` reconstructed exactly (relative L2 0). Four basic data-integrity gates PASS.
- \`||mean(A)||2 / ||mean(S)||2 = 3.362980221740157e-05\` (dimensionless, **not physical eta, not observational percent change**).
- Euclidean cosine of original two **mean** additive contributions to \`S\`: \`0.9999999980960939\`.
- The four original numeric lambda-specific \`||A_lambda||2 / ||S_lambda||2\` values are \`[8.8148367e-06,1.6517684e-05,4.0119967e-05,9.7632606e-05]\` for lambda \`[10,5,2.5,1.25]\`.
- **Key numerical warning:** \`||A_lambda - mean(A)||2/||mean(A)||2 = [1.03683,0.74112,0.77064,1.98602]\`. This is **74%–199% disagreement**, even though the original \`S\` is stable to roughly \`0.02%–0.03%\` and Weyl/matter native source-level parents separately PASS. The anti response is a **difference of nearly aligned contributions** and is **NOT numerically resolved** as its own physical effect. These values are descriptive, not a pre-existing certification cutoff.
- \`A/S\` by native z ranges from \`2.7508e-05\` to \`1.6260e-04\`, but these are diagnostic means of an unstable small difference; do not claim a measured growing-in-z effect.

**This is a scientifically useful negative/uncertainty result.** Our present simulation strongly supports a reproducible shared amplitude/shape perturbation of matter and Weyl but not a robust, distinct "geometry remembers differently than matter" signature. Even if A were converged, a generic arbitrary instantaneous \`mu(k,z)\` can mimic one causal history, so a true memory discovery demands a more restrictive, falsifiable multi-history or multi-probe discriminant.

## Which observational path is now rational?

**Do not fit DES residuals yet**. Our LW07b data-metadata result identifies redMaGiC bins 4 and 5 as having >99.9% *n(z)-mass* support at the original four ell values, but this is not shear-power completeness and the published J-hat fiducial data use the first four **MagLim** bins, not the two redMaGiC bins. Re-using those J-hat four points as a fit to our selected redMaGiC bins would conflate different selections.

Two possible bounded scientific next questions, in order:

**P0—action/gauge/observable.** Verify a self-consistent galaxy-tracer overdensity/velocity/Weyl and physical eta response, including gauge and sign dictionaries and the model at \`z*=10\` if adapting published J-hat, *before* making any survey claim. The unresolved LW03 radial integral and LW05 full LOS remain distinct STOP gates for cosmic shear.

**P1—distinctive causal history, not another density–geometry null test.** Construct a concrete physics-first two-history counterexample in the positive Drude linear constitutive bath: two past strain histories \`X_1(t),X_2(t)\` that agree now, but exhibit different retarded memory \`B_1(t)\ne B_2(t)\`; then prove whether the **coupled Einstein+AeST observer** maps that difference into a gauge-invariant quantity with accessible independent cosmological histories. Such a constitutive demonstration is not by itself a detectable astronomical signature. Compare with explicitly specified restricted Markovian instantaneous competitors; a fully free \`mu(k,z)\` remains observationally non-identifiable from one history.

**P2—real data only if P0 and P1 authorize.** Build the actual observed pseudo-C_ell bandpower forward matrix or a full real-space gamma_t Hankel response with complete k/z support, source n(z), bias/IA/magnification, covariances and trial control. Run an Asimov/nuisance degeneracy test before real DES/ACT residuals.

### Journal stop/go

- A real *Nature Astronomy/Physics*-level case would require a truly new observational signature or a strong, broadly consequential bound **and** independent physical model checks, not merely nonzero \`dW/deta\` or selecting redMaGiC 4/5.
- Current **LW08 PASS is an algebraic replay, not evidence of differential metric response**.
- Remains: \`LW01 PASS\`, \`LW03 radial quadrature FAIL\`, \`LW04 temporal source-time PASS\`, \`LW05 cosmic shear full LOS BLOCK\`, \`LW06 signed native matter–Weyl cross PASS\`, \`LW07b official calibrated DES n(z) read PASS with actual shear BLOCK\`, \`LW08 differential source response UNRESOLVED\`, \`H4/Z21 uncertified\`.
