#!/usr/bin/env python3
"""GE19 LW18: reduced 1+1 temporal diffeomorphism / bath Noether audit.

Exact tensor Lie transformations of the frozen 1+1 ADM metric/aether;
derived off-shell variational identity from diffeomorphism invariance;
first-order FLRW positive-NL0B bath scalar/rapidity source cancellation.

Not a fresh full GE06+GE05 Euler-variation comparison, a full 3+1
Noether/Ward certification, an action-to-CLASS-fluid dictionary, or data.
No CLASS runs, no numerical scans, no observed cosmology.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/"ge19/lw18_reduced_time_diffeo_noether_predata_20261110.json"
PRE_BLOB="c87e52553aacfa0eb2ece6cd9a6e4571c86bdad4"
SOURCE_BLOBS={
 "ge06/analytic_aest_directional_source_generator.py":
  "a7afe0035054a9dca55d74a6497c081422114b4c",
 "ge05/memory_directional_source_generator.py":
  "40837d77f89028da30c28899e2d0530a4401844e",
 "ge19/lw17_full_reduced_scalar_action_current_20261110.py":
  "df5acc2c97076736ccdd7755691cacdaaada0e22",
}

def require(b,key):
    if not bool(b):
        raise RuntimeError("GE19_LW18_"+key)

def symbolic():
    import sympy as s
    t,x=s.symbols("t x",real=True)
    N,L,R,b,u,phi,q,f=[s.Function(n)(t,x)
                         for n in ("N","L","R","b","u","phi","q","f")]
    ft,fx=s.diff(f,t),s.diff(f,x)
    variations={
      N:f*s.diff(N,t)+N*ft-N*b*fx,
      L:f*s.diff(L,t)+L*b*fx,
      R:f*s.diff(R,t),
      b:f*s.diff(b,t)+b*ft-(N**2/L**2+b**2)*fx,
      u:f*s.diff(u,t)-N*fx/L,
      phi:f*s.diff(phi,t),
      q:f*s.diff(q,t),
    }
    def vary(expr):
        return sum(s.diff(expr,p)*dp for p,dp in variations.items())

    # Original GE06 coframe ADM metric and unit-aether 1+1 vector.
    g=s.Matrix([[-N**2+L**2*b**2,L**2*b],
                [L**2*b,L**2]])
    ae=s.Matrix([s.cosh(u)/N,-b*s.cosh(u)/N+s.sinh(u)/L])

    checks={}
    for i in range(2):
        for j in range(2):
            lie=(f*s.diff(g[i,j],t)
                 +g[0,j]*s.diff(f,(t,x)[i])
                 +g[i,0]*s.diff(f,(t,x)[j]))
            checks[f"Lie_metric_{i}{j}"]=(s.simplify(s.expand(
                vary(g[i,j])-lie))==0)
    for i in range(2):
        lie=(f*s.diff(ae[i],t)
             -(ae[0]*ft+ae[1]*fx if i==0 else 0))
        checks[f"Lie_unit_aether_{i}"]=(s.trigsimp(
            s.simplify(s.expand(vary(ae[i])-lie)))==0)

    volume=N*L*R**2
    checks["Lie_transverse_metric"]=(
        s.simplify(vary(R**2)-f*s.diff(R**2,t))==0)
    checks["Lie_action_volume_density"]=(
        s.simplify(vary(volume)-s.diff(f*volume,t))==0)

    # On an arbitrary Euler-functional collection, integration by parts
    # defines the exact time-diffeomorphism Noether differential operator.
    EN,EL,ER,Eb,Eu,Ephi,Eq=[s.Function("E_"+n)(t,x)
                            for n in ("N","L","R","b","u","phi","q")]
    Efields={N:EN,L:EL,R:ER,b:Eb,u:Eu,phi:Ephi,q:Eq}
    work=sum(variations[z]*Efields[z] for z in Efields)
    Acoef=N*EN+b*Eb
    Bcoef=(-N*b*EN+L*b*EL
           -(N**2/L**2+b**2)*Eb-(N/L)*Eu)
    noether=sum(s.diff(z,t)*Efields[z] for z in Efields)
    noether-=s.diff(Acoef,t)+s.diff(Bcoef,x)
    checks["off_shell_noether_integration_by_parts"]=(
        s.simplify(s.expand(work-(
          f*noether+s.diff(f*Acoef,t)+s.diff(f*Bcoef,x))))==0)

    # Negative control: omit the genuine time-refoliation f_x
    # compensation in the aether rapidity transformation.
    wrong_u=f*s.diff(u,t)
    wrong_ae_t=vary(ae[0])-s.diff(ae[0],u)*(
        variations[u]-wrong_u)
    true_lie_ae_t=f*s.diff(ae[0],t)-ae[0]*ft-ae[1]*fx
    checks["negative_omit_aether_boost_breaks_Lie"]=(
      s.trigsimp(s.simplify(wrong_ae_t-true_lie_ae_t))!=0)

    # At relaxed FLRW the original GE05 quadratic action has no
    # linear scalar charge J_phi^t but has scalar spatial flux.
    a,k,Q,eta,w,om,q1,uv,px,qt,Bchi=s.symbols(
      "a k Q eta w omega q u1 px qt Bchi",positive=True,real=True)
    X1=Q*uv+px/a
    Bx=w*X1-om*s.sqrt(w)*q1
    Lbath=eta*a**3*s.Rational(1,4)*(
        qt**2-(om*q1-s.sqrt(w)*X1)**2)
    Eu_bath=s.diff(Lbath,uv)
    Jx_bath=s.diff(Lbath,px)
    checks["bath_rapidity_Euler_from_action"]=(
        s.simplify(Eu_bath+eta*a**3*Q*Bx/2)==0)
    checks["bath_scalar_spatial_current_from_action"]=(
        s.simplify(Jx_bath+eta*a**2*Bx/2)==0)
    # Fourier convention B_X1=(i k/a)Bchi, Euler_phi=-i k Jx.
    Ephi_fourier=-eta*a*k**2*Bchi/2
    Eu_fourier=-s.I*eta*a**2*k*Q*Bchi/2
    checks["FLRW_linear_bath_time_Noether_cancellation"]=(
        s.simplify(Q*Ephi_fourier+s.I*k*Eu_fourier/a)==0)
    checks["negative_omit_scalar_partner_breaks_Noether"]=(
        s.simplify(s.I*k*Eu_fourier/a)!=0)

    require(all(checks.values()),"SYMBOLIC_SOURCE_OR_NOETHER_FAIL")
    return {
      "checks":checks,
      "sympy_version":s.__version__,
      "field_order":["N","L","R","b","u","phi","q"],
      "time_diffeomorphism":"xi=f(t,x)*partial_t; variations=+Lie_xi",
      "transformations":{
       "delta_N":"f*N_t+N*f_t-N*b*f_x",
       "delta_L":"f*L_t+L*b*f_x",
       "delta_R":"f*R_t",
       "delta_b":"f*b_t+b*f_t-(N²/L²+b²)*f_x",
       "delta_u":"f*u_t-(N/L)*f_x",
       "delta_phi":"f*phi_t",
       "delta_q":"f*q_t",
      },
      "off_shell_Noether_operator":{
       "A":"N E_N+b E_b",
       "B":"-N b E_N+L b E_L-(N²/L²+b²)E_b-(N/L)E_u",
       "I":"N_t E_N+L_t E_L+R_t E_R+b_t E_b+u_t E_u+phi_t E_phi+q_t E_q-partial_t(A)-partial_x(B)",
       "scope":"I=0 is guaranteed by diffeomorphism invariance of complete ORIGINAL REDUCED action and its Euler derivatives; actual full Euler expressions are not all recomputed here.",
      },
      "FLRW_linear_bath_identity":{
       "E_phi_bath":"-eta*a*k²*Bchi/2",
       "E_u_bath":"-i*eta*a²*k*Q*Bchi/2",
       "identity":"Q E_phi_bath + (i k/a) E_u_bath = 0",
       "metric_bath_direct_linear_stress":"already prior NL0B Identity6; not recalculated here",
       "scalar_shift_current_consistent_with_LW17":True,
      },
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--self-test",action="store_true")
    p.add_argument("--out",type=Path,default=ROOT/
      "results/ge19_lw18_reduced_time_diffeo_noether_20261110.json")
    a=p.parse_args()
    v=symbolic()
    if a.self_test:
        print("GE19_LW18_REDUCED_TIME_NOETHER_SELFTEST_PASS",
              len(v["checks"]),flush=True)
        return

    pre=subprocess.check_output(["git","hash-object",str(PRE)],
                                text=True).strip()
    require(pre==PRE_BLOB,"PROTOCOL_BLOB_CHANGED")
    d=json.loads(PRE.read_text())
    require(d["classification"]==
      "GE19_LW18_REDUCED_1PLUS1_TEMPORAL_DIFFEO_NOETHER_SOURCE_GATE_PRELOCK",
      "PROTOCOL_CONTENT_CHANGED")
    for file,blob in SOURCE_BLOBS.items():
        actual=subprocess.check_output(
           ["git","hash-object",str(ROOT/file)],text=True).strip()
        require(actual==blob,"FROZEN_SOURCE_CHANGED_"+Path(file).name)
    result={
      "classification":
       "GE19_LW18_REDUCED_TIME_DIFFEO_NOETHER_KINEMATICS_AND_BATH_LINEAR_IDENTITY_PASS_CLASS_ACTION_MAP_OPEN",
      "protocol_git_blob_sha1":PRE_BLOB,
      "source_git_blobs":SOURCE_BLOBS,
      **v,
      "direct_full_action_Euler_to_Noether_contraction_assembled":False,
      "full_3plus1_temporal_spatial_Ward_certified":False,
      "original_CLASS_effective_D_T_E_aether_dictionary_certified":False,
      "physical_JD_JT_action_zero_certified":False,
      "full_constrained_metric_Green_certified":False,
      "physical_two_history_Weyl_observer_certified":False,
      "DES_ACT_observational_memory_detection":False,
      "LW03_radial_FAIL_preserved":True,
      "LW05_full_shear_LOS_BLOCK_preserved":True,
      "LW08_differential_source_UNRESOLVED_preserved":True,
      "H4_Z21_certified":False,
      "LW17_researcher_r1_json_content_archived":False,
      "LW17_researcher_r1_reported_json_valid":True,
      "scope":"Exact time-coordinate Lie kinematics, implied off-shell Noether operator and positive bath linear source cancellation for the frozen 1+1 reduced action. NOT a complete full-action Euler-to-CLASS independent verification.",
    }
    out=a.out.resolve()
    require(out.parent.is_dir() and not out.exists(),
            "OUTPUT_EXISTS_OR_PARENT_MISSING")
    out.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n")
    print("GE19_LW18_CLASSIFICATION",result["classification"],flush=True)
    print("GE19_LW18_GATES",len(v["checks"]),"PASS",flush=True)
    print("GE19_LW18_FULL_CLASS_ACTION_MAP",False,flush=True)
    print("GE19_LW18_OUTPUT",out,flush=True)

if __name__=="__main__":
    main()
