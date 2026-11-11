#!/usr/bin/env python3
"""GE19 read-only observer rescue: use EXISTING CLASS mTk tables, never run CLASS.

Reads three already-generated single-z transfer tables:
candidate_eta0, candidate_eta001, historical_eta001.
Compares the native *Newtonian-gauge* baryon density transfer d_b to Weyl
and to the previously reported potentially misinterpreted d_m. Produces
only an explicitly non-observational JSON. No arbitrary tuning, no
cosmological evolution, no DES data, no source rewriting.
"""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path
import numpy as np

CASES = ("candidate_eta0", "candidate_eta001", "historical_eta001")
FIELDS = ("d_b", "d_m", "phi", "psi")
WINDOW = (0.03, 0.20)

def require(ok, label):
    if not bool(ok):
        raise RuntimeError("GE19_EXISTING_BARYON_WEYL_"+label)

def locate(directory, prefix):
    paths = sorted(directory.glob(prefix + "_*tk.dat"))
    require(len(paths) == 1, "MISSING_OR_AMBIGUOUS_MTK_"+prefix+
            "_COUNT_"+str(len(paths)))
    return paths[0]

def load_table(path):
    comments=[]
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.startswith("#"):
                comments.append(line[1:].strip())
            elif line.strip():
                break
    # CLASS class_format headers use "1:k (h/Mpc) 2:d_g ...".
    # Refuse CAMB style and ambiguous fields rather than guess units.
    require(any("Transfer functions T_i(k)" in h for h in comments),
            "NOT_NATIVE_CLASS_FORMAT_"+path.name)
    columns={}
    for num,key in re.findall(r"(?:^|\s)(\d+):([A-Za-z_][A-Za-z_0-9]*)",
                              " ".join(comments)):
        require(key not in columns,"DUPLICATE_COLUMN_"+key)
        columns[key]=int(num)-1
    for key in FIELDS:
        require(key in columns,"COLUMN_MISSING_"+key+"_"+path.name)
    data=np.atleast_2d(np.loadtxt(path,comments="#",dtype=float))
    require(data.ndim==2 and data.shape[0]>=8 and
            np.isfinite(data).all(),"BAD_TRANSFER_"+path.name)
    require(data.shape[1]>max(columns.values()),"COLUMN_COUNT_"+path.name)
    k=data[:,0]
    require(np.isfinite(k).all() and np.all(k>0) and
            np.all(np.diff(k)>0),"INVALID_K_AXIS_"+path.name)
    return {"k":k,**{key:data[:,col] for key,col in columns.items()
                     if key in FIELDS}}

def metrics(reference, old, candidate, field, mask):
    b=reference[field][mask]
    h=old[field][mask]
    q=candidate[field][mask]
    d=h-q
    scale=max(float(np.max(np.abs(reference[field]))),1e-30)
    sign=np.sign(d)
    nonzero=sign[sign!=0]
    flips=int(np.count_nonzero(nonzero[1:]!=nonzero[:-1])) if len(nonzero)>1 else 0
    response_h=h-b
    response_q=q-b
    return {
        "max_abs_historic_minus_quarter":float(np.max(np.abs(d))),
        "max_abs_difference_over_full_k_eta0_max":float(np.max(np.abs(d))/scale),
        "sign_changes_between_nonzero_adjacent_k":flips,
        "positive_difference_points":int(np.count_nonzero(d>0)),
        "negative_difference_points":int(np.count_nonzero(d<0)),
        "response_norm_historical":float(np.linalg.norm(response_h)),
        "response_norm_candidate":float(np.linalg.norm(response_q)),
        "difference_norm":float(np.linalg.norm(d)),
        "factor_two_test_norm_ratio": (
            float(np.linalg.norm(response_h-2*response_q)
                  /np.linalg.norm(response_h))
            if float(np.linalg.norm(response_h))>0 else None
        ),
        "warning":"Not a convergence claim or a projected P_bW signal"
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--existing-dir",required=True,type=Path)
    ap.add_argument("--out",required=True,type=Path)
    ap.add_argument("--prior-npz",type=Path)
    args=ap.parse_args()
    directory=args.existing_dir.expanduser().resolve()
    require(directory.is_dir(),"OUTPUT_DIR_MISSING")
    loaded={}
    names={}
    for name in CASES:
        path=locate(directory,name)
        loaded[name]=load_table(path)
        names[name]=path.name
    k=loaded[CASES[0]]["k"]
    for name in CASES[1:]:
        require(np.array_equal(k,loaded[name]["k"]),"K_GRID_CHANGED_"+name)
    require(8<=len(k)<=200000,"SUSPICIOUS_GRID_SIZE")
    if args.prior_npz is not None:
        with np.load(args.prior_npz.expanduser().resolve(),
                     allow_pickle=False) as cached:
            require(np.array_equal(k,cached["k_hmpc"]),"PREVIOUS_NPZ_K_MISMATCH")
            for name in CASES:
                for field in ("phi","psi","d_m"):
                    previous_name="density" if field=="d_m" else field
                    key=name+"_"+previous_name
                    require(key in cached,"PREVIOUS_NPZ_FIELD_MISSING_"+key)
                    require(np.array_equal(loaded[name][field],cached[key]),
                            "PREVIOUS_NPZ_VALUE_DIFFERENCE_"+key)
        print("GE19_EXISTING_BARYON_WEYL_PRIOR_NPZ_IDENTITY_PASS",flush=True)

    for name in CASES:
        loaded[name]["W"]=(loaded[name]["phi"]+loaded[name]["psi"])/2.
    mask=(k>=WINDOW[0])&(k<=WINDOW[1])
    require(mask.sum()>=8,"WINDOW_TOO_FEW_NODES")
    baseline=loaded["candidate_eta0"]
    half=loaded["historical_eta001"]
    quarter=loaded["candidate_eta001"]
    fields=("d_b","d_m","W")
    result={field:metrics(baseline,half,quarter,field,mask) for field in fields}
    deltab=half["d_b"][mask]-quarter["d_b"][mask]
    deltaW=half["W"][mask]-quarter["W"][mask]
    delta_m=half["d_m"][mask]-quarter["d_m"][mask]
    def corr(x,y):
        if np.std(x)<=0 or np.std(y)<=0: return None
        return float(np.corrcoef(x,y)[0,1])
    report={
        "classification":"EXISTING_NEWTONIAN_BARYON_WEYL_TRANSFER_DIAGNOSTIC_ONLY_NOT_PHYSICS_GO",
        "reused_existing_CLASS_run":True,
        "new_CLASS_run":False,
        "tuning_performed":False,
        "time":"previously fixed z_pk=0.5; no new redshifts",
        "fixed_eta":"historical and quarter eta=0.01; quarter eta=0",
        "table_names":names,
        "n_all_k":int(k.size),
        "n_window_k":int(np.count_nonzero(mask)),
        "k_window_hmpc":list(WINDOW),
        "k_window_first_last_hmpc":[float(k[mask][0]),float(k[mask][-1])],
        "field_names":{
            "d_b":"CLASS native d_b baryon density transfer in Newtonian gauge",
            "d_m":"CLASS default (possibly pressureless-assumption) exported total matter transfer; NOT independent physical survey matter",
            "W":"(CLASS phi + CLASS psi)/2"
        },
        "metrics":result,
        "correlation_delta_b_delta_W_in_fixed_window":corr(deltab,deltaW),
        "correlation_delta_m_delta_W_in_fixed_window":corr(delta_m,deltaW),
        "baryon_is_not_an_observed_galaxy_tracer":True,
        "physical_galaxy_bias_and_projected_GGL_not_calculated":True,
        "physical_constraint_propagation_certified":False,
        "retarded_auxiliary_branch_uniqueness_proven":False,
        "DES_observed_detection":False,
    }
    dest=args.out.expanduser().resolve()
    require(not dest.exists(),"REFUSE_OUTPUT_OVERWRITE")
    require(dest.parent.is_dir(),"OUTPUT_PARENT_MISSING")
    dest.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
    print("GE19_EXISTING_BARYON_WEYL_READ_ONLY_PASS",int(mask.sum()),flush=True)
    print("GE19_OBSERVATION_READY False",flush=True)
    print("GE19_RESULT",dest,flush=True)

if __name__=="__main__": main()
