#!/usr/bin/env python3
from pathlib import Path
import argparse, json, subprocess, sys
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import nl1c7a.a6_a10_spherical_reconstruction as rec


def run(cmd):
    p=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True)
    if p.stdout: print(p.stdout,end='')
    if p.stderr: print(p.stderr,end='',file=sys.stderr)
    return p.returncode


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--trace',required=True); ap.add_argument('--coverage-json',required=True)
    ap.add_argument('--source',required=True); ap.add_argument('--out',required=True); ap.add_argument('--state-npz',required=True)
    a=ap.parse_args()
    cov=json.loads(Path(a.coverage_json).read_text())
    density_ok=(cov.get('classification')=='NL1C7A_NATIVE_TRACE_COVERAGE_PASS' and all(cov.get('gates',{}).values()))
    r2=(cov.get('repair01',{}).get('source_sampling_only') is True and
        cov['repair01'].get('perturbations_sampling_stepsize')==0.025 and
        cov['repair01'].get('perturbations_integration_stepsize_overridden') is False and
        cov['repair01'].get('integration_tolerance_overridden') is False)

    work=Path('results'); work.mkdir(parents=True,exist_ok=True)
    raw_a5=work/'nl1c7a_repair01_a5_raw.json'; raw_rec=work/'nl1c7a_repair01_a6_a10_raw.json'
    a5_rc=run([sys.executable,'nl1c7a/a5_denominator_audit.py','--trace',a.trace,'--coverage-json',a.coverage_json,'--out',str(raw_a5)]) if density_ok else 99
    a5=json.loads(raw_a5.read_text()) if raw_a5.exists() else {'classification':'NOT_RUN','gates':{}}
    a5_ok=(a5_rc==0 and a5.get('classification')=='NL1C7A_A5_FINITE_GROWING_MODE_DENOMINATOR_PASS' and all(a5.get('gates',{}).values()))

    rec_rc=99; rr={'classification':'NOT_RUN','gates':{}}
    if density_ok and a5_ok:
        rec_rc=run([sys.executable,'nl1c7a/a6_a10_spherical_reconstruction.py',
                    '--trace',a.trace,'--coverage-json',a.coverage_json,'--a5-json',str(raw_a5),
                    '--source',a.source,'--out',str(raw_rec)])
        if raw_rec.exists(): rr=json.loads(raw_rec.read_text())

    gates={
      'R1_historical_parent_frozen':True,
      'R2_source_sampling_only_change':bool(r2),
      'R3_denser_exact_native_trace':bool(density_ok),
      'R4_A5_denominator_recheck':bool(a5_ok),
      'R5_A6_time_interpolation_control':bool(rr.get('gates',{}).get('A6_time_interpolation_control',False)),
      'R6_A7_k_interpolation_control':bool(rr.get('gates',{}).get('A7_k_interpolation_control',False)),
      'R6_A8_target_profile_reconstruction':bool(rr.get('gates',{}).get('A8_target_profile_reconstruction',False)),
      'R6_A9_bridge_identities':bool(rr.get('gates',{}).get('A9_bridge_identities',False)),
      'R6_A10_no_free_mode_injection':bool(rr.get('gates',{}).get('A10_no_free_mode_injection',False)),
    }
    if not r2: cls='NL1C7A_REPAIR01_SOURCE_SAMPLING_BOUNDARY_FAIL'
    elif not density_ok: cls='NL1C7A_REPAIR01_NATIVE_DENSITY_FAIL'
    elif not a5_ok: cls='NL1C7A_REPAIR01_TRANSFER_ZERO_FAIL'
    elif not gates['R5_A6_time_interpolation_control']: cls='NL1C7A_REPAIR01_TIME_INTERPOLATION_CONTROL_FAIL'
    elif not gates['R6_A7_k_interpolation_control']: cls='NL1C7A_REPAIR01_K_INTERPOLATION_CONTROL_FAIL'
    elif not gates['R6_A8_target_profile_reconstruction']: cls='NL1C7A_REPAIR01_RECONSTRUCTION_FAIL'
    elif not gates['R6_A9_bridge_identities']: cls='NL1C7A_REPAIR01_BRIDGE_IDENTITY_FAIL'
    elif not gates['R6_A10_no_free_mode_injection']: cls='NL1C7A_REPAIR01_FREE_MODE_INJECTION_FAIL'
    else: cls='NL1C7A_REPAIR01_DENSE_TIME_SPHERICAL_BRIDGE_CERTIFIED'

    state_written=False
    if cls=='NL1C7A_REPAIR01_DENSE_TIME_SPHERICAL_BRIDGE_CERTIFIED':
        z=rec.read_trace(a.trace); ks,gs=rec.groups(z); tv=rec.at_ai(gs,'pchip'); h=float(cov['h'])
        arrays={}
        for s in rec.SCALES:
            st=rec.make_state(s,rec.NQ,ks,h,tv,'pchip')
            tag=str(int(s))
            for k,v in st.items(): arrays[f's{tag}_{k}']=np.asarray(v)
        arrays['a_i']=np.asarray(rec.AI); arrays['scales_hinv_Mpc']=np.asarray(rec.SCALES,float)
        arrays['k_grid_Mpc_inv']=np.asarray(ks,float); arrays['h']=np.asarray(h)
        np.savez_compressed(a.state_npz,**arrays); state_written=True

    result={
      'classification':cls,
      'scope':'NL1C7A Repair01 dense accepted-source-time interface only; eta=0 initial-state bridge. No nonlinear evolution or finite eta.',
      'historical_parent':{'classification':'NL1C7A_TIME_INTERPOLATION_CONTROL_FAIL','run':35106735707,
                           'head':'8b02243fc0b1ea58f00466868d58170c73dbc4e4','artifact':10450343358,
                           'artifact_sha256':'99b795389566a21b0438977af55bae21f92b428d52ad50ba2c9855bafda28fb5',
                           'freeze_commit':'ccf2ac18dd3187f67bafcba4eeeb2b1c0dc524ae'},
      'repair_settings':cov.get('repair01',{}), 'trace_density':{'n_native_times':cov.get('n_native_times'),
          'historical_n_native_times':cov.get('historical_n_native_times'),'window':cov.get('window_0p015_0p03'),
          'requested_k_relative_miss_max':cov.get('requested_k_relative_miss_max')},
      'A5':a5,
      'A6':rr.get('A6'), 'A7':rr.get('A7'), 'A8':rr.get('A8'), 'A9':rr.get('A9'), 'A10':rr.get('A10'),
      'raw_reconstruction_classification':rr.get('classification'),'raw_return_codes':{'A5':a5_rc,'A6_A10':rec_rc},
      'gates':gates,'primary_state_npz_written':state_written,
      'claim_boundary':{'unique_eta0_initial_data_certified':cls=='NL1C7A_REPAIR01_DENSE_TIME_SPHERICAL_BRIDGE_CERTIFIED',
                        'nonlinear_evolution':False,'finite_eta':False,'observable':False},
    }
    out=Path(a.out); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))
    raise SystemExit(0 if cls=='NL1C7A_REPAIR01_DENSE_TIME_SPHERICAL_BRIDGE_CERTIFIED' else 2)

if __name__=='__main__': main()
