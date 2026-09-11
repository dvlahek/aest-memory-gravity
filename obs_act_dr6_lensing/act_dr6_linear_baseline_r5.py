#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
BASE_INI = ROOT / "v019/ini/aest_exp.ini"
PRECISION = ROOT / "v019p/pre/p3.pre"

R4_EXECUTED_HEAD = "ee1522237fa8ef9ecb4099e4e2e9576e16488a5d"
R5_PREDATA_COMMIT = "437d7cd76289e0408d479ddca60a1ed4bc050f0a"
CLASS_SHA = "e85808324f51fc694d12e3ed7439552a3c3f9540"

KB = 0.0665
TAUH0 = 1.0
MEMORY_ORDER = 39
THEORY_LMAX = 4000
ACT_REQUIRED_LMAX = 2999
ETA0_REG_GATE = 1.0e-8

START = {
    "H0": 67.3324639084866,
    "omega_b": 0.022377376877682164,
    "omega_cdm": 0.12006705327635288,
    "tau_reio": 0.06174082364515668,
    "n_s": 0.9666229454895277,
    "A_s": 2.1308864352626987e-9,
}

PASS_LABEL = "ACT_DR6_LENSING_EXPLORATORY_R5_LINEAR_BASELINE_PASS"
FAIL_LABEL = "ACT_DR6_LENSING_EXPLORATORY_R5_LINEAR_BASELINE_FAIL"


def git_head() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()


def is_ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0


def rel_l2(a, b) -> float:
    aa = np.asarray(a, dtype=float)
    bb = np.asarray(b, dtype=float)
    return float(np.linalg.norm(aa - bb) / max(np.linalg.norm(aa), np.linalg.norm(bb), 1.0e-300))


def rewrite_ini(text: str, root: str, memory_enabled: bool) -> str:
    replacements = dict(START)
    replacements["aest_KB"] = KB
    out = []
    seen = set()
    flags = {"output": False, "lensing": False, "lmax": False}
    drop_keys = {
        "aest_memory_enabled",
        "aest_memory_order",
        "aest_eta",
        "aest_tau_H0",
        "z_max_pk",
        "P_k_max_h/Mpc",
    }

    for line in text.splitlines():
        st = line.strip()
        key = st.split("=", 1)[0].strip() if "=" in st else None
        if key in drop_keys:
            continue
        if key == "non linear":
            # R5 single frozen technical change: linear CLASS lensing only.
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
        "# ACT DR6 exploratory R5: linear baseline recertification only",
        f"aest_memory_enabled = {'yes' if memory_enabled else 'no'}",
        f"aest_memory_order = {MEMORY_ORDER}",
        "aest_eta = 0",
        f"aest_tau_H0 = {TAUH0:.17g}",
    ]
    return "\n".join(out) + "\n"


def run_class(class_root: Path, memory_enabled: bool, label: str) -> Path:
    outdir = class_root / "output"
    outdir.mkdir(parents=True, exist_ok=True)
    ini = class_root / f"obs_act_r5_{label}.ini"
    root = f"output/obs_act_r5_{label}_"
    ini.write_text(rewrite_ini(BASE_INI.read_text(), root, memory_enabled))

    env = os.environ.copy()
    env["OMP_NUM_THREADS"] = "1"
    for name in (
        "AEST_TANGENT_FORCE_FILE",
        "AEST_TANGENT_LAMBDA",
        "AEST_TANGENT_TRACE_FILE",
        "AEST_OFFLINE_TRACE_FILE",
    ):
        env.pop(name, None)

    log = ROOT / "results" / f"act_dr6_r5_class_{label}.log"
    with log.open("w") as fh:
        proc = subprocess.run(
            [str(class_root / "class"), ini.name, str(PRECISION)],
            cwd=class_root,
            env=env,
            stdout=fh,
            stderr=subprocess.STDOUT,
        )
    if proc.returncode != 0:
        tail = "\n".join(log.read_text(errors="replace").splitlines()[-50:])
        raise RuntimeError(f"CLASS executable failed for {label} with code {proc.returncode}:\n{tail}")

    path = class_root / "output" / f"obs_act_r5_{label}__cl.dat"
    if not path.exists() or path.stat().st_size == 0:
        raise RuntimeError(f"CLASS _cl.dat missing for {label}: {path}")

    saved = ROOT / "results" / f"act_dr6_r5_{label}__cl.dat"
    shutil.copy2(path, saved)
    return saved


def load_linear_ckk(path: Path, label: str):
    arr = np.loadtxt(path)
    if arr.ndim != 2 or arr.shape[1] < 6:
        raise RuntimeError(f"CLASS pCl output missing phi-phi column: {path}, shape={arr.shape}")
    if not np.all(np.isfinite(arr[:, 0])):
        raise RuntimeError(f"non-finite CLASS ell column: {path}")

    ell = np.asarray(arr[:, 0], dtype=int)
    dpp = np.asarray(arr[:, 5], dtype=float)
    if ell.size == 0 or int(ell[-1]) < ACT_REQUIRED_LMAX:
        raise RuntimeError(
            f"CLASS lensing support ends at L={int(ell[-1]) if ell.size else -1} "
            f"< ACT required {ACT_REQUIRED_LMAX}"
        )

    expected = np.arange(2, ACT_REQUIRED_LMAX + 1, dtype=int)
    pos = {int(L): i for i, L in enumerate(ell)}
    missing = [int(L) for L in expected if int(L) not in pos]
    if missing:
        raise RuntimeError(f"CLASS _cl.dat missing ACT multipoles: count={len(missing)}, first={missing[:30]}")

    idx = np.asarray([pos[int(L)] for L in expected], dtype=int)
    dpp_act = dpp[idx]
    ckk = (np.pi / 2.0) * expected * (expected + 1.0) * dpp_act

    bad = ~np.isfinite(ckk)
    if np.any(bad):
        badell = expected[bad]
        raise FloatingPointError(
            f"nonfinite linear CLASS Ckk inside ACT support for {label}: "
            f"count={badell.size}, first={badell[:30].tolist()}"
        )
    zero = ckk == 0.0
    if np.any(zero):
        zell = expected[zero]
        raise FloatingPointError(
            f"zero linear CLASS Ckk inside ACT support for {label}: "
            f"count={zell.size}, first={zell[:30].tolist()}"
        )

    stats = {
        "ell_min": int(expected[0]),
        "ell_max": int(expected[-1]),
        "n_multipoles": int(expected.size),
        "ckk_min": float(np.min(ckk)),
        "ckk_max": float(np.max(ckk)),
        "dpp_min": float(np.min(dpp_act)),
        "dpp_max": float(np.max(dpp_act)),
    }
    print(
        f"R5_LINEAR_CKK_FINITE label={label} N={expected.size} "
        f"L={expected[0]}..{expected[-1]} min={stats['ckk_min']:.12e} "
        f"max={stats['ckk_max']:.12e}",
        flush=True,
    )
    return expected, ckk, stats


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--class-root", required=True)
    ap.add_argument("--json-out", default="results/act_dr6_lensing_exploratory_r5_linear_baseline.json")
    ap.add_argument("--npz-out", default="results/act_dr6_lensing_exploratory_r5_linear_baseline.npz")
    args = ap.parse_args()

    class_root = Path(args.class_root).resolve()
    jout = Path(args.json_out)
    nout = Path(args.npz_out)
    jout.parent.mkdir(parents=True, exist_ok=True)

    try:
        head = git_head()
        ancestry = {
            "r4_executed_head": is_ancestor(R4_EXECUTED_HEAD),
            "r5_predata": is_ancestor(R5_PREDATA_COMMIT),
        }
        print("ACT_DR6_LENSING_EXPLORATORY_R5_LINEAR_BASELINE_START", flush=True)
        print("HEAD=" + head, flush=True)
        print("ANCESTRY=" + json.dumps(ancestry, sort_keys=True), flush=True)
        print("CLASS_PATH=CLI+p3.pre+_cl.dat", flush=True)
        print("THEORY=linear (non linear entry removed)", flush=True)
        print(f"MODEL KB={KB} tauH0={TAUH0} memory_order={MEMORY_ORDER}", flush=True)

        if not all(ancestry.values()):
            raise RuntimeError(f"required ancestry missing: {ancestry}")
        if not (class_root / "class").exists():
            raise RuntimeError(f"CLASS executable missing: {class_root/'class'}")

        off_path = run_class(class_root, False, "eta0_off")
        ell_off, ckk_off, stats_off = load_linear_ckk(off_path, "eta0_off")

        on_path = run_class(class_root, True, "eta0_on")
        ell_on, ckk_on, stats_on = load_linear_ckk(on_path, "eta0_on")

        if not np.array_equal(ell_off, ell_on):
            raise RuntimeError("eta0 memory off/on ell grids differ")

        reg = rel_l2(ckk_off, ckk_on)
        reg_pass = bool(reg <= ETA0_REG_GATE)
        print(f"R5_ETA0_MEMORY_ON_OFF_CLKK_REL_L2={reg:.12e} gate={ETA0_REG_GATE:.1e} pass={reg_pass}", flush=True)
        if not reg_pass:
            raise RuntimeError(f"eta0 memory on/off linear Ckk regression failed: {reg}")

        np.savez_compressed(
            nout,
            ell=ell_off,
            ckk_eta0_off=ckk_off,
            ckk_eta0_on=ckk_on,
            difference=ckk_on - ckk_off,
        )

        result = {
            "classification": PASS_LABEL,
            "exploratory": True,
            "historical_R4_remains_incomplete": True,
            "historical_D2C6H_remains_formal_FAIL": True,
            "linear_act_eta_scan_licensed": True,
            "observational_claim_licensed": False,
            "head": head,
            "ancestry": ancestry,
            "class_upstream_sha": CLASS_SHA,
            "class_execution_path": "executable + v019p/pre/p3.pre + _cl.dat phi-phi column",
            "theory": {
                "KB": KB,
                "tauH0": TAUH0,
                "memory_order": MEMORY_ORDER,
                "lmax_scalars": THEORY_LMAX,
                "nonlinear": None,
                "ckk_from_class_file": "(pi/2)*L*(L+1)*D_L_phiphi",
            },
            "act_support": {"physical_ell_min": 2, "ell_max": ACT_REQUIRED_LMAX},
            "eta0_memory_off": stats_off,
            "eta0_memory_on": stats_on,
            "eta0_memory_on_off_clkk_rel_l2": reg,
            "eta0_regression_gate": ETA0_REG_GATE,
            "eta0_regression_pass": reg_pass,
            "interpretation_scope": (
                "Linear-theory baseline recertification only. PASS licenses only a subsequent "
                "exploratory linear eta scan; the AeST nonlinear/Halofit lensing interface "
                "remains unresolved and no observational claim is licensed."
            ),
        }
        jout.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print("CLASSIFICATION=" + PASS_LABEL, flush=True)
        print("LINEAR_ACT_ETA_SCAN_LICENSED=True", flush=True)
        print("OBSERVATIONAL_CLAIM_LICENSED=False", flush=True)
        print("ACT_DR6_LENSING_EXPLORATORY_R5_LINEAR_BASELINE_END", flush=True)
        return 0

    except Exception as exc:
        result = {
            "classification": FAIL_LABEL,
            "exploratory": True,
            "historical_R4_remains_incomplete": True,
            "historical_D2C6H_remains_formal_FAIL": True,
            "linear_act_eta_scan_licensed": False,
            "observational_claim_licensed": False,
            "error_type": type(exc).__name__,
            "error": str(exc),
        }
        jout.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print(f"ACT_DR6_R5_ERROR {type(exc).__name__}: {exc}", flush=True)
        print("CLASSIFICATION=" + FAIL_LABEL, flush=True)
        print("LINEAR_ACT_ETA_SCAN_LICENSED=False", flush=True)
        print("OBSERVATIONAL_CLAIM_LICENSED=False", flush=True)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
