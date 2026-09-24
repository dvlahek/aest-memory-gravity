#!/usr/bin/env python3
"""GE19 H3F corrected NL0C Y-action on-shell Z20 science certification.

Separately versioned H3F science run. Recompute frozen H1 on Nt128/Nt64,
replace the entire old scalar-only Y source by the Stage E variational
Y u+phi source, reproject source-aware p0 with unchanged Repair18 algorithm,
and enforce original H3/shift/time/spatial gates. A full legacy-Y control
replays the same core and reproduces the frozen old Repair22 state and p0.
No historical module edit; no q20 or H4/Z21 solve.
"""
from __future__ import annotations

import argparse, contextlib, hashlib, importlib.util, io, json, math, sys
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

import ge19.h3f_corrected_y_source_adapter as h3f_adapter

TINY=1e-300
EPS=float(np.finfo(float).eps)

REPAIR13_JSON_SHA="ae3cc790ecffbd5498b5852273c72ae578d4615de29bbb616673c05cdb3e74b7"
REPAIR13_NPZ_SHA="011c0ae54fd21d70c0e2c695ce62e7b74a3c5529a07c9023c882a447d5b40ca3"
REPAIR18_JSON_SHA="d5603138c2f488413686323d1241613f6ef707b586116aa7fe865ae25ceb0edc"
REPAIR21_JSON_SHA="e27d12f18a992a1c8c3217e67c0efd39dcf7c9d7aadcfbbb3220f7508bca1bb2"
REPAIR21_NPZ_SHA="c6fcde7d39480ec7f03de2acf0f33f648a997404c9cca8f83990ed7b50667f3b"

SOURCE_SPATIAL_MAX=5e-4
LINEAR_MAX=1e-8
SHIFT_ACTIVE_MAX=1e-6
ANISO_MAX=1e-6
STATE_MAX=5e-3
ORDER_MIN=2.5
P_REPRO_MAX=1e-12
INIT_CONSTRAINT_MAX=1e-8
INIT_LAPSE_MAX=1e-6
INIT_SHIFT_MAX=1e-6
INIT_ALG_MAX=1e-8
NEAR_NULL_RATIO_MAX=1000.0*EPS


def sha256(p:Path)->str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load_module(path:Path,name:str):
    spec=importlib.util.spec_from_file_location(name,path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def rel_l2(a,b):
    aa=np.asarray(a,complex); bb=np.asarray(b,complex)
    return float(np.linalg.norm(aa-bb)/max(np.linalg.norm(aa),np.linalg.norm(bb),TINY))


def cosine(a,b):
    aa=np.asarray(a,complex).ravel(); bb=np.asarray(b,complex).ravel()
    return float(np.real(np.vdot(aa,bb))/max(np.linalg.norm(aa)*np.linalg.norm(bb),TINY))


def complex_vec(pairs):
    return np.asarray([complex(float(z[0]),float(z[1])) for z in pairs],complex)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--results-dir",default=str(ROOT/"results"))
    ap.add_argument("--json-out",required=True)
    ap.add_argument("--npz-out",required=True)
    args=ap.parse_args()
    rd=Path(args.results_dir)

    required={
        "trace":rd/"ge15_R1_dense_accepted_step_trace.dat",
        "lambda":rd/"ge15_R1_cli_background.dat",
        "ge18n":rd/"ge18_repair01_on_shell_matched_dust_first_order_bridge.npz",
        "r13j":rd/"ge19_repair13_self_consistent_reduced_background_h1_reclosure.json",
        "r13n":rd/"ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz",
        "r18":rd/"ge19_repair18_zero_coordinate_constraint_projected_momentum_boundary.json",
        "r21j":rd/"ge19_repair21_on_shell_h1_parent_matched_shift_audit.json",
        "r21n":rd/"ge19_repair21_on_shell_h1_parent_matched_shift_audit.npz",
        "r22n":rd/"ge19_repair22_on_shell_parent_z20_certification.npz",
        "stageej":rd/"ge19_h4_stagee_y_source_rows_LOCAL.json",
    }
    missing=[str(p) for p in required.values() if not p.exists()]
    if missing:
        raise RuntimeError("missing frozen inputs: "+", ".join(missing))

    expected={
        "r13j":REPAIR13_JSON_SHA,
        "r13n":REPAIR13_NPZ_SHA,
        "r18":REPAIR18_JSON_SHA,
        "r21j":REPAIR21_JSON_SHA,
        "r21n":REPAIR21_NPZ_SHA,
        "r22n":"3020e0d040f902ab2609e05705f4508d9919665b1344fa0e641644ea8fc41a16",
        "stageej":"c3ff4cc18dc8c7a69ba661a68ea3de987818f1b9c1db3275b08f2976c385896e",
    }
    for key,h in expected.items():
        got=sha256(required[key])
        if got!=h:
            raise RuntimeError(f"{key} hash mismatch: {got}")

    d13=json.loads(required["r13j"].read_text())
    d18=json.loads(required["r18"].read_text())
    d21frozen=json.loads(required["r21j"].read_text())
    dstagee=json.loads(required["stageej"].read_text())
    if (dstagee.get("classification") !=
        "GE19_H4_STAGEE_Y_SOURCE_ROW_DICTIONARY_IMPLEMENTATION_PASS"
        or dstagee.get("all_implementation_gates_pass") is not True):
        raise RuntimeError("Stage E local source parent is not PASS")
    if d13.get("stage_A_pass") is not True:
        raise RuntimeError("Repair13 Stage A not PASS")
    if d18.get("routing",{}).get("next_route")!="ZERO_COORDINATE_CONSTRAINT_PROJECTED_MOMENTUM_BOUNDARY_CERTIFIED":
        raise RuntimeError("Repair18 boundary not certified")
    if d21frozen.get("routing",{}).get("next_route")!="INTERPOLATED_H1_PARENT_DEFECT_CONFIRMED":
        raise RuntimeError("Repair21 did not license certification")

    # Recompute the exact locked Repair21 pipeline rather than certifying its
    # stored arrays post hoc.
    r21=load_module(
        ROOT/"ge19/h3f_corrected_y_parent_core.py",
        "ge19_h3f_parent_core_for_science",
    )
    tmpj=Path(args.json_out).with_name(Path(args.json_out).stem+".h3fcore_tmp.json")
    tmpn=Path(args.npz_out).with_name(Path(args.npz_out).stem+".h3fcore_tmp.npz")
    old_argv=list(sys.argv)
    captured=io.StringIO()
    try:
        sys.argv=[
            str(ROOT/"ge19/h3f_corrected_y_parent_core.py"),
            "--results-dir",str(rd),
            "--json-out",str(tmpj),
            "--npz-out",str(tmpn),
        ]
        with contextlib.redirect_stdout(captured):
            r21.main()
    finally:
        sys.argv=old_argv

    if not tmpj.exists() or not tmpn.exists():
        raise RuntimeError("Repair21 certification core did not produce temporary outputs")

    d21=json.loads(tmpj.read_text())
    if d21.get("classification")!="GE19_H3F_CORRECTED_Y_PARENT_CORE_COMPLETE":
        raise RuntimeError("corrected H3F core implementation did not complete")
    if d21.get("routing",{}).get("next_route") not in (
        "H3F_CORRECTED_SOURCE_DIAGNOSTIC_GATES_PASS",
        "H3F_CORRECTED_SOURCE_SCIENCE_GATE_FAIL",
    ):
        raise RuntimeError("unexpected corrected H3F core route")

    # Mandatory Y-disabled baseline: run the SAME new H3F core with
    # historical scalar-only Y restored and compare all old certified
    # Repair22 Z20 and projected p0 arrays. No old result is relabelled.
    tmpjl=Path(args.json_out).with_name(Path(args.json_out).stem+".h3flegacy_tmp.json")
    tmpnl=Path(args.npz_out).with_name(Path(args.npz_out).stem+".h3flegacy_tmp.npz")
    try:
        sys.argv=[
            str(ROOT/"ge19/h3f_corrected_y_parent_core.py"),
            "--results-dir",str(rd),
            "--json-out",str(tmpjl),
            "--npz-out",str(tmpnl),
            "--legacy-y-control",
        ]
        with contextlib.redirect_stdout(io.StringIO()):
            r21.main()
    finally:
        sys.argv=old_argv
    if not tmpjl.exists() or not tmpnl.exists():
        raise RuntimeError("Y-disabled H3F legacy control missing outputs")
    dlegacy=json.loads(tmpjl.read_text())
    if (dlegacy.get("classification")!="GE19_H3F_LEGACY_Y_CONTROL_COMPLETE"
        or dlegacy.get("routing",{}).get("next_route")!="H3F_LEGACY_Y_CONTROL_PASS"):
        raise RuntimeError("Y-disabled legacy control did not reproduce old H3 gates")
    oldr22=np.load(required["r22n"])
    old_control=np.load(tmpnl)
    legacy_state_rel=0.0
    legacy_p0_rel=0.0
    for nt,label in ((128,"primary"),(64,"control")):
        for t in ("C_min","C_star","C_max"):
            legacy_state_rel=max(
                legacy_state_rel,
                rel_l2(
                    old_control[f"Nt{nt}_{t}_state"],
                    oldr22[f"{t}_Z20_{label}"],
                ),
            )
            legacy_p0_rel=max(
                legacy_p0_rel,
                rel_l2(
                    old_control[f"Nt{nt}_{t}_projected_p0"],
                    oldr22[f"{t}_projected_p0_{label}"],
                ),
            )
    legacy_reproduction=bool(
        legacy_state_rel<=1e-11 and legacy_p0_rel<=1e-11
    )
    if not legacy_reproduction:
        raise RuntimeError(
            "Y-disabled baseline failed to reproduce Repair22: "+
            str((legacy_state_rel,legacy_p0_rel))
        )

    # Frozen implementation modules for source and boundary audits.
    r7=load_module(ROOT/"ge19/repair07_window_retarded_reduced_h3_z20_particular.py","r7r22")
    r11=load_module(ROOT/"ge19/repair11_lambda_inclusive_reduced_h1_reclosure.py","r11r22")
    r13=load_module(ROOT/"ge19/repair13_self_consistent_reduced_background_h1_reclosure.py","r13r22")
    r14=load_module(ROOT/"ge19/repair14_self_consistent_reduced_h3_z20_particular.py","r14r22")
    r18=load_module(ROOT/"ge19/repair18_zero_coordinate_constraint_projected_momentum_boundary.py","r18r22")

    def h3f_bundle_local(r7arg,mod6arg,mod7arg,bg,rho_lambda,tag,nx,state,dot):
        return h3f_adapter.source_bundle_reduced_lambda(
            r7arg,r14,mod6arg,mod7arg,bg,rho_lambda,tag,nx,state,dot
        )

    mod6_frozen=r7.load_frozen_generator(
        ROOT/"ge06/analytic_aest_directional_source_generator.py","ge06r22"
    )
    mod6=r7.build_stable_ge06_generator_v2(mod6_frozen)
    mod7=r7.load_frozen_generator(
        ROOT/"ge07/pressureless_matter_directional_source_generator.py","ge07r22"
    )

    z=np.load(tmpn)
    base128,_,_=r7.build_ge15_reference(required["trace"],128)
    base64,_,_=r7.build_ge15_reference(required["trace"],64)
    rho128=r11.interp_lambda(required["lambda"],base128["x"])
    rho64=r11.interp_lambda(required["lambda"],base64["x"])
    bgs={}; rhos={128:rho128,64:rho64}
    for nt,base,rho in ((128,base128,rho128),(64,base64,rho64)):
        for tag in r7.C_TAGS:
            bgs[(nt,tag)],_=r13.reduced_background(r7,base,tag,rho)

    # Repair18 frozen reference p0.
    p18={}
    for q in d18["per_case"]:
        if q["grid"]=="primary":
            p18[(q["C"],float(q["beta0"]),int(q["m"]))]=complex_vec(q["boundary"]["p"])

    # Rebuild exact on-shell-parent H3 sources on both time grids.
    src={}; src2048={}
    spatial_rows=[]; spatial_max=0.0
    source_piece_norms=[]; zero_mode_rows=[]
    all_sources_finite=True
    save={}

    for nt in (128,64):
        for tag in r7.C_TAGS:
            st=np.asarray(z[f"Nt{nt}_{tag}_H1_state"],complex)
            dt=np.asarray(z[f"Nt{nt}_{tag}_H1_dot"],complex)
            src[(nt,tag)]=h3f_bundle_local(
                r7,mod6,mod7,bgs[(nt,tag)],rhos[nt],tag,r7.NX_PRIMARY,st,dt
            )

    for tag in r7.C_TAGS:
        st=np.asarray(z[f"Nt128_{tag}_H1_state"],complex)
        dt=np.asarray(z[f"Nt128_{tag}_H1_dot"],complex)
        src2048[tag]=h3f_bundle_local(
            r7,mod6,mod7,bgs[(128,tag)],rho128,tag,r7.NX_SPATIAL_CONTROL,st,dt
        )
        for beta in r7.BETAS:
            a=np.asarray(src[(128,tag)][beta]["rhs"][:,:,1:41],complex)
            b=np.asarray(src2048[tag][beta]["rhs"][:,:,1:41],complex)
            e=rel_l2(a,b)
            spatial_max=max(spatial_max,e)
            spatial_rows.append({"C":tag,"beta0":float(beta),"relative_L2_m1_40":e})
            all_sources_finite=bool(
                all_sources_finite and np.all(np.isfinite(a)) and np.all(np.isfinite(b))
            )

            qga=np.asarray(src[(128,tag)][beta]["Q_ga"][:,:,1:41],complex)
            qm=np.asarray(src[(128,tag)][beta]["Q_matter"][:,:,1:41],complex)
            ql=np.asarray(src[(128,tag)][beta]["Q_lambda"][:,:,1:41],complex)
            yy=np.asarray(src[(128,tag)][beta]["Y_H3"][:,:,1:41],complex)
            analytic=qga+qm+ql
            source_piece_norms.append({
                "C":tag,"beta0":float(beta),
                "Einstein_AeST_Q_L2":float(np.linalg.norm(qga)),
                "dust_Q_L2":float(np.linalg.norm(qm)),
                "lambda_Q_L2":float(np.linalg.norm(ql)),
                "Y_H3_L2":float(np.linalg.norm(yy)),
                "lambda_over_Einstein_AeST_plus_dust":float(
                    np.linalg.norm(ql)/max(np.linalg.norm(qga+qm),TINY)
                ),
                "Y_over_total_analytic":float(
                    np.linalg.norm(yy)/max(np.linalg.norm(analytic),TINY)
                ),
                "Y_cosine_total_analytic":cosine(yy,analytic),
            })
            zero_mode_rows.append({
                "C":tag,"beta0":float(beta),
                "m0_source_global_L2":float(np.linalg.norm(src[(128,tag)][beta]["rhs"][:,:,0]))
            })
            key=f"{tag}_beta{str(beta).replace('.','p')}"
            save[f"{key}_rhs_Nt128_Nx1024"]=np.asarray(src[(128,tag)][beta]["rhs"],complex)
            save[f"{key}_rhs_constraint_Nt128_Nx1024"]=np.asarray(src[(128,tag)][beta]["rhs_constraint"],complex)

    # Re-audit the projected boundary against exact Repair18 reference.
    boundary_rows=[]
    bp_repro=0.0; old_bp_difference=0.0; bscaled=0.0; blapse=0.0; bshift=0.0; balg=0.0
    rank_min=99; rank_max=0; aug_max=0

    for nt in (128,64):
        x=np.asarray(bgs[(nt,r7.C_TAGS[0])]["x"],float)
        for tag in r7.C_TAGS:
            for jm,m in enumerate(r7.M_SOLVE):
                k=float(m*r7.g9.K_REQ[0]/r7.FOURIER_N[0])
                rhsfun,confun=r7._source_interp(x,src[(nt,tag)],m)
                r0=np.asarray(rhsfun(float(x[0])),complex)
                c0=np.asarray(confun(float(x[0])),complex)
                if r0.ndim==1: r0=r0[:,None]
                if c0.ndim==1: c0=c0[:,None]
                M,F,ZY,ZR,WY,WR,Cmat,bp,opdiag=r7._canonical_operator_matrices(
                    mod6,mod7,bgs[(nt,tag)],tag,k,float(x[0])
                )
                for ib,beta in enumerate(r7.BETAS):
                    source0=np.concatenate([r0[:,ib],c0[:,ib]])
                    woff=WR@source0
                    lr=Cmat[4]; sr=Cmat[10]+Cmat[11]
                    A=np.vstack([lr@WY,sr@WY])[:,4:8]
                    bb=np.asarray([r0[0,ib]-lr@woff,c0[0,ib]-sr@woff],complex)
                    p,sd=r18.projected_momentum_solve(A,bb)
                    ev=r18.evaluate_candidate(Cmat,WY,WR,source0,r0[:,ib],c0[:,ib],p)
                    new_p0=np.asarray(z[f"Nt{nt}_{tag}_projected_p0"],complex)[ib,jm]
                    pr=rel_l2(p,new_p0)
                    oldpr=rel_l2(p,p18[(tag,float(beta),int(m))])
                    old_bp_difference=max(old_bp_difference,oldpr)
                    bp_repro=max(bp_repro,pr)
                    bscaled=max(bscaled,float(sd["scaled_relative_residual_final"]))
                    blapse=max(blapse,float(ev["lapse"]["metric"]))
                    bshift=max(bshift,float(ev["shift"]["metric"]))
                    balg=max(balg,float(ev["algebraic_relative_residual"]))
                    rank_min=min(rank_min,int(sd["rank"]))
                    rank_max=max(rank_max,int(sd["rank"]))
                    aug_max=max(aug_max,int(sd["augmented_rank"]))
                    boundary_rows.append({
                        "Nt":nt,"C":tag,"beta0":float(beta),"m":int(m),
                        "source_aware_projected_p0_reproduction_relative_L2":pr,
                        "historical_Repair18_p0_difference_report_only":oldpr,
                        "scaled_constraint_relative_residual":float(sd["scaled_relative_residual_final"]),
                        "lapse_backward_error":float(ev["lapse"]["metric"]),
                        "shift_backward_error":float(ev["shift"]["metric"]),
                        "anisotropy_backward_error":float(ev["anisotropy"]["metric"]),
                        "eliminated_algebraic_relative_residual":float(ev["algebraic_relative_residual"]),
                        "rank":int(sd["rank"]),
                        "augmented_rank":int(sd["augmented_rank"]),
                    })

    # Pull certification controls from the recomputed Repair21 core.
    h1=d21["H1_on_shell_controls"]
    matched=d21["matched_shift"]
    h3=d21["H3_controls"]

    h1_gates=dict(h1["gates"])
    boundary_gates={
        "source_aware_projected_p0_reproduction_le_1e12":bool(bp_repro<=P_REPRO_MAX),
        "initial_scaled_constraint_relative_residual_le_1e8":bool(bscaled<=INIT_CONSTRAINT_MAX),
        "initial_lapse_backward_error_le_1e6":bool(blapse<=INIT_LAPSE_MAX),
        "initial_shift_backward_error_le_1e6":bool(bshift<=INIT_SHIFT_MAX),
        "initial_eliminated_algebraic_relative_residual_le_1e8":bool(balg<=INIT_ALG_MAX),
        "rank_and_augmented_rank_eq_2":bool(rank_min==2 and rank_max==2 and aug_max==2),
    }
    stage_gates={
        "source_Nx1024_vs_Nx2048_m1_40_relative_L2_le_5e4":bool(spatial_max<=SOURCE_SPATIAL_MAX),
        "active_Nt128_shift_Linf_le_1e6":bool(matched["Nt128_active_Linf"]<=SHIFT_ACTIVE_MAX),
        "near_null_absolute_residual_over_Sref_le_1000eps":bool(
            matched["near_null_absolute_residual_over_Sref_Nt128"]<=NEAR_NULL_RATIO_MAX
        ),
        "matched_active_Linf_order_ge_2p5":bool(matched["observed_order_Linf"]>=ORDER_MIN),
        "matched_active_L2_order_ge_2p5":bool(matched["observed_order_L2"]>=ORDER_MIN),
        "H3_state_Nt64_vs_Nt128_relative_L2_le_5e3":bool(
            h3["state_Nt64_vs_Nt128_relative_L2"]<=STATE_MAX
        ),
        "H3_linear_system_relative_L2_residual_le_1e8":bool(
            h3["linear_system_relative_L2_residual_max"]<=LINEAR_MAX
        ),
        "H3_anisotropy_backward_error_le_1e6":bool(
            h3["anisotropy_backward_error_max"]<=ANISO_MAX
        ),
        "all_sources_finite":bool(all_sources_finite),
        "all_H3_outputs_finite":bool(h3["all_outputs_finite"]),
    }

    # Completeness and finite certified candidate arrays.
    complete=True; candidate_finite=True
    for nt in (128,64):
        for tag in r7.C_TAGS:
            arr=np.asarray(z[f"Nt{nt}_{tag}_state"],complex)
            complete=bool(complete and arr.shape==(3,40,6,nt))
            candidate_finite=bool(candidate_finite and np.all(np.isfinite(arr)))
            save[f"{tag}_Z20_{'primary' if nt==128 else 'control'}"]=arr
            save[f"{tag}_H1_{'primary' if nt==128 else 'control'}"]=np.asarray(
                z[f"Nt{nt}_{tag}_H1_state"],complex
            )
            save[f"{tag}_H1dot_{'primary' if nt==128 else 'control'}"]=np.asarray(
                z[f"Nt{nt}_{tag}_H1_dot"],complex
            )
            save[f"{tag}_shift_metric_{'primary' if nt==128 else 'control'}"]=np.asarray(
                z[f"Nt{nt}_{tag}_shift_metric"],float
            )
            save[f"{tag}_shift_abs_{'primary' if nt==128 else 'control'}"]=np.asarray(
                z[f"Nt{nt}_{tag}_shift_abs"],float
            )
            save[f"{tag}_shift_scale_{'primary' if nt==128 else 'control'}"]=np.asarray(
                z[f"Nt{nt}_{tag}_shift_scale"],float
            )
            save[f"{tag}_projected_p0_{'primary' if nt==128 else 'control'}"]=np.asarray(
                z[f"Nt{nt}_{tag}_projected_p0"],complex
            )

    completeness_gates={
        "all_C_beta_m_cases_complete":bool(complete),
        "certified_candidate_arrays_finite":bool(candidate_finite),
    }

    all_gates={**h1_gates,**boundary_gates,**stage_gates,**completeness_gates,
               "Y_disabled_Repair22_Z20_and_p0_reproduction_le_1e11":legacy_reproduction}
    passed=bool(all(all_gates.values()))

    report={
        "classification":(
            "GE19_H3F_CORRECTED_Y_H3_Z20_CERTIFIED"
            if passed else
            "GE19_H3F_CORRECTED_Y_H3_Z20_SCIENCE_FAIL"
        ),
        "predata_classification":"GE19_H3F_PREDATA_ACTION_COMPLETED_Y_Z20_PARENT_RECLOSURE",
        "certification_run":True,
        "provenance":{
            "Repair13_JSON_sha256":sha256(required["r13j"]),
            "Repair13_NPZ_sha256":sha256(required["r13n"]),
            "Repair18_JSON_sha256":sha256(required["r18"]),
            "Repair21_JSON_sha256":sha256(required["r21j"]),
            "Repair21_NPZ_sha256":sha256(required["r21n"]),
            "H3F_corrected_Y_core_recomputed":True,
            "historical_physics_modules_edited":False,
            "StageE_full_Y_aether_and_scalar_source_used":True,
            "historical_scalar_only_Y_replaced_not_added":True,
            "StageE_local_JSON_sha256":sha256(required["stageej"]),
            "Y_disabled_original_Repair22_reproduced":legacy_reproduction,
            "boundary_rule_edited":False,
            "active_shift_threshold_relaxed":False,
        },
        "H1_on_shell_controls":h1,
        "source_spatial_convergence":{
            "Nx_primary":int(r7.NX_PRIMARY),
            "Nx_control":int(r7.NX_SPATIAL_CONTROL),
            "relative_L2_m1_40_max":spatial_max,
            "per_case":spatial_rows,
            "all_sources_finite":all_sources_finite,
        },
        "source_decomposition":source_piece_norms,
        "legacy_Y_control":{"Z20_relative_L2_max":legacy_state_rel,
                            "projected_p0_relative_L2_max":legacy_p0_rel,
                            "original_Repair22_NPZ_sha256":sha256(required["r22n"]),
                            "all_original_science_results_unchanged":True},
        "zero_mode_source":zero_mode_rows,
        "boundary_certification":{
            "source_aware_projected_p0_reproduction_relative_L2_max":bp_repro,
            "historical_Repair18_p0_difference_report_only_max":old_bp_difference,
            "scaled_constraint_relative_residual_max":bscaled,
            "lapse_backward_error_max":blapse,
            "shift_backward_error_max":bshift,
            "eliminated_algebraic_relative_residual_max":balg,
            "rank_min":int(rank_min),
            "rank_max":int(rank_max),
            "augmented_rank_max":int(aug_max),
            "per_case":boundary_rows,
        },
        "shift_certification":{
            "original_all_row_metric_primary":d21["per_grid"]["128"]["original_all_row_shift_backward_error_max"],
            "original_all_row_metric_control":d21["per_grid"]["64"]["original_all_row_shift_backward_error_max"],
            "original_all_row_metric_is_report_only":True,
            "near_null_definition":d21["near_null_definition"],
            **matched,
        },
        "H3_controls":h3,
        "completeness":{
            "all_C_beta_m_cases_complete":complete,
            "certified_candidate_arrays_finite":candidate_finite,
        },
        "gates":all_gates,
        "Z20_constructed":True,
        "Z20_certified":passed,
        "project_boundary":{
            "Repair13_reduced_H1_certified":True,
            "Repair18_finite_window_boundary_certified":True,
            "frozen_Repair21_interpolated_H1_parent_defect_confirmed":True,
            "reduced_window_local_Z20_certified":passed,
            "homogeneous_primordial_Z20_certified":False,
            "full_species_Z20_certified":False,
            "physical_amplitude_nonlinear_state_certified":False,
            "new_corrected_q20_construction_licensed_after_freeze":passed,
            "old_Repair27_q20_not_relabelled":True,
            "Z21_licensed":False,
        },
        "claim_boundary":"PASS certifies only the separately versioned, action-completed Y u+phi low-mode window-local reduced-H3 Z20 particular with unchanged GE06/GE07/Lambda, on-shell H1 and source-aware Repair18 boundary algorithm. It does not certify the new dependent q20, full H4 Noether, Z21, primordial/homogeneous second-order modes, lensing or observations.",
    }

    outj=Path(args.json_out); outn=Path(args.npz_out)
    outj.parent.mkdir(parents=True,exist_ok=True); outn.parent.mkdir(parents=True,exist_ok=True)
    outj.write_text(json.dumps(report,indent=2,allow_nan=False)+"\n")
    save["x_primary"]=np.asarray(base128["x"],float)
    save["x_control"]=np.asarray(base64["x"],float)
    np.savez_compressed(outn,**save)

    try: tmpj.unlink()
    except FileNotFoundError: pass
    try: tmpn.unlink()
    except FileNotFoundError: pass
    try: tmpjl.unlink()
    except FileNotFoundError: pass
    try: tmpnl.unlink()
    except FileNotFoundError: pass

    print(json.dumps(report,indent=2,allow_nan=False))
    if not passed:
        raise SystemExit(2)


if __name__=="__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:
        print(json.dumps({
            "classification":"GE19_H3F_CORRECTED_Y_Z20_IMPLEMENTATION_FAIL",
            "error":repr(exc),
        },indent=2))
        raise
