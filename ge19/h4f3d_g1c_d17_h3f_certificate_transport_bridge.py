#!/usr/bin/env python3
"""GE19 G1C: read-only bridge from H3F H1 knots to D17 nominal trajectory.

Only immutable H3F/D17 NPZ and D47 R5g8 JSONs are read. No integration,
reprojection, source evaluation or H4 residual. D47 encloses the true
original-action H1 about D17 nominal; differences to the saved H3F H1
are an additional term, NOT part of the D47 certificate itself.

Important: nodal bridge != continuous interval enclosure transfer.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
SOURCE_BLOBS={
  "ge19/h4f3d17_actual_original_action_dense_canonical_H1.py":
      "813c350d1d1860515997ce43f223b9b6bc2091e9",
  "ge19/h4f3d17_predata_original_action_dense_canonical_H1.json":
      "ddc41ba88b6e93dfee63ac0c49943d59cebe0604",
  "ge19/h4f3d17_original_action_dense_H1_core.py":
      "6074d31050450440654bdc55980a13584d5ce5ee",
  "ge19/h3f_corrected_y_z20_science_reclosure.py":
      "31e36aaf16c8d68f0ad1ffaff97459d67a23a8b0",
  "ge19/h4f3b_actual_corrected_six_piece_source.py":
      "0423cbc64f6cda3b2a9aeb67c734935ef3ae7f9c",
  "ge19/repair07_window_retarded_reduced_h3_z20_particular.py":
      "e34d28a2062c748f48bc82fa928844b02631de25",
}
FILES={
  "h3f":("ge19_h3f_corrected_y_z20_science_reclosure.npz",
         "90840755fa9febb1d8cb84609d9e58f67dec2a0a01cd6bf8e47685b45caa4542"),
  "d17":("ge19_h4f3d17_actual_original_action_dense_canonical_H1.npz",
         "cd3bcf8cf5ac9ab14385baa4d90bd53400daae9f2bb89d4d22bfa2a581846359"),
}
MODES=(3,5,8,10,15,20)
TINY=1.e-300

def sha(path):
    hasher=hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda:stream.read(1<<20),b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def exact_git_sources():
    pins={}
    for rel,want in SOURCE_BLOBS.items():
        got=subprocess.check_output(
            ["git","rev-parse","HEAD:"+rel],cwd=ROOT,text=True).strip()
        if got!=want:
            raise RuntimeError("FROZEN_SOURCE_BLOB_MISMATCH "+rel+" "+got)
        pins[rel]={"expected":want,"observed":got,"exact":True}
    main=(ROOT/"ge19/h4f3d17_actual_original_action_dense_canonical_H1.py").read_text()
    source=(ROOT/"ge19/h4f3b_actual_corrected_six_piece_source.py").read_text()
    required={
        "D17_original_H3F_initial_q0":
            "q0=h1[im,[1,2,3,4],0]" in main,
        "D17_original_H3F_initial_v0":
            "v0=h1dot[im,:,0]" in main,
        "D17_original_action_operator":
            "r7._canonical_operator_matrices(" in main,
        "D17_saved_canonical_H1":
            "saved[prefix+'H1_canonical_y_dense_sub4']=Ydense" in main,
        "D17_retains_original_clock_knots":
            "np.array_equal(ymode[4][0][::4],xx)" in main,
        "H4F3B_H1_from_H3F":
            'h1=np.asarray(h3f[f"{tag}_H1_{label}"],complex)' in source,
    }
    if not all(required.values()):
        raise RuntimeError("FROZEN_D17_H4_H3F_SOURCE_LINEAGE_CHANGED "+str(required))
    return pins,required

def load_frozen(rd):
    data={}
    paths={}
    for key,(filename,want) in FILES.items():
        path=rd/filename
        if not path.is_file():raise FileNotFoundError("MISSING_"+key+" "+str(path))
        got=sha(path)
        if got!=want:
            raise RuntimeError("FROZEN_SHA_MISMATCH_"+key+" "+got)
        data[key]={"name":filename,"expected_sha256":want,
                   "actual_sha256":got,"bytes":path.stat().st_size}
        paths[key]=path
    return paths,data

def read_d47_reports(folder,d17_hash):
    mode_reports={}
    missing=[]
    for m in MODES:
        filename=f"d47_r5g8_primary_cstar_m{m}_n256_continuous_h1_final.json"
        p=folder/filename
        if not p.is_file():
            missing.append(filename)
            continue
        try:
            j=json.loads(p.read_text())
        except Exception as exc:
            raise RuntimeError("UNREADABLE_D47_CERT "+str(p)+" "+str(exc))
        expected=f"GE19_D47_R5G8_PRIMARY_CSTAR_M{m}_N256_CONTINUOUS_H1_ARB_PASS"
        if not isinstance(j,dict):
            raise RuntimeError("D47_CERT_NOT_JSON_OBJECT "+filename)
        def find_named(obj,key):
            matches=[]
            if isinstance(obj,dict):
                for k,v in obj.items():
                    if k==key:matches.append(v)
                    if isinstance(v,(dict,list)):matches.extend(find_named(v,key))
            elif isinstance(obj,list):
                for v in obj:
                    if isinstance(v,(dict,list)):matches.extend(find_named(v,key))
            return matches
        def find_hash(obj,hash_value):
            if isinstance(obj,str):return hash_value in obj
            if isinstance(obj,dict):return any(find_hash(v,hash_value) for v in obj.values())
            if isinstance(obj,list):return any(find_hash(v,hash_value) for v in obj)
            return False
        flags=find_named(j,"case_mode_continuous_H1_error_enclosed")
        endpoint=find_named(j,"case_mode_fullwindow_endpoint_H1_error_enclosed")
        mode_reports[str(m)]={
            "file":filename,"sha256":sha(p),"bytes":p.stat().st_size,
            "classification":j.get("classification"),
            "expected_classification":expected,
            "exact_classification_match":j.get("classification")==expected,
            "continuous_H1_flag_values":flags,
            "continuous_H1_flag_explicit_true":len(flags)>0 and all(v is True for v in flags),
            "endpoint_H1_flag_values":endpoint,
            "original_D17_NPZ_sha_text_found":find_hash(j,d17_hash),
            "available_top_level_keys":sorted(j.keys())[:100],
        }
        print("G1C_D47_CERT m="+str(m)+" class_exact="+
              str(mode_reports[str(m)]["exact_classification_match"])+
              " continuous_true="+str(mode_reports[str(m)]["continuous_H1_flag_explicit_true"])+
              " D17_SHA_visible="+str(mode_reports[str(m)]["original_D17_NPZ_sha_text_found"]),flush=True)
    return mode_reports,missing

def compare_h3f_d17(paths):
    comparisons={}
    with np.load(paths["h3f"],allow_pickle=False) as h,         np.load(paths["d17"],allow_pickle=False) as d:
        xh=np.asarray(h["x_primary"],float)
        xd=np.asarray(d["primary_C_star_x_dense_sub4"],float)
        y=np.asarray(d["primary_C_star_H1_canonical_y_dense_sub4"],complex)
        q=np.asarray(h["C_star_H1_primary"],complex)
        p=np.asarray(h["C_star_H1dot_primary"],complex)
        if xh.shape!=(128,) or xd.shape!=(509,) or y.shape!=(6,8,509):
            raise RuntimeError("ORIGINAL_D17_GRID_OR_CANONICAL_SHAPE_CHANGED")
        if q.shape!=(6,6,128) or p.shape!=(6,4,128):
            raise RuntimeError("FROZEN_H3F_PARENT_SHAPE_CHANGED")
        if not np.array_equal(xh,xd[::4]):
            raise RuntimeError("D17_H3F_CLOCK_NODES_DIFFER")
        if not all(np.isfinite(z).all() for z in (xh,xd,y,q,p)):
            raise RuntimeError("NONFINITE_FROZEN_H1_INPUT")
        for im,m in enumerate(MODES):
            # Frozen canonical y=(S,u,phi,T,pS,pu,pphi,pT),
            # frozen H3F state=(N,S,u,phi,T,drho).
            h1y=np.concatenate((q[im,[1,2,3,4],:],p[im]),axis=0)
            yn=y[im,:,::4]
            delta=yn-h1y
            per={
               "H3F_mode_index":im,
               "canonical_component_order":
                    ["S","u","phi","T","pS","pu","pphi","pT"],
               "shape":list(yn.shape),
               "initial_8D_max_abs_delta":float(np.max(np.abs(delta[:,0]))),
               "max_abs_delta_at_128_nodes":float(np.max(np.abs(delta))),
               "global_relative_L2_difference_at_nodes":
                    float(np.linalg.norm(delta)/
                          max(np.linalg.norm(yn),np.linalg.norm(h1y),TINY)),
               "per_component_max_abs_delta":
                    [float(np.max(np.abs(delta[j]))) for j in range(8)],
               "both_inputs_finite":True
            }
            comparisons[str(m)]=per
            print("G1C_CSTAR_D17_H3F m="+str(m)+
                  " initial_abs="+format(per["initial_8D_max_abs_delta"],".8g")+
                  " nodal_rel="+format(per["global_relative_L2_difference_at_nodes"],".8g"),
                  flush=True)
    return comparisons

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--results-dir",type=Path,default=ROOT/"results")
    ap.add_argument("--d47-dir",type=Path,
                    default=ROOT/"results/d47_offclock_first_interval")
    ap.add_argument("--json-out",type=Path,required=True)
    a=ap.parse_args()
    if a.json_out.exists():
        raise RuntimeError("REFUSE_OVERWRITE_FROZEN_REPORT "+str(a.json_out))
    pins,binding=exact_git_sources()
    paths,hashes=load_frozen(a.results_dir)
    comparisons=compare_h3f_d17(paths)
    d47,missing=read_d47_reports(a.d47_dir,hashes["d17"]["actual_sha256"])
    usable=(len(d47)==6 and all(x["exact_classification_match"] and
                 x["continuous_H1_flag_explicit_true"] for x in d47.values()))
    status=("GE19_G1C_D17_H3F_NODAL_BRIDGE_EXACT_SOURCE_PASS_D47_SIX_CERTS_PRESENT_CONTINUOUS_TRANSFER_OPEN"
            if usable else
            "GE19_G1C_D17_H3F_NODAL_BRIDGE_EXACT_SOURCE_PASS_D47_CERT_PROVENANCE_INCOMPLETE")
    report={
       "classification":status,
       "frozen_source_locks":pins,"source_bindings":binding,
       "frozen_file_hashes":hashes,
       "C_star_primary_H1_nodal_comparisons":comparisons,
       "D47_R5g8_six_mode_certificate_metadata":d47,
       "D47_R5g8_missing_certificate_paths":missing,
       "D47_certificates_all_six_locally_verified":usable,
       "G1B_H3F_Repair22_nodal_identity_already_pass":True,
       "original_D17_initialized_from_H3F":True,
       "D17_H3F_continuous_interpolant_difference_enclosed":False,
       "D47_continuous_certificate_transferred_to_H4_H1":False,
       "Z11_continuous_Euler_enclosure_certified":False,
       "full_H4_Ward_certified":False,"Z21_certified":False,
       "lensing_licensed":False,
       "claim_boundary":"Read-only primary/C_star bridge between D17 original-action Radau nominal "
          "canonical eight-variable trajectory and the same H3F H1/H1dot values used in H4F3B; "
          "compares only 128 frozen knots. D47 R5g8 metadata is reported without changing its "
          "true-solution enclosure or bound normalization. Nodal D17/H3F differences and "
          "D47 physical error bounds cannot by themselves enclose a continuous H3F interpolant. "
          "No new physical H4 test, budget, Z21 solve or observational tuning.",
       "next_gate":"CERTIFY_OFFCLOCK_H3F_RECONSTRUCTION_VS_D17_AND_SOURCE_LIPSCHITZ_BOUNDS_ON_ORIGINAL_CSTAR_PRIMARY_INTERVAL"
    }
    a.json_out.parent.mkdir(parents=True,exist_ok=True)
    a.json_out.write_text(json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print(status,flush=True)

if __name__=="__main__":
    main()
