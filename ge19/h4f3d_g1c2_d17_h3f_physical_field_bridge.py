#!/usr/bin/env python3
"""G1C2: correct the G1C D17/H3F comparison without new integration.

D17 y=(S,u,phi,T,pS,pu,pphi,pT), whereas H3F H1dot consists
of physical-time derivatives; p and dot(q) are NOT interchangeable.
Compare only common physical S,u,phi,T and the frozen physical X10, X10_x
observables stored by D17. All frozen source data are read-only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
SRC={
 "ge19/h4f3d17_actual_original_action_dense_canonical_H1.py":
    "813c350d1d1860515997ce43f223b9b6bc2091e9",
 "ge19/repair07_window_retarded_reduced_h3_z20_particular.py":
    "e34d28a2062c748f48bc82fa928844b02631de25",
 "ge19/h4f3d_g1c_d17_h3f_certificate_transport_bridge.py":
    "85e61246e69e6df141fbc762d5298b5662895973",
 "ge19/h4f3b_actual_corrected_six_piece_source.py":
    "0423cbc64f6cda3b2a9aeb67c734935ef3ae7f9c",
}
FILE={
 "h3f":("ge19_h3f_corrected_y_z20_science_reclosure.npz",
         "90840755fa9febb1d8cb84609d9e58f67dec2a0a01cd6bf8e47685b45caa4542"),
 "d17":("ge19_h4f3d17_actual_original_action_dense_canonical_H1.npz",
         "cd3bcf8cf5ac9ab14385baa4d90bd53400daae9f2bb89d4d22bfa2a581846359"),
}
MODES=(3,5,8,10,15,20)
FIELDS=("S","u","phi","T")
TINY=1e-300

def fail_unless(ok,reason):
    if not bool(ok):raise RuntimeError(reason)

def sha(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(1048576),b""):h.update(b)
    return h.hexdigest()

def lock_code():
    pins={}
    for p,want in SRC.items():
        got=subprocess.check_output(["git","rev-parse","HEAD:"+p],
                                    cwd=ROOT,text=True).strip()
        fail_unless(got==want,"G1C2_FROZEN_SOURCE_CHANGED "+p)
        pins[p]={"exact":True,"sha":want}
    d17=(ROOT/"ge19/h4f3d17_actual_original_action_dense_canonical_H1.py").read_text()
    r7=(ROOT/"ge19/repair07_window_retarded_reduced_h3_z20_particular.py").read_text()
    fail_unless("y0=np.concatenate([q0,p])" in r7 and
                "p=Cmat[0:4]@w" in r7 and
                "w[[6,7,8,9]]=v0" in r7,
                "ORIGINAL_CANONICAL_MOMENTUM_DICTIONARY_CHANGED")
    fail_unless("saved[prefix+'H1_canonical_y_dense_sub4']=Ydense" in d17 and
                "saved[prefix+'X10_original_action_dense_sub4']=Xdense" in d17 and
                "saved[prefix+'X10_x_original_action_dense_sub4']=Xxdense" in d17 and
                "saved[prefix+'X10_original_H3F_knots']=Xorig" in d17 and
                "saved[prefix+'X10_x_original_H3F_H1dot_knots']=Xxorig" in d17,
                "D17_SAVE_KEYS_SOURCE_CHANGED")
    return pins

def metrics(a,b):
    fail_unless(a.shape==b.shape and a.size>0,"ARRAY_SHAPE_OR_EMPTY")
    fail_unless(np.isfinite(a).all() and np.isfinite(b).all(),
                "NONFINITE_FROZEN_INPUT")
    delta=a-b
    return {
      "shape":list(a.shape),
      "max_absolute_difference":float(np.max(np.abs(delta))),
      "global_relative_L2_difference":float(
        np.linalg.norm(delta)/max(np.linalg.norm(a),np.linalg.norm(b),TINY)),
      "first_node_max_absolute_difference":float(
        np.max(np.abs(delta[...,0]))),
      "both_inputs_finite":True
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--results-dir",type=Path,default=ROOT/"results")
    ap.add_argument("--json-out",type=Path,required=True)
    args=ap.parse_args()
    fail_unless(not args.json_out.exists(),"REFUSE_OVERWRITE")
    pins=lock_code()
    paths={}
    proof={}
    for name,(filename,want) in FILE.items():
        p=args.results_dir/filename
        fail_unless(p.is_file(),"MISSING_ORIGINAL_NPZ_"+name+" "+str(p))
        got=sha(p)
        fail_unless(got==want,"FROZEN_NPZ_SHA_CHANGED "+name+" "+got)
        paths[name]=p
        proof[name]={"file":filename,"sha256":got,"bytes":p.stat().st_size}
    comparisons={}
    with np.load(paths["h3f"],allow_pickle=False) as h,\
         np.load(paths["d17"],allow_pickle=False) as d:
        xh=np.asarray(h["x_primary"],float)
        xd=np.asarray(d["primary_C_star_x_dense_sub4"],float)
        Y=np.asarray(d["primary_C_star_H1_canonical_y_dense_sub4"],complex)
        H1=np.asarray(h["C_star_H1_primary"],complex)
        H1dot=np.asarray(h["C_star_H1dot_primary"],complex)
        fail_unless(xh.shape==(128,) and xd.shape==(509,) and
                    Y.shape==(6,8,509) and H1.shape==(6,6,128) and
                    H1dot.shape==(6,4,128),
                    "FROZEN_H3F_D17_SHAPES_CHANGED")
        fail_unless(np.array_equal(xh,xd[::4]),"FROZEN_CLOCK_DISAGREES")
        values={
            "X10":(
                np.asarray(d["primary_C_star_X10_original_action_dense_sub4"],complex)[:,::4],
                np.asarray(d["primary_C_star_X10_original_H3F_knots"],complex)),
            "X10_x":(
                np.asarray(d["primary_C_star_X10_x_original_action_dense_sub4"],complex)[:,::4],
                np.asarray(d["primary_C_star_X10_x_original_H3F_H1dot_knots"],complex)),
        }
        for name,(a,b) in values.items():
            fail_unless(a.shape==(6,128) and b.shape==(6,128),
                        "FROZEN_OBSERVABLE_SHAPE_CHANGED_"+name)
        for i,m in enumerate(MODES):
            q_d17=Y[i,0:4,::4]     # physical S,u,phi,T only
            q_h3f=H1[i,[1,2,3,4],:]
            per={name:metrics(q_d17[j],q_h3f[j])
                 for j,name in enumerate(FIELDS)}
            per["X10"]=metrics(values["X10"][0][i],values["X10"][1][i])
            per["X10_x"]=metrics(values["X10_x"][0][i],values["X10_x"][1][i])
            per["all_four_physical_fields"]=metrics(q_d17,q_h3f)
            comparisons[str(m)]=per
            print("G1C2_PHYSICAL m="+str(m)+
                  " q_rel="+format(per["all_four_physical_fields"]["global_relative_L2_difference"],".9g")+
                  " q_initial_abs="+format(per["all_four_physical_fields"]["first_node_max_absolute_difference"],".9g")+
                  " X10_rel="+format(per["X10"]["global_relative_L2_difference"],".9g")+
                  " X10x_rel="+format(per["X10_x"]["global_relative_L2_difference"],".9g"),
                  flush=True)
    report={
       "classification":"GE19_G1C2_D17_H3F_COMPARABLE_PHYSICAL_FIELD_AND_X10_NODAL_DIAGNOSTIC_PASS_CONTINUOUS_OPEN",
       "source_blobs":pins,"input_sha256":proof,
       "comparison_scope":"primary C_star, original m3/5/8/10/15/20 at 128 common nodes",
       "correct_dictionary":{
          "D17_q":"S,u,phi,T", "D17_p":"pS,pu,pphi,pT",
          "H3F_H1dot":"physical-time Sdot,udot,phidot,Tdot",
          "mapping":"p=Cmat[0:4]w; p is not physical-time qdot"
       },
       "prior_G1C_8D_percentage_interpretation_valid":False,
       "physical_field_and_X10_metrics":comparisons,
       "D47_six_mode_certificate_available_in_prior_G1C":False,
       "missing_D47_report_mode_20_remains_open":True,
       "G1C_offclock_interpolant_difference_enclosed":False,
       "D47_continuous_H1_certificate_transferred_to_H4_H1":False,
       "Z11_continuous_Euler_enclosure_certified":False,
       "full_H4_Ward_certified":False,
       "Z21_certified":False,"lensing_licensed":False,
       "claim_boundary":"Original G1C eight-dimensional percentage included incomparable "
          "canonical momenta vs physical-time derivatives and must not be interpreted "
          "as a physical H1 discrepancy. This frozen-array diagnostic compares only "
          "same physical fields S,u,phi,T, true action X10 and source-derived X10_x "
          "at common nodes. Does not establish a continuous error bound or rerun D17."
    }
    args.json_out.parent.mkdir(parents=True,exist_ok=True)
    args.json_out.write_text(json.dumps(report,indent=2,sort_keys=True,
                              allow_nan=False)+"\n")
    print(report["classification"],flush=True)
if __name__=="__main__":
    main()
