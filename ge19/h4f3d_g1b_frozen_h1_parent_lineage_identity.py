#!/usr/bin/env python3
"""G1B: immutable H3F vs Repair22 nodal H1/H1dot parent identity audit.

These are the exact two H1 parent ancestry routes used in H4F3B and
Repair32B->Z11, respectively. Compare only immutable NPZ arrays on the
same grids; do not solve H1, Z11, H4 or use observed Ward residuals.

Exact array identity, if found, is a nodal-data fact, not a certified
continuous parent Euler bound or transfer of a D47/D55 enclosure.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re as regex
import subprocess
from pathlib import Path

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
FILES={
    "h3f":(
      "ge19_h3f_corrected_y_z20_science_reclosure.npz",
      "90840755fa9febb1d8cb84609d9e58f67dec2a0a01cd6bf8e47685b45caa4542",
    ),
    "repair22":(
      "ge19_repair22_on_shell_parent_z20_certification.npz",
      "3020e0d040f902ab2609e05705f4508d9919665b1344fa0e641644ea8fc41a16",
    ),
}
PINS={
    "ge19/h4f3b_actual_corrected_six_piece_source.py":
      "0423cbc64f6cda3b2a9aeb67c734935ef3ae7f9c",
    "ge19/h3f_corrected_y_z20_science_reclosure.py":
      "31e36aaf16c8d68f0ad1ffaff97459d67a23a8b0",
    "ge19/repair22_on_shell_parent_z20_certification.py":
      "4860d13c881f41dbacbdc16ff179e917644ea6a5",
    "ge19/repair32b_factor2_corrected_reduced_h2_z11_reconstruction.py":
      "6ece578e8a30f48faaded8808687a9bd5c114608",
}
TINY=1e-300

def sha256(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1<<20),b""):
            h.update(block)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--results-dir",type=Path,
                    default=ROOT/"results")
    ap.add_argument("--json-out",type=Path,required=True)
    args=ap.parse_args()
    if args.json_out.exists():
        raise RuntimeError("REFUSE_OVERWRITE_OLD_RESULT")
    locks={}
    for path,want in PINS.items():
        got=subprocess.check_output(
            ["git","rev-parse","HEAD:"+path],
            cwd=ROOT,text=True).strip()
        if got!=want:
            raise RuntimeError(f"FROZEN_SOURCE_BLOB_MISMATCH {path}")
        locks[path]={"expected":want,"observed":got,"exact":True}
    h4=(ROOT/"ge19/h4f3b_actual_corrected_six_piece_source.py").read_text()
    r32=(ROOT/"ge19/repair32b_factor2_corrected_reduced_h2_z11_reconstruction.py").read_text()
    if ('h1=np.asarray(h3f[f"{tag}_H1_{label}"],complex)' not in h4
       or 'h1=np.asarray(z22[f"{tag}_H1_{label}"],complex)' not in r32):
        raise RuntimeError("SOURCE_PARENT_LINEAGE_BINDINGS_CHANGED")

    paths={}
    hashes={}
    for key,(name,want) in FILES.items():
        p=args.results_dir/name
        if not p.is_file():
            raise FileNotFoundError(f"MISSING_IMMUTABLE_PARENT_{key}: {p}")
        actual=sha256(p)
        if actual!=want:
            raise RuntimeError(f"SHA256_MISMATCH_{key}: {actual}")
        paths[key]=p
        hashes[key]={"path":str(p),"expected":want,"observed":actual,
                     "exact":True,"bytes":p.stat().st_size}
    with np.load(paths["h3f"],allow_pickle=False) as h,         np.load(paths["repair22"],allow_pickle=False) as r:
        match=regex.compile(r"^(.+)_H1_(primary|control)$")
        hk={k for k in h.files if match.match(k)}
        rk={k for k in r.files if match.match(k)}
        if not hk or hk!=rk:
            raise RuntimeError(
                "FROZEN_H1_KEYSETS_INCONSISTENT "+
                json.dumps({"h3f":sorted(hk),"r22":sorted(rk)}))
        detail={}
        all_exact=True
        finite=True
        for grid in ("primary","control"):
            xname="x_"+grid
            if xname not in h.files or xname not in r.files:
                raise RuntimeError("MISSING_GRID_AXIS "+xname)
            pairs=[xname]
            pairs+=sorted(k for k in hk if k.endswith("_"+grid))
            pairs+=[k.replace("_H1_","_H1dot_") for k in pairs[1:]]
            for key in pairs:
                if key not in h.files or key not in r.files:
                    raise RuntimeError("MISSING_PARENT_FIELD "+key)
                A=np.asarray(h[key])
                B=np.asarray(r[key])
                if A.shape!=B.shape:
                    raise RuntimeError("SHAPE_MISMATCH "+key)
                if not np.isfinite(A).all() or not np.isfinite(B).all():
                    raise RuntimeError("NONFINITE_PARENT "+key)
                ae=float(np.max(np.abs(A-B))) if A.size else 0.0
                re=float(np.linalg.norm(A-B)/max(np.linalg.norm(A),
                                                  np.linalg.norm(B),TINY))
                same=bool(np.array_equal(A,B))
                detail[key]={"shape":list(A.shape),
                             "bitwise_numeric_array_equal":same,
                             "max_abs_difference":ae,"relative_L2":re}
                all_exact=all_exact and same
                finite=finite and bool(np.isfinite(re) and np.isfinite(ae))
                print("G1B_PARENT "+key+" exact="+str(same)+
                      " relL2="+format(re,".9g"),flush=True)
    out={
      "classification":(
        "GE19_G1B_H3F_REPAIR22_H1_NODAL_IDENTITY_EXACT_PASS_CONTINUOUS_OPEN"
        if all_exact else
        "GE19_G1B_H3F_REPAIR22_H1_NODAL_DIFFERENCE_RECORDED_CONTINUOUS_OPEN"),
      "frozen_git_source_locks":locks,
      "immutable_npz_hashes":hashes,
      "source_lineage":"H4F3B <- H3F H1; Repair32B Z11 <- Repair22 H1",
      "same_H1_nodal_values":bool(all_exact),
      "all_fields_finite":finite,
      "per_field":detail,
      "continuous_H1_Euler_enclosure_transferred":False,
      "continuous_Z11_Euler_enclosure_certified":False,
      "D47_D55_enclosure_equivalence_proved":False,
      "full_H4_Ward_certified":False,
      "Z21_certified":False,
      "lensing_licensed":False,
      "claim_boundary":"Source-locked exact-array identity/difference "
       "audit of the H1 and H1dot nodal data entering H4F3B and "
       "Repair32B parent construction. A nodal match alone proves neither "
       "off-clock trajectory identity nor interval Euler enclosures. "
       "A difference is a provenance finding, not a science FAIL. "
       "No source alteration or solver execution.",
    }
    args.json_out.parent.mkdir(parents=True,exist_ok=True)
    args.json_out.write_text(
        json.dumps(out,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print(out["classification"],flush=True)

if __name__=="__main__":
    main()
