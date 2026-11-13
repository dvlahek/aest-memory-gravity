#!/usr/bin/env python3
"""One bounded local full-CLASS two-pass eta=0 direct-tangent CAMPAIGN.
Requires the experimental 20261112 source patch preinstalled and compiled.
All photon/baryon/neutrino variables stay in CLASS. Source interpolation,
vector-switch handling, primordial IC and full Ward equivalence require audits.
Only --run executes CLASS; without --run, validates and prints campaign plan.
"""
from __future__ import annotations
import argparse
import bisect
import csv
import hashlib
import json
import math
import os
import re
import subprocess
from pathlib import Path

PATCH_MARKER = "/* GE19 FULL CLASS DIRECT TANGENT EXPERIMENT v1 */"
K_MPC=0.06732117
TARGET_A=2.0/3.0

def read_trace(path: Path):
    if not path.is_file():
        raise RuntimeError("GE19_MISSING_TRACE "+str(path))
    rows=[]
    with path.open(newline="") as f:
        for rec in csv.DictReader(f):
            tau=float(rec["tau"])
            a=float(rec["a"])
            k=float(rec["k_mpc"])
            W=float(rec["W"])
            B=float(rec["Bchi"])
            if not all(map(math.isfinite,(tau,a,k,W,B))):
                raise RuntimeError("GE19_NONFINITE_TRACE "+str(path))
            if abs(k-K_MPC)>K_MPC*1e-11:
                raise RuntimeError("GE19_K_NOT_SELECTED "+str(path))
            if rows and tau<=rows[-1][0]:
                raise RuntimeError("GE19_TRACE_NONMONOTONE "+str(path))
            rows.append((tau,a,W,B))
    if len(rows)<100:
        raise RuntimeError("GE19_TOO_FEW_SOURCE_TIMES "+str(path))
    return rows

def interpolate_a(rows,a=TARGET_A):
    scale=[r[1] for r in rows]
    if not all(scale[i+1]>scale[i] for i in range(len(scale)-1)):
        raise RuntimeError("GE19_NONMONOTONE_SCALE")
    i=bisect.bisect_left(scale,a)
    if i==len(rows) or i==0:
        raise RuntimeError("GE19_TARGET_A_NOT_IN_SOURCE_RANGE")
    x0,x1=scale[i-1],scale[i]
    f=(a-x0)/(x1-x0)
    return rows[i-1][2]*(1-f)+rows[i][2]*f

def patched_source_qualification(root:Path):
    source=root/"source"/"perturbations.c"
    manifest=root/"ge19_tangent_patch_manifest.json"
    if not source.is_file() or not manifest.is_file():
        raise RuntimeError("GE19_PATCH_OR_MANIFEST_MISSING: run source-locked patcher first")
    c=source.read_text()
    m=json.loads(manifest.read_text())
    sha=hashlib.sha256(c.encode()).hexdigest()
    if c.count(PATCH_MARKER)!=1 or m.get("modified_source_sha256")!=sha:
        raise RuntimeError("GE19_SOURCE_CHANGED_AFTER_PATCH")
    if m.get("parent_source_sha256") not in (
        "2b4d7be96b6ebf4149bef129e357a32571f69cfffb3be0b1792d578e82ad6e17",
        "276646d913348824bddf9e24138e4213ecc3fb8b605d21525bf9280474dbca80",
        "75bf9fe85f2aae85031edc109e131c6b5d1745dca8497300237e16e57c99f883"):
        raise RuntimeError("GE19_BAD_PARENT")
    if (m.get("original_CLASS_HEAD") !=
        "e85808324f51fc694d12e3ed7439552a3c3f9540" or
        m.get("original_CLASS_git_blob") !=
        "c78fe4376d2eeebfbf4ff0cfca13b048d4513fa0"):
        raise RuntimeError("GE19_PINNED_PARENT_PROVENANCE_MISMATCH")
    if c.count("ge19_force_at(tau,k)")!=1:
        raise RuntimeError("GE19_E_FORCING_NOT_EXACTLY_ONCE")
    for snippet in ("ge19_record_callback:perturbations_sources",
                    "ge19_record_selected?ge19_tau:ppt->tau_sampling",
                    "ge19_record_selected?NULL:perhaps_print_variables",
                    "ge19_write_tangent_readout(tau,a,k"):
        if snippet not in c:
            raise RuntimeError("GE19_C_SOURCE_ANCHOR_MISSING "+snippet)
    return m

def make_ini(original:Path,out_dir:Path,label:str,tol:float) -> Path:
    s=original.read_text()
    fields={
        "gauge":"newtonian",
        "ic":"ad",
        "aest_enabled":"yes",
        "aest_memory_enabled":"yes",
        "aest_memory_order":"16",
        "aest_tau_H0":"1",
        "aest_eta":"0",
        "z_pk":"0.5",
        "output":"mTk",
        # The frozen v019 paper benchmark requests lensing=yes with tCl/pCl/lCl.
        # Our one-k diagnostic instead requests ONLY mTk, so lensing MUST be
        # disabled at input_init. This is a CLASS-output fix, not cosmology tuning.
        "lensing":"no",
        "k_output_values":"0.06732117",
        "P_k_max_1/Mpc":"0.08",
        "root":str((out_dir/"native"/(label+"_")).resolve()),
        "overwrite_root":"yes",
        "tol_perturbations_integration":format(tol,".12g"),
    }
    # Replace every existing key deterministically, never append a duplicate.
    for k,v in fields.items():
        matches=list(re.finditer(r"(?m)^\s*"+re.escape(k)+r"\s*=\s*[^\n]*",s))
        if len(matches)>1:
            raise RuntimeError("GE19_DUPLICATE_PARAMETER "+k)
        if matches:
            s=s[:matches[0].start()]+k+" = "+v+s[matches[0].end():]
        else:
            s+="\n"+k+" = "+v
    # Fail closed BEFORE spending time in CLASS if the output/lensing
    # combination regresses. Keep the original v019 input unchanged.
    generated = {}
    for name in ("output", "lensing", "gauge", "aest_eta"):
        m = re.findall(r"(?m)^\s*"+re.escape(name)+r"\s*=\s*([^#\n]+)",s)
        if len(m)!=1:
            raise RuntimeError("GE19_GENERATED_INI_KEY_NOT_UNIQUE "+name)
        generated[name]=m[0].strip()
    if (generated["output"]!="mTk" or generated["lensing"].lower()!="no"
        or generated["gauge"].lower()!="newtonian" or generated["aest_eta"]!="0"):
        raise RuntimeError("GE19_GENERATED_INI_INCONSISTENT_OUTPUT_OR_BACKGROUND")
    path=out_dir/(label+".ini")
    path.write_text(s+"\n" if not s.endswith("\n") else s)
    return path

def run_class(root:Path, ini:Path,log:Path, env:dict):
    program=root/"class"
    if not program.is_file():
        raise RuntimeError("GE19_CLASS_NOT_COMPILED; run make -j2 in isolated CLASS checkout")
    if program.stat().st_mtime<(root/"source"/"perturbations.c").stat().st_mtime:
        raise RuntimeError("GE19_CLASS_BINARY_STALE_RECOMPILE_WITH_MAKE")
    with log.open("w") as f:
        result=subprocess.run([str(program),str(ini)],cwd=root,env=env,
                              stdout=f,stderr=subprocess.STDOUT,check=False)
    if result.returncode!=0:
        raise RuntimeError(f"GE19_CLASS_{env['GE19_TANGENT_MODE'].upper()}_FAILED exit="+
                           str(result.returncode)+" see "+str(log))

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--class-root",type=Path,required=True)
    p.add_argument("--original-ini",type=Path,required=True)
    p.add_argument("--out-dir",type=Path,required=True)
    p.add_argument("--run",action="store_true",
                   help="actually execute CLASS; otherwise preflight only")
    args=p.parse_args()
    root=args.class_root.expanduser().resolve()
    ini=args.original_ini.expanduser().resolve()
    out=args.out_dir.expanduser().resolve()
    if not ini.is_file():
        raise RuntimeError("GE19_ORIGINAL_FROZEN_INI_MISSING")
    frozen_sha=subprocess.check_output(["git","hash-object",str(ini)],text=True).strip()
    if frozen_sha!="f9a2bde8921a148e063f9657a8ede0a51c6a629d":
        raise RuntimeError("GE19_FROZEN_EXP_INI_SOURCE_CHANGED "+frozen_sha)
    manifest=patched_source_qualification(root)
    print("GE19_FULL_CLASS_SOURCE_PATCH_PREFLIGHT_PASS",manifest["parent_source_type"],flush=True)
    if not args.run:
        print("GE19_DRY_RUN_ONLY: specify --run to execute the 5 fixed single-k controls")
        print("GE19_PHYSICS_GO False")
        return
    if out.exists() and any(out.iterdir()):
        raise RuntimeError("GE19_OUTPUT_DIRECTORY_NOT_EMPTY_REFUSE")
    out.mkdir(parents=True,exist_ok=True)
    (out/"native").mkdir(exist_ok=True)
    environment=os.environ.copy()
    environment["OMP_NUM_THREADS"]="1"
    environment["GE19_TANGENT_K_MPC"]=format(K_MPC,".12g")
    trace1=out/"baseline_dt010.csv"
    nullfile=out/"null_W1.csv"
    t1=out/"forced_dt010_W1.csv"
    trace2=out/"baseline_dt005.csv"
    t2=out/"forced_dt005_W1.csv"
    operations=[
        ("base010","record",trace1,None,"0.1",2e-7,False),
        ("null","force",trace1,nullfile,"0.1",2e-7,True),
        ("force010","force",trace1,t1,"0.1",2e-7,False),
        ("base005","record",trace2,None,"0.05",5e-8,False),
        ("force005","force",trace2,t2,"0.05",5e-8,False),
    ]
    # The two source grids and different perturbation integrator tolerances
    # do not cover all numerical errors: classify as a pilot before Ward tests.
    for label,mode,trace,output,dt,tol,zero in operations:
        cfg=make_ini(ini,out,label,tol)
        env=environment.copy()
        env.pop("GE19_TANGENT_ZERO_SOURCE",None)
        env["GE19_TANGENT_MODE"]=mode
        env["GE19_TANGENT_TRACE"]=str(trace)
        env["GE19_TANGENT_DT_MPC"]=dt
        if mode=="force":
            env["GE19_TANGENT_OUT"]=str(output)
        if zero:
            env["GE19_TANGENT_ZERO_SOURCE"]="1"
        log=out/(label+".log")
        print("GE19_CLASS_START",label,flush=True)
        run_class(root,cfg,log,env)
        print("GE19_CLASS_FINISHED",label,flush=True)
        expected=trace if mode=="record" else output
        read_trace(expected)
    b1=read_trace(trace1);b2=read_trace(trace2)
    null=read_trace(nullfile);w1=read_trace(t1);w2=read_trace(t2)
    v0=interpolate_a(b1)
    v02=interpolate_a(b2)
    zn=interpolate_a(null)
    v1=interpolate_a(w1)
    v2=interpolate_a(w2)
    ratio=float(v2/v02) if v02 else math.nan
    noise=max(abs(zn),1e-300)
    discrepancy=abs(v2-v1)
    report={
        "classification":"GE19_FULL_CLASS_TWO_PASS_TANGENT_EXPERIMENT_RUN_NOT_YET_PHYSICS_GO",
        "source_patch_manifest":manifest,
        "k_mpc":K_MPC,"target_z":0.5,"target_a":TARGET_A,
        "base_dt010_W0":v0,"base_dt005_W0":v02,
        "null_zero_source_W":zn,
        "direct_tangent_dt010_W1":v1,"direct_tangent_dt005_W1":v2,
        "relative_tangent_per_unit_eta":ratio,
        "absolute_interpolation_plus_integration_difference":discrepancy,
        "null_control_abs":noise,
        "source_interpolation_convergence_pass":bool(
            discrepancy<=max(.03*abs(v2),1e-100)),
        "null_control_pass":bool(noise<=max(.01*abs(v2),1e-100)),
        "physical_primordial_IC_NLO_certified":False,
        "all_approximation_switch_tangent_map_certified":False,
        "independently_evolved_Einstein_and_Ward_residuals_certified":False,
        "full_covariant_action_CLASS_equivalence_certified":False,
        "DES_detection":False,"production_physics_go":False
    }
    (out/"GE19_TANGENT_EXPERIMENT_REPORT.json").write_text(
        json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+"\n")
    if not report["null_control_pass"] or not report["source_interpolation_convergence_pass"]:
        raise RuntimeError("GE19_TANGENT_NUMERIC_GATE_FAILED_READ_REPORT")
    print("GE19_FULL_CLASS_TWO_PASS_NUMERIC_SCREEN_PASS_NOT_PHYSICS_GO",ratio)
    print("GE19_FULL_CLASS_PHYSICS_GO False")
    print("GE19_REPORT",out/"GE19_TANGENT_EXPERIMENT_REPORT.json")

if __name__=="__main__":
    main()
