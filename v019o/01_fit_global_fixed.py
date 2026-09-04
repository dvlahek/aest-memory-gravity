#!/usr/bin/env python3
from pathlib import Path
import csv,json
import numpy as np
from global_fixed import fit_positive,evaluate,metrics

OUT=Path('results');OUT.mkdir(exist_ok=True)

# Broad domain chosen to include late-time small-Htau behavior and early CMB-era large-Htau behavior.
h_train=np.logspace(-4,8,19)
h_val=np.sqrt(np.logspace(-4,8,20)[:-1]*np.logspace(-4,8,20)[1:])
nu_train=np.logspace(-3,3,37)
nu_val=np.sqrt(np.logspace(-3,3,38)[:-1]*np.logspace(-3,3,38)[1:])
eps_train=[1e-6,1e-4,1e-2,1e-1]
eps_val=[3e-6,3e-4,3e-2]

candidates=[32,48,64,80,96,128]
rows=[];objects={};selected=None
for N in candidates:
    omega,w,train_rel=fit_positive(h_train,nu_train,eps_train,N,wmin=1e-10,wmax=1e10)
    val_rel=evaluate(omega,w,h_val,nu_val,eps_val)
    mt=metrics(train_rel);mv=metrics(val_rel)
    active=w>max(1e-14,1e-10*np.max(w))
    obj={
      'N_grid':N,
      'active_modes':int(np.count_nonzero(active)),
      'sum_weights':float(w.sum()),
      'sum_weight_error':float(abs(w.sum()-1.0)),
      'all_weights_nonnegative':bool(np.all(w>=0)),
      'training':mt,
      'validation':mv,
      'omega':omega.tolist(),
      'weights':w.tolist(),
      'active_mask':active.astype(int).tolist(),
    }
    objects[str(N)]=obj
    rows.append([N,obj['active_modes'],obj['sum_weights'],mt['p95'],mt['p99'],mt['max'],mv['p95'],mv['p99'],mv['max']])
    if selected is None and mv['p95']<1e-3 and mv['p99']<3e-3 and mv['max']<1e-2 and obj['sum_weight_error']<2e-3:
        selected=N

if selected is None:
    selected=min(candidates,key=lambda n:objects[str(n)]['validation']['max'])
    classification='NO_COMPLEX_DOMAIN_CANDIDATE_MET_TARGET'
else:
    classification='COMPLEX_DOMAIN_FIXED_BATH_CANDIDATE_PASS'

sel=objects[str(selected)]
active=np.asarray(sel['active_mask'],bool)
omega=np.asarray(sel['omega'],float)[active]
w=np.asarray(sel['weights'],float)[active]
reduced={
 'selected_grid_N':selected,
 'active_modes':int(len(omega)),
 'omega_tau':omega.tolist(),
 'positive_weights':w.tolist(),
 'sum_active_weights':float(w.sum()),
 'validated_h_range':[1e-4,1e8],
 'validated_nu_over_H_range':[1e-3,1e3],
 'validation_metrics':sel['validation'],
 'classification':classification,
}
(OUT/'v019o_fixed_bath.json').write_text(json.dumps(reduced,indent=2))
(OUT/'v019o_complex_candidates.json').write_text(json.dumps({'candidates':objects,'selected':selected,'classification':classification},indent=2))
with open(OUT/'v019o_complex_candidates.csv','w',newline='') as f:
    wr=csv.writer(f);wr.writerow(['Ngrid','active','sum_weights','train_p95','train_p99','train_max','val_p95','val_p99','val_max']);wr.writerows(rows)

summary={
 'training_h_range':[1e-4,1e8],
 'training_nu_over_H_range':[1e-3,1e3],
 'candidate_grids':candidates,
 'selected_grid_N':selected,
 'selected_active_modes':reduced['active_modes'],
 'selected_validation_metrics':sel['validation'],
 'selected_sum_weight_error':sel['sum_weight_error'],
 'classification':classification,
 'gate_status':'PASS_COMPLEX' if classification.endswith('_PASS') else 'CHECK',
}
(OUT/'v019o_complex_fit_summary.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
