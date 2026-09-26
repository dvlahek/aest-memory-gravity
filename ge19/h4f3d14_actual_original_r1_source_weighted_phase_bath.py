#!/usr/bin/env python3
"""GE19 H4F3d14 actual frozen GE05 source-weighted phase-binned R1 diagnostic.

Rebuild original Repair26 R1 first-order z,v on the original H3F/Repair13
background and compare all source-weighted complex W and raw phases to
exact SHA-locked ORIGINAL D13 NPZ. No bath on-shell, full H4 or Z21 claim.
"""
from __future__ import annotations
import argparse,hashlib,json,subprocess
from pathlib import Path
import numpy as np
from ge19 import h4f3d13_actual_original_r1_signed_interval_bath_parent as d13
from ge19 import h4f3d13_original_r1_interval_signed_bath_assembly as orig
from ge19 import h4f3d14_original_r1_source_weighted_phase_bath_partition as phasepart
from ge19 import h4f3b_actual_corrected_six_piece_source as s

ROOT=Path(__file__).resolve().parents[1]
SHA_D13_JSON="2b4dfbd30ec6466292e0dcf62eeed8b723555d1890a127a5e0a6ff761d2ebe76"
SHA_D13_NPZ="1608fe98dd924b2b235ecf0f8fce768f2f3a2fa4a2854de04a56fe622ad3df89"
PRE="321217d3661bf09fe67f1359606a5296faa4d304"
PHASE="727a8abb63a4aaa314d09e3396d7e2fbeb03bd71"
PINS={
 "ge19/h4f3d14_predata_original_r1_phase_weighted_signed_bath_error.json":PRE,
 "ge19/h4f3d14_original_r1_source_weighted_phase_bath_partition.py":PHASE,
 "ge19/h4f3d13_actual_original_r1_signed_interval_bath_parent.py":
  "5cce06a82869d5b7ff70c12a92e70b9257073c42",
 "ge19/h4f3d13_original_r1_interval_signed_bath_assembly.py":
  "64641d11c34a729508dbfa29d2fe65ccae3a031a",
 "ge19/h4f3d13_actual_original_r1_signed_interval_bath_independent_archive_audit.json":
  "886ac54bd7ad6f802895145fd7776f2ebd6c64d1",
 "ge05/memory_directional_source_generator.py":
  "40837d77f89028da30c28899e2d0530a4401844e"
}
TINY=1e-300

def exact_locks():
    z={}
    for path,want in PINS.items():
        head=subprocess.check_output(
            ["git","rev-parse","HEAD:"+path],cwd=ROOT,text=True).strip()
        current=subprocess.check_output(
            ["git","hash-object",str(ROOT/path)],cwd=ROOT,text=True).strip()
        good=head==current==want
        z[path]={"expected":want,"head":head,"worktree":current,"exact":good}
        if not good:
            raise RuntimeError("D14 changed immutable original source: "+path)
    original=d13.locks()
    return z,original

def compare_original_archive(original,arrays,label,tag,nq):
    prefix=f"{label}_{tag}_Nq{nq}_"
    diffs={}
    whole=arrays["original_FD4_signed_W"]
    prior=np.asarray(original[prefix+"FD4_original_signed_W"],complex)
    diffs["original_sampled_FD4_signed_W"]=orig.rel(whole,prior)
    ph=np.asarray(original[prefix+"left_original_interval_phase"],float)
    if not np.array_equal(arrays["original_interval_phase"],ph):
        raise RuntimeError("D14 original source parent phase changed: "+prefix)
    ph_right=np.asarray(original[prefix+"right_original_interval_phase"],float)
    if not np.array_equal(arrays["original_interval_phase"],ph_right):
        raise RuntimeError("D14 original right phase changed: "+prefix)
    for side,sl in (("left",slice(1,None)),("right",slice(None,-1))):
        for parent,suffix in (("ODE","signed_interval_W"),
                              ("defect","signed_derivative_defect_W")):
            reconstructed=sum(
                (arrays[side+"_"+label_+"_"+parent+"_signed_W"]
                 for label_ in phasepart.LABELS),np.zeros(
                 (len(whole)-1,orig.M_MAX+1),complex))
            frozen=np.asarray(original[prefix+side+"_"+suffix],complex)
            diffs[side+"_"+parent+"_source_parent"]=orig.rel(reconstructed,frozen)
        fd=sum((arrays[side+"_"+label_+"_FD4_signed_W"]
                 for label_ in phasepart.LABELS),
               np.zeros((len(whole)-1,orig.M_MAX+1),complex))
        diffs[side+"_FD4_bins_to_original_D13"]=orig.rel(fd,prior[sl,:])
    if max(diffs.values())>1e-11:
        raise RuntimeError("D14 original D13 phase/Fourier source parent mismatch")
    return diffs

def compare_quadrature(high,low):
    diagnostics={}
    for side in ("left","right"):
        for part in ("ODE","defect","FD4"):
            for label in phasepart.LABELS:
                x=high[side+"_"+label+"_"+part+"_signed_W"]
                y=low[side+"_"+label+"_"+part+"_signed_W"]
                diagnostics[side+"_"+label+"_"+part+"_signed_W"]={
                    "original_absolute_difference_L2_report_only":orig.l2(x-y),
                    "original_relative_difference_report_only":orig.rel(x,y)}
                a=high[side+"_"+label+"_"+part+"_unsigned_envelope"]
                b=low[side+"_"+label+"_"+part+"_unsigned_envelope"]
                diagnostics[side+"_"+label+"_"+part+"_unsigned_envelope"]={
                    "original_absolute_difference_L2_report_only":orig.l2(a-b),
                    "original_relative_difference_report_only":orig.rel(a,b)}
        for suffix in ("original_FD4_signed_W",):
            x=high["original_FD4_signed_W"]
            y=low["original_FD4_signed_W"]
            diagnostics[side+"_"+suffix]={
                "original_absolute_difference_L2_report_only":orig.l2(x-y),
                "original_relative_difference_report_only":orig.rel(x,y)}
    return diagnostics

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--results-dir",required=True)
    parser.add_argument("--repair26-trace",required=True)
    parser.add_argument("--json-out",required=True)
    parser.add_argument("--npz-out",required=True)
    args=parser.parse_args()
    rd=Path(args.results_dir).resolve()
    trace=Path(args.repair26_trace).resolve()
    outj=Path(args.json_out).resolve()
    outn=Path(args.npz_out).resolve()
    if outj.exists() or outn.exists():
        raise RuntimeError("D14 refuses to overwrite prior physical outputs")
    pre=json.loads((ROOT/
      "ge19/h4f3d14_predata_original_r1_phase_weighted_signed_bath_error.json").read_text())
    if pre["classification"]!=(
        "GE19_H4F3D14_PREDATA_ORIGINAL_R1_SIGNED_GE05_SOURCE_WEIGHTED_PHASE_BATH_ERROR_DIAGNOSTIC"):
        raise RuntimeError("D14 preregistration changed")
    pins,old_pins=exact_locks()
    original_paths=d13.original_physical_inputs(rd,trace)
    parents_paths,parents=s.frozen_inputs(rd,trace)
    if not all(parents[k]["exact"] for k in s.REQUIRED):
        raise RuntimeError("D14 frozen H3F/H3G/Z11/Repair13 parents missing")
    previous_j=rd/"ge19_h4f3d13_actual_original_r1_signed_interval_bath_parent.json"
    previous_n=rd/"ge19_h4f3d13_actual_original_r1_signed_interval_bath_parent.npz"
    if (d13.digest(previous_j)!=SHA_D13_JSON
        or d13.digest(previous_n)!=SHA_D13_NPZ):
        raise RuntimeError("D14 original D13 actual physical parent SHA mismatch")
    previous_report=json.loads(previous_j.read_text())
    if (previous_report["classification"]!=
        "GE19_H4F3D13_ACTUAL_ORIGINAL_R1_SIGNED_INTERVAL_BATH_PARENT_DIAGNOSTIC_PASS_ONSHELL_OPEN"
        or len(previous_report["rows"])!=12):
        raise RuntimeError("D14 original D13 physical classification changed")
    save={};rows=[]
    with (np.load(parents_paths["r13"],allow_pickle=False) as r13,
          np.load(parents_paths["h3fn"],allow_pickle=False) as h3f,
          np.load(original_paths["source_n"],allow_pickle=False) as source_npz,
          np.load(previous_n,allow_pickle=False) as previous):
        bg_cases,_,_,_,_,_,_,_,_=d13.old.build_context(rd,r13)
        boundaries={nq:d13.old.r24.full_history_boundary(
            d13.old.c4,d13.old.r7,trace,nq) for nq in (2048,1024)}
        tau=d13.old.r24.TAUH0/float(d13.old.r7.g9.H0_CLASS)
        kfund=float(d13.old.r7.g9.K_REQ[0]/d13.old.r7.FOURIER_N[0])
        for nt,label in ((128,"primary"),(64,"control")):
            x=np.asarray(source_npz["x_"+label],float)
            if not np.array_equal(x,np.asarray(h3f["x_"+label],float)):
                raise RuntimeError("D14 original H3F and source physical clocks differ")
            save["x_"+label]=x
            for tag in d13.old.r7.C_TAGS:
                bg=bg_cases[(nt,tag)]
                if not np.array_equal(x,np.asarray(bg["x"],float)):
                    raise RuntimeError("D14 original Repair13 physical clock changed")
                a=np.asarray(bg["a"],float)
                H=np.asarray(bg["H"],float)
                h1=np.asarray(h3f[f"{tag}_H1_{label}"],complex)
                X=d13.old.r24.first_order_X_modes(d13.old.r7,bg,h1)
                cohorts={}
                for nq in (2048,1024):
                    boundary=boundaries[nq]
                    r=np.asarray(boundary["r"],float)
                    w=np.asarray(boundary["w"],float)
                    z,v=d13.old.r24.evolve_z10(
                        d13.old.c4,bg,X,boundary["z0"],boundary["v0"],r,tau)
                    result,diagnostic=phasepart.phase_partition(
                        z,v,X,a,H,x,r,w,tau,kfund,d13.d6.fd4,
                        d13.d6.ward_signed_convolution)
                    compare=compare_original_archive(previous,result,label,tag,nq)
                    root=f"{label}_{tag}_Nq{nq}_"
                    for key,arr in result.items():
                        save[root+key]=arr
                    rows.append({
                        "C":tag,"Nt":nt,"original_Nq":nq,
                        "original_D13_actual_physical_parent_relative":compare,
                        "original_source_weighted_phase_bins":diagnostic,
                        "original_full_GE05_bath_on_shell_not_certified":True,
                        "full_H4_Noether_not_certified":True,
                        "original_source_retained_no_observation_tuning":True,
                        "pass_machine_only":True})
                    cohorts[nq]=result
                comparison=compare_quadrature(cohorts[2048],cohorts[1024])
                for row in rows[-2:]:
                    row["original_Nq2048_vs_Nq1024_source_weighted_phase_and_total_report_only"]=comparison
    if len(rows)!=12 or any(not np.isfinite(arr).all() for arr in save.values()):
        raise RuntimeError("D14 missing original cohorts or nonfinite signed high-phase archive")
    result={
        "classification":"GE19_H4F3D14_ACTUAL_ORIGINAL_R1_SOURCE_WEIGHTED_PHASE_BATH_DIAGNOSTIC_PASS_ONSHELL_OPEN",
        "preregistration":pre["classification"],
        "original_locked_D13_actual_json_sha256":d13.digest(previous_j),
        "original_locked_D13_actual_npz_sha256":d13.digest(previous_n),
        "original_locked_R1_trace_sha256":d13.digest(trace),
        "original_prior_physical_parent_SHA":{k:d13.digest(p) for k,p in original_paths.items()},
        "source_git_blob_locks":pins,
        "D13_original_source_git_blob_locks":old_pins,
        "original_H3F_H3G_Z11_Repair13_parent_locks":parents,
        "all_twelve_original_C_Nt_Nq_cohorts":True,
        "original_GE05_bath_first_order_on_shell_certified":False,
        "source_weighted_phase_tail_absolute_physical_error_budget_certified":False,
        "original_E00_F21_and_full_action_boundary_evaluated":False,
        "actual_all_sector_H4_Ward_certified":False,
        "Z21_certified":False,"lensing_licensed":False,
        "original_Repair37_SCIENCE_FAIL_immutable":True,
        "rows":rows,
        "claim_boundary":"Actual source-weighted phase-bin signed GE05 interval/FD4 bath parent and conservative noncancelling unsigned envelopes on exact original R1 2048/1024 nodes, source-bound to previous original D13 signed bath output. Original high-phase and cancellation-sensitivity are report-only; no continuous-time bath on-shell error certificate, complete H4 Ward, F21, Z21 or lensing."
    }
    outj.parent.mkdir(parents=True,exist_ok=True)
    outn.parent.mkdir(parents=True,exist_ok=True)
    outj.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+"\n")
    np.savez_compressed(outn,**save)
    print(json.dumps(result,indent=2,sort_keys=True,allow_nan=False))
if __name__=="__main__": main()
