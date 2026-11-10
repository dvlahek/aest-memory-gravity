# GE19 LW21 — actual DES Y3 source n(z) geometry, not a shear detection

**10 November 2026. Status:** source-side calculation PROGRAM READY, real DES FITS source arrays not read in this turn. Full galaxy–galaxy lensing (GGL) forward and likelihood OPEN.

## Preserved local evidence

- Actual researcher LW20 WSL 6/6 PASS, original JSON SHA256 ab0b0147b4edf1a12d182628f81476e2d23443e347fe636243d51007eca962a4, archived byte-identical on GitHub commit 61a453b970ab10d9236b3dbfb04d5876045ef767, original log commit ba07e26fd82217ee6476c9f5c5e697f4fc7c1d7e.
- The previously absent LW17 researcher WSL JSON was also recovered from uploaded conversation files and archived byte-identical as results/ge19_lw17_full_reduced_scalar_action_current_20261110_r1.json, commit 071a0907abcbf3f6b512bd50ce93617d8c2801aa: 11/11 analytic gates and 7/7 source anchors PASS. This is an archival correction, not a new physics discovery.
- Original official DES Y3 MagLim FITS release: 2pt_NG_final_2ptunblind_02_26_21_wnz_maglim_covupdate.fits, published at https://desdr-server.ncsa.illinois.edu/despublic/y3a2_files/datavectors/. Frozen LW07b original results include the exact file SHA256. LW21 checks that same SHA rather than accepting a filename alone.
- LW21 protocol ge19/lw21_des_y3_maglim4_source_behind_predata_20261110.json, commit 28e98b9a497869735cee0e740a3f96ce4b3119dc, blob 2b00093ef9621ed19c17ed5599feaa0e58d004d4. Program ge19/lw21_des_y3_maglim4_source_behind_20261110.py, commit a5cb6e0d15b042e265f278e0dcf1208688cfe211. Canonical WSL execution **not performed**. Four small independent NumPy mathematical controls PASS.

## What is new compared with LW20?

LW07b had read genuine NZ_LENS but not NZ_SOURCE, and could report only foreground-lens n(z)-mass support. LW21 reads ONLY NZ_LENS and NZ_SOURCE from the same official MagLim DES Y3 FITS; it never accesses measured GAMMAT, covariance or clustering residuals.

For the original MagLim lens redshift bin 4 and separately for each of the four source bins j, compute normalized redshift-ordering probability

\[
p_j=\int dz_L\,n_{L,4}(z_L)
\int_{z_L}^{\infty}dz_S\,n_{S,j}(z_S).
\]

For each original LW07b native k,z-supported foreground lens interval I_ell (ell 100,150,200 and negative-control ell 300), also compute the integral restricted to I_ell, retaining the missing-tail pair probability explicitly as a difference. This avoids pretending that an n(z)-mass percentage is the percentage of lensing amplitude.

The source distribution is represented piecewise-linearly. Its survival function is piecewise quadratic. Product with linear foreground n(z) is cubic on the union of knots; the code integrates the exact piecewise polynomial with 4-point Gauss–Legendre. Synthetic uniform equal-bin P=1/2, restricted interval P=1/4, source always behind P=1 and source always in front P=0 all check exactly in an independent local replay. This is not a cosmological solver precision campaign.

## Absolute physics stop

A source with z_source greater than z_lens is NOT automatically a strong lensing source. Full efficiency needs the actual original background distance relation chi(z) and geometric weighting (chi_source-chi_lens)/chi_source, as well as physical gauge-consistent P_deltaW, galaxy bias and tracer response, source selection/calibration, intrinsic alignments, magnification, angular windows, scale cuts and covariance. An unweighted redshift-ordering probability is NOT the GGL observable, the Weyl signal or an Asimov forecast. Full 3+1 action-to-CLASS source closure and physical eta also remain open; the LW08 differential matter–Weyl response is unresolved. Do not infer an observed gravity-memory detection or tune after reading residuals.

## WSL: one genuine DES source-geometry read, zero CLASS

~~~bash
cd ~/aest-memory-gravity
git pull --ff-only
source .venv/bin/activate

python3 -u -m ge19.lw21_des_y3_maglim4_source_behind_20261110 --self-test

mkdir -p data/des_y3
MAGLIM_NAME=2pt_NG_final_2ptunblind_02_26_21_wnz_maglim_covupdate.fits
MAGLIM_FITS=data/des_y3/$MAGLIM_NAME

if [ ! -s "$MAGLIM_FITS" ]; then
  curl -fL --retry 2 -o "$MAGLIM_FITS" \
    "https://desdr-server.ncsa.illinois.edu/despublic/y3a2_files/datavectors/$MAGLIM_NAME"
fi

python3 -u -m ge19.lw21_des_y3_maglim4_source_behind_20261110 \
  --fits "$MAGLIM_FITS" \
  --out results/ge19_lw21_des_y3_maglim4_source_behind_20261110_r1.json \
  2>&1 | tee results/ge19_lw21_r1.log
~~~

The FITS can instead be the identical existing file used for LW07b; the original frozen hash is checked. The program refuses to overwrite a previous output. The resulting source-behind probabilities will be useful geometry constraints but MUST NOT be labeled physical GGL efficiency or observational significance.
