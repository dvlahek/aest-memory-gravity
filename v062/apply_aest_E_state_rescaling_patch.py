#!/usr/bin/env python3
"""Diagnostic-only AeST E state-rescaling patch for v0.62.

This applies an invertible coordinate transformation to the NDF15 state only:

    E_stored = S * E_physical

with S controlled by AEST_E_STATE_SCALE (default 1). All physical uses of E
are divided by S and the E derivative is multiplied by S. Thus S=1 is exactly
the frozen implementation, while S>1 changes only the numerical coordinate
seen by the ODE solver. The physical equations, perturbation rtol, NDF15
weight floor, Jacobian abstol, target k values, and science gates are untouched.

This patch is diagnostic only. It MUST NOT be used for the preregistered v0.62
classification unless numerical equivalence is independently demonstrated.
"""

from pathlib import Path
import argparse


def replace_once(path: Path, old: str, new: str, label: str) -> None:
    text = path.read_text()
    n = text.count(old)
    if n != 1:
        raise RuntimeError(f"{label}: expected exactly one anchor, found {n} in {path}")
    path.write_text(text.replace(old, new, 1))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("class_root")
    args = ap.parse_args()

    root = Path(args.class_root).resolve()
    src = root / "source" / "perturbations.c"
    if not src.exists():
        raise SystemExit("Not a CLASS source root")

    text = src.read_text()
    marker = "AEST v0.62 E-state rescaling diagnostic"
    if marker in text:
        print("AeST E-state rescaling patch already present")
        return

    # Add a cached environment-controlled scale. Default S=1 preserves the
    # original/frozen implementation exactly.
    include_anchor = '#include "aest_memory.h"\n'
    helper = r'''#include "aest_memory.h"

/* AEST v0.62 E-state rescaling diagnostic.
   Stored coordinate: E_stored = S * E_physical. Default S=1. */
static double aest_v062_E_state_scale(void) {
  static int initialized = 0;
  static double scale = 1.0;
  if (initialized == 0) {
    const char *env = getenv("AEST_E_STATE_SCALE");
    if ((env != NULL) && (env[0] != '\0')) {
      char *end = NULL;
      double candidate = strtod(env,&end);
      if ((end != env) && (candidate > 0.0) && isfinite(candidate)) {
        scale = candidate;
      }
    }
    initialized = 1;
  }
  return scale;
}
'''
    replace_once(src, include_anchor, helper, "aest_memory include")

    # Physical source term: decode stored E before using it.
    old_source = '''          *(pba->aest_KB*y[ppw->pv->index_pt_E_aest]+(2.-pba->aest_KB)*chi_aest);'''
    new_source = '''          *(pba->aest_KB*(y[ppw->pv->index_pt_E_aest]/aest_v062_E_state_scale())+(2.-pba->aest_KB)*chi_aest);'''
    replace_once(src, old_source, new_source, "AeST E physical source decode")

    # Derivative block: decode E for all physical algebra, then encode dE/dtau
    # back into the stored coordinate.
    old_read = '''        double E_aest = y[pv->index_pt_E_aest];'''
    new_read = '''        double E_aest = y[pv->index_pt_E_aest]/aest_v062_E_state_scale();'''
    replace_once(src, old_read, new_read, "AeST E derivative decode")

    old_dy = '''        dy[pv->index_pt_E_aest] = a*E_rhs_aest/pba->aest_KB-a_prime_over_a*E_aest;'''
    new_dy = '''        dy[pv->index_pt_E_aest] = aest_v062_E_state_scale()*(a*E_rhs_aest/pba->aest_KB-a_prime_over_a*E_aest);'''
    replace_once(src, old_dy, new_dy, "AeST E derivative encode")

    print(f"patched {src}")
    print("Default AEST_E_STATE_SCALE=1 preserves frozen equations and coordinates")
    print("Set AEST_E_STATE_SCALE>1 only for the non-classifying equivalence probe")
    print("NDF15 weight floor changed: false")
    print("Jacobian abstol changed: false")
    print("Physical equations changed: false (invertible state-coordinate transform only)")
    print("Final certification changed: false")


if __name__ == "__main__":
    main()
