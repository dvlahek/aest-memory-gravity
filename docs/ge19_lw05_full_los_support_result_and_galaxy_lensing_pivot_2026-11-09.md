# GE19 LW05 — frozen finite-domain LOS audit and galaxy-lensing pivot

**Date:** 2026-11-09. **Result:** GE19_LW05_FULL_LOS_DOMAIN_BLOCKED_BY_CERTIFIED_KZ_SUPPORT. This is an analytic, read-only, archived geometry result, NOT a CLASS run, weak-lensing amplitude, or observed detection.

## Evidence / precedence

The LW05 protocol was committed BEFORE this calculation as ge19/lw05_line_of_sight_domain_audit_predata_20261109.json, commit 0dd033d70185e5313cb3db8768894759ef3a0aa5 (Git blob 86081eaa14c781cf4c5eb8586ef0bf4486f9a242). Executable code is ge19/lw05_line_of_sight_domain_audit_20261109.py, commit d7cd5f2def338f82626f01c430de1474901c75a2. The read-only analysis used these original uploaded parents:

- LW01 NPZ SHA256 56172ff827d5314cbe066deaeec520f2062b4e4a646de7cb9fe509ae03c9dac9
- LW02 JSON SHA256 1aec3ddcbe84e473dbb5edb5640cf923ac1db4d9fb1fe37ab32424bd4d05f086
- LW03 JSON SHA256 dcf057b8e51e4863f0c0765c11973de71db01240fce6421a691b3704869ae09d
- LW04 JSON SHA256 6a1dfe9923daf385a9b78d0528eddeefd8442e0a28da9b60626814d30a435ac8

The analysis-container output ge19_lw05_line_of_sight_domain_audit_20261109.json has SHA256 40dd40e7476816dae7f4ff81b32c72d5778ac6c8ca5c308956dd4330ef32a04a. The local audit used equivalent short-form preregistration metadata in an archive-only test because GitHub working-tree access was not available in that isolated container; the canonical GitHub executable includes the full strict preregistration Git-blob lock for WSL reruns. The computed geometric result follows directly from the SHA-verified parent arrays and analytic inequalities, and **does not claim** that the canonical script's Git-blob guard was exercised in the analysis container.

## Geometry

Original source z_s=2, comoving chi_s=5313.976587436474 Mpc, H0=67.3324639084866 km/s/Mpc, h=0.673324639084866. Original window: 322 native k nodes in 0.03..0.20 h/Mpc; 8 native z nodes actually spanning z=0.2476197546610166..1.3852368768513288, with chi=1035.7818424035233..4261.814874721582 Mpc.

For the Limber relation k_h=(ell+0.5)/(h chi), the available continuous domain is the intersection of the original chi interval with [(ell+0.5)/(h*0.20), (ell+0.5)/(h*0.03)] and (0,chi_s). The interval is a **necessary k,z domain condition only**, not proof that interior source interpolation is independently converged.

| ell | Supported chi lower (Mpc) | Supported chi upper (Mpc) | Supported LOS distance | Native z nodes |
|---:|---:|---:|---:|---:|
| 100 | 1035.782 | 4261.815 | 60.7085% | 8 |
| 150 | 1117.589 | 4261.815 | 59.1690% | 7 |
| 200 | 1488.881 | 4261.815 | 52.1819% | 6 |
| 300 | 2231.464 | 4261.815 | 38.2077% | 5 |
| 500 | 3716.632 | 4261.815 | 10.2594% | 2 (below original 4-node rule) |

**Scientific stop:** All five full-LOS domain gates are blocked. These are fractions of *unweighted radial distance*, NOT fractions of lensing power, expected signal, uncertainty or missing contribution. No zero-fill, extrapolation, full cosmic-shear C_ell, DES or ACT likelihood may be represented as scientifically certified by this support. LW01 Weyl native PASS, LW03 radial quadrature FAIL and LW04 source-time sampling PASS all remain unchanged. H4/Z21 remains uncertified.

## A more feasible next observable: narrow lens-galaxy cross-correlation

Under a Limber projected galaxy–shear cross-correlation, the lens galaxy selection function localizes the matter–lensing cross-spectrum to lens redshifts. The physically relevant spectrum is **signed matter–Weyl cross power P_delta,W**, not Weyl autospectrum W squared. Its formal eta derivative contains both d(delta)/deta times W and delta times dW/deta.

The originally archived native adjacent lens slab z=0.6041886577745919..0.772471983328852 corresponds to chi=2292.61485361332..2797.5736202237276 Mpc. Requiring k_h in [0.03,0.20] at every point of this slab gives integer ell **57..308**, from the inequalities ell+0.5 >=0.03*h*chi_high and ell+0.5 <=0.20*h*chi_low. This is a useful mathematical feasibility result, **not yet an independently converged observable**: two native z boundary samples alone cannot establish time-integral convergence.

A real DES galaxy lens sample may have redshift-selection tails outside this slab; do not truncate them posthoc. The DES galaxy–galaxy tangential shear gamma_t(theta) has a broad Bessel/angular-multipole window, so this 57..308 range cannot automatically be equated to safe gamma_t(theta) bins. An actual band-limited angular estimator or a full survey forward model with explicit kernels must be validated. Galaxy bias, intrinsic alignment, physical eta normalization, nonlinear scales and alternative gravity templates remain important.

## Physics-first next action (proposed LW06, not executed)

1. Derive and freeze a consistent signed native matter–Weyl P_delta,W cross-transfer from LW01 native arrays with source normalization, gauge and signs stated.
2. Independently choose a public lens-selection n(z) and angular/bin windows that genuinely fit this k,z window; if not, stop or expand the physically certified domain via a separate preregistered experiment.
3. Use an Asimov forecast and restricted competitor models to test whether a memory shape is distinguishable from S8, galaxy bias, baryon and photometric-redshift nuisances *before* looking at observed survey residuals.

Do not claim Nature-level observations from geometry alone.
