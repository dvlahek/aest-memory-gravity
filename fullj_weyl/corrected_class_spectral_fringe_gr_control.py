#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

import numpy as np
from scipy.interpolate import CubicSpline

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from nl1c6d2n import corrected_class_baseline as cb
from nl1c6d2a import baryon_matter_sector_audit as d2a

KMASK_RESULT_LOCK = "20151ab785e923de20d720f3fdd8890576b6cc05"
SOURCE_RESULT_LOCK = "86ab13ffa1048860731f65348074ede1b469c644"
GEOMETRY_RESULT_LOCK = "73fb42d64e61d69820d31a9c9f71c8d536b2376e"
DECOMP_RESULT_LOCK = "0e4a3be830e2c6a5e87a7cb259a09bcb459f9d5f"
PREDATA_LOCK = "0e26b4688eeeedd522b8dd153f84a76137d7e43c"

SOURCE_NPZ = ROOT / "results/fullj_spectral_fringe_source_decomposition.npz"
SOURCE_JSON = ROOT / "results/fullj_spectral_fringe_source_decomposition.json"
SOURCE_NPZ_SHA256 = "02dc87e3740db25460e085897a1fb35540f331f37076b94aa7ab03c8c76255c1"

SUPPORTED = "FULLJ_CORRECTED_CLASS_SPECTRAL_FRINGE_AEST_SPECIFIC_SUPPORTED"
GENERIC = "FULLJ_CORRECTED_CLASS_SPECTRAL_FRINGE_GENERIC_OR_NOT_SPECIFIC"
NUMFAIL = "FULLJ_CORRECTED_CLASS_SPECTRAL_FRINGE_NUMERICAL_CONTROL_FAIL"
INCOMPLETE = "FULLJ_CORRECTED_CLASS_SPECTRAL_FRINGE_INCOMPLETE"

CHECK_Z = np.asarray([6.0, 5.0, 4.0, 3.0, 2.0, 1.5, 1.0, 0.5, 0.2], float)
CENTERS = np.asarray([0.10125, 0.16375, 0.19625], float)
DK = 0.000625
WINDOWS = [c + DK * np.arange(-8, 9, dtype=float) for c in CENTERS]
K_DENSE = np.concatenate(WINDOWS)
K_ANCHOR = np.asarray([
    0.09875, 0.10000, 0.10125, 0.10250, 0.10375,
    0.16125, 0.16250, 0.16375, 0.16500, 0.16625,
    0.19375, 0.19500, 0.19625, 0.19750, 0.19875,
], float)

ANCHOR_GLOBAL_GATE = 2.0e-5
ANCHOR_PERK_GATE = 5.0e-5
LIST_GLOBAL_GATE = 1.0e-6
LIST_PERK_GATE = 5.0e-6
MIN_EXTREMA_PER_WINDOW = 2
MIN_AEST_KAPPA = 5.0e-2
MIN_SPEC_RATIO = 10.0


def is_ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"],
        cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    ).returncode == 0


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def rel(a, b) -> float:
    aa = np.asarray(a, float)
    bb = np.asarray(b, float)
    return float(np.linalg.norm(aa-bb) / max(float(np.linalg.norm(aa)), float(np.linalg.norm(bb)), 1e-300))


def index_of(grid, value):
    q = np.where(np.isclose(np.asarray(grid, float), float(value), rtol=0.0, atol=5e-13))[0]
    if len(q) != 1:
        raise RuntimeError(f"nonunique/missing k={value}")
    return int(q[0])


def unique_spline_x(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    if x.shape != y.shape:
        raise RuntimeError("history shape mismatch")
    order = np.argsort(x)
    xs = x[order]; ys = y[order]
    finite = np.isfinite(xs) & np.isfinite(ys)
    xs = xs[finite]; ys = ys[finite]
    if xs.size < 4:
        raise RuntimeError("insufficient finite history samples")
    keep = np.ones(xs.size, dtype=bool)
    keep[1:] = np.diff(xs) > 0.0
    xs = xs[keep]; ys = ys[keep]
    if xs.size < 4 or np.any(np.diff(xs) <= 0.0):
        raise RuntimeError("non-monotone history coordinate")
    return CubicSpline(xs, ys, bc_type="not-a-knot"), xs


def run_direct_class(k_h, aest_enabled: bool):
    from classy import Class

    kh = np.asarray(k_h, float)
    pars = dict(cb.build_params())
    pars.update({
        "output": "mTk,vTk",
        "lensing": "no",
        "k_output_values": ", ".join(f"{x*cb.h:.17g}" for x in kh),
        "P_k_max_h/Mpc": 0.30,
        "z_max_pk": 6.5,
        "aest_memory_enabled": "no",
        "aest_eta": 0.0,
        "aest_enabled": "yes" if aest_enabled else "no",
    })

    c = Class()
    c.set(pars)
    c.compute()
    try:
        pert = c.get_perturbations()
        histories, scalar_key = d2a.scalar_histories(pert)
        if len(histories) != len(kh):
            raise RuntimeError(f"history count {len(histories)} != requested {len(kh)}")

        out = np.full((len(kh), len(CHECK_Z)), np.nan, float)
        cover = []
        for i, raw in enumerate(histories):
            akey = d2a.pick(raw, "a", ("scale factor",))
            pkey = d2a.pick(raw, "phi")
            pskey = d2a.pick(raw, "psi")
            aa = np.asarray(raw[akey], float)
            phi = np.asarray(raw[pkey], float)
            psi = np.asarray(raw[pskey], float)
            sp, xs = unique_spline_x(aa, phi + psi)
            at = 1.0/(1.0+CHECK_Z)
            ok = bool(float(np.min(xs)) <= float(np.min(at))+1e-12 and float(np.max(xs)) >= float(np.max(at))-1e-12)
            cover.append(ok)
            if not ok:
                raise RuntimeError(f"history {i} lacks z=6..0.2 coverage")
            out[i, :] = sp(at)
        return {
            "W": out,
            "all_finite": bool(np.all(np.isfinite(out))),
            "coverage": bool(all(cover)),
            "scalar_key": scalar_key,
            "parameters": pars,
        }
    finally:
        c.struct_cleanup()
        c.empty()


def load_source_reference():
    if not SOURCE_NPZ.exists() or not SOURCE_JSON.exists():
        raise FileNotFoundError("missing source-decomposition JSON/NPZ")
    digest = sha256_file(SOURCE_NPZ)
    if digest != SOURCE_NPZ_SHA256:
        raise RuntimeError(f"source-decomposition NPZ SHA mismatch {digest}")
    meta = json.loads(SOURCE_JSON.read_text())
    if meta.get("classification") != "FULLJ_SPECTRAL_FRINGE_SOURCE_DECOMPOSITION_CORRECTED_CLASS_LINEAR_SECTOR_DOMINATED":
        raise RuntimeError("source-decomposition classification mismatch")
    q = np.load(SOURCE_NPZ)
    nodes = np.asarray(q["merged_nodes"], float)
    wclass = np.asarray(q["merged__W_CLASS"], complex)
    if not np.allclose(nodes, K_ANCHOR, rtol=0.0, atol=5e-13):
        raise RuntimeError("source-decomposition merged nodes are not frozen anchors")
    if wclass.shape != (len(K_ANCHOR), len(CHECK_Z)):
        raise RuntimeError(f"source W_CLASS shape mismatch {wclass.shape}")
    imag_ratio = float(np.linalg.norm(np.imag(wclass))/max(float(np.linalg.norm(np.real(wclass))),1e-300))
    return digest, np.real(wclass), imag_ratio


def extrema_count(y):
    a = np.asarray(y, float)
    mid = a[1:-1]
    maxima = (mid > a[:-2]) & (mid > a[2:])
    minima = (mid < a[:-2]) & (mid < a[2:])
    return int(np.count_nonzero(maxima | minima))


def d2_concat(w, iz):
    vals = []
    raws = []
    for iw in range(3):
        a = np.asarray(w[iw*17:(iw+1)*17, iz], float)
        vals.append(a[2:] - 2.0*a[1:-1] + a[:-2])
        raws.append(a)
    return np.concatenate(vals), np.concatenate(raws)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json-out", default="results/fullj_corrected_class_spectral_fringe_gr_control.json")
    ap.add_argument("--npz-out", default="results/fullj_corrected_class_spectral_fringe_gr_control.npz")
    args = ap.parse_args()

    ancestry = {
        "physical_kmask_repair_result_lock": is_ancestor(KMASK_RESULT_LOCK),
        "source_localization_result_lock": is_ancestor(SOURCE_RESULT_LOCK),
        "geometry_certification_result_lock": is_ancestor(GEOMETRY_RESULT_LOCK),
        "source_decomposition_result_lock": is_ancestor(DECOMP_RESULT_LOCK),
        "predata_lock": is_ancestor(PREDATA_LOCK),
    }

    class_root = Path(os.environ.get("NL1C6D2N_CLASS_ROOT", ""))
    class_ok = False
    class_head = "missing"
    source_sha = "missing"
    if class_root.exists() and (class_root/".git").exists() and (class_root/"source/aest_memory.c").exists():
        class_head = subprocess.check_output(["git","rev-parse","HEAD"], cwd=class_root, text=True).strip()
        source_sha = sha256_file(class_root/"source/aest_memory.c")
        class_ok = bool(class_head == cb.CLASS_SHA and source_sha == cb.CORRECTED_SOURCE_SHA)

    exact_grid = bool(
        len(K_DENSE) == 51 and len(np.unique(np.round(K_DENSE, 12))) == 51
        and all(len(w) == 17 for w in WINDOWS)
        and np.allclose(np.diff(WINDOWS[0]), DK, rtol=0, atol=1e-14)
        and all(any(np.isclose(K_DENSE, a, rtol=0, atol=5e-13)) for a in K_ANCHOR)
    )
    frozen = bool(class_ok and exact_grid and len(K_ANCHOR) == 15)

    print("FULLJ_DIRECT_CLASS_FRINGE_START", flush=True)
    print("FULLJ_DIRECT_CLASS_FRINGE_ANCESTRY="+json.dumps(ancestry,sort_keys=True), flush=True)
    print(f"FULLJ_DIRECT_CLASS_FRINGE_CLASS_PROVENANCE head={class_head} source_sha256={source_sha} pass={class_ok}", flush=True)
    print(f"FULLJ_DIRECT_CLASS_FRINGE_GRID dense={len(K_DENSE)} anchors={len(K_ANCHOR)} dk_h={DK:.9f}", flush=True)

    try:
        src_digest, source_anchor, source_imag_ratio = load_source_reference()
    except Exception as exc:
        out={"classification":INCOMPLETE,"diagnostic_complete":False,"reason":str(exc),"ancestry":ancestry,"frozen_setup":frozen}
        Path(args.json_out).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
        print("FULLJ_DIRECT_CLASS_FRINGE_CLASSIFICATION="+INCOMPLETE, flush=True)
        return 3

    if not all(ancestry.values()) or not frozen:
        out={"classification":INCOMPLETE,"diagnostic_complete":False,"ancestry":ancestry,"frozen_setup":frozen,
             "class_head":class_head,"class_source_sha256":source_sha,"source_npz_sha256":src_digest}
        Path(args.json_out).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
        print("FULLJ_DIRECT_CLASS_FRINGE_CLASSIFICATION="+INCOMPLETE, flush=True)
        return 3

    print("FULLJ_DIRECT_CLASS_FRINGE_RUN aest_dense_51", flush=True)
    aest_dense = run_direct_class(K_DENSE, True)
    print("FULLJ_DIRECT_CLASS_FRINGE_RUN aest_sparse_15", flush=True)
    aest_sparse = run_direct_class(K_ANCHOR, True)
    print("FULLJ_DIRECT_CLASS_FRINGE_RUN gr_dense_51", flush=True)
    gr_dense = run_direct_class(K_DENSE, False)

    idx_anchor = np.asarray([index_of(K_DENSE, a) for a in K_ANCHOR], int)
    dense_anchor = aest_dense["W"][idx_anchor]
    sparse_anchor = aest_sparse["W"]

    anchor_global = rel(sparse_anchor, source_anchor)
    anchor_per = [rel(sparse_anchor[i], source_anchor[i]) for i in range(len(K_ANCHOR))]
    list_global = rel(dense_anchor, sparse_anchor)
    list_per = [rel(dense_anchor[i], sparse_anchor[i]) for i in range(len(K_ANCHOR))]

    iz = int(np.where(np.isclose(CHECK_Z,0.2,rtol=0,atol=1e-14))[0][0])
    extrema = [extrema_count(aest_dense["W"][i*17:(i+1)*17, iz]) for i in range(3)]
    d2aest, rawaest = d2_concat(aest_dense["W"], iz)
    d2gr, rawgr = d2_concat(gr_dense["W"], iz)
    kappa_aest = float(np.linalg.norm(d2aest)/max(float(np.linalg.norm(rawaest)),1e-300))
    kappa_gr = float(np.linalg.norm(d2gr)/max(float(np.linalg.norm(rawgr)),1e-300))
    spec_ratio = float(kappa_aest/max(kappa_gr,1e-300))

    g1 = bool(all(ancestry.values()) and frozen)
    g2 = bool(anchor_global <= ANCHOR_GLOBAL_GATE and max(anchor_per) <= ANCHOR_PERK_GATE)
    g3 = bool(list_global <= LIST_GLOBAL_GATE and max(list_per) <= LIST_PERK_GATE)
    g4 = bool(aest_dense["all_finite"] and aest_dense["coverage"] and aest_sparse["all_finite"] and aest_sparse["coverage"]
              and gr_dense["all_finite"] and gr_dense["coverage"])
    g5 = bool(all(n >= MIN_EXTREMA_PER_WINDOW for n in extrema))
    g6 = bool(kappa_aest >= MIN_AEST_KAPPA and spec_ratio >= MIN_SPEC_RATIO)

    gates={
        "DG_G1_provenance_and_exact_setup":g1,
        "DG_G2_direct_AeST_anchor_reproduction":g2,
        "DG_G3_requested_k_list_invariance":g3,
        "DG_G4_dense_grid_health":g4,
        "DG_G5_fine_grid_spectral_structure":g5,
        "DG_G6_AeST_specificity_against_GR":g6,
    }

    if not (g2 and g3 and g4):
        classification=NUMFAIL
    elif g1 and g5 and g6:
        classification=SUPPORTED
    elif g1 and g5 and not g6:
        classification=GENERIC
    else:
        classification=INCOMPLETE

    summary={
        "source_anchor_imag_ratio":source_imag_ratio,
        "anchor_reproduction_global_relative_L2":anchor_global,
        "anchor_reproduction_per_k_max":float(max(anchor_per)),
        "k_list_invariance_global_relative_L2":list_global,
        "k_list_invariance_per_k_max":float(max(list_per)),
        "z0p2_extrema_per_window":extrema,
        "z0p2_kappa_AeST":kappa_aest,
        "z0p2_kappa_GR":kappa_gr,
        "z0p2_specificity_ratio":spec_ratio,
    }

    out={
        "classification":classification,
        "diagnostic_complete":True,
        "frozen_setup":frozen,
        "ancestry":ancestry,
        "source_npz_sha256":src_digest,
        "class_head":class_head,
        "class_source_sha256":source_sha,
        "k_dense_h_Mpc":K_DENSE.tolist(),
        "k_anchor_h_Mpc":K_ANCHOR.tolist(),
        "redshifts":CHECK_Z.tolist(),
        "summary":summary,
        "gates":gates,
        "thresholds":{
            "anchor_global":ANCHOR_GLOBAL_GATE,"anchor_per_k":ANCHOR_PERK_GATE,
            "list_global":LIST_GLOBAL_GATE,"list_per_k":LIST_PERK_GATE,
            "min_extrema_per_window":MIN_EXTREMA_PER_WINDOW,
            "min_AeST_kappa":MIN_AEST_KAPPA,"min_specificity_ratio":MIN_SPEC_RATIO,
        },
        "licenses":{
            "DIRECT_CORRECTED_CLASS_FINE_K_SPECTROSCOPY_TESTED":bool(g1 and g2 and g3 and g4),
            "AEST_SPECIFIC_SPECTRAL_FRINGE_SUPPORTED":bool(classification==SUPPORTED),
            "EVOLVING_WEYL_POWER_LICENSED":False,
            "ACT_LIKELIHOOD_LICENSED":False,
            "OBSERVATIONAL_CLAIM_LICENSED":False,
        },
    }
    Path(args.json_out).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    np.savez_compressed(
        args.npz_out,
        redshifts=CHECK_Z,
        k_dense_h_Mpc=K_DENSE,
        k_anchor_h_Mpc=K_ANCHOR,
        source_anchor_W_CLASS=source_anchor,
        aest_dense_W=aest_dense["W"],
        aest_sparse_W=aest_sparse["W"],
        gr_dense_W=gr_dense["W"],
        z0p2_D2_AeST=d2aest,
        z0p2_D2_GR=d2gr,
    )

    print("FULLJ_DIRECT_CLASS_FRINGE_SUMMARY="+json.dumps(summary,sort_keys=True), flush=True)
    print("FULLJ_DIRECT_CLASS_FRINGE_GATES="+json.dumps(gates,sort_keys=True), flush=True)
    print("FULLJ_DIRECT_CLASS_FRINGE_CLASSIFICATION="+classification, flush=True)
    return 0 if classification in (SUPPORTED,GENERIC) else 1


if __name__ == "__main__":
    raise SystemExit(main())
