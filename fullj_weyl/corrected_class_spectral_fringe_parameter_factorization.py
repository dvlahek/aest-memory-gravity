#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fullj_weyl import corrected_class_spectral_fringe_bridge_identity as b

PREDATA_LOCK = "f512257fc84c312236b2eaa23f5d3b5ef9560f1d"
BRIDGE_JSON = ROOT / "results/fullj_corrected_class_spectral_fringe_bridge_identity.json"
BRIDGE_NPZ = ROOT / "results/fullj_corrected_class_spectral_fringe_bridge_identity.npz"

INCOMPLETE = "FULLJ_CLASS_FRINGE_PARAMETER_FACTORIZATION_INCOMPLETE"
INCONSISTENT = "FULLJ_CLASS_FRINGE_PARAMETER_FACTORIZATION_INCONSISTENT"
SERIAL = "FULLJ_CLASS_FRINGE_K_SERIALIZATION_DEPENDENCE"
PKMAX = "FULLJ_CLASS_FRINGE_PKMAX_DEPENDENCE"
MULTI = "FULLJ_CLASS_FRINGE_MULTI_PARAMETER_DEPENDENCE"
INTERACT = "FULLJ_CLASS_FRINGE_PARAMETER_INTERACTION_DEPENDENCE"

GLOBAL_GATE = 2.0e-5
PERK_GATE = 5.0e-5


def is_ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"],
        cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    ).returncode == 0


def rel(a, c) -> float:
    aa=np.asarray(a,complex); cc=np.asarray(c,complex)
    return float(np.linalg.norm(aa-cc)/max(float(np.linalg.norm(aa)),float(np.linalg.norm(cc)),1e-300))


def per_k_rel(a, c):
    aa=np.asarray(a); cc=np.asarray(c)
    return [rel(aa[i],cc[i]) for i in range(aa.shape[0])]


def cmp(a, c):
    pp=per_k_rel(a,c)
    return rel(a,c), float(max(pp)), pp


def material(global_rel: float, per_k_max: float) -> bool:
    return bool(global_rel > GLOBAL_GATE or per_k_max > PERK_GATE)


def parse_kh(text: str):
    vals=np.asarray([float(q.strip()) for q in str(text).split(",") if q.strip()],float)
    return vals/float(b.base.cb.h)


def dict_diff(a, c, ignore=()):
    ign=set(ignore)
    out={}
    for k in sorted((set(a)|set(c))-ign):
        av=a.get(k,"<MISSING>"); cv=c.get(k,"<MISSING>")
        if str(av)!=str(cv):
            out[k]={"C00":str(av),"C11":str(cv)}
    return out


def eval_target(pars, target_pos: int, z):
    hs=b.run_histories(pars)
    if target_pos >= len(hs):
        raise RuntimeError(f"target positional index {target_pos} outside {len(hs)} returned histories")
    return b.eval_at_a(hs[target_pos],z), len(hs)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--json-out",default="results/fullj_corrected_class_spectral_fringe_parameter_factorization.json")
    ap.add_argument("--npz-out",default="results/fullj_corrected_class_spectral_fringe_parameter_factorization.npz")
    args=ap.parse_args()

    print("FULLJ_CLASS_FRINGE_PARAMETER_FACTORIZATION_START",flush=True)
    if not BRIDGE_JSON.exists() or not BRIDGE_NPZ.exists():
        out={"classification":INCOMPLETE,"diagnostic_complete":False,"reason":"missing bridge-identity R1 result"}
        Path(args.json_out).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
        print("FULLJ_CLASS_FRINGE_PARAMETER_FACTORIZATION_CLASSIFICATION="+INCOMPLETE,flush=True)
        return 3

    bj=json.loads(BRIDGE_JSON.read_text())
    bq=np.load(BRIDGE_NPZ)
    anchors=np.asarray(bq["anchors"],float)
    z=np.asarray(bq["redshifts"],float)
    B1=np.asarray(bq["B1_direct_bridge_list"],float)
    B2=np.asarray(bq["B2_bridge_params_fingerprint"],float)

    gates0=bj.get("gates",{})
    frozen=bool(
        is_ancestor(PREDATA_LOCK)
        and bj.get("classification")=="FULLJ_CLASS_FRINGE_BRIDGE_PARAMETER_DEPENDENCE"
        and bj.get("diagnostic_complete") is True
        and gates0.get("BI_G1_provenance_and_frozen_identity") is True
        and gates0.get("BI_G2_bridge_list_invariance_direct_params") is True
        and gates0.get("BI_G3_parameter_construction_identity") is False
        and gates0.get("BI_G4_history_order_identity") is True
        and gates0.get("BI_G5_bridge_time_coordinate_identity") is True
        and gates0.get("BI_G6_basis_fourier_extraction_identity") is True
        and gates0.get("BI_REPAIR_single_k_fingerprint_identity") is True
        and B1.shape==(15,9) and B2.shape==(15,9)
    )

    C00=np.full_like(B1,np.nan)
    C01=np.full_like(B1,np.nan)
    C10=np.full_like(B1,np.nan)
    C11=np.full_like(B1,np.nan)
    rows=[]
    all_corner_dict_identical=True
    only_expected_differences=True
    max_serialized_dkh=0.0

    for ik,kh in enumerate(anchors):
        mode_h=np.asarray(b.sd.poc.target_modes(float(kh)),float)
        q=np.where(np.isclose(mode_h,float(kh),rtol=0,atol=5e-13))[0]
        if len(q)!=1:
            raise RuntimeError(f"target {kh} not unique in bridge list")
        pos=int(q[0])

        p00,meta00=b.r3_params(mode_h)
        p11=b.bridge_params(mode_h)
        rawdiff=dict_diff(p00,p11)
        extra={k:v for k,v in rawdiff.items() if k not in {"k_output_values","P_k_max_h/Mpc"}}
        only_expected_differences=only_expected_differences and len(extra)==0

        p01=dict(p00)
        p01["k_output_values"]=p11["k_output_values"]
        p10=dict(p00)
        p10["P_k_max_h/Mpc"]=p11["P_k_max_h/Mpc"]
        p11_from_factors=dict(p00)
        p11_from_factors["k_output_values"]=p11["k_output_values"]
        p11_from_factors["P_k_max_h/Mpc"]=p11["P_k_max_h/Mpc"]
        corner_equal=(dict_diff(p11_from_factors,p11)=={})
        all_corner_dict_identical=all_corner_dict_identical and corner_equal

        kh00=parse_kh(p00["k_output_values"])
        kh11=parse_kh(p11["k_output_values"])
        if kh00.shape!=kh11.shape:
            raise RuntimeError("serialized k lists differ in count")
        dkh=float(np.max(np.abs(kh11-kh00))) if kh00.size else 0.0
        max_serialized_dkh=max(max_serialized_dkh,dkh)

        C00[ik],n00=eval_target(p00,pos,z)
        C01[ik],n01=eval_target(p01,pos,z)
        C10[ik],n10=eval_target(p10,pos,z)
        C11[ik],n11=eval_target(p11,pos,z)

        rows.append({
            "k_h":float(kh),"target_pos":pos,"bridge_list_h":mode_h.tolist(),
            "n_histories":[n00,n01,n10,n11],
            "P_k_max_C00":float(p00["P_k_max_h/Mpc"]),
            "P_k_max_C11":float(p11["P_k_max_h/Mpc"]),
            "serialization_chars_C00":len(str(p00["k_output_values"])),
            "serialization_chars_C11":len(str(p11["k_output_values"])),
            "max_abs_serialized_k_h_displacement":dkh,
            "unexpected_parameter_differences":extra,
            "factorized_corner_dictionary_identity":corner_equal,
            "r3_serialization_meta":meta00,
        })
        print(
            f"FULLJ_CLASS_FRINGE_PARAMETER_FACTORIZATION_RUN {ik+1:02d}/15 "
            f"k_h={kh:.5f} pos={pos} dkh={dkh:.3e}",flush=True
        )

    e00,m00,p00r=cmp(C00,B1)
    e11,m11,p11r=cmp(C11,B2)
    es,ms,ps=cmp(C01,C00)
    ep,mp,pp=cmp(C10,C00)
    ep_s17,mp_s17,pp_s17=cmp(C11,C01)
    es_p2,ms_p2,ps_p2=cmp(C11,C10)
    et,mt,pt=cmp(C11,C00)
    locked_et,locked_mt,_=cmp(B2,B1)

    g1=bool(frozen and e00<=GLOBAL_GATE and m00<=PERK_GATE)
    g2=bool(e11<=GLOBAL_GATE and m11<=PERK_GATE and all_corner_dict_identical and only_expected_differences)
    serial_mat=material(es,ms)
    pk_mat=material(ep,mp)
    total_mat=material(et,mt)
    g5=bool(total_mat and abs(et-locked_et)<=GLOBAL_GATE and abs(mt-locked_mt)<=PERK_GATE)

    if not g1 or not g2 or not g5:
        classification=INCOMPLETE
    elif serial_mat and not pk_mat:
        classification=SERIAL
    elif pk_mat and not serial_mat:
        classification=PKMAX
    elif serial_mat and pk_mat:
        classification=MULTI
    elif (not serial_mat) and (not pk_mat) and total_mat:
        classification=INTERACT
    else:
        classification=INCONSISTENT

    gates={
        "PF_G1_frozen_baseline_reproduction":g1,
        "PF_G2_historical_corner_reproduction_and_dictionary_identity":g2,
        "PF_G3_serialization_only_evaluated":True,
        "PF_G4_Pkmax_only_evaluated":True,
        "PF_G5_factorial_closure":g5,
    }
    summary={
        "C00_vs_locked_B1_global_relative_L2":e00,"C00_vs_locked_B1_per_k_max":m00,
        "C11_vs_locked_B2_global_relative_L2":e11,"C11_vs_locked_B2_per_k_max":m11,
        "serialization_only_C01_vs_C00_global_relative_L2":es,"serialization_only_C01_vs_C00_per_k_max":ms,
        "Pkmax_only_C10_vs_C00_global_relative_L2":ep,"Pkmax_only_C10_vs_C00_per_k_max":mp,
        "Pkmax_at_historical_serialization_C11_vs_C01_global_relative_L2":ep_s17,"Pkmax_at_historical_serialization_C11_vs_C01_per_k_max":mp_s17,
        "serialization_at_Pkmax2_C11_vs_C10_global_relative_L2":es_p2,"serialization_at_Pkmax2_C11_vs_C10_per_k_max":ms_p2,
        "total_C11_vs_C00_global_relative_L2":et,"total_C11_vs_C00_per_k_max":mt,
        "locked_B2_vs_B1_global_relative_L2":locked_et,"locked_B2_vs_B1_per_k_max":locked_mt,
        "serialization_material":serial_mat,"Pkmax_material":pk_mat,"total_material":total_mat,
        "max_abs_serialized_k_h_displacement":max_serialized_dkh,
        "all_factorized_corner_dictionaries_equal_historical":all_corner_dict_identical,
        "only_expected_parameter_differences":only_expected_differences,
    }
    out={
        "classification":classification,"diagnostic_complete":True,"predata_lock":PREDATA_LOCK,
        "gates":gates,"summary":summary,"rows":rows,
        "thresholds":{"global":GLOBAL_GATE,"per_k":PERK_GATE},
        "interpretation":{
            "historical_R3_reclassified":False,
            "bridge_identity_R1_reclassified":False,
            "equation_level_followup_licensed":False,
            "new_physics_claim_licensed":False,
            "Pkmax_convergence_and_matched_GR_required_if_Pkmax_material":bool(pk_mat),
        },
    }
    Path(args.json_out).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    np.savez_compressed(args.npz_out,anchors=anchors,redshifts=z,C00=C00,C01=C01,C10=C10,C11=C11,B1_locked=B1,B2_locked=B2)
    print("FULLJ_CLASS_FRINGE_PARAMETER_FACTORIZATION_SUMMARY="+json.dumps(summary,sort_keys=True),flush=True)
    print("FULLJ_CLASS_FRINGE_PARAMETER_FACTORIZATION_GATES="+json.dumps(gates,sort_keys=True),flush=True)
    print("FULLJ_CLASS_FRINGE_PARAMETER_FACTORIZATION_CLASSIFICATION="+classification,flush=True)
    return 0


if __name__=="__main__":
    raise SystemExit(main())
