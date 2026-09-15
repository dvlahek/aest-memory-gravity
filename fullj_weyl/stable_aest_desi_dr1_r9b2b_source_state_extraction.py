#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import inspect
import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from v063 import theory_response_map as v63
from fullj_weyl import stable_aest_desi_dr1_r9b_shapefit_projection as r9b
from fullj_weyl import stable_aest_observable_projection_r5b_derivative_zero as r5b

PREFIT_LOCK = "0485ce9d0bbaa79acccfab7fe532b122cb71f53d"
R9B2A_POSTDATA_LOCK = "00d06aa140fc8e9097be3df62ecd6013f0c8b312"
R9B2_POSTDATA_LOCK = "5f453a296d367556927cfa8e1e86b7ea103a9b52"
ADAPTER_RESULT_LOCK = "f5484b4572b673dfcead51875e3aa790c698a18c"
V078_LOCK = "31c05c22b86e8ac01ce822306efecdcb03cff1d5"

R9B2A_JSON = ROOT / "results/stable_aest_desi_dr1_r9b2a_extraction_invariance.json"
R9B2_JSON = ROOT / "results/stable_aest_desi_dr1_r9b2_direct_velocity_shapefit_projection.json"
ADAPTER_JSON = ROOT / "results/stable_aest_desi_dr1_r9b2_velocity_adapter_validation.json"
V078_NOTE = ROOT / "docs/v078_preserved_interpretation.md"

R9B2A_JSON_SHA256 = "b779d215939954195ece199bcf711e3eb6ed3262aad9206019c6d60210195874"
ADAPTER_JSON_SHA256 = "c4d9281cd504785a9e4fb187b02db2860e24622bbe1ccf4a52e44446be0a119a"

R9B2A_CLASS = "STABLE_AEST_DESI_DR1_R9B2A_SERIALIZATION_FREE_EXTRACTION_UNRESOLVED"
R9B2_CLASS = "STABLE_AEST_DESI_DR1_R9B2_CENTRAL_DERIVATIVE_FAIL"
ADAPTER_CLASS = "STABLE_AEST_DESI_DR1_R9B2_VELOCITY_ADAPTER_VALIDATED"

ZEFF = np.asarray([
    0.29536404346937617,
    0.5096288678782911,
    0.7057956472488681,
    0.9185851971138159,
    1.3170658832980264,
    1.4905017757527006,
], dtype=float)
TAUS = (10.0, 5.0, 2.5, 1.25)
REL_GATE = 5.0e-3
KH_MIN = 1.0e-4
KH_MAX = 5.0
TOL = 3.0e-8
KPIVOT = 0.05

CLS_PASS = "STABLE_AEST_DESI_DR1_R9B2B_SOURCE_STATE_EXTRACTION_VALIDATED"
CLS_PROV = "STABLE_AEST_DESI_DR1_R9B2B_PROVENANCE_FAIL"
CLS_SOURCE = "STABLE_AEST_DESI_DR1_R9B2B_SOURCE_CONSTRUCTION_FAIL"
CLS_GR = "STABLE_AEST_DESI_DR1_R9B2B_GR_BENCHMARK_FAIL"
CLS_AEST = "STABLE_AEST_DESI_DR1_R9B2B_AEST_ETA0_CLOSURE_FAIL"
CLS_TAU = "STABLE_AEST_DESI_DR1_R9B2B_ETA0_TAU_INVARIANCE_FAIL"
CLS_SANITY = "STABLE_AEST_DESI_DR1_R9B2B_SOURCE_STATE_SANITY_FAIL"
CLS_RUN = "STABLE_AEST_DESI_DR1_R9B2B_RUN_FAIL"


def ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"], cwd=ROOT,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    ).returncode == 0


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(a: float, b: float) -> float:
    aa = float(a); bb = float(b)
    return float(abs(aa-bb) / max(abs(aa), abs(bb), 1e-300))


def _clean_common(kh, *ys):
    kh = np.asarray(kh, float)
    arrs = [np.asarray(y, float) for y in ys]
    if any(y.shape != kh.shape for y in arrs):
        raise RuntimeError("source-state transfer shape mismatch")
    good = np.isfinite(kh) & (kh >= KH_MIN) & (kh <= KH_MAX)
    for y in arrs:
        good &= np.isfinite(y)
    kh = kh[good]
    arrs = [y[good] for y in arrs]
    order = np.argsort(kh)
    kh = kh[order]
    arrs = [y[order] for y in arrs]
    keep = np.ones(kh.size, dtype=bool)
    if kh.size > 1:
        keep[1:] = np.diff(kh) > 0.0
    kh = kh[keep]
    arrs = [y[keep] for y in arrs]
    if kh.size < 32 or kh[0] > 2.0e-4 or kh[-1] < 2.0:
        raise RuntimeError(
            f"insufficient source-state k support n={kh.size} "
            f"range={kh[0] if kh.size else np.nan}..{kh[-1] if kh.size else np.nan}"
        )
    return (kh, *arrs)


def _source_state_at_z(c, z: float, A_s: float, n_s: float):
    from cosmoprimo import PowerSpectrumInterpolator1D

    tr = c.get_transfer(float(z), output_format="class")
    required = ("k (h/Mpc)", "d_b", "d_cdm", "t_b", "t_cdm")
    missing = [name for name in required if name not in tr]
    if missing:
        raise RuntimeError(f"missing source-state transfer fields at z={z}: {missing}; keys={sorted(tr)}")

    kh, db, dc, tb, tc = _clean_common(
        tr["k (h/Mpc)"], tr["d_b"], tr["d_cdm"], tr["t_b"], tr["t_cdm"]
    )

    Om_b = r9b._omega(c, "Omega_b")
    Om_c = r9b._omega(c, "Omega_cdm")
    fb = Om_b / (Om_b + Om_c)
    fc = 1.0 - fb
    dcb = fb*db + fc*dc

    Hconf = float(c.Hubble(float(z))) / (1.0 + float(z))
    if not np.isfinite(Hconf) or Hconf <= 0.0:
        raise RuntimeError(f"invalid Hconf at z={z}: {Hconf}")
    vb = -tb/Hconf
    vc = -tc/Hconf
    vcb = fb*vb + fc*vc

    h = float(c.h())
    k_mpc = kh*h
    primordial = float(A_s) * (k_mpc/KPIVOT)**(float(n_s)-1.0)
    pref = (2.0*math.pi**2/k_mpc**3) * primordial

    pdd_phys = pref * dcb**2
    ptt_phys = pref * vcb**2
    pdd = pdd_phys * h**3
    ptt = ptt_phys * h**3

    good = (
        np.isfinite(kh) & np.isfinite(pdd) & np.isfinite(ptt)
        & (pdd > 0.0) & (ptt > 0.0)
    )
    kh2 = kh[good]; pdd2 = pdd[good]; ptt2 = ptt[good]
    if kh2.size < 32 or kh2[0] > 2.0e-4 or kh2[-1] < 2.0:
        raise RuntimeError(f"insufficient positive source spectra at z={z}")

    pkdd = PowerSpectrumInterpolator1D(kh2, pdd2)
    pktt = PowerSpectrumInterpolator1D(kh2, ptt2)
    sdd = float(np.asarray(pkdd.sigma8()))
    stt = float(np.asarray(pktt.sigma8()))
    fsrc = stt/sdd

    scale_d = max(float(np.max(np.abs(dcb))), 1e-300)
    scale_v = max(float(np.max(np.abs(vcb))), 1e-300)
    return {
        "z": float(z),
        "sigma8_dd_source": sdd,
        "sigma8_tt_source": stt,
        "f_source": fsrc,
        "finite_positive": bool(
            np.isfinite(sdd) and np.isfinite(stt) and np.isfinite(fsrc)
            and sdd > 0.0 and stt > 0.0 and fsrc > 0.0
        ),
        "n_k": int(kh2.size),
        "kh_min": float(kh2[0]),
        "kh_max": float(kh2[-1]),
        "fb": float(fb),
        "Hconf_1_Mpc": float(Hconf),
        "min_abs_dcb_over_max": float(np.min(np.abs(dcb))/scale_d),
        "min_abs_vcb_over_max": float(np.min(np.abs(vcb))/scale_v),
    }


def _source_construction_gate() -> bool:
    src = inspect.getsource(_source_state_at_z)
    return bool(
        "pdd_phys = pref * dcb**2" in src
        and "ptt_phys = pref * vcb**2" in src
        and "pk_cb_lin(" not in src
        and ".pk_lin(" not in src
        and "vcb/dcb" not in src
        and "vcb / dcb" not in src
    )


def _gr_params():
    p = dict(v63.class_params())
    p.update({
        "aest_enabled": "no",
        "aest_memory_enabled": "no",
        "aest_eta": 0.0,
        "output": "mPk,mTk,vTk",
        "z_max_pk": float(np.max(ZEFF) + 0.25),
        "P_k_max_h/Mpc": KH_MAX,
    })
    p.pop("non_linear", None)
    p.pop("lensing", None)
    p.pop("l_max_scalars", None)
    p.pop("k_output_values", None)
    return p


def _aest_params(tau: float):
    p, _, _ = r5b.build_params(0.0, TOL)
    p["aest_tau_H0"] = float(tau)
    p["output"] = "mPk,mTk,vTk"
    p["z_max_pk"] = max(2.3, float(np.max(ZEFF)) + 0.25)
    p["P_k_max_h/Mpc"] = KH_MAX
    p.pop("non_linear", None)
    p.pop("lensing", None)
    p.pop("l_max_scalars", None)
    p.pop("k_output_values", None)
    return p


def _run_model(params, internal_controls: bool):
    from classy import Class

    c = Class(); c.set(params); c.compute()
    try:
        As = float(params.get("A_s", v63.START["A_s"]))
        ns = float(params.get("n_s", v63.START["n_s"]))
        rows = []
        for z in ZEFF:
            rr = _source_state_at_z(c, float(z), As, ns)
            if internal_controls:
                si = float(c.sigma(8.0, float(z), h_units=True))
                fi = float(c.effective_f_sigma8(float(z), z_step=0.1))/si
                rr.update({
                    "sigma8_internal": si,
                    "legacy_growth_proxy": fi,
                    "rel_sigma8_source_vs_internal": rel(rr["sigma8_dd_source"], si),
                    "rel_f_source_vs_internal_proxy": rel(rr["f_source"], fi),
                })
            rows.append(rr)
            print(
                "R9B2B_POINT "
                f"z={float(z):.9f} sdd={rr['sigma8_dd_source']:.9g} "
                f"stt={rr['sigma8_tt_source']:.9g} f={rr['f_source']:.9g}"
                + (
                    f" si={rr['sigma8_internal']:.9g} proxy={rr['legacy_growth_proxy']:.9g} "
                    f"rel_s={rr['rel_sigma8_source_vs_internal']:.3e} "
                    f"rel_f={rr['rel_f_source_vs_internal_proxy']:.3e}"
                    if internal_controls else ""
                ), flush=True,
            )
        return rows
    finally:
        c.struct_cleanup(); c.empty()


def _rowmap(rows):
    return {float(r["z"]): r for r in rows}


def main() -> int:
    outpath = ROOT / "results/stable_aest_desi_dr1_r9b2b_source_state_extraction.json"
    print("STABLE_AEST_DESI_DR1_R9B2B_SOURCE_STATE_START", flush=True)

    parent_meta = {}
    try:
        r9b2a = json.loads(R9B2A_JSON.read_text())
        r9b2 = json.loads(R9B2_JSON.read_text())
        adapter = json.loads(ADAPTER_JSON.read_text())
        note = V078_NOTE.read_text()
        parent_meta = {
            "r9b2a_classification": r9b2a.get("classification"),
            "r9b2_classification": r9b2.get("classification"),
            "adapter_classification": adapter.get("classification"),
            "r9b2a_json_sha256": sha256(R9B2A_JSON),
            "adapter_json_sha256": sha256(ADAPTER_JSON),
        }
        b1 = bool(
            ancestor(PREFIT_LOCK)
            and ancestor(R9B2A_POSTDATA_LOCK)
            and ancestor(R9B2_POSTDATA_LOCK)
            and ancestor(ADAPTER_RESULT_LOCK)
            and ancestor(V078_LOCK)
            and sha256(R9B2A_JSON) == R9B2A_JSON_SHA256
            and sha256(ADAPTER_JSON) == ADAPTER_JSON_SHA256
            and r9b2a.get("classification") == R9B2A_CLASS
            and r9b2a.get("diagnostic_complete") is True
            and r9b2a.get("science_evaluated") is False
            and r9b2.get("classification") == R9B2_CLASS
            and r9b2.get("diagnostic_complete") is True
            and adapter.get("classification") == ADAPTER_CLASS
            and adapter.get("diagnostic_complete") is True
            and len(adapter.get("rows", [])) == len(ZEFF)
            and "V078_TIME_INTERPOLATION_OPERATOR_CLOSURE_PASS" in note
            and "V078_TIME_INTERPOLATION_OPERATOR_DISCREPANCY_LOCALIZED" in note
        )
    except Exception as exc:
        parent_meta["error"] = repr(exc)
        b1 = False
        adapter = {}

    b2 = _source_construction_gate()
    if not b1:
        out = {"classification": CLS_PROV, "diagnostic_complete": False,
               "science_evaluated": False, "gates": {"R9B2B_B1_provenance_and_historical_lock": False},
               "parent": parent_meta}
        outpath.write_text(json.dumps(out, indent=2, sort_keys=True)+"\n")
        print("STABLE_AEST_DESI_DR1_R9B2B_CLASSIFICATION="+CLS_PROV, flush=True)
        return 3
    if not b2:
        out = {"classification": CLS_SOURCE, "diagnostic_complete": False,
               "science_evaluated": False,
               "gates": {"R9B2B_B1_provenance_and_historical_lock": True,
                         "R9B2B_B2_source_state_construction": False},
               "parent": parent_meta}
        outpath.write_text(json.dumps(out, indent=2, sort_keys=True)+"\n")
        print("STABLE_AEST_DESI_DR1_R9B2B_CLASSIFICATION="+CLS_SOURCE, flush=True)
        return 3

    try:
        gr_rows = _run_model(_gr_params(), internal_controls=False)
        aest_rows = {}
        for tau in TAUS:
            print(f"STABLE_AEST_DESI_DR1_R9B2B_AEST_TAU tau_H0={tau:g}", flush=True)
            aest_rows[str(tau)] = _run_model(_aest_params(tau), internal_controls=True)
    except Exception as exc:
        out = {"classification": CLS_RUN, "diagnostic_complete": False,
               "science_evaluated": False, "error": repr(exc), "parent": parent_meta}
        outpath.write_text(json.dumps(out, indent=2, sort_keys=True)+"\n")
        print(f"STABLE_AEST_DESI_DR1_R9B2B_RUN_FAIL error={exc!r}", flush=True)
        print("STABLE_AEST_DESI_DR1_R9B2B_CLASSIFICATION="+CLS_RUN, flush=True)
        return 2

    locked_adapter = _rowmap(adapter["rows"])
    gr_cmp = []
    b3 = True
    for rr in gr_rows:
        z = float(rr["z"]); aa = locked_adapter[z]
        row = {
            "z": z,
            "rel_sigma8_dd_vs_locked_class": rel(rr["sigma8_dd_source"], aa["class_sigma8_dd"]),
            "rel_sigma8_tt_vs_locked_class": rel(rr["sigma8_tt_source"], aa["class_sigma8_tt"]),
            "rel_f_vs_locked_class": rel(rr["f_source"], aa["class_f"]),
            "rel_f_vs_locked_camb": rel(rr["f_source"], aa["camb_f"]),
        }
        row["pass"] = bool(rr["finite_positive"] and max(
            row["rel_sigma8_dd_vs_locked_class"],
            row["rel_sigma8_tt_vs_locked_class"],
            row["rel_f_vs_locked_class"],
            row["rel_f_vs_locked_camb"],
        ) <= REL_GATE)
        b3 &= row["pass"]
        gr_cmp.append(row)

    tau10 = aest_rows["10.0"]
    b4 = True
    for rr in tau10:
        physical = bool(0.1 < rr["sigma8_dd_source"] < 2.0 and 0.05 < rr["f_source"] < 2.0)
        rr["eta0_closure_pass"] = bool(
            rr["finite_positive"] and physical
            and rr["rel_sigma8_source_vs_internal"] <= REL_GATE
            and rr["rel_f_source_vs_internal_proxy"] <= REL_GATE
        )
        b4 &= rr["eta0_closure_pass"]

    base = _rowmap(tau10)
    tau_metrics = {"max_rel_sigma8_dd": 0.0, "max_rel_sigma8_tt": 0.0, "max_rel_f": 0.0}
    for key, rows in aest_rows.items():
        if key == "10.0":
            continue
        mm = _rowmap(rows)
        for z in base:
            tau_metrics["max_rel_sigma8_dd"] = max(
                tau_metrics["max_rel_sigma8_dd"], rel(mm[z]["sigma8_dd_source"], base[z]["sigma8_dd_source"])
            )
            tau_metrics["max_rel_sigma8_tt"] = max(
                tau_metrics["max_rel_sigma8_tt"], rel(mm[z]["sigma8_tt_source"], base[z]["sigma8_tt_source"])
            )
            tau_metrics["max_rel_f"] = max(
                tau_metrics["max_rel_f"], rel(mm[z]["f_source"], base[z]["f_source"])
            )
    b5 = bool(max(tau_metrics.values()) <= REL_GATE)

    b6 = True
    for rows in aest_rows.values():
        for rr in rows:
            b6 &= bool(
                rr["finite_positive"]
                and 0.1 < rr["sigma8_dd_source"] < 2.0
                and 0.05 < rr["f_source"] < 2.0
            )

    gates = {
        "R9B2B_B1_provenance_and_historical_lock": bool(b1),
        "R9B2B_B2_source_state_construction": bool(b2),
        "R9B2B_B3_pure_GR_benchmark": bool(b3),
        "R9B2B_B4_AeST_eta0_source_internal_consistency": bool(b4),
        "R9B2B_B5_eta0_tau_invariance": bool(b5),
        "R9B2B_B6_pathological_point_removal": bool(b6),
    }

    if not b3:
        classification = CLS_GR
    elif not b4:
        classification = CLS_AEST
    elif not b5:
        classification = CLS_TAU
    elif not b6:
        classification = CLS_SANITY
    else:
        classification = CLS_PASS

    metrics = {
        "rel_gate": REL_GATE,
        "GR_max_rel_sigma8_dd_vs_locked_class": float(max(x["rel_sigma8_dd_vs_locked_class"] for x in gr_cmp)),
        "GR_max_rel_sigma8_tt_vs_locked_class": float(max(x["rel_sigma8_tt_vs_locked_class"] for x in gr_cmp)),
        "GR_max_rel_f_vs_locked_class": float(max(x["rel_f_vs_locked_class"] for x in gr_cmp)),
        "GR_max_rel_f_vs_locked_camb": float(max(x["rel_f_vs_locked_camb"] for x in gr_cmp)),
        "AeST_tau10_max_rel_sigma8_source_vs_internal": float(max(x["rel_sigma8_source_vs_internal"] for x in tau10)),
        "AeST_tau10_max_rel_f_source_vs_internal_proxy": float(max(x["rel_f_source_vs_internal_proxy"] for x in tau10)),
        **tau_metrics,
    }

    out = {
        "classification": classification,
        "diagnostic_complete": True,
        "science_evaluated": False,
        "desi_data_loaded": False,
        "parent": parent_meta,
        "settings": {
            "zeff": ZEFF.tolist(), "eta": 0.0, "tau_H0": list(TAUS),
            "rel_gate": REL_GATE, "KH_MIN": KH_MIN, "KH_MAX": KH_MAX,
            "construction": "Pdd=C(k)*dcb^2; Ptt=C(k)*vcb^2; no local v/d ratio; no pk_lin/pk_cb_lin",
        },
        "gates": gates,
        "metrics": metrics,
        "GR_source_rows": gr_rows,
        "GR_comparison_to_locked_adapter": gr_cmp,
        "AeST_source_rows_by_tau": aest_rows,
        "interpretation": {
            "historical_R9b2_reclassified": False,
            "historical_R9b2a_reclassified": False,
            "desi_detection_claim_licensed": False,
            "eta_or_tau_constraint_licensed": False,
            "source_consistent_DESI_followup_licensed": classification == CLS_PASS,
        },
    }
    outpath.write_text(json.dumps(out, indent=2, sort_keys=True)+"\n")
    print("STABLE_AEST_DESI_DR1_R9B2B_GATES="+json.dumps(gates, sort_keys=True), flush=True)
    print("STABLE_AEST_DESI_DR1_R9B2B_METRICS="+json.dumps(metrics, sort_keys=True), flush=True)
    print("STABLE_AEST_DESI_DR1_R9B2B_CLASSIFICATION="+classification, flush=True)
    return 0 if classification == CLS_PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
