#!/usr/bin/env python3
from pathlib import Path
import argparse, json


def replace_once(path, old, new, label):
    p=Path(path); s=p.read_text(); n=s.count(old)
    if n != 1:
        raise RuntimeError(f'{label}: expected exactly one post-v0.72 trace anchor, found {n} in {p}')
    p.write_text(s.replace(old,new,1))


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('class_root'); args=ap.parse_args()
    root=Path(args.class_root).resolve(); repo=Path(__file__).resolve().parents[1]

    hp=root/'include'/'aest_memory.h'
    src=root/'source'/'aest_memory.c'
    pert=root/'source'/'perturbations.c'

    old_proto='''void aest_offline_trace_state(double k,double tau,double a,double H,double H0,\n                              double chi,double Q);\n'''
    new_proto='''void aest_offline_trace_state(double k,double tau,double a,double H,double H0,\n                              double chi,double Q,double rhoA,double KQ,double KQQ,\n                              double delta_b,double theta_b,double delta_A,double theta_A,\n                              double alpha_A,double E_A,double Phi,double Phi_prime,double Psi);\n'''
    replace_once(hp,old_proto,new_proto,'trace prototype')

    # Repair01: the validated stack applies v0.72 before C7A. Anchor to the
    # post-v0.72 helper and preserve all runtime path reload/flush semantics.
    old_helper=r'''void aest_offline_trace_state(double k,double tau,double a,double H,double H0,
                              double chi,double Q) {
  static FILE *fp = NULL;
  static char active_path[4096] = "";
  const char *path;
  path = getenv("AEST_OFFLINE_TRACE_FILE");
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
      fprintf(stderr,"AEST_OFFLINE_TRACE_OPEN_FAILED %s\n",path);
      active_path[0] = '\0';
      return;
    }
    snprintf(active_path,sizeof(active_path),"%s",path);
    fprintf(fp,"k tau a H_over_H0 chi Q\n");
    fflush(fp);
  }
  fprintf(fp,"%.17g %.17g %.17g %.17g %.17g %.17g\n",
          k,tau,a,H/H0,chi,Q);
  fflush(fp);
}
'''
    new_helper=r'''void aest_offline_trace_state(double k,double tau,double a,double H,double H0,
                              double chi,double Q,double rhoA,double KQ,double KQQ,
                              double delta_b,double theta_b,double delta_A,double theta_A,
                              double alpha_A,double E_A,double Phi,double Phi_prime,double Psi) {
  static FILE *fp = NULL;
  static char active_path[4096] = "";
  const char *path;
  path = getenv("AEST_OFFLINE_TRACE_FILE");
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
      fprintf(stderr,"AEST_OFFLINE_TRACE_OPEN_FAILED %s\n",path);
      active_path[0] = '\0';
      return;
    }
    snprintf(active_path,sizeof(active_path),"%s",path);
    fprintf(fp,"k tau a H_Mpc_inv H_over_H0 chi Q rhoA KQ KQQ delta_b theta_b delta_A theta_A alpha_A E_A Phi Phi_prime Psi\n");
    fflush(fp);
  }
  fprintf(fp,"%.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g\n",
          k,tau,a,H,H/H0,chi,Q,rhoA,KQ,KQQ,delta_b,theta_b,delta_A,theta_A,alpha_A,E_A,Phi,Phi_prime,Psi);
  fflush(fp);
}
'''
    replace_once(src,old_helper,new_helper,'trace helper')

    old_call='''  if ((pba->aest_enabled == _TRUE_) &&\n      (index_md == ppt->index_md_scalars)) {\n    double Q_trace = pvecback[pba->index_bg_Q_aest];\n    double theta_trace = y[ppw->pv->index_pt_theta_cdm];\n    double alpha_trace = y[ppw->pv->index_pt_alpha_aest];\n    double chi_trace = Q_trace*(a*theta_trace/(k*k)+alpha_trace);\n    aest_offline_trace_state(k,tau,a,pvecback[pba->index_bg_H],pba->H0,\n                             chi_trace,Q_trace);\n  }\n'''
    new_call='''  if ((pba->aest_enabled == _TRUE_) &&\n      (index_md == ppt->index_md_scalars)) {\n    double Q_trace = pvecback[pba->index_bg_Q_aest];\n    double theta_trace = y[ppw->pv->index_pt_theta_cdm];\n    double alpha_trace = y[ppw->pv->index_pt_alpha_aest];\n    double chi_trace = Q_trace*(a*theta_trace/(k*k)+alpha_trace);\n    double rhoA_trace = pvecback[pba->index_bg_rho_cdm];\n    double KQ_trace = pvecback[pba->index_bg_KQ_aest];\n    double cad2_trace = pvecback[pba->index_bg_cad2_aest];\n    double KQQ_trace = KQ_trace/(Q_trace*cad2_trace);\n    aest_offline_trace_state(k,tau,a,pvecback[pba->index_bg_H],pba->H0,\n                             chi_trace,Q_trace,rhoA_trace,KQ_trace,KQQ_trace,\n                             y[ppw->pv->index_pt_delta_b],y[ppw->pv->index_pt_theta_b],\n                             y[ppw->pv->index_pt_delta_cdm],y[ppw->pv->index_pt_theta_cdm],\n                             alpha_trace,y[ppw->pv->index_pt_E_aest],\n                             y[ppw->pv->index_pt_phi],ppw->pvecmetric[ppt->index_mt_phi_prime],\n                             ppw->pvecmetric[ppt->index_mt_psi]);\n  }\n'''
    replace_once(pert,old_call,new_call,'accepted source trace call')

    stxt=src.read_text(); ptxt=pert.read_text()
    helper_start=stxt.find('void aest_offline_trace_state(')
    helper_end=stxt.find('\n}\n',helper_start)
    helper=stxt[helper_start:helper_end+3]
    checks={
      'post_v072_runtime_path_refresh':'strcmp(active_path,path) != 0' in helper,
      'post_v072_no_permanent_disable':'disabled' not in helper,
      'post_v072_flush_retained':helper.count('fflush(fp);')>=3,
      'output_only_fields_present':all(x in helper for x in ['delta_b','theta_b','delta_A','theta_A','alpha_A','E_A','Phi','Phi_prime','Psi','KQQ']),
      'accepted_source_location_retained':'aest_offline_trace_state(k,tau,a,pvecback[pba->index_bg_H],pba->H0' in ptxt,
      'no_new_derivative_assignment':'NL1C7A' not in ''.join(line for line in ptxt.splitlines() if 'dy[' in line),
    }
    report={
      'classification':'NL1C7A_OUTPUT_ONLY_TRACE_EXTENSION_REPAIR01',
      'historical_technical_failure_run':35092490498,
      'repair':'anchor and replacement helper updated from original v0.23 form to post-v0.72 runtime-reload form; science gates unchanged',
      'fields':['k','tau','a','H_Mpc_inv','H_over_H0','chi','Q','rhoA','KQ','KQQ','delta_b','theta_b','delta_A','theta_A','alpha_A','E_A','Phi','Phi_prime','Psi'],
      'replacements':{'prototype':1,'helper':1,'accepted_source_call':1},
      'checks':checks,
    }
    if not all(checks.values()): raise RuntimeError(report)
    (repo/'results').mkdir(exist_ok=True)
    (repo/'results'/'nl1c7a_trace_extension_patch.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__': main()
