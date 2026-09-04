#!/usr/bin/env python3
from pathlib import Path
import argparse,json


def replace_once(path,old,new,label):
    p=Path(path);s=p.read_text();n=s.count(old)
    if n != 1:
        raise RuntimeError(f'{label}: expected exactly one anchor, found {n} in {p}')
    p.write_text(s.replace(old,new,1))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('class_root');args=ap.parse_args()
    root=Path(args.class_root).resolve();repo=Path(__file__).resolve().parents[1]

    # Input/state fields.
    replace_once(root/'include'/'background.h',
'''  double aest_I0;            /**< calibrated shift-charge integration constant */\n''',
'''  double aest_I0;            /**< calibrated shift-charge integration constant */\n  short aest_memory_enabled;   /**< finite positive Drude bath in scalar closure */\n  double aest_eta;             /**< dimensionless high-frequency memory strength */\n  double aest_tau_H0;          /**< relaxation time in H0^{-1} units */\n  int aest_memory_order;       /**< positive bath design: 16 or 20 */\n''','memory background fields')

    replace_once(root/'include'/'perturbations.h',
'''  int index_pt_E_aest;     /**< AeST scalar closure E=alpha_dot+Psi */\n''',
'''  int index_pt_E_aest;     /**< AeST scalar closure E=alpha_dot+Psi */\n  int index_pt_mem_q_aest; /**< first normalized finite-bath coordinate */\n  int index_pt_mem_p_aest; /**< first conformal derivative of bath coordinate */\n''','memory perturbation indices')

    # Expose positive bath designs from the compiled module.
    replace_once(root/'include'/'aest_memory.h',
'''int aest_memory_selfcheck(double *max_rel);\n''',
'''int aest_memory_selfcheck(double *max_rel);\nint aest_memory_active_count(int order);\ndouble aest_memory_node_order(int order,int j);\ndouble aest_memory_weight_order(int order,int j);\n''','memory module prototypes')

    src=root/'source'/'aest_memory.c'
    s=src.read_text()
    marker='/* AeST v0.19j positive finite-bath design accessors */'
    if marker not in s:
        s += r'''

/* AeST v0.19j positive finite-bath design accessors */
static const double _aest_nodes16[15] = {
  3.1622776601683794e-4,9.261187281287938e-4,2.712272579332028e-3,
  7.943282347242814e-3,2.326305067153626e-2,6.812920690579608e-2,
  1.9952623149688795e-1,5.843414133735175e-1,1.7113283041617808,
  5.011872336272725,14.67799267622069,42.986623470822764,
  125.89254117941675,368.69450645195735,1079.7751623277093
};
static const double _aest_weights16[15] = {
  3.5602e-4,6.0227e-4,1.85947e-3,5.43372e-3,1.590377e-2,
  4.637989e-2,1.3142693e-1,2.9663175e-1,3.0196035e-1,
  1.2703549e-1,4.951583e-2,1.380963e-2,6.8728e-3,
  6.8313e-4,1.77056e-3
};

int aest_memory_active_count(int order) {
  if (order == 16) return 15;
  if (order == 20) return 19; /* final fitted weight is exactly zero */
  return 0;
}

double aest_memory_node_order(int order,int j) {
  if (order == 16) {
    if (j<0 || j>=15) return -1.;
    return _aest_nodes16[j];
  }
  if (order == 20) {
    if (j<0 || j>=19) return -1.;
    return _aest_nodes[j];
  }
  return -1.;
}

double aest_memory_weight_order(int order,int j) {
  if (order == 16) {
    if (j<0 || j>=15) return -1.;
    return _aest_weights16[j];
  }
  if (order == 20) {
    if (j<0 || j>=19) return -1.;
    return _aest_weights[j];
  }
  return -1.;
}
'''
        src.write_text(s)

    # Defaults and parser.
    replace_once(root/'source'/'input.c',
'''  pba->aest_I0 = 0.;\n''',
'''  pba->aest_I0 = 0.;\n  pba->aest_memory_enabled = _FALSE_;\n  pba->aest_eta = 0.;\n  pba->aest_tau_H0 = 1.;\n  pba->aest_memory_order = 16;\n''','memory defaults')

    replace_once(root/'source'/'input.c',
'''  class_read_double("aest_Z0",pba->aest_Z0);\n  if (pba->aest_enabled == _TRUE_) {\n''',
'''  class_read_double("aest_Z0",pba->aest_Z0);\n  class_read_flag("aest_memory_enabled",pba->aest_memory_enabled);\n  class_read_double("aest_eta",pba->aest_eta);\n  class_read_double("aest_tau_H0",pba->aest_tau_H0);\n  class_read_int("aest_memory_order",pba->aest_memory_order);\n  class_test((pba->aest_memory_enabled == _TRUE_) && (pba->aest_enabled == _FALSE_),errmsg,\n             "aest_memory_enabled requires aest_enabled=yes");\n  class_test(pba->aest_eta < 0.,errmsg,"AeST memory requires aest_eta >= 0");\n  class_test(pba->aest_tau_H0 <= 0.,errmsg,"AeST memory requires aest_tau_H0 > 0");\n  class_test((pba->aest_memory_order != 16) && (pba->aest_memory_order != 20),errmsg,\n             "aest_memory_order must be 16 or 20");\n  if (pba->aest_enabled == _TRUE_) {\n''','memory parser')

    # Allocate the normalized q_j and q_j' arrays only when the memory representation is active.
    replace_once(root/'source'/'perturbations.c',
'''    class_define_index(ppv->index_pt_alpha_aest,pba->aest_enabled && (ppt->gauge == newtonian),index_pt,1);\n    class_define_index(ppv->index_pt_E_aest,pba->aest_enabled && (ppt->gauge == newtonian),index_pt,1);\n''',
'''    class_define_index(ppv->index_pt_alpha_aest,pba->aest_enabled && (ppt->gauge == newtonian),index_pt,1);\n    class_define_index(ppv->index_pt_E_aest,pba->aest_enabled && (ppt->gauge == newtonian),index_pt,1);\n    class_define_index(ppv->index_pt_mem_q_aest,pba->aest_enabled && pba->aest_memory_enabled && (ppt->gauge == newtonian),index_pt,aest_memory_active_count(pba->aest_memory_order));\n    class_define_index(ppv->index_pt_mem_p_aest,pba->aest_enabled && pba->aest_memory_enabled && (ppt->gauge == newtonian),index_pt,aest_memory_active_count(pba->aest_memory_order));\n''','memory vector allocation')

    # Preserve bath states across CLASS approximation-vector rebuilds.
    replace_once(root/'source'/'perturbations.c',
'''          if (pba->aest_enabled == _TRUE_) {\n            ppv->y[ppv->index_pt_alpha_aest] = ppw->pv->y[ppw->pv->index_pt_alpha_aest];\n            ppv->y[ppv->index_pt_E_aest] = ppw->pv->y[ppw->pv->index_pt_E_aest];\n          }\n''',
'''          if (pba->aest_enabled == _TRUE_) {\n            int jm;\n            ppv->y[ppv->index_pt_alpha_aest] = ppw->pv->y[ppw->pv->index_pt_alpha_aest];\n            ppv->y[ppv->index_pt_E_aest] = ppw->pv->y[ppw->pv->index_pt_E_aest];\n            if (pba->aest_memory_enabled == _TRUE_) {\n              int nm=aest_memory_active_count(pba->aest_memory_order);\n              for (jm=0;jm<nm;jm++) {\n                ppv->y[ppv->index_pt_mem_q_aest+jm] = ppw->pv->y[ppw->pv->index_pt_mem_q_aest+jm];\n                ppv->y[ppv->index_pt_mem_p_aest+jm] = ppw->pv->y[ppw->pv->index_pt_mem_p_aest+jm];\n              }\n            }\n          }\n''','memory approximation-switch copy')

    # Regular memory initial condition. The leading adiabatic mode has chi_i=0,
    # so the bath has the unique regular zero solution at leading order.
    replace_once(root/'source'/'perturbations.c',
'''      ppw->pv->y[ppw->pv->index_pt_E_aest] = 0.;\n    }\n\n      /** - (e) In any gauge, we should now implement the relativistic initial conditions in ur and ncdm variables */\n''',
'''      ppw->pv->y[ppw->pv->index_pt_E_aest] = 0.;\n      if (pba->aest_memory_enabled == _TRUE_) {\n        int jm,nm=aest_memory_active_count(pba->aest_memory_order);\n        for (jm=0;jm<nm;jm++) {\n          ppw->pv->y[ppw->pv->index_pt_mem_q_aest+jm] = 0.;\n          ppw->pv->y[ppw->pv->index_pt_mem_p_aest+jm] = 0.;\n        }\n      }\n    }\n\n      /** - (e) In any gauge, we should now implement the relativistic initial conditions in ur and ncdm variables */\n''','memory adiabatic IC')

    # Add the positive finite bath and the -Q B_chi/2 closure source.
    replace_once(root/'source'/'perturbations.c',
'''        E_rhs_aest = KQ_aest*chi_aest\n          -(2.-pba->aest_KB)*(Q_aest*Pi_aest/(1.+w_aest)\n                              +(H_aest+Q_aest)*chi_aest\n                              -3.*cad2_aest*H_aest*Q_aest*alpha_aest);\n        dy[pv->index_pt_E_aest] = a*E_rhs_aest/pba->aest_KB-a_prime_over_a*E_aest;\n''',
'''        E_rhs_aest = KQ_aest*chi_aest\n          -(2.-pba->aest_KB)*(Q_aest*Pi_aest/(1.+w_aest)\n                              +(H_aest+Q_aest)*chi_aest\n                              -3.*cad2_aest*H_aest*Q_aest*alpha_aest);\n\n        if (pba->aest_memory_enabled == _TRUE_) {\n          int jm,nm=aest_memory_active_count(pba->aest_memory_order);\n          double Bchi_aest=0.;\n          for (jm=0;jm<nm;jm++) {\n            double rj=aest_memory_node_order(pba->aest_memory_order,jm);\n            double wj=aest_memory_weight_order(pba->aest_memory_order,jm);\n            double sw=sqrt(wj);\n            double omega_j=rj*pba->H0/pba->aest_tau_H0;\n            double qj=y[pv->index_pt_mem_q_aest+jm];\n            double pj=y[pv->index_pt_mem_p_aest+jm];\n\n            /* q_j=sqrt(w_j) u_j. In conformal time:\n               q_j''+2 Hconf q_j'+a^2 omega_j^2 q_j\n               = a k omega_j sqrt(w_j) chi. */\n            dy[pv->index_pt_mem_q_aest+jm] = pj;\n            dy[pv->index_pt_mem_p_aest+jm] =\n              -2.*a_prime_over_a*pj-a*a*omega_j*omega_j*qj\n              +a*k*omega_j*sw*chi_aest;\n\n            Bchi_aest += wj*chi_aest-sw*(a*omega_j/k)*qj;\n          }\n          Bchi_aest *= pba->aest_eta;\n          E_rhs_aest -= 0.5*Q_aest*Bchi_aest;\n        }\n\n        dy[pv->index_pt_E_aest] = a*E_rhs_aest/pba->aest_KB-a_prime_over_a*E_aest;\n''','memory E closure and bath dynamics')

    # Source audit.
    ptxt=(root/'source'/'perturbations.c').read_text();htxt=(root/'include'/'background.h').read_text()
    checks={
      'eta_input':'aest_eta' in htxt,
      'bath_q_index':'index_pt_mem_q_aest' in ptxt,
      'bath_p_index':'index_pt_mem_p_aest' in ptxt,
      'positive_weight_sqrt':'sqrt(wj)' in ptxt,
      'conformal_friction':'-2.*a_prime_over_a*pj' in ptxt,
      'memory_closure':'E_rhs_aest -= 0.5*Q_aest*Bchi_aest' in ptxt,
      'no_direct_memory_stress':'Bchi_aest' not in ptxt[ptxt.find('/* cdm contribution, promoted'):ptxt.find('/* idm contribution */')],
    }
    if not all(checks.values()):raise RuntimeError('v0.19j source audit failed: '+repr(checks))

    report={
      'classification':'FINITE_POSITIVE_DRUDE_MEMORY_CLASS_PATCH',
      'memory_background_correction':0,
      'memory_direct_linear_Einstein_stress':0,
      'inputs':['aest_memory_enabled','aest_eta','aest_tau_H0','aest_memory_order'],
      'orders':[16,20],
      'active_nodes':{'16':15,'20':19},
      'normalized_states':'q_j=sqrt(w_j) u_j, p_j=dq_j/d(conformal time)',
      'leading_memory_IC':'q_j=p_j=0 because chi_i=0 in the leading adiabatic mode',
      'closure_source':'E_rhs -> E_rhs - Q B_chi/2',
      'source_audit':checks,
    }
    (repo/'results').mkdir(exist_ok=True)
    (repo/'results'/'v019j_apply_report.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
