#!/usr/bin/env python3
from pathlib import Path
import argparse,json


def replace_once(path,old,new,label):
    p=Path(path);s=p.read_text();n=s.count(old)
    if n!=1: raise RuntimeError(f'{label}: expected one anchor, found {n} in {p}')
    p.write_text(s.replace(old,new,1))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('class_root');args=ap.parse_args()
    root=Path(args.class_root).resolve();repo=Path(__file__).resolve().parents[1]

    replace_once(root/'source'/'aest_memory.c',
'''#include <math.h>\n#include <stddef.h>\n#include "aest_memory.h"\n''',
'''#include <math.h>\n#include <stddef.h>\n#include <stdio.h>\n#include <stdlib.h>\n#include "aest_memory.h"\n''','trace helper includes')

    # Append a test-only tracer. It is inactive unless AEST_TRACE_FILE is defined.
    p=root/'source'/'aest_memory.c';s=p.read_text()
    helper=r'''

void aest_memory_trace_point(double k,double a,double H,double H0,
                             double chi,double alpha,double E,
                             double theta_div,double Q) {
  static FILE *fp = NULL;
  static int disabled = 0;
  static const double targets[] = {1.e-4,3.e-4,1.e-3,3.e-3,1.e-2,3.e-2,1.e-1,3.e-1};
  const char *path;
  int j,best=-1;
  double bestrel=1.e99;
  if (disabled) return;
  path=getenv("AEST_TRACE_FILE");
  if (path == NULL) { disabled=1; return; }
  for (j=0;j<8;j++) {
    double rel=fabs(k-targets[j])/targets[j];
    if (rel < bestrel) { bestrel=rel; best=j; }
  }
  if ((best < 0) || (bestrel > 5.e-4)) return;
  if (fp == NULL) {
    fp=fopen(path,"w");
    if (fp == NULL) { disabled=1; return; }
    fprintf(fp,"target_k,k,a,H_over_H0,k_over_aH,chi,alpha,E,theta_div,Q\n");
  }
  fprintf(fp,"%.17g,%.17g,%.17g,%.17g,%.17g,%.17g,%.17g,%.17g,%.17g,%.17g\n",
          targets[best],k,a,H/H0,k/(a*H),chi,alpha,E,theta_div,Q);
}
'''
    if 'void aest_memory_trace_point(' not in s:
        p.write_text(s+helper)

    hp=root/'include'/'aest_memory.h';hs=hp.read_text()
    proto='''\nvoid aest_memory_trace_point(double k,double a,double H,double H0,\n                             double chi,double alpha,double E,\n                             double theta_div,double Q);\n'''
    if 'aest_memory_trace_point' not in hs:
        hs=hs.replace('\n#ifdef __cplusplus\n}\n#endif\n',proto+'\n#ifdef __cplusplus\n}\n#endif\n')
        hp.write_text(hs)

    replace_once(root/'source'/'perturbations.c',
'''        double H_aest = pvecback[pba->index_bg_H];\n        double E_rhs_aest;\n''',
'''        double H_aest = pvecback[pba->index_bg_H];\n        double E_rhs_aest;\n        aest_memory_trace_point(k,a,H_aest,pba->H0,chi_aest,alpha_aest,E_aest,theta_div_aest,Q_aest);\n''','trace call in AeST derivative block')

    txt=(root/'source'/'perturbations.c').read_text()
    checks={
      'trace_call':'aest_memory_trace_point(k,a,H_aest,pba->H0' in txt,
      'memory_not_enabled':'aest_eta' not in txt,
      'eta0_AeST_active':'chi_aest = Q_aest*(theta_potential_aest+alpha_aest)' in txt,
    }
    report={'classification':'ETA0_CLASS_CHI_TRACE_PATCH','test_only':True,'source_audit':checks}
    if not all(checks.values()): raise RuntimeError(report)
    (repo/'results').mkdir(exist_ok=True)
    (repo/'results'/'v019q_trace_patch.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
