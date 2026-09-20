#!/usr/bin/env python3
"""GE11 Repair01 fixed two-level refinement with active pinned-CLASS precision keys.

Uses the exact frozen GE11 numerical values with corrected precision-parameter
names. Historical GE11 remains FAIL.
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
    dense=ROOT/"results"/f"ge11r1_{tag}_dense_accepted_step_trace.dat"
    source=ROOT/"results"/f"ge11r1_{tag}_source_state_trace.dat"
    prefix=ROOT/"results"/f"ge11r1_{tag}_cli"
    log=ROOT/"results"/f"ge11r1_{tag}_class.log"
    for p in (dense,source,log):
        if p.exists(): p.unlink()
    for i in range(len(g9.K_REQ)):
        p=Path(str(prefix)+f"_perturbations_k{i}_s.dat")
        if p.exists(): p.unlink()

    ini=class_root/f"ge11r1_{tag}.ini"
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
    if not (active_keys_present and obsolete_keys_absent):
        result={
            "classification":"GE11_REPAIR01_PRECISION_BINDING_IMPLEMENTATION_FAIL",
            "active_precision_keys_present":active_keys_present,
            "obsolete_singular_keys_absent":obsolete_keys_absent,
        }
        Path(args.json_out).write_text(json.dumps(result,indent=2)+"\n")
        print(json.dumps(result,indent=2))
        raise SystemExit(3)

    results={tag:run_level(class_root,tag,pre) for tag,pre in LEVELS.items()}
    r1,r2=results["R1"],results["R2"]
    cross,cross_gl,cross_p=compare_jets(r1,r2)

    r1_n=np.asarray(r1["accepted_points_per_k_in_window"],int)
    r2_n=np.asarray(r2["accepted_points_per_k_in_window"],int)
    r1_gap=np.asarray(r1["max_ln_a_gap_per_k_in_window"],float)
    r2_gap=np.asarray(r2["max_ln_a_gap_per_k_in_window"],float)
    r1_src=float(r1["source_grid_validation"]["abs_or_rel_max"])
    r2_src=float(r2["source_grid_validation"]["abs_or_rel_max"])

    dense_hashes={}
    for tag in ("R1","R2"):
        p=ROOT/"results"/f"ge11r1_{tag}_dense_accepted_step_trace.dat"
        dense_hashes[tag]=hashlib.sha256(p.read_bytes()).hexdigest()
    traces_differ=bool(dense_hashes["R1"] != dense_hashes["R2"])

    refinement_gates={
        "active_precision_keys_present_in_pinned_CLASS":bool(active_keys_present),
        "obsolete_singular_keys_absent_from_repair_precision_files":bool(obsolete_keys_absent),
        "R1_R2_dense_trace_hashes_differ":traces_differ,
        "R1_all_single_level_gates":bool(all(r1["gates"].values())),
        "R2_all_single_level_gates":bool(all(r2["gates"].values())),
        "accepted_points_R1_not_less_than_historical_runtime_each_k":bool(np.all(r1_n>=np.asarray(HIST_N))),
        "accepted_points_R2_not_less_than_R1_each_k":bool(np.all(r2_n>=r1_n)),
        "max_ln_a_gap_R1_not_greater_than_historical_runtime_each_k":bool(np.all(r1_gap<=HIST_GAPS*(1+1e-12))),
        "max_ln_a_gap_R2_not_greater_than_R1_each_k":bool(np.all(r2_gap<=r1_gap*(1+1e-12))),
        "source_validation_R2_not_greater_than_R1":bool(r2_src<=r1_src*(1+1e-12)),
        "R1_vs_R2_complete_jet_global_relative_L2_le_5e4":bool(cross_gl<=5e-4),
        "R1_vs_R2_complete_jet_pointwise_abs_or_rel_le_2e3":bool(cross_p<=2e-3),
    }
    passed=bool(all(refinement_gates.values()))
    classification=(
        "GE11_REPAIR01_DENSE_LOCAL_JET_FIXED_REFINEMENT_PASS"
        if passed else
        "GE11_REPAIR01_DENSE_LOCAL_JET_FIXED_REFINEMENT_FAIL"
    )

    result={
        "classification":classification,
        "scope":"GE11 Repair01 fixed two-level refinement using the frozen GE11 numerical values bound to the active pinned-CLASS precision keys.",
        "historical_GE09_classification":"GE09_DENSE_ACCEPTED_STEP_LOCAL_JET_BRIDGE_FAIL",
        "historical_GE11_classification":"GE11_DENSE_LOCAL_JET_FIXED_REFINEMENT_FAIL",
        "GE10_diagnosis":"GE10_GE09_SOURCE_INTERPOLATION_LIMIT_CONFIRMED",
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
        "refinement_gates":refinement_gates,
        "project_boundary":{
            "complete_GE06_local_jet_certified":passed,
            "historical_GE09_relabelled":False,
            "historical_GE11_relabelled":False,
            "standard_matter_closure_certified":False,
            "Z20_solve_licensed":False,
            "finite_eta_licensed":False,
        },
        "claim_boundary":"PASS certifies only the complete GE06 first-order local jet under the corrected fixed R1/R2 precision binding. Historical GE09/GE11 remain unchanged. GE08 Repair01 matter incompleteness remains and Z20 is not licensed.",
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
