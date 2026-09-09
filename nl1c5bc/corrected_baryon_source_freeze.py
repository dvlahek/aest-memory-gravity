#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from v063 import theory_response_map as v63
from nl1c6d2n.corrected_class_baseline_r1 import provenance_audit

CLASS_SHA = "e85808324f51fc694d12e3ed7439552a3c3f9540"
K_H = np.asarray([0.03, 0.05, 0.08, 0.10, 0.15, 0.20], float)
H = float(v63.START["H0"]) / 100.0
K_REQ = K_H * H
TOL = 1.0e-12
PASS_LABEL = "NL1C5BC_CORRECTED_BARYON_SOURCE_FREEZE_PASS"
FAIL_LABEL = "NL1C5BC_CORRECTED_BARYON_SOURCE_FREEZE_FAIL"


def pick(d, key, alts=()):
    if key in d:
        return key
    for a in alts:
        if a in d:
            return a
    raise RuntimeError(f"missing {key}; available={sorted(d.keys())}")


def rel_l2(a, b):
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    return float(np.linalg.norm(a-b) / max(np.linalg.norm(b), 1.0e-300))


def build_params():
    p = dict(v63.class_params())
    p.update({
        "output": "mPk,mTk",
        "lensing": "no",
        "k_output_values": ", ".join(f"{k:.17g}" for k in K_REQ),
        "P_k_max_h/Mpc": 2.0,
        "z_max_pk": 5.0,
        "k_per_decade_for_pk": 80.0,
        "k_per_decade_for_bao": 560.0,
        "aest_memory_enabled": "no",
        "aest_eta": 0.0,
    })
    return p


def extract(pars):
    from classy import Class
    c = Class()
    c.set(pars)
    c.compute()
    try:
        tk, k, z = c.get_transfer_and_k_and_z(output_format="class", h_units=False)
        kb = pick(tk, "d_b", ("delta_b",))
        km = pick(tk, "d_m", ("delta_m",))
        db = np.asarray(tk[kb], float).copy()
        dm = np.asarray(tk[km], float).copy()
        k = np.asarray(k, float).copy()
        z = np.asarray(z, float).copy()
        if db.shape != (k.size, z.size) or dm.shape != (k.size, z.size):
            raise RuntimeError(
                f"unexpected transfer orientation db={db.shape} dm={dm.shape} k={k.size} z={z.size}"
            )
        context = {}
        for key in sorted(tk.keys()):
            lk = key.lower()
            arr = np.asarray(tk[key])
            if ("ncdm" in lk or "nu" in lk) and arr.shape == dm.shape:
                context[key] = np.asarray(arr, float).copy()
        return {
            "transfer_keys": sorted(tk.keys()),
            "baryon_key": kb,
            "total_matter_key": km,
            "k": k,
            "z": z,
            "d_b": db,
            "d_m": dm,
            "context": context,
        }
    finally:
        c.struct_cleanup()
        c.empty()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json-out", required=True)
    ap.add_argument("--npz-out", required=True)
    args = ap.parse_args()

    class_root = Path(os.environ.get("NL1C6D2N_CLASS_ROOT", ""))
    if not class_root.exists():
        raise RuntimeError("NL1C6D2N_CLASS_ROOT must point to the isolated corrected CLASS tree")

    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=ROOT, text=True).strip()
    except Exception:
        head, branch = "unknown", "unknown"

    provenance = provenance_audit(class_root, head, branch)
    pars = build_params()

    print("NL1C5BC_CORRECTED_BARYON_SOURCE_FREEZE_START", flush=True)
    print(f"repo_head={head} branch={branch}", flush=True)

    a = extract(pars)
    b = extract(pars)

    kh_a = a["k"] / H
    kh_b = b["k"] / H

    finite_db = bool(np.all(np.isfinite(a["d_b"])))
    finite_dm = bool(np.all(np.isfinite(a["d_m"])))

    requested = []
    reqmax = 0.0
    for target in K_H:
        j = int(np.argmin(np.abs(kh_a-target)))
        miss = abs(kh_a[j]-target) / target
        reqmax = max(reqmax, miss)
        requested.append({
            "requested_k_h_per_Mpc": float(target),
            "index": j,
            "actual_k_h_per_Mpc": float(kh_a[j]),
            "relative_miss": float(miss),
        })

    nwin = int(np.count_nonzero((a["z"] >= 0.2) & (a["z"] <= 1.5)))

    same_shape = bool(
        a["d_b"].shape == b["d_b"].shape
        and a["d_m"].shape == b["d_m"].shape
        and a["k"].shape == b["k"].shape
        and a["z"].shape == b["z"].shape
    )
    if same_shape:
        krel = float(np.max(np.abs(kh_a-kh_b) / np.maximum(np.abs(kh_b), 1.0e-300)))
        zabs = float(np.max(np.abs(a["z"]-b["z"])))
        dbrel = rel_l2(a["d_b"], b["d_b"])
        dmrel = rel_l2(a["d_m"], b["d_m"])
    else:
        krel = zabs = dbrel = dmrel = float("inf")

    gates = {
        "C1_corrected_CLASS_provenance": bool(provenance["pass"]),
        "C2_d_b_exists_and_finite": finite_db,
        "C2_d_m_exists_and_finite": finite_dm,
        "C3_requested_k_match_le_1e-12": bool(reqmax <= TOL),
        "C4_minimum_8_native_times_z0p2_1p5": bool(nwin >= 8),
        "C5_duplicate_shapes_identical": same_shape,
        "C5_duplicate_k_rel_le_1e-12": bool(krel <= TOL),
        "C5_duplicate_z_abs_le_1e-12": bool(zabs <= TOL),
        "C5_duplicate_d_b_relL2_le_1e-12": bool(dbrel <= TOL),
        "C5_duplicate_d_m_relL2_le_1e-12": bool(dmrel <= TOL),
    }
    passed = bool(all(gates.values()))
    classification = PASS_LABEL if passed else FAIL_LABEL

    result = {
        "classification": classification,
        "scope": "corrected Exp eta=0 native CLASS baryon-source freeze; no memory forcing, finite eta, likelihood, refit, or nonlinear branch selection",
        "git": {"head": head, "branch": branch},
        "CLASS_commit": CLASS_SHA,
        "provenance": provenance,
        "parameters": pars,
        "transfer_keys": a["transfer_keys"],
        "baryon_key": a["baryon_key"],
        "total_matter_key": a["total_matter_key"],
        "massive_neutrino_context_keys": sorted(a["context"].keys()),
        "grid": {
            "n_k": int(a["k"].size),
            "n_z": int(a["z"].size),
            "native_times_0p2_to_1p5": nwin,
            "requested_k_relative_miss_max": float(reqmax),
            "requested_k": requested,
        },
        "duplicate_extraction": {
            "shape_match": same_shape,
            "k_relative_mismatch_max": krel,
            "z_absolute_mismatch_max": zabs,
            "d_b_relative_L2": dbrel,
            "d_m_relative_L2": dmrel,
        },
        "baryon_state": {
            "all_finite": finite_db,
            "abs_min": float(np.min(np.abs(a["d_b"]))),
            "abs_max": float(np.max(np.abs(a["d_b"]))),
        },
        "gates": gates,
        "historical_results_unchanged": True,
        "historical_source_reused": False,
        "corrected_D2A_licensed": passed,
        "corrected_source_dependent_reclosure_licensed": passed,
        "memory_or_likelihood_licensed": False,
        "NL1C7_authorized": False,
    }

    jout = Path(args.json_out)
    nout = Path(args.npz_out)
    jout.parent.mkdir(parents=True, exist_ok=True)
    jout.write_text(json.dumps(result, indent=2, sort_keys=True, default=str) + "\n")

    save = {
        "k_native_h": kh_a,
        "z_native": a["z"],
        "d_b": a["d_b"],
        "d_m": a["d_m"],
    }
    for key, val in a["context"].items():
        safe = key.replace(" ", "_").replace("/", "_")
        save[f"context_{safe}"] = val
    np.savez_compressed(nout, **save)

    print(f"C1_PROVENANCE pass={gates['C1_corrected_CLASS_provenance']}", flush=True)
    print(f"C2_SOURCE d_b={finite_db} d_m={finite_dm}", flush=True)
    print(f"C3_K requested_max={reqmax:.12e} pass={gates['C3_requested_k_match_le_1e-12']}", flush=True)
    print(f"C4_TIME n={nwin} pass={gates['C4_minimum_8_native_times_z0p2_1p5']}", flush=True)
    print(f"C5_DUP k={krel:.12e} z={zabs:.12e} db={dbrel:.12e} dm={dmrel:.12e} pass={all(v for k,v in gates.items() if k.startswith('C5_'))}", flush=True)
    print(f"CLASSIFICATION={classification}", flush=True)
    print(f"JSON={jout}", flush=True)
    print(f"NPZ={nout}", flush=True)
    print("NL1C5BC_CORRECTED_BARYON_SOURCE_FREEZE_END", flush=True)
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
