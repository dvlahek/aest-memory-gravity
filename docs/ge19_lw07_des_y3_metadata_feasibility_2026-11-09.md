# GE19 LW07 — DES Y3 lens-bin feasibility prior to any observed-data fit

**Date:** 2026-11-09. **Status:** archived *published photo-z selection metadata geometry* executed with original uploaded LW02 background; **official DES true calibrated n(z) FITS NOT YET EXAMINED**. No observed shear, no covariance, no CLASS solver, no DES/ACT likelihood.

## Preregistration and source evidence

- Frozen metadata predata before calculations: `ge19/lw07_des_y3_lens_window_predata_20261109.json`, commit `21ab3605e4edfcc1192e96b050451723e8dea227`, Git blob `d455ba3db31ea02ba02511735be4bec34cc7e040`.
- Canonical local Python reexecution: `ge19/lw07_des_y3_lens_window_audit_20261109.py`, commit `6e0cfa38bb876eea79a6bb23c77b7ccac380b3e8`. It checks the predata Git blob, the original LW02 SHA and all 11 published photo-z bins. New CLASS calls: **zero**.
- Read-only independent archive output `ge19_lw07_des_y3_photoz_nominal_window_audit_20261109.json`, SHA256 `af2fa3b8ae874243327f2ee23717e7eeceb515afea374145e98d1989d31263b3`. This is an independent, small-form equivalent calculation against the supplied LW02 JSON, not a claim that canonical WSL runner executed. Frozen LW02 JSON SHA256 `1aec3ddcbe84e473dbb5edb5640cf923ac1db4d9fb1fe37ab32424bd4d05f086`.
- DES Y3 photo-z selection edges verified in original [DES Y3 MagLim galaxy galaxy lensing paper](https://www.darkenergysurvey.org/wp-content/uploads/2021/05/desy3_maglim2x2pt.pdf) and [DES Y3 harmonic-space 2x2pt analysis](https://doi.org/10.1093/mnras/stae2654). **These are PHOTO-z selection cuts, NOT strict supports of calibrated true galaxy n(z).**
- Official DES Y3 FITS directory (metadata kernel source, not yet inspected): https://desdr-server.ncsa.illinois.edu/despublic/y3a2_files/datavectors/

## Calculation: nominal photo-z bin fully within LW01 k,z envelope

Original native eight z nodes span `0.2476197546610166..1.3852368768513288`, with chi from `1035.7818424035233..4261.814874721582 Mpc`. Original 0.03≤k_h≤0.20 h/Mpc and h=0.673324639084866. For a nominal photo-z bin [z_lo,z_hi], use *linear interpolation of original LW02 z–chi anchors* (no extrapolation). If bin endpoints are inside the native z envelope, the **necessary** fully common integer multipole interval is

```
ell_min = ceil(0.03 * h * chi(z_hi) - 0.5)
ell_max = floor(0.20 * h * chi(z_lo) - 0.5)
```

The values below are geometric-only: no comparison with DES n(z), sky data, angular bandpower windows or gauge-corrected galaxy bias.

| Sample | Lens photo-z selection bin | Nominal full-bin ell interval | Status |
|---|---|---|---|
| MagLim 1 | 0.20–0.40 | none | lower z below original native envelope |
| MagLim 2 | 0.40–0.55 | 43–215 | only nominal geometry |
| MagLim 3 | 0.55–0.70 | 52–284 | only nominal geometry |
| MagLim 4 | 0.70–0.85 | 61–346 | only nominal geometry |
| MagLim 5 | 0.85–0.95 | 66–404 | only nominal geometry |
| MagLim 6 | 0.95–1.05 | 71–440 | only nominal geometry |
| redMaGiC 1 | 0.15–0.35 | none | lower z below original native envelope |
| redMaGiC 2 | 0.35–0.50 | 39–190 | only nominal geometry |
| redMaGiC 3 | 0.50–0.65 | 49–261 | only nominal geometry |
| redMaGiC 4 | 0.65–0.80 | 58–326 | only nominal geometry |
| redMaGiC 5 | 0.80–0.90 | 63–386 | only nominal geometry |

**Correct qualification:** 9 of 11 published *nominal photo-z selection bins* have at least one finite ell interval not crossing the original k,z envelope. This does not imply 9 actual DES bins can be fitted; actual true n(z) extends beyond their photo-z selection edges. Also, bin 5/6 MagLim were not in the original fiducial four-bin MagLim cosmology combination; do not treat all six as equal fiducial science cases.

## Required physics and statistical forward model

The DES Y3 measured tangential shear is **real-space** gamma_t(theta), a Bessel J2 transform of C_ell^{gκ} over a broad ell range. A nominal finite interval like 52–284 is **not** a strict angular bandpass for any observed gamma_t(theta), and it would be invalid to set unknown C_ell values outside it to zero. A valid harmonic-space bandpower analysis requires real pseudo-Cl mode coupling / window functions, explicit leakage budget and released bandpowers/covariance; the published DES Y3 harmonic-space analysis uses pseudo-Cl and is a useful methodology reference, but public availability of complete matching bandpower windows was not verified here.

Additionally, the theoretical LW06 P_{d_m W} is in the original Newtonian gauge, and is not yet a covariant observed galaxy-position–shear prediction. A real forward model must include galaxy selection/bias, gauge-convention mapping, source n(z), magnification and intrinsic-alignment effects as needed, physical eta calibration, redshift integration and the survey's angular window.

**Stop classification:** `GE19_LW07_NOMINAL_DESY3_PHOTOZ_GEOMETRIC_FEASIBILITY_ONLY_OBSERVATIONAL_FORWARD_MODEL_BLOCKED`. Do not inspect observed DES shear residuals to select a favorable angular bin.

## Next authorized data task: true n(z) metadata only (LW07b)

Predata was locked **before reading any FITS NZ_LENS kernel**, with a source-name correction when the official directory showed a different redMaGiC filename from the third-party CosmoSIS mirror. Original predata `ge19/lw07b_des_y3_nz_only_predata_20261109.json` was preserved, corrected pre-execution protocol `ge19/lw07b_des_y3_nz_only_predata_officialname_20261109.json`, commit `81ac521de2659e5ddac809ef4f05ecef2906f953`; executable `ge19/lw07b_des_y3_nz_only_audit_20261109.py`, commit `8e0538294e66b15a904bb7e189a0d5b1de1646fa`.

Official DES data files are ~27–28 MB each:
- `2pt_NG_final_2ptunblind_02_26_21_wnz_maglim_covupdate.fits` (MagLim);
- `2pt_NG_final_2ptunblind_02_24_21_wnz_redmagic_covupdate.fits` (redMaGiC).

The script reads **only** `NZ_LENS` calibrated redshift-kernel extension via astropy, neither measured correlation functions nor covariance. It reports n(z) mass fraction inside the original k,z envelope and each predeclared ell=100/150/200/300, with original parent and source SHA. The 99% threshold is an *informational* completeness flag, not a detection, fitted-p value or scientific bound on the missing shear contribution. Even if all n(z) fractions look high, gamma_t and finite physical eta remain blocked.

Official release URL: https://desdr-server.ncsa.illinois.edu/despublic/y3a2_files/datavectors/

### Safe local execution — no CLASS, no GitHub Actions

```bash
set +e
cd ~/aest-memory-gravity
git pull --ff-only
source .venv/bin/activate

mkdir -p results/des_y3_metadata
BASE="https://desdr-server.ncsa.illinois.edu/despublic/y3a2_files/datavectors"
curl -fL --retry 2 -o results/des_y3_metadata/2pt_NG_final_2ptunblind_02_26_21_wnz_maglim_covupdate.fits "$BASE/2pt_NG_final_2ptunblind_02_26_21_wnz_maglim_covupdate.fits"
curl -fL --retry 2 -o results/des_y3_metadata/2pt_NG_final_2ptunblind_02_24_21_wnz_redmagic_covupdate.fits "$BASE/2pt_NG_final_2ptunblind_02_24_21_wnz_redmagic_covupdate.fits"

python3 -m pip install astropy
python3 -u -m ge19.lw07b_des_y3_nz_only_audit_20261109 --self-test

set -o pipefail
python3 -u -m ge19.lw07b_des_y3_nz_only_audit_20261109 \
  --maglim-fits results/des_y3_metadata/2pt_NG_final_2ptunblind_02_26_21_wnz_maglim_covupdate.fits \
  --redmagic-fits results/des_y3_metadata/2pt_NG_final_2ptunblind_02_24_21_wnz_redmagic_covupdate.fits \
  2>&1 | tee results/ge19_lw07b_des_y3_nz_only_audit_20261109.log
echo "EXIT=${PIPESTATUS[0]}"
```

Expected JSON `results/ge19_lw07b_des_y3_nz_only_audit_20261109.json` is small; **only that JSON and the log** should be shared, not the two 27-MB DES FITS containers.
