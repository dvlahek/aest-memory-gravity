#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from nl1c6d2n import corrected_class_baseline as base
from nl1c6d2a import baryon_matter_sector_audit as d2a


def find_bg_key(bg, tokens, exact=()):
    return base.find_key(bg,tokens,exact=exact)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--tag',required=True)
    ap.add_argument('--npz-out',required=True)
    ap.add_argument('--json-out',required=True)
    a=ap.parse_args()

    from classy import Class
    pars=base.build_params()
    c=Class(); c.set(pars); c.compute()
    try:
        bg=c.get_background()
        tk,k,z=c.get_transfer_and_k_and_z(output_format='class',h_units=False)
        cl=c.raw_cl(2500)
        db=np.asarray(tk[d2a.pick(tk,'d_b',('delta_b',))],float)
        tb=np.asarray(tk[d2a.pick(tk,'t_b',('theta_b',))],float)
        dm=np.asarray(tk[d2a.pick(tk,'d_m',('delta_m',))],float)
        kh=np.asarray(k,float)/base.h
        zz=np.asarray(z,float)
        phi=np.asarray(tk['phi'],float) if 'phi' in tk else None
        psi=np.asarray(tk['psi'],float) if 'psi' in tk else None

        zkey=find_bg_key(bg,('z',),exact=('z',))
        hkey=find_bg_key(bg,('h [1/mpc]','hubble'),exact=('H [1/Mpc]',))
        rkey=find_bg_key(bg,('rho_cdm','rho aest','rho_aest'))
        if None in (zkey,hkey,rkey):
            raise RuntimeError(f'public background keys missing: z={zkey} H={hkey} rho={rkey}; available={sorted(bg)}')
        bgz=np.asarray(bg[zkey],float)
        bgh=np.asarray(bg[hkey],float)
        bgrho=np.asarray(bg[rkey],float)
    finally:
        c.struct_cleanup(); c.empty()

    save={
      'k_native_h':kh,'z_native':zz,'d_b':db,'t_b':tb,'d_m':dm,
      'ell':np.asarray(cl['ell'],int),'cl_tt':np.asarray(cl['tt'],float),
      'cl_te':np.asarray(cl['te'],float),'cl_ee':np.asarray(cl['ee'],float),
      'bg_z':bgz,'bg_H':bgh,'bg_rho_cdm':bgrho,
    }
    if phi is not None: save['phi']=phi
    if psi is not None: save['psi']=psi
    out=Path(a.npz_out); out.parent.mkdir(parents=True,exist_ok=True)
    np.savez_compressed(out,**save)
    meta={
      'tag':a.tag,'parameters':pars,'transfer_shape':list(db.shape),
      'n_ell':int(np.asarray(cl['ell']).size),'background_samples':int(bgz.size),
      'memory_or_likelihood_evaluated':False,'cosmological_refit_performed':False,
    }
    Path(a.json_out).write_text(json.dumps(meta,indent=2,sort_keys=True)+'\n')
    print(f'EXPORT_TAG={a.tag}')
    print(f'NPZ={out}')
    print(f'JSON={a.json_out}')

if __name__=='__main__':
    raise SystemExit(main())
