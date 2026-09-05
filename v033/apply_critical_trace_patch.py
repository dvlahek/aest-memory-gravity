#!/usr/bin/env python3
from pathlib import Path
import argparse, json


def replace_once(path, old, new, label):
    p=Path(path); s=p.read_text(); n=s.count(old)
    if n != 1:
        raise RuntimeError(f'{label}: expected one anchor, found {n} in {p}')
    p.write_text(s.replace(old,new,1))


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('class_root'); z=ap.parse_args()
    root=Path(z.class_root).resolve(); repo=Path(__file__).resolve().parents[1]
    src=root/'source'/'aest_memory.c'; hp=root/'include'/'aest_memory.h'

    s=src.read_text()
    marker='/* AeST v0.33 intrinsic critical-mode trace */'
    if marker not in s:
        helper=r'''

/* AeST v0.33 intrinsic critical-mode trace */
void aest_critical_trace_state(double k,double tau,double a,double H,double H0,
                               double rho,double w,double cad2,double Q,double KQ,
                               double delta,double theta,double alpha,double E) {
  static FILE *fp=NULL;
  static int disabled=0;
  const char *path;
  if (disabled) return;
  path=getenv("AEST_CRITICAL_TRACE_FILE");
  if (path==NULL || path[0]=='\0') { disabled=1; return; }
  if (fp==NULL) {
    fp=fopen(path,"w");
    if (fp==NULL) {
      fprintf(stderr,"AEST_CRITICAL_TRACE_OPEN_FAILED %s\n",path);
      disabled=1; return;
    }
    fprintf(fp,"k tau a H H0 rho w cad2 Q KQ delta theta alpha E\n");
  }
  fprintf(fp,"%.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g %.17g\n",
          k,tau,a,H,H0,rho,w,cad2,Q,KQ,delta,theta,alpha,E);
}
'''
        src.write_text(s+helper)

    hs=hp.read_text()
    proto='''\nvoid aest_critical_trace_state(double k,double tau,double a,double H,double H0,\n                               double rho,double w,double cad2,double Q,double KQ,\n                               double delta,double theta,double alpha,double E);\n'''
    if 'aest_critical_trace_state' not in hs:
        anchor='\n#ifdef __cplusplus\n}\n#endif\n'
        if anchor not in hs: raise RuntimeError('aest_memory.h extern-C anchor not found')
        hp.write_text(hs.replace(anchor,proto+anchor,1))

    old='''    aest_offline_trace_state(k,tau,a,pvecback[pba->index_bg_H],pba->H0,\n                             chi_trace,Q_trace);\n'''
    new='''    aest_offline_trace_state(k,tau,a,pvecback[pba->index_bg_H],pba->H0,\n                             chi_trace,Q_trace);\n    aest_critical_trace_state(k,tau,a,pvecback[pba->index_bg_H],pba->H0,\n                              pvecback[pba->index_bg_rho_cdm],\n                              pvecback[pba->index_bg_w_aest],\n                              pvecback[pba->index_bg_cad2_aest],\n                              Q_trace,pvecback[pba->index_bg_KQ_aest],\n                              y[ppw->pv->index_pt_delta_cdm],theta_trace,alpha_trace,\n                              y[ppw->pv->index_pt_E_aest]);\n'''
    replace_once(root/'source'/'perturbations.c',old,new,'accepted-grid critical trace call')

    checks={
      'accepted_grid_call':'aest_critical_trace_state(k,tau,a,pvecback[pba->index_bg_H],pba->H0' in (root/'source'/'perturbations.c').read_text(),
      'runtime_path':'AEST_CRITICAL_TRACE_FILE' in src.read_text(),
      'rho_traced':'index_bg_rho_cdm' in (root/'source'/'perturbations.c').read_text(),
      'KQ_traced':'index_bg_KQ_aest' in (root/'source'/'perturbations.c').read_text(),
      'states_traced':'index_pt_E_aest' in (root/'source'/'perturbations.c').read_text(),
    }
    report={'classification':'V033_ACCEPTED_GRID_CRITICAL_MODE_TRACE',
            'fields':['k','tau','a','H','H0','rho','w','cad2','Q','KQ','delta','theta','alpha','E'],
            'purpose':'reconstruct the frozen-coefficient intrinsic AeST scalar perturbation block and diagnose the KB->0 singular-perturbation structure',
            'checks':checks}
    if not all(checks.values()): raise RuntimeError(report)
    (repo/'results').mkdir(exist_ok=True)
    (repo/'results'/'v033_trace_patch.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))

if __name__=='__main__': main()
