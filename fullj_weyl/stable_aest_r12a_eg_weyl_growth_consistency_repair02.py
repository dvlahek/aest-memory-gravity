#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import os
import sys
from pathlib import Path

import numpy as np

from fullj_weyl import stable_aest_r12a_eg_weyl_growth_consistency as base
from fullj_weyl import stable_aest_r12a_eg_weyl_growth_consistency_repair01 as r01
from fullj_weyl import stable_aest_desi_dr1_r9b_shapefit_projection as r9b
from nl1c6d2a import baryon_matter_sector_audit as d2a

ROOT = Path(__file__).resolve().parents[1]

REPAIR02_PREFIT_LOCK = "af78442d475d35b588e39ce818386979910a4419"
REPAIR01_RUNNER_LOCK = "29b4f737c61a47cf79251ff5f1a27ce1f9bd6f47"
CORRECT_R11A_R02_POSTDATA_LOCK = "84c4ba550ce3b262c78c69054056ab2778014677"
PASS_R02 = "STABLE_AEST_R12A_REPAIR02_SINGLE_MODE_IDENTITY_CERTIFIED"
FAIL_R02_IDENTITY = "STABLE_AEST_R12A_REPAIR02_SINGLE_MODE_IDENTITY_FAIL"
BG_RTOL = 1.0e-12
BG_ATOL = 1.0e-14

# Repair01 already establishes that the original frozen implementation carries
# only an invalid provenance pointer. Repair02 keeps that correction and changes
# only the mode-identity extraction architecture.
if r01.CORRECT_R11A_R02_POSTDATA_LOCK != CORRECT_R11A_R02_POSTDATA_LOCK:
    raise RuntimeError("R12a Repair02 authoritative R11a lock mismatch")
base.R11A_R02_POSTDATA_LOCK = CORRECT_R11A_R02_POSTDATA_LOCK


def _safe_tag(x: float) -> str:
    s = f"{float(x):+.6f}"
    return s.replace("+", "p").replace("-", "m").replace(".", "p")


def _case_name(pure_gr: bool, tau: float, eta: float) -> str:
    return "gr" if pure_gr else base._key(float(tau), float(eta))


def _mode_path(mode_root: Path, pure_gr: bool, tau: float, eta: float, kh: float) -> Path:
    case = _case_name(pure_gr, tau, eta).replace("+", "p").replace("-", "m")
    return mode_root / f"{case}_k{float(kh):.5f}.npz"


def _bg_close(a: float, b: float) -> bool:
    return bool(math.isclose(float(a), float(b), rel_tol=BG_RTOL, abs_tol=BG_ATOL))


def _run_single_mode(eta: float, tau: float, pure_gr: bool, kh: float) -> dict:
    from classy import Class

    p, bits, pos = base._build_params(float(eta), float(tau), bool(pure_gr))
    h_req = base._h_from_params(p)
    # Exactly one requested physical mode. No mapping by returned-list position
    # is needed because the returned scalar-history cardinality is required to be one.
    p["k_output_values"] = f"{float(kh) * float(h_req):.17g}"

    c = Class(); c.set(p); c.compute()
    try:
        h = float(c.h())
        if not _bg_close(h, h_req):
            raise RuntimeError(f"CLASS h differs from requested h: {h} vs {h_req}")
        ob = r9b._omega(c, "Omega_b")
        oc = r9b._omega(c, "Omega_cdm")
        onu = r9b._omega(c, "Omega_nu", 0.0)
        try:
            om = float(c.Omega_m())
        except Exception:
            om = float(ob + oc + onu)
        if not (ob > 0.0 and oc > 0.0 and om > 0.0):
            raise RuntimeError("invalid matter density fractions")
        fb = ob / (ob + oc); fc = oc / (ob + oc)
        H0 = float(c.Hubble(0.0))
        Hconf = np.asarray([float(c.Hubble(float(z))) / (1.0 + float(z)) for z in base.Z], float)
        if not (np.isfinite(H0) and H0 > 0.0 and np.all(np.isfinite(Hconf)) and np.all(Hconf > 0.0)):
            raise RuntimeError("invalid Hubble values")

        pert = c.get_perturbations()
        histories, scalar_key = d2a.scalar_histories(pert)
        if len(histories) != 1:
            raise RuntimeError(
                f"single-mode request k={kh} h/Mpc returned {len(histories)} scalar histories"
            )
        raw = histories[0]

        # Required fields are resolved by the same frozen helpers used by base R12a.
        required = {
            "phi": d2a.pick(raw, "phi"),
            "psi": d2a.pick(raw, "psi"),
            "delta_b": d2a.pick(raw, "delta_b", ("d_b",)),
            "theta_b": d2a.pick(raw, "theta_b", ("t_b",)),
            "delta_cdm": d2a.pick(raw, "delta_cdm", ("d_cdm",)),
            "theta_cdm": d2a.pick(raw, "theta_cdm", ("t_cdm",)),
        }
        for _, key in required.items():
            arr = np.asarray(raw[key], float)
            if arr.size < 8 or not np.all(np.isfinite(arr)):
                raise RuntimeError(f"invalid required history field {key} for k={kh}")

        out = {}
        for method in ("cubic", "pchip"):
            out[method] = base._fields_for_mode(raw, method, fb, fc, Hconf, float(kh), h, H0)

        return {
            "schema": 2,
            "pure_gr": bool(pure_gr),
            "tau_H0": float(tau),
            "eta": float(eta),
            "requested_k_h_Mpc": float(kh),
            "single_requested_mode_Mpc_inv": float(kh) * h,
            "history_count": 1,
            "scalar_key": str(scalar_key),
            "bits": int(bits),
            "target_pos": int(pos),
            "h": h,
            "H0_Mpc_inv": H0,
            "Hconf_Mpc_inv": Hconf,
            "Omega_b": float(ob),
            "Omega_cdm": float(oc),
            "Omega_nu": float(onu),
            "Omega_m": float(om),
            "fb": float(fb),
            "fc": float(fc),
            "required_keys": required,
            "cubic": out["cubic"],
            "pchip": out["pchip"],
        }
    finally:
        c.struct_cleanup(); c.empty()


def _save_mode(path: Path, v: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    arrays = {
        "schema": np.asarray([int(v["schema"])]),
        "pure_gr": np.asarray([int(v["pure_gr"])]),
        "tau_H0": np.asarray([v["tau_H0"]]),
        "eta": np.asarray([v["eta"]]),
        "requested_k_h_Mpc": np.asarray([v["requested_k_h_Mpc"]]),
        "single_requested_mode_Mpc_inv": np.asarray([v["single_requested_mode_Mpc_inv"]]),
        "history_count": np.asarray([v["history_count"]]),
        "bits": np.asarray([v["bits"]]),
        "target_pos": np.asarray([v["target_pos"]]),
        "h": np.asarray([v["h"]]),
        "H0_Mpc_inv": np.asarray([v["H0_Mpc_inv"]]),
        "Hconf_Mpc_inv": np.asarray(v["Hconf_Mpc_inv"], float),
        "Omega_b": np.asarray([v["Omega_b"]]),
        "Omega_cdm": np.asarray([v["Omega_cdm"]]),
        "Omega_nu": np.asarray([v["Omega_nu"]]),
        "Omega_m": np.asarray([v["Omega_m"]]),
        "fb": np.asarray([v["fb"]]),
        "fc": np.asarray([v["fc"]]),
    }
    for method in ("cubic", "pchip"):
        for field in ("W", "delta_cb", "theta_cb", "fdelta", "fcb", "EG"):
            arrays[f"{method}_{field}"] = np.asarray(v[method][field], float)
    np.savez_compressed(path, **arrays)


def _load_mode(path: Path, pure_gr: bool, tau: float, eta: float, kh: float) -> dict:
    q = np.load(path)
    if int(q["schema"][0]) != 2:
        raise RuntimeError("single-mode schema mismatch")
    if bool(int(q["pure_gr"][0])) != bool(pure_gr):
        raise RuntimeError("single-mode pure_gr mismatch")
    if not _bg_close(float(q["tau_H0"][0]), float(tau)) or not _bg_close(float(q["eta"][0]), float(eta)):
        raise RuntimeError("single-mode tau/eta mismatch")
    if not _bg_close(float(q["requested_k_h_Mpc"][0]), float(kh)):
        raise RuntimeError("single-mode requested-k mismatch")
    if int(q["history_count"][0]) != 1:
        raise RuntimeError("single-mode history cardinality mismatch")
    out = {
        "schema": 2,
        "pure_gr": bool(pure_gr),
        "tau_H0": float(tau),
        "eta": float(eta),
        "requested_k_h_Mpc": float(kh),
        "single_requested_mode_Mpc_inv": float(q["single_requested_mode_Mpc_inv"][0]),
        "history_count": 1,
        "bits": int(q["bits"][0]),
        "target_pos": int(q["target_pos"][0]),
        "h": float(q["h"][0]),
        "H0_Mpc_inv": float(q["H0_Mpc_inv"][0]),
        "Hconf_Mpc_inv": np.asarray(q["Hconf_Mpc_inv"], float),
        "Omega_b": float(q["Omega_b"][0]),
        "Omega_cdm": float(q["Omega_cdm"][0]),
        "Omega_nu": float(q["Omega_nu"][0]),
        "Omega_m": float(q["Omega_m"][0]),
        "fb": float(q["fb"][0]),
        "fc": float(q["fc"][0]),
    }
    for method in ("cubic", "pchip"):
        out[method] = {}
        for field in ("W", "delta_cb", "theta_cb", "fdelta", "fcb", "EG"):
            arr = np.asarray(q[f"{method}_{field}"], float)
            if arr.shape != base.Z.shape or not np.all(np.isfinite(arr)):
                raise RuntimeError(f"invalid cached {method}_{field}")
            out[method][field] = arr
    return out


def _background_vector(v: dict) -> np.ndarray:
    return np.asarray([
        v["h"], v["H0_Mpc_inv"], v["Omega_b"], v["Omega_cdm"],
        v["Omega_nu"], v["Omega_m"], v["fb"], v["fc"],
    ], float)


def _run_case_single_mode(pure_gr: bool, tau: float, eta: float, mode_root: Path) -> tuple[dict, dict]:
    modes = []
    mode_rows = []
    for kh in base.K_H:
        path = _mode_path(mode_root, pure_gr, tau, eta, float(kh))
        reused = False
        if path.is_file():
            try:
                v = _load_mode(path, pure_gr, tau, eta, float(kh)); reused = True
            except Exception:
                path.unlink(missing_ok=True)
                v = _run_single_mode(eta, tau, pure_gr, float(kh)); _save_mode(path, v)
        else:
            v = _run_single_mode(eta, tau, pure_gr, float(kh)); _save_mode(path, v)
        modes.append(v)
        mode_rows.append({
            "k_h_Mpc": float(kh), "history_count": int(v["history_count"]),
            "reused": bool(reused), "cache": str(path),
        })
        print(
            f"STABLE_AEST_R12A_R02_MODE case={_case_name(pure_gr,tau,eta)} "
            f"k={float(kh):.5f} history_count={v['history_count']} reused={int(reused)}",
            flush=True,
        )

    ref = modes[0]
    bg_ref = _background_vector(ref)
    max_bg_rel = 0.0
    max_hconf_rel = 0.0
    bits = {int(v["bits"]) for v in modes}; pos = {int(v["target_pos"]) for v in modes}
    if len(bits) != 1 or len(pos) != 1:
        raise RuntimeError("single-mode case changed bits/target_pos across k")
    for v in modes[1:]:
        bg = _background_vector(v)
        denom = np.maximum(np.maximum(np.abs(bg_ref), np.abs(bg)), BG_ATOL)
        rel = float(np.max(np.abs(bg-bg_ref)/denom))
        max_bg_rel = max(max_bg_rel, rel)
        hc0 = np.asarray(ref["Hconf_Mpc_inv"], float); hc = np.asarray(v["Hconf_Mpc_inv"], float)
        hden = np.maximum(np.maximum(np.abs(hc0), np.abs(hc)), BG_ATOL)
        hrel = float(np.max(np.abs(hc-hc0)/hden))
        max_hconf_rel = max(max_hconf_rel, hrel)
        if not all(_bg_close(a,b) for a,b in zip(bg_ref,bg)) or not np.allclose(hc,hc0,rtol=BG_RTOL,atol=BG_ATOL):
            raise RuntimeError(
                f"background inconsistency across single-k computes: bg_rel={rel} Hconf_rel={hrel}"
            )

    rows = []
    for kh, v in zip(base.K_H, modes):
        row = {
            "requested_k_h_Mpc": float(kh),
            "reported_k_h_Mpc": float(kh),
            "reported_k_key": "single_requested_input_identity",
            "cubic": v["cubic"],
            "pchip": v["pchip"],
        }
        rows.append(row)

    case = {
        "pure_gr": bool(pure_gr), "tau_H0": float(tau), "eta": float(eta),
        "bits": int(ref["bits"]), "target_pos": int(ref["target_pos"]),
        "h": float(ref["h"]), "H0_Mpc_inv": float(ref["H0_Mpc_inv"]),
        "Omega_b": float(ref["Omega_b"]), "Omega_cdm": float(ref["Omega_cdm"]),
        "Omega_nu": float(ref["Omega_nu"]), "Omega_m": float(ref["Omega_m"]),
        "fb": float(ref["fb"]), "fc": float(ref["fc"]),
        # In Repair02 the mode identity is exact by one-input/one-history construction,
        # not by a measured returned-k metadata field.
        "max_k_match_error_h_Mpc": 0.0,
        "rows": rows,
    }
    audit = {
        "case": _case_name(pure_gr,tau,eta), "pure_gr": bool(pure_gr),
        "tau_H0": float(tau), "eta": float(eta), "n_modes": len(modes),
        "all_history_count_one": all(v["history_count"] == 1 for v in modes),
        "background_max_relative_difference": max_bg_rel,
        "Hconf_max_relative_difference": max_hconf_rel,
        "background_rtol": BG_RTOL, "background_atol": BG_ATOL,
        "modes": mode_rows,
    }
    return case, audit


def _write_identity_fail(path: Path, reason: str, audits: list[dict]) -> None:
    out = {
        "classification": FAIL_R02_IDENTITY,
        "diagnostic_complete": True,
        "science_evaluated": False,
        "gates": {
            "R12A_R02_G1_provenance_source": True,
            "R12A_R02_G2_single_mode_identity_coverage": False,
        },
        "reason": reason,
        "single_mode_audit": audits,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, indent=2, sort_keys=True)+"\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workdir", default="results/stable_aest_r12a_eg_work_repair02")
    ap.add_argument("--mode-workdir", default="results/stable_aest_r12a_eg_single_mode_repair02")
    ap.add_argument("--json-out", default="results/stable_aest_r12a_eg_weyl_growth_consistency_repair02.json")
    ap.add_argument("--npz-out", default="results/stable_aest_r12a_eg_weyl_growth_consistency_repair02.npz")
    args = ap.parse_args()

    work = Path(args.workdir); mode_root = Path(args.mode_workdir)
    work.mkdir(parents=True, exist_ok=True); mode_root.mkdir(parents=True, exist_ok=True)
    json_out = Path(args.json_out)

    print("STABLE_AEST_R12A_R02_START", flush=True)
    specs = [("gr", True, 10.0, 0.0)] + [
        (base._key(tau, eta), False, float(tau), float(eta))
        for tau in base.TAUS for eta in base.ETAS
    ]
    audits = []
    try:
        for name, pure, tau, eta in specs:
            case_path = work / f"{name}.npz"
            # Repair02 case artifacts are rebuilt only from the single-mode cache.
            # Existing aggregate files are validated by the frozen loader; invalid
            # aggregates are discarded and reconstructed.
            aggregate_ok = False
            if case_path.is_file():
                try:
                    base._load_case(case_path, pure, tau, eta)
                    aggregate_ok = True
                except Exception:
                    case_path.unlink(missing_ok=True)
            if aggregate_ok:
                # Still inspect/reconstruct the six single-mode audits so G2 is explicit.
                case, audit = _run_case_single_mode(pure, tau, eta, mode_root)
                base._save_case(case_path, case)
            else:
                case, audit = _run_case_single_mode(pure, tau, eta, mode_root)
                base._save_case(case_path, case)
            base._load_case(case_path, pure, tau, eta)
            audits.append(audit)
            print(
                f"STABLE_AEST_R12A_R02_CASE_READY name={name} "
                f"bg_rel={audit['background_max_relative_difference']:.3e} "
                f"Hconf_rel={audit['Hconf_max_relative_difference']:.3e}",
                flush=True,
            )
    except Exception as exc:
        _write_identity_fail(json_out, repr(exc), audits)
        print(f"STABLE_AEST_R12A_R02_IDENTITY_FAIL error={exc!r}", flush=True)
        print("STABLE_AEST_R12A_R02_CLASSIFICATION="+FAIL_R02_IDENTITY, flush=True)
        return 1

    g2 = bool(
        len(audits) == len(specs)
        and all(a["n_modes"] == len(base.K_H) and a["all_history_count_one"] for a in audits)
        and all(a["background_max_relative_difference"] <= max(BG_RTOL, BG_ATOL) for a in audits)
        and all(a["Hconf_max_relative_difference"] <= max(BG_RTOL, BG_ATOL) for a in audits)
    )
    if not g2:
        _write_identity_fail(json_out, "single-mode audit aggregate gate failed", audits)
        print("STABLE_AEST_R12A_R02_CLASSIFICATION="+FAIL_R02_IDENTITY, flush=True)
        return 1

    # Run the frozen R12a science engine entirely on the now-complete aggregate
    # case files. Because every expected case file exists and validates, base.main
    # must reuse them and cannot enter its historical multi-mode worker path.
    old_argv = list(sys.argv)
    try:
        sys.argv = [
            old_argv[0], "--workdir", str(work),
            "--json-out", str(json_out), "--npz-out", str(args.npz_out),
        ]
        code = int(base.main())
    finally:
        sys.argv = old_argv

    if not json_out.is_file():
        raise RuntimeError("frozen R12a science engine did not write JSON")
    result = json.loads(json_out.read_text())
    base_class = result.get("classification")
    result["repair02"] = {
        "prefit_lock": REPAIR02_PREFIT_LOCK,
        "repair01_runner_lock": REPAIR01_RUNNER_LOCK,
        "authoritative_r11a_repair02_lock": CORRECT_R11A_R02_POSTDATA_LOCK,
        "mode_identity_method": "one requested k per CLASS compute plus exactly one returned scalar history",
        "multi_mode_list_position_mapping_used": False,
        "returned_k_metadata_required": False,
        "single_mode_audit": audits,
        "R12A_R02_G2_single_mode_identity_coverage": True,
    }
    result.setdefault("gates", {})["R12A_R02_G2_single_mode_identity_coverage"] = True
    result["base_classification"] = base_class
    if code == 0 and base_class == base.CLS_PASS:
        result["classification"] = PASS_R02
        result["science_evaluated"] = True
    json_out.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")

    final_class = result.get("classification")
    print("STABLE_AEST_R12A_R02_SINGLE_MODE_GATE_PASS", flush=True)
    print("STABLE_AEST_R12A_R02_BASE_CLASSIFICATION="+str(base_class), flush=True)
    print("STABLE_AEST_R12A_R02_CLASSIFICATION="+str(final_class), flush=True)
    return 0 if final_class == PASS_R02 else code


if __name__ == "__main__":
    raise SystemExit(main())
