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

R5_EXECUTED_HEAD = "9d719245f3e63e3e6646fd87f8f49ef91697b269"
R6_PREDATA_COMMIT = "d4b83118a384f9e91167484cbb52bc98c5f2f7d3"
CLASS_SHA = "e85808324f51fc694d12e3ed7439552a3c3f9540"

KB = 0.0665
TAUH0 = 1.0
MEMORY_ORDER = 39
THEORY_LMAX = 4000
TRIM_LMAX = 2998
ACT_REQUIRED_LMAX = 2999
ETA0_REG_GATE = 1.0e-8
ETA_GRID = np.asarray(
    [0.0, 1.0/256.0, 1.0/128.0, 1.0/64.0, 1.0/32.0, 1.0/16.0, 1.0/8.0],
    dtype=float,
)

START = {
    "H0": 67.3324639084866,
    "omega_b": 0.022377376877682164,
    "omega_cdm": 0.12006705327635288,
    "tau_reio": 0.06174082364515668,
    "n_s": 0.9666229454895277,
    "A_s": 2.1308864352626987e-9,
}

COMPLETE_LABEL = "ACT_DR6_LENSING_EXPLORATORY_R6_LINEAR_ETA_SCAN_COMPLETE"
INCOMPLETE_LABEL = "ACT_DR6_LENSING_EXPLORATORY_R6_LINEAR_ETA_SCAN_INCOMPLETE"


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


def rewrite_ini(text: str, root: str, memory_enabled: bool, eta: float) -> str:
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
            # R6 inherits the R5 certified linear-only lensing path.
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
        "# ACT DR6 exploratory R6: R5-certified linear lensing eta scan",
        f"aest_memory_enabled = {'yes' if memory_enabled else 'no'}",
        f"aest_memory_order = {MEMORY_ORDER}",
        f"aest_eta = {float(eta):.17g}",
        f"aest_tau_H0 = {TAUH0:.17g}",
    ]
    return "\n".join(out) + "\n"


def run_class(class_root: Path, memory_enabled: bool, eta: float, label: str) -> Path:
    outdir = class_root / "output"
    outdir.mkdir(parents=True, exist_ok=True)
    ini = class_root / f"obs_act_r6_{label}.ini"
    root = f"output/obs_act_r6_{label}_"
    ini.write_text(rewrite_ini(BASE_INI.read_text(), root, memory_enabled, eta))

    env = os.environ.copy()
    env["OMP_NUM_THREADS"] = "1"
    for name in (
        "AEST_TANGENT_FORCE_FILE",
        "AEST_TANGENT_LAMBDA",
        "AEST_TANGENT_TRACE_FILE",
        "AEST_OFFLINE_TRACE_FILE",
    ):
        env.pop(name, None)

    log = ROOT / "results" / f"act_dr6_r6_class_{label}.log"
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

    path = class_root / "output" / f"obs_act_r6_{label}__cl.dat"
    if not path.exists() or path.stat().st_size == 0:
        raise RuntimeError(f"CLASS _cl.dat missing for {label}: {path}")

    saved = ROOT / "results" / f"act_dr6_r6_{label}__cl.dat"
    shutil.copy2(path, saved)
    return saved


def load_linear_ckk(path: Path, label: str):
    arr = np.loadtxt(path)
    if arr.ndim != 2 or arr.shape[1] < 6:
        raise RuntimeError(f"CLASS pCl output missing phi-phi column: {path}, shape={arr.shape}")
    if not np.all(np.isfinite(arr[:, 0])):
        raise RuntimeError(f"non-finite CLASS ell column: {path}")

    ell_rows = np.asarray(arr[:, 0], dtype=int)
    dpp_rows = np.asarray(arr[:, 5], dtype=float)
    if ell_rows.size == 0 or int(ell_rows[-1]) < ACT_REQUIRED_LMAX:
        raise RuntimeError(
            f"CLASS lensing support ends at L={int(ell_rows[-1]) if ell_rows.size else -1} "
            f"< ACT required {ACT_REQUIRED_LMAX}"
        )

    expected = np.arange(2, ACT_REQUIRED_LMAX + 1, dtype=int)
    pos = {int(L): i for i, L in enumerate(ell_rows)}
    missing = [int(L) for L in expected if int(L) not in pos]
    if missing:
        raise RuntimeError(f"CLASS _cl.dat missing ACT multipoles: count={len(missing)}, first={missing[:30]}")

    idx = np.asarray([pos[int(L)] for L in expected], dtype=int)
    dpp = dpp_rows[idx]
    ckk_phys = (np.pi / 2.0) * expected * (expected + 1.0) * dpp

    bad = ~np.isfinite(ckk_phys)
    if np.any(bad):
        badell = expected[bad]
        raise FloatingPointError(
            f"nonfinite linear CLASS Ckk inside ACT support for {label}: "
            f"count={badell.size}, first={badell[:30].tolist()}"
        )
    zero = ckk_phys == 0.0
    if np.any(zero):
        zell = expected[zero]
        raise FloatingPointError(
            f"zero linear CLASS Ckk inside ACT support for {label}: "
            f"count={zell.size}, first={zell[:30].tolist()}"
        )

    ckk = np.zeros(ACT_REQUIRED_LMAX + 1, dtype=float)
    ckk[expected] = ckk_phys
    stats = {
        "ell_min": int(expected[0]),
        "ell_max": int(expected[-1]),
        "n_multipoles": int(expected.size),
        "ckk_min": float(np.min(ckk_phys)),
        "ckk_max": float(np.max(ckk_phys)),
        "dpp_min": float(np.min(dpp)),
        "dpp_max": float(np.max(dpp)),
    }
    print(
        f"R6_LINEAR_CKK_FINITE label={label} N={expected.size} "
        f"L={expected[0]}..{expected[-1]} min={stats['ckk_min']:.12e} "
        f"max={stats['ckk_max']:.12e}",
        flush=True,
    )
    return ckk, stats


def act_chi2(data, ckk):
    binmat = np.asarray(data["binmat_act"], dtype=float)
    ntheory = int(binmat.shape[1])
    if ckk.size < ntheory:
        raise RuntimeError(f"Ckk has {ckk.size} entries but ACT binmat needs {ntheory}")
    theory = np.asarray(ckk[:ntheory], dtype=float)
    binned = binmat @ theory
    obs = np.asarray(data["data_binned_clkk"], dtype=float)
    cinv = np.asarray(data["cinv"], dtype=float)
    delta = obs - binned
    chi2 = float(delta @ cinv @ delta)
    if not math.isfinite(chi2) or not np.all(np.isfinite(binned)):
        raise FloatingPointError("nonfinite ACT DR6 likelihood result")
    return chi2, binned


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--class-root", required=True)
    ap.add_argument("--json-out", default="results/act_dr6_lensing_exploratory_r6_linear_eta_scan.json")
    ap.add_argument("--npz-out", default="results/act_dr6_lensing_exploratory_r6_linear_eta_scan.npz")
    args = ap.parse_args()

    class_root = Path(args.class_root).resolve()
    jout = Path(args.json_out)
    nout = Path(args.npz_out)
    jout.parent.mkdir(parents=True, exist_ok=True)

    try:
        import act_dr6_lenslike as alike

        head = git_head()
        ancestry = {
            "r5_executed_head": is_ancestor(R5_EXECUTED_HEAD),
            "r6_predata": is_ancestor(R6_PREDATA_COMMIT),
        }
        print("ACT_DR6_LENSING_EXPLORATORY_R6_LINEAR_ETA_SCAN_START", flush=True)
        print("HEAD=" + head, flush=True)
        print("ANCESTRY=" + json.dumps(ancestry, sort_keys=True), flush=True)
        print("THEORY=linear", flush=True)
        print(f"MODEL KB={KB} tauH0={TAUH0} memory_order={MEMORY_ORDER}", flush=True)
        print("ETA_GRID=" + ",".join(f"{x:.12e}" for x in ETA_GRID), flush=True)
        print("LIKELIHOOD variant=act_baseline lens_only=True corrections=False data=v1.2", flush=True)

        if not all(ancestry.values()):
            raise RuntimeError(f"required ancestry missing: {ancestry}")
        if not (class_root / "class").exists():
            raise RuntimeError(f"CLASS executable missing: {class_root/'class'}")

        data = alike.load_data(
            "act_baseline",
            lens_only=True,
            like_corrections=False,
            trim_lmax=TRIM_LMAX,
            version="v1.2",
        )
        print(f"ACT_DR6_NBINS={len(data['data_binned_clkk'])}", flush=True)

        off_path = run_class(class_root, False, 0.0, "eta0_off")
        ckk_off, stats_off = load_linear_ckk(off_path, "eta0_off")
        on0_path = run_class(class_root, True, 0.0, "eta0_on")
        ckk_0, stats_0 = load_linear_ckk(on0_path, "eta0_on")
        reg = rel_l2(ckk_off[2:], ckk_0[2:])
        reg_pass = bool(reg <= ETA0_REG_GATE)
        print(f"R6_ETA0_MEMORY_ON_OFF_CLKK_REL_L2={reg:.12e} gate={ETA0_REG_GATE:.1e} pass={reg_pass}", flush=True)
        if not reg_pass:
            raise RuntimeError(f"eta0 memory on/off linear Ckk regression failed: {reg}")

        rows = []
        spectra = []
        binned_all = []
        for i, eta in enumerate(ETA_GRID):
            if i == 0:
                ckk = ckk_0
                stats = stats_0
            else:
                path = run_class(class_root, True, float(eta), f"eta_{i:02d}")
                ckk, stats = load_linear_ckk(path, f"eta_{i:02d}")
            chi2, binned = act_chi2(data, ckk)
            shift = rel_l2(ckk[2:], ckk_0[2:])
            row = {
                "index": int(i),
                "eta": float(eta),
                "chi2": float(chi2),
                "spectrum_rel_l2_vs_eta0": float(shift),
                "ckk_min": float(stats["ckk_min"]),
                "ckk_max": float(stats["ckk_max"]),
            }
            rows.append(row)
            spectra.append(ckk)
            binned_all.append(binned)
            print(
                f"ACT_DR6_POINT {i+1:02d}/{len(ETA_GRID):02d} "
                f"eta={eta:.12e} chi2={chi2:.12e} relL2={shift:.12e}",
                flush=True,
            )

        chi0 = rows[0]["chi2"]
        for row in rows:
            row["delta_chi2_vs_eta0"] = float(row["chi2"] - chi0)
        best = min(rows, key=lambda x: x["chi2"])
        best_summary = {
            "grid_index": int(best["index"]),
            "eta": float(best["eta"]),
            "chi2": float(best["chi2"]),
            "delta_chi2_vs_eta0": float(best["delta_chi2_vs_eta0"]),
        }

        np.savez_compressed(
            nout,
            eta=ETA_GRID,
            ell=np.arange(ACT_REQUIRED_LMAX + 1, dtype=int),
            clkk=np.stack(spectra),
            binned_theory=np.stack(binned_all),
            data_binned_clkk=np.asarray(data["data_binned_clkk"], dtype=float),
            bcents_act=np.asarray(data["bcents_act"], dtype=float),
            chi2=np.asarray([r["chi2"] for r in rows], dtype=float),
            delta_chi2=np.asarray([r["delta_chi2_vs_eta0"] for r in rows], dtype=float),
            spectrum_rel_l2=np.asarray([r["spectrum_rel_l2_vs_eta0"] for r in rows], dtype=float),
        )

        result = {
            "classification": COMPLETE_LABEL,
            "exploratory": True,
            "historical_D2C6H_remains_formal_FAIL": True,
            "historical_R4_remains_incomplete": True,
            "R5_linear_baseline_passed": True,
            "nonlinear_halofit_interface_resolved": False,
            "observational_claim_licensed": False,
            "head": head,
            "ancestry": ancestry,
            "class_upstream_sha": CLASS_SHA,
            "class_execution_path": "executable + v019p/pre/p3.pre + _cl.dat phi-phi column",
            "likelihood": {
                "package": "act_dr6_lenslike",
                "package_version_frozen": "1.2.1",
                "data_version": "v1.2",
                "variant": "act_baseline",
                "lens_only": True,
                "like_corrections": False,
                "trim_lmax": TRIM_LMAX,
            },
            "theory": {
                "KB": KB,
                "tauH0": TAUH0,
                "memory_order": MEMORY_ORDER,
                "lmax_scalars": THEORY_LMAX,
                "nonlinear": None,
                "ckk_from_class_file": "(pi/2)*L*(L+1)*D_L_phiphi",
                "direct_R2_H_quadratic_metric_stress_in_linear_CLASS": False,
            },
            "eta_grid": ETA_GRID.tolist(),
            "eta0_memory_off": stats_off,
            "eta0_memory_on": stats_0,
            "eta0_memory_on_off_clkk_rel_l2": reg,
            "eta0_regression_gate": ETA0_REG_GATE,
            "eta0_regression_pass": reg_pass,
            "points": rows,
            "best_grid_point": best_summary,
            "interpretation_scope": (
                "Exploratory ACT DR6 standalone lensing scan in linear CLASS theory only. "
                "No physical ACT constraint or detection is licensed because the AeST-specific "
                "nonlinear/Halofit lensing interface remains unresolved and D2C6H remains a formal FAIL."
            ),
        }
        jout.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")

        print(
            "BEST_GRID_POINT=" + json.dumps(best_summary, sort_keys=True, separators=(",", ":")),
            flush=True,
        )
        print("CLASSIFICATION=" + COMPLETE_LABEL, flush=True)
        print("OBSERVATIONAL_CLAIM_LICENSED=False", flush=True)
        print("ACT_DR6_LENSING_EXPLORATORY_R6_LINEAR_ETA_SCAN_END", flush=True)
        return 0

    except Exception as exc:
        result = {
            "classification": INCOMPLETE_LABEL,
            "exploratory": True,
            "historical_D2C6H_remains_formal_FAIL": True,
            "historical_R4_remains_incomplete": True,
            "nonlinear_halofit_interface_resolved": False,
            "observational_claim_licensed": False,
            "error_type": type(exc).__name__,
            "error": str(exc),
        }
        jout.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print(f"ACT_DR6_R6_ERROR {type(exc).__name__}: {exc}", flush=True)
        print("CLASSIFICATION=" + INCOMPLETE_LABEL, flush=True)
        print("OBSERVATIONAL_CLAIM_LICENSED=False", flush=True)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
