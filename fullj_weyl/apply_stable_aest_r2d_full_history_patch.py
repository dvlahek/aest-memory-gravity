#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

MARKER = "FULLJ_STABLE_AEST_R2D_FULL_HISTORY_V1"


def replace_once(path: Path, old: str, new: str, label: str) -> None:
    text = path.read_text()
    n = text.count(old)
    if n != 1:
        raise RuntimeError(f"{label}: expected one anchor, found {n} in {path}")
    path.write_text(text.replace(old, new, 1))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("class_root")
    args = ap.parse_args()
    root = Path(args.class_root).resolve()
    pc = root / "source" / "perturbations.c"
    am = root / "source" / "aest_memory.c"
    ah = root / "include" / "aest_memory.h"
    if not pc.is_file() or not am.is_file() or not ah.is_file():
        raise SystemExit("not an AeST CLASS source root")

    ptxt = pc.read_text()
    if MARKER in ptxt:
        print("STABLE_AEST_R2D_FULL_HISTORY_PATCH already=1")
        return 0
    if "FULLJ_AEST_STABLE_CHI_RESIDUAL_V1" not in ptxt:
        raise RuntimeError("stable residual parent marker missing")
    if "FULLJ_STABLE_AEST_R2B_VARIATIONAL_V1" not in ptxt:
        raise RuntimeError("R2b variational parent marker missing")

    htxt = ah.read_text()
    proto = "void aest_r2d_trace_force(double k,double h,double tau,double force);"
    if proto not in htxt:
        anchor = "double aest_tangent_external_force(double k,double tau);\n"
        if anchor not in htxt:
            raise RuntimeError("historical variational prototype anchor missing")
        htxt = htxt.replace(anchor, anchor + proto + "\n", 1)
        ah.write_text(htxt)

    atxt = am.read_text()
    if "void aest_r2d_trace_force(" in atxt:
        raise RuntimeError("R2d trace helper unexpectedly already present without marker")
    atxt += r'''

/* Stable AeST R2d full-history RHS forcing trace helper. Diagnostic only. */
void aest_r2d_trace_force(double k,double h,double tau,double force) {
  static FILE *fp = NULL;
  static int disabled = 0;
  const char *path;
  const char *skh;
  const char *sall;
  int all_k = 0;
  double target_kh,kh,rel;
  if (disabled) return;
  path = getenv("AEST_R2D_TRACE_FILE");
  skh = getenv("AEST_R2D_TRACE_KH");
  sall = getenv("AEST_R2D_TRACE_ALL_K");
  if (sall != NULL && sall[0] != '\0' && strtol(sall,NULL,10) != 0) all_k = 1;
  if (path == NULL || path[0] == '\0') {
    disabled = 1;
    return;
  }
  if (!all_k) {
    if (skh == NULL || skh[0] == '\0') {
      disabled = 1;
      return;
    }
    target_kh = strtod(skh,NULL);
    if (!(h > 0.) || !(target_kh > 0.)) return;
    kh = k/h;
    rel = fabs(kh-target_kh)/(fabs(target_kh)+1.e-300);
    if (rel > 2.e-10) return;
  }
  if (fp == NULL) {
    fp = fopen(path,"w");
    if (fp == NULL) {
      fprintf(stderr,"AEST_R2D_TRACE_OPEN_FAILED %s\n",path);
      disabled = 1;
      return;
    }
  }
  fprintf(fp,"%.17g %.17g %.17g\n",k,tau,force);
}
'''
    am.write_text(atxt)

    old = '''            Bchi_aest += wj*chi_aest-sw*(a*omega_j/k)*qj;\n          }\n          Bchi_aest *= pba->aest_eta;\n          E_rhs_aest -= 0.5*Q_aest*Bchi_aest;\n'''
    new = '''            Bchi_aest += wj*chi_aest-sw*(a*omega_j/k)*qj;\n          }\n          /* FULLJ_STABLE_AEST_R2D_FULL_HISTORY_V1: trace the exact raw eta derivative\n             inside the physical RHS block before eta multiplication. */\n          aest_r2d_trace_force(k,pba->h,tau,-0.5*a*Q_aest*Bchi_aest/pba->aest_KB);\n          Bchi_aest *= pba->aest_eta;\n          E_rhs_aest -= 0.5*Q_aest*Bchi_aest;\n'''
    replace_once(pc, old, new, "R2d physical memory RHS trace")

    ptxt = pc.read_text(); atxt = am.read_text(); htxt = ah.read_text()
    checks = {
        "marker": MARKER in ptxt,
        "stable_parent": "FULLJ_AEST_STABLE_CHI_RESIDUAL_V1" in ptxt,
        "r2b_parent": "FULLJ_STABLE_AEST_R2B_VARIATIONAL_V1" in ptxt,
        "direct_inblock_trace": "aest_r2d_trace_force(k,pba->h,tau,-0.5*a*Q_aest*Bchi_aest/pba->aest_KB);" in ptxt,
        "trace_before_eta": ptxt.find("aest_r2d_trace_force(k,pba->h,tau,-0.5*a*Q_aest*Bchi_aest/pba->aest_KB);") < ptxt.find("Bchi_aest *= pba->aest_eta;"),
        "physical_eta_multiply_once": ptxt.count("Bchi_aest *= pba->aest_eta;") == 1,
        "physical_closure_once": ptxt.count("E_rhs_aest -= 0.5*Q_aest*Bchi_aest;") == 1,
        "helper_once": atxt.count("void aest_r2d_trace_force(") == 1,
        "target_filter": "AEST_R2D_TRACE_KH" in atxt,
        "all_k_transport": "AEST_R2D_TRACE_ALL_K" in atxt and "if (!all_k)" in atxt,
        "trace_file_env": "AEST_R2D_TRACE_FILE" in atxt,
        "prototype": proto in htxt,
    }
    if not all(checks.values()):
        raise RuntimeError("R2d full-history source audit failed: "+repr(checks))
    print("STABLE_AEST_R2D_FULL_HISTORY_PATCH_PASS")
    for k,v in checks.items():
        print(f"{k}={v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
