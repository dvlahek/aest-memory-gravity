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
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fullj_weyl import aest_stable_chi_precision_convergence as pc

PREDATA_LOCK = "4b7acaf908e91a83b2fa69260ae3dbd13ad2226b"
PARENT_CLASS = "FULLJ_AEST_STABLE_CHI_NOT_PRECISION_CONVERGED"
PARENT_JSON = ROOT / "results/fullj_aest_stable_chi_precision_convergence.json"
PARENT_STABLE_NPZ = ROOT / "results/fullj_aest_stable_chi_precision_stable.npz"
TARGETS = (0.09875, 0.10000, 0.10125)
CONTROL = 0.19750
ANCHORS = TARGETS + (CONTROL,)
TOLS = (1e-7, 3e-8)
PARENT_TOL = 3e-7
PLATEAU = 1e-6

INCOMPLETE = "FULLJ_AEST_STABLE_CHI_PRECISION_FLOOR_INCOMPLETE"
NOT_REACHED = "FULLJ_AEST_STABLE_CHI_PRECISION_FLOOR_NOT_REACHED"
ULP_FAIL = "FULLJ_AEST_STABLE_CHI_PRECISION_FLOOR_ULP_FAIL"
IDENT_FAIL = "FULLJ_AEST_STABLE_CHI_PRECISION_FLOOR_IDENTITY_FAIL"
PASS = "FULLJ_AEST_STABLE_CHI_PRECISION_FLOOR_CERTIFIED"


def is_ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"], cwd=ROOT,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    ).returncode == 0


def rel(a, b) -> float:
    aa = np.asarray(a, float)
    bb = np.asarray(b, float)
    return float(np.linalg.norm(aa-bb) / max(float(np.linalg.norm(aa)), float(np.linalg.norm(bb)), 1e-300))


def stable_source_ok() -> bool:
    root = os.environ.get("AEST_STABLE_CLASS_ROOT", "")
    if not root:
        return False
    ph = Path(root) / "include" / "perturbations.h"
    src = Path(root) / "source" / "perturbations.c"
    if not ph.is_file() or not src.is_file():
        return False
    text = ph.read_text() + "\n" + src.read_text()
    required = (
        "FULLJ_AEST_STABLE_CHI_RESIDUAL_V1",
        "index_pt_s_aest",
        "double chi_aest = Q_aest*s_aest;",
        "3.*cad2_aest*a_prime_over_a*(s_aest-alpha_aest)",
    )
    return all(x in text for x in required)


def parent_key(kh: float) -> str:
    return f"W_3em07_{pc.tag_of(kh)}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json-out", default="results/fullj_aest_stable_chi_precision_floor.json")
    ap.add_argument("--npz-out", default="results/fullj_aest_stable_chi_precision_floor.npz")
    args = ap.parse_args()

    print("FULLJ_AEST_STABLE_CHI_FLOOR_START", flush=True)

    if not PARENT_JSON.exists() or not PARENT_STABLE_NPZ.exists():
        out = {"classification": INCOMPLETE, "diagnostic_complete": False,
               "reason": "missing parent precision result"}
        Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True)+"\n")
        print("FULLJ_AEST_STABLE_CHI_FLOOR_CLASSIFICATION="+INCOMPLETE, flush=True)
        return 3

    parent = json.loads(PARENT_JSON.read_text())
    pnpz = np.load(PARENT_STABLE_NPZ)
    g1 = bool(
        is_ancestor(PREDATA_LOCK)
        and parent.get("classification") == PARENT_CLASS
        and parent.get("diagnostic_complete") is True
        and stable_source_ok()
    )

    arrays = {}
    rows = []
    all_plateau = True
    targets_plateau = True
    ulp_ok = True
    identity_ok = True

    for kh in ANCHORS:
        bits = pc.bits_for_anchor(kh)
        tag = pc.tag_of(kh)
        pk = parent_key(kh)
        if pk not in pnpz:
            raise RuntimeError(f"missing parent stable key {pk}")
        W37 = np.asarray(pnpz[pk], float)
        arrays[f"W_3em07_{tag}"] = W37

        direct = {}
        raw_tight = None
        kval_tight = None
        for tol in TOLS:
            raw, nh, pos, kval = pc.raw_for(kh, bits, tol)
            W = pc.W_at_z(raw)
            direct[tol] = W
            tl = f"{tol:.0e}".replace("-", "m")
            arrays[f"W_{tl}_{tag}"] = W
            if tol == TOLS[-1]:
                raw_tight = raw
                kval_tight = kval
            print(
                f"FULLJ_AEST_STABLE_CHI_FLOOR_COLLECT k_h={kh:.5f} tol={tol:.1e} histories={nh} pos={pos}",
                flush=True,
            )

        c17 = rel(direct[1e-7], direct[3e-8])
        c37 = rel(W37, direct[3e-8])
        plateau = bool(c17 <= PLATEAU and c37 <= PLATEAU)
        all_plateau &= plateau
        if kh in TARGETS:
            targets_plateau &= plateau

        # Tight adjacent-ULP control.
        rawB, _, _, _ = pc.raw_for(kh, bits+1, 3e-8)
        WB = pc.W_at_z(rawB)
        u = rel(direct[3e-8], WB)
        arrays[f"W_nextulp_3em08_{tag}"] = WB
        this_ulp = bool(u <= PLATEAU)
        ulp_ok &= this_ulp

        sid, nmask = pc.dense_s_identity(raw_tight, kval_tight)
        this_ident = bool(nmask >= 8 and sid <= PLATEAU)
        identity_ok &= this_ident

        row = {
            "k_h": float(kh), "bits_direct": int(bits), "bits_next": int(bits+1),
            "C_1e7_to_3e8": float(c17), "C_3e7_to_3e8": float(c37),
            "plateau_pass": plateau, "tight_ULP_relL2": float(u), "tight_ULP_pass": this_ulp,
            "s_identity_relL2": float(sid), "s_identity_point_count": int(nmask),
            "identity_pass": this_ident, "role": "target" if kh in TARGETS else "control",
        }
        rows.append(row)
        print(
            f"FULLJ_AEST_STABLE_CHI_FLOOR_ANCHOR k_h={kh:.5f} "
            f"C17={c17:.3e} C37={c37:.3e} ULP={u:.3e} sid={sid:.3e} plateau={plateau}",
            flush=True,
        )

    g2 = bool(all_plateau)
    g3 = bool(targets_plateau)
    g4 = bool(ulp_ok)
    g5 = bool(identity_ok)
    gates = {
        "PF_G1_provenance_and_parent_lock": g1,
        "PF_G2_primary_Cauchy_plateau": g2,
        "PF_G3_targeted_nonmonotone_anchor_closure": g3,
        "PF_G4_tight_adjacent_ULP_continuity": g4,
        "PF_G5_residual_state_identity": g5,
    }

    if not g1:
        classification = INCOMPLETE
    elif not g2 or not g3:
        classification = NOT_REACHED
    elif not g4:
        classification = ULP_FAIL
    elif not g5:
        classification = IDENT_FAIL
    else:
        classification = PASS

    summary = {
        "classification": classification,
        "anchor_count": len(rows),
        "target_count": len(TARGETS),
        "plateau_pass_count": int(sum(r["plateau_pass"] for r in rows)),
        "max_C_1e7_to_3e8": float(max(r["C_1e7_to_3e8"] for r in rows)),
        "max_C_3e7_to_3e8": float(max(r["C_3e7_to_3e8"] for r in rows)),
        "max_tight_ULP_relL2": float(max(r["tight_ULP_relL2"] for r in rows)),
        "max_identity_relL2": float(max(r["s_identity_relL2"] for r in rows)),
    }
    out = {
        "classification": classification,
        "diagnostic_complete": True,
        "predata_lock": PREDATA_LOCK,
        "parent_classification": parent.get("classification"),
        "gates": gates,
        "summary": summary,
        "anchors": rows,
        "interpretation": {
            "parent_reclassified": False,
            "historical_R3_reclassified": False,
            "new_physics_claim_licensed": False,
            "physical_instability_claim_licensed": False,
            "stable_AeST_host_followup_licensed": classification == PASS,
        },
    }

    Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True)+"\n")
    np.savez_compressed(args.npz_out, redshifts=pc.Z, **arrays)
    print("FULLJ_AEST_STABLE_CHI_FLOOR_GATES="+json.dumps(gates, sort_keys=True), flush=True)
    print("FULLJ_AEST_STABLE_CHI_FLOOR_SUMMARY="+json.dumps(summary, sort_keys=True), flush=True)
    print("FULLJ_AEST_STABLE_CHI_FLOOR_CLASSIFICATION="+classification, flush=True)
    return 0 if classification == PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
