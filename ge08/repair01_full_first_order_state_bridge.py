#!/usr/bin/env python3
"""GE08 Repair01 full first-order eta=0 state bridge audit.

Runs the pinned patched CLASS/AeST baseline once, records both the historical
accepted-source-grid chi/Q trace and the new diagnostic full-state trace, and
checks the exact Newtonian-gauge -> longitudinal 3+1 dictionary.

Repair01 preserves the parent state trace and replaces only the invalid
source-callback dy equality gates with static physical-RHS and NDF15 callback
semantics checks. No physics equation is modified here.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
from pathlib import Path

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

import v063.theory_response_map as v63
import nl1c4.expanding_memory_source_trajectory as c4

KB=0.0665
TOL=1.0e-12
ZMIN,ZMAX=0.2,1.5
TINY=1.0e-300
K_TARGET=c4.K_MPC.copy()


def read_space_table(path: Path):
    with path.open(newline="") as f:
        reader=csv.DictReader(f,delimiter=" ",skipinitialspace=True)
        if reader.fieldnames is None:
            raise RuntimeError(f"missing header in {path}")
        rows=[]
        for rr in reader:
            try:
                row={k:float(rr[k]) for k in reader.fieldnames}
            except Exception:
                continue
            if all(np.isfinite(list(row.values()))):
                rows.append(row)
    if not rows:
        raise RuntimeError(f"empty table {path}")
    return rows


def aor_metric(a,b):
    aa=np.asarray(a,float); bb=np.asarray(b,float)
    ae=np.abs(aa-bb)
    re=ae/np.maximum(np.maximum(np.abs(aa),np.abs(bb)),TINY)
    return float(np.max(np.minimum(ae,re)))


def rel_l2(a,b=None):
    aa=np.asarray(a,float)
    if b is None:
        return float(np.linalg.norm(aa))
    bb=np.asarray(b,float)
    return float(np.linalg.norm(aa-bb)/max(np.linalg.norm(aa),np.linalg.norm(bb),TINY))


def nearest_rel(x,grid):
    grid=np.asarray(grid,float)
    i=int(np.argmin(np.abs(grid-float(x))))
    return i,float(abs(grid[i]-float(x))/max(abs(float(x)),TINY))


def select_window(rows):
    out=[]
    kmiss=0.0
    for row in rows:
        ik,miss=nearest_rel(row["k"],K_TARGET)
        if miss>TOL:
            continue
        z=1.0/row["a"]-1.0
        if z<ZMIN-1e-12 or z>ZMAX+1e-12:
            continue
        q=dict(row)
        q["target_k_index"]=ik
        q["z"]=z
        out.append(q)
        kmiss=max(kmiss,miss)
    if not out:
        raise RuntimeError("empty GE08 selected full-state window")
    return out,kmiss


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--class-root",required=True)
    ap.add_argument("--json-out",required=True)
    ap.add_argument("--npz-out",required=True)
    args=ap.parse_args()

    class_root=Path(args.class_root).resolve()
    out_json=Path(args.json_out)
    out_npz=Path(args.npz_out)
    out_json.parent.mkdir(parents=True,exist_ok=True)

    legacy=ROOT/"results"/"ge08_legacy_chi_trace.dat"
    full=ROOT/"results"/"ge08_full_state_trace.dat"
    for p in (legacy,full):
        if p.exists(): p.unlink()

    saved={
        "AEST_OFFLINE_TRACE_FILE":os.environ.get("AEST_OFFLINE_TRACE_FILE"),
        "AEST_FULL_STATE_TRACE_FILE":os.environ.get("AEST_FULL_STATE_TRACE_FILE"),
        "AEST_TANGENT_FORCE_FILE":os.environ.get("AEST_TANGENT_FORCE_FILE"),
        "AEST_TANGENT_LAMBDA":os.environ.get("AEST_TANGENT_LAMBDA"),
        "OMP_NUM_THREADS":os.environ.get("OMP_NUM_THREADS"),
    }
    try:
        os.environ["AEST_OFFLINE_TRACE_FILE"]=str(legacy.resolve())
        os.environ["AEST_FULL_STATE_TRACE_FILE"]=str(full.resolve())
        os.environ.pop("AEST_TANGENT_FORCE_FILE",None)
        os.environ.pop("AEST_TANGENT_LAMBDA",None)
        os.environ["OMP_NUM_THREADS"]="1"

        from classy import Class
        pars=dict(v63.class_params())
        pars["output"]="mPk"
        pars["lensing"]="no"
        pars["k_output_values"]=", ".join(f"{x:.17g}" for x in K_TARGET)
        pars["P_k_max_h/Mpc"]=2.0
        pars["z_max_pk"]=5.0

        cc=Class()
        cc.set(pars)
        cc.compute()
        sources,source_k,source_tau=cc.get_sources()
        if "delta_m" not in sources:
            raise RuntimeError(f"CLASS delta_m source missing; keys={sorted(sources)}")
        source_k=np.asarray(source_k,float)
        source_tau=np.asarray(source_tau,float)
        source_dm=np.asarray(sources["delta_m"],float)
        if source_dm.shape!=(source_k.size,source_tau.size):
            raise RuntimeError(f"unexpected delta_m source shape {source_dm.shape}")
        cc.struct_cleanup()
        cc.empty()
    finally:
        for key,val in saved.items():
            if val is None: os.environ.pop(key,None)
            else: os.environ[key]=val

    old_rows=read_space_table(legacy)
    full_rows=read_space_table(full)

    # The legacy and GE08 hooks run once inside the same accepted source call.
    sequence_shape_pass=len(old_rows)==len(full_rows)
    nseq=min(len(old_rows),len(full_rows))
    seq_grid_err=math.inf
    chi_err=math.inf
    if nseq>0:
        old_k=np.asarray([r["k"] for r in old_rows[:nseq]])
        full_k=np.asarray([r["k"] for r in full_rows[:nseq]])
        old_tau=np.asarray([r["tau"] for r in old_rows[:nseq]])
        full_tau=np.asarray([r["tau"] for r in full_rows[:nseq]])
        seq_grid_err=max(aor_metric(old_k,full_k),aor_metric(old_tau,full_tau))
        old_chi=np.asarray([r["chi"] for r in old_rows[:nseq]])
        chi_re=np.asarray([
            r["Q"]*(r["a"]*r["theta_dark"]/(r["k"]*r["k"])+r["alpha_aest"])
            for r in full_rows[:nseq]
        ])
        chi_err=aor_metric(old_chi,chi_re)

    alpha_id_err=aor_metric(
        [r["alpha_prime_dy"] for r in full_rows],
        [r["a"]*(r["E_aest"]-r["psi_newtonian"]) for r in full_rows],
    )
    phi_id_err=aor_metric(
        [r["phi_prime_dy"] for r in full_rows],
        [r["phi_prime_conformal"] for r in full_rows],
    )

    # Repair01: certify the actual physical RHS identities in the pinned,
    # patched source tree and separately certify the NDF15 output-callback
    # semantics that made the parent numerical dy gate invalid.
    pert_txt=(class_root/"source"/"perturbations.c").read_text()
    ndf_txt=(class_root/"tools"/"evolver_ndf15.c").read_text()
    rhs_semantics={
        "phi_physical_rhs_identity_present": (
            "dy[pv->index_pt_phi] = pvecmetric[ppw->index_mt_phi_prime];" in pert_txt
        ),
        "alpha_physical_rhs_identity_present": (
            "dy[pv->index_pt_alpha_aest] = a*(E_aest-psi_aest);" in pert_txt
        ),
        "ndf15_interpolates_output_derivative": (
            "interp_from_dif(t_vec[next],tnew,ynew,h,dif,k,yinterp,ypinterp,yppinterp,interpidx,neq,2);" in ndf_txt
        ),
        "ndf15_passes_ypinterp_to_output": (
            "(*output)(t_vec[next],yinterp+1,ypinterp+1,next,parameters_and_workspace_for_derivs" in ndf_txt
        ),
    }

    selected,k_miss=select_window(full_rows)

    # Match traced ppw->delta_m against the actual CLASS native source table.
    dm_trace=[]
    dm_source=[]
    tau_miss=0.0
    source_k_miss=0.0
    for r in selected:
        ik,ek=nearest_rel(r["k"],source_k)
        it,et=nearest_rel(r["tau"],source_tau)
        source_k_miss=max(source_k_miss,ek)
        tau_miss=max(tau_miss,et)
        dm_trace.append(r["delta_m_native"])
        dm_source.append(source_dm[ik,it])
    dm_err=aor_metric(dm_trace,dm_source)

    # Matter exactness after subtracting the AeST effective-dark contribution.
    std_drho=[]; std_mom=[]; std_dp=[]; std_shear=[]; baryon_drho=[]
    bridge_arrays={
        "k":[],"tau":[],"a":[],"z":[],
        "deltaN":[],"deltaL_over_a":[],"deltaR_over_a":[],"shift_b":[],
        "alpha_aest":[],"E_aest":[],"uA":[],"varphi":[],"chi":[],
        "rapidity_gradient_amplitude":[],
        "delta_dark":[],"theta_dark":[],"delta_b":[],"theta_b":[],
        "delta_m_native":[],"theta_m_native":[],
    }
    for r in selected:
        k=r["k"]; a=r["a"]; Q=r["Q"]
        chi=Q*(a*r["theta_dark"]/(k*k)+r["alpha_aest"])
        Pi_dark=(
            r["cad2_dark"]*r["delta_dark"]
            + r["cad2_dark"]*k*k/(3.0*a*a*r["rho_dark"])
              *(KB*r["E_aest"]+(2.0-KB)*chi)
        )
        dr=r["total_delta_rho"]-r["rho_dark"]*r["delta_dark"]
        mm=r["total_rho_plus_p_theta"]-(r["rho_dark"]+r["p_dark"])*r["theta_dark"]
        dp=r["total_delta_p"]-r["rho_dark"]*Pi_dark
        sh=r["total_rho_plus_p_shear"]
        std_drho.append(dr); std_mom.append(mm); std_dp.append(dp); std_shear.append(sh)
        baryon_drho.append(r["rho_b"]*r["delta_b"])

        uA=a*r["theta_dark"]/(k*k)
        bridge_arrays["k"].append(k)
        bridge_arrays["tau"].append(r["tau"])
        bridge_arrays["a"].append(a)
        bridge_arrays["z"].append(r["z"])
        bridge_arrays["deltaN"].append(r["psi_newtonian"])
        bridge_arrays["deltaL_over_a"].append(-r["phi_newtonian"])
        bridge_arrays["deltaR_over_a"].append(-r["phi_newtonian"])
        bridge_arrays["shift_b"].append(0.0)
        bridge_arrays["alpha_aest"].append(r["alpha_aest"])
        bridge_arrays["E_aest"].append(r["E_aest"])
        bridge_arrays["uA"].append(uA)
        bridge_arrays["varphi"].append(Q*uA)
        bridge_arrays["chi"].append(chi)
        bridge_arrays["rapidity_gradient_amplitude"].append((k/a)*r["alpha_aest"])
        bridge_arrays["delta_dark"].append(r["delta_dark"])
        bridge_arrays["theta_dark"].append(r["theta_dark"])
        bridge_arrays["delta_b"].append(r["delta_b"])
        bridge_arrays["theta_b"].append(r["theta_b"])
        bridge_arrays["delta_m_native"].append(r["delta_m_native"])
        bridge_arrays["theta_m_native"].append(r["theta_m_native"])

    std_drho=np.asarray(std_drho,float)
    std_mom=np.asarray(std_mom,float)
    std_dp=np.asarray(std_dp,float)
    std_shear=np.asarray(std_shear,float)
    baryon_drho=np.asarray(baryon_drho,float)

    pressure_ratio=rel_l2(std_dp)/max(rel_l2(std_drho),TINY)
    shear_ratio=rel_l2(std_shear)/max(rel_l2(std_drho),TINY)
    non_baryon_density_ratio=rel_l2(std_drho,baryon_drho)
    pressureless_ready=bool(pressure_ratio<=TOL and shear_ratio<=TOL)

    finite=bool(
        all(np.all(np.isfinite(np.asarray(v,float))) for v in bridge_arrays.values())
        and np.all(np.isfinite(std_drho))
        and np.all(np.isfinite(std_dp))
        and np.all(np.isfinite(std_shear))
    )

    # Count distinct accepted native times in the requested k-z window.
    times=sorted({round(float(r["tau"]),12) for r in selected})
    bridge_gates={
        "legacy_and_full_trace_sequence_count_equal":bool(sequence_shape_pass),
        "legacy_and_full_trace_grid_abs_or_rel_le_1e12":bool(seq_grid_err<=TOL),
        "old_chi_trace_reproduction_abs_or_rel_le_1e12":bool(chi_err<=TOL),
        "phi_physical_rhs_identity_present":bool(rhs_semantics["phi_physical_rhs_identity_present"]),
        "alpha_physical_rhs_identity_present":bool(rhs_semantics["alpha_physical_rhs_identity_present"]),
        "ndf15_interpolates_output_derivative":bool(rhs_semantics["ndf15_interpolates_output_derivative"]),
        "ndf15_passes_ypinterp_to_output":bool(rhs_semantics["ndf15_passes_ypinterp_to_output"]),
        "native_delta_m_trace_vs_CLASS_source_abs_or_rel_le_1e12":bool(dm_err<=TOL),
        "requested_k_relative_miss_le_1e12":bool(max(k_miss,source_k_miss)<=TOL),
        "common_native_tau_relative_mismatch_le_1e12":bool(tau_miss<=TOL),
        "minimum_8_native_times":bool(len(times)>=8),
        "all_traced_values_finite":finite,
    }
    bridge_pass=bool(all(bridge_gates.values()))

    if not bridge_pass:
        classification="GE08_REPAIR01_FULL_FIRST_ORDER_STATE_BRIDGE_FAIL"
    elif pressureless_ready:
        classification="GE08_REPAIR01_FULL_FIRST_ORDER_STATE_BRIDGE_H3_READY"
    else:
        classification="GE08_REPAIR01_FULL_FIRST_ORDER_STATE_BRIDGE_PASS_MATTER_INCOMPLETE"

    result={
        "classification":classification,
        "predata_classification":"GE08_REPAIR01_PREDATA_SOURCE_DERIVATIVE_SEMANTICS",
        "scope":"GE08 Repair01 diagnostic eta=0 first-order state bridge with corrected source-callback derivative semantics and unchanged exact pressureless-matter completeness audit; no Z20/Z21 solve.",
        "trace_counts":{
            "legacy_rows":len(old_rows),
            "full_rows":len(full_rows),
            "selected_rows":len(selected),
            "distinct_native_times_in_window":len(times),
        },
        "dictionary":{
            "deltaN":"psi_newtonian",
            "deltaL_over_a":"-phi_newtonian",
            "deltaR_over_a":"-phi_newtonian",
            "shift_b":"0 in Newtonian gauge",
            "uA":"a theta_dark/k^2",
            "varphi":"Q uA",
            "chi":"varphi+Q alpha_aest",
            "rapidity":"a r=partial_x alpha, so Fourier gradient amplitude |r|=(k/a)|alpha| with derivative phase retained in real-space reconstruction",
            "alpha_prime":"a(E_aest-psi)",
        },
        "bridge_errors":{
            "legacy_full_grid_abs_or_rel_max":seq_grid_err,
            "chi_abs_or_rel_max":chi_err,
            "parent_callback_alpha_prime_dy_mismatch_descriptive":alpha_id_err,
            "parent_callback_phi_prime_dy_mismatch_descriptive":phi_id_err,
            "delta_m_native_abs_or_rel_max":dm_err,
            "requested_k_relative_miss_max":max(k_miss,source_k_miss),
            "native_tau_relative_mismatch_max":tau_miss,
        },
        "source_derivative_semantics":rhs_semantics,
        "matter_completeness":{
            "standard_pressure_relative_L2_to_standard_density":pressure_ratio,
            "standard_shear_relative_L2_to_standard_density":shear_ratio,
            "standard_density_vs_baryon_only_relative_L2":non_baryon_density_ratio,
            "exact_pressureless_limit":TOL,
            "pressureless_H3_ready":pressureless_ready,
            "interpretation":"If false, the full CLASS late-time standard-matter state contains non-dust stress and cannot be represented exactly by the single GE07 pressureless action without a separately preregistered approximation or additional matter source blocks.",
        },
        "bridge_gates":bridge_gates,
        "project_boundary":{
            "first_order_state_bridge_certified":bridge_pass,
            "full_CLASS_pressureless_basic_state_ready":bool(bridge_pass and pressureless_ready),
            "complete_GE06_local_jet_certified":False,
            "local_jet_completion_required":True,
            "Z20_solve_licensed_on_full_CLASS_reference":False,
            "finite_eta_licensed":False,
        },
        "historical_parent_classification":"GE08_FULL_FIRST_ORDER_STATE_BRIDGE_FAIL",
        "claim_boundary":"Repair01 certifies only the basic first-order state dictionary and exact matter-completeness status. It does not certify the complete GE06 local jet, solve Z20/Z21, introduce finite eta, or establish nonlinear-collapse/observational claims.",
    }

    out_json.write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
    np.savez_compressed(
        out_npz,
        **{k:np.asarray(v,float) for k,v in bridge_arrays.items()},
        standard_delta_rho=std_drho,
        standard_momentum=std_mom,
        standard_delta_p=std_dp,
        standard_shear=std_shear,
        baryon_delta_rho=baryon_drho,
    )
    print(json.dumps(result,indent=2,allow_nan=False))
    if not bridge_pass:
        raise SystemExit(2)


if __name__=="__main__":
    main()
