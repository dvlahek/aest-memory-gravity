#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import v063.theory_response_map as v63

CLASS_SHA='e85808324f51fc694d12e3ed7439552a3c3f9540'
K_H=np.asarray([0.03,0.05,0.08,0.10,0.15,0.20],float)
H=float(v63.START['H0'])/100.0
K_REQ=K_H*H


def pick(d,key,alts=()):
    if key in d: return key
    for a in alts:
        if a in d: return a
    raise RuntimeError(f'missing {key}; available={sorted(d.keys())}')


def rel_l2(a,b):
    a=np.asarray(a,float); b=np.asarray(b,float)
    return float(np.linalg.norm(a-b)/max(np.linalg.norm(b),1e-300))


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--v077-npz',required=True)
    ap.add_argument('--json-out',required=True)
    ap.add_argument('--npz-out',required=True)
    args=ap.parse_args()
    from classy import Class

    pars=dict(v63.class_params())
    pars['output']='mPk,mTk'
    pars['lensing']='no'
    pars['k_output_values']=', '.join(f'{k:.17g}' for k in K_REQ)
    pars['P_k_max_h/Mpc']=2.0
    pars['z_max_pk']=5.0
    pars['k_per_decade_for_pk']=80.0
    pars['k_per_decade_for_bao']=560.0

    c=Class(); c.set(pars); c.compute()
    try:
        tk,k,z=c.get_transfer_and_k_and_z(output_format='class',h_units=False)
        kb=pick(tk,'d_b',('delta_b',))
        km=pick(tk,'d_m',('delta_m',))
        db=np.asarray(tk[kb],float); dm=np.asarray(tk[km],float)
        k=np.asarray(k,float); z=np.asarray(z,float)
        if db.shape!=(k.size,z.size) or dm.shape!=(k.size,z.size):
            raise RuntimeError(f'unexpected transfer orientation db={db.shape} dm={dm.shape} k={k.size} z={z.size}')
        context_keys=[x for x in sorted(tk.keys()) if ('ncdm' in x.lower() or 'nu' in x.lower()) and np.asarray(tk[x]).shape==dm.shape]
        context={x:np.asarray(tk[x],float) for x in context_keys}
    finally:
        c.struct_cleanup(); c.empty()

    old=np.load(args.v077_npz)
    old_k=np.asarray(old['k_native_h'],float)
    old_z=np.asarray(old['z_native'],float)
    old_dm=np.asarray(old['d_m_base'],float)
    kh=k/H
    if dm.shape!=old_dm.shape:
        raise RuntimeError(f'fresh/preserved d_m shape mismatch {dm.shape} != {old_dm.shape}')
    krel=float(np.max(np.abs(kh-old_k)/np.maximum(np.abs(old_k),1e-300)))
    zabs=float(np.max(np.abs(z-old_z)))
    dmrel=rel_l2(dm,old_dm)

    req=[]; reqmax=0.0
    for target in K_H:
        j=int(np.argmin(np.abs(kh-target)))
        miss=abs(kh[j]-target)/target
        reqmax=max(reqmax,miss)
        req.append({'requested_k_h_per_Mpc':float(target),'index':j,
                    'actual_k_h_per_Mpc':float(kh[j]),'relative_miss':float(miss)})

    finite_db=bool(np.all(np.isfinite(db))); finite_dm=bool(np.all(np.isfinite(dm)))
    nwin=int(np.count_nonzero((z>=0.2)&(z<=1.5)))
    gates={
        'd_b_exists_and_finite':finite_db,
        'd_m_exists_and_finite':finite_dm,
        'k_grid_match_le_1e-12':krel<=1e-12,
        'z_grid_match_le_1e-12':zabs<=1e-12,
        'd_m_identity_relL2_le_1e-10':dmrel<=1e-10,
        'requested_k_match_le_1e-12':reqmax<=1e-12,
        'minimum_8_native_times':nwin>=8,
    }
    passed=bool(all(gates.values()))
    classification='NL1C5B_BARYON_SOURCE_FREEZE_PASS' if passed else 'NL1C5B_BARYON_SOURCE_FREEZE_FAIL'

    result={
        'classification':classification,
        'scope':'fresh theory-only native CLASS baryon-source extraction from the frozen v0.77 model; no memory forcing, finite eta, observational data or likelihood',
        'CLASS_commit':CLASS_SHA,
        'transfer_keys':sorted(tk.keys()),
        'baryon_key':kb,'total_matter_key':km,'massive_neutrino_context_keys':context_keys,
        'grid':{'n_k':int(k.size),'n_z':int(z.size),'native_times_0p2_to_1p5':nwin,
                'k_relative_mismatch_vs_v077':krel,'z_absolute_mismatch_vs_v077':zabs,
                'requested_k_relative_miss_max':reqmax,'requested_k':req},
        'historical_identity':{'fresh_d_m_vs_v077_relative_L2':dmrel},
        'baryon_state':{'all_finite':finite_db,
                        'abs_min':float(np.min(np.abs(db))),
                        'abs_max':float(np.max(np.abs(db)))},
        'gates':gates,'historical_results_unchanged':True,
        'interpretation':'PASS freezes the native baryon transfer d_b on exactly the same native grid as the certified v0.77 total-matter state. This d_b block is the primary rho_b source for the next published full-J quasistatic AeST reclosure.'
    }
    Path(args.json_out).parent.mkdir(parents=True,exist_ok=True)
    Path(args.json_out).write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    save={'k_native_h':kh,'z_native':z,'d_b':db,'d_m':dm}
    for key,val in context.items():
        save['context_'+key.replace(' ','_').replace('/','_')]=val
    np.savez_compressed(args.npz_out,**save)
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__': main()
