#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fullj_weyl import stable_aest_cosmic_memory_r8a_tau_amplitude_scan as r8a
from fullj_weyl import stable_aest_observable_projection_r5b_derivative_zero as r5b

PREFIT_LOCK = "63f4bea97c95a5627f659415f556636c1af21fad"
R7A_POSTDATA_LOCK = "86c03e6ba2ee9fcbf33a9d319d12ae778a747881"
R8A2_POSTDATA_LOCK = "590dbc69e2823f583b157af2297e357991103c47"
R8B_POSTDATA_LOCK = "9e21c61210979ab841918ba16f2210020daa245a"
R7A_CLASS = "STABLE_AEST_COSMIC_MEMORY_R7A_LIVE_LOOKBACK_DECOMPOSITION_CERTIFIED"
R8A2_CLASS = "STABLE_AEST_COSMIC_MEMORY_R8A2_TAU_GENERALITY_CERTIFIED"
R8B_CLASS = "STABLE_AEST_COSMIC_MEMORY_R8B_TWO_TAU_LOOKBACK_CERTIFIED"

R8B_JSON_SHA256 = "925d882609149720dc84360142085038953384b548f22945ddc58fdb83a6d861"
R8B_NPZ_SHA256 = "a9aaba1f0daf635358a24832bd5ccc3d606a6e70e65b4aa186dd0117ba757fa4"

BOSS_REPO_COMMIT = "bb0c1c9009dc76d1391300e169e8df38fd1096db"
BOSS_DATA_SHA256 = "eae45d2629dc1214b351716b3ff9a6f5a22f170b71e3d0e93aeeddc169d80e30"
BOSS_COV_SHA256 = "dea6d8d4893d2b84772f9b83d0653bf7d4ee81a0aeb63ce04859e20d0ad3a289"
BOSS_DATA_NAME = "sdss_DR12Consensus_final.dat"
BOSS_COV_NAME = "final_consensus_covtot_dM_Hz_fsig.txt"
Z_BOSS = np.asarray([0.38, 0.51, 0.61], dtype=float)
FS_INDICES = np.asarray([2, 5, 8], dtype=int)
TAUS = (10.0, 5.0, 2.5, 1.25)
EPS_PRIMARY = 0.025
EPS_CONTROL = 0.05
TOL = 3e-8
OBS = "fsigma8"
ETA_PHYS_MIN = 0.0
ETA_PHYS_MAX = 0.05

R7A_JSON = ROOT / "results/stable_aest_cosmic_memory_r7a_live_epoch_derivative.json"
R8A2_JSON = ROOT / "results/stable_aest_cosmic_memory_r8a2_precision_qualified_tau_scan.json"
R8B_JSON = ROOT / "results/stable_aest_cosmic_memory_r8b_two_tau_lookback.json"
R8B_NPZ = ROOT / "results/stable_aest_cosmic_memory_r8b_two_tau_lookback.npz"

CLS_INCOMPLETE = "STABLE_AEST_BOSS_DR12_R9A_INCOMPLETE"
CLS_PARENT = "STABLE_AEST_BOSS_DR12_R9A_PARENT_PROVENANCE_FAIL"
CLS_SOURCE = "STABLE_AEST_BOSS_DR12_R9A_SOURCE_TOPOLOGY_FAIL"
CLS_RUN = "STABLE_AEST_BOSS_DR12_R9A_THEORY_RUN_FAIL"
CLS_CENTRAL = "STABLE_AEST_BOSS_DR12_R9A_CENTRAL_DERIVATIVE_FAIL"
CLS_ALG = "STABLE_AEST_BOSS_DR12_R9A_LIKELIHOOD_ALGEBRA_FAIL"
CLS_GLS = "STABLE_AEST_BOSS_DR12_R9A_MATCHED_FILTER_GLS_FAIL"
CLS_PASS = "STABLE_AEST_BOSS_DR12_R9A_GROWTH_TEMPLATE_PROJECTION_CERTIFIED"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"], cwd=ROOT,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    ).returncode == 0


def load_boss(data_dir: Path):
    dp = data_dir / BOSS_DATA_NAME
    cp = data_dir / BOSS_COV_NAME
    if not dp.is_file() or not cp.is_file():
        raise FileNotFoundError("missing pinned BOSS data files")
    if sha256(dp) != BOSS_DATA_SHA256:
        raise RuntimeError("BOSS data SHA256 mismatch")
    if sha256(cp) != BOSS_COV_SHA256:
        raise RuntimeError("BOSS covariance SHA256 mismatch")

    vals = []
    zs = []
    obs = []
    for line in dp.read_text().splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        p = line.split()
        if len(p) != 3:
            raise RuntimeError("unexpected BOSS data row")
        zs.append(float(p[0])); vals.append(float(p[1])); obs.append(p[2])
    zs = np.asarray(zs, float); vals = np.asarray(vals, float)
    cov9 = np.loadtxt(cp, dtype=float)
    if zs.size != 9 or vals.size != 9 or cov9.shape != (9, 9):
        raise RuntimeError("unexpected BOSS data/covariance dimensions")
    if [obs[i] for i in FS_INDICES] != ["f_sigma8"] * 3:
        raise RuntimeError("BOSS f_sigma8 ordering mismatch")
    z = zs[FS_INDICES]
    d = vals[FS_INDICES]
    C = cov9[np.ix_(FS_INDICES, FS_INDICES)]
    if not np.allclose(z, Z_BOSS, rtol=0.0, atol=1e-14):
        raise RuntimeError("BOSS redshift mismatch")
    return z, d, C, cov9


def run_case(eta: float, tau: float):
    from classy import Class
    params, bits, pos = r5b.build_params(float(eta), float(TOL))
    params["aest_tau_H0"] = float(tau)
    c = Class(); c.set(params); c.compute()
    try:
        fs = np.asarray([float(c.effective_f_sigma8(float(z), z_step=0.1)) for z in Z_BOSS], float)
        finite = bool(np.all(np.isfinite(fs)))
        positive = bool(np.all(fs > 0.0))
        return {"fsigma8": fs, "finite": finite, "domain_positive": positive,
                "bits": int(bits), "target_pos": int(pos)}
    finally:
        c.struct_cleanup(); c.empty()


def save_case(path: Path, v: dict):
    np.savez_compressed(
        path, fsigma8=v["fsigma8"], z=Z_BOSS,
        finite=np.asarray([int(v["finite"])]), positive=np.asarray([int(v["domain_positive"])]),
        bits=np.asarray([v["bits"]]), target_pos=np.asarray([v["target_pos"]]),
    )


def load_case(path: Path):
    q = np.load(path)
    return {
        "fsigma8": np.asarray(q["fsigma8"], float), "z": np.asarray(q["z"], float),
        "finite": bool(int(q["finite"][0])), "domain_positive": bool(int(q["positive"][0])),
        "bits": int(q["bits"][0]), "target_pos": int(q["target_pos"][0]),
    }


def qform(x, P):
    x = np.asarray(x, float)
    return float(x @ P @ x)


def gls_two_column(d, a, t, P):
    X = np.column_stack([a, t])
    M = X.T @ P @ X
    rhs = X.T @ P @ d
    beta = np.linalg.solve(M, rhs)
    return float(beta[0]), float(beta[1]), M


def likelihood_summary(d, C, b, T):
    P = np.linalg.inv(C)
    a = np.asarray(b, float)
    t = a * np.asarray(T, float)
    r = d - a
    aa = float(a @ P @ a)
    tt = float(t @ P @ t)
    at = float(a @ P @ t)
    if aa <= 0 or tt <= 0:
        raise RuntimeError("non-positive raw Fisher geometry")
    proj = at / aa
    tperp = t - proj * a
    Fperp = float(tperp @ P @ tperp)
    rho = float(at / np.sqrt(aa * tt))
    if Fperp <= 0:
        raise RuntimeError("non-positive deprojected Fisher information")

    eta_mf = float((tperp @ P @ r) / Fperp)
    A_gls, eta_gls, M = gls_two_column(d, a, t, P)
    sigma_eta = float(1.0 / np.sqrt(Fperp))

    chi2_fixed1 = qform(d - a, P)
    A0 = float((a @ P @ d) / aa)
    chi2_A0 = qform(d - A0 * a, P)

    eta_phys = float(np.clip(eta_gls, ETA_PHYS_MIN, ETA_PHYS_MAX))
    A_phys = float((a @ P @ (d - eta_phys * t)) / aa)
    chi2_phys = qform(d - A_phys * a - eta_phys * t, P)
    dchi2_phys = float(chi2_A0 - chi2_phys)

    eta_raw = float((t @ P @ r) / tt)
    chi2_gls = qform(d - A_gls * a - eta_gls * t, P)

    return {
        "baseline_chi2_amplitude_fixed_one": chi2_fixed1,
        "amplitude_hat_eta0": A0,
        "chi2_profiled_eta0": chi2_A0,
        "F_raw": tt,
        "F_perp": Fperp,
        "rho_amplitude_memory": rho,
        "eta_hat_raw_amplitude_fixed_one": eta_raw,
        "eta_hat_signed_matched_filter": eta_mf,
        "eta_hat_signed_gls": eta_gls,
        "amplitude_hat_signed_gls": A_gls,
        "chi2_signed_gls": chi2_gls,
        "sigma_eta_shape": sigma_eta,
        "signed_shape_sn": float(eta_gls / sigma_eta),
        "physical_eta_hat_0_to_0p05": eta_phys,
        "physical_amplitude_hat": A_phys,
        "physical_profile_chi2": chi2_phys,
        "physical_delta_chi2_vs_eta0": dchi2_phys,
        "tangent_dimensional": t.tolist(),
        "tangent_deprojected": tperp.tolist(),
        "gls_normal_matrix": M.tolist(),
    }


def worker(args) -> int:
    if os.environ.get("AEST_R7A_EPOCH_MODE") != "full":
        raise SystemExit("R9a requires AEST_R7A_EPOCH_MODE=full")
    v = run_case(float(args.eta), float(args.tau))
    save_case(Path(args.out), v)
    print(json.dumps({"tau_H0": float(args.tau), "eta": float(args.eta),
                      "finite": v["finite"], "positive": v["domain_positive"],
                      "bits": v["bits"], "target_pos": v["target_pos"]}, sort_keys=True), flush=True)
    return 0 if v["finite"] and v["domain_positive"] else 2


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--worker", action="store_true")
    ap.add_argument("--tau", type=float)
    ap.add_argument("--eta", type=float)
    ap.add_argument("--out")
    ap.add_argument("--boss-data-dir", default=os.environ.get("AEST_R9A_BOSS_DATA_DIR", ""))
    ap.add_argument("--json-out", default="results/stable_aest_boss_dr12_r9a_growth_fixed_template.json")
    ap.add_argument("--npz-out", default="results/stable_aest_boss_dr12_r9a_growth_fixed_template.npz")
    ap.add_argument("--workdir", default="results/stable_aest_boss_dr12_r9a_work")
    args = ap.parse_args()
    if args.worker:
        if None in (args.tau, args.eta, args.out):
            raise SystemExit("worker requires --tau --eta --out")
        return worker(args)

    print("STABLE_AEST_BOSS_DR12_R9A_START", flush=True)
    data_dir = Path(args.boss_data_dir).resolve() if args.boss_data_dir else None
    if data_dir is None or not data_dir.is_dir():
        out = {"classification": CLS_INCOMPLETE, "diagnostic_complete": False, "reason": "missing BOSS data directory"}
        Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True)+"\n")
        print("STABLE_AEST_BOSS_DR12_R9A_CLASSIFICATION="+CLS_INCOMPLETE, flush=True)
        return 3

    required = [R7A_JSON, R8A2_JSON, R8B_JSON, R8B_NPZ]
    if not all(p.exists() for p in required):
        out = {"classification": CLS_INCOMPLETE, "diagnostic_complete": False, "reason": "missing parent result"}
        Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True)+"\n")
        print("STABLE_AEST_BOSS_DR12_R9A_CLASSIFICATION="+CLS_INCOMPLETE, flush=True)
        return 3

    r7 = json.loads(R7A_JSON.read_text())
    r82 = json.loads(R8A2_JSON.read_text())
    r8b = json.loads(R8B_JSON.read_text())
    try:
        z_data, d, C, C9 = load_boss(data_dir)
        data_ok = True
    except Exception as exc:
        z_data = d = C = C9 = None
        data_ok = False
        print(f"STABLE_AEST_BOSS_DR12_R9A_DATA_FAIL error={exc!r}", flush=True)

    g1 = bool(
        ancestor(PREFIT_LOCK) and ancestor(R7A_POSTDATA_LOCK) and ancestor(R8A2_POSTDATA_LOCK) and ancestor(R8B_POSTDATA_LOCK)
        and r7.get("classification") == R7A_CLASS and r7.get("diagnostic_complete") is True and all(r7.get("gates", {}).values())
        and r82.get("classification") == R8A2_CLASS and r82.get("diagnostic_complete") is True and all(r82.get("gates", {}).values())
        and r8b.get("classification") == R8B_CLASS and r8b.get("diagnostic_complete") is True and all(r8b.get("gates", {}).values())
        and sha256(R8B_JSON) == R8B_JSON_SHA256 and sha256(R8B_NPZ) == R8B_NPZ_SHA256
        and data_ok
    )
    g2, source_meta = r8a.source_topology()
    print("STABLE_AEST_BOSS_DR12_R9A_SOURCE "+json.dumps(source_meta, sort_keys=True), flush=True)

    work = Path(args.workdir); work.mkdir(parents=True, exist_ok=True)
    py = sys.executable
    mod = "fullj_weyl.stable_aest_boss_dr12_r9a_growth_fixed_template"
    specs = []
    for tau in TAUS:
        specs += [(tau, 0.0, "e0"), (tau, +EPS_PRIMARY, "p025"), (tau, -EPS_PRIMARY, "m025"),
                  (tau, +EPS_CONTROL, "p05"), (tau, -EPS_CONTROL, "m05")]

    vals = {}; runs = []; all_runs = True
    for tau, eta, tag in specs:
        key = f"tau{r8a.tau_tag(tau)}_{tag}"
        outp = work / f"{key}.npz"
        env = os.environ.copy(); env["AEST_R7A_EPOCH_MODE"] = "full"
        for x in ("AEST_TANGENT_FORCE_FILE", "AEST_TANGENT_LAMBDA", "AEST_TANGENT_TRACE_FILE",
                  "AEST_R2D_TRACE_FILE", "AEST_R2D_TRACE_KH", "AEST_R2D_TRACE_ALL_K",
                  "AEST_TANGENT_ALLOW_K_MISS", "AEST_ERHS_TRACE_FILE", "AEST_ERHS_TRACE_K"):
            env.pop(x, None)
        try:
            subprocess.run([py, "-m", mod, "--worker", "--tau", str(tau), "--eta", str(eta), "--out", str(outp)],
                           cwd=ROOT, env=env, check=True)
            v = load_case(outp); vals[key] = v
            exact_z = bool(np.allclose(v["z"], Z_BOSS, rtol=0.0, atol=1e-14))
            ok = bool(v["finite"] and v["domain_positive"] and exact_z)
            all_runs &= ok
            runs.append({"name": key, "tau_H0": tau, "eta": eta, "finite": v["finite"],
                         "domain_positive": v["domain_positive"], "exact_boss_redshifts": exact_z,
                         "bits": v["bits"], "target_pos": v["target_pos"]})
            print(f"STABLE_AEST_BOSS_DR12_R9A_RUN name={key} tau={tau:g} eta={eta:g} finite={v['finite']} positive={v['domain_positive']} exact_z={exact_z}", flush=True)
        except Exception as exc:
            all_runs = False
            runs.append({"name": key, "tau_H0": tau, "eta": eta, "finite": False, "domain_positive": False, "error": repr(exc)})
            print(f"STABLE_AEST_BOSS_DR12_R9A_RUN_FAIL name={key} error={exc!r}", flush=True)

    g3 = bool(all_runs and len(vals) == len(specs))
    central_metrics = {}; tangents = {}; baselines = {}
    g4 = False
    if g3:
        ok = True
        for tau in TAUS:
            tag = r8a.tau_tag(tau)
            b = vals[f"tau{tag}_e0"][OBS]
            t25 = r8a.central(vals[f"tau{tag}_p025"][OBS], vals[f"tau{tag}_m025"][OBS], b, EPS_PRIMARY)
            t50 = r8a.central(vals[f"tau{tag}_p05"][OBS], vals[f"tau{tag}_m05"][OBS], b, EPS_CONTROL)
            met = r8a.metric(t25, t50)
            central_metrics[str(tau)] = met
            baselines[str(tau)] = b
            tangents[str(tau)] = t25
            ok &= bool(met["E"] <= 0.10 and met["C"] >= 0.995)
        g4 = bool(ok)

    like = {}; g5 = False; g6 = False
    if g4 and data_ok:
        try:
            symmetric = bool(np.allclose(C, C.T, rtol=0.0, atol=1e-14))
            evals = np.linalg.eigvalsh(C)
            pd = bool(np.all(np.isfinite(evals)) and np.min(evals) > 0.0)
            finite_cov = bool(np.all(np.isfinite(C)) and np.all(np.isfinite(d)))
            alg_ok = bool(symmetric and pd and finite_cov)
            gls_ok = True
            for tau in TAUS:
                s = likelihood_summary(d, C, baselines[str(tau)], tangents[str(tau)])
                like[str(tau)] = s
                finite_s = all(np.isfinite(v) for k, v in s.items() if isinstance(v, (int, float)))
                alg_ok &= bool(finite_s and s["F_raw"] > 0.0 and s["F_perp"] > 0.0)
                x = s["eta_hat_signed_matched_filter"]; y = s["eta_hat_signed_gls"]
                tol = max(1e-12, 1e-10 * max(abs(x), abs(y)))
                gls_ok &= bool(abs(x-y) <= tol)
            g5 = bool(alg_ok)
            g6 = bool(g5 and gls_ok)
            cov_meta = {"symmetric": symmetric, "positive_definite": pd,
                        "eigenvalues": evals.tolist(), "data": d.tolist(), "z": z_data.tolist(),
                        "covariance_fsigma8": C.tolist()}
        except Exception as exc:
            cov_meta = {"error": repr(exc)}
            g5 = g6 = False
            print(f"STABLE_AEST_BOSS_DR12_R9A_LIKELIHOOD_FAIL error={exc!r}", flush=True)
    else:
        cov_meta = {}

    gates = {
        "R9A_G1_parent_and_data_provenance_lock": g1,
        "R9A_G2_direct_physical_source_topology": g2,
        "R9A_G3_exact_redshift_theory_runs": g3,
        "R9A_G4_central_derivative_consistency": g4,
        "R9A_G5_boss_likelihood_algebra": g5,
        "R9A_G6_matched_filter_gls_identity": g6,
    }
    if not g1: cls = CLS_PARENT
    elif not g2: cls = CLS_SOURCE
    elif not g3: cls = CLS_RUN
    elif not g4: cls = CLS_CENTRAL
    elif not g5: cls = CLS_ALG
    elif not g6: cls = CLS_GLS
    else: cls = CLS_PASS

    arrays = {"z_boss": Z_BOSS}
    if data_ok:
        arrays.update({"boss_fsigma8": d, "boss_cov_fsigma8": C, "boss_cov_full9": C9})
    for tau in TAUS:
        if str(tau) in baselines:
            tag = r8a.tau_tag(tau)
            arrays[f"baseline_tau{tag}_fsigma8"] = baselines[str(tau)]
            arrays[f"T_tau{tag}_fsigma8"] = tangents[str(tau)]
            if str(tau) in like:
                arrays[f"template_tau{tag}_dimensional"] = np.asarray(like[str(tau)]["tangent_dimensional"], float)
                arrays[f"template_tau{tag}_deprojected"] = np.asarray(like[str(tau)]["tangent_deprojected"], float)

    reportable = bool(cls == CLS_PASS)
    summary = {"classification": cls, "central_derivative_metrics": central_metrics,
               "boss_covariance": cov_meta, "tau_likelihood": like, "gates": gates}
    out = {
        "classification": cls,
        "diagnostic_complete": bool(len(vals) == len(specs)),
        "prefit_lock": PREFIT_LOCK,
        "parents": {"r7a_postdata_lock": R7A_POSTDATA_LOCK, "r8a2_postdata_lock": R8A2_POSTDATA_LOCK,
                    "r8b_postdata_lock": R8B_POSTDATA_LOCK, "r7a_classification": r7.get("classification"),
                    "r8a2_classification": r82.get("classification"), "r8b_classification": r8b.get("classification")},
        "data_provenance": {"repository": "CobayaSampler/bao_data", "commit": BOSS_REPO_COMMIT,
                            "data_file": BOSS_DATA_NAME, "data_sha256": BOSS_DATA_SHA256,
                            "covariance_file": BOSS_COV_NAME, "covariance_sha256": BOSS_COV_SHA256,
                            "fsigma8_indices": FS_INDICES.tolist()},
        "settings": {"tau_H0_grid": list(TAUS), "epsilon_primary": EPS_PRIMARY, "epsilon_control": EPS_CONTROL,
                     "eta_physical_interval": [ETA_PHYS_MIN, ETA_PHYS_MAX], "tol": TOL,
                     "z_boss": Z_BOSS.tolist(), "memory_order": 20, "nonlinear_halofit": False,
                     "broadband_growth_amplitude_profiled": True},
        "source_topology": source_meta,
        "runs": runs,
        "central_derivative_metrics": central_metrics,
        "boss_covariance": cov_meta,
        "tau_likelihood": like,
        "gates": gates,
        "interpretation": {"compressed_real_data_projection_reportable": reportable,
                           "observational_detection_claim_licensed": False,
                           "full_shape_modified_gravity_claim_licensed": False,
                           "tau_bound_claim_licensed": False},
        "summary": summary,
    }
    Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True)+"\n")
    np.savez_compressed(args.npz_out, **arrays)
    print("STABLE_AEST_BOSS_DR12_R9A_GATES="+json.dumps(gates, sort_keys=True), flush=True)
    print("STABLE_AEST_BOSS_DR12_R9A_SUMMARY="+json.dumps(summary, sort_keys=True), flush=True)
    print("STABLE_AEST_BOSS_DR12_R9A_CLASSIFICATION="+cls, flush=True)
    return 0 if cls == CLS_PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
