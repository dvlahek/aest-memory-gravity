#!/usr/bin/env python3
"""GE19 Repair12 remaining-standard-momentum audit.

Diagnostic only.  Loads the frozen Repair11 Lambda-inclusive reduced-H1
trajectory, reconstructs the exact same local operator, and asks how the
shift residual changes if only the reduced-dust momentum contribution is
replaced by the frozen full-standard CLASS momentum contribution.

No trajectory is recomputed.  No operator, sign, threshold, background,
C value, DAE partition, H3 source or Z20 object is changed.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

import ge09.repair01_dense_accepted_step_local_jet_bridge as g9
import ge18.repair01_on_shell_matched_dust_first_order_bridge as g18

TINY=1.0e-300

REPAIR11_JSON_SHA="5283dd425864e8f6613678a1ad90a71e2d69243cbecd868685af45c52be077ab"
REPAIR11_NPZ_SHA="ed2431e59d89f820796f6e9b534b8ca19ae026ad55597302bf92ddb120dfec83"
REPAIR11_SHIFT_MAX=5.016294027155656e-5
REPRO_REL_MAX=1.0e-10

SCIENCE_SHIFT_GATE=1.0e-6
CLASS_FLOOR=1.0e-5
DOMINANT_IMPROVEMENT=10.0


def sha256(path:Path)->str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module(path:Path,name:str):
    spec=importlib.util.spec_from_file_location(name,path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def pair_metric(a,b):
    return float(abs(a+b)/max(abs(a),abs(b),TINY))


def state_w(state,dot,imode,it):
    # Frozen Repair07/11 local order:
    # (N,dr,S,u,phi,T,Sdot,udot,phidot,Tdot)
    return np.asarray([
        state[imode,0,it],
        state[imode,5,it],
        state[imode,1,it],
        state[imode,2,it],
        state[imode,3,it],
        state[imode,4,it],
        dot[imode,0,it],
        dot[imode,1,it],
        dot[imode,2,it],
        dot[imode,3,it],
    ],complex)


def positive_mode_series(r7,arr,amp,phase):
    arr=np.asarray(arr,float)
    return r7.positive_mode_coeff(arr,np.zeros_like(arr),amp,phase)


def summary(vals,z):
    vals=np.asarray(vals,float)
    i=int(np.argmax(vals))
    return {
        "initial":float(vals[0]),
        "max":float(vals[i]),
        "max_index":i,
        "max_z":float(z[i]),
        "final":float(vals[-1]),
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--results-dir",default=str(ROOT/"results"))
    ap.add_argument("--json-out",required=True)
    args=ap.parse_args()
    rd=Path(args.results_dir)

    required=[
        rd/"ge15_R1_dense_accepted_step_trace.dat",
        rd/"ge15_R1_cli_background.dat",
        rd/"ge19_repair11_lambda_inclusive_reduced_h1_reclosure.json",
        rd/"ge19_repair11_lambda_inclusive_reduced_h1_reclosure.npz",
    ]+[rd/f"ge15_R1_cli_perturbations_k{i}_s.dat" for i in range(6)]
    missing=[str(p) for p in required if not p.exists()]
    if missing:
        raise RuntimeError("missing frozen inputs: "+", ".join(missing))

    r11_json_path=rd/"ge19_repair11_lambda_inclusive_reduced_h1_reclosure.json"
    r11_npz_path=rd/"ge19_repair11_lambda_inclusive_reduced_h1_reclosure.npz"
    jsha=sha256(r11_json_path)
    nsha=sha256(r11_npz_path)
    if jsha!=REPAIR11_JSON_SHA:
        raise RuntimeError(f"Repair11 JSON hash mismatch: {jsha}")
    if nsha!=REPAIR11_NPZ_SHA:
        raise RuntimeError(f"Repair11 NPZ hash mismatch: {nsha}")

    r11_result=json.loads(r11_json_path.read_text())
    if r11_result.get("classification")!="GE19_REPAIR11_LAMBDA_INCLUSIVE_REDUCED_H1_RECLOSURE_FAIL":
        raise RuntimeError("unexpected Repair11 classification")
    if r11_result.get("stage_A_pass") is not False:
        raise RuntimeError("Repair11 parent unexpectedly reports Stage-A PASS")

    r7=load_module(
        ROOT/"ge19/repair07_window_retarded_reduced_h3_z20_particular.py",
        "ge19_repair07_for_repair12",
    )
    r11=load_module(
        ROOT/"ge19/repair11_lambda_inclusive_reduced_h1_reclosure.py",
        "ge19_repair11_for_repair12",
    )

    mod6_frozen=r7.load_frozen_generator(
        ROOT/"ge06/analytic_aest_directional_source_generator.py",
        "ge19r12_ge06",
    )
    mod6=r7.build_stable_ge06_generator_v2(mod6_frozen)
    mod7=r7.load_frozen_generator(
        ROOT/"ge07/pressureless_matter_directional_source_generator.py",
        "ge19r12_ge07",
    )

    dense=rd/"ge15_R1_dense_accepted_step_trace.dat"
    bg64,_,_=r7.build_ge15_reference(dense,r7.NT_PRIMARY)
    bg32,_,_=r7.build_ge15_reference(dense,r7.NT_CONTROL)

    z64=1.0/np.asarray(bg64["a"],float)-1.0
    z32=1.0/np.asarray(bg32["a"],float)-1.0

    data=np.load(r11_npz_path)
    for key in ("x64","x32","rho_lambda64","rho_lambda32"):
        if key not in data:
            raise RuntimeError(f"Repair11 NPZ missing {key}")
    if not np.allclose(data["x64"],bg64["x"],rtol=0,atol=1e-14):
        raise RuntimeError("Repair11 x64 does not reproduce frozen bg64")
    if not np.allclose(data["x32"],bg32["x"],rtol=0,atol=1e-14):
        raise RuntimeError("Repair11 x32 does not reproduce frozen bg32")

    lambda_by_bg={
        id(bg64):np.asarray(data["rho_lambda64"],float),
        id(bg32):np.asarray(data["rho_lambda32"],float),
    }
    r11.install_lambda_operator(r7,lambda_by_bg)

    # Full-standard CLASS momentum on both frozen grids.
    raw_bg=g18.parse_background(rd/"ge15_R1_cli_background.dat")
    bgi=g18.interp_bg(raw_bg)
    raw_modes=[
        g18.parse_raw_mode(rd/f"ge15_R1_cli_perturbations_k{i}_s.dat")
        for i in range(6)
    ]
    full64=[g18.mode_standard_state(raw_modes[i],bgi,bg64["x"]) for i in range(6)]
    full32=[g18.mode_standard_state(raw_modes[i],bgi,bg32["x"]) for i in range(6)]

    amps,_,_=r7.amplitudes()

    rows=[]
    reproduced_shift_max=0.0
    current_pair_global=0.0
    full_pair_global=0.0
    identity_abs_global=0.0
    correction_to_current_residual_ratio_global=0.0

    for tag in r7.C_TAGS:
        for grid,bg,z,full,suffix in (
            ("primary",bg64,z64,full64,"primary"),
            ("control",bg32,z32,full32,"control"),
        ):
            state=np.asarray(data[f"{tag}_Z10_lambda_{suffix}"],complex)
            dot=np.asarray(data[f"{tag}_Z10_lambda_dot_{suffix}"],complex)

            for imode,m in enumerate(r7.FOURIER_N):
                k=float(g9.K_REQ[imode])
                amp=float(amps[imode])
                phase=float(r7.PHASES[imode])
                mom_pos=positive_mode_series(
                    r7,full[imode]["momentum_std"],amp,phase
                )

                sci=[]
                cur_pair=[]
                full_pair=[]
                abs_current=[]
                abs_full=[]
                abs_corr=[]
                identity_abs=[]
                corr_ratio=[]

                for it,xq in enumerate(np.asarray(bg["x"],float)):
                    w=state_w(state,dot,imode,it)
                    Cmat,bp,_=r7._local_linear_matrix(
                        mod6,mod7,bg,tag,k,float(xq)
                    )

                    sga=Cmat[10]@w
                    sdust=Cmat[11]@w
                    current=sga+sdust

                    met=r7._constraint_backward_error(
                        Cmat[10]+Cmat[11],w,0.0,sga,sdust
                    )
                    sci.append(met["metric"])
                    cur_pair.append(pair_metric(sga,sdust))

                    sfull=-6j*(float(bp["a"])**4)*mom_pos[it]/k
                    fullres=sga+sfull
                    delta=sfull-sdust
                    reconstructed=current+delta

                    full_pair.append(pair_metric(sga,sfull))
                    abs_current.append(float(abs(current)))
                    abs_full.append(float(abs(fullres)))
                    abs_corr.append(float(abs(delta)))
                    identity_abs.append(float(abs(fullres-reconstructed)))
                    corr_ratio.append(float(abs(delta)/max(abs(current),TINY)))

                sci_arr=np.asarray(sci,float)
                cur_arr=np.asarray(cur_pair,float)
                full_arr=np.asarray(full_pair,float)

                reproduced_shift_max=max(
                    reproduced_shift_max,float(np.max(sci_arr))
                )
                current_pair_global=max(
                    current_pair_global,float(np.max(cur_arr))
                )
                full_pair_global=max(
                    full_pair_global,float(np.max(full_arr))
                )
                identity_abs_global=max(
                    identity_abs_global,float(np.max(identity_abs))
                )
                correction_to_current_residual_ratio_global=max(
                    correction_to_current_residual_ratio_global,
                    float(np.max(corr_ratio)),
                )

                rows.append({
                    "C":tag,
                    "grid":grid,
                    "m":int(m),
                    "k_Mpc":k,
                    "repair11_science_shift_metric":summary(sci_arr,z),
                    "repair11_current_pair_metric":summary(cur_arr,z),
                    "full_standard_counterfactual_pair_metric":summary(full_arr,z),
                    "absolute_current_shift_residual":summary(abs_current,z),
                    "absolute_full_standard_shift_residual":summary(abs_full,z),
                    "absolute_omitted_momentum_correction":summary(abs_corr,z),
                    "omitted_correction_over_current_residual":summary(corr_ratio,z),
                    "identity_abs_max":float(np.max(identity_abs)),
                })

    repro_rel=abs(reproduced_shift_max-REPAIR11_SHIFT_MAX)/max(
        abs(REPAIR11_SHIFT_MAX),TINY
    )
    reproduction_pass=bool(repro_rel<=REPRO_REL_MAX)

    improvement=REPAIR11_SHIFT_MAX/max(full_pair_global,TINY)

    if not reproduction_pass:
        classification="GE19_REPAIR12_IMPLEMENTATION_REPRODUCTION_FAIL"
        route="REPAIR12_IMPLEMENTATION_REPRODUCTION_FAIL"
    elif full_pair_global<=SCIENCE_SHIFT_GATE:
        classification="GE19_REPAIR12_REMAINING_STANDARD_MOMENTUM_AUDIT_COMPLETE"
        route="OMITTED_STANDARD_MOMENTUM_EXPLAINS_REMAINING_SHIFT"
    elif improvement>=DOMINANT_IMPROVEMENT and full_pair_global<=CLASS_FLOOR:
        classification="GE19_REPAIR12_REMAINING_STANDARD_MOMENTUM_AUDIT_COMPLETE"
        route="OMITTED_STANDARD_MOMENTUM_DOMINANT_WITH_CLASS_INTERPOLATION_FLOOR"
    else:
        classification="GE19_REPAIR12_REMAINING_STANDARD_MOMENTUM_AUDIT_COMPLETE"
        route="BACKGROUND_OR_REDUCED_DYNAMICS_REMAIN"

    report={
        "classification":classification,
        "predata_classification":"GE19_REPAIR12_PREDATA_REMAINING_STANDARD_MOMENTUM_AUDIT",
        "predata_amendment01":"GE19_REPAIR12_PREDATA_AMENDMENT01_METRIC_AND_REPRODUCTION_LOCK",
        "diagnostic_only":True,
        "repair11_json_sha256":jsha,
        "repair11_npz_sha256":nsha,
        "metric_contract":{
            "repair11_science_shift":"componentwise_backward_error",
            "full_standard_counterfactual":"Repair08 pair metric abs(a+b)/max(abs(a),abs(b),TINY)",
            "full_standard_shift":"-6 i a^4 [(rho+p)theta]_std / k",
        },
        "reproduction":{
            "target_repair11_shift_max":REPAIR11_SHIFT_MAX,
            "reproduced_shift_max":reproduced_shift_max,
            "relative_error":repro_rel,
            "relative_error_limit":REPRO_REL_MAX,
            "pass":reproduction_pass,
        },
        "global":{
            "repair11_shift_science_max":REPAIR11_SHIFT_MAX,
            "repair11_current_pair_metric_max":current_pair_global,
            "full_standard_counterfactual_pair_metric_max":full_pair_global,
            "repair11_science_to_full_counterfactual_improvement_factor":improvement,
            "omitted_correction_identity_abs_max":identity_abs_global,
            "omitted_correction_over_current_residual_ratio_max":correction_to_current_residual_ratio_global,
        },
        "thresholds":{
            "science_shift_gate":SCIENCE_SHIFT_GATE,
            "diagnostic_CLASS_interpolation_floor_reference":CLASS_FLOOR,
            "minimum_dominant_improvement_factor":DOMINANT_IMPROVEMENT,
        },
        "routing":{
            "next_route":route,
            "full_counterfactual_meets_science_gate":bool(
                full_pair_global<=SCIENCE_SHIFT_GATE
            ),
            "full_counterfactual_within_CLASS_floor":bool(
                full_pair_global<=CLASS_FLOOR
            ),
            "dominant_improvement":bool(improvement>=DOMINANT_IMPROVEMENT),
        },
        "per_case":rows,
        "claim_boundary":"Diagnostic attribution of the remaining Repair11 shift residual only. No trajectory, operator, sign, threshold, background, H3 source or Z20 result is changed or licensed."
    }

    out=Path(args.json_out)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2,allow_nan=False)+"\n")
    print(json.dumps(report,indent=2,allow_nan=False))


if __name__=="__main__":
    main()
