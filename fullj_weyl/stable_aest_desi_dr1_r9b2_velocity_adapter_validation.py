#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]

from v063 import theory_response_map as v63

PREFIT_LOCK = "5864a8a56f420c578629763d478f60dfc49c2620"
R9B_POSTDATA_LOCK = "22583094f3c5a417e7af6b1d7f284f739553048b"
R9B_JSON = ROOT / "results/stable_aest_desi_dr1_r9b_shapefit_projection.json"
R9B_CLASS = "STABLE_AEST_DESI_DR1_R9B_CENTRAL_DERIVATIVE_FAIL"

ZEFF = np.asarray([
    0.29536404346937617,
    0.5096288678782911,
    0.7057956472488681,
    0.9185851971138159,
    1.3170658832980264,
    1.4905017757527006,
], dtype=float)

REL_GATE = 5.0e-3
KH_MIN = 1.0e-4
KH_MAX = 5.0

CLS_PASS = "STABLE_AEST_DESI_DR1_R9B2_VELOCITY_ADAPTER_VALIDATED"
CLS_FAIL = "STABLE_AEST_DESI_DR1_R9B2_VELOCITY_ADAPTER_VALIDATION_FAIL"
CLS_PARENT = "STABLE_AEST_DESI_DR1_R9B2_VELOCITY_ADAPTER_PARENT_FAIL"
CLS_RUN = "STABLE_AEST_DESI_DR1_R9B2_VELOCITY_ADAPTER_RUN_FAIL"


def ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0


def rel(a: float, b: float) -> float:
    return float(abs(float(a) - float(b)) / max(abs(float(a)), abs(float(b)), 1e-300))


def sigma8_1d(kh, pk):
    from cosmoprimo import PowerSpectrumInterpolator1D

    kh = np.asarray(kh, float)
    pk = np.asarray(pk, float)
    good = np.isfinite(kh) & np.isfinite(pk) & (kh > 0.0) & (pk >= 0.0)
    kh = kh[good]
    pk = pk[good]
    order = np.argsort(kh)
    kh = kh[order]
    pk = pk[order]
    keep = np.ones(kh.size, dtype=bool)
    if kh.size > 1:
        keep[1:] = np.diff(kh) > 0.0
    kh = kh[keep]
    pk = pk[keep]
    if kh.size < 16 or kh[0] > 2.0e-4 or kh[-1] < 2.0:
        raise RuntimeError(f"insufficient k support for sigma8: n={kh.size} range={kh[0] if kh.size else np.nan}..{kh[-1] if kh.size else np.nan}")
    if not np.all(pk > 0.0):
        # isolated exact zeros are not expected in the retained linear spectra
        raise RuntimeError("non-positive P(k) in sigma8 input")
    return float(np.asarray(PowerSpectrumInterpolator1D(kh, pk).sigma8()))


def class_rows():
    from classy import Class

    params = dict(v63.class_params())
    params.update({
        "aest_enabled": "no",
        "aest_memory_enabled": "no",
        "aest_eta": 0.0,
        "output": "mPk,mTk,vTk",
        "z_max_pk": float(np.max(ZEFF) + 0.25),
        "P_k_max_h/Mpc": KH_MAX,
    })
    params.pop("non_linear", None)
    params.pop("lensing", None)

    c = Class()
    c.set(params)
    c.compute()
    try:
        h = float(c.h())
        Om_b = float(c.Omega_b())
        Om_c = float(c.Omega_cdm())
        fb = Om_b / (Om_b + Om_c)
        fc = 1.0 - fb
        rows = []
        for z in ZEFF:
            tr = c.get_transfer(float(z), output_format="class")
            required = ("k (h/Mpc)", "d_b", "d_cdm", "t_b", "t_cdm")
            missing = [x for x in required if x not in tr]
            if missing:
                raise RuntimeError(f"CLASS transfer fields missing at z={z}: {missing}; keys={sorted(tr)}")

            kh = np.asarray(tr["k (h/Mpc)"], float)
            db = np.asarray(tr["d_b"], float)
            dc = np.asarray(tr["d_cdm"], float)
            tb = np.asarray(tr["t_b"], float)
            tc = np.asarray(tr["t_cdm"], float)
            if not (kh.shape == db.shape == dc.shape == tb.shape == tc.shape):
                raise RuntimeError(f"CLASS transfer shape mismatch at z={z}")

            mask = np.isfinite(kh) & (kh >= KH_MIN) & (kh <= KH_MAX)
            if np.count_nonzero(mask) < 32:
                raise RuntimeError(f"too few CLASS transfer modes at z={z}")
            kh = kh[mask]; db = db[mask]; dc = dc[mask]; tb = tb[mask]; tc = tc[mask]
            k = kh * h

            H_phys = float(c.Hubble(float(z)))  # 1/Mpc
            Hconf = H_phys / (1.0 + float(z))
            if not np.isfinite(Hconf) or Hconf <= 0.0:
                raise RuntimeError(f"invalid CLASS conformal H at z={z}: {Hconf}")

            dcb = fb * db + fc * dc
            vnb = -tb / Hconf
            vnc = -tc / Hconf
            vcb = fb * vnb + fc * vnc
            if np.any(~np.isfinite(dcb)) or np.any(~np.isfinite(vcb)):
                raise RuntimeError(f"nonfinite CLASS density/velocity transfer at z={z}")
            floor = 1e-14 * max(float(np.max(np.abs(dcb))), 1.0)
            if np.any(np.abs(dcb) <= floor):
                raise RuntimeError(f"CLASS delta_cb near zero on retained grid at z={z}")

            pdd = np.asarray([float(c.pk_cb_lin(float(kk), float(z))) for kk in k], float) * h**3
            ptt = pdd * (vcb / dcb) ** 2
            if np.any(~np.isfinite(pdd)) or np.any(~np.isfinite(ptt)) or np.any(pdd <= 0.0) or np.any(ptt <= 0.0):
                raise RuntimeError(f"invalid reconstructed CLASS spectra at z={z}")

            sdd = sigma8_1d(kh, pdd)
            stt = sigma8_1d(kh, ptt)
            f = stt / sdd
            proxy = float(c.effective_f_sigma8(float(z), z_step=0.1)) / float(c.sigma(8.0, float(z), h_units=True))
            rows.append({
                "z": float(z),
                "sigma8_dd": sdd,
                "sigma8_tt": stt,
                "f": f,
                "old_proxy": proxy,
                "Hconf_1_Mpc": Hconf,
                "fb": fb,
                "n_k": int(kh.size),
                "kh_min": float(np.min(kh)),
                "kh_max": float(np.max(kh)),
            })
        return rows
    finally:
        c.struct_cleanup()
        c.empty()


def camb_rows():
    import camb

    p = v63.class_params()
    H0 = float(p["H0"])
    ombh2 = float(p["omega_b"])
    omch2 = float(p["omega_cdm"])
    h = H0 / 100.0
    fb = ombh2 / (ombh2 + omch2)
    fc = 1.0 - fb

    cp = camb.CAMBparams()
    cp.set_cosmology(
        H0=H0,
        ombh2=ombh2,
        omch2=omch2,
        mnu=0.06,
        num_massive_neutrinos=1,
        nnu=3.046,
        tau=float(p["tau_reio"]),
        YHe=float(p["YHe"]),
    )
    cp.InitPower.set_params(As=float(p["A_s"]), ns=float(p["n_s"]))
    cp.set_matter_power(redshifts=list(map(float, ZEFF[::-1])), kmax=KH_MAX * h * 1.25)
    cp.NonLinear = camb.model.NonLinear_none
    res = camb.get_results(cp)

    kwargs = dict(nonlinear=False, hubble_units=True, k_hunit=True, silent=True)
    pdd_i = res.get_matter_power_interpolator(var1="delta_nonu", var2="delta_nonu", **kwargs)
    pbb_i = res.get_matter_power_interpolator(var1="v_newtonian_baryon", var2="v_newtonian_baryon", **kwargs)
    pbc_i = res.get_matter_power_interpolator(var1="v_newtonian_baryon", var2="v_newtonian_cdm", **kwargs)
    pcc_i = res.get_matter_power_interpolator(var1="v_newtonian_cdm", var2="v_newtonian_cdm", **kwargs)

    kh = np.geomspace(KH_MIN, KH_MAX, 1600)
    rows = []
    for z in ZEFF:
        pdd = np.asarray(pdd_i.P(float(z), kh), float)
        ptt = (
            fb**2 * np.asarray(pbb_i.P(float(z), kh), float)
            + 2.0 * fb * fc * np.asarray(pbc_i.P(float(z), kh), float)
            + fc**2 * np.asarray(pcc_i.P(float(z), kh), float)
        )
        if np.any(~np.isfinite(pdd)) or np.any(~np.isfinite(ptt)) or np.any(pdd <= 0.0) or np.any(ptt <= 0.0):
            raise RuntimeError(f"invalid CAMB spectra at z={z}")
        sdd = sigma8_1d(kh, pdd)
        stt = sigma8_1d(kh, ptt)
        rows.append({"z": float(z), "sigma8_dd": sdd, "sigma8_tt": stt, "f": stt / sdd, "fb": fb})
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json-out", default="results/stable_aest_desi_dr1_r9b2_velocity_adapter_validation.json")
    args = ap.parse_args()
    outpath = ROOT / args.json_out if not Path(args.json_out).is_absolute() else Path(args.json_out)
    outpath.parent.mkdir(parents=True, exist_ok=True)

    print("STABLE_AEST_DESI_DR1_R9B2_VELOCITY_ADAPTER_START", flush=True)

    parent_ok = bool(ancestor(PREFIT_LOCK) and ancestor(R9B_POSTDATA_LOCK) and R9B_JSON.is_file())
    parent_meta = {}
    if R9B_JSON.is_file():
        try:
            d = json.loads(R9B_JSON.read_text())
            parent_meta = {"classification": d.get("classification"), "gates": d.get("gates", {})}
            parent_ok = bool(
                parent_ok
                and d.get("classification") == R9B_CLASS
                and d.get("diagnostic_complete") is True
                and d.get("gates", {}).get("R9B_G1_parent_and_official_data_provenance") is True
                and d.get("gates", {}).get("R9B_G2_direct_physical_source_topology") is True
                and d.get("gates", {}).get("R9B_G3_shapefit_data_construction") is True
            )
        except Exception:
            parent_ok = False

    if not parent_ok:
        out = {"classification": CLS_PARENT, "diagnostic_complete": False, "parent": parent_meta}
        outpath.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
        print("STABLE_AEST_DESI_DR1_R9B2_VELOCITY_ADAPTER_CLASSIFICATION=" + CLS_PARENT, flush=True)
        return 3

    try:
        cr = class_rows()
        mr = camb_rows()
    except Exception as exc:
        out = {"classification": CLS_RUN, "diagnostic_complete": False, "error": repr(exc), "parent": parent_meta}
        outpath.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
        print(f"STABLE_AEST_DESI_DR1_R9B2_VELOCITY_ADAPTER_RUN_FAIL error={exc!r}", flush=True)
        print("STABLE_AEST_DESI_DR1_R9B2_VELOCITY_ADAPTER_CLASSIFICATION=" + CLS_RUN, flush=True)
        return 2

    rows = []
    passed = True
    for a, b in zip(cr, mr):
        if not np.isclose(a["z"], b["z"], rtol=0.0, atol=1e-13):
            raise RuntimeError("CLASS/CAMB redshift ordering mismatch")
        rd = rel(a["sigma8_dd"], b["sigma8_dd"])
        rt = rel(a["sigma8_tt"], b["sigma8_tt"])
        rf = rel(a["f"], b["f"])
        ok = bool(rd <= REL_GATE and rt <= REL_GATE and rf <= REL_GATE)
        passed = passed and ok
        row = {
            "z": a["z"],
            "class_sigma8_dd": a["sigma8_dd"],
            "camb_sigma8_dd": b["sigma8_dd"],
            "rel_sigma8_dd": rd,
            "class_sigma8_tt": a["sigma8_tt"],
            "camb_sigma8_tt": b["sigma8_tt"],
            "rel_sigma8_tt": rt,
            "class_f": a["f"],
            "camb_f": b["f"],
            "rel_f": rf,
            "old_proxy": a["old_proxy"],
            "old_proxy_rel_to_direct": rel(a["old_proxy"], a["f"]),
            "pass": ok,
        }
        rows.append(row)
        print(
            "R9B2_VELOCITY_ADAPTER "
            f"z={a['z']:.9f} f_class={a['f']:.9g} f_camb={b['f']:.9g} "
            f"rel_dd={rd:.3e} rel_tt={rt:.3e} rel_f={rf:.3e} pass={ok}",
            flush=True,
        )

    classification = CLS_PASS if passed else CLS_FAIL
    out = {
        "classification": classification,
        "diagnostic_complete": True,
        "gate": REL_GATE,
        "adapter": {
            "class_velocity_columns": ["t_b", "t_cdm"],
            "class_column_meaning": ["theta_b", "theta_cdm"],
            "mapping": "v_newtonian_x = -theta_x / Hconf",
            "Hconf": "Hubble(z)/(1+z)",
            "velocity_spectrum": "P_cb * (v_cb/delta_cb)^2",
        },
        "parent": parent_meta,
        "rows": rows,
        "science_evaluated": False,
    }
    outpath.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print("STABLE_AEST_DESI_DR1_R9B2_VELOCITY_ADAPTER_CLASSIFICATION=" + classification, flush=True)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
