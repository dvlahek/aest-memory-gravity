#!/usr/bin/env python3
from pathlib import Path
import argparse
import json


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
    src = root / 'source' / 'aest_memory.c'

    old = r'''void aest_offline_trace_state(double k,double tau,double a,double H,double H0,
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

    new = r'''void aest_offline_trace_state(double k,double tau,double a,double H,double H0,
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

    replace_once(src, old, new, 'v072 multi-instance offline trace reload')

    txt = src.read_text()
    checks = {
        'runtime_path_refresh': 'strcmp(active_path,path) != 0' in txt,
        'old_permanent_disable_removed': 'if (disabled) return;' not in txt,
        'flush_after_trace_write': 'k,tau,a,H/H0,chi,Q);\n  fflush(fp);' in txt,
        'trace_formula_unchanged': 'k,tau,a,H/H0,chi,Q' in txt,
    }
    report = {
        'classification': 'V072_OFFLINE_TRACE_MULTI_INSTANCE_TECHNICAL_FIX',
        'physics_modified': False,
        'solver_tolerances_modified': False,
        'purpose': 'Allow successive Class instances in one Python process to write accepted-source-grid traces to different requested diagnostic files.',
        'checks': checks,
    }
    if not all(checks.values()):
        raise RuntimeError(report)
    (repo / 'results').mkdir(exist_ok=True)
    (repo / 'results' / 'v072_trace_reload_patch.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
