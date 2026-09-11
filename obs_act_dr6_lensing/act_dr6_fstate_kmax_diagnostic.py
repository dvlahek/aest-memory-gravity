#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import os
import shutil
import subprocess
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
BASE_INI = ROOT / "v019/ini/aest_exp.ini"
BASE_PRECISION = ROOT / "v019p/pre/p3.pre"
FSTATE_BASE = "15c70257a7aec84da5ad0fe628ecf5c91dab5cfe"
PREDATA = "905d65ed7cd28778a920e48304e9a85a8e998177"
CLASS_SHA = "e85808324f51fc694d12e3ed7439552a3c3f9540"
KB = 0.0665
TAUH0 = 1.0
MEMORY_ORDER = 39
THEORY_LMAX = 4000
LMAX_DIAG = 2999
KMAX_GRID = np.asarray([2.4, 3.0, 4.0, 5.0], dtype=float)
LPOINTS = np.asarray([10,20,50,100,200,500,700,1000,1500,2000,2500,2999], dtype=int)
START = dict(
    H0=67.3324639084866,
    omega_b=0.022377376877682164,
    omega_cdm=0.12006705327635288,
    tau_reio=0.06174082364515668,
    n_s=0.9666229454895277,
    A_s=2.1308864352626987e-9,
)


def git_head() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()


def ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"], cwd=ROOT,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    ).returncode == 0


def rel_l2(a, b) -> float:
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    return float(np.linalg.norm(a-b) / max(np.linalg.norm(a), np.linalg.norm(b), 1e-300))


def tag(kmax: float) -> str:
    return (f"{kmax:.1f}").replace(".", "p")


def make_pre(kmax: float) -> Path:
    p = ROOT / "results" / f"act_dr6_fs_kdiag_k{tag(kmax)}.pre"
    p.write_text(
        BASE_PRECISION.read_text().rstrip()
        + f"\n\n# nonredundant F-state high-k diagnostic\n"
        + f"k_max_tau0_over_l_max = {float(kmax):.17g}\n"
    )
    return p


def make_ini(text: str, root: str) -> str:
    repl = dict(START)
    repl["aest_KB"] = KB
    drop = {
        "aest_enabled", "aest_memory_enabled", "aest_memory_order", "aest_eta", "aest_tau_H0",
        "want_lcmb_full_limber", "l_switch_limber", "z_max_pk", "P_k_max_h/Mpc", "P_k_max_1/Mpc",
    }
    out = []
    seen = set()
    flags = {"output": False, "lensing": False, "lmax": False}
    for line in text.splitlines():
        st = line.strip()
        key = st.split("=", 1)[0].strip() if "=" in st else None
        if key in drop or key == "non linear":
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
        elif key in repl:
            out.append(f"{key} = {repl[key]:.17g}")
            seen.add(key)
        else:
            out.append(line)
    missing = set(repl) - seen
    if missing:
        raise RuntimeError(f"missing CLASS parameters: {sorted(missing)}")
    if not flags["output"]:
        out.append("output = tCl,pCl,lCl")
    if not flags["lensing"]:
        out.append("lensing = yes")
    if not flags["lmax"]:
        out.append(f"l_max_scalars = {THEORY_LMAX}")
    out += [
        "# nonredundant F-state high-k diagnostic",
        "aest_enabled = yes",
        "aest_memory_enabled = yes",
        f"aest_memory_order = {MEMORY_ORDER}",
        "aest_eta = 0",
        f"aest_tau_H0 = {TAUH0:.17g}",
        "want_lcmb_full_limber = no",
    ]
    return "\n".join(out) + "\n"


def run_class(class_root: Path, kmax: float) -> Path:
    ktag = tag(kmax)
    ini = class_root / f"obs_act_fs_kdiag_k{ktag}.ini"
    outroot = f"output/obs_act_fs_kdiag_k{ktag}_"
    ini.write_text(make_ini(BASE_INI.read_text(), outroot))
    shutil.copy2(ini, ROOT / "results" / f"act_dr6_fs_kdiag_k{ktag}.ini")
    pre = make_pre(kmax)
    env = os.environ.copy()
    env["OMP_NUM_THREADS"] = "1"
    for name in (
        "AEST_TANGENT_FORCE_FILE", "AEST_TANGENT_LAMBDA", "AEST_TANGENT_TRACE_FILE",
        "AEST_OFFLINE_TRACE_FILE", "AEST_TANGENT_ALLOW_K_MISS",
    ):
        env.pop(name, None)
    log = ROOT / "results" / f"act_dr6_fs_kdiag_class_k{ktag}.log"
    with log.open("w") as fh:
        proc = subprocess.run(
            [str(class_root / "class"), ini.name, str(pre)],
            cwd=class_root, env=env, stdout=fh, stderr=subprocess.STDOUT,
        )
    if proc.returncode:
        tail = "\n".join(log.read_text(errors="replace").splitlines()[-100:])
        raise RuntimeError(f"CLASS failed for kmax={kmax}:\n{tail}")
    src = class_root / "output" / f"obs_act_fs_kdiag_k{ktag}__cl.dat"
    if not src.exists() or not src.stat().st_size:
        raise RuntimeError(f"missing _cl.dat for kmax={kmax}")
    dst = ROOT / "results" / f"act_dr6_fs_kdiag_k{ktag}__cl.dat"
    shutil.copy2(src, dst)
    return dst


def load_ckk(path: Path, kmax: float):
    arr = np.loadtxt(path)
    if arr.ndim != 2 or arr.shape[1] < 6:
        raise RuntimeError(f"bad CLASS pCl shape for kmax={kmax}: {arr.shape}")
    ell_raw = np.asarray(arr[:, 0], int)
    dpp = np.asarray(arr[:, 5], float)
    ell = np.arange(2, LMAX_DIAG+1, dtype=int)
    pos = {int(L): i for i, L in enumerate(ell_raw)}
    if not ell_raw.size or int(ell_raw[-1]) < LMAX_DIAG or any(int(L) not in pos for L in ell):
        raise RuntimeError(f"kmax={kmax}: insufficient/missing L support")
    d = dpp[np.asarray([pos[int(L)] for L in ell])]
    ckk_phys = (np.pi/2.0) * ell * (ell+1) * d
    if not np.all(np.isfinite(ckk_phys)):
        raise FloatingPointError(f"kmax={kmax}: nonfinite Ckk")
    if np.any(ckk_phys <= 0):
        bad = ell[ckk_phys <= 0][:20].tolist()
        raise FloatingPointError(f"kmax={kmax}: non-positive Ckk first={bad}")
    ckk = np.zeros(LMAX_DIAG+1, float)
    ckk[ell] = ckk_phys
    summary = {
        "ell_min": 2,
        "ell_max": LMAX_DIAG,
        "n_multipoles": int(ell.size),
        "ckk_min": float(np.min(ckk_phys)),
        "ckk_max": float(np.max(ckk_phys)),
    }
    print(
        f"KDIAG_CKK_FINITE kmax={kmax:.1f} N={ell.size} L=2..{LMAX_DIAG} "
        f"min={summary['ckk_min']:.12e} max={summary['ckk_max']:.12e}", flush=True
    )
    return ckk, summary


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--class-root", required=True)
    ap.add_argument("--json-out", default="results/act_dr6_fstate_kmax_diagnostic.json")
    ap.add_argument("--npz-out", default="results/act_dr6_fstate_kmax_diagnostic.npz")
    args = ap.parse_args()
    class_root = Path(args.class_root).resolve()
    jout = Path(args.json_out)
    nout = Path(args.npz_out)
    jout.parent.mkdir(parents=True, exist_ok=True)

    try:
        head = git_head()
        anc = {"fstate_base": ancestor(FSTATE_BASE), "predata": ancestor(PREDATA)}
        print("ACT_DR6_FSTATE_KMAX_DIAGNOSTIC_START", flush=True)
        print("HEAD=" + head, flush=True)
        print("ANCESTRY=" + json.dumps(anc, sort_keys=True), flush=True)
        print(f"MODEL AeST Exp KB={KB} tauH0={TAUH0} memory_order={MEMORY_ORDER} eta=0", flush=True)
        print("NUMERICAL_REPRESENTATION=nonredundant_F_state", flush=True)
        print("FULL_LIMBER=False", flush=True)
        print("KMAX_GRID=" + ",".join(f"{x:.1f}" for x in KMAX_GRID), flush=True)
        if not all(anc.values()):
            raise RuntimeError(f"missing ancestry: {anc}")
        if not (class_root / "class").exists():
            raise RuntimeError("CLASS executable missing")

        spectra = []
        summaries = []
        for kmax in KMAX_GRID:
            p = run_class(class_root, float(kmax))
            c, s = load_ckk(p, float(kmax))
            spectra.append(c)
            summaries.append(s)
        spectra = np.stack(spectra)

        step_rows = []
        for i in range(1, len(KMAX_GRID)):
            r = rel_l2(spectra[i, 2:], spectra[i-1, 2:])
            row = {"from": float(KMAX_GRID[i-1]), "to": float(KMAX_GRID[i]), "rel_l2": float(r)}
            step_rows.append(row)
            print(f"KDIAG_STEP {KMAX_GRID[i-1]:.1f}->{KMAX_GRID[i]:.1f} relL2={r:.12e}", flush=True)

        rel_to_k5 = []
        for i, kmax in enumerate(KMAX_GRID):
            r = rel_l2(spectra[i, 2:], spectra[-1, 2:])
            rel_to_k5.append(float(r))
            print(f"KDIAG_TO_K5 kmax={kmax:.1f} relL2={r:.12e}", flush=True)

        point_rows = []
        logden = math.log(5.0/4.0)
        for L in LPOINTS:
            vals = spectra[:, int(L)]
            ratios = vals[1:] / vals[:-1]
            exponent45 = float(math.log(vals[-1]/vals[-2]) / logden)
            row = {
                "L": int(L),
                "Ckk": {f"k{tag(k)}": float(v) for k, v in zip(KMAX_GRID, vals)},
                "ratio_3_over_2p4": float(ratios[0]),
                "ratio_4_over_3": float(ratios[1]),
                "ratio_5_over_4": float(ratios[2]),
                "p_4_to_5": exponent45,
            }
            point_rows.append(row)
            print(
                f"KDIAG_POINT L={int(L)} r30_24={ratios[0]:.8f} r40_30={ratios[1]:.8f} "
                f"r50_40={ratios[2]:.8f} p45={exponent45:.8f}", flush=True
            )

        rel34 = step_rows[1]["rel_l2"]
        rel45 = step_rows[2]["rel_l2"]
        if rel45 <= 0.01:
            classification = "PLATEAU_LIKE"
        elif rel45 < rel34:
            classification = "SLOWING_BUT_NOT_CONVERGED"
        else:
            classification = "NO_PLATEAU"

        result = {
            "classification": classification,
            "diagnostic_complete": True,
            "observational_claim_licensed": False,
            "act_likelihood_used": False,
            "head": head,
            "ancestry": anc,
            "class_upstream_sha": CLASS_SHA,
            "numerical_representation": "nonredundant_F_state",
            "model": {"aest_model": "Exp", "KB": KB, "tauH0": TAUH0, "memory_order": MEMORY_ORDER, "eta": 0.0, "theory": "linear"},
            "route": {"want_lcmb_full_limber": False, "lmax_scalars": THEORY_LMAX, "kmax_grid": KMAX_GRID.tolist()},
            "spectra": summaries,
            "step_rel_l2": step_rows,
            "rel_l2_to_k5": rel_to_k5,
            "representative_multipoles": point_rows,
            "interpretation": "Descriptive high-k saturation diagnostic only; no ACT likelihood or observational validity claim.",
        }
        jout.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        np.savez_compressed(
            nout,
            ell=np.arange(LMAX_DIAG+1),
            kmax=KMAX_GRID,
            clkk=spectra,
            lpoints=LPOINTS,
            step_rel_l2=np.asarray([x["rel_l2"] for x in step_rows]),
            rel_l2_to_k5=np.asarray(rel_to_k5),
        )
        print("KDIAG_CLASSIFICATION=" + classification, flush=True)
        print("OBSERVATIONAL_CLAIM_LICENSED=False", flush=True)
        return 0
    except Exception as exc:
        result = {
            "classification": "FSTATE_KMAX_DIAGNOSTIC_INCOMPLETE",
            "diagnostic_complete": False,
            "observational_claim_licensed": False,
            "error": f"{type(exc).__name__}: {exc}",
        }
        jout.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print("KDIAG_ERROR=" + result["error"], flush=True)
        print("KDIAG_CLASSIFICATION=FSTATE_KMAX_DIAGNOSTIC_INCOMPLETE", flush=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
