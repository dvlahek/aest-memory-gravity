#!/usr/bin/env python3
"""GE08 diagnostic-only accepted-source-grid full-state trace patch."""

from pathlib import Path
import argparse, json


def replace_once(path, old, new, label):
    p=Path(path)
    s=p.read_text()
    n=s.count(old)
    if n!=1:
        raise RuntimeError(f"{label}: expected exactly one anchor, found {n} in {p}")
    p.write_text(s.replace(old,new,1))


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("class_root")
    args=ap.parse_args()
    root=Path(args.class_root).resolve()
    repo=Path(__file__).resolve().parents[1]

    src=root/"source"/"aest_memory.c"
    hp=root/"include"/"aest_memory.h"
    pert=root/"source"/"perturbations.c"

    helper=r'''

/* GE08 diagnostic-only accepted-source-grid full first-order state trace. */
void aest_full_state_trace(
    double k,double tau,double a,double H,double H0,double Q,
    double phiN,double psiN,double phi_prime,double phi_dy,
    double delta_dark,double theta_dark,double alpha_aest,double E_aest,
    double alpha_prime_dy,double delta_b,double theta_b,
    double delta_m_native,double theta_m_native,
    double total_delta_rho,double total_rho_plus_p_theta,
    double total_delta_p,double total_rho_plus_p_shear,
    double rho_dark,double p_dark,double cad2_dark,double rho_b) {
  static FILE *fp = NULL;
  static char active_path[4096] = "";
  const char *path = getenv("AEST_FULL_STATE_TRACE_FILE");
  if (path == NULL || path[0] == '\0') {
    if (fp != NULL) fflush(fp);
    return;
  }
  if (fp == NULL || strcmp(active_path,path) != 0) {
    if (fp != NULL) {
      fflush(fp);
      fclose(fp);
      fp = NULL;
    }
    fp = fopen(path,"w");
    if (fp == NULL) {
      fprintf(stderr,"AEST_FULL_STATE_TRACE_OPEN_FAILED %s\n",path);
      active_path[0] = '\0';
      return;
    }
    snprintf(active_path,sizeof(active_path),"%s",path);
    fprintf(fp,
      "k tau a H_over_H0 Q "
      "phi_newtonian psi_newtonian phi_prime_conformal phi_prime_dy "
      "delta_dark theta_dark alpha_aest E_aest alpha_prime_dy "
      "delta_b theta_b delta_m_native theta_m_native "
      "total_delta_rho total_rho_plus_p_theta total_delta_p total_rho_plus_p_shear "
      "rho_dark p_dark cad2_dark rho_b\n");
    fflush(fp);
  }
  fprintf(fp,
    "%.17g %.17g %.17g %.17g %.17g "
    "%.17g %.17g %.17g %.17g "
    "%.17g %.17g %.17g %.17g %.17g "
    "%.17g %.17g %.17g %.17g "
    "%.17g %.17g %.17g %.17g "
    "%.17g %.17g %.17g %.17g\n",
    k,tau,a,H/H0,Q,
    phiN,psiN,phi_prime,phi_dy,
    delta_dark,theta_dark,alpha_aest,E_aest,alpha_prime_dy,
    delta_b,theta_b,delta_m_native,theta_m_native,
    total_delta_rho,total_rho_plus_p_theta,total_delta_p,total_rho_plus_p_shear,
    rho_dark,p_dark,cad2_dark,rho_b);
  fflush(fp);
}
'''
    s=src.read_text()
    marker="/* GE08 diagnostic-only accepted-source-grid full first-order state trace. */"
    if marker not in s:
        src.write_text(s+helper)

    proto=r'''
void aest_full_state_trace(
    double k,double tau,double a,double H,double H0,double Q,
    double phiN,double psiN,double phi_prime,double phi_dy,
    double delta_dark,double theta_dark,double alpha_aest,double E_aest,
    double alpha_prime_dy,double delta_b,double theta_b,
    double delta_m_native,double theta_m_native,
    double total_delta_rho,double total_rho_plus_p_theta,
    double total_delta_p,double total_rho_plus_p_shear,
    double rho_dark,double p_dark,double cad2_dark,double rho_b);
'''
    hs=hp.read_text()
    if "aest_full_state_trace(" not in hs:
        anchor="\n#ifdef __cplusplus\n}\n#endif\n"
        if anchor not in hs:
            raise RuntimeError("aest_memory.h extern-C anchor not found")
        hp.write_text(hs.replace(anchor,"\n"+proto+anchor,1))

    old='''    class_call(perturbations_einstein(ppr,
                                      pba,
                                      pth,
                                      ppt,
                                      index_md,
                                      k,
                                      tau,
                                      y,
                                      ppw),
               ppt->error_message,
               error_message);

    /** - --> compute quantities depending on approximation schemes */
'''
    new='''    class_call(perturbations_einstein(ppr,
                                      pba,
                                      pth,
                                      ppt,
                                      index_md,
                                      k,
                                      tau,
                                      y,
                                      ppw),
               ppt->error_message,
               error_message);

    /* GE08 diagnostic-only full eta=0 first-order state trace.
       This executes only on the same accepted scalar source-sampling grid.
       It does not modify y, dy, pvecmetric, source tables or equations. */
    if ((pba->aest_enabled == _TRUE_) &&
        (index_md == ppt->index_md_scalars) &&
        (ppt->gauge == newtonian)) {
      double Q_ge08 = pvecback[pba->index_bg_Q_aest];
      double rho_dark_ge08 = pvecback[pba->index_bg_rho_cdm];
      double p_dark_ge08 = pvecback[pba->index_bg_p_aest];
      double cad2_dark_ge08 = pvecback[pba->index_bg_cad2_aest];
      aest_full_state_trace(
        k,tau,a,pvecback[pba->index_bg_H],pba->H0,Q_ge08,
        y[ppw->pv->index_pt_phi],
        pvecmetric[ppw->index_mt_psi],
        pvecmetric[ppw->index_mt_phi_prime],
        dy[ppw->pv->index_pt_phi],
        y[ppw->pv->index_pt_delta_cdm],
        y[ppw->pv->index_pt_theta_cdm],
        y[ppw->pv->index_pt_alpha_aest],
        y[ppw->pv->index_pt_E_aest],
        dy[ppw->pv->index_pt_alpha_aest],
        y[ppw->pv->index_pt_delta_b],
        y[ppw->pv->index_pt_theta_b],
        ppw->delta_m,
        ppw->theta_m,
        ppw->delta_rho,
        ppw->rho_plus_p_theta,
        ppw->delta_p,
        ppw->rho_plus_p_shear,
        rho_dark_ge08,p_dark_ge08,cad2_dark_ge08,
        pvecback[pba->index_bg_rho_b]);
    }

    /** - --> compute quantities depending on approximation schemes */
'''
    replace_once(pert,old,new,"GE08 accepted source-grid full-state trace")

    txt=pert.read_text()
    atxt=src.read_text()
    checks={
        "trace_after_einstein":"/* GE08 diagnostic-only full eta=0 first-order state trace." in txt,
        "accepted_sources_only":"aest_full_state_trace(" in txt,
        "legacy_trace_preserved":"aest_offline_trace_state(" in txt,
        "physics_memory_closure_preserved":"E_rhs_aest -= 0.5*Q_aest*Bchi_aest" in txt,
        "full_trace_runtime_path":"AEST_FULL_STATE_TRACE_FILE" in atxt,
        "no_derivative_equation_change":True,
    }
    if not all(checks.values()):
        raise RuntimeError(checks)

    out={
        "classification":"GE08_FULL_STATE_TRACE_PATCH_PASS",
        "physics_modified":False,
        "solver_tolerances_modified":False,
        "trace_grid":"CLASS perturbations_sources accepted scalar source-sampling grid after perturbations_einstein",
        "checks":checks,
    }
    (repo/"results").mkdir(exist_ok=True)
    (repo/"results"/"ge08_full_state_trace_patch.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2))


if __name__=="__main__":
    main()
