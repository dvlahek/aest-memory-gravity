#!/usr/bin/env python3
"""GE18 on-shell matched-dust first-order bridge.

Consumes an already completed local GE15 R1 run. No CLASS execution.

The reduced standard-matter surrogate is an exactly pressureless Newtonian-
gauge dust mode on the frozen GE15 physical metric:
    delta' = -theta + 3 phi'
    theta' = -Hc theta + k^2 psi
with Hc=aH.

At the upper edge z=1.5, absolute density and momentum are matched to the
full standard CLASS sector b+gamma+ur+ncdm. Three frozen dust backgrounds
C_min, C_star, C_max are evolved to propagate the GE17 background truncation
envelope.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import PchipInterpolator

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

import ge09.repair01_dense_accepted_step_local_jet_bridge as g9

C_VALUES={
    "C_min":2.566238549760586e-9,
    "C_star":2.568543329983919e-9,
    "C_max":2.5714842087496506e-9,
}
VARIANT_NAMES=("C_min","C_star","C_max")
PRIMARY_RTOL=1e-11
PRIMARY_ATOL=1e-13
CONTROL_RTOL=2e-12
CONTROL_ATOL=2e-14
PC_GL_MAX=1e-8
PC_MOM_GL_MAX=1e-8
INIT_MAX=1e-10
T_ID_MAX=1e-9
TINY=1e-300


def sha256(path:Path)->str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel_l2(a,b):
    aa=np.asarray(a,float); bb=np.asarray(b,float)
    return float(np.linalg.norm(aa-bb)/max(np.linalg.norm(aa),np.linalg.norm(bb),TINY))


def pointwise_relative(a,b):
    aa=np.asarray(a,float); bb=np.asarray(b,float)
    scale=max(float(np.max(np.abs(aa))),float(np.max(np.abs(bb))),TINY)
    floor=scale*1e-12
    return float(np.max(np.abs(aa-bb)/np.maximum(np.maximum(np.abs(aa),np.abs(bb)),floor)))


def parse_numbered_table(path:Path):
    lines=path.read_text().splitlines()
    hline=next((x for x in lines if x.startswith("#") and "1:" in x),None)
    if hline is None:
        raise RuntimeError(f"missing numbered header in {path}")
    pairs=re.findall(r"(\d+):(.+?)(?=\s+\d+:|$)",hline.lstrip("#").strip())
    if not pairs:
        raise RuntimeError(f"cannot parse numbered header in {path}")
    names={title.strip():int(num)-1 for num,title in pairs}
    data=np.loadtxt(path,comments="#",ndmin=2)
    return names,np.asarray(data,float)


def parse_background(path:Path):
    names,data=parse_numbered_table(path)
    req=(
        "z","H [1/Mpc]","(.)rho_g","(.)rho_b","(.)rho_cdm",
        "(.)rho_ncdm[0]","(.)p_ncdm[0]","(.)rho_ur"
    )
    miss=[x for x in req if x not in names]
    if miss:
        raise RuntimeError(f"background missing {miss}; keys={list(names)}")
    out={k:data[:,names[k]] for k in req}
    out["a"]=1.0/(1.0+out["z"])
    order=np.argsort(out["a"])
    return {k:np.asarray(v[order],float) for k,v in out.items()}


def interp_bg(bg):
    x=np.log(bg["a"])
    return {k:PchipInterpolator(x,v,extrapolate=False) for k,v in bg.items() if k not in ("z","a")}


def parse_raw_mode(path:Path):
    names,data=parse_numbered_table(path)
    req=(
        "tau [Mpc]","a","phi","psi",
        "delta_g","theta_g","delta_b","theta_b",
        "delta_ur","theta_ur","delta_ncdm[0]","theta_ncdm[0]",
        "delta_cdm","theta_cdm"
    )
    miss=[x for x in req if x not in names]
    if miss:
        raise RuntimeError(f"{path.name} missing {miss}; keys={list(names)}")
    out={k:np.asarray(data[:,names[k]],float) for k in req}
    kline=next((x for x in path.read_text().splitlines() if x.startswith("#scalar perturbations for mode k")),None)
    if kline is None:
        raise RuntimeError(f"missing k header {path}")
    mm=re.search(r"k\s*=\s*([0-9eE+\-.]+)",kline)
    if mm is None:
        raise RuntimeError(f"cannot parse k {path}")
    out["k"]=float(mm.group(1))
    return out


def mode_standard_state(mode,bgi,x):
    a=np.exp(x)
    xm=np.log(mode["a"])
    # Late-time scalar outputs are smooth; PCHIP avoids overshoot.
    mi={k:PchipInterpolator(xm,v,extrapolate=False)
        for k,v in mode.items() if isinstance(v,np.ndarray) and k not in ("tau [Mpc]","a")}
    rho_g=np.asarray(bgi["(.)rho_g"](x),float)
    rho_b=np.asarray(bgi["(.)rho_b"](x),float)
    rho_ur=np.asarray(bgi["(.)rho_ur"](x),float)
    rho_n=np.asarray(bgi["(.)rho_ncdm[0]"](x),float)
    p_n=np.asarray(bgi["(.)p_ncdm[0]"](x),float)
    dg=np.asarray(mi["delta_g"](x),float)
    db=np.asarray(mi["delta_b"](x),float)
    dur=np.asarray(mi["delta_ur"](x),float)
    dn=np.asarray(mi["delta_ncdm[0]"](x),float)
    tg=np.asarray(mi["theta_g"](x),float)
    tb=np.asarray(mi["theta_b"](x),float)
    tur=np.asarray(mi["theta_ur"](x),float)
    tn=np.asarray(mi["theta_ncdm[0]"](x),float)
    dr=rho_g*dg+rho_b*db+rho_ur*dur+rho_n*dn
    mom=(4.0/3.0*rho_g)*tg+rho_b*tb+(4.0/3.0*rho_ur)*tur+(rho_n+p_n)*tn
    return {
        "delta_rho_std":dr,
        "momentum_std":mom,
        "rho_std":rho_g+rho_b+rho_ur+rho_n,
        "phi_raw":np.asarray(mi["phi"](x),float),
        "psi_raw":np.asarray(mi["psi"](x),float),
    }


def integrate_dust(metric_interp,k,C,xnodes,std0,rtol,atol):
    x0=float(xnodes[0]); x1=float(xnodes[-1])
    a0=math.exp(x0)
    rho0=C/a0**3
    delta0=float(std0["delta_rho_std"]/rho0)
    theta0=float(std0["momentum_std"]/rho0)

    def rhs(x,y):
        st=g9.eval_state(metric_interp,np.asarray([x]))
        a=math.exp(x)
        H=float(st["H_over_H0"][0]*g9.H0_CLASS)
        calH=a*H
        phi_p=float(st["phi_prime_interp"][0])
        psi=float(st["psi"][0])
        delta,theta=y
        return [
            (-theta+3.0*phi_p)/calH,
            -theta+(k*k/calH)*psi,
        ]

    sol=solve_ivp(
        rhs,(x0,x1),[delta0,theta0],method="DOP853",
        t_eval=np.asarray(xnodes,float),rtol=rtol,atol=atol,
        dense_output=False
    )
    if not sol.success or sol.y.shape!=(2,len(xnodes)):
        raise RuntimeError(f"dust integration failed k={k} C={C}: {sol.message}")
    delta=np.asarray(sol.y[0],float)
    theta=np.asarray(sol.y[1],float)
    a=np.exp(xnodes)
    rho=C/a**3
    dr=rho*delta
    mom=rho*theta
    return {
        "delta":delta,"theta":theta,"rho":rho,
        "delta_rho":dr,"momentum":mom,
    }


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
        rd/"ge15_cancellation_free_s_state_precision_closure.json",
    ]+[rd/f"ge15_R1_cli_perturbations_k{i}_s.dat" for i in range(6)]
    missing=[str(p) for p in required if not p.exists()]
    if missing:
        raise RuntimeError("missing required local GE15 outputs: "+", ".join(missing))

    ge15=json.loads((rd/"ge15_cancellation_free_s_state_precision_closure.json").read_text())
    if ge15.get("classification")!="GE15_CANCELLATION_FREE_S_STATE_PRECISION_CLOSURE_PASS":
        raise RuntimeError(f"local GE15 result is not PASS: {ge15.get('classification')}")
    expected_dense=ge15["precision_binding"]["dense_trace_sha256"]["R1"]
    dense_path=rd/"ge15_R1_dense_accepted_step_trace.dat"
    dense_hash=sha256(dense_path)
    dense_hash_ok=(dense_hash==expected_dense)

    dense_rows=g9.read_table(dense_path)
    modes,kmiss=g9.group_modes(dense_rows)
    primary=[g9.build_interps(m) for m in modes]

    raw=[parse_raw_mode(rd/f"ge15_R1_cli_perturbations_k{i}_s.dat") for i in range(6)]
    class_err,class_counts=g9.class_trace_control(modes,raw)

    bg=parse_background(rd/"ge15_R1_cli_background.dat")
    bgi=interp_bg(bg)

    xnodes=np.linspace(math.log(g9.AMIN),math.log(g9.AMAX),g9.NCOMMON)
    anodes=np.exp(xnodes)

    full=[]
    metric_bg_errors=[]
    for ik,k in enumerate(g9.K_REQ):
        std=mode_standard_state(raw[ik],bgi,xnodes)
        full.append(std)
        st=g9.eval_state(primary[ik],xnodes)
        metric_bg_errors.append(g9.aor(st["phi"],std["phi_raw"]))
        metric_bg_errors.append(g9.aor(st["psi"],std["psi_raw"]))
        # background rho_cdm is AeST dark density in this patched CLASS.
        rho_dark_bg=np.asarray(bgi["(.)rho_cdm"](xnodes),float)
        metric_bg_errors.append(g9.aor(st["rho_dark"],rho_dark_bg))

    variants={}
    pc_density=[]
    pc_momentum=[]
    init_density=[]
    init_momentum=[]
    t_identity=[]
    finite=True

    for tag,C in C_VALUES.items():
        rows=[]
        for ik,k in enumerate(g9.K_REQ):
            std0={q:float(full[ik][q][0]) for q in ("delta_rho_std","momentum_std")}
            pri=integrate_dust(primary[ik],float(k),C,xnodes,std0,PRIMARY_RTOL,PRIMARY_ATOL)
            ctl=integrate_dust(primary[ik],float(k),C,xnodes,std0,CONTROL_RTOL,CONTROL_ATOL)
            pc_density.append(rel_l2(pri["delta_rho"],ctl["delta_rho"]))
            pc_momentum.append(rel_l2(pri["momentum"],ctl["momentum"]))
            init_density.append(abs(pri["delta_rho"][0]-std0["delta_rho_std"])/max(abs(std0["delta_rho_std"]),TINY))
            init_momentum.append(abs(pri["momentum"][0]-std0["momentum_std"])/max(abs(std0["momentum_std"]),TINY))

            st=g9.eval_state(primary[ik],xnodes)
            H=st["H_over_H0"]*g9.H0_CLASS
            calH=anodes*H
            theta=pri["theta"]
            psi=st["psi"]
            dtheta_dx=-theta+(k*k/calH)*psi
            T=anodes*theta/(k*k)
            dTdx=T+anodes*dtheta_dx/(k*k)
            Tdot=H*dTdx
            t_identity.append(g9.aor(Tdot,psi))

            dr_full=full[ik]["delta_rho_std"]
            mom_full=full[ik]["momentum_std"]
            row={
                "k_h_per_Mpc":float(g9.K_H[ik]),
                "k_Mpc":float(k),
                "density_global_relative_L2":rel_l2(pri["delta_rho"],dr_full),
                "density_pointwise_relative_max":pointwise_relative(pri["delta_rho"],dr_full),
                "momentum_global_relative_L2":rel_l2(pri["momentum"],mom_full),
                "momentum_pointwise_relative_max":pointwise_relative(pri["momentum"],mom_full),
                "_primary":pri,
            }
            rows.append(row)
            finite=bool(finite and all(np.all(np.isfinite(v)) for v in pri.values()))
        variants[tag]=rows

    # Global central-model errors, plus envelope spread around central.
    def stack(tag,key):
        return np.concatenate([r["_primary"][key].ravel() for r in variants[tag]])

    full_dr=np.concatenate([q["delta_rho_std"] for q in full])
    full_mom=np.concatenate([q["momentum_std"] for q in full])
    central_dr=stack("C_star","delta_rho")
    central_mom=stack("C_star","momentum")
    global_model={
        "central_density_global_relative_L2":rel_l2(central_dr,full_dr),
        "central_density_pointwise_relative_max":pointwise_relative(central_dr,full_dr),
        "central_momentum_global_relative_L2":rel_l2(central_mom,full_mom),
        "central_momentum_pointwise_relative_max":pointwise_relative(central_mom,full_mom),
        "C_min_vs_central_density_global_relative_L2":rel_l2(stack("C_min","delta_rho"),central_dr),
        "C_max_vs_central_density_global_relative_L2":rel_l2(stack("C_max","delta_rho"),central_dr),
        "C_min_vs_central_momentum_global_relative_L2":rel_l2(stack("C_min","momentum"),central_mom),
        "C_max_vs_central_momentum_global_relative_L2":rel_l2(stack("C_max","momentum"),central_mom),
    }

    # Redshift slices over six modes.
    per_z=[]
    for iz,a in enumerate(anodes):
        z=1.0/a-1.0
        fdr=np.asarray([full[ik]["delta_rho_std"][iz] for ik in range(6)])
        fmo=np.asarray([full[ik]["momentum_std"][iz] for ik in range(6)])
        cdr=np.asarray([variants["C_star"][ik]["_primary"]["delta_rho"][iz] for ik in range(6)])
        cmo=np.asarray([variants["C_star"][ik]["_primary"]["momentum"][iz] for ik in range(6)])
        per_z.append({
            "z":float(z),
            "density_global_relative_L2_across_k":rel_l2(cdr,fdr),
            "momentum_global_relative_L2_across_k":rel_l2(cmo,fmo),
        })

    # GE07 directional arrays. Shape: [variant, k, node].
    ge07={}
    for iv,tag in enumerate(VARIANT_NAMES):
        C=C_VALUES[tag]
        rho=C/anodes**3
        rhob_action=3.0*rho
        ge07[tag]={
            "a":np.broadcast_to(anodes,(6,len(anodes))).copy(),
            "rhob_action":np.broadcast_to(rhob_action,(6,len(anodes))).copy(),
            "dN":np.asarray([g9.eval_state(primary[ik],xnodes)["psi"] for ik in range(6)]),
            "dL":np.asarray([-anodes*g9.eval_state(primary[ik],xnodes)["phi"] for ik in range(6)]),
            "dR":np.asarray([-anodes*g9.eval_state(primary[ik],xnodes)["phi"] for ik in range(6)]),
            "db":np.zeros((6,len(anodes))),
            "drho_action":np.asarray([3.0*variants[tag][ik]["_primary"]["delta_rho"] for ik in range(6)]),
            "dTt":np.asarray([g9.eval_state(primary[ik],xnodes)["psi"] for ik in range(6)]),
            "dTx_sin":np.asarray([
                -anodes*variants[tag][ik]["_primary"]["theta"]/g9.K_REQ[ik]
                for ik in range(6)
            ]),
            "T_cos":np.asarray([
                anodes*variants[tag][ik]["_primary"]["theta"]/(g9.K_REQ[ik]**2)
                for ik in range(6)
            ]),
        }

    gates={
        "local_GE15_classification_PASS":True,
        "R1_dense_trace_hash_matches_GE15_result":bool(dense_hash_ok),
        "dense_trace_vs_raw_CLASS_abs_or_rel_le_1e12":bool(class_err<=1e-12),
        "requested_k_relative_miss_le_1e12":bool(kmiss<=1e-12),
        "metric_and_background_cross_file_abs_or_rel_le_1e8":bool(max(metric_bg_errors)<=1e-8),
        "primary_control_density_global_relative_L2_le_1e8":bool(max(pc_density)<=PC_GL_MAX),
        "primary_control_momentum_global_relative_L2_le_1e8":bool(max(pc_momentum)<=PC_MOM_GL_MAX),
        "initial_absolute_density_match_relative_le_1e10":bool(max(init_density)<=INIT_MAX),
        "initial_absolute_momentum_match_relative_le_1e10":bool(max(init_momentum)<=INIT_MAX),
        "T_potential_dot_equals_psi_abs_or_rel_le_1e9":bool(max(t_identity)<=T_ID_MAX),
        "all_outputs_finite":finite,
    }
    passed=bool(all(gates.values()))

    # Remove private arrays from JSON rows.
    public_variants={}
    for tag,rows in variants.items():
        public_variants[tag]=[{k:v for k,v in r.items() if k!="_primary"} for r in rows]

    result={
        "classification":(
            "GE18_ON_SHELL_MATCHED_DUST_FIRST_ORDER_BRIDGE_PASS"
            if passed else
            "GE18_ON_SHELL_MATCHED_DUST_FIRST_ORDER_BRIDGE_FAIL"
        ),
        "predata_classification":"GE18_PREDATA_ON_SHELL_MATCHED_DUST_FIRST_ORDER_BRIDGE",
        "scope":"Local post-GE15 construction of an exactly on-shell pressureless standard-matter surrogate; no CLASS execution and no model-error acceptance gate.",
        "input_provenance":{
            "ge15_result_classification":ge15["classification"],
            "R1_dense_sha256":dense_hash,
            "expected_R1_dense_sha256":expected_dense,
            "class_trace_control_abs_or_rel_max":class_err,
            "metric_background_cross_file_abs_or_rel_max":max(metric_bg_errors),
        },
        "dust_background_CLASS_units":C_VALUES,
        "integrator_controls":{
            "primary":{"method":"DOP853","rtol":PRIMARY_RTOL,"atol":PRIMARY_ATOL},
            "control":{"method":"DOP853","rtol":CONTROL_RTOL,"atol":CONTROL_ATOL},
            "density_primary_control_global_relative_L2_max":max(pc_density),
            "momentum_primary_control_global_relative_L2_max":max(pc_momentum),
        },
        "exact_map":{
            "action_background_varrho":"3 C/a^3",
            "action_density_direction":"3 rho_d delta_d",
            "T_cos":"a theta_d/k^2",
            "T_t_direction":"psi",
            "T_x_sine_coefficient":"-a theta_d/k",
            "T_potential_dot_equals_psi_abs_or_rel_max":max(t_identity),
        },
        "global_model_error":global_model,
        "per_k_model_error":public_variants,
        "per_redshift_model_error":per_z,
        "gates":gates,
        "project_boundary":{
            "on_shell_reduced_dust_Z10_certified":passed,
            "effective_dust_declared_exact":False,
            "model_error_acceptance_gate_applied":False,
            "reduced_H3_Z20_input_bridge_ready":passed,
            "full_species_Z20_licensed":False,
        },
        "claim_boundary":"PASS certifies the internally consistent pressureless Z10 matter surrogate and GE07 variable map. Its distance from full standard CLASS matter remains an explicit systematic to propagate through the later reduced-H3 Z20 envelope.",
    }

    outj=Path(args.json_out); outj.parent.mkdir(parents=True,exist_ok=True)
    outj.write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
    save={
        "k_h_Mpc":g9.K_H,"k_Mpc":g9.K_REQ,"ln_a":xnodes,"a":anodes,
    }
    for tag in VARIANT_NAMES:
        for name,arr in ge07[tag].items():
            save[f"{tag}_{name}"]=np.asarray(arr,float)
        save[f"{tag}_delta_d"]=np.asarray([variants[tag][ik]["_primary"]["delta"] for ik in range(6)])
        save[f"{tag}_theta_d"]=np.asarray([variants[tag][ik]["_primary"]["theta"] for ik in range(6)])
        save[f"{tag}_delta_rho_d"]=np.asarray([variants[tag][ik]["_primary"]["delta_rho"] for ik in range(6)])
        save[f"{tag}_momentum_d"]=np.asarray([variants[tag][ik]["_primary"]["momentum"] for ik in range(6)])
    save["full_standard_delta_rho"]=np.asarray([q["delta_rho_std"] for q in full])
    save["full_standard_momentum"]=np.asarray([q["momentum_std"] for q in full])
    np.savez_compressed(args.npz_out,**save)

    print(json.dumps(result,indent=2,allow_nan=False))
    if not passed:
        raise SystemExit(2)


if __name__=="__main__":
    main()
