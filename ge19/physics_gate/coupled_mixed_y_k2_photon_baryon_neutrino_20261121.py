#!/usr/bin/env python3
"""GE19 complete O(y_m*(k*tau)^2) coupled radiation+dust test-fluid seed.

42 coefficient-level Einstein/Boltzmann residual checks with arbitrary
positive neutrino fraction 0<Rnu<1 and baryon fraction 0<=beta<=1.
This is a pressureless AeST-LIKE species, NOT original action scalar Ward,
no actual memory/Weyl prediction and no CLASS/DES run.
"""
from __future__ import annotations
import argparse,json,subprocess
from functools import lru_cache
from pathlib import Path
import sympy as s

LOCKS={
 "ge19/physics_gate/physical_baryon_Exp_leading_seed_20261121.py":
 "b58e4119a73a2d4a4a279e9a858177e99fbd95fb",
 "ge19/physics_gate/radiation_neutrino_finite_k_NLO_memory_source_20261121.py":
 "eb0bf46391bbce136a69e3d41f90f4b0d58a7ce9",
 "ge19/physics_gate/corrected_octupole_and_causal_memory_onset_20261121.py":
 "a697f719e33de40a9df24d1808b2284bf7364c81",
}
def source_locks(root):
 for p,expected in LOCKS.items():
  f=root/p
  if not f.is_file():raise RuntimeError("SOURCE_MISSING "+p)
  got=subprocess.check_output(["git","hash-object",str(f)],
                              cwd=root,text=True).strip()
  if got!=expected:raise RuntimeError("SOURCE_CHANGED "+p+" "+got)
 print("GE19_MIXED_FINITE_K_SOURCE_LOCKS_PASS",len(LOCKS),flush=True)

def derive():
 R,B,y,k,t=s.symbols("R_nu beta y_m k tau",real=True)
 x2=k**2*t**2
 fy=-(15+16*R)/(16*(15+2*R))
 gy=(40*R-15)/(16*(15+2*R))
 fk=-(56*R**2+580*R+525)/(630*(2*R+25))
 gk=(56*R**2+10*R-525)/(630*(2*R+25))
 # Unique mixed correction after solving Hamiltonian plus shear.
 # Momentum and spatial trace independently checked, not fitted.
 F=(896*R**4+66160*R**3+1023300*R**2+5386500*R+4659375)/(
     10080*(2*R+15)*(2*R+25)*(4*R+75))
 G=-(896*R**4+116080*R**3+1050900*R**2+1074000*R-4659375)/(
     10080*(2*R+15)*(2*R+25)*(4*R+75))
 Thy=(fy+gy)/2
 ThAy=(gy-s.Rational(1,8))/3
 Dgk=4*fk-s.Rational(1,3)
 Dak=3*fk-s.Rational(1,4)
 Tgk=(fk+gk-s.Rational(1,12))/3
 Tnk=(fk+gk-s.Rational(3,20))/3
 Tak=gk/4
 S2=s.Rational(1,15)
 S2y=4*Thy/45
 F3=s.Rational(2,105)
 F3y=3*S2y/14
 S4=Tnk/15-s.Rational(3,40)*F3
 Dgyk=4*F-s.Rational(4,9)*Thy
 Da_yk=3*F-ThAy/3
 Db_yk=3*F-Thy/3
 Rbcoef=3*B/(4*(1-R))
 Tgyk=(Dgyk/4+G-Rbcoef*(Dgk/4+Tgk))/4
 Tnyk=(Dgyk/4+G-S2y)/4
 Tayk=(G-Tak/4)/5
 S4y=(s.Rational(4,15)*Tnyk-s.Rational(3,10)*F3y)/5
 Phi=1+2*R/5+fy*y+fk*x2+F*y*x2
 Psi=1+gy*y+gk*x2+G*y*x2
 Dg=-2+4*fy*y+Dgk*x2+Dgyk*y*x2
 Dn=Dg
 Da=-s.Rational(3,2)+3*fy*y+Dak*x2+Da_yk*y*x2
 Db=-s.Rational(3,2)+3*fy*y+Dak*x2+Db_yk*y*x2
 Tg=k**2*t*(s.Rational(1,2)+Thy*y+Tgk*x2+Tgyk*y*x2)
 Tn=k**2*t*(s.Rational(1,2)+Thy*y+Tnk*x2+Tnyk*y*x2)
 Ta=k**2*t*(s.Rational(1,2)+ThAy*y+Tak*x2+Tayk*y*x2)
 Sn=S2*x2+S2y*y*x2+S4*x2**2+S4y*y*x2**2
 Fnu3=(F3+F3y*y)*k**3*t**3
 H=(1+y/s.Integer(4))/t
 Ar=(1-y/s.Integer(2))/t**2
 AA=(1-B)*y/t**2
 Ab=B*y/t**2
 Rb=Rbcoef*y
 @lru_cache(None)
 def Dt(ex):return s.diff(ex,t)+y*s.diff(ex,y)/t
 @lru_cache(None)
 def coeff(ex,powery,powerk):
  return s.factor(s.together(s.expand(ex).coeff(y,powery).coeff(k,powerk)))
 rad_d=(1-R)*Dg+R*Dn
 rad_t=(1-R)*Tg+R*Tn
 ham=k**2*Phi+3*H*(Dt(Phi)+H*Psi)+s.Rational(3,2)*(
   Ar*rad_d+AA*Da+Ab*Db)
 mom=Dt(Phi)+H*Psi-s.Rational(3,2)/k**2*(
   s.Rational(4,3)*Ar*rad_t+AA*Ta+Ab*Tg)
 shear=Phi-Psi-6*R*Ar*Sn/k**2
 trace=Dt(Dt(Phi))+H*(Dt(Psi)+2*Dt(Phi))+(
   2*Dt(H)+H**2)*Psi+k**2*(Phi-Psi)/3-Ar*rad_d/2
 cg=Dt(Dg)+s.Rational(4,3)*Tg-4*Dt(Phi)
 cn=Dt(Dn)+s.Rational(4,3)*Tn-4*Dt(Phi)
 cb=Dt(Db)+Tg-3*Dt(Phi)
 ca=Dt(Da)+Ta-3*Dt(Phi)
 # Correct O(y) tight-coupling expansion of 1/(1+R_b).
 eg=Dt(Tg)+H*Rb*Tg-k**2*(Dg*(1-Rb)/4+Psi)
 en=Dt(Tn)-k**2*(Dn/4+Psi-Sn)
 ea=Dt(Ta)+H*Ta-k**2*Psi
 es=Dt(Sn)-s.Rational(4,15)*Tn+s.Rational(3,10)*k*Fnu3
 ef3=Dt(Fnu3)-s.Rational(6,7)*k*Sn
 families=[
  ("Einstein_Hamiltonian",ham,((0,0),(1,0),(0,2),(1,2))),
  ("Einstein_momentum",mom,((0,0),(1,0),(0,2),(1,2))),
  ("Einstein_shear",shear,((0,0),(1,0),(0,2),(1,2))),
  ("Einstein_spatial_trace",trace,((0,0),(1,0),(0,2),(1,2))),
  ("photon_continuity",cg,((0,2),(1,2))),
  ("neutrino_continuity",cn,((0,2),(1,2))),
  ("baryon_continuity",cb,((0,2),(1,2))),
  ("aestlike_dust_continuity",ca,((0,2),(1,2))),
  ("photon_baryon_tight_coupling_Euler",eg,((0,2),(1,2),(0,4),(1,4))),
  ("free_neutrino_Euler",en,((0,2),(1,2),(0,4),(1,4))),
  ("aestlike_dust_Euler",ea,((0,2),(1,2),(0,4),(1,4))),
  ("free_neutrino_quadrupole",es,((0,2),(1,2),(0,4),(1,4))),
  ("free_neutrino_octupole_CORRECT_k3",ef3,((0,3),(1,3))),
 ]
 checks={}
 for name,res,orders in families:
  for py,pk in orders:
   checks[f"{name}_y{py}_k{pk}"]=s.cancel(coeff(res,py,pk))==0
 failed=[key for key,val in checks.items() if not bool(val)]
 if failed:raise RuntimeError("MIXED_FINITE_K_GATE_FAIL "+str(failed))
 Delta_A=s.expand(Da+3*H*Ta/k**2)
 leading=s.simplify(coeff(Delta_A,0,2)/t**2)
 mixed=s.simplify(coeff(Delta_A,1,2)/t**2)
 if s.simplify(leading+(15+4*R)/40)!=0:
  raise RuntimeError("MIXED_FINITE_K_ZERO_MATTER_SEED_FAIL")
 if s.simplify(mixed-(15+4*R)/200)!=0:
  raise RuntimeError("MIXED_FINITE_K_SOURCE_CORRECTION_FAIL")
 if s.simplify(s.diff(mixed,B))!=0 or (
     s.simplify(s.diff(F,B))!=0 or s.simplify(s.diff(G,B))!=0):
  raise RuntimeError("MIXED_FINITE_K_BARYON_FRACTION_FAIL")
 return {
  "classification":"GE19_COUPLED_PRESSURELESS_PHOTON_BARYON_NEUTRINO_AESTLIKE_MIXED_Y_KTAU2_PASS_NOT_FULL_AEST",
  "checks":{k:bool(v) for k,v in checks.items()},
  "gate_count":len(checks),
  "expansion":"y_m=(rho_A+rho_b)/rho_r, beta=rho_b/(rho_b+rho_A), x=k*tau; first order y_m and x² including the mixed y_m*x² term",
  "metric_Phi_yx2_over_Psi0":str(s.factor(F)),
  "metric_Psi_yx2_over_Psi0":str(s.factor(G)),
  "Delta_A_x2_over_Psi0":str(s.factor(leading)),
  "Delta_A_yx2_over_Psi0":str(s.factor(mixed)),
  "Delta_A_compact":"Delta_A=-(15+4R_nu)*Psi0*(k*tau)**2/40*(1-y_m/5)+O(y_m**2,(k*tau)**4)",
  "beta_independence_of_mixed_Phi_Psi_Delta_A":True,
  "neutrino_hierarchy":"Quadrupole to O(y*x^4), octupole to O(y*x^3), necessary for Einstein shear y*x²",
  "caveats":"Strict tight-coupling photons, massless relativistic free-streaming neutrinos, separate pressureless AeST-like species, no actual Exp c_a², scalar/aether X/E initial state, NL0B bath, original Ward, neutrino mass transition, CLASS or DES.",
  "full_physics_GO":False,"DES_detection":False
 }
def main():
 p=argparse.ArgumentParser()
 p.add_argument("--repo-root",type=Path,default=Path(__file__).resolve().parents[2])
 p.add_argument("--self-test",action="store_true")
 p.add_argument("--out",type=Path)
 args=p.parse_args()
 if not args.self_test:source_locks(args.repo_root.resolve())
 result=derive()
 print("GE19_COUPLED_MIXED_FINITE_K_SYMBOLIC_PASS",result["gate_count"],flush=True)
 print("GE19_FULL_PHYSICS_GO False",flush=True)
 if args.out:
  out=args.out.resolve()
  if out.exists():raise RuntimeError("REFUSE_OVERWRITE "+str(out))
  out.parent.mkdir(parents=True,exist_ok=True)
  out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
  print("GE19_MIXED_FINITE_K_REPORT",out,flush=True)
 elif args.self_test:print(json.dumps(result,indent=2,sort_keys=True))
if __name__=="__main__":main()
