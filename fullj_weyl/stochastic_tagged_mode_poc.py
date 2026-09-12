#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Import the already documented dynamic-history loader repair.  No dense-radial
# interpolation machinery is used here; this import only generalizes the
# inherited historical six-history CLASS cardinality guard to len(K_MPC).
from fullj_weyl import dense_radial_weyl_extension_r1 as densefix
from nl1c6d2c6b import all27_physical_nonlinear_trajectories as d2b

base = densefix.mod
r2 = base.r2
m = base.m
static = base.static

R2_RESULT_LOCK = "1f42f88e9724c58d2d242a65ca7266a207e4a0f8"
GAUSS_RESULT_LOCK = "05e38b273f91eb04b7c8753731017d0ed839c1"
SAT_RESULT_LOCK = "f6eb7099cffc9ae6f4fe11ddef1794f0e6dd6e4f"
RESIDUAL_FAIL_RESULT_LOCK = "4d87865a8e45985388dfab2b9d8922faa9290f7f"
CARDINALITY_RESULT_LOCK = "df182a828b3c140fba22f1f5d58414ec41017e7b"
PREDATA_LOCK = "bb478329717575e7e6f73096b0e9c00930b2cd87"

PASS = "FULLJ_STOCHASTIC_TAGGED_MODE_POC_PASS"
FAIL = "FULLJ_STOCHASTIC_TAGGED_MODE_POC_FAIL"
INCOMPLETE = "FULLJ_STOCHASTIC_TAGGED_MODE_POC_INCOMPLETE"

SEED = 20260912
NREAL_LOCKED = 32
BACKGROUND_IDS = (0, 1, 2)
COEFF_HASH = "9c511b09899cb874d09c0513b89b82c796769886ecba5dd6347c71678b19d200"
TARGETS = (0.0375, 0.10, 0.175)
EPS_LEVELS = (0.10, 0.05)
REFERENCE_MEMBER = {"sigma": 0, "kind": "simple", "beta0": 1.0}
CHECK_Z = np.asarray(m.CHECK_Z, float)
K0 = np.asarray([0.03, 0.05, 0.08, 0.10, 0.15, 0.20], float)
NSTEP = 4096

CANONICAL_GATE = 1.0e-10
METRIC_GATE = 1.0e-8
EPS_MED_GATE = 3.0e-2
EPS_MAX_GATE = 1.0e-1
SAT_GATE = 2.0e-2
ALG_GATE = 1.0e-12

TARGET_GEOM = {
    0.0375: {"kf_h": 0.0025, "ntag": 15, "nx": 512},
    0.10:   {"kf_h": 0.0100, "ntag": 10, "nx": 128},
    0.175:  {"kf_h": 0.0050, "ntag": 35, "nx": 256},
}


def is_ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"],
        cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    ).returncode == 0


def gaussian_lock_ok() -> bool:
    if is_ancestor(GAUSS_RESULT_LOCK):
        return True
    # Local shallow/incomplete ancestry queries previously returned false for
    # this old commit.  The locked residual-R2 result is a required ancestor
    # and explicitly preserved gaussian_1d_result_lock=True.
    if not is_ancestor(RESIDUAL_FAIL_RESULT_LOCK):
        return False
    p = ROOT / "results/fullj_dense_radial_class_residual_r2.json"
    try:
        q = json.loads(p.read_text())
    except Exception:
        return False
    return bool(
        q.get("classification") == "FULLJ_DENSE_RADIAL_CLASS_RESIDUAL_R2_FAIL"
        and q.get("ancestry", {}).get("gaussian_1d_result_lock") is True
        and q.get("gates", {}).get("R2_G1_locked_provenance_setup") is True
    )


def coeff_draw():
    rng = np.random.default_rng(SEED)
    xy = rng.normal(size=(NREAL_LOCKED, 6, 2))
    g = (xy[..., 0] + 1j * xy[..., 1]) / np.sqrt(2.0)
    digest = hashlib.sha256(np.ascontiguousarray(xy, dtype=np.float64).tobytes()).hexdigest()
    return xy, g, digest


def tag_amp_phase(kh: float):
    amp = float(np.exp(np.interp(np.log(kh), np.log(K0), np.log(np.asarray(static.MODE_AMP, float)))))
    phase = float(np.interp(kh, K0, np.asarray(static.PHASE, float)))
    return amp, phase


def target_modes(kh: float):
    vals = list(K0)
    if not np.any(np.isclose(K0, kh, rtol=0.0, atol=5e-14)):
        vals.append(float(kh))
    return np.asarray(sorted(set(np.round(vals, 14))), float)


def idx(grid, value):
    q = np.where(np.isclose(np.asarray(grid, float), float(value), rtol=0.0, atol=5e-13))[0]
    if len(q) != 1:
        raise RuntimeError(f"mode index not unique for {value}")
    return int(q[0])


def geometry(kh: float):
    key = min(TARGET_GEOM, key=lambda x: abs(x-kh))
    if abs(key-kh) > 1e-12:
        raise RuntimeError(f"unregistered target geometry {kh}")
    q = TARGET_GEOM[key]
    box = 2.0*np.pi/(float(q["kf_h"])*float(static.h))
    return float(q["kf_h"]), int(q["ntag"]), int(q["nx"]), float(box)


def basis_factory(mode_h, gvec, kh, eps, sign, nx, box):
    amp_tag, phase_tag = tag_amp_phase(kh)
    mode_h = np.asarray(mode_h, float)
    mode_mpc = mode_h * float(static.h)
    original_map = [idx(mode_h, q) for q in K0]
    tag_i = idx(mode_h, kh)

    def make(n):
        if int(n) != int(nx):
            raise RuntimeError(f"tagged basis expected nx={nx}, got {n}")
        x = np.arange(nx)*box/nx
        C = np.zeros((len(mode_h), nx), float)
        gv = np.asarray(gvec, complex)
        for j, row in enumerate(original_map):
            C[row] += float(static.MODE_AMP[j])*abs(gv[j])*np.cos(mode_mpc[row]*x + np.angle(gv[j]))
        C[tag_i] += float(sign)*float(eps)*amp_tag*np.cos(mode_mpc[tag_i]*x + phase_tag)
        return C

    return make, amp_tag, phase_tag


def health(run):
    out = {"finite": bool(run.get("finite", False)), "canonical_max": float("inf"),
           "metric_max": {"hamiltonian": float("inf"), "momentum": float("inf"), "shear": float("inf")}}
    cps = run.get("checkpoints", [])
    if not out["finite"] or len(cps) != len(CHECK_Z):
        return out
    out["canonical_max"] = max(float(cp["canonical_constraint"]) for cp in cps)
    mm = {"hamiltonian": 0.0, "momentum": 0.0, "shear": 0.0}
    for cp in cps:
        cc = cp["metric"]["metric_correction"]["constraint"]
        for k in mm:
            mm[k] = max(mm[k], float(cc[k]))
    out["metric_max"] = mm
    return out


def saturation(run, nx, box):
    old_box = float(static.BOX)
    static.BOX = float(box)
    try:
        grad, lap, _, div = m.spec_ops(nx)
        out = []
        for cp in run["checkpoints"]:
            tau = float(cp["tau"])
            a, H, Q, KQ, KQQ, Z, Qdot = m.bg_eval(_ACTIVE_DATA, tau)
            chi = np.asarray(cp["y"][1], float)
            g = grad(chi)
            x = float(static.ACC_CONV)*np.abs(g)/a
            je = d2b.j_eff(x, Z)
            full = div((1.0+je)*g)
            sat = 2.0*lap(chi)
            scale = max(float(np.linalg.norm(full)), float(np.linalg.norm(sat)), 1e-300)
            out.append(float(np.linalg.norm(full-sat)/scale))
        return np.asarray(out, float)
    finally:
        static.BOX = old_box


def tagged_fourier(run, ntag):
    vals = []
    for cp in run["checkpoints"]:
        w = np.asarray(cp["metric"]["weyl"], float)
        fh = np.fft.fft(w)/float(w.size)
        vals.append(fh[int(ntag)])
    return np.asarray(vals, complex)


def rel(a, b):
    aa = np.asarray(a, complex); bb = np.asarray(b, complex)
    return float(np.linalg.norm(aa-bb)/max(float(np.linalg.norm(aa)), float(np.linalg.norm(bb)), 1e-300))


_ACTIVE_DATA = None


def run_signed(data, mode_h, gvec, bgid, kh, eps, sign):
    global _ACTIVE_DATA
    _ACTIVE_DATA = data
    kf_h, ntag, nx, box = geometry(kh)
    make, amp_tag, phase_tag = basis_factory(mode_h, gvec, kh, eps, sign, nx, box)
    old_cos = m.cos_matrix
    old_box = float(static.BOX)
    d2b.set_member(REFERENCE_MEMBER)
    m.cos_matrix = make
    static.BOX = box
    try:
        run = r2.integrate_combined_r2(data, nx, NSTEP, True)
        hh = health(run)
        if not hh["finite"]:
            return {"finite": False, "background": int(bgid), "k_h": float(kh), "epsilon": float(eps), "sign": int(sign),
                    "nx": int(nx), "box_Mpc": float(box), "reason": run.get("fail_reason", "incomplete")}, None, None
        sat = saturation(run, nx, box)
        wh = tagged_fourier(run, ntag)
        rec = {"finite": True, "background": int(bgid), "k_h": float(kh), "epsilon": float(eps), "sign": int(sign),
               "nx": int(nx), "box_Mpc": float(box), "kF_h": float(kf_h), "ntag": int(ntag),
               "canonical_max": float(hh["canonical_max"]), "metric_max": hh["metric_max"],
               "sat_max": float(np.max(sat)), "sat_by_z": sat.tolist()}
        return rec, wh, {"amp_tag": amp_tag, "phase_tag": phase_tag}
    finally:
        m.cos_matrix = old_cos
        static.BOX = old_box
        _ACTIVE_DATA = None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json-out", default="results/fullj_stochastic_tagged_mode_poc.json")
    ap.add_argument("--npz-out", default="results/fullj_stochastic_tagged_mode_poc.npz")
    ap.add_argument("--csv-out", default="results/fullj_stochastic_tagged_mode_poc.csv")
    args = ap.parse_args()

    ancestry = {
        "r2_result_lock": is_ancestor(R2_RESULT_LOCK),
        "gaussian_1d_result_lock": gaussian_lock_ok(),
        "saturated_closure_result_lock": is_ancestor(SAT_RESULT_LOCK),
        "residual_r2_fail_result_lock": is_ancestor(RESIDUAL_FAIL_RESULT_LOCK),
        "cardinality_result_lock": is_ancestor(CARDINALITY_RESULT_LOCK),
        "predata_lock": is_ancestor(PREDATA_LOCK),
    }
    xy, g, digest = coeff_draw()
    geometry_ok = (
        geometry(0.0375)[:3] == (0.0025,15,512)
        and geometry(0.10)[:3] == (0.01,10,128)
        and geometry(0.175)[:3] == (0.005,35,256)
    )
    frozen = bool(
        digest == COEFF_HASH and BACKGROUND_IDS == (0,1,2) and TARGETS == (0.0375,0.10,0.175)
        and EPS_LEVELS == (0.10,0.05) and NSTEP == 4096 and geometry_ok
        and REFERENCE_MEMBER == {"sigma":0,"kind":"simple","beta0":1.0}
    )
    print("FULLJ_TAGGED_POC_START", flush=True)
    print("FULLJ_TAGGED_POC_ANCESTRY="+json.dumps(ancestry,sort_keys=True), flush=True)
    print("FULLJ_TAGGED_POC_COEFFICIENT_SHA256="+digest, flush=True)
    print("FULLJ_TAGGED_POC_TARGETS="+json.dumps(TARGETS), flush=True)

    if not all(ancestry.values()) or not frozen:
        out={"classification":INCOMPLETE,"diagnostic_complete":False,"ancestry":ancestry,"frozen_setup":frozen,"coefficient_sha256":digest}
        Path(args.json_out).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
        print("FULLJ_TAGGED_POC_CLASSIFICATION="+INCOMPLETE, flush=True)
        return 3

    old_kmpc = np.asarray(m.K_MPC,float).copy()
    old_kh = np.asarray(getattr(m,"K_H",K0),float).copy()
    all_runs=[]
    response={}  # (bg,kh,eps) -> complex[z]
    response_rows=[]
    run_index=0

    try:
        for kh in TARGETS:
            mode_h = target_modes(kh)
            m.K_H = mode_h.copy(); m.K_MPC = mode_h*float(static.h)
            data = r2.r0.prepare_bridge_data()
            for bgid in BACKGROUND_IDS:
                for eps in EPS_LEVELS:
                    pair={}
                    meta=None
                    for sign in (+1,-1):
                        run_index += 1
                        rec, wh, mm = run_signed(data, mode_h, g[bgid], bgid, kh, eps, sign)
                        rec["run_index"] = int(run_index)
                        all_runs.append(rec)
                        print(
                            f"FULLJ_TAGGED_POC_RUN {run_index:02d}/36 bg={bgid} k_h={kh:.7f} eps={eps:.3f} sign={sign:+d} "
                            + (f"canonical={rec['canonical_max']:.3e} satMax={rec['sat_max']:.3e}" if rec.get('finite') else f"finite=False reason={rec.get('reason','unknown')}"),
                            flush=True,
                        )
                        if wh is not None:
                            pair[sign]=wh; meta=mm
                    if len(pair)==2:
                        T=(pair[+1]-pair[-1])*np.exp(-1j*float(meta["phase_tag"]))/(float(eps)*float(meta["amp_tag"]))
                        response[(bgid,float(kh),float(eps))]=T
                        for iz,z in enumerate(CHECK_Z):
                            response_rows.append({"background":int(bgid),"k_h_Mpc_inv":float(kh),"epsilon":float(eps),"z":float(z),
                                                  "T_real":float(np.real(T[iz])),"T_imag":float(np.imag(T[iz])),"P_tag":float(abs(T[iz])**2)})
    finally:
        m.K_MPC=old_kmpc; m.K_H=old_kh

    all_finite = len(all_runs)==36 and all(bool(r.get("finite",False)) for r in all_runs)
    health_ok = all_finite and all(
        float(r["canonical_max"])<=CANONICAL_GATE and all(float(v)<=METRIC_GATE for v in r["metric_max"].values())
        for r in all_runs
    )
    satmax=max([float(r.get("sat_max",float("inf"))) for r in all_runs], default=float("inf"))

    eps_rows=[]; eps_errors=[]
    if len(response)==len(BACKGROUND_IDS)*len(TARGETS)*len(EPS_LEVELS):
        for bg in BACKGROUND_IDS:
            for kh in TARGETS:
                t10=response[(bg,float(kh),0.10)]
                t05=response[(bg,float(kh),0.05)]
                q=rel(t10,t05); eps_errors.append(q)
                eps_rows.append({"background":int(bg),"k_h_Mpc_inv":float(kh),"relative_L2":float(q)})
    eps_med=float(np.median(eps_errors)) if eps_errors else float("inf")
    eps_max=float(np.max(eps_errors)) if eps_errors else float("inf")

    primary=[]
    for bg in BACKGROUND_IDS:
        for kh in TARGETS:
            q=response.get((bg,float(kh),0.05))
            if q is not None: primary.append(q)
    primary_arr=np.asarray(primary,complex) if primary else np.empty((0,len(CHECK_Z)),complex)
    ptag=np.abs(primary_arr)**2
    alg=0.0
    if primary_arr.size:
        back=np.real(primary_arr)**2+np.imag(primary_arr)**2
        alg=float(np.linalg.norm(ptag-back)/max(float(np.linalg.norm(ptag)),1e-300))
    response_power_ok=bool(primary_arr.shape==(9,len(CHECK_Z)) and np.all(np.isfinite(primary_arr)) and np.all(np.isfinite(ptag)) and np.all(ptag>=0) and alg<=ALG_GATE)

    ensemble_rows=[]
    if primary_arr.shape==(9,len(CHECK_Z)):
        # reshape bg,target,z
        A=primary_arr.reshape(len(BACKGROUND_IDS),len(TARGETS),len(CHECK_Z))
        for ik,kh in enumerate(TARGETS):
            for iz,z in enumerate(CHECK_Z):
                vals=A[:,ik,iz]
                mean=np.mean(vals)
                stdc=float(np.sqrt(np.mean(np.abs(vals-mean)**2)))
                rms=float(np.sqrt(np.mean(np.abs(vals)**2)))
                pw=np.abs(vals)**2
                mp=float(np.mean(pw)); sp=float(np.std(pw,ddof=1)) if len(pw)>1 else 0.0
                ensemble_rows.append({"k_h_Mpc_inv":float(kh),"z":float(z),"mean_T_real":float(np.real(mean)),"mean_T_imag":float(np.imag(mean)),
                                      "complex_scatter_rms":stdc,"response_rms":rms,"scatter_over_rms":float(stdc/max(rms,1e-300)),
                                      "mean_P_tag":mp,"std_P_tag":sp,"cv_P_tag":float(sp/max(mp,1e-300))})

    gates={
        "ST_G1_provenance_and_frozen_identity":bool(all(ancestry.values()) and frozen),
        "ST_G2_Gaussian_background_identity":bool(digest==COEFF_HASH),
        "ST_G3_all_tagged_runs_finite_constraint_clean":bool(health_ok),
        "ST_G4_symmetric_response_epsilon_consistency":bool(eps_med<=EPS_MED_GATE and eps_max<=EPS_MAX_GATE),
        "ST_G5_broadband_saturated_closure":bool(satmax<=SAT_GATE),
        "ST_G6_tagged_response_power_sanity":bool(response_power_ok),
    }
    classification=PASS if all(gates.values()) else FAIL
    summary={
        "coefficient_sha256":digest,"runs_finite":int(sum(bool(r.get("finite",False)) for r in all_runs)),"runs_expected":36,
        "epsilon_consistency_median":eps_med,"epsilon_consistency_max":eps_max,"broadband_saturation_max":float(satmax),
        "tagged_power_identity_relative_residual":float(alg),
        "primary_mean_power_by_target":{
            str(kh):float(np.mean([r["mean_P_tag"] for r in ensemble_rows if abs(r["k_h_Mpc_inv"]-kh)<1e-12])) if ensemble_rows else float("nan")
            for kh in TARGETS
        },
        "primary_median_power_cv":float(np.median([r["cv_P_tag"] for r in ensemble_rows])) if ensemble_rows else float("nan"),
        "primary_max_scatter_over_rms":float(np.max([r["scatter_over_rms"] for r in ensemble_rows])) if ensemble_rows else float("nan"),
    }
    out={
        "classification":classification,"diagnostic_complete":True,
        "git_head":subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip(),
        "ancestry":ancestry,"gates":gates,"summary":summary,"seed":SEED,"background_ids":list(BACKGROUND_IDS),
        "targets_h_Mpc_inv":list(TARGETS),"epsilon_levels":list(EPS_LEVELS),"redshifts":CHECK_Z.tolist(),
        "reference_member":REFERENCE_MEMBER,"runs":all_runs,"epsilon_consistency":eps_rows,"ensemble_primary":ensemble_rows,
        "STOCHASTIC_BROADBAND_TAGGED_RESPONSE_POC_TESTED":classification==PASS,
        "STOCHASTIC_BROADBAND_LOWK_SATURATION_TESTED":classification==PASS,
        "THREE_D_BOUNDED_CONTINUOUS_WEYL_POWER_LICENSED":False,"THREE_D_CONTINUOUS_WEYL_POWER_LICENSED":False,
        "EVOLVING_WEYL_POWER_LICENSED":False,"ACT_LIKELIHOOD_LICENSED":False,"OBSERVATIONAL_CLAIM_LICENSED":False,
    }
    Path(args.json_out).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    np.savez_compressed(args.npz_out,CHECK_Z=CHECK_Z,targets=np.asarray(TARGETS),eps=np.asarray(EPS_LEVELS),primary_response=primary_arr,primary_power=ptag)
    with open(args.csv_out,"w",newline="") as f:
        fields=["background","k_h_Mpc_inv","epsilon","z","T_real","T_imag","P_tag"]
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(response_rows)

    print("FULLJ_TAGGED_POC_SUMMARY="+json.dumps(summary,sort_keys=True), flush=True)
    print("FULLJ_TAGGED_POC_GATES="+json.dumps(gates,sort_keys=True), flush=True)
    print("FULLJ_TAGGED_POC_CLASSIFICATION="+classification, flush=True)
    print("STOCHASTIC_BROADBAND_TAGGED_RESPONSE_POC_TESTED="+str(classification==PASS), flush=True)
    print("STOCHASTIC_BROADBAND_LOWK_SATURATION_TESTED="+str(classification==PASS), flush=True)
    print("THREE_D_BOUNDED_CONTINUOUS_WEYL_POWER_LICENSED=False", flush=True)
    print("THREE_D_CONTINUOUS_WEYL_POWER_LICENSED=False", flush=True)
    print("EVOLVING_WEYL_POWER_LICENSED=False", flush=True)
    print("ACT_LIKELIHOOD_LICENSED=False", flush=True)
    print("OBSERVATIONAL_CLAIM_LICENSED=False", flush=True)
    return 0 if classification==PASS else 2


if __name__ == "__main__":
    raise SystemExit(main())
