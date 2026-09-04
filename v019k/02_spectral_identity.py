#!/usr/bin/env python3
from pathlib import Path
import json,csv
import numpy as np
import mpmath as mp
from bath_designs import retarded_A,exact_kernel

OUT=Path('results');OUT.mkdir(exist_ok=True)
mp.mp.dps=50

def continuum(A):
    aa=mp.mpc(float(A.real),float(A.imag))
    def f(r):
        return (2/mp.pi)*aa*aa/((r*r+aa*aa)*(1+r*r))
    # Complex A can generate a narrow but finite resonance near r=|Im A|.
    # Explicitly split around it; otherwise generic double-precision quad can
    # report a false 1e-4 integration error even though the identity is exact.
    b=abs(float(A.imag));ar=abs(float(A.real))
    if b>1e-12:
        d=max(.5,5*ar)
        pts=[0,max(0.,b-d),b,b+d,mp.inf]
        clean=[]
        for x in pts:
            if not clean or x>clean[-1]:clean.append(x)
        return complex(mp.quad(f,clean))
    return complex(mp.quad(f,[0,1,mp.inf]))

rows=[];mx=0.
for h in [1.,10.,100.]:
    for wH in [.1,1.,10.,100.]:
        for eH in [1e-3,.03]:
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
 'quadrature':'50-digit mpmath with explicit resonance splitting',
 'gate_status':'PASS' if mx<1e-12 else 'CHECK'
}
(OUT/'spectral_identity_summary.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
