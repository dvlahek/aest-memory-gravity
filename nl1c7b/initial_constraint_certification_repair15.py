#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

import nl1c7a.a6_a10_spherical_reconstruction as rec
import nl1c7b.initial_constraint_certification as b4
import nl1c7b.initial_constraint_certification_repair09 as r9

R8_JSON_SHA256='054851decab71e79a05aca2bc9fb287bb1239c8fb425989f40920004c3d88453'
R8_NPZ_SHA256='4639f3b5c0afcddb2f98c8b9f6a9dbbf8661dac685b12d235c09075a106dafa7'
R14A_JSON_SHA256='d60398e2804222df70e8cd3acda5fb397e9cfdd2068415b9256af4d65a5c64ca'
R8_CLASS='NL1C7A_REPAIR08_IDENTITY_PRESERVING_SCALAR_REPRESENTATION_CERTIFIED'
R14A_CLASS='NL1C7B4_REPAIR14A_DENSITY_Q_BRIDGE_OMISSION_IDENTIFIED'
IDENTITY_LIMIT=1e-12
REGRESSION_LIMIT=1e-12
META_LIMIT=1e-15


def sha256_file(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):
            h.update(block)
    return h.hexdigest()


def rel_sym(a,b):
    a=np.asarray(a,float); b=np.asarray(b,float)
    return float(np.linalg.norm(a-b)/max(np.linalg.norm(a),np.linalg.norm(b),1e-300))


def state_arrays_for_scale(off,scale):
    prefix=f's{int(scale)}_'
    out={k[len(prefix):]:np.asarray(off[k]) for k in off.files if k.startswith(prefix)}
    required={
        'x','r','L_minus_a','R_minus_ar','Ldot_minus_aH','Rdot_minus_aHr',
        'u','udot','phi','phidot_minus_Q','delta_b','dust_vr',
        'X_from_chi','X_from_state','E_from_class','E_from_state',
    }
    missing=sorted(required-set(out))
    if missing:
        raise RuntimeError(f'Repair08 NPZ missing fields for scale={scale}: {missing}')
    return out


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--trace',required=True)
    ap.add_argument('--coverage-json',required=True)
    ap.add_argument('--repair08-json',required=True)
    ap.add_argument('--repair08-npz',required=True)
    ap.add_argument('--repair14a-json',required=True)
    ap.add_argument('--out',required=True)
    ap.add_argument('--state-npz',required=True)
    a=ap.parse_args()

    out_path=Path(a.out)
    state_path=Path(a.state_npz)
    out_path.parent.mkdir(parents=True,exist_ok=True)
    state_path.parent.mkdir(parents=True,exist_ok=True)
    if state_path.exists():
        state_path.unlink()

    hashes={
        'repair08_json_sha256':sha256_file(a.repair08_json),
        'repair08_npz_sha256':sha256_file(a.repair08_npz),
        'repair14a_json_sha256':sha256_file(a.repair14a_json),
    }
    r8j=json.loads(Path(a.repair08_json).read_text())
    r14aj=json.loads(Path(a.repair14a_json).read_text())
    cov=json.loads(Path(a.coverage_json).read_text())
    off=np.load(a.repair08_npz)

    z=rec.read_trace(a.trace)
    ks,gs=rec.groups(z)
    tv=rec.at_ai(gs,'pchip')
    h=float(cov['h'])

    metadata_parent_ok=bool(
        'a_i' in off.files and 'scales_hinv_Mpc' in off.files
        and 'k_grid_Mpc_inv' in off.files and 'h' in off.files
        and abs(float(np.asarray(off['a_i']))-rec.AI)<=META_LIMIT
        and rel_sym(np.asarray(off['scales_hinv_Mpc']),np.asarray(rec.SCALES,float))<=META_LIMIT
        and rel_sym(np.asarray(off['k_grid_Mpc_inv']),np.asarray(ks,float))<=META_LIMIT
        and abs(float(np.asarray(off['h']))-h)<=META_LIMIT
    )
    g1=bool(
        hashes['repair08_json_sha256']==R8_JSON_SHA256
        and hashes['repair08_npz_sha256']==R8_NPZ_SHA256
        and hashes['repair14a_json_sha256']==R14A_JSON_SHA256
        and r8j.get('classification')==R8_CLASS
        and len(r8j.get('gates',{}))==10 and all(r8j.get('gates',{}).values())
        and r8j.get('new_state_npz_written') is True
        and r14aj.get('classification')==R14A_CLASS
        and len(r14aj.get('gates',{}))==4 and all(r14aj.get('gates',{}).values())
        and len(r14aj.get('inherited_Repair14_gates',{}))==8
        and all(r14aj.get('inherited_Repair14_gates',{}).values())
        and r14aj.get('repair14a_parser_repair',{}).get('science_payload_exactly_reproduced_vs_attempt01') is True
        and cov.get('classification')=='NL1C7A_NATIVE_TRACE_COVERAGE_PASS'
        and cov.get('requested_k_relative_miss_max')==0
        and cov.get('n_native_times')==179
        and len(ks)==128 and np.all(np.diff(ks)>0)
        and metadata_parent_ok
    )

    kq_bg=float(np.median(tv['KQ']))
    qbg=b4.stable_q_from_kq(kq_bg)
    kqq_bg=float(np.median(tv['KQQ']))
    rhoA=float(np.median(tv['rhoA']))
    finite_bg=bool(np.isfinite([qbg,kqq_bg,rhoA]).all() and qbg!=0 and kqq_bg!=0)
    g1=bool(g1 and finite_bg)

    new_states={}
    transfer_rows=[]
    real_rows=[]
    regression_rows=[]
    change_rows=[]
    g2=g3=g4=True

    for scale in rec.SCALES:
        base=state_arrays_for_scale(off,scale)
        r=np.asarray(base['r'],float)
        k=np.geomspace(ks[0],ks[-1],rec.NQ)
        target=rec.dtarg(k,scale,h)
        db=np.asarray(tv['delta_b'],float)

        FE=rec.ik(ks,np.asarray(tv['E_A'],float)/db,k,'pchip')*target
        Fchi=rec.ik(ks,np.asarray(tv['chi'],float)/db,k,'pchip')*target
        FdA=rec.ik(ks,np.asarray(tv['delta_A'],float)/db,k,'pchip')*target

        combo=b4.KB*FE+b4.C*Fchi
        Fcorr=(k*k/(rec.AI*rec.AI*qbg*kqq_bg))*combo
        lhs=qbg*kqq_bg*Fcorr
        rhs=(k*k/(rec.AI*rec.AI))*combo
        terr=rel_sym(lhs,rhs)
        tfinite=bool(np.all(np.isfinite(Fcorr)) and np.all(np.isfinite(lhs)) and np.all(np.isfinite(rhs)))
        tpass=bool(tfinite and terr<=IDENTITY_LIMIT)
        g2 &= tpass
        transfer_rows.append({
            'scale_hinv_Mpc':float(scale),
            'quadrature_n':int(rec.NQ),
            'relative_L2':terr,
            'limit':IDENTITY_LIMIT,
            'pass':tpass,
        })

        corr=rec.inv(k,Fcorr,r)
        full_dq=np.asarray(base['phidot_minus_Q'],float)+corr

        FdensityE=-(k*k/(rec.AI*rec.AI))*combo
        Frho=rhoA*FdA
        densityE=rec.inv(k,FdensityE,r)
        rho_delta=rec.inv(k,Frho,r)
        residual=qbg*kqq_bg*full_dq+densityE-rho_delta
        rerr=float(np.linalg.norm(residual)/max(
            np.linalg.norm(qbg*kqq_bg*full_dq),
            np.linalg.norm(densityE),
            np.linalg.norm(rho_delta),
            1e-300
        ))
        rfinite=bool(
            np.all(np.isfinite(corr)) and np.all(np.isfinite(full_dq))
            and np.all(np.isfinite(densityE)) and np.all(np.isfinite(rho_delta))
            and np.all(np.isfinite(residual))
        )
        rpass=bool(rfinite and rerr<=IDENTITY_LIMIT)
        g3 &= rpass
        real_rows.append({
            'scale_hinv_Mpc':float(scale),
            'relative_L2':rerr,
            'limit':IDENTITY_LIMIT,
            'correction_L2':float(np.linalg.norm(corr)),
            'correction_Linf':float(np.max(np.abs(corr))),
            'pass':rpass,
        })

        st={k0:np.array(v,copy=True) for k0,v in base.items()}
        st['phidot_minus_Q']=np.asarray(full_dq,float)
        new_states[scale]=st

        for field,val in st.items():
            if field=='phidot_minus_Q':
                old=np.asarray(base[field],float)
                change_rows.append({
                    'scale_hinv_Mpc':float(scale),
                    'field':field,
                    'relative_L2_vs_Repair08':rel_sym(np.asarray(val,float),old),
                    'absolute_change_L2':float(np.linalg.norm(np.asarray(val,float)-old)),
                    'absolute_change_Linf':float(np.max(np.abs(np.asarray(val,float)-old))),
                    'gated_toward_parent':False,
                })
                continue
            err=rel_sym(np.asarray(val,float),np.asarray(base[field],float))
            passed=bool(np.isfinite(err) and err<=REGRESSION_LIMIT)
            g4 &= passed
            regression_rows.append({
                'scale_hinv_Mpc':float(scale),
                'field':field,
                'relative_L2':err,
                'limit':REGRESSION_LIMIT,
                'pass':passed,
            })

    output_integrity=bool(
        len(new_states)==3
        and all(len(np.asarray(new_states[s]['r']))==256 for s in rec.SCALES)
        and all(np.all(np.isfinite(np.asarray(v,float))) for s in rec.SCALES for v in new_states[s].values())
    )

    claim_boundary={
        'historical_Repair08_NPZ_overwritten':False,
        'only_phidot_minus_Q_changed':True,
        'constraint_projection_used':False,
        'B4_residual_used_to_construct_correction':False,
        'physical_coefficient_changed':False,
        'coefficient_fitted':False,
        'source_changed':False,
        'sign_changed':False,
        'clipping_used':False,
        'radial_points_removed':False,
        'scale_Y_beta_selected':False,
        'historical_threshold_changed':False,
        'nonlinear_evolution_executed':False,
        'finite_eta_executed':False,
        'B4_pass_claimed':False,
        'observational_detection_claimed':False,
    }
    g6=bool(
        not claim_boundary['historical_Repair08_NPZ_overwritten']
        and claim_boundary['only_phidot_minus_Q_changed']
        and not claim_boundary['constraint_projection_used']
        and not claim_boundary['B4_residual_used_to_construct_correction']
        and not claim_boundary['physical_coefficient_changed']
        and not claim_boundary['coefficient_fitted']
        and not claim_boundary['source_changed']
        and not claim_boundary['sign_changed']
        and not claim_boundary['clipping_used']
        and not claim_boundary['radial_points_removed']
        and not claim_boundary['scale_Y_beta_selected']
        and not claim_boundary['historical_threshold_changed']
        and not claim_boundary['nonlinear_evolution_executed']
        and not claim_boundary['finite_eta_executed']
        and not claim_boundary['B4_pass_claimed']
    )

    # Metadata is written only after the scientific/state gates are known.
    g5=bool(output_integrity)

    gates={
        'R15_G1_frozen_Repair08_and_Repair14a_provenance':g1,
        'R15_G2_exact_Fourier_density_Q_completion_identity':bool(g2),
        'R15_G3_real_space_density_Q_identity':bool(g3),
        'R15_G4_unchanged_Repair08_state_field_regression':bool(g4),
        'R15_G5_metadata_output_integrity':bool(g5),
        'R15_G6_claim_boundary':g6,
    }

    certified=bool(all(gates.values()))
    cls='NL1C7B4_REPAIR15_DENSITY_Q_COMPLETED_STATE_CERTIFIED' if certified else 'NL1C7B4_REPAIR15_IMPLEMENTATION_FAIL'

    if certified:
        arrays={}
        for scale in rec.SCALES:
            tag=str(int(scale))
            for key,val in new_states[scale].items():
                arrays[f's{tag}_{key}']=np.asarray(val)
        arrays['a_i']=np.asarray(rec.AI)
        arrays['scales_hinv_Mpc']=np.asarray(rec.SCALES,float)
        arrays['k_grid_Mpc_inv']=np.asarray(ks,float)
        arrays['h']=np.asarray(h)
        arrays['repair15_density_q_completed']=np.asarray(True)
        arrays['parent_repair08_npz_sha256']=np.asarray(R8_NPZ_SHA256)
        arrays['parent_repair14a_json_sha256']=np.asarray(R14A_JSON_SHA256)
        np.savez_compressed(state_path,**arrays)

    # Check written metadata without changing scientific semantics.
    written_meta_ok=False
    if certified and state_path.is_file():
        chk=np.load(state_path)
        written_meta_ok=bool(
            'repair15_density_q_completed' in chk.files
            and bool(np.asarray(chk['repair15_density_q_completed']))
            and str(np.asarray(chk['parent_repair08_npz_sha256']))==R8_NPZ_SHA256
            and str(np.asarray(chk['parent_repair14a_json_sha256']))==R14A_JSON_SHA256
            and abs(float(np.asarray(chk['a_i']))-rec.AI)<=META_LIMIT
            and rel_sym(np.asarray(chk['scales_hinv_Mpc']),np.asarray(rec.SCALES,float))<=META_LIMIT
            and rel_sym(np.asarray(chk['k_grid_Mpc_inv']),np.asarray(ks,float))<=META_LIMIT
            and abs(float(np.asarray(chk['h']))-h)<=META_LIMIT
        )
    if certified and not written_meta_ok:
        state_path.unlink(missing_ok=True)
        gates['R15_G5_metadata_output_integrity']=False
        certified=False
        cls='NL1C7B4_REPAIR15_IMPLEMENTATION_FAIL'

    result={
        'classification':cls,
        'scope':'Repair15 eta=0 density-Q-completed state representation only; no B4 certification, evolution, finite eta, or observable claim.',
        'provenance':{
            **hashes,
            'repair08_result_freeze_commit':'6a8812f9b8d9f4fa373212376b6c01b4649076aa',
            'repair14a_result_freeze_commit':'be1ad5287a22feb81e9fceef0483eefb17b1a800',
            'repair15_prereg_commit':'fad9c5136d04de1618d3b94ef47a483529ba4d78',
        },
        'background':{
            'a_i':rec.AI,
            'Q_background_Mpc_inv':qbg,
            'KQQ_background':kqq_bg,
            'QKQQ_background':qbg*kqq_bg,
            'rhoA_background':rhoA,
            'K_B':b4.KB,
            'C_2_minus_KB':b4.C,
        },
        'canonical_relation':{
            'deltaQ_current':'rho_A*delta_A/(Q*K_QQ)',
            'deltaQ_correction':'k^2/(a^2*Q*K_QQ)*(K_B*E_A+(2-K_B)*chi)',
            'deltaQ_full':'deltaQ_current+deltaQ_correction',
        },
        'transfer_identity_rows':transfer_rows,
        'real_space_identity_rows':real_rows,
        'unchanged_state_regression':{
            'rows':regression_rows,
            'max_relative_L2':max((x['relative_L2'] for x in regression_rows),default=0.0),
            'limit':REGRESSION_LIMIT,
            'pass':bool(g4),
        },
        'phidot_minus_Q_changes':change_rows,
        'output':{
            'new_state_npz_written':bool(certified and state_path.is_file()),
            'new_state_npz_path':str(state_path),
            'written_metadata_pass':bool(written_meta_ok),
        },
        'summary':{
            'n_scales':3,
            'max_transfer_identity_relative_L2':max(x['relative_L2'] for x in transfer_rows),
            'max_real_space_identity_relative_L2':max(x['relative_L2'] for x in real_rows),
            'max_unchanged_state_relative_L2':max((x['relative_L2'] for x in regression_rows),default=0.0),
            'max_correction_Linf':max(x['correction_Linf'] for x in real_rows),
        },
        'gates':gates,
        'claim_boundary':claim_boundary,
        'continuation':'Only a CERTIFIED Repair15 NPZ may be consumed by a separately preregistered exact nonlinear B4 retest under the original 1e-7 raw-constraint limit.',
    }

    out_path.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True,allow_nan=False))
    raise SystemExit(0 if certified else 2)


if __name__=='__main__':
    main()
