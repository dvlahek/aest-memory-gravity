#!/usr/bin/env python3
"""GE19 LW31: exact original reduced GR+AeST+bath spatial traceless Euler.

This is a plane-symmetric scalar-longitudinal Fourier-action audit, not the
complete 3+1 constrained cosmological model or an observed Weyl response.
The original CLASS memory patch and eta normalization are never changed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
PRE = ROOT / "ge19/lw31_action_spatial_traceless_shear_predata_20261110.json"
PRE_BLOB = "f0236ab323b286efb0dd325d2ab99e11b2c47629"


def require(flag, name):
    if not bool(flag):
        raise RuntimeError("GE19_LW31_" + name)


def gitblob(path):
    return subprocess.check_output(
        ["git", "hash-object", str(path)], cwd=ROOT, text=True
    ).strip()


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def algebra():
    s = sp
    N,L,R,b,u,pt,px,ut,ux,Nx,Lt,Lx,bx,Rt,Rx,qt,qx,q = s.symbols(
        "N L R b u pt px ut ux Nx Lt Lx bx Rt Rx qt qx q", real=True)
    KB,C,K0,KQ,KQQ,eta,omega,sw = s.symbols(
        "KB C K0 KQ KQQ eta omega sw", real=True)
    a,H,Q,k,eps = s.symbols("a H Q k eps", real=True, nonzero=True)
    Psi,Phi,Phidot,Phi2dot,Psidot,alpha,alphadot,alpha2dot,varphi,varphidot = s.symbols(
        "Psi Phi Phidot Phi2dot Psidot alpha alphadot alpha2dot varphi varphidot",
        real=True)
    Hdot,Qdot,KQdot,K0dot = s.symbols("Hdot Qdot KQdot K0dot", real=True)
    C0 = 3*H*H+2*Hdot
    kL = (Lt-b*Lx-L*bx)/(N*L)
    kR = (Rt-b*Rx)/(N*R)
    sigma = (pt-b*px)/N
    ch,sh = s.cosh(u),s.sinh(u)
    Qi = ch*sigma+sh*px/L
    Xi = sh*sigma+ch*px/L
    E = ch*((ut-b*ux)/N+Nx/(N*L))+sh*(kL+ux/L)
    Aq = ch*(qt-b*qx)/N+sh*qx/L
    vol = N*L*R**2
    K = s.Function("K")
    GR = vol*(-4*kL*kR-2*kR*kR)+2*N*Rx**2/L+4*Nx*R*Rx/L
    AE = vol*(KB*E**2+2*C*E*Xi-C*Xi**2+2*K(Qi))
    bath = eta*vol*s.Rational(1,4)*(Aq**2-(omega*q-sw*Xi)**2)
    fields = {
        N:1+eps*Psi, L:a*(1-eps*Phi), R:a*(1-eps*Phi),
        b:0, u:eps*s.I*k*alpha/a,
        pt:Q+eps*varphidot, px:eps*s.I*k*varphi,
        ut:eps*s.I*k*(alphadot-H*alpha)/a, ux:0,
        Nx:eps*s.I*k*Psi,
        Lt:a*H*(1-eps*Phi)-eps*a*Phidot,
        Lx:-a*eps*s.I*k*Phi, bx:0,
        Rt:a*H*(1-eps*Phi)-eps*a*Phidot,
        Rx:-a*eps*s.I*k*Phi,
        qt:0,qx:0,q:0,
    }
    replacements = {
        s.Derivative(K(Q), Q, 2):KQQ,
        s.Derivative(K(Q), Q):KQ,
        K(Q):K0,
    }
    time_derivatives = {
        a:a*H, H:Hdot, Q:Qdot, KQ:KQdot, K0:K0dot,
        Phi:Phidot,Phidot:Phi2dot,Psi:Psidot,
        alpha:alphadot,alphadot:alpha2dot,varphi:varphidot,
    }

    def partial(src, var, order):
        z = s.diff(src,var).subs(fields)
        if order:
            z = s.diff(z,eps).subs(eps,0).doit()
        else:
            z = z.subs(eps,0).doit()
        return s.simplify(z.xreplace(replacements))

    def dt(expr):
        return s.expand(sum(s.diff(expr,p)*v for p,v in time_derivatives.items()))

    def zero(expr):
        return s.simplify(s.factor(expr))==0

    def euler_shear(src):
        # Vary L and R *independently* before enforcing equal Newtonian
        # spatial potentials. EL and ER include their first-jet time
        # and spatial derivatives. R is shared by y/z, hence factor 1/2.
        EL0 = partial(src,L,0)-dt(partial(src,Lt,0))
        ER0 = partial(src,R,0)-dt(partial(src,Rt,0))
        EL1 = (partial(src,L,1)-dt(partial(src,Lt,1))
               -s.I*k*partial(src,Lx,1))
        ER1 = (partial(src,R,1)-dt(partial(src,Rt,1))
               -s.I*k*partial(src,Rx,1))
        traceless = s.factor(a*(EL1-ER1/2)-a*Phi*(EL0-ER0/2))
        return traceless,s.factor(EL0),s.factor(ER0)

    Tgr,grL0,grR0=euler_shear(GR)
    Tae,aeL0,aeR0=euler_shear(AE)
    Tba,baL0,baR0=euler_shear(bath)
    # The two separate original curvature pieces matter: they generate
    # distinct Phi and Psi gradient terms that recombine into slip.
    Tmiss_Nx,*_=euler_shear(GR-4*Nx*R*Rx/L)
    Tmiss_Rx2,*_=euler_shear(GR-2*N*Rx**2/L)

    checks={
        "GR_background_pressure_isotropic":
            zero(grR0-2*grL0),
        "AeST_background_pressure_isotropic":
            zero(aeR0-2*aeL0),
        "bath_background_spatial_Euler_zero":
            zero(baR0) and zero(baL0),
        "GR_background_spatial_Euler_expression":
            zero(grL0-2*a*a*C0),
        "AeST_background_spatial_Euler_expression":
            zero(aeL0-2*a*a*K0),
        "GR_traceless_metric_slip_from_full_action":
            zero(Tgr-2*a*k*k*(Phi-Psi)),
        "AeST_direct_linear_traceless_source_zero":
            zero(Tae),
        "bath_direct_linear_traceless_source_zero":
            zero(Tba),
        "total_traceless_metric_slip":
            zero(Tgr+Tae+Tba-2*a*k*k*(Phi-Psi)),
        "reduced_slip_zero_on_shell_k_nonzero":
            s.solve(Tgr+Tae+Tba,Psi)==[Phi],
        "no_background_Hdot_in_traceless":
            zero(s.diff(Tgr+Tae+Tba,Hdot)),
        "spatial_k_parity_even":
            zero((Tgr+Tae+Tba).subs(k,-k)-(Tgr+Tae+Tba)),
        "negative_remove_GR_Nx_RRx_detected":
            zero(Tmiss_Nx-2*a*k*k*Phi) and not zero(Tmiss_Nx-Tgr),
        "negative_remove_GR_Rx_squared_detected":
            zero(Tmiss_Rx2+2*a*k*k*Psi) and not zero(Tmiss_Rx2-Tgr),
        "negative_wrong_GR_shear_factor_detected":
            not zero(Tgr-a*k*k*(Phi-Psi)),
    }
    failed=[key for key,flag in checks.items() if not bool(flag)]
    if failed:
        print("GE19_LW31_FAILED_SYMBOLIC_GATES",failed,flush=True)
    require(not failed,"ACTION_SHEAR_SYMBOLIC_FAIL")
    derived={
        "traceless_Euler_definition":
            "T=[L E_L-(R/2) E_R] linear perturbative coefficient; E_L=dL/dL-dt(dL/dLt)-dx(dL/dLx)",
        "GR":"2*a*k^2*(Phi-Psi)",
        "AeST":"0",
        "NL0B_bath":"0",
        "GR_no_Nx_R_Rx":"2*a*k^2*Phi (negative control)",
        "GR_no_Rx_squared":"-2*a*k^2*Psi (negative control)",
        "shear_on_shell_AeST_only":"Phi=Psi for k!=0; no freely streaming species or other anisotropic stress",
        "real_cosmological_slip":"not zero when total anisotropic stress from other species is present",
        "metric_Weyl_relation":"(Phi+Psi)/2=Phi in this reduced AeST-only linear sector; not a physical survey transfer",
        "scope":"Exact original GE06 plane-symmetric scalar-longitudinal GR+AeST and GE05 linear memory coframe; not full 3+1 tensor/vector/Y/ordinary species."
    }
    return {key:bool(flag) for key,flag in checks.items()},derived


def provenance(parent):
    require(PRE.is_file() and gitblob(PRE)==PRE_BLOB,"PREDATA_CHANGED")
    pre=json.loads(PRE.read_text())
    require(pre["classification"]==
        "GE19_LW31_REDUCED_GE06_GE05_SPATIAL_TRACeless_SHEAR_PRELOCK",
        "PREDATA_CLASSIFICATION")
    for name,original_blob in pre["source_blobs"].items():
        f=ROOT/name
        require(f.is_file() and gitblob(f)==original_blob,
                "PARENT_SOURCE_CHANGED_"+f.name)
    source=(ROOT/"ge06/analytic_aest_directional_source_generator.py").read_text()
    require("grav=N*L*R**2*(-4*kL*kR-2*kR**2) + 2*N*Rx**2/L + 4*Nx*R*Rx/L" in source,
            "GR_ACTION_SOURCE_ANCHOR")
    require("aest=N*L*R**2*(KB*E**2 + 2*C*E*Xinv - C*Xinv**2 + 2*Kfun)" in source,
            "AEST_ACTION_SOURCE_ANCHOR")
    require(parent.is_file() and sha256(parent)==
            pre["original_parent_LW30_json_sha256"],
            "ORIGINAL_LW30_SHA_CHANGED")
    parent_json=json.loads(parent.read_text())
    require(parent_json["classification"]==
      "GE19_LW30_REDUCED_3PLUS1_GR_AEST_ADM_SCALAR_CONSTRAINTS_PASS_FULL_ACTION_TO_CLASS_OPEN"
      and len(parent_json["symbolic_gates"])==17
      and all(parent_json["symbolic_gates"].values()),
      "ORIGINAL_LW30_GATES_CHANGED")
    return pre


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--self-test",action="store_true")
    ap.add_argument("--lw30",type=Path,default=ROOT/
      "results/ge19_lw30_exact_adm_hamiltonian_momentum_constraints_20261110_r1.json")
    ap.add_argument("--out",type=Path,default=ROOT/
      "results/ge19_lw31_action_spatial_traceless_shear_20261110_r1.json")
    args=ap.parse_args()
    gates,derivation=algebra()
    print("GE19_LW31_ACTION_TRACeless_SHEAR_SYMBOLIC_PASS",len(gates),flush=True)
    if args.self_test:
        return
    frozen=provenance(args.lw30)
    print("GE19_LW31_SOURCE_LOCKS_PASS",len(frozen["source_blobs"]),flush=True)
    dest=args.out.resolve()
    require(dest.parent.is_dir() and not dest.exists(),
            "OUTPUT_EXISTS_OR_PARENT_MISSING")
    report={
        "classification":
          "GE19_LW31_REDUCED_GE06_GR_AEST_NL0B_TRACeless_SHEAR_PASS_FULL_ACTION_BRIDGE_OPEN",
        "symbolic_checks":gates,
        "derived":derivation,
        "predata_git_blob":PRE_BLOB,
        "original_LW30_SHA256":frozen["original_parent_LW30_json_sha256"],
        "source_blobs":frozen["source_blobs"],
        "AeST_linear_anisotropic_stress_direct_zero_in_reduced_model":True,
        "ordinary_species_anisotropic_stress_included":False,
        "full_3plus1_gauge_multiplier_Y_constraints_certified":False,
        "original_v019j_eta_factor2_resolved":False,
        "full_physical_eta_Weyl_observer_ready":False,
        "observed_DES_Y3_memory_detection":False,
        "LW22_lensing_geometry_PASS_preserved":True,
        "LW30_ADM_constraints_PASS_preserved":True,
    }
    dest.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
    print("GE19_LW31_CLASSIFICATION",report["classification"],flush=True)
    print("GE19_LW31_PHYSICAL_OBSERVER_READY",False,flush=True)
    print("GE19_LW31_OUTPUT",dest,flush=True)


if __name__=="__main__":
    main()
