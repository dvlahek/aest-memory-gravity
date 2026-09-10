#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

from nl1c6r3 import confirm_blocking_branch_z6_sharp_beta1 as hist

NONBLOCKING="NL1C6R3C_CORRECTED_BLOCKING_SNAPSHOT_NONBLOCKING"
BLOCKING="NL1C6R3C_CORRECTED_BLOCKING_SNAPSHOT_BLOCKING"


def git_meta():
    try:
        head=subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip()
        branch=subprocess.check_output(["git","rev-parse","--abbrev-ref","HEAD"],cwd=ROOT,text=True).strip()
    except Exception:
        head,branch="unknown","unknown"
    return head,branch


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input-npz",required=True)
    ap.add_argument("--json-out",required=True)
    args=ap.parse_args()
    p=Path(args.input_npz)
    if not p.is_file(): raise FileNotFoundError(p)

    it,z,a,beta,kind,rhs=hist.first_snapshot(str(p))
    head,branch=git_meta()
    print("NL1C6R3C_CORRECTED_BLOCKING_SNAPSHOT_START",flush=True)
    print(f"index={it} z={z:.16g} a={a:.16g} beta={beta} kind={kind}",flush=True)
    print(f"repo_head={head} branch={branch}",flush=True)

    t0=time.perf_counter()
    screened=hist.summarize_route("screened",rhs,a,beta,kind)
    mass=hist.summarize_route("mass",rhs,a,beta,kind)
    wall=time.perf_counter()-t0
    blocking=bool((not screened["endpoint_valid"]) and (not mass["endpoint_valid"]))
    classification=BLOCKING if blocking else NONBLOCKING

    payload={
        "classification":classification,
        "git":{"head":head,"branch":branch},
        "input_npz":str(p),
        "input_npz_sha256":hist.sha256_file(p),
        "snapshot":{"index":it,"z":z,"a":a},
        "kind":kind,"beta":beta,
        "screened":screened,"mass":mass,
        "neither_route_residual_valid_at_theta1":blocking,
        "historical_R3_solver_reused_unchanged":True,
        "solver_repair_performed":False,
        "historical_results_unchanged":True,
        "full_corrected_R3_licensed":not blocking,
        "memory_or_likelihood_evaluated":False,
        "cosmological_refit_performed":False,
        "NL1C7_authorized":False,
        "total_wall_seconds":float(wall),
    }
    out=Path(args.json_out); out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n")
    print(f"SCREENED endpoint_valid={screened['endpoint_valid']} reason={screened['reason']}",flush=True)
    print(f"MASS endpoint_valid={mass['endpoint_valid']} reason={mass['reason']}",flush=True)
    print(f"CLASSIFICATION={classification}",flush=True)
    print(f"FULL_CORRECTED_R3_LICENSED={not blocking}",flush=True)
    print(f"JSON={out}",flush=True)
    print("NL1C6R3C_CORRECTED_BLOCKING_SNAPSHOT_END",flush=True)
    return 0

if __name__=="__main__":
    raise SystemExit(main())
