#!/usr/bin/env python3
"""Recover instant/delayed NL0B forcing from frozen full-CLASS Bchi history.
Causal Volterra inverse diagnostic, NOT a full physical Weyl-memory result.
Never patches CLASS or evolves a new cosmological baseline.
"""
from __future__ import annotations
import argparse,csv,hashlib,json,math,re,subprocess
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp

PARENT_BLOBS = {
 'v019j/apply_memory_patch.py': '14796a5ed9e6265ed6810c792a93d7328a109364',
 'v019/ini/aest_exp.ini': 'f9a2bde8921a148e063f9657a8ede0a51c6a629d',
 'ge19/physics_gate/one_forced_tangent_from_existing_history_20261113.py':'b3ea48edd926c38c7bb9a8fc3b13318875ab27f0',
 'ge19/physics_gate/run_full_class_two_pass_tangent_20261112.py':'94af6d14826d0621410204554e9d246a89660806',
}
FROZEN_BASELINE_SHA256='fbe1212cbc052343e283edae1c7496e631da6056ad983d575fd2d699e9bf2e19'
K_MPC=0.06732117

def require(ok,label):
 if not bool(ok):raise RuntimeError('GE19_HISTORY_SPLIT_'+label)

def sha(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()

def locks(root):
 for path,expected in PARENT_BLOBS.items():
  p=root/path
  require(p.is_file(),'SOURCE_MISSING '+path)
  actual=subprocess.check_output(['git','hash-object',str(p)],cwd=root,text=True).strip()
  require(actual==expected,'SOURCE_CHANGED '+path)
 print('GE19_HISTORY_INVERSE_SOURCE_LOCKS_PASS',len(PARENT_BLOBS),flush=True)

def bath_design(text):
 def take(name):
  pattern=r'static\s+const\s+double\s+_aest_'+name+r'16\[15\]\s*=\s*\{([^}]*)\}'
  m=re.search(pattern,text)
  require(m is not None,'FROZEN_BATH_DESIGN_MISSING_'+name)
  v=np.array([float(x.strip()) for x in m.group(1).split(',') if x.strip()])
  require(len(v)==15 and np.all(np.isfinite(v)),'BATH_DESIGN_SHAPE_'+name)
  return v
 nodes=take('nodes');weights=take('weights')
 require(np.all(nodes>0) and np.all(weights>0),'BATH_NONPOSITIVE')
 return nodes,weights

def synthetic():
 # Known independent exact nonstatic oscillator with omega=1, a=1.
 omega,k,w,A,T=1.0,K_MPC,.67,1.3,math.pi
 t=np.linspace(0,T,501)
 def B(time):return 2*w*A/3*(np.cos(time)-np.cos(2*time))
 def rhs(time,z):
  q,r=z
  chi=(B(time)+omega*np.sqrt(w)*q/k)/w
  return [r,-omega**2*q+k*omega*np.sqrt(w)*chi]
 sol=solve_ivp(rhs,(0,T),[0,0],t_eval=t,method='DOP853',
               max_step=.013,rtol=2e-12,atol=2e-13)
 require(sol.success,'SYNTHETIC_IVP_FAILED')
 q=sol.y[0]
 chi=(B(t)+omega*np.sqrt(w)*q/k)/w
 echi=float(np.max(np.abs(chi-A*np.sin(t)**2)))
 eq=float(np.max(np.abs(q-(k*np.sqrt(w)*A/6)*(3+np.cos(2*t)-4*np.cos(t)))))
 require(echi<1e-9 and eq<1e-9,'SYNTHETIC_INVERSE_BAD')
 print('GE19_HISTORY_INVERSE_SYNTHETIC_PASS',echi,eq,flush=True)
 return {'chi_max_abs_error':echi,'q_max_abs_error':eq}

def input_trace(path):
 require(sha(path)==FROZEN_BASELINE_SHA256,'FROZEN_BASELINE_SHA256_MISMATCH')
 with path.open(newline='') as f:
  data=np.asarray([
   [float(row[x]) for x in ('tau','a','k_mpc','W','Bchi')]
   for row in csv.DictReader(f)],dtype=float)
 require(data.shape==(141494,5),'TRACE_SHAPE')
 require(np.all(np.isfinite(data)),'NONFINITE_TRACE')
 require(np.all(np.diff(data[:,0])>0) and np.all(np.diff(data[:,1])>0),'NONMONOTONE')
 require(np.all(np.abs(data[:,2]-K_MPC)<K_MPC*1e-11),'MODE_K_CHANGED')
 require(data[0,1]<1e-5 and data[-1,1]>.99,'TRACE_COVERAGE')
 return data

def reconstruct(data,nodes,weights,H0,max_step,rtol):
 times,a,_,_,B=data.T
 omega=H0*nodes
 sw=np.sqrt(weights)
 Wb=float(np.sum(weights))
 n=len(omega)
 k=K_MPC
 # r_j=a² q_j' removes 2Hconf q_j' without differentiating tabulated a.
 # Exact causal inverse: chi=(B + a/k * sum(omega sqrt(w) q))/Wb.
 def rhs(t,z):
  q=z[:n]
  r=z[n:]
  at=float(np.interp(t,times,a))
  bt=float(np.interp(t,times,B))
  chi=(bt+(at/k)*np.dot(omega*sw,q))/Wb
  return np.r_[r/(at*at),-at**4*omega**2*q+at**3*k*omega*sw*chi]
 result=solve_ivp(rhs,(float(times[0]),float(times[-1])),
                  np.zeros(2*n),t_eval=times,method='DOP853',
                  max_step=max_step,rtol=rtol,atol=1e-10)
 require(result.success,'SOLVER_'+str(result.message))
 q=result.y[:n]
 Bdel=-(a/k)*np.einsum('i,ij->j',omega*sw,q,optimize=True)
 Binst=B-Bdel
 chi=Binst/Wb
 require(np.all(np.isfinite(Bdel)) and np.all(np.isfinite(chi)),
         'NONFINITE_RECONSTRUCTION')
 require(float(np.max(np.abs(B-(Binst+Bdel))))<
         1e-11*(1+float(np.max(np.abs(B)))),'SUM_NOT_CLOSED')
 return Binst,Bdel,chi,Wb

def output(data,out,inst,delayed,chi,Wb,H0,max_step,rtol,check):
 require(not out.exists(),'OUTPUT_DIR_EXISTS')
 out.mkdir(parents=True)
 files={}
 for name,values in (('instantaneous',inst),('delayed',delayed)):
  path=out/(name+'_Bchi.csv')
  with path.open('w',newline='') as f:
   writer=csv.writer(f)
   writer.writerow(['tau','a','k_mpc','W','Bchi'])
   for orig,v in zip(data,values):
    writer.writerow([format(x,'.17g') for x in (orig[0],orig[1],orig[2],orig[3],v)])
  files[name]=sha(path)
 report={
  'classification':'GE19_FROZEN_NATIVE_CLASS_BCHI_CAUSAL_SPLIT_DIAGNOSTIC_NOT_PHYSICAL_WEYL',
  'source_locks':True,'synthetic_inverse':check,
  'original_baseline_sha256':FROZEN_BASELINE_SHA256,
  'sample_count':len(data),'k_Mpc_inverse':K_MPC,
  'active_bath_nodes':15,'W_b':Wb,'H0_Mpc_inverse':H0,
  'inverse_initial_conditions':'q_j=qprime_j=0 at first saved source time (ASSUMED)',
  'inverse_method':'causal Volterra second-kind, a² qprime state, DOP853',
  'max_step_tau_Mpc':max_step,'rtol':rtol,
  'max_abs_total':float(np.max(np.abs(data[:,4]))),
  'max_abs_instantaneous':float(np.max(np.abs(inst))),
  'max_abs_delayed':float(np.max(np.abs(delayed))),
  'cancellation_indicator':float(
     (np.max(np.abs(inst))+np.max(np.abs(delayed)))/
     max(np.max(np.abs(data[:,4])),1e-300)),
  'output_csv_sha256':files,
  'instant_plus_delayed_algebraic_sum_pass':True,
  'independent_original_q_chi_trace_validation':False,
  'true_initial_bath_state_at_first_saved_time_verified':False,
  'independent_numerical_convergence_verified':False,
  'W1_instantaneous_computed':False,'W1_delayed_computed':False,
  'physical_delayed_Weyl_memory_certified':False,'FULL_PHYSICS_GO':False,
  'warning':'Input source B from historic provisional CLASS baseline; no full Ward/primordial certification. A small total B compared with its split pieces can amplify integration error. The two CSVs are diagnostic force inputs, not observational predictions.'
 }
 result=out/'GE19_BCHI_SOURCE_SPLIT_DIAGNOSTIC.json'
 result.write_text(json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+'\n')
 print('GE19_BCHI_SPLIT_DIAGNOSTIC_WRITTEN',result,flush=True)
 print('GE19_FULL_PHYSICS_GO False',flush=True)

def main():
 p=argparse.ArgumentParser()
 p.add_argument('--repo-root',type=Path,default=Path(__file__).resolve().parents[2])
 p.add_argument('--baseline',type=Path)
 p.add_argument('--out-dir',type=Path)
 p.add_argument('--self-test',action='store_true')
 p.add_argument('--max-step',type=float,default=.1)
 p.add_argument('--rtol',type=float,default=1e-8)
 args=p.parse_args()
 check=synthetic()
 if args.self_test:return
 require(args.baseline is not None and args.out_dir is not None,
         'NEED_BASELINE_AND_OUTPUT_DIR')
 require(0<args.max_step<=.1,'MAX_STEP_OUT_OF_RANGE')
 require(1e-11<=args.rtol<=1e-6,'RTOL_OUT_OF_RANGE')
 root=args.repo_root.resolve()
 locks(root)
 nodes,weights=bath_design((root/'v019j/apply_memory_patch.py').read_text())
 ini=(root/'v019/ini/aest_exp.ini').read_text()
 m=re.search(r'(?m)^H0\s*=\s*([0-9.]+)\s*$',ini)
 require(m is not None,'H0_MISSING')
 H0=float(m.group(1))/299792.458
 data=input_trace(args.baseline.resolve())
 inst,delayed,chi,Wb=reconstruct(data,nodes,weights,H0,args.max_step,args.rtol)
 output(data,args.out_dir.resolve(),inst,delayed,chi,Wb,H0,
        args.max_step,args.rtol,check)
if __name__=='__main__':main()
