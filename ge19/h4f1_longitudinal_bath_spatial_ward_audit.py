#!/usr/bin/env python3
"""H4F1 restricted bath-covector spatial Ward proof, exact symbolic only.

From frozen NL0B U_j=q_j s_mu and the NL1C3B longitudinal coframe,
derive (do not assume) the gauge transformation of q and of U_t/U_x.
Prove the GE05 node action transforms as a spatial density for an
arbitrary time-dependent infinitesimal spatial relabeling xi(t,x).

This is NOT the full mixed-H4 source/parent Noether identity and does
not execute H4/Z21 or introduce observational/finite-eta physics.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
BLOBS={
 "ge19/h4f1_predata_longitudinal_bath_spatial_ward.json":
   "7f26852707ba5b722adf0c934003b2cc5cccb24b",
 "docs/nl0b_predata_covariant_memory_completion.md":
   "9b1c013153faeddbd2add3d80eb29f673bc7748f",
 "docs/nl1c3b_predata_longitudinal_3plus1_memory_bridge.md":
   "22e38a08b7ee52fee8e1b0564887cdf931915644",
 "nl1c3b/longitudinal_3plus1_memory_bridge.py":
   "f64e42186f489b37800f33d99f72668268211d23",
 "ge05/memory_directional_source_generator.py":
   "40837d77f89028da30c28899e2d0530a4401844e",
 "ge19/h4_structural_stage_b_geometric_ward_primitives.py":
   "5695cf064dcc32bf4385687cbe6052521f2e36b4",
 "docs/ge19_h4_source_constraint_noether_structural_stop_gate.md":
   "249193f946e98b13fb5fa4175e997ab721d891c4",
 "docs/ge19_h3g_independent_uploaded_npz_audit_addendum.md":
   "01046254c9cfef2aba4fa285e1b42a2eba73820a",
}

def fixed_blob_audit():
    out={}
    for path,expected in BLOBS.items():
        observed=subprocess.check_output(
            ["git","rev-parse","HEAD:"+path],cwd=ROOT,text=True
        ).strip()
        out[path]={
            "expected":expected,"observed":observed,
            "exact":observed==expected
        }
    return out


def frozen_action_binding():
    cov=(ROOT/"docs/nl0b_predata_covariant_memory_completion.md").read_text()
    bridge=(ROOT/"docs/nl1c3b_predata_longitudinal_3plus1_memory_bridge.md").read_text()
    nls=(ROOT/"nl1c3b/longitudinal_3plus1_memory_bridge.py").read_text()
    ge05=(ROOT/"ge05/memory_directional_source_generator.py").read_text()
    norm=lambda x:"".join(x.split())
    lag="lag=N*L*R**2*sp.Rational(1,4)*(Aq**2-(om*q-sw*Xphi)**2)"
    return {
        "NL0B_U_is_orthogonal_covector":
            r"U_{j\mu}" in cov and r"A^\mu U_{j\mu}=0" in cov,
        "NL1C3B_explicit_orthonormal_longitudinal_U_equals_q_s":
            r"U_{j\mu}=q_j s_\mu" in bridge,
        "NL1C3B_actual_reduced_node_lag":
            norm(lag) in norm(nls),
        "GE05_actual_reduced_node_lag":
            norm(lag) in norm(ge05),
        "both_generators_same_action_lag":
            norm(lag) in norm(nls) and norm(lag) in norm(ge05),
    }


def exact_spatial_ward_audit():
    N,L,R,b,u,q,pt,px,qt,qx=sp.symbols(
        "N L R b u q pt px qt qx",real=True
    )
    Nx,Lx,Rx,bx,ux,qx_jet,ptx,pxx,qtx,qxx=sp.symbols(
        "Nx Lx Rx bx ux qx_jet ptx pxx qtx qxx",real=True
    )
    xi,xix,xit=sp.symbols("xi xix xit",real=True)
    om,sw=sp.symbols("om sw",positive=True,real=True)
    jet={
        N:Nx,L:Lx,R:Rx,b:bx,u:ux,q:qx,
        pt:ptx,px:pxx,qt:qtx,qx:qxx
    }
    vary={
        N:xi*Nx,
        L:xi*Lx+L*xix,
        R:xi*Rx,
        b:xi*bx+xit-b*xix,
        u:xi*ux,
        q:xi*qx,
        pt:xi*ptx+xit*px,
        px:xi*pxx+xix*px,
        qt:xi*qtx+xit*qx,
        qx:xi*qxx+xix*qx,
    }
    def d(expr,derivatives):
        return sum(sp.diff(expr,variable)*coefficient
                   for variable,coefficient in derivatives.items())
    def zero(expr):
        return bool(sp.trigsimp(sp.factor(expr))==0)
    def covariance(expr,want):
        return zero(d(expr,vary)-want)

    ch,sh=sp.cosh(u),sp.sinh(u)
    # From theta0=Ndt, theta1=L(dx+b dt),
    # A=ch*e0+sh*e1, s=sh*e0+ch*e1 with (-,+) signature.
    At=ch/N
    Ax=-b*ch/N+sh/L
    s_t=-sh*N+ch*L*b
    s_x=ch*L
    Ut=q*s_t
    Ux=q*s_x
    Aq=ch*(qt-b*qx)/N+sh*qx/L
    Xphi=sh*(pt-b*px)/N+ch*px/L
    volume=N*L*R**2
    potential=om*q-sw*Xphi
    lag=volume*sp.Rational(1,4)*(Aq**2-potential**2)

    gates={
      "A_t_spatial_vector_component":
          covariance(At,xi*d(At,jet)),
      "A_x_spatial_vector_component":
          covariance(Ax,xi*d(Ax,jet)-At*xit-Ax*xix),
      "U_t_spatial_covector_component":
          covariance(Ut,xi*d(Ut,jet)+Ux*xit),
      "U_x_spatial_covector_component":
          covariance(Ux,xi*d(Ux,jet)+Ux*xix),
      "A_dot_U_orthogonality":
          zero(At*Ut+Ax*Ux),
      "q_scalar_from_U_equals_q_s":
          covariance(q,xi*d(q,jet)),
      "Aq_equals_A_contract_dq":
          zero(Aq-At*qt-Ax*qx),
      "Aq_spatial_scalar":
          covariance(Aq,xi*d(Aq,jet)),
      "Xphi_spatial_scalar":
          covariance(Xphi,xi*d(Xphi,jet)),
      "memory_potential_spatial_scalar":
          covariance(potential,xi*d(potential,jet)),
      "volume_spatial_density":
          covariance(volume,xi*d(volume,jet)+xix*volume),
      "full_GE05_node_lag_spatial_density":
          covariance(lag,xi*d(lag,jet)+xix*lag),
    }
    return {
        "gates":gates,
        "exact_frame":"theta0=N dt, theta1=L(dx+b dt)",
        "covariant_bath_components":{
            "U_t":"q*(-sinh(u)*N+cosh(u)*L*b)",
            "U_x":"q*cosh(u)*L"
        },
        "exact_bath_scalar_transformation":"delta q=xi*q_x, derived by matching Lie derivatives of U_t,U_x with frozen U=q*s",
        "exact_ward_density_consequence":
          "delta L_mem = d_x(xi L_mem) under arbitrary xi(t,x), including xi_t and xi_x",
        "bath_parent_Eq_in_formal_Ward":
          "E_q*q_x enters alongside full metric, aether and scalar Euler rows",
        "full_mixed_H4_parent_residual_source_identity_derived":False,
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--json-out",required=True)
    args=ap.parse_args()
    blobs=fixed_blob_audit()
    binds=frozen_action_binding()
    ward=exact_spatial_ward_audit()
    passed=bool(all(v["exact"] for v in blobs.values())
                and all(binds.values()) and all(ward["gates"].values()))
    report={
        "classification":(
            "GE19_H4F1_LONGITUDINAL_BATH_WARD_COVARIANCE_DERIVED"
            if passed else
            "GE19_H4F1_LONGITUDINAL_BATH_WARD_COVARIANCE_UNRESOLVED"
        ),
        "predata_classification":
            "GE19_H4F1_PREDATA_LONGITUDINAL_BATH_SPATIAL_WARD_COVARIANCE",
        "frozen_source_blobs":blobs,
        "frozen_covariant_action_bindings":binds,
        "exact_reduced_bath_ward":ward,
        "all_subset_gates_pass":passed,
        "generic_transverse_bath_gauge_transformation_derived":False,
        "full_all_sector_mixed_H4_Noether_derived":False,
        "common_corrected_parent_time_H4_source_audit_performed":False,
        "H4_Z21_solve_performed":False,
        "Z21_certified":False,
        "lensing_licensed":False,
        "next_route":(
            "DERIVE_SIGNED_COMPLETE_H4_SOURCE_AND_PARENT_WARD_COEFFICIENT"
            if passed else
            "FREEZE_LOCALIZED_BATH_TRANSFORMATION_DEFECT"
        ),
        "claim_boundary":"Exact reduced bath covector and per-node action spatial covariance does not imply a complete H4 source identity or that an unrelated discrete H4 source is compatible. No H4 state solve or source fitting."
    }
    p=Path(args.json_out)
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print(json.dumps(report,indent=2,sort_keys=True,allow_nan=False))
    if not passed:
        raise SystemExit(3)


if __name__=="__main__":
    main()
