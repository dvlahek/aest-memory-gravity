#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fullj_weyl import aest_ulp_initial_amplitude_localization as amp
from fullj_weyl import stable_aest_desi_dr1_r9b_shapefit_projection as r9b
from fullj_weyl import stable_aest_desi_dr1_r9b2_direct_velocity_shapefit_projection as r9b2
from fullj_weyl import stable_aest_observable_projection_r5b_derivative_zero as r5b

PREFIT_LOCK = "950b4d37a9a6480e7f8e65d2a5a946230987b09a"
R9B2_POSTDATA_LOCK = "5f453a296d367556927cfa8e1e86b7ea103a9b52"
R9B2_PREFIT_LOCK = "5864a8a56f420c578629763d478f60dfc49c2620"
ADAPTER_RESULT_LOCK = "f5484b4572b673dfcead51875e3aa790c698a18c"

R9B2_JSON = ROOT / "results/stable_aest_desi_dr1_r9b2_direct_velocity_shapefit_projection.json"
R9B2_JSON_SHA256 = "b0afd658758eb63708f837884f9e236f945879a97b56daef571abb9342ab4697"
ADAPTER_JSON = ROOT / "results/stable_aest_desi_dr1_r9b2_velocity_adapter_validation.json"

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
MATERIAL_GATE = 5.0e-2
CANON_BITS = 4592669915990485346

CLS_CERT = "STABLE_AEST_DESI_DR1_R9B2A_DIAGNOSTIC_OUTPUT_CONTAMINATION_CERTIFIED"
CLS_PARENT = "STABLE_AEST_DESI_DR1_R9B2A_PROVENANCE_FAIL"
CLS_RUN = "STABLE_AEST_DESI_DR1_R9B2A_RUN_FAIL"
CLS_INTERNAL = "STABLE_AEST_DESI_DR1_R9B2A_INTERNAL_OUTPUT_REQUEST_DEPENDENCE"
CLS_EXTRACT = "STABLE_AEST_DESI_DR1_R9B2A_SERIALIZATION_FREE_EXTRACTION_UNRESOLVED"
CLS_TAU = "STABLE_AEST_DESI_DR1_R9B2A_ETA0_TAU_INVARIANCE_FAIL"
CLS_NOT_REPRO = "STABLE_AEST_DESI_DR1_R9B2A_CONTAMINATION_NOT_REPRODUCED"


def ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"], cwd=ROOT,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    ).returncode == 0


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(a: float, b: float) -> float:
    a = float(a); b = float(b)
    return float(abs(a-b) / max(abs(a), abs(b), 1e-300))


def prepare_params(tau: float, variant: str):
    params, bits, pos = r5b.build_params(0.0, float(r9b.TOL))
    if int(bits) != CANON_BITS:
        raise RuntimeError(f"unexpected canonical bit pattern {bits} != {CANON_BITS}")
    params["aest_tau_H0"] = float(tau)
    params["z_max_pk"] = max(2.3, float(np.max(ZEFF)) + 0.2)
    params["P_k_max_h/Mpc"] = 5.0
    params["output"] = "mPk,mTk,vTk"
    params.pop("non_linear", None)
    params.pop("lensing", None)

    if variant == "locked":
        pass
    elif variant == "ulp_plus1":
        toks = amp.tokens(params["k_output_values"])
        if pos >= len(toks):
            raise RuntimeError("canonical target position outside k_output_values")
        parsed_bits = int(amp.ulp.float_bits(float(toks[pos])))
        if parsed_bits != CANON_BITS:
            raise RuntimeError(f"serialized canonical token has bits {parsed_bits}, expected {CANON_BITS}")
        toks[pos] = format(amp.ulp.bits_float(CANON_BITS + 1), ".17g")
        params["k_output_values"] = amp.join_tokens(toks)
    elif variant == "no_kout":
        params.pop("k_output_values", None)
    else:
        raise ValueError(variant)
    return params, int(bits), int(pos)


def run_variant(name: str, tau: float, variant: str):
    from classy import Class

    params, bits, pos = prepare_params(float(tau), variant)
    c = Class(); c.set(params); c.compute()
    try:
        fid, fcache = r9b._get_fiducial_cache([float(z) for z in ZEFF])
        rows = []
        for z in ZEFF:
            z = float(z)
            internal_s8 = float(c.sigma(8.0, z, h_units=True))
            internal_fs8 = float(c.effective_f_sigma8(z, z_step=0.1))
            internal_proxy = internal_fs8 / internal_s8
            ext = r9b2._direct_velocity_shapefit_at_z(c, z, fid, fcache)
            row = {
                "z": z,
                "sigma8_internal": internal_s8,
                "legacy_growth_proxy": internal_proxy,
                "sigma8_dd_external": float(ext["sigma8_dd"]),
                "sigma8_tt_external": float(ext["sigma8_tt"]),
                "f_direct_external": float(ext["f_direct"]),
                "rel_external_dd_vs_internal": rel(ext["sigma8_dd"], internal_s8),
                "rel_direct_f_vs_legacy_proxy": rel(ext["f_direct"], internal_proxy),
                "transfer_n_k": int(ext["transfer_n_k"]),
                "transfer_kh_min": float(ext["transfer_kh_min"]),
                "transfer_kh_max": float(ext["transfer_kh_max"]),
            }
            row["finite_positive"] = bool(
                all(np.isfinite(row[k]) for k in (
                    "sigma8_internal", "legacy_growth_proxy", "sigma8_dd_external",
                    "sigma8_tt_external", "f_direct_external"
                ))
                and row["sigma8_internal"] > 0.0
                and row["sigma8_dd_external"] > 0.0
                and row["sigma8_tt_external"] > 0.0
                and row["f_direct_external"] > 0.0
            )
            rows.append(row)
            print(
                "R9B2A_POINT "
                f"variant={name} z={z:.9f} "
                f"si={internal_s8:.9g} sd={row['sigma8_dd_external']:.9g} "
                f"st={row['sigma8_tt_external']:.9g} f={row['f_direct_external']:.9g} "
                f"proxy={internal_proxy:.9g} rel_dd={row['rel_external_dd_vs_internal']:.3e}",
                flush=True,
            )
        return {
            "name": name, "variant": variant, "tau_H0": float(tau),
            "bits": int(bits), "target_pos": int(pos),
            "k_output_values_present": "k_output_values" in params,
            "rows": rows,
        }
    finally:
        c.struct_cleanup(); c.empty()


def rowmap(v):
    return {float(r["z"]): r for r in v["rows"]}


def max_pair_rel(a, b, key):
    aa = rowmap(a); bb = rowmap(b)
    return float(max(rel(aa[z][key], bb[z][key]) for z in aa))


def main() -> int:
    outpath = ROOT / "results/stable_aest_desi_dr1_r9b2a_extraction_invariance.json"
    print("STABLE_AEST_DESI_DR1_R9B2A_EXTRACTION_INVARIANCE_START", flush=True)

    parent_ok = bool(
        ancestor(PREFIT_LOCK) and ancestor(R9B2_POSTDATA_LOCK)
        and ancestor(R9B2_PREFIT_LOCK) and ancestor(ADAPTER_RESULT_LOCK)
        and R9B2_JSON.is_file() and ADAPTER_JSON.is_file()
        and sha256(R9B2_JSON) == R9B2_JSON_SHA256
    )
    parent_meta = {}
    if R9B2_JSON.is_file() and ADAPTER_JSON.is_file():
        try:
            rr = json.loads(R9B2_JSON.read_text())
            aa = json.loads(ADAPTER_JSON.read_text())
            parent_meta = {
                "r9b2_classification": rr.get("classification"),
                "r9b2_gates": rr.get("gates", {}),
                "adapter_classification": aa.get("classification"),
            }
            parent_ok = bool(
                parent_ok
                and rr.get("classification") == R9B2_CLASS
                and rr.get("diagnostic_complete") is True
                and rr.get("gates", {}).get("R9B2_G1_historical_parent_adapter_and_official_data_provenance") is True
                and rr.get("gates", {}).get("R9B2_G2_direct_physical_source_topology") is True
                and rr.get("gates", {}).get("R9B2_G3_direct_velocity_shapefit_construction") is True
                and rr.get("gates", {}).get("R9B2_G4_central_derivative_consistency") is False
                and aa.get("classification") == ADAPTER_CLASS
                and aa.get("diagnostic_complete") is True
                and len(aa.get("rows", [])) == 6
                and all(bool(x.get("pass")) for x in aa.get("rows", []))
            )
        except Exception:
            parent_ok = False

    if not parent_ok:
        out = {"classification": CLS_PARENT, "diagnostic_complete": False, "parent": parent_meta}
        outpath.write_text(json.dumps(out, indent=2, sort_keys=True)+"\n")
        print("STABLE_AEST_DESI_DR1_R9B2A_CLASSIFICATION="+CLS_PARENT, flush=True)
        return 3

    specs = [
        ("locked_tau10", 10.0, "locked"),
        ("ulp_plus1_tau10", 10.0, "ulp_plus1"),
        ("no_kout_tau10", 10.0, "no_kout"),
        ("no_kout_tau5", 5.0, "no_kout"),
        ("no_kout_tau2p5", 2.5, "no_kout"),
        ("no_kout_tau1p25", 1.25, "no_kout"),
    ]
    variants = {}
    try:
        for name, tau, variant in specs:
            variants[name] = run_variant(name, tau, variant)
    except Exception as exc:
        out = {
            "classification": CLS_RUN, "diagnostic_complete": False,
            "parent": parent_meta, "error": repr(exc), "variants": variants,
        }
        outpath.write_text(json.dumps(out, indent=2, sort_keys=True)+"\n")
        print(f"STABLE_AEST_DESI_DR1_R9B2A_RUN_FAIL error={exc!r}", flush=True)
        print("STABLE_AEST_DESI_DR1_R9B2A_CLASSIFICATION="+CLS_RUN, flush=True)
        return 2

    locked = variants["locked_tau10"]
    plus1 = variants["ulp_plus1_tau10"]
    clean10 = variants["no_kout_tau10"]
    no_kout = [variants[f"no_kout_tau{x}"] for x in ("10", "5", "2p5", "1p25")]

    internal_sigma_req = max_pair_rel(locked, clean10, "sigma8_internal")
    internal_proxy_req = max_pair_rel(locked, clean10, "legacy_growth_proxy")
    a2 = bool(max(internal_sigma_req, internal_proxy_req) <= REL_GATE)

    no_kout_dd = float(max(
        r["rel_external_dd_vs_internal"] for v in no_kout for r in v["rows"]
    ))
    a3 = bool(no_kout_dd <= REL_GATE)

    a4 = bool(all(
        r["finite_positive"] and 0.05 < float(r["f_direct_external"]) < 2.0
        for v in no_kout for r in v["rows"]
    ))

    tau_dd = 0.0; tau_f = 0.0
    for v in no_kout[1:]:
        tau_dd = max(tau_dd, max_pair_rel(clean10, v, "sigma8_dd_external"))
        tau_f = max(tau_f, max_pair_rel(clean10, v, "f_direct_external"))
    a5 = bool(max(tau_dd, tau_f) <= REL_GATE)

    contam = {
        "locked_vs_no_kout_sigma8_dd": max_pair_rel(locked, clean10, "sigma8_dd_external"),
        "locked_vs_no_kout_f_direct": max_pair_rel(locked, clean10, "f_direct_external"),
        "ulp_plus1_vs_locked_sigma8_dd": max_pair_rel(plus1, locked, "sigma8_dd_external"),
        "ulp_plus1_vs_locked_f_direct": max_pair_rel(plus1, locked, "f_direct_external"),
    }
    max_contam = float(max(contam.values()))
    a6 = bool(max_contam >= MATERIAL_GATE)

    gates = {
        "R9B2A_A1_provenance_and_historical_fail_lock": True,
        "R9B2A_A2_internal_output_request_invariance": a2,
        "R9B2A_A3_serialization_free_density_consistency": a3,
        "R9B2A_A4_serialization_free_direct_velocity_sanity": a4,
        "R9B2A_A5_eta0_tau_invariance": a5,
        "R9B2A_A6_material_diagnostic_output_contamination": a6,
    }

    if not a2:
        classification = CLS_INTERNAL
    elif not a3 or not a4:
        classification = CLS_EXTRACT
    elif not a5:
        classification = CLS_TAU
    elif not a6:
        classification = CLS_NOT_REPRO
    else:
        classification = CLS_CERT

    metrics = {
        "rel_gate": REL_GATE,
        "material_gate": MATERIAL_GATE,
        "max_internal_sigma8_locked_vs_no_kout": internal_sigma_req,
        "max_internal_growth_proxy_locked_vs_no_kout": internal_proxy_req,
        "max_no_kout_external_dd_vs_internal": no_kout_dd,
        "max_no_kout_tau_sigma8_dd": tau_dd,
        "max_no_kout_tau_f_direct": tau_f,
        "contamination": contam,
        "max_material_contamination": max_contam,
    }
    out = {
        "classification": classification,
        "diagnostic_complete": True,
        "science_evaluated": False,
        "desi_data_loaded": False,
        "parent": parent_meta,
        "settings": {
            "zeff": ZEFF.tolist(), "eta": 0.0, "tau_H0": list(TAUS),
            "canonical_k_h": float(r5b.CANON_KH), "canonical_bits": CANON_BITS,
            "adjacent_bits": CANON_BITS + 1,
            "rel_gate": REL_GATE, "material_gate": MATERIAL_GATE,
        },
        "gates": gates,
        "metrics": metrics,
        "variants": variants,
        "interpretation": {
            "historical_R9b2_reclassified": False,
            "desi_detection_claim_licensed": False,
            "physical_nonlinearity_claim_licensed": False,
            "serialization_free_science_followup_licensed": classification == CLS_CERT,
        },
    }
    outpath.write_text(json.dumps(out, indent=2, sort_keys=True)+"\n")
    print("STABLE_AEST_DESI_DR1_R9B2A_GATES="+json.dumps(gates, sort_keys=True), flush=True)
    print("STABLE_AEST_DESI_DR1_R9B2A_METRICS="+json.dumps(metrics, sort_keys=True), flush=True)
    print("STABLE_AEST_DESI_DR1_R9B2A_CLASSIFICATION="+classification, flush=True)
    return 0 if classification == CLS_CERT else 1


if __name__ == "__main__":
    raise SystemExit(main())
