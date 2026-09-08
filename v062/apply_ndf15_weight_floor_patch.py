#!/usr/bin/env python3
"""Execution-only NDF15 weight-floor diagnostic patch for v0.62.

Adds an optional environment override for the NDF15 state-weight floor used in
relative Newton/LTE norms. The default remains exactly 1e-15. The Jacobian
absolute tolerance (`abstol`) is NOT changed.

Enable with, e.g.:
  AEST_NDF15_WEIGHT_FLOOR=1e-13

This is a non-scientific diagnostic control and MUST NOT be used for the
preregistered v0.62 classification unless an explicit numerical-equivalence
study is completed first.
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

    marker = "AEST v0.62 NDF15 weight-floor diagnostic"
    if marker in text:
        print("NDF15 weight-floor patch already present")
        return

    old = "  double abstol = 1e-15, eps=1e-16, threshold=abstol;\n"
    new = r'''  double abstol = 1e-15, eps=1e-16, threshold=abstol;
  /* AEST v0.62 NDF15 weight-floor diagnostic: execution-only override.
     This changes only the floor entering wt=max(|y|,threshold).  The
     numjac absolute tolerance remains abstol=1e-15. */
  {
    const char *aest_floor_env = getenv("AEST_NDF15_WEIGHT_FLOOR");
    if ((aest_floor_env != NULL) && (aest_floor_env[0] != '\0')) {
      char *aest_end = NULL;
      double aest_floor = strtod(aest_floor_env,&aest_end);
      if ((aest_end != aest_floor_env) && (aest_floor > 0.0) && isfinite(aest_floor)) {
        threshold = aest_floor;
      }
    }
  }
'''
    replace_once(src, old, new, "NDF15 threshold declaration")

    print(f"patched {src}")
    print("Default NDF15 weight floor remains 1e-15")
    print("Set AEST_NDF15_WEIGHT_FLOOR=<positive float> for diagnostic override")
    print("Jacobian abstol changed: false")
    print("Scientific settings changed: false")


if __name__ == "__main__":
    main()
