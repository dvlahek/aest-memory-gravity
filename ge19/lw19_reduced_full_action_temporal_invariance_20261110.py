#!/usr/bin/env python3
"""LW19: exact temporal covariance of frozen reduced GE06+GE05 action.

Includes the GR boundary created by GE06 spatial integration by parts.
No CLASS solver, nonlinear Y, full 3+1 action, physical Weyl
observer, data likelihood or retuning.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/"ge19/lw19_reduced_full_action_temporal_invariance_predata_20261110.json"
PRE_BLOB="397e276abaa597412bbbfe35faf9685107f8e403"
LW18_SHA="82ab6c7c9bb8efa676de8817cb0949ace86823dd92414709486020cfa0f9fc69"
SOURCES={
 "ge06/analytic_aest_directional_source_generator.py":
    "a7afe0035054a9dca55d74a6497c081422114b4c",
 "ge05/memory_directional_source_generator.py":
    "40837d77f89028da30c28899e2d0530a4401844e",
 "ge19/lw18_reduced_time_diffeo_noether_20261110.py":
    "9a6b83d4188e5a4756c13ed8b946d2b0f49d8fce",
}
MARKERS={
 "ge06/analytic_aest_directional_source_generator.py":[
   "grav=N*L*R**2*(-4*kL*kR-2*kR**2) + 2*N*Rx**2/L + 4*Nx*R*Rx/L",
   "aest=N*L*R**2*(KB*E**2 + 2*C*E*Xinv - C*Xinv**2 + 2*Kfun)"],
 "ge05/memory_directional_source_generator.py":[
   "lag=N*L*R**2*sp.Rational(1,4)*(Aq**2-(om*q-sw*Xphi)**2)"],
 "ge19/lw18_reduced_time_diffeo_noether_20261110.py":[
   "u:f*s.diff(u,t)-N*fx/L,",
   "Bcoef=(-N*b*EN+L*b*EL"],
}
def require(ok,key):
    if not bool(ok):
        raise RuntimeError("GE19_LW19_"+key)
def sha256(path):
    d=hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda:f.read(1<<20),b""):
            d.update(chunk)
    return d.hexdigest()
def blob(path):
    return subprocess.check_output(["git","hash-object",str(path)],text=True).strip()

def symbolic():
    import sympy as s
    N,L,R,b,u,phi,q=s.symbols("N L R b u phi q",real=True)
    Nt,Nx,Lt,Lx,Rt,Rx,bt,bx,ut,ux,pt,px,qt,qx=s.symbols(
        "Nt Nx Lt Lx Rt Rx bt bx ut ux pt px qt qx",real=True)
    f,ft,fx,ftt,ftx,fxx=s.symbols("f ft fx ftt ftx fxx",real=True)
    dt={N:Nt,L:Lt,R:Rt,b:bt,u:ut,phi:pt,q:qt}
    dx={N:Nx,L:Lx,R:Rx,b:bx,u:ux,phi:px,q:qx}
    dtmap={**dt,f:ft,ft:ftt,fx:ftx}
    dxmap={**dx,f:fx,ft:ftx,fx:fxx}
    def D(expr,m):
        return sum(s.diff(expr,z)*v for z,v in m.items())
    variations={
        N:f*Nt+N*ft-N*b*fx,
        L:f*Lt+L*b*fx,
        R:f*Rt,
        b:f*bt+b*ft-(N**2/L**2+b**2)*fx,
        u:f*ut-N*fx/L,
        phi:f*pt,
        q:f*qt,
    }
    # First-jet prolongation. Set f=0 only AFTER differentiating
    # f*z_t; translation (f L_t) is then restored by chain rule.
    prolong={}
    for z,v in variations.items():
        prolong[dt[z]]=D(v,dtmap).subs(f,0)
        prolong[dx[z]]=D(v,dxmap).subs(f,0)
    prolong.update({z:v.subs(f,0) for z,v in variations.items()})
    def vary(expr,pert=prolong):
        return sum(s.diff(expr,z)*v for z,v in pert.items())
    def zero(expr):
        return s.trigsimp(s.cancel(s.expand(expr)))==0

    ch,sh=s.cosh(u),s.sinh(u)
    sigma=(pt-b*px)/N
    Q=ch*sigma+sh*px/L
    X=sh*sigma+ch*px/L
    kL=(Lt-b*Lx-L*bx)/(N*L)
    kR=(Rt-b*Rx)/(N*R)
    E=ch*((ut-b*ux)/N+Nx/(N*L))+sh*(kL+ux/L)
    Aq=ch*(qt-b*qx)/N+sh*qx/L
    volume=N*L*R**2
    KB,eta,om,sw=s.symbols("KB eta omega sw",real=True)
    C=2-KB
    K=s.Function("K")
    matter=volume*(KB*E**2+2*C*E*X-C*X**2+2*K(Q)
          +eta*s.Rational(1,4)*(Aq**2-(om*q-sw*X)**2))
    grav=volume*(-4*kL*kR-2*kR**2)+2*N*Rx**2/L+4*Nx*R*Rx/L

    checks={}
    for label,expr in (("Q",Q),("X",X),("E",E),("Aq",Aq)):
        checks["invariant_"+label+"_true_scalar"]=zero(vary(expr))
    checks["volume_weight_one"]=zero(vary(volume)-ft*volume)
    checks["entire_AeST_plus_bath_density"]=zero(vary(matter)-ft*matter)

    anomaly=s.expand(vary(grav)-ft*grav)
    coeff={str(z):s.factor(s.diff(anomaly,z))
           for z in (ft,fx,ftt,ftx,fxx)}
    bt=4*N*R*Rx/L
    bx=-4*N*R*Rt/L
    ax=s.factor(D(bt,dtmap)+D(bx,dxmap))
    checks["GR_ft_anomaly_zero"]=zero(coeff["ft"])
    checks["GR_fx_matches_boundary"]=zero(coeff["fx"]-ax)
    checks["GR_ftt_anomaly_zero"]=zero(coeff["ftt"])
    checks["GR_ftx_matches_boundary"]=zero(coeff["ftx"]-bt)
    checks["GR_fxx_matches_boundary"]=zero(coeff["fxx"]-bx)
    checks["GR_surface_derivative_integrability"]=zero(
        ax-D(bt,dtmap)-D(bx,dxmap))
    total=s.expand(vary(grav+matter)-ft*(grav+matter))
    boundary=s.expand(ax*fx+bt*ftx+bx*fxx)
    checks["full_reduced_action_exact_boundary"]=zero(total-boundary)
    checks["negative_remove_GR_boundary_detected"]=not zero(anomaly)
    checks["negative_reverse_GR_boundary_detected"]=not zero(total+boundary)

    # Negative control: purposely omit the required rapidity boost term.
    wrong_u=variations[u].subs(fx,0)
    corrupt=dict(prolong)
    corrupt.update({u:wrong_u.subs(f,0),
                    ut:D(wrong_u,dtmap).subs(f,0),
                    ux:D(wrong_u,dxmap).subs(f,0)})
    checks["negative_omit_rapidity_boost_detected"]=not zero(
        vary(X,corrupt))

    failed=[key for key,value in checks.items() if not bool(value)]
    if failed:
        print("GE19_LW19_FAILED_GATES",failed,flush=True)
    require(not failed,"FULL_REDUCED_ACTION_INVARIANCE_FAIL")
    return {
        "checks":checks,
        "sympy_version":s.__version__,
        "field_basis":["N","L","R","b","u","phi","q"],
        "original_matter_action":
          "NLR²[KB E²+2(2-KB)EX-(2-KB)X²+2K(Q)+eta/4(Aq²-(omega q-sqrt(w)X)²)]",
        "original_gravity_action":
          "NLR²(-4kL kR-2kR²)+2N Rx²/L+4 Nx R Rx/L",
        "GR_boundary_time":"4*N*R*Rx/L",
        "GR_boundary_space":"-4*N*R*Rt/L",
        "GR_anomaly_coefficients":{k:str(v) for k,v in coeff.items()},
        "GR_anomaly_fx":str(ax),
        "action_boundary_identity":
          "delta L = partial_t(f L+4*N*R*Rx*f_x/L)-partial_x(4*N*R*Rt*f_x/L)",
        "physical_scope":
          "Exact off-shell temporal diffeo variation of original full GE06+GE05 reduced Lagrangian, arbitrary analytic K(Q); not full 3+1, nonlinear Y, complete CLASS fluid map, observer or data.",
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--self-test",action="store_true")
    p.add_argument("--lw18",type=Path,default=
        ROOT/"results/ge19_lw18_reduced_time_diffeo_noether_20261110.json")
    p.add_argument("--out",type=Path,default=
        ROOT/"results/ge19_lw19_reduced_full_action_temporal_invariance_20261110.json")
    a=p.parse_args()
    proof=symbolic()
    if a.self_test:
        print("GE19_LW19_FULL_REDUCED_ACTION_SELFTEST_PASS",
              len(proof["checks"]),flush=True)
        return
    require(blob(PRE)==PRE_BLOB,"FROZEN_PREDATA_CHANGED")
    pre=json.loads(PRE.read_text())
    require(pre["classification"]==
       "GE19_LW19_REDUCED_TOTAL_ACTION_TIME_DIFFEO_BOUNDARY_THEOREM_FORMULA_FREEZE",
       "PRE_CLASS_CHANGED")
    for name,expected in SOURCES.items():
        require(blob(ROOT/name)==expected,"SOURCE_BLOB_CHANGED_"+Path(name).name)
    source_checks={}
    for name,needles in MARKERS.items():
        txt=(ROOT/name).read_text()
        for j,needle in enumerate(needles,1):
            source_checks[name+"#"+str(j)]=needle in txt
    require(all(source_checks.values()),"HISTORICAL_SOURCE_MARKERS_FAIL")
    require(a.lw18.is_file() and sha256(a.lw18)==LW18_SHA,
            "ORIGINAL_WSL_LW18_SHA_CHANGED")
    parent=json.loads(a.lw18.read_text())
    require(parent["classification"]==
       "GE19_LW18_REDUCED_TIME_DIFFEO_NOETHER_KINEMATICS_AND_BATH_LINEAR_IDENTITY_PASS_CLASS_ACTION_MAP_OPEN"
       and len(parent["checks"])==14 and all(parent["checks"].values()),
       "LW18_PARENT_INVALID")
    result={
        "classification":
          "GE19_LW19_FULL_REDUCED_GE06_GE05_TEMPORAL_ACTION_COVARIANCE_PASS_CLASS_MAP_OPEN",
        "protocol_blob_sha1":PRE_BLOB,
        "original_source_blobs":SOURCES,
        "source_anchor_checks":source_checks,
        "LW18_original_researcher_SHA256":LW18_SHA,
        **proof,
        "reduced_time_Noether_from_actual_action":True,
        "full_Euler_rows_directly_substituted":False,
        "full_3plus1_and_nonanalytic_Y_certified":False,
        "full_action_to_CLASS_fluid_map":False,
        "global_Aeff_and_retarded_G_WE":False,
        "physical_two_history_metric_signal":False,
        "DES_ACT_observational_memory_detection":False,
        "LW03_radial_FAIL_preserved":True,
        "LW05_LOS_BLOCK_preserved":True,
        "LW08_differential_UNRESOLVED_preserved":True,
        "H4_Z21_certified":False,
    }
    out=a.out.resolve()
    require(out.parent.is_dir() and not out.exists(),
            "OUTPUT_PREEXISTS_OR_PARENT_MISSING")
    out.write_text(json.dumps(result,sort_keys=True,indent=2,
                              allow_nan=False)+"\n")
    print("GE19_LW19_CLASSIFICATION",result["classification"],flush=True)
    print("GE19_LW19_GATES",len(proof["checks"]),"PASS",flush=True)
    print("GE19_LW19_FULL_CLASS_MAP",False,flush=True)
    print("GE19_LW19_OUTPUT",str(out),flush=True)

if __name__=="__main__":
    main()
