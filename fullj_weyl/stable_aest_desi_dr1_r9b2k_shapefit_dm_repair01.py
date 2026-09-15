#!/usr/bin/env python3
from __future__ import annotations

import argparse
import gc
import hashlib
import json
import pickle
import subprocess
from pathlib import Path

import numpy as np

from fullj_weyl import stable_aest_desi_dr1_r9b2k_native_k_density_convergence as k
from fullj_weyl import stable_aest_desi_dr1_r9b2i_native_variance_response_shapefit as i
from fullj_weyl import stable_aest_desi_dr1_r9b_shapefit_projection as r9b

ROOT = Path(__file__).resolve().parents[1]

PREFIT_LOCK = "9ce2e1a1accdd063c565d9cc373ce764636f9913"
PARENT_POSTDATA_LOCK = "dd3981b2fd838fb24a997af77f913c3d5dd8d07b"
HISTORY_LOCK = "be036d4e2b3e3f837f963415d1fc605b769c727e"
PARENT_IMPL_LOCK = "874218ec2db38f505307b8183e199fe9d4c73d98"
PARENT_RUNNER_LOCK = "f04a9211b6455f3d541b9679c79c56d22fed0c04"

PARENT_JSON = ROOT / "results/stable_aest_desi_dr1_r9b2k_native_k_density_convergence.json"
PARENT_SHA = "f4323f84dfa93c5ac3ef449fbe666ce3add45a50331079fe66bd27beb2b30c7e"
PARENT_CLASS = "STABLE_AEST_DESI_DR1_R9B2K_SHAPEFIT_VECTOR_FAIL"

ZEFF = k.ZEFF
TAUS = k.TAUS
ETAS = k.ETAS
EPS_PRIMARY = k.EPS_PRIMARY
EPS_CONTROL = k.EPS_CONTROL
E_GATE = k.E_GATE
C_GATE = k.C_GATE
NORM_GATE = k.NORM_GATE
FILTER_REUSE_GATE = 1e-8
GRID_ATOL = 5e-13

PASS = "STABLE_AEST_DESI_DR1_R9B2K_SHAPEFIT_DM_REPAIR01_CERTIFIED"
FAIL_PROV = "STABLE_AEST_DESI_DR1_R9B2K_SHAPEFIT_DM_REPAIR01_PROVENANCE_FAIL"
FAIL_CHECKPOINT = "STABLE_AEST_DESI_DR1_R9B2K_SHAPEFIT_DM_REPAIR01_CHECKPOINT_FAIL"
FAIL_FILTER = "STABLE_AEST_DESI_DR1_R9B2K_SHAPEFIT_DM_REPAIR01_FILTER_SUPPORT_FAIL"
FAIL_REUSE = "STABLE_AEST_DESI_DR1_R9B2K_SHAPEFIT_DM_REPAIR01_FILTER_REUSE_FAIL"
FAIL_DATA = "STABLE_AEST_DESI_DR1_R9B2K_SHAPEFIT_DM_REPAIR01_DESI_PROVENANCE_FAIL"
FAIL_VEC = "STABLE_AEST_DESI_DR1_R9B2K_SHAPEFIT_DM_REPAIR01_VECTOR_FAIL"
FAIL_EPS = "STABLE_AEST_DESI_DR1_R9B2K_SHAPEFIT_DM_REPAIR01_FULL_TANGENT_EPSILON_FAIL"
FAIL_CROSS = "STABLE_AEST_DESI_DR1_R9B2K_SHAPEFIT_DM_REPAIR01_FULL_CROSS_OPERATOR_FAIL"
FAIL_PROJ = "STABLE_AEST_DESI_DR1_R9B2K_SHAPEFIT_DM_REPAIR01_PROJECTION_FAIL"
FAIL_GLS = "STABLE_AEST_DESI_DR1_R9B2K_SHAPEFIT_DM_REPAIR01_GLS_FAIL"
FAIL_RUN = "STABLE_AEST_DESI_DR1_R9B2K_SHAPEFIT_DM_REPAIR01_RUN_FAIL"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"],
        cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    ).returncode == 0


def _write(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")


def metric_pass(m: dict) -> bool:
    return bool(
        np.isfinite(m["E"]) and np.isfinite(m["C"])
        and m["E"] <= E_GATE and m["C"] >= C_GATE
        and m["norm_a"] > NORM_GATE and m["norm_b"] > NORM_GATE
    )


def sym_rel(a: float, b: float) -> float:
    return float(abs(float(a) - float(b)) / max(abs(float(a)), abs(float(b)), 1e-300))


def provenance() -> tuple[bool, dict, dict]:
    meta = {}
    parent = {}
    try:
        parent = json.loads(PARENT_JSON.read_text()) if PARENT_JSON.is_file() else {}
        locks = (PREFIT_LOCK, PARENT_POSTDATA_LOCK, HISTORY_LOCK, PARENT_IMPL_LOCK, PARENT_RUNNER_LOCK)
        meta["ancestor_locks"] = {x: ancestor(x) for x in locks}
        meta["parent_json_exists"] = PARENT_JSON.is_file()
        meta["parent_json_sha256"] = sha256(PARENT_JSON) if PARENT_JSON.is_file() else None
        meta["parent_classification"] = parent.get("classification")
        meta["parent_gates"] = parent.get("gates", {})
        g = parent.get("gates", {})
        stage_a = (
            "R9B2K_K1_provenance",
            "R9B2K_K2_native_grid_refinement",
            "R9B2K_K3_eta0_closure_tau_invariance",
            "R9B2K_K4_epsilon_consistency",
            "R9B2K_K5_native_density_convergence",
            "R9B2K_K6_cross_operator",
        )
        ok = bool(
            all(meta["ancestor_locks"].values())
            and meta["parent_json_sha256"] == PARENT_SHA
            and parent.get("classification") == PARENT_CLASS
            and parent.get("diagnostic_complete") is True
            and all(g.get(x) is True for x in stage_a)
            and g.get("R9B2K_B1_desi_provenance") is True
            and g.get("R9B2K_B2_shapefit_vector") is False
        )
        return ok, meta, parent
    except Exception as exc:
        meta["error"] = repr(exc)
        return False, meta, parent


def load_d2_checkpoints(workdir: Path) -> tuple[bool, dict, list]:
    vals = {}
    rows = []
    ok = True
    for tau in TAUS:
        for eta in ETAS:
            cp = workdir / f"{k._ckey('D2', tau, eta)}.pkl"
            item = {"tau_H0": float(tau), "eta": float(eta), "path": str(cp), "exists": cp.is_file()}
            if not cp.is_file():
                ok = False
                rows.append(item)
                continue
            try:
                with cp.open("rb") as f:
                    case = pickle.load(f)
                valid = k._checkpoint_ok(case, "D2", tau, eta)
                item["valid"] = bool(valid)
                if not valid:
                    ok = False
                else:
                    vals[k._vkey("D2", tau, eta)] = case
                    item["n_k"] = [int(len(r["state"]["kh"])) for r in case["rows"]]
            except Exception as exc:
                item["valid"] = False
                item["error"] = repr(exc)
                ok = False
            rows.append(item)

    if not ok:
        return False, vals, rows

    ref = vals[k._vkey("D2", 10.0, 0.0)]
    for iz, z in enumerate(ZEFF):
        kh0 = np.asarray(i._row(ref, iz)["state"]["kh"], float)
        for tau in TAUS:
            for eta in ETAS:
                kh = np.asarray(i._row(vals[k._vkey("D2", tau, eta)], iz)["state"]["kh"], float)
                same = bool(kh.shape == kh0.shape and np.allclose(kh, kh0, rtol=0.0, atol=GRID_ATOL))
                if not same:
                    ok = False
                    rows.append({
                        "tau_H0": float(tau), "eta": float(eta), "z": float(z),
                        "grid_identity": False,
                    })
    return bool(ok), vals, rows


def _source_cosmo(row: dict):
    from cosmoprimo import Cosmology
    m0 = row["background"]
    h = float(m0["h"])
    cosmo = Cosmology(
        H0=100.0 * h,
        Omega_b=float(m0["Omega_b"]),
        Omega_cdm=float(m0["Omega_cdm"]),
        Omega_ncdm=float(m0["Omega_nu"]),
        n_s=float(m0["n_s"]),
    )
    try:
        cosmo.rs_drag = float(m0["rdrag"]) * h
    except Exception:
        pass
    return cosmo


def _pkdd(row: dict):
    from cosmoprimo import PowerSpectrumInterpolator1D
    st = row["state"]
    kh = np.asarray(st["kh"], float)
    pdd = np.asarray(st["pdd"], float)
    return PowerSpectrumInterpolator1D(
        kh, pdd, extrap_kmin=float(kh[0]), extrap_kmax=float(kh[-1])
    )


def _new_source_filter(row: dict, fid):
    from cosmoprimo import PowerSpectrumBAOFilter
    pkdd = _pkdd(row)
    cosmo = _source_cosmo(row)
    filt = PowerSpectrumBAOFilter(
        pkdd, engine="peakaverage", cosmo=cosmo, cosmo_fid=fid
    )
    return filt


def _shape_from_filter(row: dict, fid, fidrow: dict, filt) -> tuple[dict, dict]:
    z = float(row["z"])
    st = row["state"]
    m0 = row["background"]
    kh = np.asarray(st["kh"], float)
    pkdd = _pkdd(row)
    cosmo = _source_cosmo(row)

    fk = np.asarray(filt.k, float)
    support_ok = bool(
        np.all(np.isfinite(fk))
        and fk[0] >= kh[0] - GRID_ATOL
        and fk[-1] <= kh[-1] + GRID_ATOL
    )
    if not support_ok:
        raise RuntimeError(
            f"support-matched filter grid outside source support z={z}: "
            f"filter=[{fk[0]},{fk[-1]}] source=[{kh[0]},{kh[-1]}]"
        )

    filt(pkdd, cosmo=cosmo)
    pknow = filt.smooth_pk_interpolator(
        extrap_kmin=float(kh[0]), extrap_kmax=float(kh[-1])
    )

    h = float(m0["h"])
    rdrag = float(m0["rdrag"])
    s = (rdrag * h) / float(fid.rs_drag)
    kp = 0.03 / s
    dk = 1e-2
    kk = kp * np.asarray([1.0 - dk, 1.0 + dk], float)
    if kk[0] <= kh[0] or kk[-1] >= kh[-1]:
        raise RuntimeError(f"ShapeFit pivot outside bounded source support z={z}")

    pv = np.asarray(pknow(kk), float)
    pivot_ok = bool(pv.shape == (2,) and np.all(np.isfinite(pv)) and np.all(pv > 0.0))
    if not pivot_ok:
        raise RuntimeError(f"nonfinite/nonpositive no-wiggle pivot values z={z}: {pv!r}")

    mm = float(np.diff(np.log(pv))[0] / np.diff(np.log(kk))[0])
    Ap = float((1.0 / s**3) * np.asarray(pkdd(kp)))
    Hz = float(m0["Hubble_Mpc_inv"]) * r9b.C_KM_S
    da = float(m0["angular_distance_Mpc"])
    apar = (1.0 / (Hz / 100.0) / rdrag) / (1.0 / float(fid.efunc(z)) / float(fid.rs_drag))
    aper = (da / rdrag) / (float(fid.angular_diameter_distance(z)) / float(fid.rs_drag))

    values_ok = bool(
        np.isfinite(mm) and np.isfinite(Ap) and Ap > 0.0
        and np.isfinite(apar) and np.isfinite(aper) and apar > 0.0 and aper > 0.0
    )
    if not values_ok:
        raise RuntimeError(
            f"nonfinite ShapeFit scalar z={z}: m={mm} Ap={Ap} apar={apar} aper={aper}"
        )

    shape = {
        "m": mm,
        "Ap": Ap,
        "apar": float(apar),
        "aper": float(aper),
        "fid_m": float(fidrow["m"]),
        "fid_f_sqrt_Ap": float(fidrow["f_sqrt_Ap"]),
    }
    diag = {
        "z": z,
        "source_k_min": float(kh[0]),
        "source_k_max": float(kh[-1]),
        "filter_k_min": float(fk[0]),
        "filter_k_max": float(fk[-1]),
        "pivot_k": float(kp),
        "pivot_pair": kk.tolist(),
        "pknow_pair": pv.tolist(),
        "m": mm,
        "Ap": Ap,
        "support_ok": support_ok,
        "pivot_ok": pivot_ok,
    }
    return shape, diag


def repair_shapes(vals: dict, fid, fcache) -> tuple[bool, bool, dict]:
    baseline = vals[k._vkey("D2", 10.0, 0.0)]
    filters = {}
    setup = []
    r3 = True
    for iz, z0 in enumerate(ZEFF):
        z = float(z0)
        row0 = i._row(baseline, iz)
        try:
            filt = _new_source_filter(row0, fid)
            filters[z] = filt
            fk = np.asarray(filt.k, float)
            kh = np.asarray(row0["state"]["kh"], float)
            good = bool(
                fk[0] >= kh[0] - GRID_ATOL and fk[-1] <= kh[-1] + GRID_ATOL
                and np.all(np.isfinite(fk))
            )
            r3 &= good
            setup.append({
                "z": z, "good": good, "source_k_min": float(kh[0]),
                "source_k_max": float(kh[-1]), "filter_k_min": float(fk[0]),
                "filter_k_max": float(fk[-1]), "n_filter": int(fk.size),
            })
        except Exception as exc:
            r3 = False
            setup.append({"z": z, "good": False, "error": repr(exc)})

    if not r3:
        return False, False, {"filter_setup": setup, "rows": [], "max_cached_vs_fresh_m_rel": float("inf")}

    rows = []
    max_rel = 0.0
    r4 = True
    for tau in TAUS:
        for eta in ETAS:
            case = vals[k._vkey("D2", tau, eta)]
            for iz, z0 in enumerate(ZEFF):
                z = float(z0)
                row = i._row(case, iz)
                item = {"tau_H0": float(tau), "eta": float(eta), "z": z}
                try:
                    sh, dg = _shape_from_filter(row, fid, fcache[z], filters[z])
                    fresh = _new_source_filter(row, fid)
                    shf, dgf = _shape_from_filter(row, fid, fcache[z], fresh)
                    mr = sym_rel(sh["m"], shf["m"])
                    max_rel = max(max_rel, mr)
                    good = bool(
                        mr <= FILTER_REUSE_GATE
                        and np.isfinite(sh["m"]) and np.isfinite(shf["m"])
                    )
                    r3 &= bool(dg["support_ok"] and dg["pivot_ok"] and dgf["support_ok"] and dgf["pivot_ok"])
                    r4 &= good
                    row["shape"] = sh
                    item.update({
                        "good": good,
                        "cached_m": float(sh["m"]),
                        "fresh_m": float(shf["m"]),
                        "cached_vs_fresh_m_rel": mr,
                        "pivot_pknow_min": float(min(dg["pknow_pair"])),
                        "pivot_pknow_max": float(max(dg["pknow_pair"])),
                    })
                except Exception as exc:
                    r3 = False
                    r4 = False
                    item.update({"good": False, "error": repr(exc)})
                rows.append(item)
    return bool(r3), bool(r4), {
        "filter_setup": setup,
        "rows": rows,
        "max_cached_vs_fresh_m_rel": float(max_rel),
        "reuse_gate": FILTER_REUSE_GATE,
    }


def main(args) -> int:
    outpath = Path(args.json_out)
    print("STABLE_AEST_DESI_DR1_R9B2K_DM_REPAIR01_START", flush=True)

    r1, prov, parent = provenance()
    gates = {"R9B2K_DM_R1_parent_provenance": bool(r1)}
    if not r1:
        _write(outpath, {
            "classification": FAIL_PROV, "diagnostic_complete": False,
            "science_evaluated": False, "desi_data_loaded": False,
            "gates": gates, "provenance": prov,
        })
        print("STABLE_AEST_DESI_DR1_R9B2K_DM_REPAIR01_CLASSIFICATION=" + FAIL_PROV, flush=True)
        return 3

    work = Path(args.workdir)
    r2, vals, checkpoint_meta = load_d2_checkpoints(work)
    gates["R9B2K_DM_R2_saved_D2_checkpoints"] = bool(r2)
    if not r2:
        _write(outpath, {
            "classification": FAIL_CHECKPOINT, "diagnostic_complete": True,
            "science_evaluated": False, "desi_data_loaded": False,
            "gates": gates, "provenance": prov, "checkpoints": checkpoint_meta,
        })
        print("STABLE_AEST_DESI_DR1_R9B2K_DM_REPAIR01_CLASSIFICATION=" + FAIL_CHECKPOINT, flush=True)
        return 1

    try:
        fid, fcache = r9b._get_fiducial_cache(ZEFF)
        r3, r4, filter_meta = repair_shapes(vals, fid, fcache)
    except Exception as exc:
        r3 = r4 = False
        filter_meta = {"error": repr(exc)}
    gates["R9B2K_DM_R3_support_matched_filter"] = bool(r3)
    gates["R9B2K_DM_R4_cached_vs_fresh_filter"] = bool(r4)
    if not r3 or not r4:
        classification = FAIL_FILTER if not r3 else FAIL_REUSE
        _write(outpath, {
            "classification": classification, "diagnostic_complete": True,
            "science_evaluated": False, "desi_data_loaded": False,
            "gates": gates, "provenance": prov,
            "checkpoints": checkpoint_meta, "filter_diagnostics": filter_meta,
        })
        print("STABLE_AEST_DESI_DR1_R9B2K_DM_REPAIR01_CLASSIFICATION=" + classification, flush=True)
        return 1

    try:
        bundles = {float(tau): k._response_bundle(vals, "D2", tau) for tau in TAUS}
    except Exception as exc:
        _write(outpath, {
            "classification": FAIL_RUN, "diagnostic_complete": False,
            "science_evaluated": False, "desi_data_loaded": False,
            "error": repr(exc), "gates": gates, "provenance": prov,
        })
        return 2

    data_loaded = False
    try:
        data_dir = Path(args.data_dir).resolve()
        official_repo = Path(args.official_repo).resolve()
        bins, d, C, offsets, data_hashes, _ = r9b.load_desi(data_dir, official_repo)
        data_loaded = True
        repo_head = subprocess.check_output(
            ["git", "-C", str(official_repo), "rev-parse", "HEAD"], text=True
        ).strip()
        eig = np.linalg.eigvalsh(C)
        ze = np.asarray([float(b["zeff"]) for b in bins], float)
        b1 = bool(
            repo_head == r9b.DESI_REPO_COMMIT
            and len(bins) == 6 and len(d) == 24
            and np.allclose(ze, ZEFF, rtol=0.0, atol=1e-12)
            and np.all(np.isfinite(d)) and np.all(np.isfinite(C))
            and np.allclose(C, C.T, rtol=0.0, atol=1e-12)
            and np.all(eig > 0.0)
        )
        data_meta = {
            "repo_head": repo_head, "files_sha256": data_hashes,
            "dimension": int(len(d)), "min_cov_eigenvalue": float(eig.min()),
            "bins": [{
                "namespace": b["namespace"], "zeff": b["zeff"],
                "parameters": b["parameters"],
            } for b in bins],
        }
    except Exception as exc:
        b1 = False
        bins = []
        d = C = offsets = None
        data_meta = {"error": repr(exc)}

    gates["R9B2K_DM_B1_desi_provenance"] = bool(b1)
    if not b1:
        _write(outpath, {
            "classification": FAIL_DATA, "diagnostic_complete": True,
            "science_evaluated": False, "desi_data_loaded": data_loaded,
            "gates": gates, "provenance": prov,
            "checkpoints": checkpoint_meta, "filter_diagnostics": filter_meta,
            "data": data_meta,
        })
        return 1

    full = {"linear8192": {}, "pchip8192": {}}
    fullm = {"epsilon": {}, "cross": {}}

    basevec = i._assemble_baseline(
        vals[k._vkey("D2", 10.0, 0.0)],
        bundles[10.0][0]["linear8192"]["f"],
        bins,
    )
    b2 = bool(np.all(np.isfinite(basevec)))

    for tau in TAUS:
        s = str(tau)
        zc = vals[k._vkey("D2", tau, 0.0)]
        full["linear8192"][s] = {}
        full["pchip8192"][s] = {}
        for eps in (EPS_PRIMARY, EPS_CONTROL):
            pp = vals[k._vkey("D2", tau, +eps)]
            mm = vals[k._vkey("D2", tau, -eps)]
            for name in ("linear8192", "pchip8192"):
                resp = bundles[float(tau)][1][name][str(eps)]
                base = bundles[float(tau)][0][name]
                t = i._assemble_tangent(zc, pp, mm, resp, eps, base, bins)
                full[name][s][str(eps)] = t
                b2 &= bool(np.all(np.isfinite(t)))

    gates["R9B2K_DM_B2_shapefit_vector"] = bool(b2)

    b3 = True
    b4 = True
    for tau in TAUS:
        s = str(tau)
        me = i.metrics(
            full["linear8192"][s][str(EPS_PRIMARY)],
            full["linear8192"][s][str(EPS_CONTROL)],
        )
        fullm["epsilon"][s] = me
        b3 &= metric_pass(me)
        fullm["cross"][s] = {}
        for eps in (EPS_PRIMARY, EPS_CONTROL):
            mc = i.metrics(
                full["linear8192"][s][str(eps)],
                full["pchip8192"][s][str(eps)],
            )
            fullm["cross"][s][str(eps)] = mc
            b4 &= metric_pass(mc)

    gates["R9B2K_DM_B3_full_tangent_epsilon"] = bool(b3)
    gates["R9B2K_DM_B4_full_cross_operator"] = bool(b4)

    projection = {}
    b5 = bool(b2 and b3 and b4)
    b6 = bool(b5)
    if b5:
        for tau in TAUS:
            try:
                t = full["linear8192"][str(tau)][str(EPS_PRIMARY)]
                p = r9b.projection_summary(d, C, basevec, t, bins, offsets)
                projection[str(tau)] = p
                b5 &= bool(
                    np.isfinite(p["F_perp"]) and p["F_perp"] > 0.0
                    and p["projection_idempotence_metric"] <= 1e-8
                )
                a = p["eta_hat_signed_matched_filter"]
                bg = p["eta_hat_signed_gls"]
                b6 &= abs(a - bg) <= max(1e-10, 1e-8 * max(abs(a), abs(bg), 1.0))
            except Exception as exc:
                projection[str(tau)] = {"error": repr(exc)}
                b5 = False
                b6 = False

    gates["R9B2K_DM_B5_nuisance_projection"] = bool(b5)
    gates["R9B2K_DM_B6_matched_filter_gls"] = bool(b6)

    if not b2:
        classification = FAIL_VEC
    elif not b3:
        classification = FAIL_EPS
    elif not b4:
        classification = FAIL_CROSS
    elif not b5:
        classification = FAIL_PROJ
    elif not b6:
        classification = FAIL_GLS
    else:
        classification = PASS

    result = {
        "classification": classification,
        "diagnostic_complete": True,
        "science_evaluated": True,
        "desi_data_loaded": True,
        "gates": gates,
        "parent": {
            "classification": parent.get("classification"),
            "json_sha256": PARENT_SHA,
            "stageA_gates": {x: parent.get("gates", {}).get(x) for x in parent.get("gates", {}) if x.startswith("R9B2K_K")},
        },
        "filter_diagnostics": filter_meta,
        "stageB": {
            "baseline_vector": basevec.tolist(),
            "full_tangent_metrics": fullm,
            "tau_likelihood": projection,
        },
        "data": data_meta,
        "provenance": prov,
        "settings": {
            "repair_scope": "ShapeFit m/dm adapter only; no CLASS rerun",
            "filter_engine": "peakaverage",
            "filter_constructor_support": "D2 bounded source-state Pdd",
            "filter_cosmo_fid": "same DESI fiducial cosmology",
            "cached_vs_fresh_m_gate": FILTER_REUSE_GATE,
            "epsilon_primary": EPS_PRIMARY,
            "epsilon_control": EPS_CONTROL,
            "E_gate": E_GATE,
            "C_gate": C_GATE,
            "eta_physical_interval": [r9b.ETA_PHYS_MIN, r9b.ETA_PHYS_MAX],
        },
        "interpretation": {
            "historical_R9b2k_reclassified": False,
            "compressed_full_shape_corrected_projection_reportable": classification == PASS,
            "observational_detection_claim_licensed": False,
            "full_EFT_modified_gravity_claim_licensed": False,
            "tau_bound_claim_licensed": False,
        },
    }
    _write(outpath, result)

    arrays = {"data": d, "covariance": C, "baseline": basevec}
    for tau in TAUS:
        arrays[f"tangent_tau{tau:g}"] = full["linear8192"][str(tau)][str(EPS_PRIMARY)]
        arrays[f"source_df_response_tau{tau:g}"] = bundles[float(tau)][1]["linear8192"][str(EPS_PRIMARY)]["df"]
    np.savez_compressed(args.npz_out, **arrays)
    gc.collect()

    print("STABLE_AEST_DESI_DR1_R9B2K_DM_REPAIR01_GATES=" + json.dumps(gates, sort_keys=True), flush=True)
    print("STABLE_AEST_DESI_DR1_R9B2K_DM_REPAIR01_PROJECTION=" + json.dumps(projection, sort_keys=True), flush=True)
    print("STABLE_AEST_DESI_DR1_R9B2K_DM_REPAIR01_CLASSIFICATION=" + classification, flush=True)
    return 0 if classification == PASS else 1


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="")
    ap.add_argument("--official-repo", default="")
    ap.add_argument("--workdir", default="results/stable_aest_desi_dr1_r9b2k_work")
    ap.add_argument("--json-out", default="results/stable_aest_desi_dr1_r9b2k_shapefit_dm_repair01.json")
    ap.add_argument("--npz-out", default="results/stable_aest_desi_dr1_r9b2k_shapefit_dm_repair01.npz")
    return ap.parse_args()


if __name__ == "__main__":
    raise SystemExit(main(parse_args()))
