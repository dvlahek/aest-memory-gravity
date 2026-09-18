#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

import numpy as np

import nl1c7a.a6_a10_spherical_reconstruction as rec
import nl1c7a.evaluate_identity_preserving_repair08 as r8
import nl1c7b.initial_constraint_certification as b4
import nl1c7b.initial_constraint_certification_repair01 as r1
import nl1c7b.initial_constraint_certification_repair09 as r9
import nl1c7b.initial_constraint_certification_repair10 as r10
import nl1c7b.initial_constraint_certification_repair16 as r16

R16_JSON_SHA256='a225f435ef61eaf33a1b4466eea678b23d1a221a537589bd8e2b0717ed66335b'
R16_CLASS='NL1C7B4_REPAIR16_REPAIR15A_RAW_CONSTRAINT_FAIL'
R15A_JSON_SHA256='596c7b13c4683840bcf40f6850356e179e77f873c3a3b42ba0b54730ae80811d'
R15A_NPZ_SHA256='997d0033eeed1f3e60c1907c7938a0ea87a1cf38de6ab860340bd003d18d6e6e'
R15A_CLASS='NL1C7B4_REPAIR15A_DENSITY_Q_COMPLETED_STATE_CERTIFIED'
REPRO_LIMIT=1e-12
CLOSURE_LIMIT=1e-12
BETAS=(1.0,0.5,0.1)
KINDS=('Simple','Exponential','Sharp')


def sha256_file(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):
            h.update(block)
    return h.hexdigest()


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--trace',required=True)
    ap.add_argument('--coverage-json',required=True)
    ap.add_argument('--repair15a-json',required=True)
    ap.add_argument('--repair15a-npz',required=True)
    ap.add_argument('--repair16-json',required=True)
    ap.add_argument('--out',required=True)
    a=ap.parse_args()

    cov=json.loads(Path(a.coverage_json).read_text())
    p15=json.loads(Path(a.repair15a_json).read_text())
    p16=json.loads(Path(a.repair16_json).read_text())
    off=np.load(a.repair15a_npz)

    h15j=sha256_file(a.repair15a_json)
    h15n=sha256_file(a.repair15a_npz)
    h16=sha256_file(a.repair16_json)

    z=rec.read_trace(a.trace)
    ks,gs=rec.groups(z)
    tv_rec=rec.at_ai(gs,'pchip')
    ks_b4,gs_b4=b4.groups(b4.read_trace(a.trace))
    tv_b4=b4.at_ai(gs_b4)
    h=float(cov['h'])

    g16=p16.get('gates',{})
    g15=p15.get('gates',{})
    g15inner=p15.get('inherited_Repair15_gates',{})
    g1=bool(
        h16==R16_JSON_SHA256
        and p16.get('classification')==R16_CLASS
        and g16.get('R16_G1_exact_Repair15a_provenance') is True
        and g16.get('R16_G2_Repair15a_state_anchor_reproduction') is True
        and g16.get('R16_G3_exact_nonlinear_dictionary') is True
        and g16.get('R16_G4_original_raw_B4_constraints') is False
        and g16.get('R16_G5_two_grid_control') is True
        and g16.get('R16_G6_claim_boundary') is True
        and h15j==R15A_JSON_SHA256
        and h15n==R15A_NPZ_SHA256
        and p15.get('classification')==R15A_CLASS
        and len(g15)==3 and all(g15.values())
        and len(g15inner)==6 and all(g15inner.values())
        and cov.get('classification')=='NL1C7A_NATIVE_TRACE_COVERAGE_PASS'
        and cov.get('requested_k_relative_miss_max')==0
        and cov.get('n_native_times')==179
        and len(ks)==128 and np.array_equal(ks,ks_b4)
    )

    scalar_ai,scalar_independent,scalar_finite,_=r8.scalar_composites_at_ai(ks,gs,'pchip')
    scalar_identity=r16.rel_sym(scalar_ai,scalar_independent)
    kq_bg=float(np.median(tv_b4['KQ']))
    qbg=b4.stable_q_from_kq(kq_bg)
    kqq_bg=float(np.median(tv_rec['KQQ']))
    zbg=r9.stable_zbg(kq_bg)
    funcs,dY,kidentity=r1.build_nonK()
    g1=bool(g1 and scalar_finite and scalar_identity<=1e-10 and kidentity)

    states={}
    for scale in b4.SCALES:
        states[(scale,256)]=r16.load_primary_state(off,scale)
        states[(scale,512)]=r16.reconstructed_corrected_state(
            scale,512,ks,h,tv_b4,tv_rec,scalar_ai,qbg,kqq_bg
        )

    rows=[]
    closure_h=0.0
    closure_m=0.0
    for scale in b4.SCALES:
        for nr in (256,512):
            rr,ch,cm=r10.evaluate_localized(
                states[(scale,nr)],scale,nr,qbg,zbg,funcs,dY
            )
            rows.extend(rr)
            closure_h=max(closure_h,ch)
            closure_m=max(closure_m,cm)

    frozen={r10.key(x):x for x in p16['constraint_rows']}
    repro=[]
    repro_ok=bool(len(rows)==54 and len(frozen)==54)
    for row in rows:
        k=r10.key(row)
        fr=frozen.get(k)
        if fr is None:
            repro_ok=False
            repro.append({'key':list(k),'present_in_Repair16':False,'pass':False})
            continue
        ph,ah,rh=r10.scalar_match(row['max_epsilon_H'],fr['max_epsilon_H'],REPRO_LIMIT)
        pm,am,rm=r10.scalar_match(row['max_epsilon_M'],fr['max_epsilon_M'],REPRO_LIMIT)
        ok=bool(ph and pm)
        repro_ok &= ok
        repro.append({
            'key':list(k),
            'present_in_Repair16':True,
            'epsilon_H_abs_error':ah,
            'epsilon_H_relative_error':rh,
            'epsilon_M_abs_error':am,
            'epsilon_M_relative_error':rm,
            'limit':REPRO_LIMIT,
            'pass':ok,
        })
    g2=bool(repro_ok)

    g3=bool(
        np.isfinite(closure_h) and np.isfinite(closure_m)
        and closure_h<=CLOSURE_LIMIT and closure_m<=CLOSURE_LIMIT
    )

    source_names=[
        'GR_kin','GR_curv_NL','GR_curv_Rr','GR_Nr_boundary',
        'AeST_E2','AeST_EX','AeST_X2','AeST_J','AeST_K','dust','standard_bg',
    ]
    complete=True
    for row in rows:
        for spot in ('H_hotspot','M_hotspot'):
            s=row[spot]
            complete &= bool(
                isinstance(s.get('index'),int)
                and np.isfinite(s.get('r_Mpc'))
                and np.isfinite(s.get('epsilon'))
                and np.isfinite(s.get('numerator_signed'))
                and np.isfinite(s.get('denominator_abs_sum'))
                and set(s.get('signed_sources',{}))==set(source_names)
                and all(np.isfinite(v) for v in s['signed_sources'].values())
            )
    g4=bool(len(rows)==54 and complete)

    pair_rows=[]
    for scale in b4.SCALES:
        for kind in KINDS:
            for beta in BETAS:
                a256=next(x for x in rows if r10.key(x)==(float(scale),256,kind,float(beta)))
                a512=next(x for x in rows if r10.key(x)==(float(scale),512,kind,float(beta)))
                pair_rows.append({
                    'scale_hinv_Mpc':float(scale),
                    'Y_kind':kind,
                    'beta0':float(beta),
                    'H':{
                        'r256_Mpc':a256['H_hotspot']['r_Mpc'],
                        'r512_Mpc':a512['H_hotspot']['r_Mpc'],
                        'dominant_256':a256['H_hotspot']['dominant_label'],
                        'dominant_512':a512['H_hotspot']['dominant_label'],
                        'second_256':a256['H_hotspot']['second_label'],
                        'second_512':a512['H_hotspot']['second_label'],
                        'dominant_label_agrees':a256['H_hotspot']['dominant_label']==a512['H_hotspot']['dominant_label'],
                    },
                    'M':{
                        'r256_Mpc':a256['M_hotspot']['r_Mpc'],
                        'r512_Mpc':a512['M_hotspot']['r_Mpc'],
                        'dominant_256':a256['M_hotspot']['dominant_label'],
                        'dominant_512':a512['M_hotspot']['dominant_label'],
                        'second_256':a256['M_hotspot']['second_label'],
                        'second_512':a512['M_hotspot']['second_label'],
                        'dominant_label_agrees':a256['M_hotspot']['dominant_label']==a512['M_hotspot']['dominant_label'],
                    },
                })
    g5=bool(len(pair_rows)==27)

    claim_boundary={
        'state_modified_or_projected':False,
        'B4_residual_used_to_modify_state':False,
        'coefficient_fitted_or_rescaled':False,
        'source_fitted_inserted_or_removed':False,
        'sign_changed':False,
        'K_clipping_used':False,
        'Q_linearized':False,
        'radial_points_removed':False,
        'Y_beta_or_scale_selected':False,
        'historical_threshold_changed':False,
        'nonlinear_evolution_executed':False,
        'finite_eta_executed':False,
        'observational_detection_claimed':False,
        'B4_pass_relabel_claimed':False,
    }
    g6=bool(not any(claim_boundary.values()))

    gates={
        'R17_G1_frozen_provenance':g1,
        'R17_G2_exact_Repair16_reproduction':g2,
        'R17_G3_signed_decomposition_closure':g3,
        'R17_G4_complete_hotspot_localization':g4,
        'R17_G5_complete_two_grid_localization_report':g5,
        'R17_G6_claim_boundary':g6,
    }

    if all(gates.values()):
        classification='NL1C7B4_REPAIR17_REPAIR16_SOURCE_LOCALIZATION_PASS'; rc=0
    else:
        classification='NL1C7B4_REPAIR17_IMPLEMENTATION_FAIL'; rc=2

    hdom=Counter(x['H_hotspot']['dominant_label'] for x in rows)
    mdom=Counter(x['M_hotspot']['dominant_label'] for x in rows)
    hsecond=Counter(x['H_hotspot']['second_label'] for x in rows)
    msecond=Counter(x['M_hotspot']['second_label'] for x in rows)

    result={
        'classification':classification,
        'scope':'Repair17 exact signed source localization of frozen Repair16 raw eta=0 residual on certified Repair15a state; diagnostic only.',
        'provenance':{
            'repair16_json_sha256':h16,
            'repair16_result_freeze_commit':'af47a7c33c0f09744b98828e0727279b1c3d6475',
            'repair15a_json_sha256':h15j,
            'repair15a_npz_sha256':h15n,
            'repair17_prereg_commit':'ef7e23770590ab70691feb701e33a4a6624e7ad8',
        },
        'state_anchor_context':{
            'scalar_canonical_vs_independent_at_ai_relative_L2':scalar_identity,
            'Repair16_primary_anchor_max_relative_L2':p16['state_anchor']['max_relative_L2'],
        },
        'source_labels':source_names,
        'repair16_reproduction':{
            'limit':REPRO_LIMIT,
            'rows':repro,
            'pass':g2,
        },
        'decomposition_closure':{
            'max_H':closure_h,
            'max_M':closure_m,
            'limit':CLOSURE_LIMIT,
            'pass':g3,
        },
        'localization_rows':rows,
        'two_grid_localization':pair_rows,
        'summary':{
            'n_cases':len(rows),
            'H_dominant_label_counts':dict(sorted(hdom.items())),
            'M_dominant_label_counts':dict(sorted(mdom.items())),
            'H_second_label_counts':dict(sorted(hsecond.items())),
            'M_second_label_counts':dict(sorted(msecond.items())),
            'max_epsilon_H':float(max(x['max_epsilon_H'] for x in rows)),
            'max_epsilon_M':float(max(x['max_epsilon_M'] for x in rows)),
            'min_epsilon_H':float(min(x['max_epsilon_H'] for x in rows)),
            'min_epsilon_M':float(min(x['max_epsilon_M'] for x in rows)),
        },
        'gates':gates,
        'claim_boundary':claim_boundary,
        'interpretation_boundary':{
            'dominant_source_coefficient_declared_wrong':False,
            'Repair16_relabelled':False,
            'state_repair_performed':False,
        },
    }

    out=Path(a.out)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True,allow_nan=False))
    raise SystemExit(rc)


if __name__=='__main__':
    main()
