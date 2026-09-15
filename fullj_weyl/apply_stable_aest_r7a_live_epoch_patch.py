#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

MARKER = "FULLJ_STABLE_AEST_R7A_LIVE_EPOCH_V1"
PROTO = "double aest_r7a_epoch_weight(double a);"
OLD_MUL = "Bchi_aest *= pba->aest_eta;"
NEW_MUL = "Bchi_aest *= pba->aest_eta*aest_r7a_epoch_weight(a);"


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
        print("STABLE_AEST_R7A_LIVE_EPOCH_PATCH already=1")
        return 0
    if "FULLJ_AEST_STABLE_CHI_RESIDUAL_V1" not in ptxt:
        raise RuntimeError("R7a requires certified stable-chi source")
    if ptxt.count(OLD_MUL) != 1:
        raise RuntimeError(f"R7a physical eta multiplier expected once, found {ptxt.count(OLD_MUL)}")
    if ptxt.count("E_rhs_aest -= 0.5*Q_aest*Bchi_aest;") != 1:
        raise RuntimeError("R7a physical closure is not unique")
    if "dy[pv->index_pt_E_aest] += aest_tangent_external_force(k,tau);" in ptxt:
        raise RuntimeError("R7a requires dormant external tangent hook to be neutralized before patch")
    if "aest_r2d_trace_force(k,pba->h,tau" in ptxt:
        raise RuntimeError("R7a must not contain an R2d full-history trace hook")

    htxt = ah.read_text()
    if PROTO not in htxt:
        anchor = "\n#ifdef __cplusplus\n}\n#endif\n"
        if anchor not in htxt:
            raise RuntimeError("aest_memory.h extern-C anchor not found")
        htxt = htxt.replace(anchor, "\n" + PROTO + "\n" + anchor, 1)
        ah.write_text(htxt)

    atxt = am.read_text()
    for inc in ("#include <stdio.h>", "#include <stdlib.h>", "#include <string.h>"):
        if inc not in atxt:
            lines = atxt.splitlines(keepends=True)
            i = 0
            while i < len(lines) and lines[i].lstrip().startswith("#include"):
                i += 1
            lines.insert(i, inc + "\n")
            atxt = "".join(lines)

    if "double aest_r7a_epoch_weight(" in atxt:
        raise RuntimeError("R7a helper unexpectedly already present without marker")

    atxt += r'''

/* FULLJ_STABLE_AEST_R7A_LIVE_EPOCH_V1
   Diagnostic first-order cosmic-epoch mask applied only to the physical
   memory feedback coefficient. Bath evolution remains live and unwindowed. */
double aest_r7a_epoch_weight(double a) {
  static int mode = -1;
  const char *s;
  double z;
  if (mode < 0) {
    s = getenv("AEST_R7A_EPOCH_MODE");
    if (s == NULL || s[0] == '\0') {
      fprintf(stderr,"AEST_R7A_EPOCH_MODE_MISSING\n");
      exit(95);
    }
    if (strcmp(s,"full") == 0) mode = 0;
    else if (strcmp(s,"ancient") == 0) mode = 1;
    else if (strcmp(s,"intermediate") == 0) mode = 2;
    else if (strcmp(s,"recent_structure") == 0) mode = 3;
    else if (strcmp(s,"late") == 0) mode = 4;
    else {
      fprintf(stderr,"AEST_R7A_EPOCH_MODE_UNKNOWN %s\n",s);
      exit(96);
    }
  }
  if (!(a > 0.) || !isfinite(a)) {
    fprintf(stderr,"AEST_R7A_INVALID_SCALE_FACTOR %.17g\n",a);
    exit(97);
  }
  if (mode == 0) return 1.;
  z = 1./a - 1.;
  if (mode == 1) return (z >= 10.) ? 1. : 0.;
  if (mode == 2) return (z >= 2. && z < 10.) ? 1. : 0.;
  if (mode == 3) return (z >= 0.5 && z < 2.) ? 1. : 0.;
  if (mode == 4) return (z < 0.5) ? 1. : 0.;
  exit(98);
}
'''
    am.write_text(atxt)

    ptxt = pc.read_text()
    ptxt = ptxt.replace(OLD_MUL, NEW_MUL, 1)
    # Source-level marker beside the live multiplier for scoped audits.
    ptxt = ptxt.replace(
        NEW_MUL,
        "/* " + MARKER + ": live physical epoch weight */\n          " + NEW_MUL,
        1,
    )
    pc.write_text(ptxt)

    ptxt = pc.read_text(); atxt = am.read_text(); htxt = ah.read_text()
    checks = {
        "marker": MARKER in ptxt and MARKER in atxt,
        "stable_parent": "FULLJ_AEST_STABLE_CHI_RESIDUAL_V1" in ptxt,
        "old_multiplier_absent": OLD_MUL not in ptxt,
        "windowed_multiplier_once": ptxt.count(NEW_MUL) == 1,
        "physical_closure_once": ptxt.count("E_rhs_aest -= 0.5*Q_aest*Bchi_aest;") == 1,
        "external_hook_absent": "dy[pv->index_pt_E_aest] += aest_tangent_external_force(k,tau);" not in ptxt,
        "r2d_trace_absent": "aest_r2d_trace_force(k,pba->h,tau" not in ptxt,
        "helper_once": atxt.count("double aest_r7a_epoch_weight(") == 1,
        "mode_env": "AEST_R7A_EPOCH_MODE" in atxt,
        "all_modes": all(('\"'+x+'\"') in atxt for x in ("full","ancient","intermediate","recent_structure","late")),
        "prototype": PROTO in htxt,
    }
    if not all(checks.values()):
        raise RuntimeError("R7a live epoch patch audit failed: " + repr(checks))
    print("STABLE_AEST_R7A_LIVE_EPOCH_PATCH_PASS")
    for k,v in checks.items():
        print(f"{k}={v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
