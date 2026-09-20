#!/usr/bin/env python3
"""GE09 diagnostic-only successful-NDF15-step state/RHS trace patch."""

from pathlib import Path
import argparse, json


def replace_once(path,old,new,label):
    p=Path(path)
    s=p.read_text()
    n=s.count(old)
    if n!=1:
        raise RuntimeError(f"{label}: expected one anchor, found {n}")
    p.write_text(s.replace(old,new,1))


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("class_root")
    args=ap.parse_args()
    root=Path(args.class_root).resolve()
    repo=Path(__file__).resolve().parents[1]

    src=root/"source"/"aest_memory.c"
    hdr=root/"include"/"aest_memory.h"
    pert=root/"source"/"perturbations.c"

    helper=r'''

/* GE09 diagnostic-only successful-step state/RHS trace. */
void aest_dense_jet_trace(
    double k,double tau,double a,double H,double H0,double Q,
    double rho_dark,double p_dark,double cad2_dark,
    double phi,double psi,double phi_prime,
    double delta_dark,double delta_dark_prime,
    double theta_dark,double theta_dark_prime,
    double alpha_aest,double alpha_prime,
    double E_aest,double E_aest_prime) {
  static FILE *fp = NULL;
  static char active_path[4096] = "";
  const char *path = getenv("AEST_DENSE_JET_TRACE_FILE");
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
    fp=fopen(path,"w");
    if (fp == NULL) {
      fprintf(stderr,"AEST_DENSE_JET_TRACE_OPEN_FAILED %s\n",path);
      active_path[0]='\0';
      return;
    }
    snprintf(active_path,sizeof(active_path),"%s",path);
    fprintf(fp,
      "k tau a H_over_H0 Q rho_dark p_dark cad2_dark "
      "phi psi phi_prime "
      "delta_dark delta_dark_prime theta_dark theta_dark_prime "
      "alpha_aest alpha_prime E_aest E_aest_prime\n");
    fflush(fp);
  }
  fprintf(fp,
    "%.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g "
    "%.17g %.17g %.17g "
    "%.17g %.17g %.17g %.17g "
    "%.17g %.17g %.17g %.17g\n",
    k,tau,a,H/H0,Q,rho_dark,p_dark,cad2_dark,
    phi,psi,phi_prime,
    delta_dark,delta_dark_prime,theta_dark,theta_dark_prime,
    alpha_aest,alpha_prime,E_aest,E_aest_prime);
  fflush(fp);
}
'''
    st=src.read_text()
    marker="/* GE09 diagnostic-only successful-step state/RHS trace. */"
    if marker not in st:
        src.write_text(st+helper)

    proto=r'''
void aest_dense_jet_trace(
    double k,double tau,double a,double H,double H0,double Q,
    double rho_dark,double p_dark,double cad2_dark,
    double phi,double psi,double phi_prime,
    double delta_dark,double delta_dark_prime,
    double theta_dark,double theta_dark_prime,
    double alpha_aest,double alpha_prime,
    double E_aest,double E_aest_prime);
'''
    hs=hdr.read_text()
    if "aest_dense_jet_trace(" not in hs:
        anchor="\n#ifdef __cplusplus\n}\n#endif\n"
        if anchor not in hs:
            raise RuntimeError("aest_memory.h extern-C anchor missing")
        hdr.write_text(hs.replace(anchor,"\n"+proto+anchor,1))

    old='''  a = pvecback[pba->index_bg_a];
  a2 = a*a;
  H = pvecback[pba->index_bg_H];

  if (pba->has_ncdm == _TRUE_){
'''
    new='''  a = pvecback[pba->index_bg_a];
  a2 = a*a;
  H = pvecback[pba->index_bg_H];

  /* GE09: perturbations_print_variables() is called by NDF15 only after
     a fresh perturbations_derivs(tnew,ynew,dy) at each successful step
     endpoint. Therefore dy here is the physical RHS, unlike interpolated
     dy passed to perturbations_sources() at overshot source times. */
  if ((pba->aest_enabled == _TRUE_) &&
      (index_md == ppt->index_md_scalars) &&
      (ppt->gauge == newtonian)) {
    aest_dense_jet_trace(
      k,tau,a,H,pba->H0,
      pvecback[pba->index_bg_Q_aest],
      pvecback[pba->index_bg_rho_cdm],
      pvecback[pba->index_bg_p_aest],
      pvecback[pba->index_bg_cad2_aest],
      y[ppw->pv->index_pt_phi],
      pvecmetric[ppw->index_mt_psi],
      dy[ppw->pv->index_pt_phi],
      y[ppw->pv->index_pt_delta_cdm],
      dy[ppw->pv->index_pt_delta_cdm],
      y[ppw->pv->index_pt_theta_cdm],
      dy[ppw->pv->index_pt_theta_cdm],
      y[ppw->pv->index_pt_alpha_aest],
      dy[ppw->pv->index_pt_alpha_aest],
      y[ppw->pv->index_pt_E_aest],
      dy[ppw->pv->index_pt_E_aest]);
  }

  if (pba->has_ncdm == _TRUE_){
'''
    replace_once(pert,old,new,"GE09 successful-step trace")

    ptxt=pert.read_text()
    atxt=src.read_text()
    ndf=(root/"tools"/"evolver_ndf15.c").read_text()
    checks={
        "hook_in_print_variables":"GE09: perturbations_print_variables()" in ptxt,
        "runtime_trace_path":"AEST_DENSE_JET_TRACE_FILE" in atxt,
        "fresh_derivs_before_print_variables":(
            "(*derivs)(tnew," in ndf
            and "(*print_variables)(tnew,ynew+1,f0+1" in ndf
        ),
        "parent_source_trace_preserved":"aest_full_state_trace(" in ptxt,
        "legacy_chi_trace_preserved":"aest_offline_trace_state(" in ptxt,
        "physical_memory_closure_preserved":"E_rhs_aest -= 0.5*Q_aest*Bchi_aest" in ptxt,
    }
    if not all(checks.values()):
        raise RuntimeError(checks)
    report={
        "classification":"GE09_DENSE_ACCEPTED_STEP_TRACE_PATCH_PASS",
        "physics_modified":False,
        "solver_tolerances_modified":False,
        "trace_semantics":"successful NDF15 step endpoints through perturbations_print_variables after explicit fresh perturbations_derivs",
        "checks":checks,
    }
    (repo/"results").mkdir(exist_ok=True)
    (repo/"results"/"ge09_dense_accepted_step_trace_patch.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))


if __name__=="__main__":
    main()
