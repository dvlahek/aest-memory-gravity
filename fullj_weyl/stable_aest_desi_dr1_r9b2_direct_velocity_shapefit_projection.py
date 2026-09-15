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

from fullj_weyl import stable_aest_desi_dr1_r9b_shapefit_projection as r9b
from fullj_weyl import stable_aest_observable_projection_r5b_derivative_zero as r5b

PREFIT_LOCK = "5864a8a56f420c578629763d478f60dfc49c2620"
ADAPTER_RESULT_LOCK = "f5484b4572b673dfcead51875e3aa790c698a18c"
R9B_POSTDATA_LOCK = "22583094f3c5a417e7af6b1d7f284f739553048b"

R9B_JSON = ROOT / "results/stable_aest_desi_dr1_r9b_shapefit_projection.json"
ADAPTER_JSON = ROOT / "results/stable_aest_desi_dr1_r9b2_velocity_adapter_validation.json"
ADAPTER_JSON_SHA256 = "c4d9281cd504785a9e4fb187b02db2860e24622bbe1ccf4a52e44446be0a119a"

R9B_CLASS = "STABLE_AEST_DESI_DR1_R9B_CENTRAL_DERIVATIVE_FAIL"
ADAPTER_CLASS = "STABLE_AEST_DESI_DR1_R9B2_VELOCITY_ADAPTER_VALIDATED"

TAUS = r9b.TAUS
EPS_PRIMARY = r9b.EPS_PRIMARY
EPS_CONTROL = r9b.EPS_CONTROL
TOL = r9b.TOL
ETA_PHYS_MIN = r9b.ETA_PHYS_MIN
ETA_PHYS_MAX = r9b.ETA_PHYS_MAX

CLS_INCOMPLETE = "STABLE_AEST_DESI_DR1_R9B2_INCOMPLETE"
CLS_PARENT = "STABLE_AEST_DESI_DR1_R9B2_PARENT_OR_ADAPTER_PROVENANCE_FAIL"
CLS_SOURCE = "STABLE_AEST_DESI_DR1_R9B2_SOURCE_TOPOLOGY_FAIL"
CLS_DATA = "STABLE_AEST_DESI_DR1_R9B2_DIRECT_VELOCITY_SHAPEFIT_CONSTRUCTION_FAIL"
CLS_RUN = "STABLE_AEST_DESI_DR1_R9B2_THEORY_RUN_FAIL"
CLS_CENTRAL = "STABLE_AEST_DESI_DR1_R9B2_CENTRAL_DERIVATIVE_FAIL"
CLS_PROJ = "STABLE_AEST_DESI_DR1_R9B2_NUISANCE_PROJECTION_FAIL"
CLS_GLS = "STABLE_AEST_DESI_DR1_R9B2_MATCHED_FILTER_GLS_FAIL"
CLS_PASS = "STABLE_AEST_DESI_DR1_R9B2_DIRECT_VELOCITY_SHAPEFIT_MEMORY_PROJECTION_CERTIFIED"

KH_MIN = 1.0e-4
KH_MAX = 5.0


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"], cwd=ROOT,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    ).returncode == 0


def _direct_velocity_shapefit_at_z(c, z: float, fid, fcache):
    from cosmoprimo import Cosmology, PowerSpectrumInterpolator1D

    h = float(c.h())
    rdrag = float(c.rs_drag())

    kh_dense = np.geomspace(KH_MIN, KH_MAX, 1400)
    pdd_dense = np.asarray(
        [float(c.pk_cb_lin(float(kh*h), float(z))) for kh in kh_dense], float
    ) * h**3
    if not np.all(np.isfinite(pdd_dense)) or not np.all(pdd_dense > 0.0):
        raise RuntimeError(f"invalid direct P_cb at z={z}")
    pkdd = PowerSpectrumInterpolator1D(kh_dense, pdd_dense)

    tr = c.get_transfer(float(z), output_format="class")
    required = ("k (h/Mpc)", "d_b", "d_cdm", "t_b", "t_cdm")
    missing = [name for name in required if name not in tr]
    if missing:
        raise RuntimeError(f"missing CLASS velocity-transfer fields at z={z}: {missing}; keys={sorted(tr)}")

    kh = np.asarray(tr["k (h/Mpc)"], float)
    db = np.asarray(tr["d_b"], float)
    dc = np.asarray(tr["d_cdm"], float)
    tb = np.asarray(tr["t_b"], float)
    tc = np.asarray(tr["t_cdm"], float)
    if not (kh.shape == db.shape == dc.shape == tb.shape == tc.shape):
        raise RuntimeError(f"transfer shape mismatch at z={z}")

    good = (
        np.isfinite(kh) & np.isfinite(db) & np.isfinite(dc)
        & np.isfinite(tb) & np.isfinite(tc)
        & (kh >= KH_MIN) & (kh <= KH_MAX)
    )
    kh = kh[good]; db = db[good]; dc = dc[good]; tb = tb[good]; tc = tc[good]
    order = np.argsort(kh)
    kh = kh[order]; db = db[order]; dc = dc[order]; tb = tb[order]; tc = tc[order]
    keep = np.ones(kh.size, dtype=bool)
    if kh.size > 1:
        keep[1:] = np.diff(kh) > 0.0
    kh = kh[keep]; db = db[keep]; dc = dc[keep]; tb = tb[keep]; tc = tc[keep]
    if kh.size < 32 or kh[0] > 2.0e-4 or kh[-1] < 2.0:
        raise RuntimeError(
            f"insufficient direct velocity k support at z={z}: "
            f"n={kh.size} range={kh[0] if kh.size else np.nan}..{kh[-1] if kh.size else np.nan}"
        )

    Omega_b = r9b._omega(c, "Omega_b")
    Omega_cdm = r9b._omega(c, "Omega_cdm")
    Omega_ncdm = r9b._omega(c, "Omega_nu", 0.0)
    fb = Omega_b / (Omega_b + Omega_cdm)
    fc = 1.0 - fb

    dcb = fb*db + fc*dc
    Hconf = float(c.Hubble(float(z))) / (1.0 + float(z))
    if not np.isfinite(Hconf) or Hconf <= 0.0:
        raise RuntimeError(f"invalid Hconf at z={z}: {Hconf}")
    vnb = -tb / Hconf
    vnc = -tc / Hconf
    vcb = fb*vnb + fc*vnc

    scale = max(float(np.max(np.abs(dcb))), 1.0)
    if np.any(np.abs(dcb) <= 1.0e-14*scale):
        raise RuntimeError(f"delta_cb near zero on retained transfer grid at z={z}")

    k_mpc = kh*h
    pdd_native = np.asarray(
        [float(c.pk_cb_lin(float(k), float(z))) for k in k_mpc], float
    ) * h**3
    ptt_native = pdd_native * (vcb/dcb)**2
    if (
        np.any(~np.isfinite(pdd_native)) or np.any(~np.isfinite(ptt_native))
        or np.any(pdd_native <= 0.0) or np.any(ptt_native <= 0.0)
    ):
        raise RuntimeError(f"invalid direct density/velocity spectra at z={z}")
    pktt = PowerSpectrumInterpolator1D(kh, ptt_native)

    cstate = dict(
        H0=100.0*h,
        Omega_b=Omega_b,
        Omega_cdm=Omega_cdm,
        Omega_ncdm=Omega_ncdm,
        n_s=float(c.n_s()),
    )
    cosmo = Cosmology(**cstate)
    try:
        cosmo.rs_drag = rdrag*h
    except Exception:
        pass

    filt = fcache[float(z)]["filter"]
    filt(pkdd, cosmo=cosmo)
    pknow = filt.smooth_pk_interpolator()
    s = (rdrag*h) / float(fid.rs_drag)
    kp = 0.03/s
    dk = 1.0e-2
    kval = kp*np.array([1.0-dk, 1.0+dk])
    m = float(np.diff(np.log(np.asarray(pknow(kval), float)), axis=0)[0] / np.diff(np.log(kval))[0])
    Ap = float((1.0/s**3)*np.asarray(pkdd(kp)))

    sigma8_dd = float(np.asarray(pkdd.sigma8()))
    sigma8_tt = float(np.asarray(pktt.sigma8()))
    f_direct = sigma8_tt / sigma8_dd
    f_sqrt_Ap = f_direct*np.sqrt(Ap)

    old_sigma8 = float(c.sigma(8.0, float(z), h_units=True))
    old_fsigma8 = float(c.effective_f_sigma8(float(z), z_step=0.1))
    old_proxy = old_fsigma8/old_sigma8

    return {
        "m": m,
        "Ap": Ap,
        "f_direct": f_direct,
        "f_sqrt_Ap": f_sqrt_Ap,
        "sigma8_dd": sigma8_dd,
        "sigma8_tt": sigma8_tt,
        "old_proxy": old_proxy,
        "old_proxy_rel_to_direct": abs(old_proxy-f_direct)/max(abs(old_proxy), abs(f_direct), 1e-300),
        "Hconf_1_Mpc": Hconf,
        "fb": fb,
        "transfer_n_k": int(kh.size),
        "transfer_kh_min": float(kh[0]),
        "transfer_kh_max": float(kh[-1]),
        "rdrag": rdrag,
        "h": h,
    }


def build_theory_vector(c, bins):
    zeffs = [float(b["zeff"]) for b in bins]
    fid, fcache = r9b._get_fiducial_cache(zeffs)
    values = []
    per_bin = []
    for b in bins:
        z = float(b["zeff"])
        sf = _direct_velocity_shapefit_at_z(c, z, fid, fcache)
        apar, aper = r9b._geometry(c, z, fid)
        fidz = fcache[z]
        q = []
        for param in b["parameters"]:
            if param in ("qpar", "qper", "qiso", "qap"):
                suffix = param[1:]
                coeff = {"iso": (1./3., 2./3.), "par": (1., 0.), "per": (0., 1.), "ap": (1., -1.)}[suffix]
                val = apar**coeff[0] * aper**coeff[1]
            elif param == "df":
                val = sf["f_sqrt_Ap"] / fidz["f_sqrt_Ap"]
            elif param == "dm":
                val = sf["m"] - fidz["m"]
            else:
                raise RuntimeError(f"unsupported ShapeFit parameter {param}")
            q.append(float(val))
        q = np.asarray(q, float)
        values.append(q)
        per_bin.append({
            "namespace": b["namespace"],
            "zeff": z,
            "parameters": b["parameters"],
            "theory": q.tolist(),
            "apar": apar,
            "aper": aper,
            "m": sf["m"],
            "f_direct": sf["f_direct"],
            "Ap": sf["Ap"],
            "f_sqrt_Ap": sf["f_sqrt_Ap"],
            "sigma8_dd": sf["sigma8_dd"],
            "sigma8_tt": sf["sigma8_tt"],
            "old_proxy": sf["old_proxy"],
            "old_proxy_rel_to_direct": sf["old_proxy_rel_to_direct"],
            "Hconf_1_Mpc": sf["Hconf_1_Mpc"],
            "fb": sf["fb"],
            "transfer_n_k": sf["transfer_n_k"],
            "transfer_kh_min": sf["transfer_kh_min"],
            "transfer_kh_max": sf["transfer_kh_max"],
        })
    vec = np.concatenate(values)
    return vec, per_bin


def run_case(eta: float, tau: float, bins):
    from classy import Class

    params, bits, pos = r5b.build_params(float(eta), float(TOL))
    params["aest_tau_H0"] = float(tau)
    params["z_max_pk"] = max(2.3, max(float(b["zeff"]) for b in bins)+0.2)
    params["P_k_max_h/Mpc"] = KH_MAX
    params["output"] = "mPk,mTk,vTk"
    params.pop("non_linear", None)
    params.pop("lensing", None)
    params.pop("l_max_scalars", None)

    c = Class()
    c.set(params)
    c.compute()
    try:
        vec, per_bin = build_theory_vector(c, bins)
        finite = bool(
            np.all(np.isfinite(vec))
            and all(np.isfinite(row["f_direct"]) and row["f_direct"] > 0.0 for row in per_bin)
            and all(np.isfinite(row["sigma8_tt"]) and row["sigma8_tt"] > 0.0 for row in per_bin)
        )
        return {
            "theory": vec,
            "per_bin": per_bin,
            "finite": finite,
            "bits": int(bits),
            "target_pos": int(pos),
        }
    finally:
        c.struct_cleanup()
        c.empty()


def save_case(path: Path, v: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        path,
        theory=np.asarray(v["theory"], float),
        finite=np.asarray([int(v["finite"])]),
        bits=np.asarray([v["bits"]]),
        target_pos=np.asarray([v["target_pos"]]),
        per_bin_json=np.asarray([json.dumps(v["per_bin"], sort_keys=True)]),
    )


def load_case(path: Path):
    q = np.load(path, allow_pickle=False)
    return {
        "theory": np.asarray(q["theory"], float),
        "finite": bool(int(q["finite"][0])),
        "bits": int(q["bits"][0]),
        "target_pos": int(q["target_pos"][0]),
        "per_bin": json.loads(str(q["per_bin_json"][0])),
    }


def worker(args) -> int:
    data_dir = Path(args.data_dir).resolve()
    official_repo = Path(args.official_repo).resolve()
    bins, _, _, _, _, _ = r9b.load_desi(data_dir, official_repo)
    if os.environ.get("AEST_R7A_EPOCH_MODE") != "full":
        raise SystemExit("R9b2 worker requires AEST_R7A_EPOCH_MODE=full")
    v = run_case(float(args.eta), float(args.tau), bins)
    save_case(Path(args.out), v)
    print(json.dumps({
        "tau_H0": float(args.tau),
        "eta": float(args.eta),
        "finite": v["finite"],
        "bits": v["bits"],
        "target_pos": v["target_pos"],
    }, sort_keys=True), flush=True)
    return 0 if v["finite"] else 2


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--worker", action="store_true")
    ap.add_argument("--tau", type=float)
    ap.add_argument("--eta", type=float)
    ap.add_argument("--out")
    ap.add_argument("--data-dir", default=os.environ.get("AEST_R9B_DESI_DATA_DIR", ""))
    ap.add_argument("--official-repo", default=os.environ.get("AEST_R9B_DESI_REPO", ""))
    ap.add_argument("--json-out", default="results/stable_aest_desi_dr1_r9b2_direct_velocity_shapefit_projection.json")
    ap.add_argument("--npz-out", default="results/stable_aest_desi_dr1_r9b2_direct_velocity_shapefit_projection.npz")
    ap.add_argument("--workdir", default="results/stable_aest_desi_dr1_r9b2_work")
    args = ap.parse_args()

    if args.worker:
        if None in (args.tau, args.eta, args.out):
            raise SystemExit("worker requires --tau --eta --out")
        return worker(args)

    print("STABLE_AEST_DESI_DR1_R9B2_START", flush=True)

    data_dir = Path(args.data_dir).resolve() if args.data_dir else None
    official_repo = Path(args.official_repo).resolve() if args.official_repo else None
    if data_dir is None or official_repo is None or not data_dir.is_dir() or not official_repo.is_dir():
        out = {"classification": CLS_INCOMPLETE, "diagnostic_complete": False, "reason": "missing DESI data/repository path"}
        Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True)+"\n")
        print("STABLE_AEST_DESI_DR1_R9B2_CLASSIFICATION="+CLS_INCOMPLETE, flush=True)
        return 3

    if not R9B_JSON.is_file() or not ADAPTER_JSON.is_file():
        out = {"classification": CLS_INCOMPLETE, "diagnostic_complete": False, "reason": "missing R9b historical or R9b2 adapter result"}
        Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True)+"\n")
        print("STABLE_AEST_DESI_DR1_R9B2_CLASSIFICATION="+CLS_INCOMPLETE, flush=True)
        return 3

    hist = json.loads(R9B_JSON.read_text())
    adapter = json.loads(ADAPTER_JSON.read_text())

    try:
        bins, d, C, offsets, data_hashes, _ = r9b.load_desi(data_dir, official_repo)
        data_ok = True
    except Exception as exc:
        bins = []
        d = C = offsets = data_hashes = None
        data_ok = False
        print(f"STABLE_AEST_DESI_DR1_R9B2_DATA_FAIL error={exc!r}", flush=True)

    repo_head = subprocess.check_output(
        ["git", "-C", str(official_repo), "rev-parse", "HEAD"], text=True
    ).strip()

    adapter_rows_ok = bool(
        adapter.get("classification") == ADAPTER_CLASS
        and adapter.get("diagnostic_complete") is True
        and adapter.get("science_evaluated") is False
        and abs(float(adapter.get("gate", np.nan)) - 0.005) <= 1e-15
        and len(adapter.get("rows", [])) == 6
        and all(row.get("pass") is True for row in adapter.get("rows", []))
    )
    historical_ok = bool(
        hist.get("classification") == R9B_CLASS
        and hist.get("diagnostic_complete") is True
        and hist.get("gates", {}).get("R9B_G1_parent_and_official_data_provenance") is True
        and hist.get("gates", {}).get("R9B_G2_direct_physical_source_topology") is True
        and hist.get("gates", {}).get("R9B_G3_shapefit_data_construction") is True
        and hist.get("gates", {}).get("R9B_G4_central_derivative_consistency") is False
    )
    g1 = bool(
        ancestor(PREFIT_LOCK)
        and ancestor(ADAPTER_RESULT_LOCK)
        and ancestor(R9B_POSTDATA_LOCK)
        and sha256(ADAPTER_JSON) == ADAPTER_JSON_SHA256
        and historical_ok
        and adapter_rows_ok
        and repo_head == r9b.DESI_REPO_COMMIT
        and data_ok
    )

    g2, source_meta = r9b.r8a.source_topology()
    print("STABLE_AEST_DESI_DR1_R9B2_SOURCE "+json.dumps(source_meta, sort_keys=True), flush=True)

    g3 = False
    data_summary = {}
    if data_ok:
        eig = np.linalg.eigvalsh(C)
        sym = bool(np.allclose(C, C.T, rtol=0.0, atol=1e-12))
        pd = bool(np.all(eig > 0.0))
        finite_data = bool(np.all(np.isfinite(d)) and np.all(np.isfinite(C)))
        data_summary = {
            "dimension": int(len(d)),
            "symmetric": sym,
            "positive_definite": pd,
            "min_cov_eigenvalue": float(eig.min()),
            "max_cov_eigenvalue": float(eig.max()),
            "files_sha256": data_hashes,
            "bins": [{
                "namespace": b["namespace"],
                "tracer": b["tracer"],
                "zrange": b["zrange"],
                "zeff": b["zeff"],
                "parameters": b["parameters"],
                "file": b["file"],
            } for b in bins],
        }
        g3 = bool(finite_data and sym and pd and len(bins) == 6 and adapter_rows_ok)

    work = Path(args.workdir)
    work.mkdir(parents=True, exist_ok=True)
    py = sys.executable
    modname = "fullj_weyl.stable_aest_desi_dr1_r9b2_direct_velocity_shapefit_projection"

    specs = []
    for tau in TAUS:
        specs += [
            (tau, 0.0),
            (tau, +EPS_PRIMARY), (tau, -EPS_PRIMARY),
            (tau, +EPS_CONTROL), (tau, -EPS_CONTROL),
        ]

    vals = {}
    runs = []
    all_runs = bool(g3)
    for tau, eta in specs:
        key = f"tau{r9b.tau_tag(tau)}_{r9b.eta_tag(eta)}"
        outp = work / f"{key}.npz"
        env = os.environ.copy()
        env["AEST_R7A_EPOCH_MODE"] = "full"
        cmd = [
            py, "-u", "-m", modname,
            "--worker", "--tau", str(tau), "--eta", str(eta),
            "--out", str(outp), "--data-dir", str(data_dir),
            "--official-repo", str(official_repo),
        ]
        cp = subprocess.run(cmd, cwd=ROOT, env=env, text=True, capture_output=True)
        if cp.stdout:
            print(cp.stdout, end="", flush=True)
        if cp.stderr:
            print(cp.stderr, end="", file=sys.stderr, flush=True)
        ok = cp.returncode == 0 and outp.exists()
        if ok:
            v = load_case(outp)
            ok = bool(v["finite"] and np.all(np.isfinite(v["theory"])))
            if ok:
                ok = bool(
                    len(v["per_bin"]) == 6
                    and all(np.isfinite(row["f_direct"]) and row["f_direct"] > 0.0 for row in v["per_bin"])
                    and all(np.isfinite(row["sigma8_tt"]) and row["sigma8_tt"] > 0.0 for row in v["per_bin"])
                )
            vals[key] = v
        all_runs &= ok
        runs.append({"name": key, "tau_H0": float(tau), "eta": float(eta), "ok": bool(ok)})
        print(f"STABLE_AEST_DESI_DR1_R9B2_RUN name={key} tau={tau:g} eta={eta:g} ok={ok}", flush=True)

    if all_runs:
        g3 = bool(g3 and all(vals[f"tau{r9b.tau_tag(t)}_e0"]["finite"] for t in TAUS))

    central_metrics = {}
    tangents = {}
    baseline = None
    g4 = bool(all_runs)
    if all_runs:
        for tau in TAUS:
            tag = r9b.tau_tag(tau)
            b = vals[f"tau{tag}_e0"]["theory"]
            tp = vals[f"tau{tag}_{r9b.eta_tag(+EPS_PRIMARY)}"]["theory"]
            tm = vals[f"tau{tag}_{r9b.eta_tag(-EPS_PRIMARY)}"]["theory"]
            cp = vals[f"tau{tag}_{r9b.eta_tag(+EPS_CONTROL)}"]["theory"]
            cm = vals[f"tau{tag}_{r9b.eta_tag(-EPS_CONTROL)}"]["theory"]
            T1 = (tp-tm)/(2.0*EPS_PRIMARY)
            T2 = (cp-cm)/(2.0*EPS_CONTROL)
            central_metrics[str(tau)] = {
                "E": r9b.rel(T1, T2),
                "C": r9b.cosine(T1, T2),
                "norm_primary": float(np.linalg.norm(T1)),
            }
            tangents[str(tau)] = T1
            g4 &= (
                central_metrics[str(tau)]["E"] <= 0.05
                and central_metrics[str(tau)]["C"] >= 0.995
            )
            if baseline is None:
                baseline = b

    projection = {}
    g5 = bool(g4)
    g6 = bool(g4)
    if g4:
        for tau in TAUS:
            try:
                s = r9b.projection_summary(
                    d, C, baseline, tangents[str(tau)], bins, offsets
                )
                projection[str(tau)] = s
                g5 &= bool(
                    np.isfinite(s["F_perp"]) and s["F_perp"] > 0.0
                    and s["projection_idempotence_metric"] <= 1e-8
                )
                a = s["eta_hat_signed_matched_filter"]
                bgls = s["eta_hat_signed_gls"]
                g6 &= abs(a-bgls) <= max(
                    1e-10, 1e-8*max(abs(a), abs(bgls), 1.0)
                )
            except Exception as exc:
                projection[str(tau)] = {"error": repr(exc)}
                g5 = False
                g6 = False

    gates = {
        "R9B2_G1_historical_parent_adapter_and_official_data_provenance": bool(g1),
        "R9B2_G2_direct_physical_source_topology": bool(g2),
        "R9B2_G3_direct_velocity_shapefit_construction": bool(g3),
        "R9B2_G4_central_derivative_consistency": bool(g4),
        "R9B2_G5_nuisance_projection_algebra": bool(g5),
        "R9B2_G6_matched_filter_gls_identity": bool(g6),
    }

    if not g1:
        classification = CLS_PARENT
    elif not g2:
        classification = CLS_SOURCE
    elif not g3:
        classification = CLS_DATA if data_ok else CLS_RUN
    elif not all_runs:
        classification = CLS_RUN
    elif not g4:
        classification = CLS_CENTRAL
    elif not g5:
        classification = CLS_PROJ
    elif not g6:
        classification = CLS_GLS
    else:
        classification = CLS_PASS

    result = {
        "classification": classification,
        "diagnostic_complete": bool(all_runs and data_ok),
        "gates": gates,
        "settings": {
            "prefit_lock": PREFIT_LOCK,
            "adapter_result_lock": ADAPTER_RESULT_LOCK,
            "r9b_postdata_lock": R9B_POSTDATA_LOCK,
            "adapter_json_sha256": ADAPTER_JSON_SHA256,
            "desi_repo_commit": r9b.DESI_REPO_COMMIT,
            "lsstypes_commit": r9b.LSSTYPES_COMMIT,
            "cosmoprimo_commit": r9b.COSMOPRIMO_COMMIT,
            "desi_data_root": r9b.DESI_DATA_ROOT,
            "observable_name": r9b.OBSERVABLE_NAME,
            "tracers": list(r9b.TRACERS),
            "tau_H0_grid": list(TAUS),
            "epsilon_primary": EPS_PRIMARY,
            "epsilon_control": EPS_CONTROL,
            "eta_physical_interval": [ETA_PHYS_MIN, ETA_PHYS_MAX],
            "growth_adapter": "CLASS mTk/vTk: v_newtonian_x=-theta_x/Hconf; P_tt=P_cb*(v_cb/delta_cb)^2; f=sigma8(P_tt)/sigma8(P_dd)",
            "old_growth_proxy_role": "diagnostic_only",
            "nuisance_model": "global df scale + global dm offset",
        },
        "parents": {
            "r9b_historical": hist.get("classification"),
            "r9b2_velocity_adapter": adapter.get("classification"),
            "r9b_parents": hist.get("parents", {}),
        },
        "adapter_validation": {
            "classification": adapter.get("classification"),
            "gate": adapter.get("gate"),
            "rows": adapter.get("rows", []),
        },
        "data": data_summary,
        "source_topology": source_meta,
        "runs": runs,
        "central_derivative_metrics": central_metrics,
        "tau_likelihood": projection,
        "interpretation": {
            "compressed_full_shape_derived_real_data_projection_reportable": classification == CLS_PASS,
            "observational_detection_claim_licensed": False,
            "full_EFT_modified_gravity_claim_licensed": False,
            "tau_bound_claim_licensed": False,
            "requires_R9c_for_evidence_claim": True,
        },
    }
    Path(args.json_out).write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")

    if all_runs and data_ok:
        arrays = {"data": d, "covariance": C, "baseline": baseline}
        for tau in TAUS:
            arrays[f"tangent_tau{r9b.tau_tag(tau)}"] = tangents[str(tau)]
        np.savez_compressed(args.npz_out, **arrays)

    print("STABLE_AEST_DESI_DR1_R9B2_GATES="+json.dumps(gates, sort_keys=True), flush=True)
    print("STABLE_AEST_DESI_DR1_R9B2_SUMMARY="+json.dumps({
        "classification": classification,
        "central_derivative_metrics": central_metrics,
        "tau_likelihood": projection,
    }, sort_keys=True), flush=True)
    print("STABLE_AEST_DESI_DR1_R9B2_CLASSIFICATION="+classification, flush=True)
    return 0 if classification == CLS_PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
