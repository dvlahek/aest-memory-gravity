#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fullj_weyl import stable_aest_observable_projection_r5b_derivative_zero as r5b

PREDATA_LOCK = "5d4c514799f22fe13cc0ecf9a0be4d3e2326a514"
R2E_POSTDATA_LOCK = "c0fe57f73a7785c21b1fecd7455f19148d5f812d"
R5B_POSTDATA_LOCK = "3242335ece23fbeb743f075a1df1aa70acaab211"
R6A_POSTDATA_LOCK = "540f8f85c618209abb509e3c9c7dc188698d8e25"
R5B_JSON = ROOT / "results/stable_aest_observable_projection_r5b_derivative_zero.json"
R5B_NPZ = ROOT / "results/stable_aest_observable_projection_r5b_derivative_zero.npz"
R5B_JSON_SHA256 = "26ce723e2b7b783fcd19765c9c7f01b6101992a3f09e6ee321299bf148259ca9"
R5B_NPZ_SHA256 = "a88f99254bc1a7393e40691d5dc539bb1e1648eae1b892e43b63f593f8e367e1"
R5B_CLASS = "STABLE_AEST_OBSERVABLE_PROJECTION_R5B_DERIVATIVE_ZERO_CERTIFIED"

TAU_H0 = 10.0
ORDER = 20
TOL = 3e-8
CANON_KH = 0.165
Z_OBS = np.asarray([0.2, 0.5, 1.0, 1.5, 2.0], float)
LMIN = 40
LMAX = 2000
FULL_LAMBDAS = (30.0, -30.0, 10.0, -10.0)
EPOCH_LAMBDA = 30.0
EPOCHS = ("ancient", "intermediate", "recent_structure", "late")
FORCE_SUM_TOL = 1e-12

CLS_INCOMPLETE = "STABLE_AEST_COSMIC_MEMORY_R7_INCOMPLETE"
CLS_PARENT = "STABLE_AEST_COSMIC_MEMORY_R7_PARENT_PROVENANCE_FAIL"
CLS_SOURCE = "STABLE_AEST_COSMIC_MEMORY_R7_SOURCE_TOPOLOGY_FAIL"
CLS_TRACE = "STABLE_AEST_COSMIC_MEMORY_R7_TRACE_PARTITION_FAIL"
CLS_LINEAR = "STABLE_AEST_COSMIC_MEMORY_R7_REPLAY_LINEARITY_FAIL"
CLS_BRIDGE = "STABLE_AEST_COSMIC_MEMORY_R7_PHYSICAL_BRIDGE_FAIL"
CLS_RECON = "STABLE_AEST_COSMIC_MEMORY_R7_EPOCH_RECONSTRUCTION_FAIL"
CLS_PASS = "STABLE_AEST_COSMIC_MEMORY_R7_LOOKBACK_DECOMPOSITION_CERTIFIED"

HOOK = "dy[pv->index_pt_E_aest] += aest_tangent_external_force(k,tau);"
TRACE = "aest_r2d_trace_force(k,pba->h,tau,-0.5*a*Q_aest*Bchi_aest/pba->aest_KB);"


def ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def rel(a, b) -> float:
    aa = np.asarray(a, float)
    bb = np.asarray(b, float)
    return float(np.linalg.norm(aa - bb) / max(float(np.linalg.norm(aa)), float(np.linalg.norm(bb)), 1e-300))


def cosine(a, b) -> float:
    aa = np.asarray(a, float)
    bb = np.asarray(b, float)
    na = float(np.linalg.norm(aa))
    nb = float(np.linalg.norm(bb))
    if na <= 0.0 or nb <= 0.0:
        return float("nan")
    return float(np.dot(aa, bb) / (na * nb))


def metric(a, b) -> dict:
    return {"E": rel(a, b), "C": cosine(a, b)}


def fractional_central(p, m, x0, lam: float):
    pp = np.asarray(p, float)
    mm = np.asarray(m, float)
    xx = np.asarray(x0, float)
    if np.any(~np.isfinite(xx)) or np.any(np.abs(xx) <= 1e-300):
        raise RuntimeError("non-finite or zero baseline in fractional tangent")
    return (pp - mm) / (2.0 * float(lam) * xx)


def source_audit() -> dict:
    root = Path(os.environ.get("AEST_STABLE_R7_CLASS_ROOT", ""))
    pc = root / "source" / "perturbations.c"
    am = root / "source" / "aest_memory.c"
    if not pc.is_file() or not am.is_file():
        return {"pass": False, "reason": "missing R7 CLASS source"}
    p = pc.read_text()
    a = am.read_text()
    deriv_start = p.find("int perturbations_derivs(")
    if deriv_start < 0:
        return {"pass": False, "reason": "perturbations_derivs missing"}
    deriv = p[deriv_start:]
    checks = {
        "stable_marker": "FULLJ_AEST_STABLE_CHI_RESIDUAL_V1" in p,
        "r2d_marker": "FULLJ_STABLE_AEST_R2D_FULL_HISTORY_V1" in p,
        "r2e_marker": "FULLJ_STABLE_AEST_R2E_SINGLE_HOOK_V1" in p,
        "stable_chi": ("double chi_aest = Q_aest*s_aest;" in deriv or "double chi_aest=Q_aest*s_aest;" in deriv),
        "physical_eta_multiply_once": deriv.count("Bchi_aest *= pba->aest_eta;") == 1,
        "physical_closure_once": deriv.count("E_rhs_aest -= 0.5*Q_aest*Bchi_aest;") == 1,
        "r2d_trace_once": deriv.count(TRACE) == 1,
        "external_hook_once": deriv.count(HOOK) == 1,
        "external_helper_once": len(re.findall(r"\bdouble\s+aest_tangent_external_force\s*\(", a)) == 1,
    }
    return {
        "pass": bool(all(checks.values())),
        "checks": checks,
        "eta_multiply_count": deriv.count("Bchi_aest *= pba->aest_eta;"),
        "physical_closure_count": deriv.count("E_rhs_aest -= 0.5*Q_aest*Bchi_aest;"),
        "r2d_trace_count": deriv.count(TRACE),
        "external_hook_count": deriv.count(HOOK),
        "external_helper_defs": len(re.findall(r"\bdouble\s+aest_tangent_external_force\s*\(", a)),
    }


def _background_tau_z(c):
    bg = c.get_background()
    zkey = "z" if "z" in bg else None
    tau_candidates = [k for k in bg.keys() if "conf" in k.lower() and "time" in k.lower()]
    if zkey is None or len(tau_candidates) != 1:
        raise RuntimeError(f"background tau/z keys unresolved: z={zkey}, tau_candidates={tau_candidates}")
    tau = np.asarray(bg[tau_candidates[0]], float)
    z = np.asarray(bg[zkey], float)
    good = np.isfinite(tau) & np.isfinite(z)
    tau = tau[good]
    z = z[good]
    order = np.argsort(tau)
    tau = tau[order]
    z = z[order]
    keep = np.ones(tau.size, dtype=bool)
    if tau.size > 1:
        keep[1:] = np.diff(tau) > 0.0
    tau = tau[keep]
    z = z[keep]
    if tau.size < 10 or np.any(np.diff(tau) <= 0.0):
        raise RuntimeError("invalid background conformal-time grid")
    return tau, z, tau_candidates[0]


def build_params():
    params, bits, pos = r5b.build_params(0.0, TOL)
    params["aest_memory_enabled"] = "yes"
    params["aest_memory_order"] = int(ORDER)
    params["aest_eta"] = 0.0
    params["aest_tau_H0"] = float(TAU_H0)
    params["tol_perturbations_integration"] = float(TOL)
    params["output"] = "mPk,lCl"
    params["z_max_pk"] = 2.2
    params["P_k_max_h/Mpc"] = 5.0
    params["l_max_scalars"] = int(LMAX)
    params.pop("non_linear", None)
    params.pop("lensing", None)
    return params, bits, pos


def run_case():
    from classy import Class
    params, bits, pos = build_params()
    c = Class()
    c.set(params)
    c.compute()
    try:
        sigma8 = np.asarray([float(c.sigma(8.0, float(z), h_units=True)) for z in Z_OBS], float)
        fsigma8 = np.asarray([float(c.effective_f_sigma8(float(z), z_step=0.1)) for z in Z_OBS], float)
        raw = c.raw_cl(lmax=int(LMAX))
        if "pp" not in raw:
            raise RuntimeError("CLASS raw_cl has no pp")
        pp = np.asarray(raw["pp"], float)
        ell_all = np.arange(pp.size, dtype=float)
        sel = (ell_all >= LMIN) & (ell_all <= LMAX)
        ell = ell_all[sel]
        ckk = ((ell * (ell + 1.0) / 2.0) ** 2) * pp[sel]
        bg_tau, bg_z, bg_tau_key = _background_tau_z(c)
        finite = bool(
            np.all(np.isfinite(sigma8)) and np.all(np.isfinite(fsigma8)) and
            np.all(np.isfinite(ckk)) and np.all(np.isfinite(bg_tau)) and np.all(np.isfinite(bg_z))
        )
        positive = bool(np.all(sigma8 > 0.0) and np.all(ckk > 0.0))
        return {
            "sigma8": sigma8,
            "fsigma8": fsigma8,
            "ckk": ckk,
            "ell": ell,
            "bg_tau": bg_tau,
            "bg_z": bg_z,
            "bg_tau_key": bg_tau_key,
            "finite": finite,
            "positive": positive,
            "bits": int(bits),
            "target_pos": int(pos),
        }
    finally:
        c.struct_cleanup()
        c.empty()


def save_case(path: Path, v: dict):
    np.savez_compressed(
        path,
        sigma8=v["sigma8"], fsigma8=v["fsigma8"], ckk=v["ckk"], ell=v["ell"],
        bg_tau=v["bg_tau"], bg_z=v["bg_z"], bg_tau_key=np.asarray([v["bg_tau_key"]]),
        finite=np.asarray([int(v["finite"])]), positive=np.asarray([int(v["positive"])]),
        bits=np.asarray([v["bits"]]), target_pos=np.asarray([v["target_pos"]]),
    )


def load_case(path: Path) -> dict:
    q = np.load(path)
    return {
        "sigma8": np.asarray(q["sigma8"], float),
        "fsigma8": np.asarray(q["fsigma8"], float),
        "ckk": np.asarray(q["ckk"], float),
        "ell": np.asarray(q["ell"], float),
        "bg_tau": np.asarray(q["bg_tau"], float),
        "bg_z": np.asarray(q["bg_z"], float),
        "bg_tau_key": str(q["bg_tau_key"][0]),
        "finite": bool(int(q["finite"][0])),
        "positive": bool(int(q["positive"][0])),
    }


def normalize_force(raw: Path, clean: Path) -> dict:
    sorted_path = clean.with_suffix(".sorted.tmp")
    subprocess.run(["sort", "-g", "-k1,1", "-k2,2", str(raw), "-o", str(sorted_path)], check=True)
    raw_rows = 0
    unique_rows = 0
    k_count = 0
    max_dup_rel = 0.0
    tau_min = float("inf")
    tau_max = -float("inf")
    force_sq = 0.0
    force_max = 0.0
    last_k = last_tau = None
    vals = []

    def emit(fp, k, tau, vv):
        nonlocal unique_rows, k_count, max_dup_rel, tau_min, tau_max, force_sq, force_max, last_emitted_k
        arr = np.asarray(vv, float)
        mean = float(np.mean(arr))
        denom = max(abs(mean), float(np.max(np.abs(arr))), 1e-300)
        spread = float(np.max(np.abs(arr - mean)) / denom)
        max_dup_rel = max(max_dup_rel, spread)
        fp.write(f"{k:.17g} {tau:.17g} {mean:.17g}\n")
        unique_rows += 1
        if last_emitted_k is None or k != last_emitted_k:
            k_count += 1
            last_emitted_k = k
        tau_min = min(tau_min, tau)
        tau_max = max(tau_max, tau)
        force_sq += mean * mean
        force_max = max(force_max, abs(mean))

    last_emitted_k = None
    with sorted_path.open("r", errors="replace") as src, clean.open("w") as out:
        for line in src:
            p = line.split()
            if len(p) != 3:
                continue
            try:
                k, tau, f = map(float, p)
            except ValueError:
                continue
            if not (np.isfinite(k) and np.isfinite(tau) and np.isfinite(f)):
                continue
            raw_rows += 1
            if last_k is None:
                last_k, last_tau, vals = k, tau, [f]
            elif k == last_k and tau == last_tau:
                vals.append(f)
            else:
                emit(out, last_k, last_tau, vals)
                last_k, last_tau, vals = k, tau, [f]
        if last_k is not None:
            emit(out, last_k, last_tau, vals)
    sorted_path.unlink(missing_ok=True)
    if unique_rows == 0:
        raise RuntimeError("normalized force table is empty")
    return {
        "raw_rows": raw_rows,
        "unique_rows": unique_rows,
        "k_count": k_count,
        "tau_min": tau_min,
        "tau_max": tau_max,
        "force_l2": math.sqrt(force_sq),
        "force_max_abs": force_max,
        "max_duplicate_relative_spread": max_dup_rel,
        "sha256": sha256(clean),
        "bytes": clean.stat().st_size,
    }


def epoch_of_z(z: float) -> str:
    if z >= 10.0:
        return "ancient"
    if z >= 2.0:
        return "intermediate"
    if z >= 0.5:
        return "recent_structure"
    return "late"


def partition_force(clean: Path, bg_tau: np.ndarray, bg_z: np.ndarray, work: Path) -> tuple[dict, dict[str, Path]]:
    paths = {e: work / f"force_{e}.dat" for e in EPOCHS}
    fps = {e: paths[e].open("w") for e in EPOCHS}
    counts = {e: 0 for e in EPOCHS}
    sq = {e: 0.0 for e in EPOCHS}
    rows = 0
    finite_z = True
    exactly_one = True
    max_abs_full = 0.0
    max_abs_recon = 0.0
    tau_min = float("inf")
    tau_max = -float("inf")
    try:
        with clean.open("r") as src:
            for line in src:
                p = line.split()
                if len(p) != 3:
                    continue
                k, tau, f = map(float, p)
                rows += 1
                tau_min = min(tau_min, tau)
                tau_max = max(tau_max, tau)
                z = float(np.interp(tau, bg_tau, bg_z))
                finite_z &= bool(np.isfinite(z))
                e = epoch_of_z(z)
                masks = {name: (1.0 if name == e else 0.0) for name in EPOCHS}
                exactly_one &= (sum(int(v > 0.5) for v in masks.values()) == 1)
                vals = {}
                for name in EPOCHS:
                    fv = f * masks[name]
                    vals[name] = fv
                    fps[name].write(f"{k:.17g} {tau:.17g} {fv:.17g}\n")
                    if masks[name] > 0.5:
                        counts[name] += 1
                    sq[name] += fv * fv
                err = abs(sum(vals.values()) - f)
                max_abs_full = max(max_abs_full, abs(f))
                max_abs_recon = max(max_abs_recon, err)
    finally:
        for fp in fps.values():
            fp.close()

    coverage = bool(
        bg_tau.size >= 10 and tau_min >= float(bg_tau[0]) and tau_max <= float(bg_tau[-1])
    )
    sum_rel = max_abs_recon / max(max_abs_full, 1e-300)
    tables = {}
    for e in EPOCHS:
        tables[e] = {
            "path": str(paths[e]),
            "rows": rows,
            "active_rows": counts[e],
            "active_fraction": counts[e] / max(rows, 1),
            "force_l2": math.sqrt(sq[e]),
            "sha256": sha256(paths[e]),
            "bytes": paths[e].stat().st_size,
        }
    meta = {
        "rows": rows,
        "background_tau_min": float(bg_tau[0]),
        "background_tau_max": float(bg_tau[-1]),
        "force_tau_min": tau_min,
        "force_tau_max": tau_max,
        "background_covers_force": coverage,
        "finite_redshift_mapping": finite_z,
        "exactly_one_epoch_per_row": exactly_one,
        "max_abs_reconstruction_error": max_abs_recon,
        "scale_aware_relative_reconstruction_error": sum_rel,
        "tables": tables,
    }
    return meta, paths


def contribution_metrics(parts: dict[str, np.ndarray], full: np.ndarray) -> dict:
    f = np.asarray(full, float)
    f2 = float(np.dot(f, f))
    norms = {e: float(np.linalg.norm(np.asarray(parts[e], float))) for e in EPOCHS}
    norm_sum = max(sum(norms.values()), 1e-300)
    out = {}
    for e in EPOCHS:
        v = np.asarray(parts[e], float)
        proj = float(np.dot(v, f) / f2) if f2 > 0.0 else float("nan")
        out[e] = {
            "signed_projection_fraction": proj,
            "norm_share": norms[e] / norm_sum,
            "cosine_with_full": cosine(v, f),
            "tangent_norm": norms[e],
        }
    out["sum_signed_projection_fraction"] = float(sum(out[e]["signed_projection_fraction"] for e in EPOCHS))
    return out


def run_worker_subprocess(module: str, out: Path, env: dict):
    subprocess.run(
        [sys.executable, "-m", module, "--worker", "--out", str(out)],
        cwd=ROOT,
        env=env,
        check=True,
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--worker", action="store_true")
    ap.add_argument("--out")
    ap.add_argument("--json-out", default="results/stable_aest_cosmic_memory_r7_lookback_decomposition.json")
    ap.add_argument("--npz-out", default="results/stable_aest_cosmic_memory_r7_lookback_decomposition.npz")
    ap.add_argument("--workdir", default="results/stable_aest_cosmic_memory_r7_lookback_work")
    args = ap.parse_args()

    if args.worker:
        if not args.out:
            raise SystemExit("--worker requires --out")
        v = run_case()
        save_case(Path(args.out), v)
        print(json.dumps({"finite": v["finite"], "positive": v["positive"], "bg_tau_key": v["bg_tau_key"]}, sort_keys=True))
        return 0 if v["finite"] and v["positive"] else 2

    print("STABLE_AEST_COSMIC_MEMORY_R7_START", flush=True)
    work = Path(args.workdir)
    work.mkdir(parents=True, exist_ok=True)

    parent_exists = R5B_JSON.is_file() and R5B_NPZ.is_file()
    parent = json.loads(R5B_JSON.read_text()) if parent_exists else {}
    json_sha = sha256(R5B_JSON) if R5B_JSON.is_file() else ""
    npz_sha = sha256(R5B_NPZ) if R5B_NPZ.is_file() else ""
    g1 = bool(
        ancestor(PREDATA_LOCK) and ancestor(R2E_POSTDATA_LOCK) and ancestor(R5B_POSTDATA_LOCK)
        and ancestor(R6A_POSTDATA_LOCK) and parent_exists
        and json_sha == R5B_JSON_SHA256 and npz_sha == R5B_NPZ_SHA256
        and parent.get("classification") == R5B_CLASS
        and parent.get("diagnostic_complete") is True
        and all(bool(v) for v in parent.get("gates", {}).values())
    )

    src = source_audit()
    g2 = bool(src.get("pass"))
    print("STABLE_AEST_COSMIC_MEMORY_R7_SOURCE " + json.dumps(src, sort_keys=True), flush=True)

    module = "fullj_weyl.stable_aest_cosmic_memory_r7_lookback_decomposition"
    base_out = work / "baseline_trace.npz"
    raw_force = work / "force_full_raw.dat"
    clean_force = work / "force_full.dat"

    env = os.environ.copy()
    for key in (
        "AEST_TANGENT_FORCE_FILE", "AEST_TANGENT_LAMBDA", "AEST_TANGENT_TRACE_FILE",
        "AEST_R2D_TRACE_FILE", "AEST_R2D_TRACE_KH", "AEST_R2D_TRACE_ALL_K",
        "AEST_TANGENT_ALLOW_K_MISS",
    ):
        env.pop(key, None)
    env["AEST_R2D_TRACE_FILE"] = str(raw_force.resolve())
    env["AEST_R2D_TRACE_ALL_K"] = "1"

    trace_meta = {}
    partition_meta = {}
    epoch_paths = {}
    baseline = None
    g3 = False
    try:
        run_worker_subprocess(module, base_out, env)
        baseline = load_case(base_out)
        norm_meta = normalize_force(raw_force, clean_force)
        partition_meta, epoch_paths = partition_force(clean_force, baseline["bg_tau"], baseline["bg_z"], work)
        trace_meta = {"normalized": norm_meta, "partition": partition_meta, "background_tau_key": baseline["bg_tau_key"]}
        g3 = bool(
            baseline["finite"] and baseline["positive"]
            and norm_meta["k_count"] > 1 and norm_meta["unique_rows"] > 1000
            and partition_meta["background_covers_force"]
            and partition_meta["finite_redshift_mapping"]
            and partition_meta["exactly_one_epoch_per_row"]
            and all(partition_meta["tables"][e]["rows"] == norm_meta["unique_rows"] for e in EPOCHS)
            and partition_meta["scale_aware_relative_reconstruction_error"] <= FORCE_SUM_TOL
        )
    except Exception as exc:
        trace_meta = {"error": repr(exc)}
        print("STABLE_AEST_COSMIC_MEMORY_R7_TRACE_FAIL " + repr(exc), flush=True)

    print("STABLE_AEST_COSMIC_MEMORY_R7_TRACE " + json.dumps(trace_meta, sort_keys=True), flush=True)

    cases = {}
    run_rows = []
    all_replays = g3
    if g3:
        specs = []
        for lam in FULL_LAMBDAS:
            specs.append((f"full_{'p' if lam > 0 else 'm'}{int(abs(lam))}", clean_force, lam))
        for e in EPOCHS:
            specs.append((f"{e}_p30", epoch_paths[e], 30.0))
            specs.append((f"{e}_m30", epoch_paths[e], -30.0))

        for name, force_path, lam in specs:
            out = work / f"case_{name}.npz"
            e = os.environ.copy()
            for key in (
                "AEST_TANGENT_TRACE_FILE", "AEST_R2D_TRACE_FILE", "AEST_R2D_TRACE_KH",
                "AEST_R2D_TRACE_ALL_K", "AEST_TANGENT_ALLOW_K_MISS",
            ):
                e.pop(key, None)
            e["AEST_TANGENT_FORCE_FILE"] = str(force_path.resolve())
            e["AEST_TANGENT_LAMBDA"] = str(lam)
            try:
                run_worker_subprocess(module, out, e)
                v = load_case(out)
                ok = bool(v["finite"] and v["positive"])
                all_replays &= ok
                cases[name] = v
                run_rows.append({"name": name, "lambda": lam, "force_table": force_path.name, "finite": v["finite"], "positive": v["positive"]})
                print(f"STABLE_AEST_COSMIC_MEMORY_R7_RUN name={name} lambda={lam:g} finite={v['finite']} positive={v['positive']}", flush=True)
            except Exception as exc:
                all_replays = False
                run_rows.append({"name": name, "lambda": lam, "force_table": force_path.name, "finite": False, "error": repr(exc)})
                print(f"STABLE_AEST_COSMIC_MEMORY_R7_RUN_FAIL name={name} error={exc!r}", flush=True)

    arrays = {"z": Z_OBS}
    full_metrics = {}
    bridge_metrics = {}
    reconstruction_metrics = {}
    contributions = {}
    late_z02 = {}
    baseline_bridge = {}
    g4 = g5 = g6 = False

    if all_replays and baseline is not None and len(cases) == 12:
        parent_npz = np.load(R5B_NPZ)
        arrays["ell"] = baseline["ell"]
        for key in ("sigma8", "fsigma8", "ckk"):
            arrays[f"baseline_{key}"] = baseline[key]
            p30 = cases["full_p30"][key]
            m30 = cases["full_m30"][key]
            p10 = cases["full_p10"][key]
            m10 = cases["full_m10"][key]
            T30 = fractional_central(p30, m30, baseline[key], 30.0)
            T10 = fractional_central(p10, m10, baseline[key], 10.0)
            full_metrics[key] = metric(T10, T30)
            arrays[f"T_full30_{key}"] = T30
            arrays[f"T_full10_{key}"] = T10

            pref = np.asarray(parent_npz[f"T_{key}_eta0p01"], float)
            bridge_metrics[key] = metric(T30, pref)
            arrays[f"T_parent_r5b_{key}"] = pref
            parent_base = np.asarray(parent_npz[f"{key}_nominal_e0"], float)
            baseline_bridge[key] = metric(baseline[key], parent_base)

            parts = {}
            for ep in EPOCHS:
                Tp = cases[f"{ep}_p30"][key]
                Tm = cases[f"{ep}_m30"][key]
                Ti = fractional_central(Tp, Tm, baseline[key], 30.0)
                parts[ep] = Ti
                arrays[f"T_{ep}_{key}"] = Ti
            Tsum = np.sum(np.stack([parts[e] for e in EPOCHS], axis=0), axis=0)
            arrays[f"T_sum_{key}"] = Tsum
            reconstruction_metrics[key] = metric(Tsum, T30)
            contributions[key] = contribution_metrics(parts, T30)
            if key in ("sigma8", "fsigma8"):
                denom = float(T30[0])
                late_z02[key] = {
                    ep: (float(parts[ep][0] / denom) if abs(denom) > 1e-300 else float("nan"))
                    for ep in EPOCHS
                }
                late_z02[key]["sum"] = float(sum(late_z02[key][ep] for ep in EPOCHS))

        g4 = bool(all(m["E"] <= 0.05 and m["C"] >= 0.995 for m in full_metrics.values()))
        g5 = bool(all(m["E"] <= 0.10 and m["C"] >= 0.995 for m in bridge_metrics.values()))
        g6 = bool(all(m["E"] <= 0.02 and m["C"] >= 0.999 for m in reconstruction_metrics.values()))

    gates = {
        "R7_G1_provenance_and_parent_lock": g1,
        "R7_G2_single_hook_full_history_source_topology": g2,
        "R7_G3_trace_and_epoch_partition_integrity": g3,
        "R7_G4_full_replay_amplifier_consistency": g4,
        "R7_G5_physical_derivative_bridge": g5,
        "R7_G6_epoch_reconstruction": g6,
    }

    if not g1:
        cls = CLS_PARENT
    elif not g2:
        cls = CLS_SOURCE
    elif not g3:
        cls = CLS_TRACE
    elif not g4:
        cls = CLS_LINEAR
    elif not g5:
        cls = CLS_BRIDGE
    elif not g6:
        cls = CLS_RECON
    else:
        cls = CLS_PASS

    manifest = {
        "full_force": {
            "path": str(clean_force),
            "sha256": sha256(clean_force) if clean_force.is_file() else None,
            "bytes": clean_force.stat().st_size if clean_force.is_file() else None,
        },
        "epochs": {
            e: {
                "path": str(epoch_paths[e]),
                "sha256": sha256(epoch_paths[e]) if e in epoch_paths and epoch_paths[e].is_file() else None,
                "bytes": epoch_paths[e].stat().st_size if e in epoch_paths and epoch_paths[e].is_file() else None,
            }
            for e in EPOCHS
        },
    }
    (work / "force_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")

    out = {
        "classification": cls,
        "diagnostic_complete": True,
        "predata_lock": PREDATA_LOCK,
        "parents": {
            "r2e_postdata_lock": R2E_POSTDATA_LOCK,
            "r5b_postdata_lock": R5B_POSTDATA_LOCK,
            "r6a_postdata_lock": R6A_POSTDATA_LOCK,
            "r5b_classification": parent.get("classification"),
            "r5b_json_sha256": json_sha,
            "r5b_npz_sha256": npz_sha,
        },
        "settings": {
            "tau_H0": TAU_H0,
            "memory_order": ORDER,
            "tol": TOL,
            "physical_eta": 0.0,
            "canonical_initialization_k_h": CANON_KH,
            "observable_redshifts": Z_OBS.tolist(),
            "L_min": LMIN,
            "L_max": LMAX,
            "full_lambdas": list(FULL_LAMBDAS),
            "epoch_lambda": EPOCH_LAMBDA,
            "epochs": {
                "ancient": "z >= 10",
                "intermediate": "2 <= z < 10",
                "recent_structure": "0.5 <= z < 2",
                "late": "z < 0.5",
            },
            "nonlinear_halofit": False,
        },
        "source_topology": src,
        "trace_partition": trace_meta,
        "runs": run_rows,
        "baseline_vs_r5b": baseline_bridge,
        "full_replay_amplifier_metrics": full_metrics,
        "physical_r5b_bridge_metrics": bridge_metrics,
        "epoch_reconstruction_metrics": reconstruction_metrics,
        "epoch_contributions": contributions,
        "late_z0p2_signed_epoch_fractions": late_z02,
        "gates": gates,
        "interpretation": {
            "lookback_decomposition_licensed": cls == CLS_PASS,
            "epoch_fractions_reportable": cls == CLS_PASS,
            "universal_entire_universe_memory_claim_licensed": False,
            "observational_detection_claim_licensed": False,
            "tau_generality_claim_licensed": False,
        },
    }
    Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    np.savez_compressed(args.npz_out, **arrays)

    summary = {
        "classification": cls,
        "gates": gates,
        "full_replay_amplifier_metrics": full_metrics,
        "physical_r5b_bridge_metrics": bridge_metrics,
        "epoch_reconstruction_metrics": reconstruction_metrics,
        "epoch_contributions": contributions,
        "late_z0p2_signed_epoch_fractions": late_z02,
    }
    print("STABLE_AEST_COSMIC_MEMORY_R7_GATES=" + json.dumps(gates, sort_keys=True), flush=True)
    print("STABLE_AEST_COSMIC_MEMORY_R7_SUMMARY=" + json.dumps(summary, sort_keys=True), flush=True)
    print("STABLE_AEST_COSMIC_MEMORY_R7_CLASSIFICATION=" + cls, flush=True)
    return 0 if cls == CLS_PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
