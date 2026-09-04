#!/usr/bin/env python3
from pathlib import Path
import json,csv
import numpy as np
from scipy.integrate import solve_ivp
from bath_designs import NODES20,WEIGHTS20,retarded_A,finite_kernel

OUT=Path('results');OUT.mkdir(exist_ok=True)
h=1.0
rows=[];mx=0.

for omega in [.3,1.,3.,10.,30.]:
    r=NODES20;w=WEIGHTS20;sw=np.sqrt(w);N=len(r)
    period=2*np.pi/omega
    tend=max(80.,18*period)
    def rhs(t,y):
        q=y[:N];p=y[N:]
        chi=np.cos(omega*t)
        return np.r_[p,-3*h*p-r*r*q+r*sw*chi]
    sol=solve_ivp(rhs,(0,tend),np.zeros(2*N),method='DOP853',rtol=2e-10,atol=2e-12,
                  max_step=min(.08,period/35),dense_output=True)
    t0=tend-6*period
    ts=np.linspace(t0,tend,2400)
    q=sol.sol(ts)[:N]
    chi=np.cos(omega*ts)
    B=np.sum(w[:,None]*chi[None,:]-sw[:,None]*r[:,None]*q,axis=0)
    X=np.column_stack([np.cos(omega*ts),np.sin(omega*ts),np.ones_like(ts)])
    coef=np.linalg.lstsq(X,B,rcond=None)[0]
    measured=coef[0]-1j*coef[1]
    s=1j*omega
    A=retarded_A(s,h)
    target=finite_kernel(A,r,w)
    rel=float(abs(measured-target)/max(abs(target),1e-300));mx=max(mx,rel)
    rows.append([omega,measured.real,measured.imag,target.real,target.imag,rel,float(coef[2]),sol.nfev])

with open(OUT/'time_domain_drive.csv','w',newline='') as f:
    wr=csv.writer(f);wr.writerow(['omega_over_H','measured_real','measured_imag','finite_transfer_real','finite_transfer_imag','relative_error','dc_fit','nfev']);wr.writerows(rows)

out={
 'Htau':h,'tested_omega_over_H':[r[0] for r in rows],
 'max_relative_error_time_domain_vs_finite_transfer':mx,
 'interpretation':'A PASS validates the oscillator equations/factors against their own finite-bath transfer function; it does not validate the finite bath against the continuum Drude kernel.',
 'gate_status':'PASS' if mx<3e-4 else 'CHECK'
}
(OUT/'time_domain_drive_summary.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
