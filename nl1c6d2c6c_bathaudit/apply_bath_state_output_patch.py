#!/usr/bin/env python3
from pathlib import Path
import argparse
import json

ORDER = 39


def replace_once(path: Path, old: str, new: str, label: str) -> None:
    text = path.read_text()
    n = text.count(old)
    if n != 1:
        raise RuntimeError(f"{label}: expected exactly one anchor, found {n} in {path}")
    path.write_text(text.replace(old, new, 1))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("class_root")
    args = ap.parse_args()
    root = Path(args.class_root).resolve()
    pc = root / "source" / "perturbations.c"
    if not pc.exists():
        raise SystemExit("Not a patched CLASS source root")

    cond = "pba->aest_enabled && pba->aest_memory_enabled"
    title_anchor = '      class_store_columntitle(ppt->scalar_titles,"eta0_tangent_force_aest",pba->aest_enabled && pba->aest_memory_enabled);\n'
    titles = title_anchor
    for j in range(ORDER):
        titles += f'      class_store_columntitle(ppt->scalar_titles,"mem_q_aest_{j:02d}",{cond});\n'
    for j in range(ORDER):
        titles += f'      class_store_columntitle(ppt->scalar_titles,"mem_p_aest_{j:02d}",{cond});\n'
    replace_once(pc, title_anchor, titles, "bath-state output titles")

    data_anchor = '''      class_store_double(dataptr,\n                         eta0_tangent_force_aest,\n                         pba->aest_enabled && pba->aest_memory_enabled,\n                         storeidx);\n    }\n'''
    data = data_anchor
    for j in range(ORDER):
        data += (
            '    class_store_double(dataptr,\n'
            f'                       {cond} ? y[ppw->pv->index_pt_mem_q_aest+{j}] : 0.,\n'
            f'                       {cond},\n'
            '                       storeidx);\n'
        )
    for j in range(ORDER):
        data += (
            '    class_store_double(dataptr,\n'
            f'                       {cond} ? y[ppw->pv->index_pt_mem_p_aest+{j}] : 0.,\n'
            f'                       {cond},\n'
            '                       storeidx);\n'
        )
    replace_once(pc, data_anchor, data, "bath-state output data")

    text = pc.read_text()
    checks = {
        "q_titles_39": all(f'"mem_q_aest_{j:02d}"' in text for j in range(ORDER)),
        "p_titles_39": all(f'"mem_p_aest_{j:02d}"' in text for j in range(ORDER)),
        "q_state_reads_39": all(f'index_pt_mem_q_aest+{j}' in text for j in range(ORDER)),
        "p_state_reads_39": all(f'index_pt_mem_p_aest+{j}' in text for j in range(ORDER)),
        "physical_closure_unchanged": 'Bchi_aest *= pba->aest_eta' in text,
        "bath_dynamics_unchanged": '-2.*a_prime_over_a*pj-a*a*omega_j*omega_j*qj' in text,
    }
    if not all(checks.values()):
        raise RuntimeError(f"bath-state output patch audit failed: {checks}")

    repo = Path(__file__).resolve().parents[1]
    (repo / "results").mkdir(exist_ok=True)
    report = {
        "classification": "C3_BATH_STATE_OUTPUT_PATCH_READY",
        "physics_modified": False,
        "bath_order": ORDER,
        "checks": checks,
    }
    (repo / "results" / "c3_bath_state_output_patch.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
