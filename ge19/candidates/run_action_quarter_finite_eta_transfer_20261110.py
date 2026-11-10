#!/usr/bin/env python3
"""One fixed positive-eta native CLASS diagnostic of candidate vs historical patch.

Three *fixed* runs: quarter eta=0, quarter eta=0.01, historical eta=0.01.
One Exp background and z_pk=0.5, output=mPk,mTk. No parameter sweep.
Extract d_m, phi, psi from explicit CLASS transfer column metadata.
This is implemented-transfer diagnostics, NOT full action equivalence,
Einstein-constraint propagation, a physical P_delta,W forecast or DES fit.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
OLD=b"E_rhs_aest -= 0.5*Q_aest*Bchi_aest;"
NEW=b"E_rhs_aest -= 0.25*Q_aest*Bchi_aest;"
ETA=0.01
Z=0.5
HEAD="e85808324f51fc694d12e3ed7439552a3c3f9540"
MANIFEST_BLOB="b8767523dc62256f7d1dbe9dbd69dd12d724411d"
ETA0_JSON_BLOB="bbb15393e581585e8bc452ed710e476202ccfede"

def need(condition,label):
    if not bool(condition):
        raise RuntimeError("GE19_ACTION_QUARTER_FINITE_ETA_"+label)

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def git(cwd,*cmd):
    return subprocess.check_output(["git",*cmd],cwd=cwd,text=True).strip()

def preflight(old,new,baseline):
    need(old.is_dir() and new.is_dir() and old!=new and old.parent==new.parent,
         "CLASS_PATHS")
    for root in (old,new):
        need(git(root,"rev-parse","HEAD")==HEAD,"CLASS_HEAD_CHANGED")
        need((root/"class").is_file(),"CLASS_BINARY_MISSING_"+root.name)
    mf=ROOT/"ge19/candidates/evidence/GE19_ACTION_QUARTER_CANDIDATE_MANIFEST.json"
    need(mf.is_file() and git(ROOT,"hash-object",str(mf))==MANIFEST_BLOB,
         "ORIGINAL_MANIFEST_CHANGED")
    m=json.loads(mf.read_text())
    a=(old/"source/perturbations.c").read_bytes()
    b=(new/"source/perturbations.c").read_bytes()
    need(sha(old/"source/perturbations.c")==m["input_source_sha256"],
         "HISTORIC_C_CHANGED")
    need(sha(new/"source/perturbations.c")==m["candidate_source_sha256"],
         "CANDIDATE_C_CHANGED")
    need(a.count(OLD)==1 and b==a.replace(OLD,NEW,1),"ONLY_ONE_C_DELTA")
    need((new/"class").stat().st_mtime >=
         (new/"source/perturbations.c").stat().st_mtime,
         "CANDIDATE_BINARY_PRECEDES_CHANGED_C")
    need(baseline.is_file() and git(ROOT,"hash-object",str(baseline))==
         ETA0_JSON_BLOB,"ETA0_ARCHIVED_EVIDENCE_CHANGED")
    eta0=json.loads(baseline.read_text())
    need(eta0["classification"]==
         "GE19_ACTION_QUARTER_ETA0_EQUIVALENCE_PASS_ONLY_NOT_PHYSICS_GO"
         and eta0["zero_eta_output_equivalence"]
         and eta0["candidate_clean_rebuild_pass"]
         and eta0["candidate_class_source_sha256"]==m["candidate_source_sha256"],
         "ETA0_PRIOR_NOT_VALID")
    return m

def write_input(base,filename,prefix,eta):
    # No duplicate CLASS keys; old historical defaults exactly retained.
    override={
        "root":str(prefix),
        "overwrite_root":"no",
        "output":"mPk,mTk",
        "lensing":"no",
        "z_pk":format(Z,".17g"),
        "P_k_max_h/Mpc":"0.3",
        "k_per_decade_for_pk":"24",
        "k_per_decade_for_bao":"80",
        "write_background":"no",
        "write_parameters":"no",
        "aest_memory_enabled":"yes",
        "aest_eta":format(eta,".17g"),
        "aest_tau_H0":"1",
        "aest_memory_order":"16",
        "input_verbose":"0",
        "background_verbose":"0",
        "perturbations_verbose":"0"
    }
    lines=[]
    for line in base.splitlines():
        key=line.split("=",1)[0].strip()
        if key not in override:
            lines.append(line)
    lines.extend(f"{key} = {value}" for key,value in override.items())
    filename.write_text("\n".join(lines)+"\n")

def execute(exe,ini,log,cwd):
    env=os.environ.copy()
    env.update(OMP_NUM_THREADS="1",OPENBLAS_NUM_THREADS="1",MKL_NUM_THREADS="1")
    for key in ("AEST_TANGENT_FORCE_FILE","AEST_TANGENT_LAMBDA","AEST_OFFLINE_TRACE_FILE"):
        env.pop(key,None)
    with log.open("w") as f:
        result=subprocess.run([str(exe),str(ini)],cwd=cwd,
                              env=env,stdout=f,stderr=subprocess.STDOUT)
    need(result.returncode==0,"CLASS_EXIT_"+log.stem+"_"+str(result.returncode))
    print("GE19_ACTION_QUARTER_RUN_PASS",log.stem,flush=True)

def transfer_columns(file):
    # Read column numbers from the CLASS header, e.g. '# 1:k (h/Mpc) 2:d_m 3:phi 4:psi'.
    hdr=[]
    with file.open() as f:
        for line in f:
            if line.lstrip().startswith("#"):
                hdr.append(line.lstrip("# ").rstrip())
            elif line.strip():
                break
    tokens=re.findall(r"(?:^|\s)(\d+):([A-Za-z_][A-Za-z_0-9]*)",
                      " ".join(hdr))
    columns={key:int(number)-1 for number,key in tokens}
    for k in ("d_m","phi","psi"):
        need(k in columns,"NO_EXPLICIT_TRANSFER_COLUMN_"+k+"_"+file.name)
    data=np.atleast_2d(np.loadtxt(file,comments="#"))
    need(np.isfinite(data).all() and data.shape[0]>=4,"BAD_TRANSFER_"+file.name)
    need(max(columns.values())<data.shape[1],"TRANSFER_COLUMNS_OUT_OF_RANGE")
    # k is the first column of CLASS transfer tables, in h/Mpc.
    k=data[:,0]
    need(np.all(np.diff(k)>0) and np.all(k>0),"K_GRID_NOT_ORDERED")
    return k,{name:data[:,col].copy() for name,col in columns.items()
              if name in ("d_m","phi","psi")}

def unique_transfer(root):
    files=sorted(root.parent.glob(root.name+"*tk.dat"))
    need(len(files)==1,"TRANSFER_FILE_COUNT_"+str(len(files)))
    return files[0]

def unique_power(root):
    files=sorted(root.parent.glob(root.name+"*pk.dat"))
    need(len(files)==1,"PK_FILE_COUNT_"+str(len(files)))
    arr=np.atleast_2d(np.loadtxt(files[0],comments="#"))
    need(arr.shape[1]>=2 and np.isfinite(arr).all(),"PK_NONFINITE")
    return files[0],arr

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--historic-class",type=Path,required=True)
    ap.add_argument("--candidate-class",type=Path,required=True)
    ap.add_argument("--eta0-evidence",type=Path,default=ROOT/
      "ge19/candidates/evidence/ge19_action_quarter_eta0_r1_regression_result.json")
    ap.add_argument("--out-dir",type=Path,required=True)
    ap.add_argument("--preflight",action="store_true")
    args=ap.parse_args()
    orig=args.historic_class.expanduser().resolve()
    candidate=args.candidate_class.expanduser().resolve()
    proof=preflight(orig,candidate,args.eta0_evidence.resolve())
    print("GE19_ACTION_QUARTER_FINITE_ETA_SOURCE_PREFLIGHT_PASS",flush=True)
    if args.preflight:
        print("GE19_ACTION_QUARTER_PREFLIGHT_ONLY_NO_CLASS_RUN",flush=True)
        return
    out=args.out_dir.expanduser().resolve()
    need(not out.exists(),"OUTPUT_EXISTS")
    text=(ROOT/"v019/ini/aest_exp.ini").read_text()
    out.mkdir(parents=True)
    cases=[
        ("candidate_eta0",candidate,0.0),
        ("candidate_eta001",candidate,ETA),
        ("historical_eta001",orig,ETA)
    ]
    arrays={}
    power={}
    for name,root,eta in cases:
        prefix=out/(name+"_")
        ini=out/(name+".ini")
        write_input(text,ini,prefix,eta)
        execute(root/"class",ini,out/(name+".log"),root)
        tf=unique_transfer(prefix)
        k,values=transfer_columns(tf)
        arrays[name]={"k":k,**values,
                      "W":(values["phi"]+values["psi"])/2.0,
                      "D_W":values["d_m"]*(values["phi"]+values["psi"])/2.0}
        pf,pdata=unique_power(prefix)
        power[name]=pdata
    ref=arrays["candidate_eta0"]
    for label,arr in arrays.items():
        need(np.array_equal(arr["k"],ref["k"]),"TRANSFER_K_GRID_"+label)
    basepow=power["candidate_eta0"]
    for label,arr in power.items():
        need(arr.shape==basepow.shape and np.array_equal(arr[:,0],basepow[:,0]),
             "PK_K_GRID_"+label)
    quarter=arrays["candidate_eta001"]
    half=arrays["historical_eta001"]
    metrics={}
    for field in ("d_m","phi","psi","W","D_W"):
        b=ref[field]
        q=quarter[field]
        h=half[field]
        scale=max(float(np.max(np.abs(b))),1e-30)
        metrics[field]={
          "max_abs_quarter_minus_eta0":float(np.max(np.abs(q-b))),
          "max_abs_half_minus_eta0":float(np.max(np.abs(h-b))),
          "max_abs_half_minus_quarter":float(np.max(np.abs(h-q))),
          "quarter_minus_eta0_scaled_by_baseline":float(np.max(np.abs(q-b))/scale),
          "half_minus_quarter_scaled_by_baseline":float(np.max(np.abs(h-q))/scale)
        }
    pk_scale=max(float(np.max(np.abs(basepow[:,1]))),1e-30)
    metrics["P_k"]={
       "max_abs_half_minus_quarter":float(np.max(np.abs(power["historical_eta001"][:,1]-power["candidate_eta001"][:,1]))),
       "half_minus_quarter_scaled_by_baseline":float(np.max(np.abs(power["historical_eta001"][:,1]-power["candidate_eta001"][:,1]))/pk_scale)
    }
    np.savez_compressed(out/"native_transfer_comparison.npz",k_hmpc=ref["k"],
       **{f"{name}_{field}":val for name,arr in arrays.items()
          for field,val in arr.items() if field!="k"})
    report={
       "classification":"GE19_ACTION_QUARTER_FIXED_FINITE_ETA_IMPLEMENTED_TRANSFER_DIAGNOSTIC_NOT_PHYSICS_GO",
       "eta_fixed":ETA,
       "z_pk_fixed":Z,
       "background_input_model":"frozen v019 AeST Exp",
       "cases":[name for name,_,_ in cases],
       "source_candidate_sha256":proof["candidate_source_sha256"],
       "source_historical_sha256":proof["input_source_sha256"],
       "native_transfer_fields":["d_m","phi","psi","W","D_W"],
       "D_W_definition":"product of signed CLASS d_m and W transfer amplitudes, NOT a projected survey cross-power",
       "units":"CLASS native transfer fields, k in h/Mpc, one redshift",
       "metrics":metrics,
       "finite_eta_runs_completed":True,
       "all_source_constraints_physically_certified":False,
       "Einstein_constraint_propagation_verified":False,
       "full_retarded_physical_eta_matter_Weyl_cross_power_certified":False,
       "observed_DES_gamma_t_or_significance":False,
       "explicit_note":"This evaluates implemented full CLASS dynamics at one fixed eta, not a perturbative derivative, theory equivalence or memory detection."
    }
    (out/"fixed_eta_transfer_diagnostic.json").write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
    print("GE19_ACTION_QUARTER_FINITE_ETA_TRANSFER_DIAGNOSTIC_PASS",len(ref["k"]),flush=True)
    print("GE19_ACTION_QUARTER_EINSTEIN_CONSTRAINT_PROPAGATION_OPEN",flush=True)
    print("GE19_ACTION_QUARTER_PHYSICAL_OBSERVER_READY False",flush=True)
    print("GE19_ACTION_QUARTER_RESULT",out/"fixed_eta_transfer_diagnostic.json",flush=True)

if __name__=="__main__":
    main()
