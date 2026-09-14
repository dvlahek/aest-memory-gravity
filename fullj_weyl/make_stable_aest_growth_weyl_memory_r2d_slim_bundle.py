#!/usr/bin/env python3
from __future__ import annotations

import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
WORK = RESULTS / "stable_aest_growth_weyl_memory_r2d_work"
OUT = RESULTS / "stable_aest_growth_weyl_memory_r2d_full_history_slim_bundle.zip"
MANIFEST = RESULTS / "stable_aest_growth_weyl_memory_r2d_slim_manifest.json"

INCLUDE = [
    RESULTS / "stable_aest_growth_weyl_memory_r2d_full_history.json",
    RESULTS / "stable_aest_growth_weyl_memory_r2d_full_history.npz",
    RESULTS / "stable_aest_growth_weyl_memory_r2d_full_history.log",
    RESULTS / "stable_aest_growth_weyl_memory_r2d_full_history_FULL_runner.log",
    ROOT / "docs/stable_aest_growth_weyl_memory_r2d_full_history_predata.md",
    ROOT / "docs/stable_aest_growth_weyl_memory_r2d_full_history_postdata.md",
    ROOT / "docs/stable_aest_growth_weyl_memory_r2d_runtime_repair_01.md",
    ROOT / "docs/stable_aest_growth_weyl_memory_r2c_normalization_postdata.md",
    ROOT / "fullj_weyl/stable_aest_growth_weyl_memory_r2d_full_history.py",
    ROOT / "fullj_weyl/run_local_stable_aest_growth_weyl_memory_r2d_full_history.sh",
    ROOT / "fullj_weyl/apply_stable_aest_r2d_full_history_patch.py",
    ROOT / "fullj_weyl/apply_stable_aest_r2b_variational_patch.py",
    RESULTS / "stable_aest_growth_weyl_memory_r2c_normalization.json",
    RESULTS / "stable_aest_growth_weyl_memory_r2b_variational.json",
    RESULTS / "stable_aest_growth_weyl_memory_r2.npz",
    RESULTS / "stable_aest_finite_memory_r1c.json",
    RESULTS / "fullj_aest_stable_chi_precision_floor.json",
    RESULTS / "nl1c6d2n_corrected_class_densek64_env.sh",
]


def relpath(p: Path) -> str:
    try:
        return str(p.relative_to(ROOT))
    except ValueError:
        return str(p)


def main() -> int:
    required = [
        RESULTS / "stable_aest_growth_weyl_memory_r2d_full_history.json",
        RESULTS / "stable_aest_growth_weyl_memory_r2d_full_history.npz",
        RESULTS / "stable_aest_growth_weyl_memory_r2d_full_history.log",
    ]
    missing = [str(p) for p in required if not p.is_file()]
    if missing:
        raise SystemExit("missing completed R2d artifacts: " + repr(missing))

    omitted = []
    omitted_bytes = 0
    if WORK.exists():
        for p in sorted(WORK.rglob("*")):
            if not p.is_file():
                continue
            n = p.stat().st_size
            omitted_bytes += n
            omitted.append({"path": relpath(p), "bytes": n})

    manifest = {
        "classification_source": "results/stable_aest_growth_weyl_memory_r2d_full_history.json",
        "bundle_policy": "compact scientific/reproducibility artifacts only; generated R2d work tables omitted",
        "omitted_work_file_count": len(omitted),
        "omitted_work_total_bytes": omitted_bytes,
        "omitted_work_total_MiB": omitted_bytes / (1024.0 * 1024.0),
        "omitted_work_files": omitted,
        "regeneration": "Run fullj_weyl/run_local_stable_aest_growth_weyl_memory_r2d_full_history.sh to regenerate omitted intermediates.",
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")

    files = [p for p in INCLUDE if p.is_file()] + [MANIFEST]
    if OUT.exists():
        OUT.unlink()
    with zipfile.ZipFile(OUT, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        seen = set()
        for p in files:
            rp = relpath(p)
            if rp in seen:
                continue
            zf.write(p, arcname=rp)
            seen.add(rp)

    print(f"STABLE_AEST_GROWTH_WEYL_MEMORY_R2D_SLIM_BUNDLE={relpath(OUT)}")
    print(f"STABLE_AEST_GROWTH_WEYL_MEMORY_R2D_SLIM_SIZE_BYTES={OUT.stat().st_size}")
    print(f"STABLE_AEST_GROWTH_WEYL_MEMORY_R2D_OMITTED_WORK_MIB={manifest['omitted_work_total_MiB']:.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
