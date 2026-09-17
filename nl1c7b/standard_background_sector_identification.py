#!/usr/bin/env python3
from pathlib import Path
import argparse, json, math, sys
import numpy as np
from scipy.interpolate import PchipInterpolator

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import v063.theory_response_map as v63

AI=0.02
ZI=49.0
PARENT_RUN=35193003807
PARENT_HEAD='6804934c12b7fa02bbec3c5e1d06ec31466f1c44'
PARENT_ARTIFACT=10484278813
PARENT_SHA='76f24778c432b018724c90cdbb3c6a586dd37698fa9ae4eb644cf8acd0b99059'
PARENT_FREEZE='a932bd4a3d25b21e2e665ed53d0e09a48febf1b4'
PINNED_CLASS='e85808324f51fc694d12e3ed7439552a3c3f9540'
REPRO_LIMIT=1e-8
CLOSURE_LIMIT=1e-7
INTERP_LIMIT=2e-2
EXTRA_LIMIT=1e-7


def interp_at_ai(bg,key,method):
    z=np.asarray(bg['z'],float)
    y=np.asarray(bg[key],float)
    a=1.0/(1.0+z)
    order=np.argsort(a)
    x=np.log(a[order]); yy=y[order]
    x0=math.log(AI)
    if not (x[0] <= x0 <= x[-1]):
        raise RuntimeError(f'a_i outside CLASS background for {key}')
    if method=='pchip': return float(PchipInterpolator(x,yy)(x0))
    if method=='linear': return float(np.interp(x0,x,yy))
    raise ValueError(method)


def rel(a,b,scale=None):
    if scale is None: scale=max(abs(a),abs(b),1e-300)
    return abs(a-b)/max(scale,1e-300)


def source_gate(class_root):
    s=(Path(class_root)/'source'/'background.c').read_text()
    checks={
      'photon_density_explicit':'index_bg_rho_g' in s and 'Omega0_g * pow(pba->H0,2) / pow(a,4)' in s,
      'ur_density_explicit':'index_bg_rho_ur' in s,
      'ncdm_density_explicit':'index_bg_rho_ncdm1+n_ncdm' in s or 'index_bg_rho_ncdm1+n' in s,
      'lambda_density_explicit':'index_bg_rho_lambda' in s,
      'background_output_exposes_photons':'(.)rho_g' in s,
      'background_output_exposes_ur':'(.)rho_ur' in s,
      'background_output_exposes_ncdm':'(.)rho_ncdm[%d]' in s,
      'background_output_exposes_lambda':'(.)rho_lambda' in s,
    }
    return {'checks':checks,'pass':all(checks.values())}


def choose_key(bg,exact):
    return exact if exact in bg else None


def primary_and_extra(bg,method):
    keys=set(bg.keys())
    required=['H [1/Mpc]','(.)rho_g','(.)rho_b','(.)rho_cdm','(.)rho_ur']
    missing=[k for k in required if k not in keys]
    if missing: raise RuntimeError(f'missing CLASS background columns {missing}; keys={sorted(keys)}')
    ncdm=sorted(k for k in keys if k.startswith('(.)rho_ncdm['))
    lam='(.)rho_lambda' if '(.)rho_lambda' in keys else None
    vals={k:interp_at_ai(bg,k,method) for k in required}
    vals['ncdm']={k:interp_at_ai(bg,k,method) for k in ncdm}
    vals['lambda']=interp_at_ai(bg,lam,method) if lam else 0.0
    primary=vals['(.)rho_g']+vals['(.)rho_ur']+sum(vals['ncdm'].values())+vals['lambda']

    # Source-declared density columns not assigned to AeST, baryons, the primary sum,
    # or diagnostic critical density are reported separately and may not be hidden.
    allowed={'(.)rho_g','(.)rho_b','(.)rho_cdm','(.)rho_ur','(.)rho_lambda','(.)rho_crit'} | set(ncdm)
    rho_cols=sorted(k for k in keys if k.startswith('(.)rho_'))
    extra={}
    for k in rho_cols:
        if k in allowed: continue
        extra[k]=interp_at_ai(bg,k,method)
    return vals,primary,extra,rho_cols


def run_class(class_root):
    sys.path.insert(0,str(Path(class_root)/'python'))
    from classy import Class
    pars=dict(v63.class_params())
    # Use exactly the frozen physical model; output choice is diagnostic only.
    pars['output']='mTk'
    pars['aest_memory_enabled']='no'
    pars['aest_eta']=0.0
    c=Class(); c.set(pars); c.compute()
    try:
        bg=c.get_background()
        return {k:np.asarray(v).copy() for k,v in bg.items()}
    finally:
        c.struct_cleanup(); c.empty()


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--class-root',required=True)
    ap.add_argument('--parent-json',required=True)
    ap.add_argument('--out',required=True)
    a=ap.parse_args()
    parent=json.loads(Path(a.parent_json).read_text())
    source=source_gate(a.class_root)
    bg=run_class(a.class_root)
    pv,pstd,pextra,rho_cols=primary_and_extra(bg,'pchip')
    lv,lstd,lextra,_=primary_and_extra(bg,'linear')

    pm=parent['pchip']['median']
    lhs=float(pm['3H2']); rhoA=float(pm['rhoA_C6']); varrho_b=float(pm['varrho_b'])
    rho_rem=float(parent['missing_sector_diagnostic']['rho_rem_Mpc_inv2'])

    H_p=float(pv['H [1/Mpc]']); rb_p=float(pv['(.)rho_b']); ra_p=float(pv['(.)rho_cdm'])
    reproduce={
      'H_relative_error':rel(H_p,float(pm['H_Mpc_inv'])),
      'rho_b_relative_error':rel(rb_p,varrho_b/3.0),
      'rho_cdm_relative_error':rel(ra_p,float(pm['rhoA_trace_CLASS'])),
    }
    g2=max(reproduce.values())<=REPRO_LIMIT

    rho_std_c6=3.0*pstd
    rem_closure=abs(rho_rem-rho_std_c6)/max(lhs,1e-300)
    epsilon_full=abs(lhs-rhoA-varrho_b-rho_std_c6)/max(lhs,1e-300)
    l_rho_std_c6=3.0*lstd
    epsilon_full_linear=abs(lhs-rhoA-varrho_b-l_rho_std_c6)/max(lhs,1e-300)
    interp_change=abs(epsilon_full-epsilon_full_linear)

    extra_nonzero={k:v for k,v in pextra.items() if 3.0*abs(v)/max(lhs,1e-300)>EXTRA_LIMIT}
    g3=source['pass'] and len(extra_nonzero)==0
    g4=rem_closure<=CLOSURE_LIMIT
    g5=epsilon_full<=CLOSURE_LIMIT
    g6=interp_change<=INTERP_LIMIT
    provenance=(parent.get('classification')=='NL1C7B2_REPAIR01_HOMOGENEOUS_BACKGROUND_SECTOR_INCOMPLETE' and
                abs(rho_rem-0.00010529789814922824)<=1e-18)
    gates={'B3_G1_provenance':bool(provenance),'B3_G2_parent_reproduction':bool(g2),
           'B3_G3_standard_species_source_declared':bool(g3),'B3_G4_remainder_closure':bool(g4),
           'B3_G5_full_homogeneous_closure':bool(g5),'B3_G6_interpolation_control':bool(g6)}
    if all(gates.values()): cls='NL1C7B3_STANDARD_BACKGROUND_SECTOR_IDENTIFIED_PASS'
    elif provenance and g2 and source['pass'] and (extra_nonzero or not g4 or not g5):
        cls='NL1C7B3_STANDARD_BACKGROUND_SECTOR_INCOMPLETE'
    else: cls='NL1C7B3_STANDARD_BACKGROUND_IDENTIFICATION_FAIL'

    components={
      'rho_g_CLASS':float(pv['(.)rho_g']),
      'rho_ur_CLASS':float(pv['(.)rho_ur']),
      'rho_ncdm_CLASS':{k:float(v) for k,v in pv['ncdm'].items()},
      'rho_lambda_CLASS':float(pv['lambda']),
      'rho_std_CLASS':float(pstd),'rho_std_C6':float(rho_std_c6),
      'fractions_of_rho_std_CLASS':{}
    }
    if pstd!=0:
        components['fractions_of_rho_std_CLASS']={
          'photons':float(pv['(.)rho_g']/pstd),'ur':float(pv['(.)rho_ur']/pstd),
          'ncdm':float(sum(pv['ncdm'].values())/pstd),'lambda':float(pv['lambda']/pstd)}

    result={
      'classification':cls,
      'scope':'Identification of frozen standard homogeneous background species only; no radial constraint or trajectory.',
      'provenance':{'parent_run':PARENT_RUN,'parent_head':PARENT_HEAD,'parent_artifact':PARENT_ARTIFACT,
                    'parent_sha256':PARENT_SHA,'parent_result_freeze':PARENT_FREEZE,'pinned_CLASS':PINNED_CLASS,
                    'parameter_source':'v063/theory_response_map.py::class_params'},
      'a_i':AI,'z_i':ZI,'source_declaration':source,'background_density_columns':rho_cols,
      'parent_reproduction':reproduce,'components':components,
      'extra_density_columns_pchip':{k:float(v) for k,v in pextra.items()},
      'extra_nonzero_at_gate_scale':{k:float(v) for k,v in extra_nonzero.items()},
      'closure':{'fixed_parent_rho_rem_Mpc_inv2':rho_rem,'rho_std_C6_Mpc_inv2':float(rho_std_c6),
                 'remainder_closure_error':float(rem_closure),'epsilon_full':float(epsilon_full),
                 'epsilon_full_linear':float(epsilon_full_linear),'interpolation_change_abs':float(interp_change)},
      'limits':{'parent_reproduction':REPRO_LIMIT,'closure':CLOSURE_LIMIT,'interpolation_control':INTERP_LIMIT,'extra_sector_fraction':EXTRA_LIMIT},
      'gates':gates,
      'claim_boundary':{'radial_initial_constraint_executed':False,'nonlinear_evolution_executed':False,
                        'finite_eta_executed':False,'turnaround_or_collapse_evaluated':False},
    }
    out=Path(a.out); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))
    raise SystemExit(0 if cls.endswith('_PASS') else 2)

if __name__=='__main__': main()
