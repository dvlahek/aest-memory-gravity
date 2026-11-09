# GE19 LW01 — physical-k forcing-grid implementation failure and one bounded repair

**Date:** 2026-11-09. **Scope:** read-only diagnosis of researcher-uploaded frozen LW01 local run, plus unit-consistency repair to implementation. **Not** a new physics PASS, not a post-hoc change to any numerical/scientific gate, and not a new observational claim.

## Immutable local evidence

- Official CLASS checkout HEAD: `e85808324f51fc694d12e3ed7439552a3c3f9540`.
- Original v077 AeST patch chain built and the patched `classy` imported successfully.
- `GE19_LW01_SIGNED_NATIVE_SYNTHETIC_SELFTEST_PASS`.
- Original frozen Drude forcing: 22,032 sampled (k,tau) rows, 918 k histories; 512/1024 order control relative L2 `5.356772360739694e-07`, cosine `0.9999999999998567`. Both pass their unchanged predata gates.
- The first signed `+10` CLASS call aborted, `EXIT=94`, with `AEST_TANGENT_FORCE_K_MISS query=0.13466492781697323 nearest=0.13447612655668839 rel=1.402e-03`. Baseline had run but the signed Weyl tangent series did not complete. **No Weyl or lensing PASS was generated.**

## Exact cause (reproduced statically from pinned source)

The forcing trace builder in `ge19/linear_weyl_native_tangent_20261109.py` passed `REQ_KH=[0.03,0.05,0.08,0.10,0.15,0.20]` directly into CLASS `k_output_values`. Those values are in **h/Mpc** according to the frozen predata, while CLASS requires **1/Mpc**. The signed `compute_run` passed `REQ_KH*H`, where `H=H0/100=0.673324639084866`, into `k_output_values`.

The failed `query=0.13466492781697323` is exactly the originally requested `0.20*h` in **1/Mpc**; the mismatching nearest forcing table node `0.13447612655668839` was produced on the differently anchored trace sampling grid. This is not a physical-response failure or a need to relax the loader's strict k equality.

The original pinned `v075/fourier_k_resolution_closure.py` and `v076/native_node_power_closure.py` use `K_REQ=K_H*h` consistently on the forcing trace and signed CLASS paths. LW01 claimed to reuse this recipe but accidentally omitted `*h` in its forcing-trace INI.

## One bounded code correction

At implementation commit `fcd166270e28d652a0ba5d86b3186dd1cda6f4a1`, define `REQ_KPHYS=REQ_KH*H` and use that **same array** in both the initial eta=0 CLASS forcing-trace INI and the baseline/signed `classy` configurations. Preserve all predeclared `R4` density, 512/1024 quadrature, amplitudes, model parameters, unit conventions for reporting, native window and all gates. No C/CLASS patch and no threshold change.

This removes the *demonstrated* difference in requested mode anchors; full CLASS native node grid identity still must be verified by the actual bounded rerun. Do not infer scientific PASS from this static unit correction alone.

## Exactly one repaired local continuation; no overwrite

The failed run already created old forcing trace, table, summary and logs. Preserve them for provenance. Since the Python driver accepts `--output-prefix`, use a **new** namespaced output prefix rather than deleting those historical artifacts:

```bash
cd ~/aest-memory-gravity
git pull --ff-only
source .venv/bin/activate
set -o pipefail
python3 -u -m ge19.linear_weyl_native_tangent_20261109 --self-test
python3 -u -m ge19.linear_weyl_native_tangent_20261109 \
    --class-root "$PWD/class_v077" \
    --output-prefix results/ge19_linear_weyl_native_tangent_20261109_kgridfix \
    2>&1 | tee results/ge19_linear_weyl_native_tangent_20261109_kgridfix.log
echo "EXIT=${PIPESTATUS[0]}"
```

Expected result only if full series completes:

- `results/ge19_linear_weyl_native_tangent_20261109_kgridfix.json`
- `results/ge19_linear_weyl_native_tangent_20261109_kgridfix.npz`

If any later mismatch, native-grid failure or numerical gate failure occurs, archive it without another speculative rerun. Physical interpretation must remain bounded to native signed Weyl transfer tangent; only a separately frozen line-of-sight observable would permit a lensing prediction.

**Frozen status pending execution:** `full_H4_Ward_certified=false`, `Z21_certified=false`, `linear_lensing_prediction_certified=false`, `observational_detection=false`. All historical v068/H4 FAILs preserved.
