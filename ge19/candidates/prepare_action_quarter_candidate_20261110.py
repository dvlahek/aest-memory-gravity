#!/usr/bin/env python3
"""GE19 exploratory action-normalized LINEAR scalar CLASS candidate (NOT CERTIFIED).

Create a *separate sibling copy* of an existing official-v077 CLASS working
tree already patched by the historical v019j script, then change exactly
one original E-row source coefficient: 0.5 -> 0.25.

Never modifies original source tree or historical project patch; does not
compile, run a cosmology, fit DES, certify gauge constraints or detect memory.
"""
from __future__ import annotations
import argparse
import difflib
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

ORIGINAL_CLASS_HEAD="e85808324f51fc694d12e3ed7439552a3c3f9540"
OLD="E_rhs_aest -= 0.5*Q_aest*Bchi_aest;"
NEW="E_rhs_aest -= 0.25*Q_aest*Bchi_aest;"
REL=Path("source/perturbations.c")
ORIGINAL_PATCH=Path(__file__).resolve().parents[2]/"v019j/apply_memory_patch.py"
ORIGINAL_PATCH_BLOB="14796a5ed9e6265ed6810c792a93d7328a109364"

def digest(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def git_output(*args, cwd=None):
    return subprocess.check_output(["git",*args],cwd=cwd,text=True,
                                   stderr=subprocess.PIPE).strip()

def run():
    p=argparse.ArgumentParser()
    p.add_argument("--existing-v019j-class",required=True,type=Path)
    p.add_argument("--candidate-copy",required=True,type=Path)
    p.add_argument("--check-only",action="store_true",help="do not copy or modify anything")
    args=p.parse_args()
    src=args.existing_v019j_class.expanduser().resolve()
    dst=args.candidate_copy.expanduser().resolve()
    if not src.is_dir() or src==dst or src.parent!=dst.parent:
        raise RuntimeError("Source must exist; destination must be distinct SIBLING directory")
    if not {"action","quarter","candidate"}.issubset(set(dst.name.lower().replace("-","_").split("_"))):
        raise RuntimeError("Destination name must include action, quarter and candidate")
    if dst.exists():
        raise RuntimeError("Candidate destination EXISTS; refusing any overwrite")
    if git_output("rev-parse","HEAD",cwd=src)!=ORIGINAL_CLASS_HEAD:
        raise RuntimeError("Original CLASS HEAD differs from frozen v077 reference")
    if git_output("hash-object",str(ORIGINAL_PATCH))!=ORIGINAL_PATCH_BLOB:
        raise RuntimeError("Frozen original historical v019j patch has changed")
    f=src/REL
    if not f.is_file(): raise RuntimeError("Expected patched CLASS perturbations.c missing")
    oldtext=f.read_text()
    if oldtext.count(OLD)!=1 or NEW in oldtext:
        raise RuntimeError("Exactly one historic half-source anchor required, candidate anchor forbidden")
    for anchor in [
        "Bchi_aest *= pba->aest_eta;",
        "dy[pv->index_pt_mem_q_aest+jm] = pj;",
        "dy[pv->index_pt_mem_p_aest+jm] =",
        "dy[pv->index_pt_E_aest] = a*E_rhs_aest/pba->aest_KB-a_prime_over_a*E_aest;",
    ]:
        if anchor not in oldtext:raise RuntimeError("Missing source/auxiliary anchor: "+anchor)
    newtext=oldtext.replace(OLD,NEW,1)
    diff="".join(difflib.unified_diff(
        oldtext.splitlines(True),newtext.splitlines(True),
        fromfile="historic-v019j/source/perturbations.c",
        tofile="exploratory-v019q/source/perturbations.c"))
    print("GE19_ACTION_QUARTER_SOURCE_AUDIT_PASS")
    print(diff)
    if args.check_only:
        print("GE19_ACTION_QUARTER_CHECK_ONLY_NO_COPY")
        return
    # The only project-generated changes are the candidate's C E-row and
    # this explicit, self-describing manifest. Builds must be cleaned.
    shutil.copytree(src,dst,symlinks=True)
    cf=dst/REL
    if digest(cf)!=digest(f):
        raise RuntimeError("Copied candidate source differs before overlay")
    cf.write_text(newtext)
    if digest(f)!=hashlib.sha256(oldtext.encode()).hexdigest():
        raise RuntimeError("CRITICAL original source changed; inspect manually")
    (dst/"GE19_ACTION_QUARTER_CANDIDATE.diff").write_text(diff)
    manifest={
      "classification":"EXPLORATORY_LINEAR_SCALAR_QUARTER_SOURCE_ONLY_NOT_PHYSICS_GO",
      "original_v077_HEAD":ORIGINAL_CLASS_HEAD,
      "original_v019j_patch_git_blob":ORIGINAL_PATCH_BLOB,
      "input_source_sha256":hashlib.sha256(oldtext.encode()).hexdigest(),
      "candidate_source_sha256":hashlib.sha256(newtext.encode()).hexdigest(),
      "changed_file":str(REL),
      "exact_one_line_source_delta":OLD+" => "+NEW,
      "eta_bath_in_Bchi_already":True,
      "E_rhs_divided_by_KB_outside_source":True,
      "original_CLASS_unmodified":True,
      "compile_and_eta0_constraint_regression_completed":False,
      "full_physical_observer_certified":False,
      "observed_DES_memory":False,
      "required_next_action":"Rebuild candidate separately and execute one eta=0/source/constraint regression before any physics promotion or observational claim"
    }
    (dst/"GE19_ACTION_QUARTER_CANDIDATE_MANIFEST.json").write_text(
        json.dumps(manifest,indent=2,sort_keys=True)+"\n")
    print("GE19_ACTION_QUARTER_COPY_CREATED",dst)
    print("GE19_ACTION_QUARTER_BUILD_STALE_REBUILD_REQUIRED")
    print("GE19_ACTION_QUARTER_PHYSICAL_OBSERVER_READY False")

if __name__=="__main__":
    run()
