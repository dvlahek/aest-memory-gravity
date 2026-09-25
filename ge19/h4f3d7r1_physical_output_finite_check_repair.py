#!/usr/bin/env python3
"""GE19 H4F3d7: original R1 interval ODE versus sampled FD4 GE05 bath Euler.

No change to the frozen Repair24 propagator, R1 history, GE05 action,
H3F/H3G parents or H4 source. A manufactured test runs on Actions;
the PHYSICAL branch requires hash-locked user-local H4F3b and H4F3d6
results. Neither branch certifies full all-sector H4 Ward or Z21.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import math
import subprocess
from pathlib import Path

import numpy as np

from ge19 import h4f3d6_actual_normalized_bath_parent_ward as d6
from ge19 import repair24_q20_construction as frozen24

ROOT=Path(__file__).resolve().parents[1]
TINY=1e-300
PRE_BLOB="ccf3185b4f790d9d6068f80beb39a442b186158c"
PINNED={
    "ge19/h4f3d7_predata_bath_fd4_vs_original_r1_interval_ode.json":PRE_BLOB,
    "ge19/h4f3d6_actual_normalized_bath_parent_ward.py":
        "0419145499f5f44e06ba0c96f779c2a604e84ce7",
    "ge19/repair24_q20_construction.py":
        "fc271987d1bddcd023cc9c057ddcad036b1d72fb",
    "ge19/h4f3b_actual_corrected_six_piece_source.py":
        "0423cbc64f6cda3b2a9aeb67c734935ef3ae7f9c",
    "docs/ge19_h4f3d6_valid_local_actual_bath_parent_ward_subset_freeze.md":
        "a78dee66657a1c9fddb952d29a1084a9f48ce3ea",
}
SOURCE_JSON_SHA="1ec88fd3fd6b81bf30614b0cb78d722a02dd4f745e1f22cb9b8f956a44bac6c1"
SOURCE_NPZ_SHA="787d5d177838b05078057aa932f379dd529449ce203f5664c36cf723acb0116b"
D6_JSON_SHA="4607edde17c6820c85f32c0bbd774d5a58148eb01bfd0c81ce592e8c1b907791"
D6_NPZ_SHA="17b50c6ee584b2a8886f7114a90ea9396a127172dd9e02976b0e6275fe2fedc0"
PHASE_BINS=(0.0,0.25,0.5,1.0,float("inf"))
PHASE_NAMES=("lt_0p25","0p25_to_0p5","0p5_to_1","ge_1")

def sha256(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as file:
        for block in iter(lambda:file.read(1<<20),b""):
            h.update(block)
    return h.hexdigest()

def exact_code_lock():
    out={}
    for rel,expected in PINNED.items():
        observed=subprocess.check_output(
            ["git","rev-parse","HEAD:"+rel],cwd=ROOT,text=True
        ).strip()
        out[rel]={"expected":expected,"observed":observed,
                  "exact":observed==expected}
    if not all(row["exact"] for row in out.values()):
        raise RuntimeError("H4F3d7 frozen predata/physical code blob changed")
    return out

def stepper_ast_exact():
    """The production stepper must be the original tracked Repair24 AST."""
    original=ast.parse((ROOT/"ge19/repair24_q20_construction.py").read_text())
    function=[n for n in original.body
              if isinstance(n,ast.FunctionDef) and n.name=="step_linear_nd"]
    if len(function)!=1:
        raise RuntimeError("frozen Repair24 step_linear_nd missing/duplicated")
    # This is the actual callable imported directly from the exact frozen
    # file, not a reimplemented alternative or an outcome-dependent ODE.
    import inspect
    observed=ast.parse(inspect.getsource(frozen24.step_linear_nd)).body[0]
    if ast.dump(function[0],include_attributes=False)!=ast.dump(
        observed,include_attributes=False
    ):
        raise RuntimeError("imported Repair24 stepper AST mismatch")
    return True

def rel_l2(a,b):
    aa=np.asarray(a);bb=np.asarray(b)
    return float(np.linalg.norm(aa-bb)/
        max(np.linalg.norm(aa),np.linalg.norm(bb),TINY))

def l2(arr):
    return float(np.linalg.norm(arr))

def phase_stats(left,right,phase):
    """Every original node/interval is assigned to exactly one fixed bin.

    left and right are [node,positive_mode,interval]. The left value
    belongs to its right endpoint, the right value to its left endpoint.
    No high-frequency node is excluded or pooled into a selected subset.
    """
    if left.shape!=right.shape or left.shape[0]!=phase.shape[0] or left.shape[-1]!=phase.shape[1]:
        raise ValueError("H4F3d7 phase bins and interval arrays misaligned")
    parts={}
    assigned=0
    for name,lo,hi in zip(PHASE_NAMES,PHASE_BINS[:-1],PHASE_BINS[1:]):
        mask=(phase>=lo)&(phase<hi)
        assigned+=int(np.count_nonzero(mask))
        parts[name]={
            "node_interval_count":int(np.count_nonzero(mask)),
            "physical_complex_mode_sample_count":int(np.count_nonzero(mask)*left.shape[1]),
            "left_interval_ODE_L2":float(np.sqrt(np.sum(
                np.abs(left)**2*mask[:,None,:]))),
            "right_interval_ODE_L2":float(np.sqrt(np.sum(
                np.abs(right)**2*mask[:,None,:]))),
            "phase_min_in_bin":float(np.min(phase[mask])) if np.any(mask) else None,
            "phase_max_in_bin":float(np.max(phase[mask])) if np.any(mask) else None,
        }
    return parts,assigned==int(phase.size)

def decompose(z,v,X,a,H,x,r,w,tau):
    """Exact frozen step's BOTH one-sided currents versus existing FD4.

    For step i, r24 solves dz/ds=v; dv/ds=-3 h_mid v-r^2(z-X)
    with s=t/tau, h_mid=tau sqrt(H_i H_i+1), and X linear on
    the step. At each shared interior node report BOTH original
    adjacent h_mid values, not their average or best residual.
    """
    euler,Rfd,original=d6.normalized_bath_euler(
        z,v,X,a,H,x,r,w,tau
    )
    xx=np.asarray(x,float);aa=np.asarray(a,float)
    hh=np.asarray(H,float);rr=np.asarray(r,float)
    zz=np.asarray(z,complex);vv=np.asarray(v,complex)
    xxdrive=np.asarray(X,complex)
    nn=len(xx)
    if nn not in (64,128) and nn<9:
        raise ValueError("invalid original FD4 time grid")
    if not np.array_equal(np.asarray(d6.MODES),np.asarray([3,5,8,10,15,20])):
        raise RuntimeError("changed original positive mode scope")
    hmid=np.sqrt(hh[:-1]*hh[1:])
    hgrid=tau*hmid
    dx=np.diff(xx)
    phase=rr[:,None]*dx[None,:]/hgrid[None,:]
    a3=aa[None,None,:]**3
    rr2=rr[:,None,None]**2
    wwpot=a3*(rr[:,None,None]/tau)**2*(zz-xxdrive[None,:,:])
    current=a3*vv/tau
    sampled_kinetic=hh[None,None,:]*d6.fd4(current,xx)
    if not np.all(np.isfinite(phase)) or not np.all(phase>=0):
        raise ValueError("invalid physical bath phase bins")

    # Each interior time sample receives two independently defined
    # one-sided original interval derivatives, plus boundary-side only.
    # The original R1 step uses the geometric-mean h_mid on EACH interval.
    def side(velocity,state,drive,anode,Hnode,hinterval,kfd):
        jt=(3*Hnode[None,None,:]*anode*velocity/tau
            +anode*(-3*hinterval[None,None,:]*velocity
                    -rr2*(state-drive[None,:,:]))/tau**2)
        pot=anode*(rr[:,None,None]/tau)**2*(state-drive[None,:,:])
        r_ode=jt+pot
        r_ode_explicit=3*anode*(
            Hnode[None,None,:]-hinterval[None,None,:]/tau
        )*velocity/tau
        derivative_defect=kfd-jt
        return jt,r_ode,r_ode_explicit,derivative_defect

    left=side(vv[:,:,1:],zz[:,:,1:],xxdrive[:,1:],a3[:,:,1:],
              hh[1:],hgrid,sampled_kinetic[:,:,1:])
    right=side(vv[:,:,:-1],zz[:,:,:-1],xxdrive[:,:-1],a3[:,:,:-1],
               hh[:-1],hgrid,sampled_kinetic[:,:,:-1])
    l_jt,l_ode,l_exp,l_def=left
    r_jt,r_ode,r_exp,r_def=right
    natural=float(original["R_z10_absolute_L2"]/max(
        original["R_z10_relative_natural_L2_report_only"],TINY
    )) if original["R_z10_relative_natural_L2_report_only"]>TINY else (
        l2(sampled_kinetic)+l2(wwpot))
    natural=max(natural,TINY)
    # Explicit natural is the registered original norm ||kinetic||+||potential||.
    natural_explicit=l2(sampled_kinetic)+l2(wwpot)
    natural_scale=max(natural_explicit,TINY)
    identities={
        "left_frozen_step_ODE_equals_explicit_interval_H":
            l2(l_ode-l_exp)/natural_scale,
        "right_frozen_step_ODE_equals_explicit_interval_H":
            l2(r_ode-r_exp)/natural_scale,
        "left_FD4_equals_original_ODE_plus_sampled_derivative_defect":
            l2(Rfd[:,:,1:]-l_ode-l_def)/natural_scale,
        "right_FD4_equals_original_ODE_plus_sampled_derivative_defect":
            l2(Rfd[:,:,:-1]-r_ode-r_def)/natural_scale,
        "FD4_original_natural_norm_identity":
            abs(natural-natural_explicit)/natural_scale,
    }
    bins_l,all_l=phase_stats(l_ode,r_ode,phase)
    bins_d,all_d=phase_stats(l_def,r_def,phase)
    summary={
        "R_FD4_absolute_L2":l2(Rfd),
        "R_FD4_relative_original_natural_report_only":
            float(original["R_z10_relative_natural_L2_report_only"]),
        "original_natural_scale":float(natural_explicit),
        "original_sampled_kinetic_L2":l2(sampled_kinetic),
        "original_potential_L2":l2(wwpot),
        "left_original_interval_ODE_L2_all_available_nodes":l2(l_ode),
        "right_original_interval_ODE_L2_all_available_nodes":l2(r_ode),
        "left_FD4_minus_original_ODE_derivative_L2":l2(l_def),
        "right_FD4_minus_original_ODE_derivative_L2":l2(r_def),
        "left_original_ODE_L2_interior":l2(l_ode[:,:,:-1]),
        "right_original_ODE_L2_interior":l2(r_ode[:,:,1:]),
        "left_FD4_defect_L2_interior":l2(l_def[:,:,:-1]),
        "right_FD4_defect_L2_interior":l2(r_def[:,:,1:]),
        "initial_node_right_interval_ODE_L2":l2(r_ode[:,:,0]),
        "final_node_left_interval_ODE_L2":l2(l_ode[:,:,-1]),
        "phase_bin_original_interval_ODE":bins_l,
        "phase_bin_sampled_FD4_defect":bins_d,
        "all_node_intervals_in_predeclared_phase_bins":bool(all_l and all_d),
        "phase_nodes_per_interval":int(phase.shape[0]),
        "phase_interval_count":int(phase.shape[1]),
        "positive_mode_count":int(zz.shape[1]),
        "all_outputs_finite":bool(
            all(np.isfinite(v).all() for v in
                (Rfd,l_ode,r_ode,l_exp,r_exp,l_def,r_def,current,
                 sampled_kinetic,wwpot,phase))
        ),
    }
    outputs={
        "R_FD4_mode_time_L2":np.linalg.norm(Rfd,axis=0),
        "R_ODE_left_mode_time_L2":np.linalg.norm(l_ode,axis=0),
        "R_ODE_right_mode_time_L2":np.linalg.norm(r_ode,axis=0),
        "FD4_defect_left_mode_time_L2":np.linalg.norm(l_def,axis=0),
        "FD4_defect_right_mode_time_L2":np.linalg.norm(r_def,axis=0),
        "phase_bin_node_interval_counts":np.array(
            [bins_l[n]["node_interval_count"] for n in PHASE_NAMES],int),
    }
    return summary,identities,outputs

def manufactured_case(nt):
    """Independent physical-clock variable-H fixture evolved by ORIGINAL stepper."""
    rng=np.random.default_rng(107+nt)
    r=np.array([.2,12.0,180.0,720.0,2700.0],float)
    w=np.ones_like(r)/r.size
    tau=8.0
    x=np.linspace(math.log(.4),math.log(.87),nt)
    a=np.exp(x)
    H=.63+.09*np.sin(np.linspace(0,1.3,nt))
    modes=d6.MODES.astype(float)
    drive=(.005+.001j)*(1+.1*modes[:,None])*np.exp(
        .2j*modes[:,None]*x[None,:]
    )
    z=np.empty((r.size,modes.size,nt),complex)
    v=np.empty_like(z)
    z[:,:,0]=rng.normal(size=z[:,:,0].shape)*1e-3
    v[:,:,0]=rng.normal(size=v[:,:,0].shape)*1e-3
    for i in range(nt-1):
        hmid=tau*math.sqrt(H[i]*H[i+1])
        dxi=(x[i+1]-x[i])/hmid
        z[:,:,i+1],v[:,:,i+1]=frozen24.step_linear_nd(
            z[:,:,i],v[:,:,i],r,hmid,
            np.broadcast_to(drive[:,i],z[:,:,i].shape),
            np.broadcast_to(drive[:,i+1],z[:,:,i].shape),
            dxi
        )
    summary,identity,arrays=decompose(z,v,drive,a,H,x,r,w,tau)
    nonzero=bool(summary["R_FD4_absolute_L2"]>0
        and summary["left_FD4_minus_original_ODE_derivative_L2"]>0
        and summary["right_FD4_minus_original_ODE_derivative_L2"]>0
        and summary["left_original_interval_ODE_L2_all_available_nodes"]>0
        and summary["right_original_interval_ODE_L2_all_available_nodes"]>0)
    passed=(nonzero and all(v<=1e-11 for v in identity.values())
            and summary["all_node_intervals_in_predeclared_phase_bins"]
            and summary["all_outputs_finite"]
            and all(np.isfinite(v).all() for v in arrays.values()))
    return {
        "Nt":nt,"identity_relative_natural":identity,
        "report_only_components":summary,
        "all_phase_bins_preserved":True,
        "nonzero_negative_controls":nonzero,
        "pass":bool(passed),
    }

def manufactured_run(json_out):
    blobs=exact_code_lock()
    step=stepper_ast_exact()
    cases=[manufactured_case(nt) for nt in (64,128)]
    passed=bool(step and all(x["pass"] for x in cases))
    report={
        "classification":(
            "GE19_H4F3D7_FROZEN_ODE_FD4_COMPILER_PASS_PHYSICAL_OPEN"
            if passed else "GE19_H4F3D7_FROZEN_ODE_FD4_COMPILER_FAIL"
        ),
        "predata_classification":
            "GE19_H4F3D7_PREDATA_PHYSICAL_BATH_FD4_VERSUS_FROZEN_R1_INTERVAL_ODE",
        "frozen_blobs":blobs,
        "original_Repair24_stepper_AST_exact":step,
        "manufactured_cases":cases,
        "all_compiler_gates_pass":passed,
        "actual_physical_parent_evaluated":False,
        "full_all_sector_H4_Noether_certified":False,
        "Z21_certified":False,
        "lensing_licensed":False,
        "next_route":(
            "RUN_HASH_LOCKED_ORIGINAL_R1_ACTUAL_GRID_DIAGNOSTIC"
            if passed else "FREEZE_D7_COMPILER_FAILURE"
        ),
    }
    path=Path(json_out);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print(json.dumps(report,indent=2,sort_keys=True,allow_nan=False))
    if not passed:raise SystemExit(3)

def physical_run(args):
    """Original certified H4F3b/d6 local files, no invented or fitted fields."""
    # Historical GE19 modules can have module-level result-writing
    # generators. Caller MUST run with isolated CWD and absolute outputs.
    from ge19 import h4f3b_actual_corrected_six_piece_source as s
    from ge19 import repair37_cancellation_safe_fd8_h4_z21_reclosure as old
    rd=Path(args.results_dir).resolve()
    source_json=Path(args.source_json).resolve()
    source_npz=Path(args.source_npz).resolve()
    d6_json=Path(args.d6_json).resolve()
    d6_npz=Path(args.d6_npz).resolve()
    trace=Path(args.repair26_trace).resolve()
    needed=(
        (source_json,SOURCE_JSON_SHA),(source_npz,SOURCE_NPZ_SHA),
        (d6_json,D6_JSON_SHA),(d6_npz,D6_NPZ_SHA),
        (trace,"608ee0b4c868a701db6976f756b9a551cd9ddffe1e8e4ab37c5cd2361405a6f8")
    )
    for path,expected in needed:
        if not path.is_file() or sha256(path)!=expected:
            raise RuntimeError(f"H4F3d7 frozen actual file unavailable or changed: {path}")
    if trace.stat().st_size!=26643162:
        raise RuntimeError("changed original Repair26 R1 trace length")
    blobs=exact_code_lock()
    if not stepper_ast_exact():
        raise RuntimeError("original stepper AST mismatch")
    s.code_lock()
    files,parents=s.frozen_inputs(rd,trace)
    frozen_d6=json.loads(d6_json.read_text())
    source=json.loads(source_json.read_text())
    if (frozen_d6.get("classification")!=
        "GE19_H4F3D6_ACTUAL_BATH_PARENT_WARD_SUBSET_PASS_FULL_OPEN"
        or not frozen_d6.get("gates")
        or not all(v is True for v in frozen_d6["gates"].values())
        or source.get("classification")!=
        "GE19_H4F3B_ACTUAL_CORRECTED_SIX_SOURCE_PASS_FULL_WARD_OPEN"):
        raise RuntimeError("source or bath parent science subset not frozen PASS")
    if not all(source.get("gates",{}).values()):
        raise RuntimeError("actual H4F3b source gate changed")
    report_cases=frozen_d6["cases"]
    if len(report_cases)!=18:
        raise RuntimeError("H4F3d6 case count no longer exact")
    outputs={}
    cases=[]
    with (np.load(files["r13"],allow_pickle=False) as r13,
          np.load(files["h3fn"],allow_pickle=False) as h3f,
          np.load(files["h3gn"],allow_pickle=False) as h3g,
          np.load(files["z11"],allow_pickle=False) as z11,
          np.load(source_npz,allow_pickle=False) as six,
          np.load(d6_npz,allow_pickle=False) as d6saved):
        bgs,_,_,_,_,_,_,_,_=old.build_context(rd,r13)
        boundary=old.r24.full_history_boundary(
            old.c4,old.r7,trace,2048
        )
        r=np.asarray(boundary["r"],float)
        w=np.asarray(boundary["w"],float)
        tau=old.r24.TAUH0/float(old.r7.g9.H0_CLASS)
        for nt,label in ((128,"primary"),(64,"control")):
            x=np.asarray(six["x_"+label],float)
            for tag in old.r7.C_TAGS:
                bg=bgs[(nt,tag)]
                if not np.array_equal(x,np.asarray(bg["x"],float)):
                    raise RuntimeError("original H4F3b and R13 grid mismatch")
                for parent in (h3f,h3g,z11,d6saved):
                    if not np.array_equal(x,np.asarray(
                        parent["x_"+label],float)):
                        raise RuntimeError("H4F3d7 actual parent clock/grid mismatch")
                h1=np.asarray(h3f[f"{tag}_H1_{label}"],complex)
                X10=old.r24.first_order_X_modes(old.r7,bg,h1)
                z10,v10=old.r24.evolve_z10(
                    old.c4,bg,X10,boundary["z0"],
                    boundary["v0"],r,tau
                )
                oldw=np.asarray(h3g[
                    f"{tag}_weighted_z10_{'primary' if nt==128 else 'time_control'}"
                ],complex)
                r1_rel=rel_l2(np.einsum("b,bmt->mt",w,z10,optimize=True),oldw)
                summary,identity,stored=decompose(
                    z10,v10,X10,np.asarray(bg["a"],float),
                    np.asarray(bg["H"],float),x,r,w,tau
                )
                matching=[entry for entry in report_cases
                    if entry["C"]==tag and entry["Nt"]==nt]
                if len(matching)!=3:
                    raise RuntimeError("H4F3d6 beta-duplicate count changed")
                measured=summary["R_FD4_absolute_L2"]
                report_repro=max(
                    abs(measured-item["normalized_bath_Euler"]["R_z10_absolute_L2"])/
                    max(measured,
                        abs(item["normalized_bath_Euler"]["R_z10_absolute_L2"]),TINY)
                    for item in matching
                )
                old_ward=np.asarray(d6saved[
                    f"{label}_{tag}_bath_parent_ward_physical"],complex)
                if old_ward.shape!=(nt,41) or not np.isfinite(old_ward).all():
                    raise RuntimeError("H4F3d6 saved bath Ward array invalid")
                key=f"{label}_{tag}"
                for name,arr in stored.items():
                    outputs[f"{key}_{name}"]=arr
                outputs[f"{key}_x"]=x
                one_ok=(all(val<=1e-11 for val in identity.values())
                    and summary["all_node_intervals_in_predeclared_phase_bins"])
                cases.append({
                    "C":tag,"Nt":nt,"Nq":len(r),
                    "original_R1_weighted_z10_relative_L2":r1_rel,
                    "original_H4F3d6_R_FD4_absolute_norm_relative_reproduction":
                        report_repro,
                    "FD4_vs_original_ODE_exact_identity":identity,
                    "components_report_only":summary,
                    "both_one_sided_interior_reported":True,
                    "all_original_frequency_nodes_and_modes_included":True,
                    "no_new_on_shell_smallness_gate":True,
                    "pass":bool(one_ok and r1_rel<=1e-10
                          and report_repro<=1e-10
                          and summary["all_outputs_finite"]),
                })
        outputs["x_primary"]=np.asarray(six["x_primary"],float)
        outputs["x_control"]=np.asarray(six["x_control"],float)
    valid=bool(len(cases)==6 and all(v["pass"] for v in cases)
               and all(np.isfinite(arr).all()
                       for arr in outputs.values()))
    report={
        "classification":(
            "GE19_H4F3D7_FD4_INTERVAL_ODE_DISCREPANCY_DECOMPOSED"
            if valid else
            "GE19_H4F3D7_FROZEN_PARENT_OR_DISCRETIZATION_UNRESOLVED"
        ),
        "predata_classification":
            "GE19_H4F3D7_PREDATA_PHYSICAL_BATH_FD4_VERSUS_FROZEN_R1_INTERVAL_ODE",
        "input_hashes":{str(p.name):sha256(p) for p,_ in needed},
        "certified_parent_hashes":parents,
        "source_blobs":blobs,
        "original_Repair24_stepper_AST_exact":True,
        "cases":cases,
        "all_six_original_C_Nt_cases_complete":len(cases)==6,
        "beta_cohort_note":"bath Euler beta-independent; 3 saved beta entries in H4F3d6 are duplicated views, not 18 independent bath paths",
        "all_diagnostic_gates_pass":valid,
        "original_FD4_and_R1_ODE_unchanged":True,
        "new_bath_on_shell_smallness_gate_introduced":False,
        "full_all_sector_H4_Noether_certified":False,
        "Z21_certified":False,
        "lensing_licensed":False,
        "next_route":(
            "FREEZE_PHYSICAL_R1_ODE_VS_SAMPLED_FD4_DEFECT_THEN_NONBATH_FULL_WARD"
            if valid else "FREEZE_AND_LOCALIZE_PHYSICAL_D7_FAILURE"
        ),
        "claim_boundary":"Physical diagnostic decomposition of original R1 interval-H vs sampled FD4 GE05 bath Euler only; nonbath parents/boundary/operator not evaluated; no full Noether or H4/Z21 science claim.",
    }
    path=Path(args.json_out).resolve()
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+"\n")
    np.savez_compressed(Path(args.npz_out).resolve(),**outputs)
    print(json.dumps(report,indent=2,sort_keys=True,allow_nan=False))
    if not valid:raise SystemExit(2)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--manufactured",action="store_true")
    ap.add_argument("--results-dir")
    ap.add_argument("--repair26-trace")
    ap.add_argument("--source-json")
    ap.add_argument("--source-npz")
    ap.add_argument("--d6-json")
    ap.add_argument("--d6-npz")
    ap.add_argument("--json-out",required=True)
    ap.add_argument("--npz-out")
    args=ap.parse_args()
    if args.manufactured:
        if args.npz_out:
            ap.error("--manufactured does not produce a physical NPZ")
        manufactured_run(args.json_out)
    else:
        required=(args.results_dir,args.repair26_trace,args.source_json,
                  args.source_npz,args.d6_json,args.d6_npz,args.npz_out)
        if not all(required):
            ap.error("physical d7 requires all certified source/parent paths and --npz-out")
        physical_run(args)

if __name__=="__main__":
    main()
