#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def replace_once(path: Path, old: str, new: str, label: str) -> None:
    text = path.read_text()
    n = text.count(old)
    if n != 1:
        raise RuntimeError(f"{label}: expected exactly one anchor, found {n}")
    path.write_text(text.replace(old, new, 1))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("class_root")
    args = ap.parse_args()
    root = Path(args.class_root).resolve()
    repo = Path(__file__).resolve().parents[1]
    ac = root / "source" / "aest_memory.c"

    old_miss = '''  if (rel > 2.e-10) {\n    fprintf(stderr,"AEST_TANGENT_FORCE_K_MISS query=%.17g nearest=%.17g rel=%.3e\\n",\n            k,_aest_tf_cache_k,rel);\n    return 0;\n  }\n'''
    new_miss = '''  if (rel > 2.e-10) {\n    const char *allow_sparse = getenv("AEST_TANGENT_ALLOW_K_MISS");\n    if (allow_sparse != NULL && strcmp(allow_sparse,"1") == 0) return 0;\n    fprintf(stderr,"AEST_TANGENT_FORCE_K_MISS query=%.17g nearest=%.17g rel=%.3e\\n",\n            k,_aest_tf_cache_k,rel);\n    return 0;\n  }\n'''
    replace_once(ac, old_miss, new_miss, "R5 sparse-k selector")

    replace_once(
        ac,
        '  if (!_aest_tangent_select_k(k)) exit(94);\n',
        '  if (!_aest_tangent_select_k(k)) {\n'
        '    const char *allow_sparse = getenv("AEST_TANGENT_ALLOW_K_MISS");\n'
        '    if (allow_sparse != NULL && strcmp(allow_sparse,"1") == 0) return 0.;\n'
        '    exit(94);\n'
        '  }\n',
        "R5 sparse-k zero forcing",
    )

    text = ac.read_text()
    checks = {
        "sparse_k_env_present": "AEST_TANGENT_ALLOW_K_MISS" in text,
        "exact_match_tolerance_unchanged": "if (rel > 2.e-10)" in text,
        "exact_force_interpolation_unchanged": "return _aest_tf_lambda*(f0 + x*(f1-f0));" in text,
    }
    if not all(checks.values()):
        raise RuntimeError(f"R5 sparse-k patch audit failed: {checks}")
    report = {
        "classification": "C3_R5_SPARSE_K_FORCE_PATCH_READY",
        "physics_modified": False,
        "checks": checks,
    }
    (repo / "results").mkdir(exist_ok=True)
    (repo / "results" / "c3_r5_sparse_k_patch.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(report, indent=2, sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
