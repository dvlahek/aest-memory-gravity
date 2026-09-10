#!/usr/bin/env python3
from pathlib import Path
import argparse


def replace_once(path: Path, old: str, new: str, label: str) -> None:
    text = path.read_text()
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one anchor, found {count} in {path}")
    path.write_text(text.replace(old, new, 1))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("class_root")
    args = ap.parse_args()
    root = Path(args.class_root).resolve()
    pc = root / "source" / "perturbations.c"
    if not pc.exists():
        raise SystemExit("Not a CLASS source root")

    old_titles = '''      /* Cold dark matter */\n      class_store_columntitle(ppt->scalar_titles,"delta_cdm",pba->has_cdm);\n      class_store_columntitle(ppt->scalar_titles,"theta_cdm",pba->has_cdm);\n'''
    new_titles = '''      /* Cold dark matter / AeST effective component */\n      class_store_columntitle(ppt->scalar_titles,"delta_cdm",pba->has_cdm);\n      class_store_columntitle(ppt->scalar_titles,"theta_cdm",pba->has_cdm);\n      /* D2C6A instrumentation only: expose already-evolved AeST states. */\n      class_store_columntitle(ppt->scalar_titles,"alpha_aest",pba->aest_enabled);\n      class_store_columntitle(ppt->scalar_titles,"E_aest",pba->aest_enabled);\n'''
    replace_once(pc, old_titles, new_titles, "AeST scalar output titles")

    old_data = '''    /* Cold dark matter */\n    class_store_double(dataptr, delta_cdm, pba->has_cdm, storeidx);\n    class_store_double(dataptr, theta_cdm, pba->has_cdm, storeidx);\n'''
    new_data = '''    /* Cold dark matter / AeST effective component */\n    class_store_double(dataptr, delta_cdm, pba->has_cdm, storeidx);\n    class_store_double(dataptr, theta_cdm, pba->has_cdm, storeidx);\n    /* D2C6A instrumentation only: no reconstruction or dynamics change. */\n    class_store_double(dataptr,\n                       pba->aest_enabled ? y[ppw->pv->index_pt_alpha_aest] : 0.,\n                       pba->aest_enabled,\n                       storeidx);\n    class_store_double(dataptr,\n                       pba->aest_enabled ? y[ppw->pv->index_pt_E_aest] : 0.,\n                       pba->aest_enabled,\n                       storeidx);\n'''
    replace_once(pc, old_data, new_data, "AeST scalar output data")

    text = pc.read_text()
    checks = {
        "alpha_title": '"alpha_aest",pba->aest_enabled' in text,
        "E_title": '"E_aest",pba->aest_enabled' in text,
        "alpha_state": 'y[ppw->pv->index_pt_alpha_aest]' in text,
        "E_state": 'y[ppw->pv->index_pt_E_aest]' in text,
    }
    if not all(checks.values()):
        raise RuntimeError(f"instrumentation post-check failed: {checks}")
    print("D2C6A_AEST_STATE_OUTPUT_PATCH_PASS")
    for key, value in checks.items():
        print(f"{key}={value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
