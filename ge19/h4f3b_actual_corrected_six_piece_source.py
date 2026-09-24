#!/usr/bin/env python3
"""H4F3b: ACTUAL corrected-parent six-piece H4 source and physical source Ward.

This separately versioned SOURCE-ONLY adapter does not propagate Z21 and does
not infer a full Noether identity from the source projection. It obtains
genuine GE06/GE07/Lambda bilinear sources and GE05 M2 from the frozen
Repair37 implementation, replaces its historical scalar-only Y by Stage E
u+phi and replaces Repair22/Repair27 second-order parents by certified
H3F/H3G. All GE05 bath first-order nodes come from frozen Repair26 R1.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
from pathlib import Path

import numpy as np

from ge19 import repair37_cancellation_safe_fd8_h4_z21_reclosure as old
from ge19 import h4f2g_action_completed_six_piece_source_ledger as ledger
from ge19 import h4f2h_physical_time_source_ward_bridge as clock

ROOT=Path(__file__).resolve().parents[1]
PRE_BLOB="c3362f5360c2a9951d77060027c82830c031c145"
PINNED={
    "ge19/h4f3b_predata_actual_corrected_six_piece_source.json":PRE_BLOB,
    "ge19/h4f3_predata_integrated_corrected_parent_ward.json":
        "3e17163cb6f52f3a78c41e6f37f83ef682359162",
    "ge19/repair37_cancellation_safe_fd8_h4_z21_reclosure.py":
        "45d203a092f9ac71cc612b15df5f0c0c630f5898",
    "ge19/h4f2g_action_completed_six_piece_source_ledger.py":
        "d9778da0bb6cc52a15015238810c79978527ffc5",
    "ge19/h4f2h_physical_time_source_ward_bridge.py":
        "65ce1e68a2f77e063c4bb8848d770abb4baeeebf",
    "ge19/h4_stagee_versioned_y_source_rows.py":
        "282166ea5840d7fba4dbc328d40d7687afa6fa0f",
}
REQUIRED={
    "r13":("ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz",
           old.R13_NPZ_SHA),
    "h3fj":("ge19_h3f_corrected_y_z20_science_reclosure.json",
            "0616188d2bb7a6c09b2b56433a1f8a1860f360b2e54d2cb84e1ae214a407866b"),
    "h3fn":("ge19_h3f_corrected_y_z20_science_reclosure.npz",
            "90840755fa9febb1d8cb84609d9e58f67dec2a0a01cd6bf8e47685b45caa4542"),
    "h3gj":("ge19_h3g_corrected_y_q20_reconstruction.json",
            "9b93534e3ee90e1ce588bdbd3f271afd041f738b8dc6f62c4ec0d1413c27f2c4"),
    "h3gn":("ge19_h3g_corrected_y_q20_reconstruction.npz",
            "9e1bf36e1d81122225ff8c03f663501de7601a8fc9376fd86312e0ae1d809452"),
    "z11":("ge19_repair32b_factor2_corrected_reduced_h2_z11_reconstruction.npz",
            old.R32B_NPZ_SHA),
    "z11cert":("ge19_repair32c_artifact_only_reduced_z11_certification.json",
               old.R32C_JSON_SHA),
    "dense":("ge15_R1_dense_accepted_step_trace.dat",old.GE15_DENSE_SHA),
}
TRACE_SHA=old.REPAIR26_TRACE_SHA
BOUNDARY_N=2048
SOURCE_NX_Y=old.NX_DY_PRIMARY
SOURCE_NX_Q=old.NX_POLY
TINY=1e-300

def sha256(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as stream:
        for part in iter(lambda:stream.read(1<<20),b""):
            h.update(part)
    return h.hexdigest()

def rel_l2(a,b):
    x=np.asarray(a); y=np.asarray(b)
    return float(np.linalg.norm(x-y)/max(np.linalg.norm(x),
                       np.linalg.norm(y),TINY))

def code_lock():
    checks={}
    for path,want in PINNED.items():
        got=subprocess.check_output(
            ["git","rev-parse","HEAD:"+path],cwd=ROOT,text=True
        ).strip()
        checks[path]={"observed":got,"expected":want,"exact":got==want}
    if not all(v["exact"] for v in checks.values()):
        raise RuntimeError("H4F3b frozen source/predata Git blob mismatch")
    return checks

def frozen_inputs(rd,trace):
    inputs={}
    digests={}
    for key,(filename,want) in REQUIRED.items():
        path=rd/filename
        if not path.is_file():
            raise FileNotFoundError(f"missing H4F3b frozen input {path}")
        observed=sha256(path)
        digests[key]={"filename":filename,"expected":want,"observed":observed,
                      "exact":observed==want}
        if observed!=want:
            raise RuntimeError(f"frozen input {key} SHA-256 mismatch {observed}")
        inputs[key]=path
    if not (rd/"ge15_R1_cli_background.dat").is_file():
        raise FileNotFoundError("missing frozen GE15 Lambda CLI background")
    if not trace.is_file() or sha256(trace)!=TRACE_SHA or trace.stat().st_size!=old.REPAIR26_TRACE_BYTES:
        raise RuntimeError("missing or mismatched frozen Repair26 R1 full-history bath trace")
    h3f=json.loads(inputs["h3fj"].read_text())
    h3g=json.loads(inputs["h3gj"].read_text())
    z11=json.loads(inputs["z11cert"].read_text())
    if h3f.get("classification")!="GE19_H3F_CORRECTED_Y_H3_Z20_CERTIFIED" or h3f.get("Z20_certified") is not True:
        raise RuntimeError("H3F Z20 is not certified")
    if h3g.get("classification")!="GE19_H3G_CORRECTED_Y_Q20_RECONSTRUCTION_PASS" or h3g.get("q20_certified_projection") is not True:
        raise RuntimeError("H3G q20 is not certified")
    if z11.get("classification")!="GE19_REPAIR32C_ARTIFACT_ONLY_REDUCED_Z11_CERTIFICATION_PASS" or z11.get("Z11_certified") is not True:
        raise RuntimeError("frozen Repair32C Z11 certificate not PASS")
    for d in (h3f,h3g):
        if not d.get("gates") or not all(v is True for v in d["gates"].values()):
            raise RuntimeError("a corrected-parent science gate failed")
    digests["Repair26_R1_trace"]={"sha256":TRACE_SHA,
                                   "bytes":trace.stat().st_size}
    return inputs,digests

def actual_case_source(bg,tag,h1,dh1,z11,dz11,B20,wz10,
                       qdirect,mod6,mod7,ge05,boundary):
    nt=len(bg["x"])
    # Fully frozen GE06/GE07/Lambda mixed second directional source.
    direct=old.q_cross_direct(qdirect,bg,tag,h1,dh1,z11,dz11,SOURCE_NX_Q)
    swapped=old.q_cross_direct(qdirect,bg,tag,z11,dz11,h1,dh1,SOURCE_NX_Q)
    sym=max(rel_l2(a,b) for a,b in zip(direct,swapped))
    gm,gc,dm,dc=direct
    lam_m,lam_c,lam_exact,lam_pol,lam_sym=old.lambda_cross_direct(
        bg,h1,dh1,z11,dz11,SOURCE_NX_Q
    )
    non_y={
        ledger.PIECES[0]:(-2.0*old.fft_low(gm),-2.0*old.fft_low(gc)),
        ledger.PIECES[1]:(-2.0*old.fft_low(dm),-2.0*old.fft_low(dc)),
        ledger.PIECES[2]:(-2.0*old.fft_low(lam_m),-2.0*old.fft_low(lam_c)),
    }
    # The frozen first-order R1 bath is reconstructed only from certified
    # on-shell H1 and Repair26; no historical second-order q20 is consumed.
    mm,mc,z10,v10=old.reconstruct_m2_source(
        ge05,bg,h1,boundary,BOUNDARY_N,SOURCE_NX_Q
    )
    reproduced=np.einsum("b,bmt->mt",boundary["w"],z10,optimize=True)
    r1_rel=rel_l2(reproduced,wz10)
    non_y[ledger.PIECES[5]]=(mm,mc)
    first_real,_,first_space=old.r7.reduced_state_real(
        bg,h1,SOURCE_NX_Y,dh1
    )
    tangent_real,_,tangent_space=old.r7.reduced_state_real(
        bg,z11,SOURCE_NX_Y,dz11
    )
    all_beta={}
    m1,co1=old.m1_mapped_fourier(bg,B20)
    kfund=float(old.r7.g9.K_REQ[0]/old.r7.FOURIER_N[0])
    for ib,beta in enumerate(old.r7.BETAS):
        external=dict(non_y)
        external[ledger.PIECES[4]]=(m1[ib],co1[ib])
        assembled=ledger.assemble_six(
            external,bg["a"],bg["Q_action"],
            first_real["u20"],first_space["phi20"],
            tangent_real["u20"],tangent_space["phi20"],
            old.r7.KB,old.r7.A0_MPC_INV,float(beta),kfund,
            bg["x"],mmax=old.M_MAX
        )
        proper=clock.physical_six_piece_ward(
            assembled["piece_rows"],bg["x"],bg["a"],bg["H"],kfund
        )
        sum_error=float(np.max(np.abs(
            sum(assembled["piece_rows"].values())-
            assembled["total_rows"]
        )))
        clock_error=float(np.max(np.abs(
            sum(proper["per_piece"].values())-
            proper["total_source_ward"]
        )))
        all_beta[ib]={"assembled":assembled,"physical":proper,
                      "sum_error":sum_error,"clock_sum_error":clock_error}
    return all_beta,{
        "GE06_GE07_direct_cross_symmetry_relative_L2":sym,
        "Lambda_direct_vs_exact_relative_L2":lam_exact,
        "Lambda_direct_swap_relative_L2":lam_sym,
        "Repair26_R1_q10_vs_H3G_weighted_z10_relative_L2":r1_rel,
        "historical_scalar_only_Y_consumed":False,
        "historical_Repair27_q20_consumed":False,
        "actual_StageE_complete_Y_both_rows_used":True,
        "all_outputs_finite":bool(all(
            np.isfinite(q["assembled"]["total_rows"]).all() and
            np.isfinite(q["physical"]["total_source_ward"]).all()
            for q in all_beta.values()
        )),
    }

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--results-dir",type=Path,required=True)
    parser.add_argument("--repair26-trace",type=Path,required=True)
    parser.add_argument("--json-out",type=Path,required=True)
    parser.add_argument("--npz-out",type=Path,required=True)
    args=parser.parse_args()
    rd=args.results_dir.resolve()
    trace=args.repair26_trace.resolve()
    outj=args.json_out.resolve()
    outn=args.npz_out.resolve()
    for p in (outj,outn):
        if not p.name.startswith("ge19_h4f3b_"):
            raise ValueError("H4F3b must write new ge19_h4f3b_ result files")
    pinned=code_lock()
    paths,digests=frozen_inputs(rd,trace)
    save={}
    controls=[]
    with np.load(paths["r13"],allow_pickle=False) as r13,\
         np.load(paths["h3fn"],allow_pickle=False) as h3f,\
         np.load(paths["h3gn"],allow_pickle=False) as h3g,\
         np.load(paths["z11"],allow_pickle=False) as z11:
        bgs,bgctl,mod6,mod7,ge05,normf,normdiag,qdirect,lambda_diag=old.build_context(
            rd,r13
        )
        boundary=old.r24.full_history_boundary(old.c4,old.r7,
                                               trace,BOUNDARY_N)
        if len(boundary["w"])!=BOUNDARY_N:
            raise RuntimeError("frozen R1 bath quadrature node count changed")
        for nt,label in ((128,"primary"),(64,"control")):
            for tag in old.r7.C_TAGS:
                bg=bgs[(nt,tag)]
                for parent in (h3f,h3g,z11):
                    if not np.array_equal(
                        np.asarray(parent["x_"+label],float),
                        np.asarray(bg["x"],float)
                    ):
                        raise RuntimeError(f"mismatched certified x grid Nt={nt} {tag}")
                h1=np.asarray(h3f[f"{tag}_H1_{label}"],complex)
                dh1=np.asarray(h3f[f"{tag}_H1dot_{label}"],complex)
                tangent=np.asarray(z11[f"{tag}_Z11_{label}"],complex)
                tangent_dot=np.asarray(z11[f"{tag}_Z11dot_{label}"],complex)
                B20=np.asarray(h3g[f"{tag}_B20_linear_primary"],complex) if nt==128 else None
                if nt==64:
                    # H3G's certified Nt64 output stores weighted z20 and
                    # weighted z10, not X20/B20. Reconstruct X20 from the
                    # corrected H3F Z20 on the exact shared Nt64 grid.
                    z20=np.asarray(h3f[f"{tag}_Z20_control"],complex)
                    X20=old.r24.X20_modes(old.r7,bg,z20)
                    W20=np.asarray(h3g[f"{tag}_weighted_z20_time_control"],complex)
                    B20=X20-W20
                else:
                    z20=np.asarray(h3f[f"{tag}_Z20_primary"],complex)
                    X20=old.r24.X20_modes(old.r7,bg,z20)
                    W20=np.asarray(h3g[f"{tag}_weighted_z20_primary"],complex)
                    if not np.array_equal(B20,X20-W20):
                        raise RuntimeError("H3G certified primary B20 does not match H3F parent")
                wz10=np.asarray(h3g[f"{tag}_weighted_z10_{'primary' if nt==128 else 'time_control'}"],complex)
                if (h1.shape!=(6,6,nt) or dh1.shape!=(6,4,nt)
                    or tangent.shape!=(6,6,nt) or tangent_dot.shape!=(6,4,nt)
                    or B20.shape!=(3,40,nt) or wz10.shape!=(6,nt)):
                    raise RuntimeError(f"H4F3b incorrect certified parent shape {tag} Nt={nt}")
                per_beta,diag=actual_case_source(
                    bg,tag,h1,dh1,tangent,tangent_dot,B20,wz10,
                    qdirect,mod6,mod7,ge05,boundary
                )
                for ib,beta in enumerate(old.r7.BETAS):
                    item=per_beta[ib]
                    name=f"{label}_{tag}_beta{ib}"
                    save[f"{name}_total_rows"]=item["assembled"]["total_rows"]
                    save[f"{name}_source_ward_physical"]=item["physical"]["total_source_ward"]
                    for piece,rows in item["assembled"]["piece_rows"].items():
                        save[f"{name}_{piece}_rows"]=rows
                    controls.append({"Nt":nt,"C":tag,"beta0":float(beta),
                        **diag,
                        "six_piece_sum_max_abs":item["sum_error"],
                        "physical_source_Ward_sum_max_abs":item["clock_sum_error"],
                        "physical_source_Ward_max_abs":float(np.max(
                            np.abs(item["physical"]["total_source_ward"])
                        )),
                        "source_Ward_smallness_NOT_a_gate":True,
                    })
        save["x_primary"]=np.asarray(h3f["x_primary"],float)
        save["x_control"]=np.asarray(h3f["x_control"],float)
    # A source-Ward projection is not constrained to vanish termwise.
    gates={
      "all_exact_source_and_parent_provenance":True,
      "all_C_beta_Nt_cohorts":len(controls)==18,
      "GE06_GE07_direct_cross_symmetry_le_1e12":all(
          q["GE06_GE07_direct_cross_symmetry_relative_L2"]<=1e-12
          for q in controls
      ),
      "Lambda_exact_source_le_1e12":all(
          q["Lambda_direct_vs_exact_relative_L2"]<=1e-12
          and q["Lambda_direct_swap_relative_L2"]<=1e-12
          for q in controls
      ),
      "frozen_R1_q10_reproduced_le_1e10":all(
          q["Repair26_R1_q10_vs_H3G_weighted_z10_relative_L2"]<=1e-10
          for q in controls
      ),
      "six_source_rows_and_physical_Ward_linear":all(
          q["six_piece_sum_max_abs"]<=1e-9
          and q["physical_source_Ward_sum_max_abs"]<=1e-9
          for q in controls
      ),
      "complete_Y_both_rows_no_legacy":all(
          q["actual_StageE_complete_Y_both_rows_used"] is True
          and q["historical_scalar_only_Y_consumed"] is False
          and q["historical_Repair27_q20_consumed"] is False
          for q in controls
      ),
      "all_source_outputs_finite":all(q["all_outputs_finite"] for q in controls),
    }
    passed=all(gates.values())
    result={
       "classification":(
           "GE19_H4F3B_ACTUAL_CORRECTED_SIX_SOURCE_PASS_FULL_WARD_OPEN"
           if passed else
           "GE19_H4F3B_ACTUAL_CORRECTED_SIX_SOURCE_SCIENCE_FAIL"
       ),
       "predata_classification":
           "GE19_H4F3B_PREDATA_ACTUAL_CORRECTED_SIX_PIECE_PHYSICAL_SOURCE",
       "pinned_source_blobs":pinned,"input_sha256":digests,
       "controls":controls,"gates":gates,
       "failure_gates":[k for k,v in gates.items() if not v],
       "full_linear_operator_Ward_evaluated":False,
       "full_signed_parent_Euler_residuals_evaluated":False,
       "full_all_sector_H4_Noether_derived":False,
       "H4_Z21_solve_performed":False,"Z21_certified":False,
       "lensing_licensed":False,
       "next_route":(
           "FREEZE_GENUINE_SOURCES_AND_EVALUATE_OPERATOR_PLUS_ALL_PARENT_WARD"
           if passed else "FREEZE_VALID_ACTUAL_SOURCE_FAILURE_WITHOUT_Z21_SOLVE"
       ),
       "claim_boundary":
           "Action-bound actual six source families on corrected H3F/H3G and certified Z11, physical H*FD8/FD4 source Ward ONLY. Source Ward need not be zero. Missing linear operator and parent Euler terms prohibit full Noether, Z21 and lensing claims."
    }
    outj.parent.mkdir(parents=True,exist_ok=True)
    outj.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+"\n")
    np.savez_compressed(outn,**save)
    print(json.dumps(result,indent=2,sort_keys=True,allow_nan=False))
    if not passed:
        raise SystemExit(2)

if __name__=="__main__":
    main()
