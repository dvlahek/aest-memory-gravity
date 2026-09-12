#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import math
import re
import subprocess
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
R2_RESULT_LOCK = "1f42f88e9724c58d2d242a65ca7266a207e4a0f8"
PREDATA_LOCK = "e78114baae0ad955f954d4f1d93d70959af85fcd"
R2_PASS = "FULLJ_EVOLVING_WEYL_BRIDGE_R2_PASS"
PASS = "FULLJ_EVOLVING_WEYL_COVARIANCE_DIAGNOSTIC_PASS"
FAIL = "FULLJ_EVOLVING_WEYL_COVARIANCE_DIAGNOSTIC_FAIL"
INCOMPLETE = "FULLJ_EVOLVING_WEYL_COVARIANCE_DIAGNOSTIC_INCOMPLETE"
ALG_GATE = 1.0e-12
RANK_FRAC = 1.0e-12
KINDS = ("simple", "exponential", "sharp")
BETAS = (1.0, 0.5, 0.1)
SIGMAS = (-1, 0, 1)


def git_head():
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()


def is_ancestor(sha):
    return subprocess.run(["git", "merge-base", "--is-ancestor", sha, "HEAD"], cwd=ROOT,
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0


def rel(a, b):
    aa = np.asarray(a)
    bb = np.asarray(b)
    return float(np.linalg.norm(aa-b) / max(float(np.linalg.norm(aa)), float(np.linalg.norm(bb)), 1e-300))


def parse_name(s):
    m = re.fullmatch(r"sigma=([+-]?\d+)\|kind=([^|]+)\|beta0=([0-9.]+)", str(s))
    if not m:
        raise ValueError(f"bad member label: {s}")
    return int(m.group(1)), m.group(2), float(m.group(3))


def covariance_metrics(samples):
    x = np.asarray(samples, complex)
    if x.ndim != 2 or x.shape[0] < 2:
        raise ValueError("need sample x mode matrix with at least two samples")
    xc = x - np.mean(x, axis=0, keepdims=True)
    C = (xc.conj().T @ xc) / float(x.shape[0]-1)
    herm = rel(C, C.conj().T)
    H = 0.5*(C + C.conj().T)
    eig = np.linalg.eigvalsh(H)
    scale = max(float(np.max(np.abs(eig))), 1e-300)
    min_eig_rel = float(np.min(eig)/scale)
    rank = int(np.sum(eig > RANK_FRAC*scale))
    tr = float(np.real(np.trace(H)))
    mse = float(np.sum(np.abs(xc)**2) / float(x.shape[0]-1))
    trace_rel = abs(tr-mse)/max(abs(tr), abs(mse), 1e-300)
    diag = np.diag(np.diag(H))
    off = float(np.linalg.norm(H-diag)/max(float(np.linalg.norm(H)), 1e-300))
    return C, {
        "hermiticity_relative_residual": herm,
        "min_eigenvalue_relative": min_eig_rel,
        "numerical_rank": rank,
        "trace": tr,
        "trace_identity_relative_residual": trace_rel,
        "offdiag_frobenius_fraction": off,
        "finite": bool(np.all(np.isfinite(C))),
    }


def stats(vals):
    a = np.asarray(vals, float)
    return {"min": float(np.min(a)), "median": float(np.median(a)), "max": float(np.max(a))}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--r2-json", default="results/fullj_evolving_weyl_bridge_r2.json")
    ap.add_argument("--r2-npz", default="results/fullj_evolving_weyl_bridge_r2.npz")
    ap.add_argument("--json-out", default="results/fullj_evolving_weyl_covariance_diagnostic.json")
    ap.add_argument("--csv-out", default="results/fullj_evolving_weyl_covariance_diagnostic.csv")
    ap.add_argument("--npz-out", default="results/fullj_evolving_weyl_covariance_diagnostic.npz")
    args = ap.parse_args()

    ancestry = {"r2_result_lock": is_ancestor(R2_RESULT_LOCK), "predata_lock": is_ancestor(PREDATA_LOCK)}
    r2j = Path(args.r2_json); r2n = Path(args.r2_npz)
    if not r2j.exists() or not r2n.exists() or not all(ancestry.values()):
        result = {"classification": INCOMPLETE, "diagnostic_complete": False, "ancestry": ancestry,
                  "reason": "missing locked R2 input or ancestry"}
        Path(args.json_out).write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
        print("FULLJ_EVOLVING_WEYL_COVARIANCE_CLASSIFICATION="+INCOMPLETE)
        return 2

    meta = json.loads(r2j.read_text())
    if meta.get("classification") != R2_PASS:
        raise RuntimeError("R2 input classification is not PASS")
    d = np.load(r2n, allow_pickle=False)
    names = [str(x) for x in d["member_names"]]
    z = np.asarray(d["z"], float)
    modes = np.asarray(d["mode_number"], int)
    W = np.asarray(d["W"], complex)
    if W.shape != (27,9,33) or z.shape != (9,) or modes.shape != (33,):
        raise RuntimeError(f"unexpected R2 shapes W={W.shape} z={z.shape} modes={modes.shape}")
    if not np.all(np.isfinite(W)):
        raise RuntimeError("non-finite R2 Weyl input")

    index = {}
    for i, name in enumerate(names):
        key = parse_name(name)
        if key in index:
            raise RuntimeError(f"duplicate member key {key}")
        index[key] = i
    expected = {(s,k,b) for s in SIGMAS for k in KINDS for b in BETAS}
    if set(index) != expected:
        raise RuntimeError("member grid does not match locked 3x3x3 grid")

    rows=[]; primary=[]; branch_labels=[]
    herms=[]; mineigs=[]; traces=[]; offs=[]; traceids=[]; ranks=[]; finite_all=True
    for kind in KINDS:
        for beta in BETAS:
            branch_labels.append(f"kind={kind}|beta0={beta:g}")
            mats=[]
            for iz, zz in enumerate(z):
                samp=np.stack([W[index[(s,kind,beta)],iz,:] for s in SIGMAS], axis=0)
                C, mm=covariance_metrics(samp)
                mats.append(C)
                finite_all &= mm["finite"]
                herms.append(mm["hermiticity_relative_residual"]); mineigs.append(mm["min_eigenvalue_relative"])
                traces.append(mm["trace"]); offs.append(mm["offdiag_frobenius_fraction"])
                traceids.append(mm["trace_identity_relative_residual"]); ranks.append(mm["numerical_rank"])
                rows.append({"scope":"phase_conditioned","kind":kind,"beta0":beta,"z":float(zz),**mm})
            primary.append(mats)
    primary=np.asarray(primary, complex)  # 9,9,33,33

    secondary=[]; sec_rows=[]; sec_herm=[]; sec_mineig=[]
    for iz, zz in enumerate(z):
        C, mm=covariance_metrics(W[:,iz,:])
        secondary.append(C); sec_herm.append(mm["hermiticity_relative_residual"]); sec_mineig.append(mm["min_eigenvalue_relative"])
        sec_rows.append({"scope":"theory_grid_nonstochastic","kind":"ALL","beta0":math.nan,"z":float(zz),**mm})
    secondary=np.asarray(secondary, complex)
    rows.extend(sec_rows)

    gates={
        "G1_locked_R2_provenance": bool(meta.get("classification")==R2_PASS and all(ancestry.values()) and W.shape==(27,9,33) and set(index)==expected),
        "G2_finite_covariance_construction": bool(finite_all and np.all(np.isfinite(primary)) and np.all(np.isfinite(secondary))),
        "G3_hermiticity": bool(max(herms+sec_herm) <= ALG_GATE),
        "G4_positive_semidefinite_consistency": bool(min(mineigs+sec_mineig) >= -ALG_GATE),
        "G5_sample_covariance_trace_identity": bool(max(traceids) <= ALG_GATE),
        "G6_structural_phase_rank_le_2": bool(max(ranks) <= 2),
    }
    classification = PASS if all(gates.values()) else FAIL
    summary={
        "primary_matrices":81,
        "secondary_matrices":9,
        "modes":33,
        "max_primary_hermiticity_relative_residual":max(herms),
        "min_primary_eigenvalue_relative":min(mineigs),
        "max_primary_trace_identity_relative_residual":max(traceids),
        "primary_numerical_rank":stats(ranks),
        "primary_trace":stats(traces),
        "primary_offdiag_frobenius_fraction":stats(offs),
        "max_secondary_hermiticity_relative_residual":max(sec_herm),
        "min_secondary_eigenvalue_relative":min(sec_mineig),
    }
    result={
        "classification":classification,"diagnostic_complete":True,"git_head":git_head(),"ancestry":ancestry,
        "input_classification":R2_PASS,"gates":gates,"summary":summary,
        "primary_definition":"centered sample covariance over sigma=-1,0,+1 at fixed (kind,beta0,z)",
        "secondary_definition":"centered 27-member theory-grid sensitivity covariance; non-stochastic",
        "structural_rank_limit":2,"rows":rows,
        "EVOLVING_WEYL_COVARIANCE_DIAGNOSTIC_TESTED":True,
        "EVOLVING_WEYL_POWER_LICENSED":False,"ACT_LIKELIHOOD_LICENSED":False,
        "OBSERVATIONAL_CLAIM_LICENSED":False,"THEORY_GRID_IS_COSMOLOGICAL_ENSEMBLE":False,
    }
    jout=Path(args.json_out); cout=Path(args.csv_out); nout=Path(args.npz_out)
    for p in (jout,cout,nout): p.parent.mkdir(parents=True,exist_ok=True)
    jout.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=True)+"\n")
    with cout.open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    np.savez_compressed(nout,z=z,mode_number=modes,branch_labels=np.asarray(branch_labels,dtype="U48"),
                        C_primary_real=primary.real,C_primary_imag=primary.imag,
                        C_theory_grid_real=secondary.real,C_theory_grid_imag=secondary.imag)

    print("FULLJ_EVOLVING_WEYL_COV_SUMMARY="+json.dumps(summary,sort_keys=True),flush=True)
    print("FULLJ_EVOLVING_WEYL_COV_GATES="+json.dumps(gates,sort_keys=True),flush=True)
    print("FULLJ_EVOLVING_WEYL_COVARIANCE_CLASSIFICATION="+classification,flush=True)
    print("EVOLVING_WEYL_COVARIANCE_DIAGNOSTIC_TESTED=True",flush=True)
    print("EVOLVING_WEYL_POWER_LICENSED=False",flush=True)
    print("ACT_LIKELIHOOD_LICENSED=False",flush=True)
    print("OBSERVATIONAL_CLAIM_LICENSED=False",flush=True)
    print("THEORY_GRID_IS_COSMOLOGICAL_ENSEMBLE=False",flush=True)
    return 0 if classification==PASS else 2


if __name__ == "__main__":
    raise SystemExit(main())
