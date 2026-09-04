#!/usr/bin/env python3
from pathlib import Path
import json,csv
import numpy as np
from scipy.linalg import expm
from bath_designs import NODES20,WEIGHTS20,retarded_A,finite_kernel

OUT=Path('results');OUT.mkdir(exist_ok=True)
h=1.0
rows=[];mx=0.

for omega in [.3,1.,3.,10.,30.]:
    r=NODES20;w=WEIGHTS20;sw=np.sqrt(w);N=len(r)

    # Augmented constant-coefficient time-domain system.  The last two states
    # are c=cos(omega t), s=sin(omega t).  This exact matrix propagator avoids
    # contaminating the audit with stiffness from the six-decade bath span.
    M=np.zeros((2*N+2,2*N+2))
    for j in range(N):
        M[j,N+j]=1.0
        M[N+j,j]=-r[j]*r[j]
        M[N+j,N+j]=-3.0*h
        M[N+j,2*N]=r[j]*sw[j]
    M[2*N,2*N+1]=-omega
    M[2*N+1,2*N]=omega

    period=2*np.pi/omega
    steps_per_period=96
    dt=period/steps_per_period
    P=expm(M*dt)
    nperiod=14
    nstep=nperiod*steps_per_period
    y=np.zeros(2*N+2);y[2*N]=1.0
    keep=[]
    for n in range(nstep+1):
        if n >= (nperiod-4)*steps_per_period:
            q=y[:N].copy();chi=y[2*N]
            B=float(np.sum(w*chi-sw*r*q))
            keep.append((n*dt,chi,y[2*N+1],B))
        y=P@y

    arr=np.asarray(keep)
    ts=arr[:,0];B=arr[:,3]
    X=np.column_stack([np.cos(omega*ts),np.sin(omega*ts),np.ones_like(ts)])
    coef=np.linalg.lstsq(X,B,rcond=None)[0]
    measured=coef[0]-1j*coef[1]

    s=1j*omega
    A=retarded_A(s,h)
    target=finite_kernel(A,r,w)
    rel=float(abs(measured-target)/max(abs(target),1e-300));mx=max(mx,rel)
    rows.append([omega,measured.real,measured.imag,target.real,target.imag,rel,float(coef[2]),nstep])

with open(OUT/'time_domain_drive.csv','w',newline='') as f:
    wr=csv.writer(f);wr.writerow(['omega_over_H','measured_real','measured_imag','finite_transfer_real','finite_transfer_imag','relative_error','dc_fit','propagator_steps']);wr.writerows(rows)

out={
 'Htau':h,'tested_omega_over_H':[r[0] for r in rows],
 'max_relative_error_time_domain_vs_finite_transfer':mx,
 'method':'exact matrix exponential of the driven oscillator system',
 'interpretation':'A PASS validates the oscillator equations/factors against their own finite-bath transfer function; it does not validate the finite bath against the continuum Drude kernel.',
 'gate_status':'PASS' if mx<5e-8 else 'CHECK'
}
(OUT/'time_domain_drive_summary.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
