#!/usr/bin/env python3
"""GE17 diagnostic-only late-time standard-background dust audit.

Runs the pinned patched CLASS background only. The standard sector is the
non-AeST, non-vacuum CLASS background:
  b + gamma + ur + ncdm.
No approximation is accepted by this script.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
from scipy.interpolate import PchipInterpolator, CubicSpline

ZMIN,ZMAX=0.2,1.5
AUDIT_Z=np.asarray([0.247619,0.312010,0.451160,0.604190,0.772470,0.957560,1.161170,1.385240],float)
TINY=1e-300
PINNED_CLASS="e85808324f51fc694d12e3ed7439552a3c3f9540"


def rel_l2(a,b):
    aa=np.asarray(a,float); bb=np.asarray(b,float)
    return float(np.linalg.norm(aa-bb)/max(np.linalg.norm(aa),np.linalg.norm(bb),TINY))


def ratio_l2(num,den):
    return float(np.linalg.norm(np.asarray(num,float))/max(np.linalg.norm(np.asarray(den,float)),TINY))


def safe_abs_ratio(num,den):
    return np.abs(np.asarray(num,float))/np.maximum(np.abs(np.asarray(den,float)),TINY)


def required_key(bg,key):
    if key not in bg:
        raise RuntimeError(f"missing CLASS background column {key}; available={sorted(bg)}")
    return np.asarray(bg[key],float)


def interp_at_z(z,y):
    z=np.asarray(z,float); y=np.asarray(y,float)
    order=np.argsort(z)
    zz=z[order]; yy=y[order]
    return np.asarray(PchipInterpolator(zz,yy,extrapolate=False)(AUDIT_Z),float)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--class-root",required=True)
    ap.add_argument("--json-out",required=True)
    ap.add_argument("--npz-out",required=True)
    args=ap.parse_args()

    from classy import Class

    pars={
        "H0":67.3324639084866,
        "omega_b":0.02238280,
        "N_ur":2.046,
        "omega_cdm":0.1201075,
        "N_ncdm":1,
        "m_ncdm":0.06,
        "T_ncdm":0.7137658555036082,
        "YHe":0.2454006,
        "tau_reio":0.05430842,
        "gauge":"newtonian",
        "aest_enabled":"yes",
        "aest_model":"Exp",
        "aest_KB":0.0665,
        "aest_Q0":1e-4,
        "aest_K2":9500,
        "aest_Z0":1e-17,
    }

    c=Class()
    c.set(pars)
    c.compute()
    bg=c.get_background()
    c.struct_cleanup()
    c.empty()

    required=[
        "z","(.)rho_g","(.)rho_b","(.)rho_cdm","(.)rho_ncdm[0]",
        "(.)p_ncdm[0]","(.)rho_lambda","(.)rho_ur","(.)rho_tot","(.)p_tot"
    ]
    missing=[k for k in required if k not in bg]
    columns_ok=not missing
    if missing:
        raise RuntimeError(f"missing background columns {missing}; available={sorted(bg)}")

    z=required_key(bg,"z")
    a=1.0/(1.0+z)
    rho_g=required_key(bg,"(.)rho_g")
    rho_b=required_key(bg,"(.)rho_b")
    rho_aest=required_key(bg,"(.)rho_cdm")
    rho_n=required_key(bg,"(.)rho_ncdm[0]")
    p_n=required_key(bg,"(.)p_ncdm[0]")
    rho_l=required_key(bg,"(.)rho_lambda")
    rho_ur=required_key(bg,"(.)rho_ur")
    rho_tot=required_key(bg,"(.)rho_tot")
    p_tot=required_key(bg,"(.)p_tot")

    rho_std=rho_b+rho_g+rho_ur+rho_n
    p_std=rho_g/3.0+rho_ur/3.0+p_n
    rho_cluster=rho_std+rho_aest
    rho_reconstructed=rho_cluster+rho_l
    p_aest_inferred=p_tot-p_std+rho_l

    total_recon=rel_l2(rho_tot,rho_reconstructed)

    finite_all=bool(all(np.all(np.isfinite(x)) for x in (
        z,a,rho_g,rho_b,rho_aest,rho_n,p_n,rho_l,rho_ur,
        rho_tot,p_tot,rho_std,p_std,rho_cluster,p_aest_inferred
    )))

    mask=(z>=ZMIN-1e-14)&(z<=ZMAX+1e-14)
    idx=np.where(mask)[0]
    if idx.size==0:
        raise RuntimeError("empty frozen GE17 redshift window")

    zw=z[idx]; aw=a[idx]
    rs=rho_std[idx]; ps=p_std[idx]
    rc=rho_cluster[idx]; rt=rho_tot[idx]
    ra=rho_aest[idx]; pa=p_aest_inferred[idx]

    w=ps/rs
    p_over_cluster=ps/rc
    p_over_total=ps/rt

    C=aw**3*rs
    Cstar=float(np.mean(C))
    rho_dust=Cstar/aw**3
    C_variation=float(np.max(C)/np.min(C)-1.0)
    dust_gl=rel_l2(rs,rho_dust)
    dust_pt=float(np.max(safe_abs_ratio(rs-rho_dust,rs)))

    # Numerical continuity check on the full native background table, then
    # inspect only the frozen window. Spline derivative avoids edge artifacts.
    order=np.argsort(a)
    lna=np.log(a[order]); lnr=np.log(rho_std[order])
    dlnrho=CubicSpline(lna,lnr,bc_type="natural").derivative()(lna)
    cont_num=dlnrho+3.0
    cont_expected=-3.0*(p_std[order]/rho_std[order])
    z_order=z[order]
    morder=(z_order>=ZMIN-1e-14)&(z_order<=ZMAX+1e-14)
    cont_rel=rel_l2(cont_num[morder],cont_expected[morder])

    # Frozen audit-redshift interpolation from native background.
    audit={}
    fields={
        "rho_std":rho_std,
        "p_std":p_std,
        "rho_aest":rho_aest,
        "rho_cluster":rho_cluster,
        "rho_tot":rho_tot,
        "p_aest_inferred":p_aest_inferred,
        "w_std":p_std/rho_std,
        "p_std_over_rho_cluster":p_std/rho_cluster,
        "p_std_over_rho_tot":p_std/rho_tot,
        "C_a3rho_std":a**3*rho_std,
    }
    interp={name:interp_at_z(z,val) for name,val in fields.items()}
    for i,zz in enumerate(AUDIT_Z):
        audit[str(float(zz))]={name:float(val[i]) for name,val in interp.items()}

    summary={
        "native_rows_in_window":int(idx.size),
        "w_std_global_L2_ratio":ratio_l2(ps,rs),
        "w_std_abs_max":float(np.max(np.abs(w))),
        "p_std_over_rho_cluster_global_L2_ratio":ratio_l2(ps,rc),
        "p_std_over_rho_cluster_abs_max":float(np.max(np.abs(p_over_cluster))),
        "p_std_over_rho_tot_global_L2_ratio":ratio_l2(ps,rt),
        "p_std_over_rho_tot_abs_max":float(np.max(np.abs(p_over_total))),
        "C_a3rho_std_variation_max_over_min_minus_1":C_variation,
        "best_constant_C":Cstar,
        "best_conserved_dust_density_global_relative_L2":dust_gl,
        "best_conserved_dust_density_pointwise_relative_max":dust_pt,
        "continuity_numeric_vs_minus3w_global_relative_L2":cont_rel,
        "aest_w_inferred_global_L2_ratio":ratio_l2(pa,ra),
        "aest_w_inferred_abs_max":float(np.max(np.abs(pa/ra))),
    }

    gates={
        "exact_pinned_CLASS_commit_declared":True,
        "all_required_background_columns_present":bool(columns_ok),
        "at_least_64_native_background_rows_in_window":bool(idx.size>=64),
        "total_density_species_reconstruction_relative_L2_le_1e12":bool(total_recon<=1e-12),
        "continuity_identity_global_relative_L2_le_1e5":bool(cont_rel<=1e-5),
        "all_outputs_finite":finite_all and all(np.isfinite(list(summary.values()))),
    }
    passed=bool(all(gates.values()))

    result={
        "classification":(
            "GE17_LATE_TIME_STANDARD_BACKGROUND_DUST_DIAGNOSTIC_PASS"
            if passed else
            "GE17_LATE_TIME_STANDARD_BACKGROUND_DUST_DIAGNOSTIC_FAIL"
        ),
        "predata_classification":"GE17_PREDATA_LATE_TIME_STANDARD_BACKGROUND_DUST_DIAGNOSTIC",
        "pinned_CLASS_commit":PINNED_CLASS,
        "scope":"Background-only frozen late-time standard-sector dust-consistency diagnostic. No approximation acceptance gate.",
        "cosmology":pars,
        "species_definition":{
            "rho_std":"rho_b+rho_g+rho_ur+rho_ncdm[0]",
            "p_std":"rho_g/3+rho_ur/3+p_ncdm[0]",
            "rho_aest":"patched rho_cdm slot",
            "rho_cluster":"rho_std+rho_aest",
            "rho_lambda":"excluded from standard/clustering sectors",
            "p_aest_inferred":"p_tot-p_std+rho_lambda",
        },
        "density_reconstruction_relative_L2":total_recon,
        "summary":summary,
        "audit_redshifts":audit,
        "gates":gates,
        "interpretation_boundary":{
            "effective_dust_accepted":False,
            "Z20_licensed":False,
            "reason":"GE17 is diagnostic only. A later model-choice lock must choose an approximation budget independently.",
        },
        "claim_boundary":"PASS validates the background decomposition and quantified distance to one conserved pressureless standard fluid. It does not accept that reduction or license Z20.",
    }

    outj=Path(args.json_out); outj.parent.mkdir(parents=True,exist_ok=True)
    outj.write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
    np.savez_compressed(
        args.npz_out,
        z=z,a=a,rho_std=rho_std,p_std=p_std,rho_aest=rho_aest,
        rho_cluster=rho_cluster,rho_tot=rho_tot,p_aest_inferred=p_aest_inferred,
        window_mask=mask,C_a3rho_std=a**3*rho_std
    )
    print(json.dumps(result,indent=2,allow_nan=False))
    if not passed:
        raise SystemExit(2)


if __name__=="__main__":
    main()
