#!/usr/bin/env python3
from pathlib import Path
import csv,json
import numpy as np
from timevarying import (load_rational_table,history,smooth_drive,gaussian_drive,
                         simulate_reference,simulate_rational,waveform_metrics)

OUT=Path('results');OUT.mkdir(exist_ok=True)
anchors,qnodes,W=load_rational_table()

# Dense-reference convergence on representative histories.
conv=[]
for kind,nu in [('lcdm',1.0),('radiation',3.0),('matter',10.0)]:
    N,h=history(kind,nsteps=1400)
    x=smooth_drive(N,nu)
    r512=simulate_reference(N,h,x,Nref=512)
    r1024=simulate_reference(N,h,x,Nref=1024)
    m=waveform_metrics(r512,r1024)
    conv.append([kind,nu,m['relative_L2'],m['cosine'],m['peak_normalized_error']])

rows=[];l2_relevant=[];all_l2=[]
for kind in ['lcdm','radiation','matter']:
    N,h=history(kind,nsteps=1800)
    drives=[('sin_0p1',smooth_drive(N,.1),.1),
            ('sin_0p3',smooth_drive(N,.3),.3),
            ('sin_1',smooth_drive(N,1.),1.),
            ('sin_3',smooth_drive(N,3.),3.),
            ('sin_10',smooth_drive(N,10.),10.),
            ('gaussian',gaussian_drive(N),None)]
    for name,x,nu in drives:
        ref=simulate_reference(N,h,x,Nref=1024)
        rat=simulate_rational(N,h,x,anchors,qnodes,W)
        m=waveform_metrics(rat,ref)
        all_l2.append(m['relative_L2'])
        if nu is not None and nu>=1.0:
            l2_relevant.append(m['relative_L2'])
        rows.append([kind,name,'' if nu is None else nu,m['relative_L2'],m['cosine'],m['peak_normalized_error'],m['reference_rms']])

with open(OUT/'v019m_nonautonomous.csv','w',newline='') as f:
    w=csv.writer(f);w.writerow(['history','drive','omega_over_H','relative_L2','cosine','peak_normalized_error','reference_rms']);w.writerows(rows)
with open(OUT/'v019m_reference_convergence.csv','w',newline='') as f:
    w=csv.writer(f);w.writerow(['history','omega_over_H','N512_vs_N1024_L2','cosine','peak_normalized_error']);w.writerows(conv)

max_conv=max(r[2] for r in conv)
med_rel=float(np.median(l2_relevant));p95_rel=float(np.quantile(l2_relevant,.95));mx_rel=float(max(l2_relevant))
classification='PASS_NONAUTONOMOUS' if p95_rel<.01 and mx_rel<.02 else 'FAIL_INSTANTANEOUS_COEFFICIENT_REALIZATION'
out={
 'reference_convergence_max_relative_L2':float(max_conv),
 'nu_ge_1_metrics':{'median_relative_L2':med_rel,'p95_relative_L2':p95_rel,'max_relative_L2':mx_rel},
 'all_history_max_relative_L2':float(max(all_l2)),
 'classification':classification,
 'interpretation':('The instantaneous H-dependent rates/weights reproduce the conservative time-dependent bath to the target level.' if classification.startswith('PASS') else 'Sub-permille frozen-H transfer accuracy does not survive naive H(t) substitution: the missing effect is non-autonomous history/transport, not frozen-frequency fitting error.'),
 'gate_status':'PASS' if classification.startswith('PASS') and max_conv<5e-4 else 'CHECK'
}
(OUT/'v019m_nonautonomous_summary.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
