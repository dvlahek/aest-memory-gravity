# GE19 LW22 — DES Y3 geometric lensing efficiency on original AeST background

**Date: 2026-11-10. Status: executable committed; real LW22 WSL run pending. Not an observed memory signal.**

## Frozen LW21B result

The original researcher WSL file \`results/ge19_lw21b_signed_source_geometry_sensitivity_20261110_r1.json\` (13,613 bytes; SHA256 \`0223b698b13b1a36736274d6582889d66f7cf500ffe0b13eed40612fa4272de8\`) is archived byte-identically at GitHub commit \`eb0586249d125ac3e08c2eb01dc17ea06a368b97\`, with exact readback. The original user WSL log has SHA256 \`a7ab3200d05048f64830da41713c76b34243066ab82efb4a363c6a0bee61dbb5\`; its contents were inspected locally, but a GitHub byte-identical log archive was **not** established.

Original LW21 had correctly failed its hard predeclared signedness threshold of 0.0001 for source bin 1. LW21B is a separate post-failure sensitivity calculation; it does not change that FAIL. The original signed source bin-1 area ratio was 0.00041019367457069883; its signed/positive event change was 0.0003822400401120203, below rigorous upper bound 0.00041036200246839555. That absolute change is 0.038224 percentage points, or about 1.35% relative to source-bin-1's original 0.02829978 full pair event. It is **not** a bound on physical lensing prediction errors.

For the original DES Y3 MagLim lens bin 4, actual signed source-behind redshift event integrals (source bins 1 through 4) are 0.028299783022306523, 0.10841635008756553, 0.44147766799611754 and 0.734326893753908. At ell 200, the fraction of these redshift-ordering events within the native lens k,z domain is respectively 0.8627216066542202, 0.945650872154077, 0.9853048203971891 and 0.9911325800404506. Source bins 2–4 are fully nonnegative. **Primary source bin 4** and **secondary geometry control source bin 3** are chosen after viewing source n(z) geometry, but without inspecting new observed shear residuals. The original ell 100,150,200 candidates and ell300 exclusion control remain.

## LW22: an actual physical geometric lens kernel

Redshift ordering is not lensing efficiency. The source efficiency for a given lens redshift is

\[
g_s(z_L)=\frac{\int_{z_L}^{\infty} dz_S\,n_s(z_S)
  \left(1-\chi(z_L)/\chi(z_S)\right)}
 {\int dz_S\, n_s(z_S)}.
\]

The comoving distance \(\chi(z)\) must come from **the frozen original patched AeST CLASS background**, not a substituted guessed ΛCDM background. The one CLASS run requested here is **background only**, memory eta zero, unchanged v063 frozen cosmological parameters, no CLASS perturbation output, no new k/z solver convergence campaigns, and no observed DES shear or covariance.

The program \`ge19/lw22_aest_background_source_efficiency_20261110.py\` (commit \`fd14bd1e1ce9843136519e8d34193313aedcc432\`) uses original SHA-locked DES NZ_LENS and NZ_SOURCE, the actual LW21B WSL file, and original LW02 signed-theory geometry file SHA256 \`1aec3ddcbe84e473dbb5edb5640cf923ac1db4d9fb1fe37ab32424bd4d05f086\`. It requires official patched CLASS checkout HEAD \`e85808324f51fc694d12e3ed7439552a3c3f9540\` and compares full background chi at the eight LW02 original reference points (relative difference <=1e-4). The geometric integral is computed per source-bin and every original MagLim lens z node with Gauss 8 and 16 and refuses a max absolute quadrature mismatch above 1e-5. It records signed source response efficiency as well as a **diagnostic**, not replacement, positive-part source response, with the same total-variation bound. Output is a JSON summary plus NPZ kernel. Full lensing signal support, source response systematics and physical eta all remain open.

The formula and input locks are in \`ge19/lw22_des_y3_source_lensing_efficiency_predata_20261110.json\` (commit \`1f141b403376ce227797aae6441be58380894b3f\`). Neither original CLASS background nor DES NZ_SOURCE files are installed in this assistant's local runtime, so canonical LW22 has **NOT** been run; self-test and full source/CLASS runtime checks are pending WSL.

## Exact WSL command

~~~bash
cd ~/aest-memory-gravity
git pull --ff-only
source .venv/bin/activate
set +e
set -o pipefail

python3 -u -m ge19.lw22_aest_background_source_efficiency_20261110 --self-test

MAGLIM_FITS=data/des_y3/2pt_NG_final_2ptunblind_02_26_21_wnz_maglim_covupdate.fits

# Set CLASS_ROOT to the existing original patched class_v077 checkout.
if [ -z "$CLASS_ROOT" ]; then
  for CAND in "$HOME/class_v077" "$HOME/aest-memory-gravity/class_v077"; do
    if [ -f "$CAND/class" ]; then CLASS_ROOT="$CAND"; break; fi
  done
fi
if [ -z "$CLASS_ROOT" ]; then
  echo "CLASS_ROOT_MISSING; locate the original patched checkout"
  find "$HOME" -maxdepth 4 -type f -name class -print | head -20
else
  python3 -u -m ge19.lw22_aest_background_source_efficiency_20261110 \
    --class-root "$CLASS_ROOT" --fits "$MAGLIM_FITS" \
    --out results/ge19_lw22_des_y3_source_efficiency_20261110_r1.json \
    2>&1 | tee results/ge19_lw22_r1.log
fi
~~~

If a required original file/checkout is absent, record the exact missing input rather than substituting a different physical model. LW22 creates no observational likelihood, nuisance-marginal Asimov information, delta-Weyl evidence, or detected memory. Original LW05 full cosmic shear LOS BLOCK, LW08 antisymmetric matter-Weyl response unresolved, H4/Z21 uncertified and full 3+1 action-to-CLASS fluid closure remain open. **Next major physics gate:** one source-to-observer closure giving physical \(\partial_\eta P_{\delta,W}\) with other species and metric constraints, followed by actual gamma_t angular windows and nuisance-marginal forecast.
