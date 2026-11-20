#!/usr/bin/env python3
"""GE19: efficient self-checked Bchi causal source split on existing CLASS trace.

No CLASS runs, no rerun of the original baseline, no observational claims.
Retains exact original q oscillator dynamics and integrates on the actual
141494-row accepted source time mesh with a high-order explicit RK4 step.
Performs independent 1x/2x mesh-refinement reproducibility before any output.
"""
from __future__ import annotations

import argparse, json, math, subprocess
from pathlib import Path
import numpy as np

import reconstruct_native_Bchi_instant_delayed_20261120 as base

PARENT_BLOB = "fdf8826325460e6d38940d4ac5fe9e6fb760f4fb"

def require(cond, message):
 if not bool(cond):
  raise RuntimeError("GE19_FAST_HISTORY_"+message)

def verify_parent(root):
 path=root/"ge19/physics_gate/reconstruct_native_Bchi_instant_delayed_20261120.py"
 got=subprocess.check_output(["git","hash-object",str(path)],cwd=root,text=True).strip()
 require(got==PARENT_BLOB,"PARENT_INVERSE_SOURCE_CHANGED")
 print("GE19_FAST_HISTORY_PARENT_LOCK_PASS",flush=True)

def fixed_rk4(data,nodes,weights,H0,refinement,max_time_step=0.1):
 """Integrate q and r=a² q' with the original oscillator force.

 Known B = Wb chi - (a/k) d.q, where d_i=omega_i sqrt(w_i).
 chi = (B+(a/k)d.q)/Wb.
 Thus q'=r/a², r'=-a⁴(omega²*q-d*(d.q)/Wb)
                         + a³*k*d*B/Wb .
 Piecewise LINEAR a(t), B(t) on the original accepted trace.
 """
 require(refinement in (1,2),"REFINEMENT")
 t=data[:,0]
 a=data[:,1]
 B=data[:,4]
 n=len(nodes)
 omega=nodes*H0
 wroot=np.sqrt(weights)
 d=omega*wroot
 Wb=float(np.sum(weights))
 require(Wb>0 and np.all(omega>0),"BATH_DESIGN")
 k=base.K_MPC
 max_dt=float(np.max(np.diff(t)))
 max_omega=float(np.max(omega))
 require(np.isfinite(max_dt) and max_dt>0,"TIME_STEP")
 require(max_dt*max_omega < 1000,"UNSAFE_TIME_SCALE")
 q=np.zeros(n,dtype=float)
 r=np.zeros(n,dtype=float)
 delayed=np.zeros(len(t),dtype=float)
 omega_sq=omega*omega
 scaled_d=d/Wb
 kd=k*scaled_d
 def rhs(qv,rv,aval,bval):
  d_q=float(np.dot(d,qv))
  dq=rv/(aval*aval)
  dr=-(aval**4)*(omega_sq*qv-scaled_d*d_q)+aval**3*kd*bval
  return dq,dr
 steps=0
 for i in range(len(t)-1):
  h=float(t[i+1]-t[i])
  ai=float(a[i]); af=float(a[i+1])
  bi=float(B[i]); bf=float(B[i+1])
  substeps=refinement*max(1,int(math.ceil(h/max_time_step-1e-12)))
  dt=h/substeps
  for j in range(substeps):
   x0=j/substeps; x1=(j+1)/substeps; xm=(x0+x1)/2
   a0=ai+(af-ai)*x0
   am=ai+(af-ai)*xm
   a1=ai+(af-ai)*x1
   b0=bi+(bf-bi)*x0
   bm=bi+(bf-bi)*xm
   b1=bi+(bf-bi)*x1
   q1,r1=rhs(q,r,a0,b0)
   q2,r2=rhs(q+dt*q1/2,r+dt*r1/2,am,bm)
   q3,r3=rhs(q+dt*q2/2,r+dt*r2/2,am,bm)
   q4,r4=rhs(q+dt*q3,r+dt*r3,a1,b1)
   q=q+dt*(q1+2*q2+2*q3+q4)/6
   r=r+dt*(r1+2*r2+2*r3+r4)/6
   steps+=1
  if (i%5000)==0:
   require(np.all(np.isfinite(q)) and np.all(np.isfinite(r)),
           "NONFINITE_INTEGRATION")
  delayed[i+1]=-af/k*float(np.dot(d,q))
 require(np.all(np.isfinite(delayed)),"NONFINITE_DELAYED_SOURCE")
 return delayed,steps,max_dt,max_omega

def synthetic_fast():
 """Independent known pulse; piecewise-linear B interpolation expected O(dt²)."""
 import numpy as np
 t=np.linspace(0,np.pi,801)
 a=np.ones_like(t)
 k=base.K_MPC
 w=.67
 ampl=1.3
 B=2*w*ampl/3*(np.cos(t)-np.cos(2*t))
 data=np.column_stack([t,a,np.full_like(t,k),np.zeros_like(t),B])
 # choose node omega=1 and H0=1; weights single oscillator
 delayed,steps,_,_=fixed_rk4(data,np.array([1.]),np.array([w]),1.,1)
 qexact=k*np.sqrt(w)*ampl/6*(3+np.cos(2*t)-4*np.cos(t))
 expected=-np.sqrt(w)*qexact/k
 error=float(np.max(np.abs(delayed-expected)))
 require(error<5e-5,"SYNTHETIC_FAST_INVERSE_FAILED")
 print("GE19_FAST_HISTORY_SYNTHETIC_PASS",format(error,".9g"),flush=True)
 return error

def main():
 p=argparse.ArgumentParser()
 p.add_argument("--repo-root",type=Path,default=Path(__file__).resolve().parents[2])
 p.add_argument("--baseline",type=Path)
 p.add_argument("--out-dir",type=Path)
 p.add_argument("--self-test",action="store_true")
 p.add_argument("--time-step-ceiling",type=float,default=0.1)
 p.add_argument("--max-relative-refinement-error",type=float,default=0.001)
 args=p.parse_args()
 synthetic_fast()
 if args.self_test:return
 require(args.baseline is not None and args.out_dir is not None,
         "NEED_BASELINE_AND_OUT_DIR")
 require(args.time_step_ceiling>0 and args.time_step_ceiling<=.1,
         "STEP_CEILING")
 require(0<args.max_relative_refinement_error<=.001,"REFINEMENT_THRESHOLD")
 root=args.repo_root.resolve()
 verify_parent(root)
 base.locks(root)
 nodes,weights=base.bath_design((root/"v019j/apply_memory_patch.py").read_text())
 ini=(root/"v019/ini/aest_exp.ini").read_text()
 import re
 match=re.search(r"(?m)^H0\s*=\s*([0-9.]+)\s*$",ini)
 require(match is not None,"H0_MISSING")
 H0=float(match.group(1))/299792.458
 data=base.input_trace(args.baseline.resolve())
 print("GE19_FAST_HISTORY_TRACE_ACCEPTED",len(data),flush=True)
 first,n1,max_dt,max_om=fixed_rk4(data,nodes,weights,H0,1,args.time_step_ceiling)
 print("GE19_FAST_HISTORY_FIRST_PASS_COMPLETE",n1,flush=True)
 second,n2,_,_=fixed_rk4(data,nodes,weights,H0,2,args.time_step_ceiling)
 print("GE19_FAST_HISTORY_SECOND_PASS_COMPLETE",n2,flush=True)
 total=data[:,4]
 err=float(np.max(np.abs(first-second)))
 max_total=float(np.max(np.abs(total)))
 max_delayed=float(np.max(np.abs(second)))
 relative_to_total=err/max(max_total,1e-300)
 relative_to_delayed=err/max(max_delayed,1e-300)
 print("GE19_FAST_HISTORY_REFINEMENT",format(err,".9g"),
       format(relative_to_total,".9g"),format(relative_to_delayed,".9g"),
       flush=True)
 require(relative_to_total<=args.max_relative_refinement_error and
         relative_to_delayed<=args.max_relative_refinement_error,
         "REFINEMENT_NO_GO")
 delayed=second
 inst=total-delayed
 chi=inst/float(np.sum(weights))
 out=args.out_dir.resolve()
 require(not out.exists(),"OUTPUT_EXISTS")
 base.output(data,out,inst,delayed,chi,float(np.sum(weights)),H0,
             args.time_step_ceiling,0,{'fast_synthetic_pulse_error':synthetic_fast()})
 path=out/"GE19_BCHI_SOURCE_SPLIT_DIAGNOSTIC.json"
 report=json.loads(path.read_text())
 report.update({
  "classification":"GE19_HISTORIC_BCHI_INSTANT_DELAYED_NUMERICALLY_RECONSTRUCTED_NOT_PHYSICAL_WEYL",
  "inverse_method":"piecewise-linear original trace; canonical r=a^2 qprime; fixed RK4; 1x/2x refinement",
  "RK4_first_pass_steps":n1,"RK4_second_pass_steps":n2,
  "max_original_interval_tau_Mpc":max_dt,
  "max_bath_frequency_Mpc_inverse":max_om,
  "max_retarded_force_absolute_refinement_difference":err,
  "refinement_difference_over_max_abs_original_Bchi":relative_to_total,
  "refinement_difference_over_max_abs_delayed_Bchi":relative_to_delayed,
  "refinement_threshold":args.max_relative_refinement_error,
  "internal_RK4_refinement_verified":True,
  "independent_numerical_convergence_verified":False,
  "inverse_low_frequency_conditioning_certified":False,
  "reason_no_independent_convergence":"RK4 1x/2x controls integration steps, not source-trace interpolation or unknown initial state",
  "historical_INPUT_physical_Ward_certified":False,
  "original_q_p_initial_state_independently_verified":False,
  "full_physics_GO":False,
  "W1_delayed_computed":False
 })
 path.write_text(json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+"\n")
 print("GE19_FAST_HISTORY_SPLIT_REFINEMENT_PASS",flush=True)
 print("GE19_FAST_HISTORY_REPORT",path,flush=True)
 print("GE19_FULL_PHYSICS_GO False",flush=True)

if __name__=="__main__":
 main()
