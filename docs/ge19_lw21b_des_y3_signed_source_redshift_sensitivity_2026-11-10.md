# GE19 LW21B — honest signed DES Y3 source-response sensitivity, no threshold relaxation

**2026-11-10. Status:** one original DES Y3 MagLim FITS input integrity FAIL preserved; new independent signed-source geometry sensitivity executable ready, synthetic mathematics independently checked, real 4-bin source result still to be run.

## Actual researcher WSL log and why it stopped

- Original LW21 synthetic 4/4 PASS, FITS downloaded.
- Fixed LW21 synthetic 6/6 PASS including negative-data controls.
- Actual real FITS NZ_LENS BIN1–BIN6 all had zero negative sample values, total integrals essentially unity, no nonfinite entries.
- First NZ_SOURCE BIN1: **12 negative ordinates**, minimum **-6.771413635413951e-05**, positive integrated area **0.009934036567883761**, negative area **4.0748789630999336e-06**, epsilon \`B/A=0.00041019367457069883\`.
- Frozen original threshold \`1e-4\` was exceeded, so the source-ingestion run legitimately classified \`GE19_LW21_NZ_SIGNEDNESS_SOURCE_REVIEW_REQUIRED_NZ_SOURCE_BIN1\`, \`EXIT=1\`. **No valid LW21 physical source-bin probability output or observation occurred.** The values of source bins 2,3,4 were never printed because the previous program stopped at first offending bin.

Relevant DES Y3 science: Myles et al. 2021, MNRAS 505:4249, section 4.2.4 describes how per-galaxy shear-response weighting can produce an estimated redshift distribution with negative values, addressed by smoothing over galaxy size and signal-to-noise grids. DES Y3 effective shear redshift kernels require calibration/response uncertainty treatment; simply truncating an estimated signed response distribution is not automatically a physical inference prescription. **Do not infer source calibration correctness from this audit.** Authoritative paper: https://academic.oup.com/mnras/article/505/3/4249/6286909 .

## Why LW21B is NOT raising a tolerance

The original \`ge19/lw21_nz_signedness_handling_erratum_20261110.json\` threshold stays **1e-4**, and the original LW21 real-data input-integrity FAIL stays a FAIL. That hard gate intentionally was defined before we saw the first source bin and should not be silently rewritten to obtain a green result.

Instead, new *separate* reproducible sensitivity protocol \`ge19/lw21b_signed_source_sensitivity_predata_20261110.json\` was frozen **after** the first-bad-bin log was already known (so not a blind discovery), commit **5d850f2fe2d32fbf22b04b5711e798db82e73bd1**. Source \`ge19/lw21b_signed_source_geometry_sensitivity_20261110.py\`, commit **07f999aaf5d1af68df588f234720249f6c038358**, reads only original DES \`NZ_LENS\` and \`NZ_SOURCE\` extensions and checks official original LW07b FITS SHA and frozen LW20 WSL SHA. It reports **all four source bins** even if they contain small or sizeable signed estimates, provided their total signed integral is positive and finite.

For each source bin, it calculates redshift-ordering event integral using:
1. The original **signed** source n(z), normalized by its signed total \`A-B\` (where \`A=int max(n,0)\`, \`B=int max(-n,0)\`), **without clipping** the cumulative source response.
2. A separate **diagnostic comparison** using the normalized nonnegative positive part \`max(n,0)/A\`; this is **not** a replacement for the DES source likelihood.

For original nonnegative MagLim lens BIN4, and event \`z_source>z_lens\` (or that event with the frozen native \`ell=100,150,200,300\` lens-redshift domain restriction), the absolute source-representation sensitivity is mathematically bounded by

\[
\left|\mathcal I_{\rm signed}-\mathcal I_{\rm positive}\right|
\leq \mathrm{TV}(\mu_{\rm signed},\mu_{\rm positive})
=\frac{\epsilon}{1-\epsilon},\quad \epsilon=\frac{B}{A}.
\]

For *the one source bin the user supplied*, epsilon=0.00041019367457069883 gives a strict **absolute bound 0.00041036200246839555** on any such normalized \`[0,1]\` event weighting. In percent units of a unit-normalized event, this is **0.0410362 percentage points**, not 0.041% relative error in a weak-lensing observable. It is also NOT a DES photo-z calibration uncertainty or true physical lensing-efficiency accuracy. For the actual pair event, the numerical difference may be smaller; compute it rather than claim it.

The quadrature for the *piecewise-linear FITS n(z)* is exact per knot interval: source survival is piecewise quadratic, lens density piecewise linear, product cubic, 4-node Gauss–Legendre. An independent stand-alone NumPy check recovered synthetic full event 0.5, restricted lens 0.25, signed-vs-positive result within bound and preserved original fail for epsilon>1e-4. No CLASS, no shear, no covariance and no physical eta.

## One WSL run — same downloaded FITS, no extra CLASS

~~~bash
cd ~/aest-memory-gravity
git pull --ff-only
source .venv/bin/activate
set +e
set -o pipefail

python3 -u -m ge19.lw21b_signed_source_geometry_sensitivity_20261110 --self-test

MAGLIM_FITS=data/des_y3/2pt_NG_final_2ptunblind_02_26_21_wnz_maglim_covupdate.fits
test -s "$MAGLIM_FITS" || { echo 'Original FITS not found at expected location'; exit 3; }

python3 -u -m ge19.lw21b_signed_source_geometry_sensitivity_20261110 \
  --fits "$MAGLIM_FITS" \
  --out results/ge19_lw21b_signed_source_geometry_sensitivity_20261110_r1.json \
  2>&1 | tee results/ge19_lw21b_r1.log
~~~

The classification is expected to be \`GE19_LW21B_DES_SIGNED_SOURCE_GEOMETRY_SENSITIVITY_REPORTED_NOT_GGL_FORWARD\`. **This is reporting an input-model sensitivity, not passing the old positivity gate.**

Once four source bins have been documented, the next physics target is the actual frozen-background lens efficiency \`g_s(chi)\` with the source kernel and then the full gauge-consistent *physical* \`dP_deltaW/deta\` from the original coupled Einstein–AeST/CLASS system. No more low-value synthetic Ward campaigns should intervene. The full GGL \`gamma_t\`, covariance and nuisance-marginalized Asimov discrimination are still unavailable; original LW03 radial FAIL, LW05 cosmic-shear LOS BLOCK, LW08 differential Weyl UNRESOLVED and H4/Z21 uncertified remain unchanged.
