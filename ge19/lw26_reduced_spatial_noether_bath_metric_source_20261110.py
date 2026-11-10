#!/usr/bin/env python3
"""GE19 LW26: restricted spatial Noether identity and zero direct linear bath metric stress.

Original GE06+GE05 analytic plane-symmetric coframe. NO CLASS run, no
full 3+1 Y-sector claim, and NO assertion that theta_A is unmodified.
The LW25 aether/CLASS factor-two conditional REVIEW remains OPEN.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/"ge19/lw26_reduced_spatial_noether_bath_metric_source_predata_20261110.json"
PRE_BLOB="82c503068e2d8bf5c9c60badd62e491ed6c2714d"
MARKERS={
 "ge06/analytic_aest_directional_source_generator.py":[
   "Qinv=ch*sigma+sh*px/L","Xinv=sh*sigma+ch*px/L",
   "aest=N*L*R**2*(KB*E**2 + 2*C*E*Xinv - C*Xinv**2 + 2*Kfun)"],
 "ge05/memory_directional_source_generator.py":[
   "lag=N*L*R**2*sp.Rational(1,4)*(Aq**2-(om*q-sw*Xphi)**2)"],
 "ge19/lw19_reduced_full_action_temporal_invariance_20261110.py":[
   "matter=volume*(KB*E**2+2*C*E*X-C*X**2+2*K(Q)"],
 "ge19/lw25_aether_shift_class_source_consistency_20261110.py":[
   "factor_two_ratio_is_exact","original_reduced_shift_source"],
 "v019j/apply_memory_patch.py":[
   "E_rhs_aest -= 0.5*Q_aest*Bchi_aest;",
   "Bchi_aest *= pba->aest_eta;"]
}

def need(ok,why):
 if not bool(ok):raise RuntimeError("GE19_LW26_"+why)

def blob(path):
 return subprocess.check_output(["git","hash-object",str(path)],
                                cwd=ROOT,text=True).strip()

def sha256(path):
 h=hashlib.sha256()
 with path.open("rb") as f:
  for chunk in iter(lambda:f.read(1<<20),b""):h.update(chunk)
 return h.hexdigest()

def symbolic():
 import sympy as s
 N,L,R,b,u,pt,px,ut,ux,Nx,Lt,Lx,bx,Rt,Rx,qt,qx,q=s.symbols(
  "N L R b u pt px ut ux Nx Lt Lx bx Rt Rx qt qx q",real=True)
 gt,gx,gtx,gxx,eps=s.symbols("gt gx gtx gxx eps",real=True)
 KB,C,eta,om,sw=s.symbols("KB C eta om sw",real=True)
 ch,sh=s.cosh(u),s.sinh(u)
 sigma=(pt-b*px)/N
 Q=ch*sigma+sh*px/L
 X=sh*sigma+ch*px/L
 kL=(Lt-b*Lx-L*bx)/(N*L)
 kR=(Rt-b*Rx)/(N*R)
 E=ch*((ut-b*ux)/N+Nx/(N*L))+sh*(kL+ux/L)
 Aq=ch*(qt-b*qx)/N+sh*qx/L
 vol=N*L*R**2
 grav=vol*(-4*kL*kR-2*kR**2)+2*N*Rx**2/L+4*Nx*R*Rx/L
 K=s.Function("K")
 aest=vol*(KB*E**2+2*C*E*X-C*X**2+2*K(Q))
 bath=eta*vol*s.Rational(1,4)*(Aq**2-(om*q-sw*X)**2)
 jets={
  N:0,L:L*gx,R:0,b:gt-b*gx,u:0,
  pt:gt*px,px:gx*px,ut:gt*ux,ux:gx*ux,
  Nx:gx*Nx,Lt:gt*Lx+gx*Lt+L*gtx,
  Lx:2*gx*Lx+L*gxx,bx:gtx-b*gxx,
  Rt:gt*Rx,Rx:gx*Rx,qt:gt*qx,qx:gx*qx,q:0,
 }
 def vary(expr,subs=jets):
  return s.expand(sum(s.diff(expr,z)*dz for z,dz in subs.items()))
 def zero(e):
  return s.trigsimp(s.cancel(s.expand(e)))==0
 checks={}
 for name,ex in (("sigma",sigma),("Q",Q),("X",X),
                 ("E",E),("Aq",Aq),("kL",kL),("kR",kR)):
  checks["exact_spatial_scalar_"+name]=zero(vary(ex))
 for name,ex in (("volume",vol),("GR",grav),("AeST",aest),("bath",bath)):
  checks["spatial_weight_one_"+name]=zero(vary(ex)-gx*ex)
 a,Qb,ad=s.symbols("a Qb ad",nonzero=True,real=True)
 n,ell,rr,shift,v,vdt,nx,phix,q1,qd,phid=s.symbols(
  "n ell rr shift v vdt nx phix q1 qd phid",real=True)
 flrw={
  N:1+eps*n,L:a+eps*ell,R:a+eps*rr,
  b:eps*shift,u:eps*v,pt:Qb+eps*phid,
  px:eps*phix,ut:eps*vdt,ux:0,
  Nx:eps*nx,Lt:ad,Lx:0,bx:0,Rt:ad,Rx:0,
  qt:eps*qd,qx:0,q:eps*q1
 }
 for f in (N,L,R,b,Lt,Lx,Rt,Rx,Nx,bx):
  d=s.diff(bath,f).subs(flrw)
  lin=s.simplify(s.diff(d,eps).subs(eps,0))
  checks["direct_bath_metric_first_order_zero_"+str(f)]=lin==0
 # Formal integration-by-parts spatial Noether identity, for seven
 # completely arbitrary Euler derivatives, using full g(t,x).
 t,x=s.symbols("t x")
 g=s.Function("g")(t,x)
 z=[s.Function(z)(t,x) for z in ("N","L","R","b","u","phi","q")]
 Ev=[s.Function(e)(t,x) for e in ("EN","EL","ER","Eb","Eu","Ephi","Eq")]
 nf,lf,rf,bf,uf,pf,qf=z
 En,El,Er,Ebf,Euf,Epf,Eqf=Ev
 delta={
  nf:g*s.diff(nf,x),
  lf:g*s.diff(lf,x)+lf*s.diff(g,x),
  rf:g*s.diff(rf,x),
  bf:g*s.diff(bf,x)+s.diff(g,t)-bf*s.diff(g,x),
  uf:g*s.diff(uf,x),
  pf:g*s.diff(pf,x),
  qf:g*s.diff(qf,x)
 }
 I=sum(e*s.diff(v,x) for v,e in zip(z,Ev))\
   -s.diff(lf*El-bf*Ebf,x)-s.diff(Ebf,t)
 def ward(v):
  return s.simplify(sum(e*v[field] for field,e in zip(z,Ev))
   -g*I-s.diff(g*(lf*El-bf*Ebf),x)-s.diff(g*Ebf,t))
 checks["exact_offshell_spatial_Noether_operator"]=ward(delta)==0
 wrong=dict(delta)
 wrong[bf]-=s.diff(g,t)
 checks["negative_omit_shift_time_diffeo_detected"]=ward(wrong)!=0
 wrong=dict(delta)
 wrong[bf]+=2*bf*s.diff(g,x)
 checks["negative_wrong_shift_sign_detected"]=ward(wrong)!=0
 wrong=dict(delta)
 wrong[lf]-=lf*s.diff(g,x)
 checks["negative_omit_L_density_weight_detected"]=ward(wrong)!=0
 # Direct metric stress can be zero without implying vanishing
 # indirect metric perturbations or an unchanged effective-fluid
 # velocity equation: these are explicitly NOT gate conclusions.
 failures=[key for key,val in checks.items() if not bool(val)]
 if failures:print("GE19_LW26_FAILED_CHECKS",failures,flush=True)
 need(not failures,"SYMBOLIC_SPATIAL_WARD_FAIL")
 return {k:bool(v) for k,v in checks.items()}

def provenance(lw25):
 need(PRE.is_file() and blob(PRE)==PRE_BLOB,"PRELOCK_CHANGED")
 frozen=json.loads(PRE.read_text())
 need(frozen["classification"]==
 "GE19_LW26_REDUCED_SPATIAL_NOETHER_BATH_LINEAR_METRIC_SOURCE_PRELOCK",
 "PRECLASS_CHANGED")
 need(set(frozen["source_blobs"])==set(MARKERS),"SOURCE_SET_CHANGED")
 for name,expected in frozen["source_blobs"].items():
  p=ROOT/name
  need(p.is_file() and blob(p)==expected,"SOURCE_BLOB_CHANGED_"+p.name)
  text=p.read_text()
  for n,needle in enumerate(MARKERS[name],1):
   need(needle in text,"SOURCE_ANCHOR_MISSING_"+p.name+"_"+str(n))
 need(lw25.is_file() and sha256(lw25)==
      frozen["original_LW25_json_sha256"],"LW25_PARENT_SHA_CHANGED")
 parent=json.loads(lw25.read_text())
 need(parent["classification"]==
 "GE19_LW25_REDUCED_AETHER_CLASS_ETA_SOURCE_FACTOR_TWO_CONDITIONAL_REVIEW_REQUIRED",
 "LW25_CLASS_CHANGED")
 need(len(parent["exact_symbolic_checks"])==15 and
      all(parent["exact_symbolic_checks"].values()),"LW25_GATES_CHANGED")
 return frozen

def main():
 parser=argparse.ArgumentParser()
 parser.add_argument("--self-test",action="store_true")
 parser.add_argument("--lw25",type=Path,default=ROOT/
  "results/ge19_lw25_aether_shift_class_source_consistency_20261110_r1.json")
 parser.add_argument("--out",type=Path,default=ROOT/
  "results/ge19_lw26_reduced_spatial_noether_bath_metric_source_20261110_r1.json")
 args=parser.parse_args()
 checks=symbolic()
 print("GE19_LW26_SPATIAL_NOETHER_SELFTEST_PASS",len(checks),flush=True)
 if args.self_test:return
 frozen=provenance(args.lw25)
 print("GE19_LW26_SOURCE_LOCKS_PASS",len(MARKERS),flush=True)
 dest=args.out.resolve()
 need(dest.parent.is_dir() and not dest.exists(),"OUTPUT_PARENT_OR_EXISTENCE")
 report={
  "classification":
    "GE19_LW26_REDUCED_SPATIAL_NOETHER_AND_BATH_DIRECT_METRIC_LINEAR_ZERO_PASS_LW25_FACTOR2_OPEN",
  "predata_git_blob":PRE_BLOB,
  "original_LW25_json_sha256":frozen["original_LW25_json_sha256"],
  "source_git_blobs":frozen["source_blobs"],
  "symbolic_checks":checks,
  "off_shell_identity":
    "I_x=N_x E_N+L_x E_L+R_x E_R+b_x E_b+u_x E_u+phi_x E_phi+q_x E_q - d_x(L E_L-b E_b)-d_t E_b =0",
  "bath_metric_direct_linear_euler_zero_reduced_model":True,
  "bath_scalar_aether_linear_sources_zero":False,
  "bath_indirect_metric_perturbations_may_exist":True,
  "original_CLASS_theta_equation_unchanged_action_certified":False,
  "LW25_conditional_factor_two_gap_resolved":False,
  "fully_constrained_full_3plus1_Einstein_AeST_bridge":False,
  "physical_eta_matter_weyl_derivative_certified":False,
  "DES_observation_found":False,
  "LW22_geometry_pass_preserved":True,
  "LW23_implemented_source_pass_preserved":True,
  "LW24_reduced_density_pressure_pass_preserved":True,
  "LW25_conditional_REVIEW_preserved":True,
 }
 dest.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
 print("GE19_LW26_CLASSIFICATION",report["classification"],flush=True)
 print("GE19_LW26_PHYSICAL_OBSERVER_READY",False,flush=True)
 print("GE19_LW26_OUTPUT",dest,flush=True)

if __name__=="__main__":
 main()
