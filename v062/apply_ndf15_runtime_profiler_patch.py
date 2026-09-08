#!/usr/bin/env python3
"""Execution-only NDF15 profiler patch for the v0.62 runtime cliff.

This does not alter equations, tolerances, starting conditions, acceptance gates,
or any scientific setting. It only adds optional counters/progress output to
CLASS' NDF15 loop when AEST_NDF15_PROFILE_FILE is set.
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
    marker = "AEST v0.62 NDF15 runtime profiler"
    if marker in text:
        print("NDF15 profiler patch already present")
        return

    replace_once(
        src,
        '#include "sparse.h"\n',
        '#include "sparse.h"\n#include <stdio.h>\n#include <stdlib.h>\n\n'
        '/* AEST v0.62 NDF15 runtime profiler: execution-only instrumentation. */\n'
        'static int aest_ndf15_profile_call_seq = 0;\n'
        'static void aest_ndf15_profile_emit(int call_id,const char *phase,long long loop,\n'
        '                                      double t,double t0,double tfinal,double absh,int order,\n'
        '                                      int neq,int *stepstat) {\n'
        '  const char *path = getenv("AEST_NDF15_PROFILE_FILE");\n'
        '  FILE *fp;\n'
        '  if (path == NULL || path[0] == \'\\0\') return;\n'
        '  fp = fopen(path,"a");\n'
        '  if (fp == NULL) return;\n'
        '  fprintf(fp,"call=%d phase=%s loop=%lld neq=%d t=%.17g t0=%.17g tfinal=%.17g absh=%.17g order=%d ok=%d fail=%d feval=%d jac=%d lu=%d solve=%d\\n",\n'
        '          call_id,phase,loop,neq,t,t0,tfinal,absh,order,\n'
        '          stepstat[0],stepstat[1],stepstat[2],stepstat[3],stepstat[4],stepstat[5]);\n'
        '  fclose(fp);\n'
        '}\n',
        "include profiler helper",
    )

    replace_once(
        src,
        '  int verbose=0;\n  int funcreturn;\n',
        '  int verbose=0;\n  int funcreturn;\n'
        '  int aest_profile_call_id = ++aest_ndf15_profile_call_seq;\n'
        '  long long aest_profile_loop = 0;\n',
        "profile locals",
    )

    replace_once(
        src,
        '  /* Doing main loop: */\n  done = _FALSE_;\n  at_hmin = _FALSE_;\n  while (done==_FALSE_){\n',
        '  /* Doing main loop: */\n'
        '  done = _FALSE_;\n'
        '  at_hmin = _FALSE_;\n'
        '  aest_ndf15_profile_emit(aest_profile_call_id,"BEGIN",0,t,t0,tfinal,absh,k,neq,stepstat);\n'
        '  while (done==_FALSE_){\n'
        '    aest_profile_loop++;\n'
        '    if ((aest_profile_loop % 10000LL) == 0)\n'
        '      aest_ndf15_profile_emit(aest_profile_call_id,"LOOP",aest_profile_loop,t,t0,tfinal,absh,k,neq,stepstat);\n',
        "main-loop profiler",
    )

    print(f"patched {src}")
    print("Set AEST_NDF15_PROFILE_FILE=/path/to/profile.log to enable profiling.")
    print("Scientific settings changed: false")


if __name__ == "__main__":
    main()
