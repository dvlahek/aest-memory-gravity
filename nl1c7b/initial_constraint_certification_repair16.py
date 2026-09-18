#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

import nl1c7a.a6_a10_spherical_reconstruction as rec
import nl1c7a.evaluate_identity_preserving_repair08 as r8
import nl1c7b.initial_constraint_certification as b4
import nl1c7b.initial_constraint_certification_repair01 as r1
import nl1c7b.initial_constraint_certification_repair02 as r2
import nl1c7b.initial_constraint_certification_repair09 as r9

R15A_JSON_SHA256='596c7b13c4683840bcf40f6850356e179e77f873c3a3b42ba0b54730ae80811d'
R15A_NPZ_SHA256='997d0033eeed1f3e60c1907c7938a0ea87a1cf38de6ab860340bd003d18d6e6e'
R15A_CLASS='NL1C7B4_REPAIR15A_DENSITY_Q_COMPLETED_STATE_CERTIFIED'
R8_NPZ_SHA256='4639f3b5c0afcddb2f98c8b9f6a9dbbf8661dac685b12d235c09075a106dafa7'
R14A_JSON_SHA256='d60398e2804222df70e8cd3acda5fb397e9cfdd2068415b9256af4d65a5c64ca'
LIMIT=1e-7
DICT_LIMIT=1e-12
ANCHOR_LIMIT=1e-12
GRID_RATIO_LIMIT=2.0
BETAS=(1.0,0.5,0.1)
KINDS=('Simple','Exponential','Sharp')


def sha256_file(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):
            h.update(block)
    return h.hexdigest()


def rel_sym(a,b):
    a=np.asarray(a,float); b=np.asarray(b,float)
    return float(np.linalg.norm(a-b)/max(np.linalg.norm(a),np.linalg.norm(b),1e-300))


def load_primary_state(npz,scale):
    prefix=f's{int(scale)}_'
    out={k[len(prefix):]:np.asarray(npz[k],float) for k in npz.files if k.startswith(prefix)}
    required={
        'x','r','L_minus_a','R_minus_ar','Ldot_minus_aH','Rdot_minus_aHr',
        'u','udot','phi','phidot_minus_Q','delta_b','dust_vr',
        'X_from_chi','X_from_state','E_from_class','E_from_state',
    }
    missing=sorted(required-set(out))
    if missing:
        raise RuntimeError(f'Repair15a NPZ missing fields for scale={scale}: {missing}')
    n=len(out['r'])
    if n!=256 or any(np.asarray(out[k]).shape!=(n,) for k in required):
        raise RuntimeError(f'invalid Repair15a primary state shape for scale={scale}')
    return out


def density_q_correction(scale,r,ks,h,tv_rec,qbg,kqq_bg):
    k=np.geomspace(ks[0],ks[-1],rec.NQ)
    target=rec.dtarg(k,scale,h)
    db=np.asarray(tv_rec['delta_b'],float)
    FE=rec.ik(ks,np.asarray(tv_rec['E_A'],float)/db,k,'pchip')*target
    Fchi=rec.ik(ks,np.asarray(tv_rec['chi'],float)/db,k,'pchip')*target
    combo=b4.KB*FE+b4.C*Fchi
    Fcorr=(k*k/(rec.AI*rec.AI*qbg*kqq_bg))*combo
    return np.asarray(rec.inv(k,Fcorr,np.asarray(r,float)),float)


def reconstructed_corrected_state(scale,nr,ks,h,tv_b4,tv_rec,scalar_ai,qbg,kqq_bg):
    if nr==rec.NQ:
        st=r8.repaired_state(scale,rec.NQ,ks,h,tv_rec,'pchip',scalar_ai)
    else:
        st=r9.repaired_state_nr(scale,nr,ks,h,tv_b4,tv_rec,scalar_ai)
    st={k:np.asarray(v,float).copy() for k,v in st.items()}
    corr=density_q_correction(scale,st['r'],ks,h,tv_rec,qbg,kqq_bg)
    st['phidot_minus_Q']=np.asarray(st['phidot_minus_Q'],float)+corr
    return st


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--trace',required=True)
    ap.add_argument('--coverage-json',required=True)
    ap.add_argument('--repair15a-json',required=True)
    ap.add_argument('--repair15a-npz',required=True)
    ap.add_argument('--out',required=True)
    a=ap.parse_args()

    jsha=sha256_file(a.repair15a_json)
    nsha=sha256_file(a.repair15a_npz)
    parent=json.loads(Path(a.repair15a_json).read_text())
    cov=json.loads(Path(a.coverage_json).read_text())
    off=np.load(a.repair15a_npz)

    z=rec.read_trace(a.trace)
    ks,gs=rec.groups(z)
    tv_rec=rec.at_ai(gs,'pchip')
    ks_b4,gs_b4=b4.groups(b4.read_trace(a.trace))
    tv_b4=b4.at_ai(gs_b4)
    h=float(cov['h'])

    gates15a=parent.get('gates',{})
    gates15=parent.get('inherited_Repair15_gates',{})
    metadata_ok=bool(
        'a_i' in off.files and 'scales_hinv_Mpc' in off.files
        and 'k_grid_Mpc_inv' in off.files and 'h' in off.files
        and 'repair15_density_q_completed' in off.files
        and 'parent_repair08_npz_sha256' in off.files
        and 'parent_repair14a_json_sha256' in off.files
        and abs(float(np.asarray(off['a_i']))-b4.AI)<=1e-15
        and rel_sym(np.asarray(off['scales_hinv_Mpc']),np.asarray(b4.SCALES,float))<=1e-15
        and rel_sym(np.asarray(off['k_grid_Mpc_inv']),np.asarray(ks,float))<=1e-15
        and abs(float(np.asarray(off['h']))-h)<=1e-15
        and bool(np.asarray(off['repair15_density_q_completed']))
        and str(np.asarray(off['parent_repair08_npz_sha256']))==R8_NPZ_SHA256
        and str(np.asarray(off['parent_repair14a_json_sha256']))==R14A_JSON_SHA256
    )
    g1=bool(
        jsha==R15A_JSON_SHA256 and nsha==R15A_NPZ_SHA256
        and parent.get('classification')==R15A_CLASS
        and len(gates15a)==3 and all(gates15a.values())
        and len(gates15)==6 and all(gates15.values())
        and parent.get('output',{}).get('new_state_npz_written') is True
        and parent.get('output',{}).get('written_metadata_pass') is True
        and parent.get('repair15a_accessor_repair',{}).get('B4_residual_used') is False
        and parent.get('repair15a_accessor_repair',{}).get('formula_changed') is False
        and parent.get('repair15a_accessor_repair',{}).get('state_rule_changed') is False
        and parent.get('repair15a_accessor_repair',{}).get('threshold_changed') is False
        and cov.get('classification')=='NL1C7A_NATIVE_TRACE_COVERAGE_PASS'
        and cov.get('requested_k_relative_miss_max')==0
        and cov.get('n_native_times')==179
        and abs(float(cov.get('a_i'))-b4.AI)<=1e-15
        and len(ks)==128 and np.array_equal(ks,ks_b4)
        and metadata_ok
    )

    scalar_ai,scalar_independent,scalar_finite,_=r8.scalar_composites_at_ai(ks,gs,'pchip')
    scalar_identity_error=rel_sym(scalar_ai,scalar_independent)

    kq_bg=float(np.median(tv_b4['KQ']))
    qbg=b4.stable_q_from_kq(kq_bg)
    kqq_bg=float(np.median(tv_rec['KQQ']))
    zbg=r9.stable_zbg(kq_bg)
    g1=bool(g1 and np.isfinite([kq_bg,qbg,kqq_bg,zbg]).all() and kqq_bg!=0)

    states={}
    anchor_rows=[]
    anchor_max=0.0
    anchor_ok=bool(scalar_finite and scalar_identity_error<=1e-10)
    for scale in b4.SCALES:
        primary=load_primary_state(off,scale)
        recon256=reconstructed_corrected_state(scale,256,ks,h,tv_b4,tv_rec,scalar_ai,qbg,kqq_bg)
        for field,value in recon256.items():
            if field not in primary:
                anchor_rows.append({
                    'scale_hinv_Mpc':float(scale),'field':field,
                    'present':False,'pass':False,
                })
                anchor_ok=False
                continue
            err=rel_sym(value,primary[field])
            ok=bool(np.isfinite(err) and err<=ANCHOR_LIMIT)
            anchor_rows.append({
                'scale_hinv_Mpc':float(scale),'field':field,
                'present':True,'relative_L2':err,
                'limit':ANCHOR_LIMIT,'pass':ok,
            })
            anchor_max=max(anchor_max,err)
            anchor_ok &= ok
        states[(scale,256)]=primary
        states[(scale,512)]=reconstructed_corrected_state(
            scale,512,ks,h,tv_b4,tv_rec,scalar_ai,qbg,kqq_bg
        )

    g2=bool(anchor_ok and anchor_max<=ANCHOR_LIMIT)

    funcs,dY,kdict_identity=r1.build_nonK()
    dictionary=[]
    rows=[]
    for scale in b4.SCALES:
        for nr in (256,512):
            drow,crows=r9.evaluate_state(
                states[(scale,nr)],scale,nr,qbg,zbg,funcs,dY
            )
            dictionary.append(drow)
            rows.extend(crows)

    max_qerr=max(x['Q_target_max_normalized_error'] for x in dictionary)
    exp_finite=all(x['Exp_sector_finite'] for x in dictionary)
    g3=bool(
        kdict_identity and exp_finite
        and np.isfinite(max_qerr) and max_qerr<=DICT_LIMIT
    )

    g4=bool(len(rows)==54 and all(x['constraint_pass'] for x in rows))

    grid=[]
    grid_ok=True
    for scale in b4.SCALES:
        for kind in KINDS:
            for beta in BETAS:
                a256=next(x for x in rows if x['scale_hinv_Mpc']==scale and x['Nr']==256 and x['Y_kind']==kind and x['beta0']==beta)
                a512=next(x for x in rows if x['scale_hinv_Mpc']==scale and x['Nr']==512 and x['Y_kind']==kind and x['beta0']==beta)
                qh=r2.ratio2(a256['rms_epsilon_H'],a512['rms_epsilon_H'])
                qm=r2.ratio2(a256['rms_epsilon_M'],a512['rms_epsilon_M'])
                ok=bool(np.isfinite(qh) and np.isfinite(qm) and qh<=GRID_RATIO_LIMIT and qm<=GRID_RATIO_LIMIT)
                grid_ok &= ok
                grid.append({
                    'scale_hinv_Mpc':float(scale),'Y_kind':kind,'beta0':float(beta),
                    'rms_ratio_H':qh,'rms_ratio_M':qm,
                    'limit':GRID_RATIO_LIMIT,'pass':ok,
                })
    g5=bool(len(grid)==27 and grid_ok)

    claim_boundary={
        'primary_256_loaded_directly_from_certified_Repair15a_NPZ':True,
        'state_projection_used':False,
        'B4_residual_used_to_modify_state':False,
        'coefficient_fitted_or_rescaled':False,
        'source_fitted_inserted_or_removed':False,
        'sign_changed':False,
        'K_clipping_used':False,
        'Q_linearized':False,
        'radial_points_removed':False,
        'historical_threshold_changed':False,
        'Y_beta_or_scale_selected':False,
        'nonlinear_evolution_executed':False,
        'finite_eta_executed':False,
        'observational_detection_claimed':False,
    }
    g6=bool(
        claim_boundary['primary_256_loaded_directly_from_certified_Repair15a_NPZ']
        and not any(v for k,v in claim_boundary.items() if k!='primary_256_loaded_directly_from_certified_Repair15a_NPZ')
    )

    gates={
        'R16_G1_exact_Repair15a_provenance':g1,
        'R16_G2_Repair15a_state_anchor_reproduction':g2,
        'R16_G3_exact_nonlinear_dictionary':g3,
        'R16_G4_original_raw_B4_constraints':g4,
        'R16_G5_two_grid_control':g5,
        'R16_G6_claim_boundary':g6,
    }

    if not (g1 and g2 and g3 and g6):
        classification='NL1C7B4_REPAIR16_IMPLEMENTATION_FAIL'; rc=2
    elif not g4:
        classification='NL1C7B4_REPAIR16_REPAIR15A_RAW_CONSTRAINT_FAIL'; rc=2
    elif not g5:
        classification='NL1C7B4_REPAIR16_IMPLEMENTATION_FAIL'; rc=2
    else:
        classification='NL1C7B4_REPAIR16_REPAIR15A_EXACT_NONLINEAR_CONSTRAINT_PASS'; rc=0

    result={
        'classification':classification,
        'scope':'Repair16 exact nonlinear B4 raw eta=0 initial-constraint retest on the certified Repair15a density-Q-completed state; no evolution or finite eta.',
        'provenance':{
            'repair15a_json_sha256_observed':jsha,
            'repair15a_json_sha256_expected':R15A_JSON_SHA256,
            'repair15a_npz_sha256_observed':nsha,
            'repair15a_npz_sha256_expected':R15A_NPZ_SHA256,
            'repair15a_result_freeze_commit':'045c5b28b74ff258dbc775057cf3e9387d47b37c',
            'repair16_prereg_commit':'f39e797ab9c6df71fe4b026f783654eef45e3e2c',
            'dense_trace_artifact':10469031693,
            'dense_trace_sha256':'193325536405f9a21a238f5fbe71a772d2484a096dcbfec3d6007e825cc38f70',
        },
        'state_anchor':{
            'max_relative_L2':anchor_max,
            'limit':ANCHOR_LIMIT,
            'scalar_canonical_vs_independent_at_ai_relative_L2':scalar_identity_error,
            'pass':g2,
            'rows':anchor_rows,
        },
        'background':{
            'Q_bg_Mpc_inv':qbg,
            'KQQ_bg':kqq_bg,
            'Z_bg_stable':zbg,
            'H_Mpc_inv':b4.H_DIRECT,
            'varrho_b':b4.VAR_B,
            'rho_std_C6':b4.RHO_STD,
        },
        'symbolic_K_dictionary_identity':bool(kdict_identity),
        'dictionary_completion':dictionary,
        'constraint_rows':rows,
        'grid_control':grid,
        'gates':gates,
        'summary':{
            'n_constraint_cases':len(rows),
            'n_constraint_pass':int(sum(x['constraint_pass'] for x in rows)),
            'n_grid_pairs':len(grid),
            'max_Q_target_error':float(max_qerr),
            'max_stable_Z_abs':float(max(x['stable_Z_abs_max'] for x in dictionary)),
            'max_epsilon_H':float(max(x['max_epsilon_H'] for x in rows)),
            'max_epsilon_M':float(max(x['max_epsilon_M'] for x in rows)),
            'min_max_epsilon_H':float(min(x['max_epsilon_H'] for x in rows)),
            'min_max_epsilon_M':float(min(x['max_epsilon_M'] for x in rows)),
            'constraint_limit':LIMIT,
            'grid_ratio_limit':GRID_RATIO_LIMIT,
        },
        'claim_boundary':claim_boundary,
        'interpretation_boundary':{
            'exact_nonlinear_eta0_initial_constraints_certified_if_pass':bool(all(gates.values())),
            'nonlinear_evolution_certified':False,
            'finite_eta_certified':False,
            'observational_detection_claimed':False,
        },
    }
    out=Path(a.out)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True,allow_nan=False))
    raise SystemExit(rc)


if __name__=='__main__':
    main()
