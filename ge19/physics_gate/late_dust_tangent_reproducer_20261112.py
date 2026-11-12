#!/usr/bin/env python3
"""GE19 one-k time-dependent eta=0 tangent; POST-RECOMBINATION DUST PROXY ONLY.
No original CLASS, photons, ncdm Boltzmann hierarchy, DES, or true primordial
bath history. Reset chi=E=q=p at a=0.05; this cannot predict full memory gain.
"""
import argparse, json, subprocess, re
from pathlib import Path
from functools import lru_cache
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import solve_ivp

LOCKS={
'v019/patch/source/aest_memory.c':'9a522a653a1855eda3cb67e856f9fc10a1e73d54',
'v019/ini/aest_exp.ini':'f9a2bde8921a148e063f9657a8ede0a51c6a629d',
'v019j/apply_memory_patch.py':'14796a5ed9e6265ed6810c792a93d7328a109364',
'ge19/physics_gate/constraint_projected_joint_operator_20261112.py':'b98bec1e1af46021d810676a062957d4efe80c58'}
N=np.array([.00031622776601683794,.0009261187281287938,.002712272579332028,
.007943282347242814,.02326305067153626,.06812920690579608,.19952623149688795,
.5843414133735175,1.7113283041617808,5.011872336272725,14.67799267622069,
42.986623470822764,125.89254117941675,368.69450645195735,1079.7751623277093])
W=np.array([.00035602,.00060227,.00185947,.00543372,.01590377,.04637989,
.13142693,.29663175,.30196035,.12703549,.04951583,.01380963,.0068728,
.00068313,.00177056])
H0=67.32117/299792.458; Hh=67.32117/100.
Q0=1e-4; Z0=1e-17; K2=9500.; KB=.1; C=1.9; I0=.000400912849822208377004114
K=.1*.6732117; A0=.05; A1=2/3; SCALE=1e-14; J=len(N)
OMG=N*H0; SW=np.sqrt(W); PHI0=-1e-7
RHO_S1=(.02238280+.06/93.14)/2997.92458**2  # neutrino-as-dust is an approximation

def locks(root):
 for p,sha in LOCKS.items():
  f=root/p
  if not f.is_file() or subprocess.check_output(['git','hash-object',str(f)],cwd=root,text=True).strip()!=sha:
   raise RuntimeError('GE19_SOURCE_LOCK_FAIL '+p)
 m=(root/'v019j/apply_memory_patch.py').read_text()
 def arr(name):
  z=re.search(r'static const double '+name+r'\[15\]\s*=\s*\{([^}]+)\}',m)
  if not z:raise RuntimeError('MISSING_BATH_NODES '+name)
  return np.fromstring(z.group(1).replace('\n',''),sep=',')
 if not (np.array_equal(arr('_aest_nodes16'),N) and np.array_equal(arr('_aest_weights16'),W)):
  raise RuntimeError('GE19_BATH_NODES_CHANGED')
 print('GE19_REDUCED_TANGENT_SOURCE_LOCKS_PASS',len(LOCKS))

@lru_cache(maxsize=32768)
def bg(u):
 a=np.exp(u); KQ=I0/a**3
 f=np.log(KQ/(4*K2*Z0))
 z=brentq(lambda zz:zz**2+np.log(zz)-f,1e-7,20,xtol=1e-13)
 Q=Q0+Z0*z; r=Z0*(-np.expm1(-z*z))/(2*z)
 rhoA=KQ*(Q-r)/3; cs=Z0*z/(Q*(1+2*z*z)); rs=RHO_S1/a**3
 # exact flat late-time AeST+dust+Lambda background at a=1
 ztoday=4.39281996821595767599
 rt=Z0*(-np.expm1(-ztoday*ztoday))/(2*ztoday)
 rhoA1=I0*(Q0+Z0*ztoday-rt)/3
 lam=H0**2-rhoA1-RHO_S1
 if lam<=0:raise RuntimeError('NEGATIVE_LAMBDA')
 return a,np.sqrt(rhoA+rs+lam),Q,KQ,cs,rs

def initial():
 a,H,Q,KQ,cs,rs=bg(np.log(A0)); RA=Q*KQ/3; RT=RA+rs
 theta=2*K*K*H*PHI0/(3*a*RT)
 delta=-2*(K*K*PHI0/a**2+3*H*H*PHI0)/(3*RT)
 phi=a*Q*theta/K**2
 y=np.zeros(6+2*J+6+2)
 y[:6]=[PHI0,delta,theta,phi,0,0]; y[-2]=RA*delta
 return y

def rhs(u,y):
 a,H,Q,KQ,cs,rs=bg(u); g=cs*K*K/(a*a*KQ); RA=Q*KQ/3
 phi0,ds,th,var,x,e=y[:6]; q=y[6:6+J]; p=y[6+J:6+2*J]
 dphi,dds,dth,dvar,dx,de=y[6+2*J:6+2*J+6]
 DA,dda=y[-2:]; Om=rs*(ds+3*a*H*th/K**2); Om1=rs*(dds+3*a*H*dth/K**2)
 phit=KQ*var/2+3*a*rs*th/(2*K**2)-H*phi0
 phit1=KQ*dvar/2+3*a*rs*dth/(2*K**2)-H*dphi
 f=KB*e+C*x; f1=KB*de+C*dx
 vt=Q*phi0-3*H*cs*var+g*(SCALE*f-2*phi0)-3*cs*Om/KQ
 xt=Q*e-3*H*cs*x+g*(f-2*phi0/SCALE)-3*(cs/SCALE)*Om/KQ
 b0=np.dot(W,np.full(J,x))-a*np.dot(OMG*SW,q)/K
 et=-H*e+(KQ*x-C*(xt-Q*e+(H+Q)*x))/KB
 v1=Q*dphi-3*H*cs*dvar+g*(f1-2*dphi)-3*cs*Om1/KQ
 x1=Q*de-3*H*cs*dx+g*(f1-2*dphi)-3*cs*Om1/KQ
 e1=-H*de+(KQ*dx-C*(x1-Q*de+(H+Q)*dx)-Q*b0/4)/KB
 # Independent linear AeST fluid density, for a non-tautological constraint check.
 pa=KQ*(-3*H*cs*var+g*(SCALE*f-2*phi0)-3*cs*Om/KQ)/3
 pa1=KQ*(-3*H*cs*dvar+g*(f1-2*dphi)-3*cs*Om1/KQ)/3
 dat=-3*H*(DA+pa)-KQ*K*K*var/(3*a*a)+3*RA*phit
 da1=-3*H*(dda+pa1)-KQ*K*K*dvar/(3*a*a)+3*RA*phit1
 return np.r_[phit,-th/a+3*phit,-H*th+K*K*phi0/a,vt,xt,et,
              p,-3*H*p-OMG**2*q+OMG*SW*K*x/a,
              phit1,-dth/a+3*phit1,-H*dth+K*K*dphi/a,v1,x1,e1,dat,da1]/H

def check(y):
 a,H,Q,KQ,cs,rs=bg(np.log(A1)); RA=Q*KQ/3
 P,ds,t,v=y[:4]; dp,dds,dt,dv=y[6+2*J:6+2*J+4]
 DA,da=y[-2:]; PP=KQ*v/2+3*a*rs*t/(2*K*K)-H*P
 PP1=KQ*dv/2+3*a*rs*dt/(2*K*K)-H*dp
 CH=K*K*P/a**2+3*H*(PP+H*P)+1.5*(DA+rs*ds)
 CH1=K*K*dp/a**2+3*H*(PP1+H*dp)+1.5*(da+rs*dds)
 scale0=max(abs(K*K*P/a**2),abs(1.5*(DA+rs*ds)))
 scale1=max(abs(K*K*dp/a**2),abs(1.5*(da+rs*dds)))
 if abs(CH)>1e-6*scale0 or abs(CH1)>1e-4*scale1:
  raise RuntimeError('GE19_EINSTEIN_CONSTRAINT_DRIFT')
 return float(CH/scale0),float(CH1/scale1)

def integrate(method,rtol,max_step):
 y=initial();atol=np.r_[ [1e-17,1e-14,1e-16,1e-17,1e-13,1e-13],
 np.full(2*J,1e-14),[1e-23,1e-21,1e-22,1e-23,1e-16,1e-16,1e-15,1e-21] ]
 sol=solve_ivp(rhs,(np.log(A0),np.log(A1)),y,method=method,rtol=rtol,
              atol=atol,max_step=max_step,t_eval=[np.log(A1)])
 if not sol.success:raise RuntimeError('GE19_INTEGRATOR_FAIL '+sol.message)
 z=sol.y[:,-1]; h,h1=check(z)
 return {'method':method,'rtol':rtol,'max_step':max_step,'nfev':sol.nfev,
         'Phi0':float(z[0]),'deta_W_over_W0':float(SCALE*z[6+2*J]/z[0]),
         'deta_W':float(SCALE*z[6+2*J]),'hamiltonian_relative':h,
         'tangent_hamiltonian_relative':h1,'chi0':float(SCALE*z[4]),
         'Bchi0':float(SCALE*(np.sum(W)*z[4]-A1*np.dot(OMG*SW,z[6:6+J])/K))}

def main():
 p=argparse.ArgumentParser()
 p.add_argument('--repo-root',type=Path,default=Path(__file__).resolve().parents[2])
 p.add_argument('--no-source-lock',action='store_true')
 p.add_argument('--out',type=Path)
 args=p.parse_args()
 if not args.no_source_lock:locks(args.repo_root.resolve())
 coarse=integrate('DOP853',3e-8,.04)
 fine=integrate('DOP853',3e-10,.01)
 independent=integrate('Radau',5e-9,.04)
 val=fine['deta_W_over_W0']; den=max(abs(val),1e-40)
 err1=abs(coarse['deta_W_over_W0']-val)/den
 err2=abs(independent['deta_W_over_W0']-val)/den
 if not (err1<.05 and err2<.05):raise RuntimeError('GE19_TANGENT_CONVERGENCE_FAIL')
 out={'classification':'GE19_CONSTRAINED_LATE_DUST_TANGENT_SCREEN_NOT_FULL_CLASS',
 'model':'Frozen Exp; AeST+standard dust proxy+Lambda; original 15 positive bath modes',
 'k_hmpc':.1,'a_initial':A0,'a_final':A1,
 'caveat':'Bath and aether restarted chi=E=q=p=0 at z=19, discarding primordial prehistory',
 'standard_neutrinos':'m_ncdm=0.06eV treated as pressureless dust, no photon/radiation, no hierarchy',
 'one_eta_zero_tangent_no_finite_eta_subtraction':True,
 'independent_density_ODE_enforces_Hamiltonian_constraint':True,
 'source_locks_executed':not args.no_source_lock,
 'source_blobs':LOCKS if not args.no_source_lock else {},
 'coarse':coarse,'fine':fine,'radau':independent,
 'convergence_rel_dop853':err1,'convergence_rel_radau':err2,
 'tangent_converged_in_this_reduced_model':True,
 'complete_action_to_CLASS_PHYSICS_GO':False,'full_DES_detection':False}
 print('GE19_LATE_DUST_TANGENT_DIRECT_PASS',val)
 print('GE19_TANGENT_INDEPENDENT_CONVERGENCE_PASS',err1,err2)
 print('GE19_FULL_CLASS_PHYSICS_GO False')
 if args.out:
  dest=args.out.resolve()
  if dest.exists():raise RuntimeError('REFUSE_OVERWRITE')
  dest.parent.mkdir(parents=True,exist_ok=True)
  dest.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
  print('GE19_REDUCED_TANGENT_RESULT',dest)
if __name__=='__main__':main()
