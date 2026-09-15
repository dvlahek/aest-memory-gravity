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
from scipy.interpolate import PchipInterpolator

from fullj_weyl import stable_aest_desi_dr1_r9b2k_native_k_density_convergence as k
from fullj_weyl import stable_aest_desi_dr1_r9b2k_shapefit_dm_repair01 as r1
from fullj_weyl import stable_aest_desi_dr1_r9b2i_native_variance_response_shapefit as i
from fullj_weyl import stable_aest_desi_dr1_r9b_shapefit_projection as r9b

ROOT = Path(__file__).resolve().parents[1]
PREFIT_LOCK = "9e9fd426e3030727f0723cf7e50ae4ef0c2799e8"
REPAIR01_POSTDATA_LOCK = "8f789b8203dfbee4a9ef7a16ddfb1bfd201bc78b"
HISTORY_LOCK = "ef6d291ecc99a0af950dd44fef743a87f708b81d"
REPAIR01_IMPL_LOCK = "c0a9f430053f4080ca4990d1549a5eca32e6515e"
REPAIR01_RUNNER_LOCK = "4a0c1ce46813ed1f3fb7b407bc49fff5fbd164f6"
PARENT_R9B2K_JSON = ROOT / "results/stable_aest_desi_dr1_r9b2k_native_k_density_convergence.json"
PARENT_R9B2K_SHA = "f4323f84dfa93c5ac3ef449fbe666ce3add45a50331079fe66bd27beb2b30c7e"
PARENT_R9B2K_CLASS = "STABLE_AEST_DESI_DR1_R9B2K_SHAPEFIT_VECTOR_FAIL"
REPAIR01_JSON = ROOT / "results/stable_aest_desi_dr1_r9b2k_shapefit_dm_repair01.json"
REPAIR01_SHA = "af92b8f7c6186a5e04c7a4973840617dd64ef7afb33deddc24804c1b974f40ad"
REPAIR01_CLASS = "STABLE_AEST_DESI_DR1_R9B2K_SHAPEFIT_DM_REPAIR01_FILTER_SUPPORT_FAIL"

ZEFF = k.ZEFF
TAUS = k.TAUS
ETAS = k.ETAS
EPS_PRIMARY = k.EPS_PRIMARY
EPS_CONTROL = k.EPS_CONTROL
E_GATE = k.E_GATE
C_GATE = k.C_GATE
NORM_GATE = k.NORM_GATE
M_VALUE_GATE = 5e-3
GRID_ATOL = 5e-13
MIN_SEGMENT_NODES = 8

PASS = "STABLE_AEST_DESI_DR1_R9B2K_SHAPEFIT_DM_REPAIR02_CERTIFIED"
FAIL_PROV = "STABLE_AEST_DESI_DR1_R9B2K_SHAPEFIT_DM_REPAIR02_PROVENANCE_FAIL"
FAIL_CHECKPOINT = "STABLE_AEST_DESI_DR1_R9B2K_SHAPEFIT_DM_REPAIR02_CHECKPOINT_FAIL"
FAIL_PIVOT = "STABLE_AEST_DESI_DR1_R9B2K_SHAPEFIT_DM_REPAIR02_LOCAL_PIVOT_FAIL"
FAIL_MOP = "STABLE_AEST_DESI_DR1_R9B2K_SHAPEFIT_DM_REPAIR02_LOCAL_M_OPERATOR_FAIL"
FAIL_DATA = "STABLE_AEST_DESI_DR1_R9B2K_SHAPEFIT_DM_REPAIR02_DESI_PROVENANCE_FAIL"
FAIL_VEC = "STABLE_AEST_DESI_DR1_R9B2K_SHAPEFIT_DM_REPAIR02_VECTOR_FAIL"
FAIL_EPS = "STABLE_AEST_DESI_DR1_R9B2K_SHAPEFIT_DM_REPAIR02_FULL_TANGENT_EPSILON_FAIL"
FAIL_CROSS = "STABLE_AEST_DESI_DR1_R9B2K_SHAPEFIT_DM_REPAIR02_FULL_CROSS_OPERATOR_FAIL"
FAIL_PROJ = "STABLE_AEST_DESI_DR1_R9B2K_SHAPEFIT_DM_REPAIR02_PROJECTION_FAIL"
FAIL_GLS = "STABLE_AEST_DESI_DR1_R9B2K_SHAPEFIT_DM_REPAIR02_GLS_FAIL"
FAIL_RUN = "STABLE_AEST_DESI_DR1_R9B2K_SHAPEFIT_DM_REPAIR02_RUN_FAIL"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"], cwd=ROOT,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
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
        parent = json.loads(PARENT_R9B2K_JSON.read_text()) if PARENT_R9B2K_JSON.is_file() else {}
        rr = json.loads(REPAIR01_JSON.read_text()) if REPAIR01_JSON.is_file() else {}
        locks = (PREFIT_LOCK, REPAIR01_POSTDATA_LOCK, HISTORY_LOCK, REPAIR01_IMPL_LOCK, REPAIR01_RUNNER_LOCK)
        meta["ancestor_locks"] = {x: ancestor(x) for x in locks}
        meta["parent_r9b2k_sha256"] = sha256(PARENT_R9B2K_JSON) if PARENT_R9B2K_JSON.is_file() else None
        meta["repair01_sha256"] = sha256(REPAIR01_JSON) if REPAIR01_JSON.is_file() else None
        meta["parent_r9b2k_classification"] = parent.get("classification")
        meta["repair01_classification"] = rr.get("classification")
        pg = parent.get("gates", {})
        stage_a = (
            "R9B2K_K1_provenance", "R9B2K_K2_native_grid_refinement",
            "R9B2K_K3_eta0_closure_tau_invariance", "R9B2K_K4_epsilon_consistency",
            "R9B2K_K5_native_density_convergence", "R9B2K_K6_cross_operator",
        )
        ok = bool(
            all(meta["ancestor_locks"].values())
            and meta["parent_r9b2k_sha256"] == PARENT_R9B2K_SHA
            and parent.get("classification") == PARENT_R9B2K_CLASS
            and parent.get("diagnostic_complete") is True
            and all(pg.get(x) is True for x in stage_a)
            and meta["repair01_sha256"] == REPAIR01_SHA
            and rr.get("classification") == REPAIR01_CLASS
            and rr.get("diagnostic_complete") is True
        )
        return ok, meta, parent
    except Exception as exc:
        meta["error"] = repr(exc)
        return False, meta, parent


def load_d2_checkpoints(workdir: Path) -> tuple[bool, dict, list]:
    vals = {}
    meta = []
    ok = True
    for tau in TAUS:
        for eta in ETAS:
            cp = workdir / f"{k._ckey('D2', tau, eta)}.pkl"
            item = {"tau_H0": float(tau), "eta": float(eta), "path": str(cp), "exists": cp.is_file()}
            if not cp.is_file():
                ok = False; meta.append(item); continue
            try:
                with cp.open("rb") as f: case = pickle.load(f)
                valid = k._checkpoint_ok(case, "D2", tau, eta)
                item["valid"] = bool(valid)
                if valid:
                    vals[k._vkey("D2", tau, eta)] = case
                    item["n_k"] = [int(len(r["state"]["kh"])) for r in case["rows"]]
                else:
                    ok = False
            except Exception as exc:
                item["valid"] = False; item["error"] = repr(exc); ok = False
            meta.append(item)
    if not ok:
        return False, vals, meta
    ref = vals[k._vkey("D2", 10.0, 0.0)]
    for iz, z in enumerate(ZEFF):
        kh0 = np.asarray(i._row(ref, iz)["state"]["kh"], float)
        for tau in TAUS:
            for eta in ETAS:
                kh = np.asarray(i._row(vals[k._vkey("D2", tau, eta)], iz)["state"]["kh"], float)
                if not (kh.shape == kh0.shape and np.allclose(kh, kh0, rtol=0.0, atol=GRID_ATOL)):
                    ok = False
                    meta.append({"tau_H0": float(tau), "eta": float(eta), "z": float(z), "grid_identity": False})
    return bool(ok), vals, meta


def _contiguous_true_runs(mask: np.ndarray):
    mask = np.asarray(mask, bool)
    x = np.flatnonzero(mask)
    if x.size == 0:
        return []
    cuts = np.flatnonzero(np.diff(x) > 1)
    starts = np.r_[0, cuts + 1]
    ends = np.r_[cuts, len(x) - 1]
    return [(int(x[a]), int(x[b])) for a, b in zip(starts, ends)]


def _raw_pknow_local(row: dict, fid, fidrow: dict, filt) -> tuple[dict, dict]:
    pkdd = r1._pkdd(row)
    cosmo = r1._source_cosmo(row)
    filt(pkdd, cosmo=cosmo)
    fk = np.asarray(filt.k, float).reshape(-1)
    fp = np.asarray(filt.pknow, float).reshape(-1)
    if fk.shape != fp.shape or fk.size < MIN_SEGMENT_NODES or np.any(np.diff(fk) <= 0):
        raise RuntimeError(f"invalid raw filter arrays: k={fk.shape} pknow={fp.shape}")

    z = float(row["z"]); m0 = row["background"]
    h = float(m0["h"]); rdrag = float(m0["rdrag"])
    s = (rdrag * h) / float(fid.rs_drag)
    kp = 0.03 / s; dk = 1e-2
    kk = kp * np.asarray([1.0 - dk, 1.0 + dk], float)

    finite = np.isfinite(fp)
    positive = finite & (fp > 0.0)
    bad = ~positive
    runs = _contiguous_true_runs(positive)
    candidates = [(a, b) for a, b in runs if (b - a + 1) >= MIN_SEGMENT_NODES and fk[a] < kk[0] and fk[b] > kk[1]]
    if len(candidates) != 1:
        raise RuntimeError(
            f"pivot not in unique positive raw-pknow segment z={z}: kk={kk.tolist()} candidates={candidates} bad_count={int(np.count_nonzero(bad))}"
        )
    a, b = candidates[0]
    if np.any(bad & (fk >= kk[0]) & (fk <= kk[1])):
        raise RuntimeError(f"bad raw-pknow node between pivot points z={z}")

    ks = fk[a:b+1]; ps = fp[a:b+1]
    lx = np.log(ks); ly = np.log(ps); lq = np.log(kk)
    lplin = np.interp(lq, lx, ly)
    lppch = np.asarray(PchipInterpolator(lx, ly, extrapolate=False)(lq), float)
    pvlin = np.exp(lplin); pvpch = np.exp(lppch)
    if not (np.all(np.isfinite(pvlin)) and np.all(pvlin > 0) and np.all(np.isfinite(pvpch)) and np.all(pvpch > 0)):
        raise RuntimeError(f"nonfinite/nonpositive local pivot interpolation z={z}")
    den = float(np.diff(lq)[0])
    mlin = float(np.diff(np.log(pvlin))[0] / den)
    mpch = float(np.diff(np.log(pvpch))[0] / den)

    Ap = float((1.0 / s**3) * np.asarray(pkdd(kp)))
    Hz = float(m0["Hubble_Mpc_inv"]) * r9b.C_KM_S
    da = float(m0["angular_distance_Mpc"])
    apar = (1.0 / (Hz / 100.0) / rdrag) / (1.0 / float(fid.efunc(z)) / float(fid.rs_drag))
    aper = (da / rdrag) / (float(fid.angular_diameter_distance(z)) / float(fid.rs_drag))
    if not (np.isfinite(Ap) and Ap > 0 and np.isfinite(apar) and apar > 0 and np.isfinite(aper) and aper > 0):
        raise RuntimeError(f"nonfinite ShapeFit non-m scalar z={z}")

    common = {
        "Ap": Ap, "apar": float(apar), "aper": float(aper),
        "fid_m": float(fidrow["m"]), "fid_f_sqrt_Ap": float(fidrow["f_sqrt_Ap"]),
    }
    shlin = dict(common); shlin["m"] = mlin
    shpch = dict(common); shpch["m"] = mpch
    badk = fk[bad]
    finite_fp = fp[finite]
    diag = {
        "z": z, "pivot_k": float(kp), "pivot_pair": kk.tolist(),
        "n_raw": int(fk.size), "bad_count": int(np.count_nonzero(bad)),
        "nonfinite_count": int(np.count_nonzero(~finite)),
        "nonpositive_finite_count": int(np.count_nonzero(finite & (fp <= 0.0))),
        "finite_pknow_min": float(np.min(finite_fp)) if finite_fp.size else float("nan"),
        "finite_pknow_max": float(np.max(finite_fp)) if finite_fp.size else float("nan"),
        "bad_k_min": float(np.min(badk)) if badk.size else None,
        "bad_k_max": float(np.max(badk)) if badk.size else None,
        "segment_i0": int(a), "segment_i1": int(b), "segment_n": int(b-a+1),
        "segment_k_min": float(ks[0]), "segment_k_max": float(ks[-1]),
        "linear_pivot_p": pvlin.tolist(), "pchip_pivot_p": pvpch.tolist(),
        "m_linear": mlin, "m_pchip": mpch, "m_sym_rel": sym_rel(mlin, mpch),
    }
    return {"linear": shlin, "pchip": shpch}, diag


def build_shapes(vals: dict, fid, fcache) -> tuple[bool, bool, dict]:
    baseline = vals[k._vkey("D2", 10.0, 0.0)]
    filters = {}
    setup = []
    for iz, z0 in enumerate(ZEFF):
        z = float(z0); row0 = i._row(baseline, iz)
        try:
            filt = r1._new_source_filter(row0, fid)
            filters[z] = filt
            setup.append({"z": z, "n_filter": int(np.asarray(filt.k).size), "ok": True})
        except Exception as exc:
            setup.append({"z": z, "ok": False, "error": repr(exc)})
    if len(filters) != len(ZEFF):
        return False, False, {"filter_setup": setup, "rows": [], "max_m_sym_rel": float("inf")}

    pivot_ok = True; mop_ok = True; rows = []; max_m = 0.0
    for tau in TAUS:
        for eta in ETAS:
            case = vals[k._vkey("D2", tau, eta)]
            for iz, z0 in enumerate(ZEFF):
                z = float(z0); row = i._row(case, iz)
                item = {"tau_H0": float(tau), "eta": float(eta), "z": z}
                try:
                    shapes, dg = _raw_pknow_local(row, fid, fcache[z], filters[z])
                    row["shape_linear"] = shapes["linear"]
                    row["shape_pchip"] = shapes["pchip"]
                    mr = float(dg["m_sym_rel"]); max_m = max(max_m, mr)
                    goodm = bool(np.isfinite(mr) and mr <= M_VALUE_GATE)
                    mop_ok &= goodm
                    item.update(dg); item["m_operator_pass"] = goodm
                except Exception as exc:
                    pivot_ok = False; mop_ok = False
                    item.update({"error": repr(exc), "m_operator_pass": False})
                rows.append(item)
    return bool(pivot_ok), bool(mop_ok), {
        "filter_setup": setup, "rows": rows,
        "max_m_sym_rel": float(max_m), "m_value_gate": M_VALUE_GATE,
    }


def _q(shape: dict, param: str) -> float:
    apar = float(shape["apar"]); aper = float(shape["aper"])
    suffix = param[1:]
    aa, bb = {"iso": (1/3, 2/3), "par": (1, 0), "per": (0, 1), "ap": (1, -1)}[suffix]
    return float(apar**aa * aper**bb)


def assemble_baseline(case0: dict, f0: np.ndarray, bins, shape_key: str) -> np.ndarray:
    out = []
    for iz, b in enumerate(bins):
        sh = i._row(case0, iz)[shape_key]
        for p in b["parameters"]:
            if p in ("qpar", "qper", "qiso", "qap"):
                v = _q(sh, p)
            elif p == "df":
                v = float(f0[iz] * np.sqrt(sh["Ap"]) / sh["fid_f_sqrt_Ap"])
            elif p == "dm":
                v = float(sh["m"] - sh["fid_m"])
            else:
                raise RuntimeError(f"unsupported ShapeFit parameter {p}")
            out.append(v)
    return np.asarray(out, float)


def assemble_tangent(zero: dict, plus: dict, minus: dict, source_resp: dict,
                     eps: float, baseline: dict, bins, shape_key: str) -> np.ndarray:
    out = []; f0 = np.asarray(baseline["f"], float); df = np.asarray(source_resp["df"], float)
    for iz, b in enumerate(bins):
        sh0 = i._row(zero, iz)[shape_key]; shp = i._row(plus, iz)[shape_key]; shm = i._row(minus, iz)[shape_key]
        dAp = (float(shp["Ap"]) - float(shm["Ap"])) / (2.0 * eps)
        dS = np.sqrt(sh0["Ap"]) * df[iz] + f0[iz] * dAp / (2.0 * np.sqrt(sh0["Ap"]))
        for p in b["parameters"]:
            if p in ("qpar", "qper", "qiso", "qap"):
                v = (_q(shp, p) - _q(shm, p)) / (2.0 * eps)
            elif p == "df":
                v = float(dS / sh0["fid_f_sqrt_Ap"])
            elif p == "dm":
                v = (float(shp["m"]) - float(shm["m"])) / (2.0 * eps)
            else:
                raise RuntimeError(f"unsupported ShapeFit parameter {p}")
            out.append(v)
    return np.asarray(out, float)


def main(args) -> int:
    outpath = Path(args.json_out)
    print("STABLE_AEST_DESI_DR1_R9B2K_DM_REPAIR02_START", flush=True)
    p1, prov, parent = provenance()
    gates = {"R9B2K_DM2_P1_parent_provenance": bool(p1)}
    if not p1:
        _write(outpath, {"classification": FAIL_PROV, "diagnostic_complete": False, "science_evaluated": False, "gates": gates, "provenance": prov})
        print("STABLE_AEST_DESI_DR1_R9B2K_DM_REPAIR02_CLASSIFICATION=" + FAIL_PROV, flush=True)
        return 3

    p2, vals, cpmeta = load_d2_checkpoints(Path(args.workdir))
    gates["R9B2K_DM2_P2_saved_D2_checkpoints"] = bool(p2)
    if not p2:
        _write(outpath, {"classification": FAIL_CHECKPOINT, "diagnostic_complete": True, "science_evaluated": False, "gates": gates, "provenance": prov, "checkpoints": cpmeta})
        print("STABLE_AEST_DESI_DR1_R9B2K_DM_REPAIR02_CLASSIFICATION=" + FAIL_CHECKPOINT, flush=True)
        return 1

    try:
        fid, fcache = r9b._get_fiducial_cache(ZEFF)
        p3, p4, rawmeta = build_shapes(vals, fid, fcache)
    except Exception as exc:
        p3 = p4 = False; rawmeta = {"error": repr(exc)}
    gates["R9B2K_DM2_P3_local_positive_pivot"] = bool(p3)
    gates["R9B2K_DM2_P4_local_m_operator"] = bool(p4)
    if not p3 or not p4:
        cls = FAIL_PIVOT if not p3 else FAIL_MOP
        _write(outpath, {"classification": cls, "diagnostic_complete": True, "science_evaluated": False, "desi_data_loaded": False, "gates": gates, "provenance": prov, "checkpoints": cpmeta, "raw_pknow_diagnostics": rawmeta})
        print("STABLE_AEST_DESI_DR1_R9B2K_DM_REPAIR02_CLASSIFICATION=" + cls, flush=True)
        return 1

    try:
        bundles = {float(tau): k._response_bundle(vals, "D2", tau) for tau in TAUS}
        data_dir = Path(args.data_dir).resolve(); official_repo = Path(args.official_repo).resolve()
        bins, d, C, offsets, data_hashes, _ = r9b.load_desi(data_dir, official_repo)
        repo_head = subprocess.check_output(["git", "-C", str(official_repo), "rev-parse", "HEAD"], text=True).strip()
        eig = np.linalg.eigvalsh(C); ze = np.asarray([float(b["zeff"]) for b in bins], float)
        b1 = bool(repo_head == r9b.DESI_REPO_COMMIT and len(bins) == 6 and len(d) == 24
                  and np.allclose(ze, ZEFF, rtol=0, atol=1e-12) and np.all(np.isfinite(d)) and np.all(np.isfinite(C))
                  and np.allclose(C, C.T, rtol=0, atol=1e-12) and np.all(eig > 0))
        data_meta = {"repo_head": repo_head, "files_sha256": data_hashes, "dimension": int(len(d)), "min_cov_eigenvalue": float(eig.min())}
    except Exception as exc:
        b1 = False; bins = []; d = C = offsets = None; data_meta = {"error": repr(exc)}
    gates["R9B2K_DM2_B1_desi_provenance"] = bool(b1)
    if not b1:
        _write(outpath, {"classification": FAIL_DATA, "diagnostic_complete": True, "science_evaluated": False, "gates": gates, "raw_pknow_diagnostics": rawmeta, "data": data_meta, "provenance": prov})
        return 1

    base_primary = assemble_baseline(vals[k._vkey("D2", 10.0, 0.0)], bundles[10.0][0]["linear8192"]["f"], bins, "shape_linear")
    base_control = assemble_baseline(vals[k._vkey("D2", 10.0, 0.0)], bundles[10.0][0]["pchip8192"]["f"], bins, "shape_pchip")
    full = {"primary": {}, "control": {}}; fullm = {"epsilon_primary": {}, "epsilon_control": {}, "cross": {}}
    b2 = bool(np.all(np.isfinite(base_primary)) and np.all(np.isfinite(base_control)))
    for tau in TAUS:
        s = str(tau); full["primary"][s] = {}; full["control"][s] = {}
        zc = vals[k._vkey("D2", tau, 0.0)]
        for eps in (EPS_PRIMARY, EPS_CONTROL):
            pp = vals[k._vkey("D2", tau, +eps)]; mm = vals[k._vkey("D2", tau, -eps)]
            rp = bundles[float(tau)][1]["linear8192"][str(eps)]; bp = bundles[float(tau)][0]["linear8192"]
            rc = bundles[float(tau)][1]["pchip8192"][str(eps)]; bc = bundles[float(tau)][0]["pchip8192"]
            tp = assemble_tangent(zc, pp, mm, rp, eps, bp, bins, "shape_linear")
            tc = assemble_tangent(zc, pp, mm, rc, eps, bc, bins, "shape_pchip")
            full["primary"][s][str(eps)] = tp; full["control"][s][str(eps)] = tc
            b2 &= bool(np.all(np.isfinite(tp)) and np.all(np.isfinite(tc)))
    gates["R9B2K_DM2_B2_shapefit_vector"] = bool(b2)

    b3 = True; b4 = True
    for tau in TAUS:
        s = str(tau)
        mep = i.metrics(full["primary"][s][str(EPS_PRIMARY)], full["primary"][s][str(EPS_CONTROL)])
        mec = i.metrics(full["control"][s][str(EPS_PRIMARY)], full["control"][s][str(EPS_CONTROL)])
        fullm["epsilon_primary"][s] = mep; fullm["epsilon_control"][s] = mec
        b3 &= metric_pass(mep) and metric_pass(mec)
        fullm["cross"][s] = {}
        for eps in (EPS_PRIMARY, EPS_CONTROL):
            mc = i.metrics(full["primary"][s][str(eps)], full["control"][s][str(eps)])
            fullm["cross"][s][str(eps)] = mc; b4 &= metric_pass(mc)
    gates["R9B2K_DM2_B3_full_tangent_epsilon"] = bool(b3)
    gates["R9B2K_DM2_B4_full_cross_operator"] = bool(b4)

    projection = {}; b5 = bool(b2 and b3 and b4); b6 = bool(b5)
    if b5:
        for tau in TAUS:
            try:
                t = full["primary"][str(tau)][str(EPS_PRIMARY)]
                p = r9b.projection_summary(d, C, base_primary, t, bins, offsets)
                projection[str(tau)] = p
                b5 &= bool(np.isfinite(p["F_perp"]) and p["F_perp"] > 0 and p["projection_idempotence_metric"] <= 1e-8)
                a = p["eta_hat_signed_matched_filter"]; bg = p["eta_hat_signed_gls"]
                b6 &= abs(a-bg) <= max(1e-10, 1e-8 * max(abs(a), abs(bg), 1.0))
            except Exception as exc:
                projection[str(tau)] = {"error": repr(exc)}; b5 = False; b6 = False
    gates["R9B2K_DM2_B5_nuisance_projection"] = bool(b5)
    gates["R9B2K_DM2_B6_matched_filter_gls"] = bool(b6)

    if not b2: cls = FAIL_VEC
    elif not b3: cls = FAIL_EPS
    elif not b4: cls = FAIL_CROSS
    elif not b5: cls = FAIL_PROJ
    elif not b6: cls = FAIL_GLS
    else: cls = PASS

    result = {
        "classification": cls, "diagnostic_complete": True, "science_evaluated": True,
        "desi_data_loaded": True, "gates": gates, "raw_pknow_diagnostics": rawmeta,
        "stageB": {"baseline_primary": base_primary.tolist(), "baseline_control": base_control.tolist(), "full_tangent_metrics": fullm, "tau_likelihood": projection},
        "data": data_meta, "provenance": prov,
        "settings": {"repair_scope": "raw pknow local pivot only; no CLASS rerun", "m_value_gate": M_VALUE_GATE,
                     "minimum_positive_segment_nodes": MIN_SEGMENT_NODES, "primary": "source-linear + local log-linear m",
                     "control": "source-PCHIP + local log-PCHIP m", "E_gate": E_GATE, "C_gate": C_GATE,
                     "epsilon_primary": EPS_PRIMARY, "epsilon_control": EPS_CONTROL},
        "interpretation": {"historical_R9b2k_reclassified": False, "historical_Repair01_reclassified": False,
                           "compressed_full_shape_corrected_projection_reportable": cls == PASS,
                           "observational_detection_claim_licensed": False, "full_EFT_modified_gravity_claim_licensed": False,
                           "tau_bound_claim_licensed": False},
    }
    _write(outpath, result)
    arrays = {"data": d, "covariance": C, "baseline_primary": base_primary, "baseline_control": base_control}
    for tau in TAUS:
        arrays[f"tangent_primary_tau{tau:g}"] = full["primary"][str(tau)][str(EPS_PRIMARY)]
        arrays[f"tangent_control_tau{tau:g}"] = full["control"][str(tau)][str(EPS_PRIMARY)]
    np.savez_compressed(args.npz_out, **arrays)
    gc.collect()
    print("STABLE_AEST_DESI_DR1_R9B2K_DM_REPAIR02_GATES=" + json.dumps(gates, sort_keys=True), flush=True)
    print("STABLE_AEST_DESI_DR1_R9B2K_DM_REPAIR02_PROJECTION=" + json.dumps(projection, sort_keys=True), flush=True)
    print("STABLE_AEST_DESI_DR1_R9B2K_DM_REPAIR02_CLASSIFICATION=" + cls, flush=True)
    return 0 if cls == PASS else 1


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="")
    ap.add_argument("--official-repo", default="")
    ap.add_argument("--workdir", default="results/stable_aest_desi_dr1_r9b2k_work")
    ap.add_argument("--json-out", default="results/stable_aest_desi_dr1_r9b2k_shapefit_dm_repair02.json")
    ap.add_argument("--npz-out", default="results/stable_aest_desi_dr1_r9b2k_shapefit_dm_repair02.npz")
    return ap.parse_args()


if __name__ == "__main__":
    raise SystemExit(main(parse_args()))
