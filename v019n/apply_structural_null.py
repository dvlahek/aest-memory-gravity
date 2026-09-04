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

    # This patch is intentionally applied AFTER v019/apply_patch_v019.py.
    # It adds a second, mutually exclusive switch that allocates alpha/E
    # while leaving the physical AeST path disabled.

    replace_once(root/'include'/'background.h',
'''  short aest_enabled;\n  int aest_model;            /**< 1=Cosh, 2=Exp */\n''',
'''  short aest_enabled;\n  short aest_null_states;    /**< v0.19n: allocate frozen alpha/E with CDM physics */\n  int aest_model;            /**< 1=Cosh, 2=Exp */\n''','null flag field')

    replace_once(root/'source'/'input.c',
'''  pba->aest_enabled = _FALSE_;\n  pba->aest_model = _AEST_MODEL_COSH_;\n''',
'''  pba->aest_enabled = _FALSE_;\n  pba->aest_null_states = _FALSE_;\n  pba->aest_model = _AEST_MODEL_COSH_;\n''','null flag default')

    replace_once(root/'source'/'input.c',
'''  class_read_flag("aest_enabled",pba->aest_enabled);\n  class_call(parser_read_string(pfc,"aest_model",&string1,&flag1,errmsg),errmsg,errmsg);\n''',
'''  class_read_flag("aest_enabled",pba->aest_enabled);\n  class_read_flag("aest_null_states",pba->aest_null_states);\n  class_test((pba->aest_enabled == _TRUE_) && (pba->aest_null_states == _TRUE_),errmsg,\n             "aest_enabled and aest_null_states are mutually exclusive");\n  class_call(parser_read_string(pfc,"aest_model",&string1,&flag1,errmsg),errmsg,errmsg);\n''','null flag parser')

    replace_once(root/'source'/'perturbations.c',
'''    class_define_index(ppv->index_pt_alpha_aest,pba->aest_enabled && (ppt->gauge == newtonian),index_pt,1);\n    class_define_index(ppv->index_pt_E_aest,pba->aest_enabled && (ppt->gauge == newtonian),index_pt,1);\n''',
'''    class_define_index(ppv->index_pt_alpha_aest,(pba->aest_enabled || pba->aest_null_states) && (ppt->gauge == newtonian),index_pt,1);\n    class_define_index(ppv->index_pt_E_aest,(pba->aest_enabled || pba->aest_null_states) && (ppt->gauge == newtonian),index_pt,1);\n''','null-state vector allocation')

    replace_once(root/'source'/'perturbations.c',
'''          if (pba->aest_enabled == _TRUE_) {\n            ppv->y[ppv->index_pt_alpha_aest] = ppw->pv->y[ppw->pv->index_pt_alpha_aest];\n            ppv->y[ppv->index_pt_E_aest] = ppw->pv->y[ppw->pv->index_pt_E_aest];\n          }\n''',
'''          if ((pba->aest_enabled == _TRUE_) || (pba->aest_null_states == _TRUE_)) {\n            ppv->y[ppv->index_pt_alpha_aest] = ppw->pv->y[ppw->pv->index_pt_alpha_aest];\n            ppv->y[ppv->index_pt_E_aest] = ppw->pv->y[ppw->pv->index_pt_E_aest];\n          }\n''','null-state approximation-switch copy')

    replace_once(root/'source'/'perturbations.c',
'''    if (pba->aest_enabled == _TRUE_) {\n      class_test(ppt->gauge != newtonian,ppt->error_message,"AeST v0.19 is implemented only in Newtonian gauge");\n      ppw->pv->y[ppw->pv->index_pt_alpha_aest] =\n        -ppw->pvecback[pba->index_bg_a]*ppw->pv->y[ppw->pv->index_pt_theta_cdm]/(k*k);\n      ppw->pv->y[ppw->pv->index_pt_E_aest] = 0.;\n    }\n\n      /** - (e) In any gauge, we should now implement the relativistic initial conditions in ur and ncdm variables */\n''',
'''    if (pba->aest_enabled == _TRUE_) {\n      class_test(ppt->gauge != newtonian,ppt->error_message,"AeST v0.19 is implemented only in Newtonian gauge");\n      ppw->pv->y[ppw->pv->index_pt_alpha_aest] =\n        -ppw->pvecback[pba->index_bg_a]*ppw->pv->y[ppw->pv->index_pt_theta_cdm]/(k*k);\n      ppw->pv->y[ppw->pv->index_pt_E_aest] = 0.;\n    }\n    if (pba->aest_null_states == _TRUE_) {\n      class_test(ppt->gauge != newtonian,ppt->error_message,"AeST structural-null states require Newtonian gauge");\n      ppw->pv->y[ppw->pv->index_pt_alpha_aest] = 0.;\n      ppw->pv->y[ppw->pv->index_pt_E_aest] = 0.;\n    }\n\n      /** - (e) In any gauge, we should now implement the relativistic initial conditions in ur and ncdm variables */\n''','null-state initial values')

    old_tail='''      else {\n        if (ppt->gauge == newtonian) {\n          dy[pv->index_pt_delta_cdm] = -(y[pv->index_pt_theta_cdm]+metric_continuity);\n          dy[pv->index_pt_theta_cdm] = -a_prime_over_a*y[pv->index_pt_theta_cdm]+metric_euler;\n        }\n        if (ppt->gauge == synchronous)\n          dy[pv->index_pt_delta_cdm] = -metric_continuity;\n      }\n    }\n'''
    new_tail='''      else {\n        if (ppt->gauge == newtonian) {\n          dy[pv->index_pt_delta_cdm] = -(y[pv->index_pt_theta_cdm]+metric_continuity);\n          dy[pv->index_pt_theta_cdm] = -a_prime_over_a*y[pv->index_pt_theta_cdm]+metric_euler;\n        }\n        if (ppt->gauge == synchronous)\n          dy[pv->index_pt_delta_cdm] = -metric_continuity;\n      }\n      if (pba->aest_null_states == _TRUE_) {\n        dy[pv->index_pt_alpha_aest] = 0.;\n        dy[pv->index_pt_E_aest] = 0.;\n      }\n    }\n'''
    replace_once(root/'source'/'perturbations.c',old_tail,new_tail,'null-state frozen derivatives')

    # Source audit: the null flag must occur in allocation, copy, IC and derivative blocks.
    ptxt=(root/'source'/'perturbations.c').read_text()
    checks={
      'allocation_or_condition':'pba->aest_enabled || pba->aest_null_states' in ptxt,
      'copy_or_condition':'pba->aest_null_states == _TRUE_' in ptxt,
      'zero_alpha_derivative':'dy[pv->index_pt_alpha_aest] = 0.;' in ptxt,
      'zero_E_derivative':'dy[pv->index_pt_E_aest] = 0.;' in ptxt,
      'physical_stress_still_guarded':'if (pba->aest_enabled == _TRUE_)' in ptxt,
    }
    if not all(checks.values()):
        raise RuntimeError('structural-null source audit failed: '+repr(checks))

    report={
      'classification':'STRICT_STRUCTURAL_NULL_PATCH',
      'aest_physics_enabled':False,
      'standard_cdm_background':True,
      'standard_cdm_delta_theta_equations':True,
      'extra_states':['alpha_aest','E_aest'],
      'extra_initial_values':[0.0,0.0],
      'extra_derivatives':[0.0,0.0],
      'extra_stress_energy':False,
      'mutually_exclusive_with_aest_enabled':True,
      'source_audit':checks,
    }
    (repo/'results').mkdir(exist_ok=True)
    (repo/'results'/'v019n_apply_report.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))

if __name__=='__main__':
    main()
