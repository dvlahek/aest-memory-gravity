#!/usr/bin/env python3
"""H4F3 physical-parent binary input audit; no H4 operator/Ward/Z21 solve.

Required H3F/H3G JSON and NPZ are checked against the frozen H4F3
predata hashes. An optional frozen Repair32B Z11 NPZ may complete the
binary interface check; a valid interface never proves the full Ward
identity, verifies source dynamics or licenses a Z21 solve.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np

EXPECTED={
    'H3F_JSON':'0616188d2bb7a6c09b2b56433a1f8a1860f360b2e54d2cb84e1ae214a407866b',
    'H3F_NPZ':'90840755fa9febb1d8cb84609d9e58f67dec2a0a01cd6bf8e47685b45caa4542',
    'H3G_JSON':'9b93534e3ee90e1ce588bdbd3f271afd041f738b8dc6f62c4ec0d1413c27f2c4',
    'H3G_NPZ':'9e1bf36e1d81122225ff8c03f663501de7601a8fc9376fd86312e0ae1d809452',
    'Z11_NPZ':'5d4a0a72c08d09d096a8de0b428b3c8443fc33e8ad442ed6d997d6bf2bc6e327',
}
TAGS=('C_min','C_star','C_max')
BETAS=(1.0,0.5,0.1)

def hash_file(path):
    digest=hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda:f.read(2**20),b''):
            digest.update(chunk)
    return digest.hexdigest()

def assert_finite(arr,label):
    if not np.isfinite(arr).all():
        raise ValueError(f'nonfinite stored parent array {label}')

def main():
    parser=argparse.ArgumentParser()
    for label in ('h3f_json','h3f_npz','h3g_json','h3g_npz'):
        parser.add_argument('--'+label.replace('_','-'),type=Path,required=True)
    parser.add_argument('--z11-npz',type=Path)
    parser.add_argument('--json-out',type=Path,required=True)
    args=parser.parse_args()
    files={'H3F_JSON':args.h3f_json,'H3F_NPZ':args.h3f_npz,
           'H3G_JSON':args.h3g_json,'H3G_NPZ':args.h3g_npz}
    if args.z11_npz is not None:
        files['Z11_NPZ']=args.z11_npz
    checks={}
    for key,path in files.items():
        observed=hash_file(path)
        checks[key]={'expected_sha256':EXPECTED[key],
                     'observed_sha256':observed,
                     'bytes':path.stat().st_size,
                     'exact':observed==EXPECTED[key]}
    if not all(item['exact'] for item in checks.values()):
        raise ValueError('actual parent SHA256 does not match H4F3 preregistration')
    h3f=json.loads(args.h3f_json.read_text())
    h3g=json.loads(args.h3g_json.read_text())
    if h3f.get('classification')!='GE19_H3F_CORRECTED_Y_H3_Z20_CERTIFIED' or h3f.get('Z20_certified') is not True:
        raise ValueError('H3F parent is not the certified corrected-Y Z20')
    if h3g.get('classification')!='GE19_H3G_CORRECTED_Y_Q20_RECONSTRUCTION_PASS' or h3g.get('q20_certified_projection') is not True:
        raise ValueError('H3G parent is not the certified corrected-Y q20')
    if not all(h3f.get('gates',{}).values()) or not all(h3g.get('gates',{}).values()):
        raise ValueError('parent science gates are not all true')
    per_case={}
    grids={}
    with np.load(args.h3f_npz,allow_pickle=False) as z20, np.load(args.h3g_npz,allow_pickle=False) as bath:
        for label,nt in (('primary',128),('control',64)):
            a=np.asarray(z20['x_'+label]);b=np.asarray(bath['x_'+label])
            shared=bool(a.shape==(nt,) and np.array_equal(a,b) and np.isfinite(a).all() and np.all(np.diff(a)>0))
            grids[label]={'nt':nt,'exact_shared_x':shared,
                          'max_abs_delta':float(np.max(np.abs(a-b))),
                          'x_start':float(a[0]),'x_end':float(a[-1])}
        for tag in TAGS:
            p=np.asarray(z20[f'{tag}_Z20_primary'])
            p64=np.asarray(z20[f'{tag}_Z20_control'])
            h=np.asarray(z20[f'{tag}_H1_primary'])
            h64=np.asarray(z20[f'{tag}_H1_control'])
            w=np.asarray(bath[f'{tag}_weighted_z20_primary'])
            w64=np.asarray(bath[f'{tag}_weighted_z20_time_control'])
            x=np.asarray(bath[f'{tag}_X20_primary'])
            beta=np.asarray(bath[f'{tag}_B20_linear_primary'])
            defect=beta-(x-w)
            arrs=(p,p64,h,h64,w,w64,x,beta)
            all_finite=bool(all(np.isfinite(v).all() for v in arrs))
            shape_ok=bool(p.shape==(3,40,6,128) and p64.shape==(3,40,6,64)
                 and h.shape==(6,6,128) and h64.shape==(6,6,64)
                 and w.shape==(3,40,128) and w64.shape==(3,40,64)
                 and x.shape==w.shape and beta.shape==w.shape)
            initial_zero=bool(np.array_equal(w[:,:,0],np.zeros((3,40),dtype=w.dtype)))
            identity_exact=bool(np.array_equal(beta,x-w))
            per_case[tag]={'shapes_ok':shape_ok,'all_finite':all_finite,
               'weighted_q20_initial_exact_zero':initial_zero,
               'B20_identity_exact':identity_exact,
               'B20_identity_max_abs_defect':float(np.max(np.abs(defect)))}
        z11_info={'provided':args.z11_npz is not None,'hash_exact':None,
                  'shared_x_primary':None,'shared_x_control':None,'shapes_ok':None}
        if args.z11_npz is not None:
            with np.load(args.z11_npz,allow_pickle=False) as z11:
                status=[]
                for label,nt in (('primary',128),('control',64)):
                    exact=bool(np.array_equal(z11['x_'+label],z20['x_'+label]))
                    z11_info['shared_x_'+label]=exact
                    status.append(exact)
                    for tag in TAGS:
                        fields=np.asarray(z11[f'{tag}_Z11_{label}'])
                        dots=np.asarray(z11[f'{tag}_Z11dot_{label}'])
                        status.extend((fields.shape==(6,6,nt),dots.shape==(6,4,nt),
                                       np.isfinite(fields).all(),np.isfinite(dots).all()))
                z11_info['hash_exact']=True
                z11_info['shapes_ok']=bool(all(status))
    interface_ok=bool(all(g['exact_shared_x'] for g in grids.values())
        and all(v['shapes_ok'] and v['all_finite'] and v['weighted_q20_initial_exact_zero']
                and v['B20_identity_exact'] for v in per_case.values()))
    complete=bool(interface_ok and z11_info['provided'] and z11_info['shapes_ok'])
    report={'classification':('GE19_H4F3A_ALL_THREE_PARENT_BINARY_INTERFACE_PASS_FULL_WARD_OPEN'
         if complete else 'GE19_H4F3A_H3F_H3G_BINARY_INTERFACE_PASS_Z11_REQUIRED'
         if interface_ok else 'GE19_H4F3A_PARENT_BINARY_INTERFACE_FAIL'),
         'frozen_parent_inputs':checks,'shared_time_grid':grids,'cases':per_case,
         'Z11':z11_info,'H3F_H3G_actual_binary_interface_pass':interface_ok,
         'all_three_parent_input_gate_pass':complete,
         'all_six_actual_H4_source_families_assembled':False,
         'full_operator_and_signed_parent_Noether_evaluated':False,
         'H4_Z21_solve_performed':False,'Z21_certified':False,'lensing_licensed':False,
         'claim_boundary':'Exact binary grid, B20 and stored-parent interface only; the all-sector Ward operator/source/parent identity is not evaluated.'}
    args.json_out.parent.mkdir(parents=True,exist_ok=True)
    args.json_out.write_text(json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+'\n')
    print(json.dumps({'classification':report['classification'],
          'all_parent_input_gate':complete,'H3F_H3G_interface':interface_ok,
          'Z11_provided':z11_info['provided'],'B20_identity_exact':{k:v['B20_identity_exact'] for k,v in per_case.items()}},indent=2))
    if not interface_ok or (args.z11_npz is not None and not complete):
        raise SystemExit(3)

if __name__=='__main__':
    main()
