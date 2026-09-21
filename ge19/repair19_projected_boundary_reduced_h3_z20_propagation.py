#!/usr/bin/env python3
"""GE19 Repair19 projected-boundary reduced-H3 Z20 propagation.

Reuses the frozen Repair14 source construction and Stage-B propagation
pipeline unchanged, replacing only the inadmissible finite-window initial
condition q=0,qdot=0 by the certified Repair18 boundary q=0 with canonical
momenta projected onto lapse+shift.

No H1 recomputation, source edit, q20 or H4/Z21 construction.
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import importlib.util
import io
import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

REPAIR18_JSON_SHA="d5603138c2f488413686323d1241613f6ef707b586116aa7fe865ae25ceb0edc"
TINY=1e-300
P_REPRO_MAX=1e-12
PC_P_REPRO_MAX=1e-12
INIT_CONSTRAINT_RES_MAX=1e-8
INIT_LAPSE_MAX=1e-6
INIT_SHIFT_MAX=1e-6
INIT_ALG_MAX=1e-8


def sha256(path:Path)->str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module(path:Path,name:str):
    spec=importlib.util.spec_from_file_location(name,path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def rel_l2(a,b):
    aa=np.asarray(a,complex)
    bb=np.asarray(b,complex)
    return float(np.linalg.norm(aa-bb)/max(np.linalg.norm(aa),np.linalg.norm(bb),TINY))


def complex_vec(pairs):
    return np.asarray([complex(float(z[0]),float(z[1])) for z in pairs],complex)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--results-dir",default=str(ROOT/"results"))
    ap.add_argument("--json-out",required=True)
    ap.add_argument("--npz-out",required=True)
    args=ap.parse_args()
    rd=Path(args.results_dir)

    p18=rd/"ge19_repair18_zero_coordinate_constraint_projected_momentum_boundary.json"
    if not p18.exists():
        raise RuntimeError(f"missing frozen Repair18 parent: {p18}")
    h18=sha256(p18)
    if h18!=REPAIR18_JSON_SHA:
        raise RuntimeError(f"Repair18 JSON hash mismatch: {h18}")

    d18=json.loads(p18.read_text())
    if d18.get("classification")!="GE19_REPAIR18_ZERO_COORDINATE_CONSTRAINT_PROJECTED_MOMENTUM_BOUNDARY_AUDIT_COMPLETE":
        raise RuntimeError("Repair18 classification mismatch")
    if d18.get("routing",{}).get("next_route")!="ZERO_COORDINATE_CONSTRAINT_PROJECTED_MOMENTUM_BOUNDARY_CERTIFIED":
        raise RuntimeError("Repair18 route does not license Repair19")
    if d18.get("global",{}).get("pass_count")!=714:
        raise RuntimeError("Repair18 pass count mismatch")

    parent_index={}
    for q in d18["per_case"]:
        parent_index[(q["grid"],q["C"],float(q["beta0"]),int(q["m"]))]=q

    r18=load_module(
        ROOT/"ge19/repair18_zero_coordinate_constraint_projected_momentum_boundary.py",
        "ge19_repair18_for_repair19",
    )
    r14=load_module(
        ROOT/"ge19/repair14_self_consistent_reduced_h3_z20_particular.py",
        "ge19_repair14_for_repair19",
    )

    collector=[]

    original_r14_load=r14.load_module

    def patched_r14_load(path:Path,name:str):
        mod=original_r14_load(path,name)
        if Path(path).name!="repair07_window_retarded_reduced_h3_z20_particular.py":
            return mod
        r7=mod

        def solve_case_projected_boundary(mod6,mod7,bg,tag,sources_by_beta):
            nt=len(bg["x"]); nb=len(r7.BETAS)
            grid="primary" if nt==r7.NT_PRIMARY else ("control" if nt==r7.NT_CONTROL else f"Nt{nt}")
            states=np.empty((nb,len(r7.M_SOLVE),6,nt),complex)
            solve_res=np.zeros((nb,len(r7.M_SOLVE)),float)
            con_res=np.zeros((nb,len(r7.M_SOLVE),2),float)
            diagnostics=[]

            for jm,m in enumerate(r7.M_SOLVE):
                k=float(m*r7.g9.K_REQ[0]/r7.FOURIER_N[0])
                rhsfun,confun=r7._source_interp(bg["x"],sources_by_beta,m)
                r0=np.asarray(rhsfun(float(bg["x"][0])),complex)
                c0=np.asarray(confun(float(bg["x"][0])),complex)
                if r0.ndim==1: r0=r0[:,None]
                if c0.ndim==1: c0=c0[:,None]

                M,F,ZY,ZR,WY,WR,Cmat,bp,opdiag=r7._canonical_operator_matrices(
                    mod6,mod7,bg,tag,k,float(bg["x"][0])
                )
                y0=np.zeros((8,nb),complex)
                initdiag=[]

                for ib,beta in enumerate(r7.BETAS):
                    source=np.concatenate([r0[:,ib],c0[:,ib]])
                    woff=WR@source
                    lapse_row=Cmat[4]
                    shift_row=Cmat[10]+Cmat[11]
                    Afull=np.vstack([lapse_row@WY,shift_row@WY])
                    A=Afull[:,4:8]
                    b=np.asarray([
                        r0[0,ib]-lapse_row@woff,
                        c0[0,ib]-shift_row@woff,
                    ],complex)

                    p,sd=r18.projected_momentum_solve(A,b)
                    y0[4:8,ib]=p
                    ev=r18.evaluate_candidate(Cmat,WY,WR,source,r0[:,ib],c0[:,ib],p)

                    key=(grid,tag,float(beta),int(m))
                    if key not in parent_index:
                        raise RuntimeError(f"Repair18 boundary case missing: {key}")
                    pref=complex_vec(parent_index[key]["boundary"]["p"])
                    prepro=rel_l2(p,pref)

                    row={
                        "grid":grid,
                        "C":tag,
                        "beta0":float(beta),
                        "m":int(m),
                        "projected_p0_relative_L2_vs_Repair18":prepro,
                        "scaled_constraint_relative_residual":float(sd["scaled_relative_residual_final"]),
                        "lapse_backward_error":float(ev["lapse"]["metric"]),
                        "shift_backward_error":float(ev["shift"]["metric"]),
                        "anisotropy_backward_error":float(ev["anisotropy"]["metric"]),
                        "eliminated_algebraic_relative_residual":float(ev["algebraic_relative_residual"]),
                        "rank":int(sd["rank"]),
                        "augmented_rank":int(sd["augmented_rank"]),
                        "p0_L2":float(ev["p_L2"]),
                        "qdot0_L2":float(ev["determined_qdot_L2"]),
                        "p0":[[float(z.real),float(z.imag)] for z in p],
                        "qdot0":ev["determined_qdot"],
                    }
                    collector.append(row)
                    initdiag.append(row)

                Y,rdiag=r7._radau2_integrate_canonical(
                    mod6,mod7,bg,tag,k,y0,rhsfun,confun
                )
                st,dd,odiag=r7._reconstruct_canonical_solution(
                    mod6,mod7,bg,tag,k,Y,rhsfun,confun
                )
                states[:,jm]=st

                initial_alg=max(q["eliminated_algebraic_relative_residual"] for q in initdiag)
                initial_lapse=max(q["lapse_backward_error"] for q in initdiag)
                base=max(
                    initial_alg,
                    initial_lapse,
                    rdiag["radau_block_scaled_relative_L2_residual_max"],
                    odiag["algebraic_scaled_relative_L2_residual_max"],
                    odiag["lapse_noether_row_relative_residual_max"],
                )
                solve_res[:,jm]=base
                con_res[:,jm,0]=odiag["shift_constraint_relative_L2_max"]
                con_res[:,jm,1]=odiag["anisotropy_constraint_relative_L2_max"]
                diagnostics.append({
                    "m":int(m),
                    "initial_projected_boundary":initdiag,
                    **rdiag,
                    **odiag,
                })
            return states,solve_res,con_res,diagnostics

        r7.solve_case_canonical=solve_case_projected_boundary
        return r7

    r14.load_module=patched_r14_load

    out_json=Path(args.json_out)
    out_npz=Path(args.npz_out)
    out_json.parent.mkdir(parents=True,exist_ok=True)
    out_npz.parent.mkdir(parents=True,exist_ok=True)
    tmp_json=out_json.with_name(out_json.name+".repair14_tmp")
    tmp_npz=out_npz.with_name(out_npz.stem+".repair14_tmp.npz")

    old_argv=list(sys.argv)
    inner_exit=0
    captured=io.StringIO()
    try:
        sys.argv=[
            str(ROOT/"ge19/repair14_self_consistent_reduced_h3_z20_particular.py"),
            "--results-dir",str(rd),
            "--json-out",str(tmp_json),
            "--npz-out",str(tmp_npz),
        ]
        with contextlib.redirect_stdout(captured):
            try:
                r14.main()
            except SystemExit as exc:
                inner_exit=int(exc.code or 0)
    finally:
        sys.argv=old_argv
        r14.load_module=original_r14_load

    if not tmp_json.exists() or not tmp_npz.exists():
        raise RuntimeError(
            "Repair14 propagation core did not produce temporary outputs; "
            f"inner_exit={inner_exit}; captured_tail={captured.getvalue()[-2000:]}"
        )

    base=json.loads(tmp_json.read_text())

    material=[q for q in collector if parent_index[
        (q["grid"],q["C"],q["beta0"],q["m"])
    ]["material_source_case"]]

    def vmax(key,default=math.inf):
        return float(max((q[key] for q in material),default=default))

    # Primary/control reproduction of the newly reconstructed boundary.
    pmap={(q["grid"],q["C"],q["beta0"],q["m"]):complex_vec(q["p0"]) for q in collector}
    pc=[]
    for tag in ("C_min","C_star","C_max"):
        for beta in (1.0,0.5,0.1):
            for m in range(1,41):
                a=pmap[("primary",tag,beta,m)]
                b=pmap[("control",tag,beta,m)]
                pc.append(rel_l2(a,b))
    pcmax=float(max(pc,default=math.inf))

    boundary={
        "Repair18_JSON_sha256":h18,
        "Repair18_JSON_hash_exact":h18==REPAIR18_JSON_SHA,
        "material_case_count":len(material),
        "all_case_count":len(collector),
        "projected_p0_relative_L2_vs_Repair18_max":vmax("projected_p0_relative_L2_vs_Repair18"),
        "primary_vs_control_projected_p0_relative_L2_max":pcmax,
        "initial_scaled_constraint_relative_residual_max":vmax("scaled_constraint_relative_residual"),
        "initial_lapse_backward_error_max":vmax("lapse_backward_error"),
        "initial_shift_backward_error_max":vmax("shift_backward_error"),
        "initial_anisotropy_backward_error_max":vmax("anisotropy_backward_error"),
        "initial_eliminated_algebraic_relative_residual_max":vmax("eliminated_algebraic_relative_residual"),
        "rank_min":int(min((q["rank"] for q in material),default=0)),
        "rank_max":int(max((q["rank"] for q in material),default=0)),
        "augmented_rank_max":int(max((q["augmented_rank"] for q in material),default=0)),
        "p0_L2_max":vmax("p0_L2"),
        "qdot0_L2_max":vmax("qdot0_L2"),
        "rows":collector,
    }

    bgates={
        "Repair18_parent_hash_exact":bool(boundary["Repair18_JSON_hash_exact"]),
        "Repair18_projected_p0_relative_L2_le_1e12":bool(
            boundary["projected_p0_relative_L2_vs_Repair18_max"]<=P_REPRO_MAX
        ),
        "primary_vs_control_projected_p0_relative_L2_le_1e12":bool(
            pcmax<=PC_P_REPRO_MAX
        ),
        "initial_scaled_constraint_relative_residual_le_1e8":bool(
            boundary["initial_scaled_constraint_relative_residual_max"]<=INIT_CONSTRAINT_RES_MAX
        ),
        "initial_lapse_backward_error_le_1e6":bool(
            boundary["initial_lapse_backward_error_max"]<=INIT_LAPSE_MAX
        ),
        "initial_shift_backward_error_le_1e6":bool(
            boundary["initial_shift_backward_error_max"]<=INIT_SHIFT_MAX
        ),
        "initial_eliminated_algebraic_relative_residual_le_1e8":bool(
            boundary["initial_eliminated_algebraic_relative_residual_max"]<=INIT_ALG_MAX
        ),
        "initial_projected_constraint_rank_eq_2":bool(
            boundary["rank_min"]==2 and boundary["rank_max"]==2 and boundary["augmented_rank_max"]==2
        ),
    }

    stage_gates=dict(base["gates"])
    all_gates={**bgates,**stage_gates}
    passed=bool(all(all_gates.values()))

    base["classification"]=(
        "GE19_REPAIR19_PROJECTED_BOUNDARY_REDUCED_H3_Z20_PROPAGATION_PASS"
        if passed else
        "GE19_REPAIR19_PROJECTED_BOUNDARY_REDUCED_H3_Z20_PROPAGATION_FAIL"
    )
    base["predata_classification"]="GE19_REPAIR19_PREDATA_PROJECTED_BOUNDARY_REDUCED_H3_Z20_PROPAGATION"
    base["scope"]="m=1..40 reduced H3/Z20 propagation on the Repair13 self-consistent background using the certified Repair18 zero-coordinate constraint-projected canonical momentum boundary."
    base["provenance"]["Repair18_JSON_sha256"]=h18
    base["provenance"]["Repair18_projected_boundary_certified"]=True
    base["provenance"]["Repair14_source_construction_reused_without_physics_edit"]=True
    base["initial_boundary_reproduction"]=boundary
    base["window_retarded_convention"]={
        "z_start":1.5,
        "z_end":0.2,
        "dynamic_fields":["S20","u20","phi20","T20"],
        "initial_coordinates":"S20=u20=phi20=T20=0 exactly",
        "initial_canonical_momenta":"Repair18 doubly equilibrated GELSD lapse+shift projection with exactly four refinement sweeps",
        "meaning":"one constraint-compatible window-local particular solution; earlier-time/primordial homogeneous response remains outside the claim",
    }
    base["gates"]=all_gates
    base["project_boundary"]={
        "Repair13_reduced_H1_reclosure_certified":True,
        "Repair18_projected_finite_window_boundary_certified":True,
        "projected_boundary_reduced_H3_Z20_certified":passed,
        "homogeneous_primordial_Z20_certified":False,
        "full_species_Z20_certified":False,
        "physical_amplitude_nonlinear_state_certified":False,
        "q20_ready_after_Z20":passed,
        "Z21_licensed":False,
    }
    base["claim_boundary"]=(
        "PASS certifies only the frozen low-mode constraint-compatible window-local reduced-H3 Z20 particular directional state on the Repair13 background using the Repair18 boundary. "
        "It does not certify the omitted homogeneous/primordial second-order mode, full standard species, finite eta, physical-amplitude nonlinear evolution, collapse, lensing or observations."
    )

    out_json.write_text(json.dumps(base,indent=2,allow_nan=False)+"\n")

    # Preserve Repair14 NPZ payload and append the exact projected boundary.
    with np.load(tmp_npz) as z:
        save={k:z[k] for k in z.files}
    for grid in ("primary","control"):
        for tag in ("C_min","C_star","C_max"):
            pp=np.empty((3,40,4),complex)
            qq=np.empty((3,40,4),complex)
            for ib,beta in enumerate((1.0,0.5,0.1)):
                for jm,m in enumerate(range(1,41)):
                    row=next(q for q in collector if q["grid"]==grid and q["C"]==tag and q["beta0"]==beta and q["m"]==m)
                    pp[ib,jm]=complex_vec(row["p0"])
                    qq[ib,jm]=complex_vec(row["qdot0"])
            save[f"{tag}_projected_p0_{grid}"]=pp
            save[f"{tag}_projected_qdot0_{grid}"]=qq
    np.savez_compressed(out_npz,**save)

    try:
        tmp_json.unlink()
    except FileNotFoundError:
        pass
    try:
        tmp_npz.unlink()
    except FileNotFoundError:
        pass

    print(json.dumps(base,indent=2,allow_nan=False))
    if not passed:
        raise SystemExit(2)


if __name__=="__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:
        print(json.dumps({
            "classification":"GE19_REPAIR19_PROJECTED_BOUNDARY_REDUCED_H3_Z20_PROPAGATION_IMPLEMENTATION_FAIL",
            "error":repr(exc),
        },indent=2))
        raise
