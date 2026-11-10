#!/usr/bin/env python3
"""One bounded eta=0 regression for the separate action-quarter CLASS candidate.

Never patches or builds the historical CLASS checkout. Rebuilds ONLY the
copied candidate. Compares baseline and candidate mPk/background tables
at eta=0 using the same pinned parameter file. Constraint propagation
and finite-eta physical Weyl response are NOT certified by this test.
"""
from __future__ import annotations
import argparse, hashlib, json, os, subprocess, sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
PIN = "e85808324f51fc694d12e3ed7439552a3c3f9540"
OLD = "E_rhs_aest -= 0.5*Q_aest*Bchi_aest;"
NEW = "E_rhs_aest -= 0.25*Q_aest*Bchi_aest;"
DIFF_BLOB = "6049e86ccb1088b52600127f7f2b7d0824baf810"
MANIFEST_BLOB = "b8767523dc62256f7d1dbe9dbd69dd12d724411d"
HIST_PATCH_BLOB = "14796a5ed9e6265ed6810c792a93d7328a109364"
TOL = 1e-10

def require(ok, why):
    if not bool(ok):
        raise RuntimeError("GE19_ACTION_QUARTER_REGRESSION_"+why)

def sha256(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def git(*args, cwd=None):
    return subprocess.check_output(
        ["git", *args], cwd=cwd, text=True, stderr=subprocess.PIPE).strip()

def preflight(historic, candidate):
    historic, candidate = historic.resolve(), candidate.resolve()
    require(historic.is_dir() and candidate.is_dir(),"CLASS_PATHS_MISSING")
    require(historic != candidate and historic.parent==candidate.parent,
            "NOT_DISTINCT_SIBLING_DIRS")
    for d in (historic,candidate):
        require((d/".git").exists(),"MISSING_OFFICIAL_GIT_"+d.name)
        require(git("rev-parse","HEAD",cwd=d)==PIN,"CLASS_PIN_CHANGED_"+d.name)
    manifest=ROOT/"ge19/candidates/evidence/GE19_ACTION_QUARTER_CANDIDATE_MANIFEST.json"
    diff=ROOT/"ge19/candidates/evidence/GE19_ACTION_QUARTER_CANDIDATE.diff"
    require(git("hash-object",str(manifest))==MANIFEST_BLOB,
            "UPLOADED_MANIFEST_CHANGED")
    require(git("hash-object",str(diff))==DIFF_BLOB,"UPLOADED_DIFF_CHANGED")
    m=json.loads(manifest.read_text())
    own=json.loads((candidate/"GE19_ACTION_QUARTER_CANDIDATE_MANIFEST.json").read_text())
    require(m==own,"CANDIDATE_MANIFEST_DIFFERENT")
    require(sha256(diff)==sha256(candidate/"GE19_ACTION_QUARTER_CANDIDATE.diff"),
            "CANDIDATE_DIFF_DIFFERENT")
    require(git("hash-object",str(ROOT/"v019j/apply_memory_patch.py"))==HIST_PATCH_BLOB,
            "HISTORICAL_PATCH_CHANGED")
    original=(historic/"source/perturbations.c").read_bytes()
    changed=(candidate/"source/perturbations.c").read_bytes()
    require(sha256(historic/"source/perturbations.c")==m["input_source_sha256"],
            "HISTORICAL_CLASS_SOURCE_CHANGED")
    require(sha256(candidate/"source/perturbations.c")==m["candidate_source_sha256"],
            "CANDIDATE_CLASS_SOURCE_CHANGED")
    require(original.count(OLD.encode())==1 and NEW.encode() not in original,
            "HISTORICAL_SOURCE_ANCHOR")
    require(changed == original.replace(OLD.encode(),NEW.encode(),1),
            "NOT_EXACT_ONE_C_SOURCE_DELTA")
    require("Bchi_aest *= pba->aest_eta;" in changed.decode(),
            "SOURCE_ETA_MULTIPLICATION_MISSING")
    require(m["classification"]==
         "EXPLORATORY_LINEAR_SCALAR_QUARTER_SOURCE_ONLY_NOT_PHYSICS_GO",
         "MANIFEST_PHYSICS_STATUS_CHANGED")
    # Source-level zero-eta equivalence is exact because only changed term
    # is proportional to the eta-multiplied Bchi.
    print("GE19_ACTION_QUARTER_EXACT_SOURCE_DELTA_PASS",flush=True)
    print("GE19_ACTION_QUARTER_ETA0_ALGEBRAIC_SOURCE_EQUIVALENCE_PASS",flush=True)
    return m

def prepare_ini(label,base,out):
    lines=[]
    keys={"root","overwrite_root","output","lensing","write_background","write_parameters",
          "input_verbose","background_verbose","perturbations_verbose",
          "k_per_decade_for_pk","k_per_decade_for_bao","P_k_max_h/Mpc",
          "aest_memory_enabled","aest_eta","aest_memory_order","aest_tau_H0"}
    for line in base.splitlines():
        left=line.split("=",1)[0].strip()
        if left in keys:continue
        lines.append(line)
    lines.extend([
        "root = "+str(out/(label+"_")),
        "overwrite_root = no",
        "output = mPk",
        "lensing = no",
        "write_background = yes",
        "write_parameters = no",
        "input_verbose = 0",
        "background_verbose = 0",
        "perturbations_verbose = 0",
        "k_per_decade_for_pk = 20",
        "k_per_decade_for_bao = 80",
        "P_k_max_h/Mpc = 0.25",
        "aest_memory_enabled = yes",
        "aest_eta = 0",
        "aest_memory_order = 16",
        "aest_tau_H0 = 1",
    ])
    ini=out/(label+".ini")
    ini.write_text("\n".join(lines)+"\n")
    return ini

def run_logged(cmd,cwd,log,env,timeout):
    print("GE19_ACTION_QUARTER_COMMAND", " ".join(map(str,cmd)),flush=True)
    with log.open("w") as f:
        result=subprocess.run(cmd,cwd=cwd,env=env,stdout=f,
                              stderr=subprocess.STDOUT,timeout=timeout)
    require(result.returncode==0,
            "EXECUTION_FAILED_"+log.name+"_EXIT_"+str(result.returncode))

def compare_tables(out):
    base_files={p.name[len("historical_"):]:p for p in out.glob("historical_*.dat")}
    trial_files={p.name[len("candidate_"):]:p for p in out.glob("candidate_*.dat")}
    require(bool(base_files) and base_files.keys()==trial_files.keys(),
            "ETA0_OUTPUT_FILE_MISMATCH")
    require(any("background.dat" in s for s in base_files),
            "BACKGROUND_OUTPUT_MISSING")
    require(any("pk.dat" in s for s in base_files),"PK_OUTPUT_MISSING")
    metrics={}
    for suffix,path in sorted(base_files.items()):
        alt=trial_files[suffix]
        x=np.atleast_2d(np.loadtxt(path,comments="#",dtype=float))
        y=np.atleast_2d(np.loadtxt(alt,comments="#",dtype=float))
        require(x.shape==y.shape and x.size>0,"TABLE_SHAPE_"+suffix)
        require(np.isfinite(x).all() and np.isfinite(y).all(),"NONFINITE_"+suffix)
        colscale=np.maximum(np.max(np.maximum(np.abs(x),np.abs(y)),axis=0),1e-30)
        colerr=np.max(np.abs(x-y),axis=0)/colscale
        worst=float(np.max(colerr))
        metrics[suffix]=dict(n_rows=int(x.shape[0]),n_cols=int(x.shape[1]),
                             max_column_normalized_difference=worst,
                             identical_raw_bytes=sha256(path)==sha256(alt))
        require(worst<=TOL,"ETA0_TABLE_MISMATCH_"+suffix)
    return metrics

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--historic-class",type=Path,required=True)
    p.add_argument("--candidate-class",type=Path,required=True)
    p.add_argument("--out-dir",type=Path,default=ROOT/"results/ge19_action_quarter_eta0_r1")
    p.add_argument("--preflight",action="store_true")
    args=p.parse_args()
    orig=args.historic_class.expanduser().resolve()
    cand=args.candidate_class.expanduser().resolve()
    manifest=preflight(orig,cand)
    if args.preflight:
        print("GE19_ACTION_QUARTER_PREFLIGHT_ONLY_NO_BUILD",flush=True)
        return
    out=args.out_dir.expanduser().resolve()
    require(not out.exists(),"OUTPUT_DIRECTORY_ALREADY_EXISTS")
    # Fail before rebuilding if historical executable is absent or stale.
    exe=orig/"class"
    require(exe.is_file() and os.access(exe,os.X_OK),"HISTORICAL_BINARY_MISSING")
    require(exe.stat().st_mtime >= (orig/"source/perturbations.c").stat().st_mtime,
            "HISTORICAL_BINARY_OLDER_THAN_SOURCE")
    base=ROOT/"v019/ini/aest_exp.ini"
    require(base.is_file(),"FROZEN_EXP_INI_MISSING")
    out.mkdir(parents=True)
    env=os.environ.copy()
    env.update(OMP_NUM_THREADS="1",OPENBLAS_NUM_THREADS="1",MKL_NUM_THREADS="1")
    for e in ("AEST_TANGENT_FORCE_FILE","AEST_TANGENT_LAMBDA","AEST_OFFLINE_TRACE_FILE"):
        env.pop(e,None)
    # Rebuild only copied candidate. Historical binary and source untouched.
    run_logged(["make","clean"],cand,out/"candidate_clean.log",env,120)
    run_logged(["make","-j2","PYTHON="+sys.executable,"class"],
               cand,out/"candidate_build.log",env,300)
    target=cand/"class"
    require(target.is_file() and os.access(target,os.X_OK),
            "CANDIDATE_BINARY_MISSING")
    text=base.read_text()
    ini_old=prepare_ini("historical",text,out)
    ini_new=prepare_ini("candidate",text,out)
    run_logged([str(exe),str(ini_old)],orig,out/"historical_run.log",env,180)
    run_logged([str(target),str(ini_new)],cand,out/"candidate_run.log",env,180)
    measures=compare_tables(out)
    report={
      "classification":"GE19_ACTION_QUARTER_ETA0_EQUIVALENCE_PASS_ONLY_NOT_PHYSICS_GO",
      "exact_c_source_delta":OLD+" -> "+NEW,
      "historical_class_source_sha256":manifest["input_source_sha256"],
      "candidate_class_source_sha256":manifest["candidate_source_sha256"],
      "original_historical_checkout_modified":False,
      "original_historical_binary_rebuilt":False,
      "candidate_clean_rebuild_pass":True,
      "zero_eta_source_equivalence":True,
      "zero_eta_output_equivalence":True,
      "output_max_relative_column_error_limit":TOL,
      "tables":measures,
      "auxiliary_initial_conditions_dynamic_trace_verified":False,
      "Einstein_constraint_propagation_verified":False,
      "finite_eta_physical_source_transfer_verified":False,
      "actual_physical_Weyl_response_certified":False,
      "DES_Y3_memory_detection":False,
    }
    (out/"regression_result.json").write_text(
        json.dumps(report,sort_keys=True,indent=2)+"\n")
    print("GE19_ACTION_QUARTER_BUILD_PASS",flush=True)
    print("GE19_ACTION_QUARTER_ETA0_MATCH_PASS",len(measures),flush=True)
    print("GE19_ACTION_QUARTER_CONSTRAINT_PROPAGATION_OPEN",flush=True)
    print("GE19_ACTION_QUARTER_PHYSICAL_OBSERVER_READY False",flush=True)
    print("GE19_ACTION_QUARTER_RESULT",out/"regression_result.json",flush=True)

if __name__=="__main__":
    main()
