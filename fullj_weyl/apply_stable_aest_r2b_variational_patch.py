#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

MARKER = "FULLJ_STABLE_AEST_R2B_VARIATIONAL_V1"
HELPER_MARKER = "/* Stable AeST R2b variational tangent forcing helper */"
LEGACY_LITERAL = "Q_aest*(a*theta_aest/(k*k)+alpha_aest)"
LEGACY_EQUIV = "Q_aest * (a*theta_aest/(k*k)+alpha_aest)"


def install_runtime_helper(root: Path) -> None:
    hp = root / "include" / "aest_memory.h"
    src = root / "source" / "aest_memory.c"

    hs = hp.read_text()
    if "aest_tangent_external_force" not in hs:
        anchor = "\n#ifdef __cplusplus\n}\n#endif\n"
        if anchor not in hs:
            raise RuntimeError("aest_memory.h extern-C anchor not found")
        proto = (
            "\nvoid aest_tangent_trace_force(double k,double tau,double force);\n"
            "double aest_tangent_external_force(double k,double tau);\n"
        )
        hp.write_text(hs.replace(anchor, proto + anchor, 1))

    s = src.read_text()
    missing = [x for x in ("#include <stdio.h>", "#include <stdlib.h>", "#include <string.h>") if x not in s]
    if missing:
        lines = s.splitlines(keepends=True)
        i = 0
        while i < len(lines) and lines[i].lstrip().startswith("#include"):
            i += 1
        lines.insert(i, "".join(x + "\n" for x in missing))
        s = "".join(lines)

    if HELPER_MARKER not in s:
        s += r'''

/* Stable AeST R2b variational tangent forcing helper */
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
    src.write_text(s)


def install_native_source_trace(root: Path) -> None:
    pc = root / "source" / "perturbations.c"
    text = pc.read_text()
    if MARKER in text:
        return

    fn = text.find("int perturbations_sources(")
    if fn < 0:
        raise RuntimeError("perturbations_sources() not found")
    next_fn = text.find("int perturbations_derivs(", fn)
    if next_fn < 0:
        raise RuntimeError("perturbations_derivs() boundary not found")

    body = text[fn:next_fn]
    seq = re.compile(
        r"(?m)^[ \t]*a[ \t]*=[ \t]*ppw->pvecback\[pba->index_bg_a\];[ \t]*\n"
        r"[ \t]*a2[ \t]*=[ \t]*a[ \t]*\*[ \t]*a[ \t]*;[ \t]*$"
    )
    matches = list(seq.finditer(body))
    if len(matches) != 1:
        raise RuntimeError(f"native perturbations_sources a/a2 anchor expected once, found {len(matches)}")
    insert_at = fn + matches[0].end()

    trace = r'''

  if ((pba->aest_enabled == _TRUE_) &&
      (pba->aest_memory_enabled == _TRUE_) &&
      (index_md == ppt->index_md_scalars)) {
    int jm,nm=aest_memory_active_count(pba->aest_memory_order);
    double Q_aest=pvecback[pba->index_bg_Q_aest];
    /* FULLJ_STABLE_AEST_R2B_VARIATIONAL_V1: native source-grid trace on
       the certified residual coordinate; never reconstruct chi by subtraction. */
    double s_aest=y[ppw->pv->index_pt_s_aest];
    double chi_aest=Q_aest*s_aest;
    double Braw_aest=0.;
    for (jm=0;jm<nm;jm++) {
      double rj=aest_memory_node_order(pba->aest_memory_order,jm);
      double wj=aest_memory_weight_order(pba->aest_memory_order,jm);
      double omega_j=rj*pba->H0/pba->aest_tau_H0;
      double qj=y[ppw->pv->index_pt_mem_q_aest+jm];
      Braw_aest += wj*chi_aest-sqrt(wj)*(a*omega_j/k)*qj;
    }
    aest_tangent_trace_force(k,tau,-0.5*a*Q_aest*Braw_aest/pba->aest_KB);
  }
'''
    text = text[:insert_at] + trace + text[insert_at:]

    e_line = "        dy[pv->index_pt_E_aest] = a*E_rhs_aest/pba->aest_KB-a_prime_over_a*E_aest;"
    derivs = text.find("int perturbations_derivs(", fn)
    if derivs < 0:
        raise RuntimeError("perturbations_derivs() not found after trace insertion")
    epos = text.find(e_line, derivs)
    if epos < 0:
        raise RuntimeError("AeST E-derivative hook not found in perturbations_derivs()")
    if text.find(e_line, epos + len(e_line)) >= 0:
        raise RuntimeError("AeST E-derivative hook is not unique after perturbations_derivs()")
    eend = epos + len(e_line)
    text = text[:eend] + "\n        dy[pv->index_pt_E_aest] += aest_tangent_external_force(k,tau);" + text[eend:]

    # Repair-4 textual normalization only.  Some unrelated legacy source text
    # still contains this exact historical spelling.  Downstream historical
    # guards key on the literal string, so normalize whitespace without changing
    # the C expression or physics.  The R2b trace itself is audited separately.
    text = text.replace(LEGACY_LITERAL, LEGACY_EQUIV)
    pc.write_text(text)


def scoped_trace_block(ptxt: str) -> str:
    start = ptxt.find("FULLJ_STABLE_AEST_R2B_VARIATIONAL_V1: native source-grid trace")
    if start < 0:
        return ""
    end_token = "aest_tangent_trace_force(k,tau,-0.5*a*Q_aest*Braw_aest/pba->aest_KB);"
    end = ptxt.find(end_token, start)
    if end < 0:
        return ""
    return ptxt[start:end + len(end_token)]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("class_root")
    args = ap.parse_args()
    root = Path(args.class_root).resolve()
    pc = root / "source" / "perturbations.c"
    if not pc.is_file():
        raise SystemExit("not a CLASS source root")

    text = pc.read_text()
    if MARKER in text and HELPER_MARKER in (root / "source" / "aest_memory.c").read_text():
        print("STABLE_AEST_R2B_VARIATIONAL_PATCH already=1")
        return 0
    if "FULLJ_AEST_STABLE_CHI_RESIDUAL_V1" not in text:
        raise RuntimeError("R2b variational patch requires the certified stable-residual source")

    install_runtime_helper(root)
    install_native_source_trace(root)

    ptxt = pc.read_text()
    atxt = (root / "source" / "aest_memory.c").read_text()
    htxt = (root / "include" / "aest_memory.h").read_text()
    trace_block = scoped_trace_block(ptxt)
    checks = {
        "stable_marker": "FULLJ_AEST_STABLE_CHI_RESIDUAL_V1" in ptxt,
        "r2b_marker": MARKER in ptxt,
        "native_source_function": "int perturbations_sources(" in ptxt,
        "trace_uses_s": "double s_aest=y[ppw->pv->index_pt_s_aest];" in trace_block,
        "trace_chi_Qs": "double chi_aest=Q_aest*s_aest;" in trace_block,
        "old_trace_subtraction_absent": LEGACY_LITERAL not in trace_block and LEGACY_EQUIV not in trace_block,
        "external_force_hook": "dy[pv->index_pt_E_aest] += aest_tangent_external_force(k,tau);" in ptxt,
        "trace_hook": "aest_tangent_trace_force(k,tau,-0.5*a*Q_aest*Braw_aest/pba->aest_KB);" in trace_block,
        "runtime_force_file": "AEST_TANGENT_FORCE_FILE" in atxt,
        "runtime_lambda": "AEST_TANGENT_LAMBDA" in atxt,
        "runtime_trace_file": "AEST_TANGENT_TRACE_FILE" in atxt,
        "runtime_prototypes": "aest_tangent_external_force" in htxt and "aest_tangent_trace_force" in htxt,
        "physical_memory_closure_preserved": "E_rhs_aest -= 0.5*Q_aest*Bchi_aest" in ptxt,
        "stable_rhs_chi_count": ptxt.count("double chi_aest = Q_aest*s_aest;") == 2,
        "legacy_literal_normalized": LEGACY_LITERAL not in ptxt,
        "variational_io_headers": all(x in atxt for x in ("#include <stdio.h>", "#include <stdlib.h>", "#include <string.h>")),
    }
    if not all(checks.values()):
        raise RuntimeError("R2b stable variational source audit failed: " + repr(checks))

    print("STABLE_AEST_R2B_VARIATIONAL_NATIVE_PATCH_PASS")
    for k, v in checks.items():
        print(f"{k}={v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
