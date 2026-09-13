#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fullj_weyl import corrected_class_spectral_fringe_gr_control as base

REPAIR_PREDATA_LOCK = "1812f015682a946125e747f81b97b902dcf1bec0"
DENSE_RUNTIME_SOURCE_SHA = "4d5ab5dc7066d4880f06fcfc731d6534ed0ff992e3cc15fb473dddccb25a594f"
CLASS_HEAD = "e85808324f51fc694d12e3ed7439552a3c3f9540"


def is_ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0


def json_out_from_argv() -> Path:
    args = sys.argv[1:]
    if "--json-out" in args:
        i = args.index("--json-out")
        if i + 1 < len(args):
            return Path(args[i + 1])
    return ROOT / "results/fullj_corrected_class_spectral_fringe_gr_control.json"


def main() -> int:
    if not is_ancestor(REPAIR_PREDATA_LOCK):
        print("FULLJ_DIRECT_CLASS_FRINGE_R1_REPAIR_LOCK_FAIL", flush=True)
        return 3

    class_root = Path(os.environ.get("NL1C6D2N_CLASS_ROOT", ""))
    if not class_root.is_dir() or not (class_root / ".git").exists():
        print("FULLJ_DIRECT_CLASS_FRINGE_R1_RUNTIME_ENV_MISSING", flush=True)
        return 3

    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=class_root, text=True).strip()
    src = class_root / "source/aest_memory.c"
    if not src.is_file():
        print("FULLJ_DIRECT_CLASS_FRINGE_R1_RUNTIME_SOURCE_MISSING", flush=True)
        return 3
    source_sha = base.sha256_file(src)

    if head != CLASS_HEAD or source_sha != DENSE_RUNTIME_SOURCE_SHA:
        print(
            "FULLJ_DIRECT_CLASS_FRINGE_R1_RUNTIME_PROVENANCE_FAIL "
            f"head={head} source_sha256={source_sha}",
            flush=True,
        )
        return 3

    # The original implementation compared the fully patched dense-k64 runtime
    # source against the earlier baseline-source SHA.  Correct only that
    # provenance target.  No physics, grid, gate, or classification changes.
    base.cb.CORRECTED_SOURCE_SHA = DENSE_RUNTIME_SOURCE_SHA
    print(
        "FULLJ_DIRECT_CLASS_FRINGE_R1_RUNTIME_PROVENANCE_PASS "
        f"head={head} source_sha256={source_sha}",
        flush=True,
    )

    rc = int(base.main())

    out_path = json_out_from_argv()
    if out_path.exists():
        try:
            payload = json.loads(out_path.read_text())
            payload["runtime_provenance_repair"] = {
                "repair_predata_lock": REPAIR_PREDATA_LOCK,
                "historical_incomplete_preserved": True,
                "CLASS_head": head,
                "dense_runtime_source_sha256": source_sha,
                "baseline_provenance_target_replaced_only": True,
                "science_grid_or_gate_changed": False,
            }
            out_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
        except Exception as exc:
            print(f"FULLJ_DIRECT_CLASS_FRINGE_R1_JSON_ANNOTATION_WARNING={exc}", flush=True)

    return rc


if __name__ == "__main__":
    raise SystemExit(main())
