#!/usr/bin/env python3
from pathlib import Path
import csv,json
import numpy as np
from scipy.optimize import nnls
from timevarying import history,smooth_drive,simulate_reference,simulate_fixed_modes,waveform_metrics

OUT=Path('results');OUT.mkdir(exist_ok=True)

# Fixed physical frequencies preserve the original time-dependent-H oscillator form.
# We fit only positive spectral weights in the time domain.
NODES=64
omega=np.logspace(-3,5,NODES)
training_nu=[.1,.3,1.,3.,10.]
validation_nu=[.2,.5,2.,5.,15.]
histories=['lcdm','radiation','matter']

M=[];y=[]
for kind in histories:
    N,h=history(kind,nsteps=1100)
    for nu in training_nu:
        x=smooth_drive(N,nu)
        ref=simulate_reference(N,h,x,Nref=768)
        basis=simulate_fixed_modes(N,h,x,omega)
        sel=np.arange(int(.12*len(N)),len(N),5)
        scale=np.sqrt(np.mean(ref[sel]**2))+1e-14
        M.append(basis[sel]/scale)
        y.append(ref[sel]/scale)
M=np.vstack(M);y=np.concatenate(y)
weights,_=nnls(M,y,maxiter=20000)
active=weights>1e-10

rows=[];validation_l2=[]
for kind in histories:
    N,h=history(kind,nsteps=1300)
    for nu in validation_nu:
        x=smooth_drive(N,nu)
        ref=simulate_reference(N,h,x,Nref=1024)
        pred=simulate_fixed_modes(N,h,x,omega)@weights
        m=waveform_metrics(pred,ref)
        validation_l2.append(m['relative_L2'])
        rows.append([kind,nu,m['relative_L2'],m['cosine'],m['peak_normalized_error']])

with open(OUT/'v019m_fixed_oscillator_validation.csv','w',newline='') as f:
    w=csv.writer(f);w.writerow(['history','omega_over_H','relative_L2','cosine','peak_normalized_error']);w.writerows(rows)
with open(OUT/'v019m_fixed_oscillator_weights.csv','w',newline='') as f:
    w=csv.writer(f);w.writerow(['omega_tau','positive_weight','active']);
    for om,wt,ac in zip(omega,weights,active):w.writerow([om,wt,int(ac)])

p95=float(np.quantile(validation_l2,.95));mx=float(max(validation_l2));med=float(np.median(validation_l2))
classification='PROMISING_FIXED_OSCILLATOR_REDUCTION' if p95<.01 and mx<.02 else 'FIXED_OSCILLATOR_NEEDS_MORE_MODES_OR_OPTIMIZATION'
out={
 'candidate_grid_nodes':NODES,
 'active_positive_modes':int(np.count_nonzero(active)),
 'all_weights_nonnegative':bool(np.all(weights>=0)),
 'sum_weights':float(weights.sum()),
 'validation_metrics':{'median_relative_L2':med,'p95_relative_L2':p95,'max_relative_L2':mx},
 'classification':classification,
 'interpretation':'A fixed-frequency positive oscillator reduction preserves the exact non-autonomous covariant form. It is a fallback candidate if the H-dependent first-order rational realization fails.',
 'gate_status':'PASS_DIAGNOSTIC' if np.all(weights>=0) else 'FAIL'
}
(OUT/'v019m_fixed_oscillator_summary.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
