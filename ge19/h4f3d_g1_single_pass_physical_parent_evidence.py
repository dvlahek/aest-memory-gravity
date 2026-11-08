#!/usr/bin/env python3
"""GE19 G1 single-pass evidence: exact polynomial X10 bridge + parent scope.

No new H1/Z11/GE05 integration; no H4 source/Ward calculation. The exact
rational Bernstein bound applies ONLY to the two explicitly defined
piecewise-cubic Hermite X10 representations constructed from frozen floats.
It is NOT an original-action Euler, D47 continuous nominal, Z11, GE05 or
H4 physics certificate. The original D12R3 G3 prelock is not modified.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
from decimal import Decimal, localcontext
from fractions import Fraction as F
from pathlib import Path

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
PINS={
  "ge19/h4f3d17_actual_original_action_dense_canonical_H1.py":
      "813c350d1d1860515997ce43f223b9b6bc2091e9",
  "ge19/h4f3b_actual_corrected_six_piece_source.py":
      "0423cbc64f6cda3b2a9aeb67c734935ef3ae7f9c",
  "ge19/repair07_window_retarded_reduced_h3_z20_particular.py":
      "e34d28a2062c748f48bc82fa928844b02631de25",
  "ge19/h4f3d_g1c2_d17_h3f_physical_field_bridge.py":
      "1ae67ca13456374b8efe853fe17809229588cb10",
  "ge19/h4f3d12r3_predata_full_ward_numerical_budget_prelock.json":
      "1b6b26fe85eb9dfbdb820b8279aee2bf0ed1854f"
}
LOCKED_INPUTS={
  "D17":("results/ge19_h4f3d17_actual_original_action_dense_canonical_H1.npz",
     "cd3bcf8cf5ac9ab14385baa4d90bd53400daae9f2bb89d4d22bfa2a581846359"),
  "H3F":("results/ge19_h3f_corrected_y_z20_science_reclosure.npz",
     "90840755fa9febb1d8cb84609d9e58f67dec2a0a01cd6bf8e47685b45caa4542"),
  "G1B":("results/ge19_g1b_h1_parent_lineage_20261107_r1.json",
     "eb7de28b3c8640229d6fb24a104e97e3e4a9b41adf498b111ce2a0554ea9f300"),
  "G1C2":("results/ge19_g1c2_d17_h3f_physical_20261107.json",
     "99b21b3c52d550b3f93348b401d9abe22383c93415aeb47d56099b0742da46c4")
}
MODES=(3,5,8,10,15,20)
SCALE=10**30
ZERO=F(0)
ONE=F(1)

def require(ok,reason):
    if not bool(ok):raise RuntimeError("G1_SINGLE_PASS_"+reason)

def sha(p):
    h=hashlib.sha256()
    with Path(p).open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):h.update(b)
    return h.hexdigest()

def source_locks():
    result={}
    for path,want in PINS.items():
        got=subprocess.check_output(
            ["git","rev-parse","HEAD:"+path],cwd=ROOT,text=True).strip()
        require(len(got)==40,"MISSING_SOURCE_"+path)
        require(got==want,"SOURCE_BLOB_CHANGED_"+path)
        result[path]={"git_blob":got,
                      "exact":got==want}
    d17=(ROOT/"ge19/h4f3d17_actual_original_action_dense_canonical_H1.py").read_text()
    require("saved[prefix+'X10_original_action_dense_sub4']=Xdense" in d17 and
            "saved[prefix+'X10_x_original_action_dense_sub4']=Xxdense" in d17 and
            "saved[prefix+'X10_original_H3F_knots']=Xorig" in d17 and
            "saved[prefix+'X10_x_original_H3F_H1dot_knots']=Xxorig" in d17,
            "D17_SOURCE_DICTIONARY_CHANGED")
    return result

def locked_inputs(rd):
    paths={}
    report={}
    for k,(name,want) in LOCKED_INPUTS.items():
        p=ROOT/name if not Path(name).is_absolute() else Path(name)
        # --results-dir is intentionally supported without altering expected hashes
        if name.startswith("results/"):
            p=rd/name.split("/",1)[1]
        require(p.is_file(),"MISSING_FROZEN_INPUT_"+k+"_"+str(p))
        got=sha(p)
        require(got==want,"FROZEN_SHA256_CHANGED_"+k+"_"+got)
        paths[k]=p
        report[k]={"sha256":got,"bytes":p.stat().st_size,
                   "file":p.name}
    return paths,report

def fv(v):
    return F.from_float(float(v))

def cval(v):
    z=complex(v)
    require(math.isfinite(z.real) and math.isfinite(z.imag),
            "NONFINITE_COMPLEX_INPUT")
    return fv(z.real),fv(z.imag)

def add(a,b):return a[0]+b[0],a[1]+b[1]
def sub(a,b):return a[0]-b[0],a[1]-b[1]
def mul(s,a):return s*a[0],s*a[1]
def lin(*pairs):
    r=(ZERO,ZERO)
    for s,a in pairs:r=add(r,mul(s,a))
    return r

def hermite_exact(x0,x1,v0,v1,d0,d1,x):
    h=x1-x0
    require(h>0,"NONINCREASING_COARSE_INTERVAL")
    t=(x-x0)/h
    require(ZERO<=t<=ONE,"FINE_NODE_OUTSIDE_COARSE_INTERVAL")
    t2=t*t;t3=t2*t
    v=lin((2*t3-3*t2+1,v0),(t3-2*t2+t,mul(h,d0)),
          (-2*t3+3*t2,v1),(t3-t2,mul(h,d1)))
    derivative=lin(((6*t2-6*t)/h,v0),
                   (3*t2-4*t+1,d0),
                   ((-6*t2+6*t)/h,v1),
                   (3*t2-2*t,d1))
    return v,derivative

def upper_complex(z):
    q=z[0]*z[0]+z[1]*z[1]
    if q==0:return ZERO
    # Exact rational upper bound: floor(sqrt(q)*1e30)+1, no
    # floating-point norm or Taylor approximation.
    v=math.isqrt((q.numerator*SCALE*SCALE)//q.denominator)
    return F(v+1,SCALE)

def as_exact_decimal(x):
    with localcontext() as ctx:
        ctx.prec=80
        return format(Decimal(x.numerator)/Decimal(x.denominator),"f")

def hermite_bridge(d17):
    result={}
    max_all=ZERO
    with np.load(d17,allow_pickle=False) as a:
        keys=[
            "primary_C_star_x_dense_sub4",
            "primary_C_star_X10_original_action_dense_sub4",
            "primary_C_star_X10_x_original_action_dense_sub4",
            "primary_C_star_X10_original_H3F_knots",
            "primary_C_star_X10_x_original_H3F_H1dot_knots",
        ]
        require(all(k in a.files for k in keys),"MISSING_D17_FROZEN_X10_KEYS")
        x=np.asarray(a[keys[0]],float)
        xf=np.asarray(a[keys[1]],complex)
        dxf=np.asarray(a[keys[2]],complex)
        xh=np.asarray(a[keys[3]],complex)
        dxh=np.asarray(a[keys[4]],complex)
        require(x.shape==(509,) and
                xf.shape==dxf.shape==(6,509) and
                xh.shape==dxh.shape==(6,128),
                "ORIGINAL_X10_SHAPES_CHANGED")
        require(np.isfinite(x).all() and
                all(np.isfinite(t).all() for t in (xf,dxf,xh,dxh)),
                "NONFINITE_INPUT")
        require(np.all(np.diff(x)>0),"NONMONOTONE_D17_GRID")
        # Original Nt128 nodes must be exactly at every fourth D17 substep.
        for mindex,mode in enumerate(MODES):
            worst=ZERO
            worst_fine=-1
            worst_control=-1
            for j in range(127):
                a0=fv(x[4*j]);a1=fv(x[4*j+4])
                v0=cval(xh[mindex,j]);v1=cval(xh[mindex,j+1])
                d0=cval(dxh[mindex,j]);d1=cval(dxh[mindex,j+1])
                for k in range(4):
                    ix=4*j+k
                    z0=fv(x[ix]);z1=fv(x[ix+1]);h=z1-z0
                    require(h>0,"FINE_INTERVAL_NOT_POSITIVE")
                    coarse0,coarse_d0=hermite_exact(
                        a0,a1,v0,v1,d0,d1,z0)
                    coarse1,coarse_d1=hermite_exact(
                        a0,a1,v0,v1,d0,d1,z1)
                    f0=cval(xf[mindex,ix])
                    f1=cval(xf[mindex,ix+1])
                    fd0=cval(dxf[mindex,ix])
                    fd1=cval(dxf[mindex,ix+1])
                    g0=sub(coarse0,f0)
                    g1=sub(coarse1,f1)
                    dg0=sub(coarse_d0,fd0)
                    dg1=sub(coarse_d1,fd1)
                    # On this D17 fine interval, the DIFFERENCE of
                    # the two cubic polynomials has Bernstein controls:
                    controls=(g0,add(g0,mul(h/3,dg0)),
                              sub(g1,mul(h/3,dg1)),g1)
                    for idx,b in enumerate(controls):
                        ub=upper_complex(b)
                        if ub>worst:
                            worst,worst_fine,worst_control=ub,ix,idx
            result[str(mode)]={
                "upper_bound_exact_on_frozen_float_cubic_surrogates":
                    as_exact_decimal(worst),
                "dominant_fine_interval":worst_fine,
                "dominant_Bernstein_control":worst_control,
                "fine_intervals":508,
                "coarse_intervals":127,
                "bound_type":"global_abs_Linfty_x_of_X10_surrogate_difference"
            }
            print(f"G1_X10_HERMITE m={mode} exact_input_bound={as_exact_decimal(worst)}",
                  flush=True)
            max_all=max(max_all,worst)
    return result,as_exact_decimal(max_all)

def read_optional(path,want_class=None,want_sha=None,flags=()):
    if not path.is_file():return {"status":"MISSING","path":str(path)}
    got=sha(path)
    if want_sha is not None and got!=want_sha:
        return {"status":"SHA_MISMATCH","file":path.name,"observed":got,
                "expected":want_sha}
    try:j=json.loads(path.read_text())
    except (OSError,ValueError) as e:
        return {"status":"INVALID_JSON","file":path.name,"error":str(e)}
    if not isinstance(j,dict):
        return {"status":"INVALID_JSON_ROOT","file":path.name}
    valid=(want_class is None or j.get("classification")==want_class)
    valid=valid and all(j.get(k) is True for k in flags)
    return {"status":"FROZEN_DECLARED_SCOPE_PASS" if valid else "NOT_CERTIFIED",
            "sha256":got,"file":path.name,
            "classification":j.get("classification"),
            "required_flags":{k:j.get(k) for k in flags}}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--results-dir",type=Path,default=ROOT/"results")
    ap.add_argument("--d47-dir",type=Path,
                    default=ROOT/"results/d47_offclock_first_interval")
    ap.add_argument("--json-out",type=Path,required=True)
    args=ap.parse_args()
    require(not args.json_out.exists(),"REFUSE_OVERWRITE_REPORT")
    locks=source_locks()
    paths,digests=locked_inputs(args.results_dir)
    b=json.loads(paths["G1B"].read_text())
    c=json.loads(paths["G1C2"].read_text())
    require(b.get("classification")==
           "GE19_G1B_H3F_REPAIR22_H1_NODAL_IDENTITY_EXACT_PASS_CONTINUOUS_OPEN"
           and b.get("same_H1_nodal_values") is True,
           "G1B_FROZEN_CLASSIFICATION_CHANGED")
    require(c.get("classification")==
           "GE19_G1C2_D17_H3F_COMPARABLE_PHYSICAL_FIELD_AND_X10_NODAL_DIAGNOSTIC_PASS_CONTINUOUS_OPEN",
           "G1C2_FROZEN_CLASSIFICATION_CHANGED")
    nodal=c["physical_field_and_X10_metrics"]
    require(set(nodal)==set(map(str,MODES)),"G1C2_MISSING_MODE")
    worst_nodal={k:max(float(nodal[str(m)][k]["global_relative_L2_difference"])
                       for m in MODES)
                 for k in ("all_four_physical_fields","X10","X10_x")}
    require(all(np.isfinite(list(worst_nodal.values()))),"NONFINITE_G1C2")
    hermite,max_bound=hermite_bridge(paths["D17"])
    d47={}
    for mode in MODES:
        p=args.d47_dir/f"d47_r5g8_primary_cstar_m{mode}_n256_continuous_h1_final.json"
        exp=f"GE19_D47_R5G8_PRIMARY_CSTAR_M{mode}_N256_CONTINUOUS_H1_ARB_PASS"
        d=read_optional(p,exp,flags=("case_mode_continuous_H1_error_enclosed",
                                   "case_mode_fullwindow_endpoint_H1_error_enclosed"))
        if d["status"]=="FROZEN_DECLARED_SCOPE_PASS":
            j=json.loads(p.read_text())
            d["D17_original_sha_visible_in_report"]=(digests["D17"]["sha256"]
                                                       in json.dumps(j))
            if not d["D17_original_sha_visible_in_report"]:
                d["status"]="D17_PROVENANCE_MISSING"
        d47[str(mode)]=d
        print(f"G1_D47 m={mode} status={d['status']}",flush=True)
    pre=json.loads((ROOT/"ge19/h4f3d12r3_predata_full_ward_numerical_budget_prelock.json").read_text())
    frozen=pre["frozen_artifacts"]
    chosen={}
    for name,classification,flags in (
        ("D55CR11F_json",
         "GE19_D55CR11F_CONTINUUM_BATH_AND_GE05_ONSHELL_CLOSURE_PASS_H4_OPEN",
         ("continuous_X10_certified","continuum_bath_quadrature_certified",
          "GE05_bath_onshell_certified")),
        ("H4F3B_json",
         "GE19_H4F3B_ACTUAL_CORRECTED_SIX_SOURCE_PASS_FULL_WARD_OPEN",()),
    ):
        row=frozen[name];file=ROOT/row["path"]
        chosen[name]=read_optional(file,classification,row["sha256"],flags)
    chosen["Repair32C_Z11_artifact"] = read_optional(
        args.results_dir/"ge19_repair32c_artifact_only_reduced_z11_certification.json",
        "GE19_REPAIR32C_ARTIFACT_ONLY_REDUCED_Z11_CERTIFICATION_PASS",
        "037314effa33c5bfaf51f6f3c72459de43cb486c6ef5e9a94f5b1984a68611b9",
        ("Z11_certified",))
    reported={
      "classification":"GE19_G1_SINGLE_PASS_EXACT_X10_HERMITE_SURROGATE_BOUND_G1_CONTINUOUS_OPEN",
      "all_frozen_source_blobs_locked":True,
      "frozen_inputs":digests,"source_locks":locks,
      "G1B_nodal_lineage_14_of_14_exact":True,
      "G1C2_nodal_physical_relative_L2_worst":worst_nodal,
      "X10_exact_rational_Bernstein_piecewise_Hermite_bridge":hermite,
      "X10_exact_rational_Bernstein_worst_global_abs":max_bound,
      "X10_bound_claim":"Exact-input, ideal-representation L_infinity_x bound of difference between H3F coarse cubic Hermite X10 (128 knots) and D17 fine cubic Hermite X10 (509 knots); uses exact rational arithmetic for all stored binary64 values and an integer-sqrt outward modulus ceiling at 1e-30. Does not bound exact action trajectory, D47 certified nominal if different, actual H4 PCHIP reconstruction, or errors in frozen input arrays.",
      "D47_original_Cstar_primary_per_mode":d47,
      "D47_six_source_certificates_present_and_scoped":
          all(d.get("status")=="FROZEN_DECLARED_SCOPE_PASS" for d in d47.values()),
      "upstream_original_H4_Z11_GE05_scoped_certificates":chosen,
      "G1_continuous_H1_H3F_action_Euler_bound":False,
      "G1_continuous_Z11_Euler_bound":False,
      "G1_full_GE05_to_H4_common_cohort_certified":False,
      "G1_parent_lower_boundary_continuous_bound":False,
      "G1_PHYSICAL_CLOSED":False,
      "G3_physical_D9_B_total_frozen":False,
      "full_H4_Ward_certified":False,
      "Z21_certified":False,
      "lensing_licensed":False,
      "next_physics_decision":"G1_OPEN: Compare D47 certified continuous NOMINAL (not merely endpoints) with the declared D17 fine-Hermite X10 interpolation and actual H4 source interpolant; combine errors in identical absolute norm and scale, then certify Z11/GE05 first-order Euler and lower-boundary enclosures. Missing D47 m20 must be supplied or remain explicitly out of scope. No G3/H4/lensing license yet.",
      "no_original_science_gate_changed":True
    }
    args.json_out.parent.mkdir(parents=True,exist_ok=True)
    args.json_out.write_text(json.dumps(reported,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print(reported["classification"],flush=True)
if __name__=="__main__":
    main()
