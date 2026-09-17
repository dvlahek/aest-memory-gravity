#!/usr/bin/env python3
from pathlib import Path
import argparse, json, math, sys
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import v063.theory_response_map as v63

AI=0.02
ZI=49.0
C_KM_S=299792.458
PARENT_RUN=35195633648
PARENT_HEAD='43573a7c1eaf9090b0890297edcadde017bdb9bb'
PARENT_ARTIFACT=10484764897
PARENT_SHA='d6b80e99cb456314e130f5e7e65c15b4f608ac9fc8a8395263404045e9fa67e4'
PARENT_FREEZE='4fb8679f84585c4008008d7043ac0b5f4ca33eeb'
PINNED_CLASS='e85808324f51fc694d12e3ed7439552a3c3f9540'
BARYON_LIMIT=1e-10
CLOSURE_LIMIT=1e-7


def rel(a,b,scale=None):
    if scale is None:
        scale=max(abs(a),abs(b),1e-300)
    return abs(a-b)/max(scale,1e-300)


def source_semantics(class_root):
    root=Path(class_root)
    pyx=(root/'python'/'classy.pyx').read_text()
    bg=(root/'source'/'background.c').read_text()
    inp=(root/'source'/'input.c').read_text()
    checks={
      'direct_Hubble_method':'def Hubble(self, z)' in pyx and 'background_at_z' in pyx,
      'direct_Om_b_method':'def Om_b(self, z)' in pyx,
      'direct_Om_cdm_method':'def Om_cdm(self, z)' in pyx,
      'direct_Om_ncdm_method':'def Om_ncdm(self, z)' in pyx,
      'photon_source_identity':'Omega0_g * pow(pba->H0,2) / pow(a,4)' in bg,
      'ur_source_identity':'Omega0_ur * pow(pba->H0,2) / pow(a,4)' in bg,
      'lambda_source_identity':'Omega0_lambda * pow(pba->H0,2)' in bg,
      'N_ur_input_identity':'param1*7./8.*pow(4./11.,4./3.)*pba->Omega0_g' in inp,
      'rho_tot_is_aggregate':'index_bg_rho_tot' in bg and 'rho_tot' in bg,
    }
    return {'checks':checks,'pass':all(checks.values())}


def pchip_rho_tot_diagnostic(bg):
    if '(.)rho_tot' not in bg:
        return None
    from scipy.interpolate import PchipInterpolator
    z=np.asarray(bg['z'],float)
    a=1.0/(1.0+z)
    y=np.asarray(bg['(.)rho_tot'],float)
    order=np.argsort(a)
    return float(PchipInterpolator(np.log(a[order]),y[order])(math.log(AI)))


def direct_background(class_root):
    sys.path.insert(0,str(Path(class_root)/'python'))
    from classy import Class
    pars=dict(v63.class_params())
    pars['output']='mTk'
    pars['aest_memory_enabled']='no'
    pars['aest_eta']=0.0
    c=Class(); c.set(pars); c.compute()
    try:
        H=float(c.Hubble(ZI))
        H0=float(c.Hubble(0.0))
        Om_b=float(c.Om_b(ZI))
        Om_cdm=float(c.Om_cdm(ZI))
        Om_ncdm=float(c.Om_ncdm(ZI))
        Omega_g=float(c.Omega_g)
        Omega_lambda=float(c.Omega_Lambda)
        N_ur=float(pars['N_ur'])
        Omega_ur=N_ur*(7.0/8.0)*(4.0/11.0)**(4.0/3.0)*Omega_g

        rho_b=Om_b*H*H
        rho_cdm=Om_cdm*H*H
        rho_ncdm=Om_ncdm*H*H
        rho_g=Omega_g*H0*H0/AI**4
        rho_ur=Omega_ur*H0*H0/AI**4
        rho_lambda=Omega_lambda*H0*H0
        rho_std=rho_g+rho_ur+rho_ncdm+rho_lambda
        bg=c.get_background()
        rho_tot_diag=pchip_rho_tot_diagnostic(bg)
        return {
          'H':H,'H0':H0,'Om_b':Om_b,'Om_cdm':Om_cdm,'Om_ncdm':Om_ncdm,
          'Omega_g':Omega_g,'Omega_ur':Omega_ur,'Omega_lambda':Omega_lambda,
          'rho_b':rho_b,'rho_cdm':rho_cdm,'rho_ncdm':rho_ncdm,'rho_g':rho_g,
          'rho_ur':rho_ur,'rho_lambda':rho_lambda,'rho_std':rho_std,
          'rho_tot_exported_pchip_diagnostic':rho_tot_diag,
          'background_columns':sorted(bg.keys()),
        }
    finally:
        c.struct_cleanup(); c.empty()


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--class-root',required=True)
    ap.add_argument('--historical-json',required=True)
    ap.add_argument('--out',required=True)
    a=ap.parse_args()

    hist=json.loads(Path(a.historical_json).read_text())
    provenance=(hist.get('classification')=='NL1C7B3_STANDARD_BACKGROUND_IDENTIFICATION_FAIL' and
                abs(float(hist['closure']['fixed_parent_rho_rem_Mpc_inv2'])-0.00010529789814922824)<=1e-18)
    sem=source_semantics(a.class_root)
    d=direct_background(a.class_root)

    finite_nonnegative=all(math.isfinite(d[k]) and d[k]>=0.0 for k in
                           ['H','H0','rho_b','rho_cdm','rho_ncdm','rho_g','rho_ur','rho_lambda','rho_std'])

    varrho_b_direct=3.0*d['rho_b']
    varrho_b_frozen=3.0*(100.0/C_KM_S)**2*float(v63.START['omega_b'])*AI**-3
    baryon_rel=rel(varrho_b_direct,varrho_b_frozen)

    rhoA_C6=3.0*d['rho_cdm']
    rho_std_C6=3.0*d['rho_std']
    lhs=3.0*d['H']**2
    eps=abs(lhs-rhoA_C6-varrho_b_direct-rho_std_C6)/max(lhs,1e-300)
    class_sum=d['rho_b']+d['rho_cdm']+d['rho_std']
    class_sum_eps=abs(d['H']**2-class_sum)/max(d['H']**2,1e-300)

    pm=hist.get('parent_reproduction',{})
    hist_components=hist.get('components',{})
    hist_closure=hist.get('closure',{})
    historical_diag={
      'historical_fixed_B2_remainder':float(hist_closure.get('fixed_parent_rho_rem_Mpc_inv2',float('nan'))),
      'historical_B3_rho_std_C6':float(hist_components.get('rho_std_C6',float('nan'))),
      'direct_minus_historical_rho_std_C6':float(rho_std_C6-float(hist_components.get('rho_std_C6',0.0))),
      'historical_epsilon_full':float(hist_closure.get('epsilon_full',float('nan'))),
      'historical_parent_reproduction':pm,
      'historical_fail_retained':True,
      'no_remainder_fit':True,
    }

    gates={
      'R1_provenance':bool(provenance),
      'R2_direct_API_and_source_semantics':bool(sem['pass']),
      'R3_common_point_component_consistency':bool(finite_nonnegative and baryon_rel<=BARYON_LIMIT),
      'R4_direct_homogeneous_closure':bool(eps<=CLOSURE_LIMIT),
      'R5_independent_CLASS_sum_closure':bool(class_sum_eps<=CLOSURE_LIMIT),
    }
    cls='NL1C7B3_REPAIR01_DIRECT_BACKGROUND_POINT_PASS' if all(gates.values()) else 'NL1C7B3_REPAIR01_DIRECT_BACKGROUND_POINT_FAIL'

    result={
      'classification':cls,
      'scope':'Common direct background-point reconciliation at a_i=0.02 only; no radial constraint or trajectory.',
      'historical_parent':{'run':PARENT_RUN,'head':PARENT_HEAD,'artifact':PARENT_ARTIFACT,
                           'artifact_sha256':PARENT_SHA,'result_freeze':PARENT_FREEZE,
                           'classification':'NL1C7B3_STANDARD_BACKGROUND_IDENTIFICATION_FAIL'},
      'provenance':{'pinned_CLASS':PINNED_CLASS,'parameter_source':'v063/theory_response_map.py::class_params',
                    'a_i':AI,'z_i':ZI},
      'source_semantics':sem,
      'direct':d,
      'components_C6':{'rhoA_C6_direct':float(rhoA_C6),'varrho_b_direct':float(varrho_b_direct),
                       'varrho_b_frozen':float(varrho_b_frozen),'baryon_relative_error':float(baryon_rel),
                       'rho_std_C6_direct':float(rho_std_C6),'three_H2':float(lhs)},
      'closure':{'epsilon_direct':float(eps),'class_density_sum_relative_error':float(class_sum_eps),
                 'limit':CLOSURE_LIMIT},
      'standard_sector_fractions':{
        'photons':float(d['rho_g']/d['rho_std']),
        'ur':float(d['rho_ur']/d['rho_std']),
        'ncdm':float(d['rho_ncdm']/d['rho_std']),
        'lambda':float(d['rho_lambda']/d['rho_std']),
      },
      'aggregate_diagnostics':{'rho_tot_is_not_species':True,
                               'rho_tot_exported_pchip':d['rho_tot_exported_pchip_diagnostic']},
      'historical_representation_diagnostic':historical_diag,
      'limits':{'baryon_consistency':BARYON_LIMIT,'homogeneous_closure':CLOSURE_LIMIT},
      'gates':gates,
      'claim_boundary':{'radial_initial_constraint_executed':False,'nonlinear_evolution_executed':False,
                        'finite_eta_executed':False,'turnaround_or_collapse_evaluated':False},
    }
    out=Path(a.out); out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))
    raise SystemExit(0 if cls.endswith('_PASS') else 2)

if __name__=='__main__':
    main()
