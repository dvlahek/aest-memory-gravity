#!/usr/bin/env python3
"""GE19 LW17 — exact scalar shift current in frozen GE06+GE05 1+1 action.

Original analytic Einstein+AeST longitudinal coframe action and original
positive NL0B oscillator action (normalized q, eta overall). This is
the COMPLETE scalar variation of the FROZEN REDUCED action only, not
the full 3+1 AeST action-to-CLASS fluid/metric Euler mapping. No CLASS
solver, DES data, model retuning, H4 or observational inference.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/"ge19/lw17_full_reduced_scalar_action_current_predata_20261110.json"
PRE_BLOB="91550bc0bfc9180f0415416f08fab695a54ec277"
LW16_LOCAL_SHA="665de261c6bdc569887f6eadcaf6582b39c3ce3117b95c1b3d8d64baf26d488f"
SOURCES={
    "ge06/analytic_aest_directional_source_generator.py":
        "a7afe0035054a9dca55d74a6497c081422114b4c",
    "ge05/memory_directional_source_generator.py":
        "40837d77f89028da30c28899e2d0530a4401844e",
    "docs/nl0b_covariant_memory_completion_result.md":
        "d005b1c135fead856510aa76b6174fb9051fa552",
    "v019/apply_patch_v019.py":
        "c78484eb916bfee2730759c0bdc813a706bf9a68",
    "v019j/apply_memory_patch.py":
        "14796a5ed9e6265ed6810c792a93d7328a109364",
}
ANCHORS={
    "ge06/analytic_aest_directional_source_generator.py":[
        "Qinv=ch*sigma+sh*px/L",
        "Xinv=sh*sigma+ch*px/L",
        "aest=N*L*R**2*(KB*E**2 + 2*C*E*Xinv - C*Xinv**2 + 2*Kfun)"
    ],
    "ge05/memory_directional_source_generator.py":[
        "Aq=ch/N*(qt-b*qx)+sh/L*qx",
        "Xphi=sh/N*(pt-b*px)+ch/L*px",
        "lag=N*L*R**2*sp.Rational(1,4)*(Aq**2-(om*q-sw*Xphi)**2)"
    ],
    "v019j/apply_memory_patch.py":[
        "E_rhs_aest -= 0.5*Q_aest*Bchi_aest;"
    ]
}

def check(cond,name):
    if not bool(cond):
        raise RuntimeError("GE19_LW17_"+name)

def gitblob(file):
    return subprocess.check_output(["git","hash-object",str(file)],
                                   text=True).strip()

def sha(file):
    h=hashlib.sha256()
    with Path(file).open("rb") as f:
        for chunk in iter(lambda:f.read(1<<20), b""):
            h.update(chunk)
    return h.hexdigest()

def derive():
    import sympy as sp
    N,L,R,b,u,pt,px,ut,ux,Lt,Lx,bx,Nx,qt,qx,q,om,sw,eta,KB,C=sp.symbols(
        "N L R b u pt px ut ux Lt Lx bx Nx qt qx q om sw eta KB C",
        real=True)
    ch,sh=sp.cosh(u),sp.sinh(u)
    sigma=(pt-b*px)/N
    Qinv=ch*sigma+sh*px/L
    X=sh*sigma+ch*px/L
    kL=(Lt-b*Lx-L*bx)/(N*L)
    E=ch*((ut-b*ux)/N+Nx/(N*L))+sh*(kL+ux/L)
    Aq=ch*(qt-b*qx)/N+sh*qx/L
    K=sp.Function("K")
    lag=N*L*R**2*(
        KB*E**2+2*C*E*X-C*X**2+2*K(Qinv)
        +eta*sp.Rational(1,4)*(Aq**2-(om*q-sw*X)**2))
    z=sp.Dummy("z")
    KQexpr=sp.diff(K(z),z).subs(z,Qinv)
    Bx=sw**2*X-om*sw*q
    aux=2*C*(E-X)-eta*Bx/2
    Jt=L*R**2*(2*KQexpr*ch+aux*sh)
    Jx=N*R**2*(aux*ch+2*KQexpr*sh)-b*Jt

    # Full off-shell source identity: no bare phi dependence
    # Expand first, then reduce trig; generic nested simplify can be extremely slow
    # on the unexpanded multi-field action despite an exact zero.
    t_equal=sp.trigsimp(sp.expand(sp.diff(lag,pt)-Jt),method="fu")==0
    x_equal=sp.trigsimp(sp.expand(sp.diff(lag,px)-Jx),method="fu")==0

    ep=sp.symbols("eps",real=True)
    a,H,Qb,KQ,KQQ,I0=sp.symbols(
        "a H Qb KQ KQQ I0",positive=True,real=True)
    n,ell,rr,shift,v,pt1,px1,ut1,nx1,q1=sp.symbols(
        "n ell rr shift v pt1 px1 ut1 nx1 q1",real=True)
    perturb={
      N:1+ep*n,L:a+ep*ell,R:a+ep*rr,b:ep*shift,u:ep*v,
      pt:Qb+ep*pt1,px:ep*px1,ut:ep*ut1,Nx:ep*nx1,
      Lt:a*H,Lx:0,bx:0,ux:0,q:ep*q1,qt:0,qx:0
    }
    lin_t=sp.diff(Jt.subs(perturb),ep).subs(ep,0)
    lin_x=sp.diff(Jx.subs(perturb),ep).subs(ep,0)
    ksubs={
      sp.Derivative(K(Qb),Qb):KQ,
      sp.Derivative(K(Qb),(Qb,2)):KQQ,
    }
    lin_t=sp.simplify(lin_t.subs(ksubs))
    lin_x=sp.simplify(lin_x.subs(ksubs))
    X1=Qb*v+px1/a
    E1=ut1+nx1/a+H*v
    B1=sw**2*X1-om*sw*q1
    t_target=2*a**3*KQQ*(pt1-Qb*n)+2*a**2*KQ*(ell+2*rr)
    x_target=a**2*(2*C*(E1-X1)+2*KQ*v-eta*B1/2)-2*a**3*KQ*shift

    k,Bchi=sp.symbols("k Bchi",positive=True,real=True)
    Jx_bath=-eta*a**2*B1/2
    phi_E_bath=sp.simplify(
        (-sp.I*k*Jx_bath).subs(B1,sp.I*k*Bchi/a))
    expected_phi_E=-eta*a*k**2*Bchi/2
    j0=2*a**3*KQ

    gates={
      "full_offshell_action_Jt_exact":t_equal,
      "full_offshell_action_Jx_exact":x_equal,
      "phi_enters_only_via_derivatives":not lag.has(sp.Symbol("phi")),
      "linear_FLRW_charge_current_exact":
          sp.simplify(lin_t-t_target)==0,
      "linear_FLRW_spatial_current_exact":
          sp.simplify(lin_x-x_target)==0,
      "linear_bath_charge_current_zero":
          sp.simplify(sp.diff(lin_t,eta))==0,
      "linear_bath_spatial_flux_exact":
          sp.simplify(sp.diff(lin_x,eta)+a**2*B1/2)==0,
      "fourier_bath_Euler_matches_LW16_volume_factor":
          sp.simplify(phi_E_bath-expected_phi_E)==0,
      "background_shift_charge_constant_when_KQ_a_minus3":
          sp.simplify(j0.subs(KQ,I0/a**3)-2*I0)==0,
      "wrong_bath_sign_negative_control":
          sp.simplify(x_target-x_target.subs(eta,-eta))!=0,
      "missing_bath_flux_negative_control":
          sp.simplify(x_target-x_target.subs(eta,0))!=0,
    }
    check(all(gates.values()),"EXACT_ACTION_SCALAR_CURRENT_FAIL")
    return {
      "checks":gates,
      "sympy_version":sp.__version__,
      "original_action":"N*L*R²*[KB*E²+2*C*E*X-C*X²+2*K(Qinv)+eta/4*(Aq²-(omega*q-sqrt(w)*X)²)]",
      "original_invariants":{
        "sigma":"(pt-b*px)/N",
        "Qinv":"cosh(u)*sigma+sinh(u)*px/L",
        "X":"sinh(u)*sigma+cosh(u)*px/L",
        "E":"cosh(u)*[(ut-b*ux)/N+Nx/(N*L)]+sinh(u)*[(Lt-b*Lx-L*bx)/(N*L)+ux/L]",
        "Aq":"cosh(u)*(qt-b*qx)/N+sinh(u)*qx/L",
      },
      "full_scalar_shift_current":{
        "A":"2*C*(E-X)-eta*B_X/2",
        "B_X":"w*X-omega*sqrt(w)*q",
        "J_phi_t":"L*R²*[2*K_Q*cosh(u)+A*sinh(u)]",
        "J_phi_x":"N*R²*[A*cosh(u)+2*K_Q*sinh(u)]-b*J_phi_t",
        "Euler_phi":"-partial_t(J_phi_t)-partial_x(J_phi_x)",
      },
      "linear_FLRW":{
        "dQ":"pt1-Qb*n",
        "X1":str(X1),
        "E1":str(E1),
        "B_X1":str(B1),
        "dJ_phi_t":str(sp.factor(lin_t)),
        "dJ_phi_x":str(sp.factor(lin_x)),
        "bath_linear_dJ_phi_t":"0",
        "bath_linear_dJ_phi_x":str(sp.factor(Jx_bath)),
        "bath_linear_scalar_Euler_fourier":str(phi_E_bath),
        "expected_LW16_volume_weighted_Euler":str(expected_phi_E),
        "background_Jt":"2*a³*K_Q=2*I0",
      },
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--self-test",action="store_true")
    ap.add_argument("--lw16",type=Path,default=ROOT/
       "results/ge19_lw16_scalar_to_velocity_bath_euler_projection_20261110.json")
    ap.add_argument("--out",type=Path,default=ROOT/
       "results/ge19_lw17_full_reduced_scalar_action_current_20261110.json")
    opts=ap.parse_args()
    result=derive()
    if opts.self_test:
        print("GE19_LW17_REDUCED_SCALAR_CURRENT_SELFTEST_PASS",
              len(result["checks"]),flush=True)
        return

    check(gitblob(PRE)==PRE_BLOB,"PRELOCK_BLOB_CHANGED")
    pre=json.loads(PRE.read_text())
    check(pre["classification"]==
      "GE19_LW17_GE06_GE05_COMPLETE_REDUCED_SCALAR_SHIFT_CURRENT_FORMULA_LOCK",
      "PRELOCK_CLASS_CHANGED")
    for path,blob in SOURCES.items():
        check(gitblob(ROOT/path)==blob,"SOURCE_BLOB_CHANGED_"+Path(path).name)
    literal_checks={}
    for path,needles in ANCHORS.items():
        source=(ROOT/path).read_text()
        for j,needle in enumerate(needles,1):
            literal_checks[f"{path}#{j}"]=needle in source
    check(all(literal_checks.values()),"SOURCE_TEXT_ANCHOR_MISSING")
    check(opts.lw16.is_file() and sha(opts.lw16)==LW16_LOCAL_SHA,
          "LW16_ORIGINAL_WSL_SHA_CHANGED")
    parent=json.loads(opts.lw16.read_text())
    check(parent["classification"]==
          "GE19_LW16_BATH_SOURCE_PROJECTION_TO_THETA_PASS_FULL_ACTION_FLUID_DICTIONARY_OPEN"
          and all(parent["checks"].values()),"LW16_PARENT_FAILED")

    out={
      "classification":
        "GE19_LW17_REDUCED_COMBINED_AEST_MEMORY_SCALAR_CURRENT_EXACT_PASS_FULL_CLASS_ACTION_MAP_OPEN",
      "predata_git_blob_sha1":PRE_BLOB,
      "source_git_blobs":SOURCES,
      "source_anchor_checks":literal_checks,
      "LW16_actual_WSL_SHA256":LW16_LOCAL_SHA,
      **result,
      "scientific_scope":"Exactly the full scalar Euler current of original GE06 analytic 1+1 longitudinal AeST + GE05 one normalized positive memory mode, with arbitrary analytic K(Q). NOT full 3D covariant action, temporal/metric/aether constraints, CLASS effective-fluid equivalence or observed universe.",
      "nonanalytic_Y_beyond_linear_excluded":True,
      "full_temporal_diffeomorphism_Noether_Ward_proved":False,
      "full_metric_and_aether_Euler_to_CLASS_mapping_certified":False,
      "complete_background_matter_radiation_Aeff_certified":False,
      "action_derived_physical_JD_JT_closed":False,
      "global_metric_Green_Weyl_computed":False,
      "two_admissible_histories_Weyl_observable":False,
      "DES_ACT_detection":False,
      "LW03_radial_FAIL":True,"LW05_LOS_BLOCK":True,
      "LW08_differential_UNRESOLVED":True,"H4_Z21_certified":False,
    }
    outfile=opts.out.resolve()
    check(outfile.parent.is_dir() and not outfile.exists(),
          "OUTPUT_EXISTS_OR_PARENT_MISSING")
    outfile.write_text(json.dumps(out,indent=2,sort_keys=True,
                                  allow_nan=False)+"\n")
    print("GE19_LW17_CLASSIFICATION",out["classification"],flush=True)
    print("GE19_LW17_ACTION_GATES",len(result["checks"]),flush=True)
    print("GE19_LW17_FULL_CLASS_ACTION_CLOSURE",False,flush=True)
    print("GE19_LW17_OUTPUT",outfile,flush=True)

if __name__=="__main__":
    main()
