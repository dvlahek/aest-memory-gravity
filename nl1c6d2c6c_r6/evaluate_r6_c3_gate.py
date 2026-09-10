#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from nl1c6d2c6c import r3_modewise_full_prehistory as r3

c = r3.c


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--reference", default="results/c3_r6_frozen_metric_reference.npz")
    ap.add_argument("--reference-meta", default="results/c3_r6_frozen_metric_reference.json")
    ap.add_argument("--json-out", default="results/c3_r6_original_c3_gate.json")
    args = ap.parse_args()

    try:
        meta = json.loads(Path(args.reference_meta).read_text())
        if meta.get("classification") != "C3_R6_FROZEN_METRIC_CLASS_VARIABLE_REFERENCE_READY":
            raise RuntimeError("R6 reference metadata classification mismatch")
        if meta.get("external_metric_tangent_frozen") is not True:
            raise RuntimeError("R6 reference did not freeze metric tangent")
        if meta.get("full_CLASS_Einstein_feedback") is not False:
            raise RuntimeError("R6 reference unexpectedly contains Einstein feedback")
        audits = dict(meta.get("bath_force_audits", {}))
        if not audits or not all(bool(v) for v in audits.values()):
            raise RuntimeError(f"R6 bath-force audits not all true: {audits}")

        data = c.m.prepare_class_data()
        pre = {39: c.prehistory(data, 128, 4096, 39)}
        linear_member = {"sigma": 0, "kind": "simple", "beta0": 1.0}
        linear = c.integrate(
            data,
            128,
            4096,
            linear_member,
            orders=(39,),
            nonlinear=False,
            pre_cache=pre,
        )
        if not linear.get("finite", False):
            raise RuntimeError(f"R6 offline linear control nonfinite: {linear.get('fail_reason')}")

        # Exactly the original D2C6C reference comparison and frozen C3 gate.
        err = c.reference_compare(data, linear, Path(args.reference))
        passed = bool(
            err["alpha"] <= c.LINEAR_GATE
            and err["E"] <= c.LINEAR_GATE
            and err["chi"] <= c.LINEAR_GATE
        )
        classification = (
            "C3_R6_FROZEN_METRIC_TANGENT_PASS"
            if passed else
            "C3_R6_FROZEN_METRIC_TANGENT_FAIL"
        )
        print(
            f"R6_C3 alpha={err['alpha']:.12e} E={err['E']:.12e} "
            f"chi={err['chi']:.12e} pass={passed}",
            flush=True,
        )
        report = {
            "classification": classification,
            "historical_R2_R3_R4_R5_remain_fail": True,
            "finite_positive_eta_licensed": False,
            "linear_gate": float(c.LINEAR_GATE),
            "errors": {k: float(v) for k, v in err.items()},
            "pass": passed,
            "reference_boundary_condition": "external metric tangent frozen at eta=0",
            "reference_compare_function": "nl1c6d2c6c.eta0_nonlinear_memory_tangent.reference_compare",
        }
        Path(args.json_out).write_text(json.dumps(report, indent=2, sort_keys=True)+"\n")
        print(f"CLASSIFICATION={classification}", flush=True)
        print("FINITE_POSITIVE_ETA_NONLINEAR_MEMORY_LICENSED=False", flush=True)
        return 0 if passed else 2
    except Exception as exc:
        print(f"C3_R6_GATE_ERROR {type(exc).__name__}: {exc}", flush=True)
        print("CLASSIFICATION=C3_R6_FROZEN_METRIC_REFERENCE_REPAIR_INCOMPLETE", flush=True)
        print("FINITE_POSITIVE_ETA_NONLINEAR_MEMORY_LICENSED=False", flush=True)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
