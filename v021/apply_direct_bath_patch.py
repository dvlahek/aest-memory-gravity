#!/usr/bin/env python3
from pathlib import Path
import argparse, json
import numpy as np
from scipy.special import roots_legendre

ORDERS=(256,512)

def c_array(name,vals):
    return 'static const double '+name+'['+str(len(vals))+'] = {\n  '+',\n  '.join(f'{float(x):.17g}' for x in vals)+'\n};\n'

def nodes(n):
    z,w=roots_legendre(int(n))
    theta=0.25*np.pi*(z+1.0)
    return np.tan(theta),0.5*w

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('class_root'); args=ap.parse_args()
    root=Path(args.class_root).resolve(); repo=Path(__file__).resolve().parents[1]
    src=root/'source'/'aest_memory.c'; s=src.read_text()
    marker='/* AeST v0.19j positive finite-bath design accessors */'
    if marker not in s: raise RuntimeError('v0.19j accessor marker not found')
    prefix=s.split(marker,1)[0]
    block='/* AeST v0.21 direct positive tan-theta Drude quadrature */\n'
    data={}
    for n in ORDERS:
        om,wt=nodes(n); data[n]=(om,wt)
        block += c_array(f'_aest_v021_omega{n}',om)
        block += c_array(f'_aest_v021_weight{n}',wt)
    block += r'''
int aest_memory_active_count(int order) {
  if (order == 256) return 256;
  if (order == 512) return 512;
  return 0;
}

double aest_memory_node_order(int order,int j) {
  if (order == 256) return (j>=0 && j<256) ? _aest_v021_omega256[j] : -1.;
  if (order == 512) return (j>=0 && j<512) ? _aest_v021_omega512[j] : -1.;
  return -1.;
}

double aest_memory_weight_order(int order,int j) {
  if (order == 256) return (j>=0 && j<256) ? _aest_v021_weight256[j] : -1.;
  if (order == 512) return (j>=0 && j<512) ? _aest_v021_weight512[j] : -1.;
  return -1.;
}
'''
    src.write_text(prefix+block)

    ip=root/'source'/'input.c'; t=ip.read_text()
    old='''  class_test((pba->aest_memory_order != 16) && (pba->aest_memory_order != 20),errmsg,
             "aest_memory_order must be 16 or 20");
'''
    new='''  class_test((pba->aest_memory_order != 256) && (pba->aest_memory_order != 512),errmsg,
             "v0.21 aest_memory_order must be 256 or 512");
'''
    if old not in t: raise RuntimeError('v0.19j order parser anchor not found')
    ip.write_text(t.replace(old,new,1))

    checks={}
    for n,(om,wt) in data.items():
        checks[f'order{n}_count']=len(om)==len(wt)==n
        checks[f'order{n}_positive']=bool(np.min(om)>0 and np.min(wt)>0)
        checks[f'order{n}_sum']=bool(abs(float(np.sum(wt))-1.0)<1e-12)
    checks['tau_guard_absent']='validated only for aest_tau_H0 = 1' not in ip.read_text()
    checks['closure_preserved']='E_rhs_aest -= 0.5*Q_aest*Bchi_aest' in (root/'source'/'perturbations.c').read_text()
    report={'classification':'V021_DIRECT_POSITIVE_DRUDE_QUADRATURE','orders':list(ORDERS),
            'construction':'Gauss-Legendre in theta with omega*tau=tan(theta), positive weights=0.5*w',
            'tau_scaling':'omega_j = r_j H0/(tau H0) in existing CLASS bath equations',
            'checks':checks}
    if not all(checks.values()): raise RuntimeError(report)
    (repo/'results').mkdir(exist_ok=True)
    (repo/'results'/'v021_direct_bath_patch.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))

if __name__=='__main__': main()
