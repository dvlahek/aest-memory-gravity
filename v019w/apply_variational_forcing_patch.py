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

    # Helper needs file I/O and environment access.
    replace_once(
        root/'source'/'aest_memory.c',
        '#include <math.h>\n#include <stddef.h>\n#include "aest_memory.h"\n',
        '#include <math.h>\n#include <stddef.h>\n#include <stdio.h>\n#include <stdlib.h>\n#include <string.h>\n#include "aest_memory.h"\n',
        'variational helper includes')

    hp = root/'include'/'aest_memory.h'
    hs = hp.read_text()
    proto = '''\nvoid aest_tangent_trace_force(double k,double tau,double force);\ndouble aest_tangent_external_force(double k,double tau);\n'''
    if 'aest_tangent_external_force' not in hs:
        anchor = '\n#ifdef __cplusplus\n}\n#endif\n'
        if anchor not in hs:
            raise RuntimeError('aest_memory.h extern-C anchor not found')
        hp.write_text(hs.replace(anchor, proto + anchor, 1))

    src = root/'source'/'aest_memory.c'
    s = src.read_text()
    marker = '/* AeST v0.19w variational tangent forcing helper */'
    if marker not in s:
        helper = r'''

/* AeST v0.19w variational tangent forcing helper */
static double *_aest_tf_k = NULL;
static double *_aest_tf_tau = NULL;
static double *_aest_tf_f = NULL;
static size_t _aest_tf_n = 0;
static int _aest_tf_loaded = 0;
static double _aest_tf_lambda = 0.;
static double _aest_tf_cache_k = -1.;
static size_t _aest_tf_cache_lo = 0;
static size_t _aest_tf_cache_hi = 0;

void aest_tangent_trace_force(double k,double tau,double force) {
  static FILE *fp = NULL;
  static int disabled = 0;
  const char *path;
  if (disabled) return;
  path = getenv("AEST_TANGENT_TRACE_FILE");
  if (path == NULL || path[0] == '\0') { disabled = 1; return; }
  if (fp == NULL) {
    fp = fopen(path,"w");
    if (fp == NULL) {
      fprintf(stderr,"AEST_TANGENT_TRACE_OPEN_FAILED %s\n",path);
      disabled = 1;
      return;
    }
  }
  fprintf(fp,"%.17g %.17g %.17g\n",k,tau,force);
}

static void _aest_tangent_load_force(void) {
  const char *path;
  const char *slam;
  FILE *fp;
  size_t cap = 0;
  double k,tau,f;
  if (_aest_tf_loaded) return;
  _aest_tf_loaded = 1;
  slam = getenv("AEST_TANGENT_LAMBDA");
  _aest_tf_lambda = (slam == NULL) ? 0. : strtod(slam,NULL);
  path = getenv("AEST_TANGENT_FORCE_FILE");
  if (path == NULL || path[0] == '\0' || _aest_tf_lambda == 0.) return;
  fp = fopen(path,"r");
  if (fp == NULL) {
    fprintf(stderr,"AEST_TANGENT_FORCE_OPEN_FAILED %s\n",path);
    exit(91);
  }
  while (fscanf(fp,"%lf %lf %lf",&k,&tau,&f) == 3) {
    if (_aest_tf_n == cap) {
      size_t ncap = (cap == 0) ? 65536 : 2*cap;
      double *nk = (double*)realloc(_aest_tf_k,ncap*sizeof(double));
      double *nt = (double*)realloc(_aest_tf_tau,ncap*sizeof(double));
      double *nf = (double*)realloc(_aest_tf_f,ncap*sizeof(double));
      if (nk == NULL || nt == NULL || nf == NULL) {
        fprintf(stderr,"AEST_TANGENT_FORCE_ALLOC_FAILED\n");
        exit(92);
      }
      _aest_tf_k = nk; _aest_tf_tau = nt; _aest_tf_f = nf; cap = ncap;
    }
    _aest_tf_k[_aest_tf_n] = k;
    _aest_tf_tau[_aest_tf_n] = tau;
    _aest_tf_f[_aest_tf_n] = f;
    _aest_tf_n++;
  }
  fclose(fp);
  if (_aest_tf_n < 2) {
    fprintf(stderr,"AEST_TANGENT_FORCE_TABLE_EMPTY %s\n",path);
    exit(93);
  }
}

static int _aest_tangent_select_k(double k) {
  size_t l,r,m,pos;
  double rel;
  if (_aest_tf_cache_hi > _aest_tf_cache_lo &&
      fabs(k-_aest_tf_cache_k) <= 1.e-13*(1.+fabs(k))) return 1;
  l = 0; r = _aest_tf_n;
  while (l < r) {
    m = l + (r-l)/2;
    if (_aest_tf_k[m] < k) l = m+1; else r = m;
  }
  pos = l;
  if (pos == _aest_tf_n) pos = _aest_tf_n-1;
  else if (pos > 0 && fabs(_aest_tf_k[pos-1]-k) < fabs(_aest_tf_k[pos]-k)) pos--;
  _aest_tf_cache_k = _aest_tf_k[pos];
  rel = fabs(_aest_tf_cache_k-k)/(fabs(k)+1.e-300);
  if (rel > 2.e-10) {
    fprintf(stderr,"AEST_TANGENT_FORCE_K_MISS query=%.17g nearest=%.17g rel=%.3e\n",
            k,_aest_tf_cache_k,rel);
    return 0;
  }
  _aest_tf_cache_lo = pos;
  while (_aest_tf_cache_lo > 0 && _aest_tf_k[_aest_tf_cache_lo-1] == _aest_tf_cache_k)
    _aest_tf_cache_lo--;
  _aest_tf_cache_hi = pos+1;
  while (_aest_tf_cache_hi < _aest_tf_n && _aest_tf_k[_aest_tf_cache_hi] == _aest_tf_cache_k)
    _aest_tf_cache_hi++;
  return (_aest_tf_cache_hi > _aest_tf_cache_lo);
}

double aest_tangent_external_force(double k,double tau) {
  size_t l,r,m;
  double t0,t1,f0,f1,x;
  _aest_tangent_load_force();
  if (_aest_tf_lambda == 0. || _aest_tf_n == 0) return 0.;
  if (!_aest_tangent_select_k(k)) exit(94);
  l = _aest_tf_cache_lo;
  r = _aest_tf_cache_hi;
  if (tau <= _aest_tf_tau[l]) return 0.;
  if (tau >= _aest_tf_tau[r-1]) return _aest_tf_lambda*_aest_tf_f[r-1];
  while (l+1 < r) {
    m = l + (r-l)/2;
    if (_aest_tf_tau[m] <= tau) l = m; else r = m;
  }
  if (l+1 >= _aest_tf_cache_hi) return _aest_tf_lambda*_aest_tf_f[l];
  t0 = _aest_tf_tau[l]; t1 = _aest_tf_tau[l+1];
  f0 = _aest_tf_f[l]; f1 = _aest_tf_f[l+1];
  if (t1 <= t0) return _aest_tf_lambda*f0;
  x = (tau-t0)/(t1-t0);
  return _aest_tf_lambda*(f0 + x*(f1-f0));
}
'''
        src.write_text(s + helper)

    # Record the exact eta derivative of E' on the native CLASS source grid.
    replace_once(
        root/'source'/'perturbations.c',
        '''  a = ppw->pvecback[pba->index_bg_a];\n  a2 = a * a;\n\n  a_prime_over_a = pvecback[pba->index_bg_a] * pvecback[pba->index_bg_H]; /* (a'/a)=aH */\n''',
        '''  a = ppw->pvecback[pba->index_bg_a];\n  a2 = a * a;\n\n  if ((pba->aest_enabled == _TRUE_) &&\n      (pba->aest_memory_enabled == _TRUE_) &&\n      (index_md == ppt->index_md_scalars)) {\n    int jm,nm=aest_memory_active_count(pba->aest_memory_order);\n    double Q_aest=pvecback[pba->index_bg_Q_aest];\n    double theta_aest=y[ppw->pv->index_pt_theta_cdm];\n    double alpha_aest=y[ppw->pv->index_pt_alpha_aest];\n    double chi_aest=Q_aest*(a*theta_aest/(k*k)+alpha_aest);\n    double Braw_aest=0.;\n    for (jm=0;jm<nm;jm++) {\n      double rj=aest_memory_node_order(pba->aest_memory_order,jm);\n      double wj=aest_memory_weight_order(pba->aest_memory_order,jm);\n      double omega_j=rj*pba->H0/pba->aest_tau_H0;\n      double qj=y[ppw->pv->index_pt_mem_q_aest+jm];\n      Braw_aest += wj*chi_aest-sqrt(wj)*(a*omega_j/k)*qj;\n    }\n    aest_tangent_trace_force(k,tau,-0.5*a*Q_aest*Braw_aest/pba->aest_KB);\n  }\n\n  a_prime_over_a = pvecback[pba->index_bg_a] * pvecback[pba->index_bg_H]; /* (a'/a)=aH */\n''',
        'native source-grid tangent trace')

    # The external forcing is the exact inhomogeneous term in the eta=0
    # variational equation. It is absent unless AEST_TANGENT_FORCE_FILE and
    # a non-zero AEST_TANGENT_LAMBDA are supplied.
    replace_once(
        root/'source'/'perturbations.c',
        '''        dy[pv->index_pt_E_aest] = a*E_rhs_aest/pba->aest_KB-a_prime_over_a*E_aest;\n''',
        '''        dy[pv->index_pt_E_aest] = a*E_rhs_aest/pba->aest_KB-a_prime_over_a*E_aest;\n        dy[pv->index_pt_E_aest] += aest_tangent_external_force(k,tau);\n''',
        'external tangent forcing')

    ptxt = (root/'source'/'perturbations.c').read_text()
    atxt = (root/'source'/'aest_memory.c').read_text()
    checks = {
        'trace_on_source_grid': 'aest_tangent_trace_force(k,tau,-0.5*a*Q_aest*Braw_aest/pba->aest_KB)' in ptxt,
        'external_variational_force': 'dy[pv->index_pt_E_aest] += aest_tangent_external_force(k,tau)' in ptxt,
        'runtime_force_loader': 'AEST_TANGENT_FORCE_FILE' in atxt,
        'runtime_lambda': 'AEST_TANGENT_LAMBDA' in atxt,
        'physical_memory_closure_preserved': 'E_rhs_aest -= 0.5*Q_aest*Bchi_aest' in ptxt,
    }
    report = {
        'classification': 'ETA0_VARIATIONAL_TANGENT_FORCING_PATCH',
        'forcing': "dEprime/deta|0 = -a Q Bchi_raw/(2 KB)",
        'signed_lambda_is_physical_eta': False,
        'trace_grid': 'native CLASS perturbation source-sampling grid',
        'checks': checks,
    }
    if not all(checks.values()):
        raise RuntimeError(report)
    (repo/'results').mkdir(exist_ok=True)
    (repo/'results'/'v019w_apply_report.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    main()
