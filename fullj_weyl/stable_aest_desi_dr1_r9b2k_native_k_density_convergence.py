#!/usr/bin/env python3
from __future__ import annotations

import argparse
import gc
import hashlib
import json
import os
import pickle
import subprocess
import sys
from pathlib import Path

import numpy as np

from fullj_weyl import stable_aest_desi_dr1_r9b2j_signed_response_shapefit as j
from fullj_weyl import stable_aest_desi_dr1_r9b2j_signed_response_shapefit_repair01 as r01
from fullj_weyl import stable_aest_desi_dr1_r9b2i_native_variance_response_shapefit as i
from fullj_weyl import stable_aest_desi_dr1_r9b_shapefit_projection as r9b
from fullj_weyl import stable_aest_desi_dr1_r9b2f_full_grid_rogue_node as r9b2f

ROOT = Path(__file__).resolve().parents[1]
PREFIT_LOCK = "cbd4cd2a0fbf8315de3db7dee054e2fbf845f7c8"
R9B2J_POSTDATA_LOCK = "ce3d170e68244d6bbfea5374e6a5a5f7cc4efbc4"
R9B2J_REPAIR_PREFIT_LOCK = "040d169407d4bdde0f59f9b15380c3623a5abfe8"
R9B2J_REPAIR_IMPL_LOCK = "ba2ee3afecce27485ffa606586ba129fdc89c2d8"
R9B2J_REPAIR_RUNNER_LOCK = "0dd3914ef359e6014ea0df3c0966bed03a207219"
R9B2J_JSON = ROOT / "results/stable_aest_desi_dr1_r9b2j_signed_response_shapefit_repair01.json"
R9B2J_SHA = "e61b05279e0b2cb58c12a66cc0455f4c894ba5be2ec7d656be13cf6b8cf8c602"
R9B2J_CLASS = "STABLE_AEST_DESI_DR1_R9B2J_CROSS_OPERATOR_FAIL"

ZEFF = j.ZEFF
TAUS = j.TAUS
ETAS = j.ETAS
EPS_PRIMARY = j.EPS_PRIMARY
EPS_CONTROL = j.EPS_CONTROL
REL_GATE = j.REL_GATE
E_GATE = j.E_GATE
C_GATE = j.C_GATE
NORM_GATE = j.NORM_GATE
DEFAULT_NK = 108
DENSITIES = {
    "D1": (80.0, 560.0),
    "D2": (160.0, 1120.0),
}

PASS = "STABLE_AEST_DESI_DR1_R9B2K_NATIVE_K_DENSITY_SHAPEFIT_CERTIFIED"
FAIL_PROV = "STABLE_AEST_DESI_DR1_R9B2K_PROVENANCE_FAIL"
FAIL_GRID = "STABLE_AEST_DESI_DR1_R9B2K_NATIVE_GRID_REFINEMENT_FAIL"
FAIL_CLOSURE = "STABLE_AEST_DESI_DR1_R9B2K_ETA0_CLOSURE_FAIL"
FAIL_EPS = "STABLE_AEST_DESI_DR1_R9B2K_EPSILON_CONSISTENCY_FAIL"
FAIL_DENSITY = "STABLE_AEST_DESI_DR1_R9B2K_NATIVE_DENSITY_CONVERGENCE_FAIL"
FAIL_CROSS = "STABLE_AEST_DESI_DR1_R9B2K_CROSS_OPERATOR_FAIL"
FAIL_DATA = "STABLE_AEST_DESI_DR1_R9B2K_DESI_PROVENANCE_FAIL"
FAIL_VEC = "STABLE_AEST_DESI_DR1_R9B2K_SHAPEFIT_VECTOR_FAIL"
FAIL_FULL = "STABLE_AEST_DESI_DR1_R9B2K_FULL_TANGENT_FAIL"
FAIL_FULL_CROSS = "STABLE_AEST_DESI_DR1_R9B2K_FULL_CROSS_OPERATOR_FAIL"
FAIL_PROJ = "STABLE_AEST_DESI_DR1_R9B2K_NUISANCE_PROJECTION_FAIL"
FAIL_GLS = "STABLE_AEST_DESI_DR1_R9B2K_MATCHED_FILTER_GLS_FAIL"
FAIL_RUN = "STABLE_AEST_DESI_DR1_R9B2K_RUN_FAIL"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"], cwd=ROOT,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    ).returncode == 0


def metric_pass(m: dict) -> bool:
    return bool(
        np.isfinite(m["E"]) and np.isfinite(m["C"])
        and m["E"] <= E_GATE and m["C"] >= C_GATE
        and m["norm_a"] > NORM_GATE and m["norm_b"] > NORM_GATE
    )


def _write(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")


def _density_meta(tier: str) -> dict:
    kp, kb = DENSITIES[tier]
    return {"tier": tier, "k_per_decade_for_pk": kp, "k_per_decade_for_bao": kb}


def _params_density(eta: float, tau: float, tier: str):
    p, bits, pos = i._params(float(eta), float(tau))
    kp, kb = DENSITIES[tier]
    p["k_per_decade_for_pk"] = float(kp)
    p["k_per_decade_for_bao"] = float(kb)
    return p, int(bits), int(pos)


def _ckey(tier: str, tau: float, eta: float) -> str:
    return f"{tier}_tau{tau:g}_eta{eta:+.3f}"


def _vkey(tier: str, tau: float, eta: float) -> str:
    return f"{tier}:{i._key(tau, eta)}"


def run_light_case_density(eta: float, tau: float, tier: str) -> dict:
    from classy import Class

    p, bits, pos = _params_density(eta, tau, tier)
    c = Class(); c.set(p); c.compute()
    try:
        As = float(p["A_s"]); ns = float(p["n_s"])
        meta0 = {
            "h": float(c.h()), "rdrag": float(c.rs_drag()),
            "Omega_b": r9b._omega(c, "Omega_b"),
            "Omega_cdm": r9b._omega(c, "Omega_cdm"),
            "Omega_nu": r9b._omega(c, "Omega_nu", 0.0),
            "n_s": float(c.n_s()),
        }
        rows = []
        for z0 in ZEFF:
            z = float(z0)
            st = r9b2f._state_at_z(c, z, As, ns)
            si = float(c.sigma(8.0, z, h_units=True))
            proxy = float(c.effective_f_sigma8(z, z_step=0.1)) / si
            bg = dict(meta0)
            bg.update({
                "Hubble_Mpc_inv": float(c.Hubble(z)),
                "angular_distance_Mpc": float(c.angular_distance(z)),
            })
            rows.append({
                "z": z, "state": st, "sigma_internal": si,
                "growth_proxy": proxy, "background": bg,
            })
        return {
            "tier": tier,
            "density": _density_meta(tier),
            "tau_H0": float(tau), "eta": float(eta),
            "rows": rows, "bits": bits, "target_pos": pos,
        }
    finally:
        c.struct_cleanup(); c.empty()


def _checkpoint_ok(case: dict, tier: str, tau: float, eta: float) -> bool:
    try:
        if case.get("tier") != tier: return False
        if float(case["tau_H0"]) != float(tau) or float(case["eta"]) != float(eta): return False
        dm = case["density"]; expected = _density_meta(tier)
        if float(dm["k_per_decade_for_pk"]) != float(expected["k_per_decade_for_pk"]): return False
        if float(dm["k_per_decade_for_bao"]) != float(expected["k_per_decade_for_bao"]): return False
        rows = case["rows"]
        if len(rows) != len(ZEFF): return False
        for z, row in zip(ZEFF, rows):
            if abs(float(row["z"]) - float(z)) > 1e-13: return False
            st = row["state"]
            kh = np.asarray(st["kh"], float)
            if kh.ndim != 1 or kh.size < 32 or not np.all(np.isfinite(kh)) or np.any(np.diff(kh) <= 0): return False
            for q in ("pdd", "ptt"):
                a = np.asarray(st[q], float)
                if a.shape != kh.shape or not np.all(np.isfinite(a)) or not np.all(a > 0): return False
        return True
    except Exception:
        return False


def worker(args) -> int:
    case = run_light_case_density(args.eta, args.tau, args.tier)
    p = Path(args.out); p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    with tmp.open("wb") as f:
        pickle.dump(case, f, protocol=pickle.HIGHEST_PROTOCOL)
    tmp.replace(p)
    nk = [int(len(r["state"]["kh"])) for r in case["rows"]]
    print(
        f"STABLE_AEST_DESI_DR1_R9B2K_WORKER_PASS tier={args.tier} tau={args.tau:g} "
        f"eta={args.eta:+.3f} nk_min={min(nk)} nk_max={max(nk)}",
        flush=True,
    )
    return 0


def provenance() -> tuple[bool, dict]:
    meta = {}
    try:
        old = json.loads(R9B2J_JSON.read_text()) if R9B2J_JSON.is_file() else {}
        gates = old.get("gates", {})
        locks = (
            PREFIT_LOCK, R9B2J_POSTDATA_LOCK, R9B2J_REPAIR_PREFIT_LOCK,
            R9B2J_REPAIR_IMPL_LOCK, R9B2J_REPAIR_RUNNER_LOCK,
        )
        meta["ancestor_locks"] = {x: ancestor(x) for x in locks}
        meta["r9b2j_json_exists"] = R9B2J_JSON.is_file()
        meta["r9b2j_json_sha256"] = sha256(R9B2J_JSON) if R9B2J_JSON.is_file() else None
        meta["r9b2j_classification"] = old.get("classification")
        meta["r9b2j_gates"] = gates
        source_ok, source_meta = r9b.r8a.source_topology()
        meta["source_topology"] = source_meta
        expected_pass = (
            "R9B2J_J1_provenance", "R9B2J_J2_common_bounded_grid",
            "R9B2J_J3_eta0_closure_tau_invariance", "R9B2J_J4_response_resolution",
            "R9B2J_J5_epsilon_consistency",
        )
        ok = bool(
            all(meta["ancestor_locks"].values())
            and meta["r9b2j_json_sha256"] == R9B2J_SHA
            and old.get("classification") == R9B2J_CLASS
            and old.get("diagnostic_complete") is True
            and old.get("science_evaluated") is False
            and all(gates.get(x) is True for x in expected_pass)
            and gates.get("R9B2J_J6_cross_operator") is False
            and source_ok
        )
        return ok, meta
    except Exception as exc:
        meta["error"] = repr(exc)
        return False, meta


def _case(vals: dict, tier: str, tau: float, eta: float) -> dict:
    return vals[_vkey(tier, tau, eta)]


def _response_bundle(vals: dict, tier: str, tau: float):
    zc = _case(vals, tier, tau, 0.0)
    bases = {
        "linear8192": j.baseline(zc, "linear", 8192),
        "pchip8192": j.baseline(zc, "pchip", 8192),
    }
    resp = {"linear8192": {}, "pchip8192": {}}
    for name, mode in (("linear8192", "linear"), ("pchip8192", "pchip")):
        for eps in (EPS_PRIMARY, EPS_CONTROL):
            resp[name][str(eps)] = j.response(
                zc, _case(vals, tier, tau, +eps), _case(vals, tier, tau, -eps),
                eps, mode, 8192,
            )
    return bases, resp


def main(args) -> int:
    outpath = Path(args.json_out)
    work = Path(args.workdir); work.mkdir(parents=True, exist_ok=True)
    print("STABLE_AEST_DESI_DR1_R9B2K_START", flush=True)

    k1, prov = provenance()
    if not k1:
        _write(outpath, {
            "classification": FAIL_PROV, "diagnostic_complete": False,
            "science_evaluated": False, "desi_data_loaded": False,
            "gates": {"R9B2K_K1_provenance": False}, "provenance": prov,
        })
        print("STABLE_AEST_DESI_DR1_R9B2K_CLASSIFICATION=" + FAIL_PROV, flush=True)
        return 3

    vals = {}; runs = []
    specs = [("D1", 10.0, eta) for eta in ETAS]
    specs += [("D2", tau, eta) for tau in TAUS for eta in ETAS]
    mod = "fullj_weyl.stable_aest_desi_dr1_r9b2k_native_k_density_convergence"
    for tier, tau, eta in specs:
        cp = work / f"{_ckey(tier, tau, eta)}.pkl"
        reused = False; case = None
        if cp.is_file():
            try:
                with cp.open("rb") as f: case = pickle.load(f)
                reused = _checkpoint_ok(case, tier, tau, eta)
            except Exception:
                reused = False
        if not reused:
            print(f"STABLE_AEST_DESI_DR1_R9B2K_RUN tier={tier} tau={tau:g} eta={eta:+.3f}", flush=True)
            cmd = [
                sys.executable, "-u", "-m", mod, "--worker", "--tier", tier,
                "--tau", str(tau), "--eta", str(eta), "--out", str(cp),
            ]
            rc = subprocess.run(cmd, env=os.environ.copy()).returncode
            if rc != 0:
                _write(outpath, {
                    "classification": FAIL_RUN, "diagnostic_complete": False,
                    "science_evaluated": False, "desi_data_loaded": False,
                    "error": f"worker exit {rc}", "runs": runs, "provenance": prov,
                })
                return 2
            with cp.open("rb") as f: case = pickle.load(f)
            if not _checkpoint_ok(case, tier, tau, eta):
                _write(outpath, {
                    "classification": FAIL_RUN, "diagnostic_complete": False,
                    "science_evaluated": False, "desi_data_loaded": False,
                    "error": "invalid worker checkpoint", "runs": runs, "provenance": prov,
                })
                return 2
        vals[_vkey(tier, tau, eta)] = case
        nk = [int(len(r["state"]["kh"])) for r in case["rows"]]
        print(
            f"STABLE_AEST_DESI_DR1_R9B2K_CASE_READY tier={tier} tau={tau:g} eta={eta:+.3f} "
            f"reused={str(reused).lower()} nk={min(nk)}..{max(nk)}",
            flush=True,
        )
        runs.append({
            "tier": tier, "tau_H0": tau, "eta": eta, "ok": True,
            "checkpoint_reused": reused, "n_k_min": min(nk), "n_k_max": max(nk),
        })

    # K2: common central grids within each density and actual D1 -> D2 refinement.
    k2 = True; grid = []
    for tier, taus in (("D1", (10.0,)), ("D2", TAUS)):
        for tau in taus:
            zc = _case(vals, tier, tau, 0.0)
            for eps in (EPS_PRIMARY, EPS_CONTROL):
                pp = _case(vals, tier, tau, +eps); mm = _case(vals, tier, tau, -eps)
                for iz, z in enumerate(ZEFF):
                    ss = [i._row(x, iz)["state"] for x in (zc, pp, mm)]
                    same = i._same_k(*ss); st = ss[0]; kh = np.asarray(st["kh"], float)
                    healthy = bool(
                        same and kh.size >= 32 and np.all(np.isfinite(kh)) and np.all(np.diff(kh) > 0)
                        and kh[0] <= 2e-4 and kh[-1] >= 2.0
                        and np.all(np.isfinite(st["pdd"])) and np.all(np.asarray(st["pdd"]) > 0)
                        and np.all(np.isfinite(st["ptt"])) and np.all(np.asarray(st["ptt"]) > 0)
                    )
                    k2 &= healthy
                    grid.append({
                        "tier": tier, "tau_H0": tau, "epsilon": eps, "z": float(z),
                        "same_k": same, "healthy": healthy, "n_k": int(kh.size),
                        "kh_min": float(kh[0]), "kh_max": float(kh[-1]),
                    })
    refinement = []
    for iz, z in enumerate(ZEFF):
        n1 = len(i._row(_case(vals, "D1", 10.0, 0.0), iz)["state"]["kh"])
        n2 = len(i._row(_case(vals, "D2", 10.0, 0.0), iz)["state"]["kh"])
        passed = bool(n2 > n1 > DEFAULT_NK)
        k2 &= passed
        refinement.append({"z": float(z), "n_default_frozen": DEFAULT_NK, "n_D1": int(n1), "n_D2": int(n2), "pass": passed})

    # Build D1 tau10 and all D2 response bundles.
    bundles = {}
    try:
        bundles[("D1", 10.0)] = _response_bundle(vals, "D1", 10.0)
        for tau in TAUS:
            bundles[("D2", tau)] = _response_bundle(vals, "D2", tau)
    except Exception as exc:
        _write(outpath, {
            "classification": FAIL_RUN, "diagnostic_complete": False,
            "science_evaluated": False, "desi_data_loaded": False,
            "error": repr(exc), "runs": runs, "provenance": prov,
        })
        print(f"STABLE_AEST_DESI_DR1_R9B2K_RESPONSE_FAIL error={exc!r}", flush=True)
        return 2

    # K3: D2 eta0 closure and tau invariance.
    closure = {"sigma8_dd": 0.0, "f": 0.0}; tauvar = {q: 0.0 for q in ("sigma8_dd", "sigma8_tt", "f")}
    k3 = True
    for tau in TAUS:
        base = bundles[("D2", tau)][0]["linear8192"]
        case = _case(vals, "D2", tau, 0.0)
        for iz in range(len(ZEFF)):
            si = i._row(case, iz)["sigma_internal"]; gp = i._row(case, iz)["growth_proxy"]
            rd = abs(base["sigma8_dd"][iz] - si) / max(abs(base["sigma8_dd"][iz]), abs(si), 1e-300)
            rf = abs(base["f"][iz] - gp) / max(abs(base["f"][iz]), abs(gp), 1e-300)
            closure["sigma8_dd"] = max(closure["sigma8_dd"], rd)
            closure["f"] = max(closure["f"], rf)
            k3 &= bool(rd <= REL_GATE and rf <= REL_GATE)
    for iz in range(len(ZEFF)):
        for q in tauvar:
            a = np.asarray([bundles[("D2", t)][0]["linear8192"][q][iz] for t in TAUS], float)
            rv = (float(np.max(a)) - float(np.min(a))) / max(float(np.max(np.abs(a))), 1e-300)
            tauvar[q] = max(tauvar[q], rv); k3 &= bool(rv <= REL_GATE)

    # K4: D2 epsilon consistency for each operator and tau.
    epsilon_metrics = {"linear8192": {}, "pchip8192": {}}; k4 = True
    for tau in TAUS:
        resp = bundles[("D2", tau)][1]
        for name in epsilon_metrics:
            m = i.metrics(resp[name][str(EPS_PRIMARY)]["df"], resp[name][str(EPS_CONTROL)]["df"])
            epsilon_metrics[name][str(tau)] = m; k4 &= metric_pass(m)

    # K5: actual D1 -> D2 native-density convergence at tau=10.
    density_metrics = {"linear8192": {}, "pchip8192": {}}; k5 = True
    r1 = bundles[("D1", 10.0)][1]; r2 = bundles[("D2", 10.0)][1]
    for name in density_metrics:
        for eps in (EPS_PRIMARY, EPS_CONTROL):
            m = i.metrics(r1[name][str(eps)]["df"], r2[name][str(eps)]["df"])
            density_metrics[name][str(eps)] = m; k5 &= metric_pass(m)

    # K6: D2 linear-vs-PCHIP agreement for all tau and both epsilon values.
    cross_metrics = {}; k6 = True
    for tau in TAUS:
        resp = bundles[("D2", tau)][1]; cross_metrics[str(tau)] = {}
        for eps in (EPS_PRIMARY, EPS_CONTROL):
            m = i.metrics(resp["linear8192"][str(eps)]["df"], resp["pchip8192"][str(eps)]["df"])
            cross_metrics[str(tau)][str(eps)] = m; k6 &= metric_pass(m)

    gates = {
        "R9B2K_K1_provenance": True,
        "R9B2K_K2_native_grid_refinement": bool(k2),
        "R9B2K_K3_eta0_closure_tau_invariance": bool(k3),
        "R9B2K_K4_epsilon_consistency": bool(k4),
        "R9B2K_K5_native_density_convergence": bool(k5),
        "R9B2K_K6_cross_operator": bool(k6),
    }
    stageA = {
        "grid": grid, "refinement": refinement,
        "closure_max_rel": closure, "tau_variation_max_rel": tauvar,
        "epsilon_metrics": epsilon_metrics,
        "density_metrics": density_metrics,
        "cross_operator_metrics": cross_metrics,
    }
    print("STABLE_AEST_DESI_DR1_R9B2K_STAGE_A_GATES=" + json.dumps(gates, sort_keys=True), flush=True)
    print("STABLE_AEST_DESI_DR1_R9B2K_STAGE_A_METRICS=" + json.dumps({
        "refinement": refinement, "closure": closure, "tauvar": tauvar,
        "epsilon": epsilon_metrics, "density": density_metrics, "cross": cross_metrics,
    }, sort_keys=True), flush=True)

    fail = None
    if not k2: fail = FAIL_GRID
    elif not k3: fail = FAIL_CLOSURE
    elif not k4: fail = FAIL_EPS
    elif not k5: fail = FAIL_DENSITY
    elif not k6: fail = FAIL_CROSS
    if fail is not None:
        _write(outpath, {
            "classification": fail, "diagnostic_complete": True,
            "science_evaluated": False, "desi_data_loaded": False,
            "gates": gates, "stageA": stageA, "provenance": prov, "runs": runs,
            "settings": {
                "densities": {k: list(v) for k, v in DENSITIES.items()},
                "primary_response": "signed dP/deta linear in ln(k), 8192 nodes, Simpson",
                "control_response": "signed dP/deta PCHIP in ln(k), 8192 nodes, Simpson",
                "E_gate": E_GATE, "C_gate": C_GATE,
            },
            "interpretation": {
                "historical_failures_reclassified": False,
                "compressed_full_shape_corrected_projection_reportable": False,
                "observational_detection_claim_licensed": False,
            },
        })
        print("STABLE_AEST_DESI_DR1_R9B2K_CLASSIFICATION=" + fail, flush=True)
        return 1

    # Conditional Stage B: all CLASS subprocesses are gone before CAMB/ShapeFit construction.
    print("STABLE_AEST_DESI_DR1_R9B2K_STAGE_A_PASS_LOADING_DESI", flush=True)
    data_loaded = False
    try:
        data_dir = Path(args.data_dir).resolve(); official_repo = Path(args.official_repo).resolve()
        if not data_dir.is_dir() or not official_repo.is_dir():
            raise RuntimeError("missing DESI data/repository path")
        bins, d, C, offsets, data_hashes, _ = r9b.load_desi(data_dir, official_repo)
        data_loaded = True
        repo_head = subprocess.check_output(["git", "-C", str(official_repo), "rev-parse", "HEAD"], text=True).strip()
        eig = np.linalg.eigvalsh(C); ze = np.asarray([float(b["zeff"]) for b in bins], float)
        b1 = bool(
            repo_head == r9b.DESI_REPO_COMMIT and len(bins) == 6 and len(d) == 24
            and np.allclose(ze, ZEFF, rtol=0, atol=1e-12)
            and np.all(np.isfinite(d)) and np.all(np.isfinite(C))
            and np.allclose(C, C.T, rtol=0, atol=1e-12) and np.all(eig > 0)
        )
        data_meta = {
            "repo_head": repo_head, "files_sha256": data_hashes, "dimension": int(len(d)),
            "min_cov_eigenvalue": float(eig.min()),
            "bins": [{"namespace": b["namespace"], "zeff": b["zeff"], "parameters": b["parameters"]} for b in bins],
        }
    except Exception as exc:
        b1 = False; bins = []; d = C = offsets = None; data_meta = {"error": repr(exc)}
    gates["R9B2K_B1_desi_provenance"] = bool(b1)
    if not b1:
        _write(outpath, {
            "classification": FAIL_DATA, "diagnostic_complete": True,
            "science_evaluated": False, "desi_data_loaded": data_loaded,
            "gates": gates, "stageA": stageA, "data": data_meta,
            "provenance": prov, "runs": runs,
        })
        print("STABLE_AEST_DESI_DR1_R9B2K_CLASSIFICATION=" + FAIL_DATA, flush=True)
        return 1

    # Add ShapeFit scalars from the same saved D2 bounded source-state Pdd.
    fid, fcache = r9b._get_fiducial_cache(ZEFF)
    for tau in TAUS:
        for eta in ETAS:
            case = _case(vals, "D2", tau, eta)
            for row in case["rows"]:
                row["shape"] = r01.source_shape_saved(row, fid, fcache)
    gc.collect()

    full = {"linear8192": {}, "pchip8192": {}}
    fullm = {"epsilon": {}, "cross": {}}
    basevec = i._assemble_baseline(
        _case(vals, "D2", 10.0, 0.0), bundles[("D2", 10.0)][0]["linear8192"]["f"], bins,
    )
    b2 = bool(np.all(np.isfinite(basevec)))
    for tau in TAUS:
        s = str(tau); zc = _case(vals, "D2", tau, 0.0)
        full["linear8192"][s] = {}; full["pchip8192"][s] = {}
        for eps in (EPS_PRIMARY, EPS_CONTROL):
            pp = _case(vals, "D2", tau, +eps); mm = _case(vals, "D2", tau, -eps)
            for name in ("linear8192", "pchip8192"):
                resp = bundles[("D2", tau)][1][name][str(eps)]
                base = bundles[("D2", tau)][0][name]
                t = i._assemble_tangent(zc, pp, mm, resp, eps, base, bins)
                full[name][s][str(eps)] = t; b2 &= bool(np.all(np.isfinite(t)))
    gates["R9B2K_B2_shapefit_vector"] = bool(b2)

    b3 = True; b4 = True
    for tau in TAUS:
        s = str(tau)
        m = i.metrics(full["linear8192"][s][str(EPS_PRIMARY)], full["linear8192"][s][str(EPS_CONTROL)])
        fullm["epsilon"][s] = m; b3 &= metric_pass(m)
        fullm["cross"][s] = {}
        for eps in (EPS_PRIMARY, EPS_CONTROL):
            mc = i.metrics(full["linear8192"][s][str(eps)], full["pchip8192"][s][str(eps)])
            fullm["cross"][s][str(eps)] = mc; b4 &= metric_pass(mc)
    gates["R9B2K_B3_full_tangent_epsilon"] = bool(b3)
    gates["R9B2K_B4_full_cross_operator"] = bool(b4)

    projection = {}; b5 = bool(b2 and b3 and b4); b6 = bool(b5)
    if b5:
        for tau in TAUS:
            try:
                t = full["linear8192"][str(tau)][str(EPS_PRIMARY)]
                p = r9b.projection_summary(d, C, basevec, t, bins, offsets)
                projection[str(tau)] = p
                b5 &= bool(np.isfinite(p["F_perp"]) and p["F_perp"] > 0 and p["projection_idempotence_metric"] <= 1e-8)
                a = p["eta_hat_signed_matched_filter"]; bg = p["eta_hat_signed_gls"]
                b6 &= abs(a-bg) <= max(1e-10, 1e-8*max(abs(a), abs(bg), 1.0))
            except Exception as exc:
                projection[str(tau)] = {"error": repr(exc)}; b5 = False; b6 = False
    gates["R9B2K_B5_nuisance_projection"] = bool(b5)
    gates["R9B2K_B6_matched_filter_gls"] = bool(b6)

    if not b2: classification = FAIL_VEC
    elif not b3: classification = FAIL_FULL
    elif not b4: classification = FAIL_FULL_CROSS
    elif not b5: classification = FAIL_PROJ
    elif not b6: classification = FAIL_GLS
    else: classification = PASS

    result = {
        "classification": classification, "diagnostic_complete": True,
        "science_evaluated": True, "desi_data_loaded": True,
        "gates": gates, "stageA": stageA,
        "stageB": {"full_tangent_metrics": fullm, "tau_likelihood": projection},
        "data": data_meta, "provenance": prov, "runs": runs,
        "settings": {
            "densities": {k: list(v) for k, v in DENSITIES.items()},
            "tau_H0_grid": list(TAUS), "eta_grid": list(ETAS),
            "epsilon_primary": EPS_PRIMARY, "epsilon_control": EPS_CONTROL,
            "E_gate": E_GATE, "C_gate": C_GATE, "rel_gate": REL_GATE,
            "primary_response": "D2 signed dP/deta linear in ln(k), 8192 nodes, Simpson",
            "control_response": "D2 signed dP/deta PCHIP in ln(k), 8192 nodes, Simpson",
            "shapefit_power_source": "D2 bounded source-state Pdd; no CLASS pk_cb_lin in R9b2k path",
            "eta_physical_interval": [r9b.ETA_PHYS_MIN, r9b.ETA_PHYS_MAX],
        },
        "interpretation": {
            "historical_failures_reclassified": False,
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
        arrays[f"source_df_response_tau{tau:g}"] = bundles[("D2", tau)][1]["linear8192"][str(EPS_PRIMARY)]["df"]
    np.savez_compressed(args.npz_out, **arrays)
    print("STABLE_AEST_DESI_DR1_R9B2K_GATES=" + json.dumps(gates, sort_keys=True), flush=True)
    print("STABLE_AEST_DESI_DR1_R9B2K_PROJECTION=" + json.dumps(projection, sort_keys=True), flush=True)
    print("STABLE_AEST_DESI_DR1_R9B2K_CLASSIFICATION=" + classification, flush=True)
    return 0 if classification == PASS else 1


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--worker", action="store_true")
    ap.add_argument("--tier", choices=tuple(DENSITIES))
    ap.add_argument("--tau", type=float)
    ap.add_argument("--eta", type=float)
    ap.add_argument("--out")
    ap.add_argument("--data-dir", default=os.environ.get("AEST_R9B_DESI_DATA_DIR", ""))
    ap.add_argument("--official-repo", default=os.environ.get("AEST_R9B_DESI_REPO", ""))
    ap.add_argument("--json-out", default="results/stable_aest_desi_dr1_r9b2k_native_k_density_convergence.json")
    ap.add_argument("--npz-out", default="results/stable_aest_desi_dr1_r9b2k_native_k_density_convergence.npz")
    ap.add_argument("--workdir", default="results/stable_aest_desi_dr1_r9b2k_work")
    return ap.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if args.worker:
        if args.tier is None or args.tau is None or args.eta is None or args.out is None:
            raise SystemExit("worker requires --tier --tau --eta --out")
        raise SystemExit(worker(args))
    raise SystemExit(main(args))
