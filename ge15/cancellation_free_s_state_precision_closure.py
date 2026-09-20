#!/usr/bin/env python3
"""GE15 cancellation-free s-state R1/R2 precision-closure test.

The CLASS runtime has already been patched so the legacy alpha state slot
internally carries s=chi/Q. Diagnostic traces expose physical alpha, therefore
the frozen GE09/GE11 local-jet dictionary remains unchanged.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import subprocess
import sys
import hashlib
from pathlib import Path

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

import ge09.repair01_dense_accepted_step_local_jet_bridge as g9
import v063.theory_response_map as v63

LEVELS={
    "R1": ROOT/"ge11"/"pre"/"R1_repair01.pre",
    "R2": ROOT/"ge11"/"pre"/"R2_repair01.pre",
}
HIST_N=[17,17,20,20,22,30]
HIST_GAPS=np.asarray([
    0.043892916349146716,0.04748747310334933,0.04502616770712542,
    0.04425855292928327,0.037237892493284463,0.03764573147119232
],float)

def run_level(class_root:Path,tag:str,pre:Path):
    dense=ROOT/"results"/f"ge15_{tag}_dense_accepted_step_trace.dat"
    source=ROOT/"results"/f"ge15_{tag}_source_state_trace.dat"
    prefix=ROOT/"results"/f"ge15_{tag}_cli"
    log=ROOT/"results"/f"ge15_{tag}_class.log"
    for p in (dense,source,log):
        if p.exists(): p.unlink()
    for i in range(len(g9.K_REQ)):
        p=Path(str(prefix)+f"_perturbations_k{i}_s.dat")
        if p.exists(): p.unlink()

    ini=class_root/f"ge15_{tag}.ini"
    text=v63.rewrite_ini(v63.BASE.read_text(),str(prefix))
    text=text.replace("lensing = yes","lensing = no")
    text += "k_output_values = " + ", ".join(f"{k:.17g}" for k in g9.K_REQ) + "\n"
    ini.write_text(text)

    env=os.environ.copy()
    env["AEST_DENSE_JET_TRACE_FILE"]=str(dense.resolve())
    env["AEST_FULL_STATE_TRACE_FILE"]=str(source.resolve())
    env.pop("AEST_OFFLINE_TRACE_FILE",None)
    env.pop("AEST_TANGENT_FORCE_FILE",None)
    env.pop("AEST_TANGENT_LAMBDA",None)
    env["OMP_NUM_THREADS"]="1"

    with log.open("w") as fh:
        subprocess.run(
            [str(class_root/"class"),ini.name,str(pre)],
            cwd=class_root,env=env,stdout=fh,stderr=subprocess.STDOUT,check=True
        )

    pt=[
        g9.read_class_perturbation(Path(str(prefix)+f"_perturbations_k{i}_s.dat"))
        for i in range(len(g9.K_REQ))
    ]
    dense_rows=g9.read_table(dense)
    source_rows=g9.read_table(source)
    modes,kmiss=g9.group_modes(dense_rows)
    class_err,class_counts=g9.class_trace_control(modes,pt)

    nwin=[]; gaps=[]; primary=[]; control=[]
    for m in modes:
        inwin=[r for r in m if g9.AMIN-1e-14<=r["a"]<=g9.AMAX+1e-14]
        nwin.append(len(inwin))
        xx=np.log(np.asarray([r["a"] for r in inwin],float))
        gaps.append(float(np.max(np.diff(xx))) if len(xx)>1 else math.inf)
        if m[0]["a"]>g9.AMIN or m[-1]["a"]<g9.AMAX:
            raise RuntimeError(f"{tag}: accepted trace does not bracket common window")
        primary.append(g9.build_interps(m))
        control.append(g9.build_interps(g9.decimate(m)))

    xcommon=np.linspace(math.log(g9.AMIN),math.log(g9.AMAX),g9.NCOMMON)
    acommon=np.exp(xcommon)
    source_errs,source_used=g9.source_validation(source_rows,primary)

    jp={name:[] for name in g9.JET_NAMES}
    jc={name:[] for name in g9.JET_NAMES}
    jsp={name:[] for name in g9.JET_NAMES}
    jsc={name:[] for name in g9.JET_NAMES}
    all_finite=True
    for ik,k in enumerate(g9.K_REQ):
        sp=g9.eval_state(primary[ik],xcommon)
        sc=g9.eval_state(control[ik],xcommon)
        cp,ss_p,_=g9.jet_from_state(sp,acommon,k)
        cc,ss_c,_=g9.jet_from_state(sc,acommon,k)
        for name in g9.JET_NAMES:
            jp[name].append(cp[name]); jc[name].append(cc[name])
            jsp[name].append(ss_p[name]); jsc[name].append(ss_c[name])
            all_finite=bool(all_finite and
                np.all(np.isfinite(cp[name])) and np.all(np.isfinite(cc[name])) and
                np.all(np.isfinite(ss_p[name])) and np.all(np.isfinite(ss_c[name])))
    for d in (jp,jc,jsp,jsc):
        for name in d: d[name]=np.asarray(d[name],float)

    control={}
    glmax=0.0; pmax=0.0
    for name in g9.JET_NAMES:
        a=np.concatenate([jp[name].ravel(),jsp[name].ravel()])
        b=np.concatenate([jc[name].ravel(),jsc[name].ravel()])
        gl=g9.rel_l2(a,b); pp=g9.aor(a,b)
        control[name]={"global_relative_L2":gl,"pointwise_abs_or_rel_max":pp}
        glmax=max(glmax,gl); pmax=max(pmax,pp)

    pt_err=g9.accepted_pt_identity(dense_rows)
    srcmax=float(max(source_errs.values()))
    gates={
        "dense_trace_vs_CLASS_table_abs_or_rel_le_1e12":bool(class_err<=g9.TRACE_CLASS_MAX),
        "minimum_accepted_points_per_k_ge_16":bool(min(nwin)>=g9.MIN_ACCEPTED),
        "common_grid_nodes_exact_64":bool(len(xcommon)==g9.NCOMMON),
        "source_grid_state_validation_abs_or_rel_le_1e4":bool(srcmax<=g9.SOURCE_MAX),
        "primary_vs_decimated_global_relative_L2_le_5e4":bool(glmax<=g9.CONTROL_GL2_MAX),
        "primary_vs_decimated_pointwise_abs_or_rel_le_2e3":bool(pmax<=g9.CONTROL_POINT_MAX),
        "pt_identity_abs_or_rel_le_1e12":bool(pt_err<=g9.PT_ID_MAX),
        "all_complete_jet_entries_finite":bool(all_finite),
    }
    state_primary_public=[]
    for ik,k in enumerate(g9.K_REQ):
        sp=g9.eval_state(primary[ik],xcommon)
        Q=sp["Q"]; a=acommon
        alpha=sp["alpha_aest"]; E=sp["E_aest"]; theta=sp["theta_dark"]
        chi=Q*(a*theta/(k*k)+alpha)
        state_primary_public.append({
            "alpha":np.asarray(alpha,float),
            "E":np.asarray(E,float),
            "chi":np.asarray(chi,float),
        })

    return {
        "tag":tag,
        "precision_file":str(pre.relative_to(ROOT)),
        "dense_rows":len(dense_rows),
        "source_rows":len(source_rows),
        "accepted_points_per_k_in_window":nwin,
        "max_ln_a_gap_per_k_in_window":gaps,
        "requested_k_relative_miss_max":float(kmiss),
        "trace_vs_CLASS_table_abs_or_rel_max":float(class_err),
        "trace_vs_CLASS_counts":class_counts,
        "source_grid_validation":{
            "rows_used":source_used,
            "abs_or_rel_max_by_field":source_errs,
            "abs_or_rel_max":srcmax,
            "limit":g9.SOURCE_MAX,
        },
        "jet_control":{
            "by_entry":control,
            "global_relative_L2_max":glmax,
            "pointwise_abs_or_rel_max":pmax,
        },
        "pt_identity_abs_or_rel_max":pt_err,
        "gates":gates,
        "_jet_cos":jp,
        "_jet_sin":jsp,
        "_ln_a":xcommon,
        "_a":acommon,
        "_state_physical":state_primary_public,
    }

def compare_jets(r1,r2):
    by={}
    glmax=0.0; pmax=0.0
    for name in g9.JET_NAMES:
        a=np.concatenate([r1["_jet_cos"][name].ravel(),r1["_jet_sin"][name].ravel()])
        b=np.concatenate([r2["_jet_cos"][name].ravel(),r2["_jet_sin"][name].ravel()])
        gl=g9.rel_l2(a,b); pp=g9.aor(a,b)
        by[name]={"global_relative_L2":gl,"pointwise_abs_or_rel_max":pp}
        glmax=max(glmax,gl); pmax=max(pmax,pp)
    return by,glmax,pmax

def cosine(a,b):
    aa=np.asarray(a,float).ravel(); bb=np.asarray(b,float).ravel()
    return float(np.dot(aa,bb)/max(np.linalg.norm(aa)*np.linalg.norm(bb),1e-300))

def physical_shape_control(r1,r2):
    rows=[]
    cmin=1.0
    for ik,kh in enumerate(g9.K_H):
        q={"k_h_per_Mpc":float(kh)}
        for name in ("alpha","E","chi"):
            co=cosine(r1["_state_physical"][ik][name],r2["_state_physical"][ik][name])
            q[name+"_cosine"]=co
            cmin=min(cmin,co)
        rows.append(q)
    return rows,float(cmin)

def public_level(r):
    return {k:v for k,v in r.items() if not k.startswith("_")}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--class-root",required=True)
    ap.add_argument("--json-out",required=True)
    ap.add_argument("--npz-out",required=True)
    args=ap.parse_args()
    class_root=Path(args.class_root).resolve()
    Path(args.json_out).parent.mkdir(parents=True,exist_ok=True)

    patch_report_path=ROOT/"results"/"ge15_s_state_patch.json"
    if not patch_report_path.exists():
        result={"classification":"GE15_CANCELLATION_FREE_S_STATE_IMPLEMENTATION_FAIL",
                "reason":"missing ge15_s_state_patch.json"}
        Path(args.json_out).write_text(json.dumps(result,indent=2)+"\n")
        print(json.dumps(result,indent=2))
        raise SystemExit(3)
    patch_report=json.loads(patch_report_path.read_text())
    patch_ok=bool(
        patch_report.get("classification")=="GE15_CANCELLATION_FREE_S_STATE_PATCH_PASS"
        and patch_report.get("physics_modified") is False
        and patch_report.get("state_dimension_modified") is False
        and patch_report.get("initial_s")==0.0
        and all(patch_report.get("checks",{}).values())
    )

    precision_header=(class_root/"include"/"precisions.h").read_text()
    active_keys_present=all(
        key in precision_header
        for key in ("tol_perturbations_integration","perturbations_sampling_stepsize")
    )
    obsolete_keys_absent=all(
        "tol_perturb_integration" not in pre.read_text()
        and "perturb_sampling_stepsize" not in pre.read_text()
        for pre in LEVELS.values()
    )
    if not (patch_ok and active_keys_present and obsolete_keys_absent):
        result={
            "classification":"GE15_CANCELLATION_FREE_S_STATE_IMPLEMENTATION_FAIL",
            "s_state_patch_pass":patch_ok,
            "active_precision_keys_present":active_keys_present,
            "obsolete_singular_keys_absent":obsolete_keys_absent,
        }
        Path(args.json_out).write_text(json.dumps(result,indent=2)+"\n")
        print(json.dumps(result,indent=2))
        raise SystemExit(3)

    results={tag:run_level(class_root,tag,pre) for tag,pre in LEVELS.items()}
    r1,r2=results["R1"],results["R2"]
    cross,cross_gl,cross_p=compare_jets(r1,r2)
    shape_rows,shape_cos_min=physical_shape_control(r1,r2)

    r1_n=np.asarray(r1["accepted_points_per_k_in_window"],int)
    r2_n=np.asarray(r2["accepted_points_per_k_in_window"],int)
    r1_gap=np.asarray(r1["max_ln_a_gap_per_k_in_window"],float)
    r2_gap=np.asarray(r2["max_ln_a_gap_per_k_in_window"],float)
    r1_src=float(r1["source_grid_validation"]["abs_or_rel_max"])
    r2_src=float(r2["source_grid_validation"]["abs_or_rel_max"])

    dense_hashes={}
    for tag in ("R1","R2"):
        p=ROOT/"results"/f"ge15_{tag}_dense_accepted_step_trace.dat"
        dense_hashes[tag]=hashlib.sha256(p.read_bytes()).hexdigest()
    traces_differ=bool(dense_hashes["R1"] != dense_hashes["R2"])

    representation_gates={
        "s_state_patch_report_pass":bool(patch_ok),
        "active_precision_keys_present_in_pinned_CLASS":bool(active_keys_present),
        "obsolete_singular_keys_absent_from_precision_files":bool(obsolete_keys_absent),
        "R1_R2_dense_trace_hashes_differ":bool(traces_differ),
        "same_number_of_AeST_dynamical_states":bool(
            patch_report.get("state_dimension_modified") is False
        ),
        "s_initial_value_exact_zero":bool(patch_report.get("initial_s")==0.0),
        "physical_alpha_trace_reconstructed_from_s_minus_velocity":bool(
            patch_report.get("checks",{}).get("dense_trace_physical_alpha",False)
        ),
        "no_physics_rhs_reconstructs_chi_from_alpha_plus_velocity":bool(
            patch_report.get("checks",{}).get("legacy_stress_cancellation_absent",False)
            and patch_report.get("checks",{}).get("legacy_derivative_cancellation_absent",False)
        ),
    }
    closure_gates={
        "R1_all_single_level_gates":bool(all(r1["gates"].values())),
        "R2_all_single_level_gates":bool(all(r2["gates"].values())),
        "R1_vs_R2_complete_jet_global_relative_L2_le_5e4":bool(cross_gl<=5e-4),
        "R1_vs_R2_complete_jet_pointwise_abs_or_rel_le_2e3":bool(cross_p<=2e-3),
        "alpha_E_chi_per_k_shape_cosine_ge_0p9999":bool(shape_cos_min>=0.9999),
    }
    refinement_gates={**representation_gates,**closure_gates}
    passed=bool(all(refinement_gates.values()))
    classification=(
        "GE15_CANCELLATION_FREE_S_STATE_PRECISION_CLOSURE_PASS"
        if passed else
        "GE15_CANCELLATION_FREE_S_STATE_PRECISION_CLOSURE_FAIL"
    )

    result={
        "classification":classification,
        "scope":"Exact cancellation-free s=chi/Q internal-state reparameterization tested with the frozen R1/R2 precision pair; diagnostic traces retain physical alpha and the GE06 local-jet dictionary.",
        "predata_classification":"GE15_PREDATA_CANCELLATION_FREE_S_STATE_PRECISION_CLOSURE",
        "historical_GE09_classification":"GE09_DENSE_ACCEPTED_STEP_LOCAL_JET_BRIDGE_FAIL",
        "historical_GE11_repair01_classification":"GE11_REPAIR01_DENSE_LOCAL_JET_FIXED_REFINEMENT_FAIL",
        "GE14_diagnosis":"GE14_CHI_CANCELLATION_STIFF_SEED_LOCALIZED",
        "s_state_patch_report":patch_report,
        "physical_shape_control":{"per_k":shape_rows,"cosine_min":shape_cos_min},
        "precision_binding":{
            "active_keys_present":active_keys_present,
            "obsolete_keys_absent":obsolete_keys_absent,
            "dense_trace_sha256":dense_hashes
        },
        "levels":{"R1":public_level(r1),"R2":public_level(r2)},
        "refinement_control":{
            "by_entry":cross,
            "global_relative_L2_max":cross_gl,
            "pointwise_abs_or_rel_max":cross_p,
        },
        "representation_gates":representation_gates,
        "closure_gates":closure_gates,
        "refinement_gates":refinement_gates,
        "project_boundary":{
            "complete_GE06_local_jet_certified_under_s_state":passed,
            "historical_GE09_relabelled":False,
            "historical_GE11_repair01_relabelled":False,
            "standard_matter_closure_certified":False,
            "Z20_solve_licensed":False,
            "finite_eta_licensed":False,
        },
        "claim_boundary":"PASS certifies precision closure of the eta=0 AeST first-order local jet under the exact cancellation-free s=chi/Q state reparameterization. Historical GE09/GE11 remain unchanged. GE08 Repair01 standard-matter incompleteness remains and Z20 is not licensed.",
    }
    Path(args.json_out).write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")

    save={
        "k_Mpc":g9.K_REQ,"k_h_Mpc":g9.K_H,
        "ln_a":r2["_ln_a"],"a":r2["_a"],
    }
    for tag,r in (("R1",r1),("R2",r2)):
        for name in g9.JET_NAMES:
            save[f"{tag}_cos_{name}"]=r["_jet_cos"][name]
            save[f"{tag}_sin_{name}"]=r["_jet_sin"][name]
    np.savez_compressed(args.npz_out,**save)

    print(json.dumps(result,indent=2,allow_nan=False))
    if not passed:
        raise SystemExit(2)

if __name__=="__main__":
    main()
