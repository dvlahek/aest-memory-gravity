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

    # File I/O helper. Unlike v0.19r, record every CLASS k used by the
    # perturbation integration, because the resulting force table will be fed
    # back to CLASS on the same k grid.
    replace_once(
        root/'source'/'aest_memory.c',
        '#include <math.h>\n#include <stddef.h>\n#include <stdio.h>\n#include <stdlib.h>\n#include <string.h>\n#include "aest_memory.h"\n',
        '#include <math.h>\n#include <stddef.h>\n#include <stdio.h>\n#include <stdlib.h>\n#include <string.h>\n#include "aest_memory.h"\n',
        'offline helper includes')

    src = root/'source'/'aest_memory.c'
    s = src.read_text()
    marker = '/* AeST v0.22 eta0 source trace for offline Drude continuum */'
    if marker not in s:
        helper = r'''

/* AeST v0.22 eta0 source trace for offline Drude continuum */
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

    # Trace the same eta=0 AeST chi_A and Q_A that enter the memory closure.
    replace_once(
        root/'source'/'perturbations.c',
        '''        double H_aest = pvecback[pba->index_bg_H];\n        double E_rhs_aest;\n''',
        '''        double H_aest = pvecback[pba->index_bg_H];\n        double E_rhs_aest;\n        aest_offline_trace_state(k,tau,a,H_aest,pba->H0,chi_aest,Q_aest);\n''',
        'offline trace call')

    ptxt = (root/'source'/'perturbations.c').read_text()
    atxt = (root/'source'/'aest_memory.c').read_text()
    checks = {
        'trace_call_on_AeST_derivative_grid': 'aest_offline_trace_state(k,tau,a,H_aest,pba->H0,chi_aest,Q_aest)' in ptxt,
        'runtime_trace_path': 'AEST_OFFLINE_TRACE_FILE' in atxt,
        'eta0_chi_definition_preserved': 'chi_aest = Q_aest*(theta_potential_aest+alpha_aest)' in ptxt,
        'physical_memory_closure_preserved': 'E_rhs_aest -= 0.5*Q_aest*Bchi_aest' in ptxt,
    }
    report = {
        'classification': 'V022_ETA0_NATIVE_K_TRACE',
        'purpose': 'trace eta=0 AeST source once; evaluate Drude continuum offline; feed only variational forcing back to CLASS',
        'fields': ['k','tau','a','H_over_H0','chi','Q'],
        'checks': checks,
    }
    if not all(checks.values()):
        raise RuntimeError(report)
    (repo/'results').mkdir(exist_ok=True)
    (repo/'results'/'v022_trace_patch.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    main()
