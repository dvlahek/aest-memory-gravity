#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, os, subprocess, sys
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from fullj_weyl import aest_ulp_initial_amplitude_localization as amp
from fullj_weyl import aest_stable_chi_precision_convergence as pc

PREDATA_LOCK='68a9341a9648cd490dfb9b599577ae3e1e296086'
R1B_POSTDATA_LOCK='0c9ddd2488cdbfc3fc668ebefaf140c8b2e3583a'
R1B_JSON=ROOT/'results/stable_aest_finite_memory_r1b.json'
HOST_JSON=ROOT/'results/fullj_aest_stable_chi_precision_floor.json'
R1B_CLASS='STABLE_AEST_FINITE_MEMORY_R1B_ETA_TANGENT_FAIL'
HOST_CLASS='FULLJ_AEST_STABLE_CHI_PRECISION_FLOOR_CERTIFIED'
ANCHORS=(0.09875,0.16125,0.19500)
ORDERS=(16,20)
ETAS=(0.0,0.005,0.01)
TAU=10.0
TOL=3e-8
Z=np.asarray([6.,5.,4.,3.,2.,1.5,1.,0.5,0.2])

INCOMPLETE='STABLE_AEST_FINITE_MEMORY_R1C_INCOMPLETE'
NUMFAIL='STABLE_AEST_FINITE_MEMORY_R1C_NUMERICAL_FAIL'
ETAFAIL='STABLE_AEST_FINITE_MEMORY_R1C_ETA_TANGENT_FAIL'
ORDERFAIL='STABLE_AEST_FINITE_MEMORY_R1C_BATH_ORDER_FAIL'
UNRES='STABLE_AEST_FINITE_MEMORY_R1C_RESPONSE_UNRESOLVED'
PASS='STABLE_AEST_FINITE_MEMORY_R1C_LONG_RELAXATION_CERTIFIED'

def ancestor(s):
 return subprocess.run(['git','merge-base','--is-ancestor',s,'HEAD'],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode==0

def rel(a,b):
 a=np.asarray(a,float); b=np.asarray(b,float)
 return float(np.linalg.norm(a-b)/max(float(np.linalg.norm(a)),float(np.linalg.norm(b)),1e-300))

def cosine(a,b):
 a=np.asarray(a,float); b=np.asarray(b,float); na=float(np.linalg.norm(a)); nb=float(np.linalg.norm(b))
 if na==0 or nb==0:return float('nan')
 return float(np.dot(a,b)/(na*nb))

def field(raw,names): return pc.field_at_z(raw,names)
def extract(raw):
 phi=field(raw,('phi',)); psi=field(raw,('psi',))
 return {'W':phi+psi,'delta':field(raw,('delta_cdm',)),'alpha':field(raw,('alpha_aest','alpha')),'E':field(raw,('E_aest','E')),'s':field(raw,('s_aest',))}

def run_case(kh,order,eta):
 bits=pc.bits_for_anchor(kh); p,pos=amp.make_params(kh,int(bits))
 p['tol_perturbations_integration']=float(TOL)
 p['aest_memory_enabled']='yes'; p['aest_memory_order']=int(order); p['aest_eta']=float(eta); p['aest_tau_H0']=float(TAU)
 raw,nh=amp.raw_target(p,pos,True); vals=extract(raw)
 ok=all(np.all(np.isfinite(v)) for v in vals.values())
 return vals,int(nh),int(pos),int(bits),bool(ok)

def source_ok():
 root=os.environ.get('AEST_STABLE_CLASS_ROOT','')
 if not root:return False
 root=Path(root); paths=[root/'source/perturbations.c',root/'include/perturbations.h',root/'include/background.h',root/'source/aest_memory.c']
 if not all(p.is_file() for p in paths):return False
 text='\n'.join(p.read_text() for p in paths)
 req=('FULLJ_AEST_STABLE_CHI_RESIDUAL_V1','double chi_aest = Q_aest*s_aest;','aest_memory_enabled','aest_memory_order','E_rhs_aest -= 0.5*Q_aest*Bchi_aest','if (order == 16)','if (order == 20)')
 return all(x in text for x in req) and text.count('double chi_aest = Q_aest*s_aest;')>=2

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--json-out',default='results/stable_aest_finite_memory_r1c.json'); ap.add_argument('--npz-out',default='results/stable_aest_finite_memory_r1c.npz'); a=ap.parse_args()
 print('STABLE_AEST_FINITE_MEMORY_R1C_START',flush=True)
 if not R1B_JSON.exists() or not HOST_JSON.exists():
  out={'classification':INCOMPLETE,'diagnostic_complete':False,'reason':'missing parent json'}; Path(a.json_out).write_text(json.dumps(out,indent=2)+'\n'); return 3
 r1b=json.loads(R1B_JSON.read_text()); host=json.loads(HOST_JSON.read_text())
 g1=bool(ancestor(PREDATA_LOCK) and ancestor(R1B_POSTDATA_LOCK) and r1b.get('classification')==R1B_CLASS and host.get('classification')==HOST_CLASS and source_ok())
 vals={}; rows=[]; arrays={'redshifts':Z}; allfinite=True
 for kh in ANCHORS:
  for order in ORDERS:
   for eta in ETAS:
    v,nh,pos,bits,ok=run_case(kh,order,eta); vals[(kh,order,eta)]=v; allfinite &= ok
    tag=pc.tag_of(kh); et=f'{eta:.3f}'.replace('.','p')
    for n,x in v.items(): arrays[f'{n}_{tag}_o{order}_e{et}']=x
    rows.append({'k_h':kh,'order':order,'eta':eta,'finite':ok,'histories':nh,'target_pos':pos,'bits':bits})
    print(f'STABLE_AEST_FINITE_MEMORY_R1C_RUN k_h={kh:.5f} order={order} eta={eta:.3g} finite={ok} histories={nh} pos={pos}',flush=True)
 eta_rows=[]; eta_strict=0; eta_loose=True; response_count=0; response_all=True
 Q={}; A={}
 for kh in ANCHORS:
  for order in ORDERS:
   z=vals[(kh,order,0.0)]['W']; d5=vals[(kh,order,0.005)]['W']-z; d10=vals[(kh,order,0.01)]['W']-z
   q5=d5/0.005; q10=d10/0.01; Q[(kh,order)]=q10
   e=rel(q5,q10); strict=e<=0.02; loose=e<=0.05; eta_strict+=int(strict); eta_loose &= loose
   aw=float(np.linalg.norm(d10)/max(float(np.linalg.norm(z)),1e-300)); A[(kh,order)]=aw
   nonzero=bool(np.all(np.isfinite(q10)) and np.linalg.norm(q10)>0); response_all &= nonzero; response_count += int(nonzero and aw>=1e-12)
   eta_rows.append({'k_h':kh,'order':order,'E_eta':e,'strict_pass':strict,'loose_pass':loose,'A_M_W':aw,'nonzero':nonzero})
   print(f'STABLE_AEST_FINITE_MEMORY_R1C_ETA k_h={kh:.5f} order={order} E={e:.3e} A={aw:.3e} strict={strict}',flush=True)
 order_rows=[]; order_strict=0; order_loose=True
 for kh in ANCHORS:
  q16=Q[(kh,16)]; q20=Q[(kh,20)]; e=rel(q16,q20); c=cosine(q16,q20)
  strict=bool(e<=0.10 and c>=0.99); loose=bool(e<=0.20 and c>=0.95); order_strict+=int(strict); order_loose &= loose
  order_rows.append({'k_h':kh,'E_order':e,'cosine':c,'strict_pass':strict,'loose_pass':loose})
  print(f'STABLE_AEST_FINITE_MEMORY_R1C_ORDER k_h={kh:.5f} E={e:.3e} cos={c:.9f} strict={strict}',flush=True)
 g2=bool(allfinite); g3=bool(eta_loose and eta_strict>=5); g4=bool(order_loose and order_strict>=2); g5=bool(response_all and response_count>=5)
 gates={'R1C_G1_provenance_and_parent_lock':g1,'R1C_G2_numerical_regularity':g2,'R1C_G3_heldout_eta_tangent_consistency':g3,'R1C_G4_bath_order_tangent_consistency':g4,'R1C_G5_resolved_nonzero_response':g5}
 if not g1:cl=INCOMPLETE
 elif not g2:cl=NUMFAIL
 elif not g3:cl=ETAFAIL
 elif not g4:cl=ORDERFAIL
 elif not g5:cl=UNRES
 else:cl=PASS
 summary={'classification':cl,'run_count':len(rows),'eta_strict_pass_count':eta_strict,'order_strict_pass_count':order_strict,'resolved_amplitude_pass_count':response_count,'max_eta_error':float(max(r['E_eta'] for r in eta_rows)),'max_order_error':float(max(r['E_order'] for r in order_rows)),'min_order_cosine':float(min(r['cosine'] for r in order_rows)),'min_A_M_W':float(min(r['A_M_W'] for r in eta_rows))}
 out={'classification':cl,'diagnostic_complete':True,'predata_lock':PREDATA_LOCK,'r1b_parent_classification':r1b.get('classification'),'host_parent_classification':host.get('classification'),'settings':{'anchors':list(ANCHORS),'orders':list(ORDERS),'etas':list(ETAS),'tau_H0':TAU,'tol_perturbations_integration':TOL,'redshifts':Z.tolist()},'gates':gates,'summary':summary,'runs':rows,'eta_tangent':eta_rows,'bath_order':order_rows,'interpretation':{'historical_R1_reclassified':False,'historical_R1b_reclassified':False,'tau1_certified':False,'observational_claim_licensed':False,'new_physics_claim_licensed':False,'long_relaxation_growth_Weyl_followup_licensed':cl==PASS}}
 Path(a.json_out).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n'); np.savez_compressed(a.npz_out,**arrays)
 print('STABLE_AEST_FINITE_MEMORY_R1C_GATES='+json.dumps(gates,sort_keys=True),flush=True); print('STABLE_AEST_FINITE_MEMORY_R1C_SUMMARY='+json.dumps(summary,sort_keys=True),flush=True); print('STABLE_AEST_FINITE_MEMORY_R1C_CLASSIFICATION='+cl,flush=True)
 return 0 if cl==PASS else 1
if __name__=='__main__': raise SystemExit(main())
