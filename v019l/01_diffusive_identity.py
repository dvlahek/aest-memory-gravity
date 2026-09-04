#!/usr/bin/env python3
from pathlib import Path
import json,csv
import numpy as np
from scipy.integrate import quad
from passive_rational import exact_kernel

OUT=Path('results');OUT.mkdir(exist_ok=True)


def diffusive_integral(z,h):
    a=3.0*h
    D=np.sqrt(a*a+4.0)
    r0=(a+D)/2.0
    c0=2.0/(r0*D)
    def mu(r):
        y=np.sqrt(max(r*(a-r),0.0))
        return y/(np.pi*r*(1.0+y*y))
    def term(r):
        return mu(r)*z/(z+r)
    re=quad(lambda r:term(r).real,0,a,epsabs=2e-11,epsrel=2e-11,limit=1000,points=[0,a])[0]
    im=quad(lambda r:term(r).imag,0,a,epsabs=2e-11,epsrel=2e-11,limit=1000,points=[0,a])[0]
    return c0*z/(z+r0)+re+1j*im,r0,c0

rows=[];mx=0.0;min_mu=np.inf
for h in [1.,3.,10.,30.,100.,300.,1000.]:
    a=3*h
    rr=np.linspace(a*1e-8,a*(1-1e-8),1000)
    yy=np.sqrt(rr*(a-rr))
    mu=yy/(np.pi*rr*(1+yy*yy))
    min_mu=min(min_mu,float(mu.min()))
    for wh in [.001,.01,.1,1.,10.,100.,1000.]:
        for eh in [1e-6,.01,.1]:
            z=h*(eh+1j*wh)
            exact=complex(exact_kernel(np.array([z]),h)[0])
            num,r0,c0=diffusive_integral(z,h)
            rel=abs(num-exact)/max(abs(exact),1e-300)
            mx=max(mx,rel)
            rows.append([h,wh,eh,r0,c0,num.real,num.imag,exact.real,exact.imag,rel])

with open(OUT/'diffusive_identity.csv','w',newline='') as f:
    w=csv.writer(f);w.writerow(['Htau','omega_over_H','eps_over_H','atom_rate','atom_weight','integral_real','integral_imag','exact_real','exact_imag','relative_error']);w.writerows(rows)

out={
 'identity':'K_h(z)=c_* z/(z+r_*) + integral_0^(3h) mu_h(r) z/(z+r) dr',
 'mu':'sqrt[r(3h-r)]/[pi r (1+r(3h-r))]',
 'all_measure_samples_positive':bool(min_mu>0),
 'max_relative_error':float(mx),
 'tested_points':len(rows),
 'interpretation':'For fixed H the Hubble-dressed memory kernel is a positive Debye/Stieltjes superposition, so positive finite weights and rates give a passive rational approximation.',
 'gate_status':'PASS' if mx<2e-8 and min_mu>0 else 'CHECK'
}
(OUT/'diffusive_identity_summary.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
