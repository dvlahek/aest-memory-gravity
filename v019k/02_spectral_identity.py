#!/usr/bin/env python3
from pathlib import Path
import json,csv
import numpy as np
from scipy.integrate import quad
from bath_designs import retarded_A,exact_kernel

OUT=Path('results');OUT.mkdir(exist_ok=True)

def continuum(A):
    def f(r):
        return (2/np.pi)*A*A/((r*r+A*A)*(1+r*r))
    re=quad(lambda r:f(r).real,0,np.inf,epsabs=2e-11,epsrel=2e-11,limit=1000)[0]
    im=quad(lambda r:f(r).imag,0,np.inf,epsabs=2e-11,epsrel=2e-11,limit=1000)[0]
    return re+1j*im

rows=[];mx=0.
for h in [1.,3.,10.,100.]:
    for wH in [.03,.1,.3,1.,3.,10.,30.,100.]:
        for eH in [1e-3,.03,.1]:
            z=h*(eH+1j*wH)
            A=retarded_A(z,h)
            ex=exact_kernel(A)
            num=continuum(A)
            rel=float(abs(num-ex)/max(abs(ex),1e-300));mx=max(mx,rel)
            rows.append([h,wH,eH,A.real,A.imag,num.real,num.imag,ex.real,ex.imag,rel])

with open(OUT/'spectral_identity.csv','w',newline='') as f:
    w=csv.writer(f);w.writerow(['Htau','omega_over_H','eps_over_H','A_real','A_imag','integral_real','integral_imag','exact_real','exact_imag','relative_error']);w.writerows(rows)

out={
 'identity':'A/(1+A)=(2/pi) integral_0^inf A^2/[(r^2+A^2)(1+r^2)] dr',
 'complex_points':len(rows),'max_relative_error':mx,
 'positive_measure':'(2/pi)/(1+r^2) dr',
 'gate_status':'PASS' if mx<1e-8 else 'CHECK'
}
(OUT/'spectral_identity_summary.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
