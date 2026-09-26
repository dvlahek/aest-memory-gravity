#!/usr/bin/env python3
"""GE19 D13 actual original Repair26 R1 interval-native signed GE05 bath parent.

Both original one-sided interval ODE Euler residuals are converted into the
exact original signed +/- Fourier parent +4 sum_j E_qj10 dchi q_j10.
Original FD4 sampled bath Ward and derivative defect remain distinct.
NO bath-on-shell smallness gate, full H4 Ward, F21 or Z21 claim.
"""
from __future__ import annotations
import argparse,hashlib,json,subprocess
from pathlib import Path
import numpy as np
from ge19 import h4f3d13_original_r1_interval_signed_bath_assembly as signed
from ge19 import h4f3d7r1_physical_output_finite_check_repair as d7
from ge19 import h4f3d6_actual_normalized_bath_parent_ward as d6
from ge19 import h4f3b_actual_corrected_six_piece_source as s
from ge19 import repair37_cancellation_safe_fd8_h4_z21_reclosure as old

ROOT=Path(__file__).resolve().parents[1]
REG="ec07d6be5c267dcbbdb05395ea81cc5e7405781e"
HELPERS={
"ge19/h4f3d13_predata_original_r1_interval_signed_bath_parent.json":REG,
"ge19/h4f3d13_original_r1_interval_signed_bath_assembly.py":
"64641d11c34a729508dbfa29d2fe65ccae3a031a",
"ge05/memory_directional_source_generator.py":
"40837d77f89028da30c28899e2d0530a4401844e",
"ge19/h4f3d2_dust_bath_parent_euler_currents.py":
"42b2405759402195ffb371056d9e48b70dcded71",
"ge19/h4f3d4_complete_eta_regularized_mixed_ward_ledger.py":
"87d8be9ec44ecb099feecbaf59a904bd989da2fb",
"ge19/h4f3d6_actual_normalized_bath_parent_ward.py":
"0419145499f5f44e06ba0c96f779c2a604e84ce7",
"ge19/h4f3d7_bath_fd4_vs_original_r1_interval_ode.py":
"b598a5cc49b3d87827b4758c55d3ce7f3a1198a8",
"ge19/h4f3d7r1_physical_output_finite_check_repair.py":
"e4cb9d6638b427368647a29b86ccf5445b43d7a2",
"ge19/h4f3b_actual_corrected_six_piece_source.py":
"0423cbc64f6cda3b2a9aeb67c734935ef3ae7f9c",
"ge19/repair24_q20_construction.py":
"fc271987d1bddcd023cc9c057ddcad036b1d72fb",
"ge19/repair37_cancellation_safe_fd8_h4_z21_reclosure.py":
"45d203a092f9ac71cc612b15df5f0c0c630f5898",
"ge19/h4f3d12_freeze_manifest.json":
"b7b8a97ea9e27e6f31a85e7724532bb4dfc4fc4b",
}
D7J="031229d570d29ae9c4ea0ab8e25222d94e9cda4520c991cd203e9d7b97e01dc9"
D7N="4f011c96c2c11165df6332eafc459c5d2c5e7bc5164a436bde3d1563696f0e13"
TRACE_SHA="608ee0b4c868a701db6976f756b9a551cd9ddffe1e8e4ab37c5cd2361405a6f8"
TINY=1e-300

def digest(path:Path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1<<20),b""):
            h.update(block)
    return h.hexdigest()

def locks():
    observed={}
    for path,want in HELPERS.items():
        head=subprocess.check_output(["git","rev-parse","HEAD:"+path],
            cwd=ROOT,text=True).strip()
        work=subprocess.check_output(["git","hash-object",str(ROOT/path)],
            cwd=ROOT,text=True).strip()
        observed[path]={"expected":want,"head":head,"worktree":work,
                        "exact":want==head==work}
        if not observed[path]["exact"]:
            raise RuntimeError("D13 source or immutable prior-stage blob mismatch: "+path)
    if not d7.stepper_ast_exact():
        raise RuntimeError("D13 original R1 Repair24 solver AST mismatch")
    d7.exact_code_lock()
    s.code_lock()
    return observed

def original_physical_inputs(rd,trace):
    expected={
      "source_j":("ge19_h4f3b_actual_corrected_six_piece_source.json",
                  d7.SOURCE_JSON_SHA),
      "source_n":("ge19_h4f3b_actual_corrected_six_piece_source.npz",
                  d7.SOURCE_NPZ_SHA),
      "d6j":("ge19_h4f3d6_actual_normalized_bath_parent_ward.json",
                  d7.D6_JSON_SHA),
      "d6n":("ge19_h4f3d6_actual_normalized_bath_parent_ward.npz",
                  d7.D6_NPZ_SHA),
      "d7j":("ge19_h4f3d7r1_physical_r1_fd4_vs_interval_ode.json",D7J),
      "d7n":("ge19_h4f3d7r1_physical_r1_fd4_vs_interval_ode.npz",D7N),
    }
    result={}
    for key,(filename,sha) in expected.items():
        path=rd/filename
        if not path.is_file() or digest(path)!=sha:
            raise RuntimeError("D13 original actual parent missing or changed: "+filename)
        result[key]=path
    if not trace.is_file() or digest(trace)!=TRACE_SHA or trace.stat().st_size!=26643162:
        raise RuntimeError("D13 original 26,643,162-byte Repair26 R1 trace missing or changed")
    j6=json.loads(result["d6j"].read_text())
    j7=json.loads(result["d7j"].read_text())
    js=json.loads(result["source_j"].read_text())
    if (j6.get("classification")!="GE19_H4F3D6_ACTUAL_BATH_PARENT_WARD_SUBSET_PASS_FULL_OPEN"
        or j7.get("classification")!="GE19_H4F3D7_FD4_INTERVAL_ODE_DISCREPANCY_DECOMPOSED"
        or js.get("classification")!="GE19_H4F3B_ACTUAL_CORRECTED_SIX_SOURCE_PASS_FULL_WARD_OPEN"
        or j7.get("all_diagnostic_gates_pass") is not True
        or len(j7.get("cases",[]))!=6):
        raise RuntimeError("D13 original D6/D7r1/six-source science subset classification changed")
    return result

def original_scope_compare(npz,label,tag,actual):
    prefix=label+"_"+tag+"_"
    diffs={}
    for name,new in (
       ("R_ODE_left_mode_time_L2",actual["left_original_R_ODE_mode_time_L2"]),
       ("R_ODE_right_mode_time_L2",actual["right_original_R_ODE_mode_time_L2"]),
       ("FD4_defect_left_mode_time_L2",actual["left_original_FD4_defect_mode_time_L2"]),
       ("FD4_defect_right_mode_time_L2",actual["right_original_FD4_defect_mode_time_L2"])):
        recorded=np.asarray(npz[prefix+name],float)
        if recorded.shape!=new.shape:
            raise RuntimeError("D13 original D7r1 phase/mode-time archive shape changed: "+name)
        diffs[name]=signed.rel(recorded,new)
    return diffs

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--results-dir",required=True)
    p.add_argument("--repair26-trace",required=True)
    p.add_argument("--json-out",required=True)
    p.add_argument("--npz-out",required=True)
    args=p.parse_args()
    rd=Path(args.results_dir).resolve()
    trace=Path(args.repair26_trace).resolve()
    outj=Path(args.json_out).resolve()
    outn=Path(args.npz_out).resolve()
    if outj.exists() or outn.exists():
        raise RuntimeError("D13 refuses to overwrite original or previous result")
    pre=json.loads((ROOT/"ge19/h4f3d13_predata_original_r1_interval_signed_bath_parent.json").read_text())
    if pre["classification"]!="GE19_H4F3D13_PREDATA_ORIGINAL_R1_ONE_SIDED_INTERVAL_SIGNED_GE05_BATH_PARENT":
        raise RuntimeError("D13 preregistration changed")
    pins=locks()
    paths=original_physical_inputs(rd,trace)
    original_paths,parents=s.frozen_inputs(rd,trace)
    if not all(parents[k]["exact"] for k in s.REQUIRED):
        raise RuntimeError("D13 original H3F/H3G/Z11/Repair13 parents changed")
    save={};rows=[]
    with (np.load(original_paths["r13"],allow_pickle=False) as r13,
          np.load(original_paths["h3fn"],allow_pickle=False) as h3f,
          np.load(original_paths["h3gn"],allow_pickle=False) as h3g,
          np.load(paths["source_n"],allow_pickle=False) as source_archive,
          np.load(paths["d6n"],allow_pickle=False) as d6_archive,
          np.load(paths["d7n"],allow_pickle=False) as d7_archive):
        bgs,_,_,_,_,_,_,_,_=old.build_context(rd,r13)
        boundaries={Nq:old.r24.full_history_boundary(
            old.c4,old.r7,trace,Nq) for Nq in (2048,1024)}
        tau=old.r24.TAUH0/float(old.r7.g9.H0_CLASS)
        kfund=float(old.r7.g9.K_REQ[0]/old.r7.FOURIER_N[0])
        results_by_scope={}
        for nt,label in ((128,"primary"),(64,"control")):
            xx=np.asarray(source_archive["x_"+label],float)
            if xx.shape!=(nt,) or not np.array_equal(
                xx,np.asarray(h3f["x_"+label],float)):
                raise RuntimeError("D13 original certified H3F clock mismatch")
            save["x_"+label]=xx
            for tag in old.r7.C_TAGS:
                bg=bgs[(nt,tag)]
                if not np.array_equal(xx,np.asarray(bg["x"],float)):
                    raise RuntimeError("D13 original Repair13 clock mismatch")
                H=np.asarray(bg["H"],float)
                a=np.asarray(bg["a"],float)
                h1=np.asarray(h3f[f"{tag}_H1_{label}"],complex)
                X10=old.r24.first_order_X_modes(old.r7,bg,h1)
                scope={}
                for nq in (2048,1024):
                    boundary=boundaries[nq]
                    rr=np.asarray(boundary["r"],float)
                    w=np.asarray(boundary["w"],float)
                    if len(rr)!=nq or len(w)!=nq:
                        raise RuntimeError("D13 original quadrature node count changed")
                    z,v=old.r24.evolve_z10(
                        old.c4,bg,X10,boundary["z0"],boundary["v0"],rr,tau
                    )
                    actual,diagnostic=signed.interval_signed(
                        z,v,X10,a,H,xx,rr,w,tau,kfund,
                        d6.fd4,d6.ward_signed_convolution)
                    keys=f"{label}_{tag}_Nq{nq}"
                    for name,arr in actual.items():
                        save[keys+"_"+name]=arr
                    extra={"original_Nq":nq,
                      "C":tag,"Nt":nt,"original_six_modes":list(map(int,signed.MODES)),
                      "both_one_sided_interval_ODE_Euler":diagnostic,
                      "no_new_GE05_on_shell_smallness_gate":True,
                      "full_H4_Noether_not_certified":True}
                    tests=[
                       diagnostic[side][metric]
                       for side in ("left","right")
                       for metric in (
                        "original_ODE_unsimplified_vs_explicit_interval_H_relative_natural",
                        "original_FD4_equals_interval_ODE_plus_derivative_defect_relative_natural",
                        "original_signed_FD4_equals_interval_plus_defect_relative_natural")]
                    extra["max_original_exact_ODE_FD4_signed_assembly_relative"]=max(tests)
                    if nq==2048:
                        saved_H3G=np.asarray(h3g[
                            f"{tag}_weighted_z10_{'primary' if nt==128 else 'time_control'}"],complex)
                        reproduced=np.einsum("b,bmt->mt",w,z,optimize=True)
                        extra["original_H3G_weighted_z10_relative_reproduction"]=signed.rel(saved_H3G,reproduced)
                        previous=np.asarray(d6_archive[
                            f"{label}_{tag}_bath_parent_ward_physical"],complex)
                        extra["original_D6_signed_FD4_W_relative_reproduction"]=signed.rel(
                            previous,actual["FD4_original_signed_W"])
                        extra["original_D7r1_mode_time_norm_relative_reproduction"]=original_scope_compare(
                            d7_archive,label,tag,actual)
                        original_d7=max(extra["original_D7r1_mode_time_norm_relative_reproduction"].values())
                        parent_ok=(extra["original_H3G_weighted_z10_relative_reproduction"]<=1e-10
                          and extra["original_D6_signed_FD4_W_relative_reproduction"]<=1e-10
                          and original_d7<=1e-10)
                    else:
                        parent_ok=True
                    extra["original_existing_assembly_identity_le_1e11"]=(max(tests)<=1e-11)
                    extra["original_parent_archive_reproduction_unchanged"]=bool(parent_ok)
                    extra["pass_machine_only"]=bool(parent_ok and max(tests)<=1e-11)
                    scope[nq]=actual
                    rows.append(extra)
                prev=scope[2048];control=scope[1024]
                for side in ("left","right"):
                    key=side+"_signed_interval_W"
                    scale=max(signed.l2(prev[key]),signed.l2(control[key]),signed.TINY)
                    for row in rows[-2:]:
                        row["Nq2048_vs_Nq1024_"+side+"_signed_interval_W_relative_report_only"]=(
                            signed.l2(prev[key]-control[key])/scale)
        if len(rows)!=12 or not all(row["pass_machine_only"] for row in rows):
            raise RuntimeError("D13 original physical signed bath implementation/parent regression unresolved")
        if any(not np.isfinite(arr).all() for arr in save.values()):
            raise RuntimeError("D13 nonfinite signed interval bath archive")
    result={
     "classification":"GE19_H4F3D13_ACTUAL_ORIGINAL_R1_SIGNED_INTERVAL_BATH_PARENT_DIAGNOSTIC_PASS_ONSHELL_OPEN",
     "preregistered_classification":pre["classification"],
     "exact_source_code_blobs":pins,
     "original_input_sha256":{k:digest(path) for k,path in paths.items()},
     "original_Repair26_R1_trace_sha256":digest(trace),
     "original_certified_parent_hashes":parents,
     "all_six_C_Nt_Nq2048_and_Nq1024_actual_cohorts_saved":len(rows)==12,
     "rows":rows,
     "original_GE05_bath_first_order_on_shell_certified":False,
     "original_H4F3d7r1_diag_does_not_imply_onshell":True,
     "actual_full_all_sector_H4_Noether_certified":False,
     "actual_E00_F21_and_full_action_boundary_evaluated":False,
     "Z21_certified":False,"lensing_licensed":False,
     "original_Repair37_SCIENCE_FAIL_immutable":True,
     "claim_boundary":"Physical original R1 2048-node and separate 1024-node quadrature, both true one-sided interval ODE and separately retained original sampled FD4 GE05 signed +4 Eq10*dchi q10 bath parent. Exact signed convolution/mode-time parent reproduction is a machine identity only. Original phase and original FD4/ODE defects are retained; no bath-on-shell error budget, no full H4 Noether, Z21 or lensing claim."
    }
    outj.parent.mkdir(parents=True,exist_ok=True)
    outn.parent.mkdir(parents=True,exist_ok=True)
    outj.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+"\n")
    np.savez_compressed(outn,**save)
    print(json.dumps(result,indent=2,sort_keys=True,allow_nan=False))
if __name__=="__main__":
    main()
