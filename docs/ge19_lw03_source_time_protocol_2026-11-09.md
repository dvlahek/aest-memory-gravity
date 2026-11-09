# GE19 LW03 — bounded source-time replay following LW02

**Research state:** LW01 native signed Weyl tangent is numerical PASS, LW02 windowed Born+Limber projection computed but its radial sign is unresolved. This checkpoint does **not** claim full lensing or observational detection.

## Post-LW02 diagnostic (NOT a new physical prediction)

A read-only analysis of the uploaded LW01 NPZ and LW02 JSON re-evaluated the *same, per-ell truncated native-chi integration interval* with separately interpolated native `W` and `dW/deta`, using nested dense quadrature and `scipy.interpolate.PchipInterpolator` along chi. That interpolation adds **no independent perturbation information**. The signed relative derivatives `(dC/deta)/C` were:

| ell | original LW02 5–8 native-node trapezoid | post-run smooth PCHIP sampling |
|--:|--:|--:|
| 100 | -0.0075963659361 | -0.0013858934293 |
| 150 | -0.0195100921352 | -0.0107923683792 |
| 200 | -0.0026748078850 | +0.0007183990777 |
| 300 | -0.0016459350532 | +0.0016353064141 |

Linear-in-chi and cubic-in-chi interpolants show the same sign pattern, though with different magnitudes. These are **post hoc diagnostics, not separately pre-registered or independently converged physical results**. They show that denser integration of a smooth representation need not preserve the sparse-node trapezoidal signs at `ell=200,300`. An interpolated sign is not certified.

## Pre-LW03 execution protocol

Predata committed as `ge19/lw03_source_time_closure_predata_20261109.json` in commit `68719e4ddd2d60a369fa35e20540a6f411492db9`, before any LW03 CLASS execution. Implementation: `ge19/lw03_source_time_closure_20261109.py`.

Scientific question: **Does the native LW01 signed Weyl tangent agree with CLASS's own off-native source-time transfer interpolation on its original eight native redshifts, and does a nested 17/33/65-node chi quadrature stabilize within that interpolation operator?** This specifically probes the source-time vs Fourier-time operator difference already diagnosed under v078.

- Exact original force file SHA256 `55b7b4cfdbe85b63182c883424a464d47cb33a8f5af7ec5e02540fb6df15a6b0`.
- Original pinned CLASS HEAD `e85808324f51fc694d12e3ed7439552a3c3f9540`.
- **Three** original CLASS perturbed-transfer configuration executions: eta=0 baseline, external signed lambda=+2.5 and -2.5. No v039 forcing reconstruction or nine-run amplification sweep. Reuse original R4 native k and fixed frozen model.
- New redshift evaluation uses `Class.get_transfer(z,output_format='class')` at 65 chi points inside the **same per-ell LW02 native source window**; the 17/33/65 grids are nested.
- Source operator at all eight original native z is checked against the LW01 parent baseline and **the same** signed `lambda=2.5` tangent (not the four-lambda mean) on the original 322 k × 8 z mask using additive L2 norms. Preregistered 0.005 maximum L2 error for each; k match 1e-10; geometry 1e-8.
- For each ell the 17→33 derivative integrated difference normalized by 33's absolute signed-derivative integral must be <=0.02; 33→65 <=0.005, with consistent nonzero signed derivative across 17/33/65. Never normalize numerical convergence by a near-zero signed integral.
- Original `ell=500` native support remains insufficient (only two original redshift nodes), irrespective of how many intermediate interpolation samples are generated.
- Save new JSON and NPZ; stop on failure; no H4 sweep, no physics retuning or survey comparison.

**Critical evidence boundary:** `get_transfer(z)` is still an interpolation from the CLASS perturbation source grid, **not independent perturbation integration on a newly refined native time mesh**. If the three-run replay passes, only the original finite-window projection under this selected interpolation operator has converged *as an integral of that operator*. It does **not** establish the correct physical lensing sign or the full line-of-sight lensing spectrum. A genuine physical sign certification would require an independent time-resolution/source-grid and full-support test before observations.

## Local invocation

```bash
cd ~/aest-memory-gravity
git pull --ff-only
source .venv/bin/activate
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
python3 -m py_compile ge19/lw03_source_time_closure_20261109.py
python3 -u -m ge19.lw03_source_time_closure_20261109 --self-test
set -o pipefail
python3 -u -m ge19.lw03_source_time_closure_20261109 --class-root "$PWD/class_v077" 2>&1 | tee results/ge19_lw03_source_time_closure_20261109.log
echo "EXIT=${PIPESTATUS[0]}"
```

Expected `results/ge19_lw03_source_time_closure_20261109.{json,npz}`; if failed, upload log. No Actions.
