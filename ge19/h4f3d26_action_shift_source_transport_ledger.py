#!/usr/bin/env python3
"""D26: exact signed endpoint ledger plus original-action first-interval g' diagnostic.

Diagnostic of three D25R1 locked modes only; immutable D17/D22A and D25R1
archives. No integration, source adjustment, constraint projection or certification.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess
from contextlib import ExitStack
from pathlib import Path
import numpy as np
from scipy.interpolate import PchipInterpolator
from ge19 import h4f3d25r1_first_interval_shift_substep_decision as d25
from ge19 import h4f3d20r1_recompute_five_sources_and_bath_ward as d20
from ge19 import h4f3d17_actual_original_action_dense_canonical_H1 as d17driver
from ge19 import h4f3d17_original_action_dense_H1_core as d17core

ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/'ge19/h4f3d26_action_shift_source_transport_prereg.json'
LOCK=ROOT/'ge19/h4f3d26_action_shift_source_transport_lock.json'
TINY=1e-300
CASES=((14,0.1),(1,1.0),(40,0.1))
EPS_FRACTIONS=(1/16,1/32,1/64)


def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for part in iter(lambda:f.read(1<<20),b''):h.update(part)
    return h.hexdigest()


def pair(c):
    c=complex(c)
    return [float(c.real),float(c.imag)]


def norm(z):
    return float(np.linalg.norm(np.asarray(z,complex)))


def signed_ledger(ky0,ky1,ks0,ks1,y0,y1,s0,s1):
    """Symmetric exact complex product rule for g=ky*y+ks*s-s[6]."""
    terms={
        'action_operator_change_on_state':complex((ky1-ky0)@((y0+y1)/2)),
        'canonical_state_change':complex(((ky0+ky1)/2)@(y1-y0)),
        'action_source_map_change':complex((ks1-ks0)@((s0+s1)/2)),
        'source_evolution_through_action_map':complex(((ks0+ks1)/2)@(s1-s0)),
        'negative_shift_source_change':complex(-(s1[6]-s0[6])),
    }
    total=sum(terms.values())
    return terms,total


def signed_derivative(ky,ks,kyd,ksd,y,yd,s,sd):
    """All original-action operator and source terms; no constraint tuning."""
    terms={
        'operator_explicit_time_on_state':complex(kyd@y),
        'canonical_evolution':complex(ky@yd),
        'operator_explicit_time_on_sources':complex(ksd@s),
        'source_time_derivative_through_action_map':complex(ks@sd),
        'negative_shift_source_time_derivative':complex(-sd[6]),
    }
    return terms,sum(terms.values())


def source_and_derivative(x,src,m,ib):
    """Exactly the frozen original PCHIP representation used by Repair07."""
    beta=(1.0,0.5,0.1)[ib]
    arr=np.concatenate((np.asarray(src[beta]['rhs'][:,:,m],complex),
                        np.asarray(src[beta]['rhs_constraint'][:,:,m],complex)),axis=0)
    re=PchipInterpolator(x,arr.real,axis=1,extrapolate=False)
    im=PchipInterpolator(x,arr.imag,axis=1,extrapolate=False)
    return (lambda t:np.asarray(re(t)+1j*im(t),complex),
            lambda t:np.asarray(re.derivative()(t)+1j*im.derivative()(t),complex))


def operator(r7,mod6,mod7,bg,tag,k,t):
    M,F,ZY,ZR,WY,WR,C,bp,diag=r7._canonical_operator_matrices(mod6,mod7,bg,tag,k,float(t))
    row=C[10]+C[11]
    return np.asarray(row@WY,complex),np.asarray(row@WR,complex),M,F


def one_sided(fun,t,e):
    return (-3*fun(t)+4*fun(t+e)-fun(t+2*e))/(2*e)


def checked_source_files(rd):
    prereg=json.loads(PRE.read_text())
    lock=json.loads(LOCK.read_text())
    if prereg['classification']!='GE19_D26_PREDATA_FROZEN_D25R1_SIGNED_SHIFT_SOURCE_TRANSPORT':
        raise RuntimeError('D26 prereg changed')
    if subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()!='physics-first-gravitational-elasticity':
        raise RuntimeError('D26 wrong branch')
    for rel,want in lock['sha256_local_files'].items():
        if sha(ROOT/rel)!=want:raise RuntimeError('D26 source/predata lock mismatch '+rel)
    d25.verify_r1_code_lock()
    parent=d25.verify(rd,json.loads(d25.MANIFEST.read_text()))
    for key,spec in prereg['frozen_D25R1_outputs'].items():
        f=rd/spec['filename']
        if not f.is_file() or sha(f)!=spec['sha256']:raise RuntimeError('D26 D25R1 output hash mismatch '+key)
        parent[key]=f
    print('GE19_D26_ORIGINAL_ACTION_AND_D25R1_OUTPUT_LOCK_PASS',flush=True)
    return parent,prereg


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--results-dir',required=True)
    ap.add_argument('--json-out',required=True)
    ap.add_argument('--npz-out',required=True)
    a=ap.parse_args();rd=Path(a.results_dir).resolve()
    jp=Path(a.json_out).resolve();npz=Path(a.npz_out).resolve()
    if jp.exists() or npz.exists():raise RuntimeError('D26 no-overwrite outputs')
    parents,prereg=checked_source_files(rd)
    old=d20.source.old;r7=old.r7
    report={
        'classification':'GE19_D26_FROZEN_D25R1_FIRST_INTERVAL_SIGNED_SHIFT_TRANSPORT_DIAGNOSTIC_COMPLETE_PARENTS_UNCERTIFIED',
        'preregistration':prereg['classification'],'source_sha256':sha(Path(__file__)),
        'all_parent_sha256':{key:sha(val) for key,val in parents.items()},
        'scope':'original action, three D25R1 selected modes, original first interval, D25R1 n8 endpoint',
        'action_source_changed':False,'boundary_changed':False,'solver_rerun':False,
        'D22A_science_FAIL_immutable':True,'D25_original_replay_FAIL_immutable':True,
        'D25R1_diagnostic_not_parent_certification':True,
        'Z11_certified':False,'Z20_certified':False,'q20_B20_recomputed':False,
        'full_H4_Ward_certified':False,'Z21_certified':False,'lensing_licensed':False,
        'claim_boundary':'Exact finite signed ledger for frozen n8 endpoints; first-node gdot by original-action operator and PCHIP frozen D22A source. Finite differences of operator are numerical and not a continuum certificate. No source origin attribution or theory inconsistency proved.',
        'per_case':[],
    }
    out={}
    with ExitStack() as es:
        z22=es.enter_context(np.load(parents['D22A_NPZ'],allow_pickle=False))
        z13=es.enter_context(np.load(rd/'ge19_repair13_self_consistent_reduced_background_h1_reclosure.npz',allow_pickle=False))
        dr=es.enter_context(np.load(parents['D25R1_NPZ'],allow_pickle=False))
        dj=json.loads(parents['D25R1_JSON'].read_text())
        if dj['classification']!='GE19_D25R1_FIRST_INTERVAL_SHIFT_SUBSTEP_BETA_ALIGNED_DIAGNOSTIC_COMPLETE_PARENTS_UNCERTIFIED':
            raise RuntimeError('D26 wrong D25R1 classification')
        bgs,_,mod6,mod7,_,_,_,_,_=old.build_context(rd,z13)
        bg=bgs[(128,'C_star')];tag='C_star';x=np.asarray(bg['x'],float)
        if not np.array_equal(x,np.asarray(z22['x_primary'],float)):
            raise RuntimeError('D26 original clock mismatch')
        src=d25.freeze_source(r7,bg,z22)
        orig_bgpoint=r7._bg_point;orig_cache=r7._CANONICAL_LOCAL_CACHE
        r7._CANONICAL_LOCAL_CACHE={};active={'ctx':None}
        def action_bgpoint(b,t):
            if active['ctx'] is None:raise RuntimeError('D26 original action background unavailable')
            return active['ctx'](b,t)
        r7._bg_point=action_bgpoint
        try:
            evalH,_=d17driver.d16r1.d15.clk.make_original_action_background(r7,bg,tag)
            ctx=d17core.ActionBackground(r7,bg,evalH);active['ctx']=ctx;ctx.knot_check()
            t0,t1=float(x[0]),float(x[1]);h=t1-t0
            for m,beta in CASES:
                ib=list(r7.BETAS).index(beta);k=float(m*r7.g9.K_REQ[0]/r7.FOURIER_N[0])
                name=f'm{m}_beta{str(beta).replace(".","p")}'
                y0=np.asarray(dr[f'{name}_y0'],complex)
                y8=np.asarray(dr[f'{name}_n8_y1'],complex)
                srcf,srcd=source_and_derivative(x,src,m,ib)
                s0,s1,sd0=srcf(t0),srcf(t1),srcd(t0)
                ky0,ks0,M0,F0=operator(r7,mod6,mod7,bg,tag,k,t0)
                ky1,ks1,_,_=operator(r7,mod6,mod7,bg,tag,k,t1)
                g0=complex(ky0@y0+ks0@s0-s0[6]);g1=complex(ky1@y8+ks1@s1-s1[6])
                rows=[q for q in dj['per_case'] if int(q['mode'])==m and float(q['beta'])==beta]
                if len(rows)!=1:raise RuntimeError('D26 D25R1 case ambiguous')
                oldrow=rows[0]
                gref=complex(*oldrow['substep_results'][-1]['shift']['complex_defect'])
                if abs(g1-gref)>1e-10*max(abs(ky1@y8),abs(ks1@s1),abs(s1[6]),1e-30):
                    raise RuntimeError(f'D26 n8 signed endpoint does not replay D25R1 m={m}')
                i0=complex(*oldrow['initial_shift']['complex_defect'])
                if abs(g0-i0)>1e-10*max(abs(ky0@y0),abs(ks0@s0),abs(s0[6]),1e-30):
                    raise RuntimeError(f'D26 original projected initial shift mismatch m={m}')
                terms,total=signed_ledger(ky0,ky1,ks0,ks1,y0,y8,s0,s1)
                ledger_error=abs(total-(g1-g0))/max(sum(abs(v) for v in terms.values()),abs(g1-g0),TINY)
                if ledger_error>1e-11:raise RuntimeError('D26 signed ledger identity FAIL')
                ydot=M0@y0+F0@s0
                deriv=[]
                for fraction in EPS_FRACTIONS:
                    e=h*fraction
                    def coeff(t):
                        ky,ks,*_=operator(r7,mod6,mod7,bg,tag,k,t)
                        return np.r_[ky,ks]
                    cd=one_sided(coeff,t0,e)
                    dt,gt=signed_derivative(ky0,ks0,cd[:8],cd[8:],y0,ydot,s0,sd0)
                    def glin(t):
                        ky,ks,*_=operator(r7,mod6,mod7,bg,tag,k,t)
                        return complex(ky@(y0+(t-t0)*ydot)+ks@srcf(t)-srcf(t)[6])
                    gd_ind=one_sided(glin,t0,e)
                    den=max(sum(abs(v) for v in dt.values()),abs(gt),abs(gd_ind),TINY)
                    deriv.append({'epsilon':e,'epsilon_over_h':fraction,
                                  'terms':{a:pair(v) for a,v in dt.items()},
                                  'gdot_signed':pair(gt),'gdot_independent_linearized':pair(gd_ind),
                                  'decomposition_relative':float(abs(gt-gd_ind)/den)})
                lhs0=complex(ky0@y0+ks0@s0);lhs1=complex(ky1@y8+ks1@s1)
                lhs_delta=lhs1-lhs0;source_delta=s1[6]-s0[6]
                case={
                    'mode':m,'beta':beta,'initial_shift':pair(g0),'n8_shift':pair(g1),
                    'initial_source_shift':pair(s0[6]),'n8_source_shift':pair(s1[6]),
                    'signed_source_shift_change':pair(source_delta),
                    'signed_canonical_lhs_change':pair(lhs_delta),
                    'canonical_lhs_change_over_source_shift_change_magnitude':float(abs(lhs_delta)/max(abs(source_delta),TINY)),
                    'signed_endpoint_terms':{a:pair(v) for a,v in terms.items()},
                    'signed_endpoint_ledger_total':pair(total),'signed_ledger_identity_relative':float(ledger_error),
                    'first_node_source_shift_time_derivative_pchip':pair(sd0[6]),
                    'first_node_derivative':deriv,
                    'derivative_refinement_relative_report_only':float(abs(complex(*deriv[1]['gdot_signed'])-complex(*deriv[2]['gdot_signed']))/
                          max(abs(complex(*deriv[1]['gdot_signed'])),abs(complex(*deriv[2]['gdot_signed'])),TINY)),
                }
                report['per_case'].append(case)
                out[f'{name}_signed_endpoint_terms']=np.asarray(list(terms.values()),complex)
                cd32=one_sided(coeff,t0,h/32)
                out[f'{name}_gdot_terms_h32']=np.asarray(list(signed_derivative(ky0,ks0,cd32[:8],cd32[8:],y0,ydot,s0,sd0)[0].values()),complex)
                print(f'GE19_D26_FIRST_INTERVAL m={m} beta={beta} '
                      f'shift={abs(g1):.6e} source_delta={abs(source_delta):.6e} '
                      f'lhs_delta={abs(lhs_delta):.6e} signed_ledger={ledger_error:.3e}',flush=True)
        finally:
            r7._bg_point=orig_bgpoint;r7._CANONICAL_LOCAL_CACHE=orig_cache
    if len(report['per_case'])!=3 or not all(np.isfinite(v).all() for v in out.values()):
        raise RuntimeError('D26 incomplete/nonfinite')
    jp.parent.mkdir(parents=True,exist_ok=True)
    np.savez_compressed(npz,**out)
    jp.write_text(json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+'\n')
    print('GE19_D26_CLASSIFICATION '+report['classification'],flush=True)

if __name__=='__main__':main()
