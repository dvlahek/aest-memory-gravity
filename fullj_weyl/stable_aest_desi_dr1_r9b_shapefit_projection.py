#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
from scipy.linalg import block_diag

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fullj_weyl import stable_aest_cosmic_memory_r8a_tau_amplitude_scan as r8a
from fullj_weyl import stable_aest_observable_projection_r5b_derivative_zero as r5b

PREFIT_LOCK = "f19f7ddb85ee37d86a516ebdf41d73b96aef311e"
PREFIT_REPAIR01_LOCK = "76f2a9002b9fde5e568670d3ea2f638f999cef74"
R9A_POSTDATA_LOCK = "a6c0ed87dbc489f929c2a62fdac93ca6e4a2fd37"
R8B_POSTDATA_LOCK = "9e21c61210979ab841918ba16f2210020daa245a"
R8A2_POSTDATA_LOCK = "590dbc69e2823f583b157af2297e357991103c47"
R7A_POSTDATA_LOCK = "86c03e6ba2ee9fcbf33a9d319d12ae778a747881"

R9A_CLASS = "STABLE_AEST_BOSS_DR12_R9A_GROWTH_TEMPLATE_PROJECTION_CERTIFIED"
R8B_CLASS = "STABLE_AEST_COSMIC_MEMORY_R8B_TWO_TAU_LOOKBACK_CERTIFIED"
R8A2_CLASS = "STABLE_AEST_COSMIC_MEMORY_R8A2_TAU_GENERALITY_CERTIFIED"
R7A_CLASS = "STABLE_AEST_COSMIC_MEMORY_R7A_LIVE_LOOKBACK_DECOMPOSITION_CERTIFIED"

DESI_REPO_COMMIT = "7d51f4f86dc3bee6bf10f1a684913c943a89a844"
LSSTYPES_COMMIT = "53f048e610bcb008548f66822b0879ce9df58cb1"
COSMOPRIMO_COMMIT = "2e59c963c9b8e7cba1a4c8f161e978c6f4d80c2d"
DESI_DATA_ROOT = "https://data.desi.lbl.gov/public/dr1/vac/dr1/full-shape-bao-clustering/v1.0/data/likelihood/"
OBSERVABLE_NAME = "spectrum-poles-rotated+bao-recon"

TRACERS = (
    "bgs_z0", "lrg_z0", "lrg_z1", "lrg_z2", "elg_z1", "qso_z0",
)
TAUS = (10.0, 5.0, 2.5, 1.25)
EPS_PRIMARY = 0.025
EPS_CONTROL = 0.05
TOL = 3e-8
ETA_PHYS_MIN = 0.0
ETA_PHYS_MAX = 0.05
C_KM_S = 299792.458

R9A_JSON = ROOT / "results/stable_aest_boss_dr12_r9a_growth_fixed_template.json"
R8B_JSON = ROOT / "results/stable_aest_cosmic_memory_r8b_two_tau_lookback.json"
R8A2_JSON = ROOT / "results/stable_aest_cosmic_memory_r8a2_precision_qualified_tau_scan.json"
R7A_JSON = ROOT / "results/stable_aest_cosmic_memory_r7a_live_epoch_derivative.json"

CLS_INCOMPLETE = "STABLE_AEST_DESI_DR1_R9B_INCOMPLETE"
CLS_PARENT = "STABLE_AEST_DESI_DR1_R9B_PARENT_OR_DATA_PROVENANCE_FAIL"
CLS_SOURCE = "STABLE_AEST_DESI_DR1_R9B_SOURCE_TOPOLOGY_FAIL"
CLS_DATA = "STABLE_AEST_DESI_DR1_R9B_SHAPEFIT_DATA_CONSTRUCTION_FAIL"
CLS_RUN = "STABLE_AEST_DESI_DR1_R9B_THEORY_RUN_FAIL"
CLS_CENTRAL = "STABLE_AEST_DESI_DR1_R9B_CENTRAL_DERIVATIVE_FAIL"
CLS_PROJ = "STABLE_AEST_DESI_DR1_R9B_NUISANCE_PROJECTION_FAIL"
CLS_GLS = "STABLE_AEST_DESI_DR1_R9B_MATCHED_FILTER_GLS_FAIL"
CLS_PASS = "STABLE_AEST_DESI_DR1_R9B_SHAPEFIT_MEMORY_PROJECTION_CERTIFIED"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"], cwd=ROOT,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    ).returncode == 0


def rel(a, b) -> float:
    a = np.asarray(a, float); b = np.asarray(b, float)
    return float(np.linalg.norm(a-b) / max(np.linalg.norm(a), np.linalg.norm(b), 1e-300))


def cosine(a, b) -> float:
    a = np.asarray(a, float); b = np.asarray(b, float)
    na = float(np.linalg.norm(a)); nb = float(np.linalg.norm(b))
    if na == 0.0 or nb == 0.0:
        return float("nan")
    return float(a.dot(b)/(na*nb))


def tau_tag(tau: float) -> str:
    return str(float(tau)).replace(".", "p")


def eta_tag(eta: float) -> str:
    if eta == 0.0:
        return "e0"
    sign = "p" if eta > 0 else "m"
    return sign + str(abs(float(eta))).replace("0.", "").replace(".", "p")


def _import_official(official_repo: Path):
    p = official_repo / "dr1" / "cobaya"
    if not p.is_dir():
        raise RuntimeError("official DESI dr1/cobaya directory missing")
    sys.path.insert(0, str(p))
    try:
        mod = importlib.import_module("desi_shapefit_bao_all")
    finally:
        try:
            sys.path.remove(str(p))
        except ValueError:
            pass
    return mod


def load_desi(data_dir: Path, official_repo: Path):
    import lsstypes as types
    mod = _import_official(official_repo)
    selected = {x.lower() for x in TRACERS}
    bins = []
    hashes = {}
    for tracer, iz, zrange in mod.list_zrange:
        if "lya" in tracer.lower():
            continue
        label = mod.get_tracer_label(tracer)
        namespace = f"{label}_z{iz}"
        if namespace.lower() not in selected:
            continue
        fn = Path(mod.dataset_fn(data_dir, tracer, zrange, observable_name=OBSERVABLE_NAME))
        if not fn.is_file():
            raise FileNotFoundError(f"missing DESI ShapeFit file: {fn}")
        hashes[fn.name] = sha256(fn)
        likelihood_data = types.read(fn)
        shapefit = likelihood_data.observable.get("shapefit")
        if shapefit is None:
            raise RuntimeError(f"no shapefit observable in {fn.name}")
        value = np.asarray(shapefit.value(), float).reshape(-1)
        params = [str(x) for x in list(shapefit.parameters)]
        zeff = float(shapefit.attrs["zeff"])
        cov = np.asarray(likelihood_data.covariance.value(), float)
        if cov.shape != (value.size, value.size):
            raise RuntimeError(f"covariance shape mismatch in {fn.name}: {cov.shape} vs {value.size}")
        if len(params) != value.size:
            raise RuntimeError(f"parameter count mismatch in {fn.name}")
        bins.append({
            "namespace": namespace,
            "tracer": tracer,
            "zrange": [float(zrange[0]), float(zrange[1])],
            "zeff": zeff,
            "parameters": params,
            "data": value,
            "cov": cov,
            "file": fn.name,
        })
    if [b["namespace"].lower() for b in bins] != list(TRACERS):
        raise RuntimeError(f"DESI bin ordering mismatch: {[b['namespace'] for b in bins]}")
    d = np.concatenate([b["data"] for b in bins])
    C = block_diag(*[b["cov"] for b in bins])
    offsets = []
    i0 = 0
    for b in bins:
        i1 = i0 + len(b["data"])
        offsets.append((i0, i1))
        i0 = i1
    return bins, d, C, offsets, hashes, mod


def _omega(c, name: str, default=0.0):
    if not hasattr(c, name):
        return float(default)
    x = getattr(c, name)
    try:
        return float(x())
    except TypeError:
        return float(x)


def _get_fiducial_cache(zeffs):
    from cosmoprimo.fiducial import DESI
    from cosmoprimo import PowerSpectrumBAOFilter
    fid = DESI(engine="camb")
    fo = fid.get_fourier()
    out = {}
    for z in zeffs:
        pkdd = fo.pk_interpolator(of="delta_cb").to_1d(z=float(z))
        pktt = fo.pk_interpolator(of="theta_cb").to_1d(z=float(z))
        filt = PowerSpectrumBAOFilter(pkdd, engine="peakaverage", cosmo=fid, cosmo_fid=fid)
        filt(pkdd, cosmo=fid)
        pknow = filt.smooth_pk_interpolator()
        kp = 0.03
        dk = 1e-2
        k = kp*np.array([1.-dk, 1.+dk])
        m = float(np.diff(np.log(np.asarray(pknow(k), float)), axis=0)[0] / np.diff(np.log(k))[0])
        Ap = float(np.asarray(pkdd(kp)))
        f = float(np.asarray(pktt.sigma8()) / np.asarray(pkdd.sigma8()))
        out[float(z)] = {
            "m": m,
            "Ap": Ap,
            "f": f,
            "f_sqrt_Ap": f*np.sqrt(Ap),
            "filter": filt,
        }
    return fid, out


def _model_shapefit_at_z(c, z: float, fid, fcache):
    from cosmoprimo import PowerSpectrumInterpolator1D, Cosmology
    h = float(c.h())
    rdrag = float(c.rs_drag())
    kh = np.geomspace(1e-4, 5.0, 1400)
    pk = np.asarray([float(c.pk_cb_lin(float(k*h), float(z))) for k in kh], float)*h**3
    if not np.all(np.isfinite(pk)) or not np.all(pk > 0.0):
        raise RuntimeError(f"invalid P_cb at z={z}")
    pkdd = PowerSpectrumInterpolator1D(kh, pk)

    Omega_b = _omega(c, "Omega_b")
    Omega_cdm = _omega(c, "Omega_cdm")
    Omega_ncdm = _omega(c, "Omega_nu", 0.0)
    cstate = dict(H0=100.*h, Omega_b=Omega_b, Omega_cdm=Omega_cdm,
                  Omega_ncdm=Omega_ncdm, n_s=float(c.n_s()))
    cosmo = Cosmology(**cstate)
    try:
        cosmo.rs_drag = rdrag*h
    except Exception:
        pass

    filt = fcache[float(z)]["filter"]
    filt(pkdd, cosmo=cosmo)
    pknow = filt.smooth_pk_interpolator()
    s = (rdrag*h)/float(fid.rs_drag)
    kp = 0.03/s
    dk = 1e-2
    k = kp*np.array([1.-dk, 1.+dk])
    m = float(np.diff(np.log(np.asarray(pknow(k), float)), axis=0)[0] / np.diff(np.log(k))[0])
    Ap = float((1./s**3)*np.asarray(pkdd(kp)))
    sigma8 = float(c.sigma(8.0, float(z), h_units=True))
    fsigma8 = float(c.effective_f_sigma8(float(z), z_step=0.1))
    f_eff = fsigma8/sigma8
    f_sqrt_Ap = f_eff*np.sqrt(Ap)
    return {"m": m, "Ap": Ap, "f_eff": f_eff, "f_sqrt_Ap": f_sqrt_Ap,
            "rdrag": rdrag, "h": h}


def _geometry(c, z: float, fid):
    rdrag = float(c.rs_drag())
    Hz = float(c.Hubble(float(z)))*C_KM_S
    da = float(c.angular_distance(float(z)))
    apar = (1.0/(Hz/100.0)/rdrag) / (1.0/float(fid.efunc(float(z)))/float(fid.rs_drag))
    aper = (da/rdrag) / (float(fid.angular_diameter_distance(float(z)))/float(fid.rs_drag))
    return float(apar), float(aper)


def build_theory_vector(c, bins):
    zeffs = [float(b["zeff"]) for b in bins]
    fid, fcache = _get_fiducial_cache(zeffs)
    values = []
    per_bin = []
    for b in bins:
        z = float(b["zeff"])
        sf = _model_shapefit_at_z(c, z, fid, fcache)
        apar, aper = _geometry(c, z, fid)
        fidz = fcache[z]
        q = []
        for param in b["parameters"]:
            if param in ("qpar", "qper", "qiso", "qap"):
                suffix = param[1:]
                coeff = {"iso": (1./3., 2./3.), "par": (1., 0.), "per": (0., 1.), "ap": (1., -1.)}[suffix]
                val = apar**coeff[0]*aper**coeff[1]
            elif param == "df":
                val = sf["f_sqrt_Ap"]/fidz["f_sqrt_Ap"]
            elif param == "dm":
                val = sf["m"]-fidz["m"]
            else:
                raise RuntimeError(f"unsupported ShapeFit parameter {param}")
            q.append(float(val))
        q = np.asarray(q, float)
        values.append(q)
        per_bin.append({
            "namespace": b["namespace"], "zeff": z, "parameters": b["parameters"],
            "theory": q.tolist(), "apar": apar, "aper": aper,
            "m": sf["m"], "f_eff": sf["f_eff"], "Ap": sf["Ap"],
            "f_sqrt_Ap": sf["f_sqrt_Ap"],
        })
    vec = np.concatenate(values)
    return vec, per_bin


def run_case(eta: float, tau: float, bins):
    from classy import Class
    params, bits, pos = r5b.build_params(float(eta), float(TOL))
    params["aest_tau_H0"] = float(tau)
    params["z_max_pk"] = max(2.3, max(float(b["zeff"]) for b in bins)+0.2)
    params["P_k_max_h/Mpc"] = 5.0
    params.pop("non_linear", None)
    c = Class(); c.set(params); c.compute()
    try:
        vec, per_bin = build_theory_vector(c, bins)
        finite = bool(np.all(np.isfinite(vec)))
        return {"theory": vec, "per_bin": per_bin, "finite": finite,
                "bits": int(bits), "target_pos": int(pos)}
    finally:
        c.struct_cleanup(); c.empty()


def save_case(path: Path, v: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(path, theory=np.asarray(v["theory"], float),
                        finite=np.asarray([int(v["finite"])]),
                        bits=np.asarray([v["bits"]]), target_pos=np.asarray([v["target_pos"]]),
                        per_bin_json=np.asarray([json.dumps(v["per_bin"], sort_keys=True)]))


def load_case(path: Path):
    q = np.load(path, allow_pickle=False)
    return {"theory": np.asarray(q["theory"], float),
            "finite": bool(int(q["finite"][0])),
            "bits": int(q["bits"][0]), "target_pos": int(q["target_pos"][0]),
            "per_bin": json.loads(str(q["per_bin_json"][0]))}


def build_nuisance(baseline, bins, offsets):
    n = len(baseline)
    cols = []
    names = []
    col_df = np.zeros(n, float)
    col_dm = np.zeros(n, float)
    has_df = False; has_dm = False
    for b, (i0, i1) in zip(bins, offsets):
        for j, p in enumerate(b["parameters"]):
            idx = i0+j
            if p == "df":
                col_df[idx] = baseline[idx]
                has_df = True
            elif p == "dm":
                col_dm[idx] = 1.0
                has_dm = True
    if has_df:
        cols.append(col_df); names.append("global_df_scale")
    if has_dm:
        cols.append(col_dm); names.append("global_dm_offset")
    if not cols:
        raise RuntimeError("no ShapeFit df/dm nuisance columns found")
    return np.column_stack(cols), names


def profile_nuisance(r, P, N):
    M = N.T@P@N
    beta = np.linalg.solve(M, N.T@P@r)
    rr = r-N@beta
    return beta, float(rr@P@rr), M


def projection_summary(d, C, baseline, tangent, bins, offsets):
    P = np.linalg.inv(C)
    N, nuisance_names = build_nuisance(baseline, bins, offsets)
    M = N.T@P@N
    Minv = np.linalg.inv(M)
    Pperp = P-P@N@Minv@N.T@P
    F = float(tangent@Pperp@tangent)
    if not np.isfinite(F) or F <= 0.0:
        raise RuntimeError("non-positive deprojected Fisher information")
    r = d-baseline
    eta_mf = float(tangent@Pperp@r/F)
    sigma = float(1./np.sqrt(F))

    X = np.column_stack([N, tangent])
    Mgls = X.T@P@X
    betagls = np.linalg.solve(Mgls, X.T@P@r)
    eta_gls = float(betagls[-1])

    beta0, chi20, Mn = profile_nuisance(r, P, N)
    eta_phys = float(np.clip(eta_gls, ETA_PHYS_MIN, ETA_PHYS_MAX))
    betap, chi2p, _ = profile_nuisance(r-eta_phys*tangent, P, N)

    idem_num = np.linalg.norm(Pperp@C@Pperp-Pperp)
    idem_den = max(np.linalg.norm(Pperp), 1e-300)
    idem = float(idem_num/idem_den)
    return {
        "nuisance_names": nuisance_names,
        "nuisance_normal_matrix": Mn.tolist(),
        "projection_idempotence_metric": idem,
        "F_perp": F,
        "eta_hat_signed_matched_filter": eta_mf,
        "eta_hat_signed_gls": eta_gls,
        "sigma_eta_shape": sigma,
        "signed_shape_sn": float(eta_gls/sigma),
        "chi2_profiled_eta0": chi20,
        "nuisance_hat_eta0": beta0.tolist(),
        "physical_eta_hat_0_to_0p05": eta_phys,
        "physical_profile_chi2": chi2p,
        "physical_nuisance_hat": betap.tolist(),
        "physical_delta_chi2_vs_eta0": float(chi20-chi2p),
        "gls_normal_matrix": Mgls.tolist(),
    }


def worker(args) -> int:
    data_dir = Path(args.data_dir).resolve()
    official_repo = Path(args.official_repo).resolve()
    bins, _, _, _, _, _ = load_desi(data_dir, official_repo)
    if os.environ.get("AEST_R7A_EPOCH_MODE") != "full":
        raise SystemExit("R9b worker requires AEST_R7A_EPOCH_MODE=full")
    v = run_case(float(args.eta), float(args.tau), bins)
    save_case(Path(args.out), v)
    print(json.dumps({"tau_H0": float(args.tau), "eta": float(args.eta), "finite": v["finite"],
                      "bits": v["bits"], "target_pos": v["target_pos"]}, sort_keys=True), flush=True)
    return 0 if v["finite"] else 2


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--worker", action="store_true")
    ap.add_argument("--tau", type=float)
    ap.add_argument("--eta", type=float)
    ap.add_argument("--out")
    ap.add_argument("--data-dir", default=os.environ.get("AEST_R9B_DESI_DATA_DIR", ""))
    ap.add_argument("--official-repo", default=os.environ.get("AEST_R9B_DESI_REPO", ""))
    ap.add_argument("--json-out", default="results/stable_aest_desi_dr1_r9b_shapefit_projection.json")
    ap.add_argument("--npz-out", default="results/stable_aest_desi_dr1_r9b_shapefit_projection.npz")
    ap.add_argument("--workdir", default="results/stable_aest_desi_dr1_r9b_work")
    args = ap.parse_args()
    if args.worker:
        if None in (args.tau, args.eta, args.out):
            raise SystemExit("worker requires --tau --eta --out")
        return worker(args)

    print("STABLE_AEST_DESI_DR1_R9B_START", flush=True)
    data_dir = Path(args.data_dir).resolve() if args.data_dir else None
    official_repo = Path(args.official_repo).resolve() if args.official_repo else None
    if data_dir is None or official_repo is None or not data_dir.is_dir() or not official_repo.is_dir():
        out = {"classification": CLS_INCOMPLETE, "diagnostic_complete": False,
               "reason": "missing DESI data/repository path"}
        Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True)+"\n")
        print("STABLE_AEST_DESI_DR1_R9B_CLASSIFICATION="+CLS_INCOMPLETE, flush=True)
        return 3

    parent_paths = [R9A_JSON, R8B_JSON, R8A2_JSON, R7A_JSON]
    if not all(p.exists() for p in parent_paths):
        out = {"classification": CLS_INCOMPLETE, "diagnostic_complete": False, "reason": "missing parent results"}
        Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True)+"\n")
        print("STABLE_AEST_DESI_DR1_R9B_CLASSIFICATION="+CLS_INCOMPLETE, flush=True)
        return 3

    r9a = json.loads(R9A_JSON.read_text()); r8b = json.loads(R8B_JSON.read_text())
    r82 = json.loads(R8A2_JSON.read_text()); r7 = json.loads(R7A_JSON.read_text())
    try:
        bins, d, C, offsets, data_hashes, official_mod = load_desi(data_dir, official_repo)
        data_ok = True
    except Exception as exc:
        bins = []; d = C = offsets = data_hashes = None; official_mod = None
        data_ok = False
        print(f"STABLE_AEST_DESI_DR1_R9B_DATA_FAIL error={exc!r}", flush=True)

    repo_head = subprocess.check_output(["git", "-C", str(official_repo), "rev-parse", "HEAD"], text=True).strip()
    g1 = bool(
        ancestor(PREFIT_LOCK) and ancestor(PREFIT_REPAIR01_LOCK) and ancestor(R9A_POSTDATA_LOCK)
        and ancestor(R8B_POSTDATA_LOCK) and ancestor(R8A2_POSTDATA_LOCK) and ancestor(R7A_POSTDATA_LOCK)
        and r9a.get("classification") == R9A_CLASS and r9a.get("diagnostic_complete") is True and all(r9a.get("gates", {}).values())
        and r8b.get("classification") == R8B_CLASS and r8b.get("diagnostic_complete") is True and all(r8b.get("gates", {}).values())
        and r82.get("classification") == R8A2_CLASS and r82.get("diagnostic_complete") is True and all(r82.get("gates", {}).values())
        and r7.get("classification") == R7A_CLASS and r7.get("diagnostic_complete") is True and all(r7.get("gates", {}).values())
        and repo_head == DESI_REPO_COMMIT and data_ok
    )
    g2, source_meta = r8a.source_topology()
    print("STABLE_AEST_DESI_DR1_R9B_SOURCE "+json.dumps(source_meta, sort_keys=True), flush=True)

    g3 = False
    data_summary = {}
    if data_ok:
        eig = np.linalg.eigvalsh(C)
        sym = bool(np.allclose(C, C.T, rtol=0.0, atol=1e-12))
        pd = bool(np.all(eig > 0.0))
        finite = bool(np.all(np.isfinite(d)) and np.all(np.isfinite(C)))
        data_summary = {
            "dimension": int(len(d)), "symmetric": sym, "positive_definite": pd,
            "min_cov_eigenvalue": float(eig.min()), "max_cov_eigenvalue": float(eig.max()),
            "files_sha256": data_hashes,
            "bins": [{"namespace": b["namespace"], "tracer": b["tracer"], "zrange": b["zrange"],
                      "zeff": b["zeff"], "parameters": b["parameters"], "file": b["file"]} for b in bins],
        }
        g3 = bool(finite and sym and pd and len(bins) == 6)

    work = Path(args.workdir); work.mkdir(parents=True, exist_ok=True)
    py = sys.executable
    modname = "fullj_weyl.stable_aest_desi_dr1_r9b_shapefit_projection"
    specs = []
    for tau in TAUS:
        specs += [(tau, 0.0), (tau, +EPS_PRIMARY), (tau, -EPS_PRIMARY),
                  (tau, +EPS_CONTROL), (tau, -EPS_CONTROL)]

    vals = {}; runs = []; all_runs = bool(g3)
    for tau, eta in specs:
        key = f"tau{tau_tag(tau)}_{eta_tag(eta)}"
        outp = work / f"{key}.npz"
        env = os.environ.copy(); env["AEST_R7A_EPOCH_MODE"] = "full"
        cmd = [py, "-u", "-m", modname, "--worker", "--tau", str(tau), "--eta", str(eta),
               "--out", str(outp), "--data-dir", str(data_dir), "--official-repo", str(official_repo)]
        cp = subprocess.run(cmd, cwd=ROOT, env=env, text=True, capture_output=True)
        if cp.stdout:
            print(cp.stdout, end="", flush=True)
        if cp.stderr:
            print(cp.stderr, end="", file=sys.stderr, flush=True)
        ok = cp.returncode == 0 and outp.exists()
        if ok:
            v = load_case(outp); ok = bool(v["finite"] and np.all(np.isfinite(v["theory"])))
            vals[key] = v
        all_runs &= ok
        runs.append({"name": key, "tau_H0": float(tau), "eta": float(eta), "ok": bool(ok)})
        print(f"STABLE_AEST_DESI_DR1_R9B_RUN name={key} tau={tau:g} eta={eta:g} ok={ok}", flush=True)

    if all_runs:
        g3 = bool(g3 and all(vals[f"tau{tau_tag(t)}_e0"]["finite"] for t in TAUS))

    central_metrics = {}; tangents = {}; baseline = None
    g4 = bool(all_runs)
    if all_runs:
        for tau in TAUS:
            tag = tau_tag(tau)
            b = vals[f"tau{tag}_e0"]["theory"]
            tp = vals[f"tau{tag}_{eta_tag(+EPS_PRIMARY)}"]["theory"]
            tm = vals[f"tau{tag}_{eta_tag(-EPS_PRIMARY)}"]["theory"]
            cp = vals[f"tau{tag}_{eta_tag(+EPS_CONTROL)}"]["theory"]
            cm = vals[f"tau{tag}_{eta_tag(-EPS_CONTROL)}"]["theory"]
            T1 = (tp-tm)/(2.*EPS_PRIMARY)
            T2 = (cp-cm)/(2.*EPS_CONTROL)
            central_metrics[str(tau)] = {"E": rel(T1, T2), "C": cosine(T1, T2),
                                         "norm_primary": float(np.linalg.norm(T1))}
            tangents[str(tau)] = T1
            g4 &= central_metrics[str(tau)]["E"] <= 0.05 and central_metrics[str(tau)]["C"] >= 0.995
            if baseline is None:
                baseline = b

    projection = {}; g5 = bool(g4); g6 = bool(g4)
    if g4:
        for tau in TAUS:
            try:
                s = projection_summary(d, C, baseline, tangents[str(tau)], bins, offsets)
                projection[str(tau)] = s
                g5 &= bool(np.isfinite(s["F_perp"]) and s["F_perp"] > 0.0
                           and s["projection_idempotence_metric"] <= 1e-8)
                a = s["eta_hat_signed_matched_filter"]; bgls = s["eta_hat_signed_gls"]
                g6 &= abs(a-bgls) <= max(1e-10, 1e-8*max(abs(a), abs(bgls), 1.0))
            except Exception as exc:
                projection[str(tau)] = {"error": repr(exc)}
                g5 = False; g6 = False

    gates = {
        "R9B_G1_parent_and_official_data_provenance": bool(g1),
        "R9B_G2_direct_physical_source_topology": bool(g2),
        "R9B_G3_shapefit_data_construction": bool(g3),
        "R9B_G4_central_derivative_consistency": bool(g4),
        "R9B_G5_nuisance_projection_algebra": bool(g5),
        "R9B_G6_matched_filter_gls_identity": bool(g6),
    }
    if not g1: classification = CLS_PARENT
    elif not g2: classification = CLS_SOURCE
    elif not g3: classification = CLS_DATA if data_ok else CLS_RUN
    elif not all_runs: classification = CLS_RUN
    elif not g4: classification = CLS_CENTRAL
    elif not g5: classification = CLS_PROJ
    elif not g6: classification = CLS_GLS
    else: classification = CLS_PASS

    result = {
        "classification": classification,
        "diagnostic_complete": bool(all_runs and data_ok),
        "gates": gates,
        "settings": {
            "desi_repo_commit": DESI_REPO_COMMIT,
            "lsstypes_commit": LSSTYPES_COMMIT,
            "cosmoprimo_commit": COSMOPRIMO_COMMIT,
            "desi_data_root": DESI_DATA_ROOT,
            "observable_name": OBSERVABLE_NAME,
            "tracers": list(TRACERS), "tau_H0_grid": list(TAUS),
            "epsilon_primary": EPS_PRIMARY, "epsilon_control": EPS_CONTROL,
            "eta_physical_interval": [ETA_PHYS_MIN, ETA_PHYS_MAX],
            "growth_proxy": "effective_f_sigma8(z) / sigma8(z)",
            "nuisance_repair": "global df scale + global dm offset",
        },
        "parents": {
            "r9a": r9a.get("classification"), "r8b": r8b.get("classification"),
            "r8a2": r82.get("classification"), "r7a": r7.get("classification"),
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
            arrays[f"tangent_tau{tau_tag(tau)}"] = tangents[str(tau)]
        np.savez_compressed(args.npz_out, **arrays)

    print("STABLE_AEST_DESI_DR1_R9B_GATES="+json.dumps(gates, sort_keys=True), flush=True)
    print("STABLE_AEST_DESI_DR1_R9B_SUMMARY="+json.dumps({"classification": classification,
          "central_derivative_metrics": central_metrics, "tau_likelihood": projection}, sort_keys=True), flush=True)
    print("STABLE_AEST_DESI_DR1_R9B_CLASSIFICATION="+classification, flush=True)
    return 0 if classification == CLS_PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
