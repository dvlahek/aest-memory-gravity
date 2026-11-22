#!/usr/bin/env python3
"""GE19: STAGING-ONLY isolated CLASS source correction, no cosmology run.

Copies a verified historical CLASS v3.3.4 AeST v019+v019j checkout and
makes only: original action quarter-force and leading adiabatic AeST
enthalpy-normalized density in sync/Newtonian gauges. It does NOT derive
the finite-k primordial X/E mode, initial bath transport, scalar Ward,
or a physical matter-Weyl response. Never alter the historical source.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

PINNED_CLASS_HEAD = "e85808324f51fc694d12e3ed7439552a3c3f9540"
SOURCE_BLOBS = {
    "v019/apply_patch_v019.py": "c78484eb916bfee2730759c0bdc813a706bf9a68",
    "v019j/apply_memory_patch.py": "14796a5ed9e6265ed6810c792a93d7328a109364",
}
OLD_FORCE = "E_rhs_aest -= 0.5*Q_aest*Bchi_aest;"
NEW_FORCE = "E_rhs_aest -= 0.25*Q_aest*Bchi_aest;"
OLD_AD = (
    "ppw->pv->y[ppw->pv->index_pt_delta_cdm] = "
    "3./4.*ppw->pv->y[ppw->pv->index_pt_delta_g]; /* cdm density */"
)
NEW_AD = (
    "ppw->pv->y[ppw->pv->index_pt_delta_cdm] =\n"
    "          (pba->aest_enabled == _TRUE_ ? "
    "(1.+ppw->pvecback[pba->index_bg_w_aest]) : 1.)\n"
    "          *3./4.*ppw->pv->y[ppw->pv->index_pt_delta_g]; "
    "/* AeST adiabatic enthalpy density or original CDM */"
)
OLD_GAUGE = (
    "ppw->pv->y[ppw->pv->index_pt_delta_cdm] "
    "-= 3.*a_prime_over_a*alpha;"
)
NEW_GAUGE = (
    "ppw->pv->y[ppw->pv->index_pt_delta_cdm] "
    "-= 3.*(pba->aest_enabled == _TRUE_ ? "
    "(1.+ppw->pvecback[pba->index_bg_w_aest]) : 1.)"
    "*a_prime_over_a*alpha;"
)
REPLACEMENTS = (
    ("original_action_quarter_force", OLD_FORCE, NEW_FORCE),
    ("adiabatic_sync_density_enthalpy", OLD_AD, NEW_AD),
    ("newtonian_density_gauge_enthalpy", OLD_GAUGE, NEW_GAUGE),
)

def file_sha(path: Path):
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()

def check_source(repo: Path, root: Path):
    for name, expected in SOURCE_BLOBS.items():
        path = repo/name
        if not path.is_file():
            raise RuntimeError("MISSING_LOCKED_PROJECT_SOURCE "+name)
        got = subprocess.check_output(
            ["git","hash-object",str(path)], cwd=repo, text=True).strip()
        if got != expected:
            raise RuntimeError("PROJECT_SOURCE_LOCK_CHANGED "+name+" "+got)
    if not (root/"source/perturbations.c").is_file():
        raise RuntimeError("NOT_A_CLASS_ROOT")
    if not (root/".git").exists():
        raise RuntimeError("CLASS_PROVENANCE_GIT_MISSING")
    head = subprocess.check_output(
        ["git","rev-parse","HEAD"],cwd=root,text=True).strip()
    if head != PINNED_CLASS_HEAD:
        raise RuntimeError("CLASS_HEAD_WRONG "+head)
    background=(root/"include/background.h").read_text()
    if "index_bg_w_aest" not in background or "aest_enabled" not in background:
        raise RuntimeError("AEST_BACKGROUND_FIELD_NOT_PRESENT")
    cfile=root/"source/perturbations.c"
    if cfile.is_symlink():
        raise RuntimeError("REFUSE_SYMLINKED_ORIGINAL_C_SOURCE")
    raw=cfile.read_text()
    if "index_pt_mem_p_aest" not in raw:
        raise RuntimeError("EXPECTED_ORIGINAL_NL0B_BATH_NOT_PRESENT")
    if raw.count("if (pba->aest_enabled == _TRUE_)")<3:
        raise RuntimeError("EXPECTED_AEST_BRANCHES_MISSING")
    staged=raw
    count={}
    for label,old,new in REPLACEMENTS:
        n=staged.count(old)
        if n!=1:
            raise RuntimeError(f"EXACT_ANCHOR_{label}_COUNT_{n}")
        staged=staged.replace(old,new,1)
        count[label]=n
    # This source still uses ordinary CLASS radiation hierarchy. It does
    # NOT solve the missing physical k^2 X/E adiabatic eigenvector.
    assert OLD_FORCE not in staged and NEW_FORCE in staged
    return raw,staged,head,count

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo-root",type=Path,default=Path(__file__).resolve().parents[2])
    ap.add_argument("--source-root",type=Path,required=True)
    ap.add_argument("--candidate-root",type=Path,required=True)
    ap.add_argument("--report",type=Path,required=True)
    ap.add_argument("--apply",action="store_true",
                    help="copy source and patch a NEW isolated directory; otherwise preflight only")
    args=ap.parse_args()
    repo=args.repo_root.resolve()
    root=args.source_root.expanduser().resolve()
    candidate=args.candidate_root.expanduser().resolve()
    report=args.report.expanduser().resolve()
    if root == candidate or root in candidate.parents or candidate in root.parents:
        raise RuntimeError("CANDIDATE_NOT_DISJOINT_FROM_HISTORICAL_ROOT")
    if candidate.exists():
        raise RuntimeError("CANDIDATE_EXISTS_REFUSE_OVERWRITE "+str(candidate))
    if report.exists():
        raise RuntimeError("REPORT_EXISTS_REFUSE_OVERWRITE "+str(report))
    original,patched,head,anchors=check_source(repo,root)
    status={
        "classification":"GE19_ISOLATED_QUARTER_ENTHALPY_CLASS_SOURCE_STAGE_ONLY_NOT_PHYSICS_GO",
        "original_CLASS_git_HEAD":head,
        "original_C_sha256":hashlib.sha256(original.encode()).hexdigest(),
        "candidate_C_sha256":hashlib.sha256(patched.encode()).hexdigest(),
        "source_root":str(root),
        "candidate_root":str(candidate),
        "exact_replacement_anchor_counts":anchors,
        "original_C_preserved":True,
        "quarter_normalization_corrected_in_candidate_only":bool(args.apply),
        "adiabatic_sync_density_and_newtonian_transform_corrected_in_candidate_only":bool(args.apply),
        "full_primordial_k2_X_E_mode_selected":False,
        "retarded_qp_history_transported":False,
        "full_covariant_Ward_boltzmann_verified":False,
        "class_compiled":False,
        "class_executed":False,
        "DES_detection":False,
        "FULL_PHYSICS_GO":False,
        "scope_notice":"Necessary leading source and entropy repairs only; CLASS synch-to-Newtonian metric seed and full k^2 growing mode still require independent action-consistent certification."
    }
    if args.apply:
        # Reproducible independent candidate; never edit, delete or reset
        # the historical CLASS working tree. Build artifacts are omitted.
        ignore=shutil.ignore_patterns(
            ".git",".venv","__pycache__","build","output",
            "*.o","*.opp","*.a","*.so","*.pyc")
        shutil.copytree(root,candidate,ignore=ignore,symlinks=True)
        target=candidate/"source/perturbations.c"
        if target.is_symlink():
            raise RuntimeError("REFUSE_SYMLINKED_CANDIDATE_C_SOURCE")
        if target.read_text()!=original:
            raise RuntimeError("CANDIDATE_COPY_PROVENANCE_MISMATCH")
        target.write_text(patched)
        if file_sha(target)!=status["candidate_C_sha256"]:
            raise RuntimeError("CANDIDATE_VERIFY_FAILED")
        print("GE19_ISOLATED_CLASS_SOURCE_STAGE_PASS",len(anchors),flush=True)
        print("GE19_CLASS_CANDIDATE "+str(candidate),flush=True)
    else:
        print("GE19_ISOLATED_CLASS_SOURCE_PREFLIGHT_PASS",len(anchors),flush=True)
    report.parent.mkdir(parents=True,exist_ok=True)
    report.write_text(json.dumps(status,indent=2,sort_keys=True)+"\n")
    print("GE19_CLASS_STAGE_REPORT "+str(report),flush=True)
    print("GE19_FULL_PHYSICS_GO False",flush=True)
    print("GE19_DES_DETECTION False",flush=True)

if __name__=="__main__":
    main()
