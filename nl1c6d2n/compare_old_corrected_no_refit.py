#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import numpy as np


def rel_l2(a,b):
    a=np.asarray(a,float); b=np.asarray(b,float)
    return float(np.linalg.norm(a-b)/max(np.linalg.norm(b),1e-300))


def grid_err(a,b):
    a=np.asarray(a,float); b=np.asarray(b,float)
    if a.shape != b.shape:
        return float('inf')
    return float(np.max(np.abs(a-b)/np.maximum(np.abs(b),1e-300)))


def bg_compare(c,o,key_c,key_o):
    zc=np.asarray(c['bg_z'],float); zo=np.asarray(o['bg_z'],float)
    vc=np.asarray(c[key_c],float); vo=np.asarray(o[key_o],float)
    oc=np.argsort(zc); oo=np.argsort(zo)
    zc=zc[oc]; vc=vc[oc]; zo=zo[oo]; vo=vo[oo]
    lo=max(0.0,float(zc[0]),float(zo[0])); hi=min(6.0,float(zc[-1]),float(zo[-1]))
    m=(zc>=lo)&(zc<=hi)
    if np.count_nonzero(m)<8:
        raise RuntimeError(f'insufficient common background samples for {key_c}/{key_o}')
    oi=np.interp(zc[m],zo,vo)
    return {
      'relative_L2':rel_l2(vc[m],oi),
      'n_common':int(np.count_nonzero(m)),
      'z_min':float(np.min(zc[m])),'z_max':float(np.max(zc[m])),
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--historical',required=True)
    ap.add_argument('--corrected',required=True)
    ap.add_argument('--json-out',required=True)
    a=ap.parse_args()
    old=np.load(a.historical); cor=np.load(a.corrected)

    grids={
      'k_native_h_relative_max':grid_err(cor['k_native_h'],old['k_native_h']),
      'z_native_relative_max':grid_err(cor['z_native'],old['z_native']),
      'ell_relative_max':grid_err(cor['ell'],old['ell']),
    }
    same_native=all(np.isfinite(v) and v<=1e-12 for v in grids.values())

    fields={}
    for key in ('d_b','t_b','d_m','phi','psi'):
        if key not in old.files or key not in cor.files:
            fields[key]={'present':False}
            continue
        if old[key].shape != cor[key].shape:
            fields[key]={'present':True,'shape_match':False,'old_shape':list(old[key].shape),'corrected_shape':list(cor[key].shape)}
            continue
        fields[key]={'present':True,'shape_match':True,'relative_L2':rel_l2(cor[key],old[key])}

    spectra={}
    for key in ('cl_tt','cl_te','cl_ee'):
        if old[key].shape != cor[key].shape:
            spectra[key]={'shape_match':False,'old_shape':list(old[key].shape),'corrected_shape':list(cor[key].shape)}
        else:
            ell=np.asarray(cor['ell'],int); m=(ell>=2)&(ell<=2500)
            spectra[key]={'shape_match':True,'relative_L2_ell2_2500':rel_l2(cor[key][m],old[key][m])}

    if 'bg_rho_CLASS' in cor.files:
        rho_cor='bg_rho_CLASS'
    elif 'bg_rho_cdm' in cor.files:
        rho_cor='bg_rho_cdm'
    else:
        raise RuntimeError('corrected NPZ lacks background rho')
    background={
      'rho_cdm':bg_compare(cor,old,rho_cor,'bg_rho_cdm'),
      'H':bg_compare(cor,old,'bg_H','bg_H'),
    }

    vals=[v.get('relative_L2') for v in fields.values() if isinstance(v,dict) and 'relative_L2' in v]
    svals=[v.get('relative_L2_ell2_2500') for v in spectra.values() if isinstance(v,dict) and 'relative_L2_ell2_2500' in v]
    summary={
      'label':'NL1C6D2N_OLD_VS_CORRECTED_NO_REFIT_DIAGNOSTIC',
      'historical_npz':str(a.historical),'corrected_npz':str(a.corrected),
      'grids':grids,'native_grid_match_1e-12':bool(same_native),
      'transfer_metric_fields':fields,'spectra':spectra,'background':background,
      'max_transfer_metric_relative_L2':float(max(vals)) if vals else None,
      'max_spectra_relative_L2':float(max(svals)) if svals else None,
      'descriptive_only_no_similarity_pass_fail':True,
      'cosmological_refit_performed':False,
      'memory_or_likelihood_evaluated':False,
      'historical_results_unchanged':True,
    }
    Path(a.json_out).write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
    print('OLD_VS_CORRECTED_NO_REFIT_DIAGNOSTIC')
    print(json.dumps(summary,indent=2,sort_keys=True))
    print(f'JSON={a.json_out}')

if __name__=='__main__':
    raise SystemExit(main())
