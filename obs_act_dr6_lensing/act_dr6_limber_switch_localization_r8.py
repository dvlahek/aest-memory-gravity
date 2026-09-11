#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path
import shutil
import subprocess

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
BASE_INI = ROOT / "v019/ini/aest_exp.ini"
PRECISION = ROOT / "v019p/pre/p3.pre"

R7_EXECUTED_BASE = "11cd00061979dce8d85966f6484d4b15c9e0a8a5"
R8_PREDATA_COMMIT = "8b5218e7a27b7ce2b4b634a1f890e1ce8c48aeaf"
CLASS_SHA = "e85808324f51fc694d12e3ed7439552a3c3f9540"

KB = 0.0665
TAUH0 = 1.0
MEMORY_ORDER = 39
ETA = 0.0
THEORY_LMAX = 4000
REQUIRED_LMAX = 2999

START = {
    "H0": 67.3324639084866,
    "omega_b": 0.022377376877682164,
    "omega_cdm": 0.12006705327635288,
    "tau_reio": 0.06174082364515668,
    "n_s": 0.9666229454895277,
    "A_s": 2.1308864352626987e-9,
    "aest_KB": KB,
}

CASES = [
    {"label": "switch10", "full_limber": True, "switch": 10},
    {"label": "switch40", "full_limber": True, "switch": 40},
    {"label": "switch100", "full_limber": True, "switch": 100},
    {"label": "full_limber_off", "full_limber": False, "switch": None},
]

COMPLETE_LABEL = "ACT_DR6_LENSING_EXPLORATORY_R8_LIMBER_SWITCH_LOCALIZATION_COMPLETE"
INCOMPLETE_LABEL = "ACT_DR6_LENSING_EXPLORATORY_R8_LIMBER_SWITCH_LOCALIZATION_INCOMPLETE"


def git_head() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()


def is_ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0


def rewrite_ini(text: str, root: str, full_limber: bool, switch: int | None) -> str:
    replacements = dict(START)
    out = []
    seen = set()
    flags = {"output": False, "lensing": False, "lmax": False}
    drop_keys = {
        "aest_enabled",
        "aest_memory_enabled",
        "aest_memory_order",
        "aest_eta",
        "aest_tau_H0",
        "want_lcmb_full_limber",
        "l_switch_limber",
        "z_max_pk",
        "P_k_max_h/Mpc",
        "P_k_max_1/Mpc",
    }

    for line in text.splitlines():
        st = line.strip()
        key = st.split("=", 1)[0].strip() if "=" in st else None
        if key in drop_keys:
            continue
        if key == "non linear":
            continue
        if key == "root":
            out.append(f"root = {root}")
        elif key == "output":
            out.append("output = tCl,pCl,lCl")
            flags["output"] = True
        elif key == "lensing":
            out.append("lensing = yes")
            flags["lensing"] = True
        elif key == "l_max_scalars":
            out.append(f"l_max_scalars = {THEORY_LMAX}")
            flags["lmax"] = True
        elif key in replacements:
            out.append(f"{key} = {replacements[key]:.17g}")
            seen.add(key)
        else:
            out.append(line)

    missing = set(replacements) - seen
    if missing:
        raise RuntimeError(f"missing CLASS parameters in base ini: {sorted(missing)}")
    if not flags["output"]:
        out.append("output = tCl,pCl,lCl")
    if not flags["lensing"]:
        out.append("lensing = yes")
    if not flags["lmax"]:
        out.append(f"l_max_scalars = {THEORY_LMAX}")

    out += [
        "# ACT DR6 exploratory R8: Limber-switch localization diagnostic",
        "aest_enabled = yes",
        "aest_memory_enabled = yes",
        f"aest_memory_order = {MEMORY_ORDER}",
        f"aest_eta = {ETA:.17g}",
        f"aest_tau_H0 = {TAUH0:.17g}",
        f"want_lcmb_full_limber = {'yes' if full_limber else 'no'}",
    ]
    if full_limber:
        if switch is None:
            raise RuntimeError("full-Limber case requires l_switch_limber")
        out.append(f"l_switch_limber = {int(switch)}")
    return "\n".join(out) + "\n"


def run_class(class_root: Path, spec: dict) -> Path:
    label = spec["label"]
    outdir = class_root / "output"
    outdir.mkdir(parents=True, exist_ok=True)
    ini = class_root / f"obs_act_r8_{label}.ini"
    root = f"output/obs_act_r8_{label}_"
    ini.write_text(rewrite_ini(BASE_INI.read_text(), root, bool(spec["full_limber"]), spec["switch"]))
    shutil.copy2(ini, ROOT / "results" / f"act_dr6_r8_{label}.ini")

    env = os.environ.copy()
    env["OMP_NUM_THREADS"] = "1"
    for name in (
        "AEST_TANGENT_FORCE_FILE",
        "AEST_TANGENT_LAMBDA",
        "AEST_TANGENT_TRACE_FILE",
        "AEST_OFFLINE_TRACE_FILE",
    ):
        env.pop(name, None)

    log = ROOT / "results" / f"act_dr6_r8_class_{label}.log"
    with log.open("w") as fh:
        proc = subprocess.run(
            [str(class_root / "class"), ini.name, str(PRECISION)],
            cwd=class_root,
            env=env,
            stdout=fh,
            stderr=subprocess.STDOUT,
        )
    if proc.returncode != 0:
        tail = "\n".join(log.read_text(errors="replace").splitlines()[-60:])
        raise RuntimeError(f"CLASS failed for {label} with code {proc.returncode}:\n{tail}")

    path = class_root / "output" / f"obs_act_r8_{label}__cl.dat"
    if not path.exists() or path.stat().st_size == 0:
        raise RuntimeError(f"CLASS _cl.dat missing for {label}: {path}")
    saved = ROOT / "results" / f"act_dr6_r8_{label}__cl.dat"
    shutil.copy2(path, saved)
    return saved


def load_ckk(path: Path, label: str):
    arr = np.loadtxt(path)
    if arr.ndim != 2 or arr.shape[1] < 6:
        raise RuntimeError(f"CLASS pCl output missing phi-phi column for {label}: shape={arr.shape}")
    ell_rows = np.asarray(arr[:, 0], dtype=int)
    dpp_rows = np.asarray(arr[:, 5], dtype=float)
    if ell_rows.size == 0 or int(ell_rows[-1]) < REQUIRED_LMAX:
        raise RuntimeError(f"{label}: lensing support ends below L={REQUIRED_LMAX}")

    expected = np.arange(2, REQUIRED_LMAX + 1, dtype=int)
    pos = {int(L): i for i, L in enumerate(ell_rows)}
    missing = [int(L) for L in expected if int(L) not in pos]
    if missing:
        raise RuntimeError(f"{label}: missing multipoles count={len(missing)}, first={missing[:20]}")
    idx = np.asarray([pos[int(L)] for L in expected], dtype=int)
    dpp = dpp_rows[idx]
    ckk_phys = (np.pi / 2.0) * expected * (expected + 1.0) * dpp

    if not np.all(np.isfinite(ckk_phys)):
        bad = expected[~np.isfinite(ckk_phys)]
        raise FloatingPointError(f"{label}: nonfinite Ckk, first={bad[:20].tolist()}")
    if np.any(ckk_phys == 0.0):
        bad = expected[ckk_phys == 0.0]
        raise FloatingPointError(f"{label}: zero Ckk, first={bad[:20].tolist()}")

    ckk = np.zeros(REQUIRED_LMAX + 1, dtype=float)
    ckk[expected] = ckk_phys
    stats = {
        "ell_min": 2,
        "ell_max": REQUIRED_LMAX,
        "n_multipoles": int(expected.size),
        "ckk_min": float(np.min(ckk_phys)),
        "ckk_max": float(np.max(ckk_phys)),
    }
    print(
        f"R8_CKK_FINITE label={label} N={expected.size} L=2..{REQUIRED_LMAX} "
        f"min={stats['ckk_min']:.12e} max={stats['ckk_max']:.12e}",
        flush=True,
    )
    return ckk, stats


def jump_diag(ckk: np.ndarray, s: int) -> dict:
    vals = {str(L): float(ckk[L]) for L in range(max(2, s - 2), s + 4)}
    before = float(ckk[s] / ckk[s - 1])
    jump = float(ckk[s + 1] / ckk[s])
    normalized = float(jump / before)
    return {
        "switch": int(s),
        "C_s_minus_1": float(ckk[s - 1]),
        "C_s": float(ckk[s]),
        "C_s_plus_1": float(ckk[s + 1]),
        "background_ratio_B": before,
        "adjacent_ratio_J": jump,
        "normalized_jump_J_over_B": normalized,
        "local_values": vals,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--class-root", required=True)
    ap.add_argument("--json-out", default="results/act_dr6_lensing_exploratory_r8_limber_switch_localization.json")
    ap.add_argument("--npz-out", default="results/act_dr6_lensing_exploratory_r8_limber_switch_localization.npz")
    args = ap.parse_args()

    class_root = Path(args.class_root).resolve()
    jout = Path(args.json_out)
    nout = Path(args.npz_out)
    jout.parent.mkdir(parents=True, exist_ok=True)

    try:
        head = git_head()
        ancestry = {
            "r7_executed_base": is_ancestor(R7_EXECUTED_BASE),
            "r8_predata": is_ancestor(R8_PREDATA_COMMIT),
        }
        print("ACT_DR6_LENSING_EXPLORATORY_R8_LIMBER_SWITCH_LOCALIZATION_START", flush=True)
        print("HEAD=" + head, flush=True)
        print("ANCESTRY=" + json.dumps(ancestry, sort_keys=True), flush=True)
        print(f"MODEL AeST Exp KB={KB} tauH0={TAUH0} memory_order={MEMORY_ORDER} eta={ETA}", flush=True)
        print("THEORY=linear", flush=True)
        print("CASES=switch10,switch40,switch100,full_limber_off", flush=True)

        if not all(ancestry.values()):
            raise RuntimeError(f"required ancestry missing: {ancestry}")
        if not (class_root / "class").exists():
            raise RuntimeError(f"CLASS executable missing: {class_root/'class'}")

        spectra = {}
        rows = []
        for spec in CASES:
            label = spec["label"]
            path = run_class(class_root, spec)
            ckk, stats = load_ckk(path, label)
            spectra[label] = ckk
            if spec["full_limber"]:
                s = int(spec["switch"])
                diag = jump_diag(ckk, s)
                print(
                    f"R8_SWITCH label={label} s={s} "
                    f"B={diag['background_ratio_B']:.12e} "
                    f"J={diag['adjacent_ratio_J']:.12e} "
                    f"J_over_B={diag['normalized_jump_J_over_B']:.12e}",
                    flush=True,
                )
                diagnostics = {str(s): diag}
            else:
                diagnostics = {}
                for s in (10, 40, 100):
                    diag = jump_diag(ckk, s)
                    diagnostics[str(s)] = diag
                    print(
                        f"R8_OFF_DIAG s={s} B={diag['background_ratio_B']:.12e} "
                        f"J={diag['adjacent_ratio_J']:.12e} "
                        f"J_over_B={diag['normalized_jump_J_over_B']:.12e}",
                        flush=True,
                    )
            rows.append({
                "label": label,
                "full_limber": bool(spec["full_limber"]),
                "l_switch_limber": spec["switch"],
                "spectrum": stats,
                "diagnostics": diagnostics,
            })

        result = {
            "classification": COMPLETE_LABEL,
            "observational_claim_licensed": False,
            "exploratory": True,
            "head": head,
            "ancestry": ancestry,
            "class_upstream_sha": CLASS_SHA,
            "model": {
                "aest_enabled": True,
                "aest_model": "Exp",
                "KB": KB,
                "tauH0": TAUH0,
                "memory_order": MEMORY_ORDER,
                "eta": ETA,
                "theory": "linear",
            },
            "cases": rows,
            "interpretation_scope": "Numerical localization of the CLASS full-Limber transition only; no ACT observational claim is licensed.",
        }
        jout.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")

        save = {"ell": np.arange(REQUIRED_LMAX + 1, dtype=int)}
        for label, ckk in spectra.items():
            save[f"clkk_{label}"] = ckk
        np.savez_compressed(nout, **save)

        print("CLASSIFICATION=" + COMPLETE_LABEL, flush=True)
        print("OBSERVATIONAL_CLAIM_LICENSED=False", flush=True)
        print("ACT_DR6_LENSING_EXPLORATORY_R8_LIMBER_SWITCH_LOCALIZATION_END", flush=True)
        return 0

    except Exception as exc:
        result = {
            "classification": INCOMPLETE_LABEL,
            "observational_claim_licensed": False,
            "error": f"{type(exc).__name__}: {exc}",
        }
        jout.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print("R8_ERROR=" + result["error"], flush=True)
        print("CLASSIFICATION=" + INCOMPLETE_LABEL, flush=True)
        print("OBSERVATIONAL_CLAIM_LICENSED=False", flush=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
