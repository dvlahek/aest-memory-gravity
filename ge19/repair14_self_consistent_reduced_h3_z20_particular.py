#!/usr/bin/env python3
"""GE19 Repair14 self-consistent reduced-H3 Z20 particular solve.

Consumes the frozen Repair13 self-consistent reduced-background H1 PASS
without recomputing H1.  Adds the exact second directional source of

    L_lambda = -6 rho_lambda N L R^2

to the frozen GE06 + GE07 + Y2 H3 source, then solves

    L_total Z20 = -Q_total(Z10,Z10) - 2 Y2[Z10]

with the same Repair11 first-directional Lambda operator and the same
Repair13 AeST+dust+Lambda homogeneous background.

The result is one window-retarded particular directional solution only.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

REPAIR13_JSON_SHA="ae3cc790ecffbd5498b5852273c72ae578d4615de29bbb616673c05cdb3e74b7"
REPAIR13_NPZ_SHA="011c0ae54fd21d70c0e2c695ce62e7b74a3c5529a07c9023c882a447d5b40ca3"
TINY=1.0e-300


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
    aa=np.asarray(a)
    bb=np.asarray(b)
    return float(np.linalg.norm(aa-bb)/max(np.linalg.norm(aa),np.linalg.norm(bb),TINY))


def lambda_c2_equation_source(bg,rho_lambda,real):
    """Exact common-direction second coefficient of the Lambda equations.

    Gauge direction:
      N = 1 + eps N1,
      L = a + eps S1,
      R = a + eps S1.

    Returns the equation coefficient Q_lambda in frozen main-row order:
      lapse, isotropic, aether, scalar, dust-potential, dust-density.
    It is *not* the H3 RHS sign; H3 uses -Q_lambda.
    """
    N=np.asarray(real["N20"],float)
    S=np.asarray(real["S20"],float)
    aa=np.asarray(bg["a"],float)[:,None]
    rr=np.asarray(rho_lambda,float)[:,None]
    if N.shape!=S.shape or N.shape[0]!=len(aa):
        raise RuntimeError("Lambda c2 real-space shape mismatch")

    q=np.zeros((6,)+N.shape,float)
    q[0]=-36.0*rr*aa*S*S
    q[1]=-72.0*rr*aa*N*S-36.0*rr*S*S
    return q


def source_real_reduced_lambda(r7,mod6,mod7,bg,rho_lambda,tag,beta,nx,state,dot):
    base=r7.source_real_reduced(
        mod6,mod7,bg,tag,beta,nx,state,dot
    )
    real,_,_=r7.reduced_state_real(bg,state,nx,dot)
    qlambda=lambda_c2_equation_source(bg,rho_lambda,real)

    rhs=np.asarray(base["rhs"],float).copy()-qlambda
    rhscon=np.asarray(base["rhs_constraint"],float).copy()

    out=dict(base)
    out["rhs"]=rhs
    out["rhs_constraint"]=rhscon
    out["Q_lambda"]=-qlambda
    return out


def rhs_fourier_with_lambda(source,mmax=40):
    out={}
    for key in (
        "rhs","rhs_constraint","Q_ga","Q_matter","Q_lambda","Y_H3"
    ):
        arr=np.asarray(source[key],float)
        hh=np.fft.fft(arr,axis=2)/arr.shape[2]
        out[key]=np.asarray(hh[:,:,0:mmax+1],complex)
    return out


def source_bundle_reduced_lambda(
    r7,mod6,mod7,bg,rho_lambda,tag,nx,state,dot
):
    out={}
    for beta in r7.BETAS:
        out[beta]=rhs_fourier_with_lambda(
            source_real_reduced_lambda(
                r7,mod6,mod7,bg,rho_lambda,tag,beta,nx,state,dot
            )
        )
    return out


def cosine(a,b):
    aa=np.asarray(a,complex).ravel()
    bb=np.asarray(b,complex).ravel()
    den=np.linalg.norm(aa)*np.linalg.norm(bb)
    if den<=TINY:
        return 0.0
    return float(np.real(np.vdot(aa,bb))/den)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--results-dir",default=str(ROOT/"results"))
    ap.add_argument("--json-out",required=True)
    ap.add_argument("--npz-out",required=True)
    args=ap.parse_args()
    rd=Path(args.results_dir)

    required=[
        rd/"ge15_R1_dense_accepted_step_trace.dat",
        rd/"ge15_R1_cli_background.dat",
        rd/"ge19_repair13_self_consistent_reduced_background_h1_reclosure.json",
        rd/"ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz",
    ]
    missing=[str(p) for p in required if not p.exists()]
    if missing:
        raise RuntimeError("missing frozen local inputs: "+", ".join(missing))

    p13j=rd/"ge19_repair13_self_consistent_reduced_background_h1_reclosure.json"
    p13n=rd/"ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz"
    jsha=sha256(p13j)
    nsha=sha256(p13n)
    if jsha!=REPAIR13_JSON_SHA:
        raise RuntimeError(f"Repair13 JSON hash mismatch: {jsha}")
    if nsha!=REPAIR13_NPZ_SHA:
        raise RuntimeError(f"Repair13 NPZ hash mismatch: {nsha}")

    parent=json.loads(p13j.read_text())
    if parent.get("classification")!="GE19_REPAIR13_SELF_CONSISTENT_REDUCED_BACKGROUND_H1_RECLOSURE_PASS":
        raise RuntimeError("Repair13 parent classification mismatch")
    if parent.get("stage_A_pass") is not True:
        raise RuntimeError("Repair13 parent Stage A is not PASS")
    if parent.get("Z20_constructed") is not False:
        raise RuntimeError("Repair13 parent unexpectedly contains Z20")

    r7=load_module(
        ROOT/"ge19/repair07_window_retarded_reduced_h3_z20_particular.py",
        "ge19_repair07_for_repair14",
    )
    r11=load_module(
        ROOT/"ge19/repair11_lambda_inclusive_reduced_h1_reclosure.py",
        "ge19_repair11_for_repair14",
    )
    r13=load_module(
        ROOT/"ge19/repair13_self_consistent_reduced_background_h1_reclosure.py",
        "ge19_repair13_for_repair14",
    )

    mod6_frozen=r7.load_frozen_generator(
        ROOT/"ge06/analytic_aest_directional_source_generator.py",
        "ge19r14_ge06",
    )
    mod6=r7.build_stable_ge06_generator_v2(mod6_frozen)
    mod7=r7.load_frozen_generator(
        ROOT/"ge07/pressureless_matter_directional_source_generator.py",
        "ge19r14_ge07",
    )

    # Reconstruct only the deterministic homogeneous backgrounds.
    # The frozen Repair13 H1 state itself is loaded below and never recomputed.
    dense=rd/"ge15_R1_dense_accepted_step_trace.dat"
    base64,_,_=r7.build_ge15_reference(dense,r7.NT_PRIMARY)
    base32,_,_=r7.build_ge15_reference(dense,r7.NT_CONTROL)
    rho_l64=r11.interp_lambda(rd/"ge15_R1_cli_background.dat",base64["x"])
    rho_l32=r11.interp_lambda(rd/"ge15_R1_cli_background.dat",base32["x"])

    frozen=np.load(p13n)

    if not np.allclose(frozen["x64"],base64["x"],rtol=0.0,atol=1e-14):
        raise RuntimeError("Repair13 x64 mismatch")
    if not np.allclose(frozen["x32"],base32["x"],rtol=0.0,atol=1e-14):
        raise RuntimeError("Repair13 x32 mismatch")
    if not np.allclose(frozen["rho_lambda64"],rho_l64,rtol=0.0,atol=1e-20):
        raise RuntimeError("Repair13 rho_lambda64 mismatch")
    if not np.allclose(frozen["rho_lambda32"],rho_l32,rtol=0.0,atol=1e-20):
        raise RuntimeError("Repair13 rho_lambda32 mismatch")

    bg64={}; bg32={}; background_rows=[]
    lambda_by_bg={}
    h1_64={}; h1_32={}; h1_dot64={}; h1_dot32={}
    h_match_max=0.0
    all_h1_finite=True

    for tag in r7.C_TAGS:
        bg64[tag],d64=r13.reduced_background(r7,base64,tag,rho_l64)
        bg32[tag],d32=r13.reduced_background(r7,base32,tag,rho_l32)

        H64=np.asarray(frozen[f"{tag}_H_reduced_primary"],float)
        H32=np.asarray(frozen[f"{tag}_H_reduced_control"],float)
        hm64=rel_l2(bg64[tag]["H"],H64)
        hm32=rel_l2(bg32[tag]["H"],H32)
        h_match_max=max(h_match_max,hm64,hm32)
        if hm64>1e-14 or hm32>1e-14:
            raise RuntimeError(f"Repair13 reduced H reproduction mismatch for {tag}")

        h1_64[tag]=np.asarray(frozen[f"{tag}_Z10_reduced_primary"],complex)
        h1_32[tag]=np.asarray(frozen[f"{tag}_Z10_reduced_control"],complex)
        h1_dot64[tag]=np.asarray(frozen[f"{tag}_Z10_reduced_dot_primary"],complex)
        h1_dot32[tag]=np.asarray(frozen[f"{tag}_Z10_reduced_dot_control"],complex)

        expected64=(len(r7.FOURIER_N),6,r7.NT_PRIMARY)
        expected32=(len(r7.FOURIER_N),6,r7.NT_CONTROL)
        if h1_64[tag].shape!=expected64 or h1_32[tag].shape!=expected32:
            raise RuntimeError(f"Repair13 frozen H1 shape mismatch for {tag}")
        if h1_dot64[tag].shape!=(len(r7.FOURIER_N),4,r7.NT_PRIMARY):
            raise RuntimeError(f"Repair13 frozen H1-dot primary shape mismatch for {tag}")
        if h1_dot32[tag].shape!=(len(r7.FOURIER_N),4,r7.NT_CONTROL):
            raise RuntimeError(f"Repair13 frozen H1-dot control shape mismatch for {tag}")

        all_h1_finite=bool(
            all_h1_finite
            and np.all(np.isfinite(h1_64[tag]))
            and np.all(np.isfinite(h1_32[tag]))
            and np.all(np.isfinite(h1_dot64[tag]))
            and np.all(np.isfinite(h1_dot32[tag]))
        )

        lambda_by_bg[id(bg64[tag])]=rho_l64
        lambda_by_bg[id(bg32[tag])]=rho_l32
        background_rows.append({
            "C":tag,
            "primary":d64,
            "control":d32,
            "H_reproduction_relative_L2_primary":hm64,
            "H_reproduction_relative_L2_control":hm32,
        })

    # Install exactly the locked Repair11 first-directional Lambda operator
    # into the canonical matrices used by the H3 solve.
    lambda_linear_diag=r11.install_lambda_operator(r7,lambda_by_bg)

    # ------------------------------------------------------------------
    # Stage B source convergence on the frozen Repair13 Z10.
    # ------------------------------------------------------------------
    src1024={}; src2048={}
    spatial_rows=[]
    spatial_max=0.0
    all_sources_finite=True
    zero_mode_rows=[]
    source_piece_norms=[]

    for tag in r7.C_TAGS:
        src1024[tag]=source_bundle_reduced_lambda(
            r7,mod6,mod7,bg64[tag],rho_l64,tag,r7.NX_PRIMARY,
            h1_64[tag],h1_dot64[tag]
        )
        src2048[tag]=source_bundle_reduced_lambda(
            r7,mod6,mod7,bg64[tag],rho_l64,tag,r7.NX_SPATIAL_CONTROL,
            h1_64[tag],h1_dot64[tag]
        )

        for beta in r7.BETAS:
            a=src1024[tag][beta]["rhs"][:,:,1:41]
            b=src2048[tag][beta]["rhs"][:,:,1:41]
            e=rel_l2(a,b)
            spatial_max=max(spatial_max,e)
            spatial_rows.append({
                "C":tag,
                "beta0":beta,
                "relative_L2_m1_40":e,
            })
            all_sources_finite=bool(
                all_sources_finite
                and np.all(np.isfinite(a))
                and np.all(np.isfinite(b))
            )

            z0=src1024[tag][beta]["rhs"][:,:,0]
            zero_mode_rows.append({
                "C":tag,
                "beta0":beta,
                "m0_source_global_L2":float(np.linalg.norm(z0)),
            })

            qga=src1024[tag][beta]["Q_ga"][:,:,1:41]
            qm=src1024[tag][beta]["Q_matter"][:,:,1:41]
            ql=src1024[tag][beta]["Q_lambda"][:,:,1:41]
            yy=src1024[tag][beta]["Y_H3"][:,:,1:41]
            analytic=qga+qm+ql
            source_piece_norms.append({
                "C":tag,
                "beta0":beta,
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

    # ------------------------------------------------------------------
    # Primary H3/Z20 window-retarded particular solve.
    # ------------------------------------------------------------------
    state64_by_C={}
    solve_max=0.0
    shift_max=0.0
    aniso_max=0.0
    solve_rows=[]
    for tag in r7.C_TAGS:
        st,res,con,diag=r7.solve_case_canonical(
            mod6,mod7,bg64[tag],tag,src1024[tag]
        )
        state64_by_C[tag]=st
        solve_max=max(solve_max,float(np.max(res)))
        shift_max=max(shift_max,float(np.max(con[:,:,0])))
        aniso_max=max(aniso_max,float(np.max(con[:,:,1])))
        solve_rows.append({
            "C":tag,
            "linear_system_relative_L2_max":float(np.max(res)),
            "shift_constraint_relative_L2_max":float(np.max(con[:,:,0])),
            "anisotropy_constraint_relative_L2_max":float(np.max(con[:,:,1])),
            "canonical_march_diagnostics":diag,
        })

    # Time-grid control uses the frozen Repair13 Nt=32 H1 parent.
    src32={}
    state32_by_C={}
    time_rows=[]
    time_max=0.0
    control_solve_max=0.0
    control_shift_max=0.0
    control_aniso_max=0.0

    for tag in r7.C_TAGS:
        src32[tag]=source_bundle_reduced_lambda(
            r7,mod6,mod7,bg32[tag],rho_l32,tag,r7.NX_PRIMARY,
            h1_32[tag],h1_dot32[tag]
        )
        st32,res32,con32,diag32=r7.solve_case_canonical(
            mod6,mod7,bg32[tag],tag,src32[tag]
        )
        state32_by_C[tag]=st32
        control_solve_max=max(control_solve_max,float(np.max(res32)))
        control_shift_max=max(control_shift_max,float(np.max(con32[:,:,0])))
        control_aniso_max=max(control_aniso_max,float(np.max(con32[:,:,1])))

        p32=r7.interpolate_state_to(
            bg64[tag]["x"],state64_by_C[tag],bg32[tag]["x"]
        )
        by_field={}
        for iv,name in enumerate(r7.FIELDS):
            ee=rel_l2(p32[:,:,iv,:],st32[:,:,iv,:])
            by_field[name]=ee
            time_max=max(time_max,ee)

        time_rows.append({
            "C":tag,
            "by_field_relative_L2":by_field,
            "max":float(max(by_field.values())),
            "control_linear_system_relative_L2_max":float(np.max(res32)),
            "control_shift_constraint_relative_L2_max":float(np.max(con32[:,:,0])),
            "control_anisotropy_constraint_relative_L2_max":float(np.max(con32[:,:,1])),
            "control_canonical_march_diagnostics":diag32,
        })

    envelope=[]
    for ib,beta in enumerate(r7.BETAS):
        cs=state64_by_C["C_star"][ib]
        envelope.append({
            "beta0":beta,
            "C_min_vs_C_star_global_relative_L2":rel_l2(
                state64_by_C["C_min"][ib],cs
            ),
            "C_max_vs_C_star_global_relative_L2":rel_l2(
                state64_by_C["C_max"][ib],cs
            ),
        })

    beta_rows=[]
    central=state64_by_C["C_star"]
    for ib,beta in enumerate(r7.BETAS):
        beta_rows.append({
            "beta0":beta,
            "state_global_L2":float(np.linalg.norm(central[ib])),
            "relative_to_beta1":rel_l2(central[ib],central[0]),
            "cosine_to_beta1":cosine(central[ib],central[0]),
        })

    all_state_finite=bool(
        all(np.all(np.isfinite(v)) for v in state64_by_C.values())
        and all(np.all(np.isfinite(v)) for v in state32_by_C.values())
    )

    provenance={
        "Repair13_JSON_sha256":jsha,
        "Repair13_JSON_hash_exact":jsha==REPAIR13_JSON_SHA,
        "Repair13_NPZ_sha256":nsha,
        "Repair13_NPZ_hash_exact":nsha==REPAIR13_NPZ_SHA,
        "Repair13_stage_A_parent_PASS":True,
        "Repair13_H_reproduction_relative_L2_max":h_match_max,
        "Repair13_frozen_Z10_loaded_without_H1_recompute":True,
        "Repair13_frozen_Z10_all_finite":all_h1_finite,
        "Lambda_first_directional_operator":"locked Repair11 install_lambda_operator",
        "Lambda_second_directional_source":"exact Repair14 common-direction c2",
    }

    gates={
        "frozen_Repair13_parent_provenance_exact":bool(
            provenance["Repair13_JSON_hash_exact"]
            and provenance["Repair13_NPZ_hash_exact"]
            and h_match_max<=1e-14
            and all_h1_finite
        ),
        "all_sources_finite":bool(all_sources_finite),
        "spatial_N1024_vs_N2048_source_m1_40_global_relative_L2_le_5e4":bool(
            spatial_max<=r7.SOURCE_SPATIAL_MAX
        ),
        "primary_linear_system_relative_L2_residual_le_1e8":bool(
            solve_max<=r7.LINEAR_RES_MAX
        ),
        "shift_constraint_backward_error_le_1e6":bool(
            shift_max<=r7.CONSTRAINT_MAX
        ),
        "anisotropy_constraint_backward_error_le_1e6":bool(
            aniso_max<=r7.CONSTRAINT_MAX
        ),
        "primary64_vs_control32_state_global_relative_L2_le_5e3":bool(
            time_max<=r7.TIME_STATE_MAX
        ),
        "all_three_beta0_and_C_cases_complete":bool(
            len(state64_by_C)==3
            and all(v.shape[0]==3 for v in state64_by_C.values())
        ),
        "all_outputs_finite":bool(all_state_finite),
    }
    passed=bool(all(gates.values()))

    classification=(
        "GE19_REPAIR14_SELF_CONSISTENT_REDUCED_H3_Z20_PARTICULAR_PASS"
        if passed else
        "GE19_REPAIR14_SELF_CONSISTENT_REDUCED_H3_Z20_PARTICULAR_FAIL"
    )

    result={
        "classification":classification,
        "predata_classification":"GE19_REPAIR14_PREDATA_SELF_CONSISTENT_REDUCED_H3_Z20_PARTICULAR",
        "scope":"m=1..40 projection of one window-retarded reduced H3 particular directional state on the certified Repair13 self-consistent background.",
        "equation":"L_total Z20 = -Q_total(Z10,Z10) - 2 Y2[Z10]",
        "provenance":provenance,
        "background":{
            "definition":"H_red^2=(Q K_Q-K)/3+C/a^3+rho_lambda",
            "rows":background_rows,
        },
        "lambda_second_directional_source":{
            "action":"-6 rho_lambda N L R^2",
            "lapse":"-36 rho_lambda a S1^2",
            "longitudinal_scale":"-12 rho_lambda S1^2 - 24 rho_lambda a N1 S1",
            "transverse_scale":"-24 rho_lambda S1^2 - 48 rho_lambda a N1 S1",
            "isotropic":"-36 rho_lambda S1^2 - 72 rho_lambda a N1 S1",
            "shift":"0",
            "anisotropy":"0",
            "H3_rhs_sign":"-Q_lambda",
        },
        "frozen_direction":{
            "k_h_per_Mpc":r7.g9.K_H.tolist(),
            "integer_modes":r7.FOURIER_N.tolist(),
            "phases_rad":r7.PHASES.tolist(),
            "beta0":list(r7.BETAS),
            "C":list(r7.C_TAGS),
            "H3_solved_modes":"m=1..40",
            "m0":"reported source only; no homogeneous/backreaction solve",
        },
        "window_retarded_convention":{
            "z_start":1.5,
            "z_end":0.2,
            "dynamic_fields":["S20","u20","phi20","T20"],
            "initial_conditions":"value=0 and cosmic-time derivative=0 at z=1.5",
            "meaning":"one window-local particular solution; primordial/earlier-time response remains in omitted homogeneous solution",
        },
        "source_spatial_convergence":{
            "primary_Nx":r7.NX_PRIMARY,
            "control_Nx":r7.NX_SPATIAL_CONTROL,
            "relative_L2_max":spatial_max,
            "rows":spatial_rows,
        },
        "source_decomposition":source_piece_norms,
        "unsolved_m0_source":zero_mode_rows,
        "primary_solve_controls":{
            "max_linear_system_relative_L2":solve_max,
            "max_shift_constraint_relative_L2":shift_max,
            "max_anisotropy_constraint_relative_L2":aniso_max,
            "rows":solve_rows,
        },
        "control_solve_controls":{
            "max_linear_system_relative_L2":control_solve_max,
            "max_shift_constraint_relative_L2":control_shift_max,
            "max_anisotropy_constraint_relative_L2":control_aniso_max,
        },
        "time_grid_control":{
            "primary_Nt":r7.NT_PRIMARY,
            "control_Nt":r7.NT_CONTROL,
            "state_relative_L2_max":time_max,
            "rows":time_rows,
        },
        "matter_background_envelope":envelope,
        "beta0_state_dependence":beta_rows,
        "gates":gates,
        "project_boundary":{
            "Repair13_reduced_H1_reclosure_certified":True,
            "window_retarded_reduced_H3_particular_certified":passed,
            "homogeneous_primordial_Z20_certified":False,
            "full_species_Z20_certified":False,
            "physical_amplitude_nonlinear_state_certified":False,
            "q20_ready_after_Z20":passed,
            "Z21_licensed":False,
        },
        "claim_boundary":"PASS certifies only the frozen low-mode window-retarded reduced-H3 particular directional state on the Repair13 self-consistent background. It does not certify the omitted homogeneous/primordial second-order mode, full standard species, finite eta, physical-amplitude nonlinear evolution, collapse, lensing or observations."
    }

    out=Path(args.json_out)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")

    save={
        "beta0":np.asarray(r7.BETAS,float),
        "m":r7.M_SOLVE,
        "field_names":np.asarray(r7.FIELDS,dtype="U32"),
        "ln_a_primary":np.asarray(base64["x"],float),
        "a_primary":np.asarray(base64["a"],float),
        "ln_a_control":np.asarray(base32["x"],float),
        "a_control":np.asarray(base32["a"],float),
        "rho_lambda_primary":rho_l64,
        "rho_lambda_control":rho_l32,
    }
    for tag in r7.C_TAGS:
        save[f"{tag}_H_reduced_primary"]=np.asarray(bg64[tag]["H"],float)
        save[f"{tag}_H_reduced_control"]=np.asarray(bg32[tag]["H"],float)
        save[f"{tag}_Z10_reduced_primary"]=h1_64[tag]
        save[f"{tag}_Z10_reduced_control"]=h1_32[tag]
        save[f"{tag}_Z10_reduced_dot_primary"]=h1_dot64[tag]
        save[f"{tag}_Z10_reduced_dot_control"]=h1_dot32[tag]
        save[f"{tag}_Z20_primary"]=state64_by_C[tag]
        save[f"{tag}_Z20_control"]=state32_by_C[tag]
        for ib,beta in enumerate(r7.BETAS):
            bt=str(beta).replace(".","p")
            src=src1024[tag][beta]
            save[f"{tag}_beta{bt}_rhs_primary_m0_40"]=src["rhs"]
            save[f"{tag}_beta{bt}_Qga_primary_m0_40"]=src["Q_ga"]
            save[f"{tag}_beta{bt}_Qmatter_primary_m0_40"]=src["Q_matter"]
            save[f"{tag}_beta{bt}_Qlambda_primary_m0_40"]=src["Q_lambda"]
            save[f"{tag}_beta{bt}_YH3_primary_m0_40"]=src["Y_H3"]

    np.savez_compressed(args.npz_out,**save)

    print(json.dumps(result,indent=2,allow_nan=False))
    if not passed:
        raise SystemExit(2)


if __name__=="__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:
        print(json.dumps({
            "classification":"GE19_REPAIR14_SELF_CONSISTENT_REDUCED_H3_Z20_PARTICULAR_IMPLEMENTATION_FAIL",
            "error":repr(exc),
        },indent=2))
        raise
