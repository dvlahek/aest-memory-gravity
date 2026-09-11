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

R6_BASE_HEAD = "f4280426267e397af18f066d2c7c0755b7a105fa"
R7_PREDATA_COMMIT = "377c42d9cea3b25ce92357361d70845e48e6a13b"
CLASS_SHA = "e85808324f51fc694d12e3ed7439552a3c3f9540"

THEORY_LMAX = 4000
TRIM_LMAX = 2998
ACT_REQUIRED_LMAX = 2999

START = {
    "H0": 67.3324639084866,
    "omega_b": 0.022377376877682164,
    "omega_cdm": 0.12006705327635288,
    "tau_reio": 0.06174082364515668,
    "n_s": 0.9666229454895277,
    "A_s": 2.1308864352626987e-9,
}

COMPLETE_LABEL = "ACT_DR6_LENSING_EXPLORATORY_R7_GR_PIPELINE_CONTROL_COMPLETE"
INCOMPLETE_LABEL = "ACT_DR6_LENSING_EXPLORATORY_R7_GR_PIPELINE_CONTROL_INCOMPLETE"


def git_head() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()


def is_ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0


def rewrite_ini(text: str, root: str) -> str:
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
        "z_max_pk",
        "P_k_max_h/Mpc",
    }

    for line in text.splitlines():
        st = line.strip()
        key = st.split("=", 1)[0].strip() if "=" in st else None
        if key in drop_keys:
            continue
        if key == "non linear":
            # R7 is intentionally the same certified linear lensing path as R6.
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
        "# ACT DR6 exploratory R7: GR/vanilla pipeline control",
        "aest_enabled = no",
    ]
    return "\n".join(out) + "\n"


def run_class(class_root: Path) -> Path:
    outdir = class_root / "output"
    outdir.mkdir(parents=True, exist_ok=True)
    ini = class_root / "obs_act_r7_gr.ini"
    root = "output/obs_act_r7_gr_"
    ini.write_text(rewrite_ini(BASE_INI.read_text(), root))

    env = os.environ.copy()
    env["OMP_NUM_THREADS"] = "1"
    for name in (
        "AEST_TANGENT_FORCE_FILE",
        "AEST_TANGENT_LAMBDA",
        "AEST_TANGENT_TRACE_FILE",
        "AEST_OFFLINE_TRACE_FILE",
    ):
        env.pop(name, None)

    log = ROOT / "results" / "act_dr6_r7_class_gr.log"
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
        raise RuntimeError(f"CLASS executable failed with code {proc.returncode}:\n{tail}")

    path = class_root / "output" / "obs_act_r7_gr__cl.dat"
    if not path.exists() or path.stat().st_size == 0:
        raise RuntimeError(f"CLASS _cl.dat missing: {path}")

    saved = ROOT / "results" / "act_dr6_r7_gr__cl.dat"
    shutil.copy2(path, saved)
    return saved


def load_class_ckk(path: Path):
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

    # CLASS-format _cl.dat: D_L^phiphi = L(L+1) C_L^phiphi/(2 pi).
    # C_L^kappakappa = [L(L+1)]^2 C_L^phiphi / 4.
    ckk_phys = (np.pi / 2.0) * expected * (expected + 1.0) * dpp

    bad = ~np.isfinite(ckk_phys)
    if np.any(bad):
        badell = expected[bad]
        raise FloatingPointError(
            f"nonfinite GR CLASS Ckk inside ACT support: count={badell.size}, first={badell[:30].tolist()}"
        )
    zero = ckk_phys == 0.0
    if np.any(zero):
        zell = expected[zero]
        raise FloatingPointError(
            f"zero GR CLASS Ckk inside ACT support: count={zell.size}, first={zell[:30].tolist()}"
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
        f"R7_GR_CKK_FINITE N={expected.size} L={expected[0]}..{expected[-1]} "
        f"min={stats['ckk_min']:.12e} max={stats['ckk_max']:.12e}",
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
        raise FloatingPointError("nonfinite ACT DR6 GR-control likelihood result")
    return chi2, binned, obs, delta


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--class-root", required=True)
    ap.add_argument("--json-out", default="results/act_dr6_lensing_exploratory_r7_gr_pipeline_control.json")
    ap.add_argument("--npz-out", default="results/act_dr6_lensing_exploratory_r7_gr_pipeline_control.npz")
    args = ap.parse_args()

    class_root = Path(args.class_root).resolve()
    jout = Path(args.json_out)
    nout = Path(args.npz_out)
    jout.parent.mkdir(parents=True, exist_ok=True)

    try:
        import act_dr6_lenslike as alike

        head = git_head()
        ancestry = {
            "r6_base_head": is_ancestor(R6_BASE_HEAD),
            "r7_predata": is_ancestor(R7_PREDATA_COMMIT),
        }
        print("ACT_DR6_LENSING_EXPLORATORY_R7_GR_PIPELINE_CONTROL_START", flush=True)
        print("HEAD=" + head, flush=True)
        print("ANCESTRY=" + json.dumps(ancestry, sort_keys=True), flush=True)
        print("THEORY=linear", flush=True)
        print("MODEL=GR aest_enabled=no", flush=True)
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

        cl_path = run_class(class_root)
        ckk, stats = load_class_ckk(cl_path)
        chi2, binned, obs, residual = act_chi2(data, ckk)
        bcents = np.asarray(data["bcents_act"], dtype=float)

        print(f"R7_GR_ACT_CHI2={chi2:.12e}", flush=True)
        for i, (L, d, t, r) in enumerate(zip(bcents, obs, binned, residual), start=1):
            ratio = float(t / d) if d != 0 else math.nan
            print(
                f"R7_BIN {i:02d}/10 L={L:.6f} data={d:.12e} theory={t:.12e} "
                f"residual={r:.12e} theory_over_data={ratio:.12e}",
                flush=True,
            )

        result = {
            "classification": COMPLETE_LABEL,
            "observational_claim_licensed": False,
            "exploratory": True,
            "head": head,
            "ancestry": ancestry,
            "class_upstream_sha": CLASS_SHA,
            "class_execution_path": "executable + v019p/pre/p3.pre + _cl.dat phi-phi column",
            "model": "GR",
            "aest_enabled": False,
            "theory": "linear",
            "act": {
                "variant": "act_baseline",
                "lens_only": True,
                "like_corrections": False,
                "version": "v1.2",
                "trim_lmax": TRIM_LMAX,
                "nbins": int(obs.size),
                "chi2": float(chi2),
            },
            "spectrum": stats,
            "conversion": "Ckk=(pi/2)*L*(L+1)*D_L_phiphi from CLASS-format _cl.dat",
            "bcents_act": bcents.tolist(),
            "data_binned_clkk": obs.tolist(),
            "binned_theory": binned.tolist(),
            "residual": residual.tolist(),
            "theory_over_data": np.divide(binned, obs, out=np.full_like(binned, np.nan), where=obs != 0).tolist(),
        }
        jout.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        np.savez_compressed(
            nout,
            ell=np.arange(ACT_REQUIRED_LMAX + 1, dtype=int),
            clkk=ckk,
            bcents_act=bcents,
            data_binned_clkk=obs,
            binned_theory=binned,
            residual=residual,
            chi2=np.asarray([chi2], dtype=float),
        )

        print("CLASSIFICATION=" + COMPLETE_LABEL, flush=True)
        print("OBSERVATIONAL_CLAIM_LICENSED=False", flush=True)
        print("ACT_DR6_LENSING_EXPLORATORY_R7_GR_PIPELINE_CONTROL_END", flush=True)
        return 0

    except Exception as exc:
        result = {
            "classification": INCOMPLETE_LABEL,
            "observational_claim_licensed": False,
            "error": f"{type(exc).__name__}: {exc}",
        }
        jout.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print("R7_ERROR=" + result["error"], flush=True)
        print("CLASSIFICATION=" + INCOMPLETE_LABEL, flush=True)
        print("OBSERVATIONAL_CLAIM_LICENSED=False", flush=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
