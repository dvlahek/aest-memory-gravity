#!/usr/bin/env python3
from pathlib import Path
import argparse, shutil, json

TARGET_VERSION='v3.3.4'
TARGET_SHA='e85808324f51fc694d12e3ed7439552a3c3f9540'
OLD_SOURCE='SOURCE = input.o background.o thermodynamics.o perturbations.opp primordial.opp fourier.o transfer.opp harmonic.opp lensing.opp distortions.o'
NEW_SOURCE='SOURCE = input.o background.o thermodynamics.o aest_memory.o perturbations.opp primordial.opp fourier.o transfer.opp harmonic.opp lensing.opp distortions.o'


def replace_once(path, old, new, label):
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
    here=Path(__file__).resolve().parent
    root=Path(args.class_root).resolve()
    common=root/'include'/'common.h'
    if not common.exists():
        raise SystemExit('Not a CLASS source root')
    if f'#define _VERSION_ "{TARGET_VERSION}"' not in common.read_text(errors='replace'):
        raise SystemExit(f'CLASS version mismatch; expected {TARGET_VERSION}')

    make=root/'Makefile'
    ms=make.read_text()
    if 'aest_memory.o' not in ms:
        if OLD_SOURCE not in ms:
            raise RuntimeError('Pinned Makefile SOURCE line not found')
        make.write_text(ms.replace(OLD_SOURCE,NEW_SOURCE,1))
    shutil.copy2(here/'patch'/'include'/'aest_memory.h', root/'include'/'aest_memory.h')
    shutil.copy2(here/'patch'/'source'/'aest_memory.c', root/'source'/'aest_memory.c')

    replace_once(root/'include'/'background.h',
'''  double Omega0_cdm;      /**< \\f$ \\Omega_{0 cdm} \\f$: cold dark matter */\n''',
'''  double Omega0_cdm;      /**< \\f$ \\Omega_{0 cdm} \\f$: cold dark matter */\n\n  /* AeST v0.19: when enabled, the CDM slot is reinterpreted as the\n     effective AeST dark component while preserving standard CLASS\n     exactly when disabled. Q0 and Z0 are in Mpc^-1. */\n  short aest_enabled;\n  int aest_model;            /**< 1=Cosh, 2=Exp */\n  double aest_KB;\n  double aest_Q0;\n  double aest_K2;\n  double aest_Z0;\n  double aest_I0;            /**< calibrated shift-charge integration constant */\n''','background input fields')

    replace_once(root/'include'/'background.h',
'''  int index_bg_rho_cdm;       /**< cdm density */\n''',
'''  int index_bg_rho_cdm;       /**< cdm density, or AeST effective density when aest_enabled */\n  int index_bg_p_aest;          /**< AeST effective pressure */\n  int index_bg_w_aest;          /**< AeST w=P/rho */\n  int index_bg_cad2_aest;       /**< AeST adiabatic sound speed squared */\n  int index_bg_Q_aest;          /**< AeST homogeneous Q=phidot */\n  int index_bg_KQ_aest;         /**< dK/dQ */\n''','background indices')

    replace_once(root/'include'/'perturbations.h',
'''  int index_pt_delta_cdm; /**< cdm density */\n  int index_pt_theta_cdm; /**< cdm velocity */\n''',
'''  int index_pt_delta_cdm; /**< cdm density, or AeST effective density contrast */\n  int index_pt_theta_cdm; /**< cdm velocity divergence, or AeST effective velocity divergence */\n  int index_pt_alpha_aest; /**< AeST scalar aether potential alpha [Mpc] */\n  int index_pt_E_aest;     /**< AeST scalar closure E=alpha_dot+Psi */\n''','perturbation indices')

    replace_once(root/'source'/'input.c',
'''#include "output.h"\n''',
'''#include "output.h"\n#include "aest_memory.h"\n''','input include')

    replace_once(root/'source'/'input.c',
'''  /** 4) CDM density */\n  pba->Omega0_cdm = 0.1201075/pow(pba->h,2);\n''',
'''  /** 4) CDM density */\n  pba->Omega0_cdm = 0.1201075/pow(pba->h,2);\n\n  /** 4.a) AeST effective dark component (disabled by default) */\n  pba->aest_enabled = _FALSE_;\n  pba->aest_model = _AEST_MODEL_COSH_;\n  pba->aest_KB = 0.5;\n  pba->aest_Q0 = 0.1;\n  pba->aest_K2 = 7.5e3;\n  pba->aest_Z0 = 1.e-9;\n  pba->aest_I0 = 0.;\n''','input defaults')

    replace_once(root/'source'/'input.c',
'''  class_test(pba->Omega0_cdm<0,errmsg, "You cannot set the cold dark matter density to negative values.");\n\n  /** 4) (Second part) Omega_0_m (total non-relativistic) */\n''',
'''  class_test(pba->Omega0_cdm<0,errmsg, "You cannot set the cold dark matter density to negative values.");\n\n  /** 4.a) AeST replacement of the CDM slot */\n  class_read_flag("aest_enabled",pba->aest_enabled);\n  class_call(parser_read_string(pfc,"aest_model",&string1,&flag1,errmsg),errmsg,errmsg);\n  if (flag1 == _TRUE_) {\n    if ((strcmp(string1,"Cosh") == 0) || (strcmp(string1,"cosh") == 0)) pba->aest_model = _AEST_MODEL_COSH_;\n    else if ((strcmp(string1,"Exp") == 0) || (strcmp(string1,"exp") == 0)) pba->aest_model = _AEST_MODEL_EXP_;\n    else class_stop(errmsg,"aest_model must be Cosh or Exp");\n  }\n  class_read_double("aest_KB",pba->aest_KB);\n  class_read_double("aest_Q0",pba->aest_Q0);\n  class_read_double("aest_K2",pba->aest_K2);\n  class_read_double("aest_Z0",pba->aest_Z0);\n  if (pba->aest_enabled == _TRUE_) {\n    class_test((pba->aest_KB <= 0.) || (pba->aest_KB >= 2.),errmsg,"AeST requires 0 < aest_KB < 2");\n    class_test(pba->aest_Q0 <= 0.,errmsg,"AeST requires aest_Q0 > 0 Mpc^-1");\n    class_test(pba->aest_K2 <= 0.,errmsg,"AeST requires aest_K2 > 0");\n    class_test(pba->aest_Z0 <= 0.,errmsg,"AeST requires aest_Z0 > 0 Mpc^-1");\n  }\n\n  /** 4) (Second part) Omega_0_m (total non-relativistic) */\n''','input parser')

    replace_once(root/'source'/'background.c',
'''#include "background.h"\n''',
'''#include "background.h"\n#include "aest_memory.h"\n''','background include')

    replace_once(root/'source'/'background.c',
'''  if (pba->Omega0_cdm != 0.)\n    pba->has_cdm = _TRUE_;\n\n  if (pba->Omega0_idm != 0.)\n''',
'''  if (pba->Omega0_cdm != 0.)\n    pba->has_cdm = _TRUE_;\n\n  if (pba->aest_enabled == _TRUE_) {\n    class_test(pba->has_cdm == _FALSE_,pba->error_message,"AeST v0.19 needs a non-zero Omega_cdm/omega_cdm target density");\n    class_test(aest_background_calibrate(pba->aest_model,\n                                         pba->aest_Q0,\n                                         pba->aest_K2,\n                                         pba->aest_Z0,\n                                         3.*pba->Omega0_cdm*pow(pba->H0,2),\n                                         &(pba->aest_I0)) != 0,\n               pba->error_message,\n               "AeST background calibration failed");\n  }\n\n  if (pba->Omega0_idm != 0.)\n''','background calibration')

    replace_once(root/'source'/'background.c',
'''  /* - index for rho_cdm */\n  class_define_index(pba->index_bg_rho_cdm,pba->has_cdm,index_bg,1);\n\n  /* - index for rho_idm  */\n''',
'''  /* - index for rho_cdm / AeST effective dark density */\n  class_define_index(pba->index_bg_rho_cdm,pba->has_cdm,index_bg,1);\n  class_define_index(pba->index_bg_p_aest,pba->aest_enabled,index_bg,1);\n  class_define_index(pba->index_bg_w_aest,pba->aest_enabled,index_bg,1);\n  class_define_index(pba->index_bg_cad2_aest,pba->aest_enabled,index_bg,1);\n  class_define_index(pba->index_bg_Q_aest,pba->aest_enabled,index_bg,1);\n  class_define_index(pba->index_bg_KQ_aest,pba->aest_enabled,index_bg,1);\n\n  /* - index for rho_idm  */\n''','background normal indices')

    replace_once(root/'source'/'background.c',
'''  /* cdm */\n  if (pba->has_cdm == _TRUE_) {\n    pvecback[pba->index_bg_rho_cdm] = pba->Omega0_cdm * pow(pba->H0,2) / pow(a,3);\n    rho_tot += pvecback[pba->index_bg_rho_cdm];\n    p_tot += 0.;\n    rho_m += pvecback[pba->index_bg_rho_cdm];\n  }\n''',
'''  /* cdm, or the AeST effective dark component in the v0.19 bridge */\n  if (pba->has_cdm == _TRUE_) {\n    if (pba->aest_enabled == _TRUE_) {\n      double rho_aest,p_aest,w_aest,cad2_aest,Q_aest,KQ_aest;\n      class_test(aest_background_eval(pba->aest_model,\n                                      pba->aest_Q0,\n                                      pba->aest_K2,\n                                      pba->aest_Z0,\n                                      pba->aest_I0,\n                                      a,\n                                      &rho_aest,&p_aest,&w_aest,&cad2_aest,&Q_aest,&KQ_aest) != 0,\n                 pba->error_message,\n                 "AeST background evaluation failed at a=%e",a);\n      pvecback[pba->index_bg_rho_cdm] = rho_aest;\n      pvecback[pba->index_bg_p_aest] = p_aest;\n      pvecback[pba->index_bg_w_aest] = w_aest;\n      pvecback[pba->index_bg_cad2_aest] = cad2_aest;\n      pvecback[pba->index_bg_Q_aest] = Q_aest;\n      pvecback[pba->index_bg_KQ_aest] = KQ_aest;\n      rho_tot += rho_aest;\n      p_tot += p_aest;\n      dp_dloga += -3.*cad2_aest*(rho_aest+p_aest);\n      rho_r += 3.*p_aest;\n      rho_m += rho_aest-3.*p_aest;\n    }\n    else {\n      pvecback[pba->index_bg_rho_cdm] = pba->Omega0_cdm * pow(pba->H0,2) / pow(a,3);\n      rho_tot += pvecback[pba->index_bg_rho_cdm];\n      p_tot += 0.;\n      rho_m += pvecback[pba->index_bg_rho_cdm];\n    }\n  }\n''','background CDM/AeST law')

    replace_once(root/'source'/'perturbations.c',
'''#include "perturbations.h"\n#include "parallel.h"\n''',
'''#include "perturbations.h"\n#include "parallel.h"\n#include "aest_memory.h"\n''','perturbation include')

    replace_once(root/'source'/'perturbations.c',
'''    class_define_index(ppv->index_pt_delta_cdm,pba->has_cdm,index_pt,1); /* cdm density */\n    class_define_index(ppv->index_pt_theta_cdm,pba->has_cdm && (ppt->gauge == newtonian),index_pt,1); /* cdm velocity */\n\n    /* idm */\n''',
'''    class_define_index(ppv->index_pt_delta_cdm,pba->has_cdm,index_pt,1); /* cdm/AeST density */\n    class_define_index(ppv->index_pt_theta_cdm,pba->has_cdm && (ppt->gauge == newtonian),index_pt,1); /* cdm/AeST velocity */\n    class_define_index(ppv->index_pt_alpha_aest,pba->aest_enabled && (ppt->gauge == newtonian),index_pt,1);\n    class_define_index(ppv->index_pt_E_aest,pba->aest_enabled && (ppt->gauge == newtonian),index_pt,1);\n\n    /* idm */\n''','perturbation vector allocation')

    replace_once(root/'source'/'perturbations.c',
'''      if (pba->has_cdm == _TRUE_) {\n\n        ppv->y[ppv->index_pt_delta_cdm] =\n          ppw->pv->y[ppw->pv->index_pt_delta_cdm];\n\n        if (ppt->gauge == newtonian) {\n          ppv->y[ppv->index_pt_theta_cdm] =\n            ppw->pv->y[ppw->pv->index_pt_theta_cdm];\n        }\n''',
'''      if (pba->has_cdm == _TRUE_) {\n\n        ppv->y[ppv->index_pt_delta_cdm] =\n          ppw->pv->y[ppw->pv->index_pt_delta_cdm];\n\n        if (ppt->gauge == newtonian) {\n          ppv->y[ppv->index_pt_theta_cdm] =\n            ppw->pv->y[ppw->pv->index_pt_theta_cdm];\n          if (pba->aest_enabled == _TRUE_) {\n            ppv->y[ppv->index_pt_alpha_aest] = ppw->pv->y[ppw->pv->index_pt_alpha_aest];\n            ppv->y[ppv->index_pt_E_aest] = ppw->pv->y[ppw->pv->index_pt_E_aest];\n          }\n        }\n''','perturbation switch copy')

    replace_once(root/'source'/'perturbations.c',
'''    } /* end of gauge transformation to newtonian gauge */\n\n      /** - (e) In any gauge, we should now implement the relativistic initial conditions in ur and ncdm variables */\n''',
'''    } /* end of gauge transformation to newtonian gauge */\n\n    if (pba->aest_enabled == _TRUE_) {\n      class_test(ppt->gauge != newtonian,ppt->error_message,"AeST v0.19 is implemented only in Newtonian gauge");\n      ppw->pv->y[ppw->pv->index_pt_alpha_aest] =\n        -ppw->pvecback[pba->index_bg_a]*ppw->pv->y[ppw->pv->index_pt_theta_cdm]/(k*k);\n      ppw->pv->y[ppw->pv->index_pt_E_aest] = 0.;\n    }\n\n      /** - (e) In any gauge, we should now implement the relativistic initial conditions in ur and ncdm variables */\n''','AeST initial conditions')

    old_stress='''    /* cdm contribution */\n    if (pba->has_cdm == _TRUE_) {\n      ppw->delta_rho += ppw->pvecback[pba->index_bg_rho_cdm]*y[ppw->pv->index_pt_delta_cdm]; // contribution to total perturbed stress-energy\n      if (ppt->gauge == newtonian)\n        ppw->rho_plus_p_theta = ppw->rho_plus_p_theta + ppw->pvecback[pba->index_bg_rho_cdm]*y[ppw->pv->index_pt_theta_cdm]; // contribution to total perturbed stress-energy\n\n      ppw->rho_plus_p_tot += ppw->pvecback[pba->index_bg_rho_cdm];\n\n      if (ppt->has_source_delta_m == _TRUE_) {\n        delta_rho_m += ppw->pvecback[pba->index_bg_rho_cdm]*y[ppw->pv->index_pt_delta_cdm]; // contribution to delta rho_matter\n        rho_m += ppw->pvecback[pba->index_bg_rho_cdm];\n      }\n      if ((ppt->has_source_delta_m == _TRUE_) || (ppt->has_source_theta_m == _TRUE_)) {\n        if (ppt->gauge == newtonian)\n          rho_plus_p_theta_m += ppw->pvecback[pba->index_bg_rho_cdm]*y[ppw->pv->index_pt_theta_cdm]; // contribution to [(rho+p)theta]_matter\n        rho_plus_p_m += ppw->pvecback[pba->index_bg_rho_cdm];\n      }\n    }\n'''
    new_stress='''    /* cdm contribution, promoted to the AeST effective fluid when enabled */\n    if (pba->has_cdm == _TRUE_) {\n      double rho_dark = ppw->pvecback[pba->index_bg_rho_cdm];\n      double rho_plus_p_dark = rho_dark;\n      double Pi_aest = 0.;\n      if (pba->aest_enabled == _TRUE_) {\n        double p_aest = ppw->pvecback[pba->index_bg_p_aest];\n        double cad2_aest = ppw->pvecback[pba->index_bg_cad2_aest];\n        double Q_aest = ppw->pvecback[pba->index_bg_Q_aest];\n        double theta_potential = a*y[ppw->pv->index_pt_theta_cdm]/k2;\n        double chi_aest = Q_aest*(theta_potential+y[ppw->pv->index_pt_alpha_aest]);\n        rho_plus_p_dark = rho_dark+p_aest;\n        Pi_aest = cad2_aest*y[ppw->pv->index_pt_delta_cdm]\n          +cad2_aest*k2/(3.*a2*rho_dark)\n          *(pba->aest_KB*y[ppw->pv->index_pt_E_aest]+(2.-pba->aest_KB)*chi_aest);\n      }\n\n      ppw->delta_rho += rho_dark*y[ppw->pv->index_pt_delta_cdm];\n      if (ppt->gauge == newtonian)\n        ppw->rho_plus_p_theta += rho_plus_p_dark*y[ppw->pv->index_pt_theta_cdm];\n      ppw->rho_plus_p_tot += rho_plus_p_dark;\n      if (pba->aest_enabled == _TRUE_)\n        ppw->delta_p += rho_dark*Pi_aest;\n\n      if (ppt->has_source_delta_m == _TRUE_) {\n        delta_rho_m += rho_dark*y[ppw->pv->index_pt_delta_cdm];\n        rho_m += rho_dark;\n      }\n      if ((ppt->has_source_delta_m == _TRUE_) || (ppt->has_source_theta_m == _TRUE_)) {\n        if (ppt->gauge == newtonian)\n          rho_plus_p_theta_m += rho_plus_p_dark*y[ppw->pv->index_pt_theta_cdm];\n        rho_plus_p_m += rho_plus_p_dark;\n      }\n    }\n'''
    replace_once(root/'source'/'perturbations.c',old_stress,new_stress,'AeST stress energy')

    old_deriv='''    /** - ---> cdm */\n\n    if (pba->has_cdm == _TRUE_) {\n\n      /** - ----> newtonian gauge: cdm density and velocity */\n\n      if (ppt->gauge == newtonian) {\n        dy[pv->index_pt_delta_cdm] = -(y[pv->index_pt_theta_cdm]+metric_continuity); /* cdm density */\n\n        dy[pv->index_pt_theta_cdm] = - a_prime_over_a*y[pv->index_pt_theta_cdm] + metric_euler; /* cdm velocity */\n      }\n\n      /** - ----> synchronous gauge: cdm density only (velocity set to zero by definition of the gauge) */\n\n      if (ppt->gauge == synchronous) {\n        dy[pv->index_pt_delta_cdm] = -metric_continuity; /* cdm density */\n      }\n    }\n'''
    new_deriv='''    /** - ---> cdm / AeST effective dark component */\n\n    if (pba->has_cdm == _TRUE_) {\n\n      if (pba->aest_enabled == _TRUE_) {\n        double rho_aest = pvecback[pba->index_bg_rho_cdm];\n        double w_aest = pvecback[pba->index_bg_w_aest];\n        double cad2_aest = pvecback[pba->index_bg_cad2_aest];\n        double Q_aest = pvecback[pba->index_bg_Q_aest];\n        double KQ_aest = pvecback[pba->index_bg_KQ_aest];\n        double theta_div_aest = y[pv->index_pt_theta_cdm];\n        double theta_potential_aest = a*theta_div_aest/k2;\n        double alpha_aest = y[pv->index_pt_alpha_aest];\n        double E_aest = y[pv->index_pt_E_aest];\n        double chi_aest = Q_aest*(theta_potential_aest+alpha_aest);\n        double Pi_aest = cad2_aest*y[pv->index_pt_delta_cdm]\n          +cad2_aest*k2/(3.*a*a*rho_aest)\n          *(pba->aest_KB*E_aest+(2.-pba->aest_KB)*chi_aest);\n        double psi_aest = metric_euler/k2;\n        double H_aest = pvecback[pba->index_bg_H];\n        double E_rhs_aest;\n\n        dy[pv->index_pt_delta_cdm] =\n          3.*a_prime_over_a*(w_aest*y[pv->index_pt_delta_cdm]-Pi_aest)\n          -(1.+w_aest)*(theta_div_aest+metric_continuity);\n\n        dy[pv->index_pt_theta_cdm] =\n          (3.*cad2_aest-1.)*a_prime_over_a*theta_div_aest\n          +k2*Pi_aest/(1.+w_aest)+metric_euler;\n\n        dy[pv->index_pt_alpha_aest] = a*(E_aest-psi_aest);\n\n        E_rhs_aest = KQ_aest*chi_aest\n          -(2.-pba->aest_KB)*(Q_aest*Pi_aest/(1.+w_aest)\n                              +(H_aest+Q_aest)*chi_aest\n                              -3.*cad2_aest*H_aest*Q_aest*alpha_aest);\n        dy[pv->index_pt_E_aest] = a*E_rhs_aest/pba->aest_KB-a_prime_over_a*E_aest;\n      }\n      else {\n        if (ppt->gauge == newtonian) {\n          dy[pv->index_pt_delta_cdm] = -(y[pv->index_pt_theta_cdm]+metric_continuity);\n          dy[pv->index_pt_theta_cdm] = -a_prime_over_a*y[pv->index_pt_theta_cdm]+metric_euler;\n        }\n        if (ppt->gauge == synchronous)\n          dy[pv->index_pt_delta_cdm] = -metric_continuity;\n      }\n    }\n'''
    replace_once(root/'source'/'perturbations.c',old_deriv,new_deriv,'AeST derivatives')

    report={
      'target_version':TARGET_VERSION,
      'target_sha':TARGET_SHA,
      'physics_path_modified':True,
      'aest_eta':0.0,
      'cdm_slot_reused_for_aest_effective_component':True,
      'new_states':['alpha_aest','E_aest'],
      'initial_condition_proxy':'chi_i=0, E_i=0',
      'gauge':'newtonian only'
    }
    (here.parent/'results').mkdir(exist_ok=True)
    (here.parent/'results'/'apply_patch_v019_report.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))

if __name__=='__main__':
    main()
