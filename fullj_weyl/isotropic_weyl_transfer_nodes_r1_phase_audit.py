#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import math
import subprocess
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]

ORIGINAL_PREDATA_LOCK = "b02960733256e27d4c1883a30031392c68a5cf74"
ORIGINAL_IMPLEMENTATION_LOCK = "9e78fb19e0aa7a554bd7a60b0cde18ff5c13fa80"
ORIGINAL_RUNNER_LOCK = "a4e26d29b4a8b6ceba67151aabe01db74406a93f"
HISTORICAL_FAIL_RESULT_LOCK = "b7bb0aef90ec935821f4dc1a63db0d79966a15f8"
R1_PREDATA_LOCK = "920ab2b610e5a74448d268375caeef8f881dc8c7"

PASS = "FULLJ_ISOTROPIC_WEYL_TRANSFER_NODES_R1_PHASE_AUDIT_PASS"
FAIL = "FULLJ_ISOTROPIC_WEYL_TRANSFER_NODES_R1_PHASE_AUDIT_FAIL"
INCOMPLETE = "FULLJ_ISOTROPIC_WEYL_TRANSFER_NODES_R1_PHASE_AUDIT_INCOMPLETE"
ORIGINAL_FAIL = "FULLJ_ISOTROPIC_WEYL_TRANSFER_NODES_FAIL"

PHASE_GATE = 1.0e-8
POWER_GATE = 1.0e-12
SEP_MED_GATE = 5.0e-4
SEP_MAX_GATE = 5.0e-3
LEAK_GATE = 5.0e-3
HOM_MED_GATE = 5.0e-4
HOM_MAX_GATE = 5.0e-3
GAUSS_MED_GATE = 5.0e-3
GAUSS_MAX_GATE = 2.0e-2
ALG_GATE = 1.0e-12


def git_head() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()


def is_ancestor(sha: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", sha, "HEAD"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-json", default="results/fullj_isotropic_weyl_transfer_nodes.json")
    ap.add_argument("--json-out", default="results/fullj_isotropic_weyl_transfer_nodes_r1_phase_audit.json")
    ap.add_argument("--csv-out", default="results/fullj_isotropic_weyl_transfer_nodes_r1_phase_audit.csv")
    args = ap.parse_args()

    locks = {
        "original_predata_lock": is_ancestor(ORIGINAL_PREDATA_LOCK),
        "original_implementation_lock": is_ancestor(ORIGINAL_IMPLEMENTATION_LOCK),
        "original_runner_lock": is_ancestor(ORIGINAL_RUNNER_LOCK),
        "historical_fail_result_lock": is_ancestor(HISTORICAL_FAIL_RESULT_LOCK),
        "r1_predata_lock": is_ancestor(R1_PREDATA_LOCK),
    }

    inp = ROOT / args.input_json
    jout = ROOT / args.json_out
    cout = ROOT / args.csv_out
    jout.parent.mkdir(parents=True, exist_ok=True)

    if not inp.exists():
        result = {
            "classification": INCOMPLETE,
            "diagnostic_complete": False,
            "reason": f"missing input {args.input_json}",
            "ancestry": locks,
        }
        jout.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print("FULLJ_ISO_TRANSFER_R1_PHASE_CLASSIFICATION=" + INCOMPLETE, flush=True)
        return 3

    raw = json.loads(inp.read_text())
    rows = raw.get("transfer_nodes", [])
    if len(rows) != 54:
        result = {
            "classification": INCOMPLETE,
            "diagnostic_complete": False,
            "reason": f"expected 54 transfer nodes, got {len(rows)}",
            "ancestry": locks,
        }
        jout.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print("FULLJ_ISO_TRANSFER_R1_PHASE_CLASSIFICATION=" + INCOMPLETE, flush=True)
        return 3

    T = np.asarray([complex(float(r["T_W_R2_real"]), float(r["T_W_R2_imag"])) for r in rows], complex)
    Ts = np.asarray([complex(float(r["single_mode_T_real"]), float(r["single_mode_T_imag"])) for r in rows], complex)

    eps_global = float(np.linalg.norm(np.imag(T)) / max(float(np.linalg.norm(T)), 1.0e-300))
    eps_single = float(np.linalg.norm(np.imag(Ts)) / max(float(np.linalg.norm(Ts)), 1.0e-300))
    abs_imag_max = float(np.max(np.abs(np.imag(T))))
    abs_imag_single_max = float(np.max(np.abs(np.imag(Ts))))

    p_complex = np.abs(T) ** 2
    p_real = np.real(T) ** 2
    p_rel = np.abs(p_complex - p_real) / np.maximum(p_complex, 1.0e-300)
    power_max = float(np.max(p_rel))
    power_median = float(np.median(p_rel))

    local_ratio = np.abs(np.imag(T)) / np.maximum(np.abs(T), 1.0e-300)
    iworst = int(np.argmax(local_ratio))
    worst = rows[iworst]

    original_gates = dict(raw.get("gates", {}))
    expected_keys = {
        "G1_provenance_setup",
        "G2_finite_constraint_health",
        "G3_initial_CLASS_normalization",
        "G4_transfer_phase_consistency",
        "G5_single_mode_separability",
        "G6_off_target_leakage",
        "G7_amplitude_homogeneity",
        "G8_gaussian_ensemble_reconstruction",
        "G9_discrete_power_node_sanity",
    }
    exactly_g4_failed = (
        set(original_gates) == expected_keys
        and original_gates.get("G4_transfer_phase_consistency") is False
        and all(original_gates.get(k) is True for k in expected_keys if k != "G4_transfer_phase_consistency")
    )

    summary0 = raw.get("summary", {})
    retained = {
        "separability_median": float(summary0.get("separability_median", math.inf)),
        "separability_max": float(summary0.get("separability_max", math.inf)),
        "off_target_leakage_max": float(summary0.get("off_target_leakage_max", math.inf)),
        "amplitude_homogeneity_median": float(summary0.get("amplitude_homogeneity_median", math.inf)),
        "amplitude_homogeneity_max": float(summary0.get("amplitude_homogeneity_max", math.inf)),
        "gaussian_ratio_reconstruction_median": float(summary0.get("gaussian_ratio_reconstruction_median", math.inf)),
        "gaussian_ratio_reconstruction_max": float(summary0.get("gaussian_ratio_reconstruction_max", math.inf)),
        "power_identity_relative_residual": float(summary0.get("power_identity_relative_residual", math.inf)),
    }

    g1 = bool(all(locks.values()) and raw.get("classification") == ORIGINAL_FAIL and exactly_g4_failed)
    g2 = bool(eps_global <= PHASE_GATE and eps_single <= PHASE_GATE)
    g3 = bool(abs_imag_max <= PHASE_GATE and abs_imag_single_max <= PHASE_GATE)
    g4 = bool(power_max <= POWER_GATE)
    g5 = bool(
        retained["separability_median"] <= SEP_MED_GATE
        and retained["separability_max"] <= SEP_MAX_GATE
        and retained["off_target_leakage_max"] <= LEAK_GATE
        and retained["amplitude_homogeneity_median"] <= HOM_MED_GATE
        and retained["amplitude_homogeneity_max"] <= HOM_MAX_GATE
        and retained["gaussian_ratio_reconstruction_median"] <= GAUSS_MED_GATE
        and retained["gaussian_ratio_reconstruction_max"] <= GAUSS_MAX_GATE
        and retained["power_identity_relative_residual"] <= ALG_GATE
    )

    gates = {
        "R1_G1_provenance_historical_state_lock": g1,
        "R1_G2_global_zero_safe_phase_consistency": g2,
        "R1_G3_absolute_quadrature_leakage": g3,
        "R1_G4_real_projection_power_contamination": g4,
        "R1_G5_retained_independent_validations": g5,
    }
    classification = PASS if all(gates.values()) else FAIL

    node_rows = []
    for r, t, ts, lr, pr in zip(rows, T, Ts, local_ratio, p_rel):
        node_rows.append({
            "z": float(r["z"]),
            "mode_n": int(r["mode_n"]),
            "k_h_Mpc_inv": float(r["k_h_Mpc_inv"]),
            "T_real": float(np.real(t)),
            "T_imag": float(np.imag(t)),
            "T_single_real": float(np.real(ts)),
            "T_single_imag": float(np.imag(ts)),
            "legacy_local_phase_ratio": float(lr),
            "real_projection_power_relative_change": float(pr),
        })

    summary = {
        "global_quadrature_relL2_multi": eps_global,
        "global_quadrature_relL2_single": eps_single,
        "absolute_imaginary_max_multi": abs_imag_max,
        "absolute_imaginary_max_single": abs_imag_single_max,
        "real_projection_power_change_max": power_max,
        "real_projection_power_change_median": power_median,
        "legacy_local_phase_ratio_max": float(local_ratio[iworst]),
        "legacy_worst_cell": {
            "z": float(worst["z"]),
            "mode_n": int(worst["mode_n"]),
            "T_real": float(np.real(T[iworst])),
            "T_imag": float(np.imag(T[iworst])),
        },
    }

    result = {
        "classification": classification,
        "diagnostic_complete": True,
        "git_head": git_head(),
        "ancestry": locks,
        "historical_original_classification": raw.get("classification"),
        "historical_original_gates": original_gates,
        "gates": gates,
        "summary": summary,
        "retained_original_summary": retained,
        "nodes": node_rows,
        "HISTORICAL_ORIGINAL_FAIL_PRESERVED": True,
        "REAL_TRANSFER_PROJECTION_LICENSED": bool(classification == PASS),
        "THREE_D_ISOTROPIC_WEYL_TRANSFER_NODES_LICENSED": bool(classification == PASS),
        "THREE_D_ISOTROPIC_WEYL_POWER_NODES_LICENSED": bool(classification == PASS),
        "THREE_D_CONTINUOUS_WEYL_POWER_LICENSED": False,
        "EVOLVING_WEYL_POWER_LICENSED": False,
        "ACT_LIKELIHOOD_LICENSED": False,
        "OBSERVATIONAL_CLAIM_LICENSED": False,
        "scope": "post-failure zero-safe phase audit of the already completed six-node transfer result; no rerun, fitting, interpolation, or threshold relaxation",
    }
    jout.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")

    with cout.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(node_rows[0].keys()))
        w.writeheader()
        w.writerows(node_rows)

    print("FULLJ_ISO_TRANSFER_R1_PHASE_SUMMARY=" + json.dumps(summary, sort_keys=True), flush=True)
    print("FULLJ_ISO_TRANSFER_R1_PHASE_GATES=" + json.dumps(gates, sort_keys=True), flush=True)
    print("FULLJ_ISO_TRANSFER_R1_PHASE_CLASSIFICATION=" + classification, flush=True)
    print("HISTORICAL_ORIGINAL_FAIL_PRESERVED=True", flush=True)
    print("REAL_TRANSFER_PROJECTION_LICENSED=" + str(bool(classification == PASS)), flush=True)
    print("THREE_D_ISOTROPIC_WEYL_TRANSFER_NODES_LICENSED=" + str(bool(classification == PASS)), flush=True)
    print("THREE_D_ISOTROPIC_WEYL_POWER_NODES_LICENSED=" + str(bool(classification == PASS)), flush=True)
    print("THREE_D_CONTINUOUS_WEYL_POWER_LICENSED=False", flush=True)
    print("EVOLVING_WEYL_POWER_LICENSED=False", flush=True)
    print("ACT_LIKELIHOOD_LICENSED=False", flush=True)
    print("OBSERVATIONAL_CLAIM_LICENSED=False", flush=True)
    print("FULLJ_ISO_TRANSFER_R1_PHASE_JSON=" + args.json_out, flush=True)
    print("FULLJ_ISO_TRANSFER_R1_PHASE_CSV=" + args.csv_out, flush=True)
    return 0 if classification == PASS else 2


if __name__ == "__main__":
    raise SystemExit(main())
