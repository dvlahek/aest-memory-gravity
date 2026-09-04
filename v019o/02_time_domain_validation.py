#!/usr/bin/env python3
from pathlib import Path
import sys,csv,json
import numpy as np

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'v019m'))
from timevarying import history,smooth_drive,gaussian_drive,reference_nodes,simulate_fixed_modes,waveform_metrics

OUT=Path('results');OUT.mkdir(exist_ok=True)
red=json.loads((OUT/'v019o_fixed_bath.json').read_text())
omega=np.asarray(red['omega_tau'],float)
weights=np.asarray(red['positive_weights'],float)


def power_history(kind,hstart,hend,nsteps=1600):
    p=2.0 if kind=='radiation' else 1.5
    L=np.log(hstart/hend)/p
    N=np.linspace(0.0,L,nsteps+1)
    h=hstart*np.exp(-p*N)
    return N,h


def dense_reference(N,h,x,Nref):
    om,w=reference_nodes(Nref,wmin=1e-10,wmax=1e10)
    return simulate_fixed_modes(N,h,x,om)@w


def chirp_drive(N):
    u=(N-N[0])/(N[-1]-N[0])
    ramp=np.ones_like(u);m=u<.08
    ramp[m]=np.sin(.5*np.pi*u[m]/.08)**2
    phase=.15*(N-N[0]) + 2.8*(N-N[0])**2/max(N[-1]-N[0],1e-12)
    return ramp*np.sin(phase)

histories={
 'lcdm':history('lcdm',nsteps=1600,hstart=1e8,hend=1.0),
 'radiation':power_history('radiation',1e8,1e-2,1600),
 'matter':power_history('matter',1e6,1e-4,1600),
}

drives=[]
for nu in [.03,.1,.3,1.,3.,10.,30.]:
    drives.append((f'sine_{nu:g}',lambda N,nu=nu:smooth_drive(N,nu)))
drives += [('gaussian',gaussian_drive),('chirp',chirp_drive)]

rows=[];l2s=[];peaks=[];cosines=[]
for kind,(N,h) in histories.items():
    for name,fn in drives:
        x=fn(N)
        ref=dense_reference(N,h,x,1536)
        pred=simulate_fixed_modes(N,h,x,omega)@weights
        m=waveform_metrics(pred,ref,discard_fraction=.08)
        l2s.append(m['relative_L2']);peaks.append(m['peak_normalized_error']);cosines.append(m['cosine'])
        rows.append([kind,name,h[0],h[-1],m['relative_L2'],m['cosine'],m['peak_normalized_error'],m['reference_rms']])

# Dense-reference convergence on representative difficult histories.
conv=[]
for kind,dname in [('lcdm','sine_3'),('radiation','sine_10'),('matter','chirp')]:
    N,h=histories[kind]
    fn=dict(drives)[dname]
    x=fn(N)
    r768=dense_reference(N,h,x,768)
    r1536=dense_reference(N,h,x,1536)
    m=waveform_metrics(r768,r1536,discard_fraction=.08)
    conv.append([kind,dname,m['relative_L2'],m['peak_normalized_error']])

with open(OUT/'v019o_time_validation.csv','w',newline='') as f:
    w=csv.writer(f);w.writerow(['history','drive','Htau_start','Htau_end','relative_L2','cosine','peak_normalized_error','reference_rms']);w.writerows(rows)
with open(OUT/'v019o_reference_convergence.csv','w',newline='') as f:
    w=csv.writer(f);w.writerow(['history','drive','N768_vs_N1536_relative_L2','peak_normalized_error']);w.writerows(conv)

med=float(np.median(l2s));p95=float(np.quantile(l2s,.95));mx=float(np.max(l2s));peakmax=float(np.max(peaks));mincos=float(np.min(cosines));refmax=max(x[2] for x in conv)
classification='PASS_GLOBAL_FIXED_TIME_DOMAIN' if p95<1e-3 and mx<3e-3 and refmax<3e-4 else 'GLOBAL_FIXED_TIME_DOMAIN_NEEDS_REFINEMENT'
out={
 'selected_active_modes':int(len(omega)),
 'histories':list(histories.keys()),
 'drives':[x[0] for x in drives],
 'validation_cases':len(rows),
 'metrics':{'median_relative_L2':med,'p95_relative_L2':p95,'max_relative_L2':mx,'max_peak_normalized_error':peakmax,'minimum_cosine':mincos},
 'dense_reference_convergence_max_relative_L2':float(refmax),
 'classification':classification,
 'gate_status':'PASS_TIME_DOMAIN' if classification.startswith('PASS') else 'CHECK',
}
(OUT/'v019o_time_validation_summary.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
