#!/usr/bin/env python3
from pathlib import Path
import argparse, importlib.util, json, math

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('r31',ROOT/'v031'/'refit_baseline.py')
r=importlib.util.module_from_spec(spec); spec.loader.exec_module(r)

BASE=dict(r.START)
KB=0.0665
REFERENCE_KB=0.1
REL_GATE=1.0e-6

# Exact v0.42 reported endpoints from run 33987300140.
POINTS={
 'canonical': {'params': {'H0':67.3324639084866,'omega_b':0.022377376877682164,'omega_cdm':0.12006705327635288,'tau_reio':0.06174082364515668,'n_s':0.9666229454895277,'A_s':2.1308864352626987e-9}, 'reported_v042_snr':2.32803921427129},
 'plus': {'params': {'H0':68.83703130087879,'omega_b':0.02277827638394075,'omega_cdm':0.11605838822157599,'tau_reio':0.06266344784638739,'n_s':0.9546014805017466,'A_s':2.199858355344692e-9}, 'reported_v042_snr':0.8590293860134628},
 'minus': {'params': {'H0':65.94510245398088,'omega_b':0.021972930478623334,'omega_cdm':0.1237390404790595,'tau_reio':0.02774677490342517,'n_s':0.9805243179345311,'A_s':1.9280413771034123e-9}, 'reported_v042_snr':4.472092214889027},
 'cross': {'params': {'H0':68.75049551652114,'omega_b':0.021881703341298655,'omega_cdm':0.1238969336867782,'tau_reio':0.05235734062388316,'n_s':0.9849766186713875,'A_s':1.969091576234291e-9}, 'reported_v042_snr':4.259593544697129},
}

def shifted(**kw):
    q=dict(BASE)
    for k,v in kw.items():
        if k=='lnA_s': q['A_s']=BASE['A_s']*math.exp(v)
        else: q[k]=BASE[k]+v
    return q

# Reconstruct exactly the starts assigned to r.START by v042/refit_multistart_continued.py.
# v031/refit_baseline.py builds its KB=0.1 reference from r.START inside main(), so these
# are also the legacy v0.42 reference cosmologies. This is the provenance difference.
LEGACY_REFERENCES={
 'canonical': dict(BASE),
 'plus': shifted(H0=1.5,omega_b=0.0004,omega_cdm=-0.004,tau_reio=0.010,n_s=-0.012,lnA_s=0.05),
 'minus': shifted(H0=-1.5,omega_b=-0.0004,omega_cdm=0.004,tau_reio=-0.010,n_s=0.012,lnA_s=-0.05),
 'cross': shifted(H0=1.0,omega_b=-0.0005,omega_cdm=0.005,tau_reio=0.008,n_s=0.015,lnA_s=-0.04),
}

def load_reference(class_root, tag, params):
    return r.a.load_cl(r.run_class(class_root,tag,'base',REFERENCE_KB,params))

def evaluate(class_root, ref, tag, params):
    m=r.a.load_cl(r.run_class(class_root,tag,'candidate',KB,params))
    snr,_,_,_=r.cv_residual(ref,m)
    return float(snr)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('class_root'); ap.add_argument('--json-out',required=True); z=ap.parse_args()
    class_root=Path(z.class_root).resolve(); (ROOT/'results').mkdir(exist_ok=True); (class_root/'output').mkdir(exist_ok=True)

    locked_ref=load_reference(class_root,'v051_locked_ref',BASE)
    rows=[]
    for name,d in POINTS.items():
        legacy_ref=load_reference(class_root,'v051_legacy_ref_'+name,LEGACY_REFERENCES[name])
        legacy=evaluate(class_root,legacy_ref,'v051_'+name+'_legacy',d['params'])
        locked=evaluate(class_root,locked_ref,'v051_'+name+'_locked',d['params'])
        old=float(d['reported_v042_snr'])
        legacy_rel=abs(legacy-old)/max(abs(old),1e-12)
        locked_rel=abs(locked-old)/max(abs(old),1e-12)
        rows.append({
            'point':name,
            'reported_v042_CV_SNR':old,
            'recomputed_legacy_start_specific_reference_CV_SNR':legacy,
            'legacy_relative_difference':legacy_rel,
            'legacy_reproduced_lt_1e6':legacy_rel<REL_GATE,
            'recomputed_single_locked_reference_CV_SNR':locked,
            'locked_relative_difference_from_v042_reported':locked_rel,
            'endpoint_parameters':d['params'],
            'legacy_reference_parameters':LEGACY_REFERENCES[name],
        })

    legacy_ok=all(x['legacy_reproduced_lt_1e6'] for x in rows)
    canonical_locked_ok=rows[0]['locked_relative_difference_from_v042_reported']<REL_GATE
    noncanonical_locked_mismatch=all(x['locked_relative_difference_from_v042_reported']>=REL_GATE for x in rows[1:])
    provenance_confirmed=legacy_ok and canonical_locked_ok and noncanonical_locked_mismatch
    res={
      'classification':'V051_REFERENCE_PROVENANCE_CONFIRMED' if provenance_confirmed else 'V051_REFERENCE_PROVENANCE_NOT_FULLY_RESOLVED',
      'locked_KB':KB,'reference_KB':REFERENCE_KB,'relative_gate':REL_GATE,'rows':rows,
      'legacy_v042_all_four_reproduced':legacy_ok,
      'canonical_reproduces_under_single_locked_reference':canonical_locked_ok,
      'noncanonical_points_mismatch_under_single_locked_reference':noncanonical_locked_mismatch,
      'provenance_confirmed':provenance_confirmed,
      'root_cause':'v042/refit_multistart_continued.py assigned each multistart cosmology to r.START before calling v031 main(); v031 then constructed the KB=0.1 reference from that mutable START. Thus plus/minus/cross were optimized and reported against different reference cosmologies, while canonical used the registered canonical reference.',
      'scientific_consequence':'The v0.42 cross-start S/N spread is not a valid multistart spread for one common objective. It must not be used as evidence for multiple basins of the locked objective.',
      'scope':'objective/reference provenance audit only; no optimization, no AeST physics changes, no gate relaxation.'
    }
    Path(z.json_out).write_text(json.dumps(res,indent=2)); print(json.dumps(res,indent=2))
    if not provenance_confirmed: raise SystemExit(2)

if __name__=='__main__': main()
