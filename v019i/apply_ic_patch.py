#!/usr/bin/env python3
from pathlib import Path
import argparse,json


def replace_once(path,old,new,label):
    p=Path(path)
    s=p.read_text()
    n=s.count(old)
    if n != 1:
        raise RuntimeError(f'{label}: expected exactly one anchor, found {n} in {p}')
    p.write_text(s.replace(old,new,1))


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('class_root')
    args=ap.parse_args()
    root=Path(args.class_root).resolve()
    repo=Path(__file__).resolve().parents[1]

    # Apply after v019/apply_patch_v019.py. The old v0.19 block already sets
    # alpha=-a*Theta/k^2 and E=0. v0.19i promotes this to the derived leading
    # adiabatic mode and adds the formally correct entropy factor (1+w_A) in delta_A.
    old='''    if (pba->aest_enabled == _TRUE_) {\n      class_test(ppt->gauge != newtonian,ppt->error_message,"AeST v0.19 is implemented only in Newtonian gauge");\n      ppw->pv->y[ppw->pv->index_pt_alpha_aest] =\n        -ppw->pvecback[pba->index_bg_a]*ppw->pv->y[ppw->pv->index_pt_theta_cdm]/(k*k);\n      ppw->pv->y[ppw->pv->index_pt_E_aest] = 0.;\n    }\n'''
    new='''    if (pba->aest_enabled == _TRUE_) {\n      double w_aest_ini;\n      class_test(ppt->gauge != newtonian,ppt->error_message,"AeST v0.19i is implemented only in Newtonian gauge");\n      w_aest_ini = ppw->pvecback[pba->index_bg_w_aest];\n\n      /* Leading radiation-era adiabatic mode. Vanishing relative entropy gives\n         delta_A/(1+w_A)=delta_c. The gauge-invariant AeST combinations\n         chi=varphi+Q alpha and E=alpha_dot+Psi vanish for the long-wavelength\n         time-shift mode, hence alpha=-theta_A=-a*Theta_A/k^2 and E=0. */\n      ppw->pv->y[ppw->pv->index_pt_delta_cdm] *= (1.+w_aest_ini);\n      ppw->pv->y[ppw->pv->index_pt_alpha_aest] =\n        -ppw->pvecback[pba->index_bg_a]*ppw->pv->y[ppw->pv->index_pt_theta_cdm]/(k*k);\n      ppw->pv->y[ppw->pv->index_pt_E_aest] = 0.;\n    }\n'''
    replace_once(root/'source'/'perturbations.c',old,new,'AeST leading adiabatic IC block')

    txt=(root/'source'/'perturbations.c').read_text()
    checks={
      'entropy_factor':'index_pt_delta_cdm] *= (1.+w_aest_ini)' in txt,
      'chi_zero_relation':'-ppw->pvecback[pba->index_bg_a]*ppw->pv->y[ppw->pv->index_pt_theta_cdm]/(k*k)' in txt,
      'E_zero':'ppw->pv->y[ppw->pv->index_pt_E_aest] = 0.;' in txt,
      'memory_absent':'aest_eta' not in txt,
    }
    if not all(checks.values()):
        raise RuntimeError('v0.19i source audit failed: '+repr(checks))

    report={
      'classification':'LEADING_SUPERHORIZON_ADIABATIC_IC',
      'delta_relation':'delta_A=(1+w_A) delta_c',
      'velocity_relation':'Theta_A=Theta_c',
      'chi_relation':'chi_A=0 -> alpha_A=-a Theta_A/k^2',
      'E_relation':'E_A=0',
      'finite_gradient_status':'O((k/H)^2) terms tested by start-time convergence, not assumed zero exactly at finite k',
      'memory_enabled':False,
      'source_audit':checks,
    }
    (repo/'results').mkdir(exist_ok=True)
    (repo/'results'/'v019i_apply_report.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))

if __name__=='__main__':
    main()
