#!/usr/bin/env python3
"""Execution-only NDF15 error-dominator instrumentation for v0.62.

Apply after apply_ndf15_runtime_profiler_patch.py. This patch does not alter
ODE equations, tolerances, starting conditions, acceptance/rejection logic,
step-size selection, or scientific gates. It only records which state-vector
component dominates the Newton correction norm and local truncation-error norm.

Enable with AEST_NDF15_DOMINATOR_FILE=/path/to/log.
"""
from pathlib import Path
import argparse


def replace_once(path, old, new, label):
    p = Path(path)
    s = p.read_text()
    n = s.count(old)
    if n != 1:
        raise RuntimeError(f"{label}: expected one anchor, found {n} in {p}")
    p.write_text(s.replace(old, new, 1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("class_root")
    args = ap.parse_args()
    root = Path(args.class_root).resolve()
    src = root / "tools" / "evolver_ndf15.c"
    text = src.read_text()

    marker = "AEST v0.62 NDF15 error dominator"
    if marker in text:
        print("NDF15 error-dominator patch already present")
        return
    if "AEST v0.62 NDF15 runtime profiler" not in text:
        raise RuntimeError("apply runtime profiler patch first")

    # Add a separate optional emitter. Arrays use CLASS' 1-based indexing here.
    anchor = "static int aest_ndf15_profile_call_seq = 0;\n"
    helper = r'''static int aest_ndf15_profile_call_seq = 0;
/* AEST v0.62 NDF15 error dominator: execution-only instrumentation. */
static void aest_ndf15_dominator_emit(int call_id,long long loop,double t,double absh,int order,
                                       int err_idx,double err_raw,int newton_idx,double newton_raw,
                                       double *y,double *pred,double *difkp1,double *invwt,int neq) {
  const char *path = getenv("AEST_NDF15_DOMINATOR_FILE");
  FILE *fp;
  double ey=0., ep=0., ed=0., ew=0., ny=0., np=0., nd=0., nw=0.;
  if (path == NULL || path[0] == '\0') return;
  if (err_idx >= 1 && err_idx <= neq) {
    ey=y[err_idx]; ep=pred[err_idx]; ed=difkp1[err_idx]; ew=invwt[err_idx];
  }
  if (newton_idx >= 1 && newton_idx <= neq) {
    ny=y[newton_idx]; np=pred[newton_idx]; nd=difkp1[newton_idx]; nw=invwt[newton_idx];
  }
  fp=fopen(path,"a");
  if (fp == NULL) return;
  fprintf(fp,"call=%d loop=%lld t=%.17g absh=%.17g order=%d err_idx=%d err_raw=%.17g err_y=%.17g err_pred=%.17g err_dif=%.17g err_invwt=%.17g newton_idx=%d newton_raw=%.17g newton_y=%.17g newton_pred=%.17g newton_dif=%.17g newton_invwt=%.17g\n",
          call_id,loop,t,absh,order,err_idx,err_raw,ey,ep,ed,ew,
          newton_idx,newton_raw,ny,np,nd,nw);
  fclose(fp);
}
'''
    replace_once(src, anchor, helper, "dominator helper")

    replace_once(
        src,
        "  int aest_profile_call_id = ++aest_ndf15_profile_call_seq;\n  long long aest_profile_loop = 0;\n",
        "  int aest_profile_call_id = ++aest_ndf15_profile_call_seq;\n"
        "  long long aest_profile_loop = 0;\n"
        "  int aest_err_idx = -1, aest_newton_idx = -1;\n"
        "  double aest_err_raw = -1.0, aest_newton_raw = -1.0;\n",
        "dominator locals",
    )

    # Newton correction norm: remember the component producing max |del*invwt|.
    replace_once(
        src,
        "          newnrm = 0.0;\n          for(j=1;j<=neq;j++){\n            maxtmp = fabs(del[j]*invwt[j]);\n            newnrm = MAX(newnrm,maxtmp);\n          }\n",
        "          newnrm = 0.0;\n"
        "          aest_newton_idx = -1; aest_newton_raw = -1.0;\n"
        "          for(j=1;j<=neq;j++){\n"
        "            maxtmp = fabs(del[j]*invwt[j]);\n"
        "            if (maxtmp > newnrm) { newnrm = maxtmp; aest_newton_idx = j; aest_newton_raw = maxtmp; }\n"
        "          }\n",
        "Newton norm dominator",
    )

    # Local truncation-error norm: remember max |difkp1*invwt| before erconst scaling.
    replace_once(
        src,
        "      err = 0.0;\n      for(jj=1;jj<=neq;jj++){\n        err = MAX(err,fabs(difkp1[jj]*invwt[jj]));\n      }\n      err = err * erconst[k-1];\n",
        "      err = 0.0;\n"
        "      aest_err_idx = -1; aest_err_raw = -1.0;\n"
        "      for(jj=1;jj<=neq;jj++){\n"
        "        maxtmp = fabs(difkp1[jj]*invwt[jj]);\n"
        "        if (maxtmp > err) { err = maxtmp; aest_err_idx = jj; aest_err_raw = maxtmp; }\n"
        "      }\n"
        "      err = err * erconst[k-1];\n",
        "LTE norm dominator",
    )

    # Emit once per 10k outer steps, aligned with the existing runtime profiler.
    replace_once(
        src,
        "    if ((aest_profile_loop % 10000LL) == 0)\n      aest_ndf15_profile_emit(aest_profile_call_id,\"LOOP\",aest_profile_loop,t,t0,tfinal,absh,k,neq,stepstat);\n",
        "    if ((aest_profile_loop % 10000LL) == 0) {\n"
        "      aest_ndf15_profile_emit(aest_profile_call_id,\"LOOP\",aest_profile_loop,t,t0,tfinal,absh,k,neq,stepstat);\n"
        "      aest_ndf15_dominator_emit(aest_profile_call_id,aest_profile_loop,t,absh,k,\n"
        "                                 aest_err_idx,aest_err_raw,aest_newton_idx,aest_newton_raw,\n"
        "                                 y,pred,difkp1,invwt,neq);\n"
        "    }\n",
        "periodic dominator emit",
    )

    print(f"patched {src}")
    print("Set AEST_NDF15_DOMINATOR_FILE=/path/to/dominator.log to enable.")
    print("Scientific settings changed: false")


if __name__ == "__main__":
    main()
