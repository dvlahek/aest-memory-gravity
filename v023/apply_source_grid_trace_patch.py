#!/usr/bin/env python3
from pathlib import Path
import argparse, json


def replace_once(path, old, new, label):
    p = Path(path)
    s = p.read_text()
    n = s.count(old)
    if n != 1:
        raise RuntimeError(f'{label}: expected one anchor, found {n} in {p}')
    p.write_text(s.replace(old, new, 1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('class_root')
    args = ap.parse_args()
    root = Path(args.class_root).resolve()
    repo = Path(__file__).resolve().parents[1]

    # v0.19w already adds stdio/stdlib/string includes to aest_memory.c.
    src = root/'source'/'aest_memory.c'
    s = src.read_text()
    marker = '/* AeST v0.23 eta0 accepted source-grid trace */'
    if marker not in s:
        helper = r'''

/* AeST v0.23 eta0 accepted source-grid trace */
void aest_offline_trace_state(double k,double tau,double a,double H,double H0,
                              double chi,double Q) {
  static FILE *fp = NULL;
  static int disabled = 0;
  const char *path;
  if (disabled) return;
  path = getenv("AEST_OFFLINE_TRACE_FILE");
  if (path == NULL || path[0] == '\0') { disabled = 1; return; }
  if (fp == NULL) {
    fp = fopen(path,"w");
    if (fp == NULL) {
      fprintf(stderr,"AEST_OFFLINE_TRACE_OPEN_FAILED %s\n",path);
      disabled = 1;
      return;
    }
    fprintf(fp,"k tau a H_over_H0 chi Q\n");
  }
  fprintf(fp,"%.17g %.17g %.17g %.17g %.17g %.17g\n",
          k,tau,a,H/H0,chi,Q);
}
'''
        src.write_text(s + helper)

    hp = root/'include'/'aest_memory.h'
    hs = hp.read_text()
    proto = '''\nvoid aest_offline_trace_state(double k,double tau,double a,double H,double H0,\n                              double chi,double Q);\n'''
    if 'aest_offline_trace_state' not in hs:
        anchor = '\n#ifdef __cplusplus\n}\n#endif\n'
        if anchor not in hs:
            raise RuntimeError('aest_memory.h extern-C anchor not found')
        hp.write_text(hs.replace(anchor, proto + anchor, 1))

    # IMPORTANT: trace in perturbations_sources(), not perturbations_derivs().
    # This is the accepted CLASS source-sampling grid used by the validated
    # v0.19w tangent trace. It excludes adaptive RK stage/rejected-step states.
    old = '''  a_prime_over_a = pvecback[pba->index_bg_a] * pvecback[pba->index_bg_H]; /* (a'/a)=aH */\n'''
    new = '''  if ((pba->aest_enabled == _TRUE_) &&\n      (index_md == ppt->index_md_scalars)) {\n    double Q_trace = pvecback[pba->index_bg_Q_aest];\n    double theta_trace = y[ppw->pv->index_pt_theta_cdm];\n    double alpha_trace = y[ppw->pv->index_pt_alpha_aest];\n    double chi_trace = Q_trace*(a*theta_trace/(k*k)+alpha_trace);\n    aest_offline_trace_state(k,tau,a,pvecback[pba->index_bg_H],pba->H0,\n                             chi_trace,Q_trace);\n  }\n\n  a_prime_over_a = pvecback[pba->index_bg_a] * pvecback[pba->index_bg_H]; /* (a'/a)=aH */\n'''
    replace_once(root/'source'/'perturbations.c', old, new, 'accepted source-grid trace')

    ptxt = (root/'source'/'perturbations.c').read_text()
    atxt = src.read_text()
    checks = {
        'source_grid_trace_call': 'aest_offline_trace_state(k,tau,a,pvecback[pba->index_bg_H],pba->H0' in ptxt,
        'runtime_trace_path': 'AEST_OFFLINE_TRACE_FILE' in atxt,
        'same_chi_as_v019w': 'Q_trace*(a*theta_trace/(k*k)+alpha_trace)' in ptxt,
        'physical_memory_closure_preserved': 'E_rhs_aest -= 0.5*Q_aest*Bchi_aest' in ptxt,
        'no_derivative_grid_trace': 'aest_offline_trace_state(k,tau,a,H_aest,pba->H0,chi_aest,Q_aest)' not in ptxt,
    }
    report = {
        'classification': 'V023_ETA0_ACCEPTED_SOURCE_GRID_TRACE',
        'purpose': 'remove adaptive derivative-stage contamination from offline Drude forcing reconstruction',
        'grid': 'CLASS perturbations_sources accepted source-sampling grid',
        'fields': ['k','tau','a','H_over_H0','chi','Q'],
        'checks': checks,
    }
    if not all(checks.values()):
        raise RuntimeError(report)
    (repo/'results').mkdir(exist_ok=True)
    (repo/'results'/'v023_trace_patch.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    main()
